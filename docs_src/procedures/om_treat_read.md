---
kind: procedure
symbol: om_treat_read
title: om_treat_read
status: filled
source_hash: f187028ace6b56bc
version_label: SWAT+ 62.0.0
locals:
  titldum: Temporary character buffer for the first line of `om_treat.wal`, which serves as
    the file title/header text and is read then discarded.
  header: Temporary character buffer for the second text header line in `om_treat.wal`, read
    to advance past the file header before the data records.
  eof: I/O status flag used by each `read` statement to detect end-of-file or read failure;
    a negative value exits the loop.
  imax: Holds the number of treatment records reported in `om_treat.wal`; it drives array
    allocation and the loop that reads each treatment entry.
  i_exist: Logical flag set by `inquire` to show whether `om_treat.wal` exists before the
    routine tries to open it.
  iom_tr: Loop index for stepping through the treatment records from 1 to `imax` while reading
    names and treatment data.
uses:
  input_file_module: This module matters because the routine uses its file-handling context
    to decide whether `om_treat.wal` can be read or should be bypassed before allocating placeholder
    arrays.
  water_allocation_module: This module matters because `om_treat_read` fills the treatment-name
    array `om_treat_name`, which is the water-allocation-side index for the treatment records
    read from `om_treat.wal`.
  mgt_operations_module: This module matters because treatment files are part of the model's
    management-operation data set, so the routine imports it as part of the shared management
    state used elsewhere in the treatment workflow.
  maximum_data_module: This module matters because `db_mx%om_treat` stores the number of treatment
    records found in `om_treat.wal`, allowing the model to know how many treatment elements
    are present.
  hydrograph_module: This module matters because `wtp_om_treat` receives the per-record treatment
    data read from `om_treat.wal`, so the hydrograph/treatment output structure is the primary
    storage target for the file contents.
  constituent_mass_module: This module matters because treatment plant inputs ultimately affect
    constituent mass accounting elsewhere in the model, so the routine imports the mass module
    as part of the treatment-data dependency set.
---

<!-- facts:header -->

Reads the water allocation treatment file `om_treat.wal` and loads treatment names and output structures into shared model storage. It also records how many treatment entries are present so later routines can size and use the treatment database.

## Bottom Line

`om_treat_read` is a small file-reader for the water allocation treatment input `om_treat.wal`. It checks whether the file exists, then reads a title line, the record count, a header line, and each treatment name paired with its `wtp_om_treat` data before closing the file.

The routine matters because it populates shared state used by the water-allocation/treatment parts of SWAT+, especially `om_treat_name`, `wtp_om_treat`, and `db_mx%om_treat`. If the file is missing or disabled, it allocates minimal placeholder arrays instead of loading treatment records.

## Arguments

<!-- facts:arguments -->

## Where It Fits

This routine runs during model input initialization, after the treatment file path has been decided and before treatment-related simulation state is used. The read values feed later water-allocation and treatment handling through `om_treat_name`, `wtp_om_treat`, and `db_mx%om_treat`.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. Initialize local counters and flags | Set up temporary text buffers, the end-of-file status flag, the treatment count, and the file-existence flag before any file access. |
| 2. Check whether the treatment file exists | Use `inquire` to test for `om_treat.wal`, then branch to a placeholder-allocation path if the file is missing or its name is disabled. |
| 3. Allocate placeholder arrays when the file is unavailable | Create minimal one-element arrays for `wtp_om_treat` and `om_treat_name` so downstream code has allocated storage even without input records. |
| 4. Open the treatment file for reading | Enter the read loop and open `om_treat.wal` on unit 107 so the file contents can be scanned. |
| 5. Read and validate the file headers | Read the title line, the number of treatment records, and the header line; exit early if an end-of-file condition is encountered and store the record count in `db_mx%om_treat`. |
| 6. Allocate storage sized to the reported record count | Allocate `wtp_om_treat(imax)` and `om_treat_name(imax)` so the routine can hold every treatment entry reported in the file. |
| 7. Read each treatment record into shared arrays | Loop from 1 to `imax` and read each treatment name together with its corresponding `wtp_om_treat` record from the file. |
| 8. Repeat until end-of-file, then close the file | Continue the outer read loop until the file ends, then close unit 107 to finish the input operation. |

## Modules Used

<!-- facts:uses -->

| Module | State touched | Key components |
| --- | --- | --- |
| [sym:input_file_module] | `input_file_module` | `i/o existence status and file-control related state used with `inquire`/`open` decisions` |
| [sym:water_allocation_module] | `om_treat_name, wal` |  |
| [sym:mgt_operations_module] | `mgt_operations_module` | `mgt-operation state imported for shared management/treatment model data, though no specific symbol from this module is referenced in the extracted source lines` |
| [sym:maximum_data_module] | `db_mx` | `db_mx%om_treat` |
| [sym:hydrograph_module] | `wtp_om_treat` |  |
| [sym:constituent_mass_module] | `constituent_mass_module` | `constituent-mass state imported for treatment-related mass accounting, though no specific symbol from this module is referenced in the extracted source lines` |

## Local Variables

<!-- facts:locals -->

## State Changes

| Target | When | Meaning |
| --- | --- | --- |
| `db_mx%om_treat` | When `om_treat.wal` exists and the header/count records are successfully read, `db_mx%om_treat` is set to the file's `imax` value. | `db_mx%om_treat` becomes the model-wide count of treatment records available from `om_treat.wal`, which lets later routines know how many treatment entries to expect. |

## File I/O

<!-- facts:io -->


## Lineage

One resolved commit, d70017a, introduced `om_treat_read.f90` as a new subroutine. The diff shows the full file being added with the current file-existence check, header/count reads, allocation of `wtp_om_treat` and `om_treat_name`, the `db_mx%om_treat = imax` assignment, the per-record read loop, and the final `close(107)`.

- d70017a added the complete `om_treat_read` implementation, including the `om_treat.wal` input path, record-count capture in `db_mx%om_treat`, and allocation/read logic for `wtp_om_treat` and `om_treat_name`.

## Review Notes

- Direct file I/O exists; verify file meanings and units before finalizing.
- warning: missing_doc: Procedure 'om_treat_read' has no extracted documentation comment.
- algorithm_steps revised: split the file-read flow into header/count, allocation, record-read, and close steps to match the visible source lines.
- The source imports `mgt_operations_module` and `constituent_mass_module`, but the extracted lines do not reference specific symbols from them; their roles are inferred only as shared treatment-related dependencies.
