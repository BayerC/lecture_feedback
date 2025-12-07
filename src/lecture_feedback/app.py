import os
import uuid

import streamlit as st
from streamlit_autorefresh import st_autorefresh

from lecture_feedback.thread_safe_dict import ThreadSafeDict
from lecture_feedback.user_stats_tracker import (
    UserStatsTracker,
    UserStatus,
)


# TODO(#20): Also, should we clean up stale sessions? Maybe # noqa: FIX002
# remove sessions with empty user_stats_tracker
@st.cache_resource
def get_session_store() -> ThreadSafeDict:
    """Return a shared map of shared_session_id -> UserStatsTracker.

    This is stored as a cached resource so it's shared across reruns and
    across users in the same Streamlit process.
    """
    return ThreadSafeDict()


def add_tracker_for_session(shared_session_id: str) -> None:
    store = get_session_store()
    if shared_session_id in store:
        msg = f"Session ID '{shared_session_id}' already exists"
        raise ValueError(msg)

    store[shared_session_id] = UserStatsTracker()


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
    st.write(f"Session ID: {st.session_state.shared_session_id}")
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


def show_session_selection_screen() -> None:
    st.title("Welcome to Lecture Feedback App")
    st.write("Host or join a session to share feedback.")

    col1, col2 = st.columns([1, 1])

    with col1:
        if st.button("Start New Session", use_container_width=True):
            new_id = str(uuid.uuid4())
            add_tracker_for_session(new_id)
            st.session_state.shared_session_id = new_id
            st.rerun()

    with col2:
        join_id = st.text_input("Join Session by ID")
        if st.button("Join Session", use_container_width=True):
            if not join_id:
                st.warning("Please enter a Session ID to join.")
            else:
                store = get_session_store()
                if join_id in store:
                    st.session_state.shared_session_id = join_id
                    st.rerun()
                else:
                    st.error("Session ID not found")


def run() -> None:
    st_autorefresh(interval=2000, key="data_refresh")

    if "user_id" not in st.session_state:
        st.session_state.user_id = str(uuid.uuid4())

    if "shared_session_id" not in st.session_state:
        show_session_selection_screen()
        return

    user_stats_tracker = get_session_store()[st.session_state.shared_session_id]
    user_stats_tracker.clean_up_outdated_users()

    if st.session_state.user_id not in user_stats_tracker.get_user_stats():
        user_stats_tracker.add_user(st.session_state.user_id, UserStatus.UNKNOWN)

    user_stats_tracker.set_user_active(st.session_state.user_id)

    draw(user_stats_tracker)


if __name__ == "__main__" or "PYTEST_CURRENT_TEST" in os.environ:
    run()
