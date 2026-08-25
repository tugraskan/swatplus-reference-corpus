---
kind: procedure
symbol: respest_ave
title: respest_ave
status: filled
source_hash: 28c1d0a9d046124e
version_label: SWAT+ 62.0.0
args:
  res1: The first `res_pesticide_processes` operand (intent(in)).
  const: Scalar applied to each field of the `res_pesticide_processes` record.
locals:
  res2: 'Result variable: the `res_pesticide_processes` record the function returns, holding
    the field-by-field result.'
---

<!-- facts:header -->

Copies a `res_pesticide_processes` record field by field (identity), defined in `res_pesticide_module`.

## Bottom Line

`respest_ave` returns a new `res_pesticide_processes` record that copies every field of its input unchanged. All 14 fields are copied verbatim from the input. Despite the `_ave` suffix, this routine performs only the copy; any averaging (division by a day or period count) is done by the caller.

This is one of the small arithmetic helpers `res_pesticide_module` defines for the `res_pesticide_processes` derived type. SWAT+ output and routing code calls it to keep `res_pesticide_processes` records copied — typically when rolling daily state up into monthly, yearly, and average-annual totals. It is a pure function: its arguments are `intent(in)` and it has no side effects.

## Arguments

<!-- facts:arguments -->

## Where It Fits

`respest_ave` is a pure, side-effect-free helper in `res_pesticide_module`; it only computes a new `res_pesticide_processes` value from its arguments and does no I/O. It runs wherever `res_pesticide_processes` records are copied, chiefly along the output-accumulation path (daily → monthly → yearly → average annual).

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| Review source manually | No major control-flow steps were extracted automatically. |

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

No hand-authored source-lineage narrative was produced for this helper; see the Git Lineage Evidence below for the commit history of `res_pesticide_module.f90`.

## Review Notes

- No direct file I/O was extracted for this procedure.
- warning: missing_doc: Procedure 'res_pesticide_module::respest_ave' has no extracted documentation comment.
- info: no_flow_steps: No major control-flow or I/O steps were extracted for this procedure.
