from lecture_feedback.room import Room
from lecture_feedback.thread_safe_dict import ThreadSafeDict
from lecture_feedback.user_stats_tracker import UserStatus


class ApplicationState:
    """Application-wide shared state."""

    def __init__(self) -> None:
        """
        Initialize the ApplicationState and its thread-safe rooms mapping.
        
        Creates an empty ThreadSafeDict that maps room IDs (str) to Room instances and assigns it to `self.rooms`.
        
        Attributes:
            rooms (ThreadSafeDict[Room]): A thread-safe mapping of room IDs to Room objects, initially empty.
        """
        self.rooms: ThreadSafeDict[Room] = ThreadSafeDict()

    def get_session_room(self, session_id: str) -> Room | None:
        """
        Finds the Room that contains the given session ID.
        
        Parameters:
            session_id (str): The session identifier to locate.
        
        Returns:
            Room | None: The Room containing the session_id, or `None` if no such room exists.
        """
        for room in self.rooms.values():
            if session_id in room.sessions:
                return room
        return None

    def create_room(self, room_id: str, session_id: str) -> None:
        """
        Create a new Room and register an initial session with status `UserStatus.UNKNOWN`.
        
        If a room with the same `room_id` already exists, it will be replaced.
        
        Parameters:
            room_id (str): Identifier for the room to create.
            session_id (str): Session identifier to add to the room's sessions with `UserStatus.UNKNOWN`.
        """
        self.rooms[room_id] = Room(room_id)
        self.rooms[room_id].sessions[session_id] = UserStatus.UNKNOWN

    def join_room(self, room_id: str, session_id: str) -> None:
        """
        Add a session to an existing room and mark the session's status as UNKNOWN.
        
        Parameters:
            room_id (str): Identifier of the room to join.
            session_id (str): Identifier of the session to add to the room.
        
        Raises:
            ValueError: If the specified room does not exist (message: "Room {room_id} does not exist").
        """
        if room_id not in self.rooms:
            message = f"Room {room_id} does not exist"
            raise ValueError(message)
        self.rooms[room_id].sessions[session_id] = UserStatus.UNKNOWN