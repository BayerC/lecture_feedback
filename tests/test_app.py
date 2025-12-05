from streamlit.testing.v1 import AppTest

from lecture_feedback.user_stats_tracker import UserStatus


def run_wrapper() -> None:
    from lecture_feedback.app import run  # noqa: PLC0415

    run()


def test_app_initial_load() -> None:
    app = AppTest.from_function(run_wrapper)
    app.run()

    assert len(app.title) > 0
    assert "Lecture Feedback App" in app.title[0].value

    assert len(app.button) >= 3
    assert "user_id" in app.session_state

    red_button = next(btn for btn in app.button if UserStatus.RED.value in btn.label)
    red_button.click()
    app.run()

    yellow_button = next(
        btn for btn in app.button if UserStatus.YELLOW.value in btn.label
    )
    yellow_button.click()
    app.run()

    green_button = next(
        btn for btn in app.button if UserStatus.GREEN.value in btn.label
    )
    green_button.click()
    app.run()
