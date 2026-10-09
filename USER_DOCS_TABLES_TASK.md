# Task: align the SWAT+ user-documentation input tables with the SWAT+ `dev` branch

You are updating the input-file tables in a checkout of
`tugraskan/SWATPlus-user-documentation` (GitBook source) so they match what the
Fortran readers on the SWAT+ `dev` branch actually read. Work on a branch of the
docs fork, never on `main`.

## 0. Who does what

| Role | Source | Job |
|---|---|---|
| **swatref** (this repository, the SWAT corpus tool) | the locked `dev` commit | Finds **where** the docs and the source disagree: builds the dev input schema and the user-docs report |
| **Tamandua** (`swatplus-source` MCP) | the same `dev` checkout | Answers **what the code does**: who calls a reader, what it reads, a type's fields with units, every assignment to a variable |
| **dataselector** (`swat-dataset` MCP) | the same `dev` checkout | Answers **what a column means** and **what real input files contain** |
| **ANT models** (`local-agent-router` MCP) | facts you hand them | **Cross-check and review** your conclusions. They never supply facts. |
| **You** | all of the above | Decide, edit, and verify |

Facts come only from swatref, Tamandua, dataselector, or the Fortran itself.
A model's answer is a second opinion to compare against those facts, never a
source. Your own model (Laguna-S) must not approve its own output: every
accepted change goes through `review_code` (section 4).

## 1. Setup

Run from the root of this repository with its virtual environment
(`.venv/Scripts/swatref.exe` on Windows, or activate `.venv` first). Running
the full test suite also needs `jsonschema`: `pip install -e ".[dev]"`.

Do not run this while another agent is modifying the same checkout. ANT's
operating rules forbid two coding agents in one Git worktree.

### 1a. The dev source and its schema (swatref)

```sh
swatref source add dev                       # new [sources.dev] profile locked to today's dev tip; note the commit it prints
swatref source fetch dev                     # checkout: external/swatplus-dev
swatref schema --source dev --version dev build
```

The schema is written to `schema_artifacts/releases/swatplus-dev.json`. Its
provenance sidecar records the exact commit. Every other tool below must
describe **this same commit**.

### 1b. Tamandua on the dev checkout

Tamandua's bundled facts are pinned to an older release, so build a facts file
from the dev checkout. It is already installed for the system Python
(`swatplus-build` and `swatplus-mcp` are on PATH); in another environment,
`pip install -e C:/Users/taci.ugraskan/source/repos/Tamandua` first. From the
root of this repository (`--corpus .` supplies its parser):

```sh
swatplus-build --source external/swatplus-dev --corpus . --facts external/swatplus-dev/swatplus-facts.json
```

This was tested on the 62.0.1 checkout: about 25 s, and it records the commit
it indexed. Its answers matched a manual check of the same questions.

Add the server to Hermes (`mcp_servers` in `~/.hermes/config.yaml`, stdio form;
adapt to your Hermes version's syntax), then restart Hermes:

```yaml
mcp_servers:
  swatplus-source:
    command: swatplus-mcp
    args: ["--facts", "<this repo>/external/swatplus-dev/swatplus-facts.json", "--compact"]
```

Check: Tamandua's `provenance` tool must report the dev commit from step 1a.

### 1c. dataselector on the dev checkout

The Claude Code configuration points dataselector at a different local copy
(`SWATPLUS_REPOS/swatplus_DEV`). For this task, give Hermes its own entry with
`--source` set to the dev checkout:

```yaml
  swat-dataset:
    command: node
    args: ["C:/Users/taci.ugraskan/source/repos/swatplus-dataselector/dist/mcp-server.js",
           "--source", "<this repo>/external/swatplus-dev"]
```

Keep the `--exe` argument from the existing configuration if the server
refuses to start without it. The example datasets that ship with the source
(`external/swatplus-dev/refdata/Ames_sub1`, `.../Osu_1hru`) can be selected
with `select_dataset`. `Ames_sub1` is newer; both can be older than the
readers.

### 1d. The docs checkout and the report

```sh
git -C external/SWATPlus-user-documentation fetch origin
git -C external/SWATPlus-user-documentation switch -c hermes/input-tables-dev origin/main
swatref schema --source dev --version dev user-docs-report --docs-root external/SWATPlus-user-documentation
```

The output is `schema_artifacts/reports/swatplus-dev-user-docs-report.md` and
`.json`. The report never writes to the docs checkout. On Windows the docs
clone needs `core.longpaths` (already set in this clone).

## 2. Reading the report, and its limits

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
- **Names.** Field names match on the Fortran variable, the Editor column, or an
  example-file header. The example files can be older than the readers.

## 3. Verify each `differs` table with the tools

Use the tools, not text search. Fall back to reading the Fortran only when a
tool cannot answer, and say so in your notes.

1. **Does the reader run?** Use Tamandua `callers` or `call_path` on the
   reader named in the schema entry. If nothing calls it, leave the table alone
   and record it for the developers.
2. **What does it read?** Tamandua `file_io` on the file name gives the routine,
   unit and line. Then read that `read` statement. Check:
   - `if` branches around it, since some columns are conditional on a switch in
     another file;
   - the number of header lines before data;
   - ID-placed records (`read i; backspace; read k, x(i)`).
3. **The columns, in order.** For a whole-type read, Tamandua `describe_type`
   gives every component with units and meaning.
4. **Is a value overwritten after it is read?** Tamandua `writers` lists every
   assignment to a field. An unconditional assignment after the read means the
   input has no effect; say so on the field page.
5. **Meaning, units, defaults.** Use dataselector `lookup_docs` (file and
   column) as evidence, and cross-check it against `describe_type`.
6. **Real files.** Select an example dataset and compare its header row with
   the reader. dataselector `check_inputs` counts values per line against the
   read statement: it catches missing or extra columns, not swapped ones.
7. **Types.**
   - Real documented as integer is harmless but inaccurate; fix it anyway.
   - **Integer documented as real is harmful**: an integer read of `110.0`
     fails. Fix the type, and drop decimals from its default and range.
8. **Column names.** The docs use file-header names. Prefer, in order:
   - a column name stated in a source comment;
   - the Editor name;
   - a real header at the same position;
   - otherwise the Fortran name, flagged in your notes as inferred.

Write the result for each table down as a short **facts packet**: the docs
rows, the read statement, the type fields with units, callers, writers, and the
header evidence, each with file:line. Section 4 uses it.

## 4. Use the ANT models (`local-agent-router`)

Run `gpu_pool_status` first. Use only **loaded** models: an unloaded one can
take minutes to start, and clients give up after about 100 s. At the time this
was written, `oss20` (gpt-oss-20b, 65,536-token window) and `nemo` (Mistral-Nemo
12B, 16,384 tokens, an independent model lineage) were loaded.

For **every `differs` table**:

1. **Independent derivation, with `delegate_gpu_model`.** Call it with
   `model: "oss20"`, `json_mode: true`, and the facts packet. Ask it to derive
   the correct ordered column list, with the type for each column and the
   evidence line, and **not** to see your proposed edit. Compare its list with
   yours. Where they disagree, go back to the tools (section 3) and settle it
   from the facts, not by majority. If `oss20` and you still disagree, ask
   `delegate_gpu_model` with `model: "nemo"`. It does not share gpt-oss's
   lineage.
2. **Field-page text, with `delegate_gpu_model`.** For new or replaced field
   pages, call it with `model: "oss20"` and only the facts packet. Ask for one
   description line and a short body, using **only** facts in the packet.
   Delete every sentence you cannot trace to a packet line.
3. **Mandatory review, with `review_code`.** Before you accept a table's edit,
   send `review_code`:
   - `content_to_review`: the table's diff;
   - `context`: the facts packet.

   Accept only an approval. On `REQUEST_CHANGES`, fix and re-review, or record
   why the reviewer is wrong, citing the facts. Use `delegate_quick_task`
   (Gemma 4) as a second reviewer only when the evidence is ambiguous.

Guardrails:

- Keep packets compact: under ~12k tokens for `nemo`, ~40k for `oss20`.
- Never paste the API key or whole files of unrelated code.
- Hermes stops a run after repeated tool failures (5 identical, 8 on the same
  tool). If a delegate call fails twice, do not retry it a third time: carry on
  without it, and mark that table "not cross-checked" in your findings.
- A `truncated: true` reply means the output budget ran out. Raise
  `max_tokens` once, or split the request; do not treat it as an answer.

## 5. Editing rules

- Preserve each page's format: pipe tables or single-line GitBook HTML, `\_`
  escaping, and the existing columns.
- A shared table covers several files. Edit `'object'.con`
  (`connectivity/hru.con/README.md`) **once** for all connect files.
- **Every new row gets a field page.** Create `<file folder>/<field>.md` with
  front matter (`description:`), a `# heading` with escaped underscores, and a
  short body traceable to the facts packet. Link it from the table, and
  register it in `io-docs/SUMMARY.md` in table order, nested under the file's
  README entry.
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

## 6. Verify before committing

- Re-run the comparison against the edited checkout. Every table you edited
  should be `match` or `names_to_check`, with no broken links. (Re-running the
  CLI rewrites the report under `schema_artifacts/reports/`; restore it
  afterwards if it should keep describing docs `main`.)
- Every `SUMMARY.md` target exists, every new page is registered, and nothing
  references a deleted page.
- Send the complete `git diff` to `review_code` once more, with the list of
  tables changed as context.

## 7. Deliver

- Commits on `hermes/input-tables-dev` in the docs checkout. Do not push or
  open a pull request unless asked.
- A findings list in four parts:
  - per table: what changed and the evidence (file:line);
  - the delegate calls made, with model, verdict, and any disagreement and how
    the facts settled it; mark tables "not cross-checked" where a call failed;
  - items for the SWAT+ developers: dead readers, inputs overwritten after
    being read, and files whose real columns disagree with the reader;
  - names you inferred.

After you finish (not before), you can compare your result with an earlier pass
against release 62.0.1 on branch `fix/input-tables-62.0.1` of the docs fork.
