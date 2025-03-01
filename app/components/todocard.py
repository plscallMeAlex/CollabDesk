import customtkinter as ctk
from CTkMessagebox import CTkMessagebox


# This class to representing the task as a card.
class TodoCard(ctk.CTkFrame):
    def __init__(self, master, configuration, task_data, **kwargs):
        super().__init__(
            master, fg_color=configuration.colors["snow-white"], height=30, **kwargs
        )
        self.master = master
        self._configuration = configuration
        self.__task_data = task_data

        # color for changing
        self.__normal_color = configuration.colors["snow-white"]
        self.__hover_color = configuration.colors["hover-snow-white"]

        self.bind("<Enter>", self.__on_hover)
        self.bind("<Leave>", self.__on_leave)

        self.bind("<Button-1>", self.__open_editor)

    def pack(self, **kwargs):
        super().pack(**kwargs)
        self.create_widgets()

    def create_widgets(self):
        # Label of the card
        self.__label = ctk.CTkLabel(
            self,
            text=self.__task_data.get("title", "Untitled"),
            text_color=self._configuration.colors["black-text"],
            font=(self._configuration.font, 12),
        )
        self.__label.pack(side="left", padx=5, pady=2)

        # Button to delete the task1x
        self.__delBut = ctk.CTkButton(
            self,
            text="X",
            width=5,
            height=5,
            fg_color=self._configuration.colors["black-text"],
            text_color=self._configuration.colors["white-text"],
            command=self.__delete_task,
        )
        self.__delBut.pack(side="right", padx=5, pady=2)

        self.__label.bind("<Enter>", self.__on_hover)
        self.__label.bind("<Leave>", self.__on_leave)
        self.__delBut.bind("<Enter>", self.__on_hover)
        self.__delBut.bind("<Leave>", self.__on_leave)

    # Open a modal to edit the task
    def __open_editor(self, event):
        print("Editing task")

    # Delete the task
    def __delete_task(self):
        try:
            result = CTkMessagebox(
                self.master,
                icon="warning",
                title="Delete Task",
                message="Are you sure you want to delete this task?",
                option_1="Yes",
                option_2="No",
            )
            result.grab_set()
            result.focus_force()
            result.wait_window()
            if result.get() == "Yes":
                self.destroy()
        except Exception as e:
            print(e)

    def __on_hover(self, event):
        self.configure(fg_color=self.__hover_color)

    def __on_leave(self, event):
        self.configure(fg_color=self.__normal_color)
