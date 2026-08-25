---
kind: procedure
symbol: hydout_div_conv
title: hydout_div_conv
status: filled
source_hash: 529318c447d31e56
version_label: SWAT+ 62.0.0
args:
  hyd1: '`in` argument of type `type(hyd_output)`.'
  hyd2: '`in` argument of type `type(hyd_output)`.'
locals:
  hyd3: 'Result variable: the `type(hyd_output)` value the function returns.'
---

<!-- facts:header -->

Element-wise ratio of two hydrographs (`hyd1/hyd2`), returning 0 for any constituent whose denominator is below 1e-6.

## Bottom Line

`hydout_div_conv` divides each field of `hyd1` by the matching field of `hyd2`, but guards every division: if the denominator field is at or below 1e-6 the result is set to 0 instead. It thus computes safe per-constituent conversion ratios rather than a scalar divide.

It is used where a hydrograph must be expressed as a fraction/ratio relative to another hydrograph without risking divide-by-zero.

## Arguments

<!-- facts:arguments -->

## Where It Fits

Called along the routing/conversion path to derive per-constituent ratios between two `hyd_output` hydrographs.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. Summarize source block 1 | Executes the source at the referenced lines. |
| 2. Summarize source block 2 | Executes the source at the referenced lines. |
| 3. Summarize source block 3 | Executes the source at the referenced lines. |
| 4. Summarize source block 4 | Executes the source at the referenced lines. |
| 5. Summarize source block 5 | Executes the source at the referenced lines. |
| 6. Summarize source block 6 | Executes the source at the referenced lines. |
| 7. Summarize source block 7 | Executes the source at the referenced lines. |
| 8. Summarize source block 8 | Executes the source at the referenced lines. |

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
- info: weak_doc: Procedure 'hydrograph_module::hydout_div_conv' documentation is very short.
