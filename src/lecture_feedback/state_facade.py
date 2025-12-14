import streamlit as st

from lecture_feedback.application_state import ApplicationState
from lecture_feedback.session_state import SessionState
from lecture_feedback.user_stats_tracker import UserStatsTracker


@st.cache_resource
def get_application_state() -> ApplicationState:
    return ApplicationState()


class StateFacade:
    """Unified interface coordinating application and session state."""

    def __init__(self) -> None:
        self.application_state = get_application_state()
        self.session_state = SessionState()

    def create_and_join_room(self) -> str:
        room_id = self.application_state.create_room()
        self.join_room(room_id)
        return room_id

    def join_room(self, room_id: str) -> None:
        if self.session_state.is_in_room:
            msg = "User is already in a room"
            raise RuntimeError(msg)

        if not self.application_state.room_exists(room_id):
            msg = f"Room {room_id} does not exist"
            raise ValueError(msg)

        user_id = self.session_state.user_id
        self.application_state.add_user_to_room(room_id, user_id)
        self.session_state.join_room(room_id)

    @property
    def is_in_room(self) -> bool:
        return self.session_state.is_in_room

    @property
    def current_room_id(self) -> str | None:
        return self.session_state.joined_room_id

    def get_user_stats_tracker(self, room_id: str) -> UserStatsTracker:
        return self.application_state.get_user_stats_tracker(room_id)
