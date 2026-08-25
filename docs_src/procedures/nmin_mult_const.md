---
kind: procedure
symbol: nmin_mult_const
title: nmin_mult_const
status: filled
source_hash: c0f11dd0c6bd51fc
version_label: SWAT+ 62.0.0
args:
  const: Scalar applied to each field of the `mineral_nitrogen` record.
  nmin_m1: The first `mineral_nitrogen` operand (intent(in)).
locals:
  nmin_m2: 'Result variable: the `mineral_nitrogen` record the function returns, holding the
    field-by-field result.'
---

<!-- facts:header -->

Scales a `mineral_nitrogen` record by a scalar (`const`) field by field, defined in `organic_mineral_mass_module`.

## Bottom Line

`nmin_mult_const` returns a new `mineral_nitrogen` record whose fields are its input's fields each multiplied by the scalar `const`. 2 of the 2 fields are multiplied by `const`: `no3`, `nh4`.

This is one of the small arithmetic helpers `organic_mineral_mass_module` defines for the `mineral_nitrogen` derived type. SWAT+ output and routing code calls it to keep `mineral_nitrogen` records scaled — typically when rolling daily state up into monthly, yearly, and average-annual totals. It is a pure function: its arguments are `intent(in)` and it has no side effects.

## Arguments

<!-- facts:arguments -->

## Where It Fits

`nmin_mult_const` is a pure, side-effect-free helper in `organic_mineral_mass_module`; it only computes a new `mineral_nitrogen` value from its arguments and does no I/O. It runs wherever `mineral_nitrogen` records are scaled, chiefly along the output-accumulation path (daily → monthly → yearly → average annual).

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
- info: weak_doc: Procedure 'organic_mineral_mass_module::nmin_mult_const' documentation is very short.
- info: no_flow_steps: No major control-flow or I/O steps were extracted for this procedure.
