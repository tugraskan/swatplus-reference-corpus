---
kind: procedure
symbol: hru_control
title: hru_control
status: filled
source_hash: 443a451e2d91d800
version_label: SWAT+ 62.0.0
locals:
  j: Current HRU index copied from `ihru` and used to index nearly all HRU state.
  j1: Loop counter for soil layers when summing profile water.
  ulu: Urban land-use code for the active HRU, read from `hru(j)%luse%urb_lu`.
  iob: Object-connectivity index for the active HRU, read from `hru(j)%obj_no`.
  ith: Topography/database index for the active HRU, read from `hru(j)%dbs%topo`.
  iwgn: Weather-generator index for the active HRU, read from `wst(iwst)%wco%wgn`.
  ires: Surface-storage/reservoir index for the active HRU, read from `hru(j)%dbs%surf_stor`.
  isched: Management schedule index for the active HRU, read from `hru(j)%mgt_ops`.
  isalt: Loop counter over simulated salt ions when building salt outputs.
  ics: Loop counter over simulated constituents when building constituent outputs.
  iauto: Loop counter over automatic management operations in the schedule.
  id: Decision-table index selected from the management schedule.
  jj: Working HRU index passed into `conditions` and `actions`.
  ly: Soil-layer loop counter used for layer updates and profile sums.
  ipest: Loop counter over simulated pesticides.
  strsa_av: Average air-stress factor across growing plants.
  icn: Curve-number-related working variable used in runoff/output bookkeeping.
  xx: Temporary sum of pollutant load components used to decide whether urban BMPs run.
  iob_out: Output-routing object index, possibly remapped to a route unit.
  iout: Loop counter over outgoing object destinations.
  iac: Loop counter over decision-table actions.
  npl_gro: Count of plants currently growing and not dormant.
  dep: Temporary depth variable used in soil-water depth calculations.
  strsw_av: Average water-stress factor across growing plants.
  strsn_av: Average nitrogen-stress factor across growing plants.
  strsp_av: Average phosphorus-stress factor across growing plants.
  strss_av: Average salt-stress factor across growing plants.
  strstmp_av: Average temperature-stress factor across growing plants.
  wet_outflow: Wetland outflow depth equivalent for the day.
  tile_fr_surf: Fraction of tile flow treated as surface runon.
  ifrt: Index of future fertilizer application.
  idp: Plant database index for the current plant.
  hru_rcv: Receiving HRU index for saturated-buffer routing.
  rto: Area ratio used when transferring saturated-buffer flow to the receiving HRU.
  sw_volume_begin: Soil water stored at the start of the day.
  soil_prof_labp: Total labile phosphorus in the soil profile.
  sum_conc: Temporary sum of salt or constituent concentrations across soil layers.
  sum_mass: Temporary sum of salt or constituent masses across soil layers.
  sum_sorb: Temporary sum of sorbed constituent mass across soil layers.
  saltcon: Daily salt concentration output value written to the paddy/wetland output record.
  qsurf: Temporary copy of surface runoff depth.
  sedppm: Sediment concentration used in the paddy/wetland output record.
uses:
  hru_module: '`hru_module` provides the active HRU identity, land use, management schedule,
    surface-storage linkage, saturated-buffer routing, paddy irrigation settings, and area
    needed to drive the entire daily land-phase sequence.'
  soil_module: '`soil_module` supplies the soil-layer count, layer water storage, and tillage-mixing
    factor that are updated or read throughout the daily HRU sequence.'
  plant_module: '`plant_module` provides plant-community state, future fertilizer scheduling,
    plant stress, and phenology fields used by management, growth, and output calculations.'
  basin_module: '`basin_module` provides basin-wide control flags that switch lapse-rate adjustment,
    carbon-code behavior, crack flow, and phosphorus model selection.'
  organic_mineral_mass_module: '`organic_mineral_mass_module` provides soil-profile mass pools,
    including layer mixing efficiency and labile phosphorus, that are updated and summarized
    in the HRU sequence.'
  carbon_module: 'Imported wholesale at `hru_control.f90:22`, but no symbol owned by this
    module is referenced anywhere in `hru_control.f90:1-890`. Verified by checking all 64
    symbols declared in `carbon_module` against this routine''s executable body: none appear.
    The carbon pools it carries are reached indirectly through `cbn_surfrsd_decomp`, `cbn_rsd_transfer`
    and `cbn_zhang2` at `hru_control.f90:389-394`.'
  hydrograph_module: '`hydrograph_module` provides object connectivity, inflow hydrographs,
    irrigation transfers, and wetland/output hydrograph state used for routing and daily balances.'
  climate_module: '`climate_module` provides weather station linkage, daily weather, heat
    units, and subdaily precipitation used throughout the HRU daily sequence.'
  septic_data_module: '`septic_data_module` provides septic-system activation and start-year
    flags used to decide whether septic biozone processes run.'
  reservoir_data_module: Supplies the wetland hydrology type tested at `hru_control.f90:552`,
    which decides whether the HRU is a paddy and therefore whether the daily paddy diagnostic
    record is written to unit 100100. Ownership confirmed against `reservoir_data_module.f90:14`.
  plant_data_module: Supplies the plant database growth trigger tested at `hru_control.f90:431`;
    when it is `moisture_gro` a monsoon-season tropical plant is released from dormancy. Ownership
    confirmed against `plant_data_module.f90:107`.
  mgt_operations_module: '`mgt_operations_module` supplies the management schedule and decision-table
    mapping used to run automatic operations.'
  reservoir_module: '`reservoir_module` provides wetland depth state used for paddy irrigation
    checks and wetland output.'
  output_landscape_module: '`output_landscape_module` holds daily landscape water and nutrient
    balance arrays that `hru_control` resets and populates.'
  output_ls_pesticide_module: '`output_ls_pesticide_module` provides the daily pesticide-balance
    arrays that are reset and updated by the HRU pesticide sequence.'
  time_module: '`time_module` provides the current day, year-end flag, timestep, and year
    counter used throughout the daily HRU sequence.'
  conditional_module: '`conditional_module` provides decision-table structures used by `conditions`
    and `actions` to evaluate automatic management operations.'
  constituent_mass_module: '`constituent_mass_module` provides counts of simulated pesticides,
    salts, and generic constituents that gate the corresponding daily process loops.'
  water_body_module: Imported wholesale at `hru_control.f90:35`, but none of the 5 symbols
    it declares is referenced in this routine's executable body. The water-body state this
    routine touches (`wet`, `ht1`, `ht2`) resolves to `hydrograph_module` in the packet's
    ownership table.
  salt_module: Holds the daily per-ion salt balance filled at `hru_control.f90:786-803` from
    the salt transport arrays and the profile-average concentration and total mass. Ownership
    confirmed against `salt_module.f90:36`.
  cs_module: Holds the daily per-constituent balance filled at `hru_control.f90:806-836`,
    including dissolved and sorbed profile mass and every transport pathway. Ownership confirmed
    against `cs_module.f90:45`.
  gwflow_module: 'Carries the gwflow coupling state this routine writes: the unmet ET residual
    at `hru_control.f90:505`, percolation handed to the groundwater model at `hru_control.f90:737`,
    and the nitrate leaching concentration stored for gwflow at `hru_control.f90:857-858`.
    The references are visible in the source block; the declaration sites were not included
    in this packet, so the module attribution is inferred from the `use` list.'
  tillage_data_module: Supplies the tillage effect duration compared against `tillage_days`
    at `hru_control.f90:148` and the biological mixing efficiency tested before calling `mgt_biomix`
    at `hru_control.f90:387`. Ownership confirmed against `tillage_data_module.f90:6-7`, where
    `till_eff_days` defaults to 30 days.
---

<!-- facts:header -->

Drives the complete daily land-phase simulation for one HRU: resolves the HRU's weather and database indices, runs scheduled and automatic management, routes incoming and generated water through the soil profile, advances plant, nutrient, pesticide, salt and constituent state, and fills the HRU's daily output balance arrays before hydrographs are assembled.

## Bottom Line

`hru_control` is the main daily HRU driver. It pulls weather, soil, plant, management, wetland, septic, salt, constituent, and routing state together, then runs the sequence of hydrology, management, plant growth, nutrient, pesticide, and output updates for the active HRU.

It matters because it is where most land-surface state is advanced for the day: precipitation is adjusted, runoff and percolation are routed, management and crop operations are applied, and the daily output balance arrays are populated before hydrographs are assembled for downstream routing.

## Arguments

<!-- facts:arguments -->

## Where It Fits

Called from `command` when the current object type is `hru` (`command.f90:293-296`). It runs after the command layer has selected the active HRU and before any downstream hydrograph output is produced.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. Resolve HRU and database indices | Set the local HRU index from `ihru`, accumulate start-of-day soil water into `sw_volume_begin` for the end-of-day storage change, zero the per-layer mixing efficiency `soil1(j)%emix`, and resolve the urban land use, object number, weather station, weather generator, topography, surface-storage and management-schedule indices that the rest of the routine keys off. |
| 2. Load weather and apply lapse rates | Copy the weather station's daily record into `w`. When basin lapse-rate correction is enabled, raise precipitation by the object's precipitation lapse and shift maximum, minimum and average temperature by the temperature lapse, flooring precipitation at zero, then publish the result as `precip_eff`. |
| 3. Zero daily accumulators | Reset the daily soil-carbon, residue, plant-carbon and carbon-flux output structures, clear wetland seepage, irrigation demand, N and P uptake, wetland outflow and denitrification. Under the SWAT-C carbon model (`bsn_cc%cswat == 2`), age the tillage switch: clear the per-layer tillage-mixing factor once `tillage_days` reaches `till_eff_days`, otherwise increment the counter. Zero the per-pesticide balance, call `varinit`, advance the 30-day rolling counter `nd_30`, and zero the deposition and inflow hydrographs `ht1` and `ht2`. |
| 4. Run automatic management tables | For each automatic operation on the HRU's schedule, point `d_tbl` at the land-use decision table and call `conditions` then `actions`. Apply any future fertilizer whose scheduled day matches the current day through `pl_fert` and clear its trigger. At year end reset each action's one-per-year counter, advance the rotation year, and increment the days-since-action counters for every active action. |
| 5. Advance counters and reset stress | Increment days since planting, harvest, kill and irrigation; accumulate base-zero heat units into `phubase(j)` when the average temperature is above zero and the station has a positive total; and reset all six per-plant stress factors (water, temperature, nitrogen, phosphorus, aeration, salinity) to 1.0 for every plant in the community. |
| 6. Compute albedo, chemistry, soil temperature | Call `albedo`, then run salt equilibrium chemistry (`salt_chem_hru`) when salts are simulated and constituent reaction and sorption (`cs_rctn_hru`, `cs_sorb_hru`) when generic constituents are simulated. Compute layer soil temperatures with `stmp_solt`, canopy interception with `sq_canopyint`, and snowmelt with `sq_snom`. |
| 7. Route incoming flows onto the HRU | Assume all tile flow travels overland (`tile_fr_surf = 1`). Incoming surface runon is either added to the wetland store when the HRU has surface storage, or routed across the HRU by `rls_routesurf` so it can infiltrate and deposit sediment. Route incoming lateral soil flow (`rls_routesoil`), tile flow into a saturated buffer (`rls_routetile`) and aquifer inflow (`rls_routeaqu`) when each is present, then compute crack volume with `sq_crackvol` if crack flow is enabled. |
| 8. Partition ET, runoff and wetlands | Compute potential and actual evapotranspiration (`et_pot`, `et_act`) and run scheduled management operations with `mgt_operatn` unless the HRU is in a skipped year. Generate surface runoff with `surface` for upland HRUs; for wetland HRUs force surface runoff, irrigation runoff and sediment yield to zero because all transport happens through the impoundment. Add sediment routed in from upslope to the HRU's sediment yield, trigger manual paddy irrigation through `wet_irrp` when ponding depth falls below the minimum irrigation depth, and run `wetland_control` for impounded HRUs or release the wetland store directly into `ht2%flo` otherwise. Close by computing effective rainfall reaching the soil — wetland seepage for impounded HRUs, precipitation minus surface runoff elsewhere, floored at zero — and spreading applied irrigation across the subdaily precipitation series when running sub-daily. |
| 9. Percolate water, graze, mineralize | Route water through the soil profile with `swr_percmain`, then lag saturation excess into `bss_ex` and release `satexq_chan` to the channel. Graze when a grazing period is active and close the period once `grz_days` is reached. Under the static carbon model run `rsd_decomp` and `nut_nminrl`; under SWAT-C run biological mixing, `cbn_surfrsd_decomp`, `cbn_rsd_transfer` and `cbn_zhang2`. Always volatilize nitrogen with `nut_nitvol`, then mineralize phosphorus with `nut_pminrl2` or `nut_pminrl` depending on `bsn_cc%sol_P_model`. |
| 10. Run septic and plant growth | Run `sep_biozone` for septic HRUs whose biozone layer is above freezing and whose start year has passed. Partition the plant community with `pl_community`, sum profile labile phosphorus, and release monsoon-triggered tropical plants from dormancy when the precipitation-to-PET ratio exceeds 0.5. Grow biomass with `pl_grow`, reset yearly yield and harvest counters at year end, and average the six stress factors across the plants that are actually growing. |
| 11. Summarize soil water and pesticide fate | Compute soil water in the top 300 mm and per-layer volumetric water content, total actual ET from plant, soil and canopy evaporation, and the gwflow residual `etremain`. Then run the pesticide sequence: wash-off when precipitation reaches 2.54 mm (`pest_washp`), plant uptake (`pest_pl_up`), degradation (`pest_decay`), movement in soil (`pest_lch`) and the profile total (`pest_soil_tot`). |
| 12. Move nutrients, salts, pathogens | When runoff and peak flow are both present, compute pesticide enrichment and sediment-bound pesticide, organic nitrogen in runoff via the static or SWAT-C path, and sediment-bound phosphorus. Add nitrate from rainfall (`nut_nrain`) and leach nitrate (`nut_nlch`); for paddy wetlands write the daily diagnostic record to unit 100100. Compute soluble phosphorus (`nut_solp`), then salt deposition, road salt and leaching, constituent deposition and leaching, and pathogen routing, runoff and process steps when each constituent class is simulated. |
| 13. Apply urban, BMP, and buffer reductions | Compute urban loadings with the daily or sub-daily routine, add lateral-flow sediment (`swr_latsed`), and lag surface (`stor_surfstor`) and subsurface (`swr_substor`) loads. Reduce pollutants through the edge-of-field filter strip, buffer, grass waterway and fixed BMP where each is configured. Convert wetland outflow into depth and add it to `qday` and water yield, store the surface-runoff remainder with `sq_surfst`, and split tile flow and tile nitrate to the receiving HRU when this HRU is a saturated-buffer source. Sum water yield, compute in-stream water quality loads (`swr_subwq`) and apply urban BMP removal when concentrations are non-zero. |
| 14. Split outflow and fill daily outputs | Resolve the outflow object, redirecting through the routing unit when the HRU belongs to one, and split surface and lateral flow across channel, reservoir and landscape destinations by each connection's output fraction. Populate the daily water balance, nutrient balance, salt balance, constituent balance, plant/weather and losses output structures, clearing the applied-irrigation, overbank and saturation-excess accumulators as they are consumed. Finally call `hru_hyds` to build the hydrographs for direct routing or the landscape unit. |

## Modules Used

<!-- facts:uses -->

| Module | State touched | Key components |
| --- | --- | --- |
| [sym:hru_module] | `hru` | `hru(j)%luse%urb_lu, hru(j)%obj_no, hru(j)%dbs%topo, hru(j)%dbs%surf_stor, hru(j)%mgt_ops, hru(j)%water_seep, hru(j)%sb%sb_db%hru_rcv, hru(j)%paddy_irr, hru(j)%irr_hmin, hru(j)%area_ha` |
| [sym:soil_module] | `soil` | `soil(j)%nly, soil(j)%phys(j1)%st, soil(j)%ly(ly)%tillagef_tillmix` |
| [sym:plant_module] | `pcom` | `pcom(ihru)%fert_fut_num, pcom(ihru)%fert_fut(ifrt)%day_fert, pcom(ihru)%fert_fut(ifrt)%fertnum, pcom(ihru)%fert_fut(ifrt)%fert_kg, pcom(ihru)%fert_fut(ifrt)%appnum, pcom(j)%dtbl(iauto)%num_actions(iac), pcom(j)%rot_yr, pcom(j)%dtbl(iauto)%days_act(iac), pcom(j)%days_plant, pcom(j)%days_harv, pcom(j)%days_kill, pcom(j)%days_irr, pcom(j)%npl, pcom(j)%plstr(ipl)%strsw, pcom(j)%plstr(ipl)%strst, pcom(j)%plstr(ipl)%strsn, pcom(j)%plstr(ipl)%strsp, pcom(j)%plstr(ipl)%strsa, pcom(j)%plstr(ipl)%strss, pcom(j)%plcur(ipl)%mseas` |
| [sym:basin_module] | `bsn_cc` | `bsn_cc%lapse, bsn_cc%cswat, bsn_cc%crk, bsn_cc%sol_P_model` |
| [sym:organic_mineral_mass_module] | `soil1` | `soil1(j)%emix(ly), soil1(j)%mp(ly)%lab` |
| [sym:carbon_module] | `no direct reference in this procedure` |  |
| [sym:hydrograph_module] | `ob, irrig, ht2, wet` | `ob(iob)%wst, ob(iob)%plaps, ob(iob)%tlaps, irrig(j)%demand, ob(icmd)%hin_sur%flo, ob(icmd)%hin_sur, ob(icmd)%hin_til, ob(icmd)%hin_lat%flo, ob(icmd)%hin_aqu%flo, irrig(j)%runoff, ht2%sed, ht2%flo, wet(j)%flo, irrig(j)%applied` |
| [sym:climate_module] | `wst, w, wgn_pms` | `wst(iwst)%wco%wgn, wst(iwst)%weat, w%precip, w%tmax, w%tmin, w%tave, wgn_pms(iwgn)%phutot, w%ts(:)` |
| [sym:septic_data_module] | `sep` | `sep(isep)%opt, sep(isep)%yr` |
| [sym:reservoir_data_module] | `wet_dat_c` | `wet_dat_c(ires)%hyd` |
| [sym:plant_data_module] | `pldb` | `pldb(idp)%trig` |
| [sym:mgt_operations_module] | `sched` | `sched(isched)%num_autos, sched(isched)%num_db(iauto)` |
| [sym:reservoir_module] | `wet_ob` | `wet_ob(j)%depth` |
| [sym:output_landscape_module] | `hnb_d, hwb_d` | `hnb_d(j)%nuptake, hnb_d(j)%puptake, hwb_d(j)%wet_out, hnb_d(j)%denit` |
| [sym:output_ls_pesticide_module] | `hpestb_d` | `hpestb_d(j)%pest(ipest)` |
| [sym:time_module] | `time` | `time%day, time%end_yr, time%step, time%yrc` |
| [sym:conditional_module] | `d_tbl, dtbl_lum` | `d_tbl%acts, dtbl_lum(id)%acts` |
| [sym:constituent_mass_module] | `cs_db` | `cs_db%num_pests, cs_db%num_salts, cs_db%num_cs` |
| [sym:water_body_module] | `no direct reference resolved` |  |
| [sym:salt_module] | `hsaltb_d` | `hsaltb_d(j)%salt(isalt)%surq, hsaltb_d(j)%salt(isalt)%latq, hsaltb_d(j)%salt(isalt)%urbq, hsaltb_d(j)%salt(isalt)%wetq, hsaltb_d(j)%salt(isalt)%wtsp, hsaltb_d(j)%salt(isalt)%tile, hsaltb_d(j)%salt(isalt)%perc, hsaltb_d(j)%salt(isalt)%gwup, hsaltb_d(j)%salt(isalt)%conc, hsaltb_d(j)%salt(isalt)%soil` |
| [sym:cs_module] | `hcsb_d` | `hcsb_d(j)%cs(ics)%conc, hcsb_d(j)%cs(ics)%soil, hcsb_d(j)%cs(ics)%srbd, hcsb_d(j)%cs(ics)%surq, hcsb_d(j)%cs(ics)%sedm, hcsb_d(j)%cs(ics)%latq, hcsb_d(j)%cs(ics)%urbq, hcsb_d(j)%cs(ics)%wetq, hcsb_d(j)%cs(ics)%wtsp, hcsb_d(j)%cs(ics)%tile, hcsb_d(j)%cs(ics)%perc, hcsb_d(j)%cs(ics)%gwup` |
| [sym:gwflow_module] | `etremain, gwflow_perc, gwflow_percsol, gw_solute_flag` | `etremain(j), gwflow_perc(j), gwflow_percsol(j,1), gw_solute_flag` |
| [sym:tillage_data_module] | `till_eff_days, bmix_eff` | `till_eff_days, bmix_eff` |

## Local Variables

<!-- facts:locals -->

## State Changes

| Target | When | Meaning |
| --- | --- | --- |
| `soil1(j)%emix(ly)` | During the daily per-HRU reset/setup block at the top of the routine. | Per-layer tillage mixing efficiency, zeroed each day. Reset at the start of the day. |
| `iwst` | During the daily per-HRU reset/setup block at the top of the routine. | Weather-station index for the HRU's object. Reset at the start of the day. |
| `iwgen` | During the daily per-HRU reset/setup block at the top of the routine. | Weather-generator index for the HRU. Reset at the start of the day. |
| `w` | During the daily per-HRU reset/setup block at the top of the routine. | Local copy of the day's weather for the HRU. Reset at the start of the day. |
| `w%precip` | When `bsn_cc%lapse == 1`. | Elevation-adjusted daily precipitation. Set under the noted condition. |
| `w%tmax` | When `bsn_cc%lapse == 1`. | Elevation-adjusted daily maximum temperature. Set under the noted condition. |
| `w%tmin` | When `bsn_cc%lapse == 1`. | Elevation-adjusted daily minimum temperature. Set under the noted condition. |
| `w%tave` | When `bsn_cc%lapse == 1`. | Elevation-adjusted daily average temperature. Set under the noted condition. |
| `precip_eff` | During the daily per-HRU reset/setup block at the top of the routine. | Effective precipitation reaching the soil surface. Reset at the start of the day. |
| `hsc_d(j)` | During the daily per-HRU reset/setup block at the top of the routine. | Daily soil-carbon output accumulator, reset. Reset at the start of the day. |
| `hrc_d(j)` | During the daily per-HRU reset/setup block at the top of the routine. | Daily residue-carbon output accumulator, reset. Reset at the start of the day. |
| `hpc_d(j)` | During the daily per-HRU reset/setup block at the top of the routine. | Daily plant-carbon output accumulator, reset. Reset at the start of the day. |
| `hscf_d(j)` | During the daily per-HRU reset/setup block at the top of the routine. | Daily soil-carbon-flux output accumulator, reset. Reset at the start of the day. |
| `hru(j)%water_seep` | During the daily per-HRU reset/setup block at the top of the routine. | Water seeping into the soil profile, reset daily. Reset at the start of the day. |
| `irrig(j)%demand` | During the daily per-HRU reset/setup block at the top of the routine. | Irrigation demand for the HRU, reset daily. Reset at the start of the day. |
| `hnb_d(j)%nuptake` | During the daily per-HRU reset/setup block at the top of the routine. | Daily plant nitrogen uptake accumulator, reset. Reset at the start of the day. |
| `hnb_d(j)%puptake` | During the daily per-HRU reset/setup block at the top of the routine. | Daily plant phosphorus uptake accumulator, reset. Reset at the start of the day. |
| `hwb_d(j)%wet_out` | During the daily per-HRU reset/setup block at the top of the routine. | Daily wetland outflow in the HRU water balance. Reset at the start of the day. |
| `hnb_d(j)%denit` | During the daily per-HRU reset/setup block at the top of the routine. | Daily denitrification accumulator, reset. Reset at the start of the day. |
| `tillage_switch(ihru)` | When CENTURY carbon is on and the tillage effect window has elapsed. | Flag that tillage disturbance is active on the HRU. Set under the noted condition. |
| `tillage_days(ihru)` | When CENTURY carbon is on and tillage is active. | Days since the last tillage on the HRU. Set under the noted condition. |
| `soil(j)%ly(ly)%tillagef_tillmix` | When the tillage effect window has elapsed. | Per-layer tillage-mixing factor, cleared when the effect ends. Set under the noted condition. |
| `hpestb_d(j)%pest(ipest)` | When pesticides are simulated (`cs_db%num_pests > 0`). | Daily pesticide-balance accumulators, zeroed (except soil/plant pools). Set under the noted condition. |
| `nd_30` | During the daily per-HRU reset/setup block at the top of the routine. | Rolling 30-day counter. Reset at the start of the day. |

## File I/O

<!-- facts:io -->


## Lineage

`hru_control.f90` was introduced in `df07e3f` (2024-03-05, "init all") and has been changed in 45 non-merge commit(s) since, most recently `dfce092` (2026-06-02, "move carbon activation to cswat = 2, reserve 1 for C-FARM"). Lineage is reconstructed from commit metadata (SHA, date, subject); per-line diffs were unavailable in this build environment, so only the commits touching `hru_control.f90` are listed.

- `dfce092` (2026-06-02) — move carbon activation to cswat = 2, reserve 1 for C-FARM
- `1b2a997` (2026-04-27) — Made changes to implement a linear increase in biomixing after a tillage event.
- `ea6ae76` (2026-04-25) — Further fixed the build up the n and p carbon pool.
- `4bb77aa` (2026-04-24) — updated after merge with main.
- `d98c126` (2026-04-22) — Removed cbn_surfrsd_decomp_3 and copied contents to cbn_surfrst_decomp and changed hru_control to call cbn_surfrsd_decomp if cswat == 1
- `df07e3f` (2024-03-05) — init all

## Review Notes

- algorithm_steps revised: re-split into 14 contiguous, non-overlapping spans covering hru_control.f90:99-885. The previous decomposition nested steps inside one another (99-144 contained 124-133 and overlapped 135-171; 296-312 overlapped 303-348), which makes the renderer's range lookup assign a CFG node the enclosing step's label and drop the inner steps' labels. Two grab-bag steps were also split so that the saturated-buffer source logic (634-649) and the outflow-object fraction split (665-726) are visible as described behavior instead of being folded into a single 588-885 step.
- Context packet coverage is partial: the `Candidate Outside References` list stopped at 80 entries spanning roughly hru_control.f90:99-431, so every symbol first used after line 431 was absent from the resolved-ownership table. Those references were recovered from the packet's own source block. Module ownership has since been confirmed directly against the module context packets for `pldb` (plant_data_module.f90:107), `wet_dat_c` (reservoir_data_module.f90:14), `till_eff_days` and `bmix_eff` (tillage_data_module.f90:6-7), `hsaltb_d` (salt_module.f90:36) and `hcsb_d` (cs_module.f90:45). The gwflow symbols (`etremain`, `gwflow_perc`, `gwflow_percsol`, `gw_solute_flag`) remain attributed from the `use` list only, because no gwflow_module packet is available to check against.
- `cs_soil` is read at `hru_control.f90:798-799` for salt mass and concentration and at `hru_control.f90:811-813` for constituent mass, concentration and sorbed mass. It is declared by neither `salt_module` nor `cs_module` — both were checked directly — so it most likely belongs to `constituent_mass_module`, whose packet is not available. It is deliberately left unattributed in `outside_state` rather than assigned on a guess.
- `core_graph` is the parser's control-flow graph and only reaches hru_control.f90:264; the rendered Core Algorithm diagram therefore covers roughly the first third of the routine. The step ranges above span the whole procedure, so regenerating the CFG would extend the diagram without further overlay edits.
- Direct file I/O is limited to one write to unit 100100 at `hru_control.f90:554-556`. The unit is never opened, closed or rewound here, so the connection is established elsewhere; the record is only written for paddy wetlands whose depth exceeds -0.1 m.
- `hru_control` carries no extracted documentation comment beyond the PURPOSE header at `hru_control.f90:3-5`.
- `es_day = es_day` at `hru_control.f90:501` is a self-assignment and has no effect.
- Lineage was reconstructed from file-level commit metadata; per-line diffs were unavailable in this environment (blobless clone), so line-span filtering was not applied.
