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
