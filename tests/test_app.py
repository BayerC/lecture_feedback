from streamlit.testing.v1 import AppTest

from lecture_feedback.user_stats_tracker import UserStatus


def run_wrapper() -> None:
    from lecture_feedback.app import run  # noqa: PLC0415

    run()


def test_app_initial_load() -> None:
    at = AppTest.from_function(run_wrapper)

    at.run()

    assert len(at.title) > 0
    assert "Lecture Feedback App" in at.title[0].value

    assert len(at.button) >= 3
    assert "user_id" in at.session_state

    red_button = next(btn for btn in at.button if UserStatus.RED.value in btn.label)
    red_button.click()

    at.run()

    yellow_button = next(
        btn for btn in at.button if UserStatus.YELLOW.value in btn.label
    )
    yellow_button.click()

    at.run()

    green_button = next(btn for btn in at.button if UserStatus.GREEN.value in btn.label)
    green_button.click()

    at.run()
