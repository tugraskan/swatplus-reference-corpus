import csv
import importlib.util
import json
import subprocess
from pathlib import Path

SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "equation_map_drift.py"
spec = importlib.util.spec_from_file_location("equation_map_drift", SCRIPT)
drift = importlib.util.module_from_spec(spec)
spec.loader.exec_module(drift)


def _git(cwd, *args):
    return subprocess.run(
        ["git", "-c", "user.name=t", "-c", "user.email=t@t", "-c", "core.autocrlf=false", *args],
        cwd=cwd, check=True, capture_output=True, text=True,
    ).stdout.strip()


def _commit(repo, files, msg):
    for name, text in files.items():
        path = repo / "src" / name
        if text is None:
            path.unlink()
        else:
            path.write_bytes(text.encode())
    _git(repo, "add", "-A")
    _git(repo, "commit", "-q", "-m", msg)
    return _git(repo, "rev-parse", "HEAD")


def test_drift_labels_and_suggested_lines(tmp_path):
    repo = tmp_path / "swatplus"
    (repo / "src").mkdir(parents=True)
    _git(repo, "init", "-q", "-b", "main")
    old = _commit(repo, {
        "a.f90": "x = 1\ny = 2\nz = 3\nw = 4\nv = 5\n",
        "b.f90": "q = 1\n",
        "gone.f90": "g = 1\n",
    }, "old")
    # header inserted (shifts everything), z edited, w only re-indented, u inserted between w and v
    new = _commit(repo, {
        "a.f90": "! header\nx = 1\ny = 2\nz = 30\n    w = 4\nu = 9\nv = 5\n",
        "gone.f90": None,
    }, "new")

    cited = {
        "moved": "a.f90:2",
        "edited": "a.f90:3",
        "whitespace": "a.f90:4",
        "range": "a.f90:1-2",
        "list": "a.f90:1,5",
        "insert_inside": "a.f90:4-5",
        "two_files": "a.f90:2 b.f90:1",
        "unchanged": "b.f90:1",
        "missing": "gone.f90:1",
        "past_end": "b.f90:5",
        "never_existed": "nope.f90:1",
        "file_only": "b.f90",
        "file_only_gone": "gone.f90",
        "none": "",
    }
    eq_map = tmp_path / "equation_map.json"
    eq_map.write_text(json.dumps({"mappings": [
        {"equation_id": f"1:{k}", "routine": "r", "source_lines": v, "status": "implemented"}
        for k, v in cited.items()
    ]}), encoding="utf-8")

    out = tmp_path / "out"
    assert drift.main(["--repo", str(repo), "--map", str(eq_map), "--old", old, "--new", new, "--out", str(out)]) == 0

    [csv_path] = out.glob("map_drift_*.csv")
    rows = {r["equation_id"].split(":", 1)[1]: r for r in csv.DictReader(csv_path.open(encoding="utf-8"))}
    got = {k: (r["drift_result"], r["suggested_lines"]) for k, r in rows.items()}
    assert got == {
        "moved": ("moved", "a.f90:3"),
        "edited": ("edited", ""),
        "whitespace": ("moved", "a.f90:5"),
        "range": ("moved", "a.f90:2-3"),
        "list": ("moved", "a.f90:2,7"),
        "insert_inside": ("edited", ""),
        "two_files": ("moved", "a.f90:3 b.f90:1"),
        "unchanged": ("unchanged", ""),
        "missing": ("missing", ""),
        "past_end": ("missing", ""),
        "never_existed": ("missing", ""),
        "file_only": ("no_code", ""),
        "file_only_gone": ("missing", ""),
        "none": ("no_code", ""),
    }
    md = csv_path.with_suffix(".md").read_text(encoding="utf-8")
    assert "| Edited: the cited code changed; check the equation again | 2 |" in md


def test_new_line_handles_insertions_and_replacements():
    # old 3 replaced by new 3-4; two lines inserted after old 6
    hunks = [(3, 1, 3, 2), (6, 0, 8, 2)]
    assert [drift.new_line(hunks, n) for n in (1, 2, 3, 4, 6, 7)] == [1, 2, None, 5, 7, 10]
