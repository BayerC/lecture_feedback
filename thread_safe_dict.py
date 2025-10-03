import threading


class ThreadSafeDict:
    """A simple thread-safe dictionary with only the methods we need"""

    def __init__(self):
        self._data = {}
        self._lock = threading.RLock()

    def __setitem__(self, key, value):
        with self._lock:
            self._data[key] = value

    def __getitem__(self, key):
        with self._lock:
            return self._data[key]

    def __delitem__(self, key):
        with self._lock:
            del self._data[key]

    def copy(self):
        with self._lock:
            return self._data.copy()

    def items(self):
        with self._lock:
            return self._data.copy().items()
