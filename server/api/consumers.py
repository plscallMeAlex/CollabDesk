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
        self.channel_layer = get_channel_layer()
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = f"voice_{self.room_name}"

        # Get user info safely with fallbacks
        try:
            if self.scope.get("user") and self.scope["user"].is_authenticated:
                self.user_id = str(self.scope["user"].id)
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

        # First send list of existing users in the room to the new user
        existing_users = await self.get_existing_users()
        for user in existing_users:
            if user["user_id"] != self.user_id:  # Don't send yourself
                await self.send(
                    text_data=json.dumps(
                        {
                            "type": "user_join",
                            "user_id": user["user_id"],
                            "username": user["username"],
                        }
                    )
                )

        # Then notify group about new user (including yourself)
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "user_join",
                "user_id": self.user_id,
                "username": self.username,
            },
        )

        # Add self to active users
        await self.add_active_user(self.user_id, self.username)

    async def disconnect(self, close_code):
        # Remove from active users
        await self.remove_active_user(self.user_id)

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

            # Use sender_id from message if available, otherwise use self.user_id
            sender_id = data.get("sender_id", self.user_id)
            target_id = data.get("target_id")

            if message_type == "offer":
                await self.channel_layer.group_send(
                    self.room_group_name,
                    {
                        "type": "webrtc_offer",
                        "offer": data["sdp"],
                        "sender_id": sender_id,
                        "target_id": target_id,
                    },
                )
            elif message_type == "answer":
                await self.channel_layer.group_send(
                    self.room_group_name,
                    {
                        "type": "webrtc_answer",
                        "answer": data["answer"],
                        "sender_id": sender_id,
                        "target_id": target_id,
                    },
                )
            elif message_type == "ice_candidate":
                await self.channel_layer.group_send(
                    self.room_group_name,
                    {
                        "type": "ice_candidate",
                        "candidate": data["candidate"],
                        "sender_id": sender_id,
                        "target_id": target_id,
                    },
                )
            elif message_type == "mute_status":
                # Forward mute status to other participants
                await self.channel_layer.group_send(
                    self.room_group_name,
                    {
                        "type": "mute_status_change",
                        "user_id": sender_id,
                        "is_muted": data["is_muted"],
                    },
                )

        except json.JSONDecodeError:
            print(f"Invalid JSON received: {text_data}")
        except Exception as e:
            print(f"Error processing message: {str(e)}")

    # Active user management
    async def add_active_user(self, user_id, username):
        """Add user to active users list"""
        await self.channel_layer.group_add(f"user_{user_id}", self.channel_name)

        # Store in room-specific group information using group_send
        room_users = await self.get_group_users()
        room_users[user_id] = {"username": username}

        # Store through Redis pub/sub instead of direct Redis access
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "store_room_users",
                "room_users": room_users,
            },
        )

    async def remove_active_user(self, user_id):
        """Remove user from active users list"""
        await self.channel_layer.group_discard(f"user_{user_id}", self.channel_name)

        # Remove from room-specific group information
        room_users = await self.get_group_users()
        if user_id in room_users:
            del room_users[user_id]

        # Store through Redis pub/sub instead of direct Redis access
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "store_room_users",
                "room_users": room_users,
            },
        )

    # We'll use an in-memory cache as Redis channel layer doesn't have direct get/set
    _room_users_cache = {}  # Class variable to store room users

    async def get_existing_users(self):
        """Get list of existing users in the room"""
        room_users = await self.get_group_users()
        return [
            {"user_id": uid, "username": data.get("username", "Unknown")}
            for uid, data in room_users.items()
        ]

    async def get_group_users(self):
        """Get users in this group from the memory cache"""
        # Using in-memory cache instead of Redis direct access
        key = f"voice_room_{self.room_name}_users"
        return self.__class__._room_users_cache.get(key, {})

    async def store_room_users(self, event):
        """Handler for storing room users in memory cache"""
        key = f"voice_room_{self.room_name}_users"
        self.__class__._room_users_cache[key] = event["room_users"]

    # Event handlers
    async def user_join(self, event):
        """Forward user join event to clients"""
        await self.send(text_data=json.dumps(event))

    async def user_leave(self, event):
        """Forward user leave event to clients"""
        await self.send(text_data=json.dumps(event))

    async def webrtc_offer(self, event):
        """Forward WebRTC offer to clients"""
        # Only send to target if specified, otherwise send to everyone
        target_id = event.get("target_id")
        if target_id is None or target_id == self.user_id:
            await self.send(text_data=json.dumps(event))

    async def webrtc_answer(self, event):
        """Forward WebRTC answer to clients"""
        # Only send to target if specified, otherwise send to everyone
        target_id = event.get("target_id")
        if target_id is None or target_id == self.user_id:
            await self.send(text_data=json.dumps(event))

    async def ice_candidate(self, event):
        """Forward ICE candidate to clients"""
        # Only send to target if specified, otherwise send to everyone
        target_id = event.get("target_id")
        if target_id is None or target_id == self.user_id:
            await self.send(text_data=json.dumps(event))

    async def mute_status_change(self, event):
        """Forward mute status change to clients"""
        # Send to all clients in the room
        await self.send(
            text_data=json.dumps(
                {
                    "type": "mute_status",
                    "user_id": event["user_id"],
                    "is_muted": event["is_muted"],
                }
            )
        )
