---
kind: procedure
symbol: cb_soil_snap_period
title: cb_soil_snap_period
status: filled
source_hash: 8ea2325546d520ae
version_label: SWAT+ 62.0.0
args:
  freq_in: '`freq_in` chooses which snapshot period this wrapper handles. Only the three two-character
    codes `'' d''`, `'' m''`, and `'' y''` are recognized; any other value returns without
    output.'
  hru_j: '`hru_j` identifies the HRU whose soil snapshot is being written. It is forwarded
    to the emitter so the output row uses the correct HRU soil profile data.'
  hru_iob: '`hru_iob` identifies the HRU''s object record in `ob`. It is forwarded so the
    emitted snapshot row can be tagged with the right HRU metadata.'
locals:
  u_txt: Text output unit selected from the period code. It points to the already-open period-specific
    soil snapshot text file.
  u_csv: CSV output unit selected from the period code. It points to the already-open period-specific
    soil snapshot CSV file when CSV output is enabled.
---

<!-- facts:header -->

Writes an HRU soil-property snapshot for the requested period frequency. It selects the period-specific snapshot files and only emits rows when that HRU snapshot output is enabled.

## Bottom Line

This routine is a frequency gate for soil snapshot output. Given a period code (`freq_in`), it maps that code to the matching text and CSV units for day, month, or year HRU soil snapshot files, then stops immediately if that output family is disabled in `pco%cb_snap_hru`.

If the requested period is enabled, it delegates the actual row emission to `cb_soil_snap_emit`, passing the selected units plus the HRU indices. That keeps the period wrapper focused on routing while the callee writes the snapshot row content.

## Arguments

<!-- facts:arguments -->

## Where It Fits

This wrapper runs inside `soil_nutcarb_write` after the loop has determined the current output frequency. The caller passes `out_freq` together with the current HRU indices, and this routine routes only the daily, monthly, or yearly soil snapshot cases; downstream behavior depends on it because the chosen units determine which period snapshot files receive the HRU soil rows.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. select period | Branch on `freq_in` so the routine can route to the correct period-specific soil snapshot output units. |
| 2. handle daily | For daily snapshots, assign text unit 4598 and CSV unit 4602, then return immediately unless `pco%cb_snap_hru%d` is enabled. |
| 3. handle monthly | For monthly snapshots, assign text unit 4599 and CSV unit 4603, then return immediately unless `pco%cb_snap_hru%m` is enabled. |
| 4. handle yearly | For yearly snapshots, assign text unit 4600 and CSV unit 4604, then return immediately unless `pco%cb_snap_hru%y` is enabled. |
| 5. reject other codes | Return immediately for any other `freq_in` value, including the auxiliary `aa`-style frequency that is not written here. |
| 6. emit snapshot row | Call `cb_soil_snap_emit` with the selected units, the stage label `period`, and the HRU indices so the shared emitter can write the snapshot row. |

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

Resolved lineage shows one behavior change relevant to this routine: commit bc7755a expanded the parent soil snapshot workflow to add the new `a`/`al` frequency handling and moved snapshot-family gating into per-family emit routines. The period wrapper itself still follows the same pattern of selecting period-specific units and then delegating to the shared emitter.

- bc7755a: the surrounding soil snapshot system was refactored so gating is handled per family and the new `a`/`al` frequency paths were added elsewhere in the module; this wrapper continues to route day/month/year period output through a shared emitter.

## Review Notes

- No direct file I/O was extracted for this procedure.
- warning: missing_doc: Procedure 'cb_soil_snap_period' has no extracted documentation comment.
