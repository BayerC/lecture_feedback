from pytest_bdd import parsers, scenario, then, when
from streamlit.testing.v1 import AppTest

from lecture_feedback.user_status import UserStatus
from tests.bdd.fixture import captured, run_wrapper
from tests.bdd.test_helper import get_room_id

STATUS_MAP = {status.name.lower(): status.value for status in UserStatus}


@scenario("features/multiple_session.feature", "Two users in one room share statistics")
def test_two_users_share_statistics() -> None:
    pass


# @scenario(
#    "features/multiple_session.feature",
#    "Three users in two separate rooms maintain independent statistics",
# )
# def test_three_users_in_two_separate_rooms_maintain_independent_statistics() -> None:
#    pass


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
    status_names = [s.strip() for s in statuses.split(",")]
    user_keys = [u.strip() for u in users.split(",")]

    for user in user_keys:
        room_id = get_room_id(context[user])
        df = captured.room_data[room_id]
        for status in UserStatus:
            status_value = status.value
            expected_count = sum(1 for s in status_names if s == status.value)

            actual_count = df[status_value].iloc[0]
            assert actual_count == expected_count
