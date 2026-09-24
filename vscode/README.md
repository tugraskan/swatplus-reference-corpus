# SWAT+ Corpus

Add, build, and compare SWAT+ reference corpus source versions from buttons,
without typing `swatref` commands.

## Install

```bash
cd vscode
npm install
npm run compile
```

Press F5 in VS Code (with `vscode/` open, or the repository root with a
multi-root workspace including it) to launch an Extension Development Host.

The corpus itself needs `swatplus_reference` installed in the Python the
extension calls:

```bash
pip install -e .
```

Set `swatplusCorpus.pythonPath` in Settings if that Python is not the first
`python3`/`python` on your `PATH`.

## Use

Open a folder containing `swatref.toml`. A **SWAT+ Corpus** icon appears in
the Activity Bar with a **Sources** tree listing every profile from
`swatref source list`.

- **Add Version…** (toolbar) — pick a release, tag, branch, or pull request
  from upstream and lock it to its current commit.
- **Build…** (item menu) — build the input schema, the docs snapshot, or
  both, for a version.
- **Compare With…** (item menu) — run a locked source-to-source comparison
  and open its report.
- **Fetch** (item menu) — fetch a version's checkout without building
  anything.
- **Refresh** (toolbar) — reload the tree from `swatref source list`.

All output streams to the **SWAT+ Corpus** output channel
(**SWAT+ Corpus: Show Output**).

## Develop

```bash
npm run lint
npm run test:unit   # mocha unit tests of the pure swatref.ts module
npm test            # full extension test in a VS Code instance
```

This extension never parses or writes `swatref.toml`, runs `git` itself, or
duplicates anything `swatref` already knows — it only shells out to
`python -m swatplus_reference.cli` and reads its JSON.
