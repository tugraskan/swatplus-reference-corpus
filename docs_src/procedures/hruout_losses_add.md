---
kind: procedure
symbol: hruout_losses_add
title: hruout_losses_add
status: filled
source_hash: 6319cf046827d68a
version_label: SWAT+ 62.0.0
args:
  hru1: The first `output_losses` operand (intent(in)).
  hru2: The second `output_losses` operand (intent(in)).
locals:
  hru3: 'Result variable: the `output_losses` record the function returns, holding the field-by-field
    result.'
---

<!-- facts:header -->

Field-by-field addition of two `output_losses` records, defined in `output_landscape_module` and used to accumulate `output_losses` state.

## Bottom Line

`hruout_losses_add` returns a new `output_losses` record whose fields are the field-by-field sum of its two inputs. All 12 of the record's 12 value fields are combined with `+`.

This is one of the small arithmetic helpers `output_landscape_module` defines for the `output_losses` derived type. SWAT+ output and routing code calls it to keep `output_losses` records accumulated — typically when rolling daily state up into monthly, yearly, and average-annual totals. It is a pure function: its arguments are `intent(in)` and it has no side effects.

## Arguments

<!-- facts:arguments -->

## Where It Fits

`hruout_losses_add` is a pure, side-effect-free helper in `output_landscape_module`; it only computes a new `output_losses` value from its arguments and does no I/O. It runs wherever `output_losses` records are accumulated, chiefly along the output-accumulation path (daily → monthly → yearly → average annual).

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

No hand-authored source-lineage narrative was produced for this helper; see the Git Lineage Evidence below for the commit history of `output_landscape_module.f90`.

## Review Notes

- No direct file I/O was extracted for this procedure.
- warning: missing_doc: Procedure 'output_landscape_module::hruout_losses_add' has no extracted documentation comment.
- info: no_flow_steps: No major control-flow or I/O steps were extracted for this procedure.
