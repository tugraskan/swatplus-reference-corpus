---
kind: procedure
symbol: pmin_add
title: pmin_add
status: filled
source_hash: b72275fcdd65eb96
version_label: SWAT+ 62.0.0
args:
  pmin_m1: The first `mineral_phosphorus` operand (intent(in)).
  pmin_m2: The second `mineral_phosphorus` operand (intent(in)).
locals:
  pmin_m3: 'Result variable: the `mineral_phosphorus` record the function returns, holding
    the field-by-field result.'
---

<!-- facts:header -->

Field-by-field addition of two `mineral_phosphorus` records, defined in `organic_mineral_mass_module` and used to accumulate `mineral_phosphorus` state.

## Bottom Line

`pmin_add` returns a new `mineral_phosphorus` record whose fields are the field-by-field sum of its two inputs. All 4 of the record's 4 value fields are combined with `+`.

This is one of the small arithmetic helpers `organic_mineral_mass_module` defines for the `mineral_phosphorus` derived type. SWAT+ output and routing code calls it to keep `mineral_phosphorus` records accumulated — typically when rolling daily state up into monthly, yearly, and average-annual totals. It is a pure function: its arguments are `intent(in)` and it has no side effects.

## Arguments

<!-- facts:arguments -->

## Where It Fits

`pmin_add` is a pure, side-effect-free helper in `organic_mineral_mass_module`; it only computes a new `mineral_phosphorus` value from its arguments and does no I/O. It runs wherever `mineral_phosphorus` records are accumulated, chiefly along the output-accumulation path (daily → monthly → yearly → average annual).

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

No hand-authored source-lineage narrative was produced for this helper; see the Git Lineage Evidence below for the commit history of `organic_mineral_mass_module.f90`.

## Review Notes

- No direct file I/O was extracted for this procedure.
- warning: missing_doc: Procedure 'organic_mineral_mass_module::pmin_add' has no extracted documentation comment.
- info: no_flow_steps: No major control-flow or I/O steps were extracted for this procedure.
