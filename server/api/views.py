from django.shortcuts import HttpResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status  # Import status codes

from .models import User
from .serializers import UserSerializer


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
