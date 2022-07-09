from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .views import RegisterView, UserList, UserDetail, PhotoList, PhotoDetail

urlpatterns = [
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api-token-auth/', obtain_auth_token, name='api_token_auth'),
    path('register/', RegisterView.as_view(), name='auth_register'),
    path('users/', UserList.as_view(), name='users_list'),
    path('users/<int:pk>/', UserDetail.as_view(), name='user_details'),
    path('images/', PhotoList.as_view(), name='images_list'),
    path('images/<int:pk>/', PhotoDetail.as_view(), name='image_details'),
]

urlpatterns = format_suffix_patterns(urlpatterns)
