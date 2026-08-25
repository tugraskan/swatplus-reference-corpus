---
kind: procedure
symbol: res_allo
title: res_allo
status: filled
source_hash: 7e78e6b073af5086
version_label: SWAT+ 62.0.0
locals:
  ires: Loop index over reservoir objects. It is initialized to 0 and then used as the per-reservoir
    index when allocating subarrays for each reservoir from 1 to `sp_ob%res`.
  mres: Holds the total number of reservoir objects from `sp_ob%res`. It controls the upper
    bound for the top-level allocation arrays such as `res(0:mres)` and the daily/monthly/yearly/average
    reservoir tracking arrays.
uses:
  reservoir_module: '`res_ob` stores each reservoir object, and its `aq_mix` array is allocated
    here to hold pesticide-related aquatic mixing values for each reservoir. `res_allo` needs
    `reservoir_module` because it creates the reservoir object storage that later reservoir
    and constituent routines populate and use.'
  reservoir_data_module: '`res_prm` and `res_hyd` are the reservoir parameter and hydrology
    data tables that back reservoir behavior. `res_allo` allocates their object arrays so
    later routines can load reservoir-specific setup and hydrologic properties into per-reservoir
    storage.'
  res_pesticide_module: The pesticide output arrays hold reservoir pesticide hydrographs for
    daily, monthly, yearly, and annual summaries, plus basin-level summary containers. `res_allo`
    allocates them because reservoir constituent initialization later writes pesticide mass-balance
    results into these structures.
  res_salt_module: The salt output arrays provide the reservoir salt hydrograph containers
    for the different reporting intervals. `res_allo` must allocate them so salt constituent
    tracking for reservoirs has storage before salt data are read and simulated.
  res_cs_module: The CS output arrays provide the reservoir constituent hydrograph containers
    for daily, monthly, yearly, and annual reporting. `res_allo` allocates them so non-salt
    constituent tracking has storage before the reservoir constituent routines run.
  hydrograph_module: '`sp_ob%res` supplies the number of reservoir objects to allocate. `res_allo`
    uses that count to size every reservoir-related array consistently, so the hydrograph
    module can manage reservoir water and constituent outputs for each object.'
  constituent_mass_module: '`cs_db` contains the simulated constituent counts that decide
    which per-reservoir arrays need suballocation and how large they must be. `res_water`
    and `res_benthic` hold the actual reservoir water-column and benthic constituent masses,
    so this module is the driver for allocating pesticide, pathogen, metal, salt, and other
    constituent storage.'
  water_body_module: '`res_wat_d`, `res_wat_m`, `res_wat_y`, and `res_wat_a` are the water-body
    summary arrays for reservoirs. `res_allo` allocates them because reservoir water-body
    reporting depends on these containers being present before the reservoir model populates
    summary values.'
---

<!-- facts:header -->

Allocates and sizes the reservoir state and output arrays used by the reservoir process. It uses the configured number of reservoir objects and constituent counts to prepare daily, monthly, yearly, and average tracking storage before reservoir data are read and initialized.

## Bottom Line

`res_allo` is the reservoir allocation setup routine. It reads the reservoir count from `sp_ob%res`, allocates the reservoir object arrays and the associated hydrograph, water-body, pesticide, salt, and constituent-mass output arrays, then sizes per-reservoir subarrays according to `cs_db` counts.

This matters because later reservoir processing expects these arrays to exist before `res_objects`, `res_read`, `res_read_salt_cs`, and `res_initial` run. The routine also zero-initializes selected mass arrays so downstream reservoir mass-balance calculations start from defined storage.

## Arguments

<!-- facts:arguments -->

## Where It Fits

This routine runs early in `proc_res`, immediately after reservoir constituent databases are read (`res_read_saltdb`, `res_read_csdb`, and `res_read_conds`) and only when `sp_ob%res > 0`. `proc_res` then calls `res_objects`, `res_read`, `res_read_salt_cs`, and `res_initial`, all of which depend on the arrays allocated here being ready.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. Capture the reservoir count and allocate the top-level reservoir and reporting arrays. | Read `sp_ob%res` into `mres`, then allocate the reservoir object array and the reservoir-level hydrograph, parameter, hydrology, object, inflow, outflow, and water-body summary arrays for indices tied to the number of reservoir objects. |
| 2. Allocate the reservoir constituent tracking arrays for pesticides, salts, and other constituents. | Create the per-reservoir summary containers for pesticide, salt, and general constituent outputs so later mass-balance routines can record daily through annual reservoir constituent results. |
| 3. Enter per-reservoir allocation only when any constituents are simulated. | Guard the detailed allocations with `if (cs_db%num_tot > 0)` and loop over each reservoir object from 1 to `sp_ob%res` so subarrays are only created when constituent simulation is enabled. |
| 4. Allocate reservoir pesticide storage when pesticides are present. | If pesticides are simulated, allocate the reservoir water-column and benthic pesticide arrays, the reservoir mixing array `res_ob(ires)%aq_mix`, the reservoir pesticide hydrograph outputs, and the per-reservoir pathogen-path arrays for each reservoir. |
| 5. Allocate the remaining water-column hydrograph and heavy-metal storage for each reservoir. | Allocate the pathogen and heavy-metal arrays on both the water and benthic sides, using zero initialization where the source code requests it, so each reservoir has storage for those constituent classes. |
| 6. Allocate salt output and reservoir salt mass arrays when salts are simulated. | If salts are simulated, allocate the salt hydrograph outputs for the reservoir and the water-column and benthic salt mass arrays, including the concentration array that is explicitly source-initialized to zero. |
| 7. Allocate generic constituent output and reservoir constituent mass arrays when other constituents are simulated. | If generic constituents are simulated, allocate the reservoir constituent hydrograph outputs and the water-column and benthic constituent mass arrays, including the concentration array that is explicitly source-initialized to zero. |
| 8. Allocate the basin-level pesticide summary arrays after all per-reservoir allocations are complete. | When pesticides are simulated, allocate the basin summary pesticide output containers so aggregated reservoir pesticide reporting can be collected after per-reservoir storage exists. |
| 9. Return after allocation is complete. | Exit the subroutine once all requested reservoir and constituent storage has been allocated. |

## Modules Used

<!-- facts:uses -->

| Module | State touched | Key components |
| --- | --- | --- |
| [sym:reservoir_module] | `res_ob` | `res_ob(ires)%aq_mix` |
| [sym:reservoir_data_module] | `res_prm, res_hyd` |  |
| [sym:res_pesticide_module] | `respst_d, respst_m, respst_y, respst_a, brespst_d, brespst_m, brespst_y, brespst_a` | `respst_d(ires)%pest, respst_m(ires)%pest, respst_y(ires)%pest, respst_a(ires)%pest, brespst_d%pest, brespst_m%pest, brespst_y%pest, brespst_a%pest` |
| [sym:res_salt_module] | `ressalt_d, ressalt_m, ressalt_y, ressalt_a` | `ressalt_d(ires)%salt, ressalt_m(ires)%salt, ressalt_y(ires)%salt, ressalt_a(ires)%salt` |
| [sym:res_cs_module] | `rescs_d, rescs_m, rescs_y, rescs_a` | `rescs_d(ires)%cs, rescs_m(ires)%cs, rescs_y(ires)%cs, rescs_a(ires)%cs` |
| [sym:hydrograph_module] | `sp_ob, res, res_om_init, res_trap, res_in_d, res_in_m, res_in_y, res_in_a, res_out_d, res_out_m, res_out_y, res_out_a` | `sp_ob%res` |
| [sym:constituent_mass_module] | `cs_db, res_water, res_benthic` | `cs_db%num_tot, cs_db%num_pests, res_water(ires)%pest, res_benthic(ires)%pest, res_water(ires)%path, cs_db%num_paths, res_benthic(ires)%path, res_water(ires)%hmet, cs_db%num_metals, res_benthic(ires)%hmet, cs_db%num_salts, res_water(ires)%salt, res_water(ires)%saltc, res_benthic(ires)%salt, cs_db%num_cs, res_water(ires)%cs, res_water(ires)%csc, res_benthic(ires)%cs` |
| [sym:water_body_module] | `res_wat_d, res_wat_m, res_wat_y, res_wat_a` |  |

## Local Variables

<!-- facts:locals -->

## State Changes

| Target | When | Meaning |
| --- | --- | --- |
| `none extracted` | none extracted | No assignment targets were extracted automatically. |

## File I/O

<!-- facts:io -->


## Lineage

Resolved lineage commits show the routine was introduced in `df07e3f` as a new allocation subroutine, then expanded in `96c2bfb` to add `res_prm` and `res_hyd` allocations, in `f8bb6ec` to zero-initialize some constituent arrays, in `39fabde` to initialize `ires` and `mres` and add more zero-initialized allocations, and in `e08326e` to add `res_trap` allocation.

- `df07e3f` created `res_allo` with the reservoir, hydrograph, constituent, and object-array allocation structure that later calls depend on.
- `96c2bfb` added allocation of `res_prm(0:mres)` and `res_hyd(0:mres)`, extending the routine to reserve parameter and hydrology storage.
- `f8bb6ec` changed reservoir constituent allocations so `res_water(ires)%pest` and `res_benthic(ires)%pest` use `source = 0.` and `res_benthic(ires)%path` uses `source = 0.`, making those arrays start from defined zero values.
- `39fabde` initialized `ires` and `mres` to zero and added zero-initialization to several reservoir constituent allocations, including `res_ob(ires)%aq_mix`, `res_water(ires)%hmet`, `res_benthic(ires)%hmet`, and `res_water(ires)%saltc`; it also kept the salt and CS allocation blocks aligned with those initialized outputs.
- `e08326e` added allocation for `res_trap(mres)`, extending the reservoir hydrograph output storage.

## Review Notes

- No direct file I/O was extracted for this procedure.
- warning: missing_doc: Procedure 'res_allo' has no extracted documentation comment.
