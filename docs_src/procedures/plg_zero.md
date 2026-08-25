---
kind: procedure
symbol: plg_zero
title: plg_zero
status: filled
source_hash: 45cf918b752f55d1
version_label: SWAT+ 62.0.0
args:
  plg: '`inout` argument of type `type(plant_growth)`.'
---

<!-- facts:header -->

Zeroes a `plant_growth` record — canopy height, LAI, ET trackers, harvest-index and senescence state, root depth/fraction, and per-plant root fractions — to a clean starting state.

## Bottom Line

`plg_zero` resets every field of a `plant_growth` object in place: canopy height and leaf area index, plant ET and PET accumulators, the LAI-decline and harvest-index fractions, days since senescence, leaf fraction, root depth and fraction, and the per-plant `rtfr` array.

It gives a plant/community growth record a defined zero baseline before a growth cycle begins or a plant is (re)initialized.

## Arguments

<!-- facts:arguments -->

## Where It Fits

Called when a plant or plant community is initialized or reset, so subsequent growth routines start from a clean `plant_growth` state.

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

No hand-authored source-lineage narrative was produced for this helper; see the Git Lineage Evidence below for the commit history of `plant_module.f90`.

## Review Notes

- No direct file I/O was extracted for this procedure.
- info: no_flow_steps: No major control-flow or I/O steps were extracted for this procedure.
