import streamlit as st
from streamlit_autorefresh import st_autorefresh

from lecture_feedback.room_manager import RoomManager
from lecture_feedback.session_manager import SessionManager


@st.cache_resource
def get_room_manager() -> RoomManager:
    return RoomManager()


def show_room_selection_screen(
    room_manager: RoomManager,
    session_manager: SessionManager,
) -> None:
    st.title("Welcome to Lecture Feedback App")
    st.write("Host or join a room to share feedback.")

    col1, col2 = st.columns(2, gap="medium")

    with col1:
        st.subheader("Start New Room")
        if st.button("Create Room", use_container_width=True, key="start_room"):
            room_id = room_manager.create_room()
            room_manager.join_room(session_manager, room_id)
            st.rerun()

    with col2:
        st.subheader("Join Existing Room")
        join_id = st.text_input("Room ID", key="join_room_id")
        if st.button("Join Room", use_container_width=True, key="join_room"):
            if not join_id:
                st.warning("Please enter a Room ID to join.")
            else:
                try:
                    room_manager.join_room(session_manager, join_id)
                    st.rerun()
                except ValueError:
                    st.error("Room ID not found")


def show_active_room(
    room_manager: RoomManager,
    session_manager: SessionManager,
) -> None:
    room_id = session_manager.joined_session_id
    st.title("Active Room")
    st.write(f"**Room ID:** `{room_id}`")
    st.divider()

    user_stats_tracker = room_manager.get_user_stats_tracker(room_id)
    user_stats = user_stats_tracker.get_user_stats_copy()
    st.subheader(f"{len(user_stats)} users joined")
    for user_id, user_data in user_stats.items():
        st.write(f"• User ID: `{user_id}` - Status: {user_data.status.value}")


def run() -> None:
    st_autorefresh(interval=2000, key="data_refresh")

    room_manager = get_room_manager()
    session_manager = SessionManager()

    if not session_manager.is_in_session:
        show_room_selection_screen(room_manager, session_manager)
    else:
        show_active_room(room_manager, session_manager)
