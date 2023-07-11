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
            raise CustomValidation("a user with this phone number already exists", "phone_number", status.HTTP_400_BAD_REQUEST)
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

        # update email expiry field of the user model
        user.activation_link_expires_at = timezone.now() + timezone.timedelta(days=1)
        user.save()

        return user


# serializer for user email account verification  
class ActivationSerializer(serializers.Serializer):
    uid = serializers.CharField(required=True, max_length=10)
    token = serializers.CharField(required=True, max_length=255)

    def create(self, validated_data):
        uid = validated_data['uid']
        token = validated_data['token']

        #get the current user from the uid encoded string
        try:
            uid = force_str(urlsafe_base64_decode(uid))
            user = User.objects.get(pk=uid)
        except:
            user = None
            raise CustomValidation("the link you clicked on is not valid", "link", status.HTTP_400_BAD_REQUEST)
        
        if user.is_active:
            raise CustomValidation("this email account has already been verified", "email", status.HTTP_400_BAD_REQUEST)

        if user.activation_link_expires_at is not None and timezone.now() > user.activation_link_expires_at:
            raise CustomValidation("the link you clicked on has expired", "link", status.HTTP_400_BAD_REQUEST)
        else:
            if is_token_valid(user, token):
                user.is_active = True
                user.save()
            else:
                raise CustomValidation("The link you clicked on is not valid", "link", status.HTTP_400_BAD_REQUEST)

        return validated_data

# serializer for resend email activation/verification link
class ResendActivationSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def create(self, validated_data):
        email = validated_data['email']

        try:
            user = User.objects.get(email=email)
        except:
            user = None
        
        if user is None:
            raise CustomValidation("user with that email does not exist", "email", status.HTTP_400_BAD_REQUEST)
        
        if user.is_active:
            raise CustomValidation("user with that email address is already verified", "email", status.HTTP_400_BAD_REQUEST) 
        

        """
        user exists and account is inactive
        send an activation link to the user
        """
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

        # update email expiry field of the user model
        user.activation_link_expires_at = timezone.now() + timezone.timedelta(days=1)
        user.save()

        return validated_data


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
            raise CustomValidation("Your account email is not verified or your account may be blocked. Please verifiy your email or contact the system admin for your account to be unblocked.", "account", status.HTTP_400_BAD_REQUEST) 

        """
        user is active, send the forgot password link
        """
        token = generate_token(user)
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        username = user.username
        email = user.email
        frontend_base_url = settings.FRONTEND_BASE_URL
        email_subject = "Reset Your Password"
        email_body = render_to_string('authentication/forgot_password_email.html',
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

        # update email expiry field of the user model
        user.reset_password_link_expires_at = timezone.now() + timezone.timedelta(days=1)
        user.save()

        return validated_data
        


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
            raise CustomValidation("Your email account is not verified or is blocked. Please verify your email or contact the system admin to unblock your account", "email", status.HTTP_400_BAD_REQUEST)

        if user.reset_password_link_expires_at is not None and timezone.now() > user.reset_password_link_expires_at:
            raise CustomValidation("the link you clicked on has expired", "link", status.HTTP_400_BAD_REQUEST)
        else:
            if is_token_valid(user, token):
                user.set_password(password)
                user.save()
            else:
                raise CustomValidation("The link you clicked on is not valid", "link", status.HTTP_400_BAD_REQUEST)

        return validated_data
