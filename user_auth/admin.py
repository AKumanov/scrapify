from django.contrib import admin
from .models import CustomUser
from django.contrib.auth import get_user_model

UserModel = get_user_model()

# Register your models here.
admin.site.register(UserModel)