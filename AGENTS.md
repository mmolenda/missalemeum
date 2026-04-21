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
