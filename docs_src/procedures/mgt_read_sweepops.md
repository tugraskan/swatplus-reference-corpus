---
kind: procedure
symbol: mgt_read_sweepops
title: mgt_read_sweepops
status: filled
source_hash: 731986bc00652031
version_label: SWAT+ 62.0.0
locals:
  titldum: Temporary text holder for the file title/header lines and the first-field reads
    while counting and loading records from `sweep.ops`.
  header: Temporary text holder for the second header line in `sweep.ops`; it is read and
    discarded during both the counting pass and the data-loading pass.
  eof: I/O status flag returned by list-directed reads; it controls the file-scan loops and
    signals end-of-file or read failure when it becomes nonzero.
  imax: Counter for the number of sweeping-operation data records found in `sweep.ops`; it
    becomes the allocation size and is later stored in `db_mx%sweepop_db`.
  i_exist: Logical flag from `inquire` that tells the routine whether the configured sweep-ops
    file is present before any read attempts are made.
  msweepops: Unused local counter initialized to zero; it appears to be a leftover placeholder
    and does not affect the routine's behavior.
  isweepop: Loop counter used on the second pass to read each sweeping-operation record into
    `sweepop_db(1:imax)`.
uses:
  input_file_module: This module supplies `in_ops%sweep_ops`, the configured path to the street-sweeping
    operations file. The routine must consult it to know which file to check, open, and read.
  maximum_data_module: This module holds `db_mx%sweepop_db`, the shared count of loaded sweeping-operation
    records. The routine updates that size so other parts of the model can know how many sweep-operation
    records are available.
  mgt_operations_module: This module defines the allocatable `sweepop_db` array and the `streetsweep_operation`
    record type. The routine allocates and fills that shared array, so this module is the
    destination for the parsed sweep operations.
---

<!-- facts:header -->

Reads the street-sweeping operations definition file `sweep.ops` and loads its records into the shared `sweepop_db` array. It also records how many sweeping operations were found so later management code can use them.

## Bottom Line

mgt_read_sweepops is the management-file loader for street sweeping operations. It checks whether the configured `sweep.ops` file exists and is enabled, counts the data records, allocates `sweepop_db` to fit, and then reads each operation record into the global operations database.

This matters because `proc_db` calls it during management-data startup, before the model begins using the operation database. The routine also writes the final record count into `db_mx%sweepop_db`, which other code can use as the size of the sweeping-operation set.

## Arguments

<!-- facts:arguments -->

## Where It Fits

This routine runs during database/setup processing, when `proc_db` is reading management and scheduling input files. It depends on `proc_db` having already reached the management-file section, and its output is used later when the model needs the populated street-sweeping operation database and the record count in `db_mx%sweepop_db`.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. Initialize local counters and status flags | The routine starts with blank title/header buffers, zeroes the end-of-file status, resets the record counter, and initializes the file-existence flag and loop index. It also redundantly assigns zero to some locals again after declaration. |
| 2. Check whether the configured sweep-ops file exists | It uses `inquire` on `in_ops%sweep_ops` to test for the file, then handles the disabled/missing case by allocating a minimal `sweepop_db(0:0)` array. |
| 3. Open the sweep-ops file and begin a counting pass | The routine opens unit 107 on `sweep.ops`, reads past the title and header lines, and then loops through the remaining records to count how many sweep-operation entries are present. |
| 4. Allocate the operation database to the counted size | After counting finishes, it allocates `sweepop_db(0:imax)` so the shared operation array can hold every sweeping-operation record plus the zero index element. |
| 5. Rewind the file and skip the headers again | The file is rewound to the beginning and the title/header lines are read again so the second pass starts at the first data record. |
| 6. Load each sweep operation into shared state | The routine loops from 1 to `imax` and reads each record into `sweepop_db(isweepop)`, populating the allocatable operations database. |
| 7. Close the file and publish the record count | It closes unit 107 and stores the final record count in `db_mx%sweepop_db` so other routines can see how many sweeping operations were loaded. |

## Modules Used

<!-- facts:uses -->

| Module | State touched | Key components |
| --- | --- | --- |
| [sym:input_file_module] | `in_ops` | `in_ops%sweep_ops` |
| [sym:maximum_data_module] | `db_mx` | `db_mx%sweepop_db` |
| [sym:mgt_operations_module] | `sweepop_db` |  |

## Local Variables

<!-- facts:locals -->

## State Changes

| Target | When | Meaning |
| --- | --- | --- |
| `db_mx%sweepop_db` | After the file check/counting logic completes, including the missing-file branch or the successful load branch. | `db_mx%sweepop_db` is set to the number of sweeping-operation records found in `sweep.ops` (`imax`). This publishes the array size to shared model state so later code can size loops or validate access to `sweepop_db`. |

## File I/O

<!-- facts:io -->


## Lineage

The procedure was introduced in commit df07e3f as a new routine that reads `sweep.ops`, counts records, allocates `sweepop_db`, and loads each operation. Commit 94b6dec kept the same logic but updated the source from the imported bitbucket version. Commit 39fabde changed only local variable initialization by giving `titldum`, `header`, `eof`, `imax`, `msweepops`, and `isweepop` explicit initial values.

- df07e3f added the full `mgt_read_sweepops` implementation, including file existence checking, counting, allocation, rewind, record loading, and final `db_mx%sweepop_db` assignment.
- 94b6dec imported the same routine structure from the earlier source snapshot without changing the algorithm shown in the diff for this procedure.
- 39fabde initialized local variables at declaration time, replacing uninitialized locals with explicit defaults for the title/header buffers, EOF flag, counter, and loop index.

## Review Notes

- Direct file I/O exists; verify file meanings and units before finalizing.
- warning: missing_doc: Procedure 'mgt_read_sweepops' has no extracted documentation comment.
- algorithm_steps revised: split the original scan/load/finalize description into seven source-backed steps to reflect the actual count-pass, allocation, rewind, and load phases visible in the code.
- msweepops is initialized but not used in the visible routine body; this may be a leftover local.
- The missing-file branch still reaches `close(107)`; that is safe only if the unit was actually opened in the executed branch, so the control flow is worth reviewing.
