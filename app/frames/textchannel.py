import customtkinter as ctk
from datetime import datetime
import requests
import pytz

import asyncio
import websockets
import json
from threading import Thread


class ChatFrame(ctk.CTkFrame):
    def __init__(self, parent, configuration, channel, **kwargs):
        super().__init__(parent, **kwargs)
        self.__configuration = configuration
        self.__channel = channel
        self.__guildId = channel["guild"]

        # Configure layout
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)  # Messages frame expands
        self.grid_rowconfigure(1, weight=0)  # Input field stays fixed

        # Main chat area
        self.create_chat_area()

        # for websocket
        self.websocket = None
        self.room_name = self.__channel["wsroom"]  # Change this as needed
        self.ws_url = f"ws://127.0.0.1:8000/ws/chat/{self.room_name}/"

        self.loop = asyncio.new_event_loop()
        self.thread = Thread(target=self.start_loop, args=(self.loop,))
        self.thread.start()

    def create_chat_area(self):
        # Chat container (Expands to fit the parent)
        chat_frame = ctk.CTkFrame(self, fg_color="#ffffff")
        chat_frame.grid(row=0, column=0, sticky="nsew")
        chat_frame.grid_columnconfigure(0, weight=1)
        chat_frame.grid_rowconfigure(0, weight=1)  # Messages area expands
        chat_frame.grid_rowconfigure(1, weight=0)  # Input area stays fixed

        # Messages area (Scrollable and takes up full space)
        self.messages_frame = ctk.CTkScrollableFrame(chat_frame, fg_color="#ffffff")
        self.messages_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

        # Message input area (Stays at bottom)
        input_frame = ctk.CTkFrame(self, fg_color="#f3f3f3")
        input_frame.grid(row=1, column=0, sticky="ew")
        input_frame.grid_columnconfigure(0, weight=1)

        # Text input (Full width)
        self.message_entry = ctk.CTkEntry(
            input_frame, placeholder_text="Message #general", fg_color="#ffffff"
        )
        self.message_entry.grid(row=0, column=0, sticky="ew", padx=10, pady=10)
        self.message_entry.bind("<Return>", self.send_message)

        self.load_messages()  # Load messages when the frame is created

    def add_message(self, message, is_sender=False):
        # Get username from API with error handling
        try:
            response = requests.get(
                f"{self.__configuration.api_url}/users/get_user_by_id/",
                params={"user_id": message["sender"]},
            )

            if response.status_code == 200:
                user = response.json()
                username = user["username"]
            else:
                # Fallback username if API call fails
                username = "Unknown User"
                print(f"Failed to fetch user data: {response.status_code}")
        except Exception as e:
            username = "Unknown User"
            print(f"Error fetching user data: {e}")

        # Format timestamp
        try:
            utc_time = datetime.fromisoformat(
                message["created_at"].split("+")[0]
            )  # Convert to UTC datetime
            bangkok_tz = pytz.timezone("Asia/Bangkok")  # Define Bangkok timezone
            bangkok_time = utc_time.astimezone(bangkok_tz)  # Convert to Bangkok time
            timestamp = bangkok_time.strftime(
                "%b %d, %Y - %I:%M %p"
            )  # Format the timestamp
        except Exception as e:
            print(f"Error formatting timestamp: {e}")
            timestamp = "Unknown time"

        content = message["content"]

        message_container = ctk.CTkFrame(self.messages_frame, fg_color="transparent")

        # Set anchor and fill based on sender
        if is_sender:
            message_container.pack(
                fill="x", padx=5, pady=10, anchor="e"
            )  # Anchor east (right)
        else:
            message_container.pack(
                fill="x", padx=5, pady=10, anchor="w"
            )  # Anchor west (left)

        # Container for text elements
        text_container = ctk.CTkFrame(message_container, fg_color="transparent")

        if is_sender:
            text_container.pack(anchor="e")  # Align text container to the right
        else:
            text_container.pack(anchor="w")  # Align text container to the left

        # Username and timestamp
        username_label = ctk.CTkLabel(
            text_container,
            text=f"{username} ({timestamp})",
            font=(self.__configuration.font, 8),
        )
        username_label.pack(anchor="e" if is_sender else "w")

        # Message content
        content_label = ctk.CTkLabel(
            text_container,
            text=content,
            font=(self.__configuration.font, 14),
            text_color="#333",
        )
        content_label.pack(anchor="e" if is_sender else "w")
        content_label.configure(fg_color="#f0f0f0", corner_radius=5)

    def send_message(self, event=None):
        message_text = self.message_entry.get().strip()
        if message_text and self.websocket:
            # create message on the server
            sender = self.__configuration.load_user()["id"]
            payload = {
                "content": message_text,
                "channel": self.__channel["id"],
                "sender": sender,
            }

            self.loop.create_task(self.websocket.send(json.dumps(payload)))
            self.message_entry.delete(0, ctk.END)
        else:
            print("No message to send or websocket not connected.")

    def load_messages(self):
        # Fetch messages from the server
        messages = self.fetch_messages()
        user_id = self.__configuration.load_user()["id"]
        for message in messages:
            is_sender = message["sender"] == user_id
            self.add_message(message, is_sender)

    def fetch_messages(self):
        try:
            params = {
                "channel_id": self.__channel["id"],
            }
            response = requests.get(
                f"{self.__configuration.api_url}/messages/get_messages/",
                params=params,
            )
            if response.status_code == 200:
                messages = response.json()
                return messages
            else:
                print("Failed to fetch messages:", response.status_code)
        except requests.RequestException as e:
            print("Request failed:", e)
        return []

    def start_loop(self, loop):
        asyncio.set_event_loop(loop)
        loop.run_until_complete(self.connect_ws())

    async def connect_ws(self):
        async with websockets.connect(self.ws_url) as ws:
            self.websocket = ws
            async for message in ws:
                data = json.loads(message)
                if data["sender"] != self.__configuration.load_user()["id"]:
                    self.add_message(data, is_sender=False)
                else:
                    self.add_message(data, is_sender=True)
