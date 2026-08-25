---
kind: procedure
symbol: cal_allo_init
title: cal_allo_init
status: filled
source_hash: 0c342ab8f067336b
version_label: SWAT+ 62.0.0
locals:
  nplt: Holds the number of plants in the current HRU's plant community, taken from `pcomdb(icom)%plants_com`,
    and used to size the per-plant allocation arrays.
  icom: Holds the plant community index for the current HRU, read from `hru(iihru)%plant_cov`,
    so the routine can look up how many plants belong to that community.
  iauto: Loop index over the auto-operation entries in the current management schedule; it
    is used to allocate and initialize each `dtbl` entry.
  isched: Holds the management schedule index for the current HRU, read from `hru(iihru)%mgt_ops`,
    so the routine can access that schedule's auto-operation counts and database links.
  id: Temporary lookup index into `dtbl_lum`, taken from `sched(isched)%num_db(iauto)`, used
    to size each auto-operation's action/day arrays.
  nly1: Stores the soil layer count plus one for the current HRU, used to allocate `soil_init(iihru)%ly`
    and `soil_init(iihru)%phys`.
  iihru: Loop index over HRUs; each pass allocates and initializes the baseline state for
    one HRU-linked object set.
uses:
  sd_channel_module: '`sd_channel_module` provides the channel dynamic arrays that hold SWAT-deg
    channel state. `cal_allo_init` copies `sd_ch` into `sdch_init` when channel-deg objects
    exist so calibration can start from the current channel conditions.'
  hru_lte_module: '`hru_lte_module` provides the HRU-LTE dynamic state. `cal_allo_init` copies
    `hlt` into `hlt_init` when HRU-LTE objects exist so calibration has a preserved starting
    state for those landscape elements.'
  organic_mineral_mass_module: '`organic_mineral_mass_module` contains the plant and soil
    organic-mass structures that this routine allocates and copies. `pl_mass_init` and `soil1_init`
    must exist as baseline mass states so calibration routines can work with plant biomass
    and soil organic pools without altering the live model state.'
  hru_module: '`hru_module` provides the active HRU definitions and the `hru_init` and `bss`
    state that are copied or reset here. The HRU''s `plant_cov` and `mgt_ops` fields determine
    how much calibration storage to allocate, and `bss` is cleared because calibration starts
    from a fresh balance state.'
  soil_module: '`soil_module` provides the active soil profile and soil initialization structures.
    `cal_allo_init` uses the current HRU soil layer count to size `soil_init`, then copies
    `soil` into `soil_init` so calibration can reference a preserved soil profile baseline.'
  plant_module: '`plant_module` holds the active plant community definitions and the corresponding
    initialization copies. `cal_allo_init` allocates `pcom_init` members, initializes auto-operation
    counters inside `dtbl`, and later copies `pcom` into `pcom_init` so calibration can work
    with baseline plant community state.'
  plant_data_module: '`plant_data_module` supplies `pcomdb`, which tells the routine how many
    plants belong to each plant community. That count drives the allocation size for `pcom_init`
    plant arrays and `pl_mass_init` plant mass arrays.'
  hydrograph_module: '`hydrograph_module` holds the live hydrologic storage/output arrays
    and the `sp_ob` object counts that gate allocation. `cal_allo_init` uses those counts
    to decide which HRU, channel, reservoir, wetland, and aquifer initialization arrays to
    allocate and copy.'
  calibration_data_module: '`calibration_data_module` is imported for calibration-related
    state that governs whether this initialization path is needed and how calibration setup
    proceeds, even though no specific symbol from it was extracted in the packet.'
  reservoir_data_module: '`reservoir_data_module` is imported because reservoir calibration
    and initialization depend on reservoir-related data structures elsewhere in the calibration
    workflow, even though no specific symbol from it was extracted here.'
  aquifer_module: '`aquifer_module` provides the aquifer dynamic arrays that are copied into
    `aqu_d` from `aqu_om_init` when aquifer objects exist. This preserves the aquifer starting
    state for calibration.'
  mgt_operations_module: '`mgt_operations_module` provides the management schedule array used
    to size and index each HRU''s auto-operation table. `sched(isched)%num_autos` determines
    how many auto-operation entries to allocate, and `sched(isched)%num_db(iauto)` identifies
    the database record that sets each entry''s action list size.'
  conditional_module: '`conditional_module` is imported as part of the calibration initialization
    environment because conditional management logic can depend on the initialized baseline
    state, even though no direct symbol from it was extracted in this routine.'
---

<!-- facts:header -->

Initializes calibration-time allocation and copies baseline HRU, soil, plant, channel, reservoir, and aquifer state into *_init arrays. It also sizes per-HRU plant community and auto-management arrays so later calibration routines can edit them safely.

## Bottom Line

`cal_allo_init` is a setup routine that allocates and initializes the calibration working copies used by SWAT+ when soft or hard calibration is enabled. It sizes the HRU-linked plant, soil, and management structures from the current model state, then copies the active dynamic objects into their corresponding `_init` arrays so calibration can operate on a preserved baseline.

It matters because later calibration code expects these initialization copies to exist for HRUs, HRU_LTE objects, channels, reservoirs, and aquifers. The routine also resets some state, such as `bss`, and prepares auto-operation counters for each plant community's date table entries.

## Arguments

<!-- facts:arguments -->

## Where It Fits

`cal_allo_init` runs inside `proc_cal` after the calibration input and object-element readers have populated the HRU, channel, reservoir, recall, and aquifer structures. When calibration is enabled (`cal_soft` or `cal_hard`), it prepares the `_init` copies and related allocation sizes that later calibration adjustments rely on before any parameter editing or simulation replay begins.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. Import the model state needed for calibration setup and initialize local indices to zero. | Brings in the dynamic HRU, plant, soil, hydrologic, aquifer, channel, and management modules, then declares loop and lookup variables with safe starting values so the routine can size calibration arrays deterministically. |
| 2. Allocate top-level initialization arrays for HRUs, soils, plant mass, and plant communities. | Creates the baseline containers that will hold copied HRU-linked state for every HRU index from 0 through `sp_ob%hru`. |
| 3. For each HRU, determine its plant community size and allocate plant and biomass arrays. | Uses `hru(iihru)%plant_cov` and `pcomdb(icom)%plants_com` to size the plant growth, mass, stress, and status arrays for that HRU, then allocates all plant biomass components that calibration may need to preserve. |
| 4. For each HRU, allocate and initialize the auto-operation table from the HRU's management schedule. | Reads the schedule index from `hru(iihru)%mgt_ops`, allocates the `dtbl` entries based on `sched(isched)%num_autos`, then sizes each entry's `num_actions` and `days_act` arrays using the linked database record and initializes them to 1 and 0 respectively. |
| 5. For each HRU, allocate soil initialization substructures using the live soil layer count. | Computes `nly1 = soil(iihru)%nly + 1` and allocates `soil_init(iihru)%ly` and `soil_init(iihru)%phys` so the soil baseline copy has room for the full profile plus the surface layer bookkeeping used by SWAT+. |
| 6. Allocate initialization arrays for HRU-LTE and SWAT-deg channel objects. | Creates `hlt_init` and `sdch_init` with the full object counts from `sp_ob%hru_lte` and `sp_ob%chandeg`, making space for those landscape and channel baselines. |
| 7. Copy the current HRU-linked baseline state when HRUs are present and reset balance storage. | Copies live HRU, soil, soil1, plant community, and plant mass state into their `_init` counterparts, copies wetland hydrologic output state from `wet_om_init` into `wet`, and clears `bss` to zero to start calibration from a clean balance state. |
| 8. Copy the current LTE, channel, reservoir, and aquifer baseline state when those object types are present. | Copies `hlt` into `hlt_init` for HRU-LTE objects, `sd_ch` into `sdch_init` plus water-storage initializations into `ch_stor` and `fp_stor` for SWAT-deg channels, `res_om_init` into `res` for reservoirs, and `aqu_om_init` into `aqu_d` for aquifers. |
| 9. Return to the caller after all calibration initialization copies are ready. | Ends the subroutine once all initialization arrays have been allocated and populated. |

## Modules Used

<!-- facts:uses -->

| Module | State touched | Key components |
| --- | --- | --- |
| [sym:sd_channel_module] | `sdch_init, sd_ch` |  |
| [sym:hru_lte_module] | `hlt_init, hlt` |  |
| [sym:organic_mineral_mass_module] | `pl_mass_init, soil1_init, soil1, pl_mass` | `pl_mass_init(iihru)%tot(nplt), pl_mass_init(iihru)%ab_gr(nplt), pl_mass_init(iihru)%leaf(nplt), pl_mass_init(iihru)%stem(nplt), pl_mass_init(iihru)%seed(nplt), pl_mass_init(iihru)%root(nplt), pl_mass_init(iihru)%yield_tot(nplt), pl_mass_init(iihru)%yield_yr(nplt)` |
| [sym:hru_module] | `hru, hru_init, bss` | `hru(iihru)%plant_cov, hru(iihru)%mgt_ops` |
| [sym:soil_module] | `soil, soil_init` | `soil(iihru)%nly, soil_init(iihru)%ly(nly1), soil_init(iihru)%phys(nly1)` |
| [sym:plant_module] | `pcom_init, pcom` | `pcom_init(iihru)%plg(nplt), pcom_init(iihru)%plm(nplt), pcom_init(iihru)%plstr(nplt), pcom_init(iihru)%plcur(nplt), pcom_init(iihru)%dtbl(iauto)%num_actions, pcom_init(iihru)%dtbl(iauto)%days_act` |
| [sym:plant_data_module] | `pcomdb` | `pcomdb(icom)%plants_com` |
| [sym:hydrograph_module] | `sp_ob, wet, wet_om_init, ch_stor, ch_om_water_init, fp_stor, fp_om_water_init, res, res_om_init` | `sp_ob%hru, sp_ob%hru_lte, sp_ob%chandeg, sp_ob%res, sp_ob%aqu` |
| [sym:calibration_data_module] | `calibration_data_module state` | `No candidate outside references were resolved to this module in the context packet.` |
| [sym:reservoir_data_module] | `reservoir_data_module state` | `No candidate outside references were resolved to this module in the context packet.` |
| [sym:aquifer_module] | `aqu_d, aqu_om_init` |  |
| [sym:mgt_operations_module] | `sched` | `sched(isched)%num_autos, sched(isched)%num_db(iauto)` |
| [sym:conditional_module] | `conditional_module state` | `No candidate outside references were resolved to this module in the context packet.` |

## Local Variables

<!-- facts:locals -->

## State Changes

| Target | When | Meaning |
| --- | --- | --- |
| `pcom_init(iihru)%dtbl(iauto)%num_actions` | During the HRU loop when `sched(isched)%num_autos > 0`; each `dtbl(iauto)` entry is allocated and then set. | `pcom_init(iihru)%dtbl(iauto)%num_actions` is initialized to 1 for each auto-operation, establishing one active action counter per database entry before calibration adjustments or yearly resets. |
| `pcom_init(iihru)%dtbl(iauto)%days_act` | During the HRU loop when `sched(isched)%num_autos > 0`; each `dtbl(iauto)` entry is allocated and then set. | `pcom_init(iihru)%dtbl(iauto)%days_act` is initialized to 0 for each auto-operation so the day-since-action counters start clean in the calibration baseline. |
| `hru_init` | When `sp_ob%hru > 0`. | `hru_init` is allocated and then assigned from `hru`, preserving the current HRU state as the calibration starting copy. |
| `soil_init` | When `sp_ob%hru > 0`, after `soil_init(iihru)%ly` and `soil_init(iihru)%phys` have been allocated. | `soil_init` is assigned from `soil`, preserving the current soil-profile state as the calibration starting copy. |
| `soil1_init` | When `sp_ob%hru > 0`, after `soil1_init` has been allocated elsewhere and is ready for copying. | `soil1_init` is assigned from `soil1`, preserving the soil organic-mass profile as the calibration starting copy. |
| `pcom_init` | When `sp_ob%hru > 0`. | `pcom_init` is assigned from `pcom`, preserving the active plant community state so calibration can reference the original growth and management structures. |
| `pl_mass_init` | When `sp_ob%hru > 0` and the per-HRU plant arrays have been allocated. | `pl_mass_init` is assigned from `pl_mass`, preserving plant biomass and yield components as the calibration starting copy. |
| `wet` | When `sp_ob%hru > 0`. | `wet` is overwritten by `wet_om_init` to reset wetland hydrologic outputs/storage to their initialization state for calibration. |
| `bss` | When `sp_ob%hru > 0`. | `bss` is reset to 0.0, clearing the balance-storage state before calibration runs. |
| `hlt_init` | When `sp_ob%hru_lte > 0`. | `hlt_init` is assigned from `hlt`, preserving the current HRU-LTE dynamic state as the calibration baseline. |
| `sdch_init` | When `sp_ob%chandeg > 0`. | `sdch_init` is assigned from `sd_ch`, preserving the current SWAT-deg channel dynamic state as the calibration baseline. |
| `ch_stor` | When `sp_ob%chandeg > 0`. | `ch_stor` is assigned from `ch_om_water_init`, restoring channel storage to its organic-matter/water initialization state for calibration. |
| `fp_stor` | When `sp_ob%chandeg > 0`. | `fp_stor` is assigned from `fp_om_water_init`, restoring floodplain storage to its initialization state for calibration. |
| `res` | When `sp_ob%res > 0`. | `res` is assigned from `res_om_init`, resetting reservoir hydrologic outputs/storage to the initialization state. |
| `aqu_d` | When `sp_ob%aqu > 0`. | `aqu_d` is assigned from `aqu_om_init`, resetting aquifer dynamic state to the initialization baseline for calibration. |

## File I/O

<!-- facts:io -->


## Lineage

Four source-backed commits were resolved for `cal_allo_init`. The initial addition (`df07e3f`) created the subroutine and its allocation/copy structure. `c7c8e22` brought the file in from Bitbucket but did not change the routine's behavior in the shown diff. `39fabde` changed local index declarations to initialize them to zero and added `source = 0` to the `num_actions` and `days_act` allocations before the explicit assignments. `eb22103` removed the obsolete `rsd1_init` allocations and copy, leaving the current residue setup to the newer `soil1` structure.

- df07e3f introduced the calibration initialization routine with allocations for HRU, soil, plant, management, channel, reservoir, and aquifer baseline state copies.
- 39fabde made the local loop/index variables explicitly zero-initialized and changed the auto-operation arrays to allocate with `source = 0` before setting `num_actions = 1` and `days_act = 0`.
- eb22103 removed `rsd1_init` allocation and copying from the routine, reflecting the move to the newer soil1-based residue organization.

## Review Notes

- No direct file I/O was extracted for this procedure.
- warning: missing_doc: Procedure 'cal_allo_init' has no extracted documentation comment.
