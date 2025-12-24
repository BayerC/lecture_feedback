from streamlit import cache_resource

from lecture_feedback.application_state import ApplicationState, Room
from lecture_feedback.session_state import SessionState
from lecture_feedback.user_status import UserStatus


@cache_resource
def get_application_state() -> ApplicationState:
    return ApplicationState()


class App:
    def __init__(self) -> None:
        self.application_state = get_application_state()
        session_state = SessionState()
        self.session_id = session_state.session_id

    def get_active_room(self) -> Room | None:
        return self.application_state.get_session_room(self.session_id)

    def create_room(self, room_id: str) -> None:
        self.application_state.create_room(room_id, self.session_id)

    def join_room(self, room_id: str) -> None:
        self.application_state.join_room(room_id, self.session_id)

    def set_session_status(self, status: UserStatus) -> None:
        if (room := self.get_active_room()) is not None:
            room.set_session_status(self.session_id, status)
        else:
            msg = "No active room for this session"
            raise ValueError(msg)
