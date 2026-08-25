---
kind: procedure
symbol: carbon_residue_gl_div
title: carbon_residue_gl_div
status: filled
source_hash: a384b148b9ef63f2
version_label: SWAT+ 62.0.0
args:
  const: Scalar applied to each field of the `carbon_residue_gain_losses` record.
  hru1: The first `carbon_residue_gain_losses` operand (intent(in)).
locals:
  hru2: 'Result variable: the `carbon_residue_gain_losses` record the function returns, holding
    the field-by-field result.'
---

<!-- facts:header -->

Divides a `carbon_residue_gain_losses` record by a scalar (`const`) field by field, defined in `carbon_module` and used to average accumulated `carbon_residue_gain_losses` state.

## Bottom Line

`carbon_residue_gl_div` returns a new `carbon_residue_gain_losses` record whose fields are its input's fields each divided by the scalar `const`. 6 of the 6 fields are divided by `const`: `plant_surf_c`, `plant_surf_c`, `rsd_surfdecay_c`, `rsd_rootdecay_c`, `harv_stov_c`, `emit_c`.

This is one of the small arithmetic helpers `carbon_module` defines for the `carbon_residue_gain_losses` derived type. SWAT+ output and routing code calls it to keep `carbon_residue_gain_losses` records averaged — typically when rolling daily state up into monthly, yearly, and average-annual totals. It is a pure function: its arguments are `intent(in)` and it has no side effects.

## Arguments

<!-- facts:arguments -->

## Where It Fits

`carbon_residue_gl_div` is a pure, side-effect-free helper in `carbon_module`; it only computes a new `carbon_residue_gain_losses` value from its arguments and does no I/O. It runs wherever `carbon_residue_gain_losses` records are averaged, chiefly along the output-accumulation path (daily → monthly → yearly → average annual).

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
- warning: missing_doc: Procedure 'carbon_module::carbon_residue_gl_div' has no extracted documentation comment.
- info: no_flow_steps: No major control-flow or I/O steps were extracted for this procedure.
