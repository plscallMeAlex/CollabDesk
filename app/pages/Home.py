import customtkinter as ctk
from app.pages.pagemanager import Page
import requests
from app.frames.bulletinboard import BulletinBoard
from app.components.sidebar import SidebarFrame
from app.components.header import Header
from app.components.channelbar import ChannelBar
from app.frames.calendar import TaskCalendarWidget
from app.frames.dashboard import Dashboard


class HomePage(Page):
    def __init__(self, master):
        super().__init__(
            master,
            fg_color=master.configuration.colors["frame-color-secondary"],
        )
        self.master = master
        self.__current_guild = None
        self.__current_frame = None
        self.__frame_context = {}

    def create_widgets(self):
        # Fetch the guilds
        response = self.__fetch_guilds()

        # Set the current guild to the first one in the list
        if response:
            self.__current_guild = response[0]["id"]
        else:
            self.__current_guild = None

        # Main frame for the page
        self.__mainframe = ctk.CTkFrame(self, fg_color="transparent")
        self.__mainframe.pack(expand=True, fill="both")

        # Header at the top
        self.header = Header(self.__mainframe)
        self.header.pack(side="top", fill="x", pady=10)

        # Container for sidebar, channel bar, and main content
        self.content_container = ctk.CTkFrame(self.__mainframe, fg_color="transparent")
        self.content_container.pack(expand=True, fill="both", padx=10, pady=10)

        # Sidebar on the left
        self.sidebar = SidebarFrame(
            self.content_container,
            self.master.configuration,
            self.change_guild_callback,
        )
        self.sidebar.pack(side="left", fill="y")

        # Channel bar next to sidebar
        self.channel_bar = ChannelBar(
            self.content_container,
            self.master.configuration,
            self.change_frame_callback,
            self.__current_guild,
        )
        self.channel_bar.pack(side="left", fill="y")

        # Main content area (right side)
        self.main_content = ctk.CTkFrame(self.content_container, fg_color="transparent")
        self.main_content.pack(side="right", expand=True, fill="both")

        # Frame container for switching
        self.frame_container = ctk.CTkFrame(self.main_content, fg_color="transparent")
        self.frame_container.pack(expand=True, fill="both", pady=20)

        # Initial all content frame
        self.__frame_context["BulletinBoard"] = BulletinBoard(
            self.frame_container, self.master.configuration, guildId=response[0]["id"]
        )
        self.__frame_context["Calendar"] = TaskCalendarWidget(
            self.frame_container, self.master.configuration, guildId=response[0]["id"]
        )
        self.__frame_context["Dashboard"] = Dashboard(
            self.frame_container, self.master.configuration, guildId=response[0]["id"]
        )
        # Init one frame
        self.__current_frame = self.__frame_context["BulletinBoard"]
        self.__frame_context["BulletinBoard"].pack(expand=True, fill="both")

    # Example usage of the switch_frame method
    # def __but1_click(self):
    #     self.__frame1 = ctk.CTkFrame(self.frame_container, fg_color="transparent")

    #     self.__label2 = ctk.CTkLabel(self.__frame1, text="Label 2", fg_color="Green")
    #     self.__label2.pack()

    #     self.master.pagemanager.switch_frame(self.__frame0, self.__frame1)

    # use for changing guild via sidebar
    def change_guild_callback(self, guild_id):
        self.__frame0.destroy()
        # Tracking the current guild
        self.__current_guild = guild_id
        self.__frame0 = BulletinBoard(
            self.frame_container, self.master.configuration, guildId=guild_id
        )
        self.__frame0.pack(expand=True, fill="both")

    # use for changing the frame via channel bar
    def change_frame_callback(self, frame_name):
        # Check the frame id
        if frame_name not in self.__frame_context:
            print("Frame not found")
            return

        self.__current_frame.pack_forget()

        if self.__current_guild is not None:
            self.__frame_context[frame_name].set_guildId(self.__current_guild)
        self.__frame_context[frame_name].pack(expand=True, fill="both")
        self.__current_frame = self.__frame_context[frame_name]

    def __fetch_guilds(self):
        params = {"user_id": self.master.configuration.load_user_data()}
        reponse = requests.get(
            self.master.configuration.api_url + "/guilds/get_guilds_by_user/",
            params=params,
        )

        if reponse.status_code == 200:
            return reponse.json()
        else:
            return []
