from rest_framework import serializers

from .models import ChatMessage, Party, Session


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


class SessionStateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Session
        fields = ("id", "status", "initiative", "current_turn")
        read_only_fields = fields


class ChatMessageSerializer(serializers.ModelSerializer):
    sender = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = ChatMessage
        fields = (
            "id",
            "session",
            "sender",
            "content",
            "roll_info",
            "toxicity_score",
            "created_at",
        )
        read_only_fields = fields  # Only server can create


class DiceRollSerializer(serializers.Serializer):
    expression = serializers.CharField()
    advantage = serializers.BooleanField(default=False)
    disadvantage = serializers.BooleanField(default=False)

    def validate(self, data):
        if data["advantage"] and data["disadvantage"]:
            raise serializers.ValidationError(
                "Cannot set both advantage and disadvantage"
            )
        return data
