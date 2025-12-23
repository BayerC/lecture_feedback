from streamlit.testing.v1 import AppTest

from lecture_feedback.user_status import UserStatus


def test_room_and_application_state_basic() -> None:
    from lecture_feedback.room import Room

    # Room basic operations
    room = Room("room-1")
    assert room.room_id == "room-1"

    room.set_session_status("s1", UserStatus.GREEN)
    assert room.get_session_status("s1") is UserStatus.GREEN


def test_session_state_initializes_in_streamlit_context() -> None:
    def run_wrapper() -> None:
        import streamlit as st

        from lecture_feedback.session_state import SessionState

        # constructing SessionState will ensure a session_id exists
        ss = SessionState()
        # expose the id via streamlit write so AppTest can inspect it
        st.write(ss.session_id)

    app = AppTest.from_function(run_wrapper)
    app.run()

    # One write call with a session id should exist
    assert len(app.markdown) == 1
    assert isinstance(app.markdown[0].value, str)
