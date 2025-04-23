import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from characters.models.character import Character
from users.models import User
from game.models import Party, Session
from ai.views import GeminiClient
from django.test import override_settings
from asgiref.sync import sync_to_async


@pytest.fixture(autouse=True)
def no_real_api(monkeypatch):
    monkeypatch.setattr(
        GeminiClient,
        "chat",
        lambda self, prompt: '{"narrative":"ok","character_updates":{}}',
    )


@pytest.mark.asyncio
@override_settings(
    CHANNEL_LAYERS={"default": {"BACKEND": "channels.layers.InMemoryChannelLayer"}}
)
@pytest.mark.django_db
async def test_ai_action_flow():
    user = await sync_to_async(User.objects.create_user)("frodo", password="Ring123")
    char = await sync_to_async(Character.objects.create)(
        user=user,
        name="Frodo",
        char_class="Rogue",
        subclass="Thief",
    )
    party = await sync_to_async(Party.objects.create)(owner=user, name="Shire")
    await sync_to_async(party.members.add)(user)
    session = await sync_to_async(Session.objects.create)(party=party, status="active")
    client = APIClient()
    client.force_authenticate(user=user)
    url = reverse("ai-action", args=[session.id])
    resp = await sync_to_async(client.post)(
        url,
        {
            "sender_id": user.id,
            "character_id": char.id,
            "content": "I search the room",
        },
        format="json",
    )
    assert resp.status_code == 200
    assert "narrative" in resp.data


@pytest.mark.django_db
def test_ai_action_flow_fail():
    user = User.objects.create_user("frodo_fail", password="Ring123")
    party = Party.objects.create(owner=user, name="Shire")
    party.members.add(user)
    session = Session.objects.create(party=party, status="active")
    client = APIClient()
    client.force_authenticate(user=user)
    # expect exception because no character is assigned
    # to the user
    with pytest.raises(ValueError):
        client.post(
            reverse("ai-action", args=[session.id]),
            {
                "sender_id": user.id,
                "content": "I search the room",
            },
            format="json",
        )
