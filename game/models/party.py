import secrets

from django.conf import settings
from django.db import models


def gen_invite():
    return secrets.token_urlsafe(6)


class Party(models.Model):
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="owned_parties"
    )
    name = models.CharField(max_length=60)
    invite_code = models.CharField(max_length=12, unique=True, default=gen_invite)
    members = models.ManyToManyField(
        settings.AUTH_USER_MODEL, related_name="parties", blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
