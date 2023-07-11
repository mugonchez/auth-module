from django.contrib.auth.tokens import default_token_generator
from rest_framework.exceptions import APIException
from django.utils.encoding import force_str
from rest_framework import status

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




