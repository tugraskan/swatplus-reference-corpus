---
kind: procedure
symbol: hru_allo
title: hru_allo
status: filled
source_hash: f145f8d6ee694420
version_label: SWAT+ 62.0.0
locals:
  imax: '`imax` stores the number of HRU objects reported by `sp_ob%hru` and is used to choose
    the allocation bounds for every HRU-indexed array.'
  ii: '`ii` is a loop counter used to step through each HRU when allocating per-HRU wetland
    salt and constituent subarrays.'
uses:
  hru_module: '`hru_module` provides the `hru` array that holds each hydrologic response unit''s
    state, so this routine must allocate it before any HRU records can be read or initialized.'
  hydrograph_module: '`hydrograph_module` supplies the HRU-linked hydrograph and transfer
    containers, including `sp_ob%hru` for sizing and arrays such as `irrig`, `wet`, and the
    wetland input/output trackers that must exist before HRU and wetland processing can populate
    them.'
  organic_mineral_mass_module: '`organic_mineral_mass_module` defines the soil-profile and
    plant-community mass arrays (`soil1`, `soil1_init`, `pl_mass`) that store HRU mass state,
    so they must be allocated here before soil and vegetation initialization uses them.'
  constituent_mass_module: '`constituent_mass_module` provides the constituent database counts
    and the HRU/wetland mass containers for salts and other constituents, and `hru_allo` uses
    those counts to decide whether to allocate the corresponding per-HRU and per-wetland arrays.'
  reservoir_module: '`reservoir_module` defines the wetland object array `wet_ob`, which is
    part of the wetland state that must be allocated alongside the HRU and wetland bookkeeping
    arrays.'
  reservoir_data_module: '`reservoir_data_module` supplies the wetland parameter and hydraulic-data
    arrays (`wet_prm`, `wet_hyd`) that are sized by HRU count and later filled by wetland
    initialization routines.'
  carbon_module: The module is part of the initialization dependency set for `hru_allo`, so
    its state must be available before downstream HRU setup can complete even though no specific
    carbon symbol was extracted in this packet.
  plant_module: '`plant_module` provides the `pcom` plant-community array, which must be allocated
    so HRU land cover and plant community data can be loaded after this routine runs.'
  soil_module: '`soil_module` provides the `soil` profile array, and `hru_allo` allocates
    it so each HRU can later carry its soil profile state into soil initialization and process
    calculations.'
  water_body_module: '`water_body_module` supplies the wetland water-body hydrograph arrays
    (`wet_wat_d`, `wet_wat_m`, `wet_wat_y`, `wet_wat_a`) that store wetland water-balance
    outputs and therefore must be allocated here with the rest of the wetland state.'
  channel_velocity_module: '`channel_velocity_module` provides `grwway_vel`, the channel/grassway
    velocity parameter array that is sized per HRU and needed for later routing and runoff
    calculations.'
  res_salt_module: '`res_salt_module` holds the wetland salt-output arrays, and `hru_allo`
    allocates them only when salt constituents are simulated so later wetland salt balances
    have storage for daily, monthly, yearly, and annual outputs.'
  res_cs_module: '`res_cs_module` holds the wetland other-constituent output arrays, and `hru_allo`
    allocates them only when other constituents are simulated so the wetland constituent balances
    can be recorded at each output time scale.'
---

<!-- facts:header -->

Allocates and sizes the HRU, wetland, soil, plant, irrigation, and constituent-mass arrays used for hydrologic response unit processing.

## Bottom Line

`hru_allo` is a setup routine. It looks at `sp_ob%hru` and allocates the core HRU arrays either as a one-element placeholder when there are no HRUs or as `0:imax` arrays when HRUs are present.

It also allocates the wetland-related storage needed for later hydrology and chemistry bookkeeping: wetland water-body objects, wetland input/output hydrographs, seepage tracking, and salt/constituent mass balances when `cs_db%num_salts` or `cs_db%num_cs` are positive. Later HRU initialization and output routines depend on these arrays existing at the right size.

## Arguments

<!-- facts:arguments -->

## Where It Fits

`hru_allo` runs at the start of HRU processing, immediately after `proc_hru` confirms there are HRUs and before `hru_read`, `hrudb_init`, `hru_lum_init_all`, `topohyd_init`, and `hru_output_allo`. Its allocations are the storage foundation those later routines fill and use to initialize soils, plants, wetlands, irrigation, and chemical mass state.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. Read the HRU count and decide whether to create placeholder arrays or full HRU-sized arrays. | The routine initializes `imax` to the number of HRUs in `sp_ob%hru`, then branches on whether that count is zero. This determines whether the code allocates one-element placeholder arrays or arrays sized to the actual HRU index range. |
| 2. Allocate the core HRU, soil, plant, irrigation, and constituent containers for the zero-HRU case. | When no HRUs exist, the routine allocates minimal `0:0` storage for the HRU state, grassway velocity, soil profile, soil mass, plant mass, plant communities, soil/plant/irrigation constituent masses, and irrigation transfer arrays so later code can still reference these symbols safely. |
| 3. Allocate the same core HRU, soil, plant, irrigation, and constituent containers for the normal HRU case. | When HRUs exist, the routine allocates each core array over `0:imax`, matching the number of HRUs reported by `sp_ob%hru`. These arrays become the main per-HRU storage used by later initialization and process routines. |
| 4. Allocate wetland and wetland-output arrays that are only needed when HRUs are present. | The routine allocates wetland storage for the HRU case: wetland hydrologic outputs, wetland parameter and hydraulic-data arrays, initial wetland mass state, wetland object storage, seepage tracking, and wetland water-body hydrographs. These arrays support later wetland routing and balance calculations. |
| 5. Allocate wetland salt storage only when salts are being simulated. | If `cs_db%num_salts` is positive, the routine allocates daily, monthly, yearly, and annual salt-output containers for each HRU and then allocates a salt vector inside each HRU's wetland water container. It also initializes the wetland water concentration array `saltc` to zero at allocation time. |
| 6. Allocate wetland other-constituent storage only when other constituents are being simulated. | If `cs_db%num_cs` is positive, the routine allocates the corresponding wetland constituent output containers for each HRU and then allocates each HRU's wetland water constituent mass and concentration arrays, zero-initializing `csc` during allocation. |
| 7. Finish without further computation. | The routine exits after allocation. It performs no direct I/O, no calculations beyond sizing and initializing arrays, and no downstream calls. |

## Modules Used

<!-- facts:uses -->

| Module | State touched | Key components |
| --- | --- | --- |
| [sym:hru_module] | `hru` |  |
| [sym:hydrograph_module] | `sp_ob, irrig, wet, wet_om_init, wet_in_d, wet_in_m, wet_in_y, wet_in_a, wet_out_d, wet_out_m, wet_out_y, wet_out_a, wet_seep_day` | `sp_ob%hru` |
| [sym:organic_mineral_mass_module] | `soil1, soil1_init, pl_mass` |  |
| [sym:constituent_mass_module] | `cs_db, wet_water, cs_soil, cs_pl, cs_irr` | `cs_db%num_salts, wet_water(ii)%salt, wet_water(ii)%saltc, cs_db%num_cs, wet_water(ii)%cs, wet_water(ii)%csc` |
| [sym:reservoir_module] | `wet_ob` |  |
| [sym:reservoir_data_module] | `wet_prm, wet_hyd` |  |
| [sym:carbon_module] | `carbon-related module state and types are imported but no specific carbon symbols were resolved from the extracted context.` |  |
| [sym:plant_module] | `pcom` |  |
| [sym:soil_module] | `soil` |  |
| [sym:water_body_module] | `wet_wat_d, wet_wat_m, wet_wat_y, wet_wat_a` |  |
| [sym:channel_velocity_module] | `grwway_vel` |  |
| [sym:res_salt_module] | `wetsalt_d, wetsalt_m, wetsalt_y, wetsalt_a` | `wetsalt_d(ii)%salt, wetsalt_m(ii)%salt, wetsalt_y(ii)%salt, wetsalt_a(ii)%salt` |
| [sym:res_cs_module] | `wetcs_d, wetcs_m, wetcs_y, wetcs_a` | `wetcs_d(ii)%cs, wetcs_m(ii)%cs, wetcs_y(ii)%cs, wetcs_a(ii)%cs` |

## Local Variables

<!-- facts:locals -->

## State Changes

| Target | When | Meaning |
| --- | --- | --- |
| `none extracted` | none extracted | No assignment targets were extracted automatically. |

## File I/O

<!-- facts:io -->


## Lineage

Source-backed lineage commits were resolved. The initial addition in df07e3f created `hru_allo` with the core HRU, soil, plant, irrigation, wetland, and constituent allocations. 96c2bfb added `reservoir_data_module` and the `wet_prm`/`wet_hyd` allocations. 39fabde initialized `imax` and `ii` to zero and adjusted wetland salt/constituent allocation formatting and zero-initialization. eb22103 removed obsolete `rsd1` allocations after residue management moved to the new soil1 structure.

- df07e3f established the routine as the HRU allocation entry point and defined the baseline per-HRU and wetland allocation structure used by later initialization code.
- 96c2bfb expanded the allocation set to include wetland parameter and hydraulic-data arrays from `reservoir_data_module`, enabling wetland setup to use explicit data containers.
- 39fabde made the local counters explicitly initialized and changed wetland salt/constituent allocation details, including zero-initializing `wet_water(ii)%saltc` and `wet_water(ii)%csc` during allocation.
- eb22103 removed allocation of the obsolete `rsd1` array, aligning HRU allocation with the newer `soil1` residue handling.

## Review Notes

- No direct file I/O was extracted for this procedure.
- warning: missing_doc: Procedure 'hru_allo' has no extracted documentation comment.
