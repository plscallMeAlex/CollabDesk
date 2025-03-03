import os
import pickle
import jwt
import requests
from datetime import datetime, timezone
from pathlib import Path


class TokenManger(object):
    def __init__(self, app_name="CollabDesk"):
        self.appdata_path = Path(os.getenv("APPDATA")) / app_name
        self.file_path = self.appdata_path / "token_data.pkl"
        self.appdata_path.mkdir(parents=True, exist_ok=True)
        self.refresh_token_url = os.getenv("API_URL") + "/token/refresh/"

    def store_token(self, token):
        """Store access and refresh token in a file"""
        token_data = {"access": token["access"], "refresh": token["refresh"]}
        with open(self.file_path, "wb") as file:
            pickle.dump(token_data, file)

    def get_token(self):
        """Get access and refresh token from file"""
        try:
            with open(self.file_path, "rb") as file:
                token_data = pickle.load(file)
                return token_data
        except FileNotFoundError:
            return None

    def check_token_expired(self):
        """Check if token is expired"""
        token = self.get_token()
        if not token:
            return True
        access = token.get("access")
        try:
            decoded_token = jwt.decode(access, options={"verify_signature": False})
            exp_time = datetime.fromtimestamp(decoded_token["exp"], timezone.utc)
            return datetime.now(timezone.utc) > exp_time
        except jwt.ExpiredSignatureError:
            return True
        except jwt.DecodeError:
            return True

    def refresh_access_token(self):
        """Refresh access token using refresh token"""
        token = self.get_token()
        if not token:
            return None

        response = requests.post(
            self.refresh_token_url, data={"refresh": token["refresh"]}
        )

        if response.status_code == 200:
            access = response.json()["access"]
            token["access"] = access
            self.store_token(token)
            return access
        else:
            self.delete_token()
            return None

    def delete_token(self):
        """Delete token file"""
        try:
            os.remove(self.file_path)
        except FileNotFoundError:
            pass
