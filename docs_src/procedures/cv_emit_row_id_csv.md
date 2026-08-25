---
kind: procedure
symbol: cv_emit_row_id_csv
title: cv_emit_row_id_csv
status: filled
source_hash: 5f6c5158407be942
version_label: SWAT+ 62.0.0
args:
  unit_no: File unit number for the CSV output stream. The routine writes the row prefix to
    this already-open unit and does not open or close it.
  hru_j: HRU index to print in the row identifier field. It is written as part of the CSV
    prefix so each output row can be tied back to the HRU being processed.
  hru_iob: Index into `ob` for the current HRU object. The routine uses it to fetch that HRU's
    GIS ID and name for the CSV row prefix.
---

<!-- facts:header -->

Writes the CSV row prefix for a carbon-variable output record: date fields, HRU number, GIS ID, and HRU name.

## Bottom Line

`cv_emit_row_id_csv` is a small helper that emits the leading identifier columns for one CSV output record. It writes the current model date, the HRU index, and the HRU's GIS identifier and name, with commas inserted between fields and no line advance so later routines can append more columns to the same row.

This matters because the carbon output writer builds wider CSV rows in pieces. `soil_carbvar_write` calls this helper before writing the remaining per-HRU data, so the row starts with a consistent ID header across the carbon output files.

## Arguments

<!-- facts:arguments -->

## Where It Fits

`cv_emit_row_id_csv` runs inside `soil_carbvar_write` while preparing per-HRU carbon output rows. `soil_carbvar_write` supplies the target unit, the HRU number, and the HRU object index, and later write helpers depend on this prefix so the CSV record has its date and identity fields before the numeric carbon data are appended.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. write row prefix | Write the current day, month, day-of-month, year, HRU number, GIS ID, and trimmed HRU name to the supplied unit as comma-separated fields. The write uses `advance='no'`, so it leaves the record open for later CSV columns to be appended. |

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

Resolved lineage shows the routine was introduced in commit f66c8e6 as a new helper in `soil_carbvar_write.f90` for the initial carbon-variable output workflow. Commit bc7755a later refactored the carbon output subsystem but did not change this helper's body in the resolved diff, and commit 2ee1889 only cleaned the subroutine ending statement.

- f66c8e6 added `cv_emit_row_id_csv` as part of the first carbon-variable output implementation, writing the date/HRU/GIS/name prefix for CSV rows.
- bc7755a reworked the surrounding carbon output framework but the resolved diff does not show a behavioral change to this helper.
- 2ee1889 made only a source-form cleanup to the subroutine terminator with no runtime behavior change.

## Review Notes

- Direct file I/O exists; verify file meanings and units before finalizing.
- warning: missing_doc: Procedure 'cv_emit_row_id_csv' has no extracted documentation comment.
