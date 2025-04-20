from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """
    Custom user with more fields.
    """

    ROLE_CHOICES = (
        ("admin", "Admin"),
        ("moderator", "Moderator"),
        ("player", "Player"),
        ("guest", "Guest"),
    )
    role = models.CharField(max_length=15, choices=ROLE_CHOICES, default="player")

    def __str__(self):
        return self.username
