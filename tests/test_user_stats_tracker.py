import time

import pytest

from lecture_feedback.user_stats_tracker import UserStatsTracker, UserStatus


def test_user_stats_tracker(monkeypatch: pytest.MonkeyPatch) -> None:
    fake_time = time.time()
    monkeypatch.setattr(time, "time", lambda: fake_time)

    tracker = UserStatsTracker()

    tracker.add_user("user1", UserStatus.GREEN)
    fake_time += 1
    tracker.add_user("user2", UserStatus.YELLOW)
    fake_time += 1
    tracker.add_user("user3", UserStatus.RED)
    fake_time += 1

    tracker.update_user_status("user1", UserStatus.RED)
    tracker.set_user_active("user2")

    stats = tracker.get_user_stats()
    assert stats["user1"].status == UserStatus.RED
    assert stats["user2"].status == UserStatus.YELLOW
    assert stats["user3"].status == UserStatus.RED

    counts = tracker.get_status_counts()
    assert counts[UserStatus.RED] == 2
    assert counts[UserStatus.YELLOW] == 1
    assert counts[UserStatus.GREEN] == 0
    assert counts[UserStatus.UNKNOWN] == 0

    tracker.clean_up_outdated_users()
    assert len(tracker.get_user_stats()) == 3
    fake_time += 2.5
    tracker.clean_up_outdated_users()
    assert len(tracker.get_user_stats()) == 2
    fake_time += 1
    tracker.clean_up_outdated_users()
    assert len(tracker.get_user_stats()) == 1
    assert "user2" in tracker.get_user_stats()  # since this user was set active later
    fake_time += 1
    tracker.clean_up_outdated_users()
    assert len(tracker.get_user_stats()) == 0
