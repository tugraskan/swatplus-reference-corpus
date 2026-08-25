---
kind: module
symbol: channel_velocity_module
title: channel_velocity_module
status: filled
source_hash: 15249adddd5a9b57
version_label: SWAT+ 62.0.0
variables:
  ch_vel: Main-channel cache written by `ch_ttcoef` after `proc_cha` finishes the channel
    input reads. `ch_rtday` later uses the cached bottom width and bankfull area to estimate
    capacity, depth, top width, travel time, and losses. A visible source-wide scan did not
    find where this allocatable array is allocated.
  sd_ch_vel: SWAT-deg channel cache allocated in `sd_channel_read` and partially filled in
    `sd_hydsed_init`. Visible source assigns only `wid_btm` and `dep_bf` here; `sd_channel_control3`
    later reads `dep_bf` and `vel_bf` for morphology output.
  grwway_vel: Grassed-waterway cache allocated per HRU in `hru_allo`. `ttcoef_wway` computes
    bankfull and low-flow geometry from `hru(:)%lumv%grwat_*`, and `smp_grass_wway` reuses
    the cached area, width, discharge capacity, and celerity.
type_components:
  channel_velocity_parameters:
    area: Cross-sectional area at bankfull depth. `ch_rtday` and `smp_grass_wway` treat it
      as the cached bankfull area before iterating to other depths.
    vel_bf: Bankfull discharge capacity returned by `Qman(a, rh, ...)`, despite the `vel_`
      prefix. Downstream code compares it against flow rates (`volrt`, `qp_cms`) rather than
      treating it as a velocity.
    wid_btm: Computed trapezoid bottom width after reconciling the supplied top width, depth,
      and side slope.
    dep_bf: Bankfull depth copied from the upstream channel or waterway hydraulic input.
    velav_bf: Average bankfull velocity from `Qman(1., rh, ...)`.
    celerity_bf: Wave celerity approximation at bankfull depth, computed as `velav_bf * 5.
      / 3.`.
    st_dis: Bankfull storage time constant in hours, computed from reach or waterway length
      divided by celerity.
    vel_1bf: Average velocity at 0.1 bankfull depth for low-flow routing behavior.
    celerity_1bf: Wave celerity at 0.1 bankfull depth, also derived from `vel_1bf * 5. / 3.`.
    stor_dis_1bf: Storage time constant at 0.1 bankfull depth.
type_summaries:
  channel_velocity_parameters: Shared record of trapezoidal cross-section geometry plus bankfull
    and low-flow routing coefficients. The same layout backs `ch_vel`, `sd_ch_vel`, and `grwway_vel`,
    even though the SWAT-deg path only fills a subset of fields in visible source.
---

<!-- facts:header -->

Computed hydraulic-geometry cache for main channels, SWAT-deg channels, and grassed waterways. The module stores bankfull and low-flow cross-section metrics that routing and morphology code reuse instead of recomputing them each time step.

## Contained Procedures And Types

<!-- facts:members -->

## Module Variables

<!-- facts:variables -->

## Derived Types

<!-- facts:types -->



## Initialization

This module has no reader of its own. Other startup routines allocate the arrays and then derive geometry and routing coefficients from hydraulic properties that were already read into channel, SWAT-deg, or HRU structures.

## Populated By

| Reader | Input file | Target | Behavior |
| --- | --- | --- | --- |
| [sym:hru_allo] | `sp_ob%hru` | `grwway_vel(0:imax)` | Allocates the grassed-waterway cache alongside the HRU arrays before any structural practice parameters are applied. |
| [sym:ttcoef_wway] | `hru(k)%lumv%grwat_w, grwat_d, grwat_n, grwat_s, grwat_l` | `grwway_vel(k)` | Called from `structure_set_parms` after a width/depth sanity check. Computes bottom width, bankfull area/discharge, bankfull average velocity/celerity, and low-flow storage constants for each grassed waterway. |
| [sym:sd_channel_read] | `sp_ob%chandeg` | `sd_ch_vel(0:sp_ob%chandeg)` | Allocates the SWAT-deg channel cache with the rest of the channel-routing state. |
| [sym:sd_hydsed_init] | `sd_ch(i)%chw, chd, chss, chn, chs, chl` | `sd_ch_vel(i)` | Computes a bottom width and copies bankfull depth before continuing with rating-curve and Muskingum setup on `sd_ch`. Visible source does not populate the remaining `sd_ch_vel` components here. |
| [sym:ch_ttcoef] | `ch_hyd(k)%w, d, side, n, s, l` | `ch_vel(k)` | Called from `proc_cha` after the channel input reads. Computes bottom width, bankfull area/discharge, bankfull average velocity/celerity, and low-flow storage constants for each main channel, but the visible source scan did not find the matching `allocate(ch_vel(...))` site. |

## Key Consumers

The visible consumers use these arrays as cached hydraulic geometry and capacity state, not as independent model inputs.

| Consumer | Uses | Effect |
| --- | --- | --- |
| [sym:ch_rtday] | ch_vel(jrch)%area and ch_vel(jrch)%wid_btm | Computes bankfull capacity, iterates to a flow depth for the day, derives top width, and applies channel transmission-loss and evaporation calculations without recomputing the bankfull trapezoid from scratch. |
| [sym:smp_grass_wway] | grwway_vel(j)%vel_bf, area, wid_btm, celerity_bf | Chooses whether runoff exceeds bankfull waterway capacity, iterates to a working flow depth when it does not, and caps routed velocity at the cached bankfull celerity. |
| [sym:sd_channel_control3] | sd_ch_vel(ich)%dep_bf and sd_ch_vel(ich)%vel_bf | Copies cached SWAT-deg bankfull depth into daily morphology output and reports `vel_bf` through an output field named `velav_bf`. |

## Lineage

`channel_velocity_module.f90` was introduced in `df07e3f` (2024-03-05, "init all") and has been changed in 3 non-merge commit(s) since, most recently `b9df6cf` (2026-04-01, "gwflow re-merge: host file guards, ch_temp component mixing restoration"). Lineage is reconstructed from commit metadata (SHA, date, subject); per-line diffs were unavailable in this build environment, so only the commits touching `channel_velocity_module.f90` are listed.

- `b9df6cf` (2026-04-01) — gwflow re-merge: host file guards, ch_temp component mixing restoration
- `c7c8e22` (2024-05-30) — Added latest source code from bitbucket
- `df07e3f` (2024-03-05) — init all

## Review Notes

- The module and its shared derived type have no module-level purpose comment beyond field-level notes.
- `vel_bf` is a misleading name: `ch_ttcoef` and `ttcoef_wway` assign it from `Qman(a, rh, ...)`, so it behaves as bankfull discharge capacity rather than velocity, while `velav_bf` is the actual bankfull average velocity.
- A visible source-wide scan of `src/` found no `allocate(ch_vel(...))` site even though `ch_ttcoef` writes `ch_vel(k)%...` during startup.
- `sd_hydsed_init` only assigns `sd_ch_vel(i)%wid_btm` and `sd_ch_vel(i)%dep_bf`; no visible writer populates `sd_ch_vel%area`, `%vel_bf`, `%velav_bf`, `%celerity_bf`, `%st_dis`, `%vel_1bf`, `%celerity_1bf`, or `%stor_dis_1bf`.
- `sd_channel_control3` writes `sd_ch_vel(ich)%vel_bf` into an output field named `velav_bf`, so the SWAT-deg daily morphology output appears to mix a discharge-like cached field into a velocity-labelled column.
- Lineage was reconstructed from file-level commit metadata; per-line diffs were unavailable in this environment (blobless clone), so line-span filtering was not applied.
