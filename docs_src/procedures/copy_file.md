---
kind: procedure
symbol: copy_file
title: copy_file
status: filled
source_hash: 83f64351d4be9af9
version_label: SWAT+ 62.0.0
args:
  source: Path to the file that will be read and copied from. The routine first checks whether
    this file exists; if it does not, `copy_file` exits immediately without opening anything.
  destination: Path to the file that will be created or replaced with the copied contents.
    The routine writes each line read from `source` into this destination file.
locals:
  eof: Holds the I/O status code from the `read` statement. A nonzero value signals end-of-file
    or another read condition and causes the loop to stop.
  line: Temporary text buffer for one record at a time. Each successful read fills `line`,
    and the trimmed contents are written to the destination.
  i_exist: Logical flag set by `inquire(file=source, exist=i_exist)`. It records whether the
    source file is present so the routine can skip copying when the file is missing.
---

<!-- facts:header -->

Copies a text file from a source path to a destination path, line by line. If the source file does not exist, it returns without doing anything.

## Bottom Line

`copy_file` is a simple file duplication helper used by SWAT+ output code. It checks that the source file exists, opens the source for reading and the destination for writing, then copies every text line until end-of-file and closes both files.

This matters because `swift_output` uses it to stage a set of SWAT input/configuration files into the SWIFT directory before later output routines write additional files there.

## Arguments

<!-- facts:arguments -->

## Where It Fits

This routine runs inside `swift_output`, after that procedure has built the list of files to stage into the SWIFT folder. `swift_output` passes each selected file name as `source` and a matching `SWIFT/` destination path as `destination`; the copied files are then available for the later SWIFT output workflow, including the precipitation file written immediately afterward in the same routine.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. if | Check whether the source file was found; if not, skip the copy entirely. |
| 2. return | Exit immediately when the source file does not exist, leaving the destination untouched. |
| 3. io | Open the existing source file on unit 107 for sequential reading. |
| 4. io | Open or replace the destination file on unit 1007 for sequential writing. |
| 5. loop | Begin a record-by-record copy loop that continues until a read status ends the loop. |
| 6. io | Read one text line from the source file into the buffer and capture read status in `eof`. |
| 7. if | Stop copying when the read status indicates end-of-file or another read condition. |
| 8. io | Write the trimmed line buffer to the destination file. |
| 9. io | Close the source file after all records have been processed. |
| 10. io | Close the destination file to finish and flush the copied output. |

## Modules Used

<!-- facts:uses -->



## Local Variables

<!-- facts:locals -->

## State Changes

| Target | When | Meaning |
| --- | --- | --- |
| `none extracted` | none extracted | No assignment targets were extracted automatically. |

## File I/O

<!-- facts:io -->


## Lineage

The procedure was added in 54a9d44 as a new `copy_file` subroutine that copies a file from source to destination, with a 9000-character line buffer and a 9000-record-length destination open. Commit f146c70 then changed only the internal buffer and destination record length from 9000 to 32000, without changing the copy logic.

- 54a9d44 introduced the new `copy_file` subroutine, including the source-exists check, file open/read/write/close sequence, and the initial 9000-character buffer and record length.
- f146c70 increased the line buffer and destination `recl` from 9000 to 32000 to better accommodate longer files, while leaving the copy algorithm unchanged.

## Review Notes

- Direct file I/O exists; verify file meanings and units before finalizing.
