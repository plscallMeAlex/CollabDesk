import customtkinter as ctk
from PIL import Image
import os

class CreateServerDialog(ctk.CTkToplevel):
    def __init__(self, parent, server_type):
        super().__init__(parent)
        self.parent = parent
        self.server_type = server_type
        
        # Configure dialog window
        self.title("Create a Server")
        self.geometry("480x400")
        self.resizable(False, False)
        self.center_window()
        
        # Main container
        self.main_frame = ctk.CTkFrame(self, fg_color="#313338")
        self.main_frame.pack(fill="both", expand=True)
        
        # Title
        title_text = "Create a Community Server" if server_type == "community" else "Create a Friends Server"
        self.title_label = ctk.CTkLabel(
            self.main_frame,
            text=title_text,
            font=("Arial", 24, "bold"),
            text_color="white"
        )
        self.title_label.pack(pady=(20, 10))
        
        # Server name label
        self.name_label = ctk.CTkLabel(
            self.main_frame,
            text="SERVER NAME",
            font=("Arial", 12),
            text_color="#B5BAC1"
        )
        self.name_label.pack(pady=(20, 5), padx=20, anchor="w")
        
        # Server name entry
        self.name_entry = ctk.CTkEntry(
            self.main_frame,
            font=("Arial", 14),
            fg_color="#1E1F22",
            border_color="#1E1F22",
            text_color="white",
            placeholder_text="Enter server name"
        )
        self.name_entry.pack(fill="x", padx=20)
        
        # Buttons frame
        self.button_frame = ctk.CTkFrame(
            self.main_frame,
            fg_color="transparent"
        )
        self.button_frame.pack(side="bottom", fill="x", padx=20, pady=20)
        
        # Back button
        self.back_button = ctk.CTkButton(
            self.button_frame,
            text="Back",
            font=("Arial", 14),
            fg_color="#2B2D31",
            hover_color="#404249",
            command=self.on_back
        )
        self.back_button.pack(side="left")
        
        # Create button
        self.create_button = ctk.CTkButton(
            self.button_frame,
            text="Create Server",
            font=("Arial", 14),
            fg_color="#5865F2",
            hover_color="#4752C4",
            command=self.on_create
        )
        self.create_button.pack(side="right")

    def center_window(self):
        self.update_idletasks()
        width = self.winfo_width()
        height = self.winfo_height()
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry(f'+{x}+{y}')

    def on_back(self):
        self.destroy()
        ServerTypeDialog(self.parent)

    def on_create(self):
        server_name = self.name_entry.get()
        if server_name:
            print(f"Creating {self.server_type} server: {server_name}")
            if hasattr(self.parent, 'add_server_icon'):
                self.parent.add_server_icon(server_name)
            self.destroy()

