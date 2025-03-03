import jwt
from datetime import datetime, timezone
from django.http import JsonResponse
from django.utils.deprecation import MiddlewareMixin
from django.conf import settings

EXCLUDE_PATH = [
    path.rstrip("/")
    for path in ["/token/refresh/", "/users/login/", "/users/register/"]
]


class JWTMiddleware(MiddlewareMixin):
    """Middleware to check if access token is valid during request and handle expiration."""

    def process_request(self, request):
        normalize = request.path.rstrip("/")
        print(f"🔹 Request path: {normalize}")
        print(f"🔹 Excluded paths: {EXCLUDE_PATH}")

        if normalize in EXCLUDE_PATH:
            print("✅ Path is excluded from authentication")
            return None  # Bypass authentication check

        auth_header = request.headers.get("Authorization")
        if not auth_header or not auth_header.startswith("Bearer "):
            print("❌ Missing or invalid Authorization header")
            return JsonResponse(
                {"error": "Authentication credentials were not provided"}, status=401
            )

        token = auth_header.split(" ")[1]

        try:
            decoded_token = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
            exp_time = datetime.fromtimestamp(decoded_token["exp"], timezone.utc)
            if datetime.now(timezone.utc) > exp_time:
                print("❌ Access token expired")
                return JsonResponse({"error": "Access token expired"}, status=401)

        except jwt.ExpiredSignatureError:
            print("❌ JWT Signature Expired")
            return JsonResponse({"error": "Access token expired"}, status=401)
        except jwt.InvalidTokenError:
            print("❌ Invalid JWT Token")
            return JsonResponse({"error": "Invalid access token"}, status=401)

        return None  # Request is allowed
