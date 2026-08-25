---
kind: procedure
symbol: salt_hru_init
title: salt_hru_init
status: filled
source_hash: 9651589310bc5805
version_label: SWAT+ 62.0.0
locals:
  ihru: HRU loop index; identifies which hydrologic response unit is currently being initialized.
  npmx: Number of salt ions simulated, copied from `cs_db%num_salts`, and used to size and
    loop over salt arrays.
  ly: Soil-layer loop index within the current HRU.
  isalt: Salt-ion loop index used to assign each simulated salt species.
  isalt_db: Index of the salt initial-condition database selected for the current HRU via
    `sol_plt_ini(isp_ini)%salt`.
  isp_ini: Index of the soil-plant initialization record for the current HRU, taken from `hru(ihru)%dbs%soil_plant_init`.
  hru_area_m2: Current HRU area converted from hectares to square meters for water-volume
    and mass-per-area calculations.
  water_volume: Water volume represented by a soil layer, computed from layer storage depth
    and HRU area, then used to convert concentration to salt mass.
uses:
  hru_module: '`hru_module` supplies the HRU list, each HRU''s area, and the soil-plant initialization
    pointer that determines which salt initial database to use; without those fields the routine
    cannot size or seed the salt state per HRU.'
  soil_module: '`soil_module` provides the number of layers in each HRU and each layer''s
    stored water (`st`), both of which control the nested loops and the concentration-to-mass
    conversion.'
  organic_mineral_mass_module: '`organic_mineral_mass_module` is imported by the routine,
    but no resolved symbols from it were extracted in the supplied evidence, so its direct
    role here is uncertain from the packet.'
  constituent_mass_module: '`constituent_mass_module` owns the salt-state containers and the
    initial salt concentration tables that this routine allocates and fills; the routine writes
    into `cs_soil`, `cs_irr`, `salt_soil_ini`, and `salt_water_irr` to establish starting
    salt concentrations and masses.'
  output_ls_pesticide_module: '`output_ls_pesticide_module` is imported here, but no resolved
    state from that module appears in the extracted source lines, so its specific use in this
    routine is not evident from the packet.'
  hydrograph_module: '`hydrograph_module` provides `sp_ob%hru`, the HRU count used to iterate
    over every HRU that needs salt initialization.'
  plant_module: '`plant_module` is imported, but the extracted source does not show any resolved
    plant symbols being referenced directly in this subroutine.'
  pesticide_data_module: '`pesticide_data_module` is imported, but no resolved pesticide-data
    symbols are shown being used in the extracted body of this routine.'
  salt_module: '`salt_module` is imported to make salt-specific state and database definitions
    available to the initialization routine, even though the extracted lines do not resolve
    a specific symbol from that module.'
---

<!-- facts:header -->

Initializes salt concentration and mass storage for each HRU and soil layer before the simulation begins.

## Bottom Line

salt_hru_init initializes salt state for every HRU when salts are being simulated. It sizes the per-HRU soil and irrigation salt arrays from the salt-count database, then seeds each soil layer with initial salt concentrations, salt masses, irrigation-water salt concentrations, and mineral salt fractions from the matched salt initialization record.

This setup matters because later salt routing, mass-balance, and output code depend on these arrays being allocated and populated before any transport or accounting steps run.

## Arguments

<!-- facts:arguments -->

## Where It Fits

This routine runs during HRU initialization inside `proc_hru`, after soil, structure, plant, CN2, and hydrograph setup and before later HRU constituent initialization. It depends on the HRU/soil database selections already being established, and its initialized salt arrays are then available for downstream salt transport, irrigation, and output calculations.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. get salt count | Read the number of simulated salt ions from `cs_db%num_salts` and store it in `npmx` so the routine can size arrays and decide whether salt initialization is needed. |
| 2. loop HRUs | Iterate over every HRU in `sp_ob%hru` so each hydrologic response unit gets its salt state initialized. |
| 3. check salt flag | Only allocate and fill salt arrays when at least one salt ion is being simulated. |
| 4. allocate soil salt storage | For each soil layer in the current HRU, allocate the soil salt mass array, mineral-salt fraction array, and salt concentration array, then allocate the HRU irrigation salt concentration array, all with zero initial values. |
| 5. select salt database | Use the HRU's soil-plant initialization index to choose the matching salt initial-condition database record. |
| 6. convert HRU area | Convert HRU area from hectares to square meters for later concentration-to-mass calculations. |
| 7. loop salt ions | Visit each simulated salt ion so concentration and mass can be assigned species by species. |
| 8. seed soil layer salts | For each soil layer, copy the initial soil salt concentration, compute the layer water volume from stored water and HRU area, and convert that concentration to salt mass per hectare. |
| 9. seed irrigation salts | Set the irrigation-water salt concentration for the current salt ion from the irrigation salt database. |
| 10. seed mineral fractions | Copy the five mineral salt fraction values into every soil layer from the same initial salt database record. |
| 11. finish | End the HRU loop and return to the caller after all salt state has been initialized. |

## Modules Used

<!-- facts:uses -->

| Module | State touched | Key components |
| --- | --- | --- |
| [sym:hru_module] | `hru, sol_plt_ini` | `hru(ihru)%dbs%soil_plant_init, sol_plt_ini(isp_ini)%salt, hru(ihru)%area_ha` |
| [sym:soil_module] | `soil` | `soil(ihru)%nly, soil(ihru)%phys(ly)%st` |
| [sym:organic_mineral_mass_module] | `organic_mineral_mass_module` |  |
| [sym:constituent_mass_module] | `cs_db, cs_soil, cs_irr, salt_soil_ini, salt_water_irr` | `cs_db%num_salts, cs_soil(ihru)%ly(ly)%salt(npmx), cs_soil(ihru)%ly(ly)%salt_min(5), cs_soil(ihru)%ly(ly)%saltc(npmx), cs_irr(ihru)%saltc(npmx), cs_soil(ihru)%ly(ly)%saltc(isalt), salt_soil_ini(isalt_db)%soil(isalt), cs_soil(ihru)%ly(ly)%salt(isalt), cs_irr(ihru)%saltc(isalt), salt_water_irr(isalt_db)%water(isalt), cs_soil(ihru)%ly(ly)%salt_min(isalt), salt_soil_ini(isalt_db)%soil(npmx+isalt)` |
| [sym:output_ls_pesticide_module] | `output_ls_pesticide_module` |  |
| [sym:hydrograph_module] | `sp_ob` | `sp_ob%hru` |
| [sym:plant_module] | `plant_module` |  |
| [sym:pesticide_data_module] | `pesticide_data_module` |  |
| [sym:salt_module] | `salt_module` |  |

## Local Variables

<!-- facts:locals -->

## State Changes

| Target | When | Meaning |
| --- | --- | --- |
| `cs_soil(ihru)%ly(ly)%saltc(isalt)` | When `cs_db%num_salts > 0`, inside the per-HRU and per-salt loops. | `cs_soil(ihru)%ly(ly)%saltc(isalt)` is set to the initial soil salt concentration for the selected salt database record, giving each layer a starting concentration for that salt ion. |
| `cs_soil(ihru)%ly(ly)%salt(isalt)` | When `cs_db%num_salts > 0`, inside the per-HRU, per-salt, and per-layer loops. | `cs_soil(ihru)%ly(ly)%salt(isalt)` is computed from the initial soil concentration and the layer water volume, so each layer starts with a salt mass per hectare consistent with its stored water. |
| `cs_irr(ihru)%saltc(isalt)` | When `cs_db%num_salts > 0`, for each salt ion in each HRU. | `cs_irr(ihru)%saltc(isalt)` is assigned the initial irrigation-water salt concentration so later irrigation routines can use a seeded salt concentration for that HRU. |
| `cs_soil(ihru)%ly(ly)%salt_min(isalt)` | When `cs_db%num_salts > 0`, for each of the five mineral salt fraction slots in each soil layer. | `cs_soil(ihru)%ly(ly)%salt_min(isalt)` is copied from the tail of the salt soil initial-condition table, establishing the starting mineral-fraction values used later in salt bookkeeping. |

## File I/O

<!-- facts:io -->


## Lineage

Resolved lineage shows four changes to `salt_hru_init`: it was introduced in `df07e3f` with the HRU-loop salt initialization logic; `f8bb6ec` changed the soil salt allocation to zero-initialize `cs_soil(ihru)%ly(ly)%salt`; `39fabde` expanded zero-initialization to `salt_min`, `saltc`, and `cs_irr(ihru)%saltc` and initialized local scalars; `1c812c1` renamed the imported soil-plant salt selector from `sol_plt_ini_cs` to `sol_plt_ini`, and `2ee1889` removed the unused `icmd` import and local `wt1` variable.

- df07e3f introduced `salt_hru_init` and the HRU-wide salt seeding workflow.
- f8bb6ec changed soil salt mass allocation to use `source = 0.` so new arrays start defined as zero.
- 39fabde changed allocation of `salt_min`, `saltc`, and `cs_irr%saltc` to zero-initialize them and set local scalar defaults.
- 1c812c1 renamed the imported HRU salt initialization pointer from `sol_plt_ini_cs` to `sol_plt_ini` and updated the database lookup accordingly.
- 2ee1889 removed the unused `icmd` module symbol and the unused local `wt1`.

## Review Notes

- No direct file I/O was extracted for this procedure.
- warning: missing_doc: Procedure 'salt_hru_init' has no extracted documentation comment.
