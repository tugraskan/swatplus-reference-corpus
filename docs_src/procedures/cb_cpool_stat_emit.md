---
kind: procedure
symbol: cb_cpool_stat_emit
title: cb_cpool_stat_emit
status: filled
source_hash: ed48b09543d63cc1
version_label: SWAT+ 62.0.0
args:
  freq_in: Selects which output frequency branch to use (' d', ' m', ' y', or ' a'); that
    choice determines the text/CSV unit numbers and whether the matching `pco%cb_cpool_hru`
    flag allows output.
  hru_j: Identifies the HRU whose layer profile and soil-carbon pool values will be exported;
    it is also written in the row header and used to index `soil(hru_j)` and `soil1(hru_j)`.
  hru_iob: Selects the object record that supplies GIS ID and name for the row header, so
    the emitted record can be linked back to the correct HRU object.
locals:
  u_txt: Holds the text output unit chosen from `freq_in`; all wide-row text writes for this
    frequency go to this unit.
  u_csv: Holds the CSV output unit chosen from `freq_in`; it is used only when `pco%csvout
    == 'y'`.
  k: Loop index over soil layers when copying layer values into the temporary buffer.
  n_use: Stores the number of active soil layers for `soil(hru_j)`, which limits how many
    buffer entries are populated and tells the write helpers how many layers are real versus
    padded.
  buf: Temporary layer-value buffer passed to the row-writing helpers; it is refilled with
    one variable block at a time before each write call.
---

<!-- facts:header -->

Emits one wide per-layer carbon-pool status row for a single HRU at the requested frequency. It writes both text and optional CSV output, gated by the corresponding carbon-pool export flags.

## Bottom Line

cb_cpool_stat_emit builds one fixed-format, wide per-layer export record for an HRU's carbon-pool state. It writes the current date/time plus HRU and object identifiers, then appends depth, residue, structural, metabolic, humic, passive, microbial, lignin, non-lignin, root, and soil-water values across the soil layers in a single row.

The routine only runs for frequencies enabled in `pco%cb_cpool_hru` and returns immediately for unsupported frequency codes. When CSV output is enabled it emits the matching CSV row prefix and then writes the same layer blocks to the CSV unit.

## Arguments

<!-- facts:arguments -->

## Where It Fits

This routine runs inside `soil_nutcarb_write` after the per-HRU carbon-output frequency has been selected and the `bsn_cc%cswat == 2` carbon pathway has been confirmed. `soil_nutcarb_write` passes the HRU index and object index for the current HRU, and downstream model documentation or postprocessing depends on the resulting per-layer carbon-pool snapshot files for day, month, year, or average-annual reporting.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. Select output units and gate on frequency flags. | The routine branches on `freq_in`, assigns the matching text and CSV unit numbers for daily, monthly, yearly, or average-annual output, and immediately returns if the corresponding `pco%cb_cpool_hru` flag is not enabled or if the frequency code is unknown. |
| 2. Determine how many soil layers are active. | It sets `n_use` from `soil(hru_j)%nly` so later write helpers know how many layer values are real and how many must be padded. |
| 3. Write the text row prefix. | It starts the text record on `u_txt` with the date, HRU number, GIS ID, and object name, using non-advancing output so later helper calls can append more columns to the same row. |
| 4. Emit the depth columns for the text row. | It fills `buf` with soil layer depths and calls `cb_write_depth_row` to append the depth block for all configured layers. |
| 5. Emit each carbon-pool variable block to the text row. | It repeatedly loads `buf` from `soil1(hru_j)` or `soil(hru_j)` and calls `cb_write_var_block` for residue carbon, structural carbon, metabolic carbon, humic soil pools, passive soil pools, microbial carbon, lignin, non-lignin, root mass, and soil total water, ending the record on the final call. |
| 6. Optionally emit the CSV row prefix and variable blocks. | If `pco%csvout == 'y'`, it writes the CSV row header with `cb_emit_row_id_csv` and then repeats the same depth and variable-block sequence on `u_csv`, again terminating on the final helper call. |

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

Two resolved commits changed this procedure. Commit bc7755a refactored the carbon export logic so the average-annual (`' a'`) branch is recognized, `cb_cpool_stat_emit` uses per-frequency HRU flags, and the old diagnostic/wide-soil snapshot behavior was replaced by the current carbon-pool emitter structure. Commit 1c5d6c8 added the current `cb_cpool_stat_emit` routine and its per-frequency text/CSV output path for carbon-pool status files.

- bc7755a: added average-annual carbon-pool export handling and per-family gating through `pco%cb_cpool_hru`, replacing the earlier diagnostics-based snapshot path.
- 1c5d6c8: introduced `cb_cpool_stat_emit` as the wide per-layer carbon-pool status writer with text and optional CSV output.

## Review Notes

- Direct file I/O exists; verify file meanings and units before finalizing.
- warning: missing_doc: Procedure 'cb_cpool_stat_emit' has no extracted documentation comment.
