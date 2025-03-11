from api.models import User, Guild, GuildMembership
from api.serializers.guild_serializer import GuildSerializer
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status


class GuildViewSet(ModelViewSet):
    queryset = Guild.objects.all()
    serializer_class = GuildSerializer

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
