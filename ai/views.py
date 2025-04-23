from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from django.shortcuts import get_object_or_404
from characters.models.character import Character
from game.models import Session
from .services import GeminiClient
from .prompt import build_prompt
import json
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from game.utils.char_patch import apply_character_updates, CharacterPatchError
from game.models import ChatMessage


class AiActionView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request, session_id: int):
        session = get_object_or_404(Session, id=session_id, party__members=request.user)
        prompt = build_prompt(session, request.data)
        ai_resp = GeminiClient().chat(prompt)
        try:
            json_block = ai_resp[ai_resp.index("{") : ai_resp.rindex("}") + 1]
            parsed = json.loads(json_block)
        except Exception:
            return Response({"error": "AI response malformed"}, status=500)

        try:
            char_id = request.data.get("character_id")
            char = session.party.members.get(id=request.user.id).characters.get(
                id=char_id
            )
        except Character.DoesNotExist:
            return Response({"error": "Character not found"}, status=400)

        try:
            diff = apply_character_updates(char, parsed.get("character_updates", {}))
        except CharacterPatchError as e:
            return Response({"error": str(e)}, status=400)

        # save AI narrative as ChatMessage
        ChatMessage.objects.create(
            session=session,
            sender=None,
            content=parsed["narrative"],
        )

        # broadcast narrative + patch
        channel_layer = get_channel_layer()
        payload = {
            "type": "state.patch",
            "message": {
                "narrative": parsed["narrative"],
                "character_id": char.id,
                "diff": diff,
            },
        }
        async_to_sync(channel_layer.group_send)(f"session_{session.id}", payload)

        return Response(parsed, status=status.HTTP_200_OK)
