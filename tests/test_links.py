"""Tests for the rendered GitHub source-link audit."""

from __future__ import annotations

from pathlib import Path

import pytest

from swatplus_reference.docs.links import audit_source_links, count_source_links


BASE = "https://github.com/swat-model/swatplus/blob/" + "a" * 40 + "/src"


def _tree(tmp_path: Path, page_body: str) -> tuple[Path, Path]:
    render_dir = tmp_path / "docs"
    (render_dir / "procedures").mkdir(parents=True)
    (render_dir / "procedures" / "demo.md").write_text(page_body, encoding="utf-8")
    source_dir = tmp_path / "src"
    source_dir.mkdir()
    (source_dir / "demo.f90").write_text("\n".join(f"line {n}" for n in range(1, 11)), encoding="utf-8")
    return render_dir, source_dir


def test_valid_single_and_span_links_pass(tmp_path):
    render_dir, source_dir = _tree(
        tmp_path,
        f"See [demo]({BASE}/demo.f90#L1-L10) and [call]({BASE}/demo.f90#L4).\n",
    )

    assert audit_source_links(render_dir, source_dir, BASE) == []
    assert count_source_links(render_dir, BASE) == 2


def test_line_beyond_end_of_file_is_reported(tmp_path):
    render_dir, source_dir = _tree(tmp_path, f"[x]({BASE}/demo.f90#L11)\n")

    findings = audit_source_links(render_dir, source_dir, BASE)

    assert [finding.code for finding in findings] == ["out-of-range"]
    assert "1-10" in findings[0].message
    assert findings[0].page == "procedures/demo.md"


@pytest.mark.parametrize("content,lines", [
    (b"", 0),
    (b"one", 1),
    (b"one\n", 1),
    (b"one\r\n", 1),
    (b"one\n\n", 2),
    (b"one\r\ntwo", 2),
    (b"\n", 1),
])
def test_line_bounds_handle_terminal_newlines_and_empty_files(tmp_path, content, lines):
    body = (
        f"[past end]({BASE}/demo.f90#L{lines + 1})\n"
        f"[span past end]({BASE}/demo.f90#L1-L{lines + 1})\n"
    )
    if lines:
        body += f"[last line]({BASE}/demo.f90#L{lines})\n"
        body += f"[valid span]({BASE}/demo.f90#L1-L{lines})\n"
    render_dir, source_dir = _tree(tmp_path, body)
    (source_dir / "demo.f90").write_bytes(content)

    findings = audit_source_links(render_dir, source_dir, BASE)

    assert len(findings) == 2
    assert all(finding.code == "out-of-range" for finding in findings)
    assert all(f"(1-{lines})" in finding.message for finding in findings)


def test_reversed_span_is_reported(tmp_path):
    render_dir, source_dir = _tree(tmp_path, f"[x]({BASE}/demo.f90#L8-L3)\n")

    assert [f.code for f in audit_source_links(render_dir, source_dir, BASE)] == [
        "out-of-range"
    ]


def test_missing_source_file_is_reported(tmp_path):
    render_dir, source_dir = _tree(tmp_path, f"[x]({BASE}/gone.f90#L2)\n")

    findings = audit_source_links(render_dir, source_dir, BASE)

    assert [finding.code for finding in findings] == ["missing-file"]
    assert "gone.f90" in findings[0].message


def test_link_on_another_commit_is_reported(tmp_path):
    other = BASE.replace("a" * 40, "b" * 40)
    render_dir, source_dir = _tree(tmp_path, f"[x]({other}/demo.f90#L2)\n")

    findings = audit_source_links(render_dir, source_dir, BASE)

    assert [finding.code for finding in findings] == ["wrong-commit"]
    # A wrong-commit link is not one of the links this audit claims to have
    # verified, so it must not inflate the reported coverage either.
    assert count_source_links(render_dir, BASE) == 0


def test_unrelated_anchors_are_ignored(tmp_path):
    render_dir, source_dir = _tree(
        tmp_path, "[docs](https://example.test/page#L9999) and [local](other.md#L3)\n"
    )

    assert audit_source_links(render_dir, source_dir, BASE) == []
    assert count_source_links(render_dir, BASE) == 0


def test_cli_fails_when_the_render_has_no_source_links(tmp_path, monkeypatch, capsys):
    """An empty or stale render must not pass the audit in silence."""
    from types import SimpleNamespace
    from swatplus_reference import cli
    from swatplus_reference.source.config import Config

    render_dir = tmp_path / "docs"
    render_dir.mkdir()
    (render_dir / "index.md").write_text("no links here\n", encoding="utf-8")
    cfg = Config(root=tmp_path, source_dir=tmp_path / "src", render_dir=Path("docs"))
    (tmp_path / "src").mkdir()
    monkeypatch.setattr(cli, "activate_docs_source", lambda _: SimpleNamespace())

    assert cli.cmd_check_links(cfg, SimpleNamespace()) == 1
    assert "no source links found" in capsys.readouterr().out
