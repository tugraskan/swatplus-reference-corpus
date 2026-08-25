---
kind: procedure
symbol: ch_rtmusk
title: ch_rtmusk
status: filled
source_hash: b44523d66261e46f
version_label: SWAT+ 62.0.0
locals:
  qman: Declared as an external real function, but it is not referenced in the visible source
    span, so its role here is uncertain from this routine alone.
  theta: Declared as an external real function, but it is not referenced in the visible source
    span, so its role here is uncertain from this routine alone.
  ii: Loop counter for the subdaily routing steps in the main time-step loop.
  ihru: Indexes floodplain HRUs while accumulating wetland storage at the start and end of
    the day.
  iihru: Holds the actual HRU index pulled from `sd_ch(jrch)%fp%hru(ihru)` so the routine
    can access the matching wetland storage and wetland evolution state.
  icha: Channel index passed to `rcurv_interp_flo`; set equal to `jrch` before interpolating
    the rating curve.
  irtstep: Subdaily hydrograph step index used to read `ob(icmd)%tsin` and write `ob(icmd)%hyd_flo(1,irtstep)`.
  isubstep: Counts substeps within a routing step so the routine can advance `irtstep` when
    the configured substep count is exceeded.
  ch_stor_init: Channel storage at the beginning of the day, saved for the end-of-day water-balance
    comparison.
  fp_stor_init: Floodplain storage above the emergency spillway at the beginning of the day,
    saved for the daily balance.
  wet_stor_init: Wetland storage at the beginning of the day, saved for the daily balance
    check.
  tot_stor_init: Initial total channel-plus-floodplain storage used in the water-balance summary.
  inout: Daily inflow minus outflow minus losses, used as a simple balance check.
  del_stor: Change in channel + floodplain + wetland storage over the day, computed for the
    water-balance summary.
  topw: Top width of the main channel used to compute evaporation loss area.
  qinday: Daily inflow accumulator; it is initialized here but not otherwise used in the visible
    span.
  qoutday: Daily outflow accumulator; it is initialized here but not otherwise used in the
    visible span.
  inflo: Subdaily inflow volume entering the reach during the current routing step.
  inflo_rate: Inflow converted to a flow rate for rating-curve interpolation.
  outflo: Routed outflow volume for the current subdaily step.
  trans_loss: Transmission-loss volume removed from channel storage after routing.
  evap: Evaporation-loss volume removed from channel storage after routing.
  rto: Fraction of current storage removed by inflow, outflow, losses, or redistribution;
    reused for several proportional updates.
  outflo_rate: Outflow converted to a rate for interpolating the outgoing rating curve.
  dts: Substep duration in seconds, derived from `time%dtm` and `sd_ch(jrch)%msk%substeps`.
  dthr: Substep duration in hours, derived from `dts`.
  scoef: Storage coefficient used by the variable-storage routing branch.
  sum_inflo: Sum of all inflow hydrograph entries for the day.
  sum_outflo: Daily outflow total accumulated in `ht2%flo`.
  wet_evol: Accumulator for wetland emergency-spillway volume evolution across floodplain
    HRUs.
uses:
  basin_module: '`basin_module` supplies the basin routing control flags and reach-evaporation
    parameter that decide whether the routine uses Muskingum routing or the variable-storage
    branch, whether groundwater flow is active, and how strongly channel PET is converted
    into evaporation loss.'
  channel_data_module: '`channel_data_module` is the intended source of channel and routing
    data referenced by this procedure, but the extracted candidate references for this span
    were owned by other modules; this matters because the routine needs reach-specific channel
    geometry and routing parameters to compute storage, routing coefficients, and losses.'
  channel_module: '`channel_module` matters because it provides `jhyd`, the channel hydraulic
    index used to select and maintain reach-related hydraulic state in this routing workflow.'
  hydrograph_module: '`hydrograph_module` provides the mutable hydrograph and storage objects
    that `ch_rtmusk` reads, updates, and writes back: inflow hydrographs, routed outflow,
    channel/floodplain/wetland storage, and the daily channel-floodplain water-balance record.'
  time_module: '`time_module` supplies the simulation step size and step count that determine
    whether the routine runs as daily routing or subdaily routing and how substep duration
    is computed.'
  channel_velocity_module: '`channel_velocity_module` is imported by the routine but no resolved
    external symbols from that module appear in the extracted span, so its direct effect here
    cannot be confirmed from the provided evidence.'
  sd_channel_module: '`sd_channel_module` holds the SWAT-DEG channel configuration, Muskingum
    coefficients, rating-curve objects, and geometry values that drive the routing method
    and loss calculations in this routine.'
  climate_module: '`climate_module` supplies the weather station PET value used to compute
    channel evaporation losses.'
  reservoir_module: '`reservoir_module` supplies wetland capacity information through `wet_ob(iihru)%evol`,
    which is accumulated when the routine builds wetland storage for the daily balance check.'
  reservoir_data_module: '`reservoir_data_module` is imported, but no resolved symbols from
    it appear in the extracted span, so its direct contribution here is not visible in the
    provided evidence.'
  water_body_module: '`water_body_module` provides the channel water-body accounting fields
    for evaporation and seepage. Those fields are reset and then populated so the routine
    can report channel losses separately from the hyd_output storage objects.'
  conditional_module: '`conditional_module` is imported, but no resolved symbols from it appear
    in the extracted span, so its direct role here cannot be confirmed from the provided evidence.'
---

<!-- facts:header -->

Routes daily and subdaily reach flow with Muskingum or variable-storage coefficient methods, then applies transmission loss, evaporation, and storage bookkeeping.

## Bottom Line

`ch_rtmusk` is the channel routing routine used for a SWAT+ reach. It takes the current reach inflow hydrograph, runs it through either Muskingum routing or a variable-storage coefficient update, and then updates the reach hydrograph, channel storage, floodplain storage, and wetland-related bookkeeping.

After routing, it subtracts transmission losses and evaporation from channel storage and records a daily water-balance summary in `ch_fp_wb`. The results feed later channel, sediment, and water-quality calculations through the updated hydrograph and storage state.

## Arguments

<!-- facts:arguments -->

## Where It Fits

`sd_channel_control3` calls `ch_rtmusk` after `sd_channel_sediment3` and after it has reset `ht2 = hz`, so the routing routine receives a clean hydrograph/storage state for the current day. Its results then feed later channel-water-quality work, including `ch_rtpest`, and the updated routed flow is retained in `ob(icmd)%hyd_flo` and the storage arrays for subsequent model steps.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. Initialize reach, hydrograph, and balance state | Set `jrch` from `isdch`, select the hydraulic data index with `sd_dat(jrch)%hyd`, zero the daily hydrograph and loss accumulators, copy `hz` into `ht2`, and build the starting wetland storage from `wet(iihru)` and `wet_ob(iihru)%evol`. |
| 2. Set routing timestep controls | If the simulation is on the first time step, force the Muskingum step counts to daily routing. Then initialize the subdaily step counters and compute the substep duration in seconds and hours. |
| 3. Loop over subdaily routing steps | Advance the substep counter, roll `irtstep` when the configured substep count is exceeded, and prepare to route one subdaily inflow/outflow update. |
| 4. Add inflow to total storage when water is present | If `ht1%flo` is nonzero, derive the current inflow volume from `ob(icmd)%tsin(irtstep)`, compute the inflow-to-total-storage ratio, and add that proportional inflow to `tot_stor(jrch)`. |
| 5. Interpolate the inflow rating curve | Set `icha = jrch`, convert inflow to a rate, call `rcurv_interp_flo`, and save the returned curve in `ch_rcurv(jrch)%in2`. |
| 6. Skip routing when storage is empty | If total storage is essentially zero, clear the rating-curve history and set the previous inflow and outflow volumes to zero so the next step starts from an empty state. |
| 7. Route by Muskingum or variable storage coefficient | Use Muskingum coefficients when `bsn_cc%rte == 1`; otherwise compute a storage coefficient from `bsn_prm%scoef` and channel travel times, then calculate routed outflow from total storage. |
| 8. Interpolate the outgoing rating curve and update routed flow | Convert routed outflow to a rate, call `rcurv_interp_flo` again, store the result in `ch_rcurv(jrch)%out2`, add routed volume to `ht2` and `ob(icmd)%hyd_flo(1,irtstep)`, and remove the routed fraction from `tot_stor(jrch)`. |
| 9. Carry rating curves forward and split channel versus floodplain storage | Copy the current in/out rating curves into the previous-step slots, then partition total storage into channel and floodplain storage using the bankfull volume in `ch_rcurv(jrch)%elev(2)%vol_ch`. |
| 10. Compute transmission loss from channel storage | If channel storage remains, compute seepage/transmission loss from channel conductivity, length, and width, cap it at channel storage, subtract it proportionally from `ch_stor(jrch)`, and record the loss in `ch_wat_d(ich)%seep` when groundwater flow is inactive. |
| 11. Compute channel evaporation loss | If channel storage remains, derive `topw` from channel geometry, read PET from `wst(iwst)%weat%pet`, compute evaporation with `bsn_prm%evrch`, cap it at channel storage, subtract it proportionally from `ch_stor(jrch)`, and store the result in `ch_wat_d(ich)%evap`. |
| 12. Recompute total storage and end-of-day balance | Rebuild `tot_stor(jrch)` from channel and floodplain storage, compute the daily inflow-outflow-loss check in `inout`, rebuild end-of-day wetland storage, and compute `del_stor` as the combined storage change across channel, floodplain, and wetland components. |
| 13. Publish channel-floodplain water-balance outputs | Store the daily inflow, outflow, transmission loss, evaporation, and initial/final storage values in `ch_fp_wb(jrch)` so later routines can inspect the routing balance. |
| 14. Return to caller | Exit the subroutine after updating all routing and water-balance state. |

## Modules Used

<!-- facts:uses -->

| Module | State touched | Key components |
| --- | --- | --- |
| [sym:basin_module] | `bsn_cc, bsn_prm` | `bsn_cc%rte, bsn_prm%scoef, bsn_cc%gwflow, bsn_prm%evrch` |
| [sym:channel_data_module] | `sd_dat, sd_ch, ch_rcurv, rcurv, rcz` | `sd_dat(jrch)%hyd, sd_ch(jrch)%fp%hru_tot, sd_ch(jrch)%fp%hru(ihru), sd_ch(jrch)%msk%nsteps, sd_ch(jrch)%msk%substeps, sd_ch(jrch)%in1_vol, sd_ch(jrch)%out1_vol, sd_ch(jrch)%msk%c1, sd_ch(jrch)%msk%c2, sd_ch(jrch)%msk%c3, sd_ch(jrch)%chk, sd_ch(jrch)%chl, sd_ch(jrch)%chw, ch_rcurv(jrch)%in2, ch_rcurv(jrch)%in1, ch_rcurv(jrch)%out1, ch_rcurv(jrch)%out2, ch_rcurv(jrch)%elev(2)%vol_ch, ch_rcurv(jrch)%in2%ttime, ch_rcurv(jrch)%out1%ttime, rcurv%wet_perim, rcz` |
| [sym:channel_module] | `jhyd` |  |
| [sym:hydrograph_module] | `ob, wet_stor, ch_stor, fp_stor, ht1, tot_stor, ht2, ch_fp_wb, wet, jrch, isdch, hz, icmd` | `ob(icmd)%hyd_flo, ob(icmd)%tsin, wet_stor(jrch)%flo, ch_stor(jrch)%flo, fp_stor(jrch)%flo, ht1%flo, ob(icmd)%tsin(irtstep), tot_stor(jrch)%flo, ob(icmd)%hyd_flo(1,irtstep), ob(icmd)%wst, ht2%flo, ch_fp_wb(jrch)%inflo, ch_fp_wb(jrch)%outflo, ch_fp_wb(jrch)%tl, ch_fp_wb(jrch)%ev, ch_fp_wb(jrch)%ch_stor_init, ch_fp_wb(jrch)%ch_stor, ch_fp_wb(jrch)%fp_stor_init, ch_fp_wb(jrch)%fp_stor, ch_fp_wb(jrch)%tot_stor_init, ch_fp_wb(jrch)%tot_stor, ch_fp_wb(jrch)%wet_stor_init, ch_fp_wb(jrch)%wet_stor` |
| [sym:time_module] | `time` | `time%step, time%dtm` |
| [sym:channel_velocity_module] | `No candidate outside references were resolved to this module.` |  |
| [sym:sd_channel_module] | `sd_dat, sd_ch, ch_rcurv, rcurv` | `sd_dat(jrch)%hyd, sd_ch(jrch)%fp%hru_tot, sd_ch(jrch)%fp%hru(ihru), sd_ch(jrch)%msk%nsteps, sd_ch(jrch)%msk%substeps, ch_rcurv(jrch)%in2, ch_rcurv(jrch)%in1, ch_rcurv(jrch)%out1, sd_ch(jrch)%in1_vol, sd_ch(jrch)%out1_vol, sd_ch(jrch)%msk%c1, sd_ch(jrch)%msk%c2, sd_ch(jrch)%msk%c3, ch_rcurv(jrch)%in2%ttime, ch_rcurv(jrch)%out1%ttime, ch_rcurv(jrch)%out2, ch_rcurv(jrch)%elev(2)%vol_ch, sd_ch(jrch)%chk, sd_ch(jrch)%chl, rcurv%wet_perim, sd_ch(jrch)%chw` |
| [sym:climate_module] | `wst` | `wst(iwst)%weat%pet` |
| [sym:reservoir_module] | `wet_ob` | `wet_ob(iihru)%evol` |
| [sym:reservoir_data_module] | `No candidate outside references were resolved to this module.` |  |
| [sym:water_body_module] | `ch_wat_d` | `ch_wat_d(jrch)%evap, ch_wat_d(jrch)%seep, ch_wat_d(ich)%seep, ch_wat_d(ich)%evap` |
| [sym:conditional_module] | `No candidate outside references were resolved to this module.` |  |

## Local Variables

<!-- facts:locals -->

## State Changes

| Target | When | Meaning |
| --- | --- | --- |
| `jrch` | At the start of the routine, `jrch = isdch`. | `jrch` is set to the current routed reach so all subsequent storage, rating-curve, and balance updates apply to the active channel element. |
| `jhyd` | Immediately after `jrch` is set, `jhyd = sd_dat(jrch)%hyd`. | `jhyd` selects the hydraulic data source for the active reach; this lets the routing routine use the channel-specific hydraulic setup tied to `sd_dat`. |
| `ht2` | After the subdaily routing loop, `ht2` has been accumulated with routed outflow via `ht2 = ht2 + rto * tot_stor(jrch)`. | `ht2` becomes the day’s routed outflow hydrograph total, reflecting the flow volume returned to the caller after all substeps are processed. |
| `ob(icmd)%hyd_flo` | Inside the routing loop, after outflow is computed, `ob(icmd)%hyd_flo(1,irtstep) = ob(icmd)%hyd_flo(1,irtstep) + outflo`. | The subdaily hydrograph entry for the current time step is incremented by the routed outflow so downstream routines see the updated channel discharge. |
| `hyd_rad` | Before any routing work, `hyd_rad = 0.`. | `hyd_rad` is cleared at the start of the routine so any prior hydraulic-geometry accumulation does not leak into the current day’s calculation. |
| `trav_time` | Before any routing work, `trav_time = 0.`. | `trav_time` is cleared at the start of the routine so the current day’s routing does not inherit a previous travel-time value. |
| `flo_dep` | Before any routing work, `flo_dep = 0.`. | `flo_dep` is reset so flood-depth accounting starts fresh for the current routing pass. |
| `ch_wat_d(jrch)%evap` | During the post-routing loss section, if `ch_stor(jrch)%flo > 1.e-6`, evaporation is computed from PET and channel surface width. | `ch_wat_d(jrch)%evap` records the channel evaporation loss for the day so water-body accounting can report it separately from storage objects. |
| `ch_wat_d(jrch)%seep` | During the post-routing loss section, if `ch_stor(jrch)%flo > 1.e-6`, transmission loss is computed and then assigned to seepage when groundwater flow is inactive. | `ch_wat_d(jrch)%seep` records the channel seepage/transmission loss for the day when `bsn_cc%gwflow == 0`; otherwise it is forced to zero because groundwater flow will handle seepage elsewhere. |
| `wet_stor(jrch)` | At the beginning of the day `wet_stor(jrch) = hz` and then each floodplain HRU contributes `wet(iihru)`; it is recomputed again near day end from the same HRU loop. | `wet_stor(jrch)` captures wetland storage at both the start and end of the day so `del_stor` can include wetland changes in the balance. |
| `sd_ch(jrch)%msk%nsteps` | If `time%step == 1`, the routine forces `sd_ch(jrch)%msk%nsteps = 1`; otherwise it keeps the existing value. | `sd_ch(jrch)%msk%nsteps` controls how many subdaily routing iterations occur; forcing it to 1 on daily runs disables extra routing substeps. |
| `sd_ch(jrch)%msk%substeps` | If `time%step == 1`, the routine forces `sd_ch(jrch)%msk%substeps = 1`; otherwise it keeps the existing value. | `sd_ch(jrch)%msk%substeps` controls the substep resolution used to split inflow for stable routing; setting it to 1 makes daily routing operate without subdivision. |
| `tot_stor(jrch)` | After routing and storage partitioning, `tot_stor(jrch) = ch_stor(jrch) + fp_stor(jrch)`. | `tot_stor(jrch)` is refreshed so it always reflects the current combined channel and floodplain storage after routing and losses. |
| `ch_rcurv(jrch)%in2` | When `tot_stor(jrch)%flo` is nonzero, `ch_rcurv(jrch)%in2 = rcurv` after inflow interpolation. | `ch_rcurv(jrch)%in2` stores the current inflow rating curve, which is needed when the next step computes time-dependent storage routing. |
| `ch_rcurv(jrch)%in1` | After the outflow rating-curve interpolation, `ch_rcurv(jrch)%in1 = ch_rcurv(jrch)%in2`. | `ch_rcurv(jrch)%in1` becomes the previous-step inflow rating curve so the next routing step can use it as history. |
| `ch_rcurv(jrch)%out1` | After the outflow rating-curve interpolation, `ch_rcurv(jrch)%out1 = ch_rcurv(jrch)%out2`. | `ch_rcurv(jrch)%out1` becomes the previous-step outflow rating curve so the next step can reference the last routed hydraulic condition. |
| `sd_ch(jrch)%in1_vol` | After outflow is computed, `sd_ch(jrch)%in1_vol = inflo`. | `sd_ch(jrch)%in1_vol` stores the current inflow volume as the Muskingum history term for the next step. |
| `sd_ch(jrch)%out1_vol` | After outflow is computed, `sd_ch(jrch)%out1_vol = outflo`. | `sd_ch(jrch)%out1_vol` stores the current outflow volume as the Muskingum history term for the next step. |
| `ch_rcurv(jrch)%out2` | After the outflow rating-curve interpolation, `ch_rcurv(jrch)%out2 = rcurv`. | `ch_rcurv(jrch)%out2` stores the current outflow rating curve, which is then copied to the history slot for the next step. |
| `ob(icmd)%hyd_flo(1,irtstep)` | For each subdaily routing step, `ob(icmd)%hyd_flo(1,irtstep)` is incremented by `outflo`. | The current hydrograph slot receives the routed outflow so the daily and subdaily discharge record carries the updated reach flow. |
| `fp_stor(jrch)` | If `tot_stor(jrch)%flo > ch_rcurv(jrch)%elev(2)%vol_ch`, storage is split and `fp_stor(jrch)` receives the excess above bankfull. | `fp_stor(jrch)` holds the floodplain storage above bankfull so the routine can preserve overbank water separately from in-channel storage. |
| `ch_stor(jrch)` | If `tot_stor(jrch)%flo <= ch_rcurv(jrch)%elev(2)%vol_ch`, `ch_stor(jrch)` is set to the whole total storage; otherwise it is reduced to the bankfull portion. | `ch_stor(jrch)` keeps the in-channel portion of storage after routing so later loss calculations operate on channel water only. |
| `ch_wat_d(ich)%seep` | When groundwater flow is inactive, `ch_wat_d(ich)%seep = trans_loss`; otherwise it is set to zero. | `ch_wat_d(ich)%seep` records the channel seepage/transmission-loss amount that should be exposed to the water-body accounting when gwflow is not handling it. |
| `iwst` | `iwst = ob(icmd)%wst` immediately before evaporation is computed. | `iwst` selects the weather station whose PET drives channel evaporation for the current object connection. |

## File I/O

<!-- facts:io -->


## Theory Equations

| Eq. | Title | Formula | Implementation |
| --- | --- | --- | --- |
| 7:1.4.3 | Muskingum routed outflow | $q_{out,2}=C_1*q_{in,2}+C_2*q_{in,1}+C_3*q_{out,1}$ | Verified against SWAT+ 62.0.0 (ch_rtmusk.f90:141). outflo = c1*inflo + c2*in1_vol + c3*out1_vol |
| 7:1.4.7 | Muskingum routed outflow volume form | $V_{out,2}=C_1*V_{in,2}+C_2*V_{in,1}+C_3*V_{out,1}$ | Verified against SWAT+ 62.0.0 (ch_rtmusk.f90:141). volume form (same line) |
| 7:1.6.1 | Evaporation losses | $E_{ch}=coef_{ev}*E_o*L_{ch}*W*fr_{\Delta t}$ | Verified against SWAT+ 62.0.0 (ch_rtmusk.f90:220). evap = evrch*pet*topw/1000. |
| 7:1.7.1 | Bank-storage inflow from transmission losses | $bnk_{in}=tloss*(1-fr_{trns})$ | Transmission loss is removed from channel storage and reported as seepage, but the code does not split it into a bank-storage inflow term with a fr_trns factor. |
| 7:1.7.3 | Maximum bank revaporation | $bnk_{revap,mx}=\beta_{rev}*E_o*L_{ch}*W$ | Channel evaporation is computed directly from PET and surface area; there is no separate bank-storage revaporation cap term. |
| 7:1.7.4 | Bank storage below revaporation cap branch | $bnk_{revap}=bnk$ | No conditional branch comparing bank storage against a revaporation maximum is present in the routine. |
| 7:1.7.5 | Bank storage above revaporation cap branch | $bnk_{revap}=bnk_{revap,mx}$ | The code does not implement the complementary capped bank-revaporation branch either; bank storage is not modeled as a separate revaporation reservoir here. |
| 7:1.4.10 | Storage time constant from length and celerity | $K=\frac{1000*L_{ch}}{c_k}$ | Verified against SWAT+ 62.0.0 (ch_rtmusk.f90). (Muskingum K=1000L/ck) |
| 7:1.4.9 | Muskingum storage-time constant | $K=coef_1*K_{bnkfull}+coef_2*K_{0.1bnkfull}$ | Verified against SWAT+ 62.0.0 (ch_rtmusk.f90). (Muskingum K weighting) |

## Lineage

`ch_rtmusk.f90` was introduced in `df07e3f` (2024-03-05, "init all") and has been changed in 15 non-merge commit(s) since, most recently `b9df6cf` (2026-04-01, "gwflow re-merge: host file guards, ch_temp component mixing restoration"). Lineage is reconstructed from commit metadata (SHA, date, subject); per-line diffs were unavailable in this build environment, so only the commits touching `ch_rtmusk.f90` are listed.

- `b9df6cf` (2026-04-01) — gwflow re-merge: host file guards, ch_temp component mixing restoration
- `bd18ad4` (2025-11-24) — Pr 107 (#108)
- `29e2d36` (2025-10-29) — Bug fixes and changes related to water allocation
- `10e5ddc` (2025-08-27) — 08272025 updates
- `09d23f0` (2025-06-26) — Comment and formatting changes
- `df07e3f` (2024-03-05) — init all

## Review Notes

- No direct file I/O was extracted for this procedure.
- warning: missing_doc: Procedure 'ch_rtmusk' has no extracted documentation comment.
- algorithm_steps revised: condensed the draft into 14 source-backed steps and aligned each step to visible line ranges.
- Lineage was reconstructed from file-level commit metadata; per-line diffs were unavailable in this environment (blobless clone), so line-span filtering was not applied.
