import customtkinter as ctk
from tkinter import StringVar, Toplevel
from PIL import Image
import os


class ChannelBar(ctk.CTkFrame):
    def __init__(self, parent, configuration, change_frame_callback, guildId):
        super().__init__(parent)
        self._conguration = configuration
        self.configure(width=250, height=600, corner_radius=10)
        self.change_frame_callback = change_frame_callback
        self.__guildId = guildId

        self.server_label = ctk.CTkLabel(
            self,
            text="CollabDesk",
            font=("Arial", 16, "bold"),
            text_color="black",
            anchor="w",
        )
        self.server_label.pack(fill="x", padx=10, pady=10)

        self.dashboard_btn = ctk.CTkButton(
            self,
            text="📊 Dashboard",
            text_color="black",
            fg_color="transparent",
            hover_color="gray",
            anchor="w",
            command=lambda: self.change_frame_callback("Dashboard"),
        )
        self.dashboard_btn.pack(fill="x", padx=10, pady=2)

        self.calendar_btn = ctk.CTkButton(
            self,
            text="📅 Calendar",
            text_color="black",
            fg_color="transparent",
            hover_color="gray",
            anchor="w",
            command=lambda: self.change_frame_callback("Calendar"),
        )
        self.calendar_btn.pack(fill="x", padx=10, pady=2)

        self.bulletin_btn = ctk.CTkButton(
            self,
            text="📌 Bulletin board",
            text_color="black",
            fg_color="transparent",
            hover_color="gray",
            anchor="w",
            command=lambda: self.change_frame_callback("BulletinBoard"),
        )
        self.bulletin_btn.pack(fill="x", padx=10, pady=2)

        self.channel_label = ctk.CTkLabel(
            self,
            text="TEXT CHANNELS",
            font=("Arial", 12, "bold"),
            text_color="black",
            anchor="w",
        )
        self.channel_label.pack(fill="x", padx=10, pady=(20, 5))

        self.channels_frame = ctk.CTkFrame(self)
        self.channels_frame.pack(fill="both", expand=True)

        self.channels = [
            "# announcement",
            "# general",
            "# talking-space",
            "# share-file",
        ]
        self.channel_buttons = {}

        for channel in self.channels:
            self.add_channel_button(channel)

        self.add_channel_btn = ctk.CTkButton(
            self,
            text="+ Add Channel",
            text_color="black",
            fg_color="transparent",
            hover_color="gray",
            anchor="w",
            command=self.open_create_channel_popup,
        )
        self.add_channel_btn.pack(fill="x", padx=10, pady=10)

        self.user_frame = ctk.CTkFrame(self, height=50)
        self.user_frame.pack(side="bottom", fill="x", pady=5)

        image_path = "assets/logo.png"
        if os.path.exists(image_path):
            profile_image = ctk.CTkImage(
                light_image=Image.open(image_path), size=(30, 30)
            )
        else:
            profile_image = None

        self.profile_label = (
            ctk.CTkLabel(self.user_frame, image=profile_image, text="")
            if profile_image
            else ctk.CTkLabel(self.user_frame, text="👤", text_color="black")
        )
        self.profile_label.pack(side="left", padx=10)

        self.user_label = ctk.CTkLabel(
            self.user_frame, text="Alex", text_color="black", anchor="w"
        )
        self.user_label.pack(side="left", padx=10, fill="x", expand=True)

        self.settings_btn = ctk.CTkButton(
            self.user_frame,
            text="⚙",
            text_color="black",
            fg_color="transparent",
            width=30,
        )
        self.settings_btn.pack(side="right", padx=10)

    def switch_page(self, page_name):
        if self.page_manager:
            self.page_manager.switch_page(page_name)

    def add_channel_button(self, channel_name):
        btn = ctk.CTkButton(
            self.channels_frame,
            text=channel_name,
            text_color="black",
            fg_color="transparent",
            hover_color="gray",
            anchor="w",
            command=lambda: self.switch_page(channel_name),
        )
        btn.pack(fill="x", padx=10, pady=2)
        self.channel_buttons[channel_name] = btn

    def open_create_channel_popup(self):
        self.popup = Toplevel(self)
        self.popup.title("Create New Channel")
        self.popup.geometry("480x400")
        self.popup.resizable(False, False)

        self.center_window(self.popup)

        self.main_frame = ctk.CTkFrame(self.popup, fg_color="transparent")
        self.main_frame.pack(fill="both", expand=True)

        self.title_label = ctk.CTkLabel(
            self.main_frame,
            text="Create a New Channel",
            font=("Arial", 24, "bold"),
            text_color="black",
        )
        self.title_label.pack(pady=(20, 10))

        self.name_label = ctk.CTkLabel(
            self.main_frame,
            text="CHANNEL NAME",
            font=("Arial", 12),
            text_color="#B5BAC1",
        )
        self.name_label.pack(pady=(20, 5), padx=20, anchor="w")

        self.channel_name_var = StringVar()
        self.channel_entry = ctk.CTkEntry(
            self.main_frame,
            font=("Arial", 14),
            fg_color="transparent",
            border_color="#1E1F22",
            text_color="white",
            placeholder_text="Enter channel name",
            textvariable=self.channel_name_var,
        )
        self.channel_entry.pack(fill="x", padx=20)

        self.button_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        self.button_frame.pack(side="bottom", fill="x", padx=20, pady=20)

        self.create_btn = ctk.CTkButton(
            self.button_frame,
            text="Create",
            font=("Arial", 14),
            fg_color="#2B2D31",
            hover_color="#404249",
            command=self.create_channel,
        )
        self.create_btn.pack(side="left", padx=10)

        self.cancel_btn = ctk.CTkButton(
            self.button_frame,
            text="Cancel",
            font=("Arial", 14),
            fg_color="#2B2D31",
            hover_color="#404249",
            command=self.cancel_create_channel,
        )
        self.cancel_btn.pack(side="right", padx=10)

    def create_channel(self):
        new_channel = f"# {self.channel_name_var.get().strip()}"
        if new_channel and new_channel not in self.channel_buttons:
            self.add_channel_button(new_channel)
        self.popup.destroy()

    def cancel_create_channel(self):
        self.popup.destroy()

    def center_window(self, window):
        window.update_idletasks()
        width = window.winfo_width()
        height = window.winfo_height()
        x = (window.winfo_screenwidth() // 2) - (width // 2)
        y = (window.winfo_screenheight() // 2) - (height // 2)
        window.geometry(f"+{x}+{y}")
