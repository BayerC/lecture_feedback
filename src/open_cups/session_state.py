import uuid

import streamlit as st
from streamlit_local_storage import LocalStorage

SESSION_ID_STORAGE_KEY = "session_id"


class SessionState:
    """Per-user session state wrapper.

    The session identity is persisted in the browser's local storage so it
    survives Streamlit session loss (websocket drops while a phone is locked,
    page reloads). Local storage is scoped to the browser and never travels in
    the URL, so sharing the room link cannot leak a user's identity.

    See https://docs.streamlit.io/develop/api-reference/caching-and-state/st.session_state
    for more details.
    """

    def __init__(self) -> None:
        if SESSION_ID_STORAGE_KEY not in st.session_state:
            st.session_state.session_id = load_or_create_session_id()

    @property
    def session_id(self) -> str:
        return str(st.session_state.session_id)


def load_or_create_session_id() -> str:
    """Return the browser's persisted session id, creating one if absent.

    This is the single seam touching the browser-backed component, which lets
    tests patch it without driving a real frontend.
    """
    local_storage = LocalStorage()
    existing = local_storage.getItem(SESSION_ID_STORAGE_KEY)
    if existing:
        return str(existing)

    new_session_id = str(uuid.uuid4())
    local_storage.setItem(SESSION_ID_STORAGE_KEY, new_session_id)
    return new_session_id
