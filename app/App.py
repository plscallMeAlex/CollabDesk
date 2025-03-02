import customtkinter as ctk
import sys

from app.configuration import Configuration
from app.pages.pagemanager import Pagemanager
from app.pages.login import LoginPage
from app.pages.home import HomePage
from app.tokenmanager import TokenManger

from app.components.sidebar import SidebarFrame
from app.components.chanelbar import ChannelBar
from app.components.header import Header


class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.minsize(1920, 1080)

        self.title("CollabDesk")
        self.config = Configuration()

        # Set main background color
        self.configure(fg_color=self.config.colors["frame-color-secondary"])

        # Pagemanagement System
        self.pagemanager = Pagemanager(self)

        # Check if user have token
        self.token_manager = TokenManger()
        self.check_user_token()

        # Add Header to the top of the app window but make it compact
        self.header = Header(self)  # Create an instance of Header
        self.header.pack(
            side="top", fill="x", pady=10
        )  # Add padding to make it compact

        # Add Sidebar to the main app
        # Add Sidebar to the main app (Left Side)
        self.sidebar_frame = SidebarFrame(self)
        self.sidebar_frame.pack(side="left", fill="y", padx=10, pady=10)

        # Add ChannelBar next to Sidebar (Left Side, but after Sidebar)
        self.ChannelBar = ChannelBar(self)
        self.ChannelBar.pack(side="left", fill="y", padx=10, pady=10)

        if sys.platform.startswith("win"):
            self.after(100, self.__maximize)

    def check_user_token(self):
        """Check if user have valid token, refresh if expired"""
        if self.token_manage.check_token_expired():
            new_token = self.token_manager.refresh_access_token()
            if new_token:
                self.pagemanager.switch_page(HomePage)
            else:
                self.pagemanager.switch_page(LoginPage)
        else:
            self.pagemanager.switch_page(HomePage)

    def __maximize(self):
        self.state("zoomed")

    def run_app(self):
        self.mainloop()
