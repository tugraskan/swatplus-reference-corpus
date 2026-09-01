from pathlib import Path

from swatplus_reference.parser.documentation import (
    RICH_DOCUMENTATION_PRODUCER,
    parse_documentation,
    project_documentation_facts,
)
from swatplus_reference.parser.facts import FactStore
from swatplus_reference.parser.rich import RichStore


FIXTURES = Path(__file__).parent / "fixtures"


def test_rich_scan_is_the_documentation_fact_producer():
    store, rich = parse_documentation(FIXTURES, "source-sha")

    assert store.producer == RICH_DOCUMENTATION_PRODUCER
    assert store.source_ref == "source-sha"
    assert rich.get_of_kind("demo_calc", "subroutine", file="demo_calc.f90")

    procedure = store.get("demo_calc")
    assert procedure is not None
    assert procedure.args[0].name == "frac"
    assert procedure.args[0].line == 8
    assert procedure.locals[0].line == 9
    assert procedure.uses[0].line == 3
    assert procedure.calls == ["demo_zero"]
    assert procedure.depends_on == ["demo_module", "time_module"]
    assert procedure.reads == ["basin_count", "dstate"]
    assert procedure.writes == ["total_area"]
    assert store.get("demo_zero").depends_on == ["demo_module", "demo_state"]


def test_rich_projection_keeps_component_locations_and_docs():
    rich = RichStore.build(FIXTURES)
    store = project_documentation_facts(rich, FIXTURES, "source-sha")

    derived = store.get("demo_state")
    assert derived is not None
    assert [(component.name, component.line) for component in derived.components] == [
        ("flow", 9),
        ("stor", 10),
    ]
    assert derived.components[0].units == "m3/s"
    assert derived.components[0].description == "current flow"


def test_fact_cache_identifies_old_thin_files():
    old = FactStore.from_json('{"source_ref": "abc", "symbols": {}}')
    assert old.producer == "thin-v1"

    current, _rich = parse_documentation(FIXTURES, "abc")
    loaded = FactStore.from_json(current.to_json())
    assert loaded.producer == RICH_DOCUMENTATION_PRODUCER
    assert loaded.get("demo_calc").args[0].line == 8
