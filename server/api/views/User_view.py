from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.contrib.auth.hashers import check_password
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from api.models import User
from api.serializers.user_serializer import UserSerializer


class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    @action(detail=False, methods=["POST"])
    def login(self, request):
        username, password = (
            request.data.get("username", "").strip(),
            request.data.get("password", "").strip(),
        )
        user = None
        try:
            validate_email(username)
            user = User.objects.get(email=username)
        except ValidationError:
            user = User.objects.filter(username=username).first()
        if user is None or not check_password(password, user.password):
            return Response(
                {"error": "Invalid username or password"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        return Response(
            {
                "message": "Login successfully",
            },
            status=status.HTTP_200_OK,
        )

    @action(detail=False, methods=["POST"])
    def register(self, request):
        serializer = UserSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
