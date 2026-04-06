import streamlit as st


class SessionState:
    """Per-user session state wrapper.

    See https://docs.streamlit.io/develop/api-reference/caching-and-state/st.session_state
    for more details.
    """

    def __init__(self) -> None:
        if "session_id" not in st.session_state:
            st.session_state.session_id = st.context.cookies["ajs_anonymous_id"]

    @property
    def session_id(self) -> str:
        return str(st.session_state.session_id)
