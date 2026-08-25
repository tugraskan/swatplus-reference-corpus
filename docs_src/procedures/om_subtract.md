---
kind: procedure
symbol: om_subtract
title: om_subtract
status: filled
source_hash: 1423c4e88011eba3
version_label: SWAT+ 62.0.0
args:
  o_m1: The first `organic_mass` operand (intent(in)).
  o_m2: The second `organic_mass` operand (intent(in)).
locals:
  o_m3: 'Result variable: the `organic_mass` record the function returns, holding the field-by-field
    result.'
---

<!-- facts:header -->

Field-by-field subtraction of two `organic_mass` records, defined in `organic_mineral_mass_module`.

## Bottom Line

`om_subtract` returns a new `organic_mass` record whose fields are the field-by-field difference of its two inputs. All 4 of the record's 4 value fields are combined with `-`.

This is one of the small arithmetic helpers `organic_mineral_mass_module` defines for the `organic_mass` derived type. SWAT+ output and routing code calls it to keep `organic_mass` records differenced — typically when rolling daily state up into monthly, yearly, and average-annual totals. It is a pure function: its arguments are `intent(in)` and it has no side effects.

## Arguments

<!-- facts:arguments -->

## Where It Fits

`om_subtract` is a pure, side-effect-free helper in `organic_mineral_mass_module`; it only computes a new `organic_mass` value from its arguments and does no I/O. It runs wherever `organic_mass` records are differenced, chiefly along the output-accumulation path (daily → monthly → yearly → average annual).

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
- info: weak_doc: Procedure 'organic_mineral_mass_module::om_subtract' documentation is very short.
- info: no_flow_steps: No major control-flow or I/O steps were extracted for this procedure.
