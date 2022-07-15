from abc import ABC

from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from .models import Photo, CustomUser as User


class ThumbnailsField(serializers.Field, ABC):

    def __init__(self, *args, **kwargs):
        kwargs['read_only'] = True
        super().__init__(*args, **kwargs)

    def to_representation(self, value):
        request = self.context.get('request')
        ret = {
            "thumbnail_200": request.build_absolute_uri(value.thumbnail_200.url),
            "thumbnail_400": request.build_absolute_uri(value.thumbnail_400.url)
        }
        return ret


class PhotoSerializer(serializers.ModelSerializer):
    creator = serializers.ReadOnlyField(source='creator.username')
    thumbnails = ThumbnailsField(source='*')

    class Meta:
        model = Photo
        fields = (
            'id', 'name', 'image', 'thumbnails',
            'creator', 'created_at')

    def to_representation(self, instance):
        user = None
        request = self.context.get("request")
        if request and hasattr(request, "user"):
            user = request.user

        representation = super().to_representation(instance)
        paid_customer_types = [v[0] for v in User.CUSTOMER_TYPE if v[0] != "basic"]
        if (user.customer_type not in paid_customer_types) and (not user.is_superuser):
            del representation["image"]
            del representation["thumbnails"]["thumbnail_400"]
        if user.customer_type == "enterprise":
            representation["binary_image"] = "soon"
        return representation


class UserSerializer(serializers.ModelSerializer):
    photos = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = User
        fields = [
            'id', 'username', 'email', 'is_active', 'is_staff',
            'customer_type', 'photos'
        ]


class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )

    password = serializers.CharField(
        write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(
        write_only=True, required=True)

    class Meta:
        model = User
        fields = (
            'username', 'password', 'password2',
            'email', 'first_name', 'last_name'
        )

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError(
                {"password": "Password fields didn't match."})

        return attrs

    def create(self, validated_data):
        del validated_data['password2']
        user = User.objects.create(**validated_data)

        user.set_password(validated_data['password'])
        user.save()

        return user
