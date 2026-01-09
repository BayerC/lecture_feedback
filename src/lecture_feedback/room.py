import time
from collections.abc import Iterator

from lecture_feedback.thread_safe_dict import ThreadSafeDict
from lecture_feedback.user_status import UserStatus


class Room:
    def __init__(self, room_id: str) -> None:
        self._room_id = room_id
        self._sessions: ThreadSafeDict[UserStatus] = ThreadSafeDict()
        self._last_seen: dict[str, float] = {}

    def set_session_status(self, session_id: str, status: UserStatus) -> None:
        self._sessions[session_id] = status

    def has_session(self, session_id: str) -> bool:
        if session_id in self._sessions:
            self._last_seen[session_id] = time.time()
            return True
        return False

    def __iter__(self) -> Iterator[tuple[str, UserStatus]]:
        return iter(self._sessions.items())

    @property
    def room_id(self) -> str:
        return self._room_id

    def remove_inactive_sessions(self, timeout_seconds: int) -> None:
        current_time = time.time()
        users_to_remove = [
            session_id
            for session_id, last_seen in self._last_seen.items()
            if current_time - last_seen > timeout_seconds
        ]

        for session_id in users_to_remove:
            del self._sessions[session_id]
            del self._last_seen[session_id]
