---
kind: procedure
symbol: water_orcv_read
title: water_orcv_read
status: filled
source_hash: 7c93b924e8e20c0d
version_label: SWAT+ 62.0.0
locals:
  titldum: Temporary string used to read and discard the title line from `outside_rcv.wal`
    before processing the data records.
  header: Temporary string used to read and discard the header line in `outside_rcv.wal` after
    the record count.
  eof: I/O status flag for the `read` statements; negative values indicate end-of-file and
    stop the read loop.
  imax: Holds the number of outside-basin receiving objects declared in `outside_rcv.wal`;
    also used to size the `orcv` allocation and copied to `db_mx%out_rcv`.
  i_exist: Logical existence check for `outside_rcv.wal`, used to decide whether to allocate
    an empty array or read the file.
  i: Counter/readback field for the object index written on each data line in `outside_rcv.wal`.
  ircv: Loop index over the receiving-object records stored in `orcv`.
  iom: Declared counter that is not used in the shown source.
  irec: Declared counter that is not used in the shown source.
uses:
  input_file_module: '`input_file_module` supplies the file-existence input used by the `inquire`
    statement, which controls whether the routine reads `outside_rcv.wal` or falls back to
    an empty allocation.'
  water_allocation_module: '`water_allocation_module` owns the `orcv` array that this routine
    allocates and fills, so it is the storage location for the receiving-object names and
    filenames read from `outside_rcv.wal`.'
  recall_module: '`recall_module` is imported by the procedure, but no resolved symbols from
    it are referenced in the visible source; it likely remains for shared compilation context
    or future use, but it does not affect the shown algorithm directly.'
  mgt_operations_module: '`mgt_operations_module` is imported by the procedure, but no resolved
    symbols from it are referenced in the visible source; it does not change the read/allocate
    logic shown here.'
  maximum_data_module: '`maximum_data_module` provides `db_mx`, and this routine writes `db_mx%out_rcv
    = imax` so the model knows how many outside receiving objects were loaded.'
  hydrograph_module: '`hydrograph_module` is imported, but no resolved symbols from it are
    used in the visible code; it is part of the broader water-routing context, not the file-reading
    loop itself.'
  constituent_mass_module: '`constituent_mass_module` is imported, but no resolved symbols
    from it are used in the visible code; it likely supports later transport calculations
    that depend on the receiving-object setup.'
  sd_channel_module: '`sd_channel_module` is imported, but no resolved symbols from it are
    used in the visible code; it matters because the receiving-object setup feeds downstream
    channel/water-routing behavior.'
---

<!-- facts:header -->

Reads the outside-basin receiving object list from `outside_rcv.wal` and allocates the `orcv` array accordingly. It also stores the file count in `db_mx%out_rcv` for later allocation and reporting.

## Bottom Line

`water_orcv_read` is a file-reader and allocator for outside-basin receiving objects. It checks whether `outside_rcv.wal` exists, opens it, reads the file title, object count, and header, then loads each receiving object name and filename into `orcv`.

The routine matters because later water-allocation logic needs `orcv` populated and `db_mx%out_rcv` set to the number of records found. If the file is missing or disabled, it creates an empty `orcv(0:0)` array instead of loading records.

## Arguments

<!-- facts:arguments -->

## Where It Fits

This routine runs during model startup or input initialization, after the file system has been set up and before water allocation routing uses outside receiving-object definitions. Its results are used later wherever the model needs the `orcv` array and the count in `db_mx%out_rcv`.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. Initialize read-status counters | The routine zeroes the end-of-file flag and maximum-record counter before starting the file scan, ensuring the later reads begin with clean status values. |
| 2. Check whether the input file exists | It tests whether `outside_rcv.wal` exists. If the file is missing or the name is set to `null`, the routine allocates a one-element placeholder array `orcv(0:0)` instead of reading records. |
| 3. Open the receiving-object file | When the file is present, the routine opens unit 107 on `outside_rcv.wal` and reads the first line into `titldum`. |
| 4. Read record count and header | It stops if the title read hit end-of-file, otherwise it reads `imax`, reads `header`, and stores `imax` in `db_mx%out_rcv` so the model knows how many receiving objects were found. |
| 5. Allocate the receiving-object array | The routine allocates `orcv(imax)` using the count read from the file, creating one storage slot for each outside-basin receiving object. |
| 6. Load each receiving-object record | It loops from 1 to `imax`, reading the object index and the `name` and `filename` fields into `orcv(ircv)` until all records are loaded or end-of-file is reached. |
| 7. Close the file and return | After the scan completes, the routine closes unit 107 and returns to the caller. |

## Modules Used

<!-- facts:uses -->

| Module | State touched | Key components |
| --- | --- | --- |
| [sym:input_file_module] | `input_file_module` | `i_exist` |
| [sym:water_allocation_module] | `orcv, wal` | `orcv(ircv)%name, orcv(ircv)%filename` |
| [sym:recall_module] | `recall_module` |  |
| [sym:mgt_operations_module] | `mgt_operations_module` |  |
| [sym:maximum_data_module] | `db_mx` | `db_mx%out_rcv` |
| [sym:hydrograph_module] | `hydrograph_module` |  |
| [sym:constituent_mass_module] | `constituent_mass_module` |  |
| [sym:sd_channel_module] | `sd_channel_module` |  |

## Local Variables

<!-- facts:locals -->

## State Changes

| Target | When | Meaning |
| --- | --- | --- |
| `db_mx%out_rcv` | When `outside_rcv.wal` exists and the file scan reaches the record-count line. | `db_mx%out_rcv` is updated to the number of outside receiving objects declared in the file, so other model code can size and interpret the receiving-object database consistently. |

## File I/O

<!-- facts:io -->


## Lineage

The procedure was introduced in commit 080211e as a new subroutine for reading `outside_rcv.wal` and allocating `orcv`. The resolved lineage evidence shows only that initial addition; no later behavioral changes were resolved for this source span.

- 080211e added `water_orcv_read` with file existence checking, file open/read/close logic, allocation of `orcv`, and assignment of `db_mx%out_rcv` from the file-record count.

## Review Notes

- Direct file I/O exists; verify file meanings and units before finalizing.
- warning: missing_doc: Procedure 'water_orcv_read' has no extracted documentation comment.
- algorithm_steps revised: condensed the draft into seven source-backed steps aligned to the visible file-read, allocate, loop, and close sequence.
- `orcv` is a variable array, not a callee; the caller/callee overlay field was interpreted from the source and ownership tables.
- `input_file_module` is imported but no specific symbol from it is resolved in the provided snippet; `i_exist` is inferred from the `inquire` statement.
