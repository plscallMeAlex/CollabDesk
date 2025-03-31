# app/dashboard/activity_section.py
import customtkinter as ctk
import requests
from datetime import datetime
import pytz


class ActivitySection(ctk.CTkFrame):
    def __init__(self, master, configuration, guildId=None):
        super().__init__(master, fg_color="#e0e0e0", corner_radius=10)
        self._configuration = configuration
        self._guildId = guildId

        # Changed activities per page to 2
        self.activities_per_page = 2
        self.current_activity_page = 0

        # Fetch and sort activities
        self.activities = self.fetch_activities()

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
                # Sort activities by created_at date in descending order (newest first)
                sorted_activities = self.sort_activities_by_date(activities)
                return sorted_activities
            else:
                print(f"Error fetching activities: {response.status_code}")
                sample_activities = self.get_sample_activities()
                return self.sort_activities_by_date(sample_activities)
        except requests.RequestException as e:
            print(f"Request error: {e}")
            return self.sort_activities_by_date(self.get_sample_activities())

    def sort_activities_by_date(self, activities):
        # Sort activities by created_at date in descending order (newest first)
        return sorted(
            activities,
            key=lambda x: datetime.fromisoformat(x["created_at"].split("+")[0]),
            reverse=True,
        )

    def get_sample_activities(self):
        return [
            {
                "user": "Alex",
                "detail": "updated task 'Database integration' to 'In Progress'",
                "created_at": "2025-02-26 10:45:00",
            },
            {
                "user": "Jon",
                "detail": "completed task 'User authentication flow'",
                "created_at": "2025-02-26 09:30:00",
            },
            {
                "user": "D",
                "detail": "added comments to task 'API documentation'",
                "created_at": "2025-02-25 16:15:00",
            },
            {
                "user": "Thun",
                "detail": "created new task 'Frontend testing'",
                "created_at": "2025-02-25 14:20:00",
            },
            {
                "user": "Alex",
                "detail": "completed task 'Login page design'",
                "created_at": "2025-02-25 11:05:00",
            },
            {
                "user": "D",
                "detail": "updated task 'Backend optimization' to 'In Progress'",
                "created_at": "2025-02-24 15:40:00",
            },
            {
                "user": "Jon",
                "detail": "commented on task 'Mobile responsiveness'",
                "created_at": "2025-02-24 13:15:00",
            },
            {
                "user": "Thun",
                "detail": "assigned task 'Security audit' to Alex",
                "created_at": "2025-02-24 11:30:00",
            },
            {
                "user": "Alex",
                "detail": "updated task 'User profile page' to 'Done'",
                "created_at": "2025-02-23 16:50:00",
            },
            {
                "user": "D",
                "detail": "created task 'Database optimization'",
                "created_at": "2025-02-23 14:10:00",
            },
        ]

    def create_widgets(self):
        # Header section
        self.header = ctk.CTkFrame(self, fg_color="transparent", height=40)
        self.header.pack(fill="x")

        self.title_label = ctk.CTkLabel(
            self.header,
            text="Recent Activities",
            font=("Inter", 16, "bold"),
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

        # Container for activities
        activities_container = ctk.CTkFrame(
            self.activities_content, fg_color="transparent"
        )
        activities_container.pack(fill="both", expand=True, padx=0, pady=0)

        # Display activities for current page
        for i in range(start_idx, end_idx):
            activity = self.activities[i]

            # Create activity item frame
            activity_item = ActivityItem(
                activities_container,
                activity["user"],
                activity["detail"],
                activity["created_at"],
                is_first=(i == start_idx),
            )
            activity_item.pack(fill="x", padx=10, pady=0)

        # Update current page
        self.current_activity_page = page

        # Navigation controls container
        nav_container = ctk.CTkFrame(
            self.activities_content, fg_color="transparent", height=30
        )
        nav_container.pack(fill="x", pady=(5, 10))

        # Page indicator
        page_indicator = ctk.CTkLabel(
            nav_container,
            text=f"Page {page + 1} of {(len(self.activities) + self.activities_per_page - 1) // self.activities_per_page}",
            font=("Inter", 10),
            text_color="gray",
        )
        page_indicator.pack(side="left", padx=10)

        # Update button states
        self.prev_activities_btn.configure(state="normal" if page > 0 else "disabled")
        self.next_activities_btn.configure(
            state="normal" if end_idx < len(self.activities) else "disabled"
        )

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
        super().__init__(master, fg_color="transparent", height=75, corner_radius=0)
        self.pack_propagate(False)

        # Format the time to "Mar 30, 2025 - 11:50 AM"
        try:
            utc_time = datetime.fromisoformat(
                time.split("+")[0]
            )  # Convert to UTC datetime
            bangkok_tz = pytz.timezone("Asia/Bangkok")  # Define Bangkok timezone
            bangkok_time = utc_time.astimezone(bangkok_tz)  # Convert to Bangkok time
            formatted_time = bangkok_time.strftime(
                "%b %d, %Y - %I:%M %p"
            )  # Format output
        except (ValueError, TypeError) as e:
            print(f"Error formatting timestamp: {e}")
            formatted_time = time  # Fallback if time is already formatted

        # Add separator except for first item
        if not is_first:
            separator = ctk.CTkFrame(self, fg_color="#e5e5e5", height=1)
            separator.pack(fill="x")

        # Main content frame
        content_frame = ctk.CTkFrame(self, fg_color="transparent")
        content_frame.pack(fill="x", expand=True, padx=5, pady=(5, 0))

        # Top row with ID and time
        id_row = ctk.CTkFrame(content_frame, fg_color="transparent")
        id_row.pack(fill="x", expand=True)

        # ID label (left)
        self.id_label = ctk.CTkLabel(
            id_row,
            text=user,
            font=("Inter", 12, "bold"),
            text_color="#3483eb",
            anchor="w",
        )
        self.id_label.pack(side="left", fill="x")

        # Time label (right)
        self.time_label = ctk.CTkLabel(
            id_row,
            text=formatted_time,
            font=("Inter", 9),
            text_color="gray",
            anchor="e",
        )
        self.time_label.pack(side="right", fill="x")

        # Action description
        self.action_label = ctk.CTkLabel(
            content_frame,
            text=action,
            font=("Inter", 11),
            anchor="w",
            justify="left",
            wraplength=350,
        )
        self.action_label.pack(fill="x", anchor="w", pady=(2, 5))
