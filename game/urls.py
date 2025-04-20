from rest_framework.routers import SimpleRouter
from .views import PartyViewSet, JoinPartyView, SessionViewSet

router = SimpleRouter()
router.register("parties", PartyViewSet, basename="party")
router.register("parties", JoinPartyView, basename="party-join")
router.register("sessions", SessionViewSet, basename="session")

urlpatterns = router.urls
