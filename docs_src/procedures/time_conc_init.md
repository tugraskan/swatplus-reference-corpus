---
kind: procedure
symbol: time_conc_init
title: time_conc_init
status: filled
source_hash: dffcd5779ef2681a
version_label: SWAT+ 62.0.0
locals:
  ii: Loop counter over elements within each routing unit while accumulating the weighted
    Manning's n.
  ielem: Holds the current routing-unit element index pulled from ru_def(iru)%num(ii).
  iob: Maps each routing unit to the corresponding object-connectivity record in ob for area
    lookup.
  ith: Holds the topography database index for the current routing unit or HRU.
  ifld: Holds the HRU field database index when stepping through HRUs; it is assigned from
    hru(ihru)%dbs%field but not otherwise used here.
  tov: Temporary overland-flow travel time used while computing a routing unit's total concentration
    time.
  ch_slope: Temporary channel slope used in the channel travel-time calculation.
  ch_n: Temporary Manning's n value for channel travel time; set from the routing unit or
    HRU landuse roughness.
  ch_l: Temporary channel length used in the travel-time formula.
  t_ch: Temporary channel travel time that is added to overland travel time to form total
    concentration time.
uses:
  ru_module: 'ru_module supplies the shared routing-unit arrays that this routine updates:
    ru_n for weighted Manning''s n, ru for drainage area and database pointers, ru_tc for
    the final routing-unit time of concentration, and iru as the module-level routing-unit
    index used by the loops.'
  hru_module: hru_module supplies each HRU's geometry and roughness values used to compute
    t_ov, tconc, and brt, and it stores those outputs so later runoff and routing code can
    reuse them.
  hydrograph_module: hydrograph_module provides the routing-unit membership and object connectivity
    needed to link each routing unit to its elements and area, which is necessary to aggregate
    roughness and convert object area into drainage area.
  topography_data_module: topography_data_module provides the slope and slope-length parameters
    used in both the routing-unit and HRU overland/channel travel-time calculations.
  time_module: time_module controls whether the runoff lag fraction uses the time-step-adjusted
    expression for subdaily simulation or the simpler daily form.
  basin_module: basin_module provides the basin-wide surface runoff lag parameter surlag that
    is converted into the fraction brt for each HRU.
---

<!-- facts:header -->

Initializes routing-unit and HRU time-of-concentration values from landuse, topography, area, and basin lag settings.

## Bottom Line

time_conc_init computes weighted Manning's n values for each routing unit, then uses routing-unit area, slope, and field length to calculate routing-unit time of concentration. It also computes each HRU's overland travel time, channel travel time, total concentration time, and the runoff lag fraction stored in brt.

These results feed later surface-runoff and routing behavior: ru_tc holds subbasin concentration time, tconc and t_ov are used at the HRU scale, and brt determines how much runoff reaches the main channel after lag.

## Arguments

<!-- facts:arguments -->

## Where It Fits

This routine runs after proc_cha has finished setting up channel and landscape linkage. It initializes concentration-time and lag parameters before later runoff routing uses them to compute how quickly surface runoff reaches channels and how much is delayed.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. loop over routing units | For each routing unit, reset ru_n and accumulate a weighted Manning's n over its member elements. HRU elements contribute hru(ihru)%luse%ovn multiplied by hru(ihru)%km; a non-HRU element forces ru_n to 0.1. |
| 2. loop over routing units | For each routing unit, find its object record, convert object area from hectares to km2, normalize the weighted Manning's n by drainage area, and fetch the topography database index. Then compute overland travel time tov, channel slope, channel roughness, channel length, and routing-unit concentration time ru_tc as tov plus t_ch. |
| 3. loop over HRUs | For each HRU, read its topography and field database pointers, compute overland travel time t_ov from slope length, roughness, and slope, then compute channel slope, channel roughness, an assumed half-length channel length, and channel travel time t_ch. Sum them into tconc. |
| 4. branch on time step | Use a time-step-adjusted runoff lag fraction for subdaily simulations, otherwise use the daily form. Store the result in brt so later runoff routines can attenuate surface runoff reaching the channel. |
| 5. return | Exit after all routing-unit and HRU concentration-time values and runoff lag fractions have been initialized. |

## Modules Used

<!-- facts:uses -->

| Module | State touched | Key components |
| --- | --- | --- |
| [sym:ru_module] | `ru_n, ru, ru_tc, iru` | `ru(iru)%da_km2, ru(iru)%dbs%toposub_db, ru(iru)%field%length` |
| [sym:hru_module] | `hru, t_ov, tconc, brt, ihru` | `hru(ihru)%km, hru(ihru)%dbs%topo, hru(ihru)%dbs%field, hru(ihru)%luse%ovn, hru(ihru)%topo%slope` |
| [sym:hydrograph_module] | `sp_ob, ru_def, ru_elem, sp_ob1, ob` | `sp_ob%ru, ru_def(iru)%num_tot, ru_def(iru)%num(ii), ru_elem(ielem)%obtyp, ru_elem(ielem)%obtypno, sp_ob1%ru, ob(iob)%area_ha, sp_ob%hru` |
| [sym:topography_data_module] | `topo_db` | `topo_db(ith)%slope_len, topo_db(ith)%slope` |
| [sym:time_module] | `time` | `time%step, time%dtm` |
| [sym:basin_module] | `bsn_prm` | `bsn_prm%surlag` |

## Local Variables

<!-- facts:locals -->

## State Changes

| Target | When | Meaning |
| --- | --- | --- |
| `ru_n(iru)` | Inside the first routing-unit loop when an element belongs to the current RU; ru_n is reset before the loop and then set to 0.1 for any non-HRU element. | ru_n(iru) is built up from member HRU roughness values and, if a non-HRU routing element is encountered, the routine falls back to a default roughness contribution. The value is later normalized by drainage area. |
| `ihru` | Inside the HRU loop for every HRU in sp_ob%hru. | ihru is repeatedly reassigned to each HRU index so the routine can fetch topography, roughness, area, and database pointers for the current HRU. |
| `ru(iru)%da_km2` | At the start of the second routing-unit loop for each routing unit. | ru(iru)%da_km2 is set from the corresponding object area in hectares divided by 100 to express drainage area in km2, and that area is then used in the travel-time formulas. |
| `ru_tc(iru)` | After the routing-unit area and normalized roughness are available, once per routing unit. | ru_tc(iru) is assigned the sum of overland and channel travel times, giving the routing-unit time of concentration used by later routing behavior. |
| `t_ov(ihru)` | For every HRU during the HRU loop. | t_ov(ihru) stores the HRU overland-flow travel time derived from slope length, Manning's n, and slope, and is used as part of the HRU concentration-time calculation. |
| `tconc(ihru)` | For every HRU during the HRU loop, after t_ov and t_ch are computed. | tconc(ihru) stores the HRU total time of concentration as the sum of overland and channel travel times; later runoff handling uses this delay scale. |
| `brt(ihru)` | For every HRU during the runoff-lag branch, with a different formula chosen when time%step > 1. | brt(ihru) stores the fraction of surface runoff that reaches the main channel after lag, and later runoff routines use it to split delivered runoff from stored runoff. |

## File I/O

<!-- facts:io -->


## Theory Equations

| Eq. | Title | Formula | Implementation |
| --- | --- | --- | --- |
| 2:1.3.2 | Time of concentration | $t_{conc}=t_{ov}+t_{ch}$ | tconc = t_ov + t_ch. |
| 2:1.3.3 | Overland flow travel time | $t_{ov}=\frac{L_{slp}}{3600*v_{ov}}$ | t_ov = 0.0556*(Lslp*n)^0.6/(slope+0.0001)^0.3; equivalent to the documented hours form. |
| 2:1.3.4 | Overland flow velocity relation | $v_{ov}=\frac{q_{ov}^{0.4}*slp^{0.3}}{n^{0.6}}$ | Code uses the collapsed travel-time form rather than computing v_ov explicitly. |
| 2:1.3.5 | Overland flow velocity with qov assumption | $v_{ov}=\frac{0.005*L_{slp}^{0.4}*slp^{0.3}}{n^{0.6}}$ | The qov = 0.005*Lslp assumption is absorbed into the 0.0556 coefficient of the direct travel-time formula. |
| 2:1.3.6 | Collapsed overland-flow time formula | $t_{ov}=\frac{L_{slp}^{0.6}*n^{0.6}}{18*slp^{0.3}}$ | Directly uses the collapsed form for overland travel time. |
| 2:1.3.7 | Channel flow travel time | $t_{ch}=\frac{L_c}{3.6*v_c}$ | Code uses t_ch = 0.31*L*n^0.75/(Area^0.125*slope^0.375) at the HRU scale, equivalent to the documented form after its internal channel-length assumption. |
| 2:1.3.8 | Channel length from field geometry | $L_c=\sqrt{L*L_{cen}}$ | Instead of Lc = sqrt(L*Lcen), code assumes an HRU length-to-width ratio of 2 and uses ch_l = 0.5*sqrt(area_ha/2). |
| 2:1.3.9 | Channel length 0.71L approximation | $L_c=0.71*L$ | The current checkout does not use the 0.71*L approximation directly; it uses the area-based half-length assumption described in comments. |
| 2:1.3.10 | Channel velocity relation | $v_c=\frac{0.489*q_{ch}^{0.25}*slp_{ch}^{0.375}}{n^{0.75}}$ | Velocity is not computed explicitly; it is absorbed into the collapsed channel travel-time formula. |
| 2:1.3.12 | Channel discharge scaling with area | $q^*_{ch}=q^*_0*(100*Area)^{-0.5}$ | The Area^0.125 term in the travel-time equation is consistent with the documented discharge-scaling derivation, but qch is not formed explicitly. |
| 2:1.3.13 | Collapsed channel velocity formula | $v_c=\frac{0.317*Area^{0.125}*slp_{ch}^{0.375}}{n^{0.75}}$ | The code uses the final travel-time form rather than computing vc as a separate variable. |
| 2:1.3.14 | Collapsed channel travel time formula | $t_{ch}=\frac{0.62*L*n^{0.75}}{Area^{0.125}*slp_{ch}^{0.375}}$ | Uses the direct empirical form for channel travel time. |
| 2:1.4.1 | Surface runoff lag fraction | $Q_{surf}=(Q'_{surf}+Q_{stor,i-1})*(1-exp[\frac{-surlag}{t_{conc}}])$ | Verified against SWAT+ 62.0.0 (time_conc_init.f90:74). brt = 1.-Exp(-surlag/tconc)` — surface-runoff lag factor |

## Lineage

Resolved lineage commits show the routine was added in df07e3f with the full initialization logic for routing-unit roughness, concentration time, and runoff lag fraction. Later commits kept the same computation but refined details: 16e54aa changed the HRU channel-length assumption to 0.5*sqrt(area_ha/2), 39fabde initialized the local counters and real temporaries to zero, and f1e61a3 only corrected whitespace in the time-step-dependent brt expression.

- df07e3f introduced time_conc_init as a new subroutine that computes weighted RU Manning's n, RU and HRU time of concentration, and brt from basin lag.
- 16e54aa changed the HRU channel-length calculation from sqrt(area_ha/2.) to 0.5*sqrt(area_ha/2.), shortening the assumed channel distance used in t_ch and tconc.
- 39fabde added explicit zero initialization to ii, ielem, iob, ith, ifld, tov, ch_slope, ch_n, ch_l, and t_ch.
- f1e61a3 made no behavioral change; it only fixed indentation/tab formatting in the brt time-step branch.

## Review Notes

- No direct file I/O was extracted for this procedure.
- warning: missing_doc: Procedure 'time_conc_init' has no extracted documentation comment.
