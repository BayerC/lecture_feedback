import uuid

import streamlit as st

from lecture_feedback.application_state import ApplicationState
from lecture_feedback.room import Room
from lecture_feedback.room_cleanup import remove_empty_rooms
from lecture_feedback.session_state import SessionState
from lecture_feedback.user_status import UserStatus


class LobbyState:
    def __init__(
        self,
        application_state: ApplicationState,
        session_state: SessionState,
    ) -> None:
        self._application_state = application_state
        self._session_state = session_state

    def create_room(self) -> None:
        room_id = str(uuid.uuid4())
        self._application_state.create_room(room_id, self._session_state.session_id)

    def join_room(self, room_id: str) -> None:
        self._application_state.join_room(room_id, self._session_state.session_id)


class RoomState:
    def __init__(
        self,
        room: Room,
        session_id: str,
    ) -> None:
        self._room = room
        self._session_id = session_id

    @property
    def room_id(self) -> str:
        return self._room.room_id

    def set_user_status(self, status: UserStatus) -> None:
        self._room.set_session_status(self._session_id, status)

    def get_user_status(self) -> UserStatus:
        return self._room.get_session_status(self._session_id)

    def get_room_participants(self) -> list[tuple[str, UserStatus]]:
        return list(self._room)

    def remove_inactive_users(self, timeout_seconds: int) -> None:
        self._room.remove_inactive_sessions(timeout_seconds)


class Context:
    def __init__(self) -> None:
        self.application_state: ApplicationState = self._get_application_state()
        remove_empty_rooms(self.application_state)
        self.session_state = SessionState()

    @staticmethod
    @st.cache_resource
    def _get_application_state() -> ApplicationState:
        return ApplicationState()


class StateProvider:
    def __init__(self) -> None:
        self.context = Context()

    def get_current(self) -> LobbyState | RoomState:
        room = self.context.application_state.get_session_room(
            self.context.session_state.session_id,
        )
        if room is None:
            return LobbyState(
                self.context.application_state,
                self.context.session_state,
            )
        return RoomState(room, self.context.session_state.session_id)
