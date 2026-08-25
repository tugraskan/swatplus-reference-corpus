---
kind: io
source_symbols:
- cal_parmchg_read
title: '`calibration.cal`'
status: filled
source_hash: f2c4aed98262412c
version_label: SWAT+ 62.0.0
---

**Primary target:** `cal_upd(:)` (array of `type update_parameters`)  
**Read by:** [sym:cal_parmchg_read]

## Bottom Line

`calibration.cal` is the hard-calibration parameter-change file. Each record names a model parameter (crosswalked to `cal_parms`), the type and magnitude of change to apply, the soil-layer / year / day ranges over which it applies, and the spatial objects it targets.

The reader `cal_parmchg_read` reads a title line, the record count `mcal`, and a column-header line, then loops `mcal` times reading each record into `cal_upd(i)` (an array of `type update_parameters`). A record's main line may continue with a target-object list, and may be followed by `conds` condition lines.

If `in_chg%cal_upd` is missing or set to `"null"`, `cal_upd` is allocated with zero size and no calibration changes are applied.

| Module | Role for this file |
| --- | --- |
| [sym:input_file_module] | Supplies `in_chg`; `in_chg%cal_upd` holds the `calibration.cal` filename opened on unit 107. |
| [sym:maximum_data_module] | Supplies `db_mx`; the reader crosswalks each parameter name against `db_mx%cal_parms` and stores the record count in `db_mx%cal_upd`. |
| [sym:calibration_data_module] | Defines `type update_parameters` and the `cal_upd` array each record is read into, plus `cal_parms` used to resolve parameter names. |
| [sym:hydrograph_module] | Supplies `sp_ob` object counts (hru, aqu, cha, res, ...) used to size `cal_upd%num_elem` when a record targets all objects of a type. |
| [sym:gwflow_module] | Supplies `ncell` (groundwater cell count), used as the element count for `gwf` (gwflow) parameters that default to all cells. |

## File Variables

`calibration.cal` is a block-structured, whitespace-delimited file. After a title line, an integer record count (`mcal`), and a column-header line, it contains `mcal` parameter records. Each record's main line lists the parameter name, change type and value, condition count, soil-layer / year / day ranges, and a spatial-unit count `nspu`; when `nspu > 0` the same line continues with the total element count and the object/element list. Each record may then be followed by `conds` condition lines (a numeric `range` condition, or a full conditional record). The reader stores each record in `cal_upd(i)` and resolves the parameter name against `cal_parms`.

| Col | Header | Target | Type | Units | Meaning |
| --- | --- | --- | --- | --- | --- |
| - | `record count` | `mcal` | integer |  | Number of parameter-change records (`mcal`) in the file; `cal_upd` is allocated to this size. |
| 1 | `name` | `cal_upd%name` | character(len=25) |  | Parameter name; crosswalks to a row in `cal_parms` (calibration parameter database). |
| 2 | `chg_typ` | `cal_upd%chg_typ` | character(len=16) |  | Type of change: `absval`, `abschg`, `pctchg`, or `relchg`. |
| 3 | `val` | `cal_upd%val` | real |  | Value of the change applied to the parameter. |
| 4 | `conds` | `cal_upd%conds` | integer |  | Number of condition lines that follow this record. |
| 5 | `lyr1` | `cal_upd%lyr1` | integer |  | First soil layer in range (0 = all layers). |
| 6 | `lyr2` | `cal_upd%lyr2` | integer |  | Last soil layer in range (0 = through last layer). |
| 7 | `year1` | `cal_upd%year1` | integer |  | First year (for precip/temp parameters). |
| 8 | `year2` | `cal_upd%year2` | integer |  | Last year. |
| 9 | `day1` | `cal_upd%day1` | integer |  | First day in range. |
| 10 | `day2` | `cal_upd%day2` | integer |  | Last day in range. |
| 11 | `nspu` | `nspu` | integer |  | Number of spatial-unit (object) groups; if > 0 the line continues with `num_tot` and the element list. |
| 12 | `num_tot` | `cal_upd%num_tot` | integer |  | Total number of integers in the element list (read only when `nspu > 0`). |
| 13 | `elem_cnt` | `elem_cnt(1:nspu)` | integer |  | Object/element specification list, expanded by `define_unit_elements` into `cal_upd%num`. |
| 1 | `range` | `range` | character(len=10) |  | Literal `range` marks a numeric-range condition; otherwise the line is a full conditional record. |
| 2 | `var` | `cal_upd%cond%var` | character(len=25) |  | Condition variable name (range condition). |
| 3 | `val1` | `cal_upd%val1` | real |  | Lower bound of the numeric range condition. |
| 4 | `val2` | `cal_upd%val2` | real |  | Upper bound of the numeric range condition. |
| - | `cond` | `cal_upd%cond(icond)` | calibration_conditions |  | Full conditional record (`var`, `alt`, `targ`, `targc`) read when the line does not start with `range`. |

## Sample

```text
Schematic of the record layout (field names in read order, not a specific dataset):

<title line>
3                                                 ! mcal: number of parameter records
name   chg_typ  val    conds lyr1 lyr2 year1 year2 day1 day2 nspu [num_tot elem_cnt...]
cn2    pctchg  -10.0     0     0    0     0     0     0    0    0
esco   absval    0.50    0     0    0     0     0     0    0    1     3   1 -5 18
awc    relchg    0.10    1     1    2     0     0     0    0    0
range  slope     0.0     5.0                       ! one condition line for the awc record
```

## Read Pattern

```fortran
open (107,file=in_chg%cal_upd)
read (107,*,iostat=eof) titldum
read (107,*,iostat=eof) mcal
read (107,*,iostat=eof) header
read (107,*,iostat=eof) cal_upd(i)%name, cal_upd(i)%chg_typ, cal_upd(i)%val, cal_upd(i)%conds, cal_upd(i)%lyr1, cal_upd(i)%lyr2, cal_upd(i)%year1, cal_upd(i)%year2, cal_upd(i)%day1, cal_upd(i)%day2, nspu
backspace (107)
read (107,*,iostat=eof) cal_upd(i)%name, cal_upd(i)%chg_typ, cal_upd(i)%val, cal_upd(i)%conds, cal_upd(i)%lyr1, cal_upd(i)%lyr2, cal_upd(i)%year1, cal_upd(i)%year2, cal_upd(i)%day1, cal_upd(i)%day2, cal_upd(i)%num_tot, (elem_cnt(isp), isp = 1, nspu)
read (107,*,iostat=eof) range
read (107,*,iostat=eof) range, cal_upd(i)%cond(icond)%var, cal_upd(i)%val1, cal_upd(i)%val2
read (107,*,iostat=eof) cal_upd(i)%cond(icond)
```

## I/O Operations

| Direction | Op | Unit | Statement |
| --- | --- | --- | --- |
| File setup | `open` | 107 | `open (107,file=in_chg%cal_upd)` |
| Input | `read` | 107 | `read (107,*,iostat=eof) titldum` |
| Input | `read` | 107 | `read (107,*,iostat=eof) mcal` |
| Input | `read` | 107 | `read (107,*,iostat=eof) header` |
| Input | `read` | 107 | `read (107,*,iostat=eof) cal_upd(i)%name, cal_upd(i)%chg_typ, cal_upd(i)%val, cal_upd(i)%conds, cal_upd(i)%lyr1, cal_upd(i)%lyr2, cal_upd(i)%year1, cal_upd(i)%year2, cal_upd(i)%day1, cal_upd(i)%day2, nspu` |
| File control | `backspace` | 107 | `backspace (107)` |
| Input | `read` | 107 | `read (107,*,iostat=eof) cal_upd(i)%name, cal_upd(i)%chg_typ, cal_upd(i)%val, cal_upd(i)%conds, cal_upd(i)%lyr1, cal_upd(i)%lyr2, cal_upd(i)%year1, cal_upd(i)%year2, cal_upd(i)%day1, cal_upd(i)%day2, cal_upd(i)%num_tot, (elem_cnt(isp), isp = 1, nspu)` |
| Input | `read` | 107 | `read (107,*,iostat=eof) range` |
| File control | `backspace` | 107 | `backspace (107)` |
| Input | `read` | 107 | `read (107,*,iostat=eof) range, cal_upd(i)%cond(icond)%var, cal_upd(i)%val1, cal_upd(i)%val2` |
| Input | `read` | 107 | `read (107,*,iostat=eof) cal_upd(i)%cond(icond)` |

## Readers

| Procedure | Operations | Role |
| --- | --- | --- |
| [sym:cal_parmchg_read] | backspace, open, read | Opens `calibration.cal` on unit 107, reads the title line, the record count `mcal`, and the column header, then loops `mcal` times reading each parameter record into `cal_upd(i)`. For records with `nspu > 0` it backspaces and re-reads the line to capture `num_tot` and the element list; it crosswalks the parameter name against `cal_parms`, reads any condition lines, and resolves the target object set into `cal_upd%num`. |

## Review Notes

- Each record's main line is read twice: first to get `nspu`, then (via `backspace`) re-read with `num_tot` and the element list when `nspu > 0` (cal_parmchg_read.f90:68-77).
- `chg_typ` accepts `absval`, `abschg`, `pctchg`, or `relchg` (see chg_par.f90).
- The parameter `name` must crosswalk to a `name` in the calibration parameter database (`cal_parms`); an unmatched name leaves `num_db = 0`.
- When `conds > 0`, each condition line is either a numeric `range` condition (`range var val1 val2`) or a full conditional record (`var alt targ targc`).
- When a record specifies no objects (`num_tot == 0`), it applies to all objects of the parameter's object type (`sp_ob%...`, `db_mx%...`, or `ncell` for `gwf`).
- If `calibration.cal` is missing or set to `null`, `cal_upd` is allocated with zero size.
