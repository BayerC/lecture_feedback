## Code
- Use modern python 3.13
- Use modern python style and techniques
- High quality code
- We use `uv` to manage python versions and dependencies. For example, use `uv run pytest` to run tests

## Coding Guideline
- Don't use abbreviations that are not widely known as such. Prefer to spell out words in variable and function names

## Git Guideline

- Use atomic commits: One commit equals one purpose.
- Use meaningful commit message
- Branch naming: Use `feat/` prefix for feature branches, `refactor/` prefix for refactoring branches, `docs/` prefix for documentation changes, `fix/` prefix for bug fixes, and `test/` prefix for test additions or modifications

## Documentation
- Whenever mentioning repository-local files in markdown, link to them using a local link (using `[text](path/to/file)`)
- Do not add docstrings that merely restate what is obvious from the name
  - BAD: `@property user_id` with `"""Get the unique user ID for this browser tab."""` - "user_id" already says it's a user ID
  - BAD: `def get_data()` with `"""Gets data"""`
  - BAD: `@property is_in_session` with `"""Check if this browser tab has joined a session."""` - name already indicates it's a check
  - GOOD: Add docstrings only when they provide non-obvious information (parameters, side effects, exceptions, business logic)

## Code review
- Absolute Mode
- Eliminate emojis, filler, hype, transitions, appendixes.
- Use blunt, directive phrasing; no mirroring, no softening.
- Suppress sentiment-boosting, engagement, or satisfaction metrics.
- No questions, offers, suggestions, or motivational content.
- Deliver info only; end immediately after.
- Do not include details about what is already correct or working. Focus only on what needs attention
- List all errors, issues and opportunities for improvements you find as enumeration.
