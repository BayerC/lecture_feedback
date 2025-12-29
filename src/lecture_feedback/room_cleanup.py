import functools
import time
from collections.abc import Callable

import streamlit as st

from lecture_feedback.application_state import ApplicationState
from lecture_feedback.thread_safe_dict import ThreadSafeDict


@st.cache_resource
def get_cleanup_throttle() -> ThreadSafeDict:
    """Store the last cleanup timestamp to throttle cleanup runs.

    Returns a dict with key 'last_cleanup_time' holding a float timestamp.
    """
    return ThreadSafeDict({"last_cleanup_time": 0.0})


def throttled_invocation(minimum_time_between_executions: float = 60.0) -> Callable:
    def decorator(function: Callable) -> Callable:
        @functools.wraps(function)
        def wrapper(*args: object, **kwargs: object) -> None:
            throttle = get_cleanup_throttle()
            now = time.time()

            if now - throttle["last_cleanup_time"] < minimum_time_between_executions:
                return

            throttle["last_cleanup_time"] = now

            function(*args, **kwargs)

        return wrapper

    return decorator


@throttled_invocation()
def remove_empty_rooms(application_state: ApplicationState) -> None:
    application_state.remove_empty_rooms()
