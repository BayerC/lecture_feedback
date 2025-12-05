"""Tests for the Streamlit app using AppTest framework."""

from streamlit.testing.v1 import AppTest


def test_app_initial_load() -> None:
    at = AppTest.from_file("src/lecture_feedback/app.py")
    at.run()

    assert not at.exception

    # Check that main title is present
    assert len(at.title) > 0
    assert "Lecture Feedback App" in at.title[0].value

    # Check that buttons are present
    assert len(at.button) >= 3

    # Check that user_id is set in session state
    assert "user_id" in at.session_state
