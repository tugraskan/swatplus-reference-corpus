"""Compare the SWAT+ user documentation's input tables with a release schema.

The user documentation (`SWATPlus-user-documentation`, published on GitBook)
has one page per input file with a ``Field | Description | Type | ...``
table. This report reads a checkout of it, read-only, and checks each table
against the fields the release's Fortran readers actually read:

- every input file the release reads has a page, and every file page names a
  file the release still reads. A file with no page of its own is checked
  against a shared table when a section page lists it and points to one
  (every ``*.con`` file uses ``'object'.con``); otherwise it is reported as
  named only (e.g. in the ``file.cio`` list) or not mentioned at all;
- each table lists the source's fields, no others, in the source's order;
- each field's documented type agrees with its Fortran type; and
- each field link points at a page that exists.

Docs name fields by their file-header (Editor) column, the source by its
Fortran variable, so a field matches on either name; Editor names come from
the field map. A name still in doubt is confirmed when one of SWAT+'s own
example input files (``refdata/``, same commit) has it in its header at that
position. Units, ranges, defaults, and descriptions are not compared.
Files read as multi-record, multi-section, runtime-arity, or decision-table
layouts are checked for a page only. The checkout is never written.
"""

from __future__ import annotations

import html
import json
import os
import re
import subprocess
from difflib import get_close_matches
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote

IO_DOCS = Path("io-docs") / "introduction-1"
STRUCTURED = ("multi_record", "multi_section", "runtime_arity", "decision_tables")
# Differences in what a table lists. A name difference alone is reported
# separately: the docs use file-header names, and without an Editor mapping
# for a field the header name cannot be checked against the Fortran name.
STRUCTURAL = {"missing_from_docs", "not_in_source", "out_of_order", "type_differs"}

# Documented type words -> the Fortran type they describe.
DOC_TYPES = {
    "integer": "integer", "int": "integer",
    "real": "real", "float": "real",
    "string": "character", "character": "character", "char": "character", "text": "character",
    "logical": "logical", "boolean": "logical",
}

_LINK_RX = re.compile(r"\[([^\]]*)\]\(([^)\s]*)[^)]*\)")
_HREF_RX = re.compile(r'<a\b[^>]*\bhref="([^"]*)"', re.I)
_TAG_RX = re.compile(r"<[^>]+>")
_FILE_RX = re.compile(r"^[a-z0-9][\w\-]*\.[a-z][\w]*", re.I)


# --------------------------------------------------------------------------
# Docs side: pages and their field tables
# --------------------------------------------------------------------------

class _Tables(HTMLParser):
    """Collect HTML tables as rows of ``(text, first link href)`` cells."""

    def __init__(self) -> None:
        super().__init__()
        self.tables: list[list[list[tuple[str, str]]]] = []
        self._rows: list | None = None
        self._row: list | None = None
        self._cell: list[str] | None = None
        self._href = ""

    def handle_starttag(self, tag, attrs):
        if tag == "table":
            self._rows = []
        elif tag == "tr" and self._rows is not None:
            self._row = []
        elif tag in ("td", "th") and self._row is not None:
            self._cell, self._href = [], ""
        elif tag == "a" and self._cell is not None and not self._href:
            self._href = dict(attrs).get("href") or ""

    def handle_endtag(self, tag):
        if tag in ("td", "th") and self._cell is not None:
            self._row.append((" ".join("".join(self._cell).split()), self._href))
            self._cell = None
        elif tag == "tr" and self._row is not None:
            self._rows.append(self._row)
            self._row = None
        elif tag == "table" and self._rows is not None:
            self.tables.append(self._rows)
            self._rows = None

    def handle_data(self, data):
        if self._cell is not None:
            self._cell.append(data)


def _pipe_tables(text: str) -> list[list[list[tuple[str, str]]]]:
    tables, current = [], []
    for line in text.splitlines() + [""]:
        s = line.strip()
        if s.startswith("|") and s.endswith("|"):
            cells = [c.strip() for c in re.split(r"(?<!\\)\|", s[1:-1])]
            # A delimiter row: every cell is hyphens with optional colons (`:--:`).
            if not all(re.fullmatch(r":?-+:?", c) for c in cells if c):
                row = []
                for c in cells:
                    # GitBook mixes HTML into pipe cells: <p>, <a href>, &#xD;
                    md, tag = _LINK_RX.search(c), _HREF_RX.search(c)
                    href = md.group(2) if md else tag.group(1) if tag else ""
                    plain = _TAG_RX.sub(" ", _LINK_RX.sub(r"\1", c))
                    plain = html.unescape(plain).replace("\\", "").replace("`", "")
                    row.append((" ".join(plain.split()), href))
                current.append(row)
        elif current:
            tables.append(current)
            current = []
    return tables


_INVISIBLE = dict.fromkeys(map(ord, "​‌‍﻿"), None) | {0xA0: " "}


def _clean(cell: str) -> str:
    """Cell text without zero-width or non-breaking spaces GitBook leaves behind."""
    return cell.translate(_INVISIBLE).strip()


def field_table(text: str) -> list[dict] | None:
    """The first table whose first column is ``Field``, as row dicts, or None.

    Each row has ``field``, ``type`` (when the table has one), and ``link``
    (the field cell's link target, "" when unlinked).
    """
    parser = _Tables()
    parser.feed(text)
    for table in parser.tables + _pipe_tables(text):
        if not table or table[0][0][0].strip().lower() != "field":
            continue
        header = [c[0].strip().lower() for c in table[0]]
        rows = []
        for cells in table[1:]:
            if not cells or not _clean(cells[0][0]):
                continue
            row = {"field": _clean(cells[0][0]), "link": cells[0][1]}
            if "type" in header and header.index("type") < len(cells):
                row["type"] = _clean(cells[header.index("type")][0])
            rows.append(row)
        return rows
    return None


def _title_files(text: str) -> set[str]:
    """File names in the H1 title (``# rout\\_unit.rtu``, ``# Master File (file.cio)``)."""
    m = re.search(r"^#\s+(.+)$", text, re.M)
    if not m:
        return set()
    title = m.group(1).replace("\\", "").replace("`", "").lower()
    return set(re.findall(r"[a-z0-9][\w\-]*\.[a-z]\w*", title))


def _page_name(path: Path) -> str:
    return (path.parent.name if path.name == "README.md" else path.stem).lower()


def _documents(name: str, file: str) -> bool:
    """Whether a page called ``name`` documents input ``file`` (GitBook slugs
    append ``-...`` words, e.g. ``pcp.cli-and-precipitation-data-files``)."""
    return name == file or name.startswith(file + "-")


def index_pages(io_root: Path, files: set[str]) -> tuple[dict[str, list[Path]], list[dict]]:
    """``{input file: [pages]}`` plus file-level pages that match no input file.

    A page documents a file when its name (README pages: the folder name) is
    that file, or when it is a README or category-level page whose H1 title
    names it (GitBook names some folders ``untitled-1``). Field pages inside a
    file's folder are not file pages.
    """
    by_file: dict[str, list[Path]] = {}
    unmatched: list[dict] = []
    for path in sorted(io_root.rglob("*.md")):
        depth = len(path.relative_to(io_root).parts)
        readme = path.name == "README.md"
        names = {_page_name(path)}
        if readme or depth <= 2:
            names |= _title_files(path.read_text(encoding="utf-8"))
        hits = sorted({f for f in files for n in names if _documents(n, f)})
        for f in hits:
            by_file.setdefault(f, []).append(path)
        file_names = sorted(n for n in names if _FILE_RX.match(n))
        if not hits and file_names and depth <= (3 if readme else 2):
            # Only near-identical names (chan_surf.lin vs chan-surf.lin); looser
            # matches pointed at the wrong file (atmo.cli -> cs_atmo.cli).
            closest = {m for n in file_names for m in get_close_matches(n, files, 1, 0.9)}
            unmatched.append({"page": path, "names": file_names, "closest": sorted(closest)})
    return by_file, unmatched


def _table_cells(text: str) -> set[str]:
    parser = _Tables()
    parser.feed(text)
    return {_clean(cell[0]).replace("*", "").lower()
            for table in parser.tables + _pipe_tables(text) for row in table for cell in row}


def _linked_pages(page: Path, text: str) -> set[Path]:
    """Docs pages ``page`` links to (a folder link means its README)."""
    out = set()
    for target in [m.group(2) for m in _LINK_RX.finditer(text)] + _HREF_RX.findall(text):
        target = unquote(target.split("#", 1)[0])
        if not target or "://" in target:
            continue
        linked = Path(os.path.normpath(page.parent / target))
        if target.endswith("/") or linked.is_dir():
            linked = linked / "README.md"
        if linked.suffix == ".md" and linked.is_file():
            out.add(linked)
    return out


def shared_tables(io_root: Path, files: set[str]) -> dict[str, tuple[Path, Path]]:
    """``{file: (table page, listing page)}`` for files documented once for many.

    A section page that lists two or more input files in a table and links to
    exactly one page with a Field table documents all of them with that table.
    (Connectivity lists every ``*.con`` file and describes them once, as
    ``'object'.con``.)
    """
    shared: dict[str, tuple[Path, Path]] = {}
    for page in sorted(io_root.rglob("README.md")):
        text = page.read_text(encoding="utf-8")
        listed = files & _table_cells(text)
        if len(listed) < 2:
            continue
        tables = {p for p in _linked_pages(page, text)
                  if field_table(p.read_text(encoding="utf-8"))}
        if len(tables) == 1:
            table = tables.pop()
            for file in listed:
                shared.setdefault(file, (table, page))
    return shared


def named_in(io_root: Path, files: set[str]) -> dict[str, dict]:
    """``{file: {"pages": [...], "not_used": bool}}`` for files the docs name.

    ``not_used`` is set when a mention is followed on its line by "currently
    not used", as the master-file (``file.cio``) list marks many files.
    """
    texts = {p: html.unescape(p.read_text(encoding="utf-8")).replace("\\", "")
             for p in sorted(io_root.rglob("*.md"))}
    named: dict[str, dict] = {}
    for file in sorted(files):
        name = re.escape(file)
        mention = re.compile(rf"(?<![\w.\-]){name}(?![\w\-])", re.I)
        pages = [p for p, t in texts.items() if mention.search(t)]
        if pages:
            not_used = re.compile(rf"{name}[^\n]{{0,40}}currently not used", re.I)
            named[file] = {"pages": pages,
                           "not_used": any(not_used.search(texts[p]) for p in pages)}
    return named


# --------------------------------------------------------------------------
# Comparison
# --------------------------------------------------------------------------

def editor_names(field_map: dict | None) -> dict[str, dict[str, str]]:
    """``{file: {fortran name: Editor column}}`` from a field-map report."""
    out: dict[str, dict[str, str]] = {}
    for file, rows in ((field_map or {}).get("files") or {}).items():
        for row in rows:
            source = (row.get("source") or {}).get("name")
            editor = (row.get("editor_database") or {}).get("name")
            if source and editor:
                out.setdefault(file.lower(), {})[source.lower()] = editor.lower()
    return out


def expected_fields(entry: dict) -> list[dict]:
    """The fields a docs table should list: fixed fields, then each repeated one once."""
    fields = list(entry.get("fields") or [])
    repeat = entry.get("repeat") or {}
    return fields + list(repeat.get("fields") or [])


def compare_table(source: list[dict], rows: list[dict], editor: dict[str, str]) -> dict:
    """Field-level differences between a docs table and the source's fields."""
    def names(f: dict) -> set[str]:
        fortran = f["fortran_name"].lower()
        return {fortran, editor.get(fortran, fortran)}

    pairs: list[tuple[int, int]] = []
    free = set(range(len(source)))
    for i, row in enumerate(rows):
        name = row["field"].lower()
        j = next((j for j in sorted(free) if name in names(source[j])), None)
        if j is not None:
            pairs.append((i, j))
            free.discard(j)
    matched_docs = {i for i, _ in pairs}
    extra = [i for i in range(len(rows)) if i not in matched_docs]
    missing = sorted(free)

    def label(f: dict) -> str:
        fortran = f["fortran_name"].lower()
        shown = editor.get(fortran)
        return f"{shown} ({fortran})" if shown and shown != fortran else fortran

    # A docs row and a source field left over at the same position are most
    # likely one field under two names; report them as a pair, not twice.
    renamed = [(i, i) for i in extra if i in missing]
    renamed_docs = {i for i, _ in renamed}
    differences = {
        "missing_from_docs": [label(source[j]) for j in missing if j not in renamed_docs],
        "not_in_source": [rows[i]["field"] for i in extra if i not in renamed_docs],
        "name_differs": [
            {"position": i + 1, "docs": rows[i]["field"], "source": label(source[i])}
            for i, _ in renamed
        ],
        "out_of_order": [
            rows[i]["field"] for k, (i, j) in enumerate(pairs)
            if any(j2 < j for _, j2 in pairs[k + 1:])
        ],
        "type_differs": [
            {"field": rows[i]["field"], "docs": rows[i]["type"],
             "source": source[j]["fortran_type"]}
            for i, j in pairs
            if DOC_TYPES.get(rows[i].get("type", "").lower(), source[j]["fortran_type"])
            != source[j]["fortran_type"]
        ],
    }
    return {k: v for k, v in differences.items() if v}


def example_headers(refdata: Path | None) -> dict[str, list[list[str]]]:
    """``{file: [header tokens, one list per example dataset]}``.

    SWAT+ ships example datasets (``refdata/<dataset>/``) whose second line is
    the column-header row real input files carry. They may be written for an
    older revision, so they confirm column names, never structure.
    """
    headers: dict[str, list[list[str]]] = {}
    if refdata is None or not refdata.is_dir():
        return headers
    for path in sorted(refdata.glob("*/*")):
        if path.is_file():
            lines = path.read_text(encoding="utf-8", errors="replace").splitlines()
            if len(lines) >= 2:
                headers.setdefault(path.name.lower(), []).append(lines[1].lower().split())
    return headers


def _confirm_names(entry: dict, headers: list[list[str]]) -> None:
    """Move name differences a real file header settles out of ``name_differs``.

    A docs name that an example file's header has at the same position is the
    real column name. Applied only after matching, so it cannot hide a
    missing, extra, or reordered field.
    """
    confirmed, open_ = [], []
    for d in entry.get("name_differs", []):
        p, name = d["position"], d["docs"].lower()
        hit = any(len(h) >= p and h[p - 1] == name for h in headers)
        (confirmed if hit else open_).append(d)
    if confirmed:
        entry["names_confirmed_by_example_header"] = confirmed
        if open_:
            entry["name_differs"] = open_
        else:
            del entry["name_differs"]


def _broken_links(page: Path, rows: list[dict]) -> list[str]:
    broken = []
    for row in rows:
        link = unquote(row["link"].split("#", 1)[0])
        if link and "://" not in link and not (page.parent / link).exists():
            broken.append(f"{row['field']} -> {link}")
    return broken


def _commit(root: Path) -> str:
    result = subprocess.run(["git", "-C", str(root), "rev-parse", "HEAD"],
                            capture_output=True, text=True, check=False)
    return result.stdout.strip() if result.returncode == 0 else ""


def build_report(schema: dict, provenance: dict, docs_root: Path,
                 field_map: dict | None, field_map_name: str = "",
                 headers: dict[str, list[list[str]]] | None = None,
                 headers_name: str = "") -> dict:
    """The user-docs input-table report for one release schema. Reads only.

    ``headers`` are example-file header rows (see `example_headers`) from the
    same source commit as the schema; they only confirm column names.
    """
    io_root = docs_root / IO_DOCS
    if not io_root.is_dir():
        raise FileNotFoundError(f"{io_root} not found; is --docs-root a SWATPlus-user-documentation checkout?")
    kinds = {f.lower(): "flat" for f in schema["files"]}
    for section in STRUCTURED:
        kinds.update({f.lower(): section for f in schema.get(section) or {}})
    kinds.update({u["file"].lower(): "unresolved" for u in schema.get("unresolved") or []})
    by_file, unmatched = index_pages(io_root, set(kinds))
    # Count every listed file when spotting a shared table (hru.con has its own
    # page but is still one of the files the connectivity table lists); the
    # loop below uses a shared table only for files without a page.
    shared = shared_tables(io_root, set(kinds))
    named = named_in(io_root, set(kinds) - set(by_file) - set(shared))
    flat = {f.lower(): e for f, e in schema["files"].items()}
    names = editor_names(field_map)

    def rel(p: Path) -> str:
        return p.relative_to(docs_root).as_posix()

    def compare(entry: dict, file: str, page: Path, rows: list[dict], own: bool) -> None:
        source = expected_fields(flat[file])
        entry.update(table_page=rel(page), docs_fields=len(rows), source_fields=len(source))
        if flat[file].get("variable_arity"):
            entry["variable_arity"] = True
        entry.update(compare_table(source, rows, names.get(file, {})))
        _confirm_names(entry, (headers or {}).get(file, []))
        # A shared table's links are its own page's; report them there only.
        if own and (broken := _broken_links(page, rows)):
            entry["broken_links"] = broken
        if set(entry) & STRUCTURAL:
            entry["status"] = "differs"
        elif "name_differs" in entry:
            entry["status"] = "names_to_check"
        else:
            entry["status"] = "match"

    files = {}
    for file in sorted(kinds):
        pages = by_file.get(file, [])
        entry: dict = {"layout": kinds[file], "pages": [rel(p) for p in pages]}
        if pages:
            tables = [(p, t) for p in pages if (t := field_table(p.read_text(encoding="utf-8")))]
            if kinds[file] != "flat":
                entry["status"] = "not_compared"
            elif not tables:
                entry["status"] = "no_field_table"
            else:
                compare(entry, file, *tables[0], own=True)
        elif file in shared:
            table, listing = shared[file]
            entry["listed_on"] = rel(listing)
            if kinds[file] == "flat":
                compare(entry, file, table, field_table(table.read_text(encoding="utf-8")),
                        own=False)
            else:
                entry.update(status="not_compared", shared_page=rel(table))
        elif file in named:
            entry.update(status="named_only", named_on=[rel(p) for p in named[file]["pages"]])
            if named[file]["not_used"]:
                entry["docs_say_not_used"] = True
        else:
            entry["status"] = "no_page"
        files[file] = entry

    counts: dict[str, int] = {}
    for e in files.values():
        counts[e["status"]] = counts.get(e["status"], 0) + 1
    return {
        "swatplus_version": schema.get("swatplus_version"),
        "source": {k: provenance.get(k) for k in ("profile", "repository", "resolved_commit")},
        "docs": {"repository": docs_root.name, "commit": _commit(docs_root)},
        "field_map": field_map_name,
        "example_headers": headers_name,
        "summary": {
            "input_files": len(files),
            **dict(sorted(counts.items())),
            "files_with_broken_links": sum(1 for e in files.values() if e.get("broken_links")),
            "pages_not_in_schema": len(unmatched),
        },
        "files": files,
        "pages_not_in_schema": [
            {"page": rel(u["page"]), "names": u["names"], "closest": u["closest"]}
            for u in unmatched
        ],
    }


# --------------------------------------------------------------------------
# Markdown
# --------------------------------------------------------------------------

def render_markdown(report: dict) -> str:
    s, src, docs = report["summary"], report["source"], report["docs"]
    out = [
        f"# User documentation vs SWAT+ {report['swatplus_version']} input files",
        "",
        f"- Source: `{src['profile']}` @ `{src['resolved_commit']}`",
        f"- Docs: `{docs['repository']}` @ `{docs['commit'] or 'unknown'}`",
        f"- Editor column names: `{report['field_map'] or 'none'}`",
        f"- Example file headers: {report.get('example_headers') or 'none'}",
        "",
        "Checks page coverage, field names and order, types, and field links. "
        "A file without its own page is compared with a shared table when a "
        "section page lists it and points to one (the `*.con` files share "
        "`'object'.con`). *Named only* means the docs name the file (usually in "
        "the `file.cio` list) but no page describes it; *no page* means it is "
        "not mentioned at all. "
        "Units, ranges, defaults, and descriptions are not compared. Non-flat "
        "layouts are checked for a page only. *Names to check* means the only "
        "difference is a field name that matches neither the Fortran variable, a "
        "known Editor column, nor an example file's header at that position; the "
        "docs may well be right.",
        "",
        "## Summary",
        "",
        "| Status | Files |",
        "| --- | --- |",
    ]
    for key in ("match", "differs", "names_to_check", "no_field_table", "named_only",
                "no_page", "not_compared"):
        if s.get(key):
            out.append(f"| {key} | {s[key]} |")
    out += [
        f"| **total input files read by {report['swatplus_version']}** | {s['input_files']} |",
        "",
        f"- Tables with broken field links: {s['files_with_broken_links']}",
        f"- Docs pages for files not in the {report['swatplus_version']} input schema: "
        f"{s['pages_not_in_schema']}",
        "",
    ]
    files = report["files"]

    def section(title: str, status: str, describe) -> None:
        names = [f for f, e in files.items() if e["status"] == status]
        if names:
            out.extend([f"## {title} ({len(names)})", ""])
            for f in names:
                out.append(describe(f, files[f]))
            out.append("")

    def differs(f: str, e: dict) -> str:
        via = f" (shared table, listed on `{e['listed_on']}`)" if e.get("listed_on") else ""
        lines = [f"- **`{f}`**: `{e['table_page']}`{via}: {e['docs_fields']} docs rows, "
                 f"{e['source_fields']} source fields"
                 + (" (repeating group)" if e.get("variable_arity") else "")]
        for key, text in (("missing_from_docs", "missing from docs"),
                          ("not_in_source", "not read by the source"),
                          ("out_of_order", "out of order")):
            if e.get(key):
                lines.append(f"  - {text}: " + ", ".join(f"`{x}`" for x in e[key]))
        for d in e.get("name_differs", []):
            lines.append(f"  - position {d['position']}: docs `{d['docs']}`, source `{d['source']}`")
        for d in e.get("type_differs", []):
            lines.append(f"  - type of `{d['field']}`: docs {d['docs']}, source {d['source']}")
        if confirmed := e.get("names_confirmed_by_example_header"):
            lines.append("  - names confirmed by an example file header: " + ", ".join(
                f"`{d['docs']}` (source `{d['source']}`)" for d in confirmed))
        return "\n".join(lines)

    section("Tables that differ from the source", "differs", differs)
    section("Tables whose field names need a check", "names_to_check", differs)
    section("Named in the docs, but no page describes them", "named_only",
            lambda f, e: f"- `{f}`: named on " + ", ".join(f"`{p}`" for p in e["named_on"][:3])
            + (" (marked *currently not used*)" if e.get("docs_say_not_used") else ""))
    section("Input files not mentioned anywhere in the docs", "no_page",
            lambda f, e: f"- `{f}` ({e['layout'].replace('_', ' ')})")
    section("Pages without a Field table", "no_field_table",
            lambda f, e: f"- `{f}`: " + ", ".join(f"`{p}`" for p in e["pages"]))
    section("Pages not compared (non-flat layout)", "not_compared",
            lambda f, e: f"- `{f}` ({e['layout'].replace('_', ' ')}): `{e['pages'][0]}`")
    section("Tables that match", "match", lambda f, e: f"- `{f}`" + (
        f" (shared table, listed on `{e['listed_on']}`)" if e.get("listed_on") else ""))

    broken = [(f, e) for f, e in files.items() if e.get("broken_links")]
    if broken:
        out.extend([f"## Broken field links ({len(broken)} tables)", ""])
        for f, e in broken:
            out.append(f"- `{f}`: " + ", ".join(f"`{b}`" for b in e["broken_links"]))
        out.append("")
    if report["pages_not_in_schema"]:
        out.extend([
            f"## Docs pages for files not in the {report['swatplus_version']} input schema",
            "",
            "Renamed or removed files, user-named files, or files the schema does not "
            "model (such as `file.cio`).",
            "",
        ])
        for u in report["pages_not_in_schema"]:
            hint = f"; near-identical input file: `{', '.join(u['closest'])}`" if u["closest"] else ""
            out.append(f"- `{u['page']}` (names `{', '.join(u['names'])}`{hint})")
        out.append("")
    return "\n".join(out).rstrip() + "\n"


def write_report(report: dict, json_path: Path) -> Path:
    """Write the JSON and Markdown reports; returns the Markdown path."""
    json_path.parent.mkdir(parents=True, exist_ok=True)
    json_path.write_bytes((json.dumps(report, indent=2, sort_keys=True) + "\n").encode("utf-8"))
    md_path = json_path.with_suffix(".md")
    md_path.write_bytes(render_markdown(report).encode("utf-8"))
    return md_path
