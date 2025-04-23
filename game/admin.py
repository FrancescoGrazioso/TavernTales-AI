from django.contrib import admin

from game.models.chat import ChatMessage
from .models import Party, Session


@admin.register(Party)
class PartyAdmin(admin.ModelAdmin):
    list_display = ("name", "owner", "invite_code", "created_at")
    search_fields = ("name", "owner__username", "invite_code")


@admin.register(Session)
class SessionAdmin(admin.ModelAdmin):
    list_display = ("party", "status", "started_at", "ended_at")
    list_filter = ("status",)

@admin.register(ChatMessage)
class ChatMessageAdmin(admin.ModelAdmin):
    list_display = ("id", "session", "sender", "short_content", "created_at")
    search_fields = ("content",)

    def short_content(self, obj):
        return f"{obj.content[:60]}..." if len(obj.content) > 60 else obj.content
    