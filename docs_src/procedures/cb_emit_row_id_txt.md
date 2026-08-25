---
kind: procedure
symbol: cb_emit_row_id_txt
title: cb_emit_row_id_txt
status: filled
source_hash: e9efb2d4c3fa4f95
version_label: SWAT+ 62.0.0
args:
  unit_no: Logical output unit number to write the row prefix to. The caller chooses which
    open text file receives the identifier line.
  hru_j: HRU index to print in the row prefix. It identifies which HRU the following data
    columns belong to.
  hru_iob: Index into `ob` for the current HRU object. It selects the GIS ID and name that
    are written with the row prefix.
---

<!-- facts:header -->

Writes a standard row identifier prefix for HRU-based carbon and soil output tables. It emits date fields, the HRU index, and the object GIS ID/name so later records can be aligned to the same row.

## Bottom Line

`cb_emit_row_id_txt` is a tiny formatting helper used by several carbon/soil emitters. It writes the common row ID prefix to a text output unit: the current simulation date, the HRU index, and the HRU object's GIS ID and name.

This routine matters because the calling emitters append layer or pool values after the shared identifier block. Keeping the ID prefix in one place makes those output tables consistent across `cb_cbn_lyr_emit`, `cb_cflux_stat_emit`, `cb_n_p_pool_emit`, and `cb_soil_snap_emit`.

## Arguments

<!-- facts:arguments -->

## Where It Fits

This helper runs inside HRU carbon/soil reporting routines after they have selected the correct output unit and confirmed the requested print frequency. The caller prepares `hru_j`, `hru_iob`, and the target unit, and later writes depend on this prefix so each row can be matched to the correct HRU and time stamp.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. Write shared row identifier fields. | Writes the current day, month, day-of-month, year, HRU index, GIS ID, and HRU name to the given output unit using a fixed-width format. The non-advancing write leaves the line open so the caller can continue the same record. |

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

Resolved lineage evidence shows one behavior-changing commit for this procedure: bc7755a updated the surrounding soil/carbon writer logic in soil_nutcarb_write.f90, but the extracted cb_emit_row_id_txt span itself is unchanged in the visible diff. No resolved commit diff shows a direct modification to the subroutine body.

## Review Notes

- Direct file I/O exists; verify file meanings and units before finalizing.
- warning: missing_doc: Procedure 'cb_emit_row_id_txt' has no extracted documentation comment.
