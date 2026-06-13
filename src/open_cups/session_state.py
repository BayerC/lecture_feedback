import uuid

import streamlit as st
from streamlit.components.v1 import html as components_html

COOKIE_NAME = "OPEN_CUPS_SESSION_ID"

class SessionState:
    """Per-user session state wrapper.

    See https://docs.streamlit.io/develop/api-reference/caching-and-state/st.session_state
    for more details.
    """

    def __init__(self, user_removal_timeout: int) -> None:
        if "session_id" not in st.session_state:
            session_id = st.context.cookies.get(COOKIE_NAME)
            if session_id is None:
                session_id = str(uuid.uuid4())
                components_html(
                    "<script>document.cookie = "
                    f'"{COOKIE_NAME}={session_id}; path=/; '
                    f'Max-Age={user_removal_timeout}; SameSite=Strict";'
                    "</script>",
                    height=0,
                )
            st.session_state.session_id = session_id

    @property
    def session_id(self) -> str:
        return str(st.session_state.session_id)
