---
kind: procedure
symbol: cv_drv_blocks
title: cv_drv_blocks
status: filled
source_hash: ae0c61e9ee384c10
version_label: SWAT+ 62.0.0
args:
  u: Selects the output unit that receives the row blocks for this HRU, so the same data can
    be written to the text or CSV stream prepared by the caller.
  is_csv: Chooses CSV-comma formatting versus fixed-width text formatting when each per-layer
    block is written.
  j_in: Identifies which HRU's soil arrays (`soil1(j_in)` and `soil(j_in)`) are read to build
    each layer block.
  n_use_in: Limits how many soil layers are copied from the source arrays into `buf_in`; layers
    beyond `n_use_in` are left as zero in the buffer and handled as missing by the writer.
  buf_in: Reusable layer buffer that this routine overwrites for each variable block before
    passing it to `cb_write_var_block`.
locals:
  kk: Loop index over layer positions. It walks from layer 1 to `min(cb_n_layers, n_use_in)`
    while copying each source field into `buf_in`.
---

<!-- facts:header -->

Writes a wide, per-layer set of soil carbon driver variables for one HRU row. It fills a reusable layer buffer and delegates the actual row/block formatting to `cb_write_var_block`.

## Bottom Line

This helper assembles one per-layer variable at a time for the requested HRU (`j_in`), storing values in `buf_in` up to `n_use_in` soil layers and padding the rest with zeros before each write. It is used by `soil_carbvar_write` to emit the driver-variable portion of the soil carbon output in a consistent wide format.

The routine matters because downstream carbon-output files rely on the same row layout for every HRU: depth is written first by the caller, then this routine writes the sequence of soil and organic-carbon driver fields, ending the last block with a newline via `cb_write_var_block`'s `advance_str` argument.

## Arguments

<!-- facts:arguments -->

## Where It Fits

This routine runs inside `soil_carbvar_write` after that caller has selected the active HRU, determined the number of layers to use, and written the row's depth block. Its output becomes the sequence of per-layer driver-variable columns in the carbon-variable file, so later analysis of soil carbon drivers depends on this block layout being consistent.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. copy sut layers into buffer | Clears `buf_in`, copies `soil1(j_in)%org_con_lr(kk)%sut` into the first `min(cb_n_layers, n_use_in)` positions, then writes that layer block to the target unit. |
| 2. copy tillagef layers into buffer | Loads `soil(j_in)%ly(kk)%tillagef` for the active layers and emits it as the next per-layer variable block. |
| 3. copy bmix layers into buffer | Loads `soil(j_in)%ly(kk)%bmix` into `buf_in` and writes that block to the same output row. |
| 4. copy tillagef_biomix layers into buffer | Loads `soil(j_in)%ly(kk)%tillagef_biomix` for the active layers and writes it as the next block. |
| 5. copy tillagef_tillmix layers into buffer | Loads `soil(j_in)%ly(kk)%tillagef_tillmix` into the buffer and writes that layer block. |
| 6. copy till_eff layers into buffer | Loads `soil1(j_in)%org_con_lr(kk)%till_eff` and emits it as the next variable block. |
| 7. copy cdg layers into buffer | Loads `soil1(j_in)%org_con_lr(kk)%cdg` into the reusable buffer and writes it. |
| 8. copy ox layers into buffer | Loads `soil1(j_in)%org_con_lr(kk)%ox` for the active layers and writes that block. |
| 9. copy cs layers into buffer | Loads `soil1(j_in)%org_con_lr(kk)%cs` and writes the carbon-soil block. |
| 10. copy no3 layers into buffer | Loads `soil1(j_in)%org_con_lr(kk)%no3` and writes the nitrate block. |
| 11. copy nh4 layers into buffer | Loads `soil1(j_in)%org_con_lr(kk)%nh4` into the buffer and writes the ammonium block. |
| 12. copy resp layers into buffer | Loads `soil1(j_in)%org_con_lr(kk)%resp` and writes the respiration-related block. |
| 13. copy tmp layers into buffer | Loads `soil(j_in)%phys(kk)%tmp` into `buf_in` and writes the temperature block. |
| 14. copy emix layers and end row | Loads `soil1(j_in)%emix(kk)` for the active layers and writes the final block with `advance_str` set to `"yes"` so the row ends after this variable. |

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

The procedure was introduced in f66c8e6 as a new helper for writing soil carbon output blocks. bc7755a later refactored the surrounding carbon-output system to a file-based, per-family wide format, but the diff shown here did not change the body of `cv_drv_blocks` itself. 2ee1889 only cleaned up the subroutine end statement in the file and did not alter the algorithm.

- f66c8e6 added `cv_drv_blocks` as the block writer for soil carbon driver variables, introducing the per-layer buffer-fill-and-write pattern.
- bc7755a changed the surrounding soil carbon output workflow to a wide per-layer format, making this helper part of the new driver-variable output path without altering its shown statements.
- 2ee1889 made a formatting-only cleanup at the end of the source file; the routine logic remained unchanged.

## Review Notes

- No direct file I/O was extracted for this procedure.
- warning: missing_doc: Procedure 'cv_drv_blocks' has no extracted documentation comment.
