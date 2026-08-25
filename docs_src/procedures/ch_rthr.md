---
kind: procedure
symbol: ch_rthr
title: ch_rthr
status: filled
source_hash: 6f8b2b261df5e947
version_label: SWAT+ 62.0.0
locals:
  ii: Loop counter for the subdaily routing steps within the day. It indexes the current inflow
    sample and the matching output slot in the hydrograph arrays.
  jrch: Reach index copied from isdch so the routine can access the current routed channel's
    parameter and rating-curve data.
  scoef: Storage coefficient used in the variable-storage routing equation. It is computed
    from the time step length and the interpolated travel time, then used to convert current
    reach volume into routed outflow.
  vol: Running volume of water stored in the reach during the day. It accumulates inflow each
    substep, is reduced by routed losses/outflow, and becomes the basis for the routed discharge
    calculation.
  topw: Computed channel surface width at the current water depth. It is used to estimate
    evaporation loss from the wetted water surface when routed outflow remains.
  inflo_rate: Current subdaily inflow converted from volume per time step to flow rate. It
    is used to locate the active point on the reach rating curve.
  ttime: Interpolated travel time for the current inflow condition. It feeds the storage coefficient
    calculation that determines routed outflow.
  t_inc: Length of one routing increment in hours, computed from time%step. It normalizes
    the travel-time-based storage coefficient.
  outflo: Current routed outflow volume for the time step. It starts as the storage-routed
    outflow and is then reduced by transmission loss and evaporation.
  tl: Transmission-loss volume for the current time step. It is computed from channel conductivity,
    length, and wetted perimeter, then subtracted from routed outflow.
  trans_loss: Daily accumulator for total transmission losses across all subdaily steps. It
    sums the stepwise tl values for the day.
  ev: Evaporation loss volume for the current time step. It is computed from reach evaporation
    factor, potential ET, channel length, and water-surface width.
  evap: Daily accumulator for total evaporation losses across all subdaily steps. It sums
    the stepwise ev values for the day.
  rto: Interpolation ratio used to blend between rating-curve points or extrapolate beyond
    the highest point. It determines the mixed rating-curve state assigned to rcurv.
  outflo_sum: Accumulator for the total routed outflow volume over the day. It sums the final
    outflow from each subdaily step.
  iwst: Weather-station index used to fetch potential evapotranspiration. This routine sets
    it to 1 before reading wst(iwst)%weat%pet.
  ielev: Loop index over the four rating-curve elevation points. It is used to find the two
    bracketing points for interpolation or the highest-point extrapolation case.
uses:
  basin_module: bsn_prm%evrch supplies the basin-wide reach-evaporation adjustment factor.
    ch_rthr multiplies this factor by potential ET, channel length, and surface width to compute
    evaporation losses from routed flow.
  climate_module: wst(iwst)%weat%pet provides the potential evapotranspiration used in the
    stepwise evaporation calculation. Without the climate module's daily PET value, the routine
    could not estimate reach evaporation loss.
  channel_data_module: channel_data_module is the place the routine gets the current reach's
    channel setup and rating-curve structures. Those data define the geometry, flow thresholds,
    and stored volumes used to interpolate routing behavior and compute losses.
  time_module: time%step determines how many subdaily routing iterations run and the duration
    of each increment. The routing coefficient, inflow conversion, loss formulas, and daily
    accumulators all depend on this step length.
  channel_module: jhyd is the identifier for the current hydrology data set associated with
    the active reach. ch_rthr loads it from sd_dat(jrch)%hyd so the routine stays aligned
    with the correct reach-specific input configuration.
  hydrograph_module: ob(icmd)%tsin(ii) is the incoming subdaily flow hydrograph and ob(icmd)%hyd_flo(1,ii)
    is where the routed outflow is written back. ch_rthr reads the inflow sample for each
    time step and stores the processed routed discharge in the same object.
  sd_channel_module: sd_channel_module holds the reach rating-curve parameters, channel properties,
    and output arrays that define the routing calculation. ch_rthr uses those fields to interpolate
    geometry, compute travel time, calculate hydraulic radius and flow depth, and write stepwise
    routed flows.
---

<!-- facts:header -->

Routes subdaily flow through a channel reach with a variable-storage coefficient method. It interpolates a reach rating curve, then updates routed outflow, transmission loss, evaporation, and channel storage for each time step.

## Bottom Line

ch_rthr is the subdaily channel-routing routine for a reach. For each time step in the day, it converts the inflow hydrograph to a flow rate, finds the matching point on the reach rating curve, interpolates reach geometry and travel time, and then routes water with a variable-storage coefficient formulation.

While routing, it also subtracts transmission losses and evaporation from the routed outflow, updates the remaining channel storage, and stores the resulting subdaily routed flow in ob(icmd)%hyd_flo(1,ii).

## Arguments

<!-- facts:arguments -->

## Where It Fits

This routine runs during subdaily channel routing after the current reach index and its hydrology setup have been established in the shared module state. It reads the reach's rating curve and inflow hydrograph, then produces routed subdaily outflow that downstream channel or hydrograph accounting uses in the rest of the simulation.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. Set the active reach and reset daily accumulators. | The routine copies the current reach index from isdch, loads the associated hydrology dataset identifier from sd_dat(jrch)%hyd, clears daily loss and flow totals, zeros hyd_rad and vol, and initializes the current rating-curve state from ch_rcurv(jrch)%out2. |
| 2. Loop over the day's subdaily time steps. | The routine processes each inflow sample in the day one step at a time, using time%step to define how many subdaily increments are routed. |
| 3. Convert the inflow sample to a flow rate and add it to reach storage. | For the current time step, the routine converts ob(icmd)%tsin(ii) from volume per step to m3/s as inflo_rate, adds the inflow volume to the running reach storage vol, and keeps vol from dropping below a tiny positive value. |
| 4. Find the rating-curve interval that brackets the current inflow. | The routine scans the four rating-curve elevation points and compares inflo_rate to each flo_rate threshold. If the inflow is below the first point, it scales the first curve point directly; if it falls between two points, it interpolates with chrc_interp; if it exceeds the highest point, it extrapolates from the fourth point and reduces travel time proportionally. During this search it also stores hyd_rad(ii), trav_time(ii), and flo_dep(ii) from the interpolated curve state. |
| 5. Route flow with the variable-storage coefficient when the reach is active. | If the interpolated curve has positive flo_rate, the routine uses its travel time to compute t_inc and scoef, then calculates routed outflow as outflo = scoef * vol, capping scoef at 1 and zeroing negligible outflow. |
| 6. Subtract transmission loss from the routed outflow. | The routine computes tl from channel conductivity, channel length, wetted perimeter, and time-step length, limits tl to the available outflow, subtracts it from outflo, and adds it to the daily transmission-loss total. |
| 7. Compute evaporation loss when water remains after transmission loss. | If routed outflow is still positive, the routine computes channel top width from the current depth and channel geometry, reads PET from wst(1)%weat%pet, scales it by bsn_prm%evrch and channel length, limits the resulting ev to the available outflow, and subtracts it from outflo while accumulating the daily evaporation total. |
| 8. Save the step result back to storage and the outflow hydrograph. | After losses are applied, the routine reduces reach storage by the final routed outflow, writes the result to ob(icmd)%hyd_flo(1,ii), and accumulates outflo_sum for the day. |

## Modules Used

<!-- facts:uses -->

| Module | State touched | Key components |
| --- | --- | --- |
| [sym:basin_module] | `bsn_prm` | `bsn_prm%evrch` |
| [sym:climate_module] | `wst` | `wst(iwst)%weat%pet` |
| [sym:channel_data_module] | `sd_dat, ch_rcurv, rcurv, sd_ch, hyd_rad, trav_time, flo_dep` | `sd_dat(jrch)%hyd, ch_rcurv(jrch)%out2, ch_rcurv(jrch)%elev(ielev)%flo_rate, ch_rcurv(jrch)%elev(ielev), rcurv%ttime, ch_rcurv(jrch)%elev(ielev)%ttime, ch_rcurv(jrch)%elev(ielev-1)%flo_rate, ch_rcurv(jrch)%elev(ielev-1), rcurv%xsec_area, rcurv%wet_perim, rcurv%dep, rcurv%flo_rate, ch_rcurv(jrch)%in2%vol, ch_rcurv(jrch)%out1%vol, rcurv%vol_fp, rcurv%vol_ch, sd_ch(jrch)%chk, sd_ch(jrch)%chl, sd_ch(jrch)%chd, ch_rcurv(jrch)%wid_btm, sd_ch(jrch)%chss, sd_ch(jrch)%chw` |
| [sym:time_module] | `time` | `time%step` |
| [sym:channel_module] | `jhyd` |  |
| [sym:hydrograph_module] | `ob, isdch, icmd` | `ob(icmd)%tsin(ii), ob(icmd)%hyd_flo(1,ii)` |
| [sym:sd_channel_module] | `sd_dat, ch_rcurv, rcurv, sd_ch, hyd_rad, trav_time, flo_dep` | `sd_dat(jrch)%hyd, ch_rcurv(jrch)%out2, ch_rcurv(jrch)%elev(ielev)%flo_rate, ch_rcurv(jrch)%elev(ielev), rcurv%ttime, ch_rcurv(jrch)%elev(ielev)%ttime, ch_rcurv(jrch)%elev(ielev-1)%flo_rate, ch_rcurv(jrch)%elev(ielev-1), rcurv%xsec_area, rcurv%wet_perim, rcurv%dep, rcurv%flo_rate, ch_rcurv(jrch)%in2%vol, ch_rcurv(jrch)%out1%vol, rcurv%vol_fp, rcurv%vol_ch, sd_ch(jrch)%chk, sd_ch(jrch)%chl, sd_ch(jrch)%chd, ch_rcurv(jrch)%wid_btm, sd_ch(jrch)%chss, sd_ch(jrch)%chw` |

## Local Variables

<!-- facts:locals -->

## State Changes

| Target | When | Meaning |
| --- | --- | --- |
| `jhyd` | At routine entry, jhyd is set from sd_dat(jrch)%hyd after jrch is copied from isdch. | The routine switches to the hydrology file/index associated with the active reach so later routing logic uses the correct reach-specific configuration. |
| `hyd_rad` | hyd_rad(ii) is assigned inside the rating-curve search after rcurv has been set for the current inflow condition. | It records the hydraulic radius implied by the interpolated curve state for this subdaily step. |
| `rcurv` | rcurv is initialized from ch_rcurv(jrch)%out2 at the start of the day and then replaced during the inflow-bracketing logic for each subdaily step. | It holds the current interpolated rating-curve state that supplies flow geometry, volume, and travel-time information for routing. |
| `rcurv%ttime` | rcurv%ttime is copied from the active rating-curve point, interpolated through chrc_interp, or adjusted in the above-highest-point extrapolation branch. | It stores the travel time for the current inflow condition, which controls the storage coefficient used to compute routed outflow. |
| `hyd_rad(ii)` | hyd_rad(ii) is updated whenever the routine finds a valid rating-curve state for the current inflow step. | It captures the hydraulic radius corresponding to the current flow depth and wetted perimeter so later model logic can refer to the step's channel hydraulics. |
| `trav_time(ii)` | trav_time(ii) is updated alongside hyd_rad(ii) after the routine identifies the current rating-curve state. | It records the stepwise travel time derived from the rating curve for diagnostic or downstream use. |
| `flo_dep(ii)` | flo_dep(ii) is updated alongside the other stepwise hydraulic summaries after the rating-curve state is chosen. | It records the flow depth for the current subdaily inflow condition. |
| `ch_rcurv(jrch)%in2%vol` | ch_rcurv(jrch)%in2%vol is set when the routine enters the variable-storage routing block with positive rcurv%flo_rate. | It stores the current-step inflow volume added to the previous outflow storage for the reach's current inflow state. |
| `ob(icmd)%hyd_flo(1,ii)` | ob(icmd)%hyd_flo(1,ii) is assigned after transmission loss and evaporation are removed from outflo. | It saves the final routed subdaily outflow for the current hydrograph object and time step so later model components can use the routed discharge. |

## File I/O

<!-- facts:io -->


## Theory Equations

| Eq. | Title | Formula | Implementation |
| --- | --- | --- | --- |
| 4:1 | Flood-plain bottom width W_btm,fld = 5*W_bnkfull | $W_{btm,fld}=5*W_{bnkfull}$ | topw=5.*sd_ch%chw+8.*(dep-chd) at line 162 computes flood-plain top width when flow exceeds bankfull; 5*chw is the 5:1 floodplain-to-channel width ratio. CSV collision: equation_id '4:1' was assigned in the section-7 Channel Characteristics page and conflicts with the chapter-4 numbering scheme (duplicate_equation_id=True in CSV). |
| 2:1.5.3 | Transmission-loss adjusted peak runoff | $q_{peak,f}=\frac{1}{(3600*dur_{flw})}*[a_x-(1-b_x)*vol_{Qsurf,i}]+b_x*q_{peak,i}$ | Verified against SWAT+ 62.0.0 (ch_rthr.f90:151). code uses conductance loss `tl=chk·chl·wet_perim·24/step`, NOT the Lane a_x/b_x peak-flow regression |

## Lineage

`ch_rthr.f90` was introduced in `df07e3f` (2024-03-05, "init all") and has been changed in 7 non-merge commit(s) since, most recently `bd18ad4` (2025-11-24, "Pr 107 (#108)"). Lineage is reconstructed from commit metadata (SHA, date, subject); per-line diffs were unavailable in this build environment, so only the commits touching `ch_rthr.f90` are listed.

- `bd18ad4` (2025-11-24) — Pr 107 (#108)
- `fd90e36` (2025-02-06) — variable initialization changes
- `889136d` (2025-02-03) — Fix typos
- `f1e61a3` (2024-10-08) — fixed tabs
- `39fabde` (2024-08-08) — Initialized varables with python script, corrected input data where integers where floats in two input files, trapped underflow errors in th…
- `df07e3f` (2024-03-05) — init all

## Review Notes

- No direct file I/O was extracted for this procedure.
- warning: missing_doc: Procedure 'ch_rthr' has no extracted documentation comment.
- Lineage was reconstructed from file-level commit metadata; per-line diffs were unavailable in this environment (blobless clone), so line-span filtering was not applied.
