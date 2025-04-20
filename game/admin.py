from django.contrib import admin
from .models import Party, Session

@admin.register(Party)
class PartyAdmin(admin.ModelAdmin):
    list_display = ("name", "owner", "invite_code", "created_at")
    search_fields = ("name", "owner__username", "invite_code")

@admin.register(Session)
class SessionAdmin(admin.ModelAdmin):
    list_display = ("party", "status", "started_at", "ended_at")
    list_filter = ("status",)