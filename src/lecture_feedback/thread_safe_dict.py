from __future__ import annotations

import threading
from collections import UserDict
from typing import TYPE_CHECKING, Any, Self

if TYPE_CHECKING:
    from collections.abc import ItemsView, Iterator


class ThreadSafeDict(UserDict[str, Any]):
    def __init__(self, *args: Any, **kwargs: Any) -> None:  # noqa: ANN401
        self._lock = threading.RLock()
        super().__init__(*args, **kwargs)

    def __getitem__(self, key: str) -> Any:  # noqa: ANN401
        with self._lock:
            return super().__getitem__(key)

    def __setitem__(self, key: str, value: Any) -> None:  # noqa: ANN401
        with self._lock:
            return super().__setitem__(key, value)

    def __delitem__(self, key: str) -> None:
        with self._lock:
            return super().__delitem__(key)

    def __iter__(self) -> Iterator[str]:
        with self._lock:
            return iter(list(self.data))  # safe copy

    def copy(self) -> ThreadSafeDict:
        """Return a shallow copy as a ThreadSafeDict instance."""
        with self._lock:
            return ThreadSafeDict(self.data.copy())

    def items(self) -> ItemsView[str, Any]:
        with self._lock:
            return self.data.copy().items()

    def __enter__(self) -> Self:
        self._lock.acquire()
        return self

    def __exit__(self, *args: object) -> None:
        self._lock.release()
