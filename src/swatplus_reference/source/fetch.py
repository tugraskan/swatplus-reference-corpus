"""Fetch and verify named SWAT+ source profiles."""

from __future__ import annotations

import subprocess
from pathlib import Path

from ..provenance.records import SourceProvenance
from .config import Config


def _git(*args: str, cwd: Path | None = None) -> str:
    result = subprocess.run(
        ["git", *args], cwd=cwd, check=False, capture_output=True, text=True
    )
    if result.returncode:
        message = result.stderr.strip() or result.stdout.strip()
        raise RuntimeError(message or f"git {' '.join(args)} failed")
    return result.stdout.strip()


def _normal_remote(value: str) -> str:
    return value.removesuffix(".git").rstrip("/").lower()


def resolve_profile(cfg: Config, name: str | None = None) -> tuple[Path, SourceProvenance]:
    """Return the source directory and verified exact Git commit."""
    profile = cfg.source_profile(name)
    checkout = profile.abs_checkout(cfg.root)
    source_dir = profile.abs_source_dir(cfg.root)
    if not (checkout / ".git").exists():
        raise FileNotFoundError(
            f"source profile {profile.name!r} is not fetched at {checkout}; "
            f"run `swatref source fetch {profile.name}`"
        )
    if not source_dir.exists():
        raise FileNotFoundError(f"source directory does not exist: {source_dir}")
    actual_remote = _git("remote", "get-url", "origin", cwd=checkout)
    if _normal_remote(actual_remote) != _normal_remote(profile.repository):
        raise RuntimeError(
            f"source profile {profile.name!r} uses remote {actual_remote!r}, "
            f"but swatref.toml requires {profile.repository!r}"
        )
    resolved = _git("rev-parse", "HEAD", cwd=checkout)
    if profile.commit and resolved.lower() != profile.commit.lower():
        raise RuntimeError(
            f"source profile {profile.name!r} is at {resolved}, "
            f"but swatref.toml pins {profile.commit}"
        )
    return source_dir, SourceProvenance(
        profile=profile.name,
        repository=profile.repository,
        requested_ref=profile.ref,
        configured_commit=profile.commit,
        resolved_commit=resolved,
    )


def fetch_profile(cfg: Config, name: str | None = None) -> SourceProvenance:
    """Fetch a branch, tag, or commit and detach at its resolved commit."""
    profile = cfg.source_profile(name)
    checkout = profile.abs_checkout(cfg.root)
    checkout.parent.mkdir(parents=True, exist_ok=True)

    if not (checkout / ".git").exists():
        checkout.mkdir(parents=True, exist_ok=True)
        _git("init", cwd=checkout)
        _git("remote", "add", "origin", profile.repository, cwd=checkout)
    else:
        current_remote = _git("remote", "get-url", "origin", cwd=checkout)
        if _normal_remote(current_remote) != _normal_remote(profile.repository):
            raise RuntimeError(
                f"{checkout} uses remote {current_remote!r}; expected {profile.repository!r}"
            )

    depth_args = ("--depth", str(profile.depth)) if profile.depth > 0 else ()
    _git("fetch", *depth_args, "origin", profile.ref, cwd=checkout)
    resolved_from_ref = _git("rev-parse", "FETCH_HEAD", cwd=checkout)
    target = profile.commit or resolved_from_ref
    if profile.commit and target.lower() != resolved_from_ref.lower():
        # A branch/tag lock can point behind its current tip. Fetching the
        # exact object keeps the configured build reproducible.
        _git("fetch", *depth_args, "origin", profile.commit, cwd=checkout)
    _git("checkout", "--detach", target, cwd=checkout)
    _, provenance = resolve_profile(cfg, profile.name)
    return provenance
