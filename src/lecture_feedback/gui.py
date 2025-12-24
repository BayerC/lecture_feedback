import uuid

import streamlit as st
from streamlit_autorefresh import st_autorefresh

from lecture_feedback.facade import App
from lecture_feedback.room import Room
from lecture_feedback.user_status import UserStatus


def show_room_selection_screen(app: App) -> None:
    st.title("Welcome to Lecture Feedback App")
    st.write("Host or join a room to share feedback.")

    col1, col2 = st.columns(2, gap="medium")

    with col1:
        st.subheader("Start New Room")
        if st.button("Create Room", use_container_width=True, key="start_room"):
            room_id = str(uuid.uuid4())
            app.create_room(room_id)
            st.rerun()

    with col2:
        st.subheader("Join Existing Room")
        room_id = st.text_input("Room ID", key="join_room_id")
        if st.button("Join Room", use_container_width=True, key="join_room"):
            if not room_id:
                st.warning("Please enter a Room ID to join.")
            else:
                try:
                    app.join_room(room_id)
                    st.rerun()
                except ValueError:
                    st.error("Room ID not found")


def show_active_room(app: App, room: Room) -> None:
    st.title("Active Room")
    st.write(f"**Room ID:** `{room.room_id}`")
    st.divider()

    if st.button(UserStatus.RED.value):
        app.set_session_status(UserStatus.RED)
    if st.button(UserStatus.YELLOW.value):
        app.set_session_status(UserStatus.YELLOW)
    if st.button(UserStatus.GREEN.value):
        app.set_session_status(UserStatus.GREEN)
    if st.button(UserStatus.UNKNOWN.value):
        app.set_session_status(UserStatus.UNKNOWN)

    for sid, status in room:
        st.write(f"Session {sid}: {status.value}")


def run() -> None:
    st_autorefresh(interval=2000, key="data_refresh")

    app = App()

    if (room := app.get_active_room()) is not None:
        show_active_room(app, room)
    else:
        show_room_selection_screen(app)
