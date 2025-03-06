import requests
import customtkinter as ctk
from CTkMessagebox import CTkMessagebox
from app.components.todocard import TodoCard
import uuid


# TaskState frontend component
class TodoBar(ctk.CTkScrollableFrame):
    def __init__(self, master, configuration, bar_data, bar_refresh):
        super().__init__(
            master,
            fg_color=configuration.colors["frame-color-main"],
            corner_radius=10,
            height=400,  # Increased height
        )
        self.master = master
        self.__configuration = configuration
        self.__bar_data = bar_data
        self.__bar_refresh = bar_refresh
        self.__tasks = []
        self.__entry_open = False

    def pack(self, **kwargs):
        super().pack(pady=10, **kwargs)
        self.create_widget()

    def create_widget(self):
        # Title of the Bar with hover effect for ellipsis
        self.__title_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.__title_label = ctk.CTkLabel(
            self.__title_frame,
            text=self.__bar_data.get("title", "Untitled"),
            text_color=self.__configuration.colors["black-text"],
            font=(self.__configuration.font, 16, "bold"),
        )
        self.__dialog_but = ctk.CTkLabel(
            self.__title_frame,
            text="X",
            text_color=self.__configuration.colors["black-text"],
            font=(self.__configuration.font, 16),
        )
        self.__dialog_but.pack(side="right", padx=20)
        self.__dialog_but.lower()

        # Pack title frame and label
        self.__title_frame.pack(fill="x", padx=5, pady=5)
        self.__title_label.pack(side="left", pady=10, padx=10)

        # Bind hover events for dialog button visibility
        self.__title_frame.bind("<Enter>", self.__dialog_hover)
        self.__title_frame.bind("<Leave>", self.__dialog_leave)
        self.__dialog_but.bind("<Enter>", self.__dialog_hover)
        self.__dialog_but.bind("<Leave>", self.__dialog_leave)
        self.__dialog_but.bind("<Button-1>", self.__open_dialog)

        # Frame for storing the task cards
        self.__frame0 = ctk.CTkFrame(self, fg_color="transparent")
        self.__frame0.pack(fill="both", expand=True, padx=10, pady=5)

        self.__taskButt = ctk.CTkButton(
            self.__frame0,
            text="+ Add a card",
            command=self.__create_entry,
            fg_color=self.__configuration.colors["green-program"],
            text_color=self.__configuration.colors["white-text"],
            font=(self.__configuration.font, 12),
            corner_radius=5,
        )
        self.__taskButt.pack(side="top", pady=5)

        # Lower the add task button
        self.__taskButt.lower()

        # Specific the event that want to show the add task button while hovering or not
        self.bind("<Enter>", self.__add_task_hover)
        self.bind("<Leave>", self.__add_task_leave)
        self.__frame0.bind("<Enter>", self.__add_task_hover)
        self.__frame0.bind("<Leave>", self.__add_task_leave)
        self.__taskButt.bind("<Enter>", self.__add_task_hover)
        self.__taskButt.bind("<Leave>", self.__add_task_leave)

        self.__fetch_tasks()

    def refresh_tasks(self):
        """Refresh all tasks in this bar"""
        for task in self.__tasks:
            task.destroy()
        self.__tasks.clear()
        self.__fetch_tasks()

    def __fetch_tasks(self):
        """Fetch all tasks that belong to this bar"""
        params = {"state_id": self.__bar_data["id"]}
        response = requests.get(
            self.__configuration.api_url + "/tasks/in_guild_by_state/",
            params=params,
        )
        if response.status_code == 200:
            tasks = response.json()
            for task in tasks:
                task_card = TodoCard(
                    self.__frame0,
                    self.__configuration,
                    task,
                    self.refresh_tasks,  # Pass the refresh callback for this bar
                    self.__bar_refresh,  # Pass the refresh callback for all bars
                )
                task_card.pack(side="top", pady=5)
                self.__tasks.append(task_card)

    def __create_task(self, event):
        """Create a new task card"""
        title = self.__entry.get()
        if title == "":
            return
        user_id = self.__configuration.load_user_data()

        # Require Title, Guild, Assigner, State
        payload = {
            "title": title,
            "guild": self.__bar_data["guild"],
            "assigner": user_id,
            "state": self.__bar_data["id"],
        }

        try:
            # send a POST request to the server to create a new task
            response = requests.post(
                self.__configuration.api_url + "/tasks/create_task/",
                json=payload,
            )

            if response.status_code == 201:
                data = response.json()
                task = TodoCard(
                    self.__frame0,
                    self.__configuration,
                    data,
                    self.refresh_tasks,  # Pass the refresh callback for this bar
                    self.__bar_refresh,  # Pass the refresh callback for all bars
                )
                task.pack(side="top", pady=5)
                self.__tasks.append(task)

                # Destroy the entry frame
                self.__entry_frame.destroy()
                self.__entry_open = False
            else:
                CTkMessagebox(
                    self.master,
                    title="Error",
                    message=response.json()["error"],
                    icon="cancel",
                )
                return

        except requests.exceptions.RequestException as e:
            CTkMessagebox(
                self.master,
                title="Error",
                message="An error occurred while creating the task",
                icon="error",
            )
            return

    def __create_entry(self):
        """Create an entry to type the title of the task"""
        if self.__entry_open:
            return

        self.__entry_open = True

        # Entry Frame
        self.__entry_frame = ctk.CTkFrame(self.__frame0, fg_color="transparent")
        self.__entry_frame.pack(side="top", fill="x", padx=5, pady=5)

        # Text entry box
        self.__entry = ctk.CTkEntry(
            self.__entry_frame,
            placeholder_text="Title",
            corner_radius=5,
        )
        self.__entry.pack(side="left", padx=5)
        self.__entry.bind("<Return>", self.__create_task)
        self.__entry.bind(
            "<Escape>",
            self.__close_entry,
        )
        self.__entry.focus_set()

    def __close_entry(self, event):
        self.__entry_frame.destroy()
        self.__entry_open = False

    def __open_dialog(self, event):
        """Open a dialog to delete the bar"""
        transfer_dialog = TransferDialog(
            self.master,
            configuration=self.__configuration,
            guild=self.__bar_data["guild"],
            state=self.__bar_data["id"],
            bar_refresh=self.__bar_refresh,
        )
        transfer_dialog.grab_set()
        transfer_dialog.focus_force()

    def __dialog_hover(self, event):
        if not self.__entry_open:
            self.__dialog_but.lift()

    def __dialog_leave(self, event):
        self.__dialog_but.lower()

    def __add_task_hover(self, event):
        if not self.__entry_open:
            self.__taskButt.lift()

    def __add_task_leave(self, event):
        self.__taskButt.lower()


class TransferDialog(ctk.CTkToplevel):
    def __init__(
        self,
        *args,
        configuration,
        guild,
        state,
        bar_refresh,
        fg_color=None,
        **kwargs,
    ):
        super().__init__(*args, fg_color=fg_color, **kwargs)
        self.__configuration = configuration
        self.__guild_id = guild
        self.__state_id = state
        self.__bar_refresh = bar_refresh
        self.title("Transfer Tasks")
        self.geometry("300x150")

        # Fetch available states
        self.__available_states = self.__fetch_state()
        self.create_widgets()

    def create_widgets(self):
        self.label = ctk.CTkLabel(
            self,
            text="Select the state to transfer the tasks",
            font=(self.__configuration.font, 12),
            text_color=self.__configuration.colors["black-text"],
            fg_color="transparent",
        )
        self.label.pack(pady=10)

        # Extract state names for dropdown menu
        state_names = [state["title"] for state in self.__available_states]

        self.state_selector = ctk.CTkOptionMenu(self, values=state_names)
        self.state_selector.pack(pady=5)

        self.confirm_button = ctk.CTkButton(
            self,
            text="Confirm",
            fg_color=self.__configuration.colors["green-program"],
            text_color=self.__configuration.colors["white-text"],
            font=(self.__configuration.font, 12),
            command=self.__transfer_tasks,
        )
        self.confirm_button.pack(pady=5)

    def __transfer_tasks(self):
        selected_state_name = self.state_selector.get()

        # Find the corresponding state ID
        selected_state = next(
            (
                state
                for state in self.__available_states
                if state["title"] == selected_state_name
            ),
            None,
        )

        if selected_state:
            print(
                f"Transferring tasks to state: {selected_state['id']} ({selected_state_name})"
            )
            # Implement actual task transfer logic here
            try:
                payload = {
                    "state_id": self.__state_id,
                    "new_state_id": selected_state["id"],
                }
                response = requests.patch(
                    self.__configuration.api_url + "/taskstates/transfer_state/",
                    json=payload,
                )
                if response.status_code == 200:
                    box = CTkMessagebox(
                        self,
                        title="Success",
                        message="Tasks transferred successfully",
                        icon="info",
                    )
                    self.__bar_refresh()
                    self.wait_window(box)
                    self.destroy()
                    return True
                else:
                    box = CTkMessagebox(
                        self,
                        title="Error",
                        message="Failed to transfer tasks",
                        icon="cancel",
                    )
                    self.wait_window(box)
                    self.destroy()
                    return False
            except requests.exceptions.RequestException:
                box = CTkMessagebox(
                    self,
                    title="Error",
                    message="An error occurred while transferring tasks",
                    icon="error",
                )
                self.wait_window(box)
                self.destroy()
                return False
        else:
            box = CTkMessagebox(
                self,
                title="Error",
                message="Selected state not found",
                icon="cancel",
            )
            self.wait_window(box)
            self.destroy()
            return False

    def __fetch_state(self):
        """Fetch available states, excluding the current state."""
        try:
            params = {"guild_id": self.__guild_id, "state_id": self.__state_id}
            response = requests.get(
                self.__configuration.api_url + "/taskstates/in_guild/",
                params=params,
            )
            if response.status_code == 200:
                return response.json()  # Returns list of JSON objects
            else:
                return []
        except requests.exceptions.RequestException:
            return []
        except Exception:
            return []
