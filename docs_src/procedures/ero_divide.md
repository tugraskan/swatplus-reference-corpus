---
kind: procedure
symbol: ero_divide
title: ero_divide
status: filled
source_hash: f9226c9abe39393c
version_label: SWAT+ 62.0.0
args:
  ero_1: The first `erosion_output_variables` operand (intent(in)).
  const: Scalar applied to each field of the `erosion_output_variables` record.
locals:
  ero_2: 'Result variable: the `erosion_output_variables` record the function returns, holding
    the field-by-field result.'
---

<!-- facts:header -->

Divides a `erosion_output_variables` record by a scalar (`const`) field by field, defined in `erosion_module` and used to average accumulated `erosion_output_variables` state.

## Bottom Line

`ero_divide` returns a new `erosion_output_variables` record whose fields are its input's fields each divided by the scalar `const`. 14 of the 14 fields are divided by `const`: `sedyld`, `precip`, `surfq`, `peak`, `k`, `s`, `l`, `ls`, `p`, `rsd_m`, `grcov_frac`, `rsd_covfact`, … (14 total).

This is one of the small arithmetic helpers `erosion_module` defines for the `erosion_output_variables` derived type. SWAT+ output and routing code calls it to keep `erosion_output_variables` records averaged — typically when rolling daily state up into monthly, yearly, and average-annual totals. It is a pure function: its arguments are `intent(in)` and it has no side effects.

## Arguments

<!-- facts:arguments -->

## Where It Fits

`ero_divide` is a pure, side-effect-free helper in `erosion_module`; it only computes a new `erosion_output_variables` value from its arguments and does no I/O. It runs wherever `erosion_output_variables` records are averaged, chiefly along the output-accumulation path (daily → monthly → yearly → average annual).

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

No hand-authored source-lineage narrative was produced for this helper; see the Git Lineage Evidence below for the commit history of `erosion_module.f90`.

## Review Notes

- No direct file I/O was extracted for this procedure.
- info: weak_doc: Procedure 'erosion_module::ero_divide' documentation is very short.
- info: no_flow_steps: No major control-flow or I/O steps were extracted for this procedure.
