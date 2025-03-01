import customtkinter as ctk
from datetime import datetime
import os

# import customtkinter as ctk

class ChatApplication(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        # Configure window
        self.title("Discord-like Chat")
        self.geometry("1200x800")
        
        # Set theme
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        
        # Configure the main window to expand
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)
        
        # Create the main chat area
        self.create_chat_area()
        
        # Create the user list sidebar (right side)
        self.create_user_sidebar()
        
    def create_chat_area(self):
        # Main chat container
        chat_frame = ctk.CTkFrame(self, fg_color="#36393f", corner_radius=0)
        chat_frame.grid(row=0, column=1, sticky="nsew")
        chat_frame.grid_rowconfigure(1, weight=1)
        chat_frame.grid_columnconfigure(0, weight=1)
        
        # Channel header
        channel_header = ctk.CTkFrame(chat_frame, fg_color="#36393f", corner_radius=0, height=48, border_width=1, border_color="#26282c")
        channel_header.grid(row=0, column=0, sticky="ew", padx=0, pady=0)
        channel_header.grid_propagate(False)
        
        # Channel name in the header
        channel_name = ctk.CTkLabel(channel_header, text="# general", font=("Arial", 16, "bold"), text_color="white")
        channel_name.place(x=20, y=14)
        
        # Channel topic
        channel_topic = ctk.CTkLabel(channel_header, text="General chat for anything", font=("Arial", 12), text_color="#96989d")
        channel_topic.place(x=120, y=14)
        
        # Search icon
        search_btn = ctk.CTkButton(
            channel_header, 
            text="🔍",
            fg_color="transparent",
            hover_color="#40444b",
            width=30,
            height=30,
            corner_radius=4
        )
        search_btn.place(relx=0.95, rely=0.5, anchor="e")
        
        # Messages area
        self.messages_frame = ctk.CTkScrollableFrame(chat_frame, fg_color="#36393f")
        self.messages_frame.grid(row=1, column=0, sticky="nsew", padx=0, pady=0)
        
        # Add some example messages
        self.add_message("System", "Welcome to #general", "Yesterday at 10:30 PM")
        self.add_message("User1", "Hey everyone! How's it going?", "Today at 9:15 AM")
        self.add_message("User2", "Working on some Python code with CustomTkinter", "Today at 9:20 AM")
        self.add_message("User1", "That sounds cool! What are you building?", "Today at 9:22 AM")
        
        # Message input area
        input_frame = ctk.CTkFrame(chat_frame, fg_color="#40444b", corner_radius=8, height=44)
        input_frame.grid(row=2, column=0, sticky="ew", padx=20, pady=20)
        input_frame.grid_propagate(False)
        input_frame.grid_columnconfigure(0, weight=1)
        
        # Plus button for adding attachments
        plus_btn = ctk.CTkButton(
            input_frame,
            text="+",
            fg_color="transparent",
            text_color="#b9bbbe",
            hover_color="#36393f",
            width=30,
            height=30,
            corner_radius=4
        )
        plus_btn.grid(row=0, column=0, sticky="w", padx=2, pady=2)
        
        # Text input
        self.message_entry = ctk.CTkEntry(
            input_frame,
            placeholder_text="Message #general",
            border_width=0,
            fg_color="transparent",
            text_color="white",
            placeholder_text_color="#72767d"
        )
        self.message_entry.grid(row=0, column=0, sticky="ew", padx=(40, 40), pady=2)
        self.message_entry.bind("<Return>", self.send_message)
        
        # Emoji button
        emoji_btn = ctk.CTkButton(
            input_frame,
            text="😊",
            fg_color="transparent",
            text_color="#b9bbbe",
            hover_color="#36393f",
            width=30,
            height=30,
            corner_radius=4
        )
        emoji_btn.grid(row=0, column=1, sticky="e", padx=2, pady=2)

    def create_user_sidebar(self):
        # User list sidebar
        user_sidebar = ctk.CTkFrame(self, fg_color="#2f3136", corner_radius=0, width=240)
        user_sidebar.grid(row=0, column=2, sticky="nsew")
        user_sidebar.grid_propagate(False)  # Prevent frame from shrinking
        
        # User list header
        user_header = ctk.CTkFrame(user_sidebar, fg_color="transparent", height=48)
        user_header.grid(row=0, column=0, sticky="ew", padx=0, pady=0)
        
        # Search box
        search_box = ctk.CTkEntry(
            user_header,
            placeholder_text="Search",
            width=200,
            height=28,
            corner_radius=4,
            border_width=0,
            fg_color="#202225",
            text_color="white",
            placeholder_text_color="#72767d"
        )
        search_box.place(relx=0.5, rely=0.5, anchor="center")
        
        # User list container
        user_list_frame = ctk.CTkScrollableFrame(user_sidebar, fg_color="#2f3136")
        user_list_frame.grid(row=1, column=0, sticky="nsew", padx=0, pady=0)
        
        # Online users category
        online_category = ctk.CTkFrame(user_list_frame, fg_color="transparent", height=30)
        online_category.pack(fill="x", padx=10, pady=(10, 2))
        
        online_label = ctk.CTkLabel(online_category, text="ONLINE — 3", font=("Arial", 12), text_color="#96989d")
        online_label.pack(side="left", padx=5)
        
        # Add online users
        users = ["User1", "User2", "Yourself"]
        for user in users:
            user_frame = ctk.CTkFrame(user_list_frame, fg_color="transparent", height=42)
            user_frame.pack(fill="x", padx=10, pady=2)
            
            # Status indicator (green dot for online)
            status = ctk.CTkButton(
                user_frame,
                text="",
                width=10,
                height=10,
                corner_radius=5,
                fg_color="#43b581",
                hover_color="#43b581"
            )
            status.place(x=2, y=16)
            
            # User avatar (placeholder)
            avatar = ctk.CTkButton(
                user_frame,
                text="",
                width=32,
                height=32,
                corner_radius=16,
                fg_color="#7289da" if user != "Yourself" else "#43b581",
                hover_color="#7289da" if user != "Yourself" else "#43b581"
            )
            avatar.place(x=20, y=5)
            
            # Username
            username = ctk.CTkLabel(user_frame, text=user, font=("Arial", 14), text_color="white")
            username.place(x=60, y=10)

    def add_message(self, user, message, timestamp):
        message_label = ctk.CTkLabel(self.messages_frame, text=f"{user}: {message}\n{timestamp}", font=("Arial", 12), text_color="white")
        message_label.pack(fill="x", padx=10, pady=5)

    def send_message(self, event):
        message = self.message_entry.get()
        if message:
            self.add_message("Yourself", message, "Now")
            self.message_entry.delete(0, "end")

if __name__ == "__main__":
    app = ChatApplication()
    app.mainloop()