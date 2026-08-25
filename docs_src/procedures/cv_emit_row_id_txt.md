---
kind: procedure
symbol: cv_emit_row_id_txt
title: cv_emit_row_id_txt
status: filled
source_hash: 5cca078045f3db21
version_label: SWAT+ 62.0.0
args:
  unit_no: '`unit_no` is the already-open output unit to write to. It controls which file/stream
    receives the identifier row, and this routine does not open or close that unit.'
  hru_j: '`hru_j` is the HRU index printed into the row. It labels the output record with
    the current hydrologic response unit number.'
  hru_iob: '`hru_iob` is the object index used to fetch `ob(hru_iob)%gis_id` and `ob(hru_iob)%name`.
    It selects which HRU object''s GIS identifier and name are written into the row.'
---

<!-- facts:header -->

Writes a single HRU identifier row to the carbon-variable output stream. It prefixes later data rows with the current date, HRU index, GIS id, and HRU name.

## Bottom Line

This helper subroutine emits the row header fields that identify one HRU in the carbon-variable text output. It writes the current time fields plus the HRU number, GIS id, and HRU name to the unit passed in by the caller.

It matters because the wider `soil_carbvar_write` workflow uses this identifier row before writing each HRU's carbon-variable blocks, so downstream output files can be matched back to a specific HRU and timestep.

## Arguments

<!-- facts:arguments -->

## Where It Fits

This routine runs inside `soil_carbvar_write` while carbon-variable output is being assembled for each HRU. The caller prepares the HRU loop indices and the output unit, then this routine writes the identifying prefix that later carbon data records depend on for row context.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. write row id prefix | Write the current day, month, day-of-month, year, HRU number, GIS id, and HRU name to the supplied output unit. The write uses `advance='no'`, so it leaves the record open for additional fields from later routines. |

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

Resolved lineage shows two substantive history points for this source. The initial addition in f66c8e6 created `soil_carbvar_write.f90` as a soil carbon output routine, and bc7755a later refactored it into a per-family carbon output writer using module-based state and wider output handling. The resolved 2ee1889 commit only cleaned up the subroutine ending syntax and did not change behavior in the shown span.

- f66c8e6 introduced the routine and its basic carbon-output purpose.
- bc7755a refactored the carbon subsystem output structure; for this span, the shown diffs did not alter the identifier-row write itself.
- 2ee1889 only changed the end statement formatting and had no behavioral impact in the shown span.

## Review Notes

- Direct file I/O exists; verify file meanings and units before finalizing.
- warning: missing_doc: Procedure 'cv_emit_row_id_txt' has no extracted documentation comment.
- source uncertainty: the surrounding caller uses carbon output units, but the exact external file name behind `unit_no` is not visible in the extracted span.
