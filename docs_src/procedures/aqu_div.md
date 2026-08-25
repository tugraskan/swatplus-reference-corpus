---
kind: procedure
symbol: aqu_div
title: aqu_div
status: filled
source_hash: d8fdcb222001bb47
version_label: SWAT+ 62.0.0
args:
  aq1: The first `aquifer_dynamic` operand (intent(in)).
  const: Scalar applied to each field of the `aquifer_dynamic` record.
locals:
  aq2: 'Result variable: the `aquifer_dynamic` record the function returns, holding the field-by-field
    result.'
---

<!-- facts:header -->

Divides a `aquifer_dynamic` record by a scalar (`const`) field by field, defined in `aquifer_module` and used to average accumulated `aquifer_dynamic` state.

## Bottom Line

`aqu_div` returns a new `aquifer_dynamic` record whose fields are its input's fields each divided by the scalar `const`. 16 of the 17 fields are divided by `const`: `flo`, `dep_wt`, `stor`, `no3_st`, `minp`, `orgn`, `rchrg`, `no3_rchg`, `no3_loss`, `seep`, `revap`, `no3_lat`, … (16 total). The other 1 field is copied through unchanged (not scaled); these are the flux totals that are not averaged.

This is one of the small arithmetic helpers `aquifer_module` defines for the `aquifer_dynamic` derived type. SWAT+ output and routing code calls it to keep `aquifer_dynamic` records averaged — typically when rolling daily state up into monthly, yearly, and average-annual totals. It is a pure function: its arguments are `intent(in)` and it has no side effects.

## Arguments

<!-- facts:arguments -->

## Where It Fits

`aqu_div` is a pure, side-effect-free helper in `aquifer_module`; it only computes a new `aquifer_dynamic` value from its arguments and does no I/O. It runs wherever `aquifer_dynamic` records are averaged, chiefly along the output-accumulation path (daily → monthly → yearly → average annual).

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

No hand-authored source-lineage narrative was produced for this helper; see the Git Lineage Evidence below for the commit history of `aquifer_module.f90`.

## Review Notes

- No direct file I/O was extracted for this procedure.
- warning: missing_doc: Procedure 'aquifer_module::aqu_div' has no extracted documentation comment.
- info: no_flow_steps: No major control-flow or I/O steps were extracted for this procedure.
