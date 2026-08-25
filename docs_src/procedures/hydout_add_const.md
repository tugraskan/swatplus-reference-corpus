---
kind: procedure
symbol: hydout_add_const
title: hydout_add_const
status: filled
source_hash: 55e67397b4a7e67c
version_label: SWAT+ 62.0.0
args:
  const: Scalar applied to each field of the `hyd_output` record.
  hyd1: The first `hyd_output` operand (intent(in)).
locals:
  hyd2: 'Result variable: the `hyd_output` record the function returns, holding the field-by-field
    result.'
---

<!-- facts:header -->

Field-by-field addition of two `hyd_output` records, defined in `hydrograph_module` and used to accumulate `hyd_output` state.

## Bottom Line

`hydout_add_const` returns a new `hyd_output` record whose fields are the field-by-field sum of its two inputs. All 17 of the record's 18 value fields are combined with `+`. 1 field is carried through unchanged rather than combined: `temp`.

This is one of the small arithmetic helpers `hydrograph_module` defines for the `hyd_output` derived type. SWAT+ output and routing code calls it to keep `hyd_output` records accumulated — typically when rolling daily state up into monthly, yearly, and average-annual totals. It is a pure function: its arguments are `intent(in)` and it has no side effects.

## Arguments

<!-- facts:arguments -->

## Where It Fits

`hydout_add_const` is a pure, side-effect-free helper in `hydrograph_module`; it only computes a new `hyd_output` value from its arguments and does no I/O. It runs wherever `hyd_output` records are accumulated, chiefly along the output-accumulation path (daily → monthly → yearly → average annual).

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

No hand-authored source-lineage narrative was produced for this helper; see the Git Lineage Evidence below for the commit history of `hydrograph_module.f90`.

## Review Notes

- No direct file I/O was extracted for this procedure.
- info: weak_doc: Procedure 'hydrograph_module::hydout_add_const' documentation is very short.
- info: no_flow_steps: No major control-flow or I/O steps were extracted for this procedure.
