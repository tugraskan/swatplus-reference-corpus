---
kind: procedure
symbol: respest_div
title: respest_div
status: filled
source_hash: 01ff64a198b36cf2
version_label: SWAT+ 62.0.0
args:
  res1: The first `res_pesticide_processes` operand (intent(in)).
  const: Scalar applied to each field of the `res_pesticide_processes` record.
locals:
  res2: 'Result variable: the `res_pesticide_processes` record the function returns, holding
    the field-by-field result.'
---

<!-- facts:header -->

Divides a `res_pesticide_processes` record by a scalar (`const`) field by field, defined in `res_pesticide_module` and used to average accumulated `res_pesticide_processes` state.

## Bottom Line

`respest_div` returns a new `res_pesticide_processes` record whose fields are its input's fields each divided by the scalar `const`. 14 of the 14 fields are divided by `const`: `tot_in`, `sol_out`, `sor_out`, `react`, `metab`, `volat`, `settle`, `resus`, `difus`, `react_bot`, `metab_bot`, `bury`, … (14 total).

This is one of the small arithmetic helpers `res_pesticide_module` defines for the `res_pesticide_processes` derived type. SWAT+ output and routing code calls it to keep `res_pesticide_processes` records averaged — typically when rolling daily state up into monthly, yearly, and average-annual totals. It is a pure function: its arguments are `intent(in)` and it has no side effects.

## Arguments

<!-- facts:arguments -->

## Where It Fits

`respest_div` is a pure, side-effect-free helper in `res_pesticide_module`; it only computes a new `res_pesticide_processes` value from its arguments and does no I/O. It runs wherever `res_pesticide_processes` records are averaged, chiefly along the output-accumulation path (daily → monthly → yearly → average annual).

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
- warning: missing_doc: Procedure 'res_pesticide_module::respest_div' has no extracted documentation comment.
- info: no_flow_steps: No major control-flow or I/O steps were extracted for this procedure.
