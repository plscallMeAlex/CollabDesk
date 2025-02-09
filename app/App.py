import customtkinter as ctk
import sys
from app.Configuration import Configuration
from app.pages.Pagemanager import Pagemanager
from app.pages.Login import LoginPage


class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.minsize(1920, 1080)

        self.title("CollabDesk")
        self.config = Configuration(self)

        # Set main background color
        self.configure(fg_color=self.config.colors["frame-color-secondary"])

        # Pagemanagement System
        self.pagemanager = Pagemanager(self)
        self.pagemanager.switch_page(LoginPage)

        if sys.platform.startswith("win"):
            self.after(100, self.__maximize)

    def __maximize(self):
        self.state("zoomed")

    def run_app(self):
        self.mainloop()
