---
kind: procedure
symbol: cal_parm_read
title: cal_parm_read
status: filled
source_hash: 55c086fbefa565ba
version_label: SWAT+ 62.0.0
locals:
  titldum: Holds the first line from `cal_parms.cal`, used as a title/label record that is
    read and discarded before the actual change-count line.
  header: Holds the header line that appears after the change count; it is read and discarded
    before the parameter records are loaded.
  eof: Receives the IOSTAT status from each `read` on unit 107; negative values signal end-of-file
    and stop the scan.
  imax: Initialized but not used in the visible source; it appears intended as a maximum-record
    counter, but this routine never updates it.
  mchg_par: Stores the number of calibration-parameter change records declared in `cal_parms.cal`,
    and drives the allocation and read loop size.
  i_exist: Flags whether the file named by `in_chg%cal_parms` exists before the routine tries
    to open it.
  i: Loop counter used to step through the `mchg_par` calibration-parameter records when reading
    them into `cal_parms(i)`.
uses:
  input_file_module: '`input_file_module` provides `in_chg%cal_parms`, the configured filename
    for the calibration-change file. The routine uses that path both to test file existence
    and to open the file it reads.'
  maximum_data_module: '`maximum_data_module` provides `db_mx%cal_parms`, the shared counter
    that records how many calibration-parameter entries were found. That count is needed by
    later calibration routines that size or iterate over the loaded change set.'
  calibration_data_module: '`calibration_data_module` owns the allocatable `cal_parms` array
    that holds the parsed calibration-parameter change records. This routine allocates and
    fills that shared array so the rest of the calibration workflow can use it.'
---

<!-- facts:header -->

Reads the calibration-parameter change file named in `in_chg%cal_parms`, counts the requested changes, and loads them into the global `cal_parms` array.

## Bottom Line

`cal_parm_read` is a small file-reader used during calibration setup. It checks whether the configured calibration-change file exists and is not set to the sentinel name `null`; if not, it allocates a one-element `cal_parms` array. Otherwise it opens the file on unit 107, reads and skips the title line, reads the number of parameter changes (`mchg_par`), allocates `cal_parms(0:mchg_par)`, skips the header line, and reads each change record into `cal_parms(i)`.

After the file is read, the routine stores the count in `db_mx%cal_parms` so later calibration code knows how many parameter-change entries are available. `proc_cal` calls this routine near the start of calibration-data loading, before other calibration and soft-data readers run.

## Arguments

<!-- facts:arguments -->

## Where It Fits

This routine runs during calibration initialization, when `proc_cal` begins reading calibration-related inputs. `proc_cal` prepares the overall calibration workflow and calls `cal_parm_read` before later readers such as `cal_parmchg_read`, `pl_read_regions_cal`, and `pl_read_parms_cal`. Its results matter because downstream calibration logic depends on the loaded `cal_parms` array and the `db_mx%cal_parms` count to know how many parameter-change entries are available.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. Check whether the configured calibration-change file can be used | The routine tests `inquire (file=in_chg%cal_parms, exist=i_exist)` and also checks whether the configured filename is the sentinel string `null`. If the file is missing or disabled, it allocates a minimal `cal_parms(0:0)` array instead of trying to read records. |
| 2. Open the calibration-change file for reading | When the file is usable, the routine opens `in_chg%cal_parms` on unit 107 and reads the first record into `titldum`. This begins the scan of the `cal_parms.cal` input file. |
| 3. Read the declared number of parameter changes | The routine reads the next record into `mchg_par`, using it as the count of calibration changes to expect. If end-of-file is reached, the scan exits early. |
| 4. Allocate storage for the change records | Using `mchg_par`, the routine allocates `cal_parms(0:mchg_par)` so the shared calibration-data array can hold the declared number of entries. |
| 5. Skip the header line and load each change record | The routine reads and discards `header`, then loops `i = 1, mchg_par` reading each record into `cal_parms(i)`. Any end-of-file during this loop stops the scan early. |
| 6. Publish the record count to shared maximum-data state | After the scan, the routine assigns `db_mx%cal_parms = mchg_par` so the rest of the model can see how many calibration-parameter changes were loaded. |

## Modules Used

<!-- facts:uses -->

| Module | State touched | Key components |
| --- | --- | --- |
| [sym:input_file_module] | `in_chg` | `in_chg%cal_parms` |
| [sym:maximum_data_module] | `db_mx` | `db_mx%cal_parms` |
| [sym:calibration_data_module] | `cal_parms` |  |

## Local Variables

<!-- facts:locals -->

## State Changes

| Target | When | Meaning |
| --- | --- | --- |
| `db_mx%cal_parms` | After the file is scanned, regardless of whether the file existed or was disabled, `db_mx%cal_parms` is assigned the final value of `mchg_par`. | This shared maximum-data counter records how many calibration-parameter change entries were found in `cal_parms.cal`. Later calibration routines can use that count to size loops or validate the loaded `cal_parms` array. |

## File I/O

<!-- facts:io -->


## Lineage

Three resolved commits changed `cal_parm_read`. The initial add in `df07e3f` introduced the routine and its current file-reading workflow. `39fabde` initialized the local variables (`titldum`, `header`, `eof`, `imax`, `mchg_par`, and `i`) with default values; the file-reading logic itself was unchanged. `889136d` only corrected a typo in the inline purpose comment from 'paramter' to 'parameter'.

- df07e3f added the subroutine, the `inquire`/`open`/`read` loop over `cal_parms.cal`, allocation of `cal_parms(0:mchg_par)`, and the assignment to `db_mx%cal_parms`.
- 39fabde changed local variable declarations to include default initial values but did not alter the reading algorithm or shared-state updates.
- 889136d made a comment-only spelling fix in the purpose text and did not change runtime behavior.

## Review Notes

- Direct file I/O exists; verify file meanings and units before finalizing.
- warning: missing_doc: Procedure 'cal_parm_read' has no extracted documentation comment.
