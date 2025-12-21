from lecture_feedback.thread_safe_dict import ThreadSafeDict
from lecture_feedback.user_stats_tracker import UserStatus


class Room:
    def __init__(self, room_id: str) -> None:
        self._room_id = room_id
        self.sessions: ThreadSafeDict[UserStatus] = ThreadSafeDict()

    def get_session_status(self, session_id: str) -> UserStatus:
        return self.sessions[session_id]

    @property
    def room_id(self) -> str:
        return self._room_id
