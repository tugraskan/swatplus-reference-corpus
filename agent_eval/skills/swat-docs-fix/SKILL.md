---
name: swat-docs-fix
description: "Propose fixes for one SWAT+ user-docs input table: tool-applied layout fixes, then wording/unit fixes drafted from code evidence (Tamandua 0.5.0) for a person to approve. Never writes wording into the docs."
version: 1.0.0
author: swatplus-reference-corpus
metadata:
  hermes:
    tags: [SWAT+, documentation, input-files, review]
---

# Propose fixes for one SWAT+ user-docs input table

You fix ONE input table, `FILE`, in two parts: the tool applies layout fixes, and you draft wording/unit
fixes from evidence in the SWAT+ code for a person to approve. You do not write the wording into the docs,
and you do not commit.

**FILE is the table named in the request**: for `/swat-docs-fix Fix <name>.` (the request may also say
`FILE = <name>`), FILE is `<name>`. Start your first reply with `FILE = <name>`, and put exactly that name
wherever a command or path below says FILE. Never switch to another table, not even one that a tool's output
or an earlier run mentions.

## Where things are

Run every command with the **terminal** tool. Never use the browser, `browser_exec`, or any browser tool, and
never ask the user to enable Chrome remote debugging: nothing in this task needs a browser.

Begin **every** terminal command with this `cd` (bash, exactly):

    cd /c/Users/taci.ugraskan/source/repos/swatplus-reference-corpus-main/swatplus-reference-corpus-main &&

All paths below are relative to that folder.

- Docs to fix: `external/SWATPlus-user-documentation-hermes` (a separate git worktree; your branch starts with
  `hermes/`). Never touch `external/SWATPlus-user-documentation` (someone else's work in progress).
- SWAT+ 62.0.1 source: `external/swatplus-release_62_0_1/src` (commit 97ca231e). Example input files:
  `external/swatplus-release_62_0_1/refdata/*/FILE`.
- Known problems for each table: `reports/user-docs/swatplus-62.0.1-docs-findings.json`; Step 1's command prints
  the ones for FILE. They are a starting point: verify each item, and look for problems it missed.
- `swatref` = `./.venv/Scripts/swatref.exe`.
- **Tamandua 0.5.0** (code facts; it can answer "where is this value used?"):
  `.swatref/tamandua-0.5/venv/Scripts/python.exe .swatref/tamandua-0.5/ask.py TOOL key=value [-- TOOL key=value ...]`
  (`ask.py --list` shows the tools). Do NOT use your built-in `tamandua` MCP tools: they are the old 0.4.1,
  which lacks `uses` and misses the main program. Set `PYTHONIOENCODING=utf-8` if output fails to print.
  **Pitfall**: argument names vary by tool — `describe_type` requires `name=` (not `type=`), and `search_fields`
  requires `text=` (not `query=`). Check `ask.py --list` if a tool rejects your argument name.

## Working rules (so you do not go in circles)

- **Never run the same command twice.** If an answer was unclear, ask a different question or move on and
  mark the point "needs review" in the proposal. Do not re-run a search hoping for a different result.
- **Tamandua first** for every "where is X used / set / read" question: `uses` and `writers`, several at once
  with `--` (e.g. `ask.py uses variable=a -- writers variable=a -- uses variable=b`). Use `grep`/`sed` only to read
  source lines Tamandua pointed you to, or when Tamandua has no answer, and at most twice per question.
- **An empty result is an answer.** If Tamandua `uses` says `reads=none`, the value is never used: record that
  and move on; do not search the source again for it. If a search finds nothing, or a file is not found, check
  the path once (e.g. with `ls`), then accept the result and move on.
- **Use the commands given here.** Never run `python -c` (Hermes blocks it) and never write your own helper
  scripts: every step below has a ready-made command.
- **Paths:** the file tools (`read_file`, `write_file`, `search_files`) take Windows paths
  (`C:\Users\...`) or paths relative to the repo folder. `/c/Users/...` paths work only in the terminal.
- **Budget:** the whole task needs about 15-25 tool calls. After 35, stop investigating: leave the open points
  marked "needs review" in the proposal you saved in Step 4, then do Steps 6 and 7.

## Step 0: gate (stop if any check fails, and report what it printed)

    cd ... && git -C external/SWATPlus-user-documentation-hermes branch --show-current && git -C external/SWATPlus-user-documentation-hermes status --short
    cd ... && .swatref/tamandua-0.5/venv/Scripts/python.exe .swatref/tamandua-0.5/ask.py provenance -- file_io file=FILE

The branch must start with `hermes/`, the status must be empty, provenance must show
`source_commit=97ca231e22b29356b9891e057238fa3c68809da5`, and `file_io` must list a `read` row for FILE (its
reader). If `file_io` lists nothing, check the spelling of FILE against the request once, then stop and report.

## Step 1: the known problems, and where the docs pages are

    cd ... && ./.venv/Scripts/python.exe agent_eval/tools/known_problems.py FILE

It prints every known problem for FILE (and any that were checked and rejected), then the docs page folder
and the exact command that reads all its pages (you run that in Step 3). Do not search for the docs folder
yourself.

## Step 2: layout fixes (the tool makes them; never edit layout yourself)

    cd ... && ./.venv/Scripts/swatref.exe schema --source release_62_0_1 user-docs-apply FILE --docs-root external/SWATPlus-user-documentation-hermes
    cd ... && ./.venv/Scripts/swatref.exe schema --source release_62_0_1 user-docs-check FILE --docs-root external/SWATPlus-user-documentation-hermes

Paste both outputs. If apply prints `NOT APPLIED`, stop and report it.

## Step 3: evidence for EVERY row of the table (not only the listed ones)

Two commands give you almost everything:

1. **All the code evidence, in one call:**
   `cd ... && .swatref/tamandua-0.5/venv/Scripts/python.exe agent_eval/tools/field_evidence.py FILE`
   For every field of the file's record it lists: the declaration, unit and comment; every place the value is
   read (calculation, condition, call argument, output, or copy); everything else in the code that sets the value
   itself (`ALSO SET BY THE CODE`: the file's value can be replaced, e.g. forced to a constant before its only
   use, in which case the input has no effect); for each copy, where the copy is read and everything that sets
   it; for a value that is never read, other variables with the same name, with their reads and setters; and the
   example input file's header name and value. "(never read)" means the input has no effect.
2. **All the docs pages for the table, in one call:** run the `Read them all (Step 3): for f in ...` command
   that Step 1 printed, exactly as printed (after the `cd ... &&`). It prints every page of the table, so you
   now have all the docs text: do not open the pages again one by one.

Judge units from the formulas in the evidence: `(1. - x)` means x is a fraction 0-1; `x / 100.` means x is a
percent; a conversion factor (e.g. `/ 1000.`) only fits one unit, so work the arithmetic through. The declaration
comment can be outdated. A `comment:` line shown next to a formula usually documents that formula's units; check
it against the arithmetic too.

The docs' Unit, Default and Range columns are recommended values (e.g. from the SWAT+ Editor), not limits the
code enforces. Keep them unless the evidence contradicts them (e.g. a `(1. - x)` formula for a value documented
as 0-100 percent, or an example value outside the range). Never remove or narrow a range only because the code
does not check it or a declaration comment gives another one (mark that "needs review" instead), and never set
a unit to n/a only because the value is never read (say "not used" in the description and keep the unit).

## Step 4: write the proposal NOW, from Steps 1-3 alone (before any follow-up, so the work is saved)

Do NOT edit the docs wording. Write the whole proposal to `.swatref/hermes-proposals/FILE.md` (create the folder)
with your file-writing tool, then prove it exists: run
`cd ... && ls -la .swatref/hermes-proposals/ && head -40 .swatref/hermes-proposals/FILE.md` and paste that
output. If the file is not there, write it again; never report a file you have not seen listed.

For each row: current description / unit / range, proposed description / unit / range (or "no change"), and the
evidence (file:line plus the quoted statement). Add any change needed to the page's intro text, and the new text
for each affected field page (front matter `description:` plus a 1-3 sentence body with practical guidance, e.g.
what value to enter). Rules: state only what the evidence shows; keep the docs' short style; do not reword rows
that are already correct. Where the evidence leaves a question open, write your best reading and mark it
"needs review" instead of investigating first.

## Step 5: follow-ups (optional; at most five)

Only for a "needs review" point: one follow-up each (`ask.py ...`, or `sed -n 'A,Bp' <file>` to read source lines
the evidence points to), at most five in total. Never read the same source file again with shifted line ranges:
the evidence already quotes each statement. After each answer, update the proposal file (patch it) and drop the
"needs review" mark if the point is settled. Do not re-collect evidence Steps 1-3 already gave you.

## Step 6: second opinion (required; do not skip it, and do not ask whether to run it)

    cd ... && .swatref/tamandua-0.5/venv/Scripts/python.exe agent_eval/tools/second_opinion.py FILE

It sends the saved proposal and the code evidence to ANT `review_code` (GPT-OSS 120B) and prints the verdict and
the review (it takes about a minute; it also saves the review to `.swatref/hermes-proposals/FILE.review.md`).
Use this command, not the `review_code` MCP tool. Then add a `## Second opinion` section to the proposal file:
the verdict, and for each point the reviewer raised, whether you changed the proposal or why not. If the command
prints `review_code FAILED`, run it once more; if it fails again, quote the error in that section and continue.

**Check each change the reviewer asks for before you accept it: the reviewer can be wrong too** (it has argued
from an outdated declaration comment before, and asked to drop ranges the code does not enforce: keep those,
see Step 3). For a change of unit, range, meaning, or used/not used, redo the
point from the evidence (the formula, the `comment:` lines next to it, and where the value is read or set) and
write that check, with the arithmetic, into the Second opinion section. Change the proposal only if your check
agrees with the reviewer; if it does not, keep your version and say why.

**Pitfall**: the reviewer may ask for **code-level** changes (input validation, dead fields, flag handling). This
skill is docs-only: it never writes code. Record such points as code issues for a separate task; do not let them
block the documentation proposal.

## Step 7: report and stop

Report: the Step 2 outputs, the Step 4 listing, the proposal table, and the second-opinion verdict (a report
without the verdict is incomplete: go back and do Step 6). Then STOP: no wording edits to the docs, no commit, no
push.

Nobody is watching the run, so nobody can answer a question: never stop to ask whether to continue. Do every
step, then report.

Never edit docs files except through `user-docs-apply`. Never hand work to a subagent. Never describe a command's
result without having run it. Never call a tool a third time after two failures.
