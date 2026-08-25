---
kind: procedure
symbol: org_flux_add1
title: org_flux_add1
status: filled
source_hash: f89f63eb6765c7af
version_label: SWAT+ 62.0.0
args:
  org_flux1: The first `organic_flux` operand (intent(in)).
  org_flux2: The second `organic_flux` operand (intent(in)).
locals:
  org_flux3: 'Result variable: the `organic_flux` record the function returns, holding the
    field-by-field result.'
---

<!-- facts:header -->

Field-by-field addition of two `organic_flux` records, defined in `organic_mineral_mass_module` and used to accumulate `organic_flux` state.

## Bottom Line

`org_flux_add1` returns a new `organic_flux` record whose fields are the field-by-field sum of its two inputs. All 37 of the record's 37 value fields are combined with `+`.

This is one of the small arithmetic helpers `organic_mineral_mass_module` defines for the `organic_flux` derived type. SWAT+ output and routing code calls it to keep `organic_flux` records accumulated — typically when rolling daily state up into monthly, yearly, and average-annual totals. It is a pure function: its arguments are `intent(in)` and it has no side effects.

## Arguments

<!-- facts:arguments -->

## Where It Fits

`org_flux_add1` is a pure, side-effect-free helper in `organic_mineral_mass_module`; it only computes a new `organic_flux` value from its arguments and does no I/O. It runs wherever `organic_flux` records are accumulated, chiefly along the output-accumulation path (daily → monthly → yearly → average annual).

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
- info: weak_doc: Procedure 'organic_mineral_mass_module::org_flux_add1' documentation is very short.
- info: no_flow_steps: No major control-flow or I/O steps were extracted for this procedure.
