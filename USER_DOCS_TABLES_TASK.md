# Task: align the SWAT+ user-documentation input tables with the SWAT+ `dev` branch

You are updating the input-file tables in a checkout of
`tugraskan/SWATPlus-user-documentation` (GitBook source) so they match what the
Fortran readers on the SWAT+ `dev` branch actually read. Work on a branch of the
docs fork, never on `main`.

The deterministic tooling lives in this repository
(`swatplus-reference-corpus`). It tells you **where** the docs and the source
disagree. It does not tell you **what is correct**: that needs reading the
Fortran. Treat every flag as a lead to verify, not an instruction.

## Ground rules

- The Fortran source on the locked `dev` commit is the authority for which
  columns a file has, their order, and their types.
- Never invent units, defaults, ranges, or descriptions. Take them from source
  declarations, comments, and usage; leave a cell empty when the source says
  nothing.
- Do not edit a table because a flag says so. Verify the flag in the reader
  first, and record the evidence (file and line) for every change.
- Keep a list of things that look like model bugs or dead code. Report them; do
  not "fix" the docs to match dead code.

## 1. Setup (tools)

Run from the root of this repository with its virtual environment
(`.venv/Scripts/swatref.exe` on Windows, or activate `.venv` first). Running
the full test suite also needs `jsonschema`: `pip install -e ".[dev]"`.

```sh
swatref source add dev                       # new [sources.dev] profile locked to today's dev tip; note the commit it prints
swatref source fetch dev
swatref schema --source dev --version dev build
```

The schema is written to `schema_artifacts/releases/swatplus-dev.json`, with a
provenance sidecar that records the exact commit.

Prepare the docs checkout (`external/SWATPlus-user-documentation`; on Windows it
needs `core.longpaths`, which this clone already has):

```sh
git -C external/SWATPlus-user-documentation fetch origin
git -C external/SWATPlus-user-documentation switch -c hermes/input-tables-dev origin/main
```

Then run the report:

```sh
swatref schema --source dev --version dev user-docs-report --docs-root external/SWATPlus-user-documentation
```

The output is `schema_artifacts/reports/swatplus-dev-user-docs-report.md` and
`.json`. The report never writes to the docs checkout.

## 2. Reading the report, and its limits

Statuses per input file:

| Status | Meaning |
|---|---|
| `match` | The table lists the source's fields, in order, with compatible types |
| `differs` | Missing, extra, reordered, or retyped fields; **this is your work list** |
| `names_to_check` | Only a field name differs and could not be confirmed. Often fine; leave unless two sources agree on a different name |
| `no_field_table` | A page exists but has no `Field` table |
| `named_only` | The docs name the file (usually in the `file.cio` list) but no page describes it |
| `no_page` | Not mentioned anywhere in the docs |
| `not_compared` | Multi-record, multi-section, runtime-sized, or decision-table layout; only page coverage is checked |

Known limits. Check for each of these before acting on a flag:

- **Dead readers.** The schema counts any file that has a reader, even if
  nothing ever calls that reader.
- **Multi-line files.** Some are modelled by their first line only, which makes
  later-line fields look "extra".
- **Shared tables.** These are detected only when a section page lists the files
  in a table and links to exactly one Field table, as `connectivity/README.md`
  does for every `*.con` file via `'object'.con`.
- **Names.** Field names match on the Fortran variable, the Editor column from
  the 62.0.0 field map, or an example file header. The example files in the
  source checkout's `refdata/` can be older than the readers.
  `refdata/Ames_sub1` is newer than `refdata/Osu_1hru`.

## 3. Verify each `differs` table (judgment)

For every table with status `differs`:

1. **Find the read.** The schema entry gives `reader` and `reader_line`. Read
   the actual `read` statement, not just the schema.
2. **Confirm the reader runs.** Search for `call <reader>`. Appearing in an
   `external ::` list does not count as a call. If the reader is never called,
   leave the table alone and record it for the developers.
3. **Read the layout.** If the statement reads a whole derived type
   (`read (u,*) x(i)`), the type's components, in order, are the columns.
   Check:
   - `if` branches around the read, since some columns are conditional on a
     switch in another file;
   - the number of header lines before data (some 62.x files have two);
   - ID-placed records (`read i; backspace; read k, x(i)`).
4. **Types.**
   - Real documented as integer is harmless but inaccurate; fix it anyway.
   - **Integer documented as real is harmful**: an integer read of `110.0`
     fails. Fix the type, and drop decimals from its default and range.
   - A string documented as an integer hides what the field does.
5. **Added vs replaced.** When a docs row and a source field are both
   unmatched at the same position, decide whether the field was renamed,
   replaced, or added. Use the type definition, older versions of the
   reader, and example headers.
6. **Meaning.** Search for the field's uses (`%field`) to write the
   description. Look for values that are **overwritten after they are read**,
   and for fields that are read but never used. Say so on the field page.
7. **Column names.** The docs use file-header names, not Fortran names.
   Prefer, in order:
   - a column name stated in a source comment;
   - the Editor name from the field map;
   - a `refdata/` header at the same position;
   - otherwise the Fortran name, flagged in your notes as inferred.

## 4. Editing rules

- Preserve each page's format: pipe tables or single-line GitBook HTML, `\_`
  escaping, and the existing columns.
- A shared table covers several files. Edit `'object'.con`
  (`connectivity/hru.con/README.md`) **once** for all connect files.
- **Every new row gets a field page.** Create `<file folder>/<field>.md` with
  front matter (`description:`), a `# heading` with escaped underscores, and a
  short source-grounded body. Link it from the table, and register it in
  `io-docs/SUMMARY.md` in table order, nested under the file's README entry.
- **For a replaced field,** `git mv` the old page to the new name, rewrite it,
  update its `SUMMARY.md` entry, and search for any other references to the old
  page.
- Do not rename a page just to fix a spelling. GitBook URLs follow file paths.
- `SUMMARY.md` has CRLF line endings in the working tree (`core.autocrlf`).
  Match them when you do string replacements.
- Leave alone:
  - tables whose reader is never called;
  - report false positives;
  - `names_to_check` rows, unless the Editor name and a real header agree.

## 5. Verify before committing

- Re-run the comparison against the edited checkout. Every table you edited
  should be `match` or `names_to_check`, with no broken links. (Re-running the
  CLI rewrites the report under `schema_artifacts/reports/`; restore it
  afterwards if it should keep describing docs `main`.)
- Every `SUMMARY.md` target exists, every new page is registered, and nothing
  references a deleted page.
- Review the whole `git diff`.

## 6. Deliver

- Commits on `hermes/input-tables-dev` in the docs checkout. Do not push or
  open a pull request unless asked.
- A findings list in three parts:
  - per table: what changed and the evidence (file:line);
  - items for the SWAT+ developers: dead readers, inputs overwritten after
    being read, and files whose real columns disagree with the reader;
  - names you inferred.

After you finish (not before), you can compare your result with an earlier pass
against release 62.0.1 on branch `fix/input-tables-62.0.1` of the docs fork.
