---
kind: procedure
symbol: ch_temp
title: ch_temp
status: filled
source_hash: 2d844b05c9650b9f
version_label: SWAT+ 62.0.0
locals:
  iob: Index of the current channel-deg object in the spatial object list; derived from `sp_ob1%chandeg
    + ich - 1` so the routine can look up the correct connectivity and outputs for this reach.
  ig: Temperature-gage index from the selected weather station (`wst(iwst)%wco%tgage`); it
    selects the measured climate record in `tmp` that supplies air temperature history for
    lagged water-temperature calculations.
  yrs_to_start: Offset from simulation year to the start year of the temperature record (`time%yrs
    - tmp(ig)%yrs_start`); it selects the correct year slice in `tmp(ig)%ts` and `ts2` when
    computing lagged air-temperature averages.
  tdx: Adjusted dew-point temperature used in the heat-exchange calculation; it is taken from
    calibrated dew point (`tdx_cal`) and limited by air temperature (`t_air`).
  t_md: Midpoint temperature used in the Edinger-style heat-transfer coefficient calculation,
    formed from the initial stream temperature and adjusted dew point temperature.
  ke_beta: Temperature-dependent factor in the bulk heat-transfer coefficient `k_e`; it shapes
    the sensitivity of exchange to the mixed stream/air temperature state.
  f_wind: Wind-speed factor in the heat-transfer coefficient; it converts `w%windsp` into
    an exchange-enhancing term.
  k_e: Bulk heat-transfer coefficient used to translate energy balance into stream temperature
    change.
  ssff: Shade factor applied to shortwave radiation; it is either read from `shf_db` when
    shade input is enabled or taken from `w_temp(0)%ssff` as a default calibration value.
  h_sr: Net shortwave solar heat input to the stream after shade reduction.
  e_s: Saturated vapor pressure at the air temperature, used to compute atmospheric emissivity
    and longwave heat exchange.
  e_a: Actual vapor pressure derived from relative humidity; it feeds the atmospheric emissivity
    calculation.
  cloud: Cloud-cover factor estimated from measured solar radiation versus maximum solar radiation,
    used in the longwave radiation term.
  e_atm: Atmospheric emissivity computed from vapor pressure and cloudiness; it drives longwave
    atmospheric radiation into the stream.
  h_atm: Longwave atmospheric radiation term delivered to the stream surface.
  numerator: Intermediate heat-balance term combining atmospheric radiation and dew-point
    correction before equilibrium temperature is computed.
  t_equil: Equilibrium water temperature target implied by current radiation and air conditions;
    the heat-exchange step moves the stream temperature toward this value.
  k_factor: Thermal capacity scaling factor based on flow depth and water properties; it converts
    heat flux into a temperature change over routing time.
  t_heat_exch: Temperature change due to heat exchange during routing; added to the mixed
    initial stream temperature to obtain the final temperature.
  dep_chan: Calibrated channel depth from `sd_chd(ich)%chd`; used with channel width and flow
    velocity to estimate effective flow depth for heat exchange.
  wid_chan: Calibrated channel width from `sd_chd(ich)%chw`; used to estimate effective flow
    geometry and is adjusted if it becomes too small.
  t_sno: Snowmelt water temperature contribution computed from lagged air temperature history
    and snowmelt coefficients.
  t_gw: Groundwater temperature contribution computed from lagged air temperature history
    and groundwater coefficients.
  t_surf: Surface-runoff water temperature contribution computed from lagged air temperature
    history and surface lag coefficients.
  t_lat: Lateral-flow water temperature contribution computed from lagged air temperature
    history and lateral lag coefficients.
  t_air: Air-temperature surrogate used in the default temperature relation and in the heat-exchange
    calculation.
  t_air_min_av: Lagged average minimum air temperature used to derive surface, lateral, groundwater,
    and snow temperatures.
  t_air_max_av: Lagged average maximum air temperature used alongside `t_air_min_av` to derive
    delayed water-temperature inputs.
  surf_lag: Surface-runoff lag length in days used to average recent air temperatures for
    surface contribution.
  lat_lag: Lateral-flow lag length in days used to average recent air temperatures for lateral
    contribution.
  sno_lag: Snowmelt lag length in days used to average recent air temperatures for snow contribution.
  gw_lag: Groundwater lag length in days used to average recent air temperatures for groundwater
    contribution.
  surf_contr: Weighted surface-runoff contribution to the LSU water-temperature mix; it combines
    flow and temperature for the surface component.
  lat_contr: Weighted lateral-flow contribution to the LSU water-temperature mix.
  gw_contr: Weighted groundwater contribution to the LSU water-temperature mix.
  sno_contr: Weighted snowmelt contribution to the LSU water-temperature mix.
  airlag_d: Daily air-temperature lag value used to compare or carry lagged thermal response
    settings; it is part of the temperature-parameter setup.
  surf_lag_coef: Coefficient applied to the surface air-temperature lag relation.
  lat_lag_coef: Coefficient applied to the lateral-flow air-temperature lag relation.
  gw_lag_coef: Coefficient applied to the groundwater air-temperature lag relation.
  sno_coef: Coefficient applied to the snowmelt air-temperature relation.
  gw_coef: Coefficient applied to the groundwater water-temperature contribution; it scales
    the groundwater component before mixing.
  sur_lat_coef: Coefficient applied to the combined surface-plus-lateral contribution in the
    mixing model.
  wid_flow: Estimated effective flow width from channel discharge and velocity; used with
    channel geometry to compute flow depth for heat exchange.
  dep_flow: Estimated effective flow depth from channel discharge and velocity; used to scale
    the stream thermal capacity in the heat-exchange step.
  q_lsu_sno: Snowmelt water yield from all landscape units contributing to the channel reach.
  q_gw: Groundwater discharge contribution entering the reach from landscape units.
  q_lsu_surf: Surface runoff water yield from all landscape units contributing to the channel
    reach.
  q_lsu_lat: Lateral flow water yield from all landscape units contributing to the channel
    reach.
  q_lsu_wyld: Total landscape water yield entering the channel reach; it is the denominator
    for the initial water-temperature mixing.
  tw_final: Final channel water temperature after mixing and heat exchange; this is the temperature
    written back to channel outputs.
  tw_local: Local mixed temperature from landscape contributions before upstream channel mixing
    and heat exchange.
  tw_init: Initial stream temperature after mixing upstream channel water with local landscape
    inflow; it is the starting point for heat exchange.
  tw_up: Upstream channel water temperature taken from `ht1%temp` before mixing with local
    inflow.
  ilsu: Loop index over output landscape units; it selects the current LSU record for contribution
    aggregation and output assignment.
  sw_init: Initial surface-water temperature accumulator used while building the temperature
    mix from landscape sources.
  sno_init: Initial snowmelt-temperature accumulator used while building the temperature mix
    from landscape sources.
  ielem: Index of a landscape unit element within `lsu_out(ilsu)%num`; it maps each output
    LSU to its member HRUs.
  ihru: Selected HRU index from the landscape-element mapping; it is used to read RU fractions
    and object types for contribution sums.
  ruid_array: Temporary list of routing-unit IDs collected from the incoming objects so the
    routine can aggregate contributions by RU.
  ru_index: Counter for iterating through `ruid_array` while accumulating per-RU contributions.
  ru_count: Number of routing units found among the incoming objects for the current channel-deg
    reach.
  const: Generic scalar constant placeholder used in the temperature calculation setup; the
    visible source does not show a unique named physical meaning for it.
  jday: Current Julian day copied from `time%day`; it drives seasonal lag logic, shade-factor
    lookup, and year-boundary handling.
  i: Loop index over shade-factor records in `shf_db`.
  rttime: Routing travel time in days, derived from `sd_ch_vel(ich)%rttime / 24`, used to
    scale the heat-exchange adjustment.
  vc: Channel flow velocity used in the effective flow-geometry calculation; it comes from
    `sd_ch_vel(ich)%vel` with a lower bound.
  tw_local_prev: Previous day's channel temperature from `ch_out_d(ich)%temp`; it is used
    to detect implausibly large jumps in the newly computed local temperature.
  trib1_temp: Temperature of the first tributary/inflow stream used in channel mixing calculations.
  trib2_temp: Temperature of the second tributary/inflow stream used in channel mixing calculations.
  trib1_flo: Flow of the first tributary/inflow stream used in channel mixing calculations.
  trib2_flo: Flow of the second tributary/inflow stream used in channel mixing calculations.
  trib_flo: Combined tributary flow used to determine the weight of incoming stream temperature
    in the mix.
  tw_def: Fallback default water temperature from the older SWAT relation `5.0 + 0.75 * air
    temperature`; it is used when the gage is missing or a temperature spike is rejected.
  tw_mix: Intermediate mixed temperature before the heat-exchange adjustment; it represents
    the blend of local and upstream water inputs.
  tw_eq: Equilibrium stream temperature target for the current heat-balance conditions.
  bulk_co: Bulk coefficient for heat exchange; the visible source does not show a distinct
    final use beyond the broader heat-transfer setup.
  eps: Small tolerance/guard value used in the temperature routine; the visible source does
    not show its exact final role in the excerpted lines.
  tdx_cal: Calibrated dew-point temperature before limiting by air temperature; it comes from
    `w%dewpt * w_temp(0)%hex_coef1`.
  in: Loop index over incoming objects/receivers in the current channel connectivity record.
uses:
  basin_module: '`basin_module` provides the basin control flag `bsn_cc%gwflow`, which switches
    whether groundwater is included in the local temperature mix or handled separately by
    gwflow subroutines.'
  input_file_module: '`input_file_module` is listed among the modules used by `ch_temp`, but
    the provided context does not resolve any concrete symbols from it. The routine appears
    to rely on imported input-file state indirectly through the weather and temperature databases
    already covered by other modules, so the specific imported names cannot be identified
    from this packet.'
  maximum_data_module: '`maximum_data_module` supplies `db_mx%lsu_out`, the loop bound used
    to traverse all landscape-output units when assembling temperature contributions from
    `lsu_out` and `lsu_elem`.'
  channel_data_module: '`channel_data_module` holds the configurable water-temperature parameters
    in `w_temp(0)`, including lag lengths, coefficients, the default shade factor, and the
    flags that control whether shade-factor input is active.'
  sd_channel_module: '`sd_channel_module` provides the reach geometry (`sd_chd(ich)%chw`,
    `sd_chd(ich)%chd`) needed to convert discharge and velocity into an effective flow width
    and depth for the heat-exchange calculation.'
  hydrograph_module: '`hydrograph_module` supplies the channel connectivity, inflow hydrographs,
    channel storage/output records, shade-factor database, and hydrograph-separation array
    that `ch_temp` reads and updates while mixing temperatures and writing diagnostics.'
  climate_module: '`climate_module` provides the active weather station, measured weather
    record, and temperature-gage metadata that determine air temperature, radiation, humidity,
    dew point, and record start year for the temperature lags.'
  output_landscape_module: '`output_landscape_module` provides the landscape water-balance
    outputs that `ch_temp` uses as part of its channel temperature bookkeeping and diagnostics
    for the contributing LSU components.'
  aquifer_module: '`aquifer_module` is imported by `ch_temp`, but no resolved references from
    that module appear in the provided source excerpt or outside-reference list. Its presence
    may reflect shared model state or future compatibility, but the packet does not show a
    direct dependence here.'
  calibration_data_module: '`calibration_data_module` provides the LSU-to-HRU mapping (`lsu_out`,
    `lsu_elem`) that lets `ch_temp` accumulate water and temperature contributions by landscape
    unit and routing-unit fraction.'
  time_module: '`time_module` provides the current simulation day and year, which drive the
    seasonal lag windows, year-start branching, and the selection of the correct measured
    climate year slice.'
  channel_velocity_module: '`channel_velocity_module` provides `sd_ch_vel(ich)%rttime`, the
    routing travel time that scales how much of the equilibrium heat exchange is realized
    during the current timestep.'
---

<!-- facts:header -->

Computes channel water temperature for a SWAT+ SWAT-deg reach by mixing inflows, weather-driven surface/groundwater contributions, and heat exchange along the channel.

## Bottom Line

`ch_temp` updates the water temperature associated with a SWAT-deg channel reach for the current day. It pulls the active weather station and measured temperature gage, estimates an initial mixed stream temperature from landscape inflows, then adjusts that temperature using an atmospheric heat-exchange calculation and channel travel time.

The routine matters because it writes the temperature that downstream channel routing uses (`ht2%temp`, `ch_stor(ich)%temp`, and `ch_out_d(ich)%temp`) and it also records diagnostic components in `hyd_sep_array`. It includes safeguards for missing temperature gages, year-start edge cases, implausible temperature jumps, and optional shade-factor input.

## Arguments

<!-- facts:arguments -->

## Where It Fits

`ch_temp` runs from `sd_channel_control3` after the routing setup has prepared the current channel-deg object, its upstream hydrograph (`ht1`), the current channel flow state (`ht2`), and the per-reach connectivity needed to identify weather and landscape inputs. Its outputs feed the subsequent routing bookkeeping in the same control routine, especially the channel temperature carried in `ht2%temp`, `ch_stor(ich)%temp`, and `ch_out_d(ich)%temp`.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. Initialize day, reach, weather, and default temperature state. | Copies the current Julian day from `time%day`, maps the current channel-deg reach to its object index and weather station, loads the daily weather record, and computes the legacy default water temperature `tw_def = 5.0 + 0.75 * w%tave`. |
| 2. Count incoming routing units and prepare the RU list. | Scans the incoming object types for the current channel object, counts how many are routing units (`'ru'`), allocates `ruid_array`, and stores the RU identifiers so downstream mixing can aggregate by routing unit. |
| 3. Gather incoming channel temperatures and flows. | Loops over incoming receivers, identifies upstream channel-deg inflows, accumulates tributary temperature and flow terms, and falls back to the default temperature if the upstream contribution is effectively zero. |
| 4. Aggregate landscape-unit water and temperature contributions. | Iterates over all output landscape units and their HRU members to sum snowmelt, groundwater, surface runoff, lateral flow, and total water yield terms that will drive the local channel temperature mix. |
| 5. Build the local mixed water temperature from LSU components. | Combines the snow, lateral, surface, and groundwater temperature contributions into `tw_local`, using the gwflow switch to exclude groundwater from the mix when gwflow is active. |
| 6. Use measured air-temperature lags for surface, lateral, groundwater, and snow inputs. | Handles missing gage input, then computes lagged air-temperature averages for surface runoff, lateral flow, groundwater, and snowmelt using the measured temperature record `tmp(ig)` and the configured lag lengths, including year-boundary handling and start-year offsets. |
| 7. Blend upstream channel water with the local mix. | Computes the reach-local mixed temperature `tw_local`, checks for implausibly large day-to-day jumps and falls back to the default temperature if needed, then mixes local inflow with upstream channel water to produce `tw_init`. |
| 8. Compute heat transfer toward equilibrium temperature. | Calculates the calibrated dew point, wind factor, heat-transfer coefficient, shade-adjusted shortwave input, atmospheric radiation terms, equilibrium temperature, effective flow geometry, travel-time scaling, and final heat-exchange temperature increment `t_heat_exch`. |
| 9. Write the final channel temperature and diagnostics. | Forms `tw_final`, prevents negative temperatures, writes the result to `ht2%temp`, `ch_stor(ich)%temp`, and `ch_out_d(ich)%temp`, updates `wtemp`, and stores the component diagnostics in `hyd_sep_array(ich,1:7)`. |
| 10. Return to the caller. | Ends the subroutine after all channel-temperature outputs and diagnostics have been written back to shared model state. |

## Modules Used

<!-- facts:uses -->

| Module | State touched | Key components |
| --- | --- | --- |
| [sym:basin_module] | `bsn_cc` | `bsn_cc%gwflow` |
| [sym:input_file_module] | `tmp, wst, w` | `wst(iwst)%wco%tgage, wst(iwst)%weat, w%tave, tmp(ig)%yrs_start, w%dewpt, w%windsp, w%solrad, w%rhum, w%solradmx, wst(iwst)%weat%tave` |
| [sym:maximum_data_module] | `db_mx` | `db_mx%lsu_out` |
| [sym:channel_data_module] | `w_temp` | `w_temp(0)%sno_lag, w_temp(0)%gw_lag, w_temp(0)%lat_lag, w_temp(0)%surf_lag, w_temp(0)%surf_lag_coef, w_temp(0)%gw_lag_coef, w_temp(0)%lat_lag_coef, w_temp(0)%sno_mlt, w_temp(0)%gw, w_temp(0)%sur_lat, w_temp(0)%hex_coef1, w_temp(0)%sf_on, w_temp(0)%ssff, w_temp(0)%hex_coef2` |
| [sym:sd_channel_module] | `sd_chd` | `sd_chd(ich)%chw, sd_chd(ich)%chd` |
| [sym:hydrograph_module] | `sp_ob1, ob, ht1, hdsep1, ch_out_d, shf_db, ht2, ch_stor, hd, ts` | `sp_ob1%chandeg, ob(iob)%wst, ob(iob)%obtyp_in(in), ob(iob)%hd(1), ob(iob)%rcv_tot, ob(iob)%hin_d(in-1)%temp, ob(iob)%hin_d(in)%temp, ob(iob)%hin_d(in-1)%flo, ob(iob)%hin_d(in)%flo, ht1%temp, hdsep1%flo_gwsw, ch_out_d(ich)%temp, ht1%flo, shf_db(i)%jday, shf_db(i)%lsu, shf_db(i)%value, ht2%flo, ht2%temp, ch_stor(ich)%temp` |
| [sym:climate_module] | `wst, w, tmp` | `wst(iwst)%wco%tgage, wst(iwst)%weat, w%tave, tmp(ig)%yrs_start, w%dewpt, w%windsp, w%solrad, w%rhum, w%solradmx, wst(iwst)%weat%tave` |
| [sym:output_landscape_module] | `lsu_wb_d, ruwb_d, hwb_d, hltwb_d` | `lsu_wb_d(ilsu)%snomlt, lsu_wb_d(ilsu)%surq_gen, lsu_wb_d(ilsu)%latq, lsu_wb_d(ilsu)%wateryld` |
| [sym:aquifer_module] | `No candidate outside references were resolved to `aquifer_module` in the provided packet.` | `No resolved aquifer-module symbols were extracted.` |
| [sym:calibration_data_module] | `lsu_out, lsu_elem` | `lsu_out(ilsu)%num_tot, lsu_out(ilsu)%num(ielem), lsu_elem(ihru)%ru_frac, lsu_elem(ihru)%obtyp` |
| [sym:time_module] | `time` | `time%day, time%yrs` |
| [sym:channel_velocity_module] | `sd_ch_vel` | `sd_ch_vel(ich)%rttime` |

## Local Variables

<!-- facts:locals -->

## State Changes

| Target | When | Meaning |
| --- | --- | --- |
| `iwst` | At routine entry for the current channel-deg reach after mapping `iob = sp_ob1%chandeg + ich - 1`. | Selects which object and weather station are active for this temperature calculation. |
| `w` | When the current station weather record is loaded with `w = wst(iwst)%weat`. | Snapshots the daily climate inputs used throughout the heat-balance and lag calculations. |
| `ht1` | When the upstream channel temperature is copied into `ht1`/`tw_up` and the routine later mixes it with local inflow. | Establishes the upstream temperature state that contributes to the initial stream temperature. |
| `ht1%temp` | When the mixed stream temperature is finalized from `tw_up`, `ht1%flo`, and `q_lsu_wyld`. | Updates the upstream-mix temperature state used before heat exchange and downstream output writing. |
| `lsu_wb_d(ilsu)` | After the final temperature is written to `lsu_wb_d(ilsu)`-related diagnostics and landscape aggregation has been completed. | Leaves the LSU-linked water-balance outputs in a state consistent with the current channel-temperature computation. |
| `ht2%temp` | After heat exchange is evaluated and before final storage/output writes. | Creates the post-exchange outlet temperature that represents the reach after atmospheric adjustment. |
| `ch_stor(ich)%temp` | At the end of the heat-exchange and mixing sequence. | Stores the final channel temperature in channel storage so later routing steps and outputs see the updated value. |
| `ch_out_d(ich)%temp` | When the final temperature is assigned to `ch_out_d(ich)%temp`. | Commits the channel-deg output temperature used by downstream output routines and diagnostics. |
| `wtemp` | After `wtemp` is recomputed from the station’s mean air temperature. | Updates the temperature summary value written to the daily channel output file. |
| `hyd_sep_array(ich,1)` | When the hydrologic separation diagnostics are written at routine end. | Stores component water yields and temperatures so the channel temperature routine can be inspected or calibrated later. |
| `hyd_sep_array(ich,2)` | When `hyd_sep_array(ich,2)` is assigned from `q_lsu_lat`. | Records the lateral-flow contribution used in the local temperature mix for diagnostics. |
| `hyd_sep_array(ich,3)` | When `hyd_sep_array(ich,3)` is assigned from `q_gw`. | Records the groundwater contribution for diagnostics and for gwflow-aware mixing interpretation. |
| `hyd_sep_array(ich,4)` | When `hyd_sep_array(ich,4)` is assigned from `q_lsu_wyld`. | Records the total landscape water yield that normalized the local temperature mix. |
| `hyd_sep_array(ich,5)` | When `hyd_sep_array(ich,5)` is assigned from `q_lsu_sno`. | Records the snowmelt contribution used in the local temperature mix. |
| `hyd_sep_array(ich,6)` | When `hyd_sep_array(ich,6)` is assigned from `tw_final`. | Stores the final routed channel water temperature for diagnostic inspection. |
| `hyd_sep_array(ich,7)` | When `hyd_sep_array(ich,7)` is assigned from `tw_init`. | Stores the pre-exchange initial stream temperature so the thermal adjustment can be reconstructed. |

## File I/O

<!-- facts:io -->


## Theory Equations

| Eq. | Title | Formula | Implementation |
| --- | --- | --- | --- |
| 1:1.3.13 | Water temperature | $T_{water}=5.0+0.75\overline T_{av}$ | tw_def = 5.0 + 0.75*w%tave; the SWAT air-temperature relation, reused at lines 150/155/330. |

## Lineage

Source-backed lineage commits were resolved. The procedure was introduced in commit b9df6cf as a new `ch_temp.f90` implementation that sets up module dependencies, temperature parameters, landscape aggregation, atmospheric exchange, and output writes. Commit 2a5e8de then modified the routine to add a missing-temperature-gage fallback (`ig <= 0`), tighten the early-year lag-window conditions, and protect the lagged air-temperature sums against out-of-range slices with `max(1, ...)` indexing.

- b9df6cf added the full `ch_temp` implementation, including weather/landscape mixing, channel heat exchange, output state writes, and hydrologic separation diagnostics.
- 2a5e8de added robustness guards for missing temperature gages and adjusted the lagged temperature averaging logic to avoid invalid array slices at year boundaries.

## Review Notes

- No direct file I/O was extracted for this procedure.
- warning: missing_doc: Procedure 'ch_temp' has no extracted documentation comment.
- algorithm_steps revised: condensed the source into 10 model-level steps aligned with the visible source blocks and final output section.
- Source excerpt shows `input_file_module` and `aquifer_module` in the USE list but no resolved candidate outside references for those modules in the packet; their specific symbols cannot be identified from the provided evidence.
