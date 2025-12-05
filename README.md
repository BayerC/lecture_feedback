# Lecture Feedback App

![CI](https://github.com/BayerC/lecture_feedback/actions/workflows/ci.yml/badge.svg)
[![codecov](https://codecov.io/gh/BayerC/lecture_feedback/branch/main/graph/badge.svg)](https://codecov.io/gh/BayerC/lecture_feedback)

The app (currently beta! All users globally share the same session) is available at <https://lecture-feedback.streamlit.app/>.

## Development

1. Install uv: https://docs.astral.sh/uv/getting-started/installation/
2. Install pre-commit: `uv run pre-commit install`
3. To run pre-commit manually run: `uv run pre-commit run --all-files`
4. To run app locally: `uv run streamlit run main.py`
