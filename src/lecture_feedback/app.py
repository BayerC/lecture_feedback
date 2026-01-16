import streamlit as st
from streamlit_autorefresh import st_autorefresh

from lecture_feedback.state_provider import (
    LobbyState,
    RoomState,
    StateProvider,
)
from lecture_feedback.user_status import UserStatus

AUTOREFRESH_INTERNAL_MS = 2000
USER_REMOVAL_TIMEOUT_SECONDS = 5


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


def show_user_status_selection(room: RoomState) -> None:
    current_user_status = room.get_user_status()
    status_options = [
        UserStatus.GREEN,
        UserStatus.YELLOW,
        UserStatus.RED,
    ]
    if current_user_status == UserStatus.UNKNOWN:
        status_options.append(UserStatus.UNKNOWN)

    index = status_options.index(current_user_status)
    selected_user_status = st.radio(
        "How well can you follow the lecture?",
        status_options,
        index=index,
        format_func=lambda s: s.value,
        captions=[status.caption() for status in status_options],
        key="user_status_selection",
    )
    room.set_user_status(selected_user_status)

    has_user_transitioned_away_from_unknown_status = (
        current_user_status == UserStatus.UNKNOWN
        and selected_user_status != UserStatus.UNKNOWN
    )
    if has_user_transitioned_away_from_unknown_status:
        st.rerun()


def show_active_room(room: RoomState) -> None:
    st.title("Active Room")
    col1, col2 = st.columns([1, 4], vertical_alignment="center")
    with col1:
        st.write("**Room ID:**")
    with col2:
        st.code(room.room_id, language=None)
    st.divider()

    show_user_status_selection(room)

    st.divider()

    for sid, user_status in room.get_room_participants():
        st.write(f"Session {sid}: {user_status.value}")


def run() -> None:
    st_autorefresh(interval=AUTOREFRESH_INTERNAL_MS, key="data_refresh")

    match StateProvider().get_current():
        case RoomState() as room:
            room.remove_inactive_users(timeout_seconds=USER_REMOVAL_TIMEOUT_SECONDS)
            show_active_room(room)
        case LobbyState() as lobby:
            show_room_selection_screen(lobby)
