---
kind: procedure
symbol: cli_lapse
title: cli_lapse
status: filled
source_hash: e6e19cfd35cdf3cd
version_label: SWAT+ 62.0.0
locals:
  iob: Loop index for the current spatial object being updated; it runs from 1 to `sp_ob%objs`
    and selects the object whose lapse values are being computed.
  iwst: Weather-station index for the current object. It is copied from `ob(iob)%wst` so the
    routine can read that object's climate-source codes and linked weather data.
  iwgn: Weather-generator index used when the station code requests simulated climate (`"sim"`).
    It points to `wgn(iwgn)` for the elevation used in the lapse calculation.
  igage: Measured gage index used when the station code points to an observed precipitation
    or temperature gage instead of simulation. It selects `pcp(igage)` or `tmp(igage)` for
    elevation.
uses:
  basin_module: The basin module supplies the global lapse-rate parameters `bsn_prm%plaps`
    and `bsn_prm%tlaps`. `cli_lapse` multiplies those basin-wide rates by each object's elevation
    difference, so without this module there is no source for the precipitation and temperature
    lapse magnitudes.
  climate_module: The climate module holds the weather-station routing codes and the elevation
    metadata needed to decide which reference elevation to use. `cli_lapse` reads `wst(iwst)%wco_c%pgage`
    and `tgage` to choose between simulated generators (`wgn`) and measured gages (`pcp`,
    `tmp`), then uses the referenced elevation field in the lapse formulas.
  hydrograph_module: The hydrograph module provides the spatial-object inventory and each
    object's weather-station assignment and stored lapse fields. `sp_ob%objs` controls how
    many objects are processed, `ob(iob)%wst` tells the routine which station to use, and
    `ob(iob)%plaps`/`ob(iob)%tlaps` are the state values this routine overwrites.
---

<!-- facts:header -->

Updates each spatial object's precipitation and temperature lapse adjustments from basin lapse rates and its assigned weather station. These lapse offsets are then used by the climate controls that apply elevation-band corrections.

## Bottom Line

cli_lapse loops over all spatial objects and computes two per-object elevation adjustments: `ob(iob)%plaps` for precipitation and `ob(iob)%tlaps` for temperature. For each object it looks up the assigned weather station, chooses either the simulated weather-generator elevation or a measured gage elevation depending on station codes, and scales the basin lapse rates by the elevation difference divided by 1000.

This routine matters because reservoir and channel climate controls call it immediately before they use weather data, so the per-object lapse values are refreshed from the current object/station configuration. The corrected lapse offsets then feed later weather-dependent behavior in `res_control` and `sd_channel_control3`.

## Arguments

<!-- facts:arguments -->

## Where It Fits

This routine runs when climate adjustments are needed for a specific object, right after the caller has selected the object and before that caller uses the object's weather state. `res_control` and `sd_channel_control3` both save `wst(iwst)%weat`, call `cli_lapse` if `bsn_cc%lapse == 1`, then restore `weat`; the updated `ob(iob)%plaps` and `ob(iob)%tlaps` are used later when those controls apply climate-driven reservoir or channel behavior.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. loop over objects | Iterate through every spatial object in the model (`1..sp_ob%objs`) so each object's precipitation and temperature lapse offsets can be refreshed. |
| 2. read object weather station | Load the weather-station index for the current object from `ob(iob)%wst`, establishing which climate data connection controls the lapse calculation. |
| 3. choose precipitation reference and compute plaps | If the station's precipitation source code is `"sim"`, use the linked weather generator elevation `wgn(iwgn)%elev`; otherwise use the measured precipitation gage elevation `pcp(igage)%elev`. Multiply the basin precipitation lapse rate by the object's elevation difference from that reference and divide by 1000 to store `ob(iob)%plaps`. |
| 4. choose temperature reference and compute tlaps | If the station's temperature source code is `"sim"`, use the linked weather generator elevation `wgn(iwgn)%elev`; otherwise use the measured temperature gage elevation `tmp(igage)%elev`. Multiply the basin temperature lapse rate by the reference elevation difference from the object and divide by 1000 to store `ob(iob)%tlaps`. |
| 5. finish loop and return | After all objects have been updated, exit the routine and return control to the caller, leaving the per-object lapse adjustments available for later climate handling. |

## Modules Used

<!-- facts:uses -->

| Module | State touched | Key components |
| --- | --- | --- |
| [sym:basin_module] | `bsn_prm` | `bsn_prm%plaps, bsn_prm%tlaps` |
| [sym:climate_module] | `wst, wgn, pcp, tmp` | `wst(iwst)%wco_c%pgage, wst(iwst)%wco%wgn, wgn(iwgn)%elev, wst(iwst)%wco%pgage, pcp(igage)%elev, wst(iwst)%wco_c%tgage, wst(iwst)%wco%tgage, tmp(igage)%elev` |
| [sym:hydrograph_module] | `sp_ob, ob` | `sp_ob%objs, ob(iob)%wst, ob(iob)%plaps, ob(iob)%elev, ob(iob)%tlaps` |

## Local Variables

<!-- facts:locals -->

## State Changes

| Target | When | Meaning |
| --- | --- | --- |
| `ob(iob)%plaps` | When `wst(iwst)%wco_c%pgage == "sim"`, `ob(iob)%plaps` is based on `wgn(iwgn)%elev`; otherwise it is based on `pcp(igage)%elev`. | `ob(iob)%plaps` is overwritten for each object with the precipitation lapse adjustment implied by that object's elevation relative to either a simulated weather-generator elevation or a measured precipitation gage elevation. |
| `ob(iob)%tlaps` | When `wst(iwst)%wco_c%tgage == "sim"`, `ob(iob)%tlaps` is based on `wgn(iwgn)%elev`; otherwise it is based on `tmp(igage)%elev`. | `ob(iob)%tlaps` is overwritten for each object with the temperature lapse adjustment implied by that object's elevation relative to either a simulated weather-generator elevation or a measured temperature gage elevation. |

## File I/O

<!-- facts:io -->


## Theory Equations

| Eq. | Title | Formula | Implementation |
| --- | --- | --- | --- |
| 1:4.1.1 | Band precipitation (lapse term) | $R_{band}=R_{day}+(EL_{band}-EL_{gage})*\frac{plaps}{days_{pcp,yr}*1000}$ | Verified against SWAT+ 62.0.0 (cli_lapse.f90). (Rday>0.01 band condition) |
| 1:4.1.2 | Band maximum temperature (lapse term) | $T_{mx,band}=T_{mx}+(EL_{band}-EL_{gage})*\frac{tlaps}{1000}$ | Verified against SWAT+ 62.0.0 (cli_lapse.f90:30). (Tmx band = Tmx + dEL*tlaps) |
| 1:4.1.3 | Band minimum temperature (lapse term) | $T_{mn,band}=T_{mn}+(EL_{band}-EL_{gage})*\frac{tlaps}{1000}$ | Verified against SWAT+ 62.0.0 (cli_lapse.f90:30). (Tmn band lapse) |
| 1:4.1.4 | Band average temperature (lapse term) | $\overline T_{av,band} =\overline T_{av} +(EL_{band}-EL_{gage})*\frac{tlaps}{1000}$ | Verified against SWAT+ 62.0.0 (cli_lapse.f90:30). (Tav band lapse) |

## Lineage

Resolved lineage shows the routine was introduced in df07e3f as a new `cli_lapse` subroutine that computes elevation-based precipitation and temperature lapse values for each object. c7c8e22 carried the same logic forward while preserving the routine body, and 39fabde only initialized the local loop variables (`iob`, `iwst`, `iwgn`, `igage`) to zero.

- df07e3f added the routine and its full object loop, including the simulated-versus-measured gage branches for `plaps` and `tlaps`.
- c7c8e22 retained the same lapse-computation logic from the imported source snapshot; no behavior change is visible in the resolved diff.
- 39fabde changed only the local variable declarations by assigning initial values of 0 to `iob`, `iwst`, `iwgn`, and `igage`.

## Review Notes

- No direct file I/O was extracted for this procedure.
- warning: missing_doc: Procedure 'cli_lapse' has no extracted documentation comment.
