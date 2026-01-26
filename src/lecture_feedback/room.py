import time
from collections.abc import Iterator
from dataclasses import dataclass

from lecture_feedback.thread_safe_dict import ThreadSafeDict
from lecture_feedback.user_status import UserStatus


@dataclass
class UserSession:
    status: UserStatus
    last_seen: float


class Room:
    def __init__(self, room_id: str, host_id: str) -> None:
        self._room_id = room_id
        self._sessions: ThreadSafeDict[UserSession] = ThreadSafeDict()
        self._host_id = host_id
        self._host_last_seen = time.time()

    def is_host(self, session_id: str) -> bool:
        return self._host_id == session_id

    def update_host_last_seen(self) -> None:
        self._host_last_seen = time.time()

    def set_session_status(self, session_id: str, status: UserStatus) -> None:
        self._sessions[session_id] = UserSession(status, time.time())

    def get_session_status(self, session_id: str) -> UserStatus:
        return self._sessions[session_id].status

    def has_session(self, session_id: str) -> bool:
        if session_id in self._sessions:
            self._sessions[session_id].last_seen = time.time()
            return True
        return False

    def __iter__(self) -> Iterator[tuple[str, UserStatus]]:
        return ((k, v.status) for k, v in self._sessions.items())

    @property
    def room_id(self) -> str:
        return self._room_id

    @property
    def is_empty(self) -> bool:
        return len(self._sessions) == 0

    def remove_inactive_sessions(self, timeout_seconds: int) -> None:
        current_time = time.time()
        users_to_remove = [
            session_id
            for session_id, user_session in self._sessions.items()
            if current_time - user_session.last_seen > timeout_seconds
        ]

        for session_id in users_to_remove:
            del self._sessions[session_id]
