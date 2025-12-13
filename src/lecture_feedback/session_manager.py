import uuid
from typing import cast

import streamlit as st


class SessionManager:
    """Handles st.session_state"""

    def __init__(self) -> None:
        if "user_id" not in st.session_state:
            st.session_state.user_id = str(uuid.uuid4())

    @property
    def user_id(self) -> str:
        return cast("str", st.session_state.user_id)

    @property
    def joined_session_id(self) -> str | None:
        return st.session_state.get("joined_session_id")

    @property
    def is_in_session(self) -> bool:
        return self.joined_session_id is not None

    def join_session_internal(self, session_id: str) -> None:
        """Do not call this method directly, use SessionsTracker.join_session()."""
        st.session_state.joined_session_id = session_id
