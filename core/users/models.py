from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager

class UserManager (BaseUserManager) : 

    def create_user(self, password, **kwargs) : 
        user = self.model(**kwargs)
        user.set_password(password)
        user.save()
        return user
    
    def create_superuser(self, **kwargs) : 
        kwargs['is_superuser'] = True
        kwargs['is_staff'] = True
        return self.create_user(**kwargs)

class User (AbstractUser) : 
    objects = UserManager()

    user_permissions = None
    groups = None
    username = None
    first_name = None
    last_name = None

    full_name = models.CharField(max_length=225)
    email = models.EmailField(unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['full_name']

    def __str__(self):
        return self.full_name
    
