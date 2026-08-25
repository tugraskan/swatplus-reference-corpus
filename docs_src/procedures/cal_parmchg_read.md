---
kind: procedure
symbol: cal_parmchg_read
title: cal_parmchg_read
status: filled
source_hash: d0e7d5505bfdc9a3
version_label: SWAT+ 62.0.0
locals:
  titldum: Holds the file title line read from `calibration.cal` before the routine starts
    parsing the update blocks.
  header: Holds the header line that follows the title and precedes the update records in
    `calibration.cal`.
  range: Temporary text token used while reading each condition line; it detects whether the
    next record is a `range` condition or a full condition record.
  eof: I/O status flag for reads from unit 107; negative values are used to stop on end-of-file
    or read failure.
  imax: Working counter initialized to zero but not used in the visible parsing logic.
  nspu: Holds the number of special unit groups or object-group entries read from an update
    record so the routine can decide whether to expand explicit element lists.
  i_exist: Tracks whether the calibration change file exists before the routine tries to open
    it.
  i: Loop counter for each calibration update record in `cal_upd`.
  ie: Loop counter used to initialize the explicit element-number array `cal_upd(i)%num`.
  mcal: Number of calibration updates declared in the file; used to allocate `cal_upd`.
  isp: Loop counter used while reading the list of element counts for each special unit group.
  ical: Loop counter over the calibration-parameter database used to crosswalk an update name
    to its database index.
  ipar: Holds the resolved calibration-parameter index for the current update before its object
    type is examined.
  ielem1: Receives the expanded number of explicit element IDs returned by `define_unit_elements`.
  nconds: Local copy of the number of conditions attached to the current update; used to allocate
    and read `cal_upd(i)%cond`.
  icond: Loop counter for each condition attached to the current update.
uses:
  input_file_module: The routine gets the calibration update filename from `in_chg%cal_upd`,
    so `input_file_module` supplies the file path that controls whether any parsing happens
    at all.
  maximum_data_module: The maximum-count fields in `db_mx` cap or describe how many calibration
    parameters and related file-backed objects exist, and `cal_parmchg_read` uses them to
    size loops and choose object counts for update targets.
  calibration_data_module: 'The `cal_upd` and `cal_parms` arrays are the routine''s main working
    data: it fills update records, matches names to parameter definitions, stores condition
    objects, and builds the element-number lists that later calibration logic consumes.'
  hydrograph_module: The spatial-object counts in `sp_ob` tell the routine how many HRUs,
    routing units, aquifers, channels, reservoirs, and SWAT-deg channels exist when an update
    applies to all objects of that type.
  gwflow_module: The groundwater-flow cell count `ncell` is the fallback total used when an
    update targets `gwf` objects, so it determines the size of the explicit element list for
    groundwater calibration updates.
---

<!-- facts:header -->

Reads the calibration change file and builds the in-memory update definitions used by calibration processing.

## Bottom Line

cal_parmchg_read opens the calibration change file named by `in_chg%cal_upd`, counts and reads each update record, and stores the result in the `cal_upd` array. It also crosswalks each update name to the calibration-parameter database, reads any conditional rules, and expands the target element list so later calibration code knows exactly which objects or cells are affected.

If an update applies to all objects of a type, the routine derives the element count from model state such as `sp_ob`, `db_mx`, or `ncell` and fills `cal_upd(i)%num` with a simple 1..N sequence. If the update lists specific defining units, it calls `define_unit_elements` to translate those groups into explicit element numbers before saving them in `cal_upd(i)%num`.

## Arguments

<!-- facts:arguments -->

## Where It Fits

This routine runs during the calibration setup phase, immediately after `cal_parm_read` and before plant-region calibration, calibration condition processing, and soft-code reading in `proc_cal`. Its output is the parsed `cal_upd` table and related counts, which later calibration routines use to apply parameter changes to the correct objects and elements.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. Check whether the calibration update file exists and is usable | The routine inquires on `in_chg%cal_upd`; if the file is missing or set to the literal `null`, it allocates an empty `cal_upd(0:0)` array and stops file parsing. |
| 2. Open and start scanning the update file | It opens unit 107 on `in_chg%cal_upd`, reads the title and update-count lines, allocates `cal_upd(mcal)`, and then reads the file header before entering the per-update loop. |
| 3. Read each update's basic fields | For each update, it reads the name, change type, value, condition count, soil-layer bounds, year/day bounds, and a temporary `nspu` count; if the read fails, it exits the loop. |
| 4. Optionally reread the record with explicit element counts | When `nspu > 0`, it backs up one record, allocates `elem_cnt`, and rereads the same update line including `num_tot` and the per-group element counts. |
| 5. Crosswalk the update name to the calibration parameter table | It searches `cal_parms` for a matching parameter name and stores the matching database index in `cal_upd(i)%num_db`. |
| 6. Read any attached conditions | If the update declares conditions, it allocates `cal_upd(i)%cond`, then reads each condition line either as a `range` record with bounds or as a full condition object. |
| 7. Build an all-object target list when no explicit objects were listed | If `num_tot` is zero, it uses the matched parameter object type to choose a total count from `sp_ob`, `db_mx`, or `ncell`, allocates `cal_upd(i)%num`, and fills it with the sequence 1..num_elem. |
| 8. Expand explicit defining-unit groups when objects were listed | If `num_tot` is nonzero, it calls `define_unit_elements`, allocates `cal_upd(i)%num` to the returned length, copies `defunit_num` into it, stores the final count, and deallocates `defunit_num`. |
| 9. Record the total number of calibration updates | After parsing, it stores `mcal` in `db_mx%cal_upd` so the rest of the calibration workflow knows how many update records were loaded. |

## Modules Used

<!-- facts:uses -->

| Module | State touched | Key components |
| --- | --- | --- |
| [sym:input_file_module] | `in_chg` | `in_chg%cal_upd` |
| [sym:maximum_data_module] | `db_mx` | `db_mx%cal_parms, db_mx%dtbl_res, db_mx%plantparm, db_mx%ch_nut, db_mx%pcpfiles, db_mx%tmpfiles, db_mx%cal_upd` |
| [sym:calibration_data_module] | `cal_upd, cal_parms` | `cal_upd(i)%name, cal_upd(i)%chg_typ, cal_upd(i)%val, cal_upd(i)%conds, cal_upd(i)%lyr1, cal_upd(i)%lyr2, cal_upd(i)%year1, cal_upd(i)%year2, cal_upd(i)%day1, cal_upd(i)%day2, cal_upd(i)%num_tot, cal_parms(ical)%name, cal_upd(i)%num_db, cal_upd(i)%cond(nconds), cal_upd(i)%cond(icond)%var, cal_upd(i)%val1, cal_upd(i)%val2, cal_upd(i)%cond(icond), cal_parms(ipar)%ob_typ, cal_upd(i)%num_elem, cal_upd(i)%num(ie), cal_upd(i)%num(ielem1), cal_upd(i)%num` |
| [sym:hydrograph_module] | `sp_ob, elem_cnt, aqu, res, defunit_num` | `sp_ob%hru, sp_ob%hru_lte, sp_ob%ru, sp_ob%aqu, sp_ob%chan, sp_ob%res, sp_ob%chandeg` |
| [sym:gwflow_module] | `ncell` |  |

## Local Variables

<!-- facts:locals -->

## State Changes

| Target | When | Meaning |
| --- | --- | --- |
| `cal_upd(i)%num_db` | When a calibration update record is parsed and `num_tot == 0`, after `num_db` has been resolved from `cal_parms`. | `cal_upd(i)%num_db` changes from its default zero to the matching calibration-parameter index so later logic can locate the parameter definition associated with the update name. |
| `cal_upd(i)%num_elem` | When `cal_upd(i)%num_tot == 0` and the routine selects a model object type from `cal_parms(ipar)%ob_typ`. | `cal_upd(i)%num_elem` is set to the total number of target objects for the chosen type, using counts such as `sp_ob%hru`, `db_mx%plantparm`, or `ncell`, so the routine can size the explicit target list. |
| `cal_upd(i)%num(ie)` | When `cal_upd(i)%num_tot == 0` and the routine is filling the default target list with `do ie = 1, cal_upd(i)%num_elem`. | `cal_upd(i)%num(ie)` is populated with the element index `ie`, creating a 1..N list of all targets for the update. |
| `cal_upd(i)%num` | When `cal_upd(i)%num_tot > 0` and `define_unit_elements` has returned the expanded defining-unit list length in `ielem1`. | `cal_upd(i)%num` is allocated to the expanded length and filled from `defunit_num`, so the update targets the explicit element numbers named in the file. |
| `db_mx%cal_upd` | After file parsing completes, regardless of whether the file was absent, empty, or fully read. | `db_mx%cal_upd` is set to the number of calibration updates read from the file, giving later calibration setup code the loaded update count. |

## File I/O

<!-- facts:io -->


## Lineage

`cal_parmchg_read.f90` was introduced in `df07e3f` (2024-03-05, "init all") and has been changed in 11 non-merge commit(s) since, most recently `b78c4ea` (2026-04-04, "gwflow re-merge: calibration wiring, canal-wallo unification, gfortran portabili…"). Lineage is reconstructed from commit metadata (SHA, date, subject); per-line diffs were unavailable in this build environment, so only the commits touching `cal_parmchg_read.f90` are listed.

- `b78c4ea` (2026-04-04) — gwflow re-merge: calibration wiring, canal-wallo unification, gfortran portability, dynamic array sizes
- `bd18ad4` (2025-11-24) — Pr 107 (#108)
- `10c2afa` (2025-02-06) — Added a new character variable `range` ; Modified the reading logic of cal_upd to handle the new `range` variable. If `range` equals "range"…
- `889136d` (2025-02-03) — Fix typos
- `3bb22ed` (2024-12-31) — souirce code updates
- `df07e3f` (2024-03-05) — init all

## Review Notes

- Direct file I/O exists; verify file meanings and units before finalizing.
- warning: missing_doc: Procedure 'cal_parmchg_read' has no extracted documentation comment.
- The routine reads `calibration.cal` through unit 107 and uses both `backspace` and rereads to reinterpret records.
- Lineage evidence reported no resolved commits for this source span.
- Lineage was reconstructed from file-level commit metadata; per-line diffs were unavailable in this environment (blobless clone), so line-span filtering was not applied.
