---
kind: procedure
symbol: ch_div
title: ch_div
status: filled
source_hash: 2b9c633b4f6be2c0
version_label: SWAT+ 62.0.0
args:
  ch1: The first `ch_output` operand (intent(in)).
  const: Scalar applied to each field of the `ch_output` record.
locals:
  ch2: 'Result variable: the `ch_output` record the function returns, holding the field-by-field
    result.'
---

<!-- facts:header -->

Divides a `ch_output` record by a scalar (`const`) field by field, defined in `channel_module` and used to average accumulated `ch_output` state.

## Bottom Line

`ch_div` returns a new `ch_output` record whose fields are its input's fields each divided by the scalar `const`. 58 of the 58 fields are divided by `const`: `flo_in`, `flo_out`, `evap`, `tloss`, `sed_in`, `sed_out`, `sed_conc`, `orgn_in`, `orgn_out`, `orgp_in`, `orgp_out`, `no3_in`, … (58 total).

This is one of the small arithmetic helpers `channel_module` defines for the `ch_output` derived type. SWAT+ output and routing code calls it to keep `ch_output` records averaged — typically when rolling daily state up into monthly, yearly, and average-annual totals. It is a pure function: its arguments are `intent(in)` and it has no side effects.

## Arguments

<!-- facts:arguments -->

## Where It Fits

`ch_div` is a pure, side-effect-free helper in `channel_module`; it only computes a new `ch_output` value from its arguments and does no I/O. It runs wherever `ch_output` records are averaged, chiefly along the output-accumulation path (daily → monthly → yearly → average annual).

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

No hand-authored source-lineage narrative was produced for this helper; see the Git Lineage Evidence below for the commit history of `channel_module.f90`.

## Review Notes

- No direct file I/O was extracted for this procedure.
- warning: missing_doc: Procedure 'channel_module::ch_div' has no extracted documentation comment.
- info: no_flow_steps: No major control-flow or I/O steps were extracted for this procedure.
