from pytest_bdd import parsers, scenario, then
from streamlit.testing.v1 import AppTest

from lecture_feedback.user_status import UserStatus
from tests.bdd.test_helper import check_page_contents

STATUS_MAP = {status.name.lower(): status.value for status in UserStatus}


@scenario("features/multi_session.feature", "Two users in one room share statistics")
def test_two_users_share_statistics() -> None:
    pass


@then(
    parsers.parse("all users in the room should see one {status_1} and one {status_2}"),
)
def all_users_in_room_see_two_statuses(
    context: dict[str, AppTest],
    status_1: str,
    status_2: str,
) -> None:
    expected = (STATUS_MAP[status_1.lower()], STATUS_MAP[status_2.lower()])
    forbidden = tuple(set(STATUS_MAP.values()) - set(expected))

    for app in context.values():
        check_page_contents(
            app,
            expected=expected,
            forbidden=forbidden,
        )
