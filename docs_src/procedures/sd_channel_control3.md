---
kind: procedure
symbol: sd_channel_control3
title: sd_channel_control3
status: filled
source_hash: fbbee1a88f8faeb6
version_label: SWAT+ 62.0.0
locals:
  isd_db: Index into the channel hydraulic data (`sd_dat(ich)%hyd`).
  ipest: Pesticide counter.
  isalt: Salt-ion counter.
  ebtm_m: Channel bottom erosion depth (m), carried to morphology output.
  ebank_m: Channel bank/meander erosion (m, one side), carried to morphology output.
  hc_sed: Headcut erosion (tons), carried to morphology output.
  a: Channel cross-sectional area (m^2).
  frac: Fraction of the hydrograph (0-1).
  ics: Constituent counter.
  rto: Ratio used to scale the sub-daily inflow series when adding aquifer inflow.
  iaq: Aquifer index linked to the channel.
  iaq_ch: Aquifer-channel link index.
  scoef: Storage routing coefficient.
  gw_salt_in: Salt mass loaded to the channel from the linked aquifer (kg).
  gw_cs_in: Constituent mass loaded to the channel from the linked aquifer (kg).
  seep_mass: Salt/constituent mass lost in channel seepage (kg).
  salt_conc: Salt-ion concentrations in channel water (g/m3).
  cs_conc: Constituent concentrations in channel water (g/m3).
  conc_chng: Fractional change in sol/org N and P from in-channel transformation.
  inflo_rate: Inflow rate (m3/s) used to interpolate the rating curve.
  aqu_inflo: Aquifer inflow volume added to the channel (m3).
  iw: Water-allocation object counter.
  iwallo: Water-allocation index passed to `wallo_control`.
uses:
  sd_channel_module: Provides SWAT-deg channel parameters and state (`sd_ch`, `sd_dat`, `chsd_d`,
    `ch_sed_bud`).
  channel_velocity_module: Provides channel velocity/geometry (`sd_ch_vel`) for morphology
    output.
  basin_module: Provides control flags (`bsn_cc` gwflow/lapse/qual2e) gating optional processing.
  hydrograph_module: Provides the routing object and hydrographs (`ob`, `ht1`, `ht2`, `hz`).
  constituent_mass_module: Provides constituent state (`cs_db`, `obcs`, `hcs1`, `hcs2`).
  conditional_module: Provides decision-table state for called actions.
  channel_data_module: Provides channel database records.
  channel_module: Provides legacy channel arrays.
  ch_pesticide_module: Provides channel pesticide state (`chpst`, `chpst_d`).
  climate_module: Provides weather stations (`wst`) and lapse inputs.
  water_body_module: Provides water-body state.
  time_module: Provides the simulation time.
  ch_salt_module: Provides channel salt output (`chsalt_d`).
  ch_cs_module: Provides channel constituent output (`chcs_d`).
  gwflow_module: Provides `flood_freq` and gwflow exchange hooks.
  water_allocation_module: Provides water-allocation state for `wallo_control`.
  maximum_data_module: Provides database dimension maxima.
---

<!-- facts:header -->

Routes one day of flow, sediment, nutrients, pesticides, pathogens, salts, and constituents through a SWAT-deg channel reach. It assembles the inflow hydrograph (upstream, transfers, aquifer, gwflow exchanges), calls the sediment, Muskingum routing, and water-quality routines, then writes the channel morphology and budget outputs.

## Bottom Line

`sd_channel_control3` is the per-reach daily controller for SWAT-deg channels. It sets the incoming hydrograph `ht1` from the routing object, adds water transfers and aquifer/groundwater exchange, lapse-adjusts weather and sets channel water temperature, then delegates to `sd_channel_sediment3` (erosion/deposition), `ch_rtmusk` (flood routing), `ch_rtpest`/`ch_rtpath` (pesticide/pathogen), and `ch_watqual4` (nutrient water quality).

After routing it computes salt/constituent concentrations and seepage losses, applies optional QUAL2E nutrient transformations, and fills the daily channel sediment/nutrient budget (`ch_sed_bud`) and morphology (`chsd_d`) output structures that feed channel reporting and downstream routing.

## Arguments

<!-- facts:arguments -->

## Where It Fits

Called once per SWAT-deg channel each day from `command` (the routing dispatcher), after upstream objects have delivered their hydrographs. It consumes the incoming routing object (`ob(icmd)%hin`) and produces the channel outflow (`ob(icmd)%hd`) plus the channel output structures. Its callees do the physical routing; this routine orchestrates them.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. Assemble inflow | Sets `ht1` to the incoming hydrograph, zeros outputs, adds water transfers and hydrograph-separation components, lapse-adjusts weather and sets channel water temperature, and adds linked-aquifer inflow with salt/constituent loads. |
| 2. Groundwater exchange | When gwflow is active, calls the channel-groundwater exchange, canal seepage, tile, and saturation-excess routines, updating `ht1`. |
| 3. Route flow and constituents | Calls `sd_channel_sediment3`, `ch_rtmusk`, `ch_rtpest`/`ch_rtpath`, and `ch_watqual4`; computes salt/constituent concentrations, optional QUAL2E nutrient transformations, and seepage losses. |
| 4. Write outputs | Fills the channel sediment/nutrient budget (`ch_sed_bud`), morphology output (`chsd_d`), and pesticide/salt/constituent output structures from the routed hydrograph and erosion/deposition terms. |

## Modules Used

<!-- facts:uses -->

| Module | State touched | Key components |
| --- | --- | --- |
| [sym:sd_channel_module] | `sd_dat, chsd_d, sd_ch, rcurv, ch_rcurv` | `sd_dat(ich)%hyd, chsd_d(ich)%flo_in, sd_ch(ich)%msk%nsteps, sd_ch(ich)%aqu_link, sd_ch(ich)%aqu_link_ch, chsd_d(ich)%aqu_in, chsd_d(ich)%aqu_in_mm, chsd_d(ich)%flo_in_mm, sd_dat(ich)%nut, sd_ch(ich)%chw, sd_ch(ich)%chl, rcurv%ttime, ch_rcurv(jrch)%in2%ttime` |
| [sym:channel_velocity_module] | `no resolved imported state` |  |
| [sym:basin_module] | `bsn_cc` | `bsn_cc%gwflow, bsn_cc%lapse, bsn_cc%qual2e` |
| [sym:hydrograph_module] | `ob, ht1, ch_in_d, hdsep1, aq_ch, ht2, ht3, ch_trans` | `ob(icmd)%wst, ob(icmd)%hin, ob(icmd)%trans%flo, ob(icmd)%trans, ht1%flo, ch_in_d(ich)%flo, hdsep1%flo_surq, ob(icmd)%hdsep_in%flo_surq, hdsep1%flo_latq, ob(icmd)%hdsep_in%flo_latq, hdsep1%flo_gwsw, ob(icmd)%hdsep_in%flo_gwsw, hdsep1%flo_swgw, ob(icmd)%hdsep_in%flo_swgw, hdsep1%flo_satex, ob(icmd)%hdsep_in%flo_satex, hdsep1%flo_satexsw, ob(icmd)%hdsep_in%flo_satexsw, hdsep1%flo_tile, ob(icmd)%hdsep_in%flo_tile, ht1%temp, ob(icmd)%tsin(1), aq_ch(iaq)%ch(iaq_ch)%flo_fr, aq_ch(iaq)%hd%flo, ob(icmd)%area_ha, ob(icmd)%tsin(:), aq_ch(iaq)%hd, ht2%flo, ht3%flo, ch_trans%orgn, ht1%orgn, ht1%no3, ch_trans%no3, ht2%orgn, ht2%no3, ch_trans%sedp, ht1%sedp, ht1%solp, ch_trans%solp, ht2%sedp, ht2%solp, ob(icmd)%hout_tot` |
| [sym:constituent_mass_module] | `cs_db, obcs, aq_chcs, hcs1, hcs2` | `cs_db%num_tot, obcs(icmd)%hd(:), obcs(icmd)%hin(1), cs_db%num_salts, aq_chcs(iaq)%hd(1)%salt(isalt), hcs1%salt(isalt), cs_db%num_cs, aq_chcs(iaq)%hd(1)%cs(ics), hcs1%cs(ics), cs_db%num_pests, obcs(icmd)%hd(1)%pest, hcs2%pest, cs_db%num_paths, hcs2%salt(isalt), hcs2%cs(ics)` |
| [sym:conditional_module] | `no resolved imported state` |  |
| [sym:channel_data_module] | `no resolved imported state` |  |
| [sym:channel_module] | `no resolved imported state` |  |
| [sym:ch_pesticide_module] | `no resolved imported state` |  |
| [sym:climate_module] | `wst` | `wst(iwst)%weat, wst(iwst)%weat%tave` |
| [sym:water_body_module] | `no resolved imported state` |  |
| [sym:time_module] | `time` | `time%dtm` |
| [sym:ch_salt_module] | `chsalt_d` | `chsalt_d(ich)%salt(isalt)%gw_in, chsalt_d(ich)%salt(isalt)%seep` |
| [sym:ch_cs_module] | `chcs_d` | `chcs_d(ich)%cs(ics)%gw_in, chcs_d(ich)%cs(ics)%seep` |
| [sym:gwflow_module] | `flood_freq` | `flood_freq` |
| [sym:ch_pesticide_module] | `no resolved imported state` |  |
| [sym:channel_velocity_module] | `no resolved imported state` |  |
| [sym:water_allocation_module] | `no resolved imported state` |  |
| [sym:maximum_data_module] | `no resolved imported state` |  |

## Local Variables

<!-- facts:locals -->

## State Changes

| Target | When | Meaning |
| --- | --- | --- |
| `ich` | At entry. | Local index of the current SWAT-deg channel. `ich = isdch`. |
| `iwst` | At entry. | Weather-station index for the channel object. `iwst = ob(icmd)%wst`. |
| `if(bsn_cc%gwflow.eq.1)flood_freq(ich)` | When gwflow is active. | Per-channel gwflow flood indicator, reset for the day. `flood_freq(ich) = 0` when gwflow is active. |
| `ht1` | At entry and as inflow sources are added. | Incoming routing hydrograph for the reach. `ht1 = ob(icmd)%hin`, then `+ trans`, `+ aquifer flow`. |
| `ht2` | Reset at entry; filled by routing callees. | Outgoing channel hydrograph. `ht2 = hz` (zeroed). |
| `obcs(icmd)%hd(:)` | When constituents are simulated. | Outgoing constituent hydrographs, zeroed. `obcs(icmd)%hd(:) = hin_csz`. |
| `ch_sed_bud(ich)` | Reset at entry, filled at the end. | Daily channel sediment/nutrient budget output. `ch_sed_bud(ich) = ch_sed_budz`, then filled. |
| `ob(icmd)%trans` | When a transfer is present. | Water transfer into the reach, consumed after adding. `ht1 = ht1 + ob(icmd)%trans` then `ob(icmd)%trans = hz`. |
| `hcs1` | When constituents are simulated. | Incoming constituent loads (salt/cs). `hcs1 = obcs(icmd)%hin(1)` plus aquifer loads. |
| `chsd_d(ich)%flo_in` | At entry and after aquifer inflow. | Inflow rate (m3/s) for morphology output. `chsd_d(ich)%flo_in = ht1%flo / 86400.` |
| `ch_in_d(ich)` | At entry and after inflow updates. | Inflow organic-mineral hydrograph for the reach. `ch_in_d(ich) = ht1`. |
| `ch_in_d(ich)%flo` | At entry. | Inflow flow rate (m3/s) for om output. `ch_in_d(ich)%flo = ht1%flo / 86400.` |
| `hdsep1%flo_surq` | At entry. | Surface-runoff component of separated inflow. `= ob(icmd)%hdsep_in%flo_surq`. |
| `hdsep1%flo_latq` | At entry. | Lateral-flow component of separated inflow. `= ob(icmd)%hdsep_in%flo_latq`. |
| `hdsep1%flo_gwsw` | At entry. | Groundwater->surface-water component. `= ob(icmd)%hdsep_in%flo_gwsw`. |
| `hdsep1%flo_swgw` | At entry. | Surface-water->groundwater component. `= ob(icmd)%hdsep_in%flo_swgw`. |
| `hdsep1%flo_satex` | At entry. | Saturation-excess component. `= ob(icmd)%hdsep_in%flo_satex`. |
| `hdsep1%flo_satexsw` | At entry. | Sat-excess-to-surface-water component. `= ob(icmd)%hdsep_in%flo_satexsw`. |
| `hdsep1%flo_tile` | At entry. | Tile-flow component of separated inflow. `= ob(icmd)%hdsep_in%flo_tile`. |
| `w` | At entry. | Local copy of the channel's daily weather. `w = wst(iwst)%weat`. |
| `wst(iwst)%weat` | After `cli_lapse`. | Channel weather updated with lapse rates. `wst(iwst)%weat = w` after lapse adjustment. |
| `ht1%temp` | At entry. | Inflow water temperature for the reach. `ht1%temp = 5.0 + 0.75 * tave`. |
| `wtemp` | At entry. | Channel water temperature (local). `wtemp = 5.0 + 0.75 * tave`. |
| `ob(icmd)%tsin(1)` | When `msk%nsteps == 1` and when aquifer inflow is added. | Sub-daily inflow time-series value. `ob(icmd)%tsin(1) = ht1%flo`; scaled by `(1+rto)` for aquifer inflow. |

## File I/O

<!-- facts:io -->


## Lineage

`sd_channel_control3.f90` was introduced in `df07e3f` (2024-03-05, "init all") and has been changed in 21 non-merge commit(s) since, most recently `c38f3b8` (2026-04-05, "clean up and bugfixes"). Lineage is reconstructed from commit metadata (SHA, date, subject); per-line diffs were unavailable in this build environment, so only the commits touching `sd_channel_control3.f90` are listed.

- `c38f3b8` (2026-04-05) — clean up and bugfixes
- `b9df6cf` (2026-04-01) — gwflow re-merge: host file guards, ch_temp component mixing restoration
- `9d9069f` (2026-03-31) — gwflow re-merge: module foundation - unified sources/sinks (ss) type, file renames, heat/pond/phreatophyte types, stubs
- `080211e` (2026-03-09) — water allocation operating properly
- `bd18ad4` (2025-11-24) — Pr 107 (#108)
- `df07e3f` (2024-03-05) — init all

## Review Notes

- No direct file I/O was extracted for this procedure.
- warning: missing_doc: Procedure 'sd_channel_control3' has no extracted documentation comment.
- Channel routing driver: assembles inflow and delegates physics to many callees; 10 use-imported modules had no specific symbol resolved.
- Lineage was reconstructed from file-level commit metadata; per-line diffs were unavailable in this environment (blobless clone), so line-span filtering was not applied.
