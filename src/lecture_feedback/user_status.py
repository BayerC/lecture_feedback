from enum import Enum


class UserStatus(Enum):
    UNKNOWN = "Unknown"
    GREEN = "🟢 Green"
    YELLOW = "🟡 Yellow"
    RED = "🔴 Red"
