import pytest
from pytest_bdd import given, scenario, then, when
from streamlit.testing.v1 import AppTest

from lecture_feedback.application_state import ApplicationState
from tests.bdd.test_helper import get_page_content


@pytest.fixture(autouse=True)
def freeze_time_to_zero(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr("lecture_feedback.room.time.time", lambda: 0)


@scenario(
    "features/room_cleanup.feature",
    "Disconnected user is removed from user status after timeout",
)
def test_disconnected_user_is_removed_from_user_status_after_timeout() -> None:
    pass


@scenario(
    "features/room_cleanup.feature",
    "Empty rooms are removed after cleanup",
)
def test_empty_rooms_are_removed_after_cleanup() -> None:
    pass


@then("both users should be visible in the user status report")
def both_users_should_be_visible_in_user_status_report(
    context: dict[str, AppTest],
) -> None:
    content = get_page_content(context["user"])
    assert "Number of participants: 2" in content


@when("the second user leaves")
def second_user_leaves(context: dict[str, AppTest]) -> None:
    del context["second_user"]  # prevent running this user further


@when("a given timeout has passed")
def timeout_has_passed(
    context: dict[str, AppTest],
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    time_to_pass = 5
    step_time = 2
    # patch this in any case to be independent of the production value
    monkeypatch.setattr("lecture_feedback.app.USER_REMOVAL_TIMEOUT_SECONDS", 3)

    for current_time in range(0, time_to_pass, step_time):
        monkeypatch.setattr(
            "lecture_feedback.room.time.time",
            lambda current_time=current_time: current_time,
        )
        context["user"].run()


@then("only I should be visible in the user status report")
def only_i_should_be_visible_in_user_status_report(context: dict[str, AppTest]) -> None:
    content = get_page_content(context["user"])
    assert "Number of participants: 1" in content


@given("I create a room with one user")
def i_create_room_with_one_user(context: dict) -> None:
    context["app_state"] = ApplicationState()
    context["room_id"] = "test_room_1"
    context["session_id_1"] = "session_1"
    context["app_state"].create_room(context["room_id"], context["session_id_1"])


@when("the user leaves")
def user_leaves(context: dict, monkeypatch: pytest.MonkeyPatch) -> None:
    # Time travel to simulate sessions becoming inactive
    # Set time to be well past any timeout window
    current_time_value = 100.0

    def mock_time() -> float:
        return current_time_value

    monkeypatch.setattr("lecture_feedback.room.time.time", mock_time)

    room = context["app_state"].rooms[context["room_id"]]

    room.remove_inactive_sessions(50)

    sessions_after = list(room)
    assert len(sessions_after) == 0, (
        f"Expected 0 sessions after cleanup, got {len(sessions_after)}"
    )


@when("the room cleanup process runs")
def room_cleanup_runs(context: dict) -> None:
    app_state = context["app_state"]
    app_state.remove_empty_rooms()


@then("the room should no longer exist in the application state")
def room_should_no_longer_exist(context: dict) -> None:
    assert context["room_id"] not in context["app_state"].rooms
