# AGENTS.md

## Tests

- In this repo, do not assume `python` or `pytest` are available globally.
- Use the local virtual environment from the repo root: `./.venv/bin/python3`.
- Run tests from the repository root.

## Verified Commands

- Run the whole selected test file:

```sh
./.venv/bin/python3 -m pytest backend/tests/test_propers.py
```

- Run only preface-related tests:

```sh
./.venv/bin/python3 -m pytest backend/tests/test_propers.py -k preface
```

- Run a narrower subset by test name fragment:

```sh
./.venv/bin/python3 -m pytest backend/tests/test_propers.py -k "correct_preface_calculated_by_date"
```

## Notes

- `pytest` correctly picks up `backend/pytest.ini` when invoked from the repo root.
- If `pytest ...` or `python ...` fails, do not keep guessing; fall back to the command pattern above.

## Fixture Drift After Divinum Officium Updates

- For changes coming from the Divinum Officium submodule update branch `chore/update-divinum-officium-submodule`, most test failures are caused by fixtures no longer matching updated source texts.
- This is only the majority case, not a rule. Every failure must be judged individually before changing fixtures.
- Typical pattern:
  - A proper, reading, or similar text differs only in wording, punctuation, accents, or other source-text details.
  - The generated output matches the updated Divinum Officium source, but the stored fixture still reflects the old text.
- How to handle it:
  - Run the failing test with a narrow `-k` filter.
  - Inspect the failure diff and identify the exact context.
  - Compare the actual generated text with the current source text and, when useful, with CLI output such as `./.venv/bin/python3 backend/api/cli.py date 2025-02-03 --language en`.
  - If the code output is correct and the source text changed upstream, update the relevant fixture.
  - If the output indicates a logic bug, wrong proper selection, broken formatting, or another behavioral regression, fix the code instead of the fixture.

## CLI

Get texts for a given calendar day:

```
./.venv/bin/python3 backend/api/cli.py date 2025-02-03 --language en
```
