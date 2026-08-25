---
kind: procedure
symbol: ero_add
title: ero_add
status: filled
source_hash: ebf204ae0de26347
version_label: SWAT+ 62.0.0
args:
  ero_1: The first `erosion_output_variables` operand (intent(in)).
  ero_2: The second `erosion_output_variables` operand (intent(in)).
locals:
  ero_3: 'Result variable: the `erosion_output_variables` record the function returns, holding
    the field-by-field result.'
---

<!-- facts:header -->

Field-by-field addition of two `erosion_output_variables` records, defined in `erosion_module` and used to accumulate `erosion_output_variables` state.

## Bottom Line

`ero_add` returns a new `erosion_output_variables` record whose fields are the field-by-field sum of its two inputs. All 14 of the record's 14 value fields are combined with `+`.

This is one of the small arithmetic helpers `erosion_module` defines for the `erosion_output_variables` derived type. SWAT+ output and routing code calls it to keep `erosion_output_variables` records accumulated — typically when rolling daily state up into monthly, yearly, and average-annual totals. It is a pure function: its arguments are `intent(in)` and it has no side effects.

## Arguments

<!-- facts:arguments -->

## Where It Fits

`ero_add` is a pure, side-effect-free helper in `erosion_module`; it only computes a new `erosion_output_variables` value from its arguments and does no I/O. It runs wherever `erosion_output_variables` records are accumulated, chiefly along the output-accumulation path (daily → monthly → yearly → average annual).

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
- info: weak_doc: Procedure 'erosion_module::ero_add' documentation is very short.
- info: no_flow_steps: No major control-flow or I/O steps were extracted for this procedure.
