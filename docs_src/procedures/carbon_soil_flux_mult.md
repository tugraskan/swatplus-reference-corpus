---
kind: procedure
symbol: carbon_soil_flux_mult
title: carbon_soil_flux_mult
status: filled
source_hash: f7924ca1bf22506e
version_label: SWAT+ 62.0.0
args:
  hru1: The first `carbon_soil_transformations` operand (intent(in)).
  const: Scalar applied to each field of the `carbon_soil_transformations` record.
locals:
  hru2: 'Result variable: the `carbon_soil_transformations` record the function returns, holding
    the field-by-field result.'
---

<!-- facts:header -->

Scales a `carbon_soil_transformations` record by a scalar (`const`) field by field, defined in `carbon_module`.

## Bottom Line

`carbon_soil_flux_mult` returns a new `carbon_soil_transformations` record whose fields are its input's fields each multiplied by the scalar `const`. 13 of the 13 fields are multiplied by `const`: `meta_micr`, `str_micr`, `str_hs`, `co2_meta`, `co2_str`, `micr_hs`, `micr_hp`, `hs_micr`, `hs_hp`, `hp_micr`, `co2_micr`, `co2_hs`, … (13 total).

This is one of the small arithmetic helpers `carbon_module` defines for the `carbon_soil_transformations` derived type. SWAT+ output and routing code calls it to keep `carbon_soil_transformations` records scaled — typically when rolling daily state up into monthly, yearly, and average-annual totals. It is a pure function: its arguments are `intent(in)` and it has no side effects.

## Arguments

<!-- facts:arguments -->

## Where It Fits

`carbon_soil_flux_mult` is a pure, side-effect-free helper in `carbon_module`; it only computes a new `carbon_soil_transformations` value from its arguments and does no I/O. It runs wherever `carbon_soil_transformations` records are scaled, chiefly along the output-accumulation path (daily → monthly → yearly → average annual).

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
- warning: missing_doc: Procedure 'carbon_module::carbon_soil_flux_mult' has no extracted documentation comment.
- info: no_flow_steps: No major control-flow or I/O steps were extracted for this procedure.
