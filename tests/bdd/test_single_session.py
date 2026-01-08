from pytest_bdd import parsers, scenario, then, when
from streamlit.testing.v1 import AppTest

from tests.bdd.test_helper import get_page_content

# ============================================================================
# Scenario Definitions
# ============================================================================


@scenario("features/single_session.feature", "Create a new Room")
def test_create_room() -> None:
    pass


@scenario(
    "features/single_session.feature",
    "Try to join room without entering Room ID",
)
def test_join_without_room_id() -> None:
    pass


@scenario("features/single_session.feature", "Try to join non existing room")
def test_join_nonexistent_room() -> None:
    pass


@scenario("features/single_session.feature", "User changes feedback status")
def test_user_changes_feedback_status() -> None:
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
    room_id = None
    for element in context["user"].markdown:
        if element.value.startswith("**Room ID:**"):
            room_id = element.value.split("`")[1]
            break
    assert room_id is not None
    assert len(room_id) > 0


@then(parsers.parse('I should see error message "{error_message}"'))
def see_room_not_found_error(context: dict[str, AppTest], error_message: str) -> None:
    assert len(context["user"].error) == 1
    assert context["user"].error[0].value == error_message


@then(parsers.parse('I should see warning message "{warning_message}"'))
def see_warning_message(context: dict[str, AppTest], warning_message: str) -> None:
    assert len(context["user"].warning) == 1
    assert context["user"].warning[0].value == warning_message


@then(parsers.parse('my status should be "{status}"'))
def verify_my_status(context: dict[str, AppTest], status: str) -> None:
    page_content = get_page_content(context["user"])
    assert status in page_content
