from streamlit.testing.v1 import AppTest


def refresh_all_apps(context: dict[str, AppTest]) -> None:
    for app in context.values():
        app.run()


def get_page_content(app: AppTest) -> str:
    return "\n".join(element.value for element in app.markdown)


def check_page_contents(
    app: AppTest,
    expected: tuple[str, ...],
    forbidden: tuple[str, ...] = (),
) -> None:
    page_content = get_page_content(app)
    for string in expected:
        assert string in page_content
    for string in forbidden:
        assert string not in page_content
