from rest_framework import serializers
from .models import Character


class CharacterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Character
        fields = "__all__"
        read_only_fields = ("id", "user", "created_at", "updated_at")

    # Level e ability score devono stare in range consentiti
    def validate_level(self, value):
        if not 1 <= value <= 20:
            raise serializers.ValidationError("Level must be between 1 and 20.")
        return value

    def validate(self, attrs):
        for ability in (
            "strength",
            "dexterity",
            "constitution",
            "intelligence",
            "wisdom",
            "charisma",
        ):
            score = attrs.get(ability, getattr(self.instance, ability, 10))
            if not 1 <= score <= 30:
                raise serializers.ValidationError(
                    {ability: "Ability scores must be 1‑30"}
                )
        return attrs

    def create(self, validated_data):
        user = self.context["request"].user
        return Character.objects.create(user=user, **validated_data)
