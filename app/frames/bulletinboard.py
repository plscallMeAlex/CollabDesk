import customtkinter as ctk
from CTkMessagebox import CTkMessagebox
import requests
from app.frames.frame import Frame
from app.components.todobar import TodoBar
from app.components.usertask import UserTask


class BulletinBoard(Frame):
    def __init__(self, master, configuration, **kwargs):
        super().__init__(
            master,
            configuration,
            fg_color=configuration.colors["frame-color-main"],
            **kwargs,
        )
        self.master = master
        self.__configuration = configuration
        self.__localframe = ctk.CTkScrollableFrame(
            self,
            fg_color=self._configuration.colors["snow-white"],
            height=600,
        )
        self.__localframe.pack(expand=True, fill="both")

        # Storing Bar
        self.__bar = {}
        self.create_widgets()
        self.__fetch_bars()

    def create_widgets(self):
        # Frame container
        self.__frame0 = ctk.CTkFrame(
            self.__localframe, fg_color="transparent"
        )  # for the storing a todobar
        self.__frame1 = ctk.CTkFrame(
            self.__localframe, fg_color="transparent"
        )  # for storing the

        self.__frame0.pack(expand=True, fill="both")
        self.__frame1.pack(expand=True, fill="both")
        self.__user_task = UserTask(self.__frame1, self.__configuration)
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
                self.__frame0, self.__configuration, bar_data, self.refresh_bars
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

    def __fetch_bars(self):
        params = {"guild_id": self._guildId}
        response = requests.get(
            self.__configuration.api_url + "/taskstates/in_guild/",
            params=params,
        )

        if response.status_code == 200 and response.json() != []:
            bar_datas = response.json()
            for data in bar_datas:
                bar = TodoBar(
                    self.__frame0,
                    self.__configuration,
                    data,
                    self.refresh_bars,
                )
                bar.pack(side="left", fill="y", padx=10)
                self.__bar[data["title"]] = bar
        else:
            self.__init_bars()

    # This method will be called once to initialize the bars if there not have any bars in the db
    def __init_bars(self):
        # POST request to create the default bars
        states = ["Todo", "Doing", "Done"]
        for state in states:
            self.create_bar(state)
