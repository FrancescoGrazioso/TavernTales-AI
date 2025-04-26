from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (
    ChatHistoryViewSet,
    JoinPartyView,
    PartyViewSet,
    SessionViewSet,
    dice_roll,
)

router = DefaultRouter()
router.register("parties", PartyViewSet, basename="party")
router.register("parties", JoinPartyView, basename="party-join")
router.register("sessions", SessionViewSet, basename="session")
router.register(
    r"sessions/(?P<session_id>\d+)/messages",
    ChatHistoryViewSet,
    basename="chat-history",
)

urlpatterns = [
    path("", include(router.urls)),
    path("dice/roll/", dice_roll, name="dice-roll"),
]
