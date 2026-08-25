---
kind: procedure
symbol: hruout_waterbal_div
title: hruout_waterbal_div
status: filled
source_hash: 1a800c8742b51dde
version_label: SWAT+ 62.0.0
args:
  hru1: The first `output_waterbal` operand (intent(in)).
  const: Scalar applied to each field of the `output_waterbal` record.
locals:
  hru2: 'Result variable: the `output_waterbal` record the function returns, holding the field-by-field
    result.'
---

<!-- facts:header -->

Divides a `output_waterbal` record by a scalar (`const`) field by field, defined in `output_landscape_module` and used to average accumulated `output_waterbal` state.

## Bottom Line

`hruout_waterbal_div` returns a new `output_waterbal` record whose fields are its input's fields each divided by the scalar `const`. 33 of the 38 fields are divided by `const`: `precip`, `snofall`, `snomlt`, `surq_gen`, `latq`, `wateryld`, `perc`, `et`, `ecanopy`, `eplant`, `esoil`, `surq_cont`, … (33 total). The other 5 fields are copied through unchanged (not scaled); these are the flux totals that are not averaged.

This is one of the small arithmetic helpers `output_landscape_module` defines for the `output_waterbal` derived type. SWAT+ output and routing code calls it to keep `output_waterbal` records averaged — typically when rolling daily state up into monthly, yearly, and average-annual totals. It is a pure function: its arguments are `intent(in)` and it has no side effects.

## Arguments

<!-- facts:arguments -->

## Where It Fits

`hruout_waterbal_div` is a pure, side-effect-free helper in `output_landscape_module`; it only computes a new `output_waterbal` value from its arguments and does no I/O. It runs wherever `output_waterbal` records are averaged, chiefly along the output-accumulation path (daily → monthly → yearly → average annual).

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

No hand-authored source-lineage narrative was produced for this helper; see the Git Lineage Evidence below for the commit history of `output_landscape_module.f90`.

## Review Notes

- No direct file I/O was extracted for this procedure.
- warning: missing_doc: Procedure 'output_landscape_module::hruout_waterbal_div' has no extracted documentation comment.
- info: no_flow_steps: No major control-flow or I/O steps were extracted for this procedure.
