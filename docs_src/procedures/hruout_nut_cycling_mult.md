---
kind: procedure
symbol: hruout_nut_cycling_mult
title: hruout_nut_cycling_mult
status: filled
source_hash: 4fc18bae32458f97
version_label: SWAT+ 62.0.0
args:
  hru1: The first `output_nutcarb_cycling` operand (intent(in)).
  const: Scalar applied to each field of the `output_nutcarb_cycling` record.
locals:
  hru2: 'Result variable: the `output_nutcarb_cycling` record the function returns, holding
    the field-by-field result.'
---

<!-- facts:header -->

Scales a `output_nutcarb_cycling` record by a scalar (`const`) field by field, defined in `output_landscape_module`.

## Bottom Line

`hruout_nut_cycling_mult` returns a new `output_nutcarb_cycling` record whose fields are its input's fields each multiplied by the scalar `const`. 8 of the 8 fields are multiplied by `const`: `lab_min_p`, `act_sta_p`, `act_nit_n`, `act_sta_n`, `org_lab_p`, `rsd_hs_c`, `rsd_nitorg_n`, `rsd_laborg_p`.

This is one of the small arithmetic helpers `output_landscape_module` defines for the `output_nutcarb_cycling` derived type. SWAT+ output and routing code calls it to keep `output_nutcarb_cycling` records scaled — typically when rolling daily state up into monthly, yearly, and average-annual totals. It is a pure function: its arguments are `intent(in)` and it has no side effects.

## Arguments

<!-- facts:arguments -->

## Where It Fits

`hruout_nut_cycling_mult` is a pure, side-effect-free helper in `output_landscape_module`; it only computes a new `output_nutcarb_cycling` value from its arguments and does no I/O. It runs wherever `output_nutcarb_cycling` records are scaled, chiefly along the output-accumulation path (daily → monthly → yearly → average annual).

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
- warning: missing_doc: Procedure 'output_landscape_module::hruout_nut_cycling_mult' has no extracted documentation comment.
- info: no_flow_steps: No major control-flow or I/O steps were extracted for this procedure.
