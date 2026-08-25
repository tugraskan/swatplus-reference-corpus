---
kind: module
symbol: recall_module
title: recall_module
status: filled
source_hash: 1ee444ade7c29f28
version_label: SWAT+ 62.0.0
variables:
  recall_db: Allocatable shared array of `recall_databases` records for all recall objects,
    including outside-basin recall sources and average annual recall-style files. The source
    comments note that exco and dr are average annual recalls in one file, while daily, monthly,
    and annual recall files are stored as individual records.
type_components:
  constituent_file_data:
    name: File or object name for the constituent/time-series source.
    units: Units tag for the file contents; the source comment identifies mass or concentration.
    tstep: Time-step tag for the file contents; the source comment identifies day, month,
      or year.
  recall_databases:
    name: Name of the recall database entry, used to match and write recall files.
    org_min: Organic-mineral recall file descriptor for this entry.
    pest: Pesticide recall file descriptor for this entry.
    path: Pathogen recall file descriptor for this entry.
    hmet: Heavy-metal recall file descriptor for this entry.
    salt: Salt recall file descriptor for this entry.
    constit: General constituent recall file descriptor for this entry.
    iorg_min: Resolved sequential index of the organic-mineral recall file within `recall_db`.
    ipest: Resolved sequential index of the pesticide recall file within `recall_db`.
    ipath: Resolved sequential index of the pathogen recall file within `recall_db`.
    ihmet: Resolved sequential index of the heavy-metal recall file within `recall_db`.
    isalt: Resolved sequential index of the salt recall file within `recall_db`.
    iconstit: Resolved sequential index of the general constituent recall file within `recall_db`.
type_summaries:
  constituent_file_data: Descriptor for one constituent or time-series file associated with
    a recall database entry.
  recall_databases: One recall database record that groups the recall file name with constituent-specific
    file descriptors and their resolved indices.
---

<!-- facts:header -->

`recall_module` owns the shared recall database array and the derived types used to describe recall files and their constituent time-series descriptors. The module is a declaration container; startup and reader routines in other procedures allocate and populate `recall_db`, then later model routines use that metadata to resolve recall-file names and choose daily, monthly, yearly, or average-annual recall data.

## Contained Procedures And Types

<!-- facts:members -->

## Module Variables

<!-- facts:variables -->

## Derived Types

<!-- facts:types -->



## Initialization

`recall_module` itself does not contain initialization procedures. Its exported array `recall_db` is allocated and filled by reader routines such as `recalldb_read` and `recall_read`, and then consumed by downstream routines that need recall metadata or recall time-series selection.

## Populated By

| Reader | Input file | Target | Behavior |
| --- | --- | --- | --- |
| [sym:command] | `unit_out_hyd_sep` | `recall_db` | Uses `recall_db(irec)%org_min%tstep` to decide whether a recall hydrograph should be read from the subdaily series or from the stored daily/monthly/yearly record during hydrologic command processing. |
| [sym:dtbl_res_read] | `res_rel.dtl` | `recall_db` | Reads reservoir decision-table actions and matches measured-release pointers against `recall_db(idb)%name` to resolve a text file pointer to a numeric recall database index. |
| [sym:hyd_connect] | `looping.con, unit_*, unit_9004` | `recall_db` | Imports the shared recall database state as part of the watershed connectivity setup, but the visible source slice in the context packet does not show a resolved `recall_db` reference in the procedure body. |
| [sym:recalldb_read] | `recall_db.rec` | `recall_db` | Reads `recall_db.rec`, finds the maximum recall index, allocates `recall_db`, and fills each record's name and constituent file descriptors. |
| [sym:recall_read] | `recall_db(irec)%org_min%name, unit_10108, pest.com, rec_pest(i)%filename` | `recall_db` | Uses `recall_db(irec)%org_min%name` and `recall_db(irec)%org_min%tstep` to open the correct recall input file, detect reuse of prior organic-mineral files, and read the time-series data into shared recall storage. |
| [sym:swift_output] | `SWIFT/file_cio.swf, SWIFT/precip.swf, SWIFT/hru_dat.swf, SWIFT/hru_exco.swf, SWIFT/hru_wet.swf, SWIFT/chan_dat.swf, SWIFT/chan_dr.swf, SWIFT/aqu_dr.swf, SWIFT/res_dat.swf, SWIFT/res_dr.swf, SWIFT/recall.swf, recall_db(irec)%name, SWIFT/object_prt.swf` | `recall_db` | Writes the SWIFT recall index and per-recall files using `recall_db` metadata, including each entry's recall name, units, and time-step tag. |
| [sym:water_allocation_read] | `water_allocation.wro` | `recall_db` | Cross-walks outside-source transfer definitions to `recall_db(irec)%iorg_min` so an outside-basin source can later be linked to the correct recall time series. |
| [sym:water_orcv_read] | `outside_rcv.wal` | `recall_db` | Imports the module for shared compilation context, but the visible source slice does not show a resolved `recall_db` access in the routine body. |
| [sym:water_osrc_read] | `out_src.wal` | `recall_db` | Imports the module for outside-source crosswalking context; the resolved source slice provided here does not show an active `recall_db` reference in the visible procedure body. |

## Key Consumers

Hydrologic routing, water allocation, decision-table loading, and SWIFT output routines all import this module so they can resolve recall database names, time-step types, and the shared `recall_db` array. Some consumers use it to read time-series data, while others use it only to translate names into sequential indices for later processing.

| Consumer | Uses | Effect |
| --- | --- | --- |
| [sym:dtbl_res_read] | recall_module | Measured-release actions can point to recall database names, so this module supplies the `recall_db` list that `file_pointer` is matched against. |
| [sym:recalldb_read] | recall_module | The routine fills `recall_db`, including each entry’s name and constituent file descriptors, so `recall_module` supplies the persistent database structure that stores all recall file metadata for later use. |
| [sym:recall_read] | recall_module | The routine fills `recall_db`, including each entry’s name and constituent file descriptors, so `recall_module` supplies the persistent database structure that stores all recall file metadata for later use. |
| [sym:swift_output] | recall_module | The recall module supplies the recall database metadata and file names that drive both the summary `recall.swf` listing and the per-recall output files. `swift_output` uses these records to create a master recall index and then write each annual recall file using the configured name and constituent descriptors. |
| [sym:water_allocation_read] | recall_module | This module provides the recall-file database used to resolve outside-basin sources. The routine reads a source number, treats it as a recall-file index when the source type is `osrc`, and copies `iorg_min` into the transfer object's day/month/year selector. |
| [sym:hyd_connect] | recall_module | The procedure imports the shared recall database as part of watershed connectivity setup, but the resolved source evidence in the packet does not show a direct `recall_db` reference in the visible body. |
| [sym:water_orcv_read] | recall_module | `recall_module` is imported by the procedure, but no resolved symbols from it are referenced in the visible source; it likely remains for shared compilation context or future use, but it does not affect the shown algorithm directly. |
| [sym:water_osrc_read] | recall_module | The procedure imports `recall_module` alongside outside-source handling; the visible source slice supplied here does not show a live `recall_db` reference, so the module's role is limited to shared dependency context in the evidence packet. |
| [sym:res_hydro] | recall_module | `recall_module` provides the metadata that tells `res_hydro` how to interpret a measured-release database, especially whether the hydrograph input is daily, monthly, or annual. That metadata selects which `recall(irel)%hd(...)` record becomes the outflow source. |
| [sym:wallo_demand] | recall_module | Maps a source object to its recall database entry and time step so the routine can pick the correct daily, monthly, or yearly flow record. |
| [sym:wallo_withdraw] | recall_module | The recall module supplies the recall database metadata that tells this routine whether an outside-basin source is indexed by day, month, or year. |
| [sym:command] | recall_module | The command routine uses `recall_db(irec)%org_min%tstep` to choose whether recall flow comes from subdaily data or from daily/monthly/yearly records when hydrologic commands are processed. |

## Lineage

`recall_module.f90` was introduced in `df07e3f` (2024-03-05, "init all") and has been changed in 6 non-merge commit(s) since, most recently `e24da22` (2026-03-11, "Add allocatable variables for outside inflow and update water tower read logic"). Lineage is reconstructed from commit metadata (SHA, date, subject); per-line diffs were unavailable in this build environment, so only the commits touching `recall_module.f90` are listed.

- `e24da22` (2026-03-11) — Add allocatable variables for outside inflow and update water tower read logic
- `080211e` (2026-03-09) — water allocation operating properly
- `72206bc` (2026-01-07) — Enhance water allocation with recall support and update soil cover calculations
- `39fabde` (2024-08-08) — Initialized varables with python script, corrected input data where integers where floats in two input files, trapped underflow errors in th…
- `94b6dec` (2024-05-30) — Added latest source code from bitbucket
- `df07e3f` (2024-03-05) — init all

## Review Notes

- Module `recall_module` has no extracted module-level documentation comment.
- Lineage was reconstructed from file-level commit metadata; per-line diffs were unavailable in this environment (blobless clone), so line-span filtering was not applied.
