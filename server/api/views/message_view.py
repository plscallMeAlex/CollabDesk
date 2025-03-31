from api.models import Message
from api.serializers.message_serializer import MessageSerializer
from rest_framework.viewsets import ModelViewSet
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response


class MessageViewSet(ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer

    @action(detail=False, methods=["POST"])
    def create_message(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=["GET"])
    def get_all_messages_by_guild(self, request):
        guild_id = request.query_params.get("guild_id")
        if guild_id is None:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        messages = Message.objects.filter(guild=guild_id).order_by("created_at")
        if not messages.exists():
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = MessageSerializer(messages, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # get all messages in a channel
    @action(detail=False, methods=["GET"])
    def get_messages(self):
        channel_id = self.request.query_params.get("channel_id")
        if channel_id is None:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        messages = Message.objects.filter(channel=channel_id).order_by("created_at")
        if not messages.exists():
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = MessageSerializer(messages, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
