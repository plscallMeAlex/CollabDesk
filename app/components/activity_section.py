# app/dashboard/activity_section.py
import customtkinter as ctk
import requests
from datetime import datetime


class ActivitySection(ctk.CTkFrame):
    def __init__(self, master, configuration, guildId=None):
        super().__init__(master, fg_color="#e0e0e0", corner_radius=10)
        self._configuration = configuration
        self._guildId = guildId

        # Sample data
        self.activities = self.fetch_activities()
        self.current_activity_page = 0
        self.activities_per_page = 5

        self.create_widgets()
        self.display_activities(0)

    def fetch_activities(self):
        try:
            params = {"guild_id": self._guildId}
            response = requests.get(
                self._configuration.api_url + "/activities/get_all_activity_by_guild/",
                params=params,
            )
            if response.status_code == 200:
                activities = response.json()
                return activities
            else:
                print(f"Error fetching activities: {response.status_code}")
                return self.get_sample_activities()
        except requests.RequestException as e:
            print(f"Request error: {e}")
            return []

            # return self.get_sample_activities()

    def get_sample_activities(self):
        return [
            {
                "user": "Alex",
                "detail": "updated task 'Database integration' to 'In Progress'",
                "created_at": "Feb 26, 2025 - 10:45 AM",
            },
            {
                "user": "Jon",
                "detail": "completed task 'User authentication flow'",
                "created_at": "Feb 26, 2025 - 09:30 AM",
            },
            {
                "user": "D",
                "detail": "added comments to task 'API documentation'",
                "created_at": "Feb 25, 2025 - 04:15 PM",
            },
            {
                "user": "Thun",
                "detail": "created new task 'Frontend testing'",
                "created_at": "Feb 25, 2025 - 02:20 PM",
            },
            {
                "user": "Alex",
                "detail": "completed task 'Login page design'",
                "created_at": "Feb 25, 2025 - 11:05 AM",
            },
            {
                "user": "D",
                "detail": "updated task 'Backend optimization' to 'In Progress'",
                "created_at": "Feb 24, 2025 - 03:40 PM",
            },
            {
                "user": "Jon",
                "detail": "commented on task 'Mobile responsiveness'",
                "created_at": "Feb 24, 2025 - 01:15 PM",
            },
            {
                "user": "Thun",
                "detail": "assigned task 'Security audit' to Alex",
                "created_at": "Feb 24, 2025 - 11:30 AM",
            },
            {
                "user": "Alex",
                "detail": "updated task 'User profile page' to 'Done'",
                "created_at": "Feb 23, 2025 - 04:50 PM",
            },
            {
                "user": "D",
                "detail": "created task 'Database optimization'",
                "created_at": "Feb 23, 2025 - 02:10 PM",
            },
        ]

    def create_widgets(self):
        # Header section
        self.header = ctk.CTkFrame(self, fg_color="transparent", height=40)
        self.header.pack(fill="x")

        self.title_label = ctk.CTkLabel(
            self.header,
            text="Recent Activities",
            font=("Arial", 16, "bold"),
            fg_color="transparent",
        )
        self.title_label.pack(side="left", padx=20, pady=10)

        # Navigation buttons
        self.nav_buttons = ctk.CTkFrame(self.header, fg_color="transparent")
        self.nav_buttons.pack(side="right", padx=20)

        self.prev_activities_btn = ctk.CTkButton(
            self.nav_buttons,
            text="◀",
            width=30,
            fg_color="#d0d0d0",
            text_color="black",
            corner_radius=5,
            command=self.prev_activities_page,
        )
        self.prev_activities_btn.pack(side="left", padx=5)

        self.next_activities_btn = ctk.CTkButton(
            self.nav_buttons,
            text="▶",
            width=30,
            fg_color="#d0d0d0",
            text_color="black",
            corner_radius=5,
            command=self.next_activities_page,
        )
        self.next_activities_btn.pack(side="left", padx=5)

        # Activities content area
        self.activities_content = ctk.CTkFrame(self, fg_color="white", corner_radius=5)
        self.activities_content.pack(fill="both", expand=True, padx=20, pady=(0, 20))

    def display_activities(self, page):
        # Clear existing activities
        for widget in self.activities_content.winfo_children():
            widget.destroy()

        # Calculate start and end indices
        start_idx = page * self.activities_per_page
        end_idx = min(start_idx + self.activities_per_page, len(self.activities))

        # Display activities for current page
        for i in range(start_idx, end_idx):
            activity = self.activities[i]

            # Create activity item frame
            activity_item = ActivityItem(
                self.activities_content,
                activity["user"],
                activity["detail"],
                activity["created_at"],
                is_first=(i == start_idx),
            )
            activity_item.pack(fill="x", padx=10, pady=5)

        # Update current page
        self.current_activity_page = page

        # Update button states
        self.prev_activities_btn.configure(state="normal" if page > 0 else "disabled")
        self.next_activities_btn.configure(
            state="normal" if end_idx < len(self.activities) else "disabled"
        )

        # Show "Show More" button if there are more pages
        if end_idx < len(self.activities):
            show_more_btn = ctk.CTkButton(
                self.activities_content,
                text="Show More",
                fg_color="#3483eb",
                corner_radius=5,
                command=self.next_activities_page,
            )
            show_more_btn.pack(pady=10)

    def prev_activities_page(self):
        if self.current_activity_page > 0:
            self.display_activities(self.current_activity_page - 1)

    def next_activities_page(self):
        total_pages = (
            len(self.activities) + self.activities_per_page - 1
        ) // self.activities_per_page
        if self.current_activity_page < total_pages - 1:
            self.display_activities(self.current_activity_page + 1)


class ActivityItem(ctk.CTkFrame):
    def __init__(self, master, user, action, time, is_first=False):
        super().__init__(master, fg_color="transparent", height=70, corner_radius=0)
        self.pack_propagate(False)

        # Format the time 2025-03-30 11:50:02.098516+00 to "Mar 30, 2025 - 11:50 AM"
        format_time = datetime.fromisoformat(time.split("+")[0])
        time = format_time.strftime("%b %d, %Y - %I:%M %p")

        # Add separator except for first item
        if not is_first:
            separator = ctk.CTkFrame(self, fg_color="#e5e5e5", height=1)
            separator.pack(fill="x", pady=(0, 0))

        # User label
        self.user_label = ctk.CTkLabel(
            self,
            text=user,
            font=("Arial", 12, "bold"),
            text_color="#3483eb",
        )
        self.user_label.pack(anchor="w", padx=5, pady=(0, 0))

        # Action label
        self.action_label = ctk.CTkLabel(self, text=action, font=("Arial", 11))
        self.action_label.pack(anchor="w", padx=5, pady=(0, 0))

        # Time label
        self.time_label = ctk.CTkLabel(
            self,
            text=time,
            font=("Arial", 10),
            text_color="gray",
        )
        self.time_label.pack(anchor="w", padx=5, pady=(0, 0))
