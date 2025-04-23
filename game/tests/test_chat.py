import json
import pytest
from asgiref.sync import sync_to_async
from channels.testing import WebsocketCommunicator
from core.asgi import application
from users.models import User
from game.models import Party, Session, ChatMessage
from django.test import override_settings

@pytest.mark.asyncio
@pytest.mark.django_db(transaction=True)
@override_settings(CHANNEL_LAYERS={"default": {"BACKEND": "channels.layers.InMemoryChannelLayer"}})
async def test_ws_message_saved():
    # ----- create DB objects in sync thread -----
    user = await sync_to_async(User.objects.create_user)(
        username="sam", password="Shire123"
    )
    party = await sync_to_async(Party.objects.create)(
        owner=user, name="Fellowship"
    )
    await sync_to_async(party.members.add)(user)
    session = await sync_to_async(Session.objects.create)(
        party=party, status="active"
    )
    # -------------------------------------------

    communicator = WebsocketCommunicator(
        application, f"/ws/session/{session.id}/"
    )
    communicator.scope["user"] = user
    connected, _ = await communicator.connect()
    assert connected

    await communicator.send_to(text_data=json.dumps({"content": "Hello!"}))
    data = json.loads(await communicator.receive_from())
    assert data["content"] == "Hello!"

    exists = await sync_to_async(ChatMessage.objects.filter(
        session=session, content="Hello!"
    ).exists)()
    assert exists
    await communicator.disconnect()