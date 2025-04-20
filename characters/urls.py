from rest_framework.routers import DefaultRouter
from .views import CharacterViewSet

router = DefaultRouter()
router.register("", CharacterViewSet, basename="character")

urlpatterns = router.urls
