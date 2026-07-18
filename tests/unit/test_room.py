import pytest

from conftest import MockTime
from open_cups.room import Room
from open_cups.types import UserStatus


def test_upvote_nonexistent_question_does_not_crash() -> None:
    room = Room("room-id", "host-id")
    room.upvote_question("user-id", "nonexistent-question-id")


def test_user_cannot_vote_twice_on_same_question() -> None:
    room = Room("room-id", "host-id")

    room.add_question("creator-id", "Question text")
    questions = room.get_open_questions()
    assert len(questions) == 1
    question = questions[0]

    assert question.vote_count == 1
    assert "creator-id" in question.voter_ids

    room.upvote_question("user-2", question.id)
    questions = room.get_open_questions()
    question = questions[0]
    assert question.vote_count == 2
    assert "user-2" in question.voter_ids

    room.upvote_question("user-2", question.id)
    questions = room.get_open_questions()
    question = questions[0]
    assert question.vote_count == 2  # Still 2, not 3
    assert question.voter_ids == {"creator-id", "user-2"}


def test_creator_cannot_upvote_their_own_question() -> None:
    room = Room("room-id", "host-id")

    room.add_question("creator-id", "Question text")
    questions = room.get_open_questions()
    question = questions[0]

    initial_count = question.vote_count
    assert initial_count == 1

    room.upvote_question("creator-id", question.id)

    questions = room.get_open_questions()
    question = questions[0]
    assert question.vote_count == initial_count
    assert len(question.voter_ids) == 1


def test_multiple_users_can_upvote_same_question() -> None:
    room = Room("room-id", "host-id")

    room.add_question("creator-id", "Question text")
    questions = room.get_open_questions()
    question = questions[0]

    room.upvote_question("user-1", question.id)
    room.upvote_question("user-2", question.id)
    room.upvote_question("user-3", question.id)

    questions = room.get_open_questions()
    question = questions[0]
    assert question.vote_count == 4
    assert question.voter_ids == {
        "creator-id",
        "user-1",
        "user-2",
        "user-3",
    }


def test_questions_sorted_by_vote_count() -> None:
    room = Room("room-id", "host-id")

    room.add_question("user-1", "Question with 1 vote")
    room.add_question("user-2", "Question with 3 votes")
    room.add_question("user-3", "Question with 2 votes")

    questions = room.get_open_questions()
    question_with_3_votes = questions[1]
    question_with_2_votes = questions[2]

    room.upvote_question("user-4", question_with_3_votes.id)
    room.upvote_question("user-5", question_with_3_votes.id)

    room.upvote_question("user-6", question_with_2_votes.id)

    sorted_questions = room.get_open_questions()
    assert len(sorted_questions) == 3
    assert sorted_questions[0].vote_count == 3
    assert sorted_questions[1].vote_count == 2
    assert sorted_questions[2].vote_count == 1


def test_integration_with_stats_tracker(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr("open_cups.room.time.time", lambda: 10.0)
    room = Room("room-id", "host-id")

    assert room.get_status_history() == []


def test_is_session_live_true_for_recent_host(mock_time: MockTime) -> None:
    mock_time.current_time = 0.0
    room = Room("room-id", "host-id")

    mock_time.current_time = 5.0

    assert room.is_session_live("host-id", timeout_seconds=10)


def test_is_session_live_true_for_recent_client(mock_time: MockTime) -> None:
    mock_time.current_time = 0.0
    room = Room("room-id", "host-id")
    room.set_session_status("user", UserStatus.GREEN)

    mock_time.current_time = 5.0

    assert room.is_session_live("user", timeout_seconds=10)


def test_is_session_live_false_for_stale_client(mock_time: MockTime) -> None:
    mock_time.current_time = 0.0
    room = Room("room-id", "host-id")
    room.set_session_status("user", UserStatus.GREEN)

    mock_time.current_time = 20.0

    assert not room.is_session_live("user", timeout_seconds=10)


def test_is_session_live_false_for_unknown_session() -> None:
    room = Room("room-id", "host-id")

    assert not room.is_session_live("unknown-id", timeout_seconds=10)


def test_get_participants_by_activity_separates_active_and_inactive(
    mock_time: MockTime,
) -> None:
    mock_time.current_time = 0.0
    room = Room("room-id", "host-id")
    room.set_session_status("old-user", UserStatus.RED)

    mock_time.current_time = 100.0
    room.set_session_status("new-user", UserStatus.GREEN)

    active, inactive = room.get_participants_by_activity(inactivity_timeout_seconds=10)

    assert len(active) == 1
    assert active[0] == ("new-user", UserStatus.GREEN)
    assert len(inactive) == 1
    assert inactive[0] == ("old-user", UserStatus.RED)
