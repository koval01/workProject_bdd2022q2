import copy
import sys
import uuid
from io import BytesIO

from PIL import Image
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.db import models


class CustomUserManager(BaseUserManager):
    def create_user(self, username, email, password=None):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not username:
            raise ValueError('Users must have a username')
        if not email:
            raise ValueError('Users must have an email address')
        if not password:
            raise ValueError('Users must have an password')

        user = self.model(
            username=username,
            email=self.normalize_email(email)
        )

        user.set_password(password)
        user.is_active = True
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password=None):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(
            username,
            password=password,
            email=email
        )
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class CustomUser(AbstractUser):
    # user = models.OneToOneField(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = CustomUserManager()

    CUSTOMER_TYPE = [
        ('basic', 'Basic'),
        ('premium', 'Premium'),
        ('enterprise', 'Enterprise'),
    ]
    customer_type = models.CharField(
        default='basic', choices=CUSTOMER_TYPE, null=False, max_length=16)

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        """Does the user have a specific permission?"""
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        """Does the user have permissions to view the app `app_label`?"""
        # Simplest possible answer: Yes, always
        return True


def get_file_path(instance, filename):
    ext = filename.split('.')[-1]
    return "%s.%s" % (uuid.uuid4(), ext)


def build_thumbnail(_image: Image, _height: int = 200) -> BytesIO:
    _image = copy.deepcopy(_image)
    new_width = int(_height / _image.height * _image.width)
    _image = _image.resize((new_width, _height))

    output = BytesIO()

    _image.save(output, format='JPEG', quality=95)
    output.seek(0)

    return output


class Photo(models.Model):
    name = models.CharField(max_length=255)
    image = models.ImageField(upload_to=get_file_path, null=False)
    thumbnail_200 = models.ImageField(upload_to=get_file_path, editable=False, null=True)
    thumbnail_400 = models.ImageField(upload_to=get_file_path, editable=False, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    creator = models.ForeignKey('rest_module.CustomUser', related_name='photos', on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        im = Image.open(self.image)
        im = im.convert('RGB')

        output = BytesIO()

        im.save(output, format='JPEG', quality=60)
        output.seek(0)

        def _save_image(_output: BytesIO) -> InMemoryUploadedFile:
            return InMemoryUploadedFile(
                _output, 'ImageField', "%s.jpg" % self.image.name.split('.')[0],
                'image/jpeg',
                sys.getsizeof(output), None)

        self.image = _save_image(output)

        self.thumbnail_200 = _save_image(build_thumbnail(im, _height=200))
        self.thumbnail_400 = _save_image(build_thumbnail(im, _height=400))

        super(Photo, self).save()

    def __str__(self):
        return f"{self.creator} | {self.id} - {self.name}"

    class Meta:
        ordering = ['-id']
