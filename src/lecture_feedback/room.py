from collections.abc import Iterator

from lecture_feedback.thread_safe_dict import ThreadSafeDict
from lecture_feedback.user_status import UserStatus


class Room:
    def __init__(self, room_id: str) -> None:
        self._room_id = room_id
        self._sessions: ThreadSafeDict[UserStatus] = ThreadSafeDict()

    def get_session_status(self, session_id: str) -> UserStatus:
        return self._sessions[session_id]

    def set_session_status(self, session_id: str, status: UserStatus) -> None:
        self._sessions[session_id] = status

    def has_session(self, session_id: str) -> bool:
        return session_id in self._sessions

    def __iter__(self) -> Iterator[tuple[str, UserStatus]]:
        return iter(self._sessions.items())

    @property
    def room_id(self) -> str:
        return self._room_id
