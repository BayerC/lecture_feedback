import uuid

import streamlit as st
import streamlit.components.v1 as components

COOKIE_NAME = "OPEN_CUPS_SESSION_ID"
COOKIE_MAX_AGE_SECONDS = 60 * 60 * 24 * 30  # 30 days


class SessionState:
    """Per-user session state wrapper.

    The session identity is persisted in a browser cookie so it survives
    Streamlit session loss (a websocket drop while a phone is locked, a page
    reload). The cookie is scoped to the browser and never travels in the URL,
    so sharing a room link cannot leak a user's identity.

    See https://github.com/streamlit/streamlit/issues/10041 for the technique.
    """

    def __init__(self) -> None:
        if "session_id" not in st.session_state:
            st.session_state.session_id = _load_or_create_session_id()

    @property
    def session_id(self) -> str:
        return str(st.session_state.session_id)


def _load_or_create_session_id() -> str:
    if existing := _read_session_cookie():
        return existing
    session_id = str(uuid.uuid4())
    _write_session_cookie(session_id)
    return session_id


def _read_session_cookie() -> str | None:  # pragma: no cover
    return st.context.cookies.get(COOKIE_NAME)


def _write_session_cookie(session_id: str) -> None:  # pragma: no cover
    # st.html() strips <script>, so the cookie must be set from a component
    # iframe (served same-origin, so document.cookie writes to the app domain).
    # ponytail: no Secure flag, keeps the cookie working on http localhost too;
    # the value is a non-sensitive random id. Upgrade path: add Secure once the
    # app is https-only.
    components.html(
        f'<script>document.cookie = "{COOKIE_NAME}={session_id}; '
        f'path=/; max-age={COOKIE_MAX_AGE_SECONDS}; SameSite=Lax";</script>',
        height=0,
    )
