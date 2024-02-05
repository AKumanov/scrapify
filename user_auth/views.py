from django.contrib.auth.models import User
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated

from .models import CustomUser, BaseUser
from .serializers import RegisterSerializer

class RegisterView(generics.CreateAPIView):
    queryset = BaseUser.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer