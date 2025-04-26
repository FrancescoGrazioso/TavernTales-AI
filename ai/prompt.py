from textwrap import dedent

from characters.models.character import Character
from game.models.session import Session

SCHEMA_BLOCK = dedent(
    """\
    Return **exactly** this JSON schema (no extra keys):

    {
      "narrative": string,
      "character_updates": {
        "hp_current": int,
        "hp_max": int,
        "armor_class": int
      },
      "dm_notes": string|null
    }
    """
)

SYSTEM_PROMPT = (
    "You are TavernTales, an AI Dungeon Master for D&D 5e.\n"
    + SCHEMA_BLOCK
    + "\nRules: never break JSON; do not invent rules beyond SRD."
)


def build_prompt(session: Session, player_msg: str) -> str:
    history = list(session.messages.order_by("-created_at")[:8])
    history_text = "\n".join(
        f"{m.sender.username if m.sender else 'AI'}: {m.content}"
        for m in reversed(history)
    )

    if char_id := player_msg.get("character_id"):
        char = Character.objects.get(id=char_id)
    else:
        char = Character.objects.filter(user_id=player_msg["sender_id"]).first()
        if not char:
            raise ValueError("No character found for sender")

    story_so_far = (session.summary + "\n") if session.summary else ""

    return (
        SYSTEM_PROMPT
        + "\n===Story so far===\n"
        + story_so_far
        + "===Recent turns===\n"
        + history_text
        + "\n===Character===\n"
        + char.to_sheet()
        + "\n===Player action===\n"
        + player_msg["content"]
    )
