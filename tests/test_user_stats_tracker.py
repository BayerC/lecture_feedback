import time

import pytest

from lecture_feedback.user_stats_tracker import UserStatsTracker, UserStatus


def test_user_stats_tracker(monkeypatch: pytest.MonkeyPatch) -> None:
    tracker = UserStatsTracker()

    tracker.add_user("user1", UserStatus.GREEN)
    tracker.add_user("user2", UserStatus.YELLOW)
    tracker.add_user("user3", UserStatus.RED)

    tracker.update_user_status("user1", UserStatus.RED)
    tracker.set_user_active("user2")

    stats = tracker.get_user_stats()
    assert stats["user1"].status == UserStatus.RED
    assert stats["user2"].status == UserStatus.YELLOW
    assert stats["user3"].status == UserStatus.RED

    red_count, yellow_count, green_count, unknown_count = tracker.get_status_counts()
    assert red_count == 2
    assert yellow_count == 1
    assert green_count == 0
    assert unknown_count == 0


    fake_time = time.time()
    monkeypatch.setattr(time, "time", lambda: fake_time)

    fake_time += UserStatsTracker.USER_TIMEOUT_SECONDS + 1
    tracker.clean_up_outdated_users()
    assert len(tracker.get_user_stats()) == 0
