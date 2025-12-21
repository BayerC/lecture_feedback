import uuid

import streamlit as st
from streamlit_autorefresh import st_autorefresh

from lecture_feedback.application_state import ApplicationState, Room
from lecture_feedback.session_state import SessionState
from lecture_feedback.user_stats_tracker import UserStatus


def show_room_selection_screen(
    application_state: ApplicationState,
    session_id: str,
) -> None:
    """
    Display the room selection UI allowing the user to create a new room or join an existing one.
    
    The left column provides a "Create Room" action which creates a room with a generated room ID and associates the current session with it, then refreshes the app. The right column lets the user enter a room ID and attempt to join; if the field is empty a warning is shown, and if the room ID is not found an error message is displayed. Successful creation or join triggers a rerun to update the UI.
    
    Parameters:
        session_id (str): The per-user session identifier used to associate this client with a room.
    """
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
    """
    Render the active room interface and let the current session select its feedback status.
    
    Parameters:
        room (Room): The active room object whose `sessions` mapping will be displayed and updated.
        session_id (str): Identifier for the current session; used as the key when recording the selected `UserStatus`.
    
    Detailed behavior:
        Displays the room ID, presents buttons to set the current session's status to `UserStatus.RED`, `UserStatus.YELLOW`, `UserStatus.GREEN`, or `UserStatus.UNKNOWN`, and lists all participants with their current status values.
    """
    st.title("Active Room")
    st.write(f"**Room ID:** `{room.room_id}`")
    st.divider()

    if st.button("red"):
        room.sessions[session_id] = UserStatus.RED
    if st.button("yellow"):
        room.sessions[session_id] = UserStatus.YELLOW
    if st.button("green"):
        room.sessions[session_id] = UserStatus.GREEN
    if st.button("unknown"):
        room.sessions[session_id] = UserStatus.UNKNOWN

    for sid, status in room.sessions.items():
        st.write(f"User {sid}: {status.value}")


@st.cache_resource
def get_application_state() -> ApplicationState:
    """
    Provide the application's shared ApplicationState instance.
    
    Returns:
        ApplicationState: The application's central state object (cached across Streamlit invocations).
    """
    return ApplicationState()


def run() -> None:
    """
    Run the Streamlit application UI and display the appropriate screen for the current session.
    
    Enables periodic UI refresh, initializes the application and session state, determines whether the current session is already in a room, and renders the active room interface if so or the room selection interface otherwise.
    """
    st_autorefresh(interval=2000, key="data_refresh")

    application_state = get_application_state()
    session_state = SessionState()
    session_id = session_state.session_id

    if (room := application_state.get_session_room(session_id)) is not None:
        show_active_room(room, session_id)
    else:
        show_room_selection_screen(application_state, session_id)