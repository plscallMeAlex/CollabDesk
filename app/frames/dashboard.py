import customtkinter as ctk
from app.frames.frame import Frame
from app.components.announcement_section import AnnouncementSection
from app.components.activity_section import ActivitySection
from app.components.chart_section import ChartSection
from app.components.setting_section import SettingsSection
import requests
import math


class Dashboard(Frame):
    def __init__(self, master, configuration, guildId=None, **kwargs):
        super().__init__(master, configuration, guildId, **kwargs)
        self.configure(fg_color="#f5f5f5")

        # Main content area - split into left and right sections
        self.content_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.content_frame.pack(fill="both", expand=True, padx=20, pady=20)

        # Left section
        self.left_frame = ctk.CTkFrame(self.content_frame, fg_color="transparent")
        self.left_frame.pack(side="left", fill="both", expand=True, padx=(0, 10))

        # Right section
        self.right_frame = ctk.CTkFrame(self.content_frame, fg_color="transparent")
        self.right_frame.pack(side="right", fill="both", expand=True, padx=(10, 0))

        # Initialize components
        self.announcement_section = AnnouncementSection(
            self.left_frame, self._configuration, self._guildId
        )
        self.announcement_section.pack(fill="x", pady=(0, 20))

        self.activity_section = ActivitySection(
            self.left_frame, self._configuration, self._guildId
        )
        self.activity_section.pack(fill="both", expand=True)

        # Fetch progress chart data
        progress_data, progress_colors = self.fetch_progress_chart_data()
        self.progress_chart = ChartSection(
            self.right_frame, "Current Progress", progress_data, progress_colors
        )
        self.progress_chart.pack(fill="x", pady=(0, 20), ipady=20)

        self.ownership_chart = ChartSection(
            self.right_frame,
            "Each task take owner",
            {"Alex": 50, "D": 30, "Jon": 10, "Thun": 10},
            {"Alex": "#3483eb", "D": "#4dc6ff", "Jon": "#57e5a1", "Thun": "#e5e5e5"},
        )
        self.ownership_chart.pack(fill="both", expand=True)

        # self.settings_section = SettingsSection(self)
        # self.settings_section.pack(fill="x", side="bottom")

    def set_guildId(self, guildId):
        self._guildId = guildId
        if hasattr(self, "announcement_section"):
            self.announcement_section.set_guildId(guildId)
        # Update charts when guild ID changes
        if hasattr(self, "progress_chart"):
            progress_data, progress_colors = self.fetch_progress_chart_data()
            self.progress_chart.update_data(progress_data, progress_colors)

    def fetch_progress_chart_data(self):
        """
        Fetch data for the progress chart from the endpoints.
        Calculate the percentage of tasks in each state.
        """
        if not self._guildId:
            # Return default data if no guild ID is set
            return (
                {"Todo": 50, "Doing": 30, "DONE": 10, "Requirement": 10},
                {
                    "Todo": "#3483eb",
                    "Doing": "#4dc6ff",
                    "DONE": "#57e5a1",
                    "Requirement": "#e5e5e5",
                },
            )

        try:
            # Get base URL from configuration
            base_url = self._configuration.api_url

            # Fetch all states in the guild
            states_response = requests.get(
                f"{base_url}/taskstates/get_all_states/",
                params={"guild_id": self._guildId},
            )
            states_response.raise_for_status()
            states = states_response.json()

            # Fetch all tasks in the guild
            all_tasks_response = requests.get(
                f"{base_url}/tasks/in_guild/", params={"guild_id": self._guildId}
            )
            all_tasks_response.raise_for_status()
            all_tasks = all_tasks_response.json()
            total_tasks = len(all_tasks)

            if total_tasks == 0:
                # Return default data if there are no tasks
                return ({"No Tasks": 100}, {"No Tasks": "#e5e5e5"})

            # Fetch tasks for each state and calculate percentages
            progress_data = {}
            progress_colors = {}

            # Define a list of colors to use
            colors = [
                "#3483eb",
                "#4dc6ff",
                "#57e5a1",
                "#e5e5e5",
                "#ff9a54",
                "#ff5478",
                "#a78bfa",
            ]

            for i, state in enumerate(states):

                state_id = state.get("id")
                state_name = state.get("title")

                # Skip if state_id or state_name is missing
                if not state_id or not state_name:
                    continue

                # Fetch tasks in this state
                state_tasks_response = requests.get(
                    f"{base_url}/tasks/in_guild_by_state/",
                    params={"state_id": state_id},
                )
                state_tasks_response.raise_for_status()
                state_tasks = state_tasks_response.json()

                # Calculate percentage and round to 1 decimal point
                state_percentage = (len(state_tasks) / total_tasks) * 100
                state_percentage = (
                    math.ceil(state_percentage * 10) / 10
                )  # Round up to 1 decimal place

                # Add to progress data
                progress_data[state_name] = state_percentage

                # Assign a color (cycle through colors if there are more states than colors)
                color_index = i % len(colors)
                progress_colors[state_name] = colors[color_index]

            return progress_data, progress_colors

        except Exception as e:
            print(f"Error fetching progress chart data: {e}")
            # Return default data in case of error
            return (
                {"Todo": 50, "Doing": 30, "DONE": 10, "Requirement": 10},
                {
                    "Todo": "#3483eb",
                    "Doing": "#4dc6ff",
                    "DONE": "#57e5a1",
                    "Requirement": "#e5e5e5",
                },
            )
