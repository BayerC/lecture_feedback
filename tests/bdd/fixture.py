import pytest
from streamlit.testing.v1 import AppTest





def run_wrapper() -> None:
    from lecture_feedback.app import run  # noqa: PLC0415

    run()


@pytest.fixture
def context() -> dict[str, AppTest]:
    application = AppTest.from_function(run_wrapper)
    application.run()
    return {"user": application}

