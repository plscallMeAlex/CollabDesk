import customtkinter as ctk
import sys
from app.Configuration import Configuration
from app.pages.Pagemanager import Pagemanager
from app.pages.Login import LoginPage


class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.__set_geometry()

        self.title("CollabDesk")
        self.config = Configuration(self)

        # Set main background color
        self.configure(fg_color=self.config.colors["frame-color-secondary"])
        self.pagemanager = Pagemanager(self)
        self.pagemanager.page_change(LoginPage)

    def __set_geometry(self):
        if sys.platform.startswith("win"):
            self.after(0, lambda: self.wm_state("zoomed"))
        else:
            screen_width = self.winfo_screenwidth()
            screen_height = self.winfo_screenheight()
            self.geometry(f"{screen_width}x{screen_height}+0+0")

    def run_app(self):
        self.mainloop()
