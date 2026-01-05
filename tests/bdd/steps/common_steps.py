from pytest_bdd import given, then, when
from streamlit.testing.v1 import AppTest


@when('I click the "Create Room" button')
def click_create_room(context: dict[str, AppTest]) -> None:
    context["app"].button(key="start_room").click().run()


@then("I should see the active room screen")
def see_active_room_screen(context: dict[str, AppTest]) -> None:
    assert len(context["app"].title) == 1
    assert context["app"].title[0].value == "Active Room"


@given("I am on the room selection screen")
@then("I should still be on the room selection screen")
def on_room_selection_screen(context: dict[str, AppTest]) -> None:
    assert len(context["app"].title) == 1
    assert context["app"].title[0].value == "Welcome to Lecture Feedback App"


@given("I am in an active room")
def in_active_room(context: dict[str, AppTest]) -> None:
    click_create_room(context)
    see_active_room_screen(context)
