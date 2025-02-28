import requests
import customtkinter as ctk
from CTkMessagebox import CTkMessagebox
from app.components.todocard import TodoCard
import uuid


# TaskState frontend component
class TodoBar(ctk.CTkFrame):
    def __init__(self, master, configuration, bar_data, show=False):
        super().__init__(
            master, fg_color=configuration.colors["frame-color-main"], corner_radius=10
        )
        self.master = master
        self.__configuration = configuration
        self.__bar_data = bar_data
        self.__show = show
        self.__entry_open = False

    def pack(self, **kwargs):
        super().pack(**kwargs)
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
        self.__ellipsis_button = ctk.CTkLabel(
            self.__title_frame,
            text="X",  # Three dots symbol
            text_color=self.__configuration.colors["black-text"],
            font=(self.__configuration.font, 16),
        )
        self.__ellipsis_button.pack(side="right", padx=20)
        self.__ellipsis_button.lower()

        # Pack title frame and label
        self.__title_frame.pack(fill="x")
        self.__title_label.pack(side="left", pady=10, padx=10)

        # Bind hover events for ellipsis visibility (using lift/lower instead of after)
        self.__title_frame.bind("<Enter>", self.__on_ellipsis_hover)
        self.__title_frame.bind("<Leave>", self.__on_ellipsis_leave)
        self.__ellipsis_button.bind("<Enter>", self.__on_ellipsis_hover)
        self.__ellipsis_button.bind("<Leave>", self.__on_ellipsis_leave)
        self.__ellipsis_button.bind("<Button-1>", self.__open_delete)

        # Frame for storing the task cards
        self.__frame0 = ctk.CTkFrame(self, fg_color="transparent")
        self.__frame0.pack(fill="both", expand=True, padx=10, pady=10)

        self.__button_space = ctk.CTkFrame(self, fg_color="transparent", height=40)
        self.__button_space.pack(fill="x", pady=(10, 0))

        self.__taskZone = ctk.CTkButton(
            self.__button_space,
            text="+ Add a card",
            command=self.__create_entry,
            fg_color=self.__configuration.colors["green-program"],
            text_color=self.__configuration.colors["white-text"],
            font=(self.__configuration.font, 12),
            corner_radius=5,
        )
        self.__taskZone.place(relx=0.5, rely=0.5, anchor="center")
        self.__taskZone.lower()

        # Specific the event that want to show the add task button while hovering or not
        if not self.__show:
            self.bind("<Enter>", self.__on_hover)
            self.bind("<Leave>", self.__on_leave)
            self.__frame0.bind("<Enter>", self.__on_hover)
            self.__frame0.bind("<Leave>", self.__on_leave)
            self.__button_space.bind("<Enter>", self.__on_hover)
            self.__button_space.bind("<Leave>", self.__on_leave)
            self.__taskZone.bind("<Enter>", self.__on_hover)
            self.__taskZone.bind("<Leave>", self.__on_leave)

    # Fetch all task state that the same guild as the current bar
    def __fetch_all_taskstates(self):
        param = {"guild": self.__bar_data.get("guild")}
        response = requests.get(
            self.__configuration.api_url + "/taskstates/in_guild/", params=param
        )
        if response.status_code == 200:
            return response.json()
        return []

    # Fetch all task that the same state as the current bar
    def __fetch_all_tasks(self):
        param = {"state_id": self.__bar_data.get("id")}
        response = requests.get(
            self.__configuration.api_url + "/tasks/in_guild_by_state/", params=param
        )
        if response.status_code == 200:
            return response.json()
        return []

    # create a task in the data and create a card for it
    def __create_card(self, text):
        try:
            print("Creating task")
            payload = {
                "title": text,
                "state": self.__bar_data.get("id"),
                "assigner": "f452d1d8-f836-4006-a63d-647e03836040",  # for user_id
            }
            print("Payload:", payload)

            try:
                response = requests.post(
                    self.__configuration.api_url + "/tasks/create_task/", json=payload
                )
                print("Response:", response.status_code, response.text)

                if response.status_code != 201:
                    print("create failed")
                    CTkMessagebox(
                        title="Error",
                        message=f"Task creation failed: {response.text}",
                        icon="cancel",
                    )
                    return

                response_data = response.json()
                card = TodoCard(self.__frame0, self.__configuration, response_data)
                card.create_widgets()
                card.pack(fill="x", pady=5, padx=5)
                card.bind("<Enter>", self.__on_hover)
                card.bind("<Leave>", self.__on_leave)
            except requests.RequestException as e:
                print(f"Network error: {e}")
                CTkMessagebox(
                    title="Netowrk Error",
                    message=f"Unable to connect to the server: {str(e)}",
                    icon="cancel",
                )
        except Exception as e:
            print(f"Exception creating card: {e}")
            CTkMessagebox(
                title="Error",
                message=f"An error occurred: {str(e)}",
                icon="cancel",
            )

    def __create_task(self, event):
        if not hasattr(self, "__entry") or not self.__entry.winfo_exists():
            return

        task_text = self.__entry.get().strip()
        if task_text:
            self.__create_card(task_text)
        try:
            self.__entry.destroy()
            self.__entry_open = False
            self.__taskZone.lift()
        except Exception as e:
            print(f"Error in __create_task: {e}")

    # The button will hidden and remove binding an event after callung this function until finish adding
    def __create_entry(self):
        self.__entry_open = True
        self.__taskZone.lower()

        self.__entry = ctk.CTkEntry(self.__frame0)
        self.__entry.pack(pady=5, padx=5, fill="x")
        self.__entry.focus_set()

        self.master.bind("<Button-1>", self.__close_entry)
        self.__entry.bind("<Return>", self.__create_task)

    def __create_del_dialog(self):
        # Main frame with subtle shadow and padding
        self.__delFrame = ctk.CTkFrame(
            self.__dialog, fg_color="#f0f4f8", corner_radius=15
        )
        self.__delFrame.pack(expand=True, fill="both", padx=20, pady=20)

        # Main title label with a bolder font and larger size
        self.__delLabel = ctk.CTkLabel(
            self.__delFrame,
            text="🚀 Move Your Task",
            text_color=self.__configuration.colors["black-text"],
            font=(self.__configuration.font, 16, "bold"),
        )
        self.__delLabel.pack(pady=(10, 15))

        # Description label with smaller font and soft color
        self.__delDesc = ctk.CTkLabel(
            self.__delFrame,
            text="Select the task you want to move to another state",
            text_color=self.__configuration.colors["black-text"],
            font=(self.__configuration.font, 12),
        )
        self.__delDesc.pack(pady=(0, 10))

        # Fetch to all of the task states from the backend
        # Data format will be {response: [{"id": ..., "title": ...}]}
        # Data for task states
        data = self.__fetch_all_taskstates()

        # Extract only the titles
        task_items = [item["title"] for item in data]

        # Enhanced combo box with rounded corners
        self.__delTask = ctk.CTkOptionMenu(
            self.__delFrame,
            values=task_items,
            fg_color=self.__configuration.colors["snow-white"],  # Background color
            text_color=self.__configuration.colors["black-text"],  # Text color
            button_color=self.__configuration.colors[
                "green-program"
            ],  # Dropdown button color
            button_hover_color="#45a049",  # Hover color
            font=(self.__configuration.font, 12),
        )
        self.__delTask.pack(pady=(5, 15), padx=10)

        # Buttons Frame for better layout
        button_frame = ctk.CTkFrame(self.__delFrame, fg_color="transparent")
        button_frame.pack(pady=(5, 10), fill="x")

        # Move Task Button with hover effect and more padding
        self.__delButton = ctk.CTkButton(
            button_frame,
            text="✔ Move Task",
            fg_color=self.__configuration.colors["green-program"],
            hover_color="#45a049",
            text_color=self.__configuration.colors["white-text"],
            font=(self.__configuration.font, 14, "bold"),
            corner_radius=12,
            command=self.__handle_move_task,
        )
        self.__delButton.pack(side="left", expand=True, padx=5, ipadx=10, ipady=5)

        # Cancel Button
        self.__cancelButton = ctk.CTkButton(
            button_frame,
            text="✖ Cancel",
            fg_color=self.__configuration.colors["black-text"],
            hover_color="#d9534f",
            text_color=self.__configuration.colors["white-text"],
            font=(self.__configuration.font, 14, "bold"),
            corner_radius=12,
            command=self.__dialog.destroy,  # Close the dialog
        )
        self.__cancelButton.pack(side="right", expand=True, padx=5, ipadx=10, ipady=5)

    def __open_delete(self, event):
        self.__dialog = ctk.CTkToplevel(
            self,
            fg_color=self.__configuration.colors["snow-white"],
        )
        self.__dialog.title("Deleting The bar")
        self.__dialog.overrideredirect(True)

        # Placing in the center of the screen
        self.__dialog.update_idletasks()  # Ensure geometry is updated

        dialog_width = 300  # Replace with actual width of the dialog

        self.__dialog.geometry(
            "+%d+%d"
            % (
                self.winfo_rootx() + (self.winfo_width() // 2) - (dialog_width // 2),
                self.winfo_rooty(),
            )
        )
        self.__dialog.bind("<FocusOut>", lambda event: self.__dialog.destroy())

        self.__create_del_dialog()

    def __on_hover(self, event):
        if not self.__entry_open:
            self.__taskZone.lift()

    def __on_leave(self, event):
        if not self.__entry_open:
            self.__taskZone.lower()

    def __close_entry(self, event):
        if hasattr(self, "__entry") and self.__entry.winfo_exists():
            self.__entry.destroy()
            self.__entry_open = False
            self.__taskZone.lift()
            self.master.unbind("<Button-1>")

    def __handle_move_task(self):
        selected_title = self.__delTask.get()
        if selected_title:
            # Fetch all task states to find the ID of the selected state
            task_states = self.__fetch_all_taskstates()
            selected_state = next(
                (state for state in task_states if state["title"] == selected_title),
                None,
            )

            if selected_state:
                # Assuming you want to move all tasks from the current state to the selected state
                tasks = self.__fetch_all_tasks()
                for task in tasks:
                    task_id = task["id"]
                    payload = {"state": selected_state["id"]}
                    response = requests.put(
                        f"{self.__configuration.api_url}/tasks/update_task/{task_id}/",
                        json=payload,
                    )
                    if response.status_code != 200:
                        print(f"Failed to move task {task_id}")
                # Close the dialog after moving tasks
                CTkMessagebox(
                    title="Success",
                    message="Tasks moved successfully!",
                    icon="check",
                )
                self.__dialog.destroy()
            else:
                CTkMessagebox(
                    title="Error",
                    message="Selected task state not found.",
                    icon="cancel",
                )

    def __on_ellipsis_hover(self, event):
        self.__ellipsis_button.lift()

    def __on_ellipsis_leave(self, event):
        self.__ellipsis_button.lower()


# testing the frame
if __name__ == "__main__":
    from app.configuration import Configuration
    from customtkinter import CTk

    app = CTk()
    config = Configuration()

    data = {"title": "Todo", "id": uuid.uuid4(), "guild_id": uuid.uuid4()}
    todobar = TodoBar(
        app,
        config,
        data,
    )
    todobar.pack(side="left", fill="y")
    app.mainloop()
