import time
import uuid
from collections.abc import Generator

import pytest

pytest_plugins = [
    "tests.bdd.fixture",
    "tests.bdd.steps.common_steps",
]


@pytest.fixture(autouse=True)
def fake_browser_session_id(monkeypatch: pytest.MonkeyPatch) -> None:
    """Bypass the browser-backed local storage component during tests.

    ``streamlit.testing.v1.AppTest`` cannot run the local storage frontend, so
    the real component would block forever. Each simulated session instead gets
    a fresh id, matching how distinct browsers behave in production.
    """
    monkeypatch.setattr(
        "open_cups.session_state.load_or_create_session_id",
        lambda: str(uuid.uuid4()),
    )


class MockTime:
    def __init__(self, initial_time: float | None = None) -> None:
        self._current_time = initial_time if initial_time is not None else time.time()

    def time(self) -> float:
        return self._current_time

    def advance(self, seconds: float) -> None:
        self._current_time += seconds

    @property
    def current_time(self) -> float:
        return self._current_time

    @current_time.setter
    def current_time(self, value: float) -> None:
        self._current_time = value


_active_mock_time: MockTime | None = None


@pytest.fixture
def mock_time(monkeypatch: pytest.MonkeyPatch) -> Generator:
    global _active_mock_time  # noqa: PLW0603
    mock_time_instance = MockTime()
    _active_mock_time = mock_time_instance
    monkeypatch.setattr("time.time", mock_time_instance.time)
    monkeypatch.setattr("open_cups.room.time.time", mock_time_instance.time)
    monkeypatch.setattr("open_cups.stats_tracker.time.time", mock_time_instance.time)
    yield mock_time_instance
    _active_mock_time = None


def get_active_mock_time() -> MockTime | None:
    return _active_mock_time
