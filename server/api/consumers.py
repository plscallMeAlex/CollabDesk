from channels.generic.websocket import AsyncWebsocketConsumer
from channels.layers import get_channel_layer
from channels.db import database_sync_to_async
import json


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.channel_layer = get_channel_layer()
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = f"chat_{self.room_name}"

        # Join room group
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        content = text_data_json["content"]
        sender = text_data_json["sender"]
        channel = text_data_json["channel"]
        print(f"text_data_json: {text_data_json}")
        # Save message to database
        message = await self.save_message(content, sender, channel)

        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "chat_message",
                "sender": sender,
                "content": content,
                "created_at": message.created_at.isoformat(),
            },
        )

    # Receive message from room group
    async def chat_message(self, event):
        content = event["content"]
        sender = event["sender"]
        created_at = event["created_at"]

        # Send message to WebSocket
        await self.send(
            text_data=json.dumps(
                {
                    "sender": sender,
                    "created_at": created_at,
                    "content": content,
                }
            )
        )

    @database_sync_to_async
    def save_message(self, message, user, channel):
        from api.models import Message
        from api.models import User
        from api.models import Channel

        user = User.objects.get(id=user)
        channel = Channel.objects.get(id=channel)

        return Message.objects.create(content=message, sender=user, channel=channel)


class VoiceChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = f"voice_{self.room_name}"

        # Get user info safely with fallbacks
        try:
            if self.scope.get("user") and self.scope["user"].is_authenticated:
                self.user_id = self.scope["user"].id
                self.username = self.scope["user"].username
            else:
                # Fallback to query parameters or generate temporary ID
                query_string = self.scope.get("query_string", b"").decode()
                query_params = dict(
                    item.split("=") for item in query_string.split("&") if "=" in item
                )
                self.user_id = query_params.get("user_id", f"anonymous_{id(self)}")
                self.username = query_params.get("username", f"Guest_{id(self) % 1000}")
        except Exception:
            # If all else fails, use anonymous identifiers
            self.user_id = f"anonymous_{id(self)}"
            self.username = f"Guest_{id(self) % 1000}"

        # Join room group
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

        # Notify group about new user
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "user_join",
                "user_id": self.user_id,
                "username": self.username,
            },
        )

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

        # Notify group about user leaving
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "user_leave",
                "user_id": self.user_id,
                "username": self.username,
            },
        )

    async def receive(self, text_data):
        try:
            data = json.loads(text_data)
            message_type = data.get("type")

            if message_type == "offer":
                await self.channel_layer.group_send(
                    self.room_group_name,
                    {
                        "type": "webrtc_offer",
                        "offer": data["sdp"],
                        "sender_id": data.get("sender_id", self.user_id),
                        "target_id": data.get("target_id"),
                    },
                )
            elif message_type == "answer":
                await self.channel_layer.group_send(
                    self.room_group_name,
                    {
                        "type": "webrtc_answer",
                        "answer": data["answer"],
                        "sender_id": data.get("sender_id", self.user_id),
                        "target_id": data.get("target_id"),
                    },
                )
            elif message_type == "ice_candidate":
                await self.channel_layer.group_send(
                    self.room_group_name,
                    {
                        "type": "ice_candidate",
                        "candidate": data["candidate"],
                        "sender_id": data.get("sender_id", self.user_id),
                        "target_id": data.get("target_id"),
                    },
                )
        except json.JSONDecodeError:
            print(f"Invalid JSON received: {text_data}")
        except Exception as e:
            print(f"Error processing message: {str(e)}")

    async def user_join(self, event):
        await self.send(text_data=json.dumps(event))

    async def user_leave(self, event):
        await self.send(text_data=json.dumps(event))

    async def webrtc_offer(self, event):
        await self.send(text_data=json.dumps(event))

    async def webrtc_answer(self, event):
        await self.send(text_data=json.dumps(event))

    async def ice_candidate(self, event):
        await self.send(text_data=json.dumps(event))
