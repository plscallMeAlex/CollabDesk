from api.serializers import ChannelSerializer
from api.models import Channel, Message
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status

class ChannelViewSet(ModelViewSet):
    queryset = Channel.objects.all()
    serializer_class = ChannelSerializer

    @action(detail=False, methods=["GET"])
    def get_messages(self, request):
        channel_id = request.query_params.get("channel_id")
        if channel_id is None:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        channel = Channel.objects.filter(id=channel_id).first()
        if channel is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        if channel.type != "text":
            return Response(status=status.HTTP_400_BAD_REQUEST)
        messages = Message.objects.filter(channel=channel).order_by("created_at")
        serializer = ChannelSerializer(messages, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

