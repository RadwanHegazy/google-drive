from uuid import uuid4
from rest_framework_simplejwt.tokens import AccessToken
from django.contrib.auth import get_user_model

User = get_user_model()

def create_user (
    email=None,
    full_name="Test",
    password='123'
)   :
    return User.objects.create_user(
        email=email or f"{uuid4()}@gmail.com",
        full_name = full_name,
        password=password
    )

def create_access_token(user=None) : 
    user = user or create_user()
    return AccessToken.for_user(user=user)

def create_headers(user=None):
    access_token = create_access_token(user)
    return {
        'Authorization' : F"Bearer {access_token}"
    }