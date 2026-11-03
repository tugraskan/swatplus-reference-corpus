"""Ask Tamandua 0.5.0 about one SWAT+ source from the command line.

Usage (from the corpus root, with the Tamandua 0.5 venv's python):
  .swatref/tamandua-0.5/venv/Scripts/python.exe agent_eval/tools/ask.py --list
  .swatref/tamandua-0.5/venv/Scripts/python.exe agent_eval/tools/ask.py uses variable=bmp_sed
  .swatref/tamandua-0.5/venv/Scripts/python.exe agent_eval/tools/ask.py callers procedure=lsu_read_elements -- writers variable=sedyld
  .swatref/tamandua-0.5/venv/Scripts/python.exe agent_eval/tools/ask.py --source release_62_0_0 provenance -- file_io file=hydrology.hyd

Options, before the first tool:
  --source NAME   a source named in swatref.toml (default release_62_0_1, SWAT+ 62.0.1)
  --facts FILE    a Tamandua facts file to use instead of the source's own

Several queries separated by `--` share one server process. Output is Tamandua's compact text, after a first line
naming the source the facts were built from. Run `provenance` to see the facts' source commit.
"""
import sys
from pathlib import Path

from tamandua.mcp.client import McpStdioClient

import swat_source

SERVER = swat_source.TAM / "venv" / "Scripts" / "swatplus-mcp.exe"


def queries(argv):
    current = []
    for arg in argv + ["--"]:
        if arg == "--":
            if current:
                yield current[0], dict(a.split("=", 1) for a in current[1:])
            current = []
        else:
            current.append(arg)


def main(argv):
    source_name, facts = None, None
    while argv and argv[0] in ("--source", "--facts"):
        if len(argv) < 2:
            print(__doc__)
            return 2
        if argv[0] == "--source":
            source_name = argv[1]
        else:
            facts = Path(argv[1])
        argv = argv[2:]
    if not argv:
        print(__doc__)
        return 2
    source = swat_source.resolve(source_name)
    if facts is None:
        swat_source.require_facts(source)
        facts = source.facts
    sys.stdout.reconfigure(encoding="utf-8")
    print(f"# Tamandua facts: {source.label if facts == source.facts else facts} ({facts.as_posix()})")
    with McpStdioClient([str(SERVER), "--facts", str(facts), "--compact"], timeout=180) as client:
        if argv == ["--list"]:
            for t in client.list_tools():
                props = list((t.get("inputSchema") or {}).get("properties", {}))
                print(f"{t['name']}({', '.join(props)}): {t.get('description', '').strip()[:160]}")
            return 0
        for tool, args in queries(argv):
            res = client.call_tool(tool, args)
            print(f"### {tool} {args}{'  [ERROR]' if res.is_error else ''}")
            print(res.text.strip())
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
