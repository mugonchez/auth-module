from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_str
from django.utils import timezone
from django.contrib.auth.hashers import check_password
from rest_framework.decorators import api_view, permission_classes, parser_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated


from .serializers import (
    UserSerializer, 
    ResendActivationSerializer,
    ActivationSerializer,
    ForgotPasswordSerializer,
    ResetPasswordSerializer,
    ChangePasswordSerializer,
    UpdateUserSerializer
)
from .models import User
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from .models import User
from .utils import is_token_valid, send_activation_email, send_reset_email



# Create your views here.
@api_view(['POST'])
def register_user(request):
    """
    register user api view.
    """
    if request.method == 'POST':
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            # send email to user upon successful registration
            send_activation_email(user)
            return Response({'message': 'User registered successfully. Verification email sent.'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    return Response({"error": "Only POST requests are allowed"},status=status.HTTP_405_METHOD_NOT_ALLOWED)


@api_view(['POST'])
def activate(request):
    """
    activate account api view
    """
    if request.method == 'POST':
        serializer = ActivationSerializer(data=request.data)
        if serializer.is_valid():
            uid = serializer.validated_data.get('uid')
            token = serializer.validated_data.get('token')

            # Decode UID and retrieve user
            try:
                uid = force_str(urlsafe_base64_decode(uid))
                user = User.objects.get(pk=uid)
            except (TypeError, ValueError, OverflowError, User.DoesNotExist):
                user = None

            # Handle user not found
            if user is None:
                return Response({"error": "Invalid activation link"}, status=status.HTTP_400_BAD_REQUEST)
            
            # Check if user is already active
            if user.is_active:
                return Response({"error": "User account already active"}, status=status.HTTP_403_FORBIDDEN) 

            # Check activation link expiration
            if user.activation_link_expires_at is not None and timezone.now() > user.activation_link_expires_at:
                return Response({"error": "Activation link has expired"}, status=status.HTTP_403_FORBIDDEN)
        
            # Check token validity and activate user
            if is_token_valid(user, token):
                user.is_active = True
                user.save()
                return Response({"message": "User activated successfully"}, status=status.HTTP_204_NO_CONTENT)
        
        return Response({"error": "Invalid activation link"}, status=status.HTTP_400_BAD_REQUEST)
    


@api_view(['POST'])
def resend_activation(request):
    """
    Resend activation API view
    """
    if request.method == 'POST':
        serializer = ResendActivationSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data.get('email')
            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                return Response({"error": "User with that email does not exist"}, status=status.HTTP_404_NOT_FOUND)
            
            if user.is_active:
                return Response({"error": "User with that email is already verified"}, status=status.HTTP_403_FORBIDDEN)
            
            send_activation_email(user)
            return Response(status=status.HTTP_204_NO_CONTENT)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)


@api_view(['POST'])
def forgot_password(request):
    """
    forgot password api view
    """
    if request.method == 'POST':
        serializer = ForgotPasswordSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data.get('email')
            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                return Response({"error": "User with that email does not exist"}, status=status.HTTP_404_NOT_FOUND)
            
            if not user.is_active:
                return Response({"error": "Kindly verify your email address before proceeding"}, status=status.HTTP_403_FORBIDDEN)
            send_reset_email(user)
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)


@api_view(['POST'])
def reset_password(request):
    """
    reset password api view
    """
    if request.method == 'POST':
        serializer = ResetPasswordSerializer(data=request.data)
        if serializer.is_valid():
            uid = serializer.validated_data.get('uid')
            token = serializer.validated_data.get('token')
            password = serializer.validated_data.get('password')

            # Decode UID and retrieve user
            try:
                uid = force_str(urlsafe_base64_decode(uid))
                user = User.objects.get(pk=uid)
            except (TypeError, ValueError, OverflowError, User.DoesNotExist):
                user = None

            # Handle user not found
            if user is None:
                return Response({"error": "Invalid reset link"}, status=status.HTTP_400_BAD_REQUEST)
            
            # Check if user is already active
            if not user.is_active:
                return Response({"error": "User account not active or account email not verified"}, status=status.HTTP_403_FORBIDDEN) 

            # Check activation link expiration
            if user.reset_password_link_expires_at is not None and timezone.now() > user.reset_password_link_expires_at:
                return Response({"error": "Reset password link has expired"}, status=status.HTTP_403_FORBIDDEN)
        
            # Check token validity and activate user
            if is_token_valid(user, token):
                user.set_password(password)
                user.save()
                return Response({"message": "Password reset successfully"}, status=status.HTTP_204_NO_CONTENT)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)



@api_view(['POST'])
@permission_classes([IsAuthenticated])
def change_password(request):
    """
    change password api view
    """
    if request.method == 'POST':
        serializer = ChangePasswordSerializer(data=request.data)
        if serializer.is_valid():
            current_password = serializer.validated_data.get('current_password')
            new_password = serializer.validated_data.get('new_password')

            user = request.user

            # password from database
            user_password = user.password

            is_correct_password = check_password(current_password, user_password)

            if not is_correct_password:
                return Response({"error": "Current password is not correct"}, status=status.HTTP_400_BAD_REQUEST)
            
            user.set_password(new_password)
            user.save()
            return Response(status=status.HTTP_204_NO_CONTENT)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)



@api_view(['GET', 'PUT', 'PATCH'])
@parser_classes([FormParser, MultiPartParser, JSONParser])
@permission_classes([IsAuthenticated])
def profile(request):
    """
    Get user profile information and update user profile
    """
    try:
        user = User.objects.get(pk=request.user.pk)
    except User.DoesNotExist:
        return Response({"error":"user does not exist"}, status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':
        serializer = UpdateUserSerializer(user)
        return Response(serializer.data, status.HTTP_200_OK)
    
    elif request.method == 'PUT':
        serializer = UpdateUserSerializer(user, data=request.data, context={'request': request, 'method': 'PUT'})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method == 'PATCH':
        serializer = UpdateUserSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            data = serializer.validated_data
            if not data:
                return Response({"error":"please provide atleast one field to update"}, status=status.HTTP_400_BAD_REQUEST)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)



        
