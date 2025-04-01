import customtkinter as ctk
import requests
from tkinter import StringVar, Toplevel, ttk
from PIL import Image
import os


class ChannelBar(ctk.CTkFrame):
    def __init__(self, parent, configuration, change_frame_callback, guildId):
        super().__init__(parent)
        self._conguration = configuration
        self.configure(width=250, corner_radius=10)
        self.change_frame_callback = change_frame_callback
        self.__guildId = guildId
        guild_name = self.fetch_guild_name()

        self.server_label = ctk.CTkLabel(
            self,
            text=guild_name,
            font=("Inter", 16, "bold"),
            text_color="black",
            anchor="w",
        )
        self.server_label.pack(fill="x", padx=10, pady=10)
        # separator
        style = ttk.Style()
        style.configure("Black.TSeparator", background="black")

        self.separator = ttk.Separator(
            self, orient="horizontal", style="Black.TSeparator"
        )
        self.separator.pack(fill="x", padx=10, pady=(0, 10))

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
        self.bulletin_btn.pack(fill="x", padx=10, pady=5)

        # separator
        self.separator = ttk.Separator(
            self, orient="horizontal", style="Black.TSeparator"
        )
        self.separator.pack(fill="x", padx=10)

        self.channel_label = ctk.CTkLabel(
            self,
            text="TEXT CHANNELS",
            font=("Inter", 12, "bold"),
            text_color="black",
            anchor="w",
        )
        self.channel_label.pack(fill="x", padx=10, pady=(10, 5))

        self.channels_frame = ctk.CTkFrame(self)
        self.channels_frame.pack(fill="both", expand=True)

        self.channels = self.__fetch_channels_in_guild()

        for channel in self.channels:
            self.pack_channel_btn(channel)

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

    def __fetch_channels_in_guild(self):
        try:
            params = {"guild_id": self.__guildId}
            response = requests.get(
                f"{self._conguration.api_url}/channels/get_all_channel_by_guild/",
                params=params,
            )
            if response.status_code == 200:
                return response.json()
            else:
                print(f"Error fetching channels: {response.status_code}")
        except requests.RequestException as e:
            print(f"Request failed: {e}")
        return self.__init_channel()

    def __init_channel(self):
        channels = ["# general", "# team1", "# team2"]
        response_obj = []
        for channel in channels:
            payload = {"name": channel, "guild": self.__guildId}
            response = requests.post(
                f"{self._conguration.api_url}/channels/create_channel/", json=payload
            )
            if response.status_code == 201:
                print(f"Channel {channel} created successfully.")
                response_obj.append(response.json())
            else:
                print(f"Error creating channel {channel}: {response.status_code}")
        return response_obj

    def pack_channel_btn(self, channel):
        channel_name = channel["name"] if isinstance(channel, dict) else channel

        btn = ctk.CTkButton(
            self.channels_frame,
            text=channel_name,
            text_color="black",
            fg_color="transparent",
            hover_color="gray",
            anchor="w",
            command=lambda txt="TextChannel", ch=channel: self.change_frame_callback(
                txt, ch
            ),
        )
        btn.pack(fill="x", padx=10, pady=2)

    def refresh_channels(self, guild_id):
        # Update current guild
        self.__guildId = guild_id
        guild_name = self.fetch_guild_name()
        self.server_label.configure(text=guild_name)

        # Clear existing buttons
        for widget in self.channels_frame.winfo_children():
            widget.destroy()

        # Fetch and repopulate channels
        self.channels = self.__fetch_channels_in_guild()
        for channel in self.channels:
            self.pack_channel_btn(channel)

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
            font=("Inter", 24, "bold"),
            text_color="black",
        )
        self.title_label.pack(pady=(20, 10))

        self.name_label = ctk.CTkLabel(
            self.main_frame,
            text="CHANNEL NAME",
            font=("Inter", 12),
            text_color="#B5BAC1",
        )
        self.name_label.pack(pady=(20, 5), padx=20, anchor="w")

        self.channel_name_var = StringVar()
        self.channel_entry = ctk.CTkEntry(
            self.main_frame,
            font=("Inter", 14),
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
            font=("Inter", 14),
            fg_color="#2B2D31",
            hover_color="#404249",
            command=self.create_channel,
        )
        self.create_btn.pack(side="left", padx=10)

        self.cancel_btn = ctk.CTkButton(
            self.button_frame,
            text="Cancel",
            font=("Inter", 14),
            fg_color="#2B2D31",
            hover_color="#404249",
            command=self.cancel_create_channel,
        )
        self.cancel_btn.pack(side="right", padx=10)

    def create_channel(self):
        new_channel_name = self.channel_name_var.get().strip()
        new_channel = f"# {new_channel_name}"

        # Create new channel on the server
        try:
            payload = {"name": new_channel, "guild": self.__guildId}
            response = requests.post(
                f"{self._conguration.api_url}/channels/create_channel/", json=payload
            )

            if response.status_code == 201:
                channel_data = response.json()
                self.pack_channel_btn(channel_data)
                print(f"Channel {new_channel} created successfully.")
            else:
                # If API fails, still add channel to UI for demo purposes
                self.pack_channel_btn(new_channel)
                print(f"Error creating channel {new_channel}: {response.status_code}")
        except Exception as e:
            # If API fails, still add channel to UI for demo purposes
            self.pack_channel_btn(new_channel)
            print(f"Error creating channel: {e}")

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

    def fetch_guild_name(self):
        try:
            params = {"guild_id": self.__guildId}
            response = requests.get(
                f"{self._conguration.api_url}/guilds/get_guild_by_id/", params=params
            )
            if response.status_code == 200:
                return response.json()["name"]
            else:
                print(f"Error fetching guild name: {response.status_code}")
        except requests.RequestException as e:
            print(f"Request failed: {e}")
        return "Unknown Guild"
