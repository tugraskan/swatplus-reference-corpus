---
kind: procedure
symbol: ch_read_parms_cal
title: ch_read_parms_cal
status: filled
source_hash: 7fb7e89098a29b96
version_label: SWAT+ 62.0.0
locals:
  titldum: Temporary title string read from the first record of `ch_sed_parms.sft`; it is
    consumed only to skip the file's title/header text before reading the record count.
  header: Temporary header string read from the file after `mchp`; it skips the column-label
    line before the parameter rows are loaded.
  eof: I/O status flag for the sequential reads on unit 107. It is checked for end-of-file
    while probing the file structure and again while reading parameter records.
  i_exist: Logical result of the `inquire` test on `in_chg%ch_sed_parms_sft`; it controls
    whether the routine tries to read the calibration file or falls back to a placeholder
    allocation.
  mchp: Holds the number of channel parameter records expected in the file. The routine reads
    it from the file and uses it to allocate `ch_prms(mchp)` and to bound the load loop.
  i: Loop counter for stepping through `ch_prms(1:mchp)` while reading each calibration record
    from the open file.
uses:
  calibration_data_module: This shared module owns `ch_prms`, the allocatable array that receives
    the channel calibration parameter records. The routine fills each element's `name`, `chg_typ`,
    `neg`, `pos`, `lo`, and `up` fields from the file, so the module is the persistent storage
    for the data this reader loads.
  input_file_module: This module provides `in_chg%ch_sed_parms_sft`, the configured filename
    for the channel sediment parameter calibration input. The routine must use that path to
    decide whether a file exists and to open the correct `.sft` file for reading.
---

<!-- facts:header -->

Reads channel sediment calibration parameters from the configured `.sft` file into `ch_prms`.

## Bottom Line

This subroutine checks the channel-sediment parameter calibration file named by `in_chg%ch_sed_parms_sft`, opens it if present, and reads a title line, a count of parameter records, a header line, and then the parameter records themselves into the shared `ch_prms` array.

If the file is missing or the filename is set to `"null"`, it allocates a 1-element placeholder array `ch_prms(0:0)` instead of loading parameter data. The results matter because later calibration setup uses `ch_prms` as the channel parameter list.

## Arguments

<!-- facts:arguments -->

## Where It Fits

This routine runs during calibration-setup processing inside `proc_cal`, after other calibration element readers and after `ch_read_orders_cal`. It prepares the shared channel calibration parameter table that later calibration logic uses when hard or soft calibration is initialized.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. Initialize local status variables and probe the configured file name. | The routine starts with empty title/header strings, zeroed counters/status, and then uses `inquire` on `in_chg%ch_sed_parms_sft` to determine whether the configured calibration file exists. |
| 2. Fall back to an empty placeholder array when the file is unavailable. | If the file does not exist or the configured name is `"null"`, the routine allocates `ch_prms(0:0)` so downstream code still sees an allocated array. |
| 3. Open the calibration file and read its header records. | The routine opens unit 107 on the configured `.sft` file, reads and discards the title line, reads the parameter count into `mchp`, reads and discards the header line, and then allocates `ch_prms(mchp)`. |
| 4. Read each channel calibration parameter row into shared storage. | Using `i` as the loop index, the routine reads each record's name, change type, bounds, and limit values into the matching `ch_prms(i)` element until the declared count is reached or end-of-file is encountered. |
| 5. Close the file and return. | After the read phase, the routine closes unit 107 and returns to its caller with `ch_prms` allocated and populated as available. |

## Modules Used

<!-- facts:uses -->

| Module | State touched | Key components |
| --- | --- | --- |
| [sym:calibration_data_module] | `ch_prms` | `ch_prms(i)%name, ch_prms(i)%chg_typ, ch_prms(i)%neg, ch_prms(i)%pos, ch_prms(i)%lo, ch_prms(i)%up` |
| [sym:input_file_module] | `in_chg` | `in_chg%ch_sed_parms_sft` |

## Local Variables

<!-- facts:locals -->

## State Changes

| Target | When | Meaning |
| --- | --- | --- |
| `none extracted` | none extracted | No assignment targets were extracted automatically. |

## File I/O

<!-- facts:io -->


## Lineage

Resolved lineage shows the procedure was added in commit df07e3f, and later commit 39fabde changed local variable initializations by assigning default values to `titldum`, `header`, `eof`, `mchp`, and `i` while leaving the file-reading logic unchanged.

- df07e3f introduced `ch_read_parms_cal` with its file-probing, allocation, record-reading, and close logic.
- 39fabde initialized the local scalars/strings (`titldum`, `header`, `eof`, `mchp`, `i`) to default values before use, but did not alter the file layout or read sequence.

## Review Notes

- Direct file I/O exists; verify file meanings and units before finalizing.
- warning: missing_doc: Procedure 'ch_read_parms_cal' has no extracted documentation comment.
