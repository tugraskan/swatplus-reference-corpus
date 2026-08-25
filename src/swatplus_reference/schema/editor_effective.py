"""Extract the schema SWAT+ Editor actually serializes to input files.

The Editor database models describe storage, not the final text contract.  This
module reads the Editor's writer source without modifying it and recognizes the
common serialization patterns used under ``src/api/fileio``.
"""

from __future__ import annotations

import ast
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable


INTEGER_LITERAL_FIELDS = frozenset(
    {
        "acts",
        "alts",
        "conds",
        "dmd_num",
        "dmd_obs",
        "elem_tot",
        "elements",
        "id",
        "mo_init",
        "npsu",
        "nspu",
        "num",
        "num_srcs",
        "num_sta",
        "num_ts",
        "obj_num",
        "obj_tot",
        "out_tot",
        "rcv_num",
        "src",
        "src_num",
        "src_obs",
        "src_tot",
        "yr_init",
    }
)
REAL_LITERAL_FIELDS = frozenset({"frac", "monthly_limit"})
CHARACTER_LITERAL_FIELDS = frozenset(
    {"alt", "comp", "hyd_typ", "obj_typ", "objects", "outcome", "use_obj_lbls"}
)

@dataclass(frozen=True)
class EffectiveField:
    name: str
    field_type: str
    numeric: bool
    position: int
    source: str | None = None
    repeated: bool = False

    def to_dict(self) -> dict[str, Any]:
        return {
            "name": self.name,
            "field_type": self.field_type,
            "numeric": self.numeric,
            "position": self.position,
            "source": self.source,
            "repeated": self.repeated,
        }


@dataclass(frozen=True)
class EffectiveBlock:
    name: str
    fields: tuple[EffectiveField, ...]
    source_line: int | None = None

    def to_dict(self) -> dict[str, Any]:
        return {
            "name": self.name,
            "source_line": self.source_line,
            "fields": [field.to_dict() for field in self.fields],
        }


@dataclass(frozen=True)
class EffectiveFileSchema:
    table_name: str
    model_class: str
    source_module: str
    writer_class: str | None
    writer_module: str | None
    extraction: str
    confidence: str
    blocks: tuple[EffectiveBlock, ...]

    @property
    def fields(self) -> tuple[EffectiveField, ...]:
        return self.blocks[0].fields if self.blocks else ()

    def to_dict(self) -> dict[str, Any]:
        return {
            "table_name": self.table_name,
            "model_class": self.model_class,
            "source_module": self.source_module,
            "writer_class": self.writer_class,
            "writer_module": self.writer_module,
            "extraction": self.extraction,
            "confidence": self.confidence,
            "blocks": [block.to_dict() for block in self.blocks],
            "fields": [field.to_dict() for field in self.fields],
        }



def _manual_field(
    name: str,
    field_type: str,
    *,
    repeated: bool = False,
) -> EffectiveField:
    return EffectiveField(
        name=name,
        field_type=field_type,
        numeric=field_type in {"integer", "real"},
        position=0,
        source="canonical_override",
        repeated=repeated,
    )


def _manual_block(name: str, *fields: EffectiveField) -> EffectiveBlock:
    return EffectiveBlock(name=name, fields=_renumber(fields))


def _canonical_editor_schema_overrides(
    models: dict[str, type[Any]],
) -> dict[str, EffectiveFileSchema]:
    def schema(
        table_name: str,
        writer_class: str,
        writer_module: str,
        *blocks: EffectiveBlock,
    ) -> EffectiveFileSchema:
        model = models[table_name]
        return EffectiveFileSchema(
            table_name=table_name,
            model_class=model.__name__,
            source_module=model.__module__,
            writer_class=writer_class,
            writer_module=writer_module,
            extraction="manual_canonical",
            confidence="high",
            blocks=blocks,
        )

    available = set(models)
    overrides: dict[str, EffectiveFileSchema] = {}

    if "atmo_cli" in available:
        overrides["atmo_cli"] = schema(
            "atmo_cli",
            "Atmo_cli",
            "climate.py",
            _manual_block(
                "control_header",
                _manual_field("num_sta", "integer"),
                _manual_field("timestep", "character"),
                _manual_field("mo_init", "integer"),
                _manual_field("yr_init", "integer"),
                _manual_field("num_ts", "integer"),
            ),
            _manual_block("station_name", _manual_field("station_name", "character")),
            _manual_block("nh4_rf", _manual_field("nh4_rf", "real", repeated=True)),
            _manual_block("no3_rf", _manual_field("no3_rf", "real", repeated=True)),
            _manual_block("nh4_dry", _manual_field("nh4_dry", "real", repeated=True)),
            _manual_block("no3_dry", _manual_field("no3_dry", "real", repeated=True)),
        )

    for table_name, writer_class in (
        ("exco_pest_exc", "Exco_pest_exc"),
        ("exco_path_exc", "Exco_path_exc"),
        ("exco_hmet_exc", "Exco_hmet_exc"),
        ("exco_salt_exc", "Exco_salt_exc"),
    ):
        if table_name in available:
            overrides[table_name] = schema(
                table_name,
                writer_class,
                "exco.py",
                _manual_block("rows", _manual_field("name", "character")),
            )

    if "management_sch" in available:
        overrides["management_sch"] = schema(
            "management_sch",
            "Management_sch",
            "lum.py",
            _manual_block(
                "header",
                _manual_field("name", "character"),
                _manual_field("numb_ops", "integer"),
                _manual_field("numb_auto", "integer"),
            ),
            _manual_block(
                "auto_ops",
                _manual_field("d_table", "character"),
                _manual_field("plant1", "character"),
                _manual_field("plant2", "character"),
            ),
            _manual_block(
                "operations",
                _manual_field("op_typ", "character"),
                _manual_field("mon", "integer"),
                _manual_field("day", "integer"),
                _manual_field("hu_sch", "real"),
                _manual_field("op_data1", "character"),
                _manual_field("op_data2", "character"),
                _manual_field("op_data3", "real"),
            ),
        )

    for table_name, writer_class, second_name, second_fields in (
        (
            "pest_hru_ini",
            "Pest_hru_ini",
            "soil_plant_concentrations",
            (
                _manual_field("constituent_name", "character"),
                _manual_field("soil", "real"),
                _manual_field("plant", "real"),
            ),
        ),
        (
            "pest_water_ini",
            "Pest_water_ini",
            "water_benthic_concentrations",
            (
                _manual_field("constituent_name", "character"),
                _manual_field("water", "real"),
                _manual_field("benthic", "real"),
            ),
        ),
        (
            "path_hru_ini",
            "Path_hru_ini",
            "soil_plant_concentrations",
            (
                _manual_field("constituent_name", "character"),
                _manual_field("soil", "real"),
                _manual_field("plant", "real"),
            ),
        ),
        (
            "path_water_ini",
            "Path_water_ini",
            "water_benthic_concentrations",
            (
                _manual_field("constituent_name", "character"),
                _manual_field("water", "real"),
                _manual_field("benthic", "real"),
            ),
        ),
    ):
        if table_name in available:
            overrides[table_name] = schema(
                table_name,
                writer_class,
                "init.py",
                _manual_block("entry_name", _manual_field("name", "character")),
                _manual_block(second_name, *second_fields),
            )

    if "plant_ini" in available:
        overrides["plant_ini"] = schema(
            "plant_ini",
            "Plant_ini",
            "init.py",
            _manual_block(
                "header",
                _manual_field("pcom_name", "character"),
                _manual_field("plt_cnt", "integer"),
                _manual_field("rot_yr_ini", "integer"),
            ),
            _manual_block(
                "plant_items",
                _manual_field("plt_name", "character"),
                _manual_field("lc_status", "character"),
                _manual_field("lai_init", "real"),
                _manual_field("bm_init", "real"),
                _manual_field("phu_init", "real"),
                _manual_field("plnt_pop", "real"),
                _manual_field("yrs_init", "real"),
                _manual_field("rsd_init", "real"),
            ),
        )

    if "weather_wgn_cli" in available:
        overrides["weather_wgn_cli"] = schema(
            "weather_wgn_cli",
            "Weather_wgn_cli",
            "climate.py",
            _manual_block(
                "header",
                _manual_field("name", "character"),
                _manual_field("lat", "real"),
                _manual_field("lon", "real"),
                _manual_field("elev", "real"),
                _manual_field("rain_yrs", "integer"),
            ),
            _manual_block(
                "monthly_values",
                _manual_field("tmp_max_ave", "real"),
                _manual_field("tmp_min_ave", "real"),
                _manual_field("tmp_max_sd", "real"),
                _manual_field("tmp_min_sd", "real"),
                _manual_field("pcp_ave", "real"),
                _manual_field("pcp_sd", "real"),
                _manual_field("pcp_skew", "real"),
                _manual_field("wet_dry", "real"),
                _manual_field("wet_wet", "real"),
                _manual_field("pcp_days", "real"),
                _manual_field("pcp_hhr", "real"),
                _manual_field("slr_ave", "real"),
                _manual_field("dew_ave", "real"),
                _manual_field("wnd_ave", "real"),
            ),
        )

    if "constituents_cs" in available:
        overrides["constituents_cs"] = schema(
            "constituents_cs",
            "Constituents_cs",
            "simulation.py",
            _manual_block("pests_count", _manual_field("num_pests", "integer")),
            _manual_block("pests_names", _manual_field("pests", "character", repeated=True)),
            _manual_block("paths_count", _manual_field("num_paths", "integer")),
            _manual_block("paths_names", _manual_field("paths", "character", repeated=True)),
            _manual_block("metals_count", _manual_field("num_metals", "integer")),
            _manual_block("metals_names", _manual_field("metals", "character", repeated=True)),
            _manual_block("salts_count", _manual_field("num_salts", "integer")),
            _manual_block("salts_names", _manual_field("salts", "character", repeated=True)),
        )

    if "exco_con" in available:
        overrides["exco_con"] = schema(
            "exco_con",
            "Exco_con",
            "connect.py",
            _manual_block(
                "rows",
                _manual_field("id", "integer"),
                _manual_field("name", "character"),
                _manual_field("gis_id", "integer"),
                _manual_field("area", "real"),
                _manual_field("lat", "real"),
                _manual_field("lon", "real"),
                _manual_field("elev", "real"),
                _manual_field("exco", "integer"),
                _manual_field("wst", "character"),
                _manual_field("cst", "integer"),
                _manual_field("ovfl", "integer"),
                _manual_field("rule", "integer"),
                _manual_field("out_tot", "integer"),
                _manual_field("obj_typ", "character", repeated=True),
                _manual_field("obj_id", "integer", repeated=True),
                _manual_field("hyd_typ", "character", repeated=True),
                _manual_field("frac", "real", repeated=True),
            ),
        )

    if "object_cnt" in available:
        overrides["object_cnt"] = schema(
            "object_cnt",
            "Object_cnt",
            "simulation.py",
            _manual_block(
                "rows",
                _manual_field("name", "character"),
                _manual_field("ls_area", "real"),
                _manual_field("tot_area", "real"),
                _manual_field("obj", "integer"),
                _manual_field("hru", "integer"),
                _manual_field("lhru", "integer"),
                _manual_field("rtu", "integer"),
                _manual_field("mfl", "integer"),
                _manual_field("aqu", "integer"),
                _manual_field("cha", "integer"),
                _manual_field("res", "integer"),
                _manual_field("rec", "integer"),
                _manual_field("exco", "integer"),
                _manual_field("dlr", "integer"),
                _manual_field("can", "integer"),
                _manual_field("pmp", "integer"),
                _manual_field("out", "integer"),
                _manual_field("lcha", "integer"),
                _manual_field("aqu2d", "integer"),
                _manual_field("hrd", "integer"),
                _manual_field("wro", "integer"),
            ),
        )

    if "plant_parms_sft" in available:
        overrides["plant_parms_sft"] = schema(
            "plant_parms_sft",
            "Plant_parms_sft",
            "change.py",
            _manual_block(
                "header",
                _manual_field("name", "character"),
                _manual_field("plants", "integer"),
                _manual_field("parms", "integer"),
                _manual_field("nspu", "integer"),
            ),
            _manual_block(
                "items",
                _manual_field("var", "character"),
                _manual_field("name", "character"),
                _manual_field("init", "real"),
                _manual_field("chg_typ", "character"),
                _manual_field("neg", "real"),
                _manual_field("pos", "real"),
                _manual_field("lo", "real"),
                _manual_field("up", "real"),
            ),
        )

    if "salt_hru_ini_cs" in available:
        overrides["salt_hru_ini_cs"] = schema(
            "salt_hru_ini_cs",
            "Salt_hru_ini_cs",
            "salts.py",
            _manual_block(
                "rows",
                _manual_field("name", "character"),
                _manual_field("so4", "real"),
                _manual_field("ca", "real"),
                _manual_field("mg", "real"),
                _manual_field("na", "real"),
                _manual_field("k", "real"),
                _manual_field("cl", "real"),
                _manual_field("co3", "real"),
                _manual_field("hco3", "real"),
            ),
        )

    if "soils_sol" in available:
        overrides["soils_sol"] = schema(
            "soils_sol",
            "Soils_sol",
            "soils.py",
            _manual_block(
                "header",
                _manual_field("name", "character"),
                _manual_field("nly", "integer"),
                _manual_field("hyd_grp", "character"),
                _manual_field("dp_tot", "real"),
                _manual_field("anion_excl", "real"),
                _manual_field("perc_crk", "real"),
                _manual_field("texture", "character"),
            ),
            _manual_block(
                "layers",
                _manual_field("dp", "real"),
                _manual_field("bd", "real"),
                _manual_field("awc", "real"),
                _manual_field("soil_k", "real"),
                _manual_field("carbon", "real"),
                _manual_field("clay", "real"),
                _manual_field("silt", "real"),
                _manual_field("sand", "real"),
                _manual_field("rock", "real"),
                _manual_field("alb", "real"),
                _manual_field("usle_k", "real"),
                _manual_field("ec", "real"),
                _manual_field("caco3", "real"),
                _manual_field("ph", "real"),
            ),
        )

    return overrides


def _attr_name(node: ast.AST) -> str | None:
    if isinstance(node, ast.Attribute):
        parent = _attr_name(node.value)
        return f"{parent}.{node.attr}" if parent else node.attr
    if isinstance(node, ast.Name):
        return node.id
    return None


def _call_name(node: ast.Call) -> str:
    name = _attr_name(node.func)
    return name.rsplit(".", 1)[-1] if name else ""


def _literal(node: ast.AST | None) -> Any:
    return node.value if isinstance(node, ast.Constant) else None


def _keyword(call: ast.Call, name: str) -> ast.AST | None:
    return next((kw.value for kw in call.keywords if kw.arg == name), None)


def _bool_keyword(call: ast.Call, name: str) -> bool:
    return bool(_literal(_keyword(call, name)))


def _string_label(node: ast.AST) -> str | None:
    value = _literal(node)
    if isinstance(value, str):
        return value
    if isinstance(node, ast.Name):
        return node.id
    if isinstance(node, ast.JoinedStr):
        text = "".join(
            part.value for part in node.values if isinstance(part, ast.Constant) and isinstance(part.value, str)
        )
        return text or "runtime_value"
    if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute):
        base = _literal(node.func.value)
        if isinstance(base, str) and node.func.attr == "format":
            return re.sub(r"\{[^}]*\}", "", base) or base
    return None


def _field_kind(field: Any, *, serialized_foreign_key: bool = False) -> tuple[str, bool]:
    name = type(field).__name__
    if name in {"IntegerField", "AutoField", "BigIntegerField", "SmallIntegerField"}:
        return "integer", True
    if name in {"DoubleField", "FloatField", "DecimalField"}:
        return "real", True
    if name == "BooleanField":
        return "character", False
    if name == "ForeignKeyField":
        return ("character", False) if serialized_foreign_key else ("integer", True)
    return "character", False


def _padding_kind(call_name: str) -> tuple[str, bool]:
    if call_name in {"int_pad", "write_int"}:
        return "integer", True
    if call_name in {"num_pad", "exp_pad", "write_num"}:
        return "real", True
    return "character", False


def _model_field(
    expression: str | None,
    primary_model: type[Any],
    models_by_class: dict[str, type[Any]],
) -> Any | None:
    if not expression:
        return None
    parts = expression.split(".")
    field_name = parts[-1]
    if len(parts) >= 2 and parts[-2] in models_by_class:
        return models_by_class[parts[-2]]._meta.fields.get(field_name)
    return primary_model._meta.fields.get(field_name)


def _writer_model_scope(
    write_node: ast.FunctionDef,
    models_by_class: dict[str, type[Any]],
) -> dict[str, type[Any]]:
    scope = dict(models_by_class)
    for node in ast.walk(write_node):
        if not isinstance(node, ast.Assign) or not isinstance(node.value, ast.Attribute):
            continue
        model = models_by_class.get(node.value.attr)
        if model is None:
            continue
        for target in node.targets:
            if isinstance(target, ast.Name):
                scope[target.id] = model
    return scope

def _alias_types(
    write_node: ast.FunctionDef,
    primary_model: type[Any],
    models_by_class: dict[str, type[Any]],
) -> dict[str, tuple[str, bool]]:
    aliases: dict[str, tuple[str, bool]] = {}
    for call in (node for node in ast.walk(write_node) if isinstance(node, ast.Call)):
        if not isinstance(call.func, ast.Attribute) or call.func.attr != "alias" or not call.args:
            continue
        alias = _literal(call.args[0])
        if not isinstance(alias, str):
            continue
        expression = _attr_name(call.func.value)
        field = _model_field(expression, primary_model, models_by_class)
        if field is not None:
            aliases[alias] = _field_kind(field, serialized_foreign_key=True)
        elif expression and expression.endswith(".name"):
            aliases[alias] = ("character", False)
    return aliases


def _parse_col(
    call: ast.Call,
    primary_model: type[Any],
    models_by_class: dict[str, type[Any]],
    aliases: dict[str, tuple[str, bool]],
    *,
    manual_row: bool,
    repeated: bool = False,
) -> EffectiveField | None:
    if _call_name(call) not in {"col", "FileColumn"} or not call.args:
        return None
    source_node = call.args[0]
    source_expression = _attr_name(source_node)
    source_field = _model_field(source_expression, primary_model, models_by_class)
    query_alias = _literal(_keyword(call, "query_alias"))
    alt_header = _literal(_keyword(call, "alt_header_name"))
    is_desc = _bool_keyword(call, "is_desc")
    if source_field is not None and source_field.name in {"desc", "description"}:
        is_desc = True
    if is_desc:
        return None

    if source_field is not None:
        name = source_field.name
        if isinstance(alt_header, str) and alt_header:
            name = alt_header
        elif isinstance(query_alias, str) and query_alias:
            name = query_alias
        elif source_field.verbose_name:
            name = source_field.verbose_name

        if _bool_keyword(call, "force_bool_type"):
            field_type, numeric = "character", False
        elif isinstance(query_alias, str) and query_alias in aliases:
            field_type, numeric = aliases[query_alias]
        else:
            field_type, numeric = _field_kind(
                source_field,
                serialized_foreign_key=manual_row,
            )
        return EffectiveField(
            name=str(name).lower(),
            field_type=field_type,
            numeric=numeric,
            position=0,
            source=source_expression,
            repeated=repeated,
        )

    name = _string_label(source_node)
    if not name or not name.strip():
        return None
    value_override = _literal(_keyword(call, "value_override"))
    normalized_name = name.lower()
    if isinstance(value_override, bool) or _bool_keyword(call, "force_bool_type"):
        field_type, numeric = "character", False
    elif isinstance(value_override, int):
        field_type, numeric = "integer", True
    elif isinstance(value_override, float):
        field_type, numeric = "real", True
    elif isinstance(value_override, str):
        field_type, numeric = "character", False
    elif normalized_name in INTEGER_LITERAL_FIELDS:
        field_type, numeric = "integer", True
    elif normalized_name in REAL_LITERAL_FIELDS:
        field_type, numeric = "real", True
    elif normalized_name in CHARACTER_LITERAL_FIELDS:
        field_type, numeric = "character", False
    else:
        field_type, numeric = "unknown", False
    return EffectiveField(
        name=name.lower(),
        field_type=field_type,
        numeric=numeric,
        position=0,
        source=source_expression or "literal_or_computed",
        repeated=repeated,
    )


def _renumber(fields: Iterable[EffectiveField]) -> tuple[EffectiveField, ...]:
    return tuple(
        EffectiveField(
            name=field.name,
            field_type=field.field_type,
            numeric=field.numeric,
            position=position,
            source=field.source,
            repeated=field.repeated,
        )
        for position, field in enumerate(fields)
    )


def _default_block(
    model: type[Any],
    call: ast.Call,
    aliases: dict[str, tuple[str, bool]],
) -> EffectiveBlock:
    ignore_id = False
    if len(call.args) >= 2 and isinstance(call.args[1], ast.Constant):
        ignore_id = bool(call.args[1].value)
    keyword_ignore = _keyword(call, "ignore_id_col")
    if isinstance(keyword_ignore, ast.Constant):
        ignore_id = bool(keyword_ignore.value)

    ignored: set[str] = set()
    ignored_node = _keyword(call, "ignored_cols")
    if isinstance(ignored_node, (ast.List, ast.Tuple, ast.Set)):
        ignored = {
            value.value
            for value in ignored_node.elts
            if isinstance(value, ast.Constant) and isinstance(value.value, str)
        }

    fields: list[EffectiveField] = []
    for field in model._meta.sorted_fields:
        if ignore_id and field.name == "id":
            continue
        if field.name in ignored or field.name in {"desc", "description"}:
            continue
        field_type, numeric = aliases.get(field.name, _field_kind(field))
        fields.append(
            EffectiveField(
                name=str(field.verbose_name or field.name).lower(),
                field_type=field_type,
                numeric=numeric,
                position=0,
                source=f"{model.__name__}.{field.name}",
            )
        )
    return EffectiveBlock(name="rows", fields=_renumber(fields), source_line=call.lineno)


def _parent_map(node: ast.AST) -> dict[ast.AST, ast.AST]:
    return {child: parent for parent in ast.walk(node) for child in ast.iter_child_nodes(parent)}


def _inside_loop(node: ast.AST, parents: dict[ast.AST, ast.AST]) -> bool:
    parent = parents.get(node)
    while parent is not None:
        if isinstance(parent, (ast.For, ast.While, ast.comprehension)):
            return True
        parent = parents.get(parent)
    return False


def _col_blocks(
    write_node: ast.FunctionDef,
    primary_model: type[Any],
    models_by_class: dict[str, type[Any]],
) -> tuple[EffectiveBlock, ...]:
    model_scope = _writer_model_scope(write_node, models_by_class)
    aliases = _alias_types(write_node, primary_model, model_scope)
    parents = _parent_map(write_node)
    assignments: dict[str, list[tuple[ast.List | ast.Tuple, int]]] = {}
    for node in ast.walk(write_node):
        if not isinstance(node, ast.Assign) or len(node.targets) != 1:
            continue
        if not isinstance(node.targets[0], ast.Name) or not isinstance(node.value, (ast.List, ast.Tuple)):
            continue
        assignments.setdefault(node.targets[0].id, []).append((node.value, node.lineno))

    uses: list[tuple[int, str, bool]] = []
    for call in (node for node in ast.walk(write_node) if isinstance(node, ast.Call)):
        call_name = _call_name(call)
        if call_name == "write_headers" and len(call.args) >= 2 and isinstance(call.args[1], ast.Name):
            uses.append((call.lineno, call.args[1].id, True))
        elif call_name == "write_query" and len(call.args) >= 2 and isinstance(call.args[1], ast.Name):
            uses.append((call.lineno, call.args[1].id, False))

    blocks: list[EffectiveBlock] = []
    seen: set[tuple[str, int]] = set()
    for use_line, variable, manual_row in sorted(uses):
        options = [value for value in assignments.get(variable, []) if value[1] <= use_line]
        if not options:
            continue
        list_node, source_line = max(options, key=lambda value: value[1])
        assignment_key = (variable, source_line)
        if assignment_key in seen:
            continue
        seen.add(assignment_key)
        next_assignment_line = min(
            (line for _, line in assignments[variable] if line > source_line),
            default=10**9,
        )
        fields: list[EffectiveField] = []
        for element in list_node.elts:
            if isinstance(element, ast.Call):
                field = _parse_col(
                    element,
                    primary_model,
                    model_scope,
                    aliases,
                    manual_row=manual_row,
                )
                if field is not None:
                    fields.append(field)

        append_calls = [
            call
            for call in ast.walk(write_node)
            if isinstance(call, ast.Call)
            and isinstance(call.func, ast.Attribute)
            and call.func.attr == "append"
            and isinstance(call.func.value, ast.Name)
            and call.func.value.id == variable
            and source_line <= call.lineno < next_assignment_line
            and call.args
            and isinstance(call.args[0], ast.Call)
        ]
        for append_call in sorted(append_calls, key=lambda item: item.lineno):
            field = _parse_col(
                append_call.args[0],
                primary_model,
                models_by_class,
                aliases,
                manual_row=manual_row,
                repeated=_inside_loop(append_call, parents),
            )
            if field is not None:
                fields.append(field)

        if fields:
            blocks.append(
                EffectiveBlock(
                    name=_block_name(variable, len(blocks)),
                    fields=_renumber(fields),
                    source_line=source_line,
                )
            )
    return tuple(blocks)


def _block_name(variable: str, index: int) -> str:
    value = variable.lower()
    if "cond" in value:
        return "condition"
    if "act" in value:
        return "action"
    if "table_header" in value or (index == 0 and "header" in value):
        return "header"
    return re.sub(r"_(header_)?cols$", "", value) or f"block_{index + 1}"


def _contains_file_write(node: ast.AST) -> bool:
    return any(
        isinstance(child, ast.Call)
        and isinstance(child.func, ast.Attribute)
        and child.func.attr == "write"
        for child in ast.walk(node)
    )


def _direct_header_block(function: ast.FunctionDef) -> EffectiveBlock | None:
    data_loop_lines = [
        node.lineno
        for node in ast.walk(function)
        if isinstance(node, (ast.For, ast.While)) and _contains_file_write(node)
    ]
    first_data_loop = min(data_loop_lines, default=10**9)
    parents = _parent_map(function)
    fields: list[EffectiveField] = []
    for call in sorted(
        (node for node in ast.walk(function) if isinstance(node, ast.Call)),
        key=lambda node: node.lineno,
    ):
        if call.lineno >= first_data_loop or not call.args:
            continue
        call_name = _call_name(call)
        if call_name not in {
            "int_pad",
            "num_pad",
            "exp_pad",
            "string_pad",
            "code_pad",
            "key_name_pad",
            "write_int",
            "write_num",
            "write_string",
            "write_code",
        }:
            continue
        label = _string_label(call.args[0])
        if not label:
            continue
        field_type, numeric = _padding_kind(call_name)
        repeated = False
        parent = parents.get(call)
        while parent is not None:
            if isinstance(parent, ast.If) and "has_con_out" in ast.unparse(
                parent.test
            ):
                repeated = True
                break
            parent = parents.get(parent)
        fields.append(
            EffectiveField(
                name=label.lower(),
                field_type=field_type,
                numeric=numeric,
                position=0,
                source="writer_literal",
                repeated=repeated,
            )
        )
    if not fields:
        return None
    return EffectiveBlock(name="rows", fields=_renumber(fields), source_line=function.lineno)


def _model_references(write_node: ast.FunctionDef) -> set[str]:
    refs: set[str] = set()
    for node in ast.walk(write_node):
        if isinstance(node, ast.Assign) and isinstance(node.value, ast.Attribute):
            if any(isinstance(target, ast.Name) and target.id == "table" for target in node.targets):
                refs.add(node.value.attr)
        if not isinstance(node, ast.Call):
            continue
        name = _call_name(node)
        if name in {"write_default_table", "write_custom_query_table"} and node.args:
            expression = _attr_name(node.args[0])
            if expression:
                refs.add(expression.rsplit(".", 1)[-1])
        if name == "write_con_table" and len(node.args) >= 3:
            expression = _attr_name(node.args[2])
            if expression:
                refs.add(expression.rsplit(".", 1)[-1])
    return refs


def _schema_for_class(
    path: Path,
    class_node: ast.ClassDef,
    functions: dict[str, ast.FunctionDef],
    models_by_class: dict[str, type[Any]],
) -> list[tuple[str, EffectiveFileSchema, int]]:
    write_node = next(
        (
            node
            for node in class_node.body
            if isinstance(node, ast.FunctionDef) and node.name == "write"
        ),
        None,
    )
    if write_node is None:
        return []
    refs = _model_references(write_node)
    if class_node.name in models_by_class:
        refs.add(class_node.name)
    primary_name = class_node.name if class_node.name in models_by_class else next(
        (name for name in refs if name in models_by_class),
        None,
    )
    if primary_name is None:
        return []
    primary_model = models_by_class[primary_name]

    default_call = next(
        (
            node
            for node in ast.walk(write_node)
            if isinstance(node, ast.Call)
            and _call_name(node) in {"write_default_table", "write_custom_query_table"}
        ),
        None,
    )
    blocks = _col_blocks(write_node, primary_model, models_by_class)
    extraction = "writer_column_blocks"
    confidence = "high"
    rank = 30
    if not blocks and default_call is not None:
        blocks = (
            _default_block(
                primary_model,
                default_call,
                _alias_types(
                    write_node,
                    primary_model,
                    _writer_model_scope(write_node, models_by_class),
                ),
            ),
        )
        extraction = "writer_default_table"
        rank = 20
    if not blocks:
        helper_call = next(
            (
                node
                for node in ast.walk(write_node)
                if isinstance(node, ast.Call) and _call_name(node) == "write_con_table"
            ),
            None,
        )
        helper = functions.get("write_header") if helper_call is not None else None
        direct = _direct_header_block(helper or write_node)
        if direct is not None:
            blocks = (direct,)
            extraction = "writer_direct_header"
            confidence = "medium"
            rank = 15
    if not blocks:
        return []

    schemas: list[tuple[str, EffectiveFileSchema, int]] = []
    for ref in refs:
        model = models_by_class.get(ref)
        if model is None:
            continue
        schema = EffectiveFileSchema(
            table_name=model._meta.table_name,
            model_class=model.__name__,
            source_module=model.__module__,
            writer_class=class_node.name,
            writer_module=path.name,
            extraction=extraction,
            confidence=confidence,
            blocks=blocks,
        )
        candidate_rank = rank + (10 if class_node.name == ref else 0)
        schemas.append((model._meta.table_name, schema, candidate_rank))
    return schemas


def _fallback_schema(model: type[Any]) -> EffectiveFileSchema:
    fields: list[EffectiveField] = []
    for field in model._meta.sorted_fields:
        if field.name == "id" or field.name in {"desc", "description"}:
            continue
        field_type, numeric = _field_kind(field)
        fields.append(
            EffectiveField(
                name=field.name,
                field_type=field_type,
                numeric=numeric,
                position=0,
                source=f"{model.__name__}.{field.name}",
            )
        )
    return EffectiveFileSchema(
        table_name=model._meta.table_name,
        model_class=model.__name__,
        source_module=model.__module__,
        writer_class=None,
        writer_module=None,
        extraction="model_fallback",
        confidence="low",
        blocks=(EffectiveBlock(name="rows", fields=_renumber(fields)),),
    )


def extract_editor_effective_schemas(
    editor_root: Path,
    models: dict[str, type[Any]],
) -> tuple[dict[str, EffectiveFileSchema], dict[str, int]]:
    """Return one best-effort serialized schema for every imported Editor table."""

    models_by_class = {model.__name__: model for model in models.values()}
    candidates: dict[str, list[tuple[EffectiveFileSchema, int]]] = {}
    fileio_root = editor_root / "src" / "api" / "fileio"
    for path in sorted(fileio_root.glob("*.py")):
        if path.name in {"__init__.py", "base.py"}:
            continue
        try:
            tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
        except SyntaxError:
            continue
        functions = {
            node.name: node for node in tree.body if isinstance(node, ast.FunctionDef)
        }
        for class_node in (node for node in tree.body if isinstance(node, ast.ClassDef)):
            for table_name, schema, rank in _schema_for_class(
                path,
                class_node,
                functions,
                models_by_class,
            ):
                candidates.setdefault(table_name, []).append((schema, rank))

    schemas: dict[str, EffectiveFileSchema] = {}
    for table_name, model in models.items():
        options = candidates.get(table_name, [])
        if options:
            schemas[table_name] = max(options, key=lambda item: item[1])[0]
        else:
            schemas[table_name] = _fallback_schema(model)

    schemas.update(_canonical_editor_schema_overrides(models))

    stats: dict[str, int] = {}
    for schema in schemas.values():
        stats[schema.extraction] = stats.get(schema.extraction, 0) + 1
    return schemas, stats
