---
kind: procedure
symbol: pesticide_init
title: pesticide_init
status: filled
source_hash: a74f6471603ebf51
version_label: SWAT+ 62.0.0
locals:
  ihru: Loop index over HRUs; it selects the current HRU whose pesticide arrays and initial
    pesticide masses are being set.
  npmx: Number of pesticides simulated in the current run, taken from `cs_db%num_pests` and
    used to skip all pesticide allocation and initialization when zero.
  ly: Loop index over soil layers within an HRU, used both for allocating layer pesticide
    storage and for filling each layer's initial pesticide mass.
  ipest: Loop index over pesticide species within the pesticide database for the current HRU.
  nly: Number of soil layers in the current HRU's soil profile, copied from `soil(ihru)%nly`
    to drive allocation and layer initialization.
  npl: Number of plants in the current HRU's plant community, copied from `pcom(ihru)%npl`
    to drive plant allocation and plant-wise pesticide distribution.
  ipest_db: Index of the pesticide soil initialization database record selected by the HRU's
    soil-plant initialization entry.
  isp_ini: Index of the HRU's soil-plant initialization record, taken from `hru(ihru)%dbs%soil_plant_init`
    and used to find which pesticide initialization database entry to use.
  ipl: Loop index over plants in the current HRU, used to apportion pesticide-on-plant mass
    by plant LAI and to step through plant constituent arrays.
  wt1: Conversion factor from initial soil concentration to areal pesticide mass, computed
    as bulk density times layer thickness divided by 100.
  solpst: The initial soil pesticide concentration for the current pesticide species, read
    from `pest_soil_ini(ipest_db)%soil(ipest)` before converting it to layer masses.
  pl_frac: Fraction of the HRU's total LAI represented by the current plant; it is used to
    split initial pesticide-on-plant mass across plants and is capped at 1.
uses:
  hru_module: This module provides the HRU list and the soil-plant initialization lookup used
    to decide which pesticide database record applies to each HRU. `hru(ihru)%dbs%soil_plant_init`
    selects the initialization record, and `sol_plt_ini(isp_ini)%pest` points to the pesticide-init
    entry that supplies the starting plant and soil concentrations.
  soil_module: The soil profile defines how many layers each HRU has and supplies the layer
    bulk density and thickness needed to convert the initial soil pesticide concentration
    into kg/ha for each layer.
  organic_mineral_mass_module: These are the pesticide mass containers that this routine allocates
    and initializes for each HRU. They hold the starting soil, plant, and irrigation pesticide
    masses that later pesticide accounting and transport routines update.
  constituent_mass_module: This module provides the pesticide-count limit and the initial
    soil/plant concentration database that drives the whole routine. `cs_db%num_pests` controls
    whether initialization runs, and `pest_soil_ini(ipest_db)%plt` / `%soil` supply the starting
    amounts copied into plant and soil state.
  output_ls_pesticide_module: This module stores the pesticide balance outputs. `hpestb_d(ihru)%pest(ipest)%plant`
    is seeded here so the model can report the initial plant pesticide load and maintain the
    plant-side balance from the start of the simulation.
  hydrograph_module: The spatial object count sets the HRU loop bound. `sp_ob%hru` tells the
    routine how many HRUs need pesticide state allocated and initialized.
  plant_module: The plant community state supplies the number of plants and each plant's LAI,
    which this routine uses to divide the initial pesticide-on-plant amount among plants in
    proportion to canopy size.
  pesticide_data_module: This initialization database provides the starting pesticide concentrations
    for each pesticide species, separately for plant and soil pools.
---

<!-- facts:header -->

Initializes pesticide state for each HRU from the pesticide and soil-plant initialization databases.

## Bottom Line

`pesticide_init` runs once during HRU setup, but only for simulations that actually include pesticides (`cs_db%num_pests > 0`). It sizes the HRU-level pesticide arrays, then seeds soil and plant pesticide masses from the initial pesticide concentrations tied to each HRU's soil-plant initialization record.

For each HRU it maps the HRU's soil-plant-init database entry to a pesticide-init database record, copies the initial pesticide-on-plant amount into the plant balance output state, distributes that plant amount across existing plants in proportion to LAI, and converts initial soil concentrations into kg/ha for each soil layer using layer bulk density and thickness. Those starting values are what later pesticide transport and balance routines build on.

## Arguments

<!-- facts:arguments -->

## Where It Fits

`pesticide_init` runs during HRU initialization in `proc_hru`, after `soils_init`, `structure_init`, `plant_all_init`, `cn2_init_all`, and `hydro_init` have already prepared the HRU, soil, and plant state. It depends on those upstream setups to know each HRU's soil layers, plant community, and soil-plant initialization record, and its results feed later pesticide balance and transport behavior because the HRU pesticide arrays and starting masses are the baseline for subsequent simulation steps.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. Set up module access and local counters. | The routine imports the HRU, soil, constituent-mass, output, hydrograph, plant, and pesticide-data state it needs, then declares loop counters and working scalars for HRU traversal, pesticide indexing, layer conversion, and LAI-based fractioning. |
| 2. Loop over every HRU in the model. | For each spatial HRU object, the routine reads the run-wide pesticide count from `cs_db%num_pests` and skips the rest of the work when no pesticides are being simulated. |
| 3. Size the pesticide storage for the HRU when pesticides are active. | It copies the HRU's soil-layer count and plant count, allocates the per-layer soil pesticide arrays, the plant input/on-plant/uptake arrays, and the irrigation pesticide array, then zero-initializes each pesticide pool. |
| 4. Select the pesticide initialization record for the HRU. | The routine looks up the HRU's soil-plant-initialization index and then resolves the corresponding pesticide initialization database entry that supplies the starting concentrations. |
| 5. Seed plant pesticide output and distribute plant pesticide load across plants. | For each pesticide species, it copies the initial plant pesticide amount into the HRU pesticide balance output, then distributes that amount across the HRU's plants in proportion to each plant's LAI relative to the community LAI sum, with a zero fallback and an upper cap of 1 on the fraction. |
| 6. Convert initial soil concentrations to layer pesticide masses. | The routine reads the initial soil concentration for the pesticide species, then multiplies it by each soil layer's bulk density and thickness-based conversion factor to store an areal pesticide mass for every layer. |
| 7. Finish the HRU loop and return to the caller. | After all pesticide species are initialized for the HRU, the routine advances to the next HRU and exits when the HRU loop completes. |

## Modules Used

<!-- facts:uses -->

| Module | State touched | Key components |
| --- | --- | --- |
| [sym:hru_module] | `hru, sol_plt_ini` | `hru(ihru)%dbs%soil_plant_init, sol_plt_ini(isp_ini)%pest` |
| [sym:soil_module] | `soil` | `soil(ihru)%nly, soil(ihru)%phys(ly)%bd, soil(ihru)%phys(ly)%thick` |
| [sym:organic_mineral_mass_module] | `cs_db, cs_irr, cs_pl, cs_soil` | `cs_db%num_pests, cs_soil(ihru)%ly(nly), cs_pl(ihru)%pl_in(npl), cs_pl(ihru)%pl_on(npl), cs_pl(ihru)%pl_up(npl), cs_soil(ihru)%ly(ly)%pest(npmx), cs_soil(ihru)%ly(ly)%pest, cs_pl(ihru)%pl_in(ipl)%pest(npmx), cs_pl(ihru)%pl_in(ipl)%pest, cs_pl(ihru)%pl_on(ipl)%pest(npmx), cs_pl(ihru)%pl_on(ipl)%pest, cs_pl(ihru)%pl_up(ipl)%pest(npmx), cs_pl(ihru)%pl_up(ipl)%pest, cs_irr(ihru)%pest(npmx), cs_irr(ihru)%pest` |
| [sym:constituent_mass_module] | `cs_db, cs_soil, cs_pl, cs_irr, pest_soil_ini` | `cs_db%num_pests, cs_soil(ihru)%ly(nly), cs_pl(ihru)%pl_in(npl), cs_pl(ihru)%pl_on(npl), cs_pl(ihru)%pl_up(npl), cs_soil(ihru)%ly(ly)%pest(npmx), cs_soil(ihru)%ly(ly)%pest, cs_pl(ihru)%pl_in(ipl)%pest(npmx), cs_pl(ihru)%pl_in(ipl)%pest, cs_pl(ihru)%pl_on(ipl)%pest(npmx), cs_pl(ihru)%pl_on(ipl)%pest, cs_pl(ihru)%pl_up(ipl)%pest(npmx), cs_pl(ihru)%pl_up(ipl)%pest, cs_irr(ihru)%pest(npmx), cs_irr(ihru)%pest, pest_soil_ini(ipest_db)%plt(ipest), cs_pl(ihru)%pl_on(ipl)%pest(ipest), pest_soil_ini(ipest_db)%soil(ipest), cs_soil(ihru)%ly(ly)%pest(ipest)` |
| [sym:output_ls_pesticide_module] | `hpestb_d` | `hpestb_d(ihru)%pest(ipest)%plant` |
| [sym:hydrograph_module] | `sp_ob` | `sp_ob%hru` |
| [sym:plant_module] | `pcom` | `pcom(ihru)%npl, pcom(ihru)%lai_sum, pcom(ihru)%plg(ipl)%lai` |
| [sym:pesticide_data_module] | `pest_soil_ini` | `pest_soil_ini(ipest_db)%plt(ipest), pest_soil_ini(ipest_db)%soil(ipest)` |

## Local Variables

<!-- facts:locals -->

## State Changes

| Target | When | Meaning |
| --- | --- | --- |
| `cs_soil(ihru)%ly(ly)%pest` | When `cs_db%num_pests > 0`, for each HRU and each soil layer. | `cs_soil(ihru)%ly(ly)%pest` is allocated and filled with the initial areal pesticide mass for every pesticide species in every soil layer. This establishes the starting soil pesticide pool that later transport, decay, and accounting routines evolve. |
| `cs_pl(ihru)%pl_in(ipl)%pest` | When `cs_db%num_pests > 0`, for each HRU and each plant in that HRU. | `cs_pl(ihru)%pl_in(ipl)%pest` is allocated and initialized to zero as part of setting up plant pesticide bookkeeping. It is the plant-input pesticide pool that later plant uptake or transfer routines can use. |
| `cs_pl(ihru)%pl_on(ipl)%pest` | When `cs_db%num_pests > 0`, for each HRU and each plant in that HRU. | `cs_pl(ihru)%pl_on(ipl)%pest` is allocated and then incremented by the LAI-weighted share of the initial plant pesticide concentration. It represents pesticide currently on plant surfaces and starts with the apportioned initial load. |
| `cs_pl(ihru)%pl_up(ipl)%pest` | When `cs_db%num_pests > 0`, for each HRU and each plant in that HRU. | `cs_pl(ihru)%pl_up(ipl)%pest` is allocated and initialized to zero as the plant uptake pesticide pool. It begins empty and is later used when pesticide moves into plant tissue. |
| `cs_irr(ihru)%pest` | When `cs_db%num_pests > 0`, for each HRU. | `cs_irr(ihru)%pest` is allocated and zeroed as the irrigation-water pesticide pool. This creates a place to track pesticide carried by irrigation inputs even though no initial mass is assigned here. |
| `hpestb_d(ihru)%pest(ipest)%plant` | When `cs_db%num_pests > 0`, for each HRU and each pesticide species. | `hpestb_d(ihru)%pest(ipest)%plant` is set to the initial plant pesticide amount from the pesticide soil initialization database. It records the plant-side starting balance used in output tracking. |
| `cs_pl(ihru)%pl_on(ipl)%pest(ipest)` | When `cs_db%num_pests > 0`, for each HRU, each pesticide species, and each plant. | `cs_pl(ihru)%pl_on(ipl)%pest(ipest)` receives the plant's LAI-weighted share of the initial pesticide-on-plant concentration. This spreads the HRU's starting foliar pesticide load across plants according to canopy size. |
| `cs_soil(ihru)%ly(ly)%pest(ipest)` | When `cs_db%num_pests > 0`, for each HRU, each pesticide species, and each soil layer. | `cs_soil(ihru)%ly(ly)%pest(ipest)` is set to the soil concentration converted to kg/ha using layer bulk density and thickness. This initializes the layer-wise pesticide reservoir in mass units. |

## File I/O

<!-- facts:io -->


## Lineage

`pesticide_init` was added in df07e3f as a new subroutine that allocates HRU pesticide pools and initializes them from soil-plant pesticide database values. The next resolved commit, 35b029c, expanded initialization by introducing cached `nly` and `npl` counts, allocating full HRU-level soil and plant pesticide structures before the per-layer and per-plant loops, zeroing `cs_irr(ihru)%pest`, and adding LAI-sum protection plus a `Min(...,1.)` cap when splitting plant pesticide load. f8bb6ec then moved the `cs_soil(ihru)%ly(ly)%pest` allocation to include `source = 0.` and shifted the plant-pool allocations inside the plant loop; 39fabde initialized the local counters and scalars to zero. e18817a made the plant allocations consistently occur inside the plant loop and kept the zeroing behavior explicit. No later resolved commit changed the routine's core initialization logic beyond these allocation/initialization refinements.

- df07e3f introduced the routine and its basic job: allocate HRU pesticide arrays, seed plant pesticide balance from `pest_soil_ini(ipest_db)%plt`, and convert soil initial concentrations to layer masses.
- 35b029c added full HRU-level allocation for `cs_soil`, `cs_pl%pl_in`, `cs_pl%pl_on`, and `cs_pl%pl_up`, added zero initialization for `cs_irr`, and made the plant split safer by guarding against tiny `lai_sum` values and capping `pl_frac` at 1.
- f8bb6ec and e18817a refined allocation placement and explicit zeroing so the pesticide arrays are created and initialized in the correct loop scope.
- 39fabde initialized local loop counters and working scalars to zero before use.

## Review Notes

- No direct file I/O was extracted for this procedure.
- warning: missing_doc: Procedure 'pesticide_init' has no extracted documentation comment.
