from django.contrib.auth.models import User
from rest_framework import generics
from rest_framework.permissions import AllowAny, IsAuthenticated
from .models import Photo

from .serializers import RegisterSerializer, PhotoSerializer


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer


class PhotoLoad(generics.CreateAPIView):
    queryset = Photo.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = PhotoSerializer
