---
kind: procedure
symbol: res_convert_mass
title: res_convert_mass
status: filled
source_hash: 69653205af5696c6
version_label: SWAT+ 62.0.0
args:
  pvol: '`in` argument of type `real`.'
  hyd1: '`inout` argument of type `type(hyd_output)`.'
---

<!-- facts:header -->

Converts a hydrograph's concentrations to masses like `hyd_convert_conc_to_mass`, but first scales flow by `pvol` (the principal-volume fraction) — used for reservoir release.

## Bottom Line

`res_convert_mass` multiplies the hydrograph flow by `pvol` (interpreted as a fraction of the principal volume), then converts each constituent concentration to mass with the same unit factors as `hyd_convert_conc_to_mass` (t = ppm·m³/1e6 for sediment, kg = ppm·m³/1e3 for nutrients).

It produces the mass carried by a reservoir release equal to a given fraction of principal storage.

## Arguments

<!-- facts:arguments -->

## Where It Fits

Called from the reservoir release path to turn concentrations plus a release fraction into transported masses.

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
- info: weak_doc: Procedure 'hydrograph_module::res_convert_mass' documentation is very short.
- info: no_flow_steps: No major control-flow or I/O steps were extracted for this procedure.
