from django.contrib.auth.tokens import default_token_generator

# Generate a token for a user
def generate_token(user):
    token = default_token_generator.make_token(user)
    return token

# Check if a token is valid for a user
def is_token_valid(user, token):
    return default_token_generator.check_token(user, token)







