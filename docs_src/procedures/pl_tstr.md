---
kind: procedure
symbol: pl_tstr
title: pl_tstr
status: filled
source_hash: 4458cc5d69c3e2e8
version_label: SWAT+ 62.0.0
locals:
  j: '`j` is the current HRU index. It is set from `ihru` and used to pick the active plant
    community in `pcom(j)`.'
  idp: '`idp` is the plant database index for the active plant. It is taken from `pcom(j)%plcur(ipl)%idplt`
    so the routine can look up that plant''s temperature limits in `pldb`.'
  tgx: '`tgx` is the temperature distance used in the stress calculation. It starts as `w%tave
    - pldb(idp)%t_base`, may be reflected around the optimum temperature, and is then reused
    in the SWAT-style exponential branch.'
  rto: '`rto` is the normalized temperature response variable. It is first used as the squared
    ratio for the exponential stress branch, then recomputed for the final APEX sine response.'
uses:
  climate_module: '`climate_module` supplies the current daily weather state and weather-generator
    annual temperature needed to judge temperature stress. `w%tave` and `w%tmin` drive the
    daily response, while `wgn_pms(iwgen)%tmp_an` is used to zero stress when the minimum
    temperature is far below the site''s annual mean.'
  plant_data_module: '`plant_data_module` provides the species-specific temperature limits
    that define the stress curve. `pldb(idp)%t_base` and `pldb(idp)%t_opt` determine when
    stress begins, when it peaks, and how the routine scales the response.'
  hru_module: '`hru_module` provides the current HRU and plant-competition indices that identify
    which plant instance to update. `ihru`, `ipl`, and `iwgen` select the active community,
    the current plant slot, and the matching weather-generator parameters.'
  plant_module: '`plant_module` holds the plant community arrays that `pl_tstr` reads and
    updates. `pcom(j)%plcur(ipl)%idplt` identifies the plant in the database, and `pcom(j)%plstr(ipl)%strst`
    is the stress factor this routine writes for later growth calculations.'
---

<!-- facts:header -->

Computes the daily temperature stress factor for the active plant in the current HRU. It uses plant temperature limits and weather conditions to update the plant stress state.

## Bottom Line

pl_tstr calculates the plant temperature stress multiplier `strst` for the current HRU/plant combination. It reads the plant's base and optimum temperature limits, the day's average and minimum temperature, and the weather-generator annual mean temperature to decide how much potential growth should be reduced by temperature stress.

The routine first follows a SWAT-style temperature-response calculation and then overwrites that result with an APEX sine-based temperature response before clamping the final stress factor to the 0 to 1 range. The resulting `pcom(j)%plstr(ipl)%strst` value is then available to the growth routines that combine plant stress factors during biomass production.

## Arguments

<!-- facts:arguments -->

## Where It Fits

This routine runs during daily plant growth processing after `pl_biomass_gro` has set up the current HRU biomass-growth context and before nutrient uptake and other stress calculations continue. Its output, `pcom(j)%plstr(ipl)%strst`, feeds the plant stress state used by later growth behavior in the same daily simulation step.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. set current HRU index | Copy `ihru` into `j` so the routine works on the current HRU's plant community. |
| 2. get plant database index and base temperature gap | Look up the active plant with `pcom(j)%plcur(ipl)%idplt` and compute `tgx = w%tave - pldb(idp)%t_base`. |
| 3. handle temperatures at or below base | If the day's average temperature is at or below the plant base temperature, set temperature stress to zero. |
| 4. reflect hot temperatures around optimum | For temperatures above optimum, replace `tgx` with the reflected distance `2*t_opt - t_base - w%tave` so the stress curve can be evaluated on the warm side. |
| 5. compute exponential stress ratio | Initialize `rto` and compute the squared normalized distance between optimum temperature and the day's average temperature. |
| 6. apply SWAT-style exponential response or zero it | If the ratio is within bounds and `tgx` remains positive, set stress to `Exp(-0.1054*rto)`; otherwise set stress to zero. |
| 7. force zero stress for very cold minima | If minimum temperature is at least 15 degrees below the site's annual mean temperature, override the stress factor to zero. |
| 8. compute final APEX temperature response | Recompute `rto` as the normalized position between base and optimum temperatures, then set stress to `Sin(1.5707*rto)` when the ratio passes the branch test, otherwise set it to zero. |
| 9. clamp final stress and return | Limit the final stress factor to the 0 to 1 range and return to the caller. |

## Modules Used

<!-- facts:uses -->

| Module | State touched | Key components |
| --- | --- | --- |
| [sym:climate_module] | `w, wgn_pms` | `w%tave, w%tmin, wgn_pms(iwgen)%tmp_an` |
| [sym:plant_data_module] | `pldb` | `pldb(idp)%t_base, pldb(idp)%t_opt` |
| [sym:hru_module] | `ihru, ipl, iwgen` |  |
| [sym:plant_module] | `pcom` | `pcom(j)%plcur(ipl)%idplt, pcom(j)%plstr(ipl)%strst` |

## Local Variables

<!-- facts:locals -->

## State Changes

| Target | When | Meaning |
| --- | --- | --- |
| `pcom(j)%plstr(ipl)%strst` | After the current HRU and plant are identified, the routine assigns a temperature stress factor based on the day's temperatures and the plant's temperature limits, with a cold-weather override when `w%tmin <= wgn_pms(iwgen)%tmp_an - 15.`. | `pcom(j)%plstr(ipl)%strst` changes when the plant is exposed to temperature conditions that reduce growth potential. The value is set to zero in cold or out-of-range cases, otherwise it is computed from an exponential or sine-based temperature response and then clamped to a valid fraction. |

## File I/O

<!-- facts:io -->


## Theory Equations

| Eq. | Title | Formula | Implementation |
| --- | --- | --- | --- |
| 5:3.1.2 | Temperature stress below base temperature | $tstrs=1$ | An intermediate SWAT-style branch sets zero growth below t_base, but the final stored temperature response is overwritten by the APEX sine formula at lines 68-77. |
| 5:3.1.3 | Temperature stress between base and optimum temperature | $tstrs=1-exp[\frac{-0.1054*(T_{opt}-\overline T_{av})^2}{(\overline T_{av}-T_{base})^2}]$ | Verified against SWAT+ 62.0.0 (pl_tstr.f90:71). APEX `strst = Sin(1.5707*rto)` is active; theory's exp(-0.1054·rto) two-branch form (:56-59) is computed then OVERWRITTEN |
| 5:3.1.4 | Temperature stress above optimum temperature | $tstrs=1-exp[\frac{-0.1054*(T_{opt}-\overline T_{av})^2}{(2*T_{opt}-\overline T_{av}-T_{base})^2}]$ | Verified against SWAT+ 62.0.0 (pl_tstr.f90:71). same — above-opt branch overwritten by APEX sin |
| 5:3.1.5 | Temperature stress beyond the upper limit | $tstrs=1$ | The intermediate branch can force zero growth when reflected tgx <= 0 or rto > 200, but the final stored value still comes from the later sine-based APEX formulation. |

## Lineage

`pl_tstr` was introduced in commit df07e3f with a documented temperature-stress routine that computed stress from plant base and optimum temperatures and weather-generator annual temperature. Commit 94b6dec kept the routine structure but added the current source version with the APEX sine-based temperature response and the surrounding SWAT-style branches. Commit 39fabde only initialized the local variables `j`, `idp`, `tgx`, and `rto` to zero; it did not change the stress logic.

- df07e3f added the `pl_tstr` subroutine with the documented temperature-stress calculation and its use of `t_base`, `t_opt`, and `tmp_an`.
- 94b6dec preserved the routine but introduced the current source form that includes the final APEX sine-based temperature stress assignment after the intermediate SWAT-style branch.
- 39fabde changed only local variable initialization for `j`, `idp`, `tgx`, and `rto` and did not alter the temperature-stress algorithm.

## Review Notes

- No direct file I/O was extracted for this procedure.
- warning: missing_doc: Procedure 'pl_tstr' has no extracted documentation comment.
