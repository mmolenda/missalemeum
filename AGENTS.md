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

### Resolving Commune Inheritance

- When a Divinum Officium proper inherits from a numbered Commune Mass, use the mapping below to resolve the Mass number to the local Commune ID.
- The number is the Mass number used by Divinum Officium. The ID is the file ID under `backend/resources/divinum-officium-local/web/www/missa/<Language>/Commune`.
- If a proper inherits from, for example, `C3`, that means the local override must expose the same section set as Commune `C3`. It does not automatically mean every section must point to `@Commune/C3`, although that may be correct when the corresponding local Commune file itself references the upstream Commune with the same ID.
- Resolve each missing section individually. Prefer direct references to the actual text-bearing source section, following any reference chain when needed.

| Mass | Commune ID | Proper ID | Description |
| --- | --- | --- | --- |
| 8 | C4b | `commune:C4b:0:w` | Si Diligis - Communi unius aut plurium Summorum Pontificum; Msza o jednym lub kilku papieżach |
| 9 | C2 | `commune:C2:0:r` | Statuit - Commune Unius Martyris Pontificis; 1 Msza o Męczenniku Biskupie |
| 10 | C2-1 | `commune:C2-1:0:r` | Sacerdotes Dei - Commune Unius Martyris Pontificis; 2 Msza o Męczenniku Biskupie |
| 11 | C2a | `commune:C2a:0:r` | In virtute - Commune Unius Martyris; 1 Msza o Męczenniku |
| 12 | C2a-1 | `commune:C2a-1:0:r` | Laetabitur - Commune Unius Martyris; 2 Msza o Męczenniku |
| 13 | C3 | `commune:C3:0:r` | Intret - Commune Plurimorum Martyrum; 1 Msza o Wielu Męczennikach |
| 14 | C3a | `commune:C3a:0:r` | Sapientiam - Commune Plurimorum Martyrum; 2 Msza o Wielu Męczennikach |
| 15 | C3a-1 | `commune:C3a-1:0:r` | Salus autem - Commune Plurimorum Martyrum; 3 Msza o Wielu Męczennikach |
| 16 | C2p | `commune:C2p:0:r` | Protexisti - Commune Unius Martyris Tempore Paschali; Msza o jednym Męczenniku w Okresie Wielkanocnym |
| 17 | C3p | `commune:C3p:0:r` | Sancti Tui - Commune Plurimorum Martyrum Tempore Paschali; Msza o wielu Męczennikach w Okresie Wielkanocnym |
| 18 | C4 | `commune:C4:0:w` | Statuit - Commune Unius Confessoris Pontificis; 1 Msza o Wyznawcy Biskupie |
| 19 | C4-1 | `commune:C4-1:0:w` | Sacerdotes Tui - Commune Unius Confessoris Pontificis; 2 Msza o Wyznawcy Biskupie |
| 20 | C4a | `commune:C4a:0:w` | In Medio - Commune Doctoris non Pontificis; Msza o Doktorze Kościoła |
| 21 | C5 | `commune:C5:0:w` | Os iusti - Commune Confessoris non pontificis; 1 Msza o Wyznawcy |
| 22 | C5-1 | `commune:C5-1:0:w` | Iustus ut palma - Commune Confessoris non Pontificis; 2 Msza o Wyznawcy |
| 23 | C5b | `commune:C5b:0:w` | Os Iusti - Commune Abbatis; Msza o Opacie |
| 24 | C6 | `commune:C6:0:r` | Loquebar - Commune Virginis et Martyris; 1 Msza o Dziewicy Męczennicy |
| 25 | C6b | `commune:C6b:0:r` | Me exspectaverunt - Commune Virginis et Martyris; 2 Msza o Dziewicy Męczennicy |
| 26 | C6a | `commune:C6a:0:w` | Dilexisti - Commune Virginis non Martyris; 1 Msza o Dziewicy |
| 27 | C6a-1 | `commune:C6a-1:0:w` | Vultum tuum - Commune Virginis non Martyris; 2 Msza o Dziewicy |
| 28 | C6-1 | `commune:C6-1:0:r` | Me exspectaverunt - Commune Mulieris Martyris; Msza o Niewieście Męczennicy |
| 29 | C7a | `commune:C7a:0:w` | Cognovi - Commune Mulieris non Martyris; Msza o Niewieście |

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
