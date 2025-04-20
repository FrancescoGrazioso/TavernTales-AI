from rest_framework import serializers
from .models import Party, Session

class PartySerializer(serializers.ModelSerializer):
    members = serializers.StringRelatedField(many=True, read_only=True)
    class Meta:
        model = Party
        fields = ("id", "name", "owner", "invite_code", "members", "created_at")
        read_only_fields = ("id", "owner", "invite_code", "members", "created_at")

    def create(self, validated_data):
        user = self.context["request"].user
        party = Party.objects.create(owner=user, **validated_data)
        party.members.add(user)
        return party

class SessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Session
        fields = "__all__"
        read_only_fields = ("id", "started_at", "ended_at")