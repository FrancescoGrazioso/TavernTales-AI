from rest_framework import viewsets, permissions, filters
from .models import Character
from .serializers import CharacterSerializer


class IsOwnerOrAdmin(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user.is_staff or obj.user_id == request.user.id


class CharacterViewSet(viewsets.ModelViewSet):
    """
    CRUD completo dei personaggi; filtrabile per classe e livello.
    """

    serializer_class = CharacterSerializer
    permission_classes = (permissions.IsAuthenticated, IsOwnerOrAdmin)
    filter_backends = (filters.OrderingFilter, filters.SearchFilter)
    ordering_fields = ("name", "level", "created_at")
    search_fields = ("name", "char_class", "race")

    def get_queryset(self):
        qs = Character.objects.all()
        # i player vedono solo i propri PG, admin tutto
        if not self.request.user.is_staff:
            qs = qs.filter(user=self.request.user)
        return qs
