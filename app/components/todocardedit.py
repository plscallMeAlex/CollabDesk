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
        self.__available_states = self.__fetch_available_states()

        self.title("Edit Task")
        self.geometry("400x600")  # Increased height for more fields
        self.configure(fg_color=configuration.colors["snow-white"])
        self.overrideredirect(True)

        self.create_widgets()
        self.create_close_button()

        self.bind("<Escape>", self.__close_dialog)
        self.after(10, self.__setup_focus)

    def __setup_focus(self):
        """Properly set up focus and grab"""
        try:
            self.focus_set()
            self.grab_set()
            self.lift()  # Bring to front
        except tk.TclError:
            # Handle potential errors in focus setting
            pass

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
        main_frame = ctk.CTkFrame(self, fg_color="transparent")
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)

        # Title
        self.__create_field_row(
            main_frame, "Title", self.__task_data.get("title", ""), "text"
        )

        # Description
        self.__create_field_row(
            main_frame, "Description", self.__task_data.get("description", ""), "text"
        )

        # Due Date
        due_date = self.__task_data.get("due_date", "")
        if due_date:
            try:
                due_date = datetime.strptime(due_date, "%Y-%m-%d").date()
            except ValueError:
                due_date = None
        self.__create_field_row(main_frame, "Due Date", due_date, "date")

        # Announce Date
        announce_date = self.__task_data.get("announce_date", "")
        if announce_date:
            try:
                announce_date = datetime.strptime(announce_date, "%Y-%m-%d").date()
            except ValueError:
                announce_date = None
        self.__create_field_row(main_frame, "Announce Date", announce_date, "date")

        # State
        current_state = self.__task_data.get("state", "")
        self.__create_field_row(main_frame, "State", current_state, "state")

    def __fetch_available_states(self):
        """Fetch available states from the server"""
        try:
            response = requests.get(
                f"{self.__configuration.api_url}/taskstates/in_guild/",
                params={"guild_id": self.__task_data.get("guild")},
            )
            if response.status_code == 200:
                return response.json()
            return []
        except Exception as e:
            print(f"Error fetching states: {e}")
            return []

    def __create_field_row(self, parent, label, value, field_type):
        """Create a row with label, value display, edit button, and appropriate input field"""
        row_frame = ctk.CTkFrame(parent, fg_color="transparent")
        row_frame.pack(fill="x", pady=5)

        # Label
        ctk.CTkLabel(
            row_frame,
            text=f"{label}:",
            font=(self.__configuration.font, 12),
        ).pack(side="left", padx=5)

        # Value display
        value_frame = ctk.CTkFrame(row_frame, fg_color="transparent")
        value_frame.pack(side="left", fill="x", expand=True, padx=5)

        if field_type == "text":
            value_label = ctk.CTkLabel(
                value_frame,
                text=str(value) if value else "Not set",
                font=(self.__configuration.font, 12),
            )
            value_label.pack(side="left")

            # Edit button
            edit_button = ctk.CTkButton(
                row_frame,
                text="Edit",
                width=60,
                command=lambda: self.__show_text_editor(value_frame, value, label),
            )
            edit_button.pack(side="right", padx=5)

        elif field_type == "date":
            value_label = ctk.CTkLabel(
                value_frame,
                text=value.strftime("%Y-%m-%d") if value else "Not set",
                font=(self.__configuration.font, 12),
            )
            value_label.pack(side="left")

            # Edit button
            edit_button = ctk.CTkButton(
                row_frame,
                text="Edit",
                width=60,
                command=lambda: self.__show_date_picker(value_frame, value, label),
            )
            edit_button.pack(side="right", padx=5)

        elif field_type == "state":
            # Create state selector
            state_names = [state["title"] for state in self.__available_states]
            current_state_name = next(
                (
                    state["title"]
                    for state in self.__available_states
                    if state["id"] == value
                ),
                "Not set",
            )

            value_label = ctk.CTkLabel(
                value_frame,
                text=current_state_name,
                font=(self.__configuration.font, 12),
            )
            value_label.pack(side="left")

            # Edit button
            edit_button = ctk.CTkButton(
                row_frame,
                text="Edit",
                width=60,
                command=lambda: self.__show_state_selector(value_frame, value, label),
            )
            edit_button.pack(side="right", padx=5)

        # Store original value
        self.__original_values[label] = value

    def __show_text_editor(self, parent, current_value, field_name):
        """Show text entry for editing"""
        # Clear existing widgets
        for widget in parent.winfo_children():
            widget.destroy()

        # Create entry
        entry = ctk.CTkEntry(parent, width=200)
        entry.pack(side="left", padx=5)
        entry.insert(0, current_value if current_value else "")
        entry.focus_set()  # Set focus to entry
        entry.focus_force()  # Force focus to entry

        # Create save button
        save_button = ctk.CTkButton(
            parent,
            text="Save",
            width=60,
            command=lambda: self.__save_text_value(parent, entry.get(), field_name),
        )
        save_button.pack(side="left", padx=5)

        # Create cancel button
        cancel_button = ctk.CTkButton(
            parent,
            text="Cancel",
            width=60,
            command=lambda: self.__restore_value(parent, field_name),
        )
        cancel_button.pack(side="left", padx=5)

        # Store editing widget
        self.__editing_fields[field_name] = entry

        # Bind click events to close editor when clicking outside
        self.bind(
            "<Button-1>", lambda e: self.__check_click_outside(e, parent, field_name)
        )
        entry.bind("<Button-1>", lambda e: "break")
        save_button.bind("<Button-1>", lambda e: "break")
        cancel_button.bind("<Button-1>", lambda e: "break")

        # Bind Enter key to save
        entry.bind(
            "<Return>",
            lambda e: self.__save_text_value(parent, entry.get(), field_name),
        )

    def __show_date_picker(self, parent, current_value, field_name):
        """Show calendar for date selection"""
        # Clear existing widgets
        for widget in parent.winfo_children():
            widget.destroy()

        # Create calendar
        cal = Calendar(
            parent,
            selectmode="day",
            year=current_value.year if current_value else datetime.now().year,
            month=current_value.month if current_value else datetime.now().month,
            day=current_value.day if current_value else datetime.now().day,
        )
        cal.pack(side="left", padx=5)

        # Create save button
        save_button = ctk.CTkButton(
            parent,
            text="Save",
            width=60,
            command=lambda: self.__save_date_value(parent, cal.get_date(), field_name),
        )
        save_button.pack(side="left", padx=5)

        # Create cancel button
        cancel_button = ctk.CTkButton(
            parent,
            text="Cancel",
            width=60,
            command=lambda: self.__restore_value(parent, field_name),
        )
        cancel_button.pack(side="left", padx=5)

        # Store editing widget
        self.__editing_fields[field_name] = cal

        # Bind click events to close editor when clicking outside
        self.bind(
            "<Button-1>", lambda e: self.__check_click_outside(e, parent, field_name)
        )
        cal.bind("<Button-1>", lambda e: "break")
        save_button.bind("<Button-1>", lambda e: "break")
        cancel_button.bind("<Button-1>", lambda e: "break")

    def __show_state_selector(self, parent, current_value, field_name):
        """Show state selector dropdown"""
        # Clear existing widgets
        for widget in parent.winfo_children():
            widget.destroy()

        # Create state selector
        state_names = [state["title"] for state in self.__available_states]
        current_state_name = next(
            (
                state["title"]
                for state in self.__available_states
                if state["id"] == current_value
            ),
            "Not set",
        )

        state_selector = ctk.CTkOptionMenu(
            parent,
            values=state_names,
            width=200,
        )
        state_selector.set(current_state_name)
        state_selector.pack(side="left", padx=5)

        # Create save button
        save_button = ctk.CTkButton(
            parent,
            text="Save",
            width=60,
            command=lambda: self.__save_state_value(
                parent, state_selector.get(), field_name
            ),
        )
        save_button.pack(side="left", padx=5)

        # Create cancel button
        cancel_button = ctk.CTkButton(
            parent,
            text="Cancel",
            width=60,
            command=lambda: self.__restore_value(parent, field_name),
        )
        cancel_button.pack(side="left", padx=5)

        # Store editing widget
        self.__editing_fields[field_name] = state_selector

        # Bind click events to close editor when clicking outside
        self.bind(
            "<Button-1>", lambda e: self.__check_click_outside(e, parent, field_name)
        )
        state_selector.bind("<Button-1>", lambda e: "break")
        save_button.bind("<Button-1>", lambda e: "break")
        cancel_button.bind("<Button-1>", lambda e: "break")

    def __check_click_outside(self, event, parent, field_name):
        """Check if click was outside the editing area"""
        # Get the widget that was clicked
        clicked_widget = event.widget

        # Check if click was outside the parent frame
        if not parent.winfo_containing(event.x_root, event.y_root):
            # Restore the original value
            self.__restore_value(parent, field_name)
            # Unbind the click event
            self.unbind("<Button-1>")

    def __save_text_value(self, parent, new_value, field_name):
        """Save text value and update display"""
        # Clear existing widgets
        for widget in parent.winfo_children():
            widget.destroy()

        # Create new label with updated value
        value_label = ctk.CTkLabel(
            parent,
            text=new_value if new_value else "Not set",
            font=(self.__configuration.font, 12),
        )
        value_label.pack(side="left")

        # Update task data
        self.__task_data[field_name.lower()] = new_value

    def __save_date_value(self, parent, new_date, field_name):
        """Save date value and update display"""
        # Clear existing widgets
        for widget in parent.winfo_children():
            widget.destroy()

        # Create new label with updated value
        value_label = ctk.CTkLabel(
            parent,
            text=new_date,
            font=(self.__configuration.font, 12),
        )
        value_label.pack(side="left")

        # Update task data
        self.__task_data[field_name.lower()] = new_date

    def __save_state_value(self, parent, new_state_name, field_name):
        """Save state value and update display"""
        # Clear existing widgets
        for widget in parent.winfo_children():
            widget.destroy()

        # Find the state ID for the selected state name
        selected_state = next(
            (
                state
                for state in self.__available_states
                if state["title"] == new_state_name
            ),
            None,
        )

        if selected_state:
            # Create new label with updated value
            value_label = ctk.CTkLabel(
                parent,
                text=new_state_name,
                font=(self.__configuration.font, 12),
            )
            value_label.pack(side="left")

            # Update task data with state ID
            self.__task_data[field_name.lower()] = selected_state["id"]

            # Get the token
            token_manager = TokenManger()
            token_data = token_manager.get_token()
            if not token_data:
                CTkMessagebox(
                    title="Error",
                    message="Authentication required",
                    icon="cancel",
                )
                return

            # Immediately save the state change
            try:
                print(f"Sending state update: {selected_state['id']}")  # Debug print
                response = requests.patch(
                    f"{self.__configuration.api_url}/tasks/{self.__task_data['id']}/update_task/",
                    json={"state": selected_state["id"]},
                    headers={"Authorization": f"Bearer {token_data['access']}"},
                )

                if response.status_code == 200:
                    # Update was successful
                    if self.__refresh_callback:
                        self.__refresh_callback()  # Call refresh callback for this bar
                    if self.__bar_refresh_callback:
                        self.__bar_refresh_callback()  # Call refresh callback for all bars
                    self.__close_dialog()
                else:
                    print(
                        f"Failed to update state. Status code: {response.status_code}"
                    )  # Debug print
                    # Show error message
                    CTkMessagebox(
                        title="Error",
                        message="Failed to update task state",
                        icon="cancel",
                    )
                    # Restore original value
                    self.__restore_value(parent, field_name)
            except Exception as e:
                print(f"Error updating state: {e}")  # Debug print
                CTkMessagebox(
                    title="Error",
                    message="An error occurred while updating task state",
                    icon="cancel",
                )
                # Restore original value
                self.__restore_value(parent, field_name)

    def __restore_value(self, parent, field_name):
        """Restore original value"""
        # Clear existing widgets
        for widget in parent.winfo_children():
            widget.destroy()

        # Create new label with original value
        value_label = ctk.CTkLabel(
            parent,
            text=(
                str(self.__original_values[field_name])
                if self.__original_values[field_name]
                else "Not set"
            ),
            font=(self.__configuration.font, 12),
        )
        value_label.pack(side="left")

    def __save_changes(self):
        """Save all changes to the task"""
        try:
            # Prepare update data only for changed fields
            update_data = {}

            # Check each field for changes
            for field_name, original_value in self.__original_values.items():
                current_value = self.__task_data.get(field_name.lower())

                # Skip if value hasn't changed
                if current_value == original_value:
                    continue

                # Handle different field types
                if field_name.lower() in ["due_date", "announce_date"]:
                    if current_value:
                        # Convert date string to ISO format
                        try:
                            date_obj = datetime.strptime(current_value, "%Y-%m-%d")
                            update_data[field_name.lower()] = date_obj.isoformat()
                        except ValueError:
                            continue
                    else:
                        update_data[field_name.lower()] = None
                else:
                    # For text fields (title, description) and state
                    update_data[field_name.lower()] = current_value

            # Only make API call if there are changes
            if update_data:
                # Get the token
                token_manager = TokenManger()
                token_data = token_manager.get_token()
                if not token_data:
                    CTkMessagebox(
                        title="Error",
                        message="Authentication required",
                        icon="cancel",
                    )
                    return

                print(f"Sending update data: {update_data}")  # Debug print
                response = requests.patch(
                    f"{self.__configuration.api_url}/tasks/{self.__task_data['id']}/update_task/",
                    json=update_data,
                    headers={"Authorization": f"Bearer {token_data['access']}"},
                )

                if response.status_code == 200:
                    # Update was successful
                    if self.__refresh_callback:
                        self.__refresh_callback()  # Call refresh callback for this bar
                    if self.__bar_refresh_callback:
                        self.__bar_refresh_callback()  # Call refresh callback for all bars
                    self.__close_dialog()
                else:
                    print(
                        f"Failed to update task. Status code: {response.status_code}"
                    )  # Debug print
                    # Show error message
                    CTkMessagebox(
                        title="Error", message="Failed to update task", icon="cancel"
                    )
            else:
                # No changes to save
                self.__close_dialog()

        except Exception as e:
            print(f"Error saving changes: {e}")  # Debug print
            CTkMessagebox(
                title="Error",
                message="An error occurred while saving changes",
                icon="cancel",
            )

    def __editing(self, event):
        pass

    def __close_dialog(self, event=None):
        """Close the dialog safely"""
        try:
            self.grab_release()
            if self.__master and self.__master.winfo_exists():
                self.__master.focus_set()
            self.destroy()
        except tk.TclError:
            pass
