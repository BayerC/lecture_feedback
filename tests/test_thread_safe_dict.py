import pytest
from lecture_feedback.thread_safe_dict import ThreadSafeDict


def test_basic_operations():
    """Test basic dictionary operations"""
    # Create a thread-safe dict
    tsd = ThreadSafeDict()

    # Test setting and getting values
    tsd["key1"] = "value1"
    tsd["key2"] = {"nested": "dict"}

    assert tsd["key1"] == "value1"
    assert tsd["key2"]["nested"] == "dict"

    # Test copy
    copy_dict = tsd.copy()
    assert copy_dict["key1"] == "value1"
    assert copy_dict["key2"]["nested"] == "dict"

    # Test items
    items = list(tsd.items())
    assert len(items) == 2
    assert ("key1", "value1") in items

    # Test deletion
    del tsd["key1"]
    with pytest.raises(KeyError):
        _ = tsd["key1"]
