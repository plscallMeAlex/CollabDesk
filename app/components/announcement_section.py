import customtkinter as ctk
import requests
from datetime import datetime


class AnnouncementSection(ctk.CTkFrame):
    def __init__(self, master, configuration, guildId=None):
        super().__init__(master, fg_color="#e0e0e0", corner_radius=10)

        self._configuration = configuration
        self.guildId = guildId

        self.announcements = self.fetch_announcements()
        self.current_announcement = 0

        self.create_widgets()
        self.display_announcement(0)

    def create_widgets(self):
        # Header section
        self.header = ctk.CTkFrame(self, fg_color="transparent", height=40)
        self.header.pack(fill="x")

        self.title_label = ctk.CTkLabel(
            self.header,
            text="Team Leader Announcement",
            font=("Arial", 16, "bold"),
            fg_color="transparent",
        )
        self.title_label.pack(side="left", padx=20, pady=10)

        # Navigation buttons
        self.nav_buttons_frame = ctk.CTkFrame(self.header, fg_color="transparent")
        self.nav_buttons_frame.pack(side="right", padx=20)

        self.add_announcement_btn = ctk.CTkButton(
            self.nav_buttons_frame,
            text="+ New",
            width=80,
            fg_color="#4CAF50",
            hover_color="#45a049",
            command=self.show_new_announcement_dialog,
        )
        self.add_announcement_btn.pack(side="left", padx=5)

        self.prev_announcement_btn = ctk.CTkButton(
            self.nav_buttons_frame,
            text="◀",
            width=30,
            fg_color="#d0d0d0",
            text_color="black",
            corner_radius=5,
            command=self.prev_announcement,
        )
        self.prev_announcement_btn.pack(side="left", padx=5)

        self.next_announcement_btn = ctk.CTkButton(
            self.nav_buttons_frame,
            text="▶",
            width=30,
            fg_color="#d0d0d0",
            text_color="black",
            corner_radius=5,
            command=self.next_announcement,
        )
        self.next_announcement_btn.pack(side="left", padx=5)

        # Announcement content
        self.announcement_content_frame = ctk.CTkFrame(
            self, fg_color="white", corner_radius=5
        )
        self.announcement_content_frame.pack(
            fill="both", padx=20, pady=(0, 20), ipady=10
        )

        # Title
        self.announcement_title = ctk.CTkLabel(
            self.announcement_content_frame,
            text="",
            font=("Arial", 14, "bold"),
            fg_color="transparent",
        )
        self.announcement_title.pack(anchor="w", padx=15, pady=(15, 5))

        # Content
        self.announcement_text = ctk.CTkTextbox(
            self.announcement_content_frame,
            fg_color="transparent",
            height=150,
            wrap="word",
            activate_scrollbars=True,
        )
        self.announcement_text.pack(fill="both", expand=True, padx=15, pady=5)
        self.announcement_text.configure(state="disabled")  # Make it read-only

        # Author and date
        self.announcement_footer = ctk.CTkLabel(
            self.announcement_content_frame,
            text="",
            font=("Arial", 10),
            fg_color="transparent",
            text_color="gray",
        )
        self.announcement_footer.pack(anchor="e", padx=15, pady=(5, 15))

    def fetch_announcements(self):
        print("Fetching announcements...")
        try:
            if not self.guildId:
                return []

            params = {"guild_id": self.guildId}
            response = requests.get(
                self._configuration.api_url
                + "/announcements/get_announcements_by_guild/",
                params=params,
            )

            if response.status_code == 200:
                res = response.json()
                for announcement in res:
                    announcement["date"] = datetime.fromisoformat(
                        announcement["created_at"]
                    ).strftime("%b %d, %Y")

                res = sorted(
                    res,
                    key=lambda x: x["created_at"],
                    reverse=True,
                )
                return res
            else:
                print("Failed to fetch announcements:", response.status_code)
        except requests.RequestException as e:
            print("Error fetching announcements:", e)

        return []

    def display_announcement(self, index):
        if not self.announcements or index >= len(self.announcements):
            return

        announcement = self.announcements[index]

        self.announcement_title.configure(text=announcement["title"])

        # Clear and update text
        self.announcement_text.configure(state="normal")
        self.announcement_text.delete("0.0", "end")
        self.announcement_text.insert("0.0", announcement["content"])
        self.announcement_text.configure(state="disabled")

        # Update footer
        self.announcement_footer.configure(
            text=f"{announcement['author']} • {announcement['date']}"
        )

        # Update current index
        self.current_announcement = index

        # Update button states
        self.prev_announcement_btn.configure(
            state="normal" if index > 0 else "disabled"
        )
        self.next_announcement_btn.configure(
            state="normal" if index < len(self.announcements) - 1 else "disabled"
        )

    def prev_announcement(self):
        if self.current_announcement > 0:
            self.display_announcement(self.current_announcement - 1)

    def next_announcement(self):
        if self.current_announcement < len(self.announcements) - 1:
            self.display_announcement(self.current_announcement + 1)

    def show_new_announcement_dialog(self):
        """Show dialog for creating a new announcement"""
        dialog = ctk.CTkToplevel(self)
        dialog.title("Create New Announcement")
        dialog.geometry("500x600")
        dialog.resizable(False, False)
        dialog.grab_set()  # Make modal

        # Title field
        ctk.CTkLabel(dialog, text="Title:", font=("Arial", 12)).pack(
            pady=(10, 5), padx=20, anchor="w"
        )
        title_entry = ctk.CTkEntry(dialog, width=400)
        title_entry.pack(pady=5, padx=20, fill="x")

        # Content field
        ctk.CTkLabel(dialog, text="Content:", font=("Arial", 12)).pack(
            pady=(10, 5), padx=20, anchor="w"
        )
        content_text = ctk.CTkTextbox(dialog, height=200)
        content_text.pack(pady=5, padx=20, fill="both", expand=True)

        # Button frame
        button_frame = ctk.CTkFrame(dialog, fg_color="transparent")
        button_frame.pack(pady=10, padx=20, fill="x")

        def add_announcement():
            title = title_entry.get()
            content = content_text.get("1.0", "end-1c")
            user_id = self._configuration.load_user_data()
            if title and content:
                new_announcement = {
                    "title": title,
                    "content": content,
                    "guild": self.guildId,
                    "user": user_id,  # Could be replaced with actual username
                }
                # Send request to publish announcement
                try:
                    response = requests.post(
                        self._configuration.api_url
                        + "/announcements/create_annoucement/",
                        json=new_announcement,
                    )
                    if response.status_code == 201:
                        # Fetch new announcements
                        self.announcements = self.fetch_announcements()
                    else:
                        print("Failed to publish announcement:", response.status_code)
                except requests.RequestException as e:
                    print("Error publishing announcement:", e)

                # Add to beginning of list
                self.current_announcement = 0
                self.display_announcement(0)
                dialog.destroy()

        # Add button
        ctk.CTkButton(
            button_frame,
            text="Publish",
            fg_color="#4CAF50",
            hover_color="#45a049",
            command=add_announcement,
        ).pack(side="right", padx=5)

        # Cancel button
        ctk.CTkButton(
            button_frame,
            text="Cancel",
            fg_color="#f44336",
            hover_color="#d32f2f",
            command=dialog.destroy,
        ).pack(side="right", padx=5)

    def set_guildId(self, guildId):
        self.guildId = guildId
        self.announcements = self.fetch_announcements()
        self.display_announcement(0)
