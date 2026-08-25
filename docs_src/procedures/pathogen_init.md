---
kind: procedure
symbol: pathogen_init
title: pathogen_init
status: filled
source_hash: 884ff016ca565f83
version_label: SWAT+ 62.0.0
locals:
  mpath: Number of pathogen databases currently enabled (`cs_db%num_paths`); it controls whether
    pathogen arrays are allocated and how many pathogen slots are created.
  ly: Loop counter for soil layers. It is used to allocate per-layer soil pathogen storage
    and to target the first soil layer during initialization.
  ipath: Loop counter over pathogen types. It selects the current pathogen database entry
    when copying initial soil and plant values.
  ipath_db: Selected pathogen soil-plant initialization database index (`sol_plt_ini(isp_ini)%path`);
    it identifies which initial concentration table to read from.
  isp_ini: HRU-specific soil-plant initialization database index from `hru(ihru)%dbs%soil_plant_init`;
    it chooses the initialization record for the current HRU.
  ipl: Loop counter over plants in the HRU plant community. It is used to allocate pathogen
    arrays for each plant entry.
uses:
  hru_module: This module provides the HRU list and each HRU’s database pointers, which are
    needed to iterate over HRUs and select the soil-plant initialization record for the current
    HRU.
  soil_module: This module provides each HRU’s soil-layer count, which determines how many
    soil pathogen arrays to allocate and which layer index is valid for initialization.
  plant_module: This module provides each HRU’s plant-community size, which determines how
    many plant pathogen arrays must be allocated before later plant-pathogen accounting can
    work.
  pathogen_data_module: This module holds the pathogen database count and the initial soil/plant
    pathogen concentration tables that drive whether allocation happens and what initial values
    are copied into the HRU state.
  channel_module: It is imported by the routine, so the pathogen initialization shares the
    model-wide channel state namespace even though no channel member is referenced in the
    extracted source span.
  basin_module: It is imported by the routine, so basin-wide state is available in the same
    initialization context even though no basin member is referenced in the extracted source
    span.
  conditional_module: It is imported because this initialization participates in the shared
    model startup environment, even though the extracted code does not reference a conditional-module
    member directly.
  organic_mineral_mass_module: It is part of the constituent-mass initialization context used
    by the pathogen start-up path, even though the extracted source does not reference a specific
    organic/mineral mass symbol.
  hydrograph_module: This module provides `sp_ob%hru`, the HRU count that drives the outer
    loop over all hydrologic response units.
  constituent_mass_module: This module provides the pathogen count, pathogen storage arrays,
    and initial concentration tables that are read to allocate and seed HRU pathogen state.
  output_ls_pathogen_module: This module provides the pathogen balance array where the initial
    plant-associated pathogen loading is stored for later output and bookkeeping.
---

<!-- facts:header -->

Initializes pathogen state for every HRU. It allocates pathogen arrays and seeds the soil and plant pathogen starting concentrations from the chosen soil-plant initialization database.

## Bottom Line

`pathogen_init` runs once during HRU preprocessing to size and initialize pathogen storage for each HRU. It uses the global pathogen database count and each HRU’s soil and plant inventories to allocate the soil-, plant-, and irrigation-pathogen arrays that the rest of the simulation will read and update.

For HRUs with at least one pathogen database entry, it copies the initial soil concentration into the first soil layer’s pathogen state and loads the initial plant pathogen amount into the pathogen balance output state. Those initialized values become the starting point for later pathogen transport and accounting routines.

## Arguments

<!-- facts:arguments -->

## Where It Fits

`proc_hru` calls `pathogen_init` during model startup after soils, structure, plant community, CN2, and hydro initialization are complete and after `cs_db%num_paths` indicates that pathogens are being simulated. The results feed later pathogen transport, balance tracking, and output reporting because they establish the per-HRU soil, plant, and irrigation pathogen state used by downstream routines.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. Set up per-HRU pathogen sizing and gate allocation on the active pathogen count. | The routine loops across all HRUs and reads `cs_db%num_paths` into `mpath`. If no pathogen databases are active, the HRU is skipped; otherwise the routine prepares to allocate pathogen storage for that HRU. |
| 2. Allocate soil-layer pathogen arrays for each HRU soil layer. | For every soil layer in the HRU, it allocates the pathogen vector `cs_soil(ihru)%ly(ly)%path(mpath)` and initializes it to zero so each pathogen type has a clean soil-layer state. |
| 3. Allocate plant-pathogen arrays for each plant in the HRU community. | For every plant in the HRU community, it allocates the three plant pathogen arrays `pl_in`, `pl_on`, and `pl_up` at length `mpath`, initializing them to zero so the plant-associated pathogen bookkeeping starts empty. |
| 4. Allocate irrigation-pathogen storage for the HRU. | It allocates `cs_irr(ihru)%path(mpath)` for irrigation-associated pathogen mass, leaving room for pathogen loading on irrigation water when pathogens are simulated. |
| 5. Select the HRU’s soil-plant initialization database. | The routine reads the HRU’s soil-plant initialization index from `hru(ihru)%dbs%soil_plant_init` and then resolves the pathogen initialization table with `sol_plt_ini(isp_ini)%path`. |
| 6. Copy initial soil pathogen concentration into the first soil layer. | For each pathogen type, the routine enters the soil-layer loop and assigns the first layer’s pathogen concentration from `path_soil_ini(ipath_db)%soil(ipath)` when `ly == 1`; the code otherwise clears that same first-layer target to zero for non-first layers. |
| 7. Copy initial plant pathogen loading into the pathogen balance state. | For each pathogen type, it initializes `hpath_bal(ihru)%path(ipath)%plant` from `path_soil_ini(ipath_db)%plt(ipath)`, establishing the starting plant pathogen balance for output and later accounting. |
| 8. Finish the HRU loop and return to the caller. | After all HRUs are processed, the subroutine returns without any further side effects. |

## Modules Used

<!-- facts:uses -->

| Module | State touched | Key components |
| --- | --- | --- |
| [sym:hru_module] | `hru, sol_plt_ini, ihru` | `hru(ihru)%dbs%soil_plant_init, sol_plt_ini(isp_ini)%path` |
| [sym:soil_module] | `soil` | `soil(ihru)%nly` |
| [sym:plant_module] | `pcom` | `pcom(ihru)%npl` |
| [sym:pathogen_data_module] | `pathogen_data_module` | `cs_db%num_paths, path_soil_ini(ipath_db)%soil(ipath), path_soil_ini(ipath_db)%plt(ipath)` |
| [sym:channel_module] | `channel_module` | `no direct component reference extracted` |
| [sym:basin_module] | `basin_module` | `no direct component reference extracted` |
| [sym:conditional_module] | `conditional_module` | `no direct component reference extracted` |
| [sym:organic_mineral_mass_module] | `organic_mineral_mass_module` | `no direct component reference extracted` |
| [sym:hydrograph_module] | `sp_ob` | `sp_ob%hru` |
| [sym:constituent_mass_module] | `cs_db, cs_soil, cs_pl, cs_irr, path_soil_ini` | `cs_db%num_paths, cs_soil(ihru)%ly(ly)%path(mpath), cs_pl(ihru)%pl_in(ipl)%path(mpath), cs_pl(ihru)%pl_on(ipl)%path(mpath), cs_pl(ihru)%pl_up(ipl)%path(mpath), cs_irr(ihru)%path(mpath), cs_soil(ihru)%ly(1)%path(ipath), path_soil_ini(ipath_db)%soil(ipath), path_soil_ini(ipath_db)%plt(ipath)` |
| [sym:output_ls_pathogen_module] | `hpath_bal` | `hpath_bal(ihru)%path(ipath)%plant` |

## Local Variables

<!-- facts:locals -->

## State Changes

| Target | When | Meaning |
| --- | --- | --- |
| `cs_soil(ihru)%ly(1)%path(ipath)` | When `mpath > 0` and the routine reaches the `ipath` loop, with `ly == 1` inside the nested soil-layer loop. | `cs_soil(ihru)%ly(1)%path(ipath)` is set to the initial soil pathogen concentration for the selected pathogen database entry. This establishes the first soil layer’s starting pathogen load for each HRU and pathogen type. |
| `hpath_bal(ihru)%path(ipath)%plant` | When `mpath > 0` and the routine processes each `ipath` after selecting the HRU’s pathogen initialization database. | `hpath_bal(ihru)%path(ipath)%plant` is set to the initial plant-associated pathogen amount from the selected initialization table. This gives the pathogen balance output state its starting plant value for later bookkeeping and reporting. |

## File I/O

<!-- facts:io -->


## Lineage

Resolved lineage shows four behavior-changing edits and one documentation-only addition. The earliest resolved commit, `94b6dec`, introduced the existing routine body and its original documentation/comments. `f8bb6ec` moved the plant pathogen allocations out of the soil-layer loop and changed them to use `pest` arrays. `16e54aa` renamed those plant allocations from `pest` to `path`. `e18817a` kept the same allocation logic but switched the plant allocations to `source = 0.` and moved them into the plant loop. `1c812c1` updated the imported initialization symbol from `sol_plt_ini_cs` to `sol_plt_ini` and changed the `ipath_db` assignment to use that symbol.

- 94b6dec established the routine structure for HRU-wise pathogen initialization, including allocation of soil, plant, and irrigation pathogen storage and copying initial concentrations from the pathogen soil-plant tables.
- f8bb6ec changed the plant pathogen allocations so they were created separately from the soil-layer loop and targeted `pest` components before the later rename to pathogen paths.
- 16e54aa renamed the plant constituent allocations from `pest` to `path`, matching the pathogen-specific storage layout used now.
- e18817a retained the allocation placement but initialized the plant pathogen arrays to zero with `source = 0.`, reducing dependence on default allocation contents.
- 1c812c1 switched the soil-plant initialization lookup to `sol_plt_ini(isp_ini)%path`, reflecting the refactor that renamed the imported initialization array.

## Review Notes

- No direct file I/O was extracted for this procedure.
- warning: missing_doc: Procedure 'pathogen_init' has no extracted documentation comment.
- algorithm_steps revised: condensed the source into 8 model-level steps and corrected the soil-layer initialization description to reflect the actual `ly == 1` assignment in the source.
- The extracted source shows `channel_module`, `basin_module`, `conditional_module`, and `organic_mineral_mass_module` are imported but not directly referenced in the visible body.
