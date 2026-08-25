---
kind: procedure
symbol: ls_read_lsparms_cal
title: ls_read_lsparms_cal
status: filled
source_hash: 0a210010413e66a6
version_label: SWAT+ 62.0.0
locals:
  titldum: Temporary string used to read and discard the file title line from `wb_parms.sft`
    before the routine reaches the record that contains the parameter count.
  header: Temporary string used to read the file header line from `wb_parms.sft` after the
    count is read; the value is not used later in this routine.
  eof: I/O status flag for the reads from unit 107. It starts at 0 and is checked for negative
    end-of-file or read failure after each record read.
  i_exist: Logical flag set by `inquire` to tell the routine whether `in_chg%wb_parms_sft`
    exists on disk.
  mlsp: Holds the number of landscape calibration parameters declared in the input file, and
    is later used to size `ls_prms` and set `db_mx%lscal_prms`.
  i: Loop counter used to read each parameter record into `ls_prms(i)`.
uses:
  maximum_data_module: This shared maximum-data counter records how many landscape calibration
    parameters were found, so later calibration setup can allocate and bound arrays from the
    parsed file size rather than re-reading the file.
  calibration_data_module: These allocatable calibration records are the destination for the
    parsed file contents; the routine fills each element's name, change type, limits, and
    parameter bounds for later calibration logic.
  input_file_module: This module supplies the configured filename `wb_parms.sft`; without
    it the routine would not know which soft calibration file to open and read.
---

<!-- facts:header -->

Reads the landscape calibration parameter definitions from the configured soft-change file and stores the count in shared calibration metadata. It also allocates the `ls_prms` array and loads each parameter's name, change type, bounds, and limits.

## Bottom Line

This routine opens the landscape calibration soft-input file named by `in_chg%wb_parms_sft`, checks that it exists and is not set to "null", then reads the file header and the declared number of calibration parameters. It allocates `ls_prms` to that size, copies the count into `db_mx%lscal_prms`, and reads each parameter record into the shared calibration array.

The result is the in-memory list of landscape calibration parameters that later calibration setup code uses to allocate and apply soft calibration changes. If the file is missing or disabled, the routine still allocates a one-element placeholder array so downstream code has a defined `ls_prms` target.

## Arguments

<!-- facts:arguments -->

## Where It Fits

This routine runs during calibration preprocessing in `proc_cal`, after the earlier soft-calibration code setup and before later element readers and calibration allocation steps. Its output sizes and populates the shared landscape calibration parameter table that downstream calibration routines depend on.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. Initialize read state and check whether the configured file exists | The routine starts with empty title and header buffers, zeroes the I/O status, and uses `inquire` on `in_chg%wb_parms_sft` to see whether the soft calibration file is available. If the file is missing or the configured name is "null", it skips file parsing and allocates a placeholder `ls_prms(0:0)` array. |
| 2. Open the soft calibration file and read its leading records | When the file is available, the routine opens unit 107 on `in_chg%wb_parms_sft`, reads and discards the title line, reads the declared parameter count into `mlsp`, reads the header line, and allocates `ls_prms(mlsp)`. The loop exits after the first successful pass through these setup records. |
| 3. Publish the parameter count to shared calibration metadata | The routine copies the parsed parameter count into `db_mx%lscal_prms` so the shared maximum-data state reflects how many landscape calibration parameters were loaded. |
| 4. Load each landscape calibration parameter record | A loop runs from 1 to `mlsp`, reading each record from unit 107 into `ls_prms(i)%name`, `%chg_typ`, `%neg`, `%pos`, `%lo`, and `%up`. These are the per-parameter soft calibration settings used later in calibration processing. |
| 5. Close the file and return to the caller | After the data records are read, the routine closes unit 107, returns to `proc_cal`, and leaves the loaded calibration array and count in shared module state. |

## Modules Used

<!-- facts:uses -->

| Module | State touched | Key components |
| --- | --- | --- |
| [sym:maximum_data_module] | `db_mx` | `db_mx%lscal_prms` |
| [sym:calibration_data_module] | `ls_prms` | `ls_prms(i)%name, ls_prms(i)%chg_typ, ls_prms(i)%neg, ls_prms(i)%pos, ls_prms(i)%lo, ls_prms(i)%up` |
| [sym:input_file_module] | `in_chg` | `in_chg%wb_parms_sft` |

## Local Variables

<!-- facts:locals -->

## State Changes

| Target | When | Meaning |
| --- | --- | --- |
| `db_mx%lscal_prms` | When `in_chg%wb_parms_sft` exists and is not "null" and the file header supplies a parameter count. | `db_mx%lscal_prms` is updated to the number of landscape calibration parameters read from `wb_parms.sft`, allowing later calibration setup to know the table size. |

## File I/O

<!-- facts:io -->


## Lineage

Resolved lineage shows the procedure was added in `df07e3f` as part of the initial source import. `94b6dec` preserved the same logic while bringing in the latest source version, and `39fabde` initialized local variables (`titldum`, `header`, `eof`, `mlsp`, `i`) and simplified the placeholder allocation formatting. `f1e61a3` made only whitespace cleanup at the end-of-block `end if` line.

- df07e3f introduced the procedure with file existence checking, header/count reads, allocation of `ls_prms`, population of `db_mx%lscal_prms`, and record-by-record loading from `wb_parms.sft`.
- 39fabde changed local declarations to initialize `titldum`, `header`, `eof`, `mlsp`, and `i` at declaration time, but did not change the file-reading algorithm.
- f1e61a3 only adjusted whitespace on the closing `end if` line and did not change behavior.

## Review Notes

- Direct file I/O exists; verify file meanings and units before finalizing.
- warning: missing_doc: Procedure 'ls_read_lsparms_cal' has no extracted documentation comment.
