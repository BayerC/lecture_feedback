from streamlit.testing.v1 import AppTest


def run_wrapper() -> None:
    from lecture_feedback.app import run  # noqa: PLC0415

    run()


def test_app_initial_load() -> None:
    app = AppTest.from_function(run_wrapper)
    app.run()
