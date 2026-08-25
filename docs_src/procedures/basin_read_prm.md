---
kind: procedure
symbol: basin_read_prm
title: basin_read_prm
status: filled
source_hash: 8a6567c41e16b9c3
version_label: SWAT+ 62.0.0
locals:
  titldum: Temporary string used to read and ignore the file title line from `parameters.bsn`
    before the actual basin parameter data are read.
  header: Temporary string used to read and ignore the file header line from `parameters.bsn`
    before loading `bsn_prm`.
  eof: I/O status flag for the sequential reads. It is initialized to 0 and checked after
    each read to stop early if end-of-file is reached.
  i_exist: Logical flag set by `inquire` to show whether `in_basin%parms_bas` exists on disk,
    which helps decide whether the routine should try to read basin parameters.
uses:
  input_file_module: This module supplies `in_basin%parms_bas`, the file name that the routine
    opens and reads. Without `input_file_module`, `basin_read_prm` would not know which basin
    parameter file to load.
  basin_module: This module owns `bsn_prm`, the global basin parameter structure that receives
    the data read from `parameters.bsn`. The rest of basin setup uses that populated state
    after this routine returns.
---

<!-- facts:header -->

Reads the basin parameter record from `parameters.bsn` into the global basin parameter structure.

## Bottom Line

This subroutine opens the basin parameter file named by `in_basin%parms_bas`, reads and discards the first two text lines, then reads the basin parameter data into `bsn_prm`. It is a small file-loader, but it matters because later basin setup routines depend on `bsn_prm` being populated before they run.

The routine only does work when the parameter file is expected to exist or has a non-`"null"` name. It also closes the file unit before returning, so it leaves the basin parameter file in a clean state for the rest of the basin initialization sequence.

## Arguments

<!-- facts:arguments -->

## Where It Fits

This routine runs during basin initialization inside `proc_bsn`, after earlier basin readers have set up the input-file state and before later basin routines such as `basin_prm_default`, `basin_print_codes_read`, and carbon-related readers use `bsn_prm`.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. if | Checks whether the basin parameter file is present on disk or has a non-"null" configured name, and only then enters the read sequence. |
| 2. loop | Starts a short loop that wraps the file open and read sequence, though the body exits after one successful pass. |
| 3. io | Opens unit 107 on the basin parameter file named by `in_basin%parms_bas` so the file can be read sequentially. |
| 4. io | Reads and discards the file title line into `titldum`, advancing to the next record. |
| 5. if | Stops the loop immediately if the read hit end-of-file or another terminating I/O condition. |
| 6. io | Reads the header line from the basin parameter file into `header`. |
| 7. if | Stops if the header read reports end-of-file, preventing an invalid basin parameter read. |
| 8. io | Reads the basin parameter data record into the global `bsn_prm` structure. |
| 9. if | Stops if the basin parameter record could not be read to the end of file status. |
| 10. io | Closes unit 107 to release the basin parameter file after the read completes. |
| 11. return | Returns control to the caller after the basin parameter state has been loaded or skipped. |

## Modules Used

<!-- facts:uses -->

| Module | State touched | Key components |
| --- | --- | --- |
| [sym:input_file_module] | `in_basin` | `in_basin%parms_bas` |
| [sym:basin_module] | `bsn_prm` |  |

## Local Variables

<!-- facts:locals -->

## State Changes

| Target | When | Meaning |
| --- | --- | --- |
| `none extracted` | none extracted | No assignment targets were extracted automatically. |

## File I/O

<!-- facts:io -->


## Lineage

Resolved lineage shows three behavior-relevant changes: the file was introduced in df07e3f, the basin parameter read logic was preserved when the source was imported in c7c8e22, and 39fabde initialized the local scratch variables (`titldum`, `header`, and `eof`) while 2ee1889 made only a whitespace-only return-line cleanup.

- df07e3f added the entire `basin_read_prm` subroutine, including the `inquire`, open/read loop, and `close(107)` sequence for loading `bsn_prm` from `parameters.bsn`.
- 39fabde changed the local scratch variables to initialized declarations (`titldum = ""`, `header = ""`, `eof = 0`) and kept the explicit `eof = 0` reset, reducing dependence on uninitialized locals.
- 2ee1889 only adjusted trailing whitespace on `return`; it did not change behavior.

## Review Notes

- Direct file I/O exists; verify file meanings and units before finalizing.
- warning: missing_doc: Procedure 'basin_read_prm' has no extracted documentation comment.
