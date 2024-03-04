from rest_framework import serializers
from .models import User
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from .utils import generate_token, is_token_valid, CustomValidation
from django.conf import settings
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.utils import timezone
from rest_framework import status
from django.contrib.auth.hashers import check_password

# user serializer create
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'username',
            'first_name',
            'last_name',
            'email',
            'phone_number',
            'password',
            'profile_photo'
        )

        extra_kwargs = {
            'password': {'write_only': True},
            'profile_photo': {'required': False}
        }

# update user serializer update
class UpdateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'username',
            'first_name',
            'last_name',
            'email',
            'phone_number',
            'profile_photo'
        )

        extra_kwargs = {
            'profile_photo': {'required': False},
            'email': {'read_only':True}
        }

# serializer for user email account verification  
class ActivationSerializer(serializers.Serializer):
    uid = serializers.CharField(required=True, max_length=10)
    token = serializers.CharField(required=True, max_length=255)


# serializer for resend email activation/verification link
class ResendActivationSerializer(serializers.Serializer):
    email = serializers.EmailField()


# forgot password serializer
class ForgotPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def create(self, validated_data):
        email = validated_data['email']

        try:
            user = User.objects.get(email=email)
        except:
            user = None
        
        if user is None:
            raise CustomValidation("user with that email does not exist", "email", status.HTTP_400_BAD_REQUEST)
        
        if not user.is_active:
            raise CustomValidation("your account email is not verified or your account may be blocked. Please verifiy your email or contact the system admin for your account to be unblocked.", "account", status.HTTP_400_BAD_REQUEST) 

  
        


class ResetPasswordSerializer(serializers.Serializer):
    uid = serializers.CharField(required=True, max_length=10)
    token = serializers.CharField(required=True, max_length=255)
    password = serializers.CharField(required=True, max_length=200, write_only=True)

    def create(self, validated_data):
        uid = validated_data['uid']
        token = validated_data['token']
        password = validated_data['password']

        #get the current user from the uid encoded string
        try:
            uid = force_str(urlsafe_base64_decode(uid))
            user = User.objects.get(pk=uid)
        except:
            user = None
            raise CustomValidation("the link you clicked on is not valid", "link", status.HTTP_400_BAD_REQUEST)
        
        if not user.is_active:
            raise CustomValidation("your email account is not verified or is blocked. Please verify your email or contact the system admin to unblock your account", "email", status.HTTP_400_BAD_REQUEST)

        if user.reset_password_link_expires_at is not None and timezone.now() > user.reset_password_link_expires_at:
            raise CustomValidation("the link you clicked on has expired", "link", status.HTTP_400_BAD_REQUEST)
        else:
            if is_token_valid(user, token):
                user.set_password(password)
                user.save()
            else:
                raise CustomValidation("the link you clicked on is not valid", "link", status.HTTP_400_BAD_REQUEST)

        return validated_data


class ChangePasswordSerializer(serializers.Serializer):
    current_password = serializers.CharField(max_length=200, write_only=True)
    new_password = serializers.CharField(max_length=200, write_only=True)

    def create(self, validated_data):
        entered_current_password = validated_data['current_password']
        new_password = validated_data['new_password']

        # get the current user from the request object
        user = self.context['request'].user

        # get current user password
        user_password = user.password
        
        # check the current password entered is correct
        is_correct_password = check_password(entered_current_password,user_password)


        # 
        if not is_correct_password:
            raise CustomValidation("current password entered is not correct", "current_password", status.HTTP_400_BAD_REQUEST)
        
        if len(new_password) < 8:
            raise CustomValidation("password should be atleast 8 characters long", "new_password", status.HTTP_400_BAD_REQUEST)

        user.set_password(new_password)
        user.save()

        return validated_data



        