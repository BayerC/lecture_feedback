from streamlit.testing.v1 import AppTest

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


def get_page_content(app: AppTest) -> str:
    return "\n".join(element.value for element in app.markdown)


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


def get_room_id(app: AppTest) -> str:
    room_id = None
    for element in app.markdown:
        if element.value.startswith("**Room ID:**"):
            room_id = element.value.split("`")[1]
            break
    assert room_id is not None
    return room_id


def test_three_sessions_in_two_rooms() -> None:
    app_1 = AppTest.from_function(run_wrapper)
    app_1.run()
    app_1.button(key="start_room").click().run()

    app_2 = AppTest.from_function(run_wrapper)
    app_2.run()
    app_2.text_input(key="join_room_id").set_value(get_room_id(app_1)).run()
    app_2.button(key="join_room").click().run()

    app_3 = AppTest.from_function(run_wrapper)
    app_3.run()
    app_3.button(key="start_room").click().run()

    app_1.button(key=UserStatus.YELLOW.value).click().run()
    app_2.button(key=UserStatus.GREEN.value).click().run()
    app_1.run()
    check_page_contents(
        app_1,
        expected=(UserStatus.YELLOW.value, UserStatus.GREEN.value),
        forbidden=(UserStatus.UNKNOWN.value, UserStatus.RED.value),
    )

    app_2.run()
    check_page_contents(
        app_2,
        expected=(UserStatus.YELLOW.value, UserStatus.GREEN.value),
        forbidden=(UserStatus.UNKNOWN.value, UserStatus.RED.value),
    )

    app_3.run()
    check_page_contents(
        app_3,
        expected=(UserStatus.UNKNOWN.value,),
        forbidden=(
            UserStatus.GREEN.value,
            UserStatus.YELLOW.value,
            UserStatus.RED.value,
        ),
    )
