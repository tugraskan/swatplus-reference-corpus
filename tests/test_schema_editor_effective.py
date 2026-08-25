from pathlib import Path

from peewee import AutoField, CharField, ForeignKeyField, Model

from swatplus_reference.schema.editor_effective import (
    EffectiveBlock,
    EffectiveField,
    EffectiveFileSchema,
    extract_editor_effective_schemas,
)
from swatplus_reference.schema.editor_compare import compare_effective_schema


class Target(Model):
    id = AutoField()
    name = CharField()

    class Meta:
        table_name = "target"


class Example(Model):
    id = AutoField()
    name = CharField()
    target = ForeignKeyField(Target)
    description = CharField(null=True)

    class Meta:
        table_name = "example"


def _schema(
    *fields: EffectiveField,
    confidence: str = "high",
    extraction: str = "writer_column_blocks",
) -> EffectiveFileSchema:
    return EffectiveFileSchema(
        table_name="example",
        model_class="Example",
        source_module="tests",
        writer_class="Example",
        writer_module="example.py",
        extraction=extraction,
        confidence=confidence,
        blocks=(EffectiveBlock(name="rows", fields=fields),),
    )


def test_compare_effective_schema_separates_labels_from_layout() -> None:
    official = [
        {
            "name": "rows",
            "fields": [
                {"name": "absmin", "field_type": "real", "position": 0},
                {"name": "absmax", "field_type": "real", "position": 1},
            ],
        }
    ]
    editor = _schema(
        EffectiveField("abs_min", "real", True, 0),
        EffectiveField("abs_max", "real", True, 1),
    )

    result = compare_effective_schema(official, editor, structured=False)

    assert result["status"] == "compatible_labels_differ"
    assert result["layout_compatible"] is True
    assert result["labels_normalized"] is True


def test_compare_effective_schema_reports_type_change() -> None:
    official = [
        {
            "name": "rows",
            "fields": [{"name": "rule", "field_type": "character", "position": 0}],
        }
    ]
    editor = _schema(EffectiveField("rule", "integer", True, 0))

    result = compare_effective_schema(official, editor, structured=False)

    assert result["status"] == "real_layout_change"
    assert result["blocks"][0]["type_differences"][0]["position"] == 0


def test_incomplete_structured_extraction_stays_review_only() -> None:
    official = [
        {"name": "header", "fields": []},
        {"name": "details", "fields": []},
    ]

    result = compare_effective_schema(official, _schema(), structured=True)

    assert result["status"] == "extraction_needs_review"


def test_official_variant_uncertainty_is_not_editor_extraction_failure() -> None:
    official = [
        {"name": "header", "fields": [{"name": "name", "field_type": "character", "position": 0}]}
    ]

    result = compare_effective_schema(
        official,
        _schema(EffectiveField("name", "character", False, 0)),
        structured=True,
        official_uncertainty="Official multi-record file has incompatible tagged variants.",
    )

    assert result["status"] == "official_schema_variant"


def test_extractor_uses_query_alias_and_keeps_reassigned_header_blocks(tmp_path: Path) -> None:
    fileio = tmp_path / "src" / "api" / "fileio"
    fileio.mkdir(parents=True)
    (fileio / "example.py").write_text(
        """
class Example:
    def write(self):
        table = db.Example
        query = table.select(Target.name.alias("target_name"))
        header_cols = [col(table.id), col(table.name), col(table.target, query_alias="target_name"), col(table.description, is_desc=True)]
        self.write_headers(file, header_cols)
        header_cols = [col(table.name)]
        self.write_headers(file, header_cols)
""",
        encoding="utf-8",
    )

    schemas, stats = extract_editor_effective_schemas(
        tmp_path,
        {"example": Example, "target": Target},
    )

    schema = schemas["example"]
    assert stats["writer_column_blocks"] == 1
    assert [field.name for field in schema.blocks[0].fields] == [
        "id",
        "name",
        "target_name",
    ]
    assert schema.blocks[0].fields[2].field_type == "character"
    assert [field.name for field in schema.blocks[1].fields] == ["name"]


def test_manual_canonical_structured_mismatch_counts_as_layout_change() -> None:
    official = [
        {"name": "entry_name", "fields": [{"name": "name", "field_type": "character", "position": 0}]},
        {"name": "values", "fields": [{"name": "coeff", "field_type": "real", "position": 0}]},
    ]

    result = compare_effective_schema(
        official,
        _schema(EffectiveField("name", "character", False, 0), extraction="manual_canonical"),
        structured=True,
    )

    assert result["status"] == "real_layout_change"
