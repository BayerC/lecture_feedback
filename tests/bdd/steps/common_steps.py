from pytest_bdd import given, parsers, then, when
from streamlit.testing.v1 import AppTest

from tests.bdd.fixture import run_wrapper
from tests.bdd.test_helper import refresh_all_apps
from tests.test_app import get_room_id


@given("I am in an active room")
def in_active_room(context: dict[str, AppTest]) -> None:
    click_create_room(context)
    see_active_room_screen(context)


@when('I click the "Create Room" button')
def click_create_room(context: dict[str, AppTest]) -> None:
    context["user"].button(key="start_room").click().run()


@when("another user joins the room")
def another_user_joins_room(context: dict[str, AppTest]) -> None:
    context["other_user"] = AppTest.from_function(run_wrapper)
    context["other_user"].run()
    context["other_user"].text_input(key="join_room_id").set_value(
        get_room_id(context["user"]),
    ).run()
    context["other_user"].button(key="join_room").click().run()
    refresh_all_apps(context)


@when(parsers.parse('I click the status "{status}" button'))
def user_click_status_button(context: dict[str, AppTest], status: str) -> None:
    context["user"].button(key=status).click().run()
    refresh_all_apps(context)


@when(parsers.parse('other user clicks the status "{status}" button'))
def other_user_click_status_button(context: dict[str, AppTest], status: str) -> None:
    context["other_user"].button(key=status).click().run()
    refresh_all_apps(context)


@then("I should see the active room screen")
def see_active_room_screen(context: dict[str, AppTest]) -> None:
    assert len(context["user"].title) == 1
    assert context["user"].title[0].value == "Active Room"


@given("I am on the room selection screen")
@then("I should still be on the room selection screen")
def on_room_selection_screen(context: dict[str, AppTest]) -> None:
    assert len(context["user"].title) == 1
    assert context["user"].title[0].value == "Welcome to Lecture Feedback App"
