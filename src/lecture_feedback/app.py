import io

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import qrcode
import streamlit as st
from streamlit_autorefresh import st_autorefresh

from lecture_feedback.state_provider import (
    ClientState,
    HostState,
    LobbyState,
    RoomState,
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
            st.error("Room ID from URL not found")

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


def get_statistics_data_frame(room: RoomState) -> pd.DataFrame:
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
        height=250,
    )

    disable_interactions_config = {
        "displayModeBar": False,
        "staticPlot": True,
    }

    _, col2, _ = st.columns([1, 3, 1])
    with col2:
        st.plotly_chart(fig, config=disable_interactions_config)
        participant_count = df.sum().sum()
        st.markdown(
            f"<p style='text-align: center;'>"
            f"Number of participants: {participant_count}"
            f"</p>",
            unsafe_allow_html=True,
        )


def show_status_history_chart(host_state: HostState) -> None:
    status_history = host_state.get_status_history()

    if not status_history:
        st.info("No status history yet. Waiting for participants to join...")
        return

    session_start = host_state.session_start_time

    data = {
        "Time (seconds)": [
            snapshot.timestamp - session_start for snapshot in status_history
        ],
        UserStatus.GREEN.value: [snapshot.green_count for snapshot in status_history],
        UserStatus.YELLOW.value: [snapshot.yellow_count for snapshot in status_history],
        UserStatus.RED.value: [snapshot.red_count for snapshot in status_history],
        UserStatus.UNKNOWN.value: [
            snapshot.unknown_count for snapshot in status_history
        ],
    }

    df = pd.DataFrame(data)

    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=df["Time (seconds)"],
            y=df[UserStatus.GREEN.value],
            name=UserStatus.GREEN.value,
            mode="lines",
            line={"color": GREEN_COLOR, "width": 2},
            stackgroup="one",
        ),
    )

    fig.add_trace(
        go.Scatter(
            x=df["Time (seconds)"],
            y=df[UserStatus.YELLOW.value],
            name=UserStatus.YELLOW.value,
            mode="lines",
            line={"color": YELLOW_COLOR, "width": 2},
            stackgroup="one",
        ),
    )

    fig.add_trace(
        go.Scatter(
            x=df["Time (seconds)"],
            y=df[UserStatus.RED.value],
            name=UserStatus.RED.value,
            mode="lines",
            line={"color": RED_COLOR, "width": 2},
            stackgroup="one",
        ),
    )

    fig.add_trace(
        go.Scatter(
            x=df["Time (seconds)"],
            y=df[UserStatus.UNKNOWN.value],
            name=UserStatus.UNKNOWN.value,
            mode="lines",
            line={"color": GREY_COLOR, "width": 2},
            stackgroup="one",
        ),
    )

    fig.update_layout(
        xaxis={"title": "Time (seconds)"},
        yaxis={"title": "Number of participants"},
        hovermode="x unified",
        legend={
            "orientation": "h",
            "yanchor": "bottom",
            "y": 1.02,
            "xanchor": "right",
            "x": 1,
        },
        margin={"l": 0, "r": 0, "t": 40, "b": 0},
        height=400,
    )

    st.plotly_chart(fig, use_container_width=True)


def generate_qr_code_image(room_id: str) -> bytes:
    base_url = st.context.url
    join_url = f"{base_url}?room_id={room_id}"

    url_qr_code = qrcode.QRCode(
        border=0,
    )
    url_qr_code.add_data(join_url)
    url_qr_code.make(fit=True)

    img = url_qr_code.make_image(fill_color="black", back_color="white")
    img_bytes = io.BytesIO()
    img.save(img_bytes)
    return img_bytes.getvalue()


def show_active_room_header(room_id: str) -> None:
    st.query_params["room_id"] = room_id
    left, right = st.columns([4, 1], vertical_alignment="center")
    with left:
        st.title("Active Room")
    with right:
        st.image(generate_qr_code_image(room_id), width="content")

    col_1, col_2 = st.columns([1, 4], vertical_alignment="center")
    with col_1:
        st.write("**Room ID:**")
    with col_2:
        st.code(room_id, language=None)

    st.divider()


def show_open_questions(state: HostState | ClientState) -> None:
    st.subheader("Open Questions")
    open_questions = state.get_open_questions()
    if not open_questions:
        st.info("No questions yet.")
    else:
        for question in open_questions:
            col1, col3 = st.columns([5, 1], vertical_alignment="center")
            with col1:
                st.write(question.text)
            with col3:
                if isinstance(state, HostState):
                    if st.button(
                        f"{question.vote_count} ✅",
                        key=f"close_{question.id}",
                        help="Close question",
                    ):
                        state.close_question(question.id)
                        st.rerun()
                elif isinstance(state, ClientState):
                    has_voted = state.has_voted(question)
                    if st.button(
                        f"{question.vote_count} 🆙",
                        key=f"upvote_{question.id}",
                        disabled=has_voted,
                    ):
                        state.upvote_question(question.id)
                        st.rerun()


def show_active_room_host(host_state: HostState) -> None:
    show_active_room_header(host_state.room_id)
    show_room_statistics(host_state)

    st.divider()

    st.subheader("Status Evolution Over Time")
    show_status_history_chart(host_state)

    st.divider()

    show_open_questions(host_state)


def show_active_room_client(client_state: ClientState) -> None:
    show_active_room_header(client_state.room_id)

    col_left, col_right = st.columns(2, gap="medium")
    with col_left:
        show_user_status_selection(client_state)
    with col_right:
        show_room_statistics(client_state)

    st.divider()

    def handle_question_submit() -> None:
        question = st.session_state.question_input
        if question and question.strip():
            client_state.submit_question(question.strip())
            st.session_state.question_input = ""

    st.text_input(
        "Ask a Question",
        key="question_input",
        placeholder="Type your question here... (Press Enter to submit)",
        on_change=handle_question_submit,
    )

    st.divider()

    show_open_questions(client_state)


def run() -> None:
    st_autorefresh(interval=AUTOREFRESH_INTERNAL_MS, key="data_refresh")

    state_provider = StateProvider()
    cleanup = state_provider.get_cleanup(USER_REMOVAL_TIMEOUT_SECONDS)
    cleanup.cleanup_all()

    match state_provider.get_current():
        case HostState() as host:
            show_active_room_host(host)
        case ClientState() as client:
            show_active_room_client(client)
        case LobbyState() as lobby:
            show_room_selection_screen(lobby)
