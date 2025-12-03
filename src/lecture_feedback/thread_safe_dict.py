import threading
from collections.abc import Iterator
from typing import Any


class ThreadSafeDict:
    """A simple thread-safe dictionary with only the methods we need"""

    def __init__(self) -> None:
        self._data: dict[str, Any] = {}
        self._lock = threading.RLock()

    def __setitem__(self, key: str, value: Any) -> None:  # noqa: ANN401
        with self._lock:
            self._data[key] = value

    def __getitem__(self, key: str) -> Any:  # noqa: ANN401
        with self._lock:
            return self._data[key]

    def __delitem__(self, key: str) -> None:
        with self._lock:
            del self._data[key]

    def copy(self) -> dict[str, Any]:
        with self._lock:
            return self._data.copy()

    def items(self) -> Iterator[tuple[str, Any]]:
        with self._lock:
            return iter(self._data.copy().items())
