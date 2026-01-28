import time
import uuid
from collections.abc import Iterator
from dataclasses import dataclass, field

from lecture_feedback.thread_safe_dict import ThreadSafeDict
from lecture_feedback.user_status import UserStatus


@dataclass
class UserSession:
    status: UserStatus
    last_seen: float


@dataclass
class Question:
    id: str
    text: str
    voters: set[str] = field(default_factory=set)
    timestamp: float = field(default_factory=time.time)
    is_open: bool = True

    @property
    def vote_count(self) -> int:
        return len(self.voters)


class Room:
    def __init__(self, room_id: str, host_id: str) -> None:
        self._room_id = room_id
        self._sessions: ThreadSafeDict[UserSession] = ThreadSafeDict()
        self._host_id = host_id
        self._host_last_seen = time.time()
        self._questions: ThreadSafeDict[Question] = ThreadSafeDict()

    def is_host(self, session_id: str) -> bool:
        return self._host_id == session_id

    def update_host_last_seen(self) -> None:
        self._host_last_seen = time.time()

    def set_session_status(self, session_id: str, status: UserStatus) -> None:
        self._sessions[session_id] = UserSession(status, time.time())

    def get_session_status(self, session_id: str) -> UserStatus:
        return self._sessions[session_id].status

    def has_session(self, session_id: str) -> bool:
        if session_id in self._sessions:
            self._sessions[session_id].last_seen = time.time()
            return True
        return bool(self.is_host(session_id))

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

    def add_question(self, session_id: str, text: str) -> None:
        question_id = uuid.uuid4().hex
        question = Question(id=question_id, text=text)
        self._questions[question_id] = question

    def upvote_question(self, question_id: str, session_id: str) -> None:
        if question_id in self._questions:
            self._questions[question_id].voters.add(session_id)

    def has_voted(self, question_id: str, session_id: str) -> bool:
        if question_id in self._questions:
            return session_id in self._questions[question_id].voters
        return False

    def close_question(self, question_id: str) -> None:
        if question_id in self._questions:
            self._questions[question_id].is_open = False

    def get_open_questions(self) -> list[Question]:
        open_questions = [
            question for question in self._questions.values() if question.is_open
        ]
        return sorted(open_questions, key=lambda q: q.vote_count, reverse=True)
