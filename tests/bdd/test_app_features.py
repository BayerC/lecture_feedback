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


# ============================================================================
# Scenario Definitions
# ============================================================================


@scenario("features/app.feature", "Create a new Room")
def test_create_room() -> None:
    pass


@scenario("features/app.feature", "Try to join non existing room")
def test_join_nonexistent_room() -> None:
    pass


# ============================================================================
# Shared Steps (used across multiple scenarios)
# ============================================================================


@given("I am on the room selection screen")
@then("I should still be on the room selection screen")
def on_room_selection_screen(app: AppTest) -> None:
    assert len(app.title) == 1
    assert app.title[0].value == "Welcome to Lecture Feedback App"


# ============================================================================
# When Steps
# ============================================================================


@when('I click the "Create Room" button')
def click_create_room(app: AppTest) -> None:
    app.button(key="start_room").click().run()


@when("I enter a non-existing room ID")
def enter_nonexistent_room_id(app: AppTest) -> None:
    app.text_input(key="join_room_id").set_value("9999").run()


@when('I click the "Join Room" button')
def click_join_room(app: AppTest) -> None:
    app.button(key="join_room").click().run()


# ============================================================================
# Then Steps
# ============================================================================


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


@then('I should see an error message "Room ID not found"')
def see_room_not_found_error(app: AppTest) -> None:
    assert len(app.error) == 1
    assert app.error[0].value == "Room ID not found"
