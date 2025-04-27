import json
import logging

from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from django.urls import reverse
from rest_framework.test import APIClient

from game.models.chat import ChatMessage

from .models import Session

log = logging.getLogger(__name__)


class SessionChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        session_id = self.scope["url_route"]["kwargs"]["session_id"]
        self.session = await database_sync_to_async(Session.objects.get)(id=session_id)
        # auth (run in thread‑safe DB context)
        if not await self.user_allowed():
            await self.close(code=403)
            return

        self.group_name = f"session_{session_id}"
        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.group_name, self.channel_name)

    @database_sync_to_async
    def user_allowed(self) -> bool:
        user = self.scope["user"]
        return (
            user.is_authenticated
            and self.session.party.members.filter(id=user.id).exists()
        )

    async def receive(self, text_data=None, bytes_data=None):
        try:
            data = json.loads(text_data)
        except (TypeError, ValueError):
            # plain text message, wrap it
            data = {"type": "chat", "content": text_data}

        msg_type = data.get("type", "chat")

        if msg_type == "player.action":
            await self._handle_player_action(data)
        else:
            await self._handle_plain_chat(data)

    async def _handle_player_action(self, data):
        user = self.scope["user"]
        char_id = data["character_id"]
        content = data["content"]

        # sync: save ChatMessage
        await database_sync_to_async(ChatMessage.objects.create)(
            session=self.session, sender=user, content=content
        )

        # call AI endpoint via DRF test client (in thread)
        ai_payload = {
            "sender_id": user.id,
            "character_id": char_id,
            "content": content,
        }

        resp_data = await database_sync_to_async(self._call_ai)(ai_payload)

        if not resp_data:
            await self.send(json.dumps({"type": "error", "detail": "AI error"}))
            return

        # broadcast narrative + diff
        await self.channel_layer.group_send(
            self.group_name,
            {
                "type": "ai.narrative",  # handled below
                "message": resp_data,
            },
        )

    async def _handle_plain_chat(self, data):
        """Fallback used by old tests: treat any message as simple chat echo."""
        user = self.scope["user"]
        content = data.get("content", "")
        await database_sync_to_async(ChatMessage.objects.create)(
            session=self.session, sender=user, content=content
        )
        payload = {"type": "chat", "sender": user.username, "content": content}
        await self.channel_layer.group_send(
            self.group_name, {"type": "chat_message", "message": payload}
        )

    def _call_ai(self, payload):
        client = APIClient()
        client.force_authenticate(user=self.scope["user"])
        url = reverse("ai-action", args=[self.session.id])
        resp = client.post(url, payload, format="json")
        if resp.status_code == 200:
            return resp.json()
        log.error("AI error %s: %s", resp.status_code, resp.content)
        return None

    async def chat_message(self, event):
        await self.send(text_data=json.dumps(event["message"]))

    async def state_patch(self, event):
        await self.send(text_data=json.dumps(event["message"]))

    async def ai_narrative(self, event):
        await self.send(text_data=json.dumps(event["message"]))
