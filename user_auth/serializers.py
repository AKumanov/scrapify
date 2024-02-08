from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from .models import BaseUser, CustomUser

UserModel = get_user_model()

class ErrorHandler:
    """
    reusable class to store different error messages
    """
    _INVALID_PASSWORD1_ERROR_MESSAGE = "Password fields didn't match."
    _INVALID_PASSWORD2_ERROR_MESSAGE = "Old password is not correct."
    _AUTHORIZATION_ERROR = "You don't have permission for this user!"
    _EMAIL_EXISTS_ERROR_MESSAGE = "This email is already in use."
    _USERNAME_EXISTS_ERROR_MESSAGE = "Username is taken."

class RegisterSerializer(serializers.ModelSerializer, ErrorHandler):
    """
    The Open-Closed Principle (OCP) states that software entities (classes, modules, methods, ect.)
    should be open for extension, but closed for modification.
    In practice, this means creating software entities whose behavior can be changed
    without the need to edit and recompile the code itself.
    """
    email = serializers.EmailField(
        required=True,
    )
    first_name = serializers.CharField(
        write_only=True,
        max_length=30,
    )
    last_name = serializers.CharField(
        write_only=True,
        max_length=50
    )
    password = serializers.CharField(
        write_only=True,
        required=True,
        validators=[validate_password]
    )
    confirm_password = serializers.CharField(
        label='Confirm Password',
        write_only=True,
        required=True
    )

    class Meta:
        model = CustomUser

        fields = ('email', 'password', 'confirm_password', 'first_name', 'last_name')
        extra_kwargs = {
            'first_name': {
                'required': True
            },
            'last_name': {
                'required': True
            },
        }
    
    @staticmethod
    def validate_email(value):
        """

        :param value: passed email
        validates if the email is not use already by another user

        :return: email if valid else throws error
        """
        custom_user = BaseUser.objects.filter(email__exact=value)
        if len(custom_user) != 0:
            raise serializers.ValidationError({
                'email': ErrorHandler._EMAIL_EXISTS_ERROR_MESSAGE
            })
        return value

    def validate(self, attrs):
        """

        :param attrs:  'username', 'password', 'confirm_password', 'email', 'first_name', 'last_name'
        checks if password and confirm passwords are matching
        :return: the body of the post request is passwords are matching, else throws error
        """
        if attrs['password'] != attrs['confirm_password']:
            raise serializers.ValidationError({
                'password': ErrorHandler._INVALID_PASSWORD1_ERROR_MESSAGE
            })
        return attrs

    def create(self, validated_data):
        """

        :param validated_data: data from post request
        :return: newly created user with valid data
        """
        user = UserModel.objects.create(
            email=validated_data['email']
        )
        print('USER IS CREATED: ')
        print(user)        
        user.set_password(validated_data['password'])
        user.is_staff = False
        user.save()

        custom_user = CustomUser.objects.create(
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            user=user
        )

        custom_user.save()
        return user

class ChangePasswordSerializer(serializers.ModelSerializer, ErrorHandler):
    """
    Serializer dealing only with the change password endpoint
    showing old user password, new password and confirm password fields
    All field validation is done as overidden class methods
    """
    password = serializers.CharField(
        write_only=True,
        required=True,
        validators=[validate_password]
    )
    confirm_password = serializers.CharField(
        write_only=True,
        required=True
    )
    old_password = serializers.CharField(
        write_only=True,
        required=True
    )

    class Meta:
        model = UserModel
        fields = ('old_password', 'password', 'confirm_password')

    def validate(self, attrs):
        if attrs.get('password') != attrs.get('confirm_password'):
            raise serializers.ValidationError({
                'password': "{}".format(ErrorHandler._INVALID_PASSWORD1_ERROR_MESSAGE)
            })
        return attrs

    def validate_old_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError({
                'old_password': "{}".format(ErrorHandler._INVALID_PASSWORD2_ERROR_MESSAGE)
            })
        return value

    def update(self, instance, validated_data):
        """

        :param instance: current user
        :param validated_data: passed data from PUT request
        checks if the current user is the one, matching the id from url param
        changes password if data is valid, else throws authorization error
        :return:
        """
        user = self.context['request'].user

        if user.pk != instance.pk:
            raise serializers.ValidationError({
                'authorize': '{}'.format(ErrorHandler._AUTHORIZATION_ERROR)
            })
        instance.set_password(validated_data.get('password'))
        instance.save()

        return instance
    
class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['email'] = user.email
        return token
    
    def validate(self, attrs):
        data = super().validate(attrs)
        data['email'] = self.user.email
        data['token'] = str(data.pop('access'))
        return data