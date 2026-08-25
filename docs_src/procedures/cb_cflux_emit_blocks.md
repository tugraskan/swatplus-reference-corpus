---
kind: procedure
symbol: cb_cflux_emit_blocks
title: cb_cflux_emit_blocks
status: filled
source_hash: b331a1ee2b57cabe
version_label: SWAT+ 62.0.0
args:
  u: '`u` is the output unit number that receives each variable block written by `cb_write_var_block`.
    The routine does not open or close the unit itself; it only streams the cflux row to this
    already-prepared destination.'
  is_csv: '`is_csv` selects the record format passed through to `cb_write_var_block`: CSV
    output uses comma-prefixed values, while non-CSV output uses spaced numeric fields. This
    flag lets the same routine serve both text and CSV emissions.'
  hru_j: '`hru_j` selects which HRU''s carbon-flux arrays are read from `soil1(hru_j)` for
    every layer value. The procedure emits one row of data for that specific HRU.'
  n_use: '`n_use` limits how many soil layers are treated as active in the row and is forwarded
    to `cb_write_var_block` for padding beyond the active layers. The loops only fill `buf(1:min(cb_n_layers,n_use))`
    before each write.'
  buf: '`buf` is a scratch vector reused to stage one variable''s layer values before each
    write. The routine overwrites it many times and relies on `cb_write_var_block` to emit
    its contents immediately.'
  use_aa: '`use_aa` chooses between annual-average cumulative flux values and the direct layer
    flux values. When true, each staged value comes from `soil1(hru_j)%org_flx_cum_lr(k)%.../yrs`;
    when false, it comes from `soil1(hru_j)%org_flx_lr(k)%...`.'
locals:
  k: '`k` is the layer index used to copy one carbon-flux field at a time from the HRU''s
    per-layer storage into `buf`. It is also bounded by `min(cb_n_layers, n_use)` so the routine
    only stages values for layers that should be written.'
  yrs: '`yrs` stores the protected divisor `max(time%yrs_prt, 1.0)`, used to convert cumulative
    flux totals into per-year averages when `use_aa` is true. The max avoids dividing by zero
    if the printed-year count is not yet positive.'
---

<!-- facts:header -->

Writes one HRU's carbon-flux variables as fixed per-layer blocks to a text or CSV record. It formats the current or cumulative flux arrays depending on `use_aa` and uses `cb_write_var_block` to emit each variable in the cflux summary row.

## Bottom Line

This routine walks through the carbon-flux variables for one HRU and fills a reusable layer buffer with either annual-average cumulative values or instantaneous values from `soil1(hru_j)%org_flx_cum_lr(k)` versus `soil1(hru_j)%org_flx_lr(k)`, selected by `use_aa`. It then writes each variable block to the requested output unit with `cb_write_var_block`.

It matters because `cb_cflux_stat_emit` uses it to produce the full cflux statistics rows for both plain-text and CSV outputs, after that caller has already written the row identifier and depth row. The last call sets the record advance so the final variable block ends the line.

## Arguments

<!-- facts:arguments -->

## Where It Fits

This routine runs inside the carbon-statistics emission workflow after `cb_cflux_stat_emit` has already chosen the HRU, opened the target unit, emitted the row ID, written the depth row, and set `n_use = soil(hru_j)%nly`. Its output is the ordered set of cflux variable blocks that downstream reporting depends on for both text and CSV summary files.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. Compute the printed-year divisor. | Sets `yrs = max(time%yrs_prt, 1.0)` so later annual-average calculations can divide cumulative flux totals safely without risking a zero divisor. |
| 2. Stage and write `cfmets1`. | Clears `buf`, fills active layers from either the cumulative or direct `cfmets1` field depending on `use_aa`, then writes the block with `cb_write_var_block`. |
| 3. Stage and write `cfstrs1`. | Repeats the same buffer-fill and write pattern for `cfstrs1`. |
| 4. Stage and write `cfstrs2`. | Copies `cfstrs2` values into `buf` and emits the block. |
| 5. Stage and write `efmets1`. | Copies the `efmets1` flux values into the shared buffer and writes them out. |
| 6. Stage and write `efstrs1`. | Loads `efstrs1` for the active layers and writes the block. |
| 7. Stage and write `efstrs2`. | Fills `buf` with `efstrs2` values and emits them. |
| 8. Stage and write `immmets1`. | Writes the `immmets1` flux block after loading the corresponding per-layer values. |
| 9. Stage and write `immstrs1`. | Copies and writes `immstrs1` for the current HRU. |
| 10. Stage and write `immstrs2`. | Loads `immstrs2` into the buffer and emits it. |
| 11. Stage and write `mnrmets1`. | Fills `buf` from `mnrmets1` and writes the block. |
| 12. Stage and write `mnrstrs1` and `mnrstrs2`. | Emits the two mineral-transfer stress blocks in sequence by staging each field into `buf` and calling `cb_write_var_block` after each fill. |
| 13. Stage and write the carbon-dioxide and soil-transfer blocks. | Continues the same pattern for `co2fmet`, `co2fstr`, `cfs1s2`, `cfs1s3`, `cfs2s1`, `cfs2s3`, `cfs3s1`, `efs1s2`, `efs1s3`, `efs2s1`, `efs2s3`, `efs3s1`, `imms1s2`, `imms1s3`, `imms2s1`, `imms2s3`, `imms3s1`, `mnrs1s2`, `mnrs1s3`, `mnrs2s1`, `mnrs2s3`, and `mnrs3s1`. |
| 14. Stage and write the final CO2 source blocks, ending the record. | Writes `co2fs1`, `co2fs2`, and `co2fs3` in order, then uses `advance_str = "yes"` on the last call so the output line is terminated after the final block. |

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

Source-backed lineage commits were resolved. The only resolved change shown in the evidence is bc7755a, which refactored this source file around carbon-output handling; however, the provided diff excerpt does not show any edits within the `cb_cflux_emit_blocks` body itself, so no behavior change for this routine is visible in the supplied diff.

- bc7755a: The provided diff excerpt shows broader carbon-output refactoring in `soil_nutcarb_write.f90`, but no lines from `cb_cflux_emit_blocks` are changed in the excerpt, so no direct impact on this routine can be confirmed from the supplied evidence.

## Review Notes

- No direct file I/O was extracted for this procedure.
- warning: missing_doc: Procedure 'cb_cflux_emit_blocks' has no extracted documentation comment.
