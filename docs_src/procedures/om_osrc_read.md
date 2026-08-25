---
kind: procedure
symbol: om_osrc_read
title: om_osrc_read
status: filled
source_hash: 94da1ad9646004d2
version_label: SWAT+ 62.0.0
locals:
  titldum: Temporary title string read from the first line of `om_osrc.wal`; it is used only
    to consume the file's heading record before the numeric size line is read.
  header: Temporary header string read after `imax`; it consumes the next header record in
    `om_osrc.wal` before the data records begin.
  eof: I/O status flag for the file reads. It is checked for end-of-file or read failure so
    the routine can stop scanning the file safely.
  imax: Holds the number of outside-source records found in `om_osrc.wal`. The routine uses
    it to size `osrc_om` and `om_osrc_name`, and to store the count in `db_mx%om_treat`.
  i_exist: Logical flag set by `inquire` to tell whether `om_osrc.wal` exists. It controls
    whether the routine allocates empty arrays or reads the file contents.
  iom_osrc: Loop index used to step through the `imax` data records and store each outside-source
    name/object pair into the shared arrays.
uses:
  input_file_module: This module is imported by the routine, but no specific symbols from
    it are referenced in the extracted source. It still matters because it may provide file/path
    configuration or shared input-state conventions used by the model's input handling around
    `om_osrc.wal`.
  water_allocation_module: The routine reads `om_osrc_name` records and stores them alongside
    `wal`-related allocation information, so `water_allocation_module` provides the shared
    name array and water-allocation state that the file populates.
  mgt_operations_module: This module is imported by the routine, but no specific symbol from
    it is referenced in the extracted lines. It matters because the outside-source records
    are part of management-operation data flow, so the module is part of the shared management
    state context around this reader.
  maximum_data_module: '`db_mx%om_treat` is updated with the number of records read from `om_osrc.wal`,
    so `maximum_data_module` matters because it owns the maximum-count database state that
    tells later code how many outside-source treatment entries were found.'
  hydrograph_module: '`osrc_om` is allocated and filled from `om_osrc.wal`, so `hydrograph_module`
    matters because it defines the shared outside-source output objects that this reader loads
    for later routing or output processing.'
  constituent_mass_module: This module is imported by the routine, but no specific symbol
    from it is referenced in the extracted source. It still matters because outside-source
    allocations can feed mass accounting elsewhere in the model, so the constituent-mass state
    context is relevant to this input reader.
---

<!-- facts:header -->

Reads the `om_osrc.wal` water-allocation input file and loads outside-source treatment names and hydrograph objects into shared model storage. It also records how many treatment entries were found.

## Bottom Line

`om_osrc_read` is a small file-reader for the outside-source water allocation setup. It checks whether `om_osrc.wal` exists, then reads the file header and the number of entries, allocates `om_osrc_name` and `osrc_om`, and fills them record by record.

The routine matters because it populates shared allocation/output state used elsewhere in the model and sets `db_mx%om_treat` to the number of outside-source treatment entries discovered in the file.

## Arguments

<!-- facts:arguments -->

## Where It Fits

This routine runs during input initialization for water-allocation outside-source data, after the model knows it may need `om_osrc.wal` and before later routines use the loaded names and `osrc_om` objects. Its results feed later allocation, routing, and mass-accounting behavior that depends on the number of outside-source treatment entries and their definitions.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. Check whether the input file is available | The routine calls `inquire` on `om_osrc.wal` to set `i_exist`, then tests whether the file is missing or explicitly named as "null". This determines whether the routine will allocate empty placeholder arrays or proceed to read real data. |
| 2. Allocate empty arrays when no file is present | If the file is unavailable, the routine allocates `osrc_om(0:0)` and `om_osrc_name(0:0)` so downstream code has defined arrays even though no outside-source entries were loaded. |
| 3. Open the file for sequential reading | When the file exists, the routine enters a loop, opens unit 107 on `om_osrc.wal`, and reads the first title record into `titldum`. The I/O status is checked so the routine can stop if the file ends unexpectedly. |
| 4. Read the record count and header | The routine reads `imax` from the next record, then reads a header string, and stores `imax` in `db_mx%om_treat`. That count becomes the basis for allocation and for later model bookkeeping. |
| 5. Allocate storage for the discovered number of entries | Using `imax`, the routine allocates `osrc_om(imax)` and `om_osrc_name(imax)` so each outside-source record has a matching name and output-object slot. |
| 6. Read each outside-source record into the arrays | A loop over `iom_osrc = 1, imax` reads each record from unit 107 and stores the name and corresponding `osrc_om` object into the shared arrays. |
| 7. Stop the scan and close the file | After the loop finishes, the routine leaves the open-file loop, executes `close(107)`, and returns to the caller with the arrays and count set up. |

## Modules Used

<!-- facts:uses -->

| Module | State touched | Key components |
| --- | --- | --- |
| [sym:input_file_module] | `input_file_module` |  |
| [sym:water_allocation_module] | `om_osrc_name, wal` |  |
| [sym:mgt_operations_module] | `mgt_operations_module` |  |
| [sym:maximum_data_module] | `db_mx` | `db_mx%om_treat` |
| [sym:hydrograph_module] | `osrc_om` |  |
| [sym:constituent_mass_module] | `constituent_mass_module` |  |

## Local Variables

<!-- facts:locals -->

## State Changes

| Target | When | Meaning |
| --- | --- | --- |
| `db_mx%om_treat` | When `om_osrc.wal` exists and the file scan reaches the record containing `imax`. | `db_mx%om_treat` is set to the number of outside-source treatment records found in `om_osrc.wal`. This records the file-defined size so later code can know how many treatment entries were loaded. |

## File I/O

<!-- facts:io -->


## Lineage

Two resolved commits affected `om_osrc_read`. Commit 72206bc created the routine and its file-reading logic, including the existence check, sequential reads from `om_osrc.wal`, allocation of `osrc_om` and `om_osrc_name`, and assignment to `db_mx%om_treat`. Commit 0d74307 only removed an unused local variable declaration (`i`) without changing the routine's behavior.

- 72206bc introduced `om_osrc_read` as a new reader for `om_osrc.wal`, including the file-open/read/allocate loop and the `db_mx%om_treat` assignment.
- 0d74307 removed the unused local integer `i` declaration; the routine's runtime behavior stayed the same.

## Review Notes

- Direct file I/O exists; verify file meanings and units before finalizing.
- warning: missing_doc: Procedure 'om_osrc_read' has no extracted documentation comment.
- input_file_module, mgt_operations_module, and constituent_mass_module are imported but no extracted source line references specific symbols from them in this routine; their roles are inferred only at module level.
- The source shows `close(107)` after the conditional block, so unit 107 is closed even when the file was not opened in the missing-file branch.
