---
kind: procedure
symbol: watbod_div
title: watbod_div
status: filled
source_hash: 156b21623b7d4128
version_label: SWAT+ 62.0.0
args:
  wbod1: The first `water_body` operand (intent(in)).
  const: Scalar applied to each field of the `water_body` record.
locals:
  wbod2: 'Result variable: the `water_body` record the function returns, holding the field-by-field
    result.'
---

<!-- facts:header -->

Divides a `water_body` record by a scalar (`const`) field by field, defined in `water_body_module` and used to average accumulated `water_body` state.

## Bottom Line

`watbod_div` returns a new `water_body` record whose fields are its input's fields each divided by the scalar `const`. 4 of the 4 fields are divided by `const`: `area_ha`, `precip`, `evap`, `seep`.

This is one of the small arithmetic helpers `water_body_module` defines for the `water_body` derived type. SWAT+ output and routing code calls it to keep `water_body` records averaged — typically when rolling daily state up into monthly, yearly, and average-annual totals. It is a pure function: its arguments are `intent(in)` and it has no side effects.

## Arguments

<!-- facts:arguments -->

## Where It Fits

`watbod_div` is a pure, side-effect-free helper in `water_body_module`; it only computes a new `water_body` value from its arguments and does no I/O. It runs wherever `water_body` records are averaged, chiefly along the output-accumulation path (daily → monthly → yearly → average annual).

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

No hand-authored source-lineage narrative was produced for this helper; see the Git Lineage Evidence below for the commit history of `water_body_module.f90`.

## Review Notes

- No direct file I/O was extracted for this procedure.
- warning: missing_doc: Procedure 'water_body_module::watbod_div' has no extracted documentation comment.
- info: no_flow_steps: No major control-flow or I/O steps were extracted for this procedure.
