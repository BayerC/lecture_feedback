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


def get_page_content(app: AppTest) -> str:
    return "\n".join(element.value for element in app.markdown)


def test_click_buttons_in_new_room() -> None:
    app = AppTest.from_function(run_wrapper)
    app.run()

    app.button(key="start_room").click().run()

    for status in (
        UserStatus.RED,
        UserStatus.YELLOW,
        UserStatus.GREEN,
    ):
        app.button(key=status.value).click().run()
        assert status.value in get_page_content(app)


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


def test_two_sessions_track_user_stats_in_same_room() -> None:
    app1 = AppTest.from_function(run_wrapper)
    app1.run()
    app1.button(key="start_room").click().run()

    app2 = AppTest.from_function(run_wrapper)
    app2.run()
    app2.text_input(key="join_room_id").set_value(get_room_id(app1)).run()
    app2.button(key="join_room").click().run()

    app1.button(key=UserStatus.RED.value).click().run()
    check_page_contents(app1, expected=(UserStatus.RED.value, UserStatus.UNKNOWN.value))

    app2.run()
    check_page_contents(app2, expected=(UserStatus.RED.value, UserStatus.UNKNOWN.value))

    app2.button(key=UserStatus.GREEN.value).click().run()
    app1.run()

    check_page_contents(
        app1,
        expected=(UserStatus.RED.value, UserStatus.GREEN.value),
        forbidden=(UserStatus.UNKNOWN.value,),
    )
    check_page_contents(
        app2,
        expected=(UserStatus.RED.value, UserStatus.GREEN.value),
        forbidden=(UserStatus.UNKNOWN.value,),
    )


def test_three_sessions_in_two_rooms() -> None:
    app1 = AppTest.from_function(run_wrapper)
    app1.run()
    app1.button(key="start_room").click().run()

    app2 = AppTest.from_function(run_wrapper)
    app2.run()
    app2.text_input(key="join_room_id").set_value(get_room_id(app1)).run()
    app2.button(key="join_room").click().run()

    app3 = AppTest.from_function(run_wrapper)
    app3.run()
    app3.button(key="start_room").click().run()

    app1.button(key=UserStatus.YELLOW.value).click().run()
    app2.button(key=UserStatus.GREEN.value).click().run()
    app1.run()
    check_page_contents(
        app1,
        expected=(UserStatus.YELLOW.value, UserStatus.GREEN.value),
        forbidden=(UserStatus.UNKNOWN.value, UserStatus.RED.value),
    )

    app2.run()
    check_page_contents(
        app2,
        expected=(UserStatus.YELLOW.value, UserStatus.GREEN.value),
        forbidden=(UserStatus.UNKNOWN.value, UserStatus.RED.value),
    )

    app3.run()
    check_page_contents(
        app3,
        expected=(UserStatus.UNKNOWN.value,),
        forbidden=(
            UserStatus.GREEN.value,
            UserStatus.YELLOW.value,
            UserStatus.RED.value,
        ),
    )
