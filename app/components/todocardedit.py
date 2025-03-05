import customtkinter as ctk
import tkinter as tk
from tkcalendar import Calendar
from datetime import datetime
import requests
from CTkMessagebox import CTkMessagebox
from app.tokenmanager import TokenManger


class TodoCardEditing(ctk.CTkToplevel):
    def __init__(
        self,
        master,
        configuration,
        task_data,
        refresh_callback=None,
        bar_refresh_callback=None,
    ):
        super().__init__(master)
        self.__master = master
        self.__configuration = configuration
        self.__task_data = task_data
        self.__refresh_callback = refresh_callback
        self.__bar_refresh_callback = bar_refresh_callback
        self.__editing_fields = {}  # Store editing widgets
        self.__original_values = {}  # Store original values

        self.title("Edit Task")
        self.geometry("400x600")  # Increased height for more fields
        self.configure(fg_color=configuration.colors["snow-white"])
        self.overrideredirect(True)

        # Set up focus and grab immediately
        self.focus_set()
        self.grab_set()
        self.lift()  # Bring to front

        self.create_widgets()
        self.create_close_button()

        self.bind("<Escape>", self.__close_dialog)
        # Bind focus events to handle alt+tab
        self.bind("<FocusIn>", self.__handle_focus_in)
        self.bind("<FocusOut>", self.__handle_focus_out)

    def create_close_button(self):
        """Create a button frame with Save Changes and Close buttons"""
        button_frame = ctk.CTkFrame(self, fg_color="transparent")
        button_frame.pack(side="bottom", pady=10)

        # Save Changes button
        save_button = ctk.CTkButton(
            button_frame,
            text="Save Changes",
            command=self.__save_changes,
            fg_color=self.__configuration.colors["black-text"],
            text_color=self.__configuration.colors["white-text"],
            width=120,
        )
        save_button.pack(side="left", padx=5)

        # Close button
        close_button = ctk.CTkButton(
            button_frame,
            text="Close",
            command=self.__close_dialog,
            fg_color=self.__configuration.colors["black-text"],
            text_color=self.__configuration.colors["white-text"],
            width=120,
        )
        close_button.pack(side="left", padx=5)

    def create_widgets(self):
        # Main container frame
        pass

    def __handle_focus_in(self, event):
        """Handle when the window gains focus"""
        try:
            self.focus_set()
            self.grab_set()
            self.lift()
        except tk.TclError:
            pass

    def __handle_focus_out(self, event):
        """Handle when the window loses focus"""
        try:
            self.focus_set()
            self.grab_set()
            self.lift()
        except tk.TclError:
            pass

    def __save_changes(self, event=None):
        pass

    def __close_dialog(self, event=None):
        """Close the dialog safely"""
        try:
            # Release grab before destroying
            self.grab_release()
            # Set focus back to master if it exists
            if self.__master and self.__master.winfo_exists():
                self.__master.focus_set()
            self.destroy()
        except tk.TclError:
            # If there's an error, just destroy
            self.destroy()
