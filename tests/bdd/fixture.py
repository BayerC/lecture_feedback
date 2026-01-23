from typing import TYPE_CHECKING

import pandas as pd
import pytest
from streamlit.testing.v1 import AppTest

from lecture_feedback.app import RoomState, get_statistics_data_frame

if TYPE_CHECKING:
    from lecture_feedback.application_state import ApplicationState


def run_wrapper() -> None:
    from lecture_feedback.app import run  # noqa: PLC0415

    run()


@pytest.fixture
def context() -> dict[str, AppTest]:
    application = AppTest.from_function(run_wrapper)
    application.run()
    return {"user": application}


class CapturedData:
    def __init__(self) -> None:
        self.room_data: dict[str, pd.DataFrame] = {}
        self.application_state: None | ApplicationState = None


captured = CapturedData()


@pytest.fixture(autouse=True)
def capture_stats(monkeypatch: pytest.MonkeyPatch) -> None:
    captured.room_data.clear()
    captured.application_state = None
    original_func = get_statistics_data_frame

    def capture_wrapper(room: RoomState) -> pd.DataFrame:
        df = original_func(room)
        captured.room_data[room.room_id] = df
        return df

    monkeypatch.setattr(
        "lecture_feedback.app.get_statistics_data_frame",
        capture_wrapper,
    )


@pytest.fixture(autouse=True)
def capture_application_state(monkeypatch: pytest.MonkeyPatch) -> None:
    from lecture_feedback.state_provider import Context  # noqa: PLC0415

    original_init = Context.__init__

    def wrapped_init(context: Context) -> None:
        original_init(context)
        captured.application_state = context.application_state

    monkeypatch.setattr(Context, "__init__", wrapped_init)
