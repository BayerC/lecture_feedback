from dataclasses import dataclass
from enum import Enum


class UserStatus(Enum):
    UNKNOWN = "Unknown"
    GREEN = "🟢 Green"
    YELLOW = "🟡 Yellow"
    RED = "🔴 Red"

    def caption(self) -> str:
        captions = {
            UserStatus.UNKNOWN: "Not decided yet",
            UserStatus.GREEN: "Following easily",
            UserStatus.YELLOW: "Need more explanation",
            UserStatus.RED: "Cannot follow",
        }
        return captions[self]


@dataclass
class UserSession:
    status: UserStatus
    last_seen: float


@dataclass
class Question:
    id: str
    text: str
    voter_ids: set[str]

    @property
    def vote_count(self) -> int:
        return len(self.voter_ids)


@dataclass
class StatusSnapshot:
    timestamp: float
    counts: dict[UserStatus, int]
    inactive_counts: dict[UserStatus, int]
