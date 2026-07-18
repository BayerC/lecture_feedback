import uuid

import streamlit as st

from open_cups.application_state import ApplicationState

# A live session refreshes its last_seen every autorefresh tick (~2s), so this
# threshold tolerates a couple of missed ticks before treating it as stale.
SESSION_LIVENESS_TIMEOUT_SECONDS = 10


class SessionState:
    """Per-user session state wrapper.

    The session id is kept in the URL so it survives a websocket drop (a phone
    locking, a page reload). To stop a copy-pasted link from cloning identity,
    a session id from the URL is only adopted when that session is currently
    stale (a genuine reconnect); if it is still live, the visitor is treated as
    a new user. See https://github.com/BayerC/open_cups/issues/165.
    """

    def __init__(self, application_state: ApplicationState) -> None:
        if "session_id" not in st.session_state:
            st.session_state.session_id = _resolve_session_id(application_state)
        st.query_params["session_id"] = st.session_state.session_id

    @property
    def session_id(self) -> str:
        return str(st.session_state.session_id)


def _resolve_session_id(application_state: ApplicationState) -> str:
    url_session_id = st.query_params.get("session_id")
    if url_session_id is None:
        return str(uuid.uuid4())
    if application_state.is_session_live(
        url_session_id,
        SESSION_LIVENESS_TIMEOUT_SECONDS,
    ):
        return str(uuid.uuid4())
    return url_session_id
