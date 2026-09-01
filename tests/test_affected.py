from __future__ import annotations

from pathlib import Path

from swatplus_reference.docs.pages import Page, STATUS_AFFECTED, STATUS_FILLED, STATUS_STALE
from swatplus_reference.docs.staleness import apply_status, compute_status
from swatplus_reference.parser.facts import FactStore, Symbol


def sym(name, calls=None, hash="h", depends_on=None) -> Symbol:
    return Symbol(kind="subroutine", name=name, file=f"{name}.f90",
                  start_line=1, end_line=5, calls=calls or [],
                  depends_on=depends_on or [], source_hash=hash)


def page(tmp, name, source_hash, status=STATUS_FILLED) -> Page:
    return Page(path=Path(tmp) / "procedures" / f"{name}.md", kind="procedure",
                symbol=name, title=name, status=status, source_hash=source_hash,
                body="<!-- facts:header -->")


def make_store():
    # caller -> changed -> callee   (caller calls changed; changed calls callee)
    store = FactStore(source_ref="t")
    store.add(sym("caller", calls=["changed"], hash="c1"))
    store.add(sym("changed", calls=["callee"], hash="X2"))  # X2 = new hash
    store.add(sym("callee", hash="e1"))
    store.add(sym("unrelated", hash="u1"))
    return store


def test_stale_symbol_flags_callers_and_callees(tmp_path):
    store = make_store()
    pages = [
        page(tmp_path, "caller", "c1"),      # unchanged own source
        page(tmp_path, "changed", "OLD"),    # own hash differs from X2 -> stale
        page(tmp_path, "callee", "e1"),      # unchanged own source
        page(tmp_path, "unrelated", "u1"),   # unchanged, no graph link
    ]
    r = compute_status(store, pages)
    stale_names = {p.symbol for p in r.stale}
    affected_names = {p.symbol for p in r.affected}
    filled_names = {p.symbol for p in r.filled}
    assert stale_names == {"changed"}
    # caller (describes calling changed) AND callee (context under changed) flagged
    assert affected_names == {"caller", "callee"}
    assert filled_names == {"unrelated"}
    # triggers recorded
    assert r.affected_by["caller.md"] == ["changed"]
    assert r.affected_by["callee.md"] == ["changed"]


def test_no_stale_means_no_affected(tmp_path):
    store = make_store()
    pages = [
        page(tmp_path, "caller", "c1"),
        page(tmp_path, "changed", "X2"),  # matches current -> filled
        page(tmp_path, "callee", "e1"),
    ]
    r = compute_status(store, pages)
    assert r.affected == []
    assert {p.symbol for p in r.filled} == {"caller", "changed", "callee"}


def test_changed_module_or_type_flags_declared_dependents(tmp_path):
    store = FactStore(source_ref="t")
    store.add(sym("shared_module", hash="module-new"))
    store.add(sym("consumer", hash="consumer-same", depends_on=["shared_module"]))
    pages = [
        page(tmp_path, "shared_module", "module-old"),
        page(tmp_path, "consumer", "consumer-same"),
    ]

    report = compute_status(store, pages)

    assert {item.symbol for item in report.stale} == {"shared_module"}
    assert {item.symbol for item in report.affected} == {"consumer"}
    assert report.affected_by["consumer.md"] == ["shared_module (dependency)"]


def test_stale_wins_over_affected(tmp_path):
    # a page that is both a neighbour of a changed symbol AND changed itself
    store = make_store()
    store.add(sym("caller", calls=["changed"], hash="cNEW"))
    pages = [
        page(tmp_path, "caller", "cOLD"),   # own source changed -> stale, not affected
        page(tmp_path, "changed", "OLD"),
        page(tmp_path, "callee", "e1"),
    ]
    r = compute_status(store, pages)
    assert {p.symbol for p in r.stale} == {"caller", "changed"}
    assert {p.symbol for p in r.affected} == {"callee"}


def test_apply_status_writes_and_reverts(tmp_path):
    (tmp_path / "procedures").mkdir(parents=True)
    store = make_store()
    caller = page(tmp_path, "caller", "c1"); caller.save()
    changed = page(tmp_path, "changed", "OLD"); changed.save()
    callee = page(tmp_path, "callee", "e1"); callee.save()
    pages = [caller, changed, callee]

    apply_status(store, pages)
    from swatplus_reference.docs.pages import load_page
    assert load_page(caller.path).status == STATUS_AFFECTED
    assert load_page(changed.path).status == STATUS_STALE
    assert load_page(callee.path).status == STATUS_AFFECTED

    # once 'changed' is refilled (hash matches), affected reverts to filled
    changed2 = load_page(changed.path); changed2.source_hash = "X2"; changed2.save()
    pages = [load_page(caller.path), changed2, load_page(callee.path)]
    apply_status(store, pages)
    assert load_page(caller.path).status == STATUS_FILLED
    assert load_page(callee.path).status == STATUS_FILLED
    assert load_page(changed.path).status == STATUS_FILLED
