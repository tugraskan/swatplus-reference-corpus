from pathlib import Path

from peewee import AutoField, CharField, DoubleField, ForeignKeyField, IntegerField, Model

from swatplus_reference.schema.editor_effective import extract_editor_effective_schemas


class Child(Model):
    id = AutoField()
    name = CharField()

    class Meta:
        table_name = "child"


class Parent(Model):
    id = AutoField()
    name = CharField()
    child = ForeignKeyField(Child)

    class Meta:
        table_name = "parent"


class ParentItem(Model):
    id = AutoField()
    name = CharField()
    amount = DoubleField()

    class Meta:
        table_name = "parent_item"


class PlantIniOverride(Model):
    name = CharField()

    class Meta:
        table_name = "plant_ini"


class WeatherWgnCliOverride(Model):
    name = CharField()

    class Meta:
        table_name = "weather_wgn_cli"


class AtmoCliOverride(Model):
    name = CharField()

    class Meta:
        table_name = "atmo_cli"


class ExcoPestExcOverride(Model):
    name = CharField()

    class Meta:
        table_name = "exco_pest_exc"


class ManagementSchOverride(Model):
    name = CharField()

    class Meta:
        table_name = "management_sch"


class ConstituentsCsOverride(Model):
    name = CharField()

    class Meta:
        table_name = "constituents_cs"


class ExcoConOverride(Model):
    name = CharField()

    class Meta:
        table_name = "exco_con"


class ObjectCntOverride(Model):
    name = CharField()
    obj = IntegerField()

    class Meta:
        table_name = "object_cnt"


class PlantParmsSftOverride(Model):
    name = CharField()

    class Meta:
        table_name = "plant_parms_sft"


class SaltHruIniCsOverride(Model):
    name = CharField()

    class Meta:
        table_name = "salt_hru_ini_cs"


class SoilsSolOverride(Model):
    name = CharField()

    class Meta:
        table_name = "soils_sol"


def test_custom_query_alias_controls_serialized_foreign_key_type(tmp_path: Path) -> None:
    fileio = tmp_path / "src" / "api" / "fileio"
    fileio.mkdir(parents=True)
    (fileio / "parent.py").write_text(
        """
class Parent:
    def write(self):
        table = db.Parent
        query = table.select(table.id, table.name, Child.name.alias("child"))
        self.write_custom_query_table(table, query, ignore_id_col=False)
""",
        encoding="utf-8",
    )

    schemas, _ = extract_editor_effective_schemas(
        tmp_path,
        {"child": Child, "parent": Parent, "parent_item": ParentItem},
    )

    fields = schemas["parent"].fields
    assert [field.name for field in fields] == ["id", "name", "child"]
    assert fields[2].field_type == "character"


def test_local_item_table_fields_are_resolved(tmp_path: Path) -> None:
    fileio = tmp_path / "src" / "api" / "fileio"
    fileio.mkdir(parents=True)
    (fileio / "parent.py").write_text(
        """
class Parent:
    def write(self):
        table = db.Parent
        item_table = db.ParentItem
        header_cols = [col(table.name)]
        self.write_headers(file, header_cols)
        row_header_cols = [col(" ", not_in_db=True), col(item_table.name), col(item_table.amount)]
        self.write_headers(file, row_header_cols)
""",
        encoding="utf-8",
    )

    schemas, _ = extract_editor_effective_schemas(
        tmp_path,
        {"child": Child, "parent": Parent, "parent_item": ParentItem},
    )

    blocks = schemas["parent"].blocks
    assert [field.name for field in blocks[1].fields] == ["name", "amount"]
    assert blocks[1].fields[1].field_type == "real"


def test_canonical_overrides_replace_fallback_for_reviewed_structured_files(tmp_path: Path) -> None:
    fileio = tmp_path / "src" / "api" / "fileio"
    fileio.mkdir(parents=True)

    schemas, stats = extract_editor_effective_schemas(
        tmp_path,
        {
            "plant_ini": PlantIniOverride,
            "weather_wgn_cli": WeatherWgnCliOverride,
            "atmo_cli": AtmoCliOverride,
            "exco_pest_exc": ExcoPestExcOverride,
            "management_sch": ManagementSchOverride,
            "constituents_cs": ConstituentsCsOverride,
            "exco_con": ExcoConOverride,
            "object_cnt": ObjectCntOverride,
            "plant_parms_sft": PlantParmsSftOverride,
            "salt_hru_ini_cs": SaltHruIniCsOverride,
            "soils_sol": SoilsSolOverride,
        },
    )

    assert stats["manual_canonical"] == 11
    assert [block.name for block in schemas["plant_ini"].blocks] == ["header", "plant_items"]
    assert [field.name for field in schemas["plant_ini"].blocks[1].fields] == [
        "plt_name",
        "lc_status",
        "lai_init",
        "bm_init",
        "phu_init",
        "plnt_pop",
        "yrs_init",
        "rsd_init",
    ]
    assert [block.name for block in schemas["weather_wgn_cli"].blocks] == ["header", "monthly_values"]
    assert schemas["atmo_cli"].blocks[2].fields[0].repeated is True
    assert [field.name for field in schemas["exco_pest_exc"].fields] == ["name"]
    assert [block.name for block in schemas["management_sch"].blocks] == ["header", "auto_ops", "operations"]
    assert [block.name for block in schemas["constituents_cs"].blocks] == [
        "pests_count",
        "pests_names",
        "paths_count",
        "paths_names",
        "metals_count",
        "metals_names",
        "salts_count",
        "salts_names",
    ]
    assert [field.name for field in schemas["object_cnt"].fields][:4] == ["name", "ls_area", "tot_area", "obj"]
    assert [block.name for block in schemas["plant_parms_sft"].blocks] == ["header", "items"]
    assert [field.name for field in schemas["salt_hru_ini_cs"].fields] == [
        "name",
        "so4",
        "ca",
        "mg",
        "na",
        "k",
        "cl",
        "co3",
        "hco3",
    ]
    assert [block.name for block in schemas["soils_sol"].blocks] == ["header", "layers"]
