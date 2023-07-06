from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import UserSerializer, CustomTokenObtainPairSerializer


# Create your views here.
@api_view(['POST'])
def register_user(request):
    """
    register user api view.
    """
    if request.method == 'POST':
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.validated_data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)


@api_view(['POST'])
def login_user(request):
    """
    login user api view
    """
    if request.method == 'POST':
        serializer = CustomTokenObtainPairSerializer(data=request.data)
        if serializer.is_valid():
            tokens = serializer.validated_data
            return Response(tokens, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)



@api_view(['POST'])
def refresh_token(request):
    refresh_token = request.data.get('refresh_token')

    if refresh_token:
        try:
            refresh = RefreshToken(refresh_token)
            access_token = str(refresh.access_token)
            refresh_token = str(refresh)
            return Response({'access_token': access_token, "refresh_token": refresh_token}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response({'error': 'Refresh token not provided.'}, status=status.HTTP_400_BAD_REQUEST)


