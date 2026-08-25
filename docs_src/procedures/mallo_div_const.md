---
kind: procedure
symbol: mallo_div_const
title: mallo_div_const
status: filled
source_hash: 2fc11c1dd2a3b27f
version_label: SWAT+ 62.0.0
args:
  mallo1: The first `source_manure_output` operand (intent(in)).
  const: Scalar applied to each field of the `source_manure_output` record.
locals:
  mallo2: 'Result variable: the `source_manure_output` record the function returns, holding
    the field-by-field result.'
---

<!-- facts:header -->

Divides a `source_manure_output` record by a scalar (`const`) field by field, defined in `manure_allocation_module` and used to average accumulated `source_manure_output` state.

## Bottom Line

`mallo_div_const` returns a new `source_manure_output` record whose fields are its input's fields each divided by the scalar `const`. 2 of the 3 fields are divided by `const`: `prod`, `withdr`. The other 1 field is copied through unchanged (not scaled); these are the flux totals that are not averaged.

This is one of the small arithmetic helpers `manure_allocation_module` defines for the `source_manure_output` derived type. SWAT+ output and routing code calls it to keep `source_manure_output` records averaged — typically when rolling daily state up into monthly, yearly, and average-annual totals. It is a pure function: its arguments are `intent(in)` and it has no side effects.

## Arguments

<!-- facts:arguments -->

## Where It Fits

`mallo_div_const` is a pure, side-effect-free helper in `manure_allocation_module`; it only computes a new `source_manure_output` value from its arguments and does no I/O. It runs wherever `source_manure_output` records are averaged, chiefly along the output-accumulation path (daily → monthly → yearly → average annual).

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

No hand-authored source-lineage narrative was produced for this helper; see the Git Lineage Evidence below for the commit history of `manure_allocation_module.f90`.

## Review Notes

- No direct file I/O was extracted for this procedure.
- warning: missing_doc: Procedure 'manure_allocation_module::mallo_div_const' has no extracted documentation comment.
- info: no_flow_steps: No major control-flow or I/O steps were extracted for this procedure.
