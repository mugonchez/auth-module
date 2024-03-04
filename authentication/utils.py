from django.contrib.auth.tokens import default_token_generator
from rest_framework.exceptions import APIException
from django.utils.encoding import force_str
from rest_framework import status
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.utils import timezone
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.conf import settings

# Generate a token for a user
def generate_token(user):
    token = default_token_generator.make_token(user)
    return token

# Check if a token is valid for a user
def is_token_valid(user, token):
    return default_token_generator.check_token(user, token)


class CustomValidation(APIException):
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    default_detail = 'A server error occurred.'

    def __init__(self, detail, field, status_code):
        if status_code is not None:self.status_code = status_code
        if detail is not None:
            self.detail = {field: force_str(detail)}
        else: self.detail = {'detail': force_str(self.default_detail)}



def send_registration_email(user):
    #send an activation link to the user
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

def send_activation_email(user):
    pass





