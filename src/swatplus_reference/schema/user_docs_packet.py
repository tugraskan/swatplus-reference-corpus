"""Evidence packet for one user-docs input table, and a pass/fail check.

`build_packet` gathers what an editor needs to fix one table without
guessing:

- the table's exact current rows, with line numbers;
- the source fields in read order, each with its declaration and comment
  (file and line);
- where each missing row goes, and which rows the source does not read;
- the reader's read statement in context;
- what calls the reader;
- example input-file headers.

`check_tables` re-runs the comparison after an edit and says whether each
table is done:

- the table matches the source, or differs only by unconfirmed names;
- no field link is broken;
- every linked page is registered in `SUMMARY.md` and has front matter.

Neither function writes anything.
"""

from __future__ import annotations

import re
from pathlib import Path
from urllib.parse import unquote

from .user_docs import (
    build_report,
    editor_names,
    field_origins,
    field_table,
    field_table_lines,
    match_rows,
)

SOURCE_SUFFIXES = (".f90", ".f", ".F90", ".F")
COMPARABLE = ("match", "names_to_check", "differs")


def _read_lines(path: Path, cache: dict[Path, list[str]]) -> list[str]:
    if path not in cache:
        cache[path] = path.read_text(encoding="utf-8", errors="replace").splitlines()
    return cache[path]


def _code(line: str) -> str:
    return line.split("!", 1)[0]


def declaration(source_root: Path, type_source: str, name: str,
                cache: dict[Path, list[str]]) -> dict | None:
    """Where component ``name`` is declared, with the comment lines that continue it.

    Looks inside the record type's own lines first (``type_source`` is
    ``file:first-last``), then anywhere in that file, for components of a
    nested type.
    """
    file, _, span = type_source.partition(":")
    path = source_root / file
    if not path.exists():
        return None
    lines = _read_lines(path, cache)
    lo, hi = (int(x) for x in span.split("-")) if "-" in span else (1, len(lines))

    def declares(line: str) -> bool:
        m = re.search(r"::(.*)", _code(line))
        listed = re.findall(r"(?:^|,)\s*([a-z_]\w*)", m.group(1), re.I) if m else []
        return name.lower() in (n.lower() for n in listed)

    n = next((k for k in range(lo, min(hi, len(lines)) + 1) if declares(lines[k - 1])), None)
    if n is None:
        n = next((k for k in range(1, len(lines) + 1) if declares(lines[k - 1])), None)
    if n is None:
        return None
    text, end = [lines[n - 1].strip()], n
    while end < len(lines) and lines[end].strip().startswith("!") and len(text) < 8:
        text.append(lines[end].strip())
        end += 1
    return {"at": f"{file}:{n}" + (f"-{end}" if end > n else ""), "text": text}


def callers(source_root: Path, routine: str, cache: dict[Path, list[str]]) -> list[str]:
    """``file:line`` of every ``call <routine>`` in the source (comments ignored)."""
    rx = re.compile(rf"\bcall\s+{re.escape(routine)}\b", re.I)
    found = []
    for path in sorted(p for p in source_root.rglob("*") if p.suffix in SOURCE_SUFFIXES):
        for n, line in enumerate(_read_lines(path, cache), 1):
            if rx.search(_code(line)):
                found.append(f"{path.relative_to(source_root).as_posix()}:{n}")
    return found


def _statement(lines: list[str], start: int) -> list[tuple[int, str]]:
    """The statement starting at line ``start``, with its ``&`` continuations."""
    out, n = [], start
    while n <= len(lines):
        out.append((n, lines[n - 1].rstrip()))
        if not _code(lines[n - 1]).rstrip().endswith("&"):
            break
        n += 1
    return out


def build_packet(schema: dict, provenance: dict, docs_root: Path, source_root: Path,
                 file: str, field_map: dict | None = None,
                 headers: dict[str, list[list[str]]] | None = None,
                 check_command: str = "") -> dict:
    """The evidence packet for one input file's docs table."""
    report = build_report(schema, provenance, docs_root, field_map, "", headers, "")
    entry = report["files"].get(file.lower())
    if entry is None:
        raise ValueError(f"{file} is not an input file SWAT+ {schema.get('swatplus_version')} reads")
    packet: dict = {
        "file": file.lower(),
        "swatplus_version": schema.get("swatplus_version"),
        "source_commit": provenance.get("resolved_commit"),
        "docs_commit": report["docs"]["commit"],
        "status": entry["status"],
        "check_command": check_command,
    }
    if "table_page" not in entry:
        packet["note"] = f"no Field table to compare ({entry['status']})"
        return packet

    flat = schema["files"][file.lower()]
    origins = field_origins(flat)
    source = [f for f, _, _ in origins]
    page = docs_root / entry["table_page"]
    text = page.read_text(encoding="utf-8")
    rows = field_table(text) or []
    raw = field_table_lines(text)
    if len(raw) != len(rows):
        raw = [(None, "")] * len(rows)
    editor = editor_names(field_map).get(file.lower(), {})
    cache: dict[Path, list[str]] = {}

    pairs = match_rows(source, rows, editor)
    row_of = {j: i for i, j in pairs}
    used = set(row_of.values())
    fields = []
    for j, f in enumerate(source):
        i, how = row_of.get(j), "same name"
        if i is None and j < len(rows) and j not in used:
            i, how = j, "same position, different name"
            used.add(j)
        fields.append({
            "position": j + 1,
            "fortran_name": f["fortran_name"],
            "type": f["fortran_type"],
            "units": f.get("units"),
            "editor_name": editor.get(f["fortran_name"].lower()),
            "read_at": origins[j][1],
            "repeated": origins[j][2],
            "docs_row": {"line": raw[i][0], "field": rows[i]["field"], "match": how}
            if i is not None else None,
            "declaration": declaration(source_root, flat["type_source"], f["fortran_name"], cache)
            if flat.get("type_source") else None,
        })
    index_of_line = {raw[i][0]: i for i in range(len(rows))}
    replaced_by: dict[int, str] = {}
    for k, f in enumerate(fields):
        if f["docs_row"] is None:
            prev = next((g["docs_row"] for g in reversed(fields[:k]) if g["docs_row"]), None)
            f["insert"] = (f"after line {prev['line']} (the {prev['field']} row)" if prev
                           else f"before line {raw[0][0]} (as the first row)" if raw
                           else "as the first row")
            # A row the source no longer reads, sitting exactly where this field
            # goes, was most likely renamed to it (e.g. bed_load -> bankfull_flo).
            nxt = index_of_line.get(prev["line"], -1) + 1 if prev else 0
            if 0 <= nxt < len(rows) and nxt not in used and nxt not in replaced_by:
                replaced_by[nxt] = f["fortran_name"]
                f["probably_replaces"] = rows[nxt]["field"]

    reader_path = source_root / flat["reader"]
    reader_lines = _read_lines(reader_path, cache) if reader_path.exists() else []
    at = flat.get("reader_line") or 1
    routine = Path(flat["reader"]).stem
    packet.update({
        "table_page": entry["table_page"],
        "listed_on": entry.get("listed_on"),
        "shares_table_with": sorted(f for f, e in report["files"].items()
                                    if e.get("table_page") == entry["table_page"]
                                    and f != file.lower()),
        "differences": {k: entry[k] for k in ("missing_from_docs", "not_in_source",
                                               "name_differs", "out_of_order",
                                               "type_differs", "broken_links") if k in entry},
        "reader": {
            "file": flat["reader"],
            "routine": routine,
            "statement": _statement(reader_lines, at) if reader_lines else [],
            "reads": [{"line": n, "statement": _statement(reader_lines, n)}
                      for n in sorted({line for _, line, _ in origins if line})]
            if reader_lines else [],
            "context": [(n, reader_lines[n - 1].rstrip())
                        for n in range(max(1, at - 10), min(len(reader_lines), at + 4) + 1)],
            "called_from": callers(source_root, routine, cache),
        },
        "record_type": {"name": flat.get("derived_type"), "at": flat.get("type_source")},
        "repeat": ({"count_field": flat["repeat"].get("count_field"),
                    "first_repeated": next(f["position"] for f in fields if f["repeated"])}
                   if flat.get("repeat") and any(f["repeated"] for f in fields) else None),
        "fields": fields,
        "docs_rows": [{"line": raw[i][0], "field": r["field"], "type": r.get("type", ""),
                       "link": r["link"], "raw": raw[i][1],
                       "read_by_source": i in used,
                       "probably_replaced_by": replaced_by.get(i)} for i, r in enumerate(rows)],
        "example_headers": (headers or {}).get(file.lower(), []),
    })
    return packet


def render_packet(packet: dict) -> str:
    p = packet
    out = [f"# Packet: {p['file']} (SWAT+ {p['swatplus_version']} @ {str(p['source_commit'])[:12]}, "
           f"docs @ {str(p['docs_commit'])[:12]})", "", f"Status: **{p['status']}**"]
    if "table_page" not in p:
        return "\n".join(out + ["", p.get("note", "")]) + "\n"
    out.append(f"Docs table: `{p['table_page']}`")
    if p.get("listed_on"):
        out.append(f"Shared table, listed on `{p['listed_on']}`")
    if p["shares_table_with"]:
        out.append("The same table also documents: " + ", ".join(f"`{f}`" for f in p["shares_table_with"]))
    r = p["reader"]
    out += ["", "## Reader", "",
            f"`{r['routine']}` in `{r['file']}` is called from: "
            + (", ".join(f"`{c}`" for c in r["called_from"]) if r["called_from"]
               else "**nothing (the reader never runs; leave this table alone)**"),
            "", "Read statement and context:", "", "```fortran"]
    out += [f"{n:5}  {line}" for n, line in r["context"]]
    out += ["```", ""]
    if len(r.get("reads", [])) > 1:
        out += ["This file is read as several records. Every read statement, in file order", "(fields below give the line they are read at):", "", "```fortran"]
        for read in r["reads"]:
            out += [f"{n:5}  {line}" for n, line in read["statement"]]
        out += ["```", ""]
    if p["record_type"]["name"]:
        out.append(f"Record type: `{p['record_type']['name']}` at `{p['record_type']['at']}`")
    if p["repeat"]:
        out.append(f"Fields from #{p['repeat']['first_repeated']} on repeat "
                   f"`{p['repeat']['count_field']}` times; the docs list them once.")
    out += ["", "## Source fields, in read order", "",
            "| # | Fortran | Type | Units | Editor column | Read at | Docs row | Declaration |",
            "| --- | --- | --- | --- | --- | --- | --- | --- |"]
    for f in p["fields"]:
        row = f["docs_row"]
        docs = (f"line {row['line']}: `{row['field']}`" + ("" if row["match"] == "same name" else f" ({row['match']})")
                if row else f"**MISSING**, insert {f['insert']}"
                + (f"; probably replaces `{f['probably_replaces']}`" if f.get("probably_replaces") else ""))
        decl = f"`{f['declaration']['at']}`" if f["declaration"] else "not found"
        read_at = f"line {f['read_at']}" + (" (repeated)" if f["repeated"] else "") if f.get("read_at") else ""
        out.append(f"| {f['position']} | `{f['fortran_name']}` | {f['type']} | {f['units'] or ''} | "
                   f"{f['editor_name'] or ''} | {read_at} | {docs} | {decl} |")
    out += ["", "## Declarations (exact source text)", ""]
    for f in p["fields"]:
        if f["declaration"]:
            out.append(f"- `{f['fortran_name']}` at `{f['declaration']['at']}`:")
            out += ["  ```fortran"] + [f"  {t}" for t in f["declaration"]["text"]] + ["  ```"]
    out += ["", "## Current docs rows (exact text)", ""]
    for d in p["docs_rows"]:
        flag = "" if d["read_by_source"] else "   <-- NOT READ BY THE SOURCE" + (
            f" (probably replaced by `{d['probably_replaced_by']}`: rename its field page)"
            if d.get("probably_replaced_by") else "")
        out.append(f"- line {d['line']}: `{d['raw'].strip()[:300]}`{flag}")
    if p["example_headers"]:
        out += ["", "## Example input-file headers (refdata; older than the readers)", ""]
        out += [f"- `{' '.join(h)}`" for h in p["example_headers"]]
    if p["differences"]:
        out += ["", "## Differences the report found", ""]
        out += [f"- {k}: {v}" for k, v in p["differences"].items()]
    if p.get("check_command"):
        out += ["", "## When you have edited the table", "", "```sh", p["check_command"], "```"]
    return "\n".join(out) + "\n"


def _front_matter_ok(path: Path) -> bool:
    text = path.read_text(encoding="utf-8")
    head = re.match(r"\A---\s*\n(.*?)\n---\s*\n", text, re.S)
    return bool(head and re.search(r"^description:", head.group(1), re.M)
                and re.search(r"^# \S", text[head.end():], re.M))


def check_tables(schema: dict, provenance: dict, docs_root: Path, files: list[str],
                 field_map: dict | None = None,
                 headers: dict[str, list[list[str]]] | None = None,
                 new_pages: set[Path] | None = None) -> tuple[bool, list[str]]:
    """Whether each table is done: ``(all passed, one line per file and problem)``.

    ``new_pages`` (added or modified field pages) are also held to the
    front-matter rule; existing pages are not.
    """
    report = build_report(schema, provenance, docs_root, field_map, "", headers, "")
    io = docs_root / "io-docs"
    summary = (io / "SUMMARY.md").read_text(encoding="utf-8")
    registered = {unquote(t) for t in re.findall(r"\]\(([^)]+\.md)\)", summary)}
    lines: list[str] = []
    ok = True

    targets: list[str] = []
    for f in files:
        f = f.lower()
        targets.append(f)
        page = (report["files"].get(f) or {}).get("table_page")
        targets += [g for g, e in sorted(report["files"].items())
                    if page and e.get("table_page") == page and g not in targets]

    for f in targets:
        e = report["files"].get(f)
        if e is None:
            ok = False
            lines.append(f"FAIL {f}: not an input file SWAT+ {schema.get('swatplus_version')} reads")
            continue
        if e["status"] not in COMPARABLE:
            lines.append(f"SKIP {f}: {e['status']}, no Field table to check")
            continue
        problems = []
        if e["status"] == "differs":
            for k in ("missing_from_docs", "not_in_source", "out_of_order"):
                if e.get(k):
                    problems.append(f"{k.replace('_', ' ')}: {', '.join(e[k])}")
            for d in e.get("type_differs", []):
                problems.append(f"type of {d['field']}: docs {d['docs']}, source {d['source']}")
        if e.get("broken_links"):
            problems.append("broken links: " + ", ".join(e["broken_links"]))
        page = docs_root / e["table_page"]
        for row in field_table(page.read_text(encoding="utf-8")) or []:
            link = unquote(row["link"].split("#", 1)[0])
            if not link or "://" in link:
                continue
            target = (page.parent / link).resolve()
            if target.is_dir():
                target = target / "README.md"
            if not target.exists():
                continue  # reported as a broken link above
            try:
                rel = target.relative_to(io.resolve()).as_posix()
            except ValueError:
                problems.append(f"{row['field']}: links outside io-docs ({link})")
                continue
            if rel not in registered:
                problems.append(f"{row['field']}: {rel} is not in SUMMARY.md")
            if new_pages is not None and target in new_pages and not _front_matter_ok(target):
                problems.append(f"{row['field']}: {rel} needs front matter with description: and a # heading")
        if problems:
            ok = False
            lines.append(f"FAIL {f}: " + "; ".join(problems))
        else:
            note = (" (names to check: " + ", ".join(d["docs"] for d in e.get("name_differs", [])) + ")"
                    if e["status"] == "names_to_check" else "")
            lines.append(f"PASS {f}{note}")

    dangling = sorted(t for t in registered if not (io / t).exists())
    if dangling:
        ok = False
        lines.append("FAIL SUMMARY.md points at missing pages: " + ", ".join(dangling))
    return ok, lines
