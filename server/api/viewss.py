import re
from django.shortcuts import HttpResponse
from django.contrib.auth.hashers import check_password
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status  # Import status codes

from .models import User
from api.serializers.User_serializer import UserSerializer


# Create your views here.
def home(request):
    return HttpResponse("Hello, World!")


@api_view(["POST"])
def register(request):
    serializer = UserSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save()
        return Response(
            serializer.data, status=status.HTTP_201_CREATED
        )  # ✅ Return 201 for successful creation
    return Response(
        serializer.errors, status=status.HTTP_400_BAD_REQUEST
    )  # ✅ Return 400 for bad request


@api_view(["POST"])
def login(request):
    username, password = request.data.get("username"), request.data.get("password")

    # Check whether are username or email entered
    if re.match(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$", username):
        print("Email Match")
        user = User.objects.filter(email=username).first()
    else:
        print("Username Match")
        user = User.objects.filter(username=username).first()

    if user is None:
        print("User not found")
        return Response(
            {"error": "Invalid username or password"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    if not check_password(password, user.password):
        print("Password does not match")
        return Response(
            {"error": "Invalid username or password"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    print("Login successful")
    return Response(
        {
            "message": "Login successfully",
        },
        status=status.HTTP_200_OK,
    )
