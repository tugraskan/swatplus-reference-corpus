---
kind: procedure
symbol: hruout_saltbal_add
title: hruout_saltbal_add
status: filled
source_hash: 0f80bdfb07caf888
version_label: SWAT+ 62.0.0
args:
  hru1: The first `salt_balance` operand (intent(in)).
  hru2: The second `salt_balance` operand (intent(in)).
locals:
  hru3: 'Result variable: the `salt_balance` record the function returns, holding the field-by-field
    result.'
---

<!-- facts:header -->

Field-by-field addition of two `salt_balance` records, defined in `output_ls_salt_module` and used to accumulate `salt_balance` state.

## Bottom Line

`hruout_saltbal_add` returns a new `salt_balance` record whose fields are the field-by-field sum of its two inputs. All 7 of the record's 7 value fields are combined with `+`.

This is one of the small arithmetic helpers `output_ls_salt_module` defines for the `salt_balance` derived type. SWAT+ output and routing code calls it to keep `salt_balance` records accumulated — typically when rolling daily state up into monthly, yearly, and average-annual totals. It is a pure function: its arguments are `intent(in)` and it has no side effects.

## Arguments

<!-- facts:arguments -->

## Where It Fits

`hruout_saltbal_add` is a pure, side-effect-free helper in `output_ls_salt_module`; it only computes a new `salt_balance` value from its arguments and does no I/O. It runs wherever `salt_balance` records are accumulated, chiefly along the output-accumulation path (daily → monthly → yearly → average annual).

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

No hand-authored source-lineage narrative was produced for this helper; see the Git Lineage Evidence below for the commit history of `output_ls_salt_module.f90`.

## Review Notes

- No direct file I/O was extracted for this procedure.
- warning: missing_doc: Procedure 'output_ls_salt_module::hruout_saltbal_add' has no extracted documentation comment.
- info: no_flow_steps: No major control-flow or I/O steps were extracted for this procedure.
