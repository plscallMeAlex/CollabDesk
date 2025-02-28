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
        self.__title_frame.pack(fill="x")
        self.__title_label.pack(side="left", pady=10, padx=10)

        # Bind hover events for dialog button visibility
        self.__title_frame.bind("<Enter>", self.__dialog_hover)
        self.__title_frame.bind("<Leave>", self.__dialog_leave)
        self.__dialog_but.bind("<Enter>", self.__dialog_hover)
        self.__dialog_but.bind("<Leave>", self.__dialog_leave)
        self.__dialog_but.bind("<Button-1>", self.__open_dialog)

        # Frame for storing the task cards
        self.__frame0 = ctk.CTkFrame(self, fg_color="transparent")
        self.__frame0.pack(fill="both", expand=True, padx=10, pady=10)

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

        # Hide the add task button if show is False
        if not self.__show:
            self.__taskButt.lower()

        # Specific the event that want to show the add task button while hovering or not
        if not self.__show:
            self.bind("<Enter>", self.__add_task_hover)
            self.bind("<Leave>", self.__add_task_leave)
            self.__frame0.bind("<Enter>", self.__add_task_hover)
            self.__frame0.bind("<Leave>", self.__add_task_leave)
            self.__taskButt.bind("<Enter>", self.__add_task_hover)
            self.__taskButt.bind("<Leave>", self.__add_task_leave)

    def __create_task(self, event):
        """Create a new task card"""
        title = self.__entry.get()
        if title == "":
            return

        # Require Title, Guild, Assigner, State
        payload = {
            "title": title,
            "guild": self.__bar_data["guild"],
            "assigner": self.__configuration.user_data["id"],
            "state": self.__bar_data["id"],
        }

        try:
            # send a POST request to the server to create a new task
            response = requests.post(
                self.__configuration.api_url + "/tasks/create_task/",
                json=payload,
                headers={"Content-Type": "application/json"},
            )

            if response.status_code == 201:
                data = response.json()
                task = TodoCard(self.__frame0, self.__configuration, data)
                task.pack(side="top", pady=5)
                self.__tasks.append(task)

                # Destroy the entry frame
                self.__entry_frame.destroy()
                self.__entry_open = False
            else:
                CTkMessagebox(
                    self.master,
                    title="Error",
                    message="An error occurred while creating the task",
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

    def __open_dialog(self, event):
        pass

    def __dialog_hover(self, event):
        self.__dialog_but.lift()

    def __dialog_leave(self, event):
        self.__dialog_but.lower()

    def __add_task_hover(self, event):
        self.__taskButt.lift()

    def __add_task_leave(self, event):
        self.__taskButt.lower()
