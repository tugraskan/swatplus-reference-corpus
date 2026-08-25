---
kind: procedure
symbol: chsednut_add
title: chsednut_add
status: filled
source_hash: 6b78103541f6a10a
version_label: SWAT+ 62.0.0
args:
  cho1: The first `channel_sediment_budget_output` operand (intent(in)).
  cho2: The second `channel_sediment_budget_output` operand (intent(in)).
locals:
  cho3: 'Result variable: the `channel_sediment_budget_output` record the function returns,
    holding the field-by-field result.'
---

<!-- facts:header -->

Field-by-field addition of two `channel_sediment_budget_output` records, defined in `sd_channel_module` and used to accumulate `channel_sediment_budget_output` state.

## Bottom Line

`chsednut_add` returns a new `channel_sediment_budget_output` record whose fields are the field-by-field sum of its two inputs. All 30 of the record's 30 value fields are combined with `+`.

This is one of the small arithmetic helpers `sd_channel_module` defines for the `channel_sediment_budget_output` derived type. SWAT+ output and routing code calls it to keep `channel_sediment_budget_output` records accumulated — typically when rolling daily state up into monthly, yearly, and average-annual totals. It is a pure function: its arguments are `intent(in)` and it has no side effects.

## Arguments

<!-- facts:arguments -->

## Where It Fits

`chsednut_add` is a pure, side-effect-free helper in `sd_channel_module`; it only computes a new `channel_sediment_budget_output` value from its arguments and does no I/O. It runs wherever `channel_sediment_budget_output` records are accumulated, chiefly along the output-accumulation path (daily → monthly → yearly → average annual).

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

No hand-authored source-lineage narrative was produced for this helper; see the Git Lineage Evidence below for the commit history of `sd_channel_module.f90`.

## Review Notes

- No direct file I/O was extracted for this procedure.
- warning: missing_doc: Procedure 'sd_channel_module::chsednut_add' has no extracted documentation comment.
- info: no_flow_steps: No major control-flow or I/O steps were extracted for this procedure.
