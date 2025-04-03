# voice_chat/views.py
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
import time
import hmac
import hashlib


@csrf_exempt
def get_turn_credentials(request):
    """Generate temporary credentials for TURN server"""
    username = f"{int(time.time())}:{request.user.username}"
    secret = "your_shared_secret"  # Change this to your actual secret

    # Create HMAC SHA1 hash
    hmac_sha1 = hmac.new(secret.encode(), username.encode(), hashlib.sha1).digest()

    # Convert to base64
    import base64

    password = base64.b64encode(hmac_sha1).decode()

    # Return credentials and server config
    return JsonResponse(
        {
            "username": username,
            "password": password,
            "ttl": 86400,  # 24 hours
            "uris": [
                "turn:your-turn-server.com:3478?transport=udp",
                "turn:your-turn-server.com:3478?transport=tcp",
                "turn:your-turn-server.com:443?transport=tcp",
                "stun:your-stun-server.com:3478",
            ],
        }
    )
