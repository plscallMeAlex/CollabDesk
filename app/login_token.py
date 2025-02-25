import os
import json
import time
from cryptography.fernet import Fernet
from datetime import datetime, timedelta
from pathlib import Path

key = b'roJ7sg8n8ttQAGRgYP-7T-3Ly0QWS2Vwoubgrb9vdvA='
cipher = Fernet(key)

appdata_path = os.getenv('APPDATA')
file_path = Path(appdata_path) / 'CollabDesk' / 'login_token.json'

def encrypt_data(token):
    creation_date = datetime.now().isoformat() 
    data = {'token': token, 'created_at': creation_date}
    data_json = json.dumps(data)
    encrypted_data = cipher.encrypt(data_json.encode())
    return encrypted_data

def decrypt_data(encrypted_data):
    decrypted_data = cipher.decrypt(encrypted_data).decode()
    data = json.loads(decrypted_data)
    return data['token'], data['created_at']

def is_token_expired(creation_date):
    created_at = datetime.fromisoformat(creation_date)
    return datetime.now() - created_at > timedelta(days=7)

def store_token(token):
    (Path(appdata_path) / 'CollabDesk').mkdir(parents=True, exist_ok=True)

    encrypted_data = encrypt_data(token)
    with open(file_path, 'wb') as f:
        f.write(encrypted_data)

def check_login():
    if not file_path.exists():
        return None

    with open(file_path, 'rb') as f:
        encrypted_data = f.read()

    token, created_at = decrypt_data(encrypted_data)

    if is_token_expired(created_at):
        print("Token has expired. Logging out...")
        return None 

    print("Token valid, user logged in.")
    return token 