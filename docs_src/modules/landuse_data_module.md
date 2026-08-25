---
kind: module
symbol: landuse_data_module
title: landuse_data_module
status: filled
source_hash: 17d76836bd790f70
version_label: SWAT+ 62.0.0
variables:
  lum: Allocatable array of `land_use_management` records. It stores the text names and pointer
    strings for each land-use management definition loaded from `landuse.lum`, with names
    and links consumed by HRU initialization, decision-table crosswalks, plant setup, and
    output routines.
  lum_str: Allocatable array of `land_use_structures` records. It stores the resolved integer
    indices for the same land-use management rows, converting text pointers into database
    indexes used later by HRU setup, curve-number lookup, conservation practice lookup, and
    structure initialization.
  cn: Allocatable array of `curvenumber_table` records holding curve-number sets. It is populated
    from `cntable.lum` and later indexed by `lum_str(ilum)%cn_lu` during curve-number initialization.
  lum_grp: Single `land_use_mgt_groups` record that stores the number of land-use groups and
    an allocatable group-name list. It is populated when region definitions read group headers
    and is used to resolve `hru(iihru)%lum_group` from `hru(iihru)%lum_group_c`.
  cons_prac: Allocatable array of `conservation_practice_table` records. It is populated from
    `cons_practice.lum` and later indexed by `lum_str(ilum)%cons_prac` to supply USLE P factor
    and maximum slope length.
  overland_n: Allocatable array of `overlandflow_n_table` records. It is populated from `ovn_table.lum`
    and later matched by `lum(ilum)%ovn` when HRU land-use roughness is assigned.
type_components:
  land_use_management:
    name: name of the land use and management (from hru-data.hru pointer)
    cal_group: calibration group (not currently used)
    plant_cov: plant community initialization (pointer to plants.ini)
    mgt_ops: management operations (pointer to management.sch)
    cn_lu: land use for curve number table (pointer to cntable.lum)
    cons_prac: conservation practice from table (cons_practice.lum)
    urb_lu: type of urban land use- ie. residential, industrial, etc (urban.urb)
    urb_ro: urban runoff model
    ovn: '"usgs_reg", simulate using USGS regression eqs

      "buildup_washoff", simulate using build up/wash off alg

      Manning"s "n" land use type for overland flow (ovn_table.lum)'
    tiledrain: tile drainage (pointer to tiledrain.str
    septic: septic tanks (pointer to septic.str)
    fstrip: filter strips (pointer to filterstrip.str)
    grassww: grass waterways (pointer to grassedww.str)
    bmpuser: user specified removal efficiency (pointer to bmpuser.str)
  land_use_structures:
    plant_cov: integer pointer to the plant community record for this land-use entry
    mgt_ops: integer pointer to the management schedule record for this land-use entry
    cn_lu: integer pointer to the curve-number table record for this land-use entry
    cons_prac: integer pointer to the conservation-practice table record for this land-use
      entry
    tiledrain: integer pointer to the tile-drain structure record for this land-use entry
    septic: integer pointer to the septic structure record for this land-use entry
    fstrip: integer pointer to the filter-strip structure record for this land-use entry
    grassww: integer pointer to the grassed-waterway structure record for this land-use entry
    bmpuser: integer pointer to the user-defined BMP structure record for this land-use entry
  curvenumber_table:
    name: name includes abbrev for lu/treatment/condition
    cn: curve number
  land_use_mgt_groups:
    num: number of land-use groups in the current region definition
    name: land use groups
  conservation_practice_table:
    name: name of conservation practice
    pfac: usle p factor
    sl_len_mx: m      !maximum slope length
  overlandflow_n_table:
    name: name of conservation practice
    ovn: overland flow mannings n - mean
    ovn_min: overland flow mannings n - min
    ovn_max: overland flow mannings n - max
type_summaries:
  land_use_management: Text-based land-use management definition for one land-use row. Each
    record names the land-use management entry and points to linked plant, management, curve-number,
    conservation-practice, urban, drainage, septic, filter-strip, grassed-waterway, and BMP-user
    definitions.
  land_use_structures: Resolved integer pointer record for one land-use management row. Each
    component stores the database index of the linked plant, management, curve-number, conservation-practice,
    and structural BMP definitions.
  curvenumber_table: One named curve-number entry containing the four SCS curve-number values
    used for hydrologic soil groups A through D.
  land_use_mgt_groups: Container for the land-use management group names read from region
    definitions, along with the number of groups present.
  conservation_practice_table: Named conservation-practice entry holding erosion-control parameters
    used when assigning USLE support factors and slope-length limits.
  overlandflow_n_table: Named overland-flow roughness entry holding mean, minimum, and maximum
    Manning's n values for land-use roughness lookup.
---

<!-- facts:header -->

Defines the shared land-use database state used across SWAT+ HRU setup, decision-table crosswalks, curve-number initialization, structural BMP setup, and regional land-use output. The module owns the land-use management records, their resolved integer pointers, and the small lookup tables for curve number, conservation practice, land-use groups, and overland-flow Manning's n. It is a declaration container only; the reader routines in other files allocate and populate the arrays.

## Contained Procedures And Types

<!-- facts:members -->

## Module Variables

<!-- facts:variables -->

## Derived Types

<!-- facts:types -->



## Initialization

This module is only a declaration container. It does not contain initialization procedures; separate reader routines allocate and populate the arrays from landuse.lum, cntable.lum, cons_practice.lum, ovn_table.lum, and region-definition files.

## Populated By

| Reader | Input file | Target | Behavior |
| --- | --- | --- | --- |
| [sym:actions] | `unit_2612, unit_3612` | `lum` | Uses land-use management names to match calibration output rows against action targets when accumulating regional crop-yield statistics. |
| [sym:cn2_init] | `hru state and soil group` | `lum_str, cn` | Reads the resolved land-use curve-number pointer from `lum_str` and selects the matching hydrologic-group curve number from `cn`. |
| [sym:cn2_init_all] | `HRU loop context` | `lum_str, cn` | Invokes `cn2_init` for each HRU after importing this module so curve-number lookup can use the shared land-use tables. |
| [sym:cntbl_read] | `cntable.lum` | `cn` | Counts, allocates, and fills the curve-number lookup table into the shared `cn` array. |
| [sym:cons_prac_read] | `cons_practice.lum` | `cons_prac` | Counts, allocates, and fills the conservation-practice lookup table into the shared `cons_prac` array. |
| [sym:dtbl_lum_read] | `lum.dtl` | `lum` | Cross-walks `lu_change` action pointers by matching the action file pointer string against `lum(idb)%name`. |
| [sym:dtbl_res_read] | `res_rel.dtl` | `none from this module` | Reads reservoir decision tables; this module is not referenced in the extracted source snippet, so no direct land-use state use is visible here. |
| [sym:dtbl_scen_read] | `scen_lu.dtl` | `lum` | Cross-walks `lu_change` action pointers to land-use database indexes using `lum(ilum)%name`. |
| [sym:hru_lum_init] | `HRU land-use assignment` | `lum, lum_str, lum_grp` | Copies plant, management, structural BMP, curve-number, and conservation-practice pointers into each HRU and resolves the HRU land-use group. |
| [sym:hru_output] | `unit_2000, unit_2004, unit_2020, unit_2024, unit_2030, unit_2034, unit_2040, unit_2044, unit_2001, unit_2005, unit_2021, unit_2025, unit_2031, unit_2035, unit_2041, unit_2045, unit_2002, unit_2006, unit_2022, unit_2026, unit_2032, unit_2036, unit_2042, unit_2046, unit_2003, unit_2007, unit_2023, unit_2027, unit_2033, unit_2037, unit_2043, unit_2047, unit_4008, unit_4009` | `lum` | Labels HRU output rows with the land-use plant cover and management names from `lum(ilum)`. |
| [sym:hru_read] | `hru-data.hru` | `lum` | Matches HRU land-use management names from the input file against `lum(ilum)%name` to resolve numeric land-use pointers. |
| [sym:hrudb_init] | `HRU database state` | `lum` | Uses `lum(ilu)%cal_group` to convert the resolved land-use index into the HRU calibration-group string. |

## Key Consumers

Downstream routines use this module as the shared land-use database. Some consumers read loaded tables, some translate names into indices, and others apply those indices to HRU setup, structure initialization, curve-number assignment, decision-table crosswalks, and regional outputs.

| Consumer | Uses | Effect |
| --- | --- | --- |
| [sym:hru_lum_init] | `lum`, `lum_str`, `lum_grp` | Resolves an HRU's land-use management into plant cover, management schedule, structural BMP pointers, curve-number and conservation-practice indexes, and the HRU's land-use group. |
| [sym:cn2_init] | landuse_data_module | Selects the curve-number row from the shared land-use tables and stores the HRU's base CN2 before runoff processing continues. |
| [sym:cntbl_read] | landuse_data_module | Allocates and fills the shared curve-number table used later by land-use and hydrologic initialization. |
| [sym:cons_prac_read] | landuse_data_module | Allocates and fills the shared conservation-practice table used later for USLE P-factor and slope-length lookups. |
| [sym:dtbl_lum_read] | landuse_data_module | Uses land-use names from the shared table to convert `lu_change` action pointers into integer land-use database indexes. |
| [sym:dtbl_scen_read] | landuse_data_module | Uses the shared land-use management names to resolve scenario decision-table `lu_change` actions into numeric indexes. |
| [sym:hru_read] | landuse_data_module | Matches each HRU's land-use management label to a loaded land-use record and stores the numeric pointer for later initialization. |
| [sym:hrudb_init] | landuse_data_module | Converts each HRU's resolved land-use index into the calibration-group string copied into the active HRU record. |
| [sym:landuse_read] | landuse_data_module | Loads the land-use management records and resolves their text pointers into the integer structure table used by the rest of the model. |
| [sym:lsreg_output] | landuse_data_module | Uses the shared land-use metadata to label regional land-use output rows and aggregate values by land-use class. |
| [sym:overland_n_read] | landuse_data_module | Allocates and fills the shared overland-flow Manning's n lookup table used later for HRU roughness assignment. |
| [sym:plant_init] | landuse_data_module | Looks up the conservation-practice row, urban runoff mode, and overland roughness for the current HRU, then copies those values into active HRU state. |
| [sym:proc_hru] | landuse_data_module | Supplies septic and structural land-management pointers that must be applied before soil and plant initialization proceeds. |
| [sym:reg_read_elements] | landuse_data_module | Loads the region's land-use group names into the shared group container used for regional bookkeeping and output. |
| [sym:structure_init] | landuse_data_module | Provides the structural practice pointers that determine which tile-drain, filter-strip, grassed-waterway, and user-defined BMP parameters are applied. |
| [sym:cn2_init_all] | landuse_data_module | Provides the shared land-use state needed by the per-HRU curve-number initialization loop. |
| [sym:dtbl_res_read] | landuse_data_module | No direct land-use-module state use is visible in the extracted evidence; the routine operates on reservoir decision tables. |
| [sym:cal_conditions] | landuse_data_module | Applies conditional calibration updates to matched plant, reservoir, soil, climate, and related targets after checking the current state. |
| [sym:actions] | landuse_data_module | Uses the shared land-use table when accumulating regional crop-yield calibration statistics for matching management actions. |
| [sym:hru_output] | landuse_data_module | Writes HRU summaries with the land-use plant cover and management labels from the shared land-use database. |

## Lineage

`landuse_data_module.f90` was introduced in `df07e3f` (2024-03-05, "init all") and has been changed in 3 non-merge commit(s) since, most recently `39fabde` (2024-08-08, "Initialized varables with python script, corrected input data where integers whe…"). Lineage is reconstructed from commit metadata (SHA, date, subject); per-line diffs were unavailable in this build environment, so only the commits touching `landuse_data_module.f90` are listed.

- `39fabde` (2024-08-08) — Initialized varables with python script, corrected input data where integers where floats in two input files, trapped underflow errors in th…
- `94b6dec` (2024-05-30) — Added latest source code from bitbucket
- `df07e3f` (2024-03-05) — init all

## Review Notes

- Module `landuse_data_module` has no extracted module-level documentation comment.
- The importer list is preserved exactly as extracted; it is the complete deterministic set of importers for this module.
- The source span has no resolved Git lineage commits, so lineage impacts remain empty.
- Lineage was reconstructed from file-level commit metadata; per-line diffs were unavailable in this environment (blobless clone), so line-span filtering was not applied.
