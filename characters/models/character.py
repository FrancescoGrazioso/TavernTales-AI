from django.conf import settings
from django.db import models


class Character(models.Model):
    """Scheda D&D 5e semplificata, estensibile in futuro."""

    CLASSES = [
        ("barbarian", "Barbarian"),
        ("bard", "Bard"),
        ("cleric", "Cleric"),
        ("druid", "Druid"),
        ("fighter", "Fighter"),
        ("monk", "Monk"),
        ("paladin", "Paladin"),
        ("ranger", "Ranger"),
        ("rogue", "Rogue"),
        ("sorcerer", "Sorcerer"),
        ("warlock", "Warlock"),
        ("wizard", "Wizard"),
    ]

    ALIGNMENTS = [
        ("LG", "Lawful Good"),
        ("NG", "Neutral Good"),
        ("CG", "Chaotic Good"),
        ("LN", "Lawful Neutral"),
        ("N", "Neutral"),
        ("CN", "Chaotic Neutral"),
        ("LE", "Lawful Evil"),
        ("NE", "Neutral Evil"),
        ("CE", "Chaotic Evil"),
    ]

    # chiave esterna all’utente proprietario
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="characters"
    )

    # dati anagrafici
    name = models.CharField(max_length=60)
    char_class = models.CharField(max_length=20, choices=CLASSES)
    subclass = models.CharField(max_length=40, blank=True)
    race = models.CharField(max_length=40)
    background = models.CharField(max_length=40, blank=True)
    level = models.PositiveSmallIntegerField(default=1)
    alignment = models.CharField(max_length=2, choices=ALIGNMENTS, blank=True)

    # abilità base
    strength = models.PositiveSmallIntegerField(default=10)
    dexterity = models.PositiveSmallIntegerField(default=10)
    constitution = models.PositiveSmallIntegerField(default=10)
    intelligence = models.PositiveSmallIntegerField(default=10)
    wisdom = models.PositiveSmallIntegerField(default=10)
    charisma = models.PositiveSmallIntegerField(default=10)

    # risorse e statistiche di combattimento
    hp_max = models.PositiveSmallIntegerField(default=1)
    hp_current = models.PositiveSmallIntegerField(default=1)
    temp_hp = models.PositiveSmallIntegerField(default=0)
    armor_class = models.PositiveSmallIntegerField(default=10)
    initiative = models.SmallIntegerField(default=0)
    speed = models.PositiveSmallIntegerField(default=30)  # feet

    proficiency_bonus = models.SmallIntegerField(default=2)
    passive_perception = models.SmallIntegerField(default=10)

    # timestamp utili
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ("user", "name")
        ordering = ("name",)

    def __str__(self) -> str:
        return f"{self.name} (lvl {self.level} {self.char_class})"
