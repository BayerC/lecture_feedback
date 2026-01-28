from pytest_bdd import parsers, scenario, then, when
from streamlit.testing.v1 import AppTest

from tests.bdd.fixture import run_wrapper
from tests.bdd.test_helper import get_page_content, get_room_id, refresh_all_apps

# ============================================================================
# Scenario Definitions
# ============================================================================


@scenario("features/question_voting.feature", "Client submits a question")
def test_client_submits_question() -> None:
    pass


@scenario("features/question_voting.feature", "Client upvotes a question")
def test_client_upvotes_question() -> None:
    pass


@scenario("features/question_voting.feature", "Client cannot upvote twice")
def test_client_cannot_upvote_twice() -> None:
    pass


@scenario("features/question_voting.feature", "Questions sorted by vote count")
def test_questions_sorted_by_votes() -> None:
    pass


@scenario("features/question_voting.feature", "Host closes a question")
def test_host_closes_question() -> None:
    pass


@scenario(
    "features/question_voting.feature",
    "Multiple questions with different vote counts",
)
def test_multiple_questions_ordering() -> None:
    pass


# ============================================================================
# When Steps
# ============================================================================


@when(parsers.parse('the second user submits a question "{question}"'))
def second_user_submits_question(context: dict[str, AppTest], question: str) -> None:
    context["second_user"].text_input(key="question_input").set_value(question).run()
    context["second_user"].button(key="send_question").click().run()
    refresh_all_apps(context)


@when(parsers.parse('the third user upvotes the question "{question}"'))
def third_user_upvotes_question(context: dict[str, AppTest], question: str) -> None:
    _upvote_question(context["third_user"], question, context)


@when(parsers.parse('the second user upvotes the question "{question}"'))
def second_user_upvotes_question(context: dict[str, AppTest], question: str) -> None:
    _upvote_question(context["second_user"], question, context)


@when("a third user joins the room")
def third_user_joins_room(context: dict[str, AppTest]) -> None:
    context["third_user"] = AppTest.from_function(run_wrapper)
    context["third_user"].run()
    context["third_user"].text_input(key="join_room_id").set_value(
        get_room_id(context["user"]),
    ).run()
    context["third_user"].button(key="join_room").click().run()
    refresh_all_apps(context)


@when(parsers.parse('I close the question "{question}"'))
def host_closes_question(context: dict[str, AppTest], question: str) -> None:
    refresh_all_apps(context)
    question_id = _get_question_id_by_text(context["user"], question)
    context["user"].button(key=f"close_{question_id}").click().run()
    refresh_all_apps(context)


# ============================================================================
# Then Steps
# ============================================================================


@then(parsers.parse('"{users}" should see question "{question}"'))
def users_see_question(context: dict[str, AppTest], users: str, question: str) -> None:
    user_list = [user.strip() for user in users.split(",")]
    for user in user_list:
        page_content = get_page_content(context[user])
        assert question in page_content, f"{user} should see question: {question}"


@then(
    parsers.parse('"{users}" should see question "{question}" with {votes:d} vote'),
    converters={"votes": int},
)
def users_see_question_with_votes(
    context: dict[str, AppTest],
    users: str,
    question: str,
    votes: int,
) -> None:
    user_list = [user.strip() for user in users.split(",")]
    for user in user_list:
        page_content = get_page_content(context[user])
        assert question in page_content, f"{user} should see question: {question}"
        assert f"👍 {votes}" in page_content, (
            f"{user} should see {votes} vote(s) for question"
        )


@then(parsers.parse('"{users}" should not see question "{question}"'))
def users_do_not_see_question(
    context: dict[str, AppTest],
    users: str,
    question: str,
) -> None:
    user_list = [user.strip() for user in users.split(",")]
    for user in user_list:
        page_content = get_page_content(context[user])
        assert question not in page_content, (
            f"{user} should not see question: {question}"
        )


@then(parsers.parse('the first question should be "{question}"'))
def first_question_is(context: dict[str, AppTest], question: str) -> None:
    questions = _get_all_questions(context["user"])
    assert len(questions) > 0, "No questions found"
    assert questions[0] == question, (
        f"First question should be '{question}', but was '{questions[0]}'"
    )


@then(parsers.parse('questions should be ordered "{order}"'))
def questions_ordered(context: dict[str, AppTest], order: str) -> None:
    expected_order = [q.strip() for q in order.split(",")]
    questions = _get_all_questions(context["user"])
    assert questions == expected_order, (
        f"Questions should be ordered {expected_order}, but were {questions}"
    )


# ============================================================================
# Helper Functions
# ============================================================================


def _upvote_question(app: AppTest, question: str, context: dict[str, AppTest]) -> None:
    refresh_all_apps(context)
    question_id = _get_question_id_by_text(app, question)
    app.button(key=f"upvote_{question_id}").click().run()
    refresh_all_apps(context)


def _get_question_id_by_text(app: AppTest, question_text: str) -> str:
    markdown_elements = list(app.markdown)
    buttons = list(app.button)

    question_button_pairs = []
    for button in buttons:
        if button.key and (
            button.key.startswith("upvote_") or button.key.startswith("close_")
        ):
            if button.key.startswith("upvote_"):
                question_id = button.key.replace("upvote_", "")
            else:
                question_id = button.key.replace("close_", "")
            question_button_pairs.append(question_id)

    questions_found = []
    for element in markdown_elements:
        if (
            element.value
            and not element.value.startswith("**")
            and not element.value.startswith("👍")
            and element.value
            not in ["How well can you follow the lecture?", "Your question"]
        ):
            questions_found.append(element.value)

    if question_text in questions_found and question_button_pairs:
        question_index = questions_found.index(question_text)
        if question_index < len(question_button_pairs):
            return question_button_pairs[question_index]

    msg = f"Question '{question_text}' not found. Questions: {questions_found}, IDs: {question_button_pairs}"
    raise AssertionError(msg)


def _get_all_questions(app: AppTest) -> list[str]:
    markdown_elements = app.markdown
    questions = []
    skip_texts = {
        "How well can you follow the lecture?",
        "Your question",
    }
    for element in markdown_elements:
        value = element.value
        if (
            value
            and not value.startswith("**")
            and not value.startswith("👍")
            and value not in skip_texts
        ):
            questions.append(value)
    return questions
