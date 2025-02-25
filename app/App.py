import customtkinter as ctk
import sys
from app.configuration import Configuration
from app.pages.pagemanager import Pagemanager
from app.pages.login import LoginPage
from app.pages.home import HomePage
import app.login_token as Login_token


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

        # Check if user is logged in
        token = Login_token.check_login() # This variable is the username. You can use at homepage to fetch data from the server
        if token is None:
            self.pagemanager.switch_page(LoginPage)
        else:
            self.pagemanager.switch_page(HomePage)


        if sys.platform.startswith("win"):
            self.after(100, self.__maximize)

    def __maximize(self):
        self.state("zoomed")

    def run_app(self):
        self.mainloop()
