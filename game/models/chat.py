from django.conf import settings
from django.db import models

class ChatMessage(models.Model):
    """
    Stores every message exchanged in a Session.
    For AI messages `sender` is NULL.
    """
    session = models.ForeignKey(
        "game.Session", on_delete=models.CASCADE, related_name="messages"
    )
    sender = models.ForeignKey(
        settings.AUTH_USER_MODEL, null=True, blank=True,
        on_delete=models.SET_NULL, related_name="chat_messages"
    )
    content = models.TextField()
    roll_info = models.JSONField(blank=True, null=True)
    toxicity_score = models.FloatField(default=0.0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ("created_at",)

    def __str__(self) -> str:
        who = self.sender.username if self.sender else "AI"
        return f"[{self.session_id}] {who}: {self.content[:40]}"