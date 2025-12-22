from lecture_feedback.room import Room
from lecture_feedback.thread_safe_dict import ThreadSafeDict
from lecture_feedback.user_status import UserStatus


class ApplicationState:
    """Application-wide shared state."""

    def __init__(self) -> None:
        self.rooms: ThreadSafeDict[Room] = ThreadSafeDict()

    def get_session_room(self, session_id: str) -> Room | None:
        for room in self.rooms.values():
            if room.has_session(session_id):
                return room
        return None

    def create_room(self, room_id: str, session_id: str) -> None:
        self.rooms[room_id] = Room(room_id)
        self.rooms[room_id].set_session_status(session_id, UserStatus.UNKNOWN)

    def join_room(self, room_id: str, session_id: str) -> None:
        if room_id not in self.rooms:
            message = f"Room {room_id} does not exist"
            raise ValueError(message)
        self.rooms[room_id].set_session_status(session_id, UserStatus.UNKNOWN)
