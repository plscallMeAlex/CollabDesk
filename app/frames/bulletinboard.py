import customtkinter as ctk
from app.frames.frame import Frame


class BulletinBoard(Frame):
    def __init__(self, master, configuration):
        super().__init__(
            master, configuration, fg_color=configuration.colors["frame-color-main"]
        )
        self.master = master
        self.__localframe = ctk.CTkFrame(
            self, fg_color=self._configuration.colors["snow-white"]
        )
        self.__localframe.pack(expand=True, fill="both")

    def create_widgets(self):
        # Frame container
        self.__frame0 = ctk.CTkFrame(self.__localframe, fg_color="transparent")
        self.__frame1 = ctk.CTkFrame(self.__localframe, fg_color="transparent")

        self.__frame0.pack(expand=True, fill="both")
        self.__frame1.pack(expand=True, fill="both")

        # Frame 0 widgets
        