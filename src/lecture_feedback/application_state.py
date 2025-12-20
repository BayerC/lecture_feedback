from lecture_feedback.thread_safe_dict import ThreadSafeDict
from lecture_feedback.user_stats_tracker import UserStatus


class Room:
    def __init__(self) -> None:
        self.sessions: ThreadSafeDict[UserStatus] = ThreadSafeDict()

    def get_session_status(self, session_id: str) -> UserStatus:
        return self.sessions[session_id]

class ApplicationState:
    """Application-wide shared state."""

    def __init__(self) -> None:
        self.rooms: ThreadSafeDict[Room] = ThreadSafeDict()

    def get_session_room(self, session_id: str) -> Room | None:
        for room in self.rooms.values():
            if session_id in room.sessions:
                return room
        return None

    def add_session_to_room(self, room_id: str,  session_id: str) -> None:
        if room_id not in self.rooms:
            self.rooms[room_id] = Room()
        self.rooms[room_id].sessions[session_id] = UserStatus.UNKNOWN
