import customtkinter as ctk
from app.pages.pagemanager import Page
import requests
from app.frames.bulletinboard import BulletinBoard


class HomePage(Page):
    def __init__(self, master):
        super().__init__(
            master,
            fg_color=master.configuration.colors["frame-color-main"],
            corner_radius=10,
        )
        self.master = master

    def create_widgets(self):
        response = self.__fetch_guilds()

        self.__mainframe = ctk.CTkFrame(self, fg_color="transparent")
        self.__mainframe.pack(expand=True, fill="both")

        # Frame container for switching
        self.frame_container = ctk.CTkFrame(self.__mainframe, fg_color="transparent")
        self.frame_container.pack(pady=20)

        # Create a BulletinBoard instance (First Frame)
        self.__frame0 = BulletinBoard(
            self.frame_container, self.master.configuration, guildId=response[0]["id"]
        )
        self.__frame0.pack(expand=True, fill="both")

    def __but1_click(self):
        self.__frame1 = ctk.CTkFrame(self.frame_container, fg_color="transparent")

        self.__label2 = ctk.CTkLabel(self.__frame1, text="Label 2", fg_color="Green")
        self.__label2.pack()

        self.master.pagemanager.switch_frame(self.__frame0, self.__frame1)

    def __fetch_guilds(self):
        guilds = requests.get(
            self.master.configuration.api_url + "/guilds/list_guilds/",
        )
        return guilds.json()
