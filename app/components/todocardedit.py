import customtkinter as ctk
import tkinter as tk


class TodoCardEditing(ctk.CTkToplevel):
    def __init__(self, master, configuration, task_data):
        super().__init__(master)
        self.__master = master
        self.__configuration = configuration
        self.__task_data = task_data

        self.title("Edit Task")
        self.geometry("300x200")
        self.configure(fg_color=configuration.colors["snow-white"])
        self.overrideredirect(True)

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
        """Create a close button to ensure the dialog can be closed"""
        close_button = ctk.CTkButton(
            self,
            text="Close",
            command=self.__close_dialog,
            fg_color=self.__configuration.colors["black-text"],
            text_color=self.__configuration.colors["white-text"],
        )
        close_button.pack(side="bottom", pady=10)

    def pack(self, **kwargs):
        super().pack(**kwargs)
        self.create_widgets()

    def create_widgets(self):
        # Title label and entry
        title_label = ctk.CTkLabel(
            self,
            text=f"Title: {self.__task_data['title']}",
            font=(self.__configuration.font, 12),
        )
        title_label.pack(anchor="w", pady=(10, 0))
        # sending event call title
        title_label.bind("<Button-1>", self.__editing)

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
