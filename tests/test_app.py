from streamlit.testing.v1 import AppTest


def run_wrapper() -> None:
    """
    Launches the Lecture Feedback application by invoking its top-level run entrypoint.
    """
    from lecture_feedback.app import run  # noqa: PLC0415

    run()


def is_on_room_selection_screen(app: AppTest) -> bool:
    """
    Determine whether the app is currently displaying the room selection screen.
    
    Returns:
        True if the app's single title equals "Welcome to Lecture Feedback App", False otherwise.
    """
    return (
        len(app.title) == 1 and app.title[0].value == "Welcome to Lecture Feedback App"
    )


def is_on_active_room_screen(app: AppTest) -> bool:
    """
    Detects whether the app is displaying the Active Room screen.
    
    Parameters:
        app (AppTest): The test app instance to inspect.
    
    Returns:
        bool: `true` if there is exactly one title element and its value is "Active Room", `false` otherwise.
    """
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