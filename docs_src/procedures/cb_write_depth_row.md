---
kind: procedure
symbol: cb_write_depth_row
title: cb_write_depth_row
status: filled
source_hash: d65f213bc2e39a64
version_label: SWAT+ 62.0.0
args:
  unit_no: '`in` argument of type `integer`.'
  depths: '`in` argument of type `real`.'
  n_use: '`in` argument of type `integer`.'
  is_csv: '`in` argument of type `logical`.'
  advance_str: '`in` argument of type `character(len=*)`.'
locals:
  k: Local variable of type `integer`.
  v: Local variable of type `real`.
---

<!-- facts:header -->

Emits the per-layer depth columns of a carbon data row, padding unused layers past `n_use` with the missing-value marker.

## Bottom Line

`cb_write_depth_row` writes the `depth_lyrK` values for a data row up to `n_use` layers and fills the remaining layer slots with `cb_lyr_missing`. The caller has already written the identity columns and continues with the variable columns afterwards.

It keeps every row rectangular across HRUs with different layer counts.

## Arguments

<!-- facts:arguments -->

## Where It Fits

Called by the carbon row writers when emitting a wide per-layer carbon data row.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. loop | Loop over `do k = 1, cb_n_layers`. |
| 2. if | Conditional branch evaluating `k <= n_use`. |
| 3. else | Alternative branch taken when the preceding condition is false. |
| 4. if | Conditional branch evaluating `is_csv`. |
| 5. io | Executes `write (unit_no, '(a,g0.7)', advance='no') ",", v`. |
| 6. else | Alternative branch taken when the preceding condition is false. |
| 7. io | Executes `write (unit_no, '(1x,g22.7)', advance='no') v`. |
| 8. if | Conditional branch evaluating `advance_str == "yes") write (unit_no, '(a)') ""`. |

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
- warning: missing_doc: Procedure 'carbon_module::cb_write_depth_row' has no extracted documentation comment.
