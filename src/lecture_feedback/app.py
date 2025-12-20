import streamlit as st
from streamlit_autorefresh import st_autorefresh

from lecture_feedback.application_state import ApplicationState
from lecture_feedback.session_state import SessionState
from lecture_feedback.state_facade import StateFacade
from lecture_feedback.user_stats_tracker import UserStatus


def show_room_selection_screen(state_facade: StateFacade) -> None:
    st.title("Welcome to Lecture Feedback App")
    st.write("Host or join a room to share feedback.")

    col1, col2 = st.columns(2, gap="medium")

    with col1:
        st.subheader("Start New Room")
        if st.button("Create Room", use_container_width=True, key="start_room"):
            state_facade.create_and_join_room()
            st.rerun()

    with col2:
        st.subheader("Join Existing Room")
        join_id = st.text_input("Room ID", key="join_room_id")
        if st.button("Join Room", use_container_width=True, key="join_room"):
            if not join_id:
                st.warning("Please enter a Room ID to join.")
            else:
                try:
                    state_facade.join_room(join_id)
                    st.rerun()
                except ValueError:
                    st.error("Room ID not found")


def show_active_room(state_facade: StateFacade) -> None:
    room_id = state_facade.current_room_id
    if room_id is None:
        msg = "User is not in a room"
        raise RuntimeError(msg)

    st.title("Active Room")
    st.write(f"**Room ID:** `{room_id}`")
    st.divider()

    user_stats_tracker = state_facade.get_user_stats_tracker(room_id)
    user_stats = user_stats_tracker.get_user_stats_copy()
    st.subheader(f"{len(user_stats)} users joined")
    for user_id, user_data in user_stats.items():
        st.write(f"• User ID: `{user_id}` - Status: {user_data.status.value}")


@st.cache_resource
def get_application_state() -> ApplicationState:
    return ApplicationState()


def run() -> None:
    st_autorefresh(interval=2000, key="data_refresh")

    # state_facade = StateFacade()
    application_state = get_application_state()
    session_state = SessionState()

    if (room := application_state.get_room(session_state.session_id)) is None:
        st.title("Not in Room")
        if st.button("Join Room", use_container_width=True, key="join_room"):
            application_state.add_user_to_room("xxx", session_state)
    else:
        st.title("In Room")
        if st.button("red"):
            session_state.set_status(UserStatus.RED)
        if st.button("yellow"):
            session_state.set_status(UserStatus.YELLOW)
        if st.button("green"):
            session_state.set_status(UserStatus.GREEN)
        if st.button("unknown"):
            session_state.set_status(UserStatus.UNKNOWN)

        st.write(f"User mean: {application_state.all_user_status(room)}")

    # application_state.is_in_room(session_state.session_id())
    # if not state_facade.is_in_room:
    #    show_room_selection_screen(state_facade)
    # else:
    #    show_active_room(state_facade)
