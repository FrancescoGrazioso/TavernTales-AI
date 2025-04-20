import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from .models import Session


class SessionChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.session_id = self.scope["url_route"]["kwargs"]["session_id"]
        self.group_name = f"session_{self.session_id}"
        # basic permission: user must belong to party
        if await self.user_allowed():
            await self.channel_layer.group_add(self.group_name, self.channel_name)
            await self.accept()
        else:
            await self.close()

    @database_sync_to_async
    def user_allowed(self):
        user = self.scope["user"]
        try:
            session = Session.objects.get(id=self.session_id)
            return (
                user.is_authenticated
                and session.party.members.filter(id=user.id).exists()
            )
        except Session.DoesNotExist:
            return False

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.group_name, self.channel_name)

    async def receive(self, text_data):
        await self.channel_layer.group_send(
            self.group_name,
            {
                "type": "chat.message",
                "text": text_data,
                "sender": self.scope["user"].username,
            },
        )

    async def chat_message(self, event):
        await self.send(
            text_data=json.dumps({"sender": event["sender"], "text": event["text"]})
        )
