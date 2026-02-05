import pytest

from lecture_feedback.room import Room
from lecture_feedback.user_status import UserStatus


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


def test_status_history_snapshot_interval(monkeypatch: pytest.MonkeyPatch) -> None:
    current_time = 10.0

    def fake_time() -> float:
        return current_time

    monkeypatch.setattr("lecture_feedback.room.time.time", fake_time)

    room = Room("room-id", "host-id", snapshot_interval_seconds=1)

    room.set_session_status("user-1", UserStatus.GREEN)
    history = room.get_status_history()
    assert len(history) == 1
    assert history[0].green_count == 1
    assert history[0].yellow_count == 0
    assert history[0].red_count == 0
    assert history[0].unknown_count == 0

    room.set_session_status("user-2", UserStatus.YELLOW)
    assert len(room.get_status_history()) == 1

    current_time = 11.0
    room.set_session_status("user-2", UserStatus.YELLOW)
    history = room.get_status_history()
    assert len(history) == 2
    assert history[-1].green_count == 1
    assert history[-1].yellow_count == 1


def test_status_history_trims_old_snapshots(monkeypatch: pytest.MonkeyPatch) -> None:
    current_time = 0.0

    def fake_time() -> float:
        return current_time

    monkeypatch.setattr("lecture_feedback.room.time.time", fake_time)

    room = Room("room-id", "host-id", snapshot_interval_seconds=0, max_snapshot_count=2)

    current_time = 1.0
    room.set_session_status("user-1", UserStatus.GREEN)
    current_time = 2.0
    room.set_session_status("user-2", UserStatus.YELLOW)
    current_time = 3.0
    room.set_session_status("user-3", UserStatus.RED)

    history = room.get_status_history()
    assert len(history) == 2
    assert history[0].timestamp == 2.0
    assert history[1].timestamp == 3.0
