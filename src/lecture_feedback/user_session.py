import uuid

import streamlit as st


class UserSession:
    """User session manager for a single user (per browser tab)"""

    def __init__(self) -> None:
        if "user_id" not in st.session_state:
            st.session_state.user_id = str(uuid.uuid4())


    def get_user_id(self) -> str:
        return st.session_state.user_id


    def get_session_id(self) -> str | None:
        return st.session_state.get("joined_session_id")

    def is_in_session(self) -> bool:
        return "joined_session_id" in st.session_state

    def join_session_internal(self, session_id: str) -> None:
        """Do not call this method directly, use SessionsTracker.join_session()."""
        st.session_state.joined_session_id = session_id
