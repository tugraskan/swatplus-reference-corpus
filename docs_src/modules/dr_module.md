---
kind: module
symbol: dr_module
title: dr_module
status: filled
source_hash: cc39a92f0c795960
version_label: SWAT+ 62.0.0
variables:
  dr_om_num: Allocatable integer crosswalk from each delivery-ratio database entry to the
    matching organic-matter record number loaded from `dr_om.del`. It is populated by `dr_read_om`
    and consumed later when routing elements or objects need `dr(idr_om)` through the resolved
    organic-matter index.
  dr_pest_num: Allocatable integer crosswalk from each delivery-ratio database entry to the
    matching pesticide record number loaded from `dr_pest.del`. It is populated by `dr_read_pest`
    and used by `constit_hyd_mult` and the pesticide hydrograph setup to choose the correct
    pesticide multiplier vector.
  dr_path_num: Allocatable integer crosswalk from each delivery-ratio database entry to the
    matching pathogen path record number loaded from `dr_path.del`. It is populated by `dr_path_read`
    and used by `constit_hyd_mult` and the pathogen hydrograph setup.
  dr_hmet_num: Allocatable integer crosswalk from each delivery-ratio database entry to the
    matching heavy-metal record number loaded from `dr_hmet.del`. It is populated by `dr_read_hmet`
    and used by `constit_hyd_mult` and the heavy-metal hydrograph setup.
  dr_salt_num: Allocatable integer crosswalk from each delivery-ratio database entry to the
    matching salt record number loaded from `dr_salt.del`. It is populated by `dr_read_salt`
    and used by `constit_hyd_mult` and the salt hydrograph setup.
  dr_om_name: Allocatable list of organic-matter delivery-ratio record names read from `dr_om.del`.
    `dr_read_om` fills it while building the organic-matter table, and the names are used
    to match `dr_db(idr)%om_file` to the correct sequential organic-matter record.
  dr_pest_name: Allocatable list of pesticide delivery-ratio record names read from `dr_pest.del`.
    `dr_read_pest` fills it while building the pesticide table, and the names are used to
    match `dr_db(idr)%pest_file` to the correct sequential pesticide record.
  dr_path_name: Allocatable list of pathogen path delivery-ratio record names read from `dr_path.del`.
    `dr_path_read` fills it while building the path table, and the names are used to match
    `dr_db(idr)%path_file` to the correct sequential path record.
  dr_hmet_name: Allocatable list of heavy-metal delivery-ratio record names read from `dr_hmet.del`.
    `dr_read_hmet` fills it while building the heavy-metal table, and the names are used to
    match `dr_db(idr)%hmet_file` to the correct sequential heavy-metal record.
  dr_salt_name: Allocatable list of salt delivery-ratio record names read from `dr_salt.del`.
    `dr_read_salt` fills it while building the salt table, and the names are used to match
    `dr_db(idr)%salts_file` to the correct sequential salt record.
  dr_db: Allocatable, saved array of `delivery_ratio_datafiles` records that holds the configured
    delivery-ratio definition names and the file-name keys for the associated organic-matter,
    pesticide, pathogen path, heavy-metal, and salt tables. `dr_db_read` allocates and fills
    it from `delratio.del`; later readers and routing routines use it as the shared lookup
    table.
type_components:
  delivery_ratio_datafiles:
    name: Delivery-ratio definition name used as the routing-object lookup key.
    om_file: Organic-matter delivery-ratio file name associated with this delivery-ratio definition.
    pest_file: Pesticide delivery-ratio file name associated with this delivery-ratio definition.
    path_file: Pathogen path delivery-ratio file name associated with this delivery-ratio
      definition.
    hmet_file: Heavy-metal delivery-ratio file name associated with this delivery-ratio definition.
    salts_file: Salt delivery-ratio file name associated with this delivery-ratio definition.
type_summaries:
  delivery_ratio_datafiles: One record names a delivery-ratio definition and the five input
    files that supply its constituent-specific lookup tables.
---

<!-- facts:header -->

dr_module owns the shared delivery-ratio lookup state for SWAT+: the main delivery-ratio database records, the per-constituent name-to-index crosswalk arrays, and the `delivery_ratio_datafiles` type that stores the file-name keys for each delivery-ratio definition. Startup readers populate these arrays from the delivery-ratio input files, and later routing and constituent-multiplication routines depend on them to resolve `dr_name` values into the correct organic-matter, pesticide, pathogen, heavy-metal, and salt records.

## Contained Procedures And Types

<!-- facts:members -->

## Module Variables

<!-- facts:variables -->

## Derived Types

<!-- facts:types -->



## Initialization

This module is a declaration container only; it contains no procedures of its own. Its allocatable arrays are populated by external reader routines such as `dr_db_read`, `dr_read_om`, `dr_read_pest`, `dr_path_read`, `dr_read_hmet`, and `dr_read_salt`, and the resolved indices are then reused by routing and constituent-transfer code.

## Populated By

| Reader | Input file | Target | Behavior |
| --- | --- | --- | --- |
| [sym:dr_db_read] | `delratio.del` | `dr_db` | Allocates and fills the shared delivery-ratio database array from the main delivery-ratio definition file, then stores the record count for later crosswalks. |
| [sym:dr_path_read] | `dr_path.del` | `dr_path_num, dr_path_name` | Loads the pathogen path lookup table, records each path name, and crosswalks `dr_db(idr)%path_file` to the matching sequential record number. |
| [sym:dr_read_hmet] | `dr_hmet.del` | `dr_hmet_num, dr_hmet_name` | Loads the heavy-metal lookup table, records each metal-set name, and crosswalks `dr_db(idr)%hmet_file` to the matching sequential record number. |
| [sym:dr_read_om] | `dr_om.del` | `dr_om_num, dr_om_name` | Loads the organic-matter delivery-ratio table, records each name, and crosswalks `dr_db(idr)%om_file` to the matching sequential record number. |
| [sym:dr_read_pest] | `dr_pest.del` | `dr_pest_num, dr_pest_name` | Loads the pesticide delivery-ratio table, records each name, and crosswalks `dr_db(idr)%pest_file` to the matching sequential record number. |
| [sym:dr_read_salt] | `dr_salt.del` | `dr_salt_num, dr_salt_name` | Loads the salt delivery-ratio table, records each name, and crosswalks `dr_db(idr)%salts_file` to the matching sequential record number. |
| [sym:hru_fr_change] | `ru_elem_upd, lsu_elem_upd` | `dr_db, dr_om_num` | Uses the shared delivery-ratio lookup table to resolve each routing element's `dr_name` and assign the matching delivery-ratio object to `ru_elem(i)%dr`. |
| [sym:ru_read_elements] | `rout_unit.ele, rout_unit.def` | `dr_db, dr_om_num` | Uses the shared delivery-ratio lookup table to resolve routing-unit element `dr_name` values and attach the matching delivery-ratio object to each element. |

## Key Consumers

The module is imported by the delivery-ratio readers that load and crosswalk the per-constituent tables, by the routing-unit readers that attach delivery-ratio objects to spatial elements, and by the constituent-multiplication routine that applies the resolved ratios to hydrograph masses.

| Consumer | Uses | Effect |
| --- | --- | --- |
| [sym:dr_db_read] | dr_module | Loads `dr_db` from `delratio.del`, establishing the shared delivery-ratio definitions that all later readers and routing setup routines crosswalk against. |
| [sym:dr_path_read] | dr_module | Reads `dr_db(idr)%path_file` to match each delivery-ratio definition to the correct pathogen path record and fill `dr_path_num`. |
| [sym:dr_read_hmet] | dr_module | Reads `dr_db(idr)%hmet_file` to match each delivery-ratio definition to the correct heavy-metal record and fill `dr_hmet_num`. |
| [sym:dr_read_om] | dr_module | Reads `dr_db(idr)%om_file` to match each delivery-ratio definition to the correct organic-matter record and fill `dr_om_num`. |
| [sym:dr_read_pest] | dr_module | Reads `dr_db(idr)%pest_file` to match each delivery-ratio definition to the correct pesticide record and fill `dr_pest_num`. |
| [sym:dr_read_salt] | dr_module | Reads `dr_db(idr)%salts_file` to match each delivery-ratio definition to the correct salt record and fill `dr_salt_num`. |
| [sym:hru_fr_change] | dr_module | Resolves each routing element's `dr_name` through `dr_db(idr)%name` so the updated routing element can carry the matching delivery-ratio object in `ru_elem(i)%dr`. |
| [sym:ru_read_elements] | dr_module | Resolves each routing-unit element's `dr_name` through `dr_db(idr)%name` so the element can be linked to the correct delivery-ratio object. |
| [sym:constit_hyd_mult] | dr_module | Uses `dr_pest_num`, `dr_path_num`, `dr_hmet_num`, and `dr_salt_num` to select the loaded constituent multiplier sets that are applied to `obcs(iob)%hin(1)` and stored in `obcs(iob)%hd(1)`. |

## Lineage

`dr_module.f90` was introduced in `df07e3f` (2024-03-05, "init all") and has been changed in 4 non-merge commit(s) since, most recently `39fabde` (2024-08-08, "Initialized varables with python script, corrected input data where integers whe…"). Lineage is reconstructed from commit metadata (SHA, date, subject); per-line diffs were unavailable in this build environment, so only the commits touching `dr_module.f90` are listed.

- `39fabde` (2024-08-08) — Initialized varables with python script, corrected input data where integers where floats in two input files, trapped underflow errors in th…
- `94b6dec` (2024-05-30) — Added latest source code from bitbucket
- `35b029c` (2024-03-24) — Mar 19 status
- `df07e3f` (2024-03-05) — init all

## Review Notes

- No module-level documentation comment was extracted from `dr_module.f90`.
- Lineage evidence reported no resolved commits for this source span.
- Lineage was reconstructed from file-level commit metadata; per-line diffs were unavailable in this environment (blobless clone), so line-span filtering was not applied.
