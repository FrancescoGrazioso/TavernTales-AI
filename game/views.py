from rest_framework import viewsets, permissions, decorators, response, status, mixins

from game.models.chat import ChatMessage
from .models import Party, Session
from .serializers import ChatMessageSerializer, PartySerializer, SessionSerializer


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
            session__id=session_id,
            session__party__members=self.request.user
        )
