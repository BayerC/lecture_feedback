import uuid

from lecture_feedback.thread_safe_dict import ThreadSafeDict
from lecture_feedback.user_stats_tracker import UserStatsTracker


class ApplicationState:
    """Application-wide shared state."""

    def __init__(self) -> None:
        self.rooms: ThreadSafeDict[UserStatsTracker] = ThreadSafeDict()

    def create_room(self) -> str:
        room_id = str(uuid.uuid4())
        self.rooms[room_id] = UserStatsTracker()
        return room_id

    def room_exists(self, room_id: str) -> bool:
        return room_id in self.rooms

    def get_user_stats_tracker(self, room_id: str) -> UserStatsTracker:
        if room_id not in self.rooms:
            msg = f"Room {room_id} does not exist"
            raise ValueError(msg)
        return self.rooms[room_id]

    def add_user_to_room(self, room_id: str, user_id: str) -> None:
        user_stats_tracker = self.get_user_stats_tracker(room_id)
        user_stats_tracker.add_user(user_id)
