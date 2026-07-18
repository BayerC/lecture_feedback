import threading
import time
import uuid
from collections.abc import Iterator

from open_cups.stats_tracker import Config as StatsTrackerConfig
from open_cups.stats_tracker import StatsTracker
from open_cups.thread_safe_dict import ThreadSafeDict
from open_cups.types import Question, StatusSnapshot, UserSession, UserStatus


class Room:
    def __init__(self, room_id: str, host_id: str) -> None:
        self._room_id = room_id
        self._sessions: ThreadSafeDict[UserSession] = ThreadSafeDict()
        self._host_id = host_id
        self._host_last_seen = time.time()
        self._questions: ThreadSafeDict[Question] = ThreadSafeDict()
        self._stats_tracker = StatsTracker(StatsTrackerConfig())
        self._lock = threading.RLock()

    def is_host(self, session_id: str) -> bool:
        return self._host_id == session_id

    def update_host_last_seen(self) -> None:
        self._host_last_seen = time.time()

    def set_session_status(self, session_id: str, status: UserStatus) -> None:
        self._sessions[session_id] = UserSession(status, time.time())

    def record_status_snapshot(self, inactivity_timeout_seconds: float) -> None:
        with self._lock:
            self._stats_tracker.record_status_snapshot(
                self._sessions.values(),
                inactivity_timeout_seconds,
            )

    def get_session_status(self, session_id: str) -> UserStatus:
        return self._sessions[session_id].status

    def update_session(self, session_id: str) -> None:
        if session_id in self._sessions:
            self._sessions[session_id].last_seen = time.time()

    def has_session(self, session_id: str) -> bool:
        if session_id in self._sessions:
            return True
        return bool(self.is_host(session_id))

    def is_session_live(self, session_id: str, timeout_seconds: float) -> bool:
        current_time = time.time()
        if self.is_host(session_id):
            return current_time - self._host_last_seen <= timeout_seconds
        if session_id not in self._sessions:
            return False
        return current_time - self._sessions[session_id].last_seen <= timeout_seconds

    def get_participants_by_activity(
        self,
        inactivity_timeout_seconds: float,
    ) -> tuple[list[tuple[str, UserStatus]], list[tuple[str, UserStatus]]]:
        current_time = time.time()
        active = []
        inactive = []
        for session_id, user_session in self._sessions.items():
            if current_time - user_session.last_seen > inactivity_timeout_seconds:
                inactive.append((session_id, user_session.status))
            else:
                active.append((session_id, user_session.status))
        return active, inactive

    def __iter__(self) -> Iterator[tuple[str, UserStatus]]:
        return ((k, v.status) for k, v in self._sessions.items())

    @property
    def room_id(self) -> str:
        return self._room_id

    def is_host_inactive(self, timeout_seconds: int) -> bool:
        current_time = time.time()
        return current_time - self._host_last_seen > timeout_seconds

    def remove_inactive_sessions(self, timeout_seconds: int) -> None:
        current_time = time.time()
        users_to_remove = [
            session_id
            for session_id, user_session in self._sessions.items()
            if current_time - user_session.last_seen > timeout_seconds
        ]

        for session_id in users_to_remove:
            del self._sessions[session_id]

    def get_open_questions(self) -> list[Question]:
        open_questions = list(self._questions.values())
        return sorted(open_questions, key=lambda q: q.vote_count, reverse=True)

    def add_question(self, session_id: str, text: str) -> None:
        question_id = str(uuid.uuid4())
        question = Question(id=question_id, text=text, voter_ids={session_id})
        self._questions[question_id] = question

    def upvote_question(self, session_id: str, question_id: str) -> None:
        with self._questions:
            if question_id not in self._questions:
                return

            question = self._questions[question_id]

            if session_id in question.voter_ids:
                return

            question.voter_ids.add(session_id)

    def close_question(self, question_id: str) -> None:
        del self._questions[question_id]

    def get_status_history(self) -> list[StatusSnapshot]:
        return self._stats_tracker.status_history
