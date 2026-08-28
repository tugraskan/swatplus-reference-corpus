# Parameter Range Crosswalk: SWAT+ 62.0.0

Ranges carried from `modular_database_rev_61_0_nbs.csv` onto the official input schema by translating
spreadsheet (Editor) names into official Fortran names through the existing
editor-schema report.

| Outcome | Count |
|---|---:|
| Applied to schema | 444 |
| Drift - name no longer in schema | 15 |
| Needs review - no Editor pairing | 13 |
| Quarantined - range contradicts the row | 14 |
| Not applicable - file outside the input schema | 526 |

Applicable rows: 486. Applied: 444.

## Drift

The spreadsheet names a parameter the current schema no longer has. These are the genuine rename or removal candidates and need a human decision.

| File | Name | Min | Max | Code | Detail |
|---|---|---:|---:|---|---|
| `aquifer.con` | `obj_numb` | 1 | 10 | `name_not_in_schema` | No official field matches this spreadsheet name. |
| `chandeg.con` | `obj_numb` | 1 | 10 | `name_not_in_schema` | No official field matches this spreadsheet name. |
| `channel.con` | `obj_numb` | 1 | 10 | `name_not_in_schema` | No official field matches this spreadsheet name. |
| `codes.bsn` | `i_fpwet` | 0 | 1 | `name_not_in_schema` | No official field matches this spreadsheet name. |
| `codes.bsn` | `rtu_wq` | 0 | 1 | `name_not_in_schema` | No official field matches this spreadsheet name. |
| `delratio.con` | `obj_numb` | 1 | 10 | `name_not_in_schema` | No official field matches this spreadsheet name. |
| `exco.con` | `obj_numb` | 1 | 10 | `name_not_in_schema` | No official field matches this spreadsheet name. |
| `hru-lte.con` | `obj_numb` | 1 | 10 | `name_not_in_schema` | No official field matches this spreadsheet name. |
| `hru.con` | `obj_numb` | 1 | 10 | `name_not_in_schema` | No official field matches this spreadsheet name. |
| `ls_unit.def` | `elem_numb` | 1 | 10 | `name_not_in_schema` | No official field matches this spreadsheet name. |
| `reservoir.con` | `obj_numb` | 1 | 10 | `name_not_in_schema` | No official field matches this spreadsheet name. |
| `rout_unit.con` | `obj_numb` | 1 | 10 | `name_not_in_schema` | No official field matches this spreadsheet name. |
| `soils.sol` | `lay_numb` | 1 | 10 | `name_not_in_schema` | No official field matches this spreadsheet name. |
| `weather-wgn.cli` | `month` | 0 | 12 | `name_not_in_schema` | No official field matches this spreadsheet name. |
| `weir.res` | `numb_steps` | 1 | 24 | `name_not_in_schema` | No official field matches this spreadsheet name. |

## Needs review

These files have no Editor pairing to translate through. Column position lines the two sides up only when no field was inserted upstream, so nothing is applied automatically here.

| File | Name | Min | Max | Code | Detail |
|---|---|---:|---:|---|---|
| `aqu_cha.lin` | `elem_numb` | 1 | 10 | `no_editor_mapping` | This file has no Editor pairing, so the name could not be translated. |
| `cntable.lum` | `cn_a` | 30 | 100 | `no_editor_mapping` | This file has no Editor pairing, so the name could not be translated. |
| `cntable.lum` | `cn_b` | 30 | 100 | `no_editor_mapping` | This file has no Editor pairing, so the name could not be translated. |
| `cntable.lum` | `cn_c` | 30 | 100 | `no_editor_mapping` | This file has no Editor pairing, so the name could not be translated. |
| `cntable.lum` | `cn_d` | 30 | 100 | `no_editor_mapping` | This file has no Editor pairing, so the name could not be translated. |
| `outlet.con` | `obj_numb` | 1 | 10 | `no_editor_mapping` | This file has no Editor pairing, so the name could not be translated. |
| `pesticide.pes` | `frac_wash` | 0 | 1 | `no_editor_mapping` | This file has no Editor pairing, so the name could not be translated. |
| `pesticide.pes` | `hl_foliage` | 0 | 10000 | `no_editor_mapping` | This file has no Editor pairing, so the name could not be translated. |
| `pesticide.pes` | `hl_soil` | 0 | 100000 | `no_editor_mapping` | This file has no Editor pairing, so the name could not be translated. |
| `pesticide.pes` | `soil_ads` | 1 | 1e+09 | `no_editor_mapping` | This file has no Editor pairing, so the name could not be translated. |
| `recall.con` | `obj_numb` | 1 | 10 | `no_editor_mapping` | This file has no Editor pairing, so the name could not be translated. |
| `rout_unit.def` | `elem_numb` | 1 | 10 | `no_editor_mapping` | This file has no Editor pairing, so the name could not be translated. |
| `sed_nut.cha` | `part_size` | 1.1 | 1.9 | `no_editor_mapping` | This file has no Editor pairing, so the name could not be translated. |

## Quarantined

A name resolved, but the range contradicts the row's own units, description, or field type. A wrong range is worse than a missing one, so these are withheld.

| File | Name | Min | Max | Code | Detail |
|---|---|---:|---:|---|---|
| `codes.sft` | `chnut` | 0 | 8 | `range_on_non_numeric_field` | The schema marks this field non-numeric, so a numeric range cannot apply. |
| `codes.sft` | `chsed` | 0 | 3500 | `range_on_non_numeric_field` | The schema marks this field non-numeric, so a numeric range cannot apply. |
| `codes.sft` | `res` | 0 | 1000 | `range_on_non_numeric_field` | The schema marks this field non-numeric, so a numeric range cannot apply. |
| `codes.sft` | `sed` | 1 |  | `range_on_non_numeric_field` | The schema marks this field non-numeric, so a numeric range cannot apply. |
| `filterstrip.str` | `vfsch` | 0 | 100 | `fraction_bound_conflict` | Row is described as a fraction but the maximum is 100.0. |
| `fire.ops` | `fr_burn` | 0 | 100 | `fraction_bound_conflict` | Row is described as a fraction but the maximum is 100.0. |
| `hydrology.hyd` | `latq_co` | 0 | 0 | `placeholder_zero_range` | Both bounds are 0; a placeholder, not a range. |
| `irr.ops` | `surq` | 0 | 100 | `fraction_bound_conflict` | Row is described as a fraction but the maximum is 100.0. |
| `landuse.lum` | `cons_prac` | 0 | 1 | `range_on_non_numeric_field` | The schema marks this field non-numeric, so a numeric range cannot apply. |
| `object.cnt` | `name` | 0 |  | `range_on_non_numeric_field` | The schema marks this field non-numeric, so a numeric range cannot apply. |
| `parameters.bsn` | `ffcb` | 1 | 24 | `fraction_bound_conflict` | Row is described as a fraction but the maximum is 24.0. |
| `plants.plt` | `hvsti` | 0.01 | 1.25 | `fraction_bound_conflict` | Row is described as a fraction but the maximum is 1.25. |
| `print.prt` | `yrc_start` | 0 | 0 | `placeholder_zero_range` | Both bounds are 0; a placeholder, not a range. |
| `sed_nut.cha` | `order` | 0 | 4 | `range_on_non_numeric_field` | The schema marks this field non-numeric, so a numeric range cannot apply. |

