import pytest
from pytest_bdd import given, parsers, scenario, then, when
from streamlit.testing.v1 import AppTest

STATUS_MAP = {
    "red": "🔴 Red",
    "green": "🟢 Green",
    "yellow": "🟡 Yellow",
    "unknown": "Unknown",
}


def run_wrapper() -> None:
    from lecture_feedback.app import run  # noqa: PLC0415

    run()


@pytest.fixture
def app() -> AppTest:
    application = AppTest.from_function(run_wrapper)
    application.run()
    return application


@pytest.fixture
def multiple_sessions_app() -> dict[int, AppTest]:
    return {}


# ============================================================================
# Scenario Definitions
# ============================================================================


@scenario("features/app.feature", "Create a new Room")
def test_create_room() -> None:
    pass


@scenario("features/app.feature", "Try to join room without entering Room ID")
def test_join_without_room_id() -> None:
    pass


@scenario("features/app.feature", "Try to join non existing room")
def test_join_nonexistent_room() -> None:
    pass


@scenario("features/app.feature", "User changes feedback status")
def test_user_changes_feedback_status() -> None:
    pass


@scenario("features/app.feature", "Two users in one room share statistics")
def test_two_users_share_statistics() -> None:
    pass


# ============================================================================
# Shared Steps (used across multiple scenarios)
# ============================================================================


@given("I am on the room selection screen")
@then("I should still be on the room selection screen")
def on_room_selection_screen(app: AppTest) -> None:
    assert len(app.title) == 1
    assert app.title[0].value == "Welcome to Lecture Feedback App"


@given("I am in an active room")
def in_active_room(app: AppTest) -> None:
    click_create_room(app)
    see_active_room_screen(app)


@given(parsers.parse("user {user_id:d} and user {other_user_id:d}"))
def user_and_other_user(
    multiple_sessions_app: dict[int, AppTest],
    user_id: int,
    other_user_id: int,
) -> None:
    multiple_sessions_app[user_id] = AppTest.from_function(run_wrapper)
    multiple_sessions_app[user_id].run()
    multiple_sessions_app[other_user_id] = AppTest.from_function(run_wrapper)
    multiple_sessions_app[other_user_id].run()


@given(parsers.parse("user {user_id:d} creates a room"))
def user_creates_room(
    multiple_sessions_app: dict[int, AppTest],
    user_id: int,
) -> None:
    multiple_sessions_app[user_id].button(key="start_room").click().run()


@given(parsers.parse("user {user_id:d} joins user {other_user_id:d}'s room"))
def user_joins_other_user_room(
    multiple_sessions_app: dict[int, AppTest],
    user_id: int,
    other_user_id: int,
) -> None:
    other_user_room_id = get_room_id(multiple_sessions_app[other_user_id])
    multiple_sessions_app[user_id].text_input(key="join_room_id").set_value(
        other_user_room_id,
    ).run()
    multiple_sessions_app[user_id].button(key="join_room").click().run()


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


@when(parsers.parse('I click the status "{status}" button'))
def click_status_button(app: AppTest, status: str) -> None:
    app.button(key=status).click().run()


@when(parsers.parse('user {user_id:d} changes status to "{status}"'))
def user_changes_status(
    multiple_sessions_app: dict[int, AppTest],
    user_id: int,
    status: str,
) -> None:
    multiple_sessions_app[user_id].button(key=status).click().run()
    for uid, app in multiple_sessions_app.items():
        if uid != user_id:
            app.run()


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


@then(parsers.parse('I should see error message "{error_message}"'))
def see_room_not_found_error(app: AppTest, error_message: str) -> None:
    assert len(app.error) == 1
    assert app.error[0].value == error_message


@then(parsers.parse('I should see warning message "{warning_message}"'))
def see_warning_message(app: AppTest, warning_message: str) -> None:
    assert len(app.warning) == 1
    assert app.warning[0].value == warning_message


@then(parsers.parse('my status should be "{status}"'))
def verify_my_status(app: AppTest, status: str) -> None:
    page_content = get_page_content(app)
    assert status in page_content


@then(
    parsers.parse("all users in the room should see one {status_1} and one {status_2}"),
)
def all_users_in_room_see_two_statuses(
    multiple_sessions_app: dict[int, AppTest],
    status_1: str,
    status_2: str,
) -> None:
    expected = (STATUS_MAP[status_1.lower()], STATUS_MAP[status_2.lower()])
    forbidden = tuple(set(STATUS_MAP.values()) - set(expected))

    for app in multiple_sessions_app.values():
        check_page_contents(
            app,
            expected=expected,
            forbidden=forbidden,
        )


# ============================================================================
# Helper Functions
# ============================================================================


def get_page_content(app: AppTest) -> str:
    return "\n".join(element.value for element in app.markdown)


def get_room_id(app: AppTest) -> str:
    room_id = None
    for element in app.markdown:
        if element.value.startswith("**Room ID:**"):
            room_id = element.value.split("`")[1]
            break
    assert room_id is not None
    return room_id


def check_page_contents(
    app: AppTest,
    expected: tuple[str, ...],
    forbidden: tuple[str, ...] = (),
) -> None:
    page_content = get_page_content(app)
    for string in expected:
        assert string in page_content
    for string in forbidden:
        assert string not in page_content
