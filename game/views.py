from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.shortcuts import get_object_or_404
from django_fsm import can_proceed
from requests import Response
from rest_framework import decorators, mixins, permissions, response, status, viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework.views import APIView

from game.models.chat import ChatMessage
from game.utils.dice import DiceError, roll

from .models import Party, Session
from .serializers import (
    ChatMessageSerializer,
    DiceRollSerializer,
    PartySerializer,
    SessionSerializer,
    SessionStateSerializer,
)


class IsOwnerOrMember(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user == obj.owner or request.user in obj.members.all()


class PartyViewSet(viewsets.ModelViewSet):
    serializer_class = PartySerializer
    permission_classes = (permissions.IsAuthenticated, IsOwnerOrMember)

    def get_queryset(self):
        return Party.objects.filter(members=self.request.user)

    @decorators.action(detail=True, methods=["post"], url_path="invite")
    def invite(self, request, pk=None):
        party = self.get_object()
        return response.Response({"invite_code": party.invite_code})


class JoinPartyView(viewsets.ViewSet):
    permission_classes = (permissions.IsAuthenticated,)

    @decorators.action(detail=False, methods=["post"])
    def join(self, request):
        code = request.data.get("code")
        try:
            party = Party.objects.get(invite_code=code)
            party.members.add(request.user)
            return response.Response({"detail": "Joined"}, status=status.HTTP_200_OK)
        except Party.DoesNotExist:
            return response.Response(
                {"detail": "Invalid code"}, status=status.HTTP_404_NOT_FOUND
            )


class SessionViewSet(viewsets.ModelViewSet):
    serializer_class = SessionSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        return Session.objects.filter(party__members=self.request.user)


class ChatHistoryViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    serializer_class = ChatMessageSerializer
    permission_classes = (permissions.IsAuthenticated,)
    ordering = "-created_at"

    def get_queryset(self):
        session_id = self.kwargs["session_id"]
        return ChatMessage.objects.filter(
            session__id=session_id, session__party__members=self.request.user
        )


@api_view(["POST"])
@permission_classes([permissions.IsAuthenticated])
def dice_roll(request):
    ser = DiceRollSerializer(data=request.data)
    ser.is_valid(raise_exception=True)
    try:
        result = roll(
            ser.validated_data["expression"],
            ser.validated_data["advantage"],
            ser.validated_data["disadvantage"],
        )
    except DiceError as e:
        return Response({"error": str(e)}, status=400)

    return Response(
        {
            "total": result.total,
            "rolls": result.rolls,
            "kept": result.kept,
        },
        status=200,
    )


class SessionLifecycleView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request, session_id, action):
        session = get_object_or_404(Session, id=session_id, party__owner=request.user)

        if action == "start":
            if not can_proceed(session.start):
                return Response({"detail": "Cannot start"}, status=400)
            session.initiative = request.data.get("initiative", [])
            session.start()
        elif action == "pause":
            if not can_proceed(session.pause):
                return Response({"detail": "Cannot pause"}, status=400)
            session.pause()
        elif action == "resume":
            if not can_proceed(session.resume):
                return Response({"detail": "Cannot resume"}, status=400)
            session.resume()
        elif action == "finish":
            if not can_proceed(session.finish):
                return Response({"detail": "Cannot finish"}, status=400)
            session.finish()
        elif action == "next-turn":
            if session.status != "active":
                return Response({"detail": "Not active"}, status=400)
            session.advance_turn()
        else:
            return Response({"detail": "Unknown action"}, status=404)

        session.save()
        # broadcast state via WS
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            f"session_{session.id}",
            {"type": "state.patch", "message": SessionStateSerializer(session).data},
        )
        return Response(SessionStateSerializer(session).data)
