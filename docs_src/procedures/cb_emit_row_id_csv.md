---
kind: procedure
symbol: cb_emit_row_id_csv
title: cb_emit_row_id_csv
status: filled
source_hash: b5f0ca6894367b35
version_label: SWAT+ 62.0.0
args:
  unit_no: Selects the output file connection to write the CSV row prefix. The caller passes
    the specific CSV unit that is already open for the target export file.
  hru_j: Identifies which HRU index to label in the CSV row. The value is written directly
    so later rows can be associated with the correct HRU.
  hru_iob: Selects the HRU object whose GIS ID and name are written into the row prefix. It
    controls which object metadata is emitted alongside the HRU index.
---

<!-- facts:header -->

Writes one CSV row prefix for an HRU, including the current time stamp, HRU index, GIS ID, and object name. It is a small helper used by several carbon and soil export routines before they append their own variables.

## Bottom Line

`cb_emit_row_id_csv` is a formatting helper for CSV output. It writes the row-identifying fields common to several soil/carbon export tables: simulation day, month, day-of-month, year, the HRU index, the HRU GIS ID, and the HRU name.

This matters because the caller routines build wider CSV records for different carbon and soil summaries. By putting the shared ID fields in one place, they keep the CSV headers and row structure consistent across `cb_cpool_stat_emit`, `cb_n_p_pool_emit`, `cb_cflux_stat_emit`, `cb_cbn_lyr_emit`, and `cb_soil_snap_emit`.

## Arguments

<!-- facts:arguments -->

## Where It Fits

This routine runs inside CSV-emitting branches of the soil/carbon output writers, after the caller has selected the correct HRU and output unit and before the caller writes depth-dependent data blocks. Its output becomes the fixed prefix for each CSV record, and later model behavior depends on it because downstream analysis expects each row to carry the time stamp and HRU identifiers alongside the exported soil or carbon variables.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. write row prefix | Writes the common CSV prefix for one HRU record: current day, month, day-of-month, year, the HRU index, the HRU GIS ID, and the trimmed HRU name. The `advance='no'` setting leaves the record open so the caller can append more comma-separated fields. |

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

A resolved lineage commit, `bc7755a`, changed this source file broadly for carbon IO, but the diff shown here does not modify `cb_emit_row_id_csv` itself. No other resolved commit in the provided lineage evidence shows a change to this routine.

## Review Notes

- Direct file I/O exists; verify file meanings and units before finalizing.
- warning: missing_doc: Procedure 'cb_emit_row_id_csv' has no extracted documentation comment.
