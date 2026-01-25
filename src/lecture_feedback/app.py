import pandas as pd
import plotly.express as px
import streamlit as st
from streamlit_autorefresh import st_autorefresh

from lecture_feedback.state_provider import (
    ClientState,
    HostState,
    LobbyState,
    StateProvider,
)
from lecture_feedback.user_status import UserStatus

AUTOREFRESH_INTERNAL_MS = 2000
USER_REMOVAL_TIMEOUT_SECONDS = (
    60  # if we go lower, chrome's background tab throttling causes faulty user removal
)

GREY_COLOR = "#9CA3AF"
RED_COLOR = "#EF4444"
YELLOW_COLOR = "#FBBF24"
GREEN_COLOR = "#10B981"


def show_room_selection_screen(lobby: LobbyState) -> None:
    if "room_id" in st.query_params:
        try:
            lobby.join_room(st.query_params["room_id"])
            st.rerun()
        except ValueError:
            st.error("Room ID from url not found")

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


def show_user_status_selection(room: ClientState) -> None:
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


def get_statistics_data_frame(room: HostState | ClientState) -> pd.DataFrame:
    participants = room.get_room_participants()
    counts = {
        status.value: sum(1 for _, s in participants if s == status)
        for status in UserStatus
    }
    df = pd.DataFrame([counts])
    # Reorder columns: UNKNOWN (bottom), RED, YELLOW, GREEN (top)
    column_order = [
        UserStatus.UNKNOWN.value,
        UserStatus.RED.value,
        UserStatus.YELLOW.value,
        UserStatus.GREEN.value,
    ]
    return df[[col for col in column_order if col in df.columns]]


def show_room_statistics(room: HostState | ClientState) -> None:
    df = get_statistics_data_frame(room)

    if df.sum().sum() == 0:
        st.info("No participants yet. Share the Room ID to get started!")
        return

    fig = px.bar(
        df,
        x=df.index,
        y=df.columns,
        color_discrete_sequence=[
            GREY_COLOR,
            RED_COLOR,
            YELLOW_COLOR,
            GREEN_COLOR,
        ],
    )

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

    _, col2, _ = st.columns([1, 2, 1])
    with col2:
        st.plotly_chart(fig, config=disable_interactions_config)
        st.text(f"Number of participants: {df.sum().sum()}")


def show_active_room_host(host_state: HostState) -> None:
    st.query_params["room_id"] = host_state.room_id
    st.title("Active Room")
    col1, col2 = st.columns([1, 4], vertical_alignment="center")
    with col1:
        st.write("**Room ID:**")
    with col2:
        st.code(host_state.room_id, language=None)
    st.divider()
    show_room_statistics(host_state)


def show_active_room_client(client_state: ClientState) -> None:
    st.query_params["room_id"] = client_state.room_id
    st.title("Active Room")
    col1, col2 = st.columns([1, 4], vertical_alignment="center")
    with col1:
        st.write("**Room ID:**")
    with col2:
        st.code(client_state.room_id, language=None)
    st.divider()
    col_left, col_right = st.columns(2, gap="medium")
    with col_left:
        show_user_status_selection(client_state)
    with col_right:
        show_room_statistics(client_state)


def run() -> None:
    st_autorefresh(interval=AUTOREFRESH_INTERNAL_MS, key="data_refresh")

    match StateProvider().get_current():
        case HostState() as host:
            host.remove_inactive_users(timeout_seconds=USER_REMOVAL_TIMEOUT_SECONDS)
            show_active_room_host(host)
        case ClientState() as client:
            show_active_room_client(client)
        case LobbyState() as lobby:
            show_room_selection_screen(lobby)
