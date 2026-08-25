---
kind: procedure
symbol: watbod_add
title: watbod_add
status: filled
source_hash: 38735d64b8c642a9
version_label: SWAT+ 62.0.0
args:
  wbod1: The first `water_body` operand (intent(in)).
  wbod2: The second `water_body` operand (intent(in)).
locals:
  wbod3: 'Result variable: the `water_body` record the function returns, holding the field-by-field
    result.'
---

<!-- facts:header -->

Field-by-field addition of two `water_body` records, defined in `water_body_module` and used to accumulate `water_body` state.

## Bottom Line

`watbod_add` returns a new `water_body` record whose fields are the field-by-field sum of its two inputs. All 4 of the record's 4 value fields are combined with `+`.

This is one of the small arithmetic helpers `water_body_module` defines for the `water_body` derived type. SWAT+ output and routing code calls it to keep `water_body` records accumulated — typically when rolling daily state up into monthly, yearly, and average-annual totals. It is a pure function: its arguments are `intent(in)` and it has no side effects.

## Arguments

<!-- facts:arguments -->

## Where It Fits

`watbod_add` is a pure, side-effect-free helper in `water_body_module`; it only computes a new `water_body` value from its arguments and does no I/O. It runs wherever `water_body` records are accumulated, chiefly along the output-accumulation path (daily → monthly → yearly → average annual).

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

No hand-authored source-lineage narrative was produced for this helper; see the Git Lineage Evidence below for the commit history of `water_body_module.f90`.

## Review Notes

- No direct file I/O was extracted for this procedure.
- info: weak_doc: Procedure 'water_body_module::watbod_add' documentation is very short.
- info: no_flow_steps: No major control-flow or I/O steps were extracted for this procedure.
