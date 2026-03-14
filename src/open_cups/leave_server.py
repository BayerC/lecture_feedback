import logging
import socket
import threading
from http.server import BaseHTTPRequestHandler, HTTPServer
from typing import ClassVar

from open_cups.application_state import ApplicationState

logger = logging.getLogger(__name__)

LEAVE_SERVER_PORT = 8502

_server_lock = threading.Lock()
_server_started = False


class LeaveHandler(BaseHTTPRequestHandler):
    application_state: ClassVar[ApplicationState | None] = None

    def do_POST(self) -> None:
        content_length = int(self.headers.get("Content-Length", 0))
        session_id = self.rfile.read(content_length).decode().strip()

        if session_id and self.application_state:
            logger.info("Removing session %s (tab closed)", session_id)
            self.application_state.disconnect_session(session_id)

        self.send_response(204)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()

    def log_message(self, format: str, *args: object) -> None:  # noqa: A002
        logger.debug(format, *args)


class DualStackHTTPServer(HTTPServer):
    """HTTPServer that accepts both IPv4 and IPv6 connections."""

    address_family = socket.AF_INET6

    def server_bind(self) -> None:
        self.socket.setsockopt(socket.IPPROTO_IPV6, socket.IPV6_V6ONLY, 0)
        super().server_bind()


def start_leave_server(
    application_state: ApplicationState,
    port: int = LEAVE_SERVER_PORT,
) -> None:
    global _server_started  # noqa: PLW0603

    with _server_lock:
        LeaveHandler.application_state = application_state

        if _server_started:
            return

        try:
            server = DualStackHTTPServer(("::", port), LeaveHandler)
        except OSError:
            logger.warning("Leave server port %d already in use", port)
            _server_started = True
            return

        thread = threading.Thread(target=server.serve_forever, daemon=True)
        thread.start()
        _server_started = True
        logger.info("Leave server started on port %d", port)
