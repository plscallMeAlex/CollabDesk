import customtkinter as ctk
from app.components.todocard import TodoCard


class TodoBar(ctk.CTkFrame):
    def __init__(self, master, configuration, title, show=False):
        super().__init__(
            master, fg_color=configuration.colors["frame-color-main"], corner_radius=10
        )
        self.master = master
        self.__configuration = configuration
        self.__title = title
        self.__show = show
        self.__entry_open = False

    def create_widget(self):
        #  Title of the Bar
        self.__title_label = ctk.CTkLabel(
            self,
            text=self.__title,
            text_color=self.__configuration.colors["black-text"],
            font=(self.__configuration.font, 16, "bold"),
        )
        self.__title_label.pack(pady=10)

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

    def __create_card(self, text):
        card = TodoCard(self.__frame0, self.__configuration, text)
        card.create_widgets()
        card.pack(fill="x", pady=5, padx=5)
        card.bind("<Enter>", self.__on_hover)
        card.bind("<Leave>", self.__on_leave)

    def __create_task(self, event):
        task_text = self.__entry.get().strip()
        if task_text:
            self.__create_card(task_text)
        self.__entry.destroy()
        self.__entry_open = False
        self.__taskZone.lift()

    # The button will hidden and remove binding an event after callung this function until finish adding
    def __create_entry(self):
        self.__entry_open = True
        self.__taskZone.lower()

        self.__entry = ctk.CTkEntry(self.__frame0)
        self.__entry.pack(pady=5, padx=5, fill="x")
        self.__entry.focus_set()

        self.master.bind("<Button-1>", self.__close_entry)
        self.__entry.bind("<Return>", self.__create_task)

    def __on_hover(self, event):
        if not self.__entry_open:
            self.__taskZone.lift()

    def __on_leave(self, event):
        if not self.__entry_open:
            self.__taskZone.lower()

    def __close_entry(self, event):
        if self.__entry:
            self.__entry.destroy()
            self.__entry_open = False
            self.__taskZone.lift()
            self.master.unbind("<Button-1>")


# testing the frame
if __name__ == "__main__":
    from app.configuration import Configuration
    from customtkinter import CTk

    app = CTk()
    config = Configuration(app)
    todobar = TodoBar(app, config, "To Do")
    todobar.pack(side="left", fill="y")
    todobar.create_widget()
    app.mainloop()
