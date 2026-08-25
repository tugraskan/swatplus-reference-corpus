---
kind: procedure
symbol: ch_read_sed
title: ch_read_sed
status: filled
source_hash: 4208b0e9c67d98d2
version_label: SWAT+ 62.0.0
locals:
  eof: I/O status flag for all reads from unit 105. It starts at 0, is updated by `read(...,
    iostat=eof)`, and is tested to detect end-of-file or read failure while counting records
    and loading `sediment.cha`.
  imax: Counts how many channel sediment records were found in `sediment.cha` during the first
    scan. That total is then used to set `db_mx%ch_sed` and to allocate `ch_sed(0:imax)`.
  titldum: Temporary string used to read and discard title or blank/data marker lines from
    `sediment.cha` before the actual `ch_sed(ich)` record is read.
  header: Temporary string used to read the file header line from `sediment.cha` during the
    initial scan and after rewind, so the routine can skip non-data lines before reading channel
    records.
  i_exist: Logical flag set by `inquire(file=in_cha%sed,exist=i_exist)` to decide whether
    the configured sediment file exists and should be read.
  sumerod: Accumulator used to sum the 12 monthly erosion fractions in `ch_sed(ich)%erod`
    so the routine can detect when no erosion schedule was supplied.
  ich: Loop counter for channel sediment records. It indexes each element of `ch_sed` as the
    file is loaded and standardized.
  mo: Monthly index from 1 to 12 used to sum and, if needed, populate the monthly erosion
    fraction array `ch_sed(ich)%erod(mo)`.
uses:
  input_file_module: This module provides `in_cha%sed`, the configured path to the channel
    sediment input file. `ch_read_sed` cannot determine which file to open without that shared
    input-file setting.
  maximum_data_module: This module holds `db_mx%ch_sed`, the shared count of channel sediment
    records. The routine stores the scanned record total there so later channel-model code
    knows how many `ch_sed` entries are valid.
  channel_data_module: This module defines the `ch_sed` allocatable array and its component
    fields. `ch_read_sed` allocates the array, reads each record into `ch_sed(ich)`, and then
    adjusts fields such as `eqn`, `cov1`, `cov2`, `bnk_kd`, `bed_kd`, and `erod` before later
    channel processes use them.
---

<!-- facts:header -->

Reads and standardizes the channel sediment input file for SWAT+ channel routing. It sizes the channel sediment database, loads each channel's sediment parameters, and fills missing values with model defaults.

## Bottom Line

`ch_read_sed` opens the channel sediment file named by `in_cha%sed`, counts how many channel sediment records it contains, allocates `ch_sed`, and then reads each record into `ch_sed(ich)` while storing the record count in `db_mx%ch_sed`. If the configured file is missing or set to `null`, it allocates a one-element placeholder array instead of reading data.

After loading each channel's sediment settings, the routine applies default values and bounds for routing method, cover factors, grain size, bulk density, erodibility coefficients, and monthly erosion fractions. Those values become the channel sediment state used later by channel-process code.

## Arguments

<!-- facts:arguments -->

## Where It Fits

This routine runs during channel initialization in `proc_cha`, after channel hydraulics are read and before later channel input routines and routing code rely on sediment parameters. Its results supply the channel sediment database used by downstream channel erosion and routing behavior.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. Check whether the configured sediment file exists | The routine tests `in_cha%sed` with `inquire`, and if the file is missing or explicitly set to `null`, it allocates a minimal `ch_sed(0:0)` array instead of reading any sediment records. |
| 2. Open and scan the file to count data records | The routine opens unit 105 on `sediment.cha`, skips the title and header lines, then loops through the remaining records to count how many channel sediment entries are present in `imax`. |
| 3. Store the record count and allocate channel sediment storage | The counted record total is copied to `db_mx%ch_sed`, and `ch_sed(0:imax)` is allocated so the shared channel sediment array matches the file size. |
| 4. Rewind and skip file prologue again | The routine rewinds unit 105 and rereads the title and header lines so it can restart at the beginning of the data section before loading records. |
| 5. Read each channel sediment record | For each channel index from 1 to `db_mx%ch_sed`, the routine reads a record token, backs up one line, then reads the structured record into `ch_sed(ich)`. |
| 6. Normalize transport, cover, and grain-size defaults | The routine forces nonpositive critical shear stresses to zero, selects sediment routing defaults through `eqn`, constrains `cov1` and `cov2` to valid ranges, and assigns default bank and bed particle sizes when they were not supplied. |
| 7. Normalize density and erodibility defaults | The routine assigns default bank and bed bulk density values, then fills missing bank and bed erodibility coefficients from the corresponding critical shear stress using the Hanson and Simon-based estimate. |
| 8. Fill monthly erosion fractions if none were provided | The routine sums the 12 monthly erosion fractions and, if they are all effectively zero, replaces each month with the channel cover factor `cov1`. |
| 9. Finish the file read and exit | After the channel records have been processed, the routine exits the loop, closes unit 105, and returns to the caller. |

## Modules Used

<!-- facts:uses -->

| Module | State touched | Key components |
| --- | --- | --- |
| [sym:input_file_module] | `in_cha` | `in_cha%sed` |
| [sym:maximum_data_module] | `db_mx` | `db_mx%ch_sed` |
| [sym:channel_data_module] | `ch_sed` | `ch_sed(ich)%tc_bnk, ch_sed(ich)%tc_bed, ch_sed(ich)%eqn, ch_sed(ich)%cov1, ch_sed(ich)%cov2, ch_sed(ich)%bnk_d50, ch_sed(ich)%bed_d50, ch_sed(ich)%bnk_bd, ch_sed(ich)%bed_bd, ch_sed(ich)%bnk_kd, ch_sed(ich)%bed_kd, ch_sed(ich)%erod(mo)` |

## Local Variables

<!-- facts:locals -->

## State Changes

| Target | When | Meaning |
| --- | --- | --- |
| `db_mx%ch_sed` | When the sediment file exists and is scanned successfully, `db_mx%ch_sed` is set to the counted number of channel sediment records before allocation and record loading. | `db_mx%ch_sed` becomes the shared record count for the channel sediment database, letting later code know how many `ch_sed` entries were read from `sediment.cha`. |
| `ch_sed(ich)%eqn` | For each loaded record, if `ch_sed(ich)%eqn <= 0`, the routine forces the routing method to 0 and applies the default cover-factor bounds for the SWAT sediment routing method. | `ch_sed(ich)%eqn` records which sediment routing equation a channel uses, and this routine normalizes missing values to the default SWAT method before later routing calculations. |
| `ch_sed(ich)%bnk_kd` | If `ch_sed(ich)%bnk_kd <= 1.e-6`, the routine replaces it with 0.2 or with `0.2 / sqrt(ch_sed(ich)%tc_bnk)` when critical bank shear stress is available. | `ch_sed(ich)%bnk_kd` becomes a usable bank erodibility coefficient even when the input file left it blank or near zero. |
| `ch_sed(ich)%bed_kd` | If `ch_sed(ich)%bed_kd <= 1.e-6`, the routine replaces it with 0.2 or with `0.2 / sqrt(ch_sed(ich)%tc_bed)` when critical bed shear stress is available. | `ch_sed(ich)%bed_kd` becomes a usable bed erodibility coefficient even when the input file left it blank or near zero. |
| `ch_sed(ich)%erod(mo)` | After summing `ch_sed(ich)%erod(mo)` for months 1 through 12, if the total is below `1.e-6`, the routine assigns every month the value of `ch_sed(ich)%cov1`. | `ch_sed(ich)%erod(mo)` provides monthly erosion fractions for the channel; when none were supplied, the routine fills the array with the channel cover factor so later erosion logic has a nonzero schedule. |

## File I/O

<!-- facts:io -->


## Lineage

The procedure was introduced in commit `df07e3f` as part of the initial `ch_read_sed.f90` addition. Commit `39fabde` initialized the local variables `eof`, `imax`, `titldum`, `header`, `sumerod`, `ich`, and `mo` with explicit starting values. Commit `f1e61a3` changed indentation and fixed tab-related formatting in the default-handling blocks, without altering the algorithm. Commit `889136d` only corrected a documentation typo in the header comment.

- df07e3f added the routine and its full file-scanning, allocation, record-loading, and default-filling behavior.
- 39fabde changed runtime initialization by assigning explicit default values to the local control variables before they are used.
- f1e61a3 adjusted formatting in the conditional blocks that set default sediment parameters, but did not change the logic.
- 889136d made a comment-only spelling correction and did not affect execution.

## Review Notes

- Direct file I/O exists; verify file meanings and units before finalizing.
- warning: missing_doc: Procedure 'ch_read_sed' has no extracted documentation comment.
