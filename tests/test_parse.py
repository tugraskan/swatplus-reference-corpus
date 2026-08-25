from swatplus_reference.parser.facts import FactStore
from swatplus_reference.parser.fortran import parse_file_fallback


def test_symbols_extracted(store):
    assert store.get("demo_module").kind == "module"
    assert store.get("demo_calc").kind == "subroutine"
    assert store.get("demo_zero").parent == "demo_module"
    assert store.get("demo_state").kind == "type"


def test_module_variables(store):
    mod = store.get("demo_module")
    names = {v.name for v in mod.variables}
    assert {"basin_count", "total_area", "dstate"} <= names
    # type components must not leak into module variables
    assert "flow" not in names


def test_procedure_details(store):
    calc = store.get("demo_calc")
    assert [a.name for a in calc.args] == ["frac"]
    assert calc.args[0].intent == "in"
    assert {v.name for v in calc.locals} == {"j", "wrk", "eof"}
    assert [u.module for u in calc.uses] == ["demo_module", "time_module"]
    assert calc.uses[1].only == ["yrs_print"]
    assert calc.calls == ["demo_zero"]


def test_io_statements(store):
    calc = store.get("demo_calc")
    kinds = [i.kind for i in calc.io]
    assert kinds == ["open", "read", "close"]
    assert calc.io[0].file_expr == '"demo.in"'
    assert calc.io[0].line > 0


def test_callers_and_members(store):
    assert [s.name for s in store.callers_of("demo_zero")] == ["demo_calc"]
    members = {m.name for m in store.members_of("demo_module")}
    assert {"demo_zero", "demo_state"} <= members


def test_source_hash_stability(store):
    sym = store.get("demo_calc")
    assert sym.source_hash and len(sym.source_hash) == 16


def test_roundtrip_json(store):
    loaded = FactStore.from_json(store.to_json())
    assert set(loaded.symbols) == set(store.symbols)
    assert loaded.get("demo_calc").calls == ["demo_zero"]


def test_fallback_scanner():
    store = FactStore()
    text = "\n".join(
        [
            "      subroutine broken_sub",
            "      use demo_module, only : dstate",
            "      call demo_zero (dstate(1))",
            "      end subroutine broken_sub",
        ]
    )
    parse_file_fallback(store, "broken.f90", text)
    sym = store.get("broken_sub")
    assert sym.kind == "subroutine"
    assert sym.calls == ["demo_zero"]
    assert sym.uses[0].only == ["dstate"]
    assert (sym.start_line, sym.end_line) == (1, 4)


def test_type_name_collision_prefers_procedure():
    store = FactStore()
    text = "\n".join(
        [
            "module m1",
            "  type balance",
            "    real :: x = 0.",
            "  end type balance",
            "end module m1",
            "subroutine balance",
            "end subroutine balance",
        ]
    )
    from swatplus_reference.parser.fortran import parse_file_ast

    parse_file_ast(store, "m1.f90", text)
    assert store.get("balance").kind == "subroutine"
    assert store.get("type::balance").kind == "type"
