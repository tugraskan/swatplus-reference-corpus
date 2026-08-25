---
kind: procedure
symbol: hruout_plantweather_ave
title: hruout_plantweather_ave
status: filled
source_hash: 9f8e5716cb656c7f
version_label: SWAT+ 62.0.0
args:
  hru1: The first `output_plantweather` operand (intent(in)).
  const: Scalar applied to each field of the `output_plantweather` record.
locals:
  hru2: 'Result variable: the `output_plantweather` record the function returns, holding the
    field-by-field result.'
---

<!-- facts:header -->

Divides a `output_plantweather` record by a scalar (`const`) field by field, defined in `output_landscape_module` and used to average accumulated `output_plantweather` state.

## Bottom Line

`hruout_plantweather_ave` returns a new `output_plantweather` record whose fields are its input's fields each divided by the scalar `const`. 17 of the 25 fields are divided by `const`: `lai`, `bioms`, `residue`, `sol_tmp`, `nplnt`, `pplnt`, `tmx`, `tmn`, `tmpav`, `wndspd`, `rhum`, `solrad`, … (17 total). The other 8 fields are copied through unchanged (not scaled); these are the flux totals that are not averaged.

This is one of the small arithmetic helpers `output_landscape_module` defines for the `output_plantweather` derived type. SWAT+ output and routing code calls it to keep `output_plantweather` records averaged — typically when rolling daily state up into monthly, yearly, and average-annual totals. It is a pure function: its arguments are `intent(in)` and it has no side effects.

## Arguments

<!-- facts:arguments -->

## Where It Fits

`hruout_plantweather_ave` is a pure, side-effect-free helper in `output_landscape_module`; it only computes a new `output_plantweather` value from its arguments and does no I/O. It runs wherever `output_plantweather` records are averaged, chiefly along the output-accumulation path (daily → monthly → yearly → average annual).

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
- warning: missing_doc: Procedure 'output_landscape_module::hruout_plantweather_ave' has no extracted documentation comment.
- info: no_flow_steps: No major control-flow or I/O steps were extracted for this procedure.
