"""Audit the GitHub source links emitted into the rendered corpus.

Every rendered page cites the pinned SWAT+ source by commit, path, and line
number. Those citations are built from ``source_link_base`` plus line numbers
the parser reported, so a line-numbering regression silently retargets tens of
thousands of links without failing any other gate. This audit resolves each
emitted URL against the local pinned checkout instead of trusting it.

It deliberately does not request URLs over the network: the pinned checkout is
the same tree GitHub would serve at that commit, and a network check would make
a build gate depend on GitHub availability and rate limits.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path


# Matches the two shapes render.py emits: a single "#L12" anchor and a
# "#L12-L34" span. Both are captured so a reversed or out-of-range span is
# checked, not just the start line.
_LINK_RE = re.compile(r"(?P<path>[^\s()\[\]<>\"']+?)#L(?P<start>\d+)(?:-L(?P<end>\d+))?")


@dataclass(frozen=True)
class LinkFinding:
    """One rendered link that does not resolve against the pinned source."""

    page: str
    url: str
    code: str
    message: str

    def __str__(self) -> str:
        return f"{self.page}: {self.code}: {self.message} ({self.url})"


def _line_count(path: Path, cache: dict[Path, int]) -> int:
    if path not in cache:
        # Count as bytes: the audit only needs line bounds, and decoding the
        # whole pinned tree as text would be both slower and encoding-fragile.
        content = path.read_bytes()
        # A terminal LF (including CRLF) ends the last line; it does not
        # create another one. Empty files have no valid line targets.
        cache[path] = content.count(b"\n") + int(bool(content) and not content.endswith(b"\n"))
    return cache[path]


def audit_source_links(
    render_dir: Path, source_dir: Path, link_base: str
) -> list[LinkFinding]:
    """Check every emitted source link against the pinned checkout.

    Verifies the commit segment matches ``link_base``, the cited file exists in
    the local source tree, and the cited lines are within that file.
    """

    findings: list[LinkFinding] = []
    lines_cache: dict[Path, int] = {}
    prefix = link_base.rstrip("/") + "/"
    # Anything pointing at the configured repository but not at the pinned
    # commit is a wrong-commit link, which is the failure a plain existence
    # check would miss entirely.
    repo_root = prefix.split("/blob/", 1)[0] + "/blob/" if "/blob/" in prefix else None

    for page_path in sorted(render_dir.rglob("*.md")):
        page = page_path.relative_to(render_dir).as_posix()
        text = page_path.read_text(encoding="utf-8")
        for match in _LINK_RE.finditer(text):
            url = match.group(0)
            if not url.startswith(prefix):
                if repo_root and url.startswith(repo_root):
                    findings.append(
                        LinkFinding(page, url, "wrong-commit", "link is not on the pinned commit")
                    )
                continue
            relative = match.group("path")[len(prefix):]
            target = source_dir / relative
            if not target.is_file():
                findings.append(
                    LinkFinding(page, url, "missing-file", f"{relative} is not in the pinned source")
                )
                continue
            start = int(match.group("start"))
            end = int(match.group("end") or start)
            total = _line_count(target, lines_cache)
            if start < 1 or end < start or end > total:
                findings.append(
                    LinkFinding(
                        page,
                        url,
                        "out-of-range",
                        f"lines {start}-{end} outside {relative} (1-{total})",
                    )
                )
    return findings


def count_source_links(render_dir: Path, link_base: str) -> int:
    """Count emitted links so the audit can report the size of what it checked."""

    prefix = link_base.rstrip("/") + "/"
    return sum(
        1
        for page_path in render_dir.rglob("*.md")
        for match in _LINK_RE.finditer(page_path.read_text(encoding="utf-8"))
        if match.group(0).startswith(prefix)
    )
