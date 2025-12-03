import time
from dataclasses import dataclass
from enum import Enum, auto

from lecture_feedback.thread_safe_dict import ThreadSafeDict


class UserStatus(Enum):
    UNKNOWN = auto()
    GREEN = auto()
    YELLOW = auto()
    RED = auto()


@dataclass
class UserData:
    status: UserStatus
    last_seen: float


class UserStatsTracker:
    """Manages button counters with thread-safe operations"""

    USER_TIMEOUT_SECONDS = 4

    def __init__(self) -> None:
        self._user_stats: ThreadSafeDict = ThreadSafeDict()

    def add_user(self, user_id: str, status: UserStatus = UserStatus.UNKNOWN) -> None:
        self._user_stats[user_id] = UserData(status=status, last_seen=time.time())

    def update_user_status(self, user_id: str, status: UserStatus) -> None:
        self._user_stats[user_id].status = status

    def set_user_active(self, user_id: str) -> None:
        self._user_stats[user_id].last_seen = time.time()

    def get_user_stats(self) -> dict[str, UserData]:
        return self._user_stats.copy()

    def clean_up_outdated_users(self) -> None:
        users_to_delete = []
        for user_id, user_data in self._user_stats.items():
            if time.time() - user_data.last_seen > self.USER_TIMEOUT_SECONDS:
                users_to_delete.append(user_id)

        for user_id in users_to_delete:
            del self._user_stats[user_id]

    def get_status_counts(self) -> tuple[int, int, int, int]:
        """Return counts of users by status"""
        user_stats = self.get_user_stats()
        red_count = sum(
            1 for user in user_stats.values() if user.status == UserStatus.RED
        )
        yellow_count = sum(
            1 for user in user_stats.values() if user.status == UserStatus.YELLOW
        )
        green_count = sum(
            1 for user in user_stats.values() if user.status == UserStatus.GREEN
        )
        unknown_count = sum(
            1 for user in user_stats.values() if user.status == UserStatus.UNKNOWN
        )
        return red_count, yellow_count, green_count, unknown_count
