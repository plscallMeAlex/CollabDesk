"""
ASGI config for server project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/howto/deployment/asgi/
"""

import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from django.urls import path
from api.consumers import ChatConsumer, VoiceChatConsumer

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "server.settings")

websocket_urlpatterns = [
    path("ws/chat/<room_name>/", ChatConsumer.as_asgi()),
    path("ws/voice/<room_name>/", VoiceChatConsumer.as_asgi()),
]

application = ProtocolTypeRouter(
    {
        "http": get_asgi_application(),
        "websocket": AuthMiddlewareStack(URLRouter(websocket_urlpatterns)),
    }
)
