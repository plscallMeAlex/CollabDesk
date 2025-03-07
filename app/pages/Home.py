import customtkinter as ctk
from app.pages.pagemanager import Page
import requests
from app.frames.bulletinboard import BulletinBoard
from app.components.sidebar import SidebarFrame
from app.components.header import Header
from app.components.chanelbar import ChannelBar
from app.frames.calendar import TaskCalendarWidget


class HomePage(Page):
    def __init__(self, master):
        super().__init__(
            master,
            fg_color=master.configuration.colors["frame-color-secondary"],
        )
        self.master = master

    def create_widgets(self):
        response = self.__fetch_guilds()

        self.__mainframe = ctk.CTkFrame(self, fg_color="transparent")
        self.__mainframe.pack(expand=True, fill="both")

        # Header at the top
        self.header = Header(self.__mainframe)
        self.header.pack(side="top", fill="x", pady=10)

        # Container for sidebar, channel bar, and main content
        self.content_container = ctk.CTkFrame(self.__mainframe, fg_color="transparent")
        self.content_container.pack(expand=True, fill="both", padx=10, pady=10)

        # Sidebar on the left
        self.sidebar = SidebarFrame(self.content_container, self.master.configuration)
        self.sidebar.pack(side="left", fill="y", padx=(0, 10))

        # Channel bar next to sidebar
        self.channel_bar = ChannelBar(self.content_container, self.master.configuration)
        self.channel_bar.pack(side="left", fill="y", padx=(0, 10))

        # Main content area (right side)
        self.main_content = ctk.CTkFrame(self.content_container, fg_color="transparent")
        self.main_content.pack(side="right", expand=True, fill="both")

        # Frame container for switching
        self.frame_container = ctk.CTkFrame(self.main_content, fg_color="transparent")
        self.frame_container.pack(expand=True, fill="both", pady=20)

        # Create a BulletinBoard instance (First Frame Guild)
        self.__frame0 = TaskCalendarWidget(
            self.frame_container, self.master.configuration
        )
        self.__frame0.pack(expand=True, fill="both")

        # BulletinBoard(
        #     self.frame_container, self.master.configuration, guildId=response[0]["id"]
        # )
        # self.__frame0.pack(expand=True, fill="both")

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
