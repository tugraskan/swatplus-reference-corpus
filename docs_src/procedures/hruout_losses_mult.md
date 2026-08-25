---
kind: procedure
symbol: hruout_losses_mult
title: hruout_losses_mult
status: filled
source_hash: 6b7e43a7fe5fc821
version_label: SWAT+ 62.0.0
args:
  hru1: The first `output_losses` operand (intent(in)).
  const: Scalar applied to each field of the `output_losses` record.
locals:
  hru2: 'Result variable: the `output_losses` record the function returns, holding the field-by-field
    result.'
---

<!-- facts:header -->

Scales a `output_losses` record by a scalar (`const`) field by field, defined in `output_landscape_module`.

## Bottom Line

`hruout_losses_mult` returns a new `output_losses` record whose fields are its input's fields each multiplied by the scalar `const`. 12 of the 12 fields are multiplied by `const`: `sedyld`, `sedorgn`, `sedorgp`, `surqno3`, `latno3`, `surqsolp`, `usle`, `sedminp`, `tileno3`, `lchlabp`, `tilelabp`, `satexn`.

This is one of the small arithmetic helpers `output_landscape_module` defines for the `output_losses` derived type. SWAT+ output and routing code calls it to keep `output_losses` records scaled — typically when rolling daily state up into monthly, yearly, and average-annual totals. It is a pure function: its arguments are `intent(in)` and it has no side effects.

## Arguments

<!-- facts:arguments -->

## Where It Fits

`hruout_losses_mult` is a pure, side-effect-free helper in `output_landscape_module`; it only computes a new `output_losses` value from its arguments and does no I/O. It runs wherever `output_losses` records are scaled, chiefly along the output-accumulation path (daily → monthly → yearly → average annual).

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
- warning: missing_doc: Procedure 'output_landscape_module::hruout_losses_mult' has no extracted documentation comment.
- info: no_flow_steps: No major control-flow or I/O steps were extracted for this procedure.
