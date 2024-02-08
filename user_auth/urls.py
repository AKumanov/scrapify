from django.urls import path
from rest_framework.response import Response
from rest_framework.authtoken.views import ObtainAuthToken, Token
from .views import RegisterView, LogoutView, LogoutAllView, ChangePasswordView, CustomTokenObtainPairView
from rest_framework_simplejwt.views import TokenRefreshView, TokenObtainPairView


urlpatterns = [
    path('register/', RegisterView.as_view(), name='auth_register'),
    path('login/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('logout_all/', LogoutAllView.as_view(), name='logout_all'),
    path('change_password/<int:pk>/', ChangePasswordView.as_view(), name='change_password'),
]