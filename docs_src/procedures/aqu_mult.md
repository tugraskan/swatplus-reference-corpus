---
kind: procedure
symbol: aqu_mult
title: aqu_mult
status: filled
source_hash: 98b1f930b83e76aa
version_label: SWAT+ 62.0.0
args:
  aq1: The first `aquifer_dynamic` operand (intent(in)).
  const: Scalar applied to each field of the `aquifer_dynamic` record.
locals:
  aq2: 'Result variable: the `aquifer_dynamic` record the function returns, holding the field-by-field
    result.'
---

<!-- facts:header -->

Scales a `aquifer_dynamic` record by a scalar (`const`) field by field, defined in `aquifer_module`.

## Bottom Line

`aqu_mult` returns a new `aquifer_dynamic` record whose fields are its input's fields each multiplied by the scalar `const`. 16 of the 17 fields are multiplied by `const`: `flo`, `dep_wt`, `stor`, `no3_st`, `minp`, `orgn`, `rchrg`, `no3_rchg`, `no3_loss`, `seep`, `revap`, `no3_lat`, … (16 total). The other 1 field is copied through unchanged (not scaled).

This is one of the small arithmetic helpers `aquifer_module` defines for the `aquifer_dynamic` derived type. SWAT+ output and routing code calls it to keep `aquifer_dynamic` records scaled — typically when rolling daily state up into monthly, yearly, and average-annual totals. It is a pure function: its arguments are `intent(in)` and it has no side effects.

## Arguments

<!-- facts:arguments -->

## Where It Fits

`aqu_mult` is a pure, side-effect-free helper in `aquifer_module`; it only computes a new `aquifer_dynamic` value from its arguments and does no I/O. It runs wherever `aquifer_dynamic` records are scaled, chiefly along the output-accumulation path (daily → monthly → yearly → average annual).

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
- warning: missing_doc: Procedure 'aquifer_module::aqu_mult' has no extracted documentation comment.
- info: no_flow_steps: No major control-flow or I/O steps were extracted for this procedure.
