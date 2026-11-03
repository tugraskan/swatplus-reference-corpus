"""The known problems for one SWAT+ input table, and where its docs pages are, in one call.

Usage (from the corpus root, with the corpus venv's python):
  ./.venv/Scripts/python.exe agent_eval/tools/known_problems.py bmpuser.str
  ./.venv/Scripts/python.exe agent_eval/tools/known_problems.py bmpuser.str --docs-root external/SWATPlus-user-documentation
  ./.venv/Scripts/python.exe agent_eval/tools/known_problems.py bmpuser.str --source release_62_0_0

Prints:
  - every item of reports/user-docs/swatplus-<version>-docs-findings.json for the file, in full (`--source NAME`,
    a source in swatref.toml, picks the version; default release_62_0_1, the only version with a findings list so
    far);
  - findings that were checked and rejected (the docs were right);
  - the docs page folder for the file, its pages, and the exact command that reads them all.
It is a script file on purpose: Hermes blocks `python -c` in unattended runs.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import swat_source
from swat_source import CORPUS

sys.path.insert(0, str(CORPUS / "src"))
from swatplus_reference.schema.user_docs import IO_DOCS, index_pages  # noqa: E402

DEFAULT_DOCS = "external/SWATPlus-user-documentation-hermes"


def findings_path(source: swat_source.Source) -> Path:
    return CORPUS / "reports" / "user-docs" / f"swatplus-{source.version}-docs-findings.json"


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("file", help="input file name, e.g. bmpuser.str")
    ap.add_argument("--docs-root", default=DEFAULT_DOCS, help=f"docs checkout (default {DEFAULT_DOCS})")
    ap.add_argument("--source", help=f"a source in swatref.toml (default {swat_source.DEFAULT_SOURCE})")
    args = ap.parse_args(argv)
    sys.stdout.reconfigure(encoding="utf-8")
    file = args.file
    source = swat_source.resolve(args.source)

    findings = findings_path(source)
    if not findings.is_file():
        print(f"# Known problems for {file} ({source.label})\n")
        print(f"(no findings list for {source.label}: {findings.relative_to(CORPUS).as_posix()} does not exist; "
              "check every row against the code evidence)")
    else:
        data = json.loads(findings.read_text(encoding="utf-8"))
        items = [i for i in data["items"] if i["file"] == file]
        rejected = [r for r in data.get("rejected", []) if r["file"] == file]
        print(f"# Known problems for {file} ({data['source']}; checked against docs commit {data['docs_commit']})\n")
        print("A starting point, not the answer: verify each item against the code evidence, and look for problems")
        print("it missed in the other rows.\n")
        if not items:
            print("(no known problems listed for this file)\n")
        for n, i in enumerate(items, 1):
            code = f" (code `{i['code']}`)" if i.get("code") else ""
            kind = " ".join(x for x in (i["verdict"], i.get("subtype")) if x)
            print(f"{n}. row `{i['row']}`{code}: {kind}; impact {i['impact']}; status {i['status']}")
            print(f"   {i['detail']}")
        if rejected:
            print("\nChecked and rejected (the docs are right here):")
            for r in rejected:
                print(f"- row `{r['row']}`: {r['why']}")

    docs = Path(args.docs_root)
    docs_abs = docs if docs.is_absolute() else CORPUS / docs
    io_root = docs_abs / IO_DOCS
    if not io_root.is_dir():
        print(f"\n# Docs pages\n\nNo docs folder at {args.docs_root}/{IO_DOCS.as_posix()}.")
        return 1
    pages = index_pages(io_root, {file.lower()})[0].get(file.lower(), [])
    print("\n# Docs pages")
    if not pages:
        print(f"\nNo page documents {file} under {args.docs_root}/{IO_DOCS.as_posix()}.")
        return 1
    for page in pages:
        folder = page.parent if page.name == "README.md" else None
        rel = (docs / page.relative_to(docs_abs)).as_posix()
        if folder is None:
            print(f"\nPage (a single file, no field pages): `{rel}`")
            print(f"Read it (Step 3): cat \"{rel}\"")
            continue
        folder_rel = (docs / folder.relative_to(docs_abs)).as_posix()
        names = sorted(p.name for p in folder.glob("*.md"))
        print(f"\nTable page: `{rel}`")
        print(f"Folder: `{folder_rel}` ({len(names)} pages: {', '.join(names)})")
        print(f"Read them all (Step 3): for f in {folder_rel}/*.md; do echo \"== $f\"; cat \"$f\"; done")
    return 0


if __name__ == "__main__":
    sys.exit(main())
