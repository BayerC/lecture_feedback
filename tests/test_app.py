"""Tests for the Streamlit app using AppTest framework."""

from streamlit.testing.v1 import AppTest


def run_wrapper() -> None:
    from lecture_feedback.app import run  # noqa: PLC0415

    run()


def test_app_initial_load() -> None:
    at = AppTest.from_function(run_wrapper)

    at.run()  # <-- this is required

    assert len(at.title) > 0
    assert "Lecture Feedback App" in at.title[0].value

    assert len(at.button) >= 3
    assert "user_id" in at.session_state
