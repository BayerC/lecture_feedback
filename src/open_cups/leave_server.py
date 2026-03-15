import threading
from http.server import BaseHTTPRequestHandler, HTTPServer

from open_cups.application_state import ApplicationState

_started = False


def start(application_state: ApplicationState, port: int = 8502) -> None:
    global _started
    if _started:
        return
    _started = True

    def handler_factory(*args):  # type: ignore[no-untyped-def]
        return _Handler(*args, app_state=application_state)

    thread = threading.Thread(
        target=lambda: HTTPServer(("", port), handler_factory).serve_forever(),
        daemon=True,
    )
    thread.start()


class _Handler(BaseHTTPRequestHandler):
    def __init__(self, *args, app_state: ApplicationState, **kwargs) -> None:  # type: ignore[no-untyped-def]
        self._app_state = app_state
        super().__init__(*args, **kwargs)

    def do_POST(self) -> None:
        length = int(self.headers.get("Content-Length", 0))
        session_id = self.rfile.read(length).decode().strip()
        room = self._app_state.get_session_room(session_id)
        if room:
            room.add_question("system", f"User {session_id[:8]}… left")
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()

    def log_message(self, *args: object) -> None:
        pass
