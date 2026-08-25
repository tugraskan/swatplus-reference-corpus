---
kind: procedure
symbol: hyd_convert_conc_to_mass
title: hyd_convert_conc_to_mass
status: filled
source_hash: efe1636ac99d13d9
version_label: SWAT+ 62.0.0
args:
  hyd1: '`inout` argument of type `type(hyd_output)`.'
---

<!-- facts:header -->

Converts a hydrograph's constituent concentrations to masses in place, multiplying each by flow with the appropriate unit factor.

## Bottom Line

`hyd_convert_conc_to_mass` takes a `hyd_output` in place and multiplies each constituent by the flow volume with its unit conversion: sediment size classes use t = ppm·m³/1e6, nutrients and organics use kg = ppm·m³/1e3. Flow itself is left unchanged.

It moves a hydrograph from a concentration representation to an absolute-mass representation for routing/summation.

## Arguments

<!-- facts:arguments -->

## Where It Fits

Called along the routing path wherever concentrations must be turned into transported masses before combining hydrographs.

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
- info: weak_doc: Procedure 'hydrograph_module::hyd_convert_conc_to_mass' documentation is very short.
- info: no_flow_steps: No major control-flow or I/O steps were extracted for this procedure.
