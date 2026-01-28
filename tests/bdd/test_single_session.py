from pytest_bdd import parsers, scenario, then, when
from streamlit.testing.v1 import AppTest

from tests.bdd.fixture import captured
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


# ============================================================================
# When Steps
# ============================================================================


@when("I enter a non-existing room ID")
def i_enter_nonexistent_room_id(context: dict[str, AppTest]) -> None:
    context["me"].text_input(key="join_room_id").set_value("9999").run()


@when('I click the "Join Room" button')
def i_click_join_room(context: dict[str, AppTest]) -> None:
    context["me"].button(key="join_room").click().run()


# ============================================================================
# Then Steps
# ============================================================================


@then("the room should have a valid room ID")
def room_should_have_valid_room_id(context: dict[str, AppTest]) -> None:
    room_id = get_room_id(context["me"])
    assert len(room_id) > 0


@then("the url should contain the room id")
def url_should_contain_room_id(context: dict[str, AppTest]) -> None:
    room_id = get_room_id(context["me"])
    assert len(context["me"].query_params["room_id"]) == 1
    assert context["me"].query_params["room_id"][0] == room_id


@then(parsers.parse('I should see error message "{error_message}"'))
def i_should_see_error_message(context: dict[str, AppTest], error_message: str) -> None:
    assert len(context["me"].error) == 1
    assert context["me"].error[0].value == error_message


@then(parsers.parse('I should see warning message "{warning_message}"'))
def i_should_see_warning_message(
    context: dict[str, AppTest],
    warning_message: str,
) -> None:
    assert len(context["me"].warning) == 1
    assert context["me"].warning[0].value == warning_message


@then(parsers.parse('my status should be "{status}"'))
def my_status_should_be(context: dict[str, AppTest], status: str) -> None:
    plotly_charts = context["me"].get("plotly_chart")
    assert len(plotly_charts) > 0, "No plotly chart found"

    room_id = get_room_id(context["me"])
    df = captured.room_data[room_id]
    assert captured.room_data[room_id] is not None, "No dataframe was captured"
    count = df[status].iloc[0]
    assert count >= 1, f"Expected at least 1 user with status '{status}', found {count}"
