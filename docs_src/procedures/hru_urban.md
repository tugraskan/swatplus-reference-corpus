---
kind: procedure
symbol: hru_urban
title: hru_urban
status: filled
source_hash: f70953c16d10d096
version_label: SWAT+ 62.0.0
locals:
  regres: '`regres` is the external USGS regression function used to compute one urban constituent
    load at a time. `hru_urban` calls it four times with selectors 1 through 4 to obtain `cod`,
    `sus_sol`, `tn`, and `tp` for the current HRU-day.'
  cod: '`cod` holds the regression-estimated carbonaceous oxygen demand load for the current
    urban HRU day. In this routine it is assigned from `Regres(1)` in the USGS branch, but
    the value is not used later in the shown code.'
  sus_sol: '`sus_sol` stores the regression-estimated suspended solid load, or the washed-off
    solids mass computed from street dirt in the build-up/wash-off branch. It is the key intermediate
    used to update sediment yields and to derive associated nutrient loads.'
  tn: '`tn` stores the total nitrogen load associated with the urban runoff or washed-off
    solids. In the USGS branch it comes from `Regres(3)`; in the wash-off branch it is derived
    from `urbdb(ulu)%tnconc` and the computed `sus_sol`.'
  tp: '`tp` stores the total phosphorus load associated with the urban runoff or washed-off
    solids. In the USGS branch it comes from `Regres(4)`; in the wash-off branch it is derived
    from `urbdb(ulu)%tpconc` and the computed `sus_sol`.'
  urbk: '`urbk` is the wash-off coefficient applied to street dirt in the build-up/wash-off
    branch. It is calculated from the urban database coefficient and peak runoff rate, converted
    to a consistent per-hour rate before use in the exponential decay.'
  turo: '`turo` is the effective runoff duration used in the wash-off decay calculation. It
    combines rainfall duration with the HRU time of concentration and is capped at 24 hours
    before being multiplied by `urbk`.'
  dirto: '`dirto` stores the amount of dirt on impervious surfaces before wash-off is applied.
    The routine uses it as the starting mass so it can compute how much dirt remains and how
    much is washed off.'
  durf: '`durf` holds the rainfall duration derived from the half-hour precipitation fraction.
    It is used to build the effective runoff duration that controls the exponential wash-off
    calculation.'
  rp1: '`rp1` is an intermediate value computed from half-hour precipitation and used to estimate
    rainfall duration. It serves only the wash-off timing calculation.'
  dirt: '`dirt` is the current amount of dirt remaining on impervious surfaces. The routine
    first computes it from buildup, then reduces it with an exponential wash-off term, and
    finally uses the remaining amount to update `twash` and washed-off loads.'
  j: '`j` is the current HRU index. The routine sets it from `ihru` and then uses it to read
    and update the HRU-specific state arrays.'
  iob: '`iob` is the connectivity-object index for the current HRU. The routine uses it to
    find the weather station number in `ob(iob)%wst`.'
  xx: '`xx` is the product of wash-off coefficient and effective runoff duration. It is capped
    at 24 before calling `Exp(-xx)` so the exponential wash-off term stays numerically safe.'
  exp: '`exp` is declared as a local real, but in the shown source it is not assigned or used.
    The actual exponential calculation is performed with the intrinsic `Exp` function.'
  tno3: '`tno3` stores the nitrate portion of the washed-off urban solids load. It is computed
    from the total nitrogen concentration and the computed suspended solids, then used to
    update `surqno3` in the wash-off branch.'
uses:
  hru_module: '`hru_module` matters because it provides the current HRU index and the per-HRU
    state arrays that this routine reads and updates. `hru(j)%luse%urb_lu` selects the urban
    database record, `hru(j)%obj_no` links the HRU to its weather station, `hru(j)%luse%urb_ro`
    chooses the runoff algorithm, and the arrays like `sedyld`, `silyld`, `surqno3`, `sedorgn`,
    `sedorgp`, `surqsolp`, `twash`, `surfq`, `tconc`, `qp_cms`, and `ihru` are the mutable
    outputs and drivers of the urban loading calculations.'
  urban_data_module: '`urban_data_module` matters because it supplies the urban parameter
    record for the selected landuse type. The fields `urbdb(ulu)%fimp`, `dirtmx`, `urbcoef`,
    `tnconc`, `tpconc`, and `tno3conc` control how much of the load is assigned to impervious
    area, how much dirt can accumulate, how quickly it washes off, and how nitrogen and phosphorus
    are partitioned from the washed-off solids.'
  hydrograph_module: '`hydrograph_module` matters because the routine needs the HRU’s weather
    station pointer and the station-specific precipitation record. `ob(iob)%wst` maps the
    HRU to `iwst`, which lets the routine access the precipitation fraction used in the wash-off
    timing calculation.'
  climate_module: '`climate_module` matters because daily precipitation controls whether the
    USGS regression branch runs and contributes to the wash-off timing in the build-up/wash-off
    branch. The routine tests `w%precip` to require a wet day before calling `Regres`, and
    the precipitation fraction is also used to estimate rainfall duration for the exponential
    wash-off calculation.'
---

<!-- facts:header -->

Simulates daily urban runoff loadings for an HRU using either USGS regression equations or a build-up/wash-off approach. It updates sediment and nutrient yield states for urban impervious areas.

## Bottom Line

`hru_urban` is the daily urban-loading routine. For each HRU with an urban runoff model enabled, it chooses between USGS regression and build-up/wash-off logic, then updates sediment and nutrient loads on the HRU’s runoff and sediment state variables.

In the USGS branch it only runs on wet days with runoff, using `Regres` to estimate carbonaceous load, suspended solids, total nitrogen, and total phosphorus, then redistributes those loads into the HRU yield arrays with the impervious fraction from `urbdb`. In the build-up/wash-off branch it computes street dirt accumulation from `twash`, removes some of that dirt with rainfall-runoff driven wash-off, and writes the resulting solids and nutrient loads back to the HRU state for later routing and output.

## Arguments

<!-- facts:arguments -->

## Where It Fits

This routine runs from `hru_control` during the daily simulation path when an HRU has `urb_lu > 0` and `time%step == 1`. `hru_control` has already selected the current HRU and populated the shared state needed here, including `ihru`, `surfq`, `qp_cms`, weather linkage, and the urban landuse metadata. The results then feed later routing and sediment/nutrient accumulation behavior, including `swr_latsed` and the rest of the daily HRU output flow.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. load HRU context | The routine copies the current HRU index from `ihru`, looks up the urban landuse ID, gets the object connectivity number, and resolves the weather station pointer for that HRU. |
| 2. choose runoff method | It branches on `hru(j)%luse%urb_ro` to decide whether to use USGS regression equations or the build-up/wash-off algorithm for this HRU. |
| 3. process USGS regression loads | On wet days with runoff, it calls `Regres` four times to compute urban carbonaceous oxygen demand, suspended solids, total nitrogen, and total phosphorus, then mixes those loads into the HRU sediment and nutrient arrays using the impervious fraction `urbdb(ulu)%fimp` and the HRU area normalization for nutrient terms. |
| 4. process build-up/wash-off case | If the HRU uses build-up/wash-off, it checks whether the day is wet enough to trigger wash-off and street-cleaning logic. |
| 5. compute pre-wash dirt | It calculates the amount of dirt on impervious surfaces from the buildup equation using `dirtmx`, `twash`, and `thalf`, then saves that amount as `dirto` before wash-off is applied. |
| 6. derive wash-off forcing | It computes the wash-off coefficient `urbk`, estimates rainfall duration from half-hour precipitation, adds time of concentration to form `turo`, and caps the duration at 24 hours. |
| 7. apply exponential wash-off | It forms the exponent term, applies exponential decay to the street dirt mass, and zeroes tiny residual dirt values to avoid roundoff noise. |
| 8. update buildup clock | It updates `twash(j)` so the next buildup calculation reflects the reduced dirt remaining after wash-off. |
| 9. compute washed-off loads | It converts the washed-off dirt mass to suspended solids and derives total nitrogen, total phosphorus, and nitrate loads from the urban database concentration factors. |
| 10. mix wash-off into HRU outputs | It updates the HRU sediment and nutrient yield arrays by blending the new urban loads into the impervious fraction while leaving the pervious fraction unchanged. |
| 11. age dry streets | On dry days, it increments `twash(j)` by one day to continue the buildup clock for the next wet event. |
| 12. finish | The routine exits after updating the urban HRU state for the day. |

## Modules Used

<!-- facts:uses -->

| Module | State touched | Key components |
| --- | --- | --- |
| [sym:hru_module] | `hru, sedyld, silyld, twash, surqno3, sedorgn, sedorgp, surqsolp, surfq, sanyld, clayld, sagyld, lagyld, tconc, ihru, ulu, qp_cms` | `hru(j)%luse%urb_lu, hru(j)%obj_no, hru(j)%luse%urb_ro, hru(j)%km` |
| [sym:urban_data_module] | `urbdb` | `urbdb(ulu)%fimp, urbdb(ulu)%dirtmx, urbdb(ulu)%urbcoef, urbdb(ulu)%tnconc, urbdb(ulu)%tpconc, urbdb(ulu)%tno3conc` |
| [sym:hydrograph_module] | `ob, iwst` | `ob(iob)%wst` |
| [sym:climate_module] | `w` | `w%precip` |

## Local Variables

<!-- facts:locals -->

## State Changes

| Target | When | Meaning |
| --- | --- | --- |
| `ulu` | `hru(j)%luse%urb_ro == 'usgs_reg'` and `w%precip > .1` and `surfq(j) > .1` | `ulu` is assigned from the current HRU’s urban landuse ID and then used to index `urbdb` for all urban parameter lookups in this call. |
| `iwst` | Immediately after `iob = hru(j)%obj_no` | `iwst` is set from the HRU’s connectivity object so the routine can read the correct weather-station precipitation record for wash-off timing. |
| `sedyld(j)` | `hru(j)%luse%urb_ro == 'usgs_reg'` and wet-day runoff conditions are met, or `hru(j)%luse%urb_ro == 'buildup_washoff'` and `surfq(j) > 0.1` | `sedyld(j)` is overwritten with the urban impervious contribution blended with the existing HRU sediment yield, so later routing sees the updated daily sediment load. |
| `silyld(j)` | Same branches as `sedyld(j)` | `silyld(j)` is updated to hold the silt-dominated share of the urban solids load plus the pre-existing nonurban portion of the HRU’s silt yield. |
| `sanyld(j)` | Same branches as `sedyld(j)` | `sanyld(j)` is reduced by the impervious fraction in the urban loading calculation so the pervious contribution remains. |
| `clayld(j)` | Same branches as `sedyld(j)` | `clayld(j)` is reduced by the impervious fraction in the urban loading calculation so the pervious contribution remains. |
| `sagyld(j)` | Same branches as `sedyld(j)` | `sagyld(j)` is reduced by the impervious fraction in the urban loading calculation so the pervious contribution remains. |
| `lagyld(j)` | Same branches as `sedyld(j)` | `lagyld(j)` is reduced by the impervious fraction in the urban loading calculation so the pervious contribution remains. |
| `sedorgn(j)` | Same branches as `sedyld(j)` | `sedorgn(j)` is updated with the urban organic nitrogen contribution from either the regression estimate or the washed-off solids-derived nitrogen pool. |
| `surqno3(j)` | Same branches as `sedyld(j)` | `surqno3(j)` is updated with the urban nitrate contribution, either from the regression estimate or from the washed-off solids-derived nitrate load. |
| `sedorgp(j)` | Same branches as `sedyld(j)` | `sedorgp(j)` is updated with the urban particulate phosphorus contribution derived from the urban phosphorus load. |
| `surqsolp(j)` | Same branches as `sedyld(j)` | `surqsolp(j)` is updated with the urban soluble phosphorus contribution derived from the urban phosphorus load. |
| `twash(j)` | `hru(j)%luse%urb_ro == 'buildup_washoff'` and `surfq(j) > 0.1`, or the same branch on a dry day | `twash(j)` is reset to a new effective buildup age after wash-off, or incremented by one day when no wash-off occurs, so the next event uses the updated street-dirt buildup history. |

## File I/O

<!-- facts:io -->


## Theory Equations

| Eq. | Title | Formula | Implementation |
| --- | --- | --- | --- |
| 6:3.4.1 | Solid build-up on impervious surfaces | $SED=\frac{SED_{mx}*td}{(t_{half}+td)}$ | Verified against SWAT+ 62.0.0 (hru_urban.f90:128). dirt = dirtmx*twash/(thalf+twash) |
| 6:3.4.2 | Solid wash-off by surface runoff | $Y_{sed}=SED_0*(1-e^{-kk*t})$ | Verified against SWAT+ 62.0.0 (hru_urban.f90:140). wash-off `Y = dirt₀·(1-Exp(-urbk·turo))`; `dirt*Exp(-xx)` is the remainder |
| 6:3.4.3 | Wash-off coefficient kk | $kk=urb_{coef}*q_{peak}$ | Verified against SWAT+ 62.0.0 (hru_urban.f90:132). urbk = urbcoef*(qp_cms*3.6/km) |
| 6:3.2.1 | Composite CN for imp_tot < 0.30 | $CN_c=CN_p+imp_{tot}*(CN_{imp}-CN_p)*(1-\frac{imp_{dcon}}{2*imp_{tot}})$ | Verified against SWAT+ 62.0.0 (hru_urban.f90:100). imp<0.30 regression-select branch → continuous `fimp` weighting `X·fimp+Y·(1-fimp) |
| 6:3.2.2 | Composite CN for imp_tot >= 0.30 | $CN_c=CN_p+imp_{tot}*(CN_{imp}-CN_p)$ | Verified against SWAT+ 62.0.0 (hru_urban.f90:100). imp>0.30 branch → same continuous fimp weighting |
| 6:3.2.3 | Disconnected impervious fraction | $imp_{dcon}=imp_{tot}-imp_{con}$ | Verified against SWAT+ 62.0.0 (hru_urban.f90). connected/disconnected impervious split |

## Lineage

Three resolved commits changed `hru_urban`: `df07e3f` introduced the subroutine with its documentation block and full daily urban-loading logic; `94b6dec` added the latest source version without changing the shown algorithm; `39fabde` initialized the local scalars and loop indices to zero and fixed a comment typo, and `bd18ad4` changed the `regres` declaration to an external interface. No later resolved commit in the evidence changed the routine’s computational flow.

- df07e3f added the daily urban-loading subroutine, including the USGS regression branch, the build-up/wash-off branch, and the updates to sediment and nutrient HRU states.
- 39fabde made the local working variables explicitly initialized, reducing the chance that unassigned values affect the urban-load calculations.
- bd18ad4 changed `regres` from a local real declaration to an external procedure declaration, making the USGS regression calls compile against the function interface.

## Review Notes

- No direct file I/O was extracted for this procedure.
- warning: missing_doc: Procedure 'hru_urban' has no extracted documentation comment.
