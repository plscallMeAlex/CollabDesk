import customtkinter as ctk
from datetime import datetime
from app.components.userSidebar import UserSideBar  # Importing the UserSideBar class

class ChatApplication(ctk.CTk):
    def __init__(self, configuration):
        super().__init__()
        
        # Configure window
        self.title("Discord-like Chat")
        self.geometry("1200x800")
        self._configuration = configuration
        
        # Set theme
        ctk.set_appearance_mode("light")  # Set to light mode for a white theme
        ctk.set_default_color_theme("blue")  # You can choose another color theme if needed
        
        # Configure the main window to expand
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)
        
        # Create the main chat area
        self.create_chat_area()
        
        # Create the user list sidebar (right side)
        self.create_user_sidebar()
        
    def create_chat_area(self):
        # Main chat container
        chat_frame = ctk.CTkFrame(self, fg_color="#f3f4f6", corner_radius=0)  # Light background color
        chat_frame.grid(row=0, column=1, sticky="nsew")
        chat_frame.grid_rowconfigure(1, weight=1)
        chat_frame.grid_columnconfigure(0, weight=1)
        
        # Channel header
        channel_header = ctk.CTkFrame(chat_frame, fg_color="#f3f4f6", corner_radius=0, height=48, border_width=1, border_color="#d1d3d6")
        channel_header.grid(row=0, column=0, sticky="ew", padx=0, pady=0)
        channel_header.grid_propagate(False)
        
        # Channel name in the header
        channel_name = ctk.CTkLabel(channel_header, text="# general", font=("Arial", 16, "bold"), text_color="black")
        channel_name.place(x=20, y=14)
        
        # Channel topic
        channel_topic = ctk.CTkLabel(channel_header, text="General chat for anything", font=("Arial", 12), text_color="#555")
        channel_topic.place(x=120, y=14)
        
        # Search icon
        search_btn = ctk.CTkButton(
            channel_header, 
            text="🔍",
            fg_color="transparent",
            hover_color="#e0e0e0",
            width=30,
            height=30,
            corner_radius=4
        )
        search_btn.place(relx=0.95, rely=0.5, anchor="e")
        
        # Messages area
        self.messages_frame = ctk.CTkScrollableFrame(chat_frame, fg_color="#f3f4f6")
        self.messages_frame.grid(row=1, column=0, sticky="nsew", padx=0, pady=0)
        
        # Add some example messages
        self.add_message("System", "Welcome to #general", "Yesterday at 10:30 PM")
        self.add_message("User1", "Hey everyone! How's it going?", "Today at 9:15 AM")
        self.add_message("User2", "Working on some Python code with CustomTkinter", "Today at 9:20 AM")
        self.add_message("User1", "That sounds cool! What are you building?", "Today at 9:22 AM")
        
        # Message input area
        input_frame = ctk.CTkFrame(chat_frame, fg_color="#ffffff", corner_radius=8, height=44)
        input_frame.grid(row=2, column=0, sticky="ew", padx=20, pady=20)
        input_frame.grid_propagate(False)
        input_frame.grid_columnconfigure(0, weight=1)
        
        # Plus button for adding attachments
        plus_btn = ctk.CTkButton(
            input_frame,
            text="+",
            fg_color="transparent",
            text_color="#555",
            hover_color="#f0f0f0",
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
            text_color="black",
            placeholder_text_color="#72767d"
        )
        self.message_entry.grid(row=0, column=0, sticky="ew", padx=(40, 40), pady=2)
        self.message_entry.bind("<Return>", self.send_message)
        
        # Emoji button
        emoji_btn = ctk.CTkButton(
            input_frame,
            text="😊",
            fg_color="transparent",
            text_color="#555",
            hover_color="#f0f0f0",
            width=30,
            height=30,
            corner_radius=4
        )
        emoji_btn.grid(row=0, column=1, sticky="e", padx=2, pady=2)
    
    def create_user_sidebar(self):
        # Create the user sidebar using UserSideBar class from another file
        user_sidebar = UserSideBar(self)  # Instantiate UserSideBar
        user_sidebar.grid(row=0, column=2, sticky="nsew")
        user_sidebar.grid_propagate(False)  # Prevent frame from shrinking

    def add_message(self, username, content, timestamp):
        message_container = ctk.CTkFrame(self.messages_frame, fg_color="transparent", height=80)
        message_container.pack(fill="x", padx=10, pady=5, anchor="w")
        
        # User avatar (placeholder)
        avatar = ctk.CTkButton(
            message_container,
            text="",
            width=40,
            height=40,
            corner_radius=20,
            fg_color="#7289da" if username != "Yourself" else "#43b581",
            hover_color="#7289da" if username != "Yourself" else "#43b581"
        )
        avatar.grid(row=0, column=0, padx=(0, 10), pady=5, rowspan=2)
        
        # Username and timestamp
        header_frame = ctk.CTkFrame(message_container, fg_color="transparent", height=20)
        header_frame.grid(row=0, column=1, sticky="w")
        
        username_label = ctk.CTkLabel(header_frame, text=username, font=("Arial", 16, "bold"), text_color="black")
        username_label.pack(side="left", padx=(0, 5))
        
        timestamp_label = ctk.CTkLabel(header_frame, text=timestamp, font=("Arial", 12), text_color="#96989d")
        timestamp_label.pack(side="left")
        
        # Message content
        content_label = ctk.CTkLabel(
            message_container, 
            text=content, 
            font=("Arial", 14), 
            text_color="#333",
            justify="left",
            anchor="w",
            wraplength=500
        )
        content_label.grid(row=1, column=1, sticky="w")
    
    def send_message(self, event=None):
        message_text = self.message_entry.get().strip()
        if message_text:
            now = datetime.now().strftime("Today at %I:%M %p")
            self.add_message("Yourself", message_text, now)
            self.message_entry.delete(0, 'end')
            
            # Auto-scroll to bottom
            self.after(100, lambda: self.messages_frame._scrollbar.set(1.0, 1.0))

if __name__ == "__main__":
    app = ChatApplication()
    app.mainloop()

