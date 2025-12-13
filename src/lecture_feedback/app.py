import streamlit as st
from streamlit_autorefresh import st_autorefresh

from lecture_feedback.session_manager import SessionManager
from lecture_feedback.sessions_tracker import SessionsTracker


@st.cache_resource
def get_sessions_tracker() -> SessionsTracker:
    return SessionsTracker()


def show_session_selection_screen(
    sessions_tracker: SessionsTracker,
    session_manager: SessionManager,
) -> None:
    st.title("Welcome to Lecture Feedback App")
    st.write("Host or join a session to share feedback.")

    col1, col2 = st.columns(2, gap="medium")

    with col1:
        st.subheader("Start New Session")
        if st.button("Create Session", use_container_width=True, key="start_session"):
            session_id = sessions_tracker.create_session()
            sessions_tracker.join_session(session_manager, session_id)
            st.rerun()

    with col2:
        st.subheader("Join Existing Session")
        join_id = st.text_input("Session ID", key="join_session_id")
        if st.button("Join Session", use_container_width=True, key="join_session"):
            if not join_id:
                st.warning("Please enter a Session ID to join.")
            else:
                try:
                    sessions_tracker.join_session(session_manager, join_id)
                    st.rerun()
                except ValueError:
                    st.error("Session ID not found")


def show_active_session(
    sessions_tracker: SessionsTracker,
    session_manager: SessionManager,
) -> None:
    session_id = session_manager.joined_session_id
    st.title("Active Session")
    st.write(f"**Session ID:** `{session_id}`")
    st.divider()

    user_stats_tracker = sessions_tracker.get_user_stats_tracker(session_id)
    user_stats = user_stats_tracker.get_user_stats_copy()
    st.subheader(f"Joined Users ({len(user_stats)})")
    for user_id, user_data in user_stats.items():
        st.write(f"• User ID: `{user_id}` - Status: {user_data.status.value}")


def run() -> None:
    st_autorefresh(interval=2000, key="data_refresh")

    sessions_tracker = get_sessions_tracker()
    session_manager = SessionManager()

    if not session_manager.is_in_session:
        show_session_selection_screen(sessions_tracker, session_manager)
    else:
        show_active_session(sessions_tracker, session_manager)
