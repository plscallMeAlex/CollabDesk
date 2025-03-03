import jwt
from datetime import datetime, timezone
from django.http import JsonResponse
from django.utils.deprecation import MiddlewareMixin


class JWTMiddleware(MiddlewareMixin):
    """Middleware to check if access token is valid during request"""

    """Also return 401 if access token is expired to let client refresh token"""

    def process_request(self, request):
        # By pass token refresh endpoint
        if request.path == "/token/refresh/" or request.path == "/users/login/":
            return None

        auth_header = request.headers.get("Authorization")
        if auth_header and auth_header.startswith("Bearer "):
            token = auth_header.split(" ")[1]
            try:
                decoded_token = jwt.decode(token, options={"verify_signature": False})
                exp_time = datetime.fromtimestamp(decoded_token["exp"], timezone.utc)

                if datetime.now(timezone.utc) > exp_time:
                    return JsonResponse({"error": "Access token expired"}, status=401)

            except jwt.ExpiredSignatureError:
                return JsonResponse({"error": "Access token expired"}, status=401)
            except jwt.DecodeError:
                return JsonResponse({"error": "Invalid token"}, status=401)

        return None
