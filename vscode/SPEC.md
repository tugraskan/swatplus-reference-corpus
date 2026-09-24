# VS Code extension: SWAT+ Reference Corpus

Build spec for a small VS Code extension that runs `swatref` from buttons.
Written to be implemented in one pass; read it all before starting.

## Goal

A corpus maintainer opens this repository in VS Code and, without typing a
command, can:

1. **Add a version**: pick a SWAT+ release tag, branch, or pull request from a list.
2. **Build** it: the input schema, the docs snapshot, or both.
3. **Compare** two versions and read the report.

That's the whole extension. Keep it small: roughly 300–500 lines of TypeScript
plus scaffolding.

## The one rule: no corpus logic in TypeScript

The extension is a thin set of buttons over the `swatref` CLI. It **never**:

- parses or writes `swatref.toml`
- runs `git` itself
- works out profile names, commits, versions, or output paths the CLI already knows
- edits Python code in this repository

Every piece of state comes from a `swatref` command that prints JSON (below). If
you find you need something the CLI does not provide, **stop and report it**.
Do not work around it in TypeScript. Profile locking to exact commits is the
point of this repository, and it lives in one place only.

## Where it lives

`vscode/` in this repository (`swatplus-reference-corpus`), next to this file.
It changes with the CLI it calls.

```
vscode/
  SPEC.md                this file
  package.json
  tsconfig.json
  esbuild.js
  eslint.config.mjs
  .vscode-test.mjs
  .vscodeignore
  .gitignore             node_modules/, dist/, out/, *.vsix
  README.md              install + usage, short
  resources/icon.svg
  src/
    extension.ts         activate(): register tree + commands
    swatref.ts           pure: JSON types, argv builders, ref grouping (no vscode import)
    runner.ts            find Python, check prerequisites, spawn with cancel + live output
    sourcesTree.ts       TreeDataProvider over `swatref source list`
    commands.ts          the three flows below
    test/
      swatref.test.ts    mocha unit tests of swatref.ts
```

## Reuse from swatplus-dataselector

Copy from `https://github.com/tugraskan/swatplus-dataselector` at `fc6c025`
(same owner, MIT). Adapt; do not add a dependency on that repository.

| Take | From | Change |
|---|---|---|
| Python candidate list | `src/indexer.ts:543` `getPythonCandidates()` | Put the `swatplusCorpus.pythonPath` setting first, then `SWATPLUS_PYTHON`, then the platform list |
| Prerequisite check with cache | `src/indexer.ts:571` `getIndexingPrerequisiteStatus()` | Check `import swatplus_reference` instead of the pandas modules |
| Async spawn with working Cancel | `src/indexer.ts:659` `runPythonIndexer()` | **Stream** each stdout/stderr chunk to the output channel as it arrives, not only at the end. Pass `cwd` = corpus root |
| Progress notification | `src/indexer.ts:884` `withProgress` usage | `cancellable: true`, wired to the spawn's cancel |
| Output channel | `src/indexer.ts:230` | Name it `SWAT+ Corpus`; show it when a run starts |
| Build and lint setup | `esbuild.js`, `eslint.config.mjs`, `tsconfig.json`, `.vscode-test.mjs`, the `package.json` scripts | Drop the webview check, the `@modelcontextprotocol/sdk` dependency, and the Python-test script |
| Activity-bar icon | `resources/splus-activitybar-cutout.svg` | Copy as `resources/icon.svg` |

Do **not** copy any webview panel. Use VS Code's built-in `TreeView`,
`QuickPick`, `InputBox`, and notifications only.

## How to run swatref

Always run `<python> -m swatplus_reference.cli <args…>` with `cwd` set to the
workspace folder that contains `swatref.toml`. Use the module form rather than
the `swatref` script, because the script may not be on `PATH` inside VS Code.
If no workspace folder contains `swatref.toml`, the extension does nothing
beyond showing a message on its commands.

If the prerequisite check fails, show an error with a **Copy install command**
button that copies `pip install -e .` (to be run in the corpus root).

Exit codes: `0` success; `1` a comparison ran but is incomplete; `2` bad
arguments or a failed step (argparse prints the reason on stderr). On any
non-zero exit, show the **last line of stderr** in the error notification,
with a **Show output** button.

## CLI contract (JSON on stdout)

These exist today (`src/swatplus_reference/cli.py`, `source/add.py`) and are
tested in `tests/test_source_add.py`.

**`source list`**: the configured profiles.
```json
[{"name": "release_62_0_0", "repository": "https://github.com/swat-model/swatplus",
  "ref": "62.0.0", "commit": "de210d64…", "label": "SWAT+ 62.0.0",
  "checkout": "external/swatplus-62.0.0", "fetched": true,
  "docs_default": false, "schema_default": true}]
```

**`source refs`**: what exists upstream (network; about 1 s). Release tags come first, newest first.
```json
{"tags": [{"ref": "62.0.0", "commit": "…", "release": true}, …],
 "branches": [{"ref": "main", "commit": "…"}, …]}
```

**`source add <ref> [--name N]`**: locks a ref to its current commit.
```json
{"profile": "release_63_0_0", "created": true, "moved": false,
 "commit": "…", "current_commit": "…", "ref": "63.0.0", "repository": "…", "checkout": "…"}
```
`created: false` means the ref was already configured and **was not relocked**.
`moved: true` means its branch has advanced since the lock.

**`source fetch <profile>`**: fetches and verifies; prints provenance JSON.

Non-JSON commands (the extension only needs the exit code; the log goes to the output channel):

| Action | argv |
|---|---|
| Schema | `schema build --source <p>` (+ `--version <v>` when the profile's ref is not a release tag) |
| Docs snapshot | `docs rich-parse --snapshot --source <p>` (about 2 min) |
| Compare | `compare --fetch --base <a> --candidate <b>` (+ `--skip-source-build`, `--skip-preview`) |

Output locations:
- **Schema:** `schema_artifacts/releases/swatplus-<version>.json`, where `<version>` is the release tag without a leading `v`, or the `--version` you passed.
- **Docs snapshot:** `snapshots/rich/`.
- **Comparison:** `reports/comparisons/<a>_vs_<b>/summary.md`.

## UI

**Activity bar:** one view container, "SWAT+ Corpus", with one tree view, **Sources**.

- One item per profile from `source list`. Label = `name`; description =
  `ref · commit[:12]`; tooltip = `label`. Icon: `check` when `fetched`,
  otherwise `cloud-download`. Append "(docs)" or "(schema)" to the
  description for the defaults.
- View title buttons: **Add version…** (`add`), **Refresh** (`refresh`).
- Item context menu: **Fetch**, **Build…**, **Compare with…**.
- Refresh after every command that can change the list (add, fetch, build).

**Commands** (also in the Command Palette, category "SWAT+ Corpus"):
`swatplusCorpus.addVersion`, `.build`, `.compare`, `.fetch`, `.refresh`,
`.showOutput`.

**Settings:** `swatplusCorpus.pythonPath` (string, default empty).

**Activation:** `workspaceContains:swatref.toml`, plus the view.

## Flows

### Add version
1. Run `source refs` under a progress notification.
2. Show a QuickPick with separators: **Releases** (`release: true`),
   **Other tags**, **Branches**, then two fixed items: **Pull request
   number…** (InputBox for digits only → ref `refs/pull/<n>/head`) and
   **Other ref or commit…** (free InputBox).
3. Run `source add <ref>`.
4. Handle the result:
   - `created` → info "Added `<profile>` locked at `<commit[:12]>`", with a **Build…** button.
   - `!created && moved` → warning "`<profile>` is locked at `<commit[:12]>`; `<ref>` is now at `<current_commit[:12]>`." Offer **no** relock; the CLI has none by design.
   - `!created && !moved` → info "`<profile>` is already configured."

### Build
1. Pick a profile (skip this step when invoked from a tree item).
2. Multi-select QuickPick: **Input schema** and **Docs snapshot**, both preselected.
3. If schema is selected and the profile's `ref` is not a release tag
   (`/^v?\d+(\.\d+)+$/`), ask for a version with an InputBox. Pre-fill it
   with the profile name. Cancelling the box cancels the build.
4. If `fetched` is false, run `source fetch <profile>` first.
5. Run the selected steps **in order, in one cancellable progress
   notification**, and stop at the first failure.
6. On success, show an info message with **Reveal schema** / **Reveal
   snapshots** buttons (`revealFileInOS`, or open the JSON in an editor).

### Compare
1. Pick a base, then a candidate. The candidate list excludes the base.
   From a tree item, that item is the candidate and you pick the base.
2. Multi-select QuickPick of options, **both unselected by default**, so the
   default is the fast path CI uses:
   - "Compile both sources (needs CMake + gfortran)". Unselected → `--skip-source-build`.
   - "Build strict docs preview (MkDocs)". Unselected → `--skip-preview`.
3. Run `compare --fetch --base <a> --candidate <b> …`.
4. Exit `0` → open `reports/comparisons/<a>_vs_<b>/summary.md` with
   `markdown.showPreview`. Exit `1` → open it anyway, plus a warning
   "Comparison incomplete: see summary". Anything else → the error handling above.

## Tests

- **`swatref.test.ts` (mocha, no VS Code):**
  - argv builders for each flow, including the `--version`, `--skip-*` and module-form prefix cases
  - the release-tag regex
  - QuickPick grouping of a `source refs` payload
  - JSON type guards that reject a malformed payload.

  Use the JSON shapes above as fixtures.
- `npm run compile`, `npm run lint`, and `npm run test:unit` must pass.
- The corpus's own Python tests must still pass:
  `python -m pytest -q` from the repository root. You are not changing Python,
  so this is a check that nothing else moved.

## Acceptance: run it, don't just test it

In an Extension Development Host (F5) opened on this repository, with the
package installed (`pip install -e ".[dev]"`):

1. The Sources tree lists `main`, `release_62_0_0`, `dev_pr252_base`, `pr_252`.
2. **Add version → Releases → 62.0.0** says it is already configured
   (as `release_62_0_0`) and changes nothing (`git diff swatref.toml` is empty).
3. **Add version → Branches → main** warns that `main` has moved, with no relock.
4. **Build `release_62_0_0` → Input schema only** succeeds, and
   `git diff schema_artifacts/` is **empty**. The rebuild is byte-identical
   to the committed artifact.
5. **Cancel** during a Docs snapshot build stops the Python process within
   about 2 seconds. Confirm with the OS process list.
6. With `swatplusCorpus.pythonPath` set to an interpreter that lacks the
   package, every command shows the install message instead of failing obscurely.
7. **Compare `dev_pr252_base` → `pr_252`** (fast path) opens its summary.
   Check that the counts match `reports/comparisons/pr-252/summary.md`.

Write down what you ran and what you saw for each step in the final report.
If any step fails, say so. Do not report the work as done.

## Out of scope

Webviews, a GitHub workflow, publishing to the Marketplace, editing
`swatref.toml` directly, relocking a moved branch, deleting profiles, a
status bar, and any change under `src/` or `tests/` (Python). If one of these
seems necessary, raise it instead of doing it.
