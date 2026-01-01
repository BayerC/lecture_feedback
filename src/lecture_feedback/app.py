import streamlit as st
from streamlit_autorefresh import st_autorefresh

from lecture_feedback.lecture_feedback_facade import (
    FacadeFactory,
    LobbyFacade,
    RoomFacade,
)
from lecture_feedback.user_status import UserStatus


def show_room_selection_screen(facade: LobbyFacade) -> None:
    st.title("Welcome to Lecture Feedback App")
    st.write("Host or join a room to share feedback.")

    col_left, col_right = st.columns(2, gap="medium")

    with col_left:
        st.subheader("Start New Room")
        if st.button("Create Room", use_container_width=True, key="start_room"):
            facade.create_room()
            st.rerun()

    with col_right:
        st.subheader("Join Existing Room")
        room_id = st.text_input("Room ID", key="join_room_id")
        if st.button("Join Room", use_container_width=True, key="join_room"):
            if not room_id:
                st.warning("Please enter a Room ID to join.")
            else:
                try:
                    facade.join_room(room_id)
                    st.rerun()
                except ValueError:
                    st.error("Room ID not found")


def show_active_room(room_facade: RoomFacade) -> None:
    st.title("Active Room")
    st.write(f"**Room ID:** `{room_facade.room_id}`")
    st.divider()

    for status in [UserStatus.GREEN, UserStatus.YELLOW, UserStatus.RED]:
        if st.button(status.value, key=status.value):
            room_facade.set_user_status(status)

    for sid, user_status in room_facade.get_room_participants():
        st.write(f"Session {sid}: {user_status.value}")


def run() -> None:
    st_autorefresh(interval=2000, key="data_refresh")

    match FacadeFactory().get_facade():
        case RoomFacade() as room_facade:
            show_active_room(room_facade)
        case LobbyFacade() as lobby_facade:
            show_room_selection_screen(lobby_facade)
