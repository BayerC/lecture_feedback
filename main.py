import uuid

import streamlit as st
from streamlit_autorefresh import st_autorefresh

from lecture_feedback.user_stats_tracker import (
    UserStatsTracker,
    UserStatus,
)


@st.cache_resource
def get_user_stats_tracker() -> UserStatsTracker:
    """Get or create the shared counter manager instance"""
    return UserStatsTracker()


def draw_debug_output(user_stats_tracker: UserStatsTracker) -> None:
    st.title("Debug Output:")
    user_stats = user_stats_tracker.get_user_stats()
    current_status = user_stats[st.session_state.user_id].status
    st.write(f"current User ID: {st.session_state.user_id}, Status: {current_status}")
    st.write(f"Current active users: {len(user_stats_tracker.get_user_stats())}")
    for user_id, user_data in user_stats_tracker.get_user_stats().items():
        st.write(f"- active user ID: {user_id}, Status: {user_data.status}")


def create_button(
    current_status: UserStatus,
    button_status: UserStatus,
    user_stats_tracker: UserStatsTracker,
) -> None:
    if current_status == button_status:
        st.button(
            button_status.value,
            use_container_width=True,
            type="primary",  # Highlight button if selected
        )
    elif st.button(
        button_status.value,
        use_container_width=True,
    ):
        user_stats_tracker.update_user_status(
            st.session_state.user_id,
            button_status,
        )
        st.rerun()


def draw(user_stats_tracker: UserStatsTracker) -> None:
    st.title("Lecture Feedback App")
    st.write(f"Num Users: {len(user_stats_tracker.get_user_stats())}")

    # Get current user status for highlighting
    user_stats = user_stats_tracker.get_user_stats()
    current_status = user_stats[st.session_state.user_id].status

    # Create large buttons that fill the screen width
    col1, col2, col3 = st.columns(3, gap="small")

    with col1:
        create_button(current_status, UserStatus.RED, user_stats_tracker)

    with col2:
        create_button(current_status, UserStatus.YELLOW, user_stats_tracker)

    with col3:
        create_button(current_status, UserStatus.GREEN, user_stats_tracker)

    # Add visual indicator for current selection
    st.markdown("---")
    if current_status == UserStatus.RED:
        st.error("🔴 **Currently selected: Red** - You need help")
    elif current_status == UserStatus.YELLOW:
        st.warning("🟡 **Currently selected: Yellow** - You're somewhat confused")
    elif current_status == UserStatus.GREEN:
        st.success("🟢 **Currently selected: Green** - You understand")
    else:
        st.info("⚪ **No selection** - Please choose your feedback")

    # show accumulated color stats
    st.title("Accumulated Color Stats")

    red_count, yellow_count, green_count, unknown_count = (
        user_stats_tracker.get_status_counts()
    )

    st.write(f"Red: {red_count}")
    st.write(f"Yellow: {yellow_count}")
    st.write(f"Green: {green_count}")
    st.write(f"Unknown: {unknown_count}")

    draw_debug_output(user_stats_tracker)


def main() -> None:
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
