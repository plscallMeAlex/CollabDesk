from api.models import User, Guild, GuildMembership, Role
from api.serializers.guild_serializer import GuildSerializer
from django.shortcuts import get_object_or_404
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status


class GuildViewSet(ModelViewSet):
    queryset = Guild.objects.all()
    serializer_class = GuildSerializer

    def create_default_role(self, guild):
        # create a default role for the guild
        Role.objects.create(
            name="admin",
            color="#59AE2A",
            guild=guild,
            can_manage_roles=True,
            can_manage_channels=True,
            can_manage_bulletins=True,
            can_manage_tasks=True,
            can_manage_announcements=True,
        )

        Role.objects.create(
            name="member",
            color="#7A7A7A",
            guild=guild,
            can_manage_roles=False,
            can_manage_channels=False,
            can_manage_bulletins=False,
            can_manage_tasks=False,
            can_manage_announcements=False,
        )

        # return the role which is admin in that server
        return Role.objects.filter(guild=guild, name="admin").first()

    @action(detail=False, methods=["POST"])
    def create_guild(self, request):
        serializer = GuildSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            # create a guild membership for the creator
            user_instance = get_object_or_404(User, id=request.data["user_id"])
            guild_membership = GuildMembership.objects.create(
                user=user_instance,
                guild=serializer.instance,
                role=None,
            )

            admin = self.create_default_role(serializer.instance)
            guild_membership.role = admin
            guild_membership.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=["POST"])
    def join_guild(self, request):
        token = request.data.get("invitetoken")
        user_id = request.data.get("user_id")

        if token is None or user_id is None:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        guild = Guild.objects.filter(invitetoken=token).first()
        if guild is None:
            return Response(status=status.HTTP_404_NOT_FOUND)

        user = User.objects.filter(id=user_id).first()
        if user is None:
            return Response(status=status.HTTP_404_NOT_FOUND)

        # Check if the user is already a member of the guild
        if GuildMembership.objects.filter(user=user, guild=guild).exists():
            return Response(status=status.HTTP_400_BAD_REQUEST)

        role = Role.objects.filter(guild=guild, name="member").first()
        if role is None:
            return Response(status=status.HTTP_404_NOT_FOUND, data="Role not found")

        # Create a guild membership for the user
        GuildMembership.objects.create(
            user=user,
            guild=guild,
            role=role,
        )
        return Response(status=status.HTTP_200_OK)

    @action(detail=False, methods=["GET"])
    def list_guilds(self, request):
        guilds = Guild.objects.all()
        serializer = GuildSerializer(guilds, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=["GET"])
    def get_guilds_by_user(self, request):
        user_id = request.query_params.get("user_id")
        if user_id is None:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        user = User.objects.filter(id=user_id).first()
        if user is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        memberships = GuildMembership.objects.filter(user=user)
        guilds = [membership.guild for membership in memberships]
        serializer = GuildSerializer(guilds, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=["GET"])
    def get_guild_by_id(self, request):
        guild_id = request.query_params.get("guild_id")
        if guild_id is None:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        guild = Guild.objects.filter(id=guild_id).first()
        if guild is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = GuildSerializer(guild)
        return Response(serializer.data, status=status.HTTP_200_OK)
