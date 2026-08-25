---
kind: procedure
symbol: ch_read_hyd
title: ch_read_hyd
status: filled
source_hash: 4d5b0aca8193466e
version_label: SWAT+ 62.0.0
locals:
  titldum: Temporary string used to read and discard title or record label lines from the
    hydrology file, and to probe each data line before backspacing and rereading it as a structured
    `ch_hyd(ich)` record.
  header: Temporary string used to read and discard the file header line during both the counting
    pass and the data-loading pass.
  eof: I/O status flag from `read(..., iostat=eof)`; it signals end-of-file or read failure
    and controls loop exit.
  i_exist: Logical flag set by `inquire` to tell whether `in_cha%hyd` exists on disk before
    attempting to open it.
  imax: Counter for the number of hydrology data records found in the file; it becomes the
    allocation upper bound and is copied to `db_mx%ch_hyd`.
  ich: Loop counter for loading each hydrology record into `ch_hyd(ich)`.
uses:
  basin_module: '`basin_module` is part of the routine’s shared model state dependency set,
    so it may supply basin-level context or globals expected by the channel-processing workflow
    even though no specific symbol from it was extracted here.'
  input_file_module: '`input_file_module` provides `in_cha%hyd`, the configured file path
    this routine checks, opens, and reads; without that shared filename the routine cannot
    locate `hydrology.cha`.'
  maximum_data_module: '`maximum_data_module` provides `db_mx%ch_hyd`, the shared maximum/record-count
    slot this routine fills after scanning the file so downstream code knows how many channel
    hydrology entries were loaded.'
  channel_data_module: '`channel_data_module` provides the allocatable `ch_hyd` array and
    its `channel_hyd_data` fields; this is the shared storage that receives each parsed hydrology
    record and the parameter adjustments applied afterward.'
---

<!-- facts:header -->

Reads the channel hydrology parameter file, counts its records, allocates channel hydrology storage, and loads each record into `ch_hyd` with basic value bounds applied.

## Bottom Line

`ch_read_hyd` is a file-reader for the channel hydrology input named by `in_cha%hyd` (normally `hydrology.cha`). It first checks that the file exists and is not set to the literal `'null'`; if not, it still allocates a one-element placeholder array so later code has a defined `ch_hyd` container.

When the file is present, the routine scans past the title and header lines to count data records, stores that count in `db_mx%ch_hyd`, allocates `ch_hyd(0:imax)`, then rewinds and reads each record into `ch_hyd(ich)`. After reading, it transforms and clamps several hydraulic parameters so later channel calculations use valid values.

## Arguments

<!-- facts:arguments -->

## Where It Fits

This routine runs during channel-setup processing in `proc_cha`, after initialization routines such as `ch_read_init`, `ch_read_init_cs`, and `sd_hydsed_read` have prepared shared channel state. Its results feed later channel readers and channel process calculations that rely on `db_mx%ch_hyd` and the populated `ch_hyd` array.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. Initialize counters and verify the file exists | Reset `eof` and `imax`, then use `inquire(file=in_cha%hyd, exist=i_exist)` to see whether the configured hydrology file is present. If it is missing or the filename is the sentinel value `'null'`, allocate a minimal `ch_hyd(0:0)` placeholder and skip the file-reading branch. |
| 2. Scan the file to count hydrology records | Open unit 105 on `in_cha%hyd`, read and discard the title and header lines, then loop while reads succeed to count each data record by incrementing `imax`. This first pass determines how many channel hydrology entries the file contains. |
| 3. Store the record count and allocate storage | Copy the scanned record count into `db_mx%ch_hyd` and allocate `ch_hyd(0:imax)` so the shared channel hydrology array is sized for all loaded records plus the zero element used by the module convention. |
| 4. Rewind and skip file prologue again | Rewind unit 105 to the start of `hydrology.cha`, then reread the title and header lines so loading can begin from the first data record. |
| 5. Load each hydrology record into the array | Loop from `ich = 1` to `db_mx%ch_hyd`, read a record probe, backspace one line, and reread the line directly into `ch_hyd(ich)`. The probe/backspace sequence ensures each structured array element receives the full record text. |
| 6. Normalize hydraulic parameters after reading | Transform and bound the loaded values so downstream channel calculations see valid ranges: exponentiate `alpha_bnk` with a negative sign, raise `s`, `n`, `l`, `wdr`, and `side` to minimum thresholds, and cap `n` at 0.70. |
| 7. Close the input file and return | Close unit 105 after the last record is processed, exit the enclosing `do` block, and return to the caller with `db_mx%ch_hyd` and `ch_hyd` populated. |

## Modules Used

<!-- facts:uses -->

| Module | State touched | Key components |
| --- | --- | --- |
| [sym:basin_module] | `basin_module state imported by the routine, but no specific candidate outside references were resolved to it in the provided evidence.` | `None resolved in the context packet.` |
| [sym:input_file_module] | `in_cha` | `in_cha%hyd` |
| [sym:maximum_data_module] | `db_mx` | `db_mx%ch_hyd` |
| [sym:channel_data_module] | `ch_hyd` | `ch_hyd(ich)%alpha_bnk, ch_hyd(ich)%s, ch_hyd(ich)%n, ch_hyd(ich)%l, ch_hyd(ich)%wdr, ch_hyd(ich)%side` |

## Local Variables

<!-- facts:locals -->

## State Changes

| Target | When | Meaning |
| --- | --- | --- |
| `db_mx%ch_hyd` | After scanning `hydrology.cha` and before allocating the array | Stores the number of hydrology data records found in the file so later routines know how many channel hydrology entries were loaded. |
| `ch_hyd(ich)%alpha_bnk` | After each record is read and before the loop advances | Replaces the raw file value with `Exp(-ch_hyd(ich)%alpha_bnk)` so the stored bank-storage recession parameter is in the form used by later channel calculations. |

## File I/O

<!-- facts:io -->


## Lineage

Two source-backed commits were resolved. The initial addition commit `df07e3f` introduced `ch_read_hyd` with its file scan, allocation, record-loading loop, and hydraulic-value adjustments. Later commit `39fabde` did not change the algorithm; it only initialized local variables `titldum`, `header`, `eof`, `imax`, and `ich` at declaration time.

- `df07e3f` added the entire routine, including file existence checks, the two-pass record count/load pattern, allocation of `ch_hyd`, and post-read parameter bounding.
- `39fabde` changed only local-variable initialization style for `titldum`, `header`, `eof`, `imax`, and `ich`; it did not alter file I/O flow or loaded-state behavior.

## Review Notes

- Direct file I/O exists; verify file meanings and units before finalizing.
- warning: missing_doc: Procedure 'ch_read_hyd' has no extracted documentation comment.
