from api.models import Channel
from api.serializers.channel_serializer import ChannelSerializer
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status


class ChannelViewSet(ModelViewSet):
    queryset = Channel.objects.all()
    serializer_class = ChannelSerializer

    @action(detail=False, methods=["POST"])
    def create_channel(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=["GET"])
    def get_all_channel_by_guild(self, request):
        guild_id = request.query_params.get("guild_id")
        if guild_id is None:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        channels = Channel.objects.filter(guild=guild_id)
        if not channels.exists():
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = ChannelSerializer(channels, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=["GET"])
    def get_channel_by_id(self, request):
        channel_id = request.query_params.get("channel_id")
        if channel_id is None:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        channel = Channel.objects.filter(id=channel_id).first()
        if channel is None:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = ChannelSerializer(channel)
        return Response(serializer.data, status=status.HTTP_200_OK)
