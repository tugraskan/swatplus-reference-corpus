---
kind: procedure
symbol: topohyd_init
title: topohyd_init
status: filled
source_hash: 6b76abd86baed70f
version_label: SWAT+ 62.0.0
locals:
  isno: Snow database index used to fetch the initial snow parameter set and initial snow
    water content for the current HRU.
  ifield_db: Field database pointer copied from the HRU database record and used to load field
    length, width, and angle into the HRU.
  itopohd_db: Topography database pointer for the HRU's hydrology-linked topographic settings;
    used to load slope length, lateral length, stream distance, and deposition coefficient.
  ihyd_db: Hydrology database pointer for the current HRU; used to load canopy, ET, percolation,
    enrichment, and lateral-flow coefficients.
  itopo_db: Topography database pointer for the HRU's topographic identity and elevation-related
    settings; used to copy the topographic name.
  isno_db: Snow database pointer copied from the HRU database and used to select which snow
    parameter record to copy into `hru(ihru)%sno`.
  iob: Object index for the HRU's corresponding hydrograph object; used to read the object
    elevation from `ob(iob)%elev`.
  perc_ln_func: Temporary real used in the logarithmic transform that converts `hru(ihru)%hyd%perco`
    into the limiting percolation coefficient `hru(ihru)%hyd%perco_lim`.
uses:
  hydrograph_module: The hydrograph module supplies the object list and the HRU count boundaries
    that this routine uses to map each HRU to its matching object and to read object elevation.
    Without `sp_ob`, `sp_ob1`, and `ob`, the routine could not assign `hru(ihru)%topo%elev`
    or determine the object offset for the loop.
  hru_module: The HRU module owns the live HRU records that this routine populates. It provides
    both the database pointers under `hru(ihru)%dbs` and the destination fields under `hru(ihru)%topo`,
    `hru(ihru)%hyd`, `hru(ihru)%sno`, `hru(ihru)%field`, and `hru(ihru)%hydcal` that receive
    the initialized values.
  hydrology_data_module: The hydrology data module holds the shared hydrology database records
    that define default HRU hydrologic parameters. `topohyd_init` copies these values into
    each HRU so later process code works from HRU-specific hydrology settings instead of raw
    database entries.
  topography_data_module: The topography data module holds the shared topography and field
    parameter tables that define the HRU geometry and land-surface characteristics. `topohyd_init`
    uses these records to set the HRU topographic name, slope, slope lengths, stream distance,
    deposition coefficient, and field dimensions.
  soil_data_module: The module is imported by this routine, but no resolved source references
    from it appear in the extracted body. It may be needed for type visibility or future expansion,
    but the visible code does not read soil state directly here.
  plant_module: The module is imported by this routine, but the extracted body does not reference
    any plant-module symbols directly. It may be included because the HRU hydrology values
    initialized here are later consumed by plant-related process code, but this routine itself
    does not read plant state.
---

<!-- facts:header -->

Initializes topographic, hydrologic, snow, and field parameters for each HRU from the database tables. It also derives a few HRU-specific coefficients needed later by water balance and management routines.

## Bottom Line

topohyd_init walks through every HRU and copies the selected topography, hydrology, snow, and field database entries into the live HRU structure. It also fills in a few derived or guarded values, such as a default lateral slope length of 50 m when the database value is effectively zero, a snow cover shape pair via `ascrv`, a percolation limit, and a normalized PET coefficient.

These initialized values matter because later daily HRU process routines use `hru(ihru)%topo`, `hru(ihru)%hyd`, `hru(ihru)%sno`, `hru(ihru)%field`, and `hru(ihru)%hydcal` as the working parameter set for runoff, lateral flow, erosion, snow cover, tile drainage, and water-balance calculations.

## Arguments

<!-- facts:arguments -->

## Where It Fits

This routine runs during HRU initialization after the HRU arrays, database pointers, and land-use management setup have already been prepared by `proc_hru` through `hru_allo`, `hru_read`, `hrudb_init`, and `hru_lum_init_all`. Its results feed the later daily HRU calculations that depend on initialized topography, hydrology, snow, and field parameters.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. loop over HRUs | Iterate through every HRU in the watershed/object set, compute the matching object index, and pull the database pointers for topography, hydrology, and field settings from the HRU's database selection record. |
| 2. copy topography basics | Load the HRU topographic name, elevation, slope, and slope length from the selected topography tables and the matching hydrograph object elevation. |
| 3. copy hydrology basics | Load the HRU hydrology name and key lateral-flow parameters from the selected hydrology and topography database entries. |
| 4. guard lateral length | If the lateral slope length is effectively zero, replace it with 50 m so the HRU has a usable value for later lateral-flow calculations. |
| 5. copy hydrology coefficients | Populate canopy storage, evaporation compensation, plant uptake compensation, organic enrichment, curve-number adjustment, and percolation coefficients from the hydrology database record. |
| 6. load snow parameters | Select the HRU snow parameter record, copy it into the HRU, and solve the snow-cover shape parameters `snocov1` and `snocov2` with `ascrv`. |
| 7. adjust tile drainage defaults | If tile drainage is enabled for the HRU, override the curve-number soil-water factor and percolation coefficient with tile-friendly values. |
| 8. derive percolation limit | Convert the percolation coefficient into a limiting value with a logarithmic formula, cap it at 1.0, or set it to zero when percolation is negligible. |
| 9. copy remaining hydrology | Load stream distance, biological mixing, lateral nutrient concentrations, lateral flow coefficient, and PET coefficient from the selected database records. |
| 10. normalize PET coefficient | Convert very small PET coefficients to 1.0 for old input compatibility, or scale small positive values to the Hargreaves form expected by later code. |
| 11. copy field data and deposition | Load field length, width, and angle, then copy the topographic deposition coefficient into the HRU topography record. |
| 12. set initial snow water | Assign the HRU's initial snow water content from the selected snow database record. |
| 13. snapshot hydrology for calibration | Copy the initialized hydrology record into `hydcal` so later soft-calibration or calibration-related logic can refer to the starting hydrology settings. |
| 14. return | Exit after all HRUs have been initialized. |

## Modules Used

<!-- facts:uses -->

| Module | State touched | Key components |
| --- | --- | --- |
| [sym:hydrograph_module] | `sp_ob, sp_ob1, ob` | `sp_ob%hru, sp_ob1%hru, ob(iob)%elev` |
| [sym:hru_module] | `hru, snodb, ihru` | `hru(ihru)%dbs%topo, hru(ihru)%dbs%hyd, hru(ihru)%dbs%field, hru(ihru)%topo%name, hru(ihru)%topo%elev, hru(ihru)%topo%slope, hru(ihru)%topo%slope_len, hru(ihru)%hyd%name, hru(ihru)%hyd%lat_ttime, hru(ihru)%hyd%lat_sed, hru(ihru)%topo%lat_len, hru(ihru)%hyd%canmx, hru(ihru)%hyd%esco, hru(ihru)%hyd%epco, hru(ihru)%hyd%erorgn, hru(ihru)%hyd%erorgp, hru(ihru)%hyd%cn3_swf, hru(ihru)%hyd%perco, hru(ihru)%dbs%snow, hru(ihru)%sno, hru(ihru)%snocov1, hru(ihru)%snocov2, hru(ihru)%tiledrain, hru(ihru)%hyd%perco_lim, hru(ihru)%topo%dis_stream, hru(ihru)%hyd%biomix, hru(ihru)%hyd%lat_orgn, hru(ihru)%hyd%lat_orgp, hru(ihru)%hyd%latq_co, hru(ihru)%hyd%pet_co, hru(ihru)%field%length, hru(ihru)%field%wid, hru(ihru)%field%ang, hru(ihru)%topo%dep_co, hru(ihru)%sno_mm, snodb(isno)%init_mm, hru(ihru)%hydcal, hru(ihru)%hyd` |
| [sym:hydrology_data_module] | `hyd_db` | `hyd_db(ihyd_db)%name, hyd_db(ihyd_db)%lat_ttime, hyd_db(ihyd_db)%lat_sed, hyd_db(ihyd_db)%canmx, hyd_db(ihyd_db)%esco, hyd_db(ihyd_db)%epco, hyd_db(ihyd_db)%erorgn, hyd_db(ihyd_db)%erorgp, hyd_db(ihyd_db)%cn3_swf, hyd_db(ihyd_db)%perco, hyd_db(ihyd_db)%biomix, hyd_db(ihyd_db)%lat_orgn, hyd_db(ihyd_db)%lat_orgp, hyd_db(ihyd_db)%latq_co, hyd_db(ihyd_db)%pet_co` |
| [sym:topography_data_module] | `topo_db, field_db` | `topo_db(itopo_db)%name, topo_db(itopohd_db)%slope, topo_db(itopohd_db)%slope_len, topo_db(itopohd_db)%lat_len, topo_db(itopohd_db)%dis_stream, field_db(ifield_db)%length, field_db(ifield_db)%wid, field_db(ifield_db)%ang, topo_db(itopohd_db)%dep_co` |
| [sym:soil_data_module] | `soil_data_module` |  |
| [sym:plant_module] | `plant_module` |  |

## Local Variables

<!-- facts:locals -->

## State Changes

| Target | When | Meaning |
| --- | --- | --- |
| `hru(ihru)%topo%name` | For every HRU in the `do ihru = 1, sp_ob%hru` loop. | The HRU topography name is filled from `topo_db(itopo_db)%name` so the live HRU record carries the selected topographic database label. |
| `hru(ihru)%topo%elev` | For every HRU in the loop. | The HRU elevation is overwritten with the associated object elevation from `ob(iob)%elev`, linking the HRU to its hydrograph object height. |
| `hru(ihru)%topo%slope` | For every HRU in the loop. | The HRU slope is loaded from the selected topography database record so later erosion and runoff routines use the configured slope steepness. |
| `hru(ihru)%topo%slope_len` | For every HRU in the loop. | The HRU slope length is loaded from the selected topography database record so later erosion calculations use the HRU-specific hillslope length. |
| `hru(ihru)%hyd%name` | For every HRU in the loop. | The HRU hydrology name is copied from the selected hydrology database record so the live HRU hydrology state reflects the chosen parameter set. |
| `hru(ihru)%hyd%lat_ttime` | For every HRU in the loop. | The lateral flow travel time is copied from the hydrology database into the HRU hydrology state. |
| `hru(ihru)%hyd%lat_sed` | For every HRU in the loop. | The lateral sediment concentration is copied from the hydrology database into the HRU hydrology state. |
| `hru(ihru)%topo%lat_len` | If the copied lateral length is smaller than `1.e-6`; otherwise it stays equal to the database value. | The HRU lateral slope length is forced to 50 m when the database value is effectively missing so later lateral-flow calculations have a stable nonzero length. |
| `hru(ihru)%hyd%canmx` | For every HRU in the loop. | The canopy maximum storage is copied from the hydrology database into the HRU hydrology state. |
| `hru(ihru)%hyd%esco` | For every HRU in the loop, before any tile-drain override. | The soil evaporation compensation factor is loaded from the hydrology database so the HRU uses the configured evaporation control. |
| `hru(ihru)%hyd%epco` | For every HRU in the loop. | The plant uptake compensation factor is loaded from the hydrology database so the HRU uses the configured transpiration control. |
| `hru(ihru)%hyd%erorgn` | For every HRU in the loop. | The organic nitrogen enrichment ratio is loaded from the hydrology database into the HRU hydrology state. |
| `hru(ihru)%hyd%erorgp` | For every HRU in the loop. | The organic phosphorus enrichment ratio is loaded from the hydrology database into the HRU hydrology state. |
| `hru(ihru)%hyd%cn3_swf` | For every HRU in the loop. | The curve-number soil-water adjustment factor is loaded from the hydrology database, then possibly overridden for tile drainage. |
| `hru(ihru)%hyd%perco` | For every HRU in the loop, then potentially transformed by the percolation-limit calculation. | The percolation coefficient is copied from the hydrology database, but may be replaced by a tile-drain default value when tile drainage is enabled. |
| `hru(ihru)%sno` | For every HRU in the loop after the snow database record is selected. | The full snow parameter structure is copied from `snodb(isno_db)` into the HRU so the model has the HRU's snow settings available during simulation. |
| `hru(ihru)%hyd%perco_lim` | If the HRU percolation coefficient is greater than `1.e-9`; otherwise it is reset to zero. | The percolation limit is derived from the percolation coefficient and capped at 1.0 so later logic can limit percolation consistently. |
| `hru(ihru)%topo%dis_stream` | For every HRU in the loop. | The average distance to stream is copied from the topography database to support routing and distance-sensitive processes. |
| `hru(ihru)%hyd%biomix` | For every HRU in the loop. | The biological mixing efficiency is copied from the hydrology database so annual soil mixing logic uses the configured value. |
| `hru(ihru)%hyd%lat_orgn` | For every HRU in the loop. | The lateral organic nitrogen concentration is copied from the hydrology database into the HRU hydrology state. |
| `hru(ihru)%hyd%lat_orgp` | For every HRU in the loop. | The lateral organic phosphorus concentration is copied from the hydrology database into the HRU hydrology state. |
| `hru(ihru)%hyd%latq_co` | For every HRU in the loop. | The lateral soil-flow coefficient is copied from the hydrology database into the HRU hydrology state. |
| `hru(ihru)%hyd%pet_co` | For every HRU in the loop, then adjusted by a compatibility check if the value is very small. | The PET coefficient is copied from the hydrology database and then normalized so old Hargreaves-style inputs or tiny values are handled consistently. |
| `hru(ihru)%field%length` | For every HRU in the loop. | The field length is copied from the field database so wind-erosion and field-geometry calculations have the HRU's field size. |

## File I/O

<!-- facts:io -->


## Theory Equations

| Eq. | Title | Formula | Implementation |
| --- | --- | --- | --- |
| 4:1.1.14 | Slope slp = tan(alpha_hill) | $slp=tan\alpha_{hill}$ | hru%topo%slope is read from topo database as fractional slope (tangent); plant_init:371 converts to sin via Sin(Atan(slope)) for the LS calculation. Definition equation only; slope loaded as a parameter. |

## Lineage

`topohyd_init.f90` was introduced in `df07e3f` (2024-03-05, "init all") and has been changed in 5 non-merge commit(s) since, most recently `bd18ad4` (2025-11-24, "Pr 107 (#108)"). Lineage is reconstructed from commit metadata (SHA, date, subject); per-line diffs were unavailable in this build environment, so only the commits touching `topohyd_init.f90` are listed.

- `bd18ad4` (2025-11-24) — Pr 107 (#108)
- `889136d` (2025-02-03) — Fix typos
- `39fabde` (2024-08-08) — Initialized varables with python script, corrected input data where integers where floats in two input files, trapped underflow errors in th…
- `94b6dec` (2024-05-30) — Added latest source code from bitbucket
- `df07e3f` (2024-03-05) — init all

## Review Notes

- No direct file I/O was extracted for this procedure.
- warning: missing_doc: Procedure 'topohyd_init' has no extracted documentation comment.
- soil_data_module and plant_module are imported but no resolved symbols from those modules appear in the extracted body.
- The source line for `iob = sp_ob1%hru + ihru - 1` is used to derive the matching object index; the overlay does not infer any additional object-mapping behavior beyond the visible assignment.
- No lineage commits were resolved for this procedure span.
- Lineage was reconstructed from file-level commit metadata; per-line diffs were unavailable in this environment (blobless clone), so line-span filtering was not applied.
