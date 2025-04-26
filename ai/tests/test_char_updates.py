import json

import pytest
from asgiref.sync import sync_to_async
from channels.testing import WebsocketCommunicator
from django.test import override_settings
from django.urls import reverse
from rest_framework.test import APIClient

from ai.views import GeminiClient
from characters.models import Character
from core.asgi import application
from game.models import Party, Session
from users.models import User


@pytest.fixture(autouse=True)
def fake_ai(monkeypatch):
    monkeypatch.setattr(
        GeminiClient,
        "chat",
        lambda self, p: '{"narrative":"hits for 2","character_updates":{"hp_current":-2}}',
    )


@pytest.mark.asyncio
@pytest.mark.django_db(transaction=True)
@override_settings(
    CHANNEL_LAYERS={"default": {"BACKEND": "channels.layers.InMemoryChannelLayer"}}
)
async def test_ai_applies_diff_and_broadcasts():
    user = await sync_to_async(User.objects.create_user)("aragorn", password="Anduril")
    char = await sync_to_async(Character.objects.create)(
        user=user, name="Aragorn", char_class="Fighter", hp_current=30, hp_max=30
    )
    party = await sync_to_async(Party.objects.create)(owner=user, name="Fellowship")
    await sync_to_async(party.members.add)(user)
    session = await sync_to_async(Session.objects.create)(party=party, status="active")

    # WS listener
    comm = WebsocketCommunicator(application, f"/ws/session/{session.id}/")
    comm.scope["user"] = user
    assert (await comm.connect())[0]

    client = APIClient()
    client.force_authenticate(user=user)
    url = reverse("ai-action", args=[session.id])
    await sync_to_async(client.post)(
        url,
        {
            "sender_id": user.id,
            "character_id": char.id,
            "content": "attack",
        },
        format="json",
    )

    # Check patch broadcast
    data = json.loads(await comm.receive_from())
    assert data["diff"]["hp_current"] == 28
    await comm.disconnect()
