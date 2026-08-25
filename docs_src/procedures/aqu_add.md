---
kind: procedure
symbol: aqu_add
title: aqu_add
status: filled
source_hash: c6ce37ab164bb454
version_label: SWAT+ 62.0.0
args:
  aqo1: The first `aquifer_dynamic` operand (intent(in)).
  aqo2: The second `aquifer_dynamic` operand (intent(in)).
locals:
  aqo3: 'Result variable: the `aquifer_dynamic` record the function returns, holding the field-by-field
    result.'
---

<!-- facts:header -->

Field-by-field addition of two `aquifer_dynamic` records, defined in `aquifer_module` and used to accumulate `aquifer_dynamic` state.

## Bottom Line

`aqu_add` returns a new `aquifer_dynamic` record whose fields are the field-by-field sum of its two inputs. All 16 of the record's 17 value fields are combined with `+`. 1 field is carried through unchanged rather than combined: `cbn`.

This is one of the small arithmetic helpers `aquifer_module` defines for the `aquifer_dynamic` derived type. SWAT+ output and routing code calls it to keep `aquifer_dynamic` records accumulated — typically when rolling daily state up into monthly, yearly, and average-annual totals. It is a pure function: its arguments are `intent(in)` and it has no side effects.

## Arguments

<!-- facts:arguments -->

## Where It Fits

`aqu_add` is a pure, side-effect-free helper in `aquifer_module`; it only computes a new `aquifer_dynamic` value from its arguments and does no I/O. It runs wherever `aquifer_dynamic` records are accumulated, chiefly along the output-accumulation path (daily → monthly → yearly → average annual).

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
- warning: missing_doc: Procedure 'aquifer_module::aqu_add' has no extracted documentation comment.
- info: no_flow_steps: No major control-flow or I/O steps were extracted for this procedure.
