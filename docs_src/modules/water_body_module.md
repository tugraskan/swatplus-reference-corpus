---
kind: module
symbol: water_body_module
title: water_body_module
status: filled
source_hash: dc138bd9e6a0aa88
version_label: SWAT+ 62.0.0
variables:
  wbodz: Shared zero-valued `water_body` template of type `water_body`, initialized by the
    type defaults in `water_body_module.f90:7-11`. Readers and output routines use it as the
    reset value for reservoir, wetland, and channel summary records, and basin output routines
    seed aggregate totals from it before accumulation.
  res_wat_d: Allocatable daily reservoir water-body array of type `water_body` (`water_body_module.f90:21`).
    `res_allo` allocates it, `res_initial` initializes each reservoir's surface area, `res_control`
    updates area, precipitation, evaporation, and seepage, and reservoir reporting and water-quality
    routines read its fields for output and mass-balance conversions.
  res_wat_m: Allocatable monthly reservoir water-body array of type `water_body` (`water_body_module.f90:22`).
    It is allocated in `res_allo` and accumulated in `reservoir_output` from the daily record
    before monthly reporting and normalization.
  res_wat_y: Allocatable yearly reservoir water-body array of type `water_body` (`water_body_module.f90:23`).
    It is allocated in `res_allo` and filled in `reservoir_output` from month-end values before
    yearly reporting.
  res_wat_a: Allocatable average-annual reservoir water-body array of type `water_body` (`water_body_module.f90:24`).
    It is allocated in `res_allo` and used by `reservoir_output` for simulation-average reporting.
  wet_wat_d: Allocatable daily wetland water-body array of type `water_body` (`water_body_module.f90:25`).
    `hru_allo` allocates it, `wet_initial` initializes wetland area, `wetland_control`, `et_act`,
    and `gwflow_wetland` update its area, precipitation, evaporation, and seepage fields,
    and wetland output routines read it for reporting.
  wet_wat_m: Allocatable monthly wetland water-body array of type `water_body` (`water_body_module.f90:26`).
    It is allocated in `hru_allo` and used by `wetland_output` to accumulate and report monthly
    wetland storage summaries.
  wet_wat_y: Allocatable yearly wetland water-body array of type `water_body` (`water_body_module.f90:27`).
    It is allocated in `hru_allo` and used by `wetland_output` for yearly accumulation and
    reporting.
  wet_wat_a: Allocatable average-annual wetland water-body array of type `water_body` (`water_body_module.f90:28`).
    It is allocated in `hru_allo` and used by `wetland_output` for simulation-average reporting.
  ch_wat_d: Allocatable daily channel water-body array of type `water_body` (`water_body_module.f90:29`).
    It is allocated in `sd_channel_read`, populated by routing and sediment routines such
    as `ch_rtmusk`, `sd_channel_control3`, and `sd_channel_sediment3`, and read by channel
    output and basin aggregation routines.
  ch_wat_m: Allocatable monthly channel water-body array of type `water_body` (`water_body_module.f90:30`).
    It is allocated in `sd_channel_read` and accumulated in `sd_channel_output` for monthly
    channel water-body reporting.
  ch_wat_y: Allocatable yearly channel water-body array of type `water_body` (`water_body_module.f90:31`).
    It is allocated in `sd_channel_read`, accumulated in `sd_channel_output`, and also referenced
    by `time_control` for annual output timing.
  ch_wat_a: Allocatable average-annual channel water-body array of type `water_body` (`water_body_module.f90:32`).
    It is allocated in `sd_channel_read` and used by `sd_channel_output` for final simulation-average
    channel reporting.
  bch_wat_d: Daily basin-level channel water-body summary of type `water_body` (`water_body_module.f90:33`).
    `basin_sdchannel_output` initializes it from `wbodz` and accumulates daily channel values
    across all SWAT-DEG channels before writing basin output.
  bch_wat_m: Monthly basin-level channel water-body summary of type `water_body` (`water_body_module.f90:34`).
    `basin_sdchannel_output` accumulates it from the daily basin summary for monthly, yearly,
    and average-annual reporting.
  bch_wat_y: Yearly basin-level channel water-body summary of type `water_body` (`water_body_module.f90:35`).
    `basin_sdchannel_output` accumulates it from the monthly basin summary before yearly output.
  bch_wat_a: Average-annual basin-level channel water-body summary of type `water_body` (`water_body_module.f90:36`).
    `basin_sdchannel_output` accumulates it from yearly basin summaries for final basin channel
    reporting.
  bres_wat_d: Daily basin-level reservoir water-body summary of type `water_body` (`water_body_module.f90:37`).
    `basin_reservoir_output` initializes it from `wbodz` and accumulates all reservoir daily
    water-body values before reporting.
  bres_wat_m: Monthly basin-level reservoir water-body summary of type `water_body` (`water_body_module.f90:38`).
    `basin_reservoir_output` accumulates it from the daily basin summary and writes monthly
    basin reservoir output.
  bres_wat_y: Yearly basin-level reservoir water-body summary of type `water_body` (`water_body_module.f90:39`).
    `basin_reservoir_output` accumulates it from the monthly basin summary and writes yearly
    basin reservoir output.
  bres_wat_a: Average-annual basin-level reservoir water-body summary of type `water_body`
    (`water_body_module.f90:40`). `basin_reservoir_output` accumulates it from yearly basin
    summaries for final simulation-average reservoir reporting.
  wbody_wb: Pointer to the currently active reservoir or wetland `water_body` record (`water_body_module.f90:41`).
    It is used for reservoir and wetlands
type_components:
  water_body:
    area_ha: ha         |water body surface area
    precip: m3         |precip on the water body
    evap: m3         |evaporation from the water surface
    seep: m3         |seepage from bottom of water body
type_summaries:
  water_body: One water-body record holds the surface area and per-period water-balance fluxes
    (precipitation, evaporation, and bottom seepage) for a single reservoir, wetland, or channel
    water surface. All four active components default to zero; the commented-out fields (temperature,
    chlorophyll-a, CBOD, dissolved oxygen, Secchi depth) are reserved water-quality metrics
    that are not currently populated.
---

<!-- facts:header -->

Declaration-and-operator module for SWAT+ water-body bookkeeping. It owns the shared `water_body` record type, the zeroed template `wbodz`, and the reservoir, wetland, channel, basin-reservoir, and basin-channel summary arrays used by downstream control, routing, and output routines. The module also provides overloaded operators for adding, dividing, and averaging `water_body` values so those summaries can be accumulated and normalized consistently.

## Contained Procedures And Types

<!-- facts:members -->

## Module Variables

<!-- facts:variables -->

## Derived Types

<!-- facts:types -->



## Initialization

This module is a declaration-and-helper container. The `water_body` type defaults every component to zero, and the scalar templates (`wbodz`, the basin `bch_wat_*` and `bres_wat_*` records) are zero-initialized in their declarations. The array containers (`res_wat_*`, `wet_wat_*`, `ch_wat_*`) are allocated by setup routines (`res_allo`, `hru_allo`, `sd_channel_read`) and then seeded or reset to the zero template `wbodz` by the control and output routines. The module also defines the overloaded `+`, `/`, and `//` operators (`watbod_add`, `watbod_div`, `watbod_ave`) used to accumulate and average water-body records across daily, monthly, yearly, and average-annual reporting periods; `//` averages only the area term while summing the flux terms.

## Populated By

| Reader | Input file | Target | Behavior |
| --- | --- | --- | --- |
| [sym:actions] | `unit_2612, unit_3612` | `wbodz, res_wat_d, res_wat_m, res_wat_y, res_wat_a, wet_wat_d` | Imports the module and resets a wetland's daily water-body record to the zero template (`wet_wat_d(j) = wbodz`) when a wetland decision-table action fires, clearing the previous day's area/precip/evap/seep before the new state is computed. |
| [sym:basin_reservoir_output] | `unit_2100, unit_2104, unit_2101, unit_2105, unit_2102, unit_2106, unit_2103, unit_2107` | `wbodz, res_wat_d, res_wat_m, res_wat_y, res_wat_a, wet_wat_d` | Seeds the basin reservoir accumulator from the zero template (`bres_wat_d = wbodz`), sums each reservoir's `res_wat_d(ires)` into `bres_wat_d`, then rolls the totals up into monthly, yearly, and average-annual basin reservoir summaries (`bres_wat_m/y/a`) and writes them to the basin reservoir output files. |
| [sym:basin_sdchannel_output] | `unit_4900, unit_4904, unit_4901, unit_4905, unit_4902, unit_4906, unit_4903, unit_4907` | `wbodz, res_wat_d, res_wat_m, res_wat_y, res_wat_a, wet_wat_d` | Seeds the basin channel accumulator from the zero template (`bch_wat_d = wbodz`), sums each channel's `ch_wat_d(ichan)` into `bch_wat_d`, then accumulates monthly and yearly basin channel summaries (`bch_wat_m/y`) and writes them to the basin channel output files. |
| [sym:hru_control] | `unit_100100` | `wbodz, res_wat_d, res_wat_m, res_wat_y, res_wat_a, wet_wat_d` | Imports `water_body_module` for access to the shared wetland/water-body state used during HRU processing; no specific water-body symbol from the module is resolved in the extracted references for this routine. |
| [sym:res_initial] | `unit_105` | `wbodz, res_wat_d, res_wat_m, res_wat_y, res_wat_a, wet_wat_d` | During reservoir setup, computes the reservoir water-body surface area `res_wat_d(ires)%area_ha` from the initialized reservoir volume and the shape parameters (`res_ob(ires)%br1 * res(ires)%flo ** res_ob(ires)%br2`), giving later evaporation, precipitation, and depth calculations a starting area. |
| [sym:reservoir_output] | `unit_2540, unit_2544, unit_2541, unit_2545, unit_2542, unit_2546, unit_2543, unit_2547` | `wbodz, res_wat_d, res_wat_m, res_wat_y, res_wat_a, wet_wat_d` | Writes each reservoir's daily `res_wat_d(j)` (area, precip, evap, seep) to the reservoir output file, then accumulates and averages the monthly (`res_wat_m`) and yearly (`res_wat_y`) summaries using the module's `+` and `//` operators before writing those periods. |
| [sym:sd_channel_output] | `unit_2508, unit_2500, unit_2504, unit_2501, unit_2505, unit_2502, unit_2506, unit_2503, unit_2507` | `wbodz, res_wat_d, res_wat_m, res_wat_y, res_wat_a, wet_wat_d` | Writes each channel's daily `ch_wat_d(ichan)` area/precip/evap/seep to the channel output file, then accumulates monthly (`ch_wat_m`) and yearly (`ch_wat_y`) summaries, averaging the area term with the `//` operator before writing each period. |
| [sym:sd_channel_read] | `channel-lte.cha` | `wbodz, res_wat_d, res_wat_m, res_wat_y, res_wat_a, wet_wat_d` | During channel setup, allocates the channel water-body arrays (`ch_wat_d`, `ch_wat_m`, `ch_wat_y`, `ch_wat_a`) over the channel count so channel water-balance reporting has its containers before the model runs. |
| [sym:time_control] | `unit_*, unit_9003, unit_5100, unit_5101, unit_8000, unit_8001` | `wbodz, res_wat_d, res_wat_m, res_wat_y, res_wat_a, wet_wat_d` | In the time loop, resets channel water-body period accumulators to the zero template (e.g. `ch_wat_y(ich) = wbodz`) at the year/period rollover so fresh totals accumulate for the next reporting period. |
| [sym:wetland_output] | `unit_2548, unit_2552, unit_2549, unit_2553, unit_2550, unit_2554, unit_2551, unit_2555` | `wbodz, res_wat_d, res_wat_m, res_wat_y, res_wat_a, wet_wat_d` | Writes each wetland's daily `wet_wat_d(j)` (area, precip, evap, seep) to the wetland output file, then accumulates and averages the monthly (`wet_wat_m`) and yearly (`wet_wat_y`) summaries with the `+` and `//` operators before writing those periods. |

## Key Consumers

The importers fall into five roles. Allocation/setup routines (`res_allo`, `hru_allo`, `sd_channel_read`) allocate the reservoir, wetland, and channel arrays. Initialization routines (`res_initial`, `wet_initial`) set the starting surface area. Hydrology and control routines (`res_control`, `res_hydro`, `res_weir_release`, `wetland_control`, `sd_channel_sediment3`, `ch_rtmusk`, `et_act`) populate area, precipitation, evaporation, and seepage. Constituent, salt, pesticide, and groundwater routines (`res_cs`, `res_pest`, `res_salt`, `wet_cs`, `wet_salt`, `gwflow_reservoir`, `gwflow_wetland`) read area and seepage to convert water fluxes into mass losses. Output routines (`reservoir_output`, `wetland_output`, `sd_channel_output`, `basin_reservoir_output`, `basin_sdchannel_output`) write and roll up the summaries.

| Consumer | Uses | Effect |
| --- | --- | --- |
| [sym:basin_reservoir_output] | water_body_module | `water_body_module` matters because it owns the basin and reservoir water-body summary types used for storage or water-state reporting. The routine accumulates `res_wat_d(ires)` into `bres_wat_d`, then propagates monthly, yearly, and average-annual water-body summaries through `bres_wat_m`, `bres_wat_y`, and `bres_wat_a`, with `wbodz` providing the zero/reset water-body state. |
| [sym:basin_sdchannel_output] | water_body_module | The `water_body_module` supplies the basin water-body accumulators used alongside the hydrograph totals. `wbodz` seeds the basin water-body summaries, `ch_wat_d` provides the per-channel daily water-body contribution, and `bch_wat_d`, `bch_wat_m`, `bch_wat_y`, and `bch_wat_a` hold the basin-level totals or averages written by this routine. |
| [sym:res_initial] | water_body_module | The reservoir water-body state stores surface area. `res_initial` computes `res_wat_d(ires)%area_ha` from the initialized reservoir volume and shape parameters so later reservoir evaporation, precipitation, and water-surface calculations have the starting area. |
| [sym:reservoir_output] | water_body_module | `water_body_module` matters because reservoir output also reports reservoir water-body summaries for depth, storage, and other water-body metrics. The routine writes the period-specific `res_wat_*` states and resets them to `wbodz` after each period, so this module provides both the running values and the zeroed reset template. |
| [sym:sd_channel_output] | water_body_module | `water_body_module` provides the daily, monthly, yearly, and average-annual channel water-body summaries that are printed and accumulated here. The routine reports channel area, precipitation, evaporation, and seepage from these structures and resets month-end water-body state after it has been written. |
| [sym:sd_channel_read] | water_body_module | The module is imported, but no specific water-body symbol from it is resolved in the extracted references. It likely supports broader channel-water initialization, but the exact dependency is not visible in the provided lines. |
| [sym:wetland_output] | water_body_module | `water_body_module` supplies the wetland water-body storage arrays and the `wbodz` scratch water-body value used to reset monthly and yearly accumulators after they are written. |
| [sym:gwflow_reservoir] | `res_wat_d` | `water_body_module` holds `res_wat_d`, the reservoir water-body balance record. Its `seep` field is overwritten with the total exchange volume computed here so reservoir water-balance calculations use the same seepage total. |
| [sym:gwflow_wetland] | `wet_wat_d` | `water_body_module` provides the wetland area and seepage bookkeeping record for the HRU. It matters because the routine converts `wet_wat_d(hru_id)%area_ha` into wetted area for flux calculations and stores the resulting seepage in `wet_wat_d(hru_id)%seep`. |
| [sym:ch_rtmusk] | water_body_module | `water_body_module` provides the channel water-body accounting fields for evaporation and seepage. Those fields are reset and then populated so the routine can report channel losses separately from the hyd_output storage objects. |
| [sym:et_act] | water_body_module | `water_body_module` stores the daily wetland evaporation volume for each HRU, which this routine updates after converting between depth over area and water-body volume. |
| [sym:hru_allo] | water_body_module | `water_body_module` supplies the wetland water-body hydrograph arrays (`wet_wat_d`, `wet_wat_m`, `wet_wat_y`, `wet_wat_a`) that store wetland water-balance outputs and therefore must be allocated here with the rest of the wetland state. |
| [sym:res_allo] | water_body_module | `res_wat_d`, `res_wat_m`, `res_wat_y`, and `res_wat_a` are the water-body summary arrays for reservoirs. `res_allo` allocates them because reservoir water-body reporting depends on these containers being present before the reservoir model populates summary values. |
| [sym:res_control] | water_body_module | `water_body_module` holds the reservoir water-body state that stores surface area and the daily evaporation, precipitation, and seepage volumes computed here. |
| [sym:res_cs] | water_body_module | The water-body module provides reservoir surface area and seepage volume. Those fields are needed to turn seepage water loss into constituent mass loss and to convert settling velocity into a settled mass over the reservoir area. |
| [sym:res_hydro] | water_body_module | `water_body_module` provides the current water-body area `wbody_wb%area_ha`, which is converted to square meters and used to compute depth from volume for the weir and geometry-based release calculations. |
| [sym:res_pest] | water_body_module | This module supplies the reservoir surface area used to convert reservoir volume into average depth. That depth is required to turn areal transport coefficients into mass losses for volatilization, settling, and outflow. |
| [sym:res_salt] | water_body_module | It provides reservoir water-body seepage volume (`res_wat_d(jres)%seep`), which is needed to convert seepage water loss into salt mass loss. |
| [sym:res_weir_release] | water_body_module | `water_body_module` matters because the routine uses `wbody_wb%area_ha` as the water-surface area for wetlands. That area controls the head-to-volume conversion for non-paddy cases and scales the weir discharge formula. |
| [sym:sd_channel_sediment3] | water_body_module | Channel-water-body state is needed to store precipitation added to the channel water surface and to compute the channel water surface area used in the precipitation volume calculation. |
| [sym:wet_cs] | water_body_module | The wetland seepage and area terms come from `wet_wat_d`; `wet_cs` uses seepage volume and wetland surface area to convert concentration into seepage loss and settling mass. |
| [sym:wet_initial] | water_body_module | The water-body state holds the daily wetland surface area used by downstream water-balance and area-dependent calculations. `wet_initial` resets and recomputes `wet_wat_d(iihru)%area_ha` from the initialized wetland volume and hydraulic geometry. |
| [sym:wet_salt] | water_body_module | The wetland seepage volume comes from `wet_wat_d(ihru)%seep`; that water loss is what gets converted into salt seepage mass in this routine. |
| [sym:wetland_control] | water_body_module | `water_body_module` provides `wet_wat_d`, the daily wetland water-body record that stores area, precipitation, and seepage. That record is the bridge between the hydrologic balance and later wetland output summaries. |

## Lineage

`water_body_module.f90` was introduced in `df07e3f` (2024-03-05, "init all") and has been changed in 6 non-merge commit(s) since, most recently `4978f46` (2025-06-26, "quickfix of error"). Lineage is reconstructed from commit metadata (SHA, date, subject); per-line diffs were unavailable in this build environment, so only the commits touching `water_body_module.f90` are listed.

- `4978f46` (2025-06-26) — quickfix of error
- `a03cc8b` (2025-06-26) — Add yearly irrigation calculations across modules
- `889136d` (2025-02-03) — Fix typos
- `94b6dec` (2024-05-30) — Added latest source code from bitbucket
- `35b029c` (2024-03-24) — Mar 19 status
- `df07e3f` (2024-03-05) — init all

## Review Notes

- Module `water_body_module` has no extracted module-level documentation comment.
- No lineage commits were resolved for `water_body_module.f90:1-103`, so lineage impacts remain empty.
- type_notes summary, initialization_intro, reader behaviors, and used_by_intro were completed locally from water_body_module.f90 and the reader source; hru_control imports the module but no specific water-body symbol was resolved for it.
- Lineage was reconstructed from file-level commit metadata; per-line diffs were unavailable in this environment (blobless clone), so line-span filtering was not applied.
