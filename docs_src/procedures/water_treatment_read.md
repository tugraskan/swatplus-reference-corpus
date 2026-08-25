---
kind: procedure
symbol: water_treatment_read
title: water_treatment_read
status: filled
source_hash: b362aad9dce2baf4
version_label: SWAT+ 62.0.0
locals:
  titldum: Temporary title line read from the top of `water_treat.wal`; it is consumed only
    to skip the file header/title record before the data count is read.
  header: Scratch string used to skip labeled section/header lines in `water_treat.wal` before
    reading treatment data and optional constituent blocks.
  eof: IOSTAT status flag for reads on unit 107; values below zero indicate end-of-file and
    are used to stop the read loop safely.
  imax: Number of water treatment objects declared in `water_treat.wal`; it is used to size
    `wtp` and the related output/storage arrays.
  i_exist: Logical flag set by `inquire` to tell whether `water_treat.wal` exists before trying
    to read it.
  i: Record counter read from the input file; it tracks the treatment record number stored
    on each line.
  iwtp: Loop index over water treatment objects while the routine reads each treatment and
    its optional constituent data.
  iom: Loop index used to search `om_treat_name` for a matching organic-mineral treatment
    name.
uses:
  input_file_module: This module provides the file-existence inquiry state that lets the routine
    decide whether to read `water_treat.wal` or fall back to an empty allocation.
  water_allocation_module: '`water_allocation_module` holds the treatment database being populated.
    The routine fills `wtp(iwtp)%name`, `stor_mx`, `lag_days`, `loss_fr`, `org_min`, `pests`,
    `paths`, `salts`, `constit`, `descrip`, and `iorg_min`, so this module is the main persistent
    destination for the file contents.'
  mgt_operations_module: The routine compares each treatment's `org_min` name against `om_treat_name(iom)`
    to convert a text label from the file into the integer pointer `wtp(iwtp)%iorg_min`.
  maximum_data_module: '`maximum_data_module` provides the shared database counters `db_mx%treat`
    and `db_mx%om_treat`. The first is set from the number of treatment records read, and
    the second bounds the crosswalk loop over organic-mineral treatment names.'
  hydrograph_module: '`hydrograph_module` owns the allocated output/storage arrays for treatment-plant
    storage, outflow, and organic-mineral removal terms. `water_treatment_read` allocates
    these arrays to the size of the treatment database so later hydrologic bookkeeping has
    storage ready.'
  constituent_mass_module: '`constituent_mass_module` provides the simulated constituent counts
    and the storage objects that hold treatment pesticide and pathogen concentrations. The
    routine uses `cs_db%num_pests` and `cs_db%num_paths` to decide whether to allocate and
    read `wtp_cs_treat(iwtp)%pest` and `%path`.'
---

<!-- facts:header -->

Reads the water treatment definition file and populates the water treatment database and related storage arrays. It also crosswalks organic-mineral treatment names to indices and loads optional pesticide and pathogen concentration arrays.

## Bottom Line

`water_treatment_read` loads `water_treat.wal` into shared SWAT+ state. It first checks whether the file exists, then reads the file title, the number of treatment records, and each treatment record into `wtp` along with the model-wide count in `db_mx%treat`.

For each treatment object it also resolves the `org_min` name to an index in `om_treat_name`, and if pesticide or pathogen constituents are being simulated it allocates and reads the corresponding `wtp_cs_treat(iwtp)%pest` and `wtp_cs_treat(iwtp)%path` arrays. The routine finishes by closing unit 107, leaving the treatment database ready for later water-allocation and constituent-mass calculations.

## Arguments

<!-- facts:arguments -->

## Where It Fits

This routine runs during input initialization when SWAT+ is loading treatment definitions. It depends on prior module setup for file availability, management-operation names, constituent counts, and shared database maxima, and its results feed later water-allocation, hydrograph, and constituent-mass calculations that need the treatment database and related arrays.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. Initialize counters and test file availability | Set local defaults, inquire whether `water_treat.wal` exists, and if it does not exist or is disabled by the literal `'null'`, allocate an empty `wtp(0:0)` array instead of attempting to read data. |
| 2. Open the treatment input file and read its title/count headers | Open unit 107 on `water_treat.wal`, read and discard the file title, read the number of treatment records into `imax`, read the next header line, and store the count in `db_mx%treat`. End-of-file status aborts the loop if encountered. |
| 3. Allocate treatment and related output arrays | Allocate `wtp(imax)` plus the hydrograph and storage arrays `wtp_om_stor`, `wtp_cs_stor`, `wtp_om_out`, `wal_tr_omd`, `wal_tr_omm`, `wal_tr_omy`, and `wal_tr_oma` so every treatment object has matching storage slots. |
| 4. Read each treatment record and crosswalk its organic-mineral name | Loop over each treatment record, read the treatment index and fields into `wtp(iwtp)`, then search `om_treat_name` for the matching `org_min` string and save the index in `wtp(iwtp)%iorg_min`. |
| 5. Read optional pesticide concentrations when simulated | If `cs_db%num_pests > 0`, allocate `wtp_cs_treat(iwtp)%pest`, read the next header line, and read the pesticide concentration array for the current treatment object. |
| 6. Read optional pathogen concentrations when simulated | If `cs_db%num_paths > 0`, allocate `wtp_cs_treat(iwtp)%path`, read the next header line, and read the pathogen concentration array for the current treatment object. |
| 7. Finish the file scan and close the input unit | Exit the input loop after one successful pass, close unit 107, and return with the treatment database and companion arrays populated. |

## Modules Used

<!-- facts:uses -->

| Module | State touched | Key components |
| --- | --- | --- |
| [sym:input_file_module] | `input_file_module state used to determine whether the configured input file can be accessed.` | `i_exist` |
| [sym:water_allocation_module] | `wtp, om_treat_name, wal` | `wtp(iwtp)%name, wtp(iwtp)%stor_mx, wtp(iwtp)%lag_days, wtp(iwtp)%loss_fr, wtp(iwtp)%org_min, wtp(iwtp)%pests, wtp(iwtp)%paths, wtp(iwtp)%salts, wtp(iwtp)%constit, wtp(iwtp)%descrip, wtp(iwtp)%iorg_min` |
| [sym:mgt_operations_module] | `mgt_operations_module state used for management-operation crosswalks.` | `om_treat_name` |
| [sym:maximum_data_module] | `db_mx` | `db_mx%treat, db_mx%om_treat` |
| [sym:hydrograph_module] | `wtp_om_stor, wtp_om_out, wal_tr_omd, wal_tr_omm, wal_tr_omy, wal_tr_oma` |  |
| [sym:constituent_mass_module] | `cs_db, wtp_cs_treat, wtp_cs_stor` | `cs_db%num_pests, wtp_cs_treat(iwtp)%pest, cs_db%num_paths, wtp_cs_treat(iwtp)%path` |

## Local Variables

<!-- facts:locals -->

## State Changes

| Target | When | Meaning |
| --- | --- | --- |
| `db_mx%treat` | When `water_treat.wal` exists and the routine successfully reads the record count. | `db_mx%treat` is set to `imax`, the number of water treatment objects declared in the input file, so shared model code knows how many treatment entries were loaded. |
| `wtp(iwtp)%iorg_min` | When a treatment record's `org_min` string matches an entry in `om_treat_name(iom)` during the crosswalk loop. | `wtp(iwtp)%iorg_min` is set to the matching organic-mineral treatment index, turning the text label from the input file into an integer reference used by later management-operation logic. |

## File I/O

<!-- facts:io -->


## Lineage

Resolved lineage commits show two behavior changes for `water_treatment_read`: the file was introduced in `d70017a`, and `080211e` changed the database counter assignment from `db_mx%water_treat` to `db_mx%treat` and added allocations for the treatment storage/output arrays before reading records.

- `d70017a` introduced `water_treatment_read.f90` with file existence checking, file opening, record reading, organic-mineral crosswalking, and optional pesticide/pathogen constituent loading.
- `080211e` corrected the model-wide treatment counter to `db_mx%treat` and added allocations for `wtp_om_stor`, `wtp_cs_stor`, `wtp_om_out`, `wal_tr_omd`, `wal_tr_omm`, `wal_tr_omy`, and `wal_tr_oma`.

## Review Notes

- Direct file I/O exists; verify file meanings and units before finalizing.
- warning: missing_doc: Procedure 'water_treatment_read' has no extracted documentation comment.
