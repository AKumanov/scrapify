from django.contrib.auth.base_user import AbstractBaseUser
from django.db import models
from django.contrib.auth.models import User, PermissionsMixin
import uuid

from .managers import CustomUserManager

"""
1. Create a model extending AbstractBaseUser and PermissionsMixin
    - AbstractBaseUser holds info about user's password
    - PermissionsMixin - user permissions and permission groups
2. Register model as authentication model in ../settings.py
3. Create user manager

4. Create model that is linked to the custom auth model via one-to-one connection
"""

class BaseUser(AbstractBaseUser, PermissionsMixin):
    uid = models.UUIDField(
        unique=True,
        editable=False,
        default=uuid.uuid4,
        verbose_name='Company identifier'
    )
    email = models.EmailField(unique=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    is_staff = models.BooleanField(default=False)

    # using email as authentication field instead of default username
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email

class CustomUser(models.Model):
    __FIRST_NAME_MAX_LENGTH = 30
    __LAST_NAME_MAX_LENGTH = 50
    
    first_name = models.CharField(
        max_length=__FIRST_NAME_MAX_LENGTH
    )
    last_name = models.CharField(
        max_length=__LAST_NAME_MAX_LENGTH
    )
    user = models.OneToOneField(
        BaseUser,
        on_delete=models.CASCADE,
        primary_key=True
    )

    def __str__(self):
        return '{} {}'.format(self.first_name, self.last_name)
