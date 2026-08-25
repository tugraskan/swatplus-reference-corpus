---
kind: procedure
symbol: hyd_convert_mass_to_conc
title: hyd_convert_mass_to_conc
status: filled
source_hash: 4ff5410b17f2a666
version_label: SWAT+ 62.0.0
args:
  hyd1: '`inout` argument of type `type(hyd_output)`.'
---

<!-- facts:header -->

Inverse of `hyd_convert_conc_to_mass`: converts a hydrograph's constituent masses back to concentrations (ppm) by dividing by flow, guarded by flow > 0.01.

## Bottom Line

`hyd_convert_mass_to_conc` takes a `hyd_output` in place and, when flow exceeds 0.01, divides each constituent mass by flow with the inverse unit factor (ppm = 1e6·t/m³ for sediment, 1e3·kg/m³ for nutrients); the individual sediment size classes are set to zero. When flow is negligible the constituents are left/zeroed to avoid divide-by-tiny-flow.

It returns a routed hydrograph to a concentration representation for reporting or further mixing.

## Arguments

<!-- facts:arguments -->

## Where It Fits

Called along the routing path after masses have been summed, to express the result as concentrations.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. if | Conditional branch evaluating `hyd1%flo > 0.01`. |
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
- info: weak_doc: Procedure 'hydrograph_module::hyd_convert_mass_to_conc' documentation is very short.
