import pytest
from pytest_bdd import given, scenario, then, when
from streamlit.testing.v1 import AppTest


def run_wrapper() -> None:
    from lecture_feedback.app import run  # noqa: PLC0415

    run()


@pytest.fixture
def app() -> AppTest:
    application = AppTest.from_function(run_wrapper)
    application.run()
    return application


@scenario("features/app.feature", "Create a new Room")
def test_create_room() -> None:
    pass


@given("I am on the room selection screen")
def on_room_selection_screen(app: AppTest) -> None:
    assert len(app.title) == 1
    assert app.title[0].value == "Welcome to Lecture Feedback App"


@when('I click the "Create Room" button')
def click_create_room(app: AppTest) -> None:
    app.button(key="start_room").click().run()


@then("I should see the active room screen")
def see_active_room_screen(app: AppTest) -> None:
    assert len(app.title) == 1
    assert app.title[0].value == "Active Room"


@then("the room should have a valid room ID")
def valid_room_id(app: AppTest) -> None:
    room_id = None
    for element in app.markdown:
        if element.value.startswith("**Room ID:**"):
            room_id = element.value.split("`")[1]
            break
    assert room_id is not None
    assert len(room_id) > 0
