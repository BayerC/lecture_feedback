from pytest_bdd import parsers, scenario, then, when
from streamlit.testing.v1 import AppTest

from lecture_feedback.user_status import UserStatus
from tests.bdd.fixture import run_wrapper
from tests.bdd.test_helper import check_page_contents

STATUS_MAP = {status.name.lower(): status.value for status in UserStatus}


@scenario("features/multiple_session.feature", "Two users in one room share statistics")
def test_two_users_share_statistics() -> None:
    pass


@scenario(
    "features/multiple_session.feature",
    "Three users in two separate rooms maintain independent statistics",
)
def test_three_users_in_two_separate_rooms_maintain_independent_statistics() -> None:
    pass


@when("a third user creates another room")
def third_user_creates_another_room(context: dict[str, AppTest]) -> None:
    context["third_user"] = AppTest.from_function(run_wrapper)
    context["third_user"].run()
    context["third_user"].button(key="start_room").click().run()


@then(parsers.parse('"{users}" should see statuses "{statuses}"'))
def users_should_see_statuses(
    context: dict[str, AppTest],
    users: str,
    statuses: str,
) -> None:
    user_keys = [u.strip() for u in users.split(",")]
    status_names = [s.strip() for s in statuses.split(",")]

    expected = tuple(STATUS_MAP[status.lower()] for status in status_names)
    forbidden = tuple(set(STATUS_MAP.values()) - set(expected))

    for user_key in user_keys:
        check_page_contents(
            context[user_key],
            expected=expected,
            forbidden=forbidden,
        )
