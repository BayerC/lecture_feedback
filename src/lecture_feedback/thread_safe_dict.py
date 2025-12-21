from __future__ import annotations

import threading
from collections import UserDict
from typing import TYPE_CHECKING, Any, Self

if TYPE_CHECKING:
    from collections.abc import ItemsView, Iterator


class ThreadSafeDict[T](UserDict[str, T]):
    def __init__(self, *args: Any, **kwargs: Any) -> None:  # noqa: ANN401
        """
        Initialize the ThreadSafeDict and its reentrant lock.
        
        Creates a reentrant lock on self._lock for synchronizing access and delegates initialization of the underlying mapping to the base UserDict with the given arguments.
        """
        self._lock = threading.RLock()
        super().__init__(*args, **kwargs)

    def __getitem__(self, key: Any) -> T:  # noqa: ANN401
        """
        Retrieve the value for the given key with thread-safe access.
        
        Returns:
            value (T): The value associated with `key`.
        """
        with self._lock:
            return super().__getitem__(key)

    def __setitem__(self, key: str, value: T) -> None:
        """
        Set the value for the given key in the mapping while ensuring thread-safe access.
        
        Acquires the container's reentrant lock before assigning the value to prevent concurrent mutations.
        """
        with self._lock:
            return super().__setitem__(key, value)

    def __delitem__(self, key: str) -> None:
        with self._lock:
            return super().__delitem__(key)

    def __iter__(self) -> Iterator[str]:
        """
        Return an iterator over a snapshot of the dictionary's keys to allow safe iteration while the mapping may change.
        
        Returns:
            Iterator[str]: An iterator over a list copy of the current keys (snapshot), preventing concurrent mutations from affecting iteration.
        """
        with self._lock:
            return iter(list(self.data))  # safe copy, in contrast to normal dict

    def copy(self) -> ThreadSafeDict[T]:
        """
        Create a shallow copy of the mapping and return it as a new ThreadSafeDict.
        
        Returns:
            ThreadSafeDict[T]: A new ThreadSafeDict containing a shallow copy of the original data.
        """
        with self._lock:
            return ThreadSafeDict(self.data.copy())

    def items(self) -> ItemsView[str, T]:
        """
        Return an items view based on a thread-safe shallow snapshot of the mapping.
        
        The method obtains the internal lock and returns an ItemsView produced from a shallow copy of the underlying data; changes to the original mapping after this call do not affect the returned view.
        
        Returns:
            ItemsView[str, T]: An items view reflecting a shallow copy of the current mapping.
        """
        with self._lock:
            return self.data.copy().items()

    def __enter__(self) -> Self:
        self._lock.acquire()
        return self

    def __exit__(self, *args: object) -> None:
        self._lock.release()