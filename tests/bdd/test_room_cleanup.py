import pytest
from pytest_bdd import scenario, then, when
from streamlit.testing.v1 import AppTest

from tests.bdd.fixture import run_wrapper
from tests.bdd.test_helper import get_page_content
from tests.test_app import get_room_id


@scenario("features/room_cleanup.feature", "User leaves room and is cleaned up")
def test_user_leaves_room_and_room_is_cleaned_up() -> None:
    pass


@when("another user joins the room")
def another_user_joins_room(context: dict[str, AppTest]) -> None:
    app2 = AppTest.from_function(run_wrapper)
    app2.run()
    app2.text_input(key="join_room_id").set_value(get_room_id(context["app"])).run()
    app2.button(key="join_room").click().run()
    context["app2"] = app2
    context["app"].run()


@then("both users should be visible in the user status report")
def both_users_should_be_visible_in_user_status_report(
    context: dict[str, AppTest],
) -> None:
    content = get_page_content(context["app"])
    assert content.count("Session") == 2


@when("the other user closes their session")
def other_user_closes_session(context: dict[str, AppTest]) -> None:
    del context["app2"]  # no more reference to the object, i.e., session finishes


@when("a given timeout has passed")
def timeout_has_passed(
    context: dict[str, AppTest],
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    pass
    # TODO(#39): implement this in production code and enable the test  # noqa: FIX002
    # monkeypatch.setattr("lecture_feedback.room.time.time", lambda: 1_000_000_000)  # noqa: E501, ERA001
    # context["app"].run()  # noqa: ERA001


@then("only I should be visible in the user status report")
def only_i_should_be_visible_in_user_status_report(context: dict[str, AppTest]) -> None:
    pass
    # TODO(#39): implement this in production code and enable the test  # noqa: FIX002
    # content = get_page_content(context["app"])  # noqa: ERA001
    # assert content.count("Session") == 1  # noqa: ERA001
