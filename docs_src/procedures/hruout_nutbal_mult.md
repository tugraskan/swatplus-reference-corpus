---
kind: procedure
symbol: hruout_nutbal_mult
title: hruout_nutbal_mult
status: filled
source_hash: f24e086ed1e09cb1
version_label: SWAT+ 62.0.0
args:
  hru1: '`in` argument of type `type(output_nutbal)`.'
  const: '`in` argument of type `real`.'
locals:
  hru2: 'Result variable: the `type(output_nutbal)` value the function returns.'
---

<!-- facts:header -->

Scales an `output_nutbal` nutrient-balance record by a scalar constant field by field, with underflow guards on the residue organic N and P fields.

## Bottom Line

`hruout_nutbal_mult` multiplies each field of an `output_nutbal` record by the scalar `const`. Two fields are guarded: `rsd_nitorg_n` and `rsd_laborg_p` are set to 0 when their input is below 1e-10 (to prevent a gfortran underflow) and otherwise scaled like the rest.

It is the scale-by-constant helper for `output_nutbal`, used when averaging or fractioning accumulated HRU nutrient-balance output.

## Arguments

<!-- facts:arguments -->

## Where It Fits

Called (typically via `operator(*)`) wherever an `output_nutbal` record is scaled — chiefly along the HRU nutrient-balance output-accumulation path (daily → monthly → yearly → average annual).

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. if | Conditional branch evaluating `hru1%rsd_nitorg_n < 1.e-10`. |
| 2. else | Alternative branch taken when the preceding condition is false. |
| 3. if | Conditional branch evaluating `hru1%rsd_laborg_p < 1.e-10`. |
| 4. else | Alternative branch taken when the preceding condition is false. |

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
- warning: missing_doc: Procedure 'output_landscape_module::hruout_nutbal_mult' has no extracted documentation comment.
