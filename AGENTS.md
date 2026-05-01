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
- `backend/resources/divinum-officium-local` is authoritative over the base Divinum Officium tree for local proper loading.
- If a proper is missing in `divinum-officium-local`, treat it as absent in local overrides. Do not change parser logic to fall back to the base tree for local lookups; add or update the needed file in `divinum-officium-local` instead.

## Divinum Officium Local Overrides

- Keep `backend/resources/divinum-officium-local` authoritative.
- When fixing a missing proper that should exist in local behavior, create or update the corresponding file under `divinum-officium-local` rather than relaxing lookup rules.
- When creating new files in `backend/resources/divinum-officium-local`, prefer references to existing Divinum Officium sections instead of copying literal text.
- Follow the existing local override style: keep local files as thin as possible and reference upstream sections wherever possible.
- Latin local files act as the blueprint for vernacular local files during parsing.
- If a section in a vernacular local file would be identical to the Latin local version, omit it from the vernacular file.
- In vernacular local files, keep only sections that differ from Latin or are language-specific, such as `Comment`.
- Some referenced sections in the target Divinum Officium proper may themselves only contain another reference.
- In that case, follow the chain until you reach the file and section containing the actual text, and make the local file reference that final text-bearing source rather than an intermediate redirect when possible.
- If a target Divinum Officium proper has `vide C5-1` or `ex C5-1` in `[Rank]`, or `vide C5-1` in `[Rule]`, treat that as meaning that any sections not defined in that proper come from `@Commune/C5-1`.
- When creating the local override file for such a proper, add explicit references for those inherited sections to the matching `@Commune/...` source, and keep direct references to the proper itself only for sections actually defined in that proper.
- Example:
  - if `Sancti/04-02.txt` has `vide C5-1` and defines `[Oratio]` but not `[Introitus]` or `[Lectio]`
  - then the local file should reference `[Introitus] -> @Commune/C5-1`, `[Oratio] -> @Sancti/04-02:Oratio`, `[Lectio] -> @Commune/C5-1`

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

Get calendar for a given year:

```
./.venv/bin/python3 backend/api/cli.py calendar 2026 --language en
```