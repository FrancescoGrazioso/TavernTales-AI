from django.contrib import admin
from .models import Character


@admin.register(Character)
class CharacterAdmin(admin.ModelAdmin):
    list_display = ("name", "user", "char_class", "level")
    list_filter = ("char_class", "level")
    search_fields = ("name", "user__username")
