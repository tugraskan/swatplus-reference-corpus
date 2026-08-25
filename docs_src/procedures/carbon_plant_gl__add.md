---
kind: procedure
symbol: carbon_plant_gl__add
title: carbon_plant_gl__add
status: filled
source_hash: c252eae4721066e3
version_label: SWAT+ 62.0.0
args:
  hru1: The first `carbon_plant_gain_losses` operand (intent(in)).
  hru2: The second `carbon_plant_gain_losses` operand (intent(in)).
locals:
  hru3: 'Result variable: the `carbon_plant_gain_losses` record the function returns, holding
    the field-by-field result.'
---

<!-- facts:header -->

Field-by-field addition of two `carbon_plant_gain_losses` records, defined in `carbon_module` and used to accumulate `carbon_plant_gain_losses` state.

## Bottom Line

`carbon_plant_gl__add` returns a new `carbon_plant_gain_losses` record whose fields are the field-by-field sum of its two inputs. All 6 of the record's 6 value fields are combined with `+`.

This is one of the small arithmetic helpers `carbon_module` defines for the `carbon_plant_gain_losses` derived type. SWAT+ output and routing code calls it to keep `carbon_plant_gain_losses` records accumulated — typically when rolling daily state up into monthly, yearly, and average-annual totals. It is a pure function: its arguments are `intent(in)` and it has no side effects.

## Arguments

<!-- facts:arguments -->

## Where It Fits

`carbon_plant_gl__add` is a pure, side-effect-free helper in `carbon_module`; it only computes a new `carbon_plant_gain_losses` value from its arguments and does no I/O. It runs wherever `carbon_plant_gain_losses` records are accumulated, chiefly along the output-accumulation path (daily → monthly → yearly → average annual).

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

No hand-authored source-lineage narrative was produced for this helper; see the Git Lineage Evidence below for the commit history of `carbon_module.f90`.

## Review Notes

- No direct file I/O was extracted for this procedure.
- warning: missing_doc: Procedure 'carbon_module::carbon_plant_gl__add' has no extracted documentation comment.
- info: no_flow_steps: No major control-flow or I/O steps were extracted for this procedure.
