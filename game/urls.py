from rest_framework.routers import SimpleRouter
from .views import ChatHistoryViewSet, PartyViewSet, JoinPartyView, SessionViewSet

router = SimpleRouter()
router.register("parties", PartyViewSet, basename="party")
router.register("parties", JoinPartyView, basename="party-join")
router.register("sessions", SessionViewSet, basename="session")
router.register(
    r"sessions/(?P<session_id>\d+)/messages",
    ChatHistoryViewSet,
    basename="chat-history",
)

urlpatterns = router.urls
