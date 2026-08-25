---
kind: procedure
symbol: cs_hru_init
title: cs_hru_init
status: filled
source_hash: 90bf97bc8d0ddcb2
version_label: SWAT+ 62.0.0
locals:
  ihru: Loop counter over HRUs; used to initialize constituent state for each HRU in turn.
  npmx: Total number of simulated constituents from `cs_db%num_cs`; controls whether constituent
    arrays are allocated and how many entries are filled.
  ly: Loop counter over soil layers within an HRU.
  ics: Loop counter over constituent index within the initialized constituent database and
    per-HRU constituent arrays.
  ics_db: Index of the soil-plant constituent initialization record selected for the current
    HRU via `sol_plt_ini(isp_ini)%cs`.
  isp_ini: Index of the soil-plant initialization set selected for the current HRU from `hru(ihru)%dbs%soil_plant_init`.
  hru_area_m2: Current HRU area converted from hectares to square meters for volume and mass
    conversions.
  water_volume: Temporary water volume for a soil layer, computed from soil water storage
    depth and HRU area.
  soil_volume: Temporary bulk soil volume for a soil layer, computed from layer thickness
    and HRU area.
  soil_mass: Temporary soil mass for a layer, computed from soil volume and bulk density.
  mass_sorbed: Temporary sorbed constituent mass for a layer, computed from initial sorbed
    concentration and soil mass before converting to kg/ha.
uses:
  hru_module: hru_module supplies the HRU objects that tell this routine which HRUs exist,
    which soil-plant initialization record each HRU should use, and how large each HRU is.
    `hru(ihru)%dbs%soil_plant_init`, `sol_plt_ini(isp_ini)%cs`, and `hru(ihru)%area_ha` together
    determine which initialization database entry to read and how to convert the source concentrations
    into HRU-scaled mass values.
  soil_module: soil_module provides the per-HRU soil layering and layer properties needed
    to size the initialization loops and convert concentrations into soil-water and sorbed
    mass. `soil(ihru)%nly`, `soil(ihru)%phys(ly)%st`, `soil(ihru)%phys(ly)%thick`, and `soil(ihru)%phys(ly)%bd`
    control how much water and soil mass each layer contains, which is required for the kg/ha
    calculations.
  organic_mineral_mass_module: No candidate outside references were resolved to `organic_mineral_mass_module`
    in the provided context, so its specific imported state is not identifiable from this
    packet. The module is listed as a dependency, but the source excerpt does not show any
    used symbols from it.
  constituent_mass_module: constituent_mass_module provides the constituent databases and
    storage arrays that this routine populates. `cs_db%num_cs` sets the number of constituents,
    `cs_soil_ini(ics_db)%soil(ics)` and `cs_water_irr(ics_db)%water(ics)` supply the starting
    concentrations, and `cs_soil(ihru)%ly(ly)%cs`, `csc`, `cs_sorb`, `csc_sorb`, and `cs_irr(ihru)%csc`
    are the target state arrays being allocated and filled for each HRU and soil layer.
  output_ls_pesticide_module: No candidate outside references were resolved to `output_ls_pesticide_module`
    in the provided context. The routine does not extract any symbol from that module in the
    source excerpt, so its role here cannot be narrowed further from this packet alone.
  hydrograph_module: hydrograph_module provides `sp_ob%hru`, the number of HRUs to iterate
    over. That count is the outer loop bound, so it determines how many HRU constituent arrays
    must be initialized before the simulation can proceed.
  plant_module: No candidate outside references were resolved to `plant_module` in the provided
    context. The routine comments mention plant mass, but the active source lines shown do
    not use a plant-module symbol, so the imported state cannot be identified from this packet.
  pesticide_data_module: No candidate outside references were resolved to `pesticide_data_module`
    in the provided context. Although the module is imported, the visible source excerpt does
    not reference any of its symbols, so its specific contribution here is not identifiable
    from this packet.
  cs_module: No candidate outside references were resolved to `cs_module` in the provided
    context. The source excerpt clearly uses `cs_db`, `cs_soil`, `cs_irr`, `cs_soil_ini`,
    and `cs_water_irr`, but the packet only resolves those as owned by `constituent_mass_module`,
    so no additional `cs_module` symbol can be identified here.
---

<!-- facts:header -->

Initializes HRU-level constituent storage from database concentrations for soil layers and irrigation water.

## Bottom Line

cs_hru_init initializes the constituent state for every HRU before simulation begins. It sizes the HRU soil and irrigation constituent arrays to the number of simulated constituents, then loads each soil layer and irrigation-water slot with starting concentrations and sorbed masses from the constituent initialization databases.

The routine matters because it turns the selected soil-plant initialization record for each HRU into model-ready mass and concentration states. Those initialized values are then available to the later transport, routing, and output routines that assume the constituent arrays already exist and contain start-of-run conditions.

## Arguments

<!-- facts:arguments -->

## Where It Fits

This routine runs during HRU initialization, after upstream setup has established the HRU list, soil profiles, plant initialization pointers, and the constituent database counts. In `proc_hru`, it is called only when `cs_db%num_cs > 0`, so the upstream workflow has already run `soils_init`, `structure_init`, `plant_all_init`, `cn2_init_all`, `hydro_init`, and the other constituent initializers as needed. Its results are the starting constituent concentrations and masses that later simulation code will read when moving constituents through soil layers and irrigation water.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. count HRUs | Read the number of simulated constituents into `npmx`, then start an outer loop over every HRU so each response unit gets its own constituent state initialized. |
| 2. allocate per-layer storage | If constituents are being simulated, allocate the soil-layer constituent arrays and the irrigation constituent array for the current HRU, initializing each allocated array to zero. |
| 3. choose initialization record | Use the HRU's soil-plant database pointer to select the corresponding constituent initialization record for this HRU. |
| 4. compute HRU area scale | Convert HRU area from hectares to square meters so the later concentration-to-mass conversions can be scaled by physical area. |
| 5. loop over constituents | Iterate through each constituent index that the model is simulating for this HRU. |
| 6. loop over soil layers | For each constituent, visit every soil layer so the layer-specific concentration and mass fields can be set. |
| 7. set soil-water concentration | Copy the initial soil concentration from `cs_soil_ini(ics_db)%soil(ics)` into the layer's dissolved constituent concentration. |
| 8. compute soil-water mass | Use soil water stored in the layer and HRU area to convert the initial concentration into a per-hectare dissolved constituent mass. |
| 9. set sorbed concentration | Load the sorbed constituent concentration from the second half of the soil initialization record, offset by `cs_db%num_cs`. |
| 10. compute sorbed mass | Derive soil volume and soil mass from layer thickness and bulk density, then convert the sorbed concentration into sorbed constituent mass per hectare. |
| 11. set irrigation concentration | Copy the initial irrigation-water concentration for the current constituent into the HRU's irrigation constituent array. |
| 12. finish | Complete the HRU loop and return to the caller after all HRU constituent states have been initialized. |

## Modules Used

<!-- facts:uses -->

| Module | State touched | Key components |
| --- | --- | --- |
| [sym:hru_module] | `hru, sol_plt_ini` | `hru(ihru)%dbs%soil_plant_init, sol_plt_ini(isp_ini)%cs, hru(ihru)%area_ha` |
| [sym:soil_module] | `soil` | `soil(ihru)%nly, soil(ihru)%phys(ly)%st, soil(ihru)%phys(ly)%thick, soil(ihru)%phys(ly)%bd` |
| [sym:organic_mineral_mass_module] | `none resolved` | `none resolved` |
| [sym:constituent_mass_module] | `cs_db, cs_soil, cs_irr, cs_soil_ini, cs_water_irr` | `cs_db%num_cs, cs_soil(ihru)%ly(ly)%cs(npmx), cs_soil(ihru)%ly(ly)%csc(npmx), cs_soil(ihru)%ly(ly)%cs_sorb(npmx), cs_soil(ihru)%ly(ly)%csc_sorb(npmx), cs_irr(ihru)%csc(npmx), cs_soil(ihru)%ly(ly)%csc(ics), cs_soil_ini(ics_db)%soil(ics), cs_soil(ihru)%ly(ly)%cs(ics), cs_soil(ihru)%ly(ly)%csc_sorb(ics), cs_soil_ini(ics_db)%soil, cs_soil(ihru)%ly(ly)%cs_sorb(ics), cs_irr(ihru)%csc(ics), cs_water_irr(ics_db)%water(ics)` |
| [sym:output_ls_pesticide_module] | `none resolved` | `none resolved` |
| [sym:hydrograph_module] | `sp_ob` | `sp_ob%hru` |
| [sym:plant_module] | `none resolved` | `none resolved` |
| [sym:pesticide_data_module] | `none resolved` | `none resolved` |
| [sym:cs_module] | `none resolved` | `none resolved` |

## Local Variables

<!-- facts:locals -->

## State Changes

| Target | When | Meaning |
| --- | --- | --- |
| `cs_soil(ihru)%ly(ly)%csc(ics)` | During the inner soil-layer loop for each HRU and constituent (`do ics = 1, npmx` and `do ly = 1, soil(ihru)%nly`). | This field is set from the initial soil constituent database entry for the active HRU, so it becomes the starting dissolved concentration in the soil layer and remains the base value for later transport calculations. |
| `cs_soil(ihru)%ly(ly)%cs(ics)` | During the inner soil-layer loop for each HRU and constituent when initial soil concentrations are copied and converted. | This field stores the dissolved constituent mass per hectare computed from the initial soil concentration and the layer's water volume, giving later routines the starting mass inventory in each layer. |
| `cs_soil(ihru)%ly(ly)%csc_sorb(ics)` | During the inner soil-layer loop for each HRU and constituent when the sorbed part of the initialization record is read. | This field is populated from the sorbed concentration slot in `cs_soil_ini(ics_db)%soil`, so it becomes the starting sorbed concentration on the soil phase for that layer. |
| `cs_soil(ihru)%ly(ly)%cs_sorb(ics)` | During the inner soil-layer loop for each HRU and constituent after soil mass is computed. | This field stores the sorbed constituent mass per hectare derived from the sorbed concentration, soil volume, and bulk density, forming the initial sorbed inventory in the layer. |
| `cs_irr(ihru)%csc(ics)` | Once per HRU and constituent after the soil initialization record is selected. | This field is filled from the irrigation-water initialization record and becomes the starting constituent concentration for irrigation inputs applied to the HRU. |

## File I/O

<!-- facts:io -->


## Lineage

The source was added in commit df07e3f as a new `cs_hru_init` subroutine that initialized HRU constituent arrays, selected the HRU-specific soil-plant record, and computed soil-water and sorbed constituent states. Commit c7c8e22 preserved that logic while carrying the file forward from bitbucket. Commit f8bb6ec changed only the `cs_soil(ihru)%ly(ly)%cs(npmx)` allocation to use `source = 0.`, and commit 39fabde extended zero-initialization to the other constituent arrays, initialized local counters/scalars to zero, and left the overall algorithm unchanged. Commit 2ee1889 removed the unused `icmd`, `ipl`, and `wt1` references from the imports/local declarations.

- df07e3f introduced the procedure and its HRU soil/irrigation constituent initialization workflow.
- f8bb6ec changed the soil constituent `cs` allocation to zero-fill on allocation.
- 39fabde zero-initialized the remaining allocated constituent arrays and local work variables, reducing dependence on undefined initial contents.
- 2ee1889 cleaned up the import list and removed unused local variables without changing the initialization algorithm.

## Review Notes

- No direct file I/O was extracted for this procedure.
- info: weak_doc: Procedure 'cs_hru_init' documentation is very short.
- algorithm_steps revised: expanded the draft into 12 source-backed steps to separate allocation, record selection, conversion, and final irrigation initialization.
- No candidate outside references were resolved to `organic_mineral_mass_module`, `output_ls_pesticide_module`, `plant_module`, `pesticide_data_module`, or `cs_module` in the provided context; these modules are imported but not symbol-resolved in the excerpt.
