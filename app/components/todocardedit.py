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
            "description": task_data.get("description", ""),
            "due_date": task_data["due_date"],
            "announce_date": task_data["announce_date"],
            "assignee": task_data["assignee"],
        }
        self.__users = {}  # Store users data
        self.__fetch_users()  # Fetch users when dialog opens

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

    def __fetch_users(self):
        """Fetch all users from the backend"""
        try:
            # Prepare headers
            headers = {
                "Content-Type": "application/json",
            }

            # Send GET request to fetch users
            response = requests.get(
                f"{self.__configuration.api_url}/users/get_all_users/", headers=headers
            )

            if response.status_code == 200:
                users_data = response.json()
                # Create a dictionary with username as key and user object as value
                self.__users = {user["username"]: user for user in users_data}
                # Add "None" option for no assignee
                self.__users["None"] = None
            else:
                print(f"Failed to fetch users: {response.status_code}")
        except Exception as e:
            print(f"Error fetching users: {e}")

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

        # Title label with fixed position
        title_label = ctk.CTkLabel(
            main_container,
            text=self.__task_data["title"],
            font=ctk.CTkFont(self.__configuration.font, size=20, weight="bold"),
        )
        title_label.pack(pady=10, anchor="w", padx=20)  # Align to left with padding
        title_label.bind("<Enter>", lambda e: self.__on_hover_enter(e))
        title_label.bind("<Leave>", lambda e: self.__on_hover_leave(e))
        title_label.bind(
            "<Button-1>", lambda e: self.__show_text_editor(title_label, "title")
        )

        # line separator
        line_separator = ttk.Separator(main_container, orient="horizontal")
        line_separator.pack(fill="x", pady=10)

        """Assignee Selection"""
        # Assignee frame
        assignee_frame = ctk.CTkFrame(main_container, fg_color="transparent")
        assignee_frame.pack(fill="x", pady=5)

        # Assignee label
        assignee_label = ctk.CTkLabel(
            assignee_frame,
            text="Assignee:",
            font=ctk.CTkFont(self.__configuration.font, size=12),
        )
        assignee_label.pack(side="left", padx=5)

        # Assignee combobox
        self.__assignee_combo = ctk.CTkComboBox(
            assignee_frame,
            values=list(self.__users.keys()),
            font=ctk.CTkFont(self.__configuration.font, size=12),
            width=200,
        )
        self.__assignee_combo.pack(side="left", padx=5)

        # Set current assignee
        current_assignee = self.__task_data.get("assignee")
        if current_assignee:
            # Handle both string and dictionary assignee values
            if isinstance(current_assignee, dict):
                assignee_id = current_assignee.get("id")
            else:
                assignee_id = current_assignee

            # Find the username for the current assignee ID
            for username, user in self.__users.items():
                if user and user.get("id") == assignee_id:
                    self.__assignee_combo.set(username)
                    break
        else:
            self.__assignee_combo.set("None")

        """Task description"""
        # Task description label
        text_description = ctk.CTkTextbox(
            main_container,
            font=ctk.CTkFont(self.__configuration.font, size=12),
            height=150,  # Set a fixed height
        )
        # Only insert text if description exists and is not empty
        if self.__task_data.get("description"):
            text_description.insert("1.0", self.__task_data["description"])
        text_description.pack(fill="x", pady=10)  # Changed from fill="both" to fill="x"

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
        self.due_date_label = ctk.CTkLabel(
            date_frame,
            text=f"Due: {self.__date_formatter(self.__task_data['due_date'])}",
            font=ctk.CTkFont(self.__configuration.font, size=12),
        )
        self.due_date_label.pack(pady=5)
        self.due_date_label.bind("<Enter>", lambda e: self.__on_hover_enter(e))
        self.due_date_label.bind("<Leave>", lambda e: self.__on_hover_leave(e))
        self.due_date_label.bind(
            "<Button-1>", lambda e: self.__show_date_picker(e, "due_date")
        )

        # Announce date label vertically
        self.announce_date_label = ctk.CTkLabel(
            date_frame,
            text=f"Announce: {self.__date_formatter(self.__task_data['announce_date'])}",
            font=ctk.CTkFont(self.__configuration.font, size=12),
        )
        self.announce_date_label.pack(pady=5)
        self.announce_date_label.bind("<Enter>", lambda e: self.__on_hover_enter(e))
        self.announce_date_label.bind("<Leave>", lambda e: self.__on_hover_leave(e))
        self.announce_date_label.bind(
            "<Button-1>", lambda e: self.__show_date_picker(e, "announce_date")
        )

    def __show_text_editor(self, label, field_name):
        """Show text entry for editing"""
        # Get the label's position and size
        x, y = label.winfo_x(), label.winfo_y()
        width, height = label.winfo_width(), label.winfo_height()

        # Create entry widget with same position and size
        entry = ctk.CTkEntry(
            label.master,
            font=ctk.CTkFont(self.__configuration.font, size=20, weight="bold"),
            fg_color=self.__configuration.colors["snow-white"],
            border_width=1,
            width=width,
            height=height,
        )
        entry.insert(0, self.__task_data[field_name])
        entry.place(x=x, y=y)  # Use place instead of pack for precise positioning
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
        label.place_forget()

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

            # Show the label again with pack
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

            # Show the label again with pack
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
        """Save the selected date to UI only"""
        try:
            # Convert the date string to a datetime object
            date_obj = datetime.strptime(new_date, "%m/%d/%y")
            # Format it as YYYY-MM-DD for backend
            formatted_date = date_obj.strftime("%Y-%m-%d")
            # Format it as YYYY-MM-DDT00:00:00Z for UI display
            display_date = f"{formatted_date}T00:00:00Z"

            # Update only the task data
            self.__task_data[field_name] = formatted_date

            # Update the label based on the field name
            if field_name == "due_date":
                self.due_date_label.configure(
                    text=f"Due: {self.__date_formatter(display_date)}"
                )
            elif field_name == "announce_date":
                self.announce_date_label.configure(
                    text=f"Announce: {self.__date_formatter(display_date)}"
                )

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
                    original_value = self.__original_values.get(field)
                    current_value = self.__task_data.get(field)

                    # Compare values and add to changed_data if different
                    if original_value != current_value:
                        changed_data[field] = current_value

            # Check for assignee changes
            selected_username = self.__assignee_combo.get()
            selected_user = self.__users.get(selected_username)
            current_assignee = self.__task_data.get("assignee")

            if selected_user != current_assignee:
                if selected_user:
                    changed_data["assignee"] = selected_user["id"]
                else:
                    changed_data["assignee"] = None

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

    def __date_formatter(self, date):
        """Format date to user-friendly string, handling multiple input formats"""
        if date is None:
            return "No date"

        try:
            # Try parsing as full datetime with timezone
            if "T" in date:
                if "." in date:  # Format with milliseconds
                    fmt = "%Y-%m-%dT%H:%M:%S.%fZ"
                else:  # Format without milliseconds
                    fmt = "%Y-%m-%dT%H:%M:%SZ"
                utc_time = datetime.strptime(date, fmt)
            else:
                # Try parsing as simple date
                utc_time = datetime.strptime(date, "%Y-%m-%d")

            # Convert to local timezone
            local_tz = pytz.timezone("Asia/Bangkok")
            local_time = utc_time.replace(tzinfo=pytz.utc).astimezone(local_tz)

            # Format for readability
            return local_time.strftime("%A, %B %d, %Y %I:%M %p %Z")
        except ValueError as e:
            print(f"Error formatting date {date}: {e}")
            return "Invalid date format"
