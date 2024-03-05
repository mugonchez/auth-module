from rest_framework import serializers
from .models import User

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
    
    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user

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



        