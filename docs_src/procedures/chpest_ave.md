---
kind: procedure
symbol: chpest_ave
title: chpest_ave
status: filled
source_hash: 51decac0dbc27cce
version_label: SWAT+ 62.0.0
args:
  ch1: The first `ch_pesticide_processes` operand (intent(in)).
  const: Scalar applied to each field of the `ch_pesticide_processes` record.
locals:
  ch2: 'Result variable: the `ch_pesticide_processes` record the function returns, holding
    the field-by-field result.'
---

<!-- facts:header -->

Scales a `ch_pesticide_processes` record by a scalar (`const`) field by field, defined in `ch_pesticide_module`.

## Bottom Line

`chpest_ave` returns a new `ch_pesticide_processes` record whose fields are its input's fields each multiplied by the scalar `const`. 14 of the 14 fields are multiplied by `const`: `tot_in`, `sol_out`, `sor_out`, `react`, `metab`, `volat`, `settle`, `resus`, `difus`, `react_bot`, `metab_bot`, `bury`, … (14 total).

This is one of the small arithmetic helpers `ch_pesticide_module` defines for the `ch_pesticide_processes` derived type. SWAT+ output and routing code calls it to keep `ch_pesticide_processes` records scaled — typically when rolling daily state up into monthly, yearly, and average-annual totals. It is a pure function: its arguments are `intent(in)` and it has no side effects.

## Arguments

<!-- facts:arguments -->

## Where It Fits

`chpest_ave` is a pure, side-effect-free helper in `ch_pesticide_module`; it only computes a new `ch_pesticide_processes` value from its arguments and does no I/O. It runs wherever `ch_pesticide_processes` records are scaled, chiefly along the output-accumulation path (daily → monthly → yearly → average annual).

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

No hand-authored source-lineage narrative was produced for this helper; see the Git Lineage Evidence below for the commit history of `ch_pesticide_module.f90`.

## Review Notes

- No direct file I/O was extracted for this procedure.
- warning: missing_doc: Procedure 'ch_pesticide_module::chpest_ave' has no extracted documentation comment.
- info: no_flow_steps: No major control-flow or I/O steps were extracted for this procedure.
