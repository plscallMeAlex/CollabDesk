import customtkinter as ctk
import requests


class UserTask(ctk.CTkFrame):
    def __init__(self, master, configuration):
        super().__init__(master)
        self.__configuration = configuration
        self.configure(
            fg_color=configuration.colors["snow-white"],
            corner_radius=10,
            border_width=2,
            border_color=configuration.colors["black-text"],
        )
        self.__task_labels = []  # List to store task labels

    def pack(self, **kwargs):
        super().pack(**kwargs)
        self.create_widgets()

    def create_widgets(self):
        # Frame
        self.__frame = ctk.CTkFrame(self, fg_color="transparent")
        self.__frame.pack(fill="both", expand=True)

        # Title
        self.__title = ctk.CTkLabel(
            self.__frame,
            text="Your Task",
            font=ctk.CTkFont(self.__configuration.font, size=20, weight="bold"),
        )
        self.__title.pack(pady=10)

        # Task list frame
        self.__task_list_frame = ctk.CTkFrame(self.__frame, fg_color="transparent")
        self.__task_list_frame.pack(fill="both", expand=True)

        # Frame
        self.__task_frame = ctk.CTkFrame(self.__task_list_frame, fg_color="transparent")
        self.__task_frame.pack(fill="both", expand=True)

        # Fill the task list inside the scrollable frame
        self.__fetch_task()

    def __fetch_task(self):
        user_id = self.__configuration.load_user_data()
        params = {"user_id": user_id}
        response = requests.get(
            self.__configuration.api_url + "/tasks/user_tasks/",
            params=params,
        )
        if response.status_code == 200:
            tasks = response.json()
            for task in tasks:
                task_label = ctk.CTkLabel(
                    self.__task_frame,
                    text=task["title"],
                    font=ctk.CTkFont(self.__configuration.font, size=16),
                )
                task_label.pack(pady=5)
                self.__task_labels.append(task_label)  # Store in the labels list
        else:
            print(f"Error fetching tasks: {response.status_code}")

    def refresh_tasks(self):
        # Clear existing task labels
        for task_label in self.__task_labels:
            task_label.destroy()
        self.__task_labels = []  # Reset the labels list
        self.__fetch_task()  # Fetch and create new labels
