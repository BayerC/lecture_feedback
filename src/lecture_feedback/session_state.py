import uuid
from typing import cast

import streamlit as st

from lecture_feedback.user_stats_tracker import UserStatus


class SessionState:
    """Per-user session state wrapper.

    See https://docs.streamlit.io/develop/api-reference/caching-and-state/st.session_state
    for more details.
    """

    def __init__(self) -> None:
        if "session_id" not in st.session_state:
            st.session_state.session_id = str(uuid.uuid4())
        self.user_status = UserStatus.UNKNOWN

    @property
    def session_id(self) -> str:
        return cast("str", st.session_state.session_id)



# Userstate should be stored in the session state
# User doesnt care about the room id, they just want to join a room and see the feedback
