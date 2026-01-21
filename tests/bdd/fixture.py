import pandas as pd
import pytest
from streamlit.testing.v1 import AppTest

from lecture_feedback.app import RoomState, get_statistics_data_frame


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


captured = CapturedData()


@pytest.fixture(autouse=True)
def capture_stats(monkeypatch: pytest.MonkeyPatch) -> None:
    captured.room_data.clear()
    original_func = get_statistics_data_frame

    def capture_wrapper(room: RoomState) -> pd.DataFrame:
        df = original_func(room)
        captured.room_data[room.room_id] = df
        return df

    monkeypatch.setattr(
        "lecture_feedback.app.get_statistics_data_frame",
        capture_wrapper,
    )
