import customtkinter as ctk
import requests
from app.frames.frame import Frame
from app.components.todobar import TodoBar


class BulletinBoard(Frame):
    def __init__(self, master, configuration, **kwargs):
        super().__init__(
            master,
            configuration,
            fg_color=configuration.colors["frame-color-main"],
            **kwargs
        )
        self.master = master
        self.__configuration = configuration
        self.__localframe = ctk.CTkFrame(
            self, fg_color=self._configuration.colors["snow-white"]
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

    def __fetch_bars(self):
        params = {"guild_id": self._guildId}
        response = requests.get(
            self.__configuration.api_url + "/taskstate/in_guild", params=params
        )

        if response.status_code == 200 and response.json() != []:
            bar_datas = response.json()
            for data in bar_datas:
                bar = TodoBar(
                    self.__frame0,
                    self.__configuration,
                    data["state"],
                    show=(data["state"] == "Todo"),
                )
                bar.pack(side="left", fill="y", padx=10)
                self.__bar[data["state"]] = bar
        else:
            self.__init_bars()

    # This method will be called once to initialize the bars if there not have any bars in the db
    def __init_bars(self):
        # POST request to create the default bars
        states = ["Todo", "Doing", "Done"]
        for state in states:
            payload = {"title": state, "guild": self._guildId}
            response = requests.post(
                self.__configuration.api_url + "/taskstates/create_state/", data=payload
            )
            if response.status_code == 201:
                bar_data = response.json()
                bar = TodoBar(
                    self.__frame0,
                    self.__configuration,
                    bar_data,
                    show=(state == "Todo"),
                )
                bar.pack(side="left", fill="y", padx=10)
                self.__bar[state] = bar
            else:
                print("Error creating the bar")


# Testing the bulletin board frame with the following code function
if __name__ == "__main__":
    from app.configuration import Configuration

    app = ctk.CTk()
    config = Configuration()
    app.title("Bulletin Board")

    bullet = BulletinBoard(app, config, guildId="ec5bae5a-c003-45b6-90b5-f3a9729273d2")
    bullet.pack(expand=True, fill="both")

    app.mainloop()
