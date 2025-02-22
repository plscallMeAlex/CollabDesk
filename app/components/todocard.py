import customtkinter as ctk
from CTkMessagebox import CTkMessagebox


# This class to representing the task as a card.
class TodoCard(ctk.CTkFrame):
    def __init__(self, master, configuration, taskName, **kwargs):
        super().__init__(master, fg_color=configuration.colors["snow-white"], **kwargs)
        self.master = master
        self._configuration = configuration
        self.__taskName = taskName

        # color for changing
        self.__normal_color = configuration.colors["snow-white"]
        self.__hover_color = configuration.colors["hover-snow-white"]

        self.bind("<Enter>", self.__on_hover)
        self.bind("<Leave>", self.__on_leave)

        self.bind("<Button-1>", self.__open_editor)

    def create_widgets(self):
        # Label of the card
        self.__label = ctk.CTkLabel(
            self,
            text=self.__taskName,
            text_color=self._configuration.colors["black-text"],
            font=(self._configuration.font, 12),
        )
        self.__label.pack(side="left", padx=10, pady=5)

        # Button to delete the task
        self.__delBut = ctk.CTkButton(
            self,
            text="X",
            width=10,
            fg_color=self._configuration.colors["black-text"],
            text_color=self._configuration.colors["white-text"],
            command=self.__delete_task,
        )
        self.__delBut.pack(side="right", padx=10, pady=5)

        self.__label.bind("<Enter>", self.__on_hover)
        self.__label.bind("<Leave>", self.__on_leave)
        self.__delBut.bind("<Enter>", self.__on_hover)
        self.__delBut.bind("<Leave>", self.__on_leave)

    # Open a modal to edit the task
    def __open_editor(self, event):
        print("Editing task")

    # Delete the task
    def __delete_task(self):
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

    def __on_hover(self, event):
        self.configure(fg_color=self.__hover_color)

    def __on_leave(self, event):
        self.configure(fg_color=self.__normal_color)
