from django.urls import path
from .consumers import SessionChatConsumer

# Con il router path() il leading slash è gestito automaticamente (scope["path"] = "/ws/...")
websocket_urlpatterns = [
    path("ws/session/<int:session_id>/", SessionChatConsumer.as_asgi()),
]