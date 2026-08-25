---
kind: procedure
symbol: cv_dyn_blocks
title: cv_dyn_blocks
status: filled
source_hash: 6e4e5f1527f73434
version_label: SWAT+ 62.0.0
args:
  u: '`u` is the already-open output unit that receives each carbon-variable block written
    by `cb_write_var_block`.'
  is_csv: '`is_csv` selects CSV-style output when true and space-delimited text output when
    false, so the downstream writer can choose commas and record formatting correctly.'
  j_in: '`j_in` selects which HRU''s soil profile is read from `soil1(j_in)` for all layer-by-layer
    values written by this routine.'
  n_use_in: '`n_use_in` limits how many layers from the HRU profile are treated as active;
    layers beyond that count are left as missing by the shared block writer.'
  buf_in: '`buf_in` is a reusable per-layer scratch buffer. The routine clears it, fills the
    active layer positions with one variable at a time, and passes it to the output helper
    for writing.'
locals:
  kk: '`kk` is the loop index over soil layers. It walks from layer 1 to `min(cb_n_layers,
    n_use_in)` while copying each variable from the HRU profile into `buf_in`.'
---

<!-- facts:header -->

Writes the per-layer soil carbon dynamic variables for one HRU as wide blocks on an output unit. It gathers values from `soil1(j_in)` and emits them through the shared carbon-block writer.

## Bottom Line

`cv_dyn_blocks` prepares a sequence of per-layer carbon dynamic variables for a single HRU (`j_in`) and writes each variable block to the supplied output unit `u`. It uses `n_use_in` to limit how many soil layers are populated from `soil1(j_in)` and relies on `cb_write_var_block` to format and emit each block consistently.

The routine is part of the carbon-variable output path started by `soil_carbvar_write`. It does not compute new carbon state; it copies existing allocation, ratio, and transformation values into a reusable buffer and streams them out in text or CSV form depending on `is_csv`.

## Arguments

<!-- facts:arguments -->

## Where It Fits

`cv_dyn_blocks` runs inside `soil_carbvar_write` after that caller has chosen the dynamic-output unit, written the row header/depth row, and decided that dynamic carbon output is enabled. Its output is used immediately to create the HRU-level dynamic carbon report, with both text and optional CSV forms depending on the caller's settings.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. Initialize the allocation block buffer. | The routine clears `buf_in`, copies `soil1(j_in)%org_allo_lr(kk)%asp` into each active layer position, and writes that allocation variable block through `cb_write_var_block`. |
| 2. Emit the remaining allocation variables. | It repeats the clear/fill/write pattern for `abp`, `abco2`, `a1co2`, `asco2`, and `apco2`, producing six allocation-related blocks in total. |
| 3. Emit the N:C ratio blocks. | The routine copies each active layer's `ncbm`, `nchp`, and `nchs` values from `soil1(j_in)%org_ratio_lr` into `buf_in` and writes each ratio block. |
| 4. Emit the transformation blocks. | It clears and refills `buf_in` for each transformation variable from `soil1(j_in)%org_tran_lr`, then calls `cb_write_var_block` after every fill to stream the block to the output unit. |
| 5. Close the final block with an advance flag. | The last call passes `advance_str = 'yes'` so the writer terminates the record after the final transformation variable and completes the output row. |

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

Two resolved commits changed `cv_dyn_blocks`. Commit f66c8e6 added the routine as part of the initial soil carbon output implementation, introducing the per-HRU/per-layer block-writing pattern for carbon variables. Commit bc7755a later refactored the carbon subsystem to file-based inputs and per-family outputs, expanding this routine into the current grouped layout of allocation, N:C ratio, and transformation blocks while keeping the same shared block writer pattern. Commit 2ee1889 only cleaned the subroutine end statement and did not change behavior.

- f66c8e6 introduced `cv_dyn_blocks` and established the shared-buffer, per-layer output pattern for soil carbon reporting.
- bc7755a reorganized the soil carbon output into per-family dynamic blocks and kept `cv_dyn_blocks` aligned with the wider carbon output refactor.
- 2ee1889 made only a syntactic cleanup at the subroutine end and did not alter runtime behavior.

## Review Notes

- No direct file I/O was extracted for this procedure.
- warning: missing_doc: Procedure 'cv_dyn_blocks' has no extracted documentation comment.
