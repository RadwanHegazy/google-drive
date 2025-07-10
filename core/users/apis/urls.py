from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from django.urls import path
from .views import (
    profile,
    register
)

urlpatterns = [
    path('auth/login/v1/', TokenObtainPairView.as_view(), name='login'),
    path('auth/refresh/v1/', TokenRefreshView.as_view(), name='refresh-token'),
    path('auth/register/v1/', register.UserRegisterAPI.as_view(), name='register'),
    path('profile/v1/', profile.UserProfileAPI.as_view(), name='profile'),

]