import pytest

from open_cups import session_state


def test_load_returns_existing_cookie(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(session_state, "_read_session_cookie", lambda: "existing-id")
    assert session_state._load_or_create_session_id() == "existing-id"  # noqa: SLF001


def test_load_mints_and_persists_when_cookie_absent(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    written: list[str] = []
    monkeypatch.setattr(session_state, "_read_session_cookie", lambda: None)
    monkeypatch.setattr(
        session_state,
        "_write_session_cookie",
        written.append,
    )

    session_id = session_state._load_or_create_session_id()  # noqa: SLF001

    assert session_id
    assert written == [session_id]
