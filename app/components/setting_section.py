# app/dashboard/settings_section.py
import customtkinter as ctk


class SettingsSection(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master, height=40, fg_color="transparent")

        self.create_widgets()

    def create_widgets(self):
        # Settings button
        self.settings_button = ctk.CTkButton(
            self,
            text="⚙️",
            width=30,
            fg_color="transparent",
            text_color="black",
            command=self.open_settings,
        )
        self.settings_button.pack(side="left", padx=20, pady=10)

    def open_settings(self):
        # Placeholder for settings functionality
        print("Settings button clicked")
