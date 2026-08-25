---
kind: procedure
symbol: actions
title: actions
status: filled
source_hash: b9bfed3e5849d4b8
version_label: SWAT+ 62.0.0
args:
  ob_cur: Current object index for the active HRU or other object being processed. Many cases
    fall back to this value when the action record does not specify an explicit object number.
  ob_num: Sequential object number for the current object context. It is used in some cases
    as the receiving or source object identifier, such as manure allocation and irrigation
    demand handling.
  idtbl: Decision-table index for the current management schedule. It selects the active action
    counters and day counters in `pcom(j)%dtbl(idtbl)` and is used to resolve schedule-specific
    behavior.
locals:
  icom: 'Plant-community database index used to look up the current community definition for
    planting, harvest, kill, and related crop selection logic. Initial value: `0`.'
  iac: 'Loop index over decision-table actions; selects the current action being evaluated
    and executed. Initial value: `0`.'
  ial: 'Loop index over alternative-condition checks; used to determine whether any condition
    path activates the current action. Initial value: `0`.'
  iburn: 'Fire-operation database index used by the burn case to select burn parameters. Initial
    value: `0`.'
  idtill: 'Tillage-operation database index used to select tillage mixing parameters and output
    labels. Initial value: `0`.'
  ifertop: 'Chemical-application database index for fertilizer surface-fraction routing. Initial
    value: `0`.'
  ifrt: 'Fertilizer database index used by fertilizer and manure cases. Initial value: `0`.'
  ipestop: 'Chemical-application database index for pesticide surface-fraction routing. Initial
    value: `0`.'
  ipst: 'Pesticide database index used by pesticide application. Initial value: `0`.'
  iharvop: 'Harvest-operation database index used to choose harvest type and minimum biomass
    threshold. Initial value: `0`.'
  iihru: 'HRU index used when initializing impounded water. Initial value: `0`.'
  ilu: 'Land-use management code used during land-use and snow-change updates. Initial value:
    `0`.'
  j: 'Current HRU/object index being acted on. It is reassigned in most cases to either `ob_cur`
    or the action''s explicit object number. Initial value: `0`.'
  iob: 'Object index for source or receiving water bodies, reservoirs, or aquifers. Initial
    value: `0`.'
  idp: 'Plant database index for the active crop or transplant record. Initial value: `0`.'
  istr: 'Structure database index used for tile drains, septic systems, filter strips, grass
    waterways, and BMPs. Initial value: `0`.'
  istr1: 'Secondary structure index used when crosswalking a named structure record from a
    database. Initial value: `0`.'
  iplt_bsn: 'Basin-level plant index used to accumulate harvested area and yield by crop.
    Initial value: `0`.'
  irrop: 'Irrigation-operation database index used to determine application amount, efficiency,
    and runoff split. Initial value: `0`.'
  igr: 'Grazing-operation database index used to select grazing parameters. Initial value:
    `0`.'
  ireg: 'Crop-region index used for regional calibration yield accumulation. Initial value:
    `0`.'
  ilum: 'Land-use management calibration index used when accumulating regional yield statistics.
    Initial value: `0`.'
  isrc: 'Source object index used in irrigation and transfer-related cases. Initial value:
    `0`.'
  isched: 'Management schedule index for the current HRU. Used to resolve auto-crop names
    and schedule-specific behavior. Initial value: `0`.'
  ipud: 'Puddling-operation database index used to select puddling parameters. Initial value:
    `0`.'
  ipdl: 'Loop index used to crosswalk puddling database entries by name. Initial value: `0`.'
  ires: 'Wetland or reservoir database index used when crosswalking impoundment settings.
    Initial value: `0`.'
  idb: 'Generic database loop index used in puddling and other crosswalks. Initial value:
    `0`.'
  imallo: 'Manure-allocation object index used by manure-demand handling. Initial value: `0`.'
  itrn: 'Manure-demand transfer index within a manure-allocation object. Initial value: `0`.'
  iplt: 'Loop index over basin plant list used when adding new plants after land-use change.
    Initial value: `0`.'
  num_plts_cur: 'Count of current basin plants used while extending the basin plant list.
    Initial value: `0`.'
  hru_rcv: Receiving HRU index for tile-flow routing. It is derived from the source HRU's
    saturated-buffer routing pointer.
  hiad1: 'Intermediate harvest-index adjustment used in the `grow_end` case. Initial value:
    `0.`.'
  biomass: 'Current plant biomass used to test harvest thresholds and report management output.
    Initial value: `0.`.'
  frt_kg: 'Applied fertilizer or manure mass in kg/ha. Initial value: `0.`.'
  harveff: 'Harvest efficiency used in residue harvest cases. Initial value: `0.`.'
  wur: 'Water-use ratio used to compute harvest index adjustment in `grow_end`. Initial value:
    `0.`.'
  rto: 'Fraction of source water removed from aquifer, channel, or reservoir during irrigation
    transfer. Initial value: `0.`.'
  rto1: 'Complement of `rto`, representing the remaining fraction left in the source. Initial
    value: `0.`.'
  pest_kg: 'Applied pesticide mass in kg/ha after efficiency adjustment. Initial value: `0.`.'
  chg_par: Temporary variable used by `cn_update` to hold the updated curve number returned
    by `chg_par`.
  yield: 'Temporary yield value used in growth-end and kill output. Initial value: `0.`.'
  sumpst: 'Counter for pesticide applications. Initial value: `0.`.'
  rock: 'Rock-factor multiplier used when recomputing USLE support factors. Initial value:
    `0.`.'
  p_factor: 'Previous USLE P factor stored before a land-use or conservation-practice change.
    Initial value: `0.`.'
  cn_prev: 'Previous curve number stored before `cn_update`. Initial value: `0.`.'
  stor_m3: 'Temporary storage volume in cubic meters used for aquifer irrigation demand checks.
    Initial value: `0.`.'
  action: 'Flag indicating whether any alternative condition activated the current action.
    Initial value: `""`.'
  lu_prev: 'Previous land-use management code saved before a land-use change. Initial value:
    `""`.'
  snow_prev: 'Previous snow-management code saved before a snow change. Initial value: `""`.'
uses:
  conditional_module: Provides the decision-table action records and condition outcomes that
    determine whether each management case runs.
  climate_module: Imported by the procedure, but no concrete symbol usage was resolved in
    the provided evidence.
  time_module: Provides the current simulation date used in management output records.
  aquifer_module: Used when irrigation draws water from an aquifer source and the source storage
    must be reduced proportionally.
  hru_module: Provides HRU state used across irrigation, planting, harvest, land-use change,
    drainage, and output logging.
  soil_module: Provides soil water, texture, and profile pools used by fertilizer, tillage,
    puddling, land-use change, and management output.
  plant_module: Provides plant-community state, action counters, and crop metadata used by
    planting, harvest, kill, grazing, and reset cases.
  plant_data_module: Provides plant database names and parameters used to match crops, compute
    transplant and harvest behavior, and reset phenology.
  mgt_operations_module: Provides operation databases and management metadata used to parameterize
    irrigation, fertilizer, harvest, burn, grazing, puddling, and structural BMP actions.
  landuse_data_module: Imported by the procedure, but no concrete symbol usage was resolved
    in the provided evidence.
  tillage_data_module: Provides tillage operation names and mixing efficiency used in tillage
    and wet-tillage actions.
  reservoir_module: Provides wetland and reservoir geometry/state used for irrigation demand,
    impoundment, and weir-height management.
  sd_channel_module: Used by channel-change actions to update channel cover and order.
  septic_data_module: Used when crosswalking septic installation records by name.
  hru_lte_module: Provides HRU-LTE growth state used by grow-init and grow-end actions.
  basin_module: Provides basin-level print control and carbon-code control used by management
    output and tillage branching.
  organic_mineral_mass_module: Provides plant biomass and residue pools updated by harvest,
    kill, burn, and grazing actions.
  hydrograph_module: Provides hydrologic transfer and wetland state used by irrigation, diversion,
    impoundment, and wetland mixing actions.
  output_landscape_module: Imported by the procedure, but no concrete symbol usage was resolved
    in the provided evidence.
  constituent_mass_module: Used to gate constituent transfers in irrigation and water-allocation
    cases.
  calibration_data_module: Imported by the procedure, but no concrete symbol usage was resolved
    in the provided evidence.
  fertilizer_data_module: Imported by the procedure, but no concrete symbol usage was resolved
    in the provided evidence.
  maximum_data_module: Provides database-size limits and basin plant counters used in crosswalk
    loops and basin plant list updates.
  tiles_data_module: Imported by the procedure, but no concrete symbol usage was resolved
    in the provided evidence.
  water_body_module: Imported by the procedure, but no concrete symbol usage was resolved
    in the provided evidence.
  reservoir_data_module: Provides wetland database records and initial-condition pointers
    used by wetland initialization and impoundment actions.
---

<!-- facts:header -->

Dispatches and executes management actions for a selected HRU or other object based on the current decision table entry. It applies irrigation, fertilizer, manure, planting, harvest, tillage, land-use changes, structural BMPs, and related resets while updating counters and optional management output.

## Bottom Line

`actions` is the central management dispatcher for SWAT+ auto-operations. For each active decision-table action, it checks whether the action is enabled by the current conditions, then routes to the matching case and performs the corresponding state updates and helper calls.

It matters because this is where many model interventions actually happen: water is moved between sources and HRUs, nutrients are applied, crops are planted or harvested, land-use and structural parameters are changed, and the per-action counters that limit repeat execution are advanced. When management output is enabled, it also writes detailed event records to the management log files.

## Arguments

<!-- facts:arguments -->

## Where It Fits

Runs inside the daily HRU/object loop (called from `hru_control`, `hru_lte_control`, `time_control`, and the allocation controllers `mallo_control`/`wallo_demand`). For the active decision table `idtbl` it executes every action whose alternative was hit, applying management operations (irrigation, fertilizer/manure, tillage, planting/harvest/kill, grazing, burning, land-use and structural changes) to the HRU. Its writes feed the management and land-use output files, and the state it changes (soil, plant, irrigation, reservoir/channel/aquifer storage) is consumed by the rest of the daily land-phase and routing simulation.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. Select firing actions and dispatch | Loop over every action in the decision table. An action fires only when some alternative both hit (`d_tbl%act_hit(ial) == "y"`) and lists this action as an outcome (`d_tbl%act_outcomes(iac,ial) == "y"`); the alternative loop exits on the first match. When the action fires, dispatch on its type through the routine's single large `select case`. |
| 2. Compute manure and irrigation demand | Handle the demand-setting actions that do not move water themselves. `manure_demand` stages a manure allocation request with its source object, application rate and method. `irr_demand` sets paddy target and threshold ponding depths and derives demand from the current ponded depth, or sets a volumetric demand from the action constant and applies it directly when the source is `unlim`. `res_irr_dmd` records demand against a reservoir and bumps its irrigation tracker; `irr_wallo` sets demand for the water-allocation path so it only irrigates when supply exists. |
| 3. Irrigate from aquifer, channel or reservoir | Apply an irrigation event after checking the per-year application limit, then branch on the source object type: withdraw from an aquifer, from a channel or swat-deg channel, or from a reservoir, updating the source's storage and the HRU's applied and runoff depths from the `irr.ops` application efficiency and surface-runoff fraction. |
| 4. Apply fertilizer, manure and tillage | Run the chemical and tillage applications: `fertilize` and `manure` resolve the database record, amount and surface-application fraction, then call the plant fertilizer or manure routine along with the salt and constituent companions. `fert_future` schedules an application for a later day, and `till` performs a tillage mixing operation. Each logs a management record when management output is enabled. |
| 5. Plant or transplant a crop | Establish a plant in the community: match the requested plant against the community's slots, set the current plant's growth status, accumulated heat units and dormancy flags, and initialize the mass pools so the plant begins growing on the following day. |
| 6. Harvest by harvest-operation type | Harvest each plant in the community whose biomass exceeds the operation's minimum, dispatching on the harvest type in `harvop_db`: biomass, tree and stripper harvests go through `mgt_harvbiomass`; grain and picker through `mgt_harvgrain`; tuber and peanuts through `mgt_harvtuber`; residue through `mgt_harvresidue` with the action's harvest efficiency. Accumulate total and yearly yield and increment the harvest count, then update the land-use calibration record. |
| 7. Kill and harvest-kill the community | `kill` moves the standing plant mass to residue and clears the plant's growth state. `harvest_kill` first harvests using the same `harvop_db` type dispatch as the harvest action, then kills the plant, accumulates yield, and updates the land-use calibration record for the region. |
| 8. Reset counters and apply pesticide | Handle the bookkeeping resets — rotation year, harvest, kill, plant and irrigation counters — that let a decision table restart a cycle. `pest_apply` then resolves the pesticide record and application fraction, scales the rate by the chemical application efficiency, applies it, logs the event and increments the action counter. |
| 9. Graze and set growth season | `graze` starts a grazing period on the HRU with its operation parameters. `grow_init` and `grow_end` open and close the growing season for the community, setting per-plant growth and dormancy status and resetting accumulated heat units at the season boundary. |
| 10. Divert, transfer and control tile flow | Water-management actions on flow objects. `divert` selects the diverted amount by option — a set rate, a minimum, a maximum capped at actual flow, all flow, no flow, or a constant fraction. `transfer` moves a set flow rate between objects. `tileflo_contol` applies the same option set in depth units to tile flow, and `tiledep_control` sets the drain depth for drainage water management. |
| 11. Set reservoir demand, impoundment and puddling | Reservoir and wetland control: `res_demand` sets a storage-based demand target, `impound_off` and `impound_on` clear or establish the HRU's surface impoundment across the wetland database, `weir_height` sets the outflow weir elevation, and `puddle` applies a puddling operation by matching the puddle and tillage database records. |
| 12. Change HRU fraction, land use and snow | Structural changes to the HRU definition. `hru_fr_update` rewrites the landscape-unit and routing-unit element fractions through `hru_fr_change`. `lu_change` swaps the HRU's land use and management to a new record and re-derives the plant community. `snow_change` switches the snow database record and resets the snow water equivalent. All three write an unguarded land-use-change record to unit 3612. |
| 13. Install conservation practices and structures | Apply conservation and structural BMPs: the P delivery factor, contouring, strip cropping and terracing adjust land-use parameters; tile drains, septic systems, filter strips, grassed waterways and user-defined BMPs are installed by matching their database record and calling `structure_set_parms`, with `grassww_uninstall` reversing the grassed waterway. Each logs an unguarded record to unit 3612. |
| 14. Change channel, burn, update CN and herd | Remaining actions: `chan_change` swaps the channel database record, `burn` removes plant and residue mass by the burn fraction across the community, `cn_update` adjusts the curve number within the 35-95 bounds through `chg_par` and recomputes retention with `curno`, `pheno_reset` opens and closes the monsoon initiation period per plant, and `herd` handles the animal herd action. Closing the `select case` ends the action loop. |

## Modules Used

<!-- facts:uses -->

| Module | State touched | Key components |
| --- | --- | --- |
| [sym:conditional_module] | `d_tbl%acts, d_tbl%alts, d_tbl%act_hit(ial), d_tbl%act_outcomes(iac,ial), d_tbl%act(iac)%typ, d_tbl%act(iac)%name, d_tbl%act(iac)%option, d_tbl%act(iac)%file_pointer, d_tbl%act(iac)%const, d_tbl%act(iac)%const2, d_tbl%act(iac)%ob_num, d_tbl%act_typ(iac), d_tbl%act_app(iac), d_tbl%lu_chg_mx(iac), d_tbl%snow_chg_mx(iac)` | `d_tbl%acts, d_tbl%alts, d_tbl%act_hit(ial), d_tbl%act_outcomes(iac,ial), d_tbl%act(iac)%typ, d_tbl%act(iac)%name, d_tbl%act(iac)%option, d_tbl%act(iac)%file_pointer, d_tbl%act(iac)%const, d_tbl%act(iac)%const2, d_tbl%act(iac)%ob_num, d_tbl%act_typ(iac), d_tbl%act_app(iac), d_tbl%lu_chg_mx(iac), d_tbl%snow_chg_mx(iac)` |
| [sym:climate_module] | `No resolved outside references were provided in the context packet` |  |
| [sym:time_module] | `time` | `time%yrc, time%mo, time%day_mo` |
| [sym:aquifer_module] | `aqu_d, aqu_prm` | `aqu_d(iob)%stor, aqu_prm(iob)%area_ha` |
| [sym:hru_module] | `hru, sol_sumno3, sol_sumsolp, phubase, cn2, fertno3, fertnh3, fertorgn, fertorgp, fertsolp, qtile, snodb` | `hru(j)%irr_hmax, hru(j)%irr_hmin, hru(j)%area_ha, hru(j)%irr_yr, hru(j)%mgt_ops, hru(j)%land_use_mgt, hru(j)%land_use_mgt_c, hru(j)%dbs%surf_stor, hru(j)%dbs%land_use_mgt, hru(j)%dbs%snow, hru(j)%lumv%sdr_dep, hru(j)%lumv%usle_p, hru(j)%lumv%usle_ls, hru(j)%lumv%usle_mult, hru(j)%topo%slope, hru(j)%sb%sb_db%hru_rcv, hru(j)%sb%inflo, hru(j)%tiledrain, hru(j)%wet_hc, hru(j)%crop_reg, hru(j)%plcur(ipl)%phuacc, hru(j)%plcur(ipl)%gro, hru(j)%plcur(ipl)%idorm, hru(j)%plcur(ipl)%lai_pot, hru(j)%plcur(ipl)%harv_num, hru(j)%plcur(ipl)%harv_num_yr, hru(j)%plcur(ipl)%bsn_num, hru(j)%plcur(ipl)%idplt, hru(j)%plg(ipl)%lai, hru(j)%plstr(ipl)%sum_n, hru(j)%plstr(ipl)%sum_p, hru(j)%plstr(ipl)%sum_tmp, hru(j)%plstr(ipl)%sum_w, hru(j)%plstr(ipl)%sum_a, hru(j)%pl(ipl), hru(j)%sno` |
| [sym:soil_module] | `soil, soil1` | `soil(j)%sw, soil(ihru)%sw, soil(j)%phys(1)%rock, soil(j)%ly(1)%usle_k, soil(j)%ly(1)%usle_p, soil(j)%ly(1)%usle_ls, soil1(jj)%mn(l)%no3, soil1(jj)%mn(l)%nh4, soil1(jj)%mp(l)%lab, soil1(jj)%tot(l)%m, soil1(jj)%tot(l)%n, soil1(jj)%tot(l)%p, soil1(jj)%hact(l)%n, soil1(jj)%hsta(l)%p, soil1(jj)%hs(l)%n, soil1(jj)%hp(l)%p, soil1(jj)%microb(l)%m, soil1(jj)%str(l)%m, soil1(jj)%lig(l)%m, soil1(jj)%meta(l)%m, soil1(jj)%pl(ipl)%rsd(l)` |
| [sym:plant_module] | `pcom` | `pcom(j)%dtbl(idtbl)%num_actions(iac), pcom(j)%plcur(ipl)%phuacc, pcom(j)%dtbl(idtbl)%days_act(iac), pcom(j)%days_irr, pcom(j)%dtbl(idtbl)%days_act(iac-1), pcom(j)%fert_fut(ifrt)%day_fert, pcom(j)%pcomdb, pcom(j)%days_plant, pcom(j)%npl, pcom(j)%plcur(ipl)%gro, pcom(j)%plcur(ipl)%idorm, pcom(j)%plcur(ipl)%lai_pot, pcom(j)%days_harv, pcom(j)%days_kill, pcom(j)%last_kill, pcom(j)%rot_yr, pcom(j)%plg(ipl)%lai, pcom(j)%plstr(ipl)%sum_n, pcom(j)%plstr(ipl)%sum_p, pcom(j)%plstr(ipl)%sum_tmp, pcom(j)%plstr(ipl)%sum_w, pcom(j)%plstr(ipl)%sum_a, pcom(j)%pl(ipl)` |
| [sym:plant_data_module] | `pcomdb, pldb` | `pcomdb(icom)%pl(ipl)%db_num, pcomdb(icom)%pl(ipl)%cpnm, pldb(idp)%plantnm, pldb(idp)%hvsti, pldb(idp)%wsyf, pldb(idp)%trig` |
| [sym:mgt_operations_module] | `irrop_db, chemapp_db, mgt, sched, harvop_db, grazeop_db, fire_db, pudl_db, sdr, sep, filtstrip_db, grwaterway_db, bmpuser_db` | `irrop_db(irrop)%amt_mm, irrop_db(irrop)%eff, irrop_db(irrop)%surq, chemapp_db(ifertop)%surf_frac, chemapp_db(ipestop)%app_eff, mgt%op_char, sched(isched)%auto_name(idtbl), sched(isched)%auto_crop(1), harvop_db(iharvop)%bm_min, harvop_db(iharvop)%typ, grazeop_db(igr), fire_db(iburn)%cn2_upd, fire_db(iburn)%fr_burn, pudl_db(ipud)%wet_hc, pudl_db(ipud)%sed, sdr(istr)%name, sep(istr)%name, filtstrip_db(istr)%name, grwaterway_db(istr)%name, bmpuser_db(istr)%name` |
| [sym:landuse_data_module] | `No resolved outside references were provided in the context packet` |  |
| [sym:tillage_data_module] | `tilldb` | `tilldb(idtill)%tillnm, tilldb(idtill)%effmix` |
| [sym:reservoir_module] | `wet_ob, res_ob` | `wet_ob(j)%depth, wet_ob(j)%weir_hgt, wet_ob(j)%pvol, wet_ob(j)%evol, res_ob(iob)%irrig_track, res_ob(iob)%d_irrig_day, res_ob(j)%weir_hgt, res_ob(j)%pvol, res_ob(j)%evol` |
| [sym:sd_channel_module] | `sd_ch, ich` | `sd_ch(ich)%cov, sd_ch(ich)%order` |
| [sym:septic_data_module] | `sep, db_mx%septic` | `sep(istr)%name, db_mx%septic` |
| [sym:hru_lte_module] | `hlt` | `hlt(j)%gro, hlt(j)%g, hlt(j)%alai, hlt(j)%dm, hlt(j)%hufh, hlt(j)%iplant, hlt(j)%pet, hlt(j)%aet, hlt(j)%yield, hlt(j)%npp, hlt(j)%lai_mx` |
| [sym:basin_module] | `pco, bsn_cc` | `pco%mgtout, bsn_cc%cswat, cal_codes%plt, basin_plants, plts_bsn, bsn_crop_yld, bsn_crop_yld_aa, bsn_crop_yld_z, cal_codes` |
| [sym:organic_mineral_mass_module] | `pl_mass, pl_yield, pl_burn, hrc_d, hpc_d, bsn_crop_yld` | `pl_mass(j)%tot(ipl)%m, pl_mass(j)%rsd_tot%m, pl_mass(j)%rsd_tot, pl_mass(j)%yield_tot(ipl), pl_mass(j)%yield_yr(ipl), pl_mass(j)%tot_com, pl_mass(j)%ab_gr_com, pl_mass(j)%leaf_com, pl_mass(j)%stem_com, pl_mass(j)%seed_com, pl_mass(j)%root_com, pl_mass(j)%rsd(ipl), pl_mass(j)%ab_gr(ipl), pl_mass(j)%leaf(ipl), pl_mass(j)%stem(ipl), pl_mass(j)%seed(ipl)` |
| [sym:hydrograph_module] | `irrig, ch_stor, res, wet, ch_water, cs_irr, cs_aqu, wet_wat_d, wet_dat, wet_init, wet_hyd, wet_prm, wet_water, wetqcs, wtspcs, trn_m3, ht2` | `irrig(j)%applied, irrig(j)%demand, irrig(j)%runoff, irrig(j)%water%flo, irrig(j)%water, ch_stor(iob)%flo, res(iob)%flo, wet(j)%flo, ch_water(iob), cs_irr(iob), cs_aqu(iob), wet_wat_d(j), wet(j)%sed, wet(j)%no3, wet(j)%nh3, wet(j)%solp, wet(j)%orgn, wet(j)%sedp` |
| [sym:output_landscape_module] | `No resolved outside references were provided in the context packet` |  |
| [sym:constituent_mass_module] | `cs_db` | `cs_db%num_cs` |
| [sym:calibration_data_module] | `No resolved outside references were provided in the context packet` |  |
| [sym:fertilizer_data_module] | `No resolved outside references were provided in the context packet` |  |
| [sym:maximum_data_module] | `db_mx, basin_plants` | `db_mx%wet_dat, db_mx%pudl_db, db_mx%tillparm, db_mx%septic, db_mx%filtop_db, db_mx%grassop_db, db_mx%bmpuserop_db, basin_plants` |
| [sym:tiles_data_module] | `No resolved outside references were provided in the context packet` |  |
| [sym:water_body_module] | `No resolved outside references were provided in the context packet` |  |
| [sym:reservoir_data_module] | `wet_dat, wet_init, wet_hyd, wet_prm, wet_water, wet_wat_d` | `wet_dat(ires)%name, wet_dat(ires)%init, wet_dat(ires)%hyd, wet_dat(ires)%release, wet_dat(ires)%sed, wet_init(isp_ini)%org_min, wet_init(isp_ini)%pest, wet_init(isp_ini)%path` |

## Local Variables

<!-- facts:locals -->

## State Changes

| Target | When | Meaning |
| --- | --- | --- |
| `mallo(imallo)%trn(itrn)%manure_amt` | In the `manure_demand` action. | Resets the manure-allocation amount record to the zero template `manure_amtz` before filling it. |
| `mallo(imallo)%trn(itrn)%manure_amt%mallo_obj` | In the `manure_demand` action. Set only when the per-action count is within the allowed limit (`num_actions(iac) <= const2`). | Sets the manure-allocation object id on the manure-allocation transfer record from the action definition. |
| `mallo(imallo)%trn(itrn)%manure_amt%src_obj` | In the `manure_demand` action. Set only when the per-action count is within the allowed limit (`num_actions(iac) <= const2`). | Sets the manure source object number on the manure-allocation transfer record from the action definition. |
| `mallo(imallo)%trn(itrn)%manure_amt%app_t_ha` | In the `manure_demand` action. Set only when the per-action count is within the allowed limit (`num_actions(iac) <= const2`). | Sets the application rate (t/ha) on the manure-allocation transfer record from the action definition. |
| `mallo(imallo)%trn(itrn)%manure_amt%app_method` | In the `manure_demand` action. Set only when the per-action count is within the allowed limit (`num_actions(iac) <= const2`). | Sets the application method on the manure-allocation transfer record from the action definition. |
| `ipl` | Set at the start of most action cases. | Selects the plant the action operates on; set to 1 (single/first plant) in irrigation, fertilizer, and similar cases. |
| `hru(j)%irr_hmax` | In paddy/ponding irrigation actions (`name == 'ponding'`). | Sets the target ponding depth for paddy irrigation from the action constant. |
| `hru(j)%irr_hmin` | In paddy/ponding irrigation actions (`name == 'ponding'`). | Sets the threshold ponding depth that triggers paddy irrigation. |
| `wet_ob(j)%depth` | In `irr_demand` ponding, after accounting for irrigation already applied today. | Adds today's already-applied irrigation depth to the wetland/paddy ponding depth. |
| `irrig(j)%demand` | In the irrigation-demand and irrigate actions. | Irrigation water demand volume from depth and HRU area (or ponding deficit). |
| `irrig(j)%applied` | In `irrigate` (and `irr_demand` unlimited source); zeroed if the source lacks water. | Irrigation depth actually applied to the soil, net of efficiency and surface loss. |
| `irrig(j)%runoff` | In `irrigate` (and unlimited source); zeroed if the source lacks water. | Portion of irrigation lost to surface runoff. |
| `res_ob(iob)%irrig_track` | In the `res_irr_dmd` action. | Increments the reservoir irrigation-demand tracker. |
| `res_ob(iob)%d_irrig_day` | In the `res_irr_dmd` action. | Records the day's irrigation demand placed on the reservoir. |
| `irrig(j)%water%flo` | In `irrigate` when the source is an aquifer (`ob == "aqu"`). | Sets the flow volume of the irrigation water withdrawn as a fraction of aquifer storage. |
| `aqu_d(iob)%stor` | In `irrigate` aquifer-source case. | Reduces aquifer storage by the withdrawn fraction (remainder stays). |
| `cs_irr(iob)` | In `irrigate` aquifer/channel cases when constituents are simulated (`cs_db%num_cs > 0`). | Sets the constituent mass carried in irrigation water as a fraction of the source constituents. |
| `cs_aqu(iob)` | In `irrigate` aquifer-source case when constituents are simulated. | Reduces aquifer constituent mass by the withdrawn fraction. |
| `irrig(j)%water` | In `irrigate` when the source is a channel (`cha`/`sdc`) or reservoir (`res`). | Sets the irrigation water hydrograph as a fraction of channel or reservoir storage. |
| `ch_stor(iob)` | In `irrigate` channel-source case. | Reduces channel storage by the withdrawn fraction. |
| `ch_water(iob)` | In `irrigate` channel-source case. | Reduces channel constituent mass by the withdrawn fraction. |
| `res(iob)` | In `irrigate` reservoir-source case. | Reduces reservoir storage by the withdrawn fraction. |
| `hru(j)%irr_yr` | In `irrigate`, after the source withdrawal. | Adds the applied irrigation to the annual irrigation total for decision-table conditioning. |
| `pcom(j)%dtbl(idtbl)%num_actions(iac)` | After an application action runs (irrigate, fertilize, manure, tillage, etc.). | Increments the per-action application counter used to cap applications per year. |

## File I/O

<!-- facts:io -->


## Lineage

`actions.f90` was introduced in `df07e3f` (2024-03-05, "init all") and has been changed in 38 non-merge commit(s) since, most recently `dfce092` (2026-06-02, "move carbon activation to cswat = 2, reserve 1 for C-FARM"). Lineage is reconstructed from commit metadata (SHA, date, subject); per-line diffs were unavailable in this build environment, so only the commits touching `actions.f90` are listed.

- `dfce092` (2026-06-02) — move carbon activation to cswat = 2, reserve 1 for C-FARM
- `08ffdd0` (2026-04-29) — Remove redundant condition check for action limits in the actions subroutine
- `f1d1ac1` (2026-04-22) — Hopefulle some finally cleanup to implement cswat == 3 to cswat = 1. Added/changed subroutines in external specificaitons due to subroutine…
- `3389f29` (2026-04-22) — Numerous changes to account for the removal of the old cswat ==1 and moving cswat == 3 to cswat =1. Also some code formatting changes to get…
- `080211e` (2026-03-09) — water allocation operating properly
- `df07e3f` (2024-03-05) — init all

## Review Notes

- algorithm_steps revised: re-split into 14 contiguous, non-overlapping spans covering actions.f90:97-1272, aligned to the top-level `select case (d_tbl%act(iac)%typ)` labels. The previous decomposition interleaved its spans (124-673, 168-848 and 356-1265 each enclosed many unrelated cases while 195-195, 298-298 and 107-107 were single lines), so six steps overlapped earlier ones. render._relabel_core_graph consumes the first step range containing a CFG node, so those enclosing spans absorbed labels belonging to the cases nested inside them.
- File I/O verified against the source: 35 write statements, no reads, opens, closes or rewinds. All 22 writes to unit 2612 are management-output records guarded by `pco%mgtout == "y"`. All 13 writes to unit 3612 are land-use-change records and are unguarded — they occur whenever the corresponding action fires. Neither unit is opened or closed here, so both connections are established elsewhere.
- `chg_par` is a function invoked in an expression at `actions.f90:1232`, not a `call` statement; its `callees` entry cites the assignment line rather than a call site.
- `actions` carries no extracted documentation comment.
- Lineage was reconstructed from file-level commit metadata; per-line diffs were unavailable in this environment (blobless clone), so line-span filtering was not applied.
