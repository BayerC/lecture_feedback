from lecture_feedback.session_state import SessionState
from lecture_feedback.thread_safe_dict import ThreadSafeDict


class ApplicationState:
    """Application-wide shared state."""

    def __init__(self) -> None:
        self.rooms: ThreadSafeDict[dict[str, SessionState]] = ThreadSafeDict()

    def get_room(self, session_id: str) -> dict[str, SessionState] | None:
        for room in self.rooms.values():
            if session_id in room:
                return room
        return None

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
