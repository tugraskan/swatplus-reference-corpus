"""ANT's second opinion (review_code, GPT-OSS 120B) on a saved docs proposal, in one call.

Usage (from the corpus root, after the proposal is written):
  .swatref/tamandua-0.5/venv/Scripts/python.exe agent_eval/tools/second_opinion.py bmpuser.str
  .swatref/tamandua-0.5/venv/Scripts/python.exe agent_eval/tools/second_opinion.py bmpuser.str --source release_62_0_0

`--source NAME` is a source in swatref.toml (default release_62_0_1, SWAT+ 62.0.1): the evidence and the reviewer's
instructions are for that version.

Reads .swatref/hermes-proposals/FILE.md, collects the code evidence (field_evidence.py FILE), sends both to
ANT review_code through the local-agent-router launcher (~/.claude/ant-mcp.cmd, which supplies the API key),
prints the verdict and the review, and saves the review to .swatref/hermes-proposals/FILE.review.md.
It exists so the agent never has to pack a long proposal into a tool call's JSON arguments.
Exit codes: 0 reviewed; 1 the review call failed (the error is printed); 2 no proposal file yet.
"""
from __future__ import annotations

import argparse
import json
import queue
import re
import subprocess
import sys
import threading
from pathlib import Path

import swat_source
from swat_source import CORPUS, TAM

PROPOSALS = CORPUS / ".swatref" / "hermes-proposals"
TAM_PYTHON = TAM / "venv" / "Scripts" / "python.exe"
LAUNCHER = Path.home() / ".claude" / "ant-mcp.cmd"
TIMEOUT = 900  # seconds; GPT-OSS reasons at length before answering

CONTEXT = """This is a proposed change to the {label} user documentation for the input file {file}
(descriptions, units and ranges of the input table, plus field-page text). It is documentation only: changing the
Fortran code is out of scope. Check each proposed statement against the code evidence below, which was collected
from the {version} source with Tamandua (`read` lists every place a value is used; `(never read)` means the input has
no effect; `comment:` lines are the source comments next to a statement). Judge units by working through each
formula's arithmetic (conversion factors only fit one unit). A declaration comment can be outdated: do not ask
for a unit change only because a declaration comment says so. Say which proposed statements are wrong or
unsupported by the evidence, and why, showing the arithmetic for any unit you dispute.

{evidence}"""


class Mcp:
    """Just enough MCP over stdio for one tools/call (UTF-8, launcher logs discarded)."""

    def __init__(self, command: list[str]) -> None:
        self.proc = subprocess.Popen(command, stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                                     stderr=subprocess.DEVNULL, text=True, encoding="utf-8", errors="replace")
        self.lines: queue.Queue[str] = queue.Queue()
        threading.Thread(target=self._pump, daemon=True).start()
        self.next_id = 1

    def _pump(self) -> None:
        for line in self.proc.stdout:
            self.lines.put(line)
        self.lines.put("")

    def request(self, method: str, params: dict, timeout: float = 120) -> dict:
        rid, self.next_id = self.next_id, self.next_id + 1
        self._send({"jsonrpc": "2.0", "id": rid, "method": method, "params": params})
        while True:
            try:
                line = self.lines.get(timeout=timeout)
            except queue.Empty:
                raise RuntimeError(f"{method}: no answer within {timeout:.0f}s") from None
            if line == "":
                raise RuntimeError(f"{method}: the router connection closed before answering")
            try:
                msg = json.loads(line)
            except json.JSONDecodeError:
                continue
            if msg.get("id") == rid:
                if "error" in msg:
                    raise RuntimeError(f"{method}: {msg['error'].get('message', msg['error'])}")
                return msg.get("result", {})

    def notify(self, method: str) -> None:
        self._send({"jsonrpc": "2.0", "method": method, "params": {}})

    def _send(self, msg: dict) -> None:
        self.proc.stdin.write(json.dumps(msg) + "\n")
        self.proc.stdin.flush()

    def close(self) -> None:
        try:
            self.proc.stdin.close()
            self.proc.wait(timeout=5)
        except Exception:
            self.proc.kill()


def verdict(review: str) -> str:
    m = re.search(r"\b(REQUEST[_ ]CHANGES|APPROVE[D]?|COMMENT|REJECT(?:ED)?)\b", review, re.I)
    return m.group(1).upper().replace(" ", "_") if m else "no verdict word found (read the review)"


def main(file: str, source_name: str | None = None) -> int:
    sys.stdout.reconfigure(encoding="utf-8")
    source = swat_source.resolve(source_name)
    proposal_path = PROPOSALS / f"{file}.md"
    if not proposal_path.exists():
        print(f"No proposal at .swatref/hermes-proposals/{file}.md: write it first (Step 5), then run this again.")
        return 2
    proposal = proposal_path.read_text(encoding="utf-8", errors="replace")
    ev = subprocess.run([str(TAM_PYTHON), str(CORPUS / "agent_eval" / "tools" / "field_evidence.py"), file,
                         "--source", source.name],
                        capture_output=True, text=True, encoding="utf-8", errors="replace", cwd=CORPUS)
    evidence = ev.stdout if ev.returncode == 0 else f"(field_evidence.py failed: {ev.stdout[-500:]}{ev.stderr[-500:]})"

    client = Mcp(["cmd", "/c", str(LAUNCHER)])
    try:
        client.request("initialize", {"protocolVersion": "2024-11-05", "capabilities": {},
                                      "clientInfo": {"name": "swat-docs-second-opinion", "version": "1"}})
        client.notify("notifications/initialized")
        result = client.request("tools/call", {"name": "review_code", "arguments": {
            "content_to_review": proposal, "context": CONTEXT.format(
                file=file, evidence=evidence, label=source.label, version=source.version)}},
            timeout=TIMEOUT)
    except Exception as e:  # noqa: BLE001 - report any failure as the tool's answer
        print(f"review_code FAILED: {e}")
        print("Quote this error in the report; do not retry more than once.")
        return 1
    finally:
        client.close()
    review = "\n".join(c.get("text", "") for c in result.get("content") or [] if c.get("type") == "text").strip()
    if result.get("isError") or not review:
        print(f"review_code FAILED: {review or 'empty answer'}")
        print("Quote this error in the report; do not retry more than once.")
        return 1
    reviewer = "review_code"
    try:  # the router wraps the answer: {"model": ..., "content": "<review text>", ...}
        wrapped = json.loads(review)
        if isinstance(wrapped, dict) and wrapped.get("content"):
            reviewer = f"review_code ({wrapped.get('model', '?')})"
            review = str(wrapped["content"]).strip()
    except json.JSONDecodeError:
        pass
    v = verdict(review)
    out = PROPOSALS / f"{file}.review.md"
    out.write_text(f"# ANT {reviewer} on {file}.md\n\nVerdict: {v}\n\n{review}\n", encoding="utf-8")
    print(f"Reviewer: ANT {reviewer}")
    print(f"Verdict: {v}")
    print(f"(saved to .swatref/hermes-proposals/{file}.review.md)\n")
    print(review)
    return 0


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("file", help="input file name, e.g. bmpuser.str")
    ap.add_argument("--source", help=f"a source in swatref.toml (default {swat_source.DEFAULT_SOURCE})")
    args = ap.parse_args()
    sys.exit(main(args.file, args.source))
