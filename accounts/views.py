from django.shortcuts import render

# Create your views here.

from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password

User = get_user_model()

@api_view(['POST'])
def signup(request):
    data = request.data

    user = User.objects.create(
        username=data['username'],
        email=data['email'],
        password=make_password(data['password'])
    )

    return Response({"message": "User created successfully"})

from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate

@api_view(['POST'])
def login(request):
    data = request.data

    user = authenticate(username=data['username'], password=data['password'])

    if user is None:
        return Response({"error": "Invalid credentials"}, status=400)

    refresh = RefreshToken.for_user(user)

    return Response({
        "access": str(refresh.access_token),
        "refresh": str(refresh)
    })