---
kind: procedure
symbol: hru_lte_control
title: hru_lte_control
status: filled
source_hash: 663c929386dbbf80
version_label: SWAT+ 62.0.0
args:
  isd: Index of the HRU-LTE dynamic object being updated. It selects the `hlt(isd)` and `hltwb_d(isd)`
    records that this routine reads and writes.
locals:
  a1: Runoff curve-number coefficient used in the effective precipitation runoff equation.
    Initial value `.2`.
  a2: Runoff curve-number coefficient used in the effective precipitation runoff equation.
    Initial value `.8`.
  ihlt_db: Index into `hlt_db` for the current HRU property record. Initial value `0`.
  iwgn: Weather generator station index from the selected weather station. Initial value `0`.
  iplt: Plant database index for the current HRU plant. Initial value `0`.
  precip: Daily precipitation read from the weather station. Initial value `0.`.
  tmax: Daily maximum temperature read from the weather station. Initial value `0.`.
  tmin: Daily minimum temperature read from the weather station. Initial value `0.`.
  raobs: Observed solar radiation used in PET calculations. Initial value `0.`.
  rmx: Maximum solar radiation used in Hargreaves PET. Initial value `0.`.
  tave: Daily mean temperature computed from `tmax` and `tmin`. Initial value `0.`.
  yield: Crop yield placeholder for output records. Initial value `0.`.
  ws: Water-stress ratio used in growth and irrigation decisions. Initial value `0.`.
  strsair: Aeration-stress factor for plant growth. Initial value `0.`.
  snowfall: Daily snowfall amount accumulated from precipitation when temperature is below
    freezing. Initial value `0.`.
  snowmelt: Daily snowmelt amount used to augment effective precipitation. Initial value `0.`.
  runoff: Daily surface runoff generated from precipitation and snowmelt. Initial value `0.`.
  xx: Intermediate runoff and curve-number helper variable. Initial value `0.`.
  exp: Intrinsic exponential helper used in several formulas.
  r2: Intermediate curve-number related storage term. Initial value `0.`.
  max: Intrinsic maximum helper used to bound values.
  cn_sd: Computed curve number for the current day. Initial value `0.`.
  precipeff: Effective precipitation after snowmelt is added. Initial value `0.`.
  xxi: Seasonal solar geometry helper based on month. Initial value `0.`.
  xsd: Seasonal solar declination-like helper. Initial value `0.`.
  ch: Cosine-like seasonal geometry term used to derive latitude angle. Initial value `0.`.
  tan: Intrinsic tangent helper used in seasonal geometry.
  hlat: Latitude angle helper derived from `ch`. Initial value `0.`.
  acos: Intrinsic arccosine helper used in seasonal geometry.
  ramm: Hargreaves extraterrestrial radiation helper. Initial value `0.`.
  pet: Potential evapotranspiration for the day. Initial value `0.`.
  tstress: Temperature stress factor for plant growth. Initial value `0.`.
  tk: Temperature in Kelvin used in Priestley-Taylor PET. Initial value `0.`.
  alb: Albedo used in Priestley-Taylor PET. Initial value `0.`.
  d: Slope of saturation vapor pressure curve used in Priestley-Taylor PET. Initial value
    `0.`.
  gma: Psychrometric factor used in Priestley-Taylor PET. Initial value `0.`.
  ho: Net radiation helper used in Priestley-Taylor PET. Initial value `0.`.
  aph: Priestley-Taylor alpha coefficient. Initial value `0.`.
  aet: Actual evapotranspiration for the day. Initial value `0.`.
  b1: ET adjustment factor applied to actual ET during growth. Initial value `0.`.
  delg: Daily growth increment based on temperature and PHU. Initial value `0.`.
  parad: Radiation available for biomass production. Initial value `0.`.
  drymat: Daily dry matter increment. Initial value `0.`.
  satco: Saturation coefficient used in aeration stress. Initial value `0.`.
  pl_aerfac: Aeration threshold factor used in aeration stress. Initial value `0.`.
  iend: Decision-table index for the end-of-growth rule set. Initial value `0`.
  istart: Decision-table index for the start-of-growth rule set. Initial value `0`.
  scparm: Aeration stress parameter derived from saturation coefficient. Initial value `0.`.
  air: Irrigation water applied to the HRU. Initial value `0.`.
  amin1: Intrinsic minimum helper used to cap irrigation and flows.
  tgx: Temperature response helper for stress calculation. Initial value `0.`.
  rto: Temperature stress ratio. Initial value `0.`.
  reg: Combined growth limitation factor from water, temperature, and aeration stress. Initial
    value `0.`.
  deltalai: Daily leaf-area increment. Initial value `0.`.
  sw_excess: Soil water above available water capacity. Initial value `0.`.
  swf: Soil-water fraction used in lateral flow and aeration calculations. Initial value `0.`.
  flowlat: Daily lateral soil flow. Initial value `0.`.
  f: Leaf-area development helper based on growth stage. Initial value `0.`.
  ff: Incremental leaf-area change helper. Initial value `0.`.
  flow_tile: Daily tile drainage flow. Initial value `0.`.
  perc: Daily percolation out of the soil profile. Initial value `0.`.
  revap: Amount of ET taken from shallow groundwater. Initial value `0.`.
  percdeep: Percolation routed to deep groundwater. Initial value `0.`.
  chflow: Total water yield to the channel from runoff, lateral flow, tile flow, and groundwater
    flow. Initial value `0.`.
  chflow_m3: Channel flow converted to cubic meters per day. Initial value `0.`.
  runoff_m3: Surface runoff converted to cubic meters per day. Initial value `0.`.
  bf_m3: Baseflow component converted to cubic meters per day. Initial value `0.`.
  peakr: Peak runoff rate used for hydrograph and sediment calculations. Initial value `0.`.
  peakrbf: Peak baseflow contribution to the hydrograph. Initial value `0.`.
  sedin: Sediment input/yield estimate before conversion to output units. Initial value `0.`.
  qssubconc: Subsurface sediment concentration constant. Initial value `0.`.
  qssub: Subsurface sediment contribution added to sediment yield. Initial value `0.`.
  cnv: Conversion factor from mm over area to cubic meters. Initial value `0.`.
uses:
  hru_lte_module: Provides the HRU-LTE property and dynamic state that this routine updates
    for the selected object.
  hydrograph_module: Provides the current object’s property index, weather station index,
    and area used to scale flows and sediment.
  output_landscape_module: Receives the daily water-balance and loss outputs produced by this
    routine.
  basin_module: Controls whether management output is written to the management and CSV files.
  climate_module: Supplies the daily weather inputs used for runoff, snow, PET, and growth
    calculations.
  time_module: Provides the current simulation date used in seasonal calculations and output
    records.
  plant_data_module: Provides plant parameters used for growth, stress, and output labeling.
---

<!-- facts:header -->

Controls one HRU-LTE object for a single day. It computes water balance, plant growth, sediment yield, and management outputs for the selected HRU.

## Bottom Line

`hru_lte_control` is the daily control routine for an HRU-LTE object. It pulls weather, plant, and HRU property state, computes runoff, snow, evapotranspiration, growth, irrigation, lateral flow, tile flow, percolation, groundwater updates, and sediment yield, then stores the results in the landscape output arrays and hydrograph state.

It matters because it is the main place where the HRU-LTE simulation turns climate and object properties into daily landscape outputs and routing inputs. It also invokes the conditional management machinery so growth-stage actions can be evaluated and applied at the right times.

## Arguments

<!-- facts:arguments -->

## Where It Fits

Called from `command` when the current object type is `hru_lte`. It uses the object index already selected by `command`, then updates daily HRU-LTE state and outputs for that object.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. Load object and weather state | Read the current HRU property index, weather station index, weather generator index, plant index, precipitation, temperature, and solar radiation from module state. |
| 2. Initialize daily variables | Compute mean temperature and reset daily accumulators for yield, water stress, snow, and air stress. |
| 3. Compute runoff and snow | Derive curve number, partition precipitation into snowfall or runoff, update snow storage, and add effective precipitation to soil water. |
| 4. Compute seasonal PET | Use month and weather data to compute seasonal geometry and potential evapotranspiration with either Hargreaves or Priestley-Taylor, then apply the ET coefficient. |
| 5. Compute growth and stress | Calculate actual ET, start or end plant growth via conditional actions, and accumulate growing-season ET and PET when growth is active. |
| 6. Write management output | Optionally write management and CSV records containing date, plant name, leaf area, biomass, and yield. |
| 7. Update biomass and leaf area | During growth, compute temperature, water, and aeration stress, apply irrigation if enabled, and update biomass, leaf area, and growth progress. |
| 8. Route soil water losses | Apply growing-season ET adjustment, then compute lateral flow, tile flow, percolation, groundwater recharge, revap, and deep aquifer transfer. |
| 9. Compute channel and sediment | Convert water components to channel flow, estimate peak runoff, and compute sediment yield including subsurface sediment. |
| 10. Store daily outputs | Populate the daily water-balance and loss output arrays with the computed daily values. |
| 11. Populate hydrograph state | Fill plant-weather output fields and the object hydrograph record used for downstream routing. |
| 12. Return | Exit the subroutine after all daily state and outputs have been updated. |

## Modules Used

<!-- facts:uses -->

| Module | State touched | Key components |
| --- | --- | --- |
| [sym:hru_lte_module] | `hlt, hlt_db` | `hlt(isd)%iplant, hlt(isd)%wrt1, hlt(isd)%wrt2, hlt(isd)%sw, hlt(isd)%smx, hlt(isd)%snow, hlt(isd)%yls, hlt_db(ihlt_db)%ipet, hlt(isd)%etco, hlt(isd)%awc, hlt(isd)%gro, hlt(isd)%start, hlt(isd)%aet, hlt(isd)%pet, hlt(isd)%end, hlt(isd)%alai, hlt(isd)%dm, hlt(isd)%phu, hlt(isd)%g, hlt(isd)%stress, hlt(isd)%por, hlt_db(ihlt_db)%irr, hlt_db(ihlt_db)%irrsrc, hlt(isd)%gw, hlt(isd)%gwdeep, hlt(isd)%hufh, hlt(isd)%sc, hlt_db(ihlt_db)%slope, hlt_db(ihlt_db)%slopelen, hlt(isd)%tdrain, hlt(isd)%perco, hlt_db(ihlt_db)%revapc, hlt_db(ihlt_db)%percc, hlt(isd)%gwflow, hlt_db(ihlt_db)%abf, hlt_db(ihlt_db)%tc, hlt(isd)%uslefac` |
| [sym:hydrograph_module] | `ob` | `ob(icmd)%props, ob(icmd)%wst, ob(icmd)%area_ha` |
| [sym:output_landscape_module] | `hltwb_d, hltls_d` | `hltwb_d(isd)%precip, hltwb_d(isd)%snofall, hltwb_d(isd)%snomlt, hltwb_d(isd)%surq_gen, hltwb_d(isd)%latq, hltwb_d(isd)%wateryld, hltwb_d(isd)%perc, hltwb_d(isd)%et, hltwb_d(isd)%ecanopy, hltwb_d(isd)%eplant, hltwb_d(isd)%esoil, hltwb_d(isd)%surq_cont, hltwb_d(isd)%cn, hltwb_d(isd)%sw, hltwb_d(isd)%sw_final, hltwb_d(isd)%sw_300, hltwb_d(isd)%snopack, hltwb_d(isd)%pet, hltwb_d(isd)%qtile, hltwb_d(isd)%irr, hltls_d(isd)%sedyld, hltls_d(isd)%sedorgn, hltls_d(isd)%sedorgp` |
| [sym:basin_module] | `pco` | `pco%mgtout, pco%csvout` |
| [sym:climate_module] | `wst` | `wst(iwst)%wco%wgn, wst(iwst)%weat%precip, wst(iwst)%weat%tmax, wst(iwst)%weat%tmin, wst(iwst)%weat%solrad, wst(iwst)%weat%solradmx` |
| [sym:time_module] | `time` | `time%mo, time%day, time%yrc` |
| [sym:plant_data_module] | `pldb, plcp` | `pldb(iplt)%plantnm, pldb(iplt)%t_base, pldb(iplt)%bio_e, pldb(iplt)%t_opt, plcp(iplt)%leaf2, pldb(iplt)%blai` |

## Local Variables

<!-- facts:locals -->

## State Changes

| Target | When | Meaning |
| --- | --- | --- |
| `iwst` | After reading object and weather state | Set from `ob(icmd)%wst` so the routine uses the correct weather station for this HRU-LTE object. |
| `hlt(isd)%snow` | When precipitation falls as snow | Increases by precipitation during subfreezing days and decreases when snowmelt is limited by stored snow. |
| `hlt(isd)%sw` | When precipitation, snowmelt, runoff, irrigation, ET, lateral flow, tile flow, and percolation are applied | Updated repeatedly as water is added to or removed from the soil profile during the daily water balance. |
| `d_tbl` | When growth starts or ends | Pointer is redirected to the start or end decision table so `conditions` and `actions` operate on the correct rule set. |
| `hlt(isd)%aet` | During active growth | Accumulated with daily actual ET for water-stress accounting. |
| `hlt(isd)%pet` | During active growth | Accumulated with daily potential ET for water-stress accounting. |
| `hlt(isd)%g` | During active growth | Incremented by daily growth progress based on temperature and PHU. |
| `hlt(isd)%gw` | After percolation and groundwater routing | Receives percolation from the soil profile and is then reduced by groundwater flow, revap, and deep percolation. |
| `hlt(isd)%gwdeep` | After deep percolation routing | Receives the portion of groundwater percolation routed to the deep aquifer. |
| `hlt(isd)%dm` | During active growth | Increased by daily dry matter production scaled by the combined stress factor. |
| `hlt(isd)%hufh` | During active growth | Updated to the current leaf-area development factor so leaf-area increment can be computed from the change in that factor. |
| `hlt(isd)%alai` | During active growth | Increased by the computed daily leaf-area increment. |
| `hlt(isd)%gwflow` | After groundwater routing | Updated as a routed groundwater-flow component using the aquifer alpha factor and percolation. |
| `hltwb_d(isd)%precip` | At end of daily water balance | Stores the day’s precipitation for water-balance output. |
| `hltwb_d(isd)%snofall` | At end of daily water balance | Stores the day’s snowfall for water-balance output. |
| `hltwb_d(isd)%snomlt` | At end of daily water balance | Stores the day’s snowmelt for water-balance output. |
| `hltwb_d(isd)%surq_gen` | At end of daily water balance | Stores the day’s generated surface runoff for water-balance output. |
| `hltwb_d(isd)%latq` | At end of daily water balance | Stores lateral flow plus groundwater flow for water-balance output. |
| `hltwb_d(isd)%wateryld` | At end of daily water balance | Stores total water yield to the channel for water-balance output. |
| `hltwb_d(isd)%perc` | At end of daily water balance | Stores soil-profile percolation for water-balance output. |
| `hltwb_d(isd)%et` | At end of daily water balance | Stores actual evapotranspiration for water-balance output. |
| `hltwb_d(isd)%ecanopy` | At end of daily water balance | Set to zero because canopy evaporation is not separately reported here. |
| `hltwb_d(isd)%eplant` | At end of daily water balance | Set to zero because plant transpiration is not separately partitioned here. |
| `hltwb_d(isd)%esoil` | At end of daily water balance | Set to zero because soil evaporation is not separately partitioned here. |

## File I/O

<!-- facts:io -->


## Lineage

`hru_lte_control.f90` was introduced in `df07e3f` (2024-03-05, "init all") and has been changed in 5 non-merge commit(s) since, most recently `bd18ad4` (2025-11-24, "Pr 107 (#108)"). Lineage is reconstructed from commit metadata (SHA, date, subject); per-line diffs were unavailable in this build environment, so only the commits touching `hru_lte_control.f90` are listed.

- `bd18ad4` (2025-11-24) — Pr 107 (#108)
- `f1e61a3` (2024-10-08) — fixed tabs
- `39fabde` (2024-08-08) — Initialized varables with python script, corrected input data where integers where floats in two input files, trapped underflow errors in th…
- `94b6dec` (2024-05-30) — Added latest source code from bitbucket
- `df07e3f` (2024-03-05) — init all

## Review Notes

- No source uncertainty was needed for the main control flow; the routine is directly backed by the visible source lines.
- The `actions` callee has no completed overlay in the packet, so its purpose is inferred only from the call site and the raw source contract.
- The `conditional_module` import is used by the called management routines, but no direct outside references were resolved for this procedure.
- Direct file I/O is limited to management output writes on units 4700 and 4701; the files are managed elsewhere.
- warning: missing_doc: Procedure 'hru_lte_control' has no extracted documentation comment.
- Lineage was reconstructed from file-level commit metadata; per-line diffs were unavailable in this environment (blobless clone), so line-span filtering was not applied.
