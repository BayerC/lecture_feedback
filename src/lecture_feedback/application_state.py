from lecture_feedback.session_state import SessionState
from lecture_feedback.thread_safe_dict import ThreadSafeDict


class ApplicationState:
    """Application-wide shared state."""

    def __init__(self) -> None:
        self.rooms: ThreadSafeDict[dict[str, SessionState]] = ThreadSafeDict()

    def is_in_room(self, session_id: str) -> bool:
        return any(session_id in room for room in self.rooms.values())

    def add_user_to_room(self, room_id: str, session: SessionState) -> None:
        if room_id not in self.rooms:
            self.rooms[room_id] = {}
        self.rooms[room_id][session.session_id] = session

    def all_user_status(self, room_id: str) -> str:
        if room_id not in self.rooms:
            return "No users in room"
        statuses = (
            session.get_status().value for session in self.rooms[room_id].values()
        )
        return ", ".join(statuses)
