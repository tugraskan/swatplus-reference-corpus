"""Evidence packet for one user-docs input table, and a pass/fail check.

`build_packet` gathers what an editor needs to fix one table without
guessing:

- the table's exact current rows, with line numbers;
- the source fields in read order, each with its declaration and comment
  (file and line);
- where each missing row goes, and which rows the source does not read;
- the reader's read statement in context;
- what calls the reader;
- example input-file headers;
- every edit as exact text: row moves, row edits (type, deletion), and each
  missing field's row, field page, and `SUMMARY.md` line. An agent applies
  these; it does not compose rows from the source.

`check_tables` re-runs the comparison after an edit and says whether each
table is done:

- the table matches the source, or differs only by unconfirmed names, or its
  reader never runs (skipped);
- no row is split across lines or has the wrong number of cells;
- no field link is broken;
- every linked page is registered in `SUMMARY.md` and has front matter.

Neither function writes anything.
"""

from __future__ import annotations

import html
import re
from difflib import SequenceMatcher
from pathlib import Path
from urllib.parse import unquote

from .user_docs import (
    _CELL_RX,
    _INVISIBLE,
    build_report,
    editor_names,
    field_origins,
    field_table,
    field_table_columns,
    field_table_lines,
    malformed_table_lines,
    match_rows,
)

SOURCE_SUFFIXES = (".f90", ".f", ".F90", ".F")
COMPARABLE = ("match", "names_to_check", "differs")
DOCS_TYPES = {"character": "string", "double precision": "real"}


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


def comment_lines(decl: dict | None) -> list[str]:
    """A declaration's comment, one entry per source line, without ``!`` or units."""
    out = []
    for k, line in enumerate((decl or {}).get("text", [])):
        part = line if k else (line.split("!", 1)[1] if "!" in line else "")
        part = part.lstrip("!").strip()
        if "|" in part:  # SWAT+ writes `!!units  |description`
            part = part.split("|", 1)[1].strip()
        if part:
            out.append(part)
    return out


def _row_start(raw: str) -> str:
    """An HTML row up to the end of its first cell: unique, and free of the
    invisible characters GitBook leaves in other cells."""
    m = re.match(r"<tr\b[^>]*>\s*<t[dh]\b.*?</t[dh]>", raw, re.S)
    return m.group(0) if m else raw


def _moves(fields: list[dict], docs_rows: list[dict], kind: str | None) -> list[dict]:
    """The fewest row moves that put the docs rows in the source's read order.

    Rows outside the longest run already in order move, in read order, to
    directly after the row of the nearest earlier source field. Done before
    the inserts, these make every "insert after" anchor land in read order.
    """
    index = {d["field"]: i for i, d in enumerate(docs_rows)}
    placed = sorted((index[f["docs_row"]["field"]], f["position"])
                    for f in fields if f["docs_row"] and f["docs_row"]["field"] in index)
    seq = [pos for _, pos in placed]
    # longest increasing subsequence of source positions, in docs order
    best: list[list[int]] = []
    for pos in seq:
        prev = max((run for run in best if run[-1] < pos), key=len, default=[])
        best.append(prev + [pos])
    keep = set(max(best, key=len, default=[]))
    row_at = {pos: docs_rows[i] for i, pos in placed}
    moves = []
    for pos in sorted(p for p in seq if p not in keep):
        row = row_at[pos]
        after = next((row_at[q] for q in sorted(keep, reverse=True) if q < pos), None)
        first = row_at[min(keep)] if after is None and keep else None
        move = {"field": row["field"], "line": row["line"],
                "after": after["field"] if after else None, "after_line": after["line"] if after else None}
        if after is None:
            move.update(before=first["field"] if first else None, before_line=first["line"] if first else None)
        target = after or first
        if kind == "html":
            move["anchor"] = _row_start(row["raw"])
            move["to_anchor"] = _row_start(target["raw"]) if target else None
        moves.append(move)
        keep.add(pos)
    return moves


def _with_cell(raw: str, kind: str, col: int, value: str) -> str:
    """Row ``raw`` with cell ``col`` set to ``value`` (HTML rows also lose invisible characters)."""
    if kind == "html":
        cells = list(_CELL_RX.finditer(raw))
        cell = cells[col]
        opening = re.match(r"<t[dh]\b[^>]*>", cell.group(0)).group(0)
        closing = cell.group(0)[-5:]
        raw = raw[:cell.start()] + opening + value + closing + raw[cell.end():]
        return raw.translate(_INVISIBLE)
    parts = re.split(r"(?<!\\)\|", raw)
    old = parts[col + 1]
    parts[col + 1] = f" {value} ".ljust(len(old)) if len(old) >= len(value) + 2 else f" {value} "
    return "|".join(parts)


def _with_name(raw: str, kind: str, name: str) -> str:
    """Row ``raw`` with its Field cell's visible name set to ``name``; the link target is kept."""
    if kind == "html":
        cell = next(_CELL_RX.finditer(raw))
        text = cell.group(0)
        link = re.search(r"(<a\b[^>]*>)(.*?)(</a>)", text, re.S)
        if link:
            text = text[:link.start(2)] + html.escape(name) + text[link.end(2):]
        else:
            opening = re.match(r"<t[dh]\b[^>]*>", text).group(0)
            text = opening + html.escape(name) + text[-5:]
        return (raw[:cell.start()] + text + raw[cell.end():]).translate(_INVISIBLE)
    escaped = name.replace("_", "\\_")
    parts = re.split(r"(?<!\\)\|", raw)
    old = parts[1]
    if re.search(r"\[[^\]]*\]\(", old):
        new = re.sub(r"\[[^\]]*\]\(", lambda _: f"[{escaped}](", old, count=1).strip()
    else:
        new = escaped
    parts[1] = f" {new} ".ljust(len(old)) if len(old) >= len(new) + 2 else f" {new} "
    return "|".join(parts)


def _same_field(docs_name: str, editor: str, match: str) -> bool:
    """Whether a docs row and the Editor column plainly name the same field.

    True when the row already uses the Fortran name, when one name contains
    the other (``unit``/``units``, ``ini``/``cha_ini``), or when they differ
    by a typo (``plt_p``/``ptl_p``). A row matched only by position with an
    unrelated name may be out of order (``irr_eff`` sits where ``amt_mm`` is
    read) or describe a field whose meaning changed (``aq_reac``/``aq_hlife``),
    so it is left to a person.
    """
    a, b = docs_name.lower(), editor.lower()
    return match == "same name" or a in b or b in a or SequenceMatcher(None, a, b).ratio() >= 0.75


def _renamed_entry(edit: dict, d: dict, name: str, table: Path, io: Path, summary: list[str]) -> None:
    """Add the SUMMARY.md entry and page heading that carry the row's old name."""
    link = unquote(d["link"].split("#", 1)[0]) if d["link"] and "://" not in d["link"] else ""
    target = (table.parent / link).resolve() if link else None
    if target is None or not target.is_file() or not target.is_relative_to(io.resolve()):
        return
    escaped = name.replace("_", "\\_")
    old = d["field"].lower()
    rel = target.relative_to(io.resolve()).as_posix()
    for line in summary:
        shown = re.search(r"\[([^\]]*)\]\(" + re.escape(rel) + r"\)", line)
        if shown and shown.group(1).replace("\\", "").lower() == old:
            edit["summary_rename"] = {"from": line, "to": line.replace(f"[{shown.group(1)}]", f"[{escaped}]", 1)}
            break
    heading = next((s for s in target.read_text(encoding="utf-8").splitlines() if s.startswith("# ")), None)
    if heading and heading[2:].strip().replace("\\", "").lower() == old:
        edit["heading"] = {"page": f"io-docs/{rel}", "from": heading, "to": f"# {escaped}"}


def _row_edits(docs_rows: list[dict], columns: tuple[list[str], str] | None, differences: dict,
               table_page: str, docs_root: Path, fields: list[dict] | None = None) -> list[dict]:
    """Exact edits for rows the source does not read (delete), rows of the wrong type,
    and rows whose name is a variant of the field's Editor column (rename)."""
    if columns is None:
        return []
    header, kind = columns
    lower = [c.lower() for c in header]
    retype = {d["field"]: DOCS_TYPES.get(d["source"], d["source"])
              for d in differences.get("type_differs", [])}
    rename = {(f["docs_row"]["line"], f["docs_row"]["field"]): f["editor_name"]
              for f in fields or []
              if f["docs_row"] and f["editor_name"]
              and f["docs_row"]["field"].lower() != f["editor_name"].lower()
              and _same_field(f["docs_row"]["field"], f["editor_name"], f["docs_row"]["match"])}
    io = docs_root / "io-docs"
    summary_path = io / "SUMMARY.md"
    summary = summary_path.read_text(encoding="utf-8").splitlines() if summary_path.exists() else []
    table = (docs_root / table_page).resolve()
    edits = []
    for d in docs_rows:
        edit = {"field": d["field"], "line": d["line"], "raw": d["raw"]}
        if kind == "html":
            edit["anchor"] = _row_start(d["raw"])
        new_name = rename.get((d["line"], d["field"]))
        if new_name and d["read_by_source"]:
            row = _with_name(d["raw"], kind, new_name)
            if d["field"] in retype and "type" in lower:
                row = _with_cell(row, kind, lower.index("type"), retype[d["field"]])
                edit["to"] = retype[d["field"]]
            edit.update(action="edit" if "to" in edit else "rename", rename_to=new_name, row=row)
            _renamed_entry(edit, d, new_name, table, io, summary)
            edits.append(edit)
            continue
        if not d["read_by_source"] and not d.get("probably_replaced_by"):
            edit["action"] = "delete"
            link = unquote(d["link"].split("#", 1)[0]) if d["link"] and "://" not in d["link"] else ""
            target = (table.parent / link).resolve() if link else None
            if target is not None and target.is_file() and target.is_relative_to(io.resolve()):
                rel = target.relative_to(io.resolve()).as_posix()
                n = next((k + 1 for k, s in enumerate(summary) if f"]({rel})" in s), None)
                if n:
                    edit["summary_line"] = n
                    edit["summary_text"] = summary[n - 1].strip()
                # remove the page too, unless another page links to it
                others = [p for p in io.rglob("*.md")
                          if p.resolve() not in (table, target, summary_path.resolve())
                          and target.name in p.read_text(encoding="utf-8", errors="replace")]
                if not others:
                    edit["remove_page"] = f"io-docs/{rel}"
        elif d["field"] in retype and "type" in lower:
            edit.update(action="retype", to=retype[d["field"]],
                        row=_with_cell(d["raw"], kind, lower.index("type"), retype[d["field"]]))
        else:
            continue
        edits.append(edit)
    return edits


def _summary_block(summary: list[str], target: str) -> tuple[int, int, str] | None:
    """``(entry line, last line of its children, child indent)`` for the entry linking ``target``."""
    k = next((k for k, s in enumerate(summary) if f"]({target})" in s), None)
    if k is None:
        return None
    indent = len(summary[k]) - len(summary[k].lstrip())
    end = k
    while end + 1 < len(summary) and (not summary[end + 1].strip()
                                      or len(summary[end + 1]) - len(summary[end + 1].lstrip()) > indent):
        end += 1
    while end > k and not summary[end].strip():
        end -= 1
    return k + 1, end + 1, " " * (indent + 2)


def _exact_text(fields: list[dict], docs_rows: list[dict], columns: tuple[list[str], str] | None,
                table_page: str, docs_root: Path, headers: list[list[str]]) -> list[dict]:
    """The exact table row, field page, and SUMMARY.md line for each missing field.

    A new row is named after its Editor column, else after the example file
    header at the same position when that header has exactly the source's
    columns (the name users see in their files), else after the Fortran name.
    """
    if columns is None:
        return []
    header, kind = columns
    io = docs_root / "io-docs"
    summary_path = io / "SUMMARY.md"
    summary = summary_path.read_text(encoding="utf-8").splitlines() if summary_path.exists() else []
    table_dir = (docs_root / table_page).parent
    folder = table_dir.relative_to(io).as_posix() if table_dir.is_relative_to(io) else ""
    block = _summary_block(summary, f"{folder}/{Path(table_page).name}") if folder else None
    by_field = {d["field"]: d for d in docs_rows}

    def summary_line_of(link: str) -> int | None:
        if not link or "://" in link or block is None:
            return None
        rel = (table_dir / unquote(link.split("#", 1)[0])).resolve()
        try:
            rel_s = rel.relative_to(io.resolve()).as_posix()
        except ValueError:
            return None
        return next((n for n in range(block[0] + 1, block[1] + 1) if f"]({rel_s})" in summary[n - 1]), None)

    out, after_new = [], None
    for k, f in enumerate(fields):
        if f["docs_row"] is not None:
            after_new = None
            continue
        same_layout = sorted({h[f["position"] - 1] for h in headers if len(h) == len(fields)})
        if f["editor_name"]:
            name, named = f["editor_name"], "the Editor column"
        elif len(same_layout) == 1:
            name, named = same_layout[0], "the example file header, which has the same columns"
        else:
            name, named = f["fortran_name"], "the Fortran variable"
        escaped = name.replace("_", "\\_")
        comment = comment_lines(f["declaration"])
        description = "; ".join(comment)
        ftype = DOCS_TYPES.get(f["type"], f["type"])
        cells = []
        for col in header:
            c = col.lower()
            if c == "field":
                cells.append(f'<a href="{name}.md">{html.escape(name)}</a>' if kind == "html"
                             else f"[{escaped}]({name}.md)")
            elif c == "description":
                cells.append(html.escape(description) if kind == "html" else description.replace("|", "\\|"))
            elif c == "type":
                cells.append(ftype)
            elif c in ("unit", "units"):
                cells.append(f["units"] or "")
            else:
                cells.append("")
        row = ("<tr>" + "".join(f"<td>{c}</td>" for c in cells) + "</tr>" if kind == "html"
               else "| " + " | ".join(cells) + " |")
        quoted = description.replace("\\", "\\\\").replace('"', '\\"')
        body = ("\n".join(f"- {c}" for c in comment) if len(comment) > 1
                else comment[0] if comment else "")
        page_text = f'---\ndescription: "{quoted}"\n---\n\n# {escaped}\n' + (f"\n{body}\n" if body else "")
        page = f"{folder}/{name}.md" if folder else f"{name}.md"
        item = {"field": f["fortran_name"], "name": name, "named_after": named,
                "position": f["position"], "row": row,
                "page": page, "page_text": page_text,
                "summary_line": (block[2] if block else "    ") + f"* [{escaped}]({page})"}

        old = by_field.get(f.get("probably_replaces") or "")
        if old:
            old_link = unquote(old["link"].split("#", 1)[0]) if old["link"] and "://" not in old["link"] else ""
            old_page = (table_dir / old_link).resolve() if old_link else None
            item["table"] = (f"replace the whole {old['field']} row, from this exact text through its `</tr>`,"
                             if kind == "html" else f"replace line {old['line']} (the {old['field']} row)")
            item["table_mode"] = "replace"
            if kind == "html":
                item["table_anchor"] = _row_start(old["raw"])
            else:
                item["table_raw"] = old["raw"]
            if old_page is not None and old_page.is_file() and old_page.is_relative_to(io.resolve()):
                item["page_from"] = f"io-docs/{old_page.relative_to(io.resolve()).as_posix()}"
                item["page_action"] = f"git mv {item['page_from']} io-docs/{page}, then replace its whole text with"
            n = summary_line_of(old["link"])
            item["summary"] = (f"replace line {n} (`{summary[n - 1].strip()}`)" if n
                               else None)
            if n:
                item["summary_mode"], item["summary_ref"] = "replace", summary[n - 1]
        elif after_new:
            item["table"] = f"insert right after the row you add for {after_new}"
            item["table_mode"] = "after_new"
        elif kind == "html" and docs_rows:
            prev = next((g["docs_row"] for g in reversed(fields[:k]) if g["docs_row"]), None)
            at = [d["field"] for d in docs_rows].index(prev["field"]) + 1 if prev else 0
            if at < len(docs_rows):
                item["table"] = (f"insert directly before this exact text, the start of the "
                                 f"{docs_rows[at]['field']} row (line {docs_rows[at]['line']})")
                item["table_anchor"] = _row_start(docs_rows[at]["raw"])
                item["table_mode"] = "before"
            elif (docs_root / table_page).read_text(encoding="utf-8").count("</tbody>") == 1:
                item["table"] = "insert directly before this exact text, the end of the table"
                item["table_anchor"] = "</tbody>"
                item["table_mode"] = "before"
            else:
                item["table"] = (f"insert directly after the `</tr>` that ends the {docs_rows[-1]['field']} "
                                 f"row, the last row, which starts with this exact text")
                item["table_anchor"] = _row_start(docs_rows[-1]["raw"])
                item["table_mode"] = "after_row_end"
        else:
            item["table"] = f"insert {f['insert']}"
            prev = next((g["docs_row"] for g in reversed(fields[:k]) if g["docs_row"]), None)
            if prev:
                item["table_mode"], item["table_raw"] = "after", by_field[prev["field"]]["raw"]
            elif docs_rows:
                item["table_mode"], item["table_raw"] = "before", docs_rows[0]["raw"]
        if "summary" not in item or item["summary"] is None:
            if after_new:
                item["summary"] = f"insert right after the line you add for {after_new}"
                item["summary_mode"] = "after_new"
            elif block is None:
                item["summary"] = "add under the table's own entry (none found in SUMMARY.md: add that too)"
            else:
                # after the nearest earlier row that has a SUMMARY.md entry, else first child
                n = next((m for g in reversed(fields[:k]) if g["docs_row"]
                          for m in [summary_line_of(by_field[g["docs_row"]["field"]]["link"])] if m),
                         block[0])
                item["summary"] = f"insert after line {n} (`{summary[n - 1].strip()}`)"
                item["summary_mode"], item["summary_ref"] = "after", summary[n - 1]
        item.setdefault("page_action", f"create io-docs/{page} with")
        out.append(item)
        after_new = name
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
        "malformed_lines": malformed_table_lines(text),
    })
    columns = field_table_columns(text)
    live = bool(packet["reader"]["called_from"])
    packet["moves"] = _moves(fields, packet["docs_rows"], columns and columns[1]) if live else []
    packet["row_edits"] = (_row_edits(packet["docs_rows"], columns, packet["differences"],
                                      entry["table_page"], docs_root, fields) if live else [])
    renamed = {(e["line"], e["field"]) for e in packet["row_edits"] if e.get("rename_to")}
    packet["names_to_decide"] = [
        {"docs": f["docs_row"]["field"], "editor": f["editor_name"], "fortran": f["fortran_name"],
         "line": f["docs_row"]["line"]}
        for f in fields
        if live and f["docs_row"] and f["editor_name"]
        and f["docs_row"]["field"].lower() != f["editor_name"].lower()
        and (f["docs_row"]["line"], f["docs_row"]["field"]) not in renamed]
    packet["exact_text"] = (_exact_text(fields, packet["docs_rows"], columns,
                                        entry["table_page"], docs_root, packet["example_headers"])
                            if live else [])
    return packet


def render_packet(packet: dict) -> str:
    p = packet
    out = [f"# Packet: {p['file']} (SWAT+ {p['swatplus_version']} @ {str(p['source_commit'])[:12]}, "
           f"docs @ {str(p['docs_commit'])[:12]})", "", f"Status: **{p['status']}**"]
    if "table_page" not in p:
        return "\n".join(out + ["", p.get("note", "")]) + "\n"
    out.append(f"Docs table: `{p['table_page']}`")
    if p.get("malformed_lines"):
        out.append("**The table is broken at line(s) " + ", ".join(map(str, p["malformed_lines"]))
                   + "**: each row must be one line with the header's number of cells. Fix these first.")
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
    if p.get("moves"):
        out += ["", "## Row moves (do these first, in this order)", ""]
        for m in p["moves"]:
            where = "after" if m["after"] else "before"
            other, other_line = (m["after"], m["after_line"]) if m["after"] else (m["before"], m["before_line"])
            if m.get("anchor"):
                out += [f"- Move the `{m['field']}` row: cut it, from this exact text through its `</tr>`,", "",
                        "  ```html", f"  {m['anchor']}", "  ```", "",
                        f"  and paste it directly {where} the `{other}` row"
                        + (" (after its `</tr>`)" if where == "after" else "") + ", which starts with:", "",
                        "  ```html", f"  {m['to_anchor']}", "  ```", ""]
            else:
                out.append(f"- Move the `{m['field']}` row (line {m['line']}) to directly {where} "
                           f"the `{other}` row (line {other_line}).")
    if p.get("row_edits"):
        out += ["", "## Row edits (exact; do these after the moves)", ""]
        for e in p["row_edits"]:
            changes = ([f"rename it to `{e['rename_to']}` (the Editor column)"] if e.get("rename_to") else []) \
                + ([f"set its type to `{e['to']}`"] if e.get("to") else [])
            what = (f"Delete the `{e['field']}` row (the source does not read it)" if e["action"] == "delete"
                    else f"`{e['field']}` row: " + " and ".join(changes))
            if e.get("anchor"):
                out += [f"- {what}: " + ("delete" if e["action"] == "delete" else "replace")
                        + " the whole row, from this exact text through its `</tr>`:", "",
                        "  ```html", f"  {e['anchor']}", "  ```", ""]
            else:
                out += [f"- {what}: " + ("delete" if e["action"] == "delete" else "replace")
                        + f" this exact line (line {e['line']}):", "",
                        "  ```markdown", f"  {e['raw'].strip()}", "  ```", ""]
            if e["action"] != "delete":
                out += ["  with:", "", "  ```" + ("html" if e.get("anchor") else "markdown"),
                        f"  {e['row'].strip()}", "  ```", ""]
            if e.get("summary_rename"):
                out.append(f"  In `io-docs/SUMMARY.md`, change `{e['summary_rename']['from'].strip()}` "
                           f"to `{e['summary_rename']['to'].strip()}`.")
            if e.get("heading"):
                out.append(f"  In `{e['heading']['page']}`, change the heading `{e['heading']['from']}` "
                           f"to `{e['heading']['to']}` (the file keeps its name).")
            if e.get("summary_rename") or e.get("heading"):
                out.append("")
            if e.get("summary_line"):
                out.append(f"  Also delete `io-docs/SUMMARY.md` line {e['summary_line']} (`{e['summary_text']}`).")
            if e.get("remove_page"):
                out.append(f"  Then remove its page: `git -C <docs checkout> rm {e['remove_page']}`.")
            if e.get("summary_line") or e.get("remove_page"):
                out.append("")
    if p.get("names_to_decide"):
        out += ["", "## Names left for a person (not renamed)", "",
                "These rows' names differ from the Editor column, but not as a spelling variant: the docs "
                "may list the columns in another order, or the field may have changed meaning. A person "
                "decides, and rewrites the description if the meaning changed.", ""]
        out += [f"- line {n['line']}: docs `{n['docs']}`, Editor column `{n['editor']}` "
                f"(Fortran `{n['fortran']}`)" for n in p["names_to_decide"]]
    if p.get("exact_text"):
        out += ["", "## Exact text for each missing row (copy it as is; do not reformat or reword)", ""]
        for x in p["exact_text"]:
            out += [f"### `{x['field']}` (source field #{x['position']})", "",
                    f"Named `{x['name']}` after {x['named_after']}.", "",
                    f"1. Table `{p['table_page']}`: {x['table']}:", ""]
            if x.get("table_anchor"):
                out += ["   ```html", f"   {x['table_anchor']}", "   ```", "", "   with:" if
                        x["table"].startswith("replace") else "   the new row:", ""]
            out += ["   ```markdown", f"   {x['row']}", "   ```", "",
                    f"2. Field page: {x['page_action']}:", "", "   ```markdown"]
            out += [f"   {line}" if line else "" for line in x["page_text"].splitlines()]
            out += ["   ```", "", f"3. `io-docs/SUMMARY.md` (CRLF line endings): {x['summary']}:", "",
                    "   ```markdown", f"   {x['summary_line']}", "   ```", ""]
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


class ApplyError(RuntimeError):
    """The packet's edits do not fit the docs as they are now; nothing was written."""


def _read_text(path: Path) -> tuple[str, str]:
    """``(text with \\n line ends, the file's own line end)``."""
    data = path.read_bytes().decode("utf-8")
    return data.replace("\r\n", "\n"), "\r\n" if "\r\n" in data else "\n"


def _one(items: list[str], wanted: str, what: str) -> int:
    found = [k for k, s in enumerate(items) if s == wanted]
    if len(found) != 1:
        raise ApplyError(f"{what}: expected exactly one line {wanted.strip()!r}, found {len(found)}")
    return found[0]


def _row_span(text: str, anchor: str, what: str) -> tuple[int, int]:
    """Start of the HTML row beginning with ``anchor`` and the end of its ``</tr>``."""
    if text.count(anchor) != 1:
        raise ApplyError(f"{what}: expected exactly one {anchor!r}, found {text.count(anchor)}")
    start = text.index(anchor)
    return start, text.index("</tr>", start) + len("</tr>")


def apply_packet(packet: dict, docs_root: Path) -> list[str]:
    """Write the packet's row moves, row edits, and missing rows into the docs.

    Every edit is resolved in memory against the exact text the packet quotes
    before anything is written, so a packet that no longer fits the files
    raises `ApplyError` and changes nothing. Line endings are kept. Field
    pages are renamed with ``git mv`` and removed with ``git rm``.
    """
    import subprocess

    if "table_page" not in packet:
        return [f"nothing to apply: {packet['file']} is {packet.get('status')}"]
    if not packet["reader"]["called_from"]:
        return [f"nothing to apply: the reader of {packet['file']} never runs"]
    if not (packet["moves"] or packet["row_edits"] or packet["exact_text"]):
        held = "".join(f"; name left for a person: {n['docs']} (Editor column {n['editor']})"
                       for n in packet.get("names_to_decide", []))
        return [f"nothing to apply: {packet['file']} is {packet.get('status')}{held}"]
    if packet.get("malformed_lines"):
        raise ApplyError("the table is broken at line(s) "
                         + ", ".join(map(str, packet["malformed_lines"])) + "; restore it first")
    dirty = subprocess.run(["git", "-C", str(docs_root), "status", "--porcelain", "--", "io-docs"],
                           capture_output=True, text=True, check=False).stdout.strip()
    if dirty:
        raise ApplyError("uncommitted changes under io-docs; commit or discard them first:\n" + dirty)

    io = docs_root / "io-docs"
    page_path = docs_root / packet["table_page"]
    text, page_nl = _read_text(page_path)
    summary_path = io / "SUMMARY.md"
    summary_text, summary_nl = _read_text(summary_path)
    summary = summary_text.split("\n")
    raw_at = {d["line"]: d["raw"] for d in packet["docs_rows"]}
    done: list[str] = []

    for m in packet["moves"]:
        other = m["after"] or m["before"]
        if m.get("anchor"):
            start, end = _row_span(text, m["anchor"], f"move {m['field']}")
            row, text = text[start:end], text[:start] + text[end:]
            t_start, t_end = _row_span(text, m["to_anchor"], f"move {m['field']} next to {other}")
            at = t_end if m["after"] else t_start
            text = text[:at] + row + text[at:]
        else:
            lines = text.split("\n")
            row = lines.pop(_one(lines, raw_at[m["line"]], f"move {m['field']}"))
            k = _one(lines, raw_at[m["after_line"] or m["before_line"]], f"move {m['field']} next to {other}")
            lines.insert(k + 1 if m["after"] else k, row)
            text = "\n".join(lines)
        done.append(f"moved the {m['field']} row {'after' if m['after'] else 'before'} the {other} row")

    removals, renames, pages, headings = [], [], [], []
    for e in packet["row_edits"]:
        new = e.get("row", "")
        if e.get("anchor"):
            start, end = _row_span(text, e["anchor"], f"{e['action']} {e['field']}")
            text = text[:start] + new + text[end:]
        else:
            lines = text.split("\n")
            k = _one(lines, e["raw"], f"{e['action']} {e['field']}")
            lines[k:k + 1] = [] if e["action"] == "delete" else [new]
            text = "\n".join(lines)
        if e.get("summary_line"):
            del summary[_one([s.strip() for s in summary], e["summary_text"], f"SUMMARY.md entry of {e['field']}")]
        if e.get("summary_rename"):
            k = _one(summary, e["summary_rename"]["from"], f"SUMMARY.md entry of {e['field']}")
            summary[k] = e["summary_rename"]["to"]
        if e.get("heading"):
            path = docs_root / e["heading"]["page"]
            page_text, nl = _read_text(path)
            lines = page_text.split("\n")
            lines[_one(lines, e["heading"]["from"], f"heading of {e['heading']['page']}")] = e["heading"]["to"]
            headings.append((path, "\n".join(lines).replace("\n", nl)))
        if e.get("remove_page"):
            removals.append(e["remove_page"])
        if e["action"] == "delete":
            done.append(f"deleted the {e['field']} row")
        else:
            parts = ([f"renamed the {e['field']} row to {e['rename_to']} (the Editor column)"]
                     if e.get("rename_to") else [f"set the {e['field']} row's type to {e['to']}"])
            if e.get("rename_to") and e.get("to"):
                parts.append(f"set its type to {e['to']}")
            done.append(" and ".join(parts))

    last_row = last_summary = None
    for x in packet["exact_text"]:
        mode, row = x.get("table_mode"), x["row"]
        if mode is None:
            raise ApplyError(f"no place for the {x['name']} row; edit it by hand")
        if x.get("table_anchor") or (mode == "after_new" and row.startswith("<tr")):
            if mode == "after_new":
                at = text.index(last_row) + len(last_row)
            elif mode == "before":
                if text.count(x["table_anchor"]) != 1:
                    raise ApplyError(f"insert {x['name']}: anchor {x['table_anchor']!r} is not unique")
                at = text.index(x["table_anchor"])
            else:
                start, end = _row_span(text, x["table_anchor"], f"place {x['name']}")
                if mode == "replace":
                    text = text[:start] + text[end:]
                    at = start
                else:  # after_row_end
                    at = end
            text = text[:at] + row + text[at:]
        else:
            lines = text.split("\n")
            if mode == "after_new":
                k = _one(lines, last_row, f"place {x['name']}") + 1
            else:
                k = _one(lines, x["table_raw"], f"place {x['name']}")
                if mode == "replace":
                    del lines[k]
                elif mode == "after":
                    k += 1
            lines.insert(k, row)
            text = "\n".join(lines)
        last_row = row

        smode = x.get("summary_mode")
        if smode == "after_new":
            k = _one(summary, last_summary, f"SUMMARY.md entry of {x['name']}") + 1
        elif smode in ("after", "replace"):
            k = _one(summary, x["summary_ref"], f"SUMMARY.md entry of {x['name']}")
            if smode == "replace":
                del summary[k]
            else:
                k += 1
        else:
            raise ApplyError(f"no SUMMARY.md entry for the {packet['file']} table; add it by hand first")
        summary.insert(k, x["summary_line"])
        last_summary = x["summary_line"]

        target = io / x["page"]
        if x.get("page_from"):
            renames.append((x["page_from"], f"io-docs/{x['page']}"))
        elif target.exists():
            raise ApplyError(f"io-docs/{x['page']} already exists but no row links to it; "
                             "link or remove it by hand, then apply again")
        pages.append((target, x["page_text"]))
        done.append(f"{'replaced' if mode == 'replace' else 'added'} the {x['name']} row, "
                    f"its page io-docs/{x['page']}, and its SUMMARY.md entry")

    page_path.write_bytes(text.replace("\n", page_nl).encode("utf-8"))
    summary_path.write_bytes("\n".join(summary).replace("\n", summary_nl).encode("utf-8"))
    git = ["git", "-C", str(docs_root)]
    for old, new in renames:
        subprocess.run(git + ["mv", old, new], check=True, capture_output=True)
    for target, page_text in pages:
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(page_text.replace("\n", page_nl).encode("utf-8"))
    for path, page_text in headings:
        path.write_bytes(page_text.encode("utf-8"))
    for path in removals:
        subprocess.run(git + ["rm", "-q", path], check=True, capture_output=True)
    return done


def _front_matter_ok(path: Path) -> bool:
    text = path.read_text(encoding="utf-8")
    head = re.match(r"\A---\s*\n(.*?)\n---\s*\n", text, re.S)
    return bool(head and re.search(r"^description:", head.group(1), re.M)
                and re.search(r"^# \S", text[head.end():], re.M))


def check_tables(schema: dict, provenance: dict, docs_root: Path, files: list[str],
                 field_map: dict | None = None,
                 headers: dict[str, list[list[str]]] | None = None,
                 new_pages: set[Path] | None = None,
                 source_root: Path | None = None) -> tuple[bool, list[str]]:
    """Whether each table is done: ``(all passed, one line per file and problem)``.

    ``new_pages`` (added or modified field pages) are also held to the
    front-matter rule; existing pages are not. With ``source_root``, a file
    whose reader nothing calls is skipped: its table is left alone.
    """
    cache: dict[Path, list[str]] = {}
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
        reader = (schema["files"].get(f) or {}).get("reader")
        if source_root is not None and reader and not callers(source_root, Path(reader).stem, cache):
            lines.append(f"SKIP {f}: its reader {Path(reader).stem} never runs; leave the table alone")
            continue
        problems = []
        bad = malformed_table_lines((docs_root / e["table_page"]).read_text(encoding="utf-8"))
        if bad:
            problems.append("table broken at line(s) " + ", ".join(map(str, bad))
                            + " (each row must be one line with the header's number of cells)")
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
