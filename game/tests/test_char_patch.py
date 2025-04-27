import pytest
from django.contrib.auth import get_user_model

from characters.models import Character
from game.utils.char_patch import CharacterPatchError, apply_character_updates


@pytest.mark.django_db
def test_apply_character_updates_valid_patch():
    User = get_user_model()
    user = User.objects.create_user(username="testuser", password="password")
    char = Character.objects.create(
        user=user, hp_current=10, hp_max=20, armor_class=15, conditions=[]
    )
    patch = {"hp_current": -5, "hp_max": 25, "armor_class": 18}
    diff = apply_character_updates(char, patch)

    assert diff == {"hp_current": 5, "hp_max": 25, "armor_class": 18}
    assert char.hp_current == 5
    assert char.hp_max == 25
    assert char.armor_class == 18


@pytest.mark.django_db
def test_apply_character_updates_invalid_field():
    User = get_user_model()
    user = User.objects.create_user(username="testuser", password="password")
    char = Character.objects.create(
        user=user, hp_current=10, hp_max=20, armor_class=15, conditions=[]
    )
    patch = {"invalid_field": 10}

    with pytest.raises(CharacterPatchError) as excinfo:
        apply_character_updates(char, patch)

    assert "Field 'invalid_field' not updatable" in str(excinfo.value)


@pytest.mark.django_db
def test_apply_character_updates_invalid_type():
    User = get_user_model()
    user = User.objects.create_user(username="testuser", password="password")
    char = Character.objects.create(
        user=user, hp_current=10, hp_max=20, armor_class=15, conditions=[]
    )
    patch = {"hp_current": "invalid_type"}

    with pytest.raises(CharacterPatchError) as excinfo:
        apply_character_updates(char, patch)

    assert "hp_current must be int" in str(excinfo.value)
