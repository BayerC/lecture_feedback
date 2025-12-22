import uuid

import streamlit as st
from streamlit_autorefresh import st_autorefresh

from lecture_feedback.application_state import ApplicationState, Room
from lecture_feedback.session_state import SessionState
from lecture_feedback.user_status import UserStatus


def show_room_selection_screen(
    application_state: ApplicationState,
    session_id: str,
) -> None:
    st.title("Welcome to Lecture Feedback App")
    st.write("Host or join a room to share feedback.")

    col1, col2 = st.columns(2, gap="medium")

    with col1:
        st.subheader("Start New Room")
        if st.button("Create Room", use_container_width=True, key="start_room"):
            room_id = str(uuid.uuid4())
            application_state.create_room(room_id, session_id)
            st.rerun()

    with col2:
        st.subheader("Join Existing Room")
        room_id = st.text_input("Room ID", key="join_room_id")
        if st.button("Join Room", use_container_width=True, key="join_room"):
            if not room_id:
                st.warning("Please enter a Room ID to join.")
            else:
                try:
                    application_state.join_room(room_id, session_id)
                    st.rerun()
                except ValueError:
                    st.error("Room ID not found")


def show_active_room(room: Room, session_id: str) -> None:
    st.title("Active Room")
    st.write(f"**Room ID:** `{room.room_id}`")
    st.divider()

    if st.button(UserStatus.RED.value):
        room.set_session_status(session_id, UserStatus.RED)
    if st.button(UserStatus.YELLOW.value):
        room.set_session_status(session_id, UserStatus.YELLOW)
    if st.button(UserStatus.GREEN.value):
        room.set_session_status(session_id, UserStatus.GREEN)
    if st.button(UserStatus.UNKNOWN.value):
        room.set_session_status(session_id, UserStatus.UNKNOWN)

    for sid, status in room:
        st.write(f"Session {sid}: {status.value}")


@st.cache_resource
def get_application_state() -> ApplicationState:
    return ApplicationState()


def run() -> None:
    st_autorefresh(interval=2000, key="data_refresh")

    application_state = get_application_state()
    session_state = SessionState()
    session_id = session_state.session_id

    if (room := application_state.get_session_room(session_id)) is not None:
        show_active_room(room, session_id)
    else:
        show_room_selection_screen(application_state, session_id)
