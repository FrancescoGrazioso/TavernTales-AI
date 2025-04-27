import pytest
from django_fsm import TransitionNotAllowed

from game.models import Party, Session
from users.models import User


@pytest.mark.django_db
def test_fsm_transitions():
    owner = User.objects.create_user("dm", password="pass")
    party = Party.objects.create(owner=owner, name="DM party")
    session = Session.objects.create(party=party)

    # start
    session.initiative = [1, 2, 3]
    session.start()
    assert session.status == "active"

    # next turn cycles
    session.advance_turn()
    assert session.current_turn == 1
    session.advance_turn()
    session.advance_turn()
    assert session.current_turn == 0

    # pause/resume
    session.pause()
    assert session.status == "paused"
    session.resume()
    assert session.status == "active"

    # finish
    session.finish()
    assert session.status == "finished"
    with pytest.raises(TransitionNotAllowed):
        session.pause()
