import requests
from app.tokenmanager import TokenManger

METHOD = ["GET", "POST", "PUT", "PATCH", "DELETE"]
EXCLUDE_PATH = ["/token/refresh/", "/users/login/", "/users/register/"]


def make_request(url, method, **kwargs):
    # Validate method
    if method not in METHOD:
        raise ValueError(f"Method must be one of {METHOD}")

    token_manager = TokenManger()
    headers = kwargs.pop("headers", {})

    # Exclude authentication for specific paths
    if any(url.rstrip("/").endswith(path.rstrip("/")) for path in EXCLUDE_PATH):
        headers.pop("Authorization", None)  # Ensure no token for excluded paths
    else:
        token = token_manager.get_token()
        if token:
            headers["Authorization"] = f"Bearer {token['access']}"

    print(f"🔹 Request URL: {url}, Method: {method}, Headers: {headers}")  # Debug log

    # Send request
    response = requests.request(method=method, url=url, headers=headers, **kwargs)

    # Handle token expiration (401 Unauthorized)
    if response.status_code == 401:
        print("🔄 Token expired, refreshing...")
        new_token = token_manager.refresh_access_token()
        if new_token:
            headers["Authorization"] = f"Bearer {new_token}"
            response = requests.request(
                method=method, url=url, headers=headers, **kwargs
            )

    return response
