import requests
from app.tokenmanager import TokenManger

METHOD = ["GET", "POST", "PUT", "PATCH", "DELETE"]


def make_request(url, method, **kwargs):
    # Check method must be in METHOD
    if method not in METHOD:
        raise ValueError(f"Method must be one of {METHOD}")
    token_manager = TokenManger()
    token = token_manager.get_token()
    if token:
        headers = headers or {}
        headers["Authorization"] = f"Bearer {token['access']}"
    response = requests.request(method=method, url=url, headers=headers, **kwargs)
    if response.status_code == 401:
        new_token = token_manager.refresh_access_token()
        if new_token:
            headers["Authorization"] = f"Bearer {new_token}"
            response = requests.request(
                method=method, url=url, headers=headers, **kwargs
            )

    return response
