import json
import os
from dotenv import load_dotenv
import customtkinter as ctk


class Configuration:
    def __init__(self):
        load_dotenv()
        self.colors = self.__color_import()
        self.font = "Inter"
        self.api_url = os.getenv("API_URL")
        self.user_data = {"id": "f452d1d8-f836-4006-a63d-647e03836040"}
        self.__setup()

    def __setup(self):
        ctk.set_appearance_mode("light")
        ctk.set_widget_scaling(1.2)

    def __color_import(self):
        with open("app/assets/themes.json", "r") as f:
            return json.load(f)
