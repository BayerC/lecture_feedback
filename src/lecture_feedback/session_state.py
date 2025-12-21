import uuid

import streamlit as st


class SessionState:
    """Per-user session state wrapper.

    See https://docs.streamlit.io/develop/api-reference/caching-and-state/st.session_state
    for more details.
    """

    def __init__(self) -> None:
        """
        Ensure a per-user session identifier exists in Streamlit's session state.
        
        If `session_id` is not already present in `st.session_state`, generate a new UUID and store it as a string under the key `session_id`.
        """
        if "session_id" not in st.session_state:
            st.session_state.session_id = str(uuid.uuid4())

    @property
    def session_id(self) -> str:
        """
        Retrieve the current per-user session identifier.
        
        Returns:
            session_id (str): The session identifier stored in Streamlit's session state.
        """
        return str(st.session_state.session_id)