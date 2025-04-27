from django.db import models
from django_fsm import FSMField, transition

from game.models.party import Party


class Session(models.Model):
    STATUS = [
        ("draft", "draft"),
        ("active", "active"),
        ("paused", "paused"),
        ("finished", "finished"),
    ]
    party = models.ForeignKey(Party, on_delete=models.CASCADE, related_name="sessions")
    status = FSMField(default="draft", choices=STATUS)
    initiative = models.JSONField(blank=True, default=list)
    current_turn = models.PositiveIntegerField(null=True, default=0)
    ai_context_id = models.CharField(max_length=100, blank=True)
    summary = models.TextField(blank=True, default="")
    started_at = models.DateTimeField(null=True, blank=True)
    ended_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.party.name} – {self.status}"

    @transition(field=status, source="draft", target="active")
    def start(self):
        if self.initiative:
            self.current_turn = 0

    @transition(field=status, source="active", target="paused")
    def pause(self):
        pass

    @transition(field=status, source="paused", target="active")
    def resume(self):
        pass

    @transition(field=status, source=["active", "paused"], target="finished")
    def finish(self):
        pass

    def advance_turn(self):
        if not self.initiative:
            return
        if self.current_turn is None:
            self.current_turn = 0
        self.current_turn = (self.current_turn + 1) % len(self.initiative)
        self.save(update_fields=["current_turn"])
