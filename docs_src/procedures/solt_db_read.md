---
kind: procedure
symbol: solt_db_read
title: solt_db_read
status: filled
source_hash: 956aa9af84298b01
version_label: SWAT+ 62.0.0
locals:
  titldum: Temporary character buffer used to read and discard the title or first line from
    `nutrients.sol` during the count and load passes.
  header: Temporary character buffer used to read and discard the header line from `nutrients.sol`
    before counting or loading records.
  eof: I/O status flag for the `read` statements; it controls loop exit and detects end-of-file
    or read failure while scanning `nutrients.sol`.
  msolt_db: Temporary counter initialized to zero but not used in the shown routine body;
    it appears to be a leftover or placeholder for a soil-test database count.
  imax: Counts how many soil-test records are present in `nutrients.sol`; that count is then
    used to allocate `solt_db(0:imax)` and to drive the record-loading loop.
  i_exist: Logical flag set by `inquire` to tell whether the configured nutrient file exists,
    so the routine can skip file loading when the file is missing or disabled.
  isolt: Loop index used to read each soil-test database record from the file into `solt_db(isolt)`.
uses:
  input_file_module: This module supplies `in_sol%nut_sol`, the configured path for the nutrient
    soil-test input file. Without that path, the routine would not know which file to open,
    and it also checks for the special disabled value `null`.
  maximum_data_module: This module holds `db_mx%soiltest`, the shared count of loaded soil-test
    records. `solt_db_read` updates it so the rest of the model can know how many soil-test
    entries are available.
  soil_data_module: This module owns the allocatable soil-test database array `solt_db`; the
    routine allocates it, fills each record from file input, and adjusts `solt_db(isolt)%exp_co`
    when needed.
---

<!-- facts:header -->

Reads the soil-test nutrient database from `nutrients.sol` into `solt_db` and records how many entries were loaded. It also normalizes an out-of-range exponential coefficient before the rest of the model uses the table.

## Bottom Line

`solt_db_read` is a file-loading routine for the soil-test database. It checks whether the configured nutrients file exists and is not set to `null`, sizes the `solt_db` array from the file contents, then rereads the file into module state.

The routine matters because later soil and nutrient calculations depend on the loaded `soiltest_db` records and on `db_mx%soiltest`, which stores the number of available soil-test entries.

## Arguments

<!-- facts:arguments -->

## Where It Fits

`proc_read` calls this routine during model initialization after other core databases have been read and before later nutrient, pesticide, and salt readers run. Its results prepare the soil-test lookup table and record count used by later soil and nutrient behavior.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. Initialize counters and flags | Set the temporary strings, end-of-file flag, database count, and record index to known starting values before any file access begins. |
| 2. Check whether the nutrient file should be read | Use `inquire` on `in_sol%nut_sol` to test whether the configured file exists, and if it does not exist or is set to `null`, allocate a minimal `solt_db(0:0)` array and skip file loading. |
| 3. Open and scan the file once to count records | Open unit 107 on `nutrients.sol`, skip the title and header lines, then loop through the remaining readable rows and increment `imax` for each record encountered. |
| 4. Allocate soil-test storage from the count | Allocate `solt_db(0:imax)` so the shared soil-test database has one element for each counted record plus the zero index slot used by the model's array convention. |
| 5. Rewind and skip the file header again | Rewind unit 107 to the start of `nutrients.sol` and reread the title and header lines so the file is positioned at the first data record for the load pass. |
| 6. Load each soil-test record into shared state | Read each `soiltest_db` record into `solt_db(isolt)` for indices 1 through `imax`, and clamp `exp_co` to 0.001 whenever the loaded value exceeds 0.005. |
| 7. Store the final record count and close the file | Copy the counted number of soil-test records into `db_mx%soiltest` and close unit 107 to finish the `nutrients.sol` read. |

## Modules Used

<!-- facts:uses -->

| Module | State touched | Key components |
| --- | --- | --- |
| [sym:input_file_module] | `in_sol` | `in_sol%nut_sol` |
| [sym:maximum_data_module] | `db_mx` | `db_mx%soiltest` |
| [sym:soil_data_module] | `solt_db` | `solt_db(isolt)%exp_co` |

## Local Variables

<!-- facts:locals -->

## State Changes

| Target | When | Meaning |
| --- | --- | --- |
| `db_mx%soiltest` | When the nutrient file exists and is not `null`, the routine counts and loads its data records; otherwise `imax` stays at 0 and a minimal array is allocated. | `db_mx%soiltest` is updated to the number of soil-test records found in `nutrients.sol`, which tells the rest of the model how many entries are available for lookup and interpolation. |

## File I/O

<!-- facts:io -->


## Lineage

Two resolved commits changed `solt_db_read`. The initial add in `df07e3f` introduced the routine, and `39fabde` only initialized the local variables (`titldum`, `header`, `eof`, `msolt_db`, `imax`, and `isolt`) at declaration time; the file-reading logic and final `db_mx%soiltest` assignment stayed the same.

- df07e3f added the full `solt_db_read` subroutine to read `nutrients.sol`, count records, allocate `solt_db`, load each record, adjust `exp_co`, assign `db_mx%soiltest`, and close unit 107.
- 39fabde changed only local-variable initialization in `solt_db_read`, setting default values at declaration for `titldum`, `header`, `eof`, `msolt_db`, `imax`, and `isolt` without altering the read algorithm.

## Review Notes

- Direct file I/O exists; verify file meanings and units before finalizing.
- warning: missing_doc: Procedure 'solt_db_read' has no extracted documentation comment.
- algorithm_steps revised: merged the original allocate/count overlap into separate count and allocate steps, and split the final close/writeback behavior into its own step to match the source order.
- Source suggests `msolt_db` is unused in the visible routine body; its purpose is uncertain from this file alone.
