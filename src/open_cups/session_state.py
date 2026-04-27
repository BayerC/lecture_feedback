import uuid

import streamlit as st
from streamlit.components.v1 import html as components_html

COOKIE_NAME = "OPEN_CUPS_SESSION_ID"


class SessionState:
    """Per-user session state wrapper.

    Uses a browser cookie to persist the session ID across page refreshes and
    reconnects. This avoids leaking the session ID into the URL, which would
    cause copy-pasted links to share the same identity.

    See https://github.com/streamlit/streamlit/issues/10041 for the cookie
    technique and https://github.com/BayerC/open_cups/issues/165 for context.
    """

    def __init__(self) -> None:
        if "session_id" not in st.session_state:
            session_id = st.context.cookies.get(COOKIE_NAME)
            if session_id is None:
                session_id = str(uuid.uuid4())
                components_html(
                    "<script>document.cookie = "
                    f'"{COOKIE_NAME}={session_id}; path=/; SameSite=Strict";'
                    "</script>",
                    height=0,
                )
            st.session_state.session_id = session_id

    @property
    def session_id(self) -> str:
        return str(st.session_state.session_id)
