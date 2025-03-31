import customtkinter as ctk
from datetime import datetime


class ChatFrame(ctk.CTkFrame):
    def __init__(self, parent, configuration, channel, **kwargs):
        super().__init__(parent, **kwargs)
        self.__configuration = configuration
        self.__channel = channel
        self.__guildId = channel["guild"]

        # Configure layout
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        # Main chat area
        self.create_chat_area()

    def create_chat_area(self):
        # Chat container
        chat_frame = ctk.CTkFrame(self, fg_color="#ffffff")
        chat_frame.grid(row=0, column=0, sticky="nsew")
        chat_frame.grid_rowconfigure(1, weight=1)
        chat_frame.grid_columnconfigure(0, weight=1)

        # Messages area
        self.messages_frame = ctk.CTkScrollableFrame(chat_frame, fg_color="#ffffff")
        self.messages_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

        # Add example messages
        self.add_message("User1", "Hello, how's everyone?", "Today at 9:15 AM")
        self.add_message(
            "User2", "I'm working on some Python stuff!", "Today at 9:20 AM"
        )

        # Message input area
        input_frame = ctk.CTkFrame(self, fg_color="#f3f3f3", height=50)
        input_frame.grid(row=1, column=0, sticky="ew", padx=10, pady=10)
        input_frame.grid_columnconfigure(0, weight=1)

        # Text input
        self.message_entry = ctk.CTkEntry(
            input_frame, placeholder_text="Message #general", fg_color="#ffffff"
        )
        self.message_entry.grid(row=0, column=0, sticky="ew", padx=10, pady=10)
        self.message_entry.bind("<Return>", self.send_message)

    def add_message(self, username, content, timestamp):
        message_container = ctk.CTkFrame(self.messages_frame, fg_color="transparent")
        message_container.pack(fill="x", padx=5, pady=2, anchor="w")

        username_label = ctk.CTkLabel(
            message_container,
            text=f"{username} ({timestamp})",
            font=("Arial", 12, "bold"),
        )
        username_label.pack(anchor="w")

        content_label = ctk.CTkLabel(
            message_container, text=content, font=("Arial", 14), text_color="#333"
        )
        content_label.pack(anchor="w")

    def send_message(self, event=None):
        message_text = self.message_entry.get().strip()
        if message_text:
            now = datetime.now().strftime("Today at %I:%M %p")
            self.add_message("You", message_text, now)
            self.message_entry.delete(0, "end")
