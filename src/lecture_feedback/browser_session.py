import uuid

import streamlit as st


class BrowserSession:
    def __init__(self) -> None:
        if "user_id" not in st.session_state:
            st.session_state.user_id = str(uuid.uuid4())


    def get_user_id(self) -> str:
        return st.session_state.user_id


    def get_session_id(self) -> str:
        if not self.is_in_session():
            return ""
        return st.session_state["joined_session_id"]

    def is_in_session(self) -> bool:
        return "joined_session_id" in st.session_state

    def join_session(self, session_id: str) -> None:
        if self.is_in_session():
            msg = "Cannot join a session while already in a session"
            raise RuntimeError(msg)
        st.session_state.joined_session_id = session_id

    def leave_session(self) -> None:
        if "joined_session_id" in st.session_state:
            del st.session_state.joined_session_id

