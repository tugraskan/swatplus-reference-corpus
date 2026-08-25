---
kind: procedure
symbol: hydout_add
title: hydout_add
status: filled
source_hash: 4c995a31d889a692
version_label: SWAT+ 62.0.0
args:
  hyd1: '`in` argument of type `type(hyd_output)`.'
  hyd2: '`in` argument of type `type(hyd_output)`.'
locals:
  hyd3: 'Result variable: the `type(hyd_output)` value the function returns.'
---

<!-- facts:header -->

Adds two hydrographs field by field (the constituents are summed) and mixes temperature as a flow-weighted average of the two inputs.

## Bottom Line

`hydout_add` returns a `hyd_output` whose flow and 16 constituent fields are the sums of the two inputs. Temperature is handled specially: when the combined flow exceeds 1e-6 it is the flow-weighted mean `(flo1·temp1 + flo2·temp2)/(flo1+flo2)`; otherwise it is set to 0.

It is the addition operator for `hyd_output` — used to merge incoming hydrographs — with the physically correct flow-weighted temperature mixing rather than a plain sum.

## Arguments

<!-- facts:arguments -->

## Where It Fits

Called (typically via `operator(+)`) wherever two `hyd_output` hydrographs are combined during routing/summation.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. if | Conditional branch evaluating `hyd1%flo + hyd2%flo > 1.e-6`. |
| 2. else | Alternative branch taken when the preceding condition is false. |

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

No hand-authored source-lineage narrative was produced for this helper; see the Git Lineage Evidence below for the commit history of `hydrograph_module.f90`.

## Review Notes

- No direct file I/O was extracted for this procedure.
- info: weak_doc: Procedure 'hydrograph_module::hydout_add' documentation is very short.
