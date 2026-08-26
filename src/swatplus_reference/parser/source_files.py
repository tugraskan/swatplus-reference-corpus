"""Portable source-file discovery for clean and previously built checkouts."""

from __future__ import annotations

import subprocess
from pathlib import Path
from typing import Iterable


def _git_tracked_files(source_root: Path) -> list[Path] | None:
    """Return tracked files below source_root, or None outside a useful checkout."""
    try:
        top = subprocess.run(
            ["git", "-C", str(source_root), "rev-parse", "--show-toplevel"],
            check=False,
            capture_output=True,
            text=True,
        )
    except OSError:
        return None
    if top.returncode != 0 or not top.stdout.strip():
        return None

    git_root = Path(top.stdout.strip()).resolve()
    try:
        prefix = source_root.resolve().relative_to(git_root).as_posix()
    except ValueError:
        return None
    target = prefix if prefix != "." else "."
    listed = subprocess.run(
        ["git", "-C", str(git_root), "ls-files", "-z", "--", target],
        check=False,
        capture_output=True,
    )
    if listed.returncode != 0:
        return None
    paths = [
        git_root / value.decode("utf-8", errors="surrogateescape")
        for value in listed.stdout.split(b"\0")
        if value
    ]
    # Temporary test/source directories can live inside a larger repository
    # while containing no tracked files of their own. Preserve filesystem
    # discovery for those standalone inputs.
    return paths or None


def source_files(source_root: Path, suffixes: Iterable[str]) -> list[Path]:
    """List exact-suffix source files in stable POSIX-relative order.

    A Git checkout is defined by its tracked tree, so ignored CMake products
    cannot silently enter a later scan. Non-Git fixture directories fall back
    to ordinary recursive discovery.
    """
    source_root = source_root.resolve()
    normalized = {
        suffix.lower() if suffix.startswith(".") else f".{suffix.lower()}"
        for suffix in suffixes
    }
    candidates = _git_tracked_files(source_root)
    if candidates is None:
        candidates = [path for path in source_root.rglob("*") if path.is_file()]
    selected = [
        path
        for path in candidates
        if path.is_file() and path.suffix.lower() in normalized
    ]
    return sorted(
        selected, key=lambda path: path.relative_to(source_root).as_posix()
    )
