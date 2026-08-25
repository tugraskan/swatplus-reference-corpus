---
kind: procedure
symbol: hyd_min
title: hyd_min
status: filled
source_hash: 0a697703bb602d1c
version_label: SWAT+ 62.0.0
args:
  hyd1: '`inout` argument of type `type(hyd_output)`.'
  hyd2: '`in` argument of type `type(hyd_output)`.'
---

<!-- facts:header -->

Returns, in place, the element-wise minimum of two hydrographs' constituents (flow passed through); used to cap water-treatment-plant loads.

## Bottom Line

`hyd_min` overwrites each constituent of `hyd1` with the smaller of `hyd1` and `hyd2` (via `amin1`), leaving flow unchanged. Despite the `!! function` comment it is a subroutine that mutates its first argument.

It caps a hydrograph's constituents at a second hydrograph's values, used in the water-treatment-plant (wwtp) logic.

## Arguments

<!-- facts:arguments -->

## Where It Fits

Called from the water-allocation/treatment path to limit constituent loads to available/target values.

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

No hand-authored source-lineage narrative was produced for this helper; see the Git Lineage Evidence below for the commit history of `hydrograph_module.f90`.

## Review Notes

- No direct file I/O was extracted for this procedure.
- info: weak_doc: Procedure 'hydrograph_module::hyd_min' documentation is very short.
- info: no_flow_steps: No major control-flow or I/O steps were extracted for this procedure.
