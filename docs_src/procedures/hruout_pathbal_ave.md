---
kind: procedure
symbol: hruout_pathbal_ave
title: hruout_pathbal_ave
status: filled
source_hash: 3c20ea8d8f3614b8
version_label: SWAT+ 62.0.0
args:
  hru1: The first `pathogen_balance` operand (intent(in)).
  const: Scalar applied to each field of the `pathogen_balance` record.
locals:
  hru2: 'Result variable: the `pathogen_balance` record the function returns, holding the
    field-by-field result.'
---

<!-- facts:header -->

Divides a `pathogen_balance` record by a scalar (`const`) field by field, defined in `output_ls_pathogen_module` and used to average accumulated `pathogen_balance` state.

## Bottom Line

`hruout_pathbal_ave` returns a new `pathogen_balance` record whose fields are its input's fields each divided by the scalar `const`. 2 of the 2 fields are divided by `const`: `plant`, `soil`.

This is one of the small arithmetic helpers `output_ls_pathogen_module` defines for the `pathogen_balance` derived type. SWAT+ output and routing code calls it to keep `pathogen_balance` records averaged — typically when rolling daily state up into monthly, yearly, and average-annual totals. It is a pure function: its arguments are `intent(in)` and it has no side effects.

## Arguments

<!-- facts:arguments -->

## Where It Fits

`hruout_pathbal_ave` is a pure, side-effect-free helper in `output_ls_pathogen_module`; it only computes a new `pathogen_balance` value from its arguments and does no I/O. It runs wherever `pathogen_balance` records are averaged, chiefly along the output-accumulation path (daily → monthly → yearly → average annual).

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

No hand-authored source-lineage narrative was produced for this helper; see the Git Lineage Evidence below for the commit history of `output_ls_pathogen_module.f90`.

## Review Notes

- No direct file I/O was extracted for this procedure.
- warning: missing_doc: Procedure 'output_ls_pathogen_module::hruout_pathbal_ave' has no extracted documentation comment.
- info: no_flow_steps: No major control-flow or I/O steps were extracted for this procedure.
