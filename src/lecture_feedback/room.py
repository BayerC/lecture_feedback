from lecture_feedback.thread_safe_dict import ThreadSafeDict
from lecture_feedback.user_stats_tracker import UserStatus


class Room:
    def __init__(self, room_id: str) -> None:
        """
        Initialize a Room with its identifier and an empty thread-safe session map.
        
        Parameters:
            room_id (str): Unique identifier for the room.
        
        Detailed behavior:
            Stores `room_id` on the instance and creates `sessions`, a ThreadSafeDict mapping session IDs to UserStatus objects.
        """
        self._room_id = room_id
        self.sessions: ThreadSafeDict[UserStatus] = ThreadSafeDict()

    def get_session_status(self, session_id: str) -> UserStatus:
        """
        Retrieve the UserStatus associated with a given session ID.
        
        Parameters:
            session_id (str): The session identifier whose status to retrieve.
        
        Returns:
            UserStatus: The status object for the specified session.
        
        Raises:
            KeyError: If no status exists for the provided session_id.
        """
        return self.sessions[session_id]

    @property
    def room_id(self) -> str:
        """
        The room's unique identifier.
        
        Returns:
            room_id (str): The identifier for this room.
        """
        return self._room_id