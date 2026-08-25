---
kind: procedure
symbol: wallo_div_const
title: wallo_div_const
status: filled
source_hash: e1b884f6edc5e54f
version_label: SWAT+ 62.0.0
args:
  wallo1: The first `source_output` operand (intent(in)).
  const: Scalar applied to each field of the `source_output` record.
locals:
  wallo2: 'Result variable: the `source_output` record the function returns, holding the field-by-field
    result.'
---

<!-- facts:header -->

Divides a `source_output` record by a scalar (`const`) field by field, defined in `water_allocation_module` and used to average accumulated `source_output` state.

## Bottom Line

`wallo_div_const` returns a new `source_output` record whose fields are its input's fields each divided by the scalar `const`. 3 of the 3 fields are divided by `const`: `demand`, `withdr`, `unmet`.

This is one of the small arithmetic helpers `water_allocation_module` defines for the `source_output` derived type. SWAT+ output and routing code calls it to keep `source_output` records averaged — typically when rolling daily state up into monthly, yearly, and average-annual totals. It is a pure function: its arguments are `intent(in)` and it has no side effects.

## Arguments

<!-- facts:arguments -->

## Where It Fits

`wallo_div_const` is a pure, side-effect-free helper in `water_allocation_module`; it only computes a new `source_output` value from its arguments and does no I/O. It runs wherever `source_output` records are averaged, chiefly along the output-accumulation path (daily → monthly → yearly → average annual).

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

No hand-authored source-lineage narrative was produced for this helper; see the Git Lineage Evidence below for the commit history of `water_allocation_module.f90`.

## Review Notes

- No direct file I/O was extracted for this procedure.
- warning: missing_doc: Procedure 'water_allocation_module::wallo_div_const' has no extracted documentation comment.
- info: no_flow_steps: No major control-flow or I/O steps were extracted for this procedure.
