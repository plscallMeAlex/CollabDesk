from api.models import User, Role, Guild, GuildMembership
from api.serializers.role_serializer import RoleSerializer
from api.serializers.user_serializer import UserSerializer
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status


class RoleViewSet(ModelViewSet):
    queryset = Role.objects.all()
    serializer_class = RoleSerializer

    # get the role by user id and guild id
    @action(detail=False, methods=["GET"])
    def get_role_by_user(self, request):
        user_id = request.query_params.get("user_id")
        guild_id = request.query_params.get("guild_id")

        membership = GuildMembership.objects.filter(
            user__id=user_id, guild__id=guild_id
        ).first()
        if membership is None:
            return Response(
                {"error": "Guild membership not found"},
                status=status.HTTP_404_NOT_FOUND,
            )
        role = membership.role
        if role is None:
            return Response(
                {"error": "Role not found"}, status=status.HTTP_404_NOT_FOUND
            )
        serializer = RoleSerializer(role)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # get all roles in a guild
    @action(detail=False, methods=["GET"])
    def in_guild(self, request):
        guild_id = request.query_params.get("guild_id")
        guild = Guild.objects.filter(id=guild_id).first()
        if guild is None:
            return Response(
                {"error": "Guild not found"}, status=status.HTTP_404_NOT_FOUND
            )
        roles = Role.objects.filter(guild=guild)
        serializer = RoleSerializer(roles, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=["GET"])
    def all_roles_and_users(self, request):
        guild_id = request.query_params.get("guild_id")
        guild = Guild.objects.filter(id=guild_id).first()
        if guild is None:
            return Response(
                {"error": "Guild not found"}, status=status.HTTP_404_NOT_FOUND
            )
        roles = Role.objects.filter(guild=guild)
        roles_and_users = []
        for role in roles:
            users = User.objects.filter(
                id__in=GuildMembership.objects.filter(role=role).values_list(
                    "user", flat=True
                )
            )
            roles_and_users.append(
                {
                    "role": RoleSerializer(role).data,
                    "users": UserSerializer(
                        User.objects.filter(id__in=users), many=True
                    ).data,
                }
            )
        return Response(roles_and_users, status=status.HTTP_200_OK)

    @action(detail=False, methods=["POST"])
    def assign_role(self, request):
        user_id_list = request.data.get("user_id")
        role_id = request.data.get("role_id")
        guild_id = request.data.get("guild_id")

        role = Role.objects.filter(id=role_id).first()
        if role is None:
            return Response(
                {"error": "Role not found"}, status=status.HTTP_404_NOT_FOUND
            )

        guild = Guild.objects.filter(id=guild_id).first()
        if guild is None:
            return Response(
                {"error": "Guild not found"}, status=status.HTTP_404_NOT_FOUND
            )

        for user_id in user_id_list:
            user = User.objects.filter(id=user_id).first()
            if user is None:
                return Response(
                    {"error": "User not found"}, status=status.HTTP_404_NOT_FOUND
                )
            GuildMembership.objects.filter(user=user, guild=guild).update(role=role)

        return Response(
            {"message": "Role assigned successfully"}, status=status.HTTP_200_OK
        )
