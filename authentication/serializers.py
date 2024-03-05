from rest_framework import serializers
from .models import User
from .utils import generate_token, is_token_valid, CustomValidation
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


# reset password serializer
class ResetPasswordSerializer(serializers.Serializer):
    uid = serializers.CharField(required=True, max_length=10)
    token = serializers.CharField(required=True, max_length=255)
    password = serializers.CharField(required=True, max_length=200, write_only=True)


# change password serializer
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



        