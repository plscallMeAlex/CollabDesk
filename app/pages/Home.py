import customtkinter as ctk
from app.pages.pagemanager import Page


class HomePage(Page):
    def __init__(self, master):
        super().__init__(
            master, fg_color=master.config.colors["frame-color-main"], corner_radius=10
        )
        self.master = master

    def create_widgets(self):
        self.__mainframe = ctk.CTkFrame(self, fg_color="transparent")
        self.__mainframe.pack(expand=True, fill="both")

        # Frame container for switching
        self.frame_container = ctk.CTkFrame(self.__mainframe, fg_color="transparent")
        self.frame_container.pack(pady=20)

        # Initial frame (Frame 1)
        self.__frame0 = ctk.CTkFrame(self.frame_container, fg_color="transparent")
        self.__frame0.pack()

        self.__label1 = ctk.CTkLabel(self.__frame0, text="Label 1", fg_color="Yellow")
        self.__label1.pack()

        self.__but1 = ctk.CTkButton(
            self.__frame0, text="Switch to Frame 2", command=self.__but1_click
        )
        self.__but1.pack()

    def __but1_click(self):
        self.__frame1 = ctk.CTkFrame(self.frame_container, fg_color="transparent")

        self.__label2 = ctk.CTkLabel(self.__frame1, text="Label 2", fg_color="Green")
        self.__label2.pack()

        self.master.pagemanager.switch_frame(self.__frame0, self.__frame1)
