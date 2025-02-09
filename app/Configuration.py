import json
import customtkinter as ctk


class Configuration:
    def __init__(self, master):
        self.__master = master
        self.colors = self.__color_import()
        self.font = "Inter"
        self.__setup()

    def __setup(self):
        ctk.set_appearance_mode("light")
        ctk.set_widget_scaling(1.2)

    def __color_import(self):
        with open("app/assets/themes.json", "r") as f:
            return json.load(f)
