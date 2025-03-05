import customtkinter as ctk
import requests
from CTkMessagebox import CTkMessagebox
from app.components.todocardedit import TodoCardEditing


# This class to representing the task as a card.
class TodoCard(ctk.CTkFrame):
    def __init__(
        self,
        master,
        configuration,
        task_data,
        refresh_callback=None,
        bar_refresh_callback=None,
        **kwargs,
    ):
        super().__init__(
            master, fg_color=configuration.colors["snow-white"], height=30, **kwargs
        )
        self.master = master
        self._configuration = configuration
        self.__task_data = task_data
        self.__refresh_callback = refresh_callback
        self.__bar_refresh_callback = bar_refresh_callback

        # color for changing
        self.__normal_color = configuration.colors["snow-white"]
        self.__hover_color = configuration.colors["hover-snow-white"]

        # Bind hover events to the entire frame
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

        # Button to delete the task
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

        # Bind hover events to all widgets
        self.__label.bind("<Enter>", self.__on_hover)
        self.__label.bind("<Leave>", self.__on_leave)
        self.__delBut.bind("<Enter>", self.__on_hover)
        self.__delBut.bind("<Leave>", self.__on_leave)

        # Bind click event to all widgets except delete button
        self.__label.bind("<Button-1>", self.__open_editor)

    # Open a modal to edit the task
    def __open_editor(self, event):
        # Prevent event from propagating to parent widgets
        event.widget.focus_set()
        event.widget.focus_force()
        # Create and show the editor dialog
        editor = TodoCardEditing(
            self.master,
            self._configuration,
            self.__task_data,
            self.__refresh_callback,
            self.__bar_refresh_callback,
        )
        editor.transient(self.master)  # Make dialog transient to master
        editor.grab_set()  # Make dialog modal
        editor.focus_set()  # Ensure dialog gets focus
        editor.focus_force()  # Force focus to dialog
        editor.lift()  # Bring dialog to front
        return "break"  # Stop event propagation

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
                self.__delete_task_db()
                self.destroy()
        except Exception as e:
            print(e)

    def __delete_task_db(self):
        task_id = self.__task_data.get("id")
        response = requests.delete(
            self._configuration.api_url + f"/tasks/{task_id}/delete_task/",
        )

        if response.status_code == 204:
            if self.__refresh_callback:
                self.__refresh_callback()  # Refresh the specific bar
            if self.__bar_refresh_callback:
                self.__bar_refresh_callback()  # Refresh all bars
            return CTkMessagebox(
                self.master,
                icon="check",
                title="Task Deleted",
                message="Task has been deleted",
            )
        else:
            return CTkMessagebox(
                self.master,
                icon="cancel",
                title="Error",
                message="Failed to delete task",
            )

    def __on_hover(self, event):
        self.configure(fg_color=self.__hover_color)

    def __on_leave(self, event):
        self.configure(fg_color=self.__normal_color)
