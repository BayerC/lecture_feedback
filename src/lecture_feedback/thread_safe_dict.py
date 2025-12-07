from __future__ import annotations

import threading
from collections import UserDict
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from collections.abc import ItemsView, Iterator


class ThreadSafeDict(UserDict[str, Any]):
    """A simple thread-safe dictionary with only the methods we need"""

    def __init__(self, *args: Any, **kwargs: Any) -> None:  # noqa: ANN401
        # Set up the lock first so any operations performed by the
        # parent `UserDict` initializer (which may call `update`) can
        # safely use our overridden methods that expect `_lock`.
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
            # Create a new ThreadSafeDict initialized with a shallow copy of the data
            return ThreadSafeDict(self.data.copy())

    def items(self) -> ItemsView[str, Any]:
        with self._lock:
            # Return a view over a shallow copy of the underlying dict so
            # callers don't accidentally iterate over a mutating mapping.
            return self.data.copy().items()
