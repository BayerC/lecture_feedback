from streamlit.testing.v1 import AppTest


def get_page_content(app: AppTest) -> str:
    return "\n".join(element.value for element in app.markdown)
