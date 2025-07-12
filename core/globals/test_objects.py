from uuid import uuid4
from rest_framework_simplejwt.tokens import AccessToken
from django.contrib.auth import get_user_model
from plan.models import StoragePlan

User = get_user_model()

def create_user (
    email=None,
    full_name="Test",
    password='123',
    is_superuser = False,
    is_staff = False
)   :
    return User.objects.create_user(
        email=email or f"{uuid4()}@gmail.com",
        full_name = full_name,
        password=password,
        is_superuser = is_superuser,
        is_staff = is_staff
    )

def create_access_token(user=None) : 
    user = user or create_user()
    return AccessToken.for_user(user=user)

def create_headers(user=None):
    access_token = create_access_token(user)
    return {
        'Authorization' : F"Bearer {access_token}"
    }

def create_storage_plan (
    name = "Test",
    storage_in_giga = 10,
    price_per_month = 10.5,
    price_per_year = 3.5
) : 
    return StoragePlan.objects.create(
        name = name,
        storage_in_giga = storage_in_giga,
        price_per_month = price_per_month,
        price_per_year = price_per_year
    )