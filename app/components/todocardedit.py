from datetime import datetime
import pytz
import customtkinter as ctk
import tkinter as tk
from tkinter import ttk
from tkcalendar import Calendar
from datetime import datetime
import requests
from CTkMessagebox import CTkMessagebox


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
        self.__original_values = {
            "title": task_data["title"],
            "description": task_data["description"],
            "due_date": task_data["due_date"],
            "announce_date": task_data["announce_date"],
        }

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
        title_label.bind(
            "<Button-1>", lambda e: self.__show_text_editor(title_label, "title")
        )

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
        due_date_label.bind(
            "<Button-1>", lambda e: self.__show_date_picker(e, "due_date")
        )

        # Announce date label vertically
        announce_date_label = ctk.CTkLabel(
            date_frame,
            text=f"Announce: {self.__date_formatter(self.__task_data['announce_date'])}",
            font=ctk.CTkFont(self.__configuration.font, size=12),
        )
        announce_date_label.pack(pady=5)
        announce_date_label.bind("<Enter>", lambda e: self.__on_hover_enter(e))
        announce_date_label.bind("<Leave>", lambda e: self.__on_hover_leave(e))
        announce_date_label.bind(
            "<Button-1>", lambda e: self.__show_date_picker(e, "announce_date")
        )

    def __show_text_editor(self, label, field_name):
        """Show text entry for editing"""
        # Create entry widget
        entry = ctk.CTkEntry(
            label.master,
            font=ctk.CTkFont(self.__configuration.font, size=20, weight="bold"),
            fg_color=self.__configuration.colors["snow-white"],
            border_width=1,
        )
        entry.insert(0, self.__task_data[field_name])
        entry.pack(pady=10)
        entry.focus_set()
        entry.focus_force()

        # Store original widget and value
        self.__editing_fields[field_name] = entry
        self.__original_values[field_name] = self.__task_data[field_name]

        # Bind events
        entry.bind(
            "<Return>", lambda e: self.__save_text_value(entry.get(), field_name)
        )
        entry.bind("<Escape>", lambda e: self.__cancel_text_edit(field_name))

        # Hide the label
        label.pack_forget()

    def __save_text_value(self, new_value, field_name):
        """Save the text value"""
        try:
            # Update the task data
            self.__task_data[field_name] = new_value

            # Update the label text
            label = self.__editing_fields[field_name].master.winfo_children()[0]
            label.configure(text=new_value)

            # Remove the entry widget
            self.__editing_fields[field_name].destroy()
            del self.__editing_fields[field_name]
            del self.__original_values[field_name]

            # Show the label again
            label.pack(pady=10)
        except Exception as e:
            print(f"Error saving text: {e}")
            CTkMessagebox(
                title="Error",
                message="Failed to save text",
                icon="cancel",
            )

    def __cancel_text_edit(self, field_name):
        """Cancel text editing"""
        try:
            # Restore original value
            self.__task_data[field_name] = self.__original_values[field_name]

            # Update the label text
            label = self.__editing_fields[field_name].master.winfo_children()[0]
            label.configure(text=self.__original_values[field_name])

            # Remove the entry widget
            self.__editing_fields[field_name].destroy()
            del self.__editing_fields[field_name]
            del self.__original_values[field_name]

            # Show the label again
            label.pack(pady=10)
        except Exception as e:
            print(f"Error canceling text edit: {e}")

    def __show_date_picker(self, event, field_name):
        """Show date picker for editing"""
        # Create a new top-level window for the date picker
        picker_window = ctk.CTkToplevel(self)
        picker_window.title("Select Date")
        picker_window.geometry("300x400")
        picker_window.transient(self)  # Make it modal
        picker_window.grab_set()  # Grab focus

        # Create calendar
        cal = Calendar(
            picker_window,
            selectmode="day",
            year=datetime.now().year,
            month=datetime.now().month,
            day=datetime.now().day,
        )
        cal.pack(pady=10)

        # Create buttons frame
        button_frame = ctk.CTkFrame(picker_window, fg_color="transparent")
        button_frame.pack(pady=10)

        # Save button
        save_button = ctk.CTkButton(
            button_frame,
            text="Save",
            command=lambda: self.__save_date_value(
                cal.get_date(), field_name, picker_window
            ),
            fg_color=self.__configuration.colors["black-text"],
            text_color=self.__configuration.colors["white-text"],
            width=100,
        )
        save_button.pack(side="left", padx=5)

        # Cancel button
        cancel_button = ctk.CTkButton(
            button_frame,
            text="Cancel",
            command=picker_window.destroy,
            fg_color=self.__configuration.colors["black-text"],
            text_color=self.__configuration.colors["white-text"],
            width=100,
        )
        cancel_button.pack(side="left", padx=5)

    def __save_date_value(self, new_date, field_name, picker_window):
        """Save the selected date"""
        try:
            # Convert the date string to a datetime object
            date_obj = datetime.strptime(new_date, "%m/%d/%y")
            # Format it as YYYY-MM-DD
            formatted_date = date_obj.strftime("%Y-%m-%d")

            # Update the task data
            self.__task_data[field_name] = formatted_date

            # Update the label text
            for widget in self.winfo_children():
                if isinstance(widget, ctk.CTkFrame):
                    for child in widget.winfo_children():
                        if isinstance(child, ctk.CTkFrame):  # date_frame
                            for label in child.winfo_children():
                                if isinstance(label, ctk.CTkLabel):
                                    if field_name in label.cget("text").lower():
                                        label.configure(
                                            text=f"{field_name.title()}: {self.__date_formatter(formatted_date)}"
                                        )
                                        break

            # Close the picker window
            picker_window.destroy()
        except Exception as e:
            print(f"Error saving date: {e}")
            CTkMessagebox(
                title="Error",
                message="Failed to save date",
                icon="cancel",
            )

    def __save_changes(self, event=None):
        """Save all changes to the backend via PATCH request"""
        try:
            # Create a dictionary to store only the changed fields
            changed_data = {}

            # Check for changes in fields we allow editing
            editable_fields = ["title", "description", "due_date", "announce_date"]
            for field in editable_fields:
                # For description, we need to get it from the textbox widget
                if field == "description":
                    # Find the textbox in the main container
                    for widget in self.winfo_children():
                        if isinstance(widget, ctk.CTkFrame):  # Main container
                            for child in widget.winfo_children():
                                if isinstance(child, ctk.CTkTextbox):
                                    # Get text and compare with original
                                    new_description = child.get("1.0", "end-1c")
                                    if (
                                        new_description
                                        != self.__task_data["description"]
                                    ):
                                        changed_data["description"] = new_description
                                        self.__task_data["description"] = (
                                            new_description
                                        )
                # For other fields, they're already updated in __task_data when edited
                else:
                    # Get the original value from the task data when it was loaded
                    if field in self.__original_values:
                        original_value = self.__original_values[field]
                        if self.__task_data[field] != original_value:
                            changed_data[field] = self.__task_data[field]

            # If no changes, show message and return
            if not changed_data:
                CTkMessagebox(
                    title="No Changes",
                    message="No changes were made to the task.",
                    icon="info",
                )
                return

            # Get the task ID
            task_id = self.__task_data["id"]

            headers = {
                "Content-Type": "application/json",
            }

            response = requests.patch(
                f"{self.__configuration.api_url}/tasks/{task_id}/update_task/",
                json=changed_data,
                headers=headers,
            )

            if response.status_code == 200:
                # Show success message
                CTkMessagebox(
                    title="Success",
                    message="Task updated successfully!",
                    icon="check",
                )

                # Call refresh callbacks if provided
                if self.__refresh_callback:
                    self.__refresh_callback()
                if self.__bar_refresh_callback:
                    self.__bar_refresh_callback()

                # Close the dialog
                self.__close_dialog()
            else:
                # Show error message
                error_msg = "Failed to update task."
                try:
                    error_data = response.json()
                    if "error" in error_data:
                        error_msg = f"Error: {error_data['error']}"
                    elif "detail" in error_data:
                        error_msg = f"Error: {error_data['detail']}"
                except:
                    pass

                CTkMessagebox(
                    title="Error",
                    message=error_msg,
                    icon="cancel",
                )

        except Exception as e:
            print(f"Error saving changes: {e}")
            CTkMessagebox(
                title="Error",
                message=f"An error occurred: {str(e)}",
                icon="cancel",
            )

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
