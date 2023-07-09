from rest_framework import serializers
from .models import User
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from .utils import generate_token
from django.conf import settings
from django.template.loader import render_to_string
from django.core.mail import EmailMessage

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


        # send an activation link to the user
        token = generate_token(user)
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        username = user.username
        email = user.email
        frontend_base_url = settings.FRONTEND_BASE_URL
        email_subject = "Verify Email To Activate Your Account"
        email_body = render_to_string('authentication/activation_email.html',
        {
            'username':username,
            'uid':uid,
            'token': token,
            'frontend_base_url': frontend_base_url 
        })

        email_message = EmailMessage(
                    email_subject,
                    email_body,
                    settings.EMAIL_HOST_USER,
                    [email]
                )
        email_message.send()

        return user

    



