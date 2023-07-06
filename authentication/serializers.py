from rest_framework import serializers
from .models import User
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


# user serializer
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'username',
            'first_name',
            'last_name',
            'email',
            'phone_number',
            'password' 
        )

        extra_kwargs = {
            'password': {'write_only': True}
        }
    
    def validate_phone_number(self, value):
        user = User.objects.filter(phone_number=value)
        if user.exists():
            raise serializers.ValidationError("user with this phone number already exists")
        return value
    

    # create user from validated data
    def create(self, validated_data):
        username = validated_data['username']
        first_name = validated_data['first_name']
        last_name = validated_data['last_name']
        email = validated_data['email']
        password = validated_data['password']
        phone_number = validated_data['phone_number']


        user = User.objects.create_user(username=username, 
                                        first_name=first_name, 
                                        last_name=last_name, 
                                        email=email, 
                                        password=password, 
                                        phone_number=phone_number)
        # deactivate user 
        user.is_active = False
        user.save()
        return user


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super(CustomTokenObtainPairSerializer, cls).get_token(user)

        # Add custom claims
        return token
    



