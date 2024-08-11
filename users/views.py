from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from .serializers import *
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view

# Create your views here.

@api_view(["POST"])
def login(request):
    user = get_object_or_404(User, username=request.data['username'])
    if not user.check_password(request.data['password']):
        return Response({"detail": "Not found or Invalid Credentials"}, status=status.HTTP_404_NOT_FOUND)
    token, created = Token.objects.get_or_create(user=user)
    serializers = UserSerializer(instance=user)
    return Response({"token":token.key, "user": serializers.data['username']}, status=status.HTTP_200_OK)

@api_view(["POST"])
def signup(request):
    print(request.data)

    serializer = SignupSerializer(data=request.data)
    if serializer.is_valid():
        # Check if user already exists
        user = User.objects.filter(username=serializer.validated_data['username']).first()
        if user:
            # User already exists, get or create token
            token, created = Token.objects.get_or_create(user=user)
            return Response({
                "token": token.key,
                "user": SignupSerializer(user).data,
                "message": "User already exists. Token provided."
            }, status=status.HTTP_200_OK)
        
        # Create new user if not exists
        user = User.objects.create_user(
            username=serializer.validated_data['username'],
            email=serializer.validated_data['email'],
            password=serializer.validated_data['password'],
            first_name=serializer.validated_data.get('first_name', ''),
            last_name=serializer.validated_data.get('last_name', '')
        )
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            "token": token.key,
            "user": SignupSerializer(user).data,
            "message": "User created successfully."
        }, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Sample API endpoint to test token authentication
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
@api_view(["POST"])
def test_token(request):
    return Response({"Authorized token!"}, status=status.HTTP_200_OK)
