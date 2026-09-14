from pathlib import Path

from swatplus_reference.docs.pages import Page
from swatplus_reference.docs.render import Renderer
from swatplus_reference.parser.refs import resolve_outside_refs
from swatplus_reference.parser.rich import RichStore
from swatplus_reference.parser.schema_model import ModuleDoc, ProcedureDoc, ProjectIndex, SourceLocation, UseRef, VariableRef


FIXTURES = Path(__file__).parent / "fixtures"


def test_rich_store_captures_declaration_backed_module_state():
    rich = RichStore.build(FIXTURES)
    refs = rich.outside_state_refs_for("demo_calc", "subroutine", "demo_calc.f90")

    dstate = next(ref for ref in refs if ref.symbol == "dstate" and ref.reference.endswith("%stor"))
    assert dstate.module == "demo_module"
    assert dstate.declaration.startswith("type (demo_state)")
    assert [component.name for component in dstate.components] == ["stor"]


def test_ambiguous_module_state_is_retained_not_dropped():
    loc = SourceLocation("fixture.f90", 1, 2)
    proc = ProcedureDoc("reader", "subroutine", loc, uses=[UseRef("left"), UseRef("right")])
    left = ModuleDoc("left", loc, variables=[VariableRef("shared", "integer :: shared", loc)])
    right = ModuleDoc("right", loc, variables=[VariableRef("shared", "integer :: shared", loc)])
    project = ProjectIndex("fixture", ".", modules=[left, right], procedures=[proc])

    ref = resolve_outside_refs(proc, project, ["shared"])[0]
    assert ref.ambiguous
    assert ref.candidates == ("left", "right")


def test_use_alias_resolves_to_the_declared_module_variable():
    loc = SourceLocation("fixture.f90", 1, 2)
    proc = ProcedureDoc(
        "reader", "subroutine", loc, uses=[UseRef("source", only=["local_name => remote_name"])]
    )
    module = ModuleDoc(
        "source", loc, variables=[VariableRef("remote_name", "integer :: remote_name", loc)]
    )
    project = ProjectIndex("fixture", ".", modules=[module], procedures=[proc])

    ref = resolve_outside_refs(proc, project, ["local_name"])[0]
    assert ref.module == "source"
    assert ref.symbol == "remote_name"


def test_non_only_use_alias_renames_one_symbol_and_keeps_other_imports():
    loc = SourceLocation("fixture.f90", 1, 2)
    proc = ProcedureDoc(
        "reader",
        "subroutine",
        loc,
        uses=[UseRef("source", renames=["local_name => remote_name"])],
    )
    module = ModuleDoc(
        "source",
        loc,
        variables=[
            VariableRef("remote_name", "integer :: remote_name", loc),
            VariableRef("unchanged", "integer :: unchanged", loc),
        ],
    )
    project = ProjectIndex("fixture", ".", modules=[module], procedures=[proc])

    refs = resolve_outside_refs(proc, project, ["local_name", "unchanged"])
    assert [(ref.reference, ref.symbol) for ref in refs] == [
        ("local_name", "remote_name"),
        ("unchanged", "unchanged"),
    ]
    assert resolve_outside_refs(proc, project, ["remote_name"]) == []


def test_state_touched_block_renders_live_receipts(cfg, store):
    rich = RichStore.build(FIXTURES)
    page = Page(
        path=cfg.abs_docs_dir / "procedures" / "demo_calc.md",
        kind="procedure",
        symbol="demo_calc",
        title="demo_calc",
        status="filled",
        version_label="TEST 1.0",
        body="<!-- facts:state_touched -->",
    )
    page.save()

    rendered = Renderer(cfg, store, [page], rich=rich).render_page(page)
    assert "| Module | Symbol | Declaration | Source | Components |" in rendered
    assert "demo_module" in rendered
    assert "demo_state%stor" in rendered
    assert "https://example.test/src/demo_module.f90#L" in rendered


def test_text_inside_a_double_quoted_literal_is_not_a_state_reference(tmp_path):
    """`write (*,*) " FERT-WET"` references no module variable.

    The scanner strips comments and single-quoted literals before looking for
    references, but not double-quoted ones -- so a name that happens to appear
    in a message or a `case ("res")` label was reported as a reference to the
    module state of the same name. The real subscripted reference on the line
    above is a separate entry and is kept.
    """

    (tmp_path / "m.f90").write_text(
        """\
module hru_module
  real :: wet = 0.
  real :: fert = 0.
end module hru_module

subroutine s()
  use hru_module
  integer :: j
  j = 1
  if (wet(j) > 0.) then
    write (2612,*) j, " FERT-WET", "    FERT "
  end if
end subroutine s
""",
        encoding="utf-8",
    )
    rich = RichStore.build(tmp_path)
    refs = rich.outside_state_refs_for("s", "subroutine", "m.f90")
    references = {ref.reference.lower() for ref in refs}

    # The literal text contributes nothing...
    assert "fert" not in references
    # ...while the genuine subscripted reference survives.
    assert "wet(j)" in references
