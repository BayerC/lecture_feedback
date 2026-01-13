import pandas as pd
import plotly.express as px
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
    st.subheader("Your Status")
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


def show_room_statistics(room: RoomState) -> None:
    participants = room.get_room_participants()

    # Count each status
    counts = {
        "Unknown": sum(1 for _, s in participants if s == UserStatus.UNKNOWN),
        "Red": sum(1 for _, s in participants if s == UserStatus.RED),
        "Yellow": sum(1 for _, s in participants if s == UserStatus.YELLOW),
        "Green": sum(1 for _, s in participants if s == UserStatus.GREEN),
    }

    df = pd.DataFrame([counts])

    # Create plotly figure
    fig = px.bar(
        df,
        x=df.index,
        y=df.columns,
        color_discrete_sequence=["#9CA3AF", "#EF4444", "#FBBF24", "#10B981"],
    )

    # Style the chart
    fig.update_layout(
        showlegend=False,
        xaxis={"visible": False},
        yaxis={"visible": False},
        margin={"l": 0, "r": 0, "t": 0, "b": 0},
    )

    disable_interactions_config = {
        "displayModeBar": False,
        "staticPlot": True,
    }

    # Center the chart
    _, col2, _ = st.columns([1, 2, 1])
    with col2:
        st.plotly_chart(fig, width="stretch", config=disable_interactions_config)
        st.text(f"Total participants: {len(participants)}")


def show_active_room(room: RoomState) -> None:
    st.title("Active Room")
    col1, col2 = st.columns([1, 4], vertical_alignment="center")
    with col1:
        st.write("**Room ID:**")
    with col2:
        st.code(room.room_id, language=None)
    st.divider()
    col_left, col_right = st.columns(2, gap="medium")
    with col_left:
        show_user_status_selection(room)
    with col_right:
        show_room_statistics(room)


def run() -> None:
    st_autorefresh(interval=AUTOREFRESH_INTERNAL_MS, key="data_refresh")

    match StateProvider().get_current():
        case RoomState() as room:
            room.remove_inactive_users(timeout_seconds=USER_REMOVAL_TIMEOUT_SECONDS)
            show_active_room(room)
        case LobbyState() as lobby:
            show_room_selection_screen(lobby)
