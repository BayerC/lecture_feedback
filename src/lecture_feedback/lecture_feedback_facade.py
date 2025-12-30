import uuid

import streamlit as st

from lecture_feedback.application_state import ApplicationState
from lecture_feedback.room import Room
from lecture_feedback.session_state import SessionState
from lecture_feedback.user_status import UserStatus


class LectureFeedbackFacade:
    def __init__(self) -> None:
        self._application_state = self._get_application_state()
        self._session_state = SessionState()

    @staticmethod
    @st.cache_resource
    def _get_application_state() -> ApplicationState:
        """Singleton cached across all sessions."""
        return ApplicationState()

    @property
    def session_id(self) -> str:
        return self._session_state.session_id

    def is_in_room(self) -> bool:
        return self._get_current_room() is not None

    def get_current_room_id(self) -> str:
        room = self._get_current_room()
        if room is None:
            message = "Not in any room"
            raise RuntimeError(message)
        return room.room_id

    def create_room(self) -> str:
        room_id = str(uuid.uuid4())
        self._application_state.create_room(room_id, self.session_id)
        return room_id

    def join_room(self, room_id: str) -> None:
        self._application_state.join_room(room_id, self.session_id)

    def set_user_status(self, status: UserStatus) -> None:
        room = self._get_current_room()
        if room is None:
            message = "Cannot set status: user not in any room"
            raise RuntimeError(message)
        room.set_session_status(self.session_id, status)

    def get_room_participants(self) -> list[tuple[str, UserStatus]]:
        room = self._get_current_room()
        if room is None:
            return []
        return list(room)

    def _get_current_room(self) -> Room | None:
        return self._application_state.get_session_room(self.session_id)
