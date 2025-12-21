import time
from collections import Counter
from dataclasses import dataclass
from enum import Enum

from lecture_feedback.thread_safe_dict import ThreadSafeDict


class UserStatus(Enum):
    UNKNOWN = "Unknown"
    GREEN = "🟢 Green"
    YELLOW = "🟡 Yellow"
    RED = "🔴 Red"


@dataclass
class UserData:
    status: UserStatus
    last_seen: float


class UserStatsTracker:
    USER_TIMEOUT_SECONDS = 4

    def __init__(self) -> None:
        """
        Initialize the UserStatsTracker instance.
        
        Creates a thread-safe internal storage named `_user_stats` for mapping user IDs (str) to `UserData` records.
        """
        self._user_stats: ThreadSafeDict = ThreadSafeDict()

    def add_user(self, user_id: str, status: UserStatus = UserStatus.UNKNOWN) -> None:
        """
        Add a new user with the given initial status and set its last-seen time to now.
        
        Parameters:
        	user_id (str): Unique identifier for the user to add.
        	status (UserStatus): Initial status assigned to the new user.
        
        Raises:
        	ValueError: If a user with the given `user_id` already exists.
        """
        if user_id in self._user_stats:
            msg = f"User {user_id} already exists"
            raise ValueError(msg)
        self._user_stats[user_id] = UserData(status=status, last_seen=time.time())

    def update_user_status(self, user_id: str, status: UserStatus) -> None:
        """
        Update the stored status for an existing user.
        
        Parameters:
            user_id (str): Identifier of the user whose status will be updated.
            status (UserStatus): New status to assign to the user.
        
        Raises:
            KeyError: If no user with `user_id` exists in the tracker.
        """
        with self._user_stats:
            self._user_stats[user_id].status = status

    def set_user_active(self, user_id: str) -> None:
        with self._user_stats:
            self._user_stats[user_id].last_seen = time.time()

    def get_user_stats_copy(self) -> dict[str, UserData]:
        return dict(self._user_stats.copy().data)

    def clean_up_outdated_users(self) -> None:
        users_to_delete = []
        for user_id, user_data in self._user_stats.items():
            if time.time() - user_data.last_seen > self.USER_TIMEOUT_SECONDS:
                users_to_delete.append(user_id)

        for user_id in users_to_delete:
            del self._user_stats[user_id]

    def get_status_counts(self) -> Counter[UserStatus]:
        return Counter(user.status for user in self.get_user_stats_copy().values())