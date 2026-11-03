"""All the code evidence for one SWAT+ input file's fields, in one call (Tamandua 0.5.0).

Usage (from the corpus root, with the Tamandua 0.5 venv's python):
  .swatref/tamandua-0.5/venv/Scripts/python.exe agent_eval/tools/field_evidence.py bmpuser.str
  .swatref/tamandua-0.5/venv/Scripts/python.exe agent_eval/tools/field_evidence.py bmpuser.str --source release_62_0_0

`--source NAME` is a source named in swatref.toml (default release_62_0_1, SWAT+ 62.0.1); the first line of the
output names the version the evidence comes from.

For the file's reader and record, then for every field:
  - declaration, unit and comment;
  - every place the value is read (`uses`): calculation, condition, call argument, output, or copy;
  - everything in the code that sets the value itself after the file is read (`writers`), e.g. an input that is
    overwritten with a constant before its only use;
  - next to each statement, the source comment lines directly above it and a comment at the end of its line
    (they often give the units of a formula, e.g. `t=ppm*ha*mm*10/100,000`, but can be outdated);
  - for each copy, where the copy is read and everything that sets it (`writers`), so values the code
    overwrites (e.g. forced to a constant) are visible;
  - if the value itself is never read: other variables with the same field name, with their uses and writers;
  - the example input file's header name and first value at that position.
It reports facts only; drawing conclusions is the reader's job.
"""
from __future__ import annotations

import argparse
import ast
import re
import sys

from tamandua.mcp.client import McpStdioClient

import swat_source
from swat_source import CORPUS, TAM

SOURCE = swat_source.resolve()  # main() switches to the --source given
REFDATA = SOURCE.refdata
SRC = SOURCE.src
MAX_ROWS = 8          # uses rows shown per path
MAX_SAME_NAME = 5     # other same-named paths shown for an unread field
MAX_COMMENTS = 2      # comment lines shown from directly above a statement


def table(text: str, declarations: bool = False) -> list[dict]:
    """Rows of a Tamandua pipe table, one per line. With ``declarations`` (describe_type), a row's comment can
    span lines and contain `|` itself (old SWAT comments: `!!none |0-1 |percolation coefficient`), so a row ends
    at its declaration line (the one with `::`) and extra `|` cells are joined back into the comment."""
    lines = [l for l in text.strip().splitlines() if not l.startswith("###")]
    if not lines or "|" not in lines[0] or "=" in lines[0].split("|")[0]:
        return []
    head = lines[0].split("|")
    if not declarations:
        return [dict(zip(head, l.split("|", len(head) - 1))) for l in lines[1:] if "|" in l]
    rows, buf, n = [], "", len(head)
    for l in lines[1:]:
        buf = f"{buf}\n{l}" if buf else l
        if "::" in l:
            parts = buf.split("|")
            if len(parts) > n:
                parts = parts[:n - 2] + ["|".join(parts[n - 2:-1]), parts[-1]]
            rows.append(dict(zip(head, parts)))
            buf = ""
    return rows


def writers(client, path: str) -> list[dict]:
    text = client.call_tool("writers", {"variable": path}).text
    return [ast.literal_eval(m) for m in re.findall(r"\{'at':.*?\}(?=,\{|$)", text.strip(), re.S)]


def uses(client, path: str) -> list[dict]:
    return table(client.call_tool("uses", {"variable": path}).text)


_source: dict[str, list[str]] = {}


def source_lines(name: str) -> list[str]:
    """Lines of a SWAT+ source file named as Tamandua names it (`swr_latsed.f90`, or `ero_cfactor` in writers)."""
    if name not in _source:
        _source[name] = []
        for candidate in (name, f"{name}.f90", f"{name}.f90.in"):
            path = SRC / candidate
            if path.is_file():
                _source[name] = path.read_text(encoding="utf-8", errors="replace").splitlines()
                break
    return _source[name]


def end_comment(line: str) -> str:
    """The `! ...` comment at the end of a Fortran line ("!" inside a string does not count)."""
    quote = ""
    for i, ch in enumerate(line):
        if quote:
            quote = "" if ch == quote else quote
        elif ch in "'\"":
            quote = ch
        elif ch == "!":
            return line[i:].strip()
    return ""


def comments_at(at: str) -> list[str]:
    """Source comments next to the statement at `file:line`: up to MAX_COMMENTS comment lines directly above it,
    then a comment at the end of the line itself. They often state the units of a formula, but can be outdated."""
    m = re.match(r"\s*([\w.]+?):(\d+)", at or "")
    if not m:
        return []
    lines, n = source_lines(m.group(1)), int(m.group(2))
    if not 0 < n <= len(lines):
        return []
    above, i = [], n - 2
    while i >= 0 and len(above) < MAX_COMMENTS and lines[i].lstrip().startswith("!"):
        above.insert(0, lines[i].strip())
        i -= 1
    found = above + [c for c in [end_comment(lines[n - 1])] if c]
    return [c for c in found if len(re.findall(r"[A-Za-z0-9]", c)) >= 3]


def with_comments(line: str, at: str, indent: str, seen: set[str]) -> list[str]:
    out = [line]
    for c in comments_at(at):
        if c not in seen:
            seen.add(c)
            out.append(f"{indent}    comment: `{c[:200]}`")
    return out


def fmt_uses(rows: list[dict], indent: str = "    ") -> list[str]:
    if not rows:
        return [f"{indent}(never read)"]
    out: list[str] = []
    seen: set[str] = set()
    for r in rows[:MAX_ROWS]:
        out += with_comments(f"{indent}- {r.get('kind')} at {r.get('at')}: `{r.get('statement', '').strip()[:160]}`",
                             r.get("at", ""), indent, seen)
    if len(rows) > MAX_ROWS:
        out.append(f"{indent}- ... {len(rows) - MAX_ROWS} more")
    return out


def fmt_writers(found: list[dict], indent: str) -> list[str]:
    out: list[str] = []
    seen: set[str] = set()
    for x in found:
        out += with_comments(f"{indent}- {x['at']}: `{x['expression'][:160]}`", x["at"], indent, seen)
    return out


def example(file: str) -> tuple[list[str], list[str], str]:
    for path in sorted(REFDATA.glob(f"*/{file}")):
        lines = path.read_text(encoding="utf-8", errors="replace").splitlines()
        if len(lines) >= 3:
            return lines[1].split(), lines[2].split(), str(path.relative_to(CORPUS)).replace("\\", "/")
    return [], [], ""


def main(file: str, source_name: str | None = None) -> int:
    global SOURCE, REFDATA, SRC
    SOURCE = swat_source.resolve(source_name)
    REFDATA, SRC = SOURCE.refdata, SOURCE.src
    swat_source.require_facts(SOURCE)
    sys.stdout.reconfigure(encoding="utf-8")
    server = TAM / "venv" / "Scripts" / "swatplus-mcp.exe"
    with McpStdioClient([str(server), "--facts", str(SOURCE.facts), "--compact"], timeout=180) as client:
        io = table(client.call_tool("file_io", {"file": file}).text)
        reads = [r for r in io if r.get("op") == "read" and r.get("fields") not in ("titldum", "header", "none")]
        if not reads:
            print(f"# Evidence for {file}\n\nNo record read found (file_io):\n")
            print("\n".join(f"- {r}" for r in io))
            return 1
        print(f"# Evidence for {file} ({SOURCE.label}, Tamandua 0.5.0)\n")
        for r in reads:
            print(f"- read at `{r['procedure']}` line {r['line']}: `{r['fields']}`")
        # record fields: a whole derived-type record, or listed components
        fields: list[tuple[str, dict]] = []
        for r in reads:
            for item in [x.strip() for x in r["fields"].split(",")]:
                base = re.sub(r"\(.*?\)", "", item)
                if "%" in base:
                    fields.append((base, {}))
                    continue
                mv = client.call_tool("module_variable", {"name": base}).text
                m = re.search(r"type=type \((\w+)\)", mv)
                if not m:
                    fields.append((base, {}))
                    continue
                print(f"- record `{base}` is type `{m.group(1)}`")
                for row in table(client.call_tool("describe_type", {"name": m.group(1)}).text, declarations=True):
                    fields.append((f"{base}%{row['field']}", row))
        header, values, ex_path = example(file)
        if ex_path:
            print(f"- example file `{ex_path}` (header line 2, first data line 3)")
        print()
        for pos, (path, info) in enumerate(fields):
            comp = path.split("%")[-1]
            unit = info.get("units", "")
            print(f"## {pos + 1}. `{path}`")
            if info:
                print(f"  declared `{info.get('declaration', '').strip()}`; unit `{unit}`; comment: {info.get('means', '')}")
            if pos < len(header):
                print(f"  example file: header `{header[pos]}`, value `{values[pos] if pos < len(values) else ''}`")
            rows = uses(client, path)
            print("  read:")
            print("\n".join(fmt_uses(rows)))
            # an input the code overwrites after reading it (e.g. `bsn_cc%cfac = 1` before its only check)
            own = writers(client, path)
            if own:
                print(f"  ALSO SET BY THE CODE (after the file is read), so the file's value can be replaced:")
                print("\n".join(fmt_writers(own, "    ")))
            else:
                print("  set by the code: never (only the file sets it)")
            for c in [r for r in rows if r.get("kind") == "copy"]:
                target = c.get("detail", "")
                print(f"  copy -> `{target}`; where it is read:")
                print("\n".join(fmt_uses(uses(client, target), "      ")))
                w = writers(client, target)
                print(f"    everything that sets `{target}`:")
                print("\n".join(fmt_writers(w, "      ")) or "      (none)")
            if not rows:
                others = sorted({r["path"] for r in uses(client, comp) if r.get("path") != path})
                if others:
                    print(f"  never read itself; other variables named `{comp}`:")
                    if len(others) > MAX_SAME_NAME:
                        print(f"    ({len(others)} paths; showing {MAX_SAME_NAME})")
                    for other in others[:MAX_SAME_NAME]:
                        print(f"    `{other}` read:")
                        print("\n".join(fmt_uses(uses(client, other), "      ")))
                        w = writers(client, other)
                        print(f"    everything that sets `{other}`:")
                        print("\n".join(fmt_writers(w, "      ")) or "      (none)")
            print()
    return 0


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("file", help="input file name, e.g. bmpuser.str")
    ap.add_argument("--source", help=f"a source in swatref.toml (default {swat_source.DEFAULT_SOURCE})")
    args = ap.parse_args()
    sys.exit(main(args.file, args.source))
