import customtkinter as ctk
from CTkMessagebox import CTkMessagebox


# This class to representing the task as a card.
class TodoCard(ctk.CTkFrame):
    def __init__(self, master, configuration, taskName, **kwargs):
        super().__init__(master, fg_color=configuration.colors["snow-white"], **kwargs)
        self.master = master
        self._configuration = configuration
        self.__taskName = taskName

        self.bind("<Button-1>", self.__open_editor)

    def create_widgets(self):
        # Label of the card
        self.__label = ctk.CTkLabel(
            self,
            text=self.__taskName,
            text_color=self._configuration.colors["black-text"],
        )
        self.__label.pack(side="left", padx=10, pady=5)

        # Button to delete the task
        self.__delBut = ctk.CTkButton(
            self,
            text="X",
            fg_color=self._configuration.colors["black-text"],
            text_color=self._configuration.colors["white-text"],
            command=self.__delete_task,
        )
        self.__delBut.pack(side="right", padx=10, pady=5)

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
