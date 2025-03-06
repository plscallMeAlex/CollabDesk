from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status

from api.models import Guild
from api.serializers.guild_serializer import GuildSerializer


class GuildViewSet(ModelViewSet):
    queryset = Guild.objects.all()
    serializer_class = GuildSerializer

    @action(detail=False, methods=["GET"])
    def list_guilds(self, request):
        guilds = Guild.objects.all()
        serializer = GuildSerializer(guilds, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
