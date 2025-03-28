from channels.generic.websocket import AsyncWebsocketConsumer
from channels.layers import get_channel_layer
from channels.db import database_sync_to_async
import json

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.channel_layer = get_channel_layer()
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f'chat_{self.room_name}'

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        # user = text_data_json['user']
        # channel = text_data_json['channel']

        # Save message to database
        # await self.save_message(message, user, channel)

        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message
            }
        )


    # Receive message from room group
    async def chat_message(self, event):
        message = event['message']
        

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message,
        }))

    # async def save_message(self, message, user, channel):
    #     from django.utils.timezone import now
    #     from api.models import Message
    #     from api.models import User
    #     from api.models import Channel

    #     user = User.objects.get(id=user)
    #     channel = Channel.objects.get(id=channel)

    #     await database_sync_to_async(Message.objects.create)(
    #         content=message,
    #         sender=user,
    #         channel=channel,
    #         created_at=now()
    #     )
