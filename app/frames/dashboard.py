# app/dashboard/dashboard.py
import customtkinter as ctk
from app.frames.frame import Frame
from app.components.announcement_section import AnnouncementSection
from app.components.activity_section import ActivitySection
from app.components.chart_section import ChartSection
from app.components.setting_section import SettingsSection


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

        self.activity_section = ActivitySection(self.left_frame)
        self.activity_section.pack(fill="both", expand=True)

        self.progress_chart = ChartSection(
            self.right_frame,
            "Current Progress",
            {"Todo": 50, "Doing": 30, "DONE": 10, "Requirement": 10},
            {
                "Todo": "#3483eb",
                "Doing": "#4dc6ff",
                "DONE": "#57e5a1",
                "Requirement": "#e5e5e5",
            },
        )
        self.progress_chart.pack(fill="x", pady=(0, 20), ipady=20)

        self.ownership_chart = ChartSection(
            self.right_frame,
            "Each task take owner",
            {"Alex": 50, "D": 30, "Jon": 10, "Thun": 10},
            {"Alex": "#3483eb", "D": "#4dc6ff", "Jon": "#57e5a1", "Thun": "#e5e5e5"},
        )
        self.ownership_chart.pack(fill="both", expand=True)

        self.settings_section = SettingsSection(self)
        self.settings_section.pack(fill="x", side="bottom")

    def set_guildId(self, guildId):
        self._guildId = guildId
        if hasattr(self, "announcement_section"):
            self.announcement_section.set_guildId(guildId)
