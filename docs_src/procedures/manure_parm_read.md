---
kind: procedure
symbol: manure_parm_read
title: manure_parm_read
status: filled
source_hash: ca609a6302f416d4
version_label: SWAT+ 62.0.0
locals:
  it: '`it` is the loop counter used when reading individual manure records into `manure_db(it)`
    after the array has been allocated.'
  titldum: '`titldum` holds the first title line from `manure.frt` during the file scan and
    again after rewinding, so the routine can skip over the file''s title/header text before
    reading data records.'
  header: '`header` stores the second header line from `manure.frt`, which is also skipped
    before the data records are counted or loaded.'
  eof: '`eof` captures the `iostat` status from each `read`; a negative value ends the scan
    or load loop at end-of-file, while zero means the file can still be read.'
  imax: '`imax` counts how many manure data records are present in `manure.frt`, and that
    count is used to allocate `manure_db(0:imax)` and later copied to `db_mx%manureparm`.'
  mfrt: '`mfrt` is initialized but not used in the visible source span; its role is unclear
    from this routine alone.'
  i_exist: '`i_exist` receives the `inquire` result and controls whether the routine tries
    to open `manure.frt` or falls back to allocating a one-element placeholder array.'
uses:
  input_file_module: '`input_file_module` is imported by the routine, but no specific symbol
    from it is referenced in the visible source span. It matters only as a shared input-file
    context module; the exact dependency is uncertain from this snippet.'
  maximum_data_module: '`maximum_data_module` provides `db_mx`, the shared maximum-data structure
    that stores the number of manure parameter records found in `manure.frt`. This count is
    needed by other code to know how many manure definitions were loaded.'
  fertilizer_data_module: '`fertilizer_data_module` provides the allocatable `manure_db` array
    that this routine sizes and fills with manure parameter records from `manure.frt`.'
---

<!-- facts:header -->

Reads the manure parameter database from `manure.frt` into the `manure_db` array. It counts the records first so the array can be sized, then loads each manure definition and records the total in `db_mx%manureparm`.

## Bottom Line

This routine is the manure-parameter file loader. It checks whether `manure.frt` exists, sizes `manure_db` to match the number of manure records in that file, and then reads each record into the fertilizer database module.

Its result matters because later model code uses the populated `manure_db` entries and the stored record count in `db_mx%manureparm` to know how many manure parameter definitions are available.

## Arguments

<!-- facts:arguments -->

## Where It Fits

This routine runs during input initialization, after the manure parameter file name has been chosen and before manure application or fertilizer-related processing needs the database. It prepares `manure_db` and `db_mx%manureparm` so later model logic can index manure parameter records safely.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. Initialize counters and status flags | The routine sets `it`, `titldum`, `header`, `eof`, `imax`, and `mfrt` to safe starting values before any file access begins. |
| 2. Check whether the manure file exists | It uses `inquire` to test for `manure.frt`; if the file is missing or effectively disabled, it allocates a minimal `manure_db(0:0)` placeholder. |
| 3. Open the manure file and begin a record-count pass | If the file is available, the routine opens unit 107 on `manure.frt` and skips the first two non-data lines by reading `titldum` and `header`. |
| 4. Count manure data records | It repeatedly reads lines until end-of-file, incrementing `imax` once for each readable manure record encountered in the first pass. |
| 5. Allocate the manure database array | After the count is known, the routine allocates `manure_db(0:imax)` so there is storage for every manure record plus the lower bound element. |
| 6. Rewind the file for the load pass | The file is rewound so the same manure data can be reread from the beginning for actual population of the array. |
| 7. Skip the title and header again | It rereads the title and header lines after the rewind, using the same skip pattern before loading records. |
| 8. Load manure records into shared state | The routine loops from `it = 1` to `imax` and reads each manure record directly into `manure_db(it)`, stopping early if an input error or end-of-file occurs. |
| 9. Publish the record count and close the file | It stores the final manure count in `db_mx%manureparm`, closes unit 107, and returns to the caller. |

## Modules Used

<!-- facts:uses -->

| Module | State touched | Key components |
| --- | --- | --- |
| [sym:input_file_module] | `input_file_module` | `[]` |
| [sym:maximum_data_module] | `db_mx` | `db_mx%manureparm` |
| [sym:fertilizer_data_module] | `manure_db` |  |

## Local Variables

<!-- facts:locals -->

## State Changes

| Target | When | Meaning |
| --- | --- | --- |
| `db_mx%manureparm` | After the file scan completes, `db_mx%manureparm` is assigned the final value of `imax`. | This updates the shared manure-parameter record count so other routines know how many manure definitions were loaded from `manure.frt`. |

## File I/O

<!-- facts:io -->


## Lineage

Two source-backed revisions were resolved for `manure_parm_read`: the routine was introduced in 16e54aa, and 39fabde changed only the local variable initializations so the counters and strings start from explicit default values.

- 16e54aa added the new `manure_parm_read` subroutine to read `manure.frt`, count manure records, allocate `manure_db`, load each record, and store the count in `db_mx%manureparm`.
- 39fabde updated the local declarations to initialize `it`, `titldum`, `header`, `eof`, `imax`, and `mfrt` at declaration time; the file-reading logic and shared state updates remained unchanged.

## Review Notes

- Direct file I/O exists; verify file meanings and units before finalizing.
- warning: missing_doc: Procedure 'manure_parm_read' has no extracted documentation comment.
- input_file_module is imported but no specific symbol from it is referenced in the visible source span; its role is uncertain from this snippet.
- mfrt is initialized but not used in the visible source span.
