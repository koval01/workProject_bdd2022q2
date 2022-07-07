from rest_framework import generics
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from .models import Photo, CustomUser as User
from .permissions import IsObjectOwner, IsMyProfile

from .serializers import RegisterSerializer, PhotoSerializer, UserSerializer


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer


class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    permission_classes = (IsAuthenticated, IsAdminUser)
    serializer_class = UserSerializer


class UserDetail(generics.RetrieveAPIView):
    queryset = User.objects.all()
    permission_classes = (IsAuthenticated, IsMyProfile)
    serializer_class = UserSerializer


class PhotoList(generics.ListCreateAPIView):
    def get_queryset(self):
        """
        This view should return a list of all the images
        for the currently authenticated user.
        """
        user = self.request.user
        return Photo.objects.filter(creator=user)

    permission_classes = (IsAuthenticated,)
    serializer_class = PhotoSerializer

    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)


class PhotoDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Photo.objects.all()
    permission_classes = (IsAuthenticated, IsObjectOwner)
    serializer_class = PhotoSerializer
