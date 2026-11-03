"""A second opinion on a saved docs proposal, in one call: GPT-OSS 120B on ANT, Codex or Claude.

Usage (from the corpus root, after the proposal is written):
  .swatref/tamandua-0.5/venv/Scripts/python.exe agent_eval/tools/second_opinion.py bmpuser.str
  .swatref/tamandua-0.5/venv/Scripts/python.exe agent_eval/tools/second_opinion.py bmpuser.str --reviewer codex
  .swatref/tamandua-0.5/venv/Scripts/python.exe agent_eval/tools/second_opinion.py bmpuser.str --source release_62_0_0

The reviewer is `primary` in agent_eval/reviewer.toml unless `--reviewer` names one:
  gpt-oss  ANT review_code through the local-agent-router launcher (~/.claude/ant-mcp.cmd, which supplies the API key)
  codex    `codex exec`, read-only sandbox, memories, sub-agents and plugins off (uses the user's Codex quota)
  claude   `claude -p --safe-mode` with no tools and no MCP servers (uses the user's Claude quota)
Codex and Claude run in an empty temporary folder, so no project instructions (AGENTS.md, CLAUDE.md) reach them;
--safe-mode also keeps the user's global ~/.claude/CLAUDE.md, skills and plugins out of the Claude review.

Reads .swatref/hermes-proposals/FILE.md (or --proposal), collects the code evidence (field_evidence.py FILE), sends
both to the reviewer, prints the verdict and the review, and saves the review to .swatref/hermes-proposals/
FILE.review.md (or --out). `--source NAME` is a source in swatref.toml (default release_62_0_1, SWAT+ 62.0.1): the
evidence and the reviewer's instructions are for that version. `--dry-run` prints what would be sent, and to whom,
without calling the reviewer. It exists so the agent never has to pack a long proposal into a tool call's arguments.
Exit codes: 0 reviewed; 1 the review call failed (the error is printed); 2 no proposal file yet.
"""
from __future__ import annotations

import argparse
import json
import os
import queue
import re
import shutil
import subprocess
import sys
import tempfile
import threading
import tomllib
from pathlib import Path

import swat_source
from swat_source import CORPUS, TAM

PROPOSALS = CORPUS / ".swatref" / "hermes-proposals"
TAM_PYTHON = TAM / "venv" / "Scripts" / "python.exe"
LAUNCHER = Path.home() / ".claude" / "ant-mcp.cmd"
CONFIG = CORPUS / "agent_eval" / "reviewer.toml"
REVIEWERS = ("gpt-oss", "codex", "claude")
TIMEOUT = 900  # seconds; reviewers reason at length before answering

CONTEXT = """This is a proposed change to the {label} user documentation for the input file {file}
(descriptions, units and ranges of the input table, plus field-page text). It is documentation only: changing the
Fortran code is out of scope. Check each proposed statement against the code evidence below, which was collected
from the {version} source with Tamandua (`read` lists every place a value is used; `(never read)` means the input has
no effect; `comment:` lines are the source comments next to a statement). Judge units by working through each
formula's arithmetic (conversion factors only fit one unit). A declaration comment can be outdated: do not ask
for a unit change only because a declaration comment says so.

The docs' Unit, Default and Range columns are recommended values for users (e.g. from the SWAT+ Editor), not
limits the code enforces. Do not ask to remove or narrow a range or default because the code does not check it.
Do flag the proposal when it changes or removes a documented unit, default or range and the only support is that
the code does not check it, or a declaration comment gives another value; and when it sets a unit to n/a only
because the value is never read.

Check, do not improve: judge only what the proposal changes or adds. Flag a statement only when the evidence
contradicts it or the proposal adds it without support; do not ask for rewording, more detail or style changes,
and leave text the proposal keeps unchanged from the current docs alone unless the evidence contradicts it.
Say which proposed statements are wrong or unsupported by the evidence, and why, showing the arithmetic for any
unit you dispute.

{evidence}"""

# Codex and Claude get the instructions, the evidence and the proposal as one message.
CLI_PROMPT = """You are reviewing a documentation proposal. Do not run commands, open files or use any tools:
everything you need is below.

{context}

## The proposal to review

{proposal}

## Your answer

Start with one verdict word, APPROVE or REQUEST_CHANGES, then your points (for each: the row, what is wrong, and the
evidence). Reply with the review only."""


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


VERDICT = r"REQUEST[\s_-]*CHANGES|APPROVED?|REJECT(?:ED)?"


def verdict(review: str) -> str:
    """The verdict the reviewer states, from its first three lines if it is there, else from anywhere: a word after
    "Verdict:"/"Decision:" first, then the first verdict word written in capitals. Prose such as "before it can be
    approved" never counts. GPT-OSS writes "REQUEST CHANGES" with a narrow no-break space (U+202F) or a
    non-breaking hyphen (U+2011), so Unicode spaces and dashes are folded first."""
    text = re.sub(r"[\u00a0\u2000-\u200b\u202f\u205f\u3000]", " ", review)
    text = re.sub(r"[\u2010-\u2015\u2212]", "-", text)
    head = "\n".join([l for l in text.splitlines() if l.strip()][:3])
    labelled = re.compile(rf"\b(?:verdict|decision)\W{{0,5}}({VERDICT})\b", re.I)
    capitals = re.compile(rf"\b({VERDICT}|COMMENT)\b")
    for where in (head, text):
        m = labelled.search(where) or capitals.search(where)
        if m:
            word = m.group(1).upper()
            return "REQUEST_CHANGES" if word.startswith("REQUEST") else word
    return "no verdict word found (read the review)"


def load_config() -> dict:
    return tomllib.loads(CONFIG.read_text(encoding="utf-8")) if CONFIG.is_file() else {}


def npm_dir() -> Path:
    return Path(os.environ.get("APPDATA", Path.home() / "AppData" / "Roaming")) / "npm"


def claude_command(model: str) -> list[str]:
    exe = npm_dir() / "node_modules" / "@anthropic-ai" / "claude-code" / "bin" / "claude.exe"
    if not exe.is_file():  # the npm wrapper (.cmd) mangles quoted arguments, so prefer the real program
        exe = Path(shutil.which("claude") or "claude")
    # --safe-mode: no CLAUDE.md (the user's global one included), skills, plugins or hooks; sign-in works as usual
    return [str(exe), "-p", "--safe-mode", "--tools", "", "--strict-mcp-config", "--no-session-persistence",
            "--output-format", "text", *(["--model", model] if model else [])]


def codex_command(model: str, out: Path) -> list[str]:
    js = npm_dir() / "node_modules" / "@openai" / "codex" / "bin" / "codex.js"
    node = shutil.which("node")
    base = [node, str(js)] if node and js.is_file() else [shutil.which("codex") or "codex"]
    plugins: list[str] = []
    try:  # every plugin enabled in the user's Codex config is switched off for this run only
        user = tomllib.loads((Path.home() / ".codex" / "config.toml").read_text(encoding="utf-8"))
        for name, cfg in user.get("plugins", {}).items():
            if isinstance(cfg, dict) and cfg.get("enabled"):
                plugins += ["-c", f'plugins."{name}".enabled=false']
    except (OSError, tomllib.TOMLDecodeError):
        pass
    return [*base, "exec", "-s", "read-only", "--skip-git-repo-check", "--disable", "memories",
            "--disable", "multi_agent", *plugins, *(["-m", model] if model else []), "-o", str(out), "-"]


def review_gpt_oss(proposal: str, context: str) -> tuple[str, str]:
    client = Mcp(["cmd", "/c", str(LAUNCHER)])
    try:
        client.request("initialize", {"protocolVersion": "2024-11-05", "capabilities": {},
                                      "clientInfo": {"name": "swat-docs-second-opinion", "version": "1"}})
        client.notify("notifications/initialized")
        result = client.request("tools/call", {"name": "review_code", "arguments": {
            "content_to_review": proposal, "context": context}}, timeout=TIMEOUT)
    finally:
        client.close()
    review = "\n".join(c.get("text", "") for c in result.get("content") or [] if c.get("type") == "text").strip()
    if result.get("isError") or not review:
        raise RuntimeError(review or "empty answer")
    label = "ANT review_code"
    try:  # the router wraps the answer: {"model": ..., "content": "<review text>", ...}
        wrapped = json.loads(review)
        if isinstance(wrapped, dict) and wrapped.get("content"):
            label = f"ANT review_code ({wrapped.get('model', '?')})"
            review = str(wrapped["content"]).strip()
    except json.JSONDecodeError:
        pass
    return label, review


def review_cli(reviewer: str, proposal: str, context: str, model: str) -> tuple[str, str]:
    prompt = CLI_PROMPT.format(context=context, proposal=proposal)
    with tempfile.TemporaryDirectory(prefix="docs-review-") as tmp:  # no project instructions in an empty folder
        out = Path(tmp) / "review.md"
        cmd = claude_command(model) if reviewer == "claude" else codex_command(model, out)
        run = subprocess.run(cmd, input=prompt, capture_output=True, text=True, encoding="utf-8",
                             errors="replace", cwd=tmp, timeout=TIMEOUT)
        review = (out.read_text(encoding="utf-8", errors="replace") if out.is_file() else run.stdout).strip()
    if run.returncode != 0 or not review:
        raise RuntimeError(f"exit {run.returncode}: {(run.stderr or run.stdout or 'empty answer').strip()[-500:]}")
    return f"{reviewer} ({model or 'default model'})", review


def main(file: str, source_name: str | None = None, reviewer: str | None = None, proposal_arg: str | None = None,
         out_arg: str | None = None, dry_run: bool = False) -> int:
    sys.stdout.reconfigure(encoding="utf-8")
    config = load_config()
    reviewer = reviewer or config.get("primary") or "gpt-oss"
    if reviewer not in REVIEWERS:
        print(f"Unknown reviewer {reviewer!r} (from --reviewer or {CONFIG.name}); choose one of {', '.join(REVIEWERS)}.")
        return 2
    model = config.get(f"{reviewer}_model", "") if reviewer != "gpt-oss" else ""
    source = swat_source.resolve(source_name)
    proposal_path = Path(proposal_arg).resolve() if proposal_arg else PROPOSALS / f"{file}.md"
    out = Path(out_arg).resolve() if out_arg else proposal_path.with_name(f"{file}.review.md")
    shown = lambda p: p.relative_to(CORPUS).as_posix() if p.is_relative_to(CORPUS) else str(p)  # noqa: E731
    if not proposal_path.exists():
        print(f"No proposal at {shown(proposal_path)}: write it first (Step 4), then run this again.")
        return 2
    proposal = proposal_path.read_text(encoding="utf-8", errors="replace")
    ev = subprocess.run([str(TAM_PYTHON), str(CORPUS / "agent_eval" / "tools" / "field_evidence.py"), file,
                         "--source", source.name],
                        capture_output=True, text=True, encoding="utf-8", errors="replace", cwd=CORPUS)
    evidence = ev.stdout if ev.returncode == 0 else f"(field_evidence.py failed: {ev.stdout[-500:]}{ev.stderr[-500:]})"
    context = CONTEXT.format(file=file, evidence=evidence, label=source.label, version=source.version)

    if dry_run:
        size = len(context) + len(proposal) + (len(CLI_PROMPT) if reviewer != "gpt-oss" else 0)
        cmd = ("ANT review_code via " + str(LAUNCHER) if reviewer == "gpt-oss" else " ".join(
            a or '""' for a in (claude_command(model) if reviewer == "claude" else codex_command(model, Path("review.md")))))
        print(f"Reviewer: {reviewer}{f' ({model})' if model else ''}\nWould run: {cmd}")
        print(f"Would send {size} characters (about {size // 4} tokens): instructions, the evidence for {file} "
              f"({source.label}) and {shown(proposal_path)}.\nWould save the review to {shown(out)}.")
        return 0
    try:
        label, review = (review_gpt_oss(proposal, context) if reviewer == "gpt-oss"
                         else review_cli(reviewer, proposal, context, model))
    except Exception as e:  # noqa: BLE001 - report any failure as the tool's answer
        print(f"review_code FAILED: {reviewer}: {e}")
        print("Quote this error in the report; do not retry more than once.")
        return 1
    v = verdict(review)
    out.write_text(f"# {label} on {file}.md\n\nVerdict: {v}\n\n{review}\n", encoding="utf-8")
    print(f"Reviewer: {label}")
    print(f"Verdict: {v}")
    print(f"(saved to {shown(out)})\n")
    print(review)
    return 0


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("file", help="input file name, e.g. bmpuser.str")
    ap.add_argument("--source", help=f"a source in swatref.toml (default {swat_source.DEFAULT_SOURCE})")
    ap.add_argument("--reviewer", choices=REVIEWERS, help=f"override `primary` in {CONFIG.relative_to(CORPUS)}")
    ap.add_argument("--proposal", help="proposal to review (default .swatref/hermes-proposals/FILE.md)")
    ap.add_argument("--out", help="where to save the review (default FILE.review.md next to the proposal)")
    ap.add_argument("--dry-run", action="store_true", help="show the reviewer, command and size; call nothing")
    args = ap.parse_args()
    sys.exit(main(args.file, args.source, args.reviewer, args.proposal, args.out, args.dry_run))
