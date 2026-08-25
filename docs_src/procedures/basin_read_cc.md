---
kind: procedure
symbol: basin_read_cc
title: basin_read_cc
status: filled
source_hash: 77b4e4d8d1148070
version_label: SWAT+ 62.0.0
locals:
  titldum: Temporary character buffer used to read and discard title records from `codes.bsn`
    and `pet.cli`; it is not retained as model state.
  header: Temporary character buffer used to read and discard the header line(s) from the
    input files before the structured basin control record is read.
  eof: I/O status flag for each `read`; it is initialized to 0 and used to detect end-of-file
    or read failure while scanning the input records.
  i_exist: Logical flag set by `inquire` to tell whether the configured basin control file
    exists before the routine tries to open it.
uses:
  input_file_module: This module provides `in_basin%codes_bas`, the configured filename for
    the basin control file. `basin_read_cc` uses that path to decide which file to open and
    read.
  basin_module: This module owns `bsn_cc`, the basin control-code structure that receives
    the parsed values from `codes.bsn`. The routine also tests `bsn_cc%pet` to decide whether
    it must open and scan `pet.cli`.
---

<!-- facts:header -->

Reads basin control codes from codes.bsn and, if basin PET is set to method 3, reads the PET climate file header records needed for later PET processing.

## Bottom Line

basin_read_cc is a setup routine that loads basin control settings from `codes.bsn` into `bsn_cc`. It also checks `bsn_cc%pet`, and when that control code equals 3 it opens `pet.cli` and reads its title and header records to advance through the file structure used by PET inputs.

The routine matters because it establishes basin-level control state before later basin initialization steps run. `proc_bsn` calls it before `basin_read_objs`, `time_read`, and `basin_read_prm`, so downstream behavior can depend on the control code values it populates.

## Arguments

<!-- facts:arguments -->

## Where It Fits

This routine runs during basin setup, immediately after output files are opened in `proc_bsn` and before other basin readers such as `basin_read_objs`, `time_read`, and `basin_read_prm`. Its results matter later because the parsed `bsn_cc` control codes determine basin configuration, including whether PET-related input handling must be performed.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. Initialize read status and file-presence check | Set temporary buffers and the EOF status flag, then inquire whether the configured basin control file exists using `in_basin%codes_bas`. |
| 2. Read basin control file records | If the basin control file is present or the filename is not the sentinel value `null`, open unit 107 on `codes.bsn`, read and discard the title and header records, then read the control record into `bsn_cc`. Exit the loop after one successful record scan or on end-of-file. |
| 3. Read PET climate file when required | If `bsn_cc%pet` equals 3, open `pet.cli` on unit 140 and consume its title and header records with additional reads, then exit the loop. |
| 4. Close the basin control file and return | Close unit 107 for `codes.bsn` and return to the caller. |

## Modules Used

<!-- facts:uses -->

| Module | State touched | Key components |
| --- | --- | --- |
| [sym:input_file_module] | `in_basin` | `in_basin%codes_bas` |
| [sym:basin_module] | `bsn_cc` | `bsn_cc%pet` |

## Local Variables

<!-- facts:locals -->

## State Changes

| Target | When | Meaning |
| --- | --- | --- |
| `none extracted` | none extracted | No assignment targets were extracted automatically. |

## File I/O

<!-- facts:io -->


## Lineage

Source-backed lineage commits were resolved. The routine was added in df07e3f with the initial basin control-file and PET-file reading logic. c7c8e22 brought in the same routine from upstream bitbucket sources without changing the behavior shown here. 39fabde initialized `titldum`, `header`, and `eof` to empty-string/zero defaults. 2ee1889 removed a stray blank line before `close(107)`.

- df07e3f introduced `basin_read_cc` with reads from `codes.bsn`, a conditional `pet.cli` read path when `bsn_cc%pet == 3`, and the final `close(107)`.
- 39fabde changed local variable declarations so `titldum` and `header` start as empty strings and `eof` starts at 0, reducing uninitialized-state risk before the reads.
- 2ee1889 made a formatting-only change by deleting a blank line before `close(107)`; no execution logic changed.

## Review Notes

- Direct file I/O exists; verify file meanings and units before finalizing.
- warning: missing_doc: Procedure 'basin_read_cc' has no extracted documentation comment.
