import uuid

import streamlit as st
from streamlit_autorefresh import st_autorefresh

from lecture_feedback.user_stats_tracker import (
    UserStatsTracker,
    UserStatus,
)


@st.cache_resource
def get_user_stats_tracker():
    """Get or create the shared counter manager instance"""
    return UserStatsTracker()


def draw(user_stats_tracker: UserStatsTracker):
    st.title("Lecture Feedback App")
    st.write(f"Num Users: {len(user_stats_tracker.get_user_stats())}")

    # create red green yellow buttons
    col1, col2, col3 = st.columns(3)

    with col1:
        if st.button("🔴 Red"):
            user_stats_tracker.update_user_status(
                st.session_state.user_id, UserStatus.RED
            )

    with col2:
        if st.button("🟡 Yellow"):
            user_stats_tracker.update_user_status(
                st.session_state.user_id, UserStatus.YELLOW
            )

    with col3:
        if st.button("🟢 Green"):
            user_stats_tracker.update_user_status(
                st.session_state.user_id, UserStatus.GREEN
            )

    # show accumulated color stats
    st.title("Accumulated Color Stats")

    red_count, yellow_count, green_count, unknown_count = (
        user_stats_tracker.get_status_counts()
    )

    st.write(f"Red: {red_count}")
    st.write(f"Yellow: {yellow_count}")
    st.write(f"Green: {green_count}")
    st.write(f"Unknown: {unknown_count}")

    st.title("Debug Output:")
    user_stats = user_stats_tracker.get_user_stats()
    current_status = user_stats[st.session_state.user_id].status
    st.write(
        f"current User ID: {st.session_state.user_id}", f"Status: {current_status}"
    )
    st.write(f"Current active users: {len(user_stats_tracker.get_user_stats())}")
    for user_id, user_data in user_stats_tracker.get_user_stats().items():
        st.write(f"- active user ID: {user_id}, Status: {user_data.status}")


def main():
    st_autorefresh(interval=2000, key="data_refresh")

    user_stats_tracker = get_user_stats_tracker()
    user_stats_tracker.clean_up_outdated_users()

    if "user_id" not in st.session_state:
        st.session_state.user_id = str(uuid.uuid4())
        user_stats_tracker.add_user(st.session_state.user_id, UserStatus.UNKNOWN)

    user_stats_tracker.set_user_active(st.session_state.user_id)

    draw(user_stats_tracker)


if __name__ == "__main__":
    main()
