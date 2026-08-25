---
kind: procedure
symbol: manure_orgmin_read
title: manure_orgmin_read
status: filled
source_hash: e6334308dbd42fa1
version_label: SWAT+ 62.0.0
locals:
  it: Loop counter used to index each manure record while reading data into `manure_om(it)`.
  titldum: Temporary string read from the file to consume title or non-data lines during the
    scan and reload passes.
  header: Temporary string used to read the header line after the title line in `manure_om.frt`.
  eof: I/O status flag from each `read`; it signals end-of-file or read failure and controls
    the scan and reload loops.
  imax: Count of manure data records found in `manure_om.frt`; also used as the upper bound
    when allocating `manure_om`.
  mfrt: Declared and reset but not used in the visible source; it appears to be a leftover
    or placeholder counter.
  i_exist: Logical flag from `inquire` that records whether `manure_om.frt` exists before
    attempting to read it.
uses:
  input_file_module: '`input_file_module` provides the `i_exist` logical used by `inquire`
    to test whether `manure_om.frt` is present before any file reading is attempted.'
  maximum_data_module: '`maximum_data_module` provides `db_mx`, the shared database-size record
    that this routine updates so the rest of the model knows how many manure organic matter
    entries were loaded.'
  fertilizer_data_module: '`fertilizer_data_module` owns the allocatable `manure_om` array
    and its component fields, so this routine fills the module-wide manure database that other
    management and application routines consume.'
---

<!-- facts:header -->

Reads the manure organic matter database from `manure_om.frt` into the shared `manure_om` array. It first counts records to size the array, then rewinds and loads each manure type's composition fields for later manure application calculations.

## Bottom Line

`manure_orgmin_read` is a database loader for manure organic matter properties. It checks whether `manure_om.frt` exists, counts the number of manure entries, allocates `manure_om(0:imax)`, and then reads each record into the shared manure attribute array.

The routine also stores the record count in `db_mx%manure_om`, which lets later code know how many manure organic matter types are available. That database is used downstream when manure applications are mapped to soil carbon, nitrogen, and phosphorus pools.

## Arguments

<!-- facts:arguments -->

## Where It Fits

This routine runs during database initialization inside `proc_db`, after fertilizer parameters are loaded and before manure application and other management routines need manure composition data. Its results feed later manure and nutrient handling because they define the shared manure organic matter database and its size.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. Initialize counters and test file presence | Reset `eof`, `imax`, and `mfrt`, then use `inquire` to see whether `manure_om.frt` exists. If the file is missing or the filename is set to `null`, allocate a minimal `manure_om(0:0)` array and skip reading. |
| 2. Open the manure database and read the title/header | Open `manure_om.frt` on unit 107, read the title line into `titldum`, then read the header line into `header` before scanning records. |
| 3. Count the number of manure records | Loop through the file reading placeholder lines into `titldum` until end-of-file, incrementing `imax` for each record encountered so the array can be sized to the number of manure types. |
| 4. Allocate storage for all manure types | Allocate the shared `manure_om` array from index 0 through `imax`, creating space for every manure organic matter entry found in the file. |
| 5. Rewind and reread file headers | Rewind unit 107 and reread the title and header lines so the second pass starts from the beginning of the record list. |
| 6. Load each manure record into shared state | Iterate from `it = 1` to `imax` and read each manure record into the corresponding `manure_om(it)` fields. Stop early if a read error or end-of-file occurs. |
| 7. Publish record count and close file | Store the final record count in `db_mx%manure_om`, close unit 107, and return to the caller. |

## Modules Used

<!-- facts:uses -->

| Module | State touched | Key components |
| --- | --- | --- |
| [sym:input_file_module] | `input_file_module` | `i_exist` |
| [sym:maximum_data_module] | `db_mx` | `db_mx%manure_om` |
| [sym:fertilizer_data_module] | `manure_om` | `manure_om(it)%name, manure_om(it)%frac_water, manure_om(it)%fcbn, manure_om(it)%fminn, manure_om(it)%fminp, manure_om(it)%forgn, manure_om(it)%forgp, manure_om(it)%fnh3n, manure_om(it)%description` |

## Local Variables

<!-- facts:locals -->

## State Changes

| Target | When | Meaning |
| --- | --- | --- |
| `db_mx%manure_om` | After the file has been scanned and `imax` has been determined, even if the file is missing the routine still leaves a valid allocated array and updates the count. | `db_mx%manure_om` records how many manure organic matter entries were found in `manure_om.frt`, giving later initialization and application code the database size to use when referencing `manure_om`. |

## File I/O

<!-- facts:io -->


## Lineage

Introduced in 561bc28 as a new subroutine to read the manure organic matter database. The resolved diff shows the initial implementation already handled file existence checks, record counting, allocation, rewind-and-reread loading, and publishing the count to `db_mx%manure_om`.

- 561bc28 added `manure_orgmin_read` and its full database-loading workflow for `manure_om.frt`, including allocation, file scanning, record loading, and the `db_mx%manure_om` size update.

## Review Notes

- Direct file I/O exists; verify file meanings and units before finalizing.
- warning: missing_doc: Procedure 'manure_orgmin_read' has no extracted documentation comment.
