from datetime import datetime
import pytz
import customtkinter as ctk
import tkinter as tk
from tkinter import ttk
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
        self.resizable(False, False)

        # Set up focus and grab immediately
        self.focus_set()
        self.grab_set()
        self.lift()  # Bring to front

        self.create_widgets()
        self.create_close_button()

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
        """Main container"""
        # Main container frame
        main_container = ctk.CTkFrame(self, fg_color="transparent")
        main_container.pack(fill="both", expand=True)

        # Title label
        title_label = ctk.CTkLabel(
            main_container,
            text=self.__task_data["title"],
            font=ctk.CTkFont(self.__configuration.font, size=20, weight="bold"),
        )
        title_label.pack(pady=10)
        title_label.bind("<Enter>", lambda e: self.__on_hover_enter(e))
        title_label.bind("<Leave>", lambda e: self.__on_hover_leave(e))

        # line separator
        line_separator = ttk.Separator(main_container, orient="horizontal")
        line_separator.pack(fill="x", pady=10)

        """Task description"""
        # Task description label
        text_description = ctk.CTkTextbox(
            main_container,
            font=ctk.CTkFont(self.__configuration.font, size=12),
        )
        text_description.insert("1.0", self.__task_data["description"])
        text_description.pack(fill="both", expand=True, pady=10)

        # Date Frame for create, update, due date
        date_frame = ctk.CTkFrame(main_container, fg_color="transparent")
        date_frame.pack(fill="both", expand=True, pady=10)

        # Create date label vertically
        create_date_label = ctk.CTkLabel(
            date_frame,
            text=f"Created: {self.__date_formatter(self.__task_data['created_at'])}",
            font=ctk.CTkFont(self.__configuration.font, size=12),
        )
        create_date_label.pack(pady=5)

        # Update date label vertically
        update_date_label = ctk.CTkLabel(
            date_frame,
            text=f"Updated: {self.__date_formatter(self.__task_data['updated_at'])}",
            font=ctk.CTkFont(self.__configuration.font, size=12),
        )
        update_date_label.pack(pady=5)

        # Due date label vertically
        due_date_label = ctk.CTkLabel(
            date_frame,
            text=f"Due: {self.__date_formatter(self.__task_data['due_date'])}",
            font=ctk.CTkFont(self.__configuration.font, size=12),
        )
        due_date_label.pack(pady=5)
        due_date_label.bind("<Enter>", lambda e: self.__on_hover_enter(e))
        due_date_label.bind("<Leave>", lambda e: self.__on_hover_leave(e))

        # Announce date label vertically
        announce_date_label = ctk.CTkLabel(
            date_frame,
            text=f"Announce: {self.__date_formatter(self.__task_data['announce_date'])}",
            font=ctk.CTkFont(self.__configuration.font, size=12),
        )
        announce_date_label.pack(pady=5)
        announce_date_label.bind("<Enter>", lambda e: self.__on_hover_enter(e))
        announce_date_label.bind("<Leave>", lambda e: self.__on_hover_leave(e))

    def __save_changes(self, event=None):
        pass

    def __close_dialog(self, event=None):
        """Close the dialog safely"""
        try:
            # Only try to release grab if we're still a valid window
            if self.winfo_exists():
                self.grab_release()
                # Set focus back to master if it exists
                if self.__master and self.__master.winfo_exists():
                    self.__master.focus_set()
            self.destroy()
        except tk.TclError:
            # If there's an error, just destroy
            self.destroy()

    def __on_hover_enter(self, event):
        """Change text color when mouse enters"""
        widget = event.widget
        try:
            # For standard tkinter Labels
            if isinstance(widget, tk.Label):
                widget.configure(fg=self.__configuration.colors["green-program"])
            # For CustomTkinter CTkLabel
            elif hasattr(widget, "configure") and hasattr(widget, "_text_label"):
                widget.configure(
                    text_color=self.__configuration.colors["green-program"]
                )
            # For CustomTkinter CTkCanvas
            elif hasattr(widget, "itemconfigure"):
                # Find all text items in the canvas and change their fill color
                for item_id in widget.find_all():
                    if widget.type(item_id) == "text":
                        widget.itemconfigure(
                            item_id, fill=self.__configuration.colors["green-program"]
                        )
        except Exception as e:
            print(f"Error in hover enter: {e}")

    def __on_hover_leave(self, event):
        """Restore text color when mouse leaves"""
        widget = event.widget
        try:
            # For standard tkinter Labels
            if isinstance(widget, tk.Label):
                widget.configure(fg=self.__configuration.colors["black-text"])
            # For CustomTkinter CTkLabel
            elif hasattr(widget, "configure") and hasattr(widget, "_text_label"):
                widget.configure(text_color=self.__configuration.colors["black-text"])
            # For CustomTkinter CTkCanvas
            elif hasattr(widget, "itemconfigure"):
                # Find all text items in the canvas and restore their fill color
                for item_id in widget.find_all():
                    if widget.type(item_id) == "text":
                        widget.itemconfigure(
                            item_id, fill=self.__configuration.colors["black-text"]
                        )
        except Exception as e:
            print(f"Error in hover leave: {e}")

    # Format date belong to user's timezone
    def __date_formatter(self, date):
        # Determine the correct format
        if "." in date:
            fmt = "%Y-%m-%dT%H:%M:%S.%fZ"
        else:
            fmt = "%Y-%m-%dT%H:%M:%SZ"

        # Parse the UTC timestamp
        utc_time = datetime.strptime(date, fmt)

        # Convert to local timezone
        local_tz = pytz.timezone("Asia/Bangkok")
        local_time = utc_time.replace(tzinfo=pytz.utc).astimezone(local_tz)

        # Format for readability
        return local_time.strftime("%A, %B %d, %Y %I:%M %p %Z")
