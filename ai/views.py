from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from django.shortcuts import get_object_or_404
from game.models import Session
from .services import GeminiClient
from .prompt import build_prompt
import json


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

        # TODO: apply character_updates atomically here

        return Response(parsed, status=status.HTTP_200_OK)
