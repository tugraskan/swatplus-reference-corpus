---
kind: procedure
symbol: ch_read_init
title: ch_read_init
status: filled
source_hash: 7019bac0259363ca
version_label: SWAT+ 62.0.0
locals:
  titldum: Temporary character buffer used to read and discard the file title or record label
    line(s) while counting and then rereading `initial.cha`.
  header: Temporary character buffer used to read the header line from `initial.cha` before
    the routine counts and loads the data records.
  eof: I/O status flag for the `read` statements; it detects end-of-file or read failure so
    the routine can stop scanning or loading records.
  imax: Counter for the number of channel initialization data records found in `initial.cha`;
    this becomes the allocation size and the value stored in `db_mx%ch_init`.
  i_exist: Logical flag set by `inquire` to tell whether `in_cha%init` exists on disk before
    the routine tries to open it.
  ich: Loop counter used when rereading `initial.cha` to load each initialization record into
    `ch_init(ich)`.
uses:
  basin_module: This module supplies the configured path to the channel initialization file.
    `ch_read_init` uses `in_cha%init` to decide what file to inquire about, open, and read.
  input_file_module: This module holds the channel input-file names. `ch_read_init` depends
    on `in_cha%init` being set to the `initial.cha` path before it runs.
  maximum_data_module: This module stores maximum record counts. `ch_read_init` writes the
    number of channel initialization entries into `db_mx%ch_init` so other routines can size
    and iterate over the loaded data.
  channel_data_module: This module provides the allocatable `ch_init` array that receives
    the channel initialization records read from `initial.cha`.
  sd_channel_module: This module provides the allocatable `sd_init` array that is sized alongside
    `ch_init` so SWAT-DEG channel initialization data can be stored in parallel.
---

<!-- facts:header -->

Reads the channel initial-condition file `initial.cha`, counts its data records, and loads channel and SWAT-DEG initialization file pointers into module arrays.

## Bottom Line

`ch_read_init` is the setup routine for channel initial-condition input. It checks whether `in_cha%init` points to a real file, sizes the channel initialization arrays to match the number of records in that file, then reads each record into `ch_init` and prepares the corresponding `sd_init` storage.

This matters because later channel processing relies on `db_mx%ch_init` and the allocated `ch_init` / `sd_init` arrays to know how many channel initialization entries exist and to hold the per-entry file references that downstream channel and SWAT-DEG readers use.

## Arguments

<!-- facts:arguments -->

## Where It Fits

This routine runs early in channel processing, when `proc_cha` is setting up channel-related inputs. `proc_cha` calls `ch_read_init` before later readers such as `ch_read_init_cs`, `sd_hydsed_read`, and `ch_read_hyd`, and those later routines depend on the channel initialization arrays and record count established here.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. Initialize counters and status flags | The routine starts with empty title/header buffers, zeroes the I/O status and record counter, and resets `eof` and `imax` before any file work begins. |
| 2. Check whether the configured file exists | It inquires on `in_cha%init` and also treats the literal name `"null"` as a disabled input case. |
| 3. Allocate empty arrays when no file is available | If the input is missing or disabled, the routine allocates one-element placeholder arrays for `ch_init` and `sd_init` at bounds `0:0` and then returns without reading records. |
| 4. Open the initialization file and scan past the header | When a real file exists, the routine opens unit 105 on `in_cha%init` and reads the title and header lines before starting the data scan. |
| 5. Count the data records | It loops through the remaining lines, reading into `titldum` and incrementing `imax` for each record until end-of-file is reached. |
| 6. Publish the record count | The routine stores the count in `db_mx%ch_init` so the rest of the model knows how many channel initialization entries were found. |
| 7. Allocate channel and SWAT-DEG initialization arrays | It allocates `ch_init(0:imax)` and `sd_init(0:imax)` to hold all discovered initialization entries plus the zero index. |
| 8. Rewind and reread the file from the start | The file is rewound, then the routine rereads the title and header lines so the subsequent loop starts at the first data record. |
| 9. Load each initialization record | A loop reads each record into `ch_init(ich)` up to `db_mx%ch_init`, stopping early if a read error or end-of-file occurs. |
| 10. Close the file and return | After the records are loaded, the routine closes unit 105 and returns to the caller. |

## Modules Used

<!-- facts:uses -->

| Module | State touched | Key components |
| --- | --- | --- |
| [sym:basin_module] | `basin_module` | `in_cha%init` |
| [sym:input_file_module] | `in_cha` | `in_cha%init` |
| [sym:maximum_data_module] | `db_mx` | `db_mx%ch_init` |
| [sym:channel_data_module] | `ch_init` |  |
| [sym:sd_channel_module] | `sd_init` |  |

## Local Variables

<!-- facts:locals -->

## State Changes

| Target | When | Meaning |
| --- | --- | --- |
| `db_mx%ch_init` | When `initial.cha` exists and is not the literal string `"null"`. | `db_mx%ch_init` is updated to the number of channel initialization records counted in the file; this count drives array allocation and later iteration over `ch_init` entries. |

## File I/O

<!-- facts:io -->


## Lineage

The procedure was introduced in commit df07e3f with the initial file-reading implementation. Commit 39fabde initialized the local scalars `titldum`, `header`, `eof`, `imax`, and `ich` to zero or blank values and kept the existing logic intact. Commit 2ee1889 only adjusted the trailing `return` formatting.

- df07e3f added the full `ch_read_init` routine: file existence checking, counting records in `initial.cha`, allocating `ch_init` and `sd_init`, rereading the file, and storing the record count in `db_mx%ch_init`.
- 39fabde changed only local variable initialization for `titldum`, `header`, `eof`, `imax`, and `ich`; it did not alter the routine's file-reading behavior.
- 2ee1889 made a formatting-only change to the `return` statement and did not affect behavior.

## Review Notes

- Direct file I/O exists; verify file meanings and units before finalizing.
- warning: missing_doc: Procedure 'ch_read_init' has no extracted documentation comment.
