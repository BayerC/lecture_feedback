import uuid

import streamlit as st


class SessionState:
    """Per-user session state wrapper.

    See https://docs.streamlit.io/develop/api-reference/caching-and-state/st.session_state
    for more details.
    """

    def __init__(self) -> None:
        if "session_id" not in st.session_state:
            st.session_state.session_id = st.context.cookies.get(
                "ajs_anonymous_id",
            ) or str(uuid.uuid4())

    @property
    def session_id(self) -> str:
        return str(st.session_state.session_id)
