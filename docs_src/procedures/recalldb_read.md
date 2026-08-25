---
kind: procedure
symbol: recalldb_read
title: recalldb_read
status: filled
source_hash: 9ae756cdb8df3d0d
version_label: SWAT+ 62.0.0
locals:
  titldum: Temporary 80-character string used to read and discard the title line from `recall_db.rec`
    during the initial scan and the final data load.
  header: Temporary 80-character string used to read the header line from `recall_db.rec`
    so the routine can skip file headings before scanning data rows.
  eof: I/O status flag for `read` operations; `0` means continue, negative values trigger
    exit conditions at end-of-file or read failure.
  imax: Tracks the largest recall index found while scanning `recall_db.rec`; becomes the
    allocated size bound and the stored database maximum.
  i: Holds the recall index read from the file during both the scan and the data load; used
    to size the database and address `recall_db(i)`.
  ii: Loop counter used to iterate through the expected number of recall entries when the
    file is rewound and the records are loaded.
  k: Holds the leading integer field from each detailed record line before the associated
    recall database fields are read into `recall_db(i)`.
  iom: Declared but not used in the shown source; likely a leftover I/O status or message
    variable from a prior version.
  i_exist: Logical flag set by `inquire` to indicate whether `recall_db.rec` exists before
    the routine proceeds with file processing.
uses:
  water_allocation_module: This module is imported by `recalldb_read` because recall database
    loading is part of the water-allocation setup path, so the routine must run in the same
    shared model state that later allocation logic will consult.
  maximum_data_module: The routine writes `db_mx%recalldb_max`, so `maximum_data_module` provides
    the shared maximum-record bookkeeping that other parts of the model use to size and validate
    recall-related arrays.
  recall_module: The routine fills `recall_db`, including each entry’s name and constituent
    file descriptors, so `recall_module` supplies the persistent database structure that stores
    all recall file metadata for later use.
  hydrograph_module: The routine allocates `recall`, `rec_d`, `rec_m`, `rec_y`, and `rec_a`
    from `hydrograph_module` because those arrays hold the recall hydrograph inputs that downstream
    hydrograph handling expects after the database has been read.
---

<!-- facts:header -->

Reads `recall_db.rec`, counts and loads recall database entries, and allocates the shared recall/hydrograph storage needed for later simulation use.

## Bottom Line

`recalldb_read` is the setup routine for recall database definitions. It opens `recall_db.rec`, scans the file to find the maximum record index, stores that size in `db_mx%recalldb_max`, and allocates the shared arrays that hold recall metadata and hydrograph inputs.

It then rewinds the file and loads each recall entry into `recall_db(i)` before calling `recall_read(i)` to process the per-recall input files. That makes the recall data available to later water-allocation and hydrograph processing.

## Arguments

<!-- facts:arguments -->

## Where It Fits

`recalldb_read` runs during model initialization, after the recall database file name is available and before recall-driven hydrograph or constituent processing begins. It prepares the shared recall database and allocates the arrays that later routines use when building recall inputs for the simulation.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. Check whether the recall database file should be processed | The routine uses `inquire` to test whether `recall_db.rec` exists, then enters the processing block when the file is present or the file name is not the literal string `null`. |
| 2. Open and scan the file header and record indices | It opens unit 107 on `recall_db.rec`, reads the title and header lines, then loops through the remaining index values to find the largest recall index in the file. |
| 3. Store the maximum recall database size | The computed maximum index is saved in `db_mx%recalldb_max` so the rest of the model knows how many recall database entries are available. |
| 4. Allocate shared recall and hydrograph arrays | The routine allocates `recall_db`, `recall`, `rec_d`, `rec_m`, `rec_y`, and `rec_a` using the maximum index it just found. |
| 5. Rewind the file and reread the header | It rewinds unit 107 and reads the title and header lines again so the second pass starts from the beginning of the file. |
| 6. Load each recall database record | For each expected record, the routine reads the leading index, backs up one record, and rereads the full line into `recall_db(i)` fields for the recall name and constituent file definitions. |
| 7. Process the referenced recall file for each entry | After loading each database row, the routine calls `recall_read(i)` so the per-entry recall input files are read and stored in the shared model state. |
| 8. Close the file when processing is finished | After the outer block ends, the routine closes unit 107 to release `recall_db.rec`. |

## Modules Used

<!-- facts:uses -->

| Module | State touched | Key components |
| --- | --- | --- |
| [sym:water_allocation_module] | `water_allocation_module` |  |
| [sym:maximum_data_module] | `db_mx` | `db_mx%recalldb_max` |
| [sym:recall_module] | `recall_db` | `recall_db(i)%name, recall_db(i)%org_min, recall_db(i)%pest, recall_db(i)%path, recall_db(i)%hmet, recall_db(i)%salt, recall_db(i)%constit` |
| [sym:hydrograph_module] | `recall, rec_d, rec_m, rec_y, rec_a` |  |

## Local Variables

<!-- facts:locals -->

## State Changes

| Target | When | Meaning |
| --- | --- | --- |
| `db_mx%recalldb_max` | When `recall_db.rec` exists or the file name is not `null` and the scan finds a maximum recall index. | `db_mx%recalldb_max` is updated to the largest recall index found in the file so later allocation and iteration logic can size recall-related arrays correctly. |

## File I/O

<!-- facts:io -->


## Lineage

Three resolved commits changed `recalldb_read`: df07e3f added the procedure and its initial scan/load logic, 080211e added hydrograph-module allocations and the per-entry `call recall_read(i)`, and e24da22 only changed the subroutine indentation at the top of the file.

- df07e3f introduced the new `recalldb_read` routine that scans `recall_db.rec`, sets `db_mx%recalldb_max`, allocates `recall_db`, and loads each database record.
- 080211e expanded the routine to use `hydrograph_module`, allocate `recall`, `rec_d`, `rec_m`, `rec_y`, and `rec_a`, and invoke `recall_read(i)` for each loaded recall entry.
- e24da22 made a formatting-only change to the subroutine declaration and did not alter behavior.

## Review Notes

- Direct file I/O exists; verify file meanings and units before finalizing.
- warning: missing_doc: Procedure 'recalldb_read' has no extracted documentation comment.
- algorithm_steps revised: split the scan/load logic into distinct steps and added a separate close-file step to match the visible source lines.
- The source includes an unconditional-looking `if (i_exist .or. "recall_db.rec" /= "null")` check; the file-name comparison is effectively always true for this literal and may reflect a legacy pattern.
- `iom` is declared in the source but not referenced elsewhere in the shown routine.
