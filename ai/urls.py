from django.urls import path
from .views import AiActionView

urlpatterns = [
    path(
        "sessions/<int:session_id>/ai-action/",
        AiActionView.as_view(),
        name="ai-action",
    ),
]
