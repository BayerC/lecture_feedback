import streamlit as st
from streamlit_autorefresh import st_autorefresh

from lecture_feedback.browser_session import BrowserSession
from lecture_feedback.session_manager import SessionsTracker


@st.cache_resource
def get_sessions_tracker() -> SessionsTracker:
    return SessionsTracker()


def show_session_selection_screen(
    sessions_tracker: SessionsTracker, browser_session: BrowserSession,
) -> None:
    st.title("Welcome to Lecture Feedback App")
    st.write("Host or join a session to share feedback.")

    col1, col2 = st.columns(2, gap="medium")

    with col1:
        st.subheader("Start New Session")
        if st.button("Create Session", use_container_width=True, key="start_session"):
            session_id = sessions_tracker.create_session()
            browser_session.join_session(session_id)
            sessions_tracker.add_user_to_session(
                session_id, browser_session.get_user_id(),
            )
            st.rerun()

    with col2:
        st.subheader("Join Existing Session")
        join_id = st.text_input("Session ID", key="join_session_id")
        if st.button("Join Session", use_container_width=True, key="join_session"):
            if not join_id:
                st.warning("Please enter a Session ID to join.")
            elif sessions_tracker.session_exists(join_id):
                browser_session.join_session(join_id)
                sessions_tracker.add_user_to_session(
                    join_id, browser_session.get_user_id(),
                )
                st.rerun()
            else:
                st.error("Session ID not found")


def show_active_session(
    sessions_tracker: SessionsTracker, browser_session: BrowserSession,
) -> None:
    session_id = browser_session.get_session_id()
    st.title("Active Session")
    st.write(f"**Session ID:** `{session_id}`")
    st.divider()

    user_stats_tracker = sessions_tracker.get_tracker(session_id)
    user_stats = user_stats_tracker.get_user_stats_copy()
    st.subheader(f"Joined Users ({len(user_stats)})")
    for user_id, user_data in user_stats.items():
        st.write(f"• User ID: `{user_id}` - Status: {user_data.status.value}")


def run() -> None:
    st_autorefresh(interval=2000, key="data_refresh")

    sessions_tracker = get_sessions_tracker()
    browser_session = BrowserSession()

    if not browser_session.is_in_session():
        show_session_selection_screen(sessions_tracker, browser_session)
    else:
        show_active_session(sessions_tracker, browser_session)
