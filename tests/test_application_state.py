from lecture_feedback.application_state import ApplicationState


def test_room_removal_on_empty() -> None:
    app_state = ApplicationState()
    room_id = "temporary_room"
    app_state.create_room(room_id, "temp_session")
    app_state.create_room("persistent_room", "persistent_session")

    assert room_id in app_state.rooms

    room = app_state.rooms[room_id]
    # such session deletion needs to be implemented in production code
    del room._sessions["temp_session"]  # noqa: SLF001

    app_state.remove_empty_rooms()

    assert room_id not in app_state.rooms
    assert "persistent_room" in app_state.rooms
