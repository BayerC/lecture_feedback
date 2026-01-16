import pytest
from pytest_bdd import scenario, then, when
from streamlit.testing.v1 import AppTest

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


@then("both users should be visible in the user status report")
def both_users_should_be_visible_in_user_status_report(
    context: dict[str, AppTest],
) -> None:
    content = get_page_content(context["user"])
    assert "Total participants: 2" in content


@when("the second user closes their session")
def second_user_closes_session(context: dict[str, AppTest]) -> None:
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
    assert content.count("Session") == 1
