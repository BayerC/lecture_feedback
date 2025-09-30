import streamlit as st
from streamlit_autorefresh import st_autorefresh
import uuid
from enum import Enum, auto
import time


class UserStatus(Enum):
    UNKNOWN = auto()
    GREEN = auto()
    YELLOW = auto()
    RED = auto()


class UserStatsTracker:
    """Manages button counters with thread-safe operations"""

    def __init__(self):
        self.user_stats = {}
        self.is_locked = False

    def add_user(self, user_id, status=UserStatus.UNKNOWN):
        while self.is_locked:
            time.sleep(0.1)
        self.is_locked = True
        self.user_stats[user_id] = {"status": status, "last_seen": time.time()}
        self.is_locked = False

    def get_user_stats(self):
        while self.is_locked:
            time.sleep(0.1)
        self.is_locked = True
        user_stats = self.user_stats.copy()
        self.is_locked = False
        return user_stats

    def clean_up_old_users(self):
        if self.is_locked:
            return

        self.is_locked = True
        users_to_delete = []
        for user_id, user_data in self.user_stats.items():
            if time.time() - user_data["last_seen"] > 4:
                users_to_delete.append(user_id)
        
        for user_id in users_to_delete:
            del self.user_stats[user_id]
        self.is_locked = False


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


    st.title(f"Debug Output:")
    st.write(f"current User ID: {st.session_state.user_id}")
    st.write(f"Current active users: {len(user_stats_tracker.get_user_stats())}")
    for user_id, status in user_stats_tracker.get_user_stats().items():
        st.write(f"- active user ID: {user_id}, Status: {status}")


if __name__ == "__main__":
    main()
