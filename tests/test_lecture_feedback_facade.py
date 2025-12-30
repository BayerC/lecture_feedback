import pytest

from lecture_feedback.lecture_feedback_facade import LectureFeedbackFacade
from lecture_feedback.user_status import UserStatus


def test_get_current_room_id_raises_when_not_in_room() -> None:
    facade = LectureFeedbackFacade()
    with pytest.raises(RuntimeError, match="Not in any room"):
        facade.get_current_room_id()


def test_set_user_status_raises_when_not_in_room() -> None:
    facade = LectureFeedbackFacade()
    with pytest.raises(RuntimeError, match="Cannot set status: user not in any room"):
        facade.set_user_status(UserStatus.GREEN)


def test_get_room_participants_returns_empty_when_not_in_room() -> None:
    facade = LectureFeedbackFacade()
    assert facade.get_room_participants() == []
