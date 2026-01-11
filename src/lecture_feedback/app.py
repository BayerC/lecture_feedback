import streamlit as st
from streamlit_autorefresh import st_autorefresh

from lecture_feedback.state_provider import (
    LobbyState,
    RoomState,
    StateProvider,
)
from lecture_feedback.user_status import UserStatus


def show_room_selection_screen(lobby: LobbyState) -> None:
    st.title("Welcome to Lecture Feedback App")
    st.write("Host or join a room to share feedback.")

    col_left, col_right = st.columns(2, gap="medium")

    with col_left:
        st.subheader("Start New Room")
        if st.button("Create Room", use_container_width=True, key="start_room"):
            lobby.create_room()
            st.rerun()

    with col_right:
        st.subheader("Join Existing Room")
        room_id = st.text_input("Room ID", key="join_room_id")
        if st.button("Join Room", use_container_width=True, key="join_room"):
            if not room_id:
                st.warning("Please enter a Room ID to join.")
            else:
                try:
                    lobby.join_room(room_id)
                    st.rerun()
                except ValueError:
                    st.error("Room ID not found")


def show_active_room(room: RoomState) -> None:
    st.title("Active Room")
    col1, col2 = st.columns([1, 4], vertical_alignment="center")
    with col1:
        st.write("**Room ID:**")
    with col2:
        st.code(room.room_id, language=None)
    st.divider()

    current_user_status = room.get_user_status()

    if current_user_status == UserStatus.UNKNOWN:
        status_options = [
            UserStatus.UNKNOWN,
            UserStatus.GREEN,
            UserStatus.YELLOW,
            UserStatus.RED,
        ]
        status_captions = [
            "Not decided yet",
            "can follow easily",
            "needs more explanation",
            "cannot follow at all",
        ]
    else:
        status_options = [
            UserStatus.GREEN,
            UserStatus.YELLOW,
            UserStatus.RED,
        ]
        status_captions = [
            "can follow easily",
            "needs more explanation",
            "cannot follow at all",
        ]

    selected_user_status = st.radio(
        "How good can you follow the lecture?",
        status_options,
        format_func=lambda s: s.value,
        captions=status_captions,
    )

    room.set_user_status(selected_user_status)

    if selected_user_status != UserStatus.UNKNOWN and current_user_status == UserStatus.UNKNOWN:
        st.rerun()



    for sid, user_status in room.get_room_participants():
        st.write(f"Session {sid}: {user_status.value}")


def run() -> None:
    st_autorefresh(interval=2000, key="data_refresh")

    match StateProvider().get_current():
        case RoomState() as room:
            show_active_room(room)
        case LobbyState() as lobby:
            show_room_selection_screen(lobby)
