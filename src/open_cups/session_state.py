import datetime
import uuid

import streamlit as st
from extra_streamlit_components import CookieManager

_SESSION_COOKIE_NAME = "open_cups_session_id"
_COOKIE_MAX_AGE = datetime.timedelta(days=1)


class SessionState:
    """Per-user session state wrapper.

    See https://docs.streamlit.io/develop/api-reference/caching-and-state/st.session_state
    for more details.
    """

    def __init__(self) -> None:
        if "session_id" not in st.session_state:
            st.session_state.session_id = self._resolve_session_id()

    @property
    def session_id(self) -> str:
        return str(st.session_state.session_id)

    @staticmethod
    def _resolve_session_id() -> str:  # pragma: no cover
        existing = st.context.cookies.get(_SESSION_COOKIE_NAME)
        if isinstance(existing, str) and existing:
            return existing
        new_id = str(uuid.uuid4())
        cookie_manager = CookieManager(key="open_cups_cookie_manager")
        cookie_manager.set(
            _SESSION_COOKIE_NAME,
            new_id,
            key="open_cups_cookie_set",
            expires_at=datetime.datetime.now(datetime.UTC) + _COOKIE_MAX_AGE,
            same_site="lax",
        )
        return new_id
