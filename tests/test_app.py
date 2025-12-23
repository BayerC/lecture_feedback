from streamlit.testing.v1 import AppTest

from lecture_feedback.app import get_application_state
from lecture_feedback.user_status import UserStatus


def run_wrapper() -> None:
    from lecture_feedback.app import run  # noqa: PLC0415

    run()


def is_on_room_selection_screen(app: AppTest) -> bool:
    return (
        len(app.title) == 1 and app.title[0].value == "Welcome to Lecture Feedback App"
    )


def is_on_active_room_screen(app: AppTest) -> bool:
    return len(app.title) == 1 and app.title[0].value == "Active Room"


def test_app_initial_load() -> None:
    app = AppTest.from_function(run_wrapper)
    app.run()

    assert is_on_room_selection_screen(app)

    app.button(key="join_room").click().run()
    assert is_on_room_selection_screen(app)

    app.text_input(key="join_room_id").set_value("1337").run()
    app.button(key="join_room").click().run()
    assert len(app.error) == 1
    assert app.error[0].value == "Room ID not found"
    assert is_on_room_selection_screen(app)

    app.button(key="start_room").click().run()
    assert is_on_active_room_screen(app)


def test_join_existing_room() -> None:
    app_state = get_application_state()
    room_id = "test_room_123"
    app_state.create_room(room_id, "host_session")

    app = AppTest.from_function(run_wrapper)
    app.run()

    app.text_input(key="join_room_id").set_value(room_id).run()
    app.button(key="join_room").click().run()

    assert is_on_active_room_screen(app)


def test_click_buttons_in_new_room() -> None:
    app = AppTest.from_function(run_wrapper)
    app.run()

    app.button(key="start_room").click().run()
    assert is_on_active_room_screen(app)

    app.button(key=UserStatus.RED.value).click().run()
    app.button(key=UserStatus.YELLOW.value).click().run()
    app.button(key=UserStatus.GREEN.value).click().run()
    app.button(key=UserStatus.UNKNOWN.value).click().run()
