from django.db import transaction

from characters.models import Character

ALLOWED_FIELDS = {
    "hp_current": int,
    "hp_max": int,
    "armor_class": int,
    "conditions": list,  # TODO: placeholder for future many-to-many
}


class CharacterPatchError(ValueError):
    """Custom error for invalid character patch operations."""

    pass


def apply_character_updates(char: Character, patch: dict) -> dict:
    """
    Applies the updates dict to the Character instance inside an atomic
    transaction. Returns a diff {field: new_value}.
    Numeric values may be absolute or relative (e.g. -3).
    """
    diff = {}
    with transaction.atomic():
        for field, value in patch.items():
            if field not in ALLOWED_FIELDS:
                raise CharacterPatchError(f"Field '{field}' not updatable")
            field_type = ALLOWED_FIELDS[field]
            if not isinstance(value, field_type):
                raise CharacterPatchError(f"{field} must be {field_type.__name__}")

            current = getattr(char, field)
            if field_type is int and isinstance(value, int):
                # Updated logic: treat all values as absolute unless explicitly negative
                new_val = current + value if value < 0 else value
            else:
                new_val = value

            setattr(char, field, new_val)
            diff[field] = new_val
        char.save(update_fields=list(diff.keys()))
    return diff
