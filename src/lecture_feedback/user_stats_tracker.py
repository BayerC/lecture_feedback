import time
from enum import Enum, auto

from lecture_feedback.thread_safe_dict import ThreadSafeDict


class UserStatus(Enum):
    UNKNOWN = auto()
    GREEN = auto()
    YELLOW = auto()
    RED = auto()


class UserStatsTracker:
    """Manages button counters with thread-safe operations"""

    def __init__(self):
        self._user_stats = ThreadSafeDict()

    def set_user_status(self, user_id, status=UserStatus.UNKNOWN):
        self._user_stats[user_id] = {"status": status, "last_seen": time.time()}

    def set_user_active(self, user_id):
        self._user_stats[user_id]["last_seen"] = time.time()

    def get_user_stats(self):
        return self._user_stats.copy()

    def clean_up_old_users(self):
        users_to_delete = []
        for user_id, user_data in self._user_stats.items():
            if time.time() - user_data["last_seen"] > 4:
                users_to_delete.append(user_id)

        for user_id in users_to_delete:
            del self._user_stats[user_id]
