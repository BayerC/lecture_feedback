from typing import Any

import pytest

from lecture_feedback.thread_safe_dict import ThreadSafeDict


def test_basic_operations() -> None:
    # Create a thread-safe dict
    thread_safe_dict: ThreadSafeDict[Any] = ThreadSafeDict()

    # Test setting and getting values
    thread_safe_dict["key1"] = "value1"
    thread_safe_dict["key2"] = {"nested": "dict"}

    assert thread_safe_dict["key1"] == "value1"
    assert thread_safe_dict["key2"]["nested"] == "dict"

    # Test copy
    copy_dict = thread_safe_dict.copy()
    assert copy_dict["key1"] == "value1"
    assert copy_dict["key2"]["nested"] == "dict"

    # Test items
    items = list(thread_safe_dict.items())
    assert len(items) == 2
    assert ("key1", "value1") in items

    # Test deletion
    del thread_safe_dict["key1"]
    with pytest.raises(KeyError):
        _ = thread_safe_dict["key1"]

    # Test context manager for atomic operations
    thread_safe_dict["counter"] = 0
    with thread_safe_dict:
        current = thread_safe_dict["counter"]
        thread_safe_dict["counter"] = current + 1
    assert thread_safe_dict["counter"] == 1
