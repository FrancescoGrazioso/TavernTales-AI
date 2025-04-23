from textwrap import dedent

from characters.models.character import Character

SYSTEM_PROMPT = dedent(
    """\
You are TavernTales, an AI Dungeon Master for D&D 5e. 
Respond as immersive narrative **and** a JSON block:
{
  "narrative": "...",
  "character_updates": { "hp_current": -3, ... }
}
Rules: never break JSON schema; do not invent rules beyond SRD.
"""
)


def build_prompt(session, player_msg):
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

    return (
        SYSTEM_PROMPT
        + "\n===History===\n"
        + history_text
        + "\n===Character===\n"
        + char.to_sheet()
        + "\n===Player action===\n"
        + player_msg["content"]
    )
