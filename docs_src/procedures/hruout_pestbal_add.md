---
kind: procedure
symbol: hruout_pestbal_add
title: hruout_pestbal_add
status: filled
source_hash: 0687085ec37f8b9c
version_label: SWAT+ 62.0.0
args:
  hru1: The first `pesticide_balance` operand (intent(in)).
  hru2: The second `pesticide_balance` operand (intent(in)).
locals:
  hru3: 'Result variable: the `pesticide_balance` record the function returns, holding the
    field-by-field result.'
---

<!-- facts:header -->

Field-by-field addition of two `pesticide_balance` records, defined in `output_ls_pesticide_module` and used to accumulate `pesticide_balance` state.

## Bottom Line

`hruout_pestbal_add` returns a new `pesticide_balance` record whose fields are the field-by-field sum of its two inputs. All 16 of the record's 16 value fields are combined with `+`.

This is one of the small arithmetic helpers `output_ls_pesticide_module` defines for the `pesticide_balance` derived type. SWAT+ output and routing code calls it to keep `pesticide_balance` records accumulated — typically when rolling daily state up into monthly, yearly, and average-annual totals. It is a pure function: its arguments are `intent(in)` and it has no side effects.

## Arguments

<!-- facts:arguments -->

## Where It Fits

`hruout_pestbal_add` is a pure, side-effect-free helper in `output_ls_pesticide_module`; it only computes a new `pesticide_balance` value from its arguments and does no I/O. It runs wherever `pesticide_balance` records are accumulated, chiefly along the output-accumulation path (daily → monthly → yearly → average annual).

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

No hand-authored source-lineage narrative was produced for this helper; see the Git Lineage Evidence below for the commit history of `output_ls_pesticide_module.f90`.

## Review Notes

- No direct file I/O was extracted for this procedure.
- warning: missing_doc: Procedure 'output_ls_pesticide_module::hruout_pestbal_add' has no extracted documentation comment.
- info: no_flow_steps: No major control-flow or I/O steps were extracted for this procedure.
