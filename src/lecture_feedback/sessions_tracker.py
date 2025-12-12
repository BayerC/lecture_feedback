import uuid

from lecture_feedback.thread_safe_dict import ThreadSafeDict
from lecture_feedback.user_session import UserSession
from lecture_feedback.user_stats_tracker import UserStatsTracker


class SessionsTracker:
    """Global session tracker for all sessions and users."""

    def __init__(self) -> None:
        self.sessions = ThreadSafeDict()

    def create_session(self) -> str:
        session_id = str(uuid.uuid4())
        self.sessions[session_id] = UserStatsTracker()
        return session_id

    def session_exists(self, session_id: str) -> bool:
        return session_id in self.sessions

    def get_user_stats_tracker(self, session_id: str) -> UserStatsTracker:
        if session_id not in self.sessions:
            msg = f"Session {session_id} does not exist"
            raise ValueError(msg)
        return self.sessions[session_id]

    def add_user_to_session(self, session_id: str, user_id: str) -> None:
        tracker = self.get_user_stats_tracker(session_id)
        tracker.add_user(user_id)

    def join_session(self, user_session: UserSession, session_id: str) -> None:
        if user_session.is_in_session():
            msg = "User is already in a session"
            raise RuntimeError(msg)

        if not self.session_exists(session_id):
            msg = f"Session {session_id} does not exist"
            raise ValueError(msg)

        user_id = user_session.get_user_id()
        self.add_user_to_session(session_id, user_id)

        user_session.join_session_internal(session_id)
