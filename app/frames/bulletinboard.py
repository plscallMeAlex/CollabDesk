import customtkinter as ctk
from tkinter import ttk
from CTkMessagebox import CTkMessagebox
import requests
from app.frames.frame import Frame
from app.components.todobar import TodoBar
from app.components.usertask import UserTask

DEFAULT_BARS = ["Todo", "Doing", "Done", "Overdue"]


class BulletinBoard(Frame):
    def __init__(self, master, configuration, **kwargs):
        super().__init__(
            master,
            configuration,
            fg_color=configuration.colors["frame-color-main"],
            **kwargs,
        )
        self.master = master
        self._guildId = kwargs.get("guildId")
        self.__configuration = configuration
        self.__localframe = ctk.CTkScrollableFrame(
            self,
            fg_color=self._configuration.colors["snow-white"],
            height=800,
            corner_radius=0,
            scrollbar_button_color="white",
            scrollbar_button_hover_color="grey",
        )
        self.__localframe.pack(expand=True, fill="both")

        # Storing Bar
        self.__bar = {}
        self.create_widgets()
        self.__fetch_bars()

    def create_widgets(self):
        # Frame container
        self.__frame0 = ctk.CTkScrollableFrame(
            self.__localframe,
            fg_color="transparent",
            orientation="horizontal",
            height=300,
            scrollbar_button_color="white",
            scrollbar_button_hover_color="grey",
        )  # for the storing a todobar
        self.__frame1 = ctk.CTkFrame(
            self.__localframe, fg_color="transparent"
        )  # for storing the

        self.__frame0.pack(expand=True, fill="both")
        # Line separator
        self.__line_separator = ttk.Separator(
            self.__localframe,
            orient="horizontal",
            style="Horizontal.TFrame",
        )
        self.__line_separator.pack(expand=True, fill="both")
        self.__frame1.pack(expand=True, fill="both")

        # Add bar button
        self.__add_bar_button = ctk.CTkButton(
            self.__frame0,
            text="Add Bar",
            command=self.__open_input_dialog,
            fg_color=self._configuration.colors["green-program"],
            text_color=self._configuration.colors["snow-white"],
            width=60,
        )
        self.__add_bar_button.pack(side="left", padx=10, pady=10, fill="y")
        # User task
        self.__user_task = UserTask(self.__frame1, self.__configuration, self._guildId)
        self.__user_task.pack(expand=True, fill="both")

    def create_bar(self, state):
        # Check if it reach the limit of bars
        if len(self.__bar) == 6:
            CTkMessagebox(
                self.master,
                icon="warning",
                title="Bar Limit",
                message="You have reached the limit of bars",
            )
            return

        payload = {"title": state, "guild": self._guildId}
        response = requests.post(
            self.__configuration.api_url + "/taskstates/create_state/",
            json=payload,
        )
        if response.status_code == 201:
            bar_data = response.json()
            bar = TodoBar(
                self.__frame0,
                self.__configuration,
                bar_data,
                self.refresh_bars,
                True if state not in DEFAULT_BARS else False,
                self.__fetch_bars,
            )
            bar.pack(side="left", fill="y", padx=10)
            self.__bar[state] = bar
        else:
            print("Failed to create bar")

            CTkMessagebox(icon="cancel", title="Error", message="Failed to create bar")

    def refresh_bars(self):
        for bar in self.__bar.values():
            bar.refresh_tasks()

        # refresh user task
        try:
            self.__user_task.refresh_tasks()
        except Exception as e:
            print(f"Error refreshing user task: {e}")

    def set_guildId(self, guildId):
        self._guildId = guildId

    def __fetch_bars(self):
        params = {"guild_id": self._guildId}
        response = requests.get(
            self.__configuration.api_url + "/taskstates/in_guild/",
            params=params,
        )

        if response.status_code == 200 and response.json() != []:
            bar_datas = response.json()
            # Clear the existing bars
            for bar in self.__bar.values():
                # unpack the bar
                bar.pack_forget()
                bar.destroy()
            self.__bar.clear()
            for data in bar_datas:
                bar = TodoBar(
                    self.__frame0,
                    self.__configuration,
                    data,
                    self.refresh_bars,
                    True if data["title"] not in DEFAULT_BARS else False,
                    self.__fetch_bars,
                )
                bar.pack(side="left", fill="y", padx=10)
                self.__bar[data["title"]] = bar
        else:
            self.__init_bars()

    # This method will be called once to initialize the bars if there not have any bars in the db
    def __init_bars(self):
        # POST request to create the default bars
        for state in DEFAULT_BARS:
            self.create_bar(state)

    def __open_input_dialog(self):
        dialog = ctk.CTkInputDialog(
            title="Add Bar",
            text="Enter the name of the state",
            button_fg_color=self._configuration.colors["green-program"],
            button_text_color=self._configuration.colors["snow-white"],
        )
        state_name = dialog.get_input()
        if state_name and state_name.strip() != "":
            # Check if state name already exists
            state_name = state_name.capitalize()
            if state_name in self.__bar:
                CTkMessagebox(
                    title="Error",
                    message="A bar with this name already exists!",
                    icon="cancel",
                )
                return
            # Create the new bar
            self.create_bar(state_name)
