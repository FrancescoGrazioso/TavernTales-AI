import pytest
from asgiref.sync import sync_to_async
from channels.testing import WebsocketCommunicator
from django.test import override_settings

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
        lambda self, p: '{"narrative":"ok","character_updates":{}}',
    )


@pytest.mark.asyncio
@pytest.mark.django_db(transaction=True)
@override_settings(
    CHANNEL_LAYERS={"default": {"BACKEND": "channels.layers.InMemoryChannelLayer"}}
)
async def test_live_flow():
    # create objects in sync
    user = await sync_to_async(User.objects.create_user)("sam", password="pass")
    char = await sync_to_async(Character.objects.create)(
        user=user, name="Sam", char_class="Fighter", hp_current=10, hp_max=10
    )
    party = await sync_to_async(Party.objects.create)(owner=user, name="Hobbits")
    await sync_to_async(party.members.add)(user)
    session = await sync_to_async(Session.objects.create)(party=party, status="active")

    comm = WebsocketCommunicator(application, f"/ws/session/{session.id}/")
    comm.scope["user"] = user
    assert (await comm.connect())[0] is True

    await comm.send_json_to(
        {"type": "player.action", "character_id": char.id, "content": "attack"}
    )
    data = await comm.receive_json_from()
    assert data["narrative"] == "ok"
    await comm.disconnect()
