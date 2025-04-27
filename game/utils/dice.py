import random
import re
from dataclasses import dataclass
from typing import List

ROLL_RE = re.compile(
    r"""
    (?P<count>\d+)?d(?P<sides>\d+)
    (?P<keepdrop>[kd][HL]?)?
    (?P<modifier>[+-]\d+)?$""",
    re.VERBOSE | re.IGNORECASE,
)

MAX_COUNT = 40
MAX_SIDES = 1000


class DiceError(ValueError): ...


@dataclass
class RollResult:
    total: int
    rolls: List[int]
    kept: List[int]


def _apply_keep_drop(rolls: List[int], keep_drop: str | None) -> List[int]:
    if not keep_drop:
        return rolls
    if keep_drop.lower() in ("k", "kh"):  # keep highest
        return [max(rolls)]
    if keep_drop.lower() == "kl":  # keep lowest
        return [min(rolls)]
    if keep_drop.lower() == "d":  # drop highest
        rolls.remove(max(rolls))
        return rolls
    if keep_drop.lower() == "dl":  # drop lowest
        rolls.remove(min(rolls))
        return rolls
    raise DiceError("Bad keep/drop flag")


def roll(expr: str, advantage: bool = False, disadvantage: bool = False) -> RollResult:
    """
    Return RollResult(total, rolls, kept).
    Supports '2d20+5', 'd6', '4d6kh', etc.
    """
    m = ROLL_RE.match(expr.replace(" ", ""))
    if not m:
        raise DiceError("Bad expression")

    cnt = int(m.group("count") or 1)
    sides = int(m.group("sides"))
    if cnt > MAX_COUNT or sides > MAX_SIDES:
        raise DiceError("Dice too large")

    keep_drop = m.group("keepdrop")
    mod = int(m.group("modifier") or 0)

    def single_roll() -> RollResult:
        rolls = [random.randint(1, sides) for _ in range(cnt)]
        kept = _apply_keep_drop(rolls.copy(), keep_drop)
        return RollResult(sum(kept) + mod, rolls, kept)

    # --- Advantage / Disadvantage ----------------------------------------
    if advantage and disadvantage:
        raise DiceError("Cannot have both advantage and disadvantage")

    if advantage or disadvantage:
        # Rules as per D&D 5e: only valid for a single d20 roll
        if cnt != 1 or sides != 20 or keep_drop:
            raise DiceError("Advantage/Disadvantage only supported for plain 1d20")

        first = random.randint(1, sides)
        second = random.randint(1, sides)
        kept_val = max(first, second) if advantage else min(first, second)
        rolls = [first, second]
        kept = [kept_val]
        total = kept_val + mod
        return RollResult(total, rolls, kept)

    # --- Standard roll ----------------------------------------------------
    return single_roll()
