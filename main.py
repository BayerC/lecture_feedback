import streamlit as st
from streamlit_autorefresh import st_autorefresh
import uuid
from enum import Enum, auto
import time
import threading


class UserStatus(Enum):
    UNKNOWN = auto()
    GREEN = auto()
    YELLOW = auto()
    RED = auto()


class UserStatsTracker:
    """Manages button counters with thread-safe operations"""

    def __init__(self):
        self._user_stats = {}
        self._lock = threading.RLock()

    def add_user(self, user_id, status=UserStatus.UNKNOWN):
        with self._lock:
            self._user_stats[user_id] = {"status": status, "last_seen": time.time()}

    def get_user_stats(self):
        with self._lock:
            return self._user_stats.copy()

    def clean_up_old_users(self):
        with self._lock:
            users_to_delete = []
            for user_id, user_data in self._user_stats.items():
                if time.time() - user_data["last_seen"] > 4:
                    users_to_delete.append(user_id)

            for user_id in users_to_delete:
                del self._user_stats[user_id]


@st.cache_resource
def get_user_stats_tracker():
    """Get or create the shared counter manager instance"""
    return UserStatsTracker()


def main():
    st_autorefresh(interval=2000, key="data_refresh")

    if "user_id" not in st.session_state:
        st.session_state.user_id = str(uuid.uuid4())

    user_stats_tracker = get_user_stats_tracker()
    user_stats_tracker.add_user(st.session_state.user_id)

    user_stats_tracker.clean_up_old_users()

    st.title("Lecture Feedback App")
    st.write(f"Num Users: {len(user_stats_tracker.get_user_stats())}")

    st.title("Debug Output:")
    st.write(f"current User ID: {st.session_state.user_id}")
    st.write(f"Current active users: {len(user_stats_tracker.get_user_stats())}")
    for user_id, status in user_stats_tracker.get_user_stats().items():
        st.write(f"- active user ID: {user_id}, Status: {status}")


if __name__ == "__main__":
    main()
