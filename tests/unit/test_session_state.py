from streamlit.testing.v1 import AppTest

from tests.bdd.fixture import run_wrapper
from tests.bdd.test_helper import get_room_id


def _resolved_session_id(app: AppTest) -> str:
    value = app.query_params["session_id"]
    resolved = value[0] if isinstance(value, list) else value
    return str(resolved)


def test_fresh_visitor_gets_a_session_id() -> None:
    app = AppTest.from_function(run_wrapper)
    app.run()

    assert _resolved_session_id(app)


def test_url_session_id_adopted_when_not_live() -> None:
    app = AppTest.from_function(run_wrapper)
    app.query_params["session_id"] = "stale-or-unknown-id"
    app.run()

    assert _resolved_session_id(app) == "stale-or-unknown-id"


def test_copy_pasted_live_session_forks_to_new_user() -> None:
    host = AppTest.from_function(run_wrapper)
    host.run()
    host.button(key="start_room").click().run()
    host_session_id = _resolved_session_id(host)
    room_id = get_room_id(host)

    visitor = AppTest.from_function(run_wrapper)
    visitor.query_params["room_id"] = room_id
    visitor.query_params["session_id"] = host_session_id
    visitor.run()

    assert _resolved_session_id(visitor) != host_session_id
