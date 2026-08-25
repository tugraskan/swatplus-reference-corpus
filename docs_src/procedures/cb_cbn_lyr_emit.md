---
kind: procedure
symbol: cb_cbn_lyr_emit
title: cb_cbn_lyr_emit
status: filled
source_hash: b043c9d4894e4b03
version_label: SWAT+ 62.0.0
args:
  freq_in: '`freq_in` selects which reporting period to emit. The routine maps `'' d''`, `''
    m''`, `'' y''`, and `'' a''` to distinct text and CSV unit numbers and only continues
    when the matching `pco%cb_lyr_hru` flag is set; any other value causes an immediate return.'
  hru_j: '`hru_j` identifies the HRU whose soil profile and carbon values are written. It
    is used to index `soil(hru_j)` and `soil1(hru_j)` when collecting layer depths and carbon
    totals.'
  hru_iob: '`hru_iob` identifies the corresponding object metadata passed to the row-id helpers.
    It lets the routine write the correct GIS ID and name for the HRU row in both text and
    CSV output.'
locals:
  u_txt: Text output unit chosen from the requested frequency; all plain-text row pieces are
    written to this unit.
  u_csv: CSV output unit chosen from the requested frequency; it is used only when `pco%csvout
    == "y"`.
  k: Loop index over soil layers while filling temporary arrays from `soil(hru_j)` and `soil1(hru_j)`.
  n_use: Number of active soil layers in the HRU, taken from `soil(hru_j)%nly` so the emit
    helpers know how many layer values to write.
  buf: Temporary layer-value buffer sized to `cb_n_layers`; it is populated with depths or
    carbon values before each helper call.
---

<!-- facts:header -->

Emits layered soil carbon output for one HRU in text and optional CSV form. It writes row identifiers, layer depths, and two carbon pools plus 300 mm summary values, gated by the requested frequency and output flags.

## Bottom Line

cb_cbn_lyr_emit formats one HRU's carbon-layer report row. It chooses the correct output units for daily, monthly, yearly, or average-annual frequency, checks the corresponding `pco%cb_lyr_hru` flag, and returns immediately if that output is disabled.

When enabled, it writes a text row and, if `pco%csvout == "y"`, a matching CSV row. The row contains the HRU identifier fields, soil layer depths, total carbon (`tot`) by layer and its 300 mm sum, and sequential carbon (`seq`) by layer and its 300 mm sum.

## Arguments

<!-- facts:arguments -->

## Where It Fits

This routine runs when `soil_nutcarb_write` is exporting carbon results for an HRU. `soil_nutcarb_write` prepares the layer totals, selects the reporting frequency, and then calls this helper so the carbon-layer table can be appended to the already-open output files; later reporting routines depend on the same per-HRU carbon state and output flags.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. Select the output unit pair for the requested frequency and honor the corresponding carbon-layer enable flag. | The routine maps `freq_in` to text and CSV unit numbers for daily, monthly, yearly, or average-annual output, and returns immediately if the matching `pco%cb_lyr_hru` switch is not enabled. |
| 2. Determine how many soil layers are active for this HRU. | It copies `soil(hru_j)%nly` into `n_use` so the emit helpers know how many layer positions contain real data. |
| 3. Emit the text row identity and depth columns. | The routine writes the text row header, fills `buf` with layer depths from `soil(hru_j)%phys(k)%d`, and passes those depths to `cb_write_depth_row`. |
| 4. Write the text 300 mm total-carbon summary and the per-layer total-carbon block. | It writes `soil1(hru_j)%tot_300_c/1000.` directly to the text unit, loads per-layer total carbon into `buf`, and emits that block with `cb_write_var_block`. |
| 5. Write the text 300 mm sequential-carbon summary and the per-layer sequential-carbon block. | It writes `soil1(hru_j)%seq_tot_300_c/1000.` to the text unit, fills `buf` with per-layer sequential carbon, and terminates the text row after `cb_write_var_block` finishes. |
| 6. If CSV output is enabled, emit the CSV row identity and mirror the depth and carbon columns. | The routine writes the CSV row prefix, repeats the depth and carbon-buffer setup for CSV formatting, writes the 300 mm total and sequential carbon summaries, and closes the CSV row with the final variable block. |

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

The resolved lineage shows one substantive change to this procedure: commit bc7755a added the average-annual frequency branch (`' a'`) so `cb_cbn_lyr_emit` can write `av_ann` outputs with their own text and CSV units and gating flag. The same diff also removed a local `write_hdr` variable from nearby code, but the procedure body here is otherwise the same layered carbon emit workflow.

- bc7755a expanded the frequency switch to handle average-annual carbon-layer output by adding unit pair 4533/4537 and the `pco%cb_lyr_hru%a` gate.

## Review Notes

- Direct file I/O exists; verify file meanings and units before finalizing.
- warning: missing_doc: Procedure 'cb_cbn_lyr_emit' has no extracted documentation comment.
