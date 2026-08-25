---
kind: procedure
symbol: sd_hydsed_read
title: sd_hydsed_read
status: filled
source_hash: 85a2e9401e4775b8
version_label: SWAT+ 62.0.0
locals:
  titldum: Scratch character buffer used to read and discard title or blank/header rows while
    scanning and rereading the input files.
  header: Scratch character buffer used to read the second header line from each file before
    the data records are counted or loaded.
  eof: I/O status flag from `read` statements; `0` means continue, negative values stop the
    scan or loading loops at end-of-file.
  imax: Temporary counter for the number of data records found in the current file; used to
    size `sd_chd` or `sd_chd1` and copied into the shared maximum counters.
  i_exist: Logical flag from `inquire` that tells the routine whether the configured file
    is present before attempting to open it.
  idb: Loop index for reading each data record into `sd_chd(idb)` or `sd_chd1(idb)` after
    the array has been sized.
  ts_sed: Chosen size for the hydrograph timing arrays; set to the larger of 10 and `time%step`
    so the arrays are long enough for the current routing timestep.
uses:
  input_file_module: This module provides `in_cha%hyd_sed`, the configured filename for the
    hyd-sed-lte channel input table. Without it, the routine would not know which file to
    count and read.
  sd_channel_module: These channel-module variables are the shared outputs and working arrays
    that this routine populates for later channel sediment processing. `sd_chd` and `sd_chd1`
    hold the parsed table records, while `timeint`, `hyd_rad`, `trav_time`, `flo_dep`, and
    `maxint` support hydrograph-based routing setup.
  channel_velocity_module: The module is imported by this routine, but no specific symbols
    from it are referenced in the extracted source lines. The source packet does not show
    any direct use here, so its role is uncertain from the available evidence.
  maximum_data_module: This module stores the shared maximum-record counts that this reader
    computes. Updating `db_mx%ch_lte` and `db_mx%ch_sednut` makes the loaded table sizes available
    to later channel initialization and downstream code that allocates or loops over these
    records.
  hydrograph_module: The module is imported alongside the channel sediment tables, but no
    concrete symbols from it are referenced in the visible source. It likely supports the
    hydrograph-related arrays being initialized here, but the extracted packet does not identify
    a direct symbol use.
  time_module: '`time%step` determines the minimum size of the hydrograph timing arrays. The
    routine uses it to pick `ts_sed = max(10, time%step)`, so the arrays are large enough
    for the current routing time resolution.'
---

<!-- facts:header -->

Reads channel hydrology-sediment lookup tables and stores them in shared channel-state arrays.

## Bottom Line

sd_hydsed_read loads two channel data files: the hyd-sed-lte channel table named by `in_cha%hyd_sed`, and the fixed `sed_nut.cha` nutrient/sediment table. It first sizes the tables by counting data rows, then rewinds and reads each record into `sd_chd` and `sd_chd1`, while also updating the shared maxima `db_mx%ch_lte`, `db_mx%ch_sednut`, and `maxint`.

The routine also allocates and initializes the hydrograph timing arrays `timeint`, `hyd_rad`, `trav_time`, and `flo_dep` using `time%step` to choose the array length. Its results are used later by channel sediment routing and channel process setup, which expect these shared arrays and counts to be populated before channel initialization continues.

## Arguments

<!-- facts:arguments -->

## Where It Fits

This routine runs during channel-process setup, immediately after `ch_read_init` and `ch_read_init_cs` in `proc_cha`. It prepares the shared channel sediment lookup tables before later channel readers and `sd_hydsed_init` rely on them.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. Initialize counters and hydrograph array size. | Reset `eof` and `imax`, set `maxint`, compute `ts_sed` from `time%step`, and allocate the hydrograph timing arrays with zero initialization. |
| 2. Check whether the hyd-sed-lte file can be read. | Test whether `in_cha%hyd_sed` exists and is not the string `null`; if not, create a minimal `sd_chd` allocation and skip the file-reading path. |
| 3. Count hyd-sed-lte data records. | Open the hyd-sed file, read past title and header rows, count remaining records by incrementing `imax` until end-of-file, and copy that count into `db_mx%ch_lte`. |
| 4. Allocate and load hyd-sed table records. | Allocate `sd_chd(0:imax)`, rewind the file, skip the title and header again, and read each record into `sd_chd(idb)` for all counted channel entries. |
| 5. Check whether the sed_nut file can be read. | Test whether `sed_nut.cha` exists and is not `null`; if not, allocate a minimal `sd_chd1` array and skip the file-reading path. |
| 6. Count sed_nut data records. | Open `sed_nut.cha`, read past title and header rows, count the remaining records by incrementing `imax`, and store the result in `db_mx%ch_sednut`. |
| 7. Allocate and load sed_nut table records. | Allocate `sd_chd1(0:imax)`, rewind the file, skip the title and header again, and read each record into `sd_chd1(idb)`. |
| 8. Close the active input unit and return. | Close unit 1 after finishing both file passes and return to the caller. |

## Modules Used

<!-- facts:uses -->

| Module | State touched | Key components |
| --- | --- | --- |
| [sym:input_file_module] | `in_cha` | `in_cha%hyd_sed` |
| [sym:sd_channel_module] | `timeint, hyd_rad, trav_time, flo_dep, sd_chd, sd_chd1, maxint` |  |
| [sym:channel_velocity_module] | `channel_velocity_module` |  |
| [sym:maximum_data_module] | `db_mx` | `db_mx%ch_lte, db_mx%ch_sednut` |
| [sym:hydrograph_module] | `hydrograph_module` |  |
| [sym:time_module] | `time` | `time%step` |

## Local Variables

<!-- facts:locals -->

## State Changes

| Target | When | Meaning |
| --- | --- | --- |
| `maxint` | When `time%step` is less than 10, `ts_sed` is set to 10; otherwise it is set to `time%step`. | `maxint` is not changed by this routine; `ts_sed` controls the size of the shared hydrograph timing arrays so they can hold at least 10 slots and enough slots for the current routing timestep. |
| `db_mx%ch_lte` | After the hyd-sed-lte file is counted successfully, `db_mx%ch_lte` is set to the number of data rows found in that file. | `db_mx%ch_lte` records how many hyd-sed channel entries were read so later channel routines can allocate and loop over the same number of records. |
| `db_mx%ch_sednut` | After the `sed_nut.cha` file is counted successfully, `db_mx%ch_sednut` is set to the number of data rows found in that file. | `db_mx%ch_sednut` records how many sediment/nutrient channel entries were read so later channel routines can allocate and loop over the same number of records. |

## File I/O

<!-- facts:io -->


## Lineage

Four lineage commits were resolved. The routine was added in df07e3f, 35b029c changed the hydrograph array allocation to use `time%step` with a `ts_sed` helper instead of fixed size 10, and 39fabde initialized local scalars and allocated the timing arrays with `source = 0.`. The 94b6dec import kept the file-counting and table-loading logic while preserving the two-file read structure.

- df07e3f introduced the subroutine and its two-pass file loading of `hyd-sed-lte.cha` and `sed_nut.cha`, along with the shared array allocations and count propagation into `db_mx`.
- 35b029c replaced the fixed 10-element hydrograph allocations with `ts_sed = max(10, time%step)`, making the timing arrays responsive to the current routing step count.
- 39fabde initialized `titldum`, `header`, `eof`, `imax`, `idb`, and `ts_sed`, and changed the hydrograph array allocations to use `source = 0.` for zero-filled initialization.

## Review Notes

- Direct file I/O exists; verify file meanings and units before finalizing.
- warning: missing_doc: Procedure 'sd_hydsed_read' has no extracted documentation comment.
- channel_velocity_module and hydrograph_module are imported but no direct symbol references were resolved in the extracted source.
