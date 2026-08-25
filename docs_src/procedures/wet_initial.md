---
kind: procedure
symbol: wet_initial
title: wet_initial
status: filled
source_hash: 27d17dc59672d68d
version_label: SWAT+ 62.0.0
args:
  iihru: HRU index for the wetland being initialized; it selects the `hru`, `wet_ob`, `wet_dat`,
    `wet_hyd`, `wet_prm`, `wet_water`, and related arrays to populate for that one HRU.
locals:
  iprop: Temporary pointer to the matched wetland database row; once `hru(iihru)%dbs%surf_stor`
    is resolved, `iprop` is used to index `wet_dat`, `wet_init`, and `wet_water`-related lookups.
  init_om: Holds the selected initial organic-mineral water database index from `wet_init(isp_ini)%org_min`
    so the routine can copy the matching initial water-quality template into `wet(iihru)`.
  init: Temporary index of the matched wetland initial-condition database entry from `wet_dat(iprop)%init`;
    it is then used to look up `wet_init(init)%org_min`.
  iweir: Stores the weir database index copied from `wet_ob(iihru)%iweir`, so the routine
    can pull weir height and width from `res_weir(iweir)` when available.
  icon: Temporary database selector for salt or constituent initialization; it is first set
    from `wet_dat(iprop)%salt` and then from `wet_dat(iprop)%cs`.
  isalt: Loop counter over salt ions when assigning initial salt concentrations and masses
    from `res_salt_data(icon)%c_init`.
  x1: Quadratic discriminant used to solve for updated wetland depth from volume and hydraulic
    coefficients when computing wetland surface area.
  wet_h: Computed wetland depth term used in the surface-area update formula after solving
    the quadratic relation for storage depth.
  wet_h1: Intermediate root of the quadratic depth equation before adding the hydraulic coefficient
    offset to obtain `wet_h`.
  wet_fr: Fractional wetland area factor derived from hydraulic coefficients and depth; it
    is capped at 1.0 before being applied to HRU area.
  ihyd: Loop counter over wetland hydrology database entries when matching `wet_dat_c(isstor)%hyd`
    to `wet_hyddb(ihyd)%name`.
  irel: Loop counter over decision-table release definitions when matching `wet_dat_c(isstor)%release`
    to `dtbl_res(irel)%name`.
  ised: Loop counter over sediment parameter database entries when matching the wetland sediment
    name and copying `res_sed(ised)` into `wet_prm(iihru)%sed`.
  inut: Loop counter over nutrient parameter database entries when matching the wetland nutrient
    name and copying `res_nut(inut)` into `wet_prm(iihru)%nut`.
  isp_ini: Loop counter over wetland initial-condition definitions; it matches `wet_dat_c(isstor)%init`
    to `res_init_dat_c(isp_ini)%init`.
  ics: Generic loop counter reused to search the initial organic-mineral, pesticide, and pathogen
    name tables while translating text names to database indices.
  isstor: Loop counter over wetland database rows used to find the wetland record whose name
    matches the HRU’s `surf_stor` pointer.
uses:
  reservoir_module: The `wet_ob` wetland object is the per-HRU target for geometry inputs
    such as weir ID, principal and emergency storage volumes, and spillway dimensions. `wet_initial`
    reads and updates those fields to establish starting wetland storage geometry before later
    wetland routing uses them.
  reservoir_data_module: The wetland database character table supplies the textual pointers
    that identify which initial-condition, hydrology, release, sediment, and nutrient records
    belong to this HRU. `wet_initial` crosswalks those names to numeric indices so the rest
    of the model can use fast array lookups.
  hydrograph_module: The hydrograph module provides the `wet` water-quality/output object
    whose flow volume is converted from a fraction of principal storage to an absolute volume.
    `wet_initial` needs it to seed the wetland water state and to convert concentration-based
    masses consistently.
  hru_module: The HRU object supplies the wetland pointer, HRU area, and the fields that store
    resolved database indices for surface storage and wetland setup. `wet_initial` uses those
    values to decide whether the HRU has wetland storage and to write back the selected wetland
    database references.
  maximum_data_module: The maximum-data module gives the loop bounds for every wetland-related
    database table. `wet_initial` depends on those limits to search the available initial-condition,
    hydrology, sediment, nutrient, and weir databases safely.
  water_body_module: The water-body state holds the daily wetland surface area used by downstream
    water-balance and area-dependent calculations. `wet_initial` resets and recomputes `wet_wat_d(iihru)%area_ha`
    from the initialized wetland volume and hydraulic geometry.
  soil_module: The soil-related module is used here because the wetland sediment and nutrient
    parameter sets are pulled from shared reservoir/soil-style parameter tables and then copied
    into wetland-specific parameter storage. Those parameters control settling and constituent
    behavior once the wetland is active.
  conditional_module: The decision-table module is needed because the wetland release rule
    is stored as a named decision table. `wet_initial` translates the text release name into
    the numeric decision-table index used by the release logic later on.
  constituent_mass_module: The constituent-mass module provides the counters and storage arrays
    for salts and other dissolved constituents in wetland water. `wet_initial` uses those
    counts to decide whether to initialize salt and constituent concentrations and masses,
    and it fills `wet_water(iihru)` accordingly.
  res_salt_module: The salt module contains the per-wetland salt initial-concentration database.
    `wet_initial` reads `res_salt_data(icon)%c_init` so it can assign initial salt concentrations
    and convert them to masses.
  res_cs_module: The constituent-species module contains the initial concentrations for the
    additional wetland constituents modeled here. `wet_initial` copies those species concentrations
    into `wet_water(iihru)` and converts them to masses.
---

<!-- facts:header -->

Initializes wetland/water-body state for one HRU by crosswalking its wetland database references to numeric indices and setting starting hydrologic, sediment, nutrient, salt, and constituent values.

## Bottom Line

`wet_initial` prepares the per-HRU wetland state that later wetland routing and update routines rely on. It resolves the HRU’s wetland database pointers, loads the selected initial-condition, hydrology, release, sediment, and nutrient definitions, and computes starting storage geometry and water quality values.

The routine also converts the chosen initial water-quality concentrations into masses using the initial wetland volume, and it derives a wetland surface area for the day from the hydraulic geometry. That makes the wetland object consistent before subsequent model steps use it for routing and mass balances.

## Arguments

<!-- facts:arguments -->

## Where It Fits

This routine runs after upstream code has already assigned the HRU’s surface-storage name or wetland pointer, as in `actions` and `wet_all_initial`. It is the one-time wetland setup step that resolves database names to indices and seeds starting state before later hydrology, constituent transport, and wetland-area calculations depend on those values.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. Read the weir pointer and confirm the HRU has wetland storage | The routine first copies the HRU's weir database index from `wet_ob(iihru)%iweir`, then checks whether the HRU's surface-storage name is anything other than `"null"`. That gate prevents wetland initialization unless the HRU is configured to use wetland storage. |
| 2. Crosswalk the wetland database row | It loops through `wet_dat` until it finds a row whose name matches the HRU's surface-storage name. When it finds the match, it stores the numeric index in `hru(iihru)%dbs%surf_stor`, mirrors that index into `iprop` and `hru(iihru)%wet_db`, and uses that row for the rest of the initialization. |
| 3. Resolve initial-condition tables | The routine finds the initial-condition definition whose name matches the wetland row, stores its index in `wet_dat(isstor)%init`, and crosswalks the initial organic-mineral, pesticide, and pathogen names to numeric IDs in `wet_init(isp_ini)%org_min`, `wet_init(isp_ini)%pest`, and `wet_init(isp_ini)%path`. |
| 4. Resolve hydrology and release definitions | It matches the wetland hydrology name to `wet_hyddb(ihyd)%name`, copies that hydrology record into `wet_hyd(iihru)`, stores the hydrology index in `wet_dat(isstor)%hyd`, and similarly crosswalks the release decision table name to `dtbl_res(irel)%name` and stores the release index in `wet_dat(isstor)%release`. |
| 5. Resolve sediment and nutrient parameters | The routine matches the wetland sediment and nutrient names against `res_sed` and `res_nut`, copies the selected records into `wet_prm(iihru)%sed` and `wet_prm(iihru)%nut`, stores the chosen indices in `wet_dat(isstor)%sed` and `wet_dat(isstor)%nut`, and sets sediment settling and soluble fraction defaults when sediment data are found. |
| 6. Report unresolved database references | If any of the wetland initial-condition, hydrology, release, sediment, or nutrient indices remain zero, the routine writes a message to unit 9001 identifying the missing wetland database reference. It also warns if the HRU's surface-storage name never matched a wetland row. |
| 7. Set hydraulic and spillway geometry | The routine assigns the HRU wetland hydraulic conductivity and computes principal and emergency storage geometry from HRU area and hydraulic depths. If a weir database is available, it uses `res_weir(iweir)` to set weir height and width and recomputes principal volume; otherwise it uses the hydrology-based principal depth and a default width. |
| 8. Seed the wetland water template and convert it to mass | It selects the initial water-quality template from `wet_dat(iprop)%init`, finds the matching organic-mineral template, copies that template into `wet(iihru)`, and calls `res_convert_mass` to scale the template to the wetland principal volume. |
| 9. Initialize salt concentrations and masses | If salts are simulated, the routine uses the wetland salt database index to populate `wet_water(iihru)%saltc` and `wet_water(iihru)%salt` from `res_salt_data(icon)%c_init`; otherwise it zeroes the salt concentrations and masses. |
| 10. Initialize additional constituent concentrations and masses | If other constituents are simulated, the routine uses the wetland constituent database index to populate `wet_water(iihru)%csc` from `res_cs_data(icon)` and converts those concentrations to masses in `wet_water(iihru)%cs`; otherwise it zeroes the constituent fields. |
| 11. Save the wetland initial water state | The initialized water-state template is copied into `wet_om_init(iihru)` so the model retains the starting wetland water condition for later use. |
| 12. Recompute daily wetland surface area from current volume | The routine zeroes the daily wetland water-body area, then if the wetland contains water it solves a quadratic relation for depth, derives a fractional area term, caps that fraction at 1.0, and computes `wet_wat_d(iihru)%area_ha` from HRU area and the hydraulic surface-area coefficient. |

## Modules Used

<!-- facts:uses -->

| Module | State touched | Key components |
| --- | --- | --- |
| [sym:reservoir_module] | `wet_ob` | `wet_ob(iihru)%iweir, wet_ob(iihru)%evol, wet_ob(iihru)%pvol, wet_ob(iihru)%psa, wet_ob(iihru)%esa, wet_ob(iihru)%weir_hgt, wet_ob(iihru)%weir_wid` |
| [sym:reservoir_data_module] | `wet_dat_c` | `wet_dat_c(isstor)%name, wet_dat_c(isstor)%init, wet_dat_c(isstor)%hyd, wet_dat_c(isstor)%release, wet_dat_c(isstor)%sed, wet_dat_c(isstor)%nut` |
| [sym:reservoir_data_module] | `wet_init, res_init_dat_c, om_init_name, pest_init_name, path_init_name` | `wet_init(isp_ini)%org_min, wet_init(isp_ini)%pest, wet_init(isp_ini)%path, res_init_dat_c(isp_ini)%init, res_init_dat_c(isp_ini)%org_min, res_init_dat_c(isp_ini)%pest, res_init_dat_c(isp_ini)%path` |
| [sym:hydrograph_module] | `wet` | `wet(iihru)%flo` |
| [sym:hru_module] | `hru` | `hru(iihru)%dbsc%surf_stor, hru(iihru)%dbs%surf_stor, hru(iihru)%wet_db, hru(iihru)%wet_hc, hru(iihru)%area_ha` |
| [sym:maximum_data_module] | `db_mx` | `db_mx%wet_dat, db_mx%res_init, db_mx%om_water_init, db_mx%pestw_ini, db_mx%pathw_ini, db_mx%wet_hyd, db_mx%dtbl_res, db_mx%res_sed, db_mx%res_nut, db_mx%res_weir` |
| [sym:water_body_module] | `wet_wat_d` | `wet_wat_d(iihru)%area_ha` |
| [sym:soil_module] | `res_sed, res_nut, res_weir` | `res_sed(ised)%name, res_sed(ised)%d50, res_nut(inut)%name, res_weir(iweir)%h, res_weir(iweir)%w` |
| [sym:conditional_module] | `dtbl_res` | `dtbl_res(irel)%name` |
| [sym:constituent_mass_module] | `cs_db, wet_water` | `cs_db%num_salts, wet_water(iihru)%saltc(isalt), wet_water(iihru)%salt(isalt), cs_db%num_cs, wet_water(iihru)%csc(1), wet_water(iihru)%csc(2), wet_water(iihru)%csc(3), wet_water(iihru)%cs(1), wet_water(iihru)%cs(2), wet_water(iihru)%cs(3)` |
| [sym:res_salt_module] | `res_salt_data` | `res_salt_data(icon)%c_init(isalt)` |
| [sym:res_cs_module] | `res_cs_data` | `res_cs_data(icon)%c_seo4, res_cs_data(icon)%c_seo3, res_cs_data(icon)%c_born` |

## Local Variables

<!-- facts:locals -->

## State Changes

| Target | When | Meaning |
| --- | --- | --- |
| `hru(iihru)%dbs%surf_stor` | When `hru(iihru)%dbsc%surf_stor` is not `"null"` and matches a row in `wet_dat_c`. | Stores the matched wetland database index in `hru(iihru)%dbs%surf_stor` so the HRU points to the selected wetland record instead of just holding the text name. |
| `hru(iihru)%wet_db` | When the HRU wetland name matches a wetland database row. | Sets `hru(iihru)%wet_db` to the chosen wetland record index so later wetland logic can tell which database entry is active for this HRU. |
| `wet_dat(isstor)%init` | When the wetland database row's `init` name matches a row in `res_init_dat_c`. | Stores the numeric initial-condition pointer for this wetland so later initialization code knows which organic-mineral/pesticide/pathogen template belongs to the wetland. |
| `wet_init(isp_ini)%org_min` | When `res_init_dat_c(isp_ini)%org_min` matches one of the names in `om_init_name`. | Converts the organic-mineral initial-condition name into an index used to copy the correct initial water template. |
| `wet_init(isp_ini)%pest` | When `res_init_dat_c(isp_ini)%pest` matches one of the names in `pest_init_name`. | Converts the pesticide initial-condition name into the index of the selected pesticide initialization template. |
| `wet_init(isp_ini)%path` | When `res_init_dat_c(isp_ini)%path` matches one of the names in `path_init_name`. | Converts the pathogen initial-condition name into the index of the selected pathogen initialization template. |
| `wet_hyd(iihru)` | After the wetland hydrology name is matched and `wet_hyddb(ihyd)` is copied to the HRU. | Copies the full wetland hydrology record into `wet_hyd(iihru)` so the HRU uses the selected hydraulic coefficients, depths, and area fractions. |
| `wet_dat(isstor)%hyd` | When the wetland hydrology name match succeeds. | Stores the matched hydrology database index in `wet_dat(isstor)%hyd` for later reference and diagnostics. |
| `wet_dat(isstor)%release` | When the wetland release decision-table name matches `dtbl_res(irel)%name`. | Stores the matched release-table index in `wet_dat(isstor)%release` so the wetland release logic can reference the correct decision table later. |
| `wet_prm(iihru)%sed` | When `res_sed(ised)%name` matches the wetland sediment name. | Copies the selected sediment parameter set into `wet_prm(iihru)%sed` so wetland sediment behavior uses the database-defined parameters. |
| `wet_prm(iihru)%sed_stlr_co` | Immediately after matching the sediment database record. | Computes the sediment settling coefficient from the selected sediment median size and stores it for later sediment settling calculations. |
| `wet_dat(isstor)%sed` | When the sediment database row is matched. | Stores the matched sediment database index in `wet_dat(isstor)%sed` for later lookup and validation. |
| `wet_prm(iihru)%soln_stl_fr` | After a sediment record is found. | Sets the soluble nitrogen fraction to 0.2 for the wetland sediment initialization used here. |
| `wet_prm(iihru)%solp_stl_fr` | After a sediment record is found. | Sets the soluble phosphorus fraction to 0.2 for the wetland sediment initialization used here. |
| `wet_prm(iihru)%nut` | When `res_nut(inut)%name` matches the wetland nutrient name. | Copies the selected nutrient parameter set into `wet_prm(iihru)%nut` so the wetland uses the proper nutrient settings. |
| `wet_dat(isstor)%nut` | When the nutrient database row is matched. | Stores the matched nutrient database index in `wet_dat(isstor)%nut` for later reference and validation. |
| `hru(iihru)%wet_hc` | After the hydrology record is resolved. | Sets the wetland hydraulic conductivity used by the HRU from the selected hydrology record. |
| `wet_ob(iihru)%evol` | When the HRU area and hydrology depths are known, and especially if the weir option is active. | Sets the wetland emergency-storage volume from HRU area and emergency depth, then possibly increases it to at least 1.2 times the principal volume. |
| `wet_ob(iihru)%pvol` | When the HRU area and hydrology depths are known, and especially if the weir option is active. | Sets the principal-storage volume from HRU area and principal depth, or recalculates it from the selected weir height when a weir table is available. |
| `wet_ob(iihru)%psa` | After hydrology is initialized. | Sets the principal surface area from the hydrology record and HRU area, then uses it as part of the wetland geometry update. |
| `wet_ob(iihru)%esa` | After hydrology is initialized. | Sets the emergency surface area from the hydrology record and HRU area, giving the wetland its overflow geometry. |
| `wet_ob(iihru)%weir_hgt` | If a weir database exists and the wetland has a positive weir ID. | Copies the selected weir height from `res_weir(iweir)%h` into the wetland object so the principal storage depth reflects the real weir geometry. |
| `wet_ob(iihru)%weir_wid` | If a weir database exists and the wetland has a positive weir ID. | Copies the selected weir width from `res_weir(iweir)%w` into the wetland object so later discharge calculations use the correct opening width. |
| `wet(iihru)` | After the initial water template is selected and converted, and only when `wet(iihru)%flo` remains positive. | Holds the initialized wetland water-quality and flow state for this HRU, including the mass-scaled initial concentrations used by later wetland and hydrograph calculations. |

## File I/O

<!-- facts:io -->


## Lineage

`wet_initial.f90` was introduced in `df07e3f` (2024-03-05, "init all") and has been changed in 9 non-merge commit(s) since, most recently `645ac00` (2025-12-11, "merge rice paddy management code"). Lineage is reconstructed from commit metadata (SHA, date, subject); per-line diffs were unavailable in this build environment, so only the commits touching `wet_initial.f90` are listed.

- `645ac00` (2025-12-11) — merge rice paddy management code
- `50968d0` (2025-10-29) — Amended wetland initialisation: minor fixes
- `d997d32` (2025-02-06) — Set wet_prm(iihru)%soln_stl_fr and wet_prm(iihru)%solp_stl_fr to 0.2 in xwalk with sediment inputs.
- `fcf3891` (2024-12-23) — source code updates 12/12 changes to MUSLE C factor and some carbon updates
- `e18817a` (2024-10-08) — Refactor and enhance various modules and subroutines
- `df07e3f` (2024-03-05) — init all

## Review Notes

- No direct file I/O was extracted for this procedure.
- warning: missing_doc: Procedure 'wet_initial' has no extracted documentation comment.
- The source uses `use reservoir_data_module` twice; this appears to be redundant but is preserved in the evidence.
- Lineage was reconstructed from file-level commit metadata; per-line diffs were unavailable in this environment (blobless clone), so line-span filtering was not applied.
