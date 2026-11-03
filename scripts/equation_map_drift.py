"""Which equation-map citations did SWAT+ code changes touch? Deterministic, no AI.

The equation map cites code by line number at the commit it was checked against
(OLD). For each mapped equation this compares the cited lines with a later
commit (NEW) using git's line-by-line diff:
  - unchanged: same code at the same line numbers,
  - moved: same code, now at other line numbers (a corrected citation is suggested),
  - edited: a cited line itself changed, or code was inserted inside a cited range;
    the equation needs another look,
  - missing: the cited file or line does not exist (at NEW, or already at OLD),
  - no lines: the mapping gives no line numbers (a file named without lines is
    still checked for existence).
Whitespace-only changes are ignored. This says where the code changed, not whether
the equation still holds; an edit can be harmless and an unchanged line can sit in
code whose callers changed.

Reads either the doc-builder overlay (equation_map.json, field source_lines) or
the master list CSV (column cited_lines).

Usage:
    python scripts/equation_map_drift.py --repo <swatplus checkout> \\
        --map <swatplus-doc-builder>/overlays/equation_map.json --old 62.0.0 --new 6f515368
"""
from __future__ import annotations

import argparse
import csv
import json
import re
import subprocess
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUT = ROOT / "reports" / "equation_verify"

# Result labels, most severe first. A row gets the most severe one that applies.
MISSING = "missing"
EDITED = "edited"
MOVED = "moved"
UNCHANGED = "unchanged"
NO_CODE = "no_code"
SEVERITY = [MISSING, EDITED, MOVED, UNCHANGED, NO_CODE]

PLAIN = {
    MISSING: "Missing: the cited file or line does not exist",
    EDITED: "Edited: the cited code changed; check the equation again",
    MOVED: "Moved: same code at new line numbers; update the citation",
    UNCHANGED: "Unchanged: same code at the same lines",
    NO_CODE: "No lines: the mapping gives no code line numbers",
}

CITE_RE = re.compile(r"([A-Za-z0-9_]+\.f90):([0-9][0-9,\- ]*)")
FILE_RE = re.compile(r"[A-Za-z0-9_]+\.f90")
HUNK_RE = re.compile(r"^@@ -(\d+)(?:,(\d+))? \+(\d+)(?:,(\d+))? @@", re.M)


def git(repo: Path, *args: str) -> str:
    return subprocess.run(
        ["git", "-C", str(repo), *args],
        check=True, capture_output=True, text=True, encoding="utf-8", errors="replace",
    ).stdout


def parse_citations(text: str) -> list[tuple[str, list[tuple[int, int]]]]:
    """'a.f90:82,89 b.f90:10-12' -> [('a.f90', [(82, 82), (89, 89)]), ('b.f90', [(10, 12)])]"""
    cites = []
    for fname, spec in CITE_RE.findall(text or ""):
        ranges = []
        for part in re.split(r"[ ,]+", spec.strip(" ,-")):
            if part:
                a, _, b = part.partition("-")
                ranges.append((int(a), int(b) if b else int(a)))
        cites.append((fname, ranges))
    return cites


def parse_hunks(diff: str) -> list[tuple[int, int, int, int]]:
    return [(int(s), int(n or 1), int(t), int(m or 1)) for s, n, t, m in HUNK_RE.findall(diff)]


def new_line(hunks: list[tuple[int, int, int, int]], line: int) -> int | None:
    """Line number at NEW of OLD line `line`, or None if that line was changed or deleted."""
    shift = 0
    for s, n, _t, m in hunks:
        if n and s <= line < s + n:
            return None
        # n == 0 is a pure insertion after old line s
        if (n and s + n - 1 < line) or (not n and s < line):
            shift += m - n
    return line + shift


def load_map(path: Path) -> list[dict]:
    """Rows of {equation_id, routine, cited, status} from the JSON overlay or the master CSV."""
    if path.suffix.lower() == ".csv":
        with path.open(encoding="utf-8", newline="") as fh:
            return [
                {"equation_id": r["equation_id"], "routine": r.get("routine", ""),
                 "cited": r.get("cited_lines", ""), "status": r.get("status", "")}
                for r in csv.DictReader(fh)
            ]
    return [
        {"equation_id": r["equation_id"], "routine": r.get("routine", ""),
         "cited": r.get("source_lines") or "", "status": r.get("status", "")}
        for r in json.loads(path.read_text(encoding="utf-8"))["mappings"]
    ]


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--repo", type=Path, required=True, help="SWAT+ git checkout holding both commits")
    ap.add_argument("--map", type=Path, required=True, help="equation_map.json or equation_master_list.csv")
    ap.add_argument("--old", required=True, help="commit or tag the map was checked against (e.g. 62.0.0)")
    ap.add_argument("--new", required=True, help="commit or tag to compare with")
    ap.add_argument("--chapter", default="all", help="equation-id prefix before ':' (e.g. 3); 'all' for every row")
    ap.add_argument("--out", type=Path, default=DEFAULT_OUT)
    args = ap.parse_args(argv)

    old = git(args.repo, "rev-parse", "--short", f"{args.old}^{{commit}}").strip()
    new = git(args.repo, "rev-parse", "--short", f"{args.new}^{{commit}}").strip()
    n_commits = git(args.repo, "rev-list", "--count", f"{old}..{new}").strip()
    rows = load_map(args.map)
    if args.chapter != "all":
        rows = [r for r in rows if r["equation_id"].split(":", 1)[0] == args.chapter]

    hunks: dict[str, list[tuple[int, int, int, int]]] = {}
    exists: dict[str, bool] = {}
    old_text: dict[str, list[str]] = {}
    new_text: dict[str, list[str]] = {}

    def load(fname: str) -> None:
        if fname in hunks:
            return
        path = f"src/{fname}"
        in_old = bool(git(args.repo, "ls-tree", old, path).strip())
        exists[fname] = bool(git(args.repo, "ls-tree", new, path).strip())
        hunks[fname] = parse_hunks(git(args.repo, "diff", "-U0", "-w", old, new, "--", path)) if exists[fname] else []
        old_text[fname] = git(args.repo, "show", f"{old}:{path}").splitlines() if in_old else []
        new_text[fname] = git(args.repo, "show", f"{new}:{path}").splitlines() if exists[fname] else []

    def same(a: str, b: str) -> bool:
        return "".join(a.split()) == "".join(b.split())

    results = []
    for r in rows:
        cites = parse_citations(r["cited"])
        reasons: dict[str, str] = {}
        suggested = []
        bare = [f for f in dict.fromkeys(FILE_RE.findall(r["cited"])) if f not in {c[0] for c in cites}]
        for fname in bare:
            load(fname)
            if not old_text[fname] or not exists[fname]:
                reasons[MISSING] = f"{fname} does not exist at {old if not old_text[fname] else new}"
        if not cites:
            reasons.setdefault(NO_CODE, f"cites {', '.join(bare)} without line numbers" if bare else "no code location recorded")
        for fname, ranges in cites:
            load(fname)
            if not old_text[fname]:
                reasons[MISSING] = f"{fname} does not exist at {old}"
                continue
            if not exists[fname]:
                reasons[MISSING] = f"{fname} does not exist at {new}"
                continue
            parts = []
            for a, b in ranges:
                if b > len(old_text[fname]):
                    reasons.setdefault(MISSING, f"{fname}:{b} is past the end of the file at {old}")
                    continue
                na, nb = new_line(hunks[fname], a), new_line(hunks[fname], b)
                inside = [new_line(hunks[fname], i) for i in range(a, b + 1)]
                if None in inside or nb - na != b - a:
                    hit = next((a + i for i, x in enumerate(inside) if x is None), a)
                    reasons.setdefault(EDITED, f"{fname}:{hit} changed")
                    parts.append(f"{a}" if a == b else f"{a}-{b}")
                    continue
                if not all(same(old_text[fname][i - 1], new_text[fname][x - 1]) for i, x in zip(range(a, b + 1), inside)):
                    reasons.setdefault(EDITED, f"{fname}:{a} text differs at its new position")
                    parts.append(f"{a}" if a == b else f"{a}-{b}")
                    continue
                if na != a:
                    reasons.setdefault(MOVED, f"{fname}:{a} is now line {na}")
                parts.append(f"{na}" if a == b else f"{na}-{nb}")
            suggested.append(f"{fname}:{','.join(parts)}")
        if not reasons:
            reasons[UNCHANGED] = ""
        result = min(reasons, key=SEVERITY.index)
        results.append(
            {
                "equation_id": r["equation_id"],
                "drift_result": result,
                "reason": "; ".join(reasons[k] for k in SEVERITY if reasons.get(k)),
                "cited_lines": r["cited"],
                "suggested_lines": " ".join(suggested) if result == MOVED else "",
                "map_status": r["status"],
                "routine": r["routine"],
            }
        )

    args.out.mkdir(parents=True, exist_ok=True)
    stem = f"map_drift_{old}_{new}" + ("" if args.chapter == "all" else f"_chapter_{args.chapter}")
    with (args.out / f"{stem}.csv").open("w", encoding="utf-8", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=list(results[0]))
        writer.writeheader()
        writer.writerows(results)

    counts = Counter(x["drift_result"] for x in results)
    by_chapter: dict[str, Counter] = defaultdict(Counter)
    for x in results:
        by_chapter[x["equation_id"].split(":", 1)[0]][x["drift_result"]] += 1
    md = [
        f"# Equation map drift: {args.old} ({old}) to {args.new} ({new})",
        "",
        f"{len(results)} mapped equations from `{args.map.name}`; {n_commits} commits between the two versions. "
        "Deterministic comparison of the cited code lines. It shows where the code changed, "
        "not whether the equation still holds.",
        "",
        "| Result | Count |",
        "|---|---:|",
    ]
    md += [f"| {PLAIN[k]} | {counts[k]} |" for k in SEVERITY if counts[k]]
    md += ["", "## By chapter", "", "| Chapter | " + " | ".join(k.replace("_", " ").capitalize() for k in SEVERITY) + " |",
           "|---|" + "---:|" * len(SEVERITY)]
    for ch in sorted(by_chapter, key=lambda c: (len(c), c)):
        md.append(f"| {ch} | " + " | ".join(str(by_chapter[ch][k]) for k in SEVERITY) + " |")
    for k in (MISSING, EDITED):
        group = [x for x in results if x["drift_result"] == k]
        if group:
            md += ["", f"## {PLAIN[k]}", "", "| Eq | Map status | Cited | Why |", "|---|---|---|---|"]
            md += [f"| `{x['equation_id']}` | {x['map_status']} | {x['cited_lines']} | {x['reason']} |" for x in group]
    if counts[MOVED]:
        md += ["", f"{counts[MOVED]} moved citations and their corrected line numbers are in `{stem}.csv` "
               "(column `suggested_lines`)."]
    (args.out / f"{stem}.md").write_text("\n".join(md) + "\n", encoding="utf-8")

    for k in SEVERITY:
        if counts[k]:
            print(f"{counts[k]:4d}  {PLAIN[k]}")
    print(f"wrote {args.out / (stem + '.csv')} and .md")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
