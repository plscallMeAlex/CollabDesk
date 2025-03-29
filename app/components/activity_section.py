# app/dashboard/activity_section.py
import customtkinter as ctk


class ActivitySection(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master, fg_color="#e0e0e0", corner_radius=10)

        # Sample data
        self.activities = self.get_sample_activities()
        self.current_activity_page = 0
        self.activities_per_page = 5

        self.create_widgets()
        self.display_activities(0)

    def get_sample_activities(self):
        return [
            {
                "user": "Alex",
                "action": "updated task 'Database integration' to 'In Progress'",
                "time": "Feb 26, 2025 - 10:45 AM",
            },
            {
                "user": "Jon",
                "action": "completed task 'User authentication flow'",
                "time": "Feb 26, 2025 - 09:30 AM",
            },
            {
                "user": "D",
                "action": "added comments to task 'API documentation'",
                "time": "Feb 25, 2025 - 04:15 PM",
            },
            {
                "user": "Thun",
                "action": "created new task 'Frontend testing'",
                "time": "Feb 25, 2025 - 02:20 PM",
            },
            {
                "user": "Alex",
                "action": "completed task 'Login page design'",
                "time": "Feb 25, 2025 - 11:05 AM",
            },
            {
                "user": "D",
                "action": "updated task 'Backend optimization' to 'In Progress'",
                "time": "Feb 24, 2025 - 03:40 PM",
            },
            {
                "user": "Jon",
                "action": "commented on task 'Mobile responsiveness'",
                "time": "Feb 24, 2025 - 01:15 PM",
            },
            {
                "user": "Thun",
                "action": "assigned task 'Security audit' to Alex",
                "time": "Feb 24, 2025 - 11:30 AM",
            },
            {
                "user": "Alex",
                "action": "updated task 'User profile page' to 'Done'",
                "time": "Feb 23, 2025 - 04:50 PM",
            },
            {
                "user": "D",
                "action": "created task 'Database optimization'",
                "time": "Feb 23, 2025 - 02:10 PM",
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
                activity["action"],
                activity["time"],
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
