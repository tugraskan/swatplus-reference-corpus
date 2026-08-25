---
kind: procedure
symbol: wallout_add
title: wallout_add
status: filled
source_hash: b52af96fc8f82516
version_label: SWAT+ 62.0.0
args:
  wallo1: The first `source_output` operand (intent(in)).
  wallo2: The second `source_output` operand (intent(in)).
locals:
  wallo3: 'Result variable: the `source_output` record the function returns, holding the field-by-field
    result.'
---

<!-- facts:header -->

Field-by-field addition of two `source_output` records, defined in `water_allocation_module` and used to accumulate `source_output` state.

## Bottom Line

`wallout_add` returns a new `source_output` record whose fields are the field-by-field sum of its two inputs. All 3 of the record's 3 value fields are combined with `+`.

This is one of the small arithmetic helpers `water_allocation_module` defines for the `source_output` derived type. SWAT+ output and routing code calls it to keep `source_output` records accumulated — typically when rolling daily state up into monthly, yearly, and average-annual totals. It is a pure function: its arguments are `intent(in)` and it has no side effects.

## Arguments

<!-- facts:arguments -->

## Where It Fits

`wallout_add` is a pure, side-effect-free helper in `water_allocation_module`; it only computes a new `source_output` value from its arguments and does no I/O. It runs wherever `source_output` records are accumulated, chiefly along the output-accumulation path (daily → monthly → yearly → average annual).

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

No hand-authored source-lineage narrative was produced for this helper; see the Git Lineage Evidence below for the commit history of `water_allocation_module.f90`.

## Review Notes

- No direct file I/O was extracted for this procedure.
- info: weak_doc: Procedure 'water_allocation_module::wallout_add' documentation is very short.
- info: no_flow_steps: No major control-flow or I/O steps were extracted for this procedure.
