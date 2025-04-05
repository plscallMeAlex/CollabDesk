import customtkinter as ctk
import requests


class MemberBar(ctk.CTkToplevel):
    def __init__(self, master, configuration, guild_id, **kwargs):
        super().__init__(master, **kwargs)
        self.master = master
        self.guild_id = guild_id
        self.configuration = configuration
        self.member_list = self.fetch_members()

        # Configure the top-level window appearance
        self.configure(
            fg_color=self.master.configuration.colors["frame-color-secondary"]
        )
        self.geometry("300x400")  # Set the size of the window
        self.title("Member List")  # Title of the window

        # Create widgets
        self.create_widgets()

    def create_widgets(self):
        """Create widgets for the member bar"""

        # frame for the member list
        self.member_list_frames = ctk.CTkFrame(
            self,
            fg_color=self.configuration.colors["frame-color-main"],
            corner_radius=10,
        )
        self.member_list_frames.pack(fill="both", expand=True, padx=10, pady=10)

        self.member_list_label = ctk.CTkLabel(
            self.member_list_frames,
            text="Members",
            font=("Inter", 16, "bold"),
            text_color=self.configuration.colors["black-text"],
        )
        self.member_list_label.pack(pady=(10, 0))

        # Create a scrollable frame for the member list
        self.member_list_frame = ctk.CTkScrollableFrame(
            self.member_list_frames,
            fg_color="transparent",
            scrollbar_button_color=self.configuration.colors["frame-color-secondary"],
            scrollbar_button_hover_color="black",
        )
        self.member_list_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Add members to the scrollable frame
        for member in self.member_list:
            self.add_member_card(member)

    def add_member_card(self, member):
        """Add a member inside a card-style frame"""
        username = member["username"]

        # Create card frame
        member_card = ctk.CTkFrame(
            self.member_list_frame,
            fg_color="#f0f0f0",
            corner_radius=8,
            border_width=1,
            border_color="#ddd",
        )
        member_card.pack(fill="x", padx=5, pady=5)

        # Icon label (emoji or image)
        icon_label = ctk.CTkLabel(
            member_card,
            text="👤",
            font=("Arial", 16),
            width=10,
        )
        icon_label.pack(side="left", padx=10, pady=5)

        # Username label
        username_label = ctk.CTkLabel(
            member_card,
            text=username,
            font=("Inter", 14),
            anchor="w",
        )
        username_label.pack(side="left", padx=10, pady=5, expand=True)

    def fetch_members(self):
        """Fetch members of the current guild"""
        try:
            params = {"guild_id": self.guild_id}
            response = requests.get(
                f"{self.configuration.api_url}/users/get_users_by_guild/", params=params
            )
            if response.status_code == 200:
                return response.json()
        except requests.RequestException as e:
            print(f"Error fetching members: {e}")
        return []
