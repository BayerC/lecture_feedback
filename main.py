import streamlit as st
from datetime import datetime
from streamlit_autorefresh import st_autorefresh
import uuid
from enum import Enum, auto


class UserStatus(Enum):
    UNKNOWN = auto()
    GREEN = auto() 
    YELLOW = auto() 
    RED = auto() 
    



class UserStatsTracker:
    """Manages button counters with thread-safe operations"""

    def __init__(self):
        self.user_stats = {}

    def add_user(self, user_id, status = UserStatus.UNKNOWN):
        self.user_stats[user_id] = status

    def get_user_stats(self):
        return self.user_stats


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
    

    # show all user ids
    for user_id, status in user_stats_tracker.get_user_stats().items():
        st.write(f"User ID: {user_id}, Status: {status}")



if __name__ == "__main__":
    main()
