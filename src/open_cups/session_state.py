import uuid

import streamlit as st
import streamlit.components.v1 as components

_COOKIE_NAME = "open_cups_user_id"
_COOKIE_MAX_AGE_SECONDS = 60 * 60 * 24 * 365  # 1 year


class SessionState:
    """Per-user session state wrapper.

    The user identity is stored in a first-party browser cookie so it survives
    websocket reconnects (for example a phone locking its screen) while never
    leaking into the shareable URL. The cookie is written client-side because
    Streamlit can only read cookies (``st.context.cookies``), not set them.

    See https://docs.streamlit.io/develop/api-reference/caching-and-state/st.session_state
    for more details.
    """

    def __init__(self) -> None:
        if "session_id" not in st.session_state:
            st.session_state.session_id = self._load_or_create_session_id()

    @staticmethod
    def _load_or_create_session_id() -> str:
        if (existing := st.context.cookies.get(_COOKIE_NAME)):
            return existing
        session_id = str(uuid.uuid4())
        SessionState._write_cookie(session_id)
        return session_id

    @staticmethod
    def _write_cookie(session_id: str) -> None:
        # The html component renders in a same-origin iframe, so writing to
        # window.parent.document sets a first-party cookie that avoids the
        # third-party storage blocking that breaks iframe-local storage.
        components.html(
            f"""
            <script>
                window.parent.document.cookie =
                    "{_COOKIE_NAME}={session_id}; "
                    + "max-age={_COOKIE_MAX_AGE_SECONDS}; path=/; SameSite=Lax";
            </script>
            """,
            height=0,
        )

    @property
    def session_id(self) -> str:
        return str(st.session_state.session_id)
