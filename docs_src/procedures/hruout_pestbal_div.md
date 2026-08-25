---
kind: procedure
symbol: hruout_pestbal_div
title: hruout_pestbal_div
status: filled
source_hash: c377851f4dcf89a6
version_label: SWAT+ 62.0.0
args:
  hru1: The first `pesticide_balance` operand (intent(in)).
  const: Scalar applied to each field of the `pesticide_balance` record.
locals:
  hru2: 'Result variable: the `pesticide_balance` record the function returns, holding the
    field-by-field result.'
---

<!-- facts:header -->

Divides a `pesticide_balance` record by a scalar (`const`) field by field, defined in `output_ls_pesticide_module` and used to average accumulated `pesticide_balance` state.

## Bottom Line

`hruout_pestbal_div` returns a new `pesticide_balance` record whose fields are its input's fields each divided by the scalar `const`. 13 of the 16 fields are divided by `const`: `sed`, `surq`, `latq`, `tileq`, `perc`, `apply_s`, `apply_f`, `decay_s`, `decay_f`, `wash`, `metab_s`, `metab_f`, … (13 total). The other 3 fields are copied through unchanged (not scaled); these are the flux totals that are not averaged.

This is one of the small arithmetic helpers `output_ls_pesticide_module` defines for the `pesticide_balance` derived type. SWAT+ output and routing code calls it to keep `pesticide_balance` records averaged — typically when rolling daily state up into monthly, yearly, and average-annual totals. It is a pure function: its arguments are `intent(in)` and it has no side effects.

## Arguments

<!-- facts:arguments -->

## Where It Fits

`hruout_pestbal_div` is a pure, side-effect-free helper in `output_ls_pesticide_module`; it only computes a new `pesticide_balance` value from its arguments and does no I/O. It runs wherever `pesticide_balance` records are averaged, chiefly along the output-accumulation path (daily → monthly → yearly → average annual).

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

No hand-authored source-lineage narrative was produced for this helper; see the Git Lineage Evidence below for the commit history of `output_ls_pesticide_module.f90`.

## Review Notes

- No direct file I/O was extracted for this procedure.
- warning: missing_doc: Procedure 'output_ls_pesticide_module::hruout_pestbal_div' has no extracted documentation comment.
- info: no_flow_steps: No major control-flow or I/O steps were extracted for this procedure.
