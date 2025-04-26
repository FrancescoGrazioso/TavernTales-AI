import pytest

from game.utils.dice import DiceError, roll


def test_basic_roll():
    r = roll("2d6+3")
    assert 5 <= r.total <= 15
    assert len(r.rolls) == 2


def test_keep_highest():
    r = roll("4d6kh")
    assert len(r.rolls) == 4 and len(r.kept) == 1


def test_advantage():
    a = roll("d20", advantage=True)
    b = roll("d20", disadvantage=True)
    assert a.total >= b.total


def test_invalid():
    with pytest.raises(DiceError):
        roll("100d10000")
