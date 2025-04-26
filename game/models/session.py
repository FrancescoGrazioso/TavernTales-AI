from django.conf import settings
from django.db import models

from game.models.party import Party


class Session(models.Model):
    STATUS = [
        ("planning", "Planning"),
        ("active", "Active"),
        ("paused", "Paused"),
        ("finished", "Finished"),
    ]
    party = models.ForeignKey(Party, on_delete=models.CASCADE, related_name="sessions")
    status = models.CharField(max_length=10, choices=STATUS, default="planning")
    current_turn = models.ForeignKey(
        settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL
    )
    ai_context_id = models.CharField(max_length=100, blank=True)
    summary = models.TextField(blank=True, default="")
    started_at = models.DateTimeField(null=True, blank=True)
    ended_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.party.name} – {self.status}"
