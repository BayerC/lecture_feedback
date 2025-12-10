## Lessons learned developing the app
- Threading and race condition handling is complex. Double-check code and use AI review to catch bugs.
- Ruff includes many checks. Verify if a check exists before adding new tools.
- Use AGENTS.md to guide LLM behavior. Modify it when responses need adjustment.
- GitHub won't let you turn on automerge per default for PRs, even with the merge queue
- Codecov is free for open source projects
- Streamlit has a [nice testing framework](https://docs.streamlit.io/develop/api-reference/app-testing)
- [There are special GitHub action triggers for fork-based workflows](https://github.com/amannn/action-semantic-pull-request?tab=readme-ov-file#event-triggers)
