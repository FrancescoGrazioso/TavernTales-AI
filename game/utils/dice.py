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

    r1 = single_roll()
    if advantage or disadvantage:
        r2 = single_roll()
        chosen = max if advantage else min
        return chosen([r1, r2], key=lambda r: r.total)
    return r1
