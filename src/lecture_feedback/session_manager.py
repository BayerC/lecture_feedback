import uuid
from typing import cast

import streamlit as st


class SessionManager:
    """Handles st.session_state.

    See https://docs.streamlit.io/develop/api-reference/caching-and-state/st.session_state
    for more details.
    """

    def __init__(self) -> None:
        if "user_id" not in st.session_state:
            st.session_state.user_id = str(uuid.uuid4())

    @property
    def user_id(self) -> str:
        return cast("str", st.session_state.user_id)

    @property
    def joined_room_id(self) -> str | None:
        return st.session_state.get("joined_room_id")

    @property
    def is_in_room(self) -> bool:
        return self.joined_room_id is not None

    def join_room_internal(self, room_id: str) -> None:
        """Do not call this method directly, use RoomManager.join_room()."""
        st.session_state.joined_room_id = room_id
