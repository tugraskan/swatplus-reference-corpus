---
kind: procedure
symbol: topo_read
title: topo_read
status: filled
source_hash: 5236b49b00929261
version_label: SWAT+ 62.0.0
locals:
  titldum: Temporary string buffer used to read and skip the title line and later the first
    data/header line from `topography.hyd`.
  header: Temporary string buffer used to read the file header line(s) before the actual topography
    records are loaded.
  eof: I/O status flag for each `read`; it detects end-of-file or read failure while counting
    and loading records.
  imax: Counter for the number of topography data records found in `topography.hyd`; it also
    sets the allocation size for `topo_db`.
  i_exist: Logical flag set by `inquire` to tell whether the configured topography input file
    exists before attempting to open it.
  mtopo: Unused local counter that is initialized to zero but not referenced after setup in
    this routine.
  ith: Loop index used to read each topography record into `topo_db(ith)`.
uses:
  input_file_module: This module provides `in_hyd%topogr_hyd`, the configured path to the
    topography input file. `topo_read` uses that path to decide which file to open and whether
    the file should be treated as absent or disabled.
  maximum_data_module: This module holds `db_mx%topo`, the shared maximum-count field for
    topography inputs. `topo_read` updates it after counting records so the rest of the model
    knows how many topography entries were loaded.
  topography_data_module: This module owns the allocatable `topo_db` array that stores the
    parsed topography records. `topo_read` allocates and fills that shared database so later
    routines can use the loaded values.
---

<!-- facts:header -->

Reads the topography input file, counts its data records, and loads them into `topo_db`.

## Bottom Line

`topo_read` is the topography-file loader used during SWAT+ input reading. It checks whether `in_hyd%topogr_hyd` points to a real file, allocates `topo_db` to fit the file contents, and then reads each topography record into the shared topography database.

It also records the number of loaded topography entries in `db_mx%topo`. That count is used later as the model’s maximum topography-file element count, so downstream code can size or iterate over the loaded topography data safely.

## Arguments

<!-- facts:arguments -->

## Where It Fits

`topo_read` runs during the central input-read sequence in `proc_read`, immediately after several other database readers and before `field_read` and `hydrol_read`. Its result matters later because the loaded `topo_db` contents and `db_mx%topo` count become the shared topography state used by downstream model setup and processing.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. Initialize counters and flags | Set temporary buffers and counters to known starting values, including zeroing `eof`, `imax`, and `mtopo` before any file I/O begins. |
| 2. Test whether the configured topography file exists | Use `inquire` on `in_hyd%topogr_hyd` to determine whether the file is present; if it is missing or explicitly set to `null`, allocate a one-element placeholder `topo_db(0:0)` and skip data loading. |
| 3. Open the topography file | Open `topography.hyd` on unit 107 so the routine can scan the file contents. |
| 4. Read and skip file prologue | Read the title and header lines into temporary character buffers and stop early if the file ends before the expected prologue is present. |
| 5. Count data records | Loop through the remaining records, incrementing `imax` once per successful read until end-of-file or a read error is encountered. |
| 6. Allocate the topography database | Allocate `topo_db(0:imax)` so the shared topography database has exactly enough slots for the counted records. |
| 7. Rewind and reread the file header | Rewind unit 107 to the beginning of `topography.hyd` and reread the title and header lines to position the file at the first data record. |
| 8. Load each topography record | Read each record into `topo_db(ith)` for `ith = 1..imax`, stopping early if an I/O status error indicates the file ended unexpectedly. |
| 9. Exit the open/read loop | Leave the surrounding `do` block after one successful load pass; the code is structured to perform the open-scan-rewind-load sequence once. |
| 10. Close the file and publish the count | Close unit 107 and store the final record count in `db_mx%topo` so other routines can use the loaded topography size. |

## Modules Used

<!-- facts:uses -->

| Module | State touched | Key components |
| --- | --- | --- |
| [sym:input_file_module] | `in_hyd` | `in_hyd%topogr_hyd` |
| [sym:maximum_data_module] | `db_mx` | `db_mx%topo` |
| [sym:topography_data_module] | `topo_db` |  |

## Local Variables

<!-- facts:locals -->

## State Changes

| Target | When | Meaning |
| --- | --- | --- |
| `db_mx%topo` | After counting records in `topography.hyd`, `db_mx%topo` is set to the final value of `imax`. | This updates the shared maximum topography element count to match the number of loaded records, making the size of the topography database visible to later routines. |

## File I/O

<!-- facts:io -->


## Lineage

The procedure was added in commit df07e3f with the full file-reading workflow: existence check, record counting, allocation, rewind, record loading, and final count storage. Commit 39fabde did not change behavior, but initialized the local scalars `titldum`, `header`, `eof`, `imax`, `mtopo`, and `ith` to zero or empty-string defaults. Commit bd18ad4 added `external :: search` near the top of the routine without changing the topography I/O logic.

- df07e3f introduced `topo_read` and its complete topography-file loading sequence, including allocation of `topo_db` and assignment to `db_mx%topo`.
- 39fabde changed only local-variable initialization defaults for `titldum`, `header`, `eof`, `imax`, `mtopo`, and `ith`.
- bd18ad4 added an `external :: search` declaration but did not alter the reading algorithm.

## Review Notes

- Direct file I/O exists; verify file meanings and units before finalizing.
- warning: missing_doc: Procedure 'topo_read' has no extracted documentation comment.
- algorithm_steps revised: merged the original scan/allocate/load split into a file-oriented sequence that matches the source lines and added explicit open/rewind/close steps.
- The source declares `external :: search`, but the routine body shown here does not call `search`; its purpose remains unrelated to the topography loading logic.
- The routine allocates `topo_db(0:0)` when the file is missing or `null`, so the shared database is always at least minimally allocated.
