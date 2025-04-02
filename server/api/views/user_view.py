from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.contrib.auth.hashers import check_password
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
from api.models import User, GuildMembership
from api.serializers.user_serializer import UserSerializer


class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def __get_token(self, user):
        """Generate a token for the given user"""
        refresh = RefreshToken.for_user(user)
        return {
            "refresh": str(refresh),
            "access": str(refresh.access_token),
        }

    @action(detail=False, methods=["POST"], permission_classes=[AllowAny])
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

        token = self.__get_token(user)

        return Response(
            {
                "message": "Login successfully",
                "user_id": user.id,
                "access": token["access"],
                "refresh": token["refresh"],
            },
            status=status.HTTP_200_OK,
        )

    @action(detail=False, methods=["POST"], permission_classes=[AllowAny])
    def register(self, request):
        serializer = UserSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # To get all users
    @action(detail=False, methods=["GET"])
    def get_all_users(self, request):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=["GET"])
    def get_user_by_id(self, request):
        user_id = request.query_params.get("user_id")
        if user_id is None:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.filter(id=user_id).first()
        if user is None:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=["GET"])
    def get_users_by_guild(self, request):
        guild_id = request.query_params.get("guild_id")

        if guild_id is None:
            return Response(
                {"detail": "guild_id is required"}, status=status.HTTP_400_BAD_REQUEST
            )

        # Fetch guild memberships
        memberships = GuildMembership.objects.filter(guild=guild_id)

        if not memberships.exists():
            return Response(
                {"detail": "No members found for this guild."},
                status=status.HTTP_404_NOT_FOUND,
            )

        # Get the users from the memberships
        users = [membership.user for membership in memberships]

        # Serialize the user data
        serializer = UserSerializer(users, many=True)

        # Return the serialized data directly
        return Response(serializer.data, status=status.HTTP_200_OK)
