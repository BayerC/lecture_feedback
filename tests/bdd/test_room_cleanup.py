import pytest
from pytest_bdd import scenario, then, when
from streamlit.testing.v1 import AppTest

from tests.bdd.test_helper import get_page_content


@scenario(
    "features/room_cleanup.feature",
    "Disconnected user is removed from user status after timeout",
)
def test_user_leaves_room_and_room_is_cleaned_up() -> None:
    pass


@when("the second user closes their session")
def second_user_closes_session(context: dict[str, AppTest]) -> None:
    del context[
        "second_user"
    ]  # no more reference to the object, i.e., session finishes


@when("a given timeout has passed")
def timeout_has_passed(
    context: dict[str, AppTest],
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    pass
    # TODO(#39): implement this in production code and enable the test  # noqa: FIX002
    # monkeypatch.setattr("lecture_feedback.room.time.time", lambda: 1_000_000_000)  # noqa: E501, ERA001
    # context["user"].run()  # noqa: ERA001


@then("both users should be visible in the user status report")
def both_users_should_be_visible_in_user_status_report(
    context: dict[str, AppTest],
) -> None:
    content = get_page_content(context["user"])
    assert content.count("Session") == 2


@then("only I should be visible in the user status report")
def only_i_should_be_visible_in_user_status_report(context: dict[str, AppTest]) -> None:
    pass
    # TODO(#39): implement this in production code and enable the test  # noqa: FIX002
    # content = get_page_content(context["user"])  # noqa: ERA001
    # assert content.count("Session") == 1  # noqa: ERA001
