---
kind: module
symbol: exco_module
title: exco_module
status: filled
source_hash: 9a0982d7d5ddb932
version_label: SWAT+ 62.0.0
variables:
  exco_om_num: Allocatable integer lookup array declared in `exco_module.f90:5` and initialized
    by `exco_read_om` to map each export-coefficient entry to the sequential organic-matter
    table row. It is used later when exco organic-matter data are matched by file name rather
    than by position.
  exco_pest_num: Allocatable integer lookup array declared in `exco_module.f90:6` and filled
    by `exco_read_pest` with the sequential pesticide table index for each export-coefficient
    entry. Downstream exco setup uses it to fetch the matching pesticide coefficients.
  exco_path_num: Allocatable integer lookup array declared in `exco_module.f90:7` and populated
    by `exco_read_path` with the sequential pathogen-path table index for each export-coefficient
    entry. It supports later object hydrograph assignment by resolved index.
  exco_hmet_num: Allocatable integer lookup array declared in `exco_module.f90:8` and populated
    by `exco_read_hmet` with the sequential heavy-metal table index for each export-coefficient
    entry. Later exco object setup uses it to copy the correct heavy-metal coefficients into
    object hydrograph state.
  exco_salt_num: Allocatable integer lookup array declared in `exco_module.f90:9` and populated
    by `exco_read_salt` with the sequential salt table index for each export-coefficient entry.
    It is used when attaching salt coefficients to exco object hydrographs.
  exco_om_name: Allocatable character lookup array declared in `exco_module.f90:10` and filled
    by `exco_read_om` with the loaded organic-matter export-coefficient file names. It is
    the name side of the name-to-index crosswalk.
  exco_pest_name: Allocatable character lookup array declared in `exco_module.f90:11` and
    filled by `exco_read_pest` with the loaded pesticide export-coefficient file names. It
    is compared against `exco_db(iexco)%pest_file` during crosswalk.
  exco_path_name: Allocatable character lookup array declared in `exco_module.f90:12` and
    filled by `exco_read_path` with the loaded pathogen-path export-coefficient file names.
    It is compared against `exco_db(iexco)%path_file` during crosswalk.
  exco_hmet_name: Allocatable character lookup array declared in `exco_module.f90:13` and
    filled by `exco_read_hmet` with the loaded heavy-metal export-coefficient file names.
    It is compared against `exco_db(iexco)%hmet_file` during crosswalk.
  exco_salt_name: Allocatable character lookup array declared in `exco_module.f90:14` and
    filled by `exco_read_salt` with the loaded salt export-coefficient file names. It is compared
    against `exco_db(iexco)%salts_file` during crosswalk.
  exco_db: Allocatable, saved array of `export_coefficient_datafiles` declared in `exco_module.f90:26`.
    Each element stores the configured file names for one export-coefficient definition and
    is loaded by `exco_db_read`; later readers use it as the shared name list for crosswalking
    to constituent tables.
type_components:
  export_coefficient_datafiles:
    name: Short identifier for the export-coefficient definition, declared as `character(len=16)`
      in `exco_module.f90:17`.
    om_file: Organic-matter export-coefficient file name for this definition, declared at
      `exco_module.f90:18`.
    pest_file: Pesticide export-coefficient file name for this definition, declared at `exco_module.f90:19`.
    path_file: Pathogen-path export-coefficient file name for this definition, declared at
      `exco_module.f90:20`.
    hmet_file: Heavy-metal export-coefficient file name for this definition, declared at `exco_module.f90:21`.
    salts_file: Salt export-coefficient file name for this definition, declared at `exco_module.f90:22`.
    constit_file: Constituent export-coefficient file name for this definition, declared at
      `exco_module.f90:23`.
    descrip: Free-text description field for the record, declared as `character(len=40)` at
      `exco_module.f90:24`.
type_summaries:
  export_coefficient_datafiles: A single export-coefficient configuration record. It stores
    the export-coefficient name plus the file names used for each constituent-specific table
    and a free-text description.
---

<!-- facts:header -->

`exco_module` owns the shared export-coefficient lookup state used by SWAT+ to crosswalk configured export-coefficient files to sequential record numbers. It declares the allocatable index/name arrays for organic matter, pesticide, pathogen path, heavy metal, and salt export coefficients, plus the `export_coefficient_datafiles` record type and the allocatable `exco_db` table that stores the configured file names for each export-coefficient definition. Reader routines populate this state during startup, and downstream readers and water-allocation logic use it to resolve names into indices.

## Contained Procedures And Types

<!-- facts:members -->

## Module Variables

<!-- facts:variables -->

## Derived Types

<!-- facts:types -->



## Initialization

This module is a declaration container only; it contains no procedures of its own. Its allocatable arrays and `exco_db` record table are populated by external reader routines such as `exco_db_read`, `exco_read_om`, `exco_read_pest`, `exco_read_path`, `exco_read_hmet`, and `exco_read_salt` during model startup.

## Populated By

| Reader | Input file | Target | Behavior |
| --- | --- | --- | --- |
| [sym:exco_db_read] | `exco.exc` | `exco_db` | Reads the export-coefficient database file, counts the records, allocates `exco_db`, and loads each export-coefficient definition into the shared module table. |
| [sym:exco_read_hmet] | `exco_hmet.exc` | `exco_hmet_num, exco_hmet_name, exco_db` | Reads heavy-metal export-coefficient rows, loads the heavy-metal name table, and crosswalks each `exco_db` record to a sequential heavy-metal row number. |
| [sym:exco_read_om] | `exco_om.exc` | `exco_om_num, exco_om_name` | Reads organic-matter export-coefficient rows and fills the organic-matter name and index lookup arrays. |
| [sym:exco_read_path] | `exco_path.exc` | `exco_path_num, exco_path_name, exco_db` | Reads pathogen-path export-coefficient rows, fills the path name and index lookup arrays, and crosswalks the file names stored in `exco_db`. |
| [sym:exco_read_pest] | `exco_pest.exc` | `exco_pest_num, exco_pest_name, exco_db` | Reads pesticide export-coefficient rows, fills the pesticide name and index lookup arrays, and crosswalks the file names stored in `exco_db`. |
| [sym:exco_read_salt] | `exco_salt.exc` | `exco_salt_num, exco_salt_name, exco_db` | Reads salt export-coefficient rows, fills the salt name and index lookup arrays, and crosswalks the file names stored in `exco_db`. |
| [sym:recall_read] | `recall_db(irec)%org_min%name, unit_10108, pest.com, rec_pest(i)%filename` | `exco_db` | Uses shared export-coefficient naming state when loading recall database and associated constituent source data; the imported exco module provides the crosswalk context used elsewhere in the recall setup path. |
| [sym:recall_read_cs] | `cs_recall.rec, rec_cs(i)%filename` | `exco_db` | Imports the export-coefficient context because the visible code contains an unresolved branch that references exco crosswalking for constituent recall mapping. |
| [sym:recall_read_salt] | `salt_recall.rec, rec_salt(i)%filename` | `exco_db` | Imports the export-coefficient context because the visible code contains an unresolved `typ == 4` branch that mentions exco-based crosswalking for salt recall mapping. |
| [sym:water_allocation_read] | `water_allocation.wro` | `exco_db, exco_om_name` | Uses the organic-matter file-name crosswalk in `exco_module` to resolve `osrc_a` outside-source references to the corresponding annual-constant source index. |

## Key Consumers

The module is used as shared state by the export-coefficient reader routines and by water-allocation and recall setup code that must resolve file names to sequential indices. Most consumers either populate the lookup arrays or consult them to crosswalk configured file names into object state.

| Consumer | Uses | Effect |
| --- | --- | --- |
| [sym:exco_db_read] | exco_module | Loads the export-coefficient database into the shared `exco_db` table, making the file-name records available for later constituent-specific crosswalks. |
| [sym:exco_read_hmet] | exco_module | Uses `exco_db`, `exco_hmet_name`, and `exco_hmet_num` to resolve each heavy-metal file name to a sequential table row, then copies the matched heavy-metal coefficients into exco object hydrographs. |
| [sym:exco_read_om] | exco_module | Allocates and fills the organic-matter lookup arrays so export-coefficient definitions can be matched to organic-matter records by name. |
| [sym:exco_read_path] | exco_module | Builds the pathogen-path lookup arrays and resolves each export-coefficient path file name to a sequential path table index. |
| [sym:exco_read_pest] | exco_module | Builds the pesticide lookup arrays and resolves each export-coefficient pesticide file name to a sequential pesticide table index. |
| [sym:exco_read_salt] | exco_module | Builds the salt lookup arrays and resolves each export-coefficient salt file name to a sequential salt table index. |
| [sym:recall_read] | exco_module | Imports the export-coefficient module as part of the broader setup environment for recall database loading and later shared state use. |
| [sym:recall_read_cs] | exco_module | Keeps the export-coefficient crosswalk state available for the unresolved constituent-recall branch that refers to exco-based mapping. |
| [sym:recall_read_salt] | exco_module | Keeps the export-coefficient crosswalk state available for the unresolved salt-recall branch that refers to exco-based mapping. |
| [sym:wallo_demand] | exco_module | Imports the module so water-allocation demand logic can consult export-coefficient-linked outside-source state when computing transfer flows. |
| [sym:water_allocation_read] | exco_module | Resolves `osrc_a` outside-source references by matching `exco_db(iexco)%om_file` against `exco_om_name`, then stores the resolved annual-constant index in `osrc(isrc)%aa`. |

## Lineage

`exco_module.f90` was introduced in `df07e3f` (2024-03-05, "init all") and has been changed in 5 non-merge commit(s) since, most recently `080211e` (2026-03-09, "water allocation operating properly"). Lineage is reconstructed from commit metadata (SHA, date, subject); per-line diffs were unavailable in this build environment, so only the commits touching `exco_module.f90` are listed.

- `080211e` (2026-03-09) — water allocation operating properly
- `39fabde` (2024-08-08) — Initialized varables with python script, corrected input data where integers where floats in two input files, trapped underflow errors in th…
- `94b6dec` (2024-05-30) — Added latest source code from bitbucket
- `35b029c` (2024-03-24) — Mar 19 status
- `df07e3f` (2024-03-05) — init all

## Review Notes

- No module-level documentation comment is present in `exco_module.f90:1-28`.
- The context packet extracted no explicit initialization code inside this module; all state population happens in external reader routines.
- Some consumer effects for `recall_read`, `recall_read_cs`, `recall_read_salt`, and `wallo_demand` remain partially inferential because the completed overlay evidence did not resolve module-owned symbols for those procedures.
- Lineage was reconstructed from file-level commit metadata; per-line diffs were unavailable in this environment (blobless clone), so line-span filtering was not applied.
