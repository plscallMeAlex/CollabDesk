import json
import os
import requests
from dotenv import load_dotenv
from app.tokenmanager import TokenManger
import customtkinter as ctk


class Configuration:
    def __init__(self):
        load_dotenv()
        self.colors = self.__color_import()
        self.font = "Inter"
        self.api_url = os.getenv("API_URL")
        self.user_data = None
        self.__setup()

    def __setup(self):
        ctk.set_appearance_mode("light")
        ctk.set_widget_scaling(1.2)

    def __color_import(self):
        with open("app/assets/themes.json", "r") as f:
            return json.load(f)

    def load_user_data(self):
        tokenM = TokenManger()
        token = tokenM.get_token()
        if token:
            return tokenM.user_from_token()
        return None

    def load_user(self):
        user = self.load_user_data()
        param = {"user_id": user}
        response = requests.get(self.api_url + "/users/get_user_by_id/", params=param)
        if response.status_code == 200:
            user_data = response.json()
            return user_data
