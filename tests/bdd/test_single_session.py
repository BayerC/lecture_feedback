import pandas as pd

import pytest
from pytest_bdd import parsers, scenario, then, when
from streamlit.testing.v1 import AppTest

from lecture_feedback.app import get_statistics_data_frame
from tests.bdd.test_helper import get_room_id

# ============================================================================
# Scenario Definitions
# ============================================================================


@scenario("features/single_session.feature", "Create a new room")
def test_create_room() -> None:
    pass


@scenario(
    "features/single_session.feature",
    "Try to join room without entering Room ID",
)
def test_join_without_room_id() -> None:
    pass


@scenario("features/single_session.feature", "Try to join non existing room")
def test_join_non_existent_room() -> None:
    pass


@scenario("features/single_session.feature", "User changes feedback status")
def test_user_changes_feedback_status(capture_statistics) -> None:
    pass


# ============================================================================
# When Steps
# ============================================================================


@when("I enter a non-existing room ID")
def enter_nonexistent_room_id(context: dict[str, AppTest]) -> None:
    context["user"].text_input(key="join_room_id").set_value("9999").run()


@when('I click the "Join Room" button')
def click_join_room(context: dict[str, AppTest]) -> None:
    context["user"].button(key="join_room").click().run()


# ============================================================================
# Then Steps
# ============================================================================


@then("the room should have a valid room ID")
def valid_room_id(context: dict[str, AppTest]) -> None:
    room_id = get_room_id(context["user"])
    assert len(room_id) > 0


@then(parsers.parse('I should see error message "{error_message}"'))
def see_room_not_found_error(context: dict[str, AppTest], error_message: str) -> None:
    assert len(context["user"].error) == 1
    assert context["user"].error[0].value == error_message


@then(parsers.parse('I should see warning message "{warning_message}"'))
def see_warning_message(context: dict[str, AppTest], warning_message: str) -> None:
    assert len(context["user"].warning) == 1
    assert context["user"].warning[0].value == warning_message



@pytest.fixture()
def capture_statistics(monkeypatch):
    capture_statistics.dataframe = None
    
    original_func = get_statistics_data_frame
    
    def capture_wrapper(room) -> pd.DataFrame:
        df = original_func(room)
        capture_statistics.dataframe = df
        return df
    
    monkeypatch.setattr(
        "lecture_feedback.app.get_statistics_data_frame", 
        capture_wrapper
    )
capture_statistics.dataframe = None


@then(parsers.parse('my status should be "{status}"'))
def verify_my_status( context: dict[str, AppTest], status: str) -> None:
    plotly_charts = context["user"].get("plotly_chart")
    assert len(plotly_charts) > 0, "No plotly chart found"

    assert capture_statistics.dataframe is not None, "No dataframe was captured"
    count = capture_statistics.dataframe[status].iloc[0]
    assert count >= 1, f"Expected at least 1 user with status '{status}', found {count}"
