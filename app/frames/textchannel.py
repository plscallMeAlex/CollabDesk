import customtkinter as ctk
from datetime import datetime
import requests


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

        # Add example messages
        # self.add_message("User1", "Hello, how's everyone?", "Today at 9:15 AM")
        # self.add_message(
        #     "User2",
        #     "I'm working on some Python stuff!",
        #     "Today at 9:20 AM",
        #     is_sender=True,
        # )

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
            format_time = datetime.fromisoformat(message["created_at"].split("+")[0])
            timestamp = format_time.strftime("%b %d, %Y - %I:%M %p")
        except Exception:
            timestamp = "Unknown time"

        content = message["content"]

        message_container = ctk.CTkFrame(self.messages_frame, fg_color="transparent")

        # Set anchor and fill based on sender
        if is_sender:
            message_container.pack(
                fill="x", padx=5, pady=2, anchor="e"
            )  # Anchor east (right)
        else:
            message_container.pack(
                fill="x", padx=5, pady=2, anchor="w"
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
            font=("Arial", 12, "bold"),
        )
        username_label.pack(anchor="e" if is_sender else "w")

        # Message content
        content_label = ctk.CTkLabel(
            text_container,
            text=content,
            font=("Arial", 14),
            text_color="#333",
        )
        content_label.pack(
            anchor="e" if is_sender else "w",
        )
        content_label.configure(fg_color="#f0f0f0", corner_radius=5)

    def send_message(self, event=None):
        message_text = self.message_entry.get().strip()
        if message_text:
            # create message on the server
            sender = self.__configuration.load_user()["id"]
            payload = {
                "content": message_text,
                "channel": self.__channel["id"],
                "sender": sender,
            }
            response = requests.post(
                f"{self.__configuration.api_url}/messages/create_message/",
                json=payload,
            )

            if response.status_code == 201:
                message = response.json()
                self.add_message(message, is_sender=True)
                # Add the message to the chat area

            else:
                print("Failed to send message:", response.status_code)
                return

    def fetch_messages(self):
        try:
            params = {
                "channel_id": self.__channel["id"],
            }
            response = requests.get(
                f"{self.__configuration['api_url']}/messages/get_messages/",
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
