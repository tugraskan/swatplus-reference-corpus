---
kind: procedure
symbol: cb_write_cbn_lyr_header
title: cb_write_cbn_lyr_header
status: filled
source_hash: 63848987d4072ea9
version_label: SWAT+ 62.0.0
args:
  unit_no: '`in` argument of type `integer`.'
  is_csv: '`in` argument of type `logical`.'
locals:
  tag: Local variable of type `character(len=32)`.
  k: Local variable of type `integer`.
---

<!-- facts:header -->

Writes the header for the `hru_cbn_lyr` files, interleaving the 300 mm scalar sums with the per-layer columns.

## Bottom Line

`cb_write_cbn_lyr_header` emits a specialized wide header in which the 300 mm scalar totals (`tot_300_sum`, `seq_300_sum`) are interleaved with the per-layer depth and value columns, rather than appended, matching the `hru_cbn_lyr` file layout.

It is a formatting helper for the total-soil-carbon-by-layer legacy output.

## Arguments

<!-- facts:arguments -->

## Where It Fits

Called when opening the `hru_cbn_lyr` carbon output files.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. Select output conditions | Executes the source at the referenced lines. |
| 2. Loop over output items | Executes the source at the referenced lines. |
| 3. Write output records | Executes the source at the referenced lines. |

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

No hand-authored source-lineage narrative was produced for this helper; see the Git Lineage Evidence below for the commit history of `carbon_module.f90`.

## Review Notes

- Direct file I/O exists; verify file meanings and units before finalizing.
- warning: missing_doc: Procedure 'carbon_module::cb_write_cbn_lyr_header' has no extracted documentation comment.
