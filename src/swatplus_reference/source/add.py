"""Add a locked source profile to swatref.toml from a branch, tag, or PR ref.

A new profile is written with the exact commit the ref resolves to right now,
so every later fetch, parse, schema build, and comparison reproduces that
commit even after the branch moves. Re-adding an existing ref never relocks
it; it reports the current tip so a moved branch is visible.
"""

from __future__ import annotations

import json
import re
import tomllib
from dataclasses import dataclass
from pathlib import Path

from .config import DEFAULT_REPOSITORY, RELEASE_TAG, SourceProfile, load_config
from .fetch import _git, _normal_remote

_SHA = re.compile(r"^[0-9a-fA-F]{40}$")
_PULL = re.compile(r"^refs/pull/(\d+)/head$")


@dataclass
class AddResult:
    profile: SourceProfile
    created: bool
    # What the ref resolves to right now; differs from profile.commit when an
    # already-configured branch has moved since it was locked.
    current_commit: str

    def to_dict(self) -> dict[str, object]:
        return {
            "profile": self.profile.name,
            "created": self.created,
            "repository": self.profile.repository,
            "ref": self.profile.ref,
            "commit": self.profile.commit,
            "current_commit": self.current_commit,
            "moved": bool(self.profile.commit)
            and self.current_commit.lower() != self.profile.commit.lower(),
            "checkout": str(self.profile.checkout),
        }


def default_profile_name(ref: str) -> str:
    """``63.0.0`` -> ``release_63_0_0``; ``refs/pull/252/head`` -> ``pr_252``."""
    if match := RELEASE_TAG.match(ref):
        return "release_" + match.group(1).replace(".", "_")
    if match := _PULL.match(ref):
        return f"pr_{match.group(1)}"
    if _SHA.match(ref):
        return f"commit_{ref[:12].lower()}"
    short = re.sub(r"^refs/(heads|tags)/", "", ref)
    return re.sub(r"[^0-9A-Za-z]+", "_", short).strip("_").lower()


def resolve_remote_ref(repository: str, ref: str) -> str:
    """Resolve a branch, tag, or full ref name to its commit without cloning."""
    if _SHA.match(ref):
        return ref.lower()
    output = _git("ls-remote", repository, ref, f"{ref}^{{}}")
    found: dict[str, str] = {}
    for line in output.splitlines():
        sha, _, name = line.partition("\t")
        found[name] = sha
    wanted = [ref] if ref.startswith("refs/") else [f"refs/heads/{ref}", f"refs/tags/{ref}"]
    commits: dict[str, str] = {}
    for name in wanted:
        # An annotated tag lists the tag object and, with ^{}, its commit.
        sha = found.get(f"{name}^{{}}") or found.get(name)
        if sha:
            commits[name] = sha
    if not commits:
        raise ValueError(f"{ref!r} is not a branch, tag, or ref in {repository}")
    if len(commits) > 1:
        raise ValueError(
            f"{ref!r} is both a branch and a tag in {repository}; "
            f"pass the full name ({' or '.join(sorted(commits))})"
        )
    return next(iter(commits.values()))


def _label(ref: str, commit: str) -> str:
    if match := RELEASE_TAG.match(ref):
        return f"SWAT+ {match.group(1)}"
    return f"SWAT+ {ref} @ {commit[:12]}"


def _insert_after_sources(text: str, block: str) -> str:
    """Place ``block`` after the last [sources.*] table, else at the end."""
    lines = text.splitlines(keepends=True)
    headers = [i for i, line in enumerate(lines) if re.match(r"\s*\[", line)]
    source_headers = [i for i in headers if re.match(r"\s*\[sources\.", lines[i])]
    if source_headers:
        following = [i for i in headers if i > source_headers[-1]]
        if following:
            at = following[0]
            while at > 0 and not lines[at - 1].strip():
                at -= 1
            return "".join(lines[:at]) + "\n" + block + "".join(lines[at:])
    if text and not text.endswith("\n"):
        text += "\n"
    return text + ("\n" if text else "") + block


def add_profile(
    config_path: str | Path,
    ref: str,
    *,
    name: str | None = None,
    repository: str = DEFAULT_REPOSITORY,
) -> AddResult:
    """Lock ``ref`` to its current commit as a new profile in ``config_path``."""
    config_path = Path(config_path)
    name = name or default_profile_name(ref)
    if not re.fullmatch(r"[A-Za-z0-9_-]+", name):
        raise ValueError(f"profile name {name!r} may use only letters, digits, _ and -")
    current = resolve_remote_ref(repository, ref)

    cfg = load_config(config_path)
    existing = cfg.sources.get(name)
    if existing is not None:
        same = existing.ref == ref and _normal_remote(existing.repository) == _normal_remote(
            repository
        )
        if not same:
            raise ValueError(
                f"source profile {name!r} already exists for {existing.ref!r}; "
                "choose another --name"
            )
        return AddResult(existing, created=False, current_commit=current)

    profile = SourceProfile(
        name=name,
        repository=repository,
        ref=ref,
        commit=current,
        checkout=Path(f"external/swatplus-{name}"),
        label=_label(ref, current),
    )
    fields = {
        "repository": profile.repository,
        "ref": profile.ref,
        "commit": profile.commit,
        "checkout": profile.checkout.as_posix(),
        "subdir": profile.subdir,
        "label": profile.label,
    }
    block = f"[sources.{name}]\n" + "".join(
        f"{key} = {json.dumps(value)}\n" for key, value in fields.items()
    ) + f"depth = {profile.depth}\n"

    original = config_path.read_text(encoding="utf-8") if config_path.exists() else ""
    updated = _insert_after_sources(original, block)
    tomllib.loads(updated)  # never write a file the next command cannot read
    config_path.write_text(updated, encoding="utf-8")
    return AddResult(profile, created=True, current_commit=current)
