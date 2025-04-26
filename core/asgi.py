"""
ASGI entrypoint for TavernTales-AI – compatibile con Django + Channels.
Ordine importante:
1. Imposta DJANGO_SETTINGS_MODULE
2. Chiama django.setup()
3. Importa moduli che toccano ORM (es. game.routing)
"""

import os

import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")
django.setup()

from channels.auth import AuthMiddlewareStack
# ruff: noqa: E402  # imports after django.setup() sono necessari
from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application

from game.routing import websocket_urlpatterns

application = ProtocolTypeRouter(
    {
        "http": get_asgi_application(),
        "websocket": AuthMiddlewareStack(URLRouter(websocket_urlpatterns)),
    }
)
