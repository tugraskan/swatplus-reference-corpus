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


# --------------------------------------------------------------------------
# Non-standard signed operands
#
# `a*-1` is rejected by fparser2 and accepted by gfortran. The rich path
# (`ast_index`) parenthesises it for the parser; this layer did not, so two
# SWAT+ files parsed cleanly into the rich store while falling back to the line
# scanner here. These pin the rewrite and, just as importantly, its limits.
# --------------------------------------------------------------------------


def _parse(tmp_path, body: str) -> FactStore:
    from swatplus_reference.parser.fortran import parse_tree

    (tmp_path / "signs.f90").write_text(body)
    return parse_tree(tmp_path)


SIGNED = """\
      subroutine signs
      integer :: q = 0
      integer :: stor = 0
      if ((q*-1) >= stor) then
        stor = q
      end if
      end subroutine signs
"""


def test_signed_operand_parses_without_falling_back(tmp_path):
    store = _parse(tmp_path, SIGNED)
    assert store.fallback_files == []
    assert store.parse_errors == {}
    assert store.get("signs") is not None


def test_the_rewrite_is_recorded_not_silent(tmp_path):
    store = _parse(tmp_path, SIGNED)
    assert store.normalized_files == {"signs.f90": [4]}


def test_normalized_files_survives_a_round_trip(tmp_path):
    store = _parse(tmp_path, SIGNED)
    assert FactStore.from_json(store.to_json()).normalized_files == store.normalized_files


def test_a_file_needing_no_rewrite_records_nothing(tmp_path):
    store = _parse(tmp_path, SIGNED.replace("(q*-1)", "(q * (-1))"))
    assert store.normalized_files == {}
    assert store.fallback_files == []


def test_a_file_that_still_fails_claims_no_rewrite(tmp_path):
    """A rewrite recorded before a parse that then dies describes input that
    produced nothing, so it must not be reported alongside the fallback."""
    store = _parse(tmp_path, SIGNED.replace("end subroutine signs", "end subroutin signs"))
    assert store.fallback_files == ["signs.f90"]
    assert "signs.f90" not in store.normalized_files
