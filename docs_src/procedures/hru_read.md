---
kind: procedure
symbol: hru_read
title: hru_read
status: filled
source_hash: a401bad3265fdda4
version_label: SWAT+ 62.0.0
locals:
  titldum: Temporary title line read from `hru-data.hru` and then discarded/used only to skip
    the file's first header record.
  header: Temporary header line read from `hru-data.hru` and then discarded/used only to skip
    the file's second header record.
  eof: I/O status flag for reads from unit 113; values below zero end the scan or record loop
    at end-of-file.
  imax: Highest HRU index found while scanning the file; used to size `hru_db(0:imax)` before
    the detailed reread.
  i_exist: Logical flag from `inquire` that tells whether the configured HRU input file is
    present on disk.
  i: HRU record index read from the file and used as the target subscripting value for `hru_db(i)`.
  max: Unused local integer in this routine; declared but not referenced in the shown source.
  k: Dummy leading integer read with each HRU record before the derived-type data in `hru_db(i)%dbsc`.
  ilum: Loop counter for searching the land-use management database `lum` for a matching name.
  ith: Loop counter for searching `topo_db` for a matching topography name.
  ithyd: Loop counter for searching `hyd_db` for a matching hydrology name.
  isol: Loop counter for searching `soildb` for a matching soil series name.
  isno: Loop counter for searching `snodb` for a matching snow parameter set name.
  ifld: Loop counter for searching `field_db` for a matching field definition name.
  isp_ini: Loop counter for searching `sol_plt_ini` for a matching soil-plant initialization
    name.
  ics: Loop counter for searching the soil-test and constituent initialization tables for
    matching names.
uses:
  maximum_data_module: '`maximum_data_module` supplies the record-count limits for every database
    table `hru_read` searches. The routine uses `db_mx%landuse`, `db_mx%sol_plt_ini`, `db_mx%soiltest`,
    `db_mx%pest_ini`, `db_mx%path_ini`, `db_mx%hmet_ini`, `db_mx%salt_ini`, `db_mx%cs_ini`,
    `db_mx%topo`, `db_mx%hyd`, `db_mx%soil`, `db_mx%sno`, and `db_mx%field` as upper bounds
    for the lookup loops that convert names in the HRU file into numeric indices.'
  reservoir_data_module: '`reservoir_data_module` is listed as a use target by the source,
    but the extracted source shown for this procedure does not reference any reservoir symbols
    directly. Because no resolved outside references were provided for this module, its practical
    role here cannot be confirmed from the packet alone.'
  landuse_data_module: '`landuse_data_module` provides the `lum` table whose `name` field
    is compared against each HRU''s land-use management label. That lookup sets `hru_db(i)%dbs%land_use_mgt`,
    which later routines use as the resolved land-use-management pointer for the HRU.'
  hydrology_data_module: '`hydrology_data_module` provides `hyd_db`, the hydrology database
    searched by name for each HRU. `hru_read` uses it to translate the HRU''s hydrology label
    into `hru_db(i)%dbs%hyd` so downstream HRU initialization and flow routines can reference
    hydrology parameters by index.'
  topography_data_module: '`topography_data_module` supplies both `topo_db` and `field_db`,
    which are searched to resolve the HRU''s topography and field labels. Those lookups populate
    `hru_db(i)%dbs%topo` and `hru_db(i)%dbs%field`, letting later erosion, routing, and field-geometry
    logic use numeric table entries.'
  soil_data_module: '`soil_data_module` provides the soil-test table `solt_db` and soil profile
    database `soildb`. `hru_read` uses these tables to resolve the HRU''s soil-test initialization
    and soil series names into indices, and those indices are required before HRU soil and
    initialization state can be used downstream.'
  input_file_module: '`input_file_module` holds `in_hru%hru_data`, the configured path for
    the HRU input file. `hru_read` uses that setting to decide whether the file exists and
    what file name to open on unit 113.'
  hru_module: '`hru_module` contains the shared HRU database being filled here. Its character
    and integer subcomponents hold the raw names read from `hru-data.hru` and the resolved
    indices that later routines such as `hrudb_init`, `hru_lum_init_all`, and `topohyd_init`
    depend on.'
  constituent_mass_module: '`constituent_mass_module` provides the initial concentration tables
    used to map each HRU''s soil-plant initialization names to constituent indices. `hru_read`
    updates `sol_plt_ini(isp_ini)%nut`, `%pest`, `%path`, `%hmet`, `%salt`, and `%cs` from
    these tables so later initial-condition logic knows which constituent record applies.'
---

<!-- facts:header -->

Reads the HRU definition file, builds the HRU database array, and resolves each HRU's management, topology, hydrology, soil, snow, and field pointers into numeric indices.

## Bottom Line

`hru_read` is the setup routine that loads `hru-data.hru` into the shared `hru_db` array. It first scans the file to find the largest HRU index, allocates storage, then rereads each HRU record and matches its named references to the corresponding database tables in the model.

It also resolves the linked plant/constituent initialization names into indices in `sol_plt_ini` and the constituent initialization tables, so later HRU initialization routines can work with integer lookups instead of raw names. If a reference cannot be found, the routine writes a warning to unit 9001.

## Arguments

<!-- facts:arguments -->

## Where It Fits

`proc_hru` calls `hru_read` immediately after `hru_allo`, so this routine runs after the HRU container objects have been allocated but before HRU initialization, land-use initialization, and topography/hydrology setup. Its results feed the later `hrudb_init`, `hru_lum_init_all`, and `topohyd_init` steps that depend on resolved HRU database indices rather than raw names.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. Allocate shared parameter storage | Calls `allocate_parms` so shared model parameter arrays and related state are ready before the HRU file is processed. |
| 2. Check whether the HRU file is available | Uses `inquire` on `in_hru%hru_data` and, if the file is missing or set to `null`, allocates a minimal `hru_db(0:0)` and skips file loading. |
| 3. Open and scan the HRU file for the highest record index | Opens unit 113 on `in_hru%hru_data`, skips the title and header lines, reads HRU indices in a loop, and tracks the maximum index in `imax` before allocating `hru_db(0:imax)`. |
| 4. Rewind and reread the file header | Rewinds unit 113 and rereads the title and header lines so the detailed data pass starts at the beginning of the file. |
| 5. Load each HRU record into the shared database | Loops over HRU indices, backs up one record, and reads the raw HRU database record into `hru_db(i)%dbsc` after capturing the leading integer field in `k`. |
| 6. Resolve land-use management names | Searches `lum` for the matching management name and stores the matched position in `hru_db(i)%dbs%land_use_mgt`; writes a warning if no match is found. |
| 7. Resolve soil-plant initialization and constituent tables | Finds the matching `sol_plt_ini` entry for the HRU's plant initialization name and then resolves its nutrient, pesticide, pathogen, heavy-metal, salt, and constituent names to indices in the corresponding soil/constituent tables. |
| 8. Resolve topography, hydrology, soil, snow, and field names | Looks up the HRU's topography, hydrology, soil, snow, and field labels in their respective tables and stores the matching indices in `hru_db(i)%dbs`; writes warnings for missing non-null names. |
| 9. Close the HRU file | Closes unit 113 after the HRU file has been scanned and the shared state has been populated. |

## Modules Used

<!-- facts:uses -->

| Module | State touched | Key components |
| --- | --- | --- |
| [sym:maximum_data_module] | `db_mx` | `db_mx%landuse, db_mx%sol_plt_ini, db_mx%soiltest, db_mx%pest_ini, db_mx%path_ini, db_mx%hmet_ini, db_mx%salt_ini, db_mx%cs_ini, db_mx%topo, db_mx%hyd, db_mx%soil, db_mx%sno, db_mx%field` |
| [sym:reservoir_data_module] | `snodb` | `snodb(isno)%name` |
| [sym:landuse_data_module] | `lum` | `lum(ilum)%name` |
| [sym:hydrology_data_module] | `hyd_db` | `hyd_db(ithyd)%name` |
| [sym:topography_data_module] | `topo_db, field_db` | `topo_db(ith)%name, field_db(ifld)%name` |
| [sym:soil_data_module] | `solt_db, soildb` | `solt_db(ics)%name, soildb(isol)%s%snam` |
| [sym:input_file_module] | `in_hru` | `in_hru%hru_data` |
| [sym:hru_module] | `hru_db, sol_plt_ini, snodb, ihru` | `hru_db(i)%dbsc, hru_db(i)%dbsc%land_use_mgt, hru_db(i)%dbs%land_use_mgt, hru_db(i)%dbsc%soil_plant_init, sol_plt_ini(isp_ini)%name, hru_db(i)%dbs%soil_plant_init, sol_plt_ini(isp_ini)%nutc, sol_plt_ini(isp_ini)%nut, sol_plt_ini(isp_ini)%pestc, sol_plt_ini(isp_ini)%pest, sol_plt_ini(isp_ini)%pathc, sol_plt_ini(isp_ini)%path, sol_plt_ini(isp_ini)%hmetc, sol_plt_ini(isp_ini)%hmet, sol_plt_ini(isp_ini)%saltc, sol_plt_ini(isp_ini)%salt, sol_plt_ini(isp_ini)%csc, sol_plt_ini(isp_ini)%cs, hru_db(i)%dbsc%topo, hru_db(i)%dbs%topo, hru_db(i)%dbsc%hyd, hru_db(i)%dbs%hyd, hru_db(i)%dbsc%soil, hru_db(i)%dbs%soil, hru_db(i)%dbsc%snow, snodb(isno)%name, hru_db(i)%dbs%snow, hru_db(i)%dbsc%field, hru_db(i)%dbs%field` |
| [sym:constituent_mass_module] | `pest_soil_ini, path_soil_ini, hmet_soil_ini, salt_soil_ini, cs_soil_ini` | `pest_soil_ini(ics)%name, path_soil_ini(ics)%name, hmet_soil_ini(ics)%name, salt_soil_ini(ics)%name, cs_soil_ini(ics)%name` |

## Local Variables

<!-- facts:locals -->

## State Changes

| Target | When | Meaning |
| --- | --- | --- |
| `hru_db(i)%dbs%land_use_mgt` | When `hru_db(i)%dbsc%land_use_mgt` matches `lum(ilum)%name` during the land-use lookup loop. | Stores the resolved land-use management index in `hru_db(i)%dbs%land_use_mgt`, converting the raw name from the HRU file into the numeric reference used by later management and initialization routines. |
| `hru_db(i)%dbs%soil_plant_init` | When `hru_db(i)%dbsc%soil_plant_init` matches `sol_plt_ini(isp_ini)%name` during the plant-initialization lookup loop. | Sets `hru_db(i)%dbs%soil_plant_init` to the matching plant-initialization record so later HRU setup can use the correct initial soil/plant database entry. |
| `sol_plt_ini(isp_ini)%nut` | When `sol_plt_ini(isp_ini)%nutc` matches `solt_db(ics)%name`. | Stores the matching soil-test initialization index in `sol_plt_ini(isp_ini)%nut`, linking the plant initialization record to the correct soil nutrient starting conditions. |
| `sol_plt_ini(isp_ini)%pest` | When `sol_plt_ini(isp_ini)%pestc` matches `pest_soil_ini(ics)%name`. | Stores the matching pesticide initialization index in `sol_plt_ini(isp_ini)%pest`, linking the plant initialization record to the correct pesticide starting conditions. |
| `sol_plt_ini(isp_ini)%path` | When `sol_plt_ini(isp_ini)%pathc` matches `path_soil_ini(ics)%name`. | Stores the matching pathogen initialization index in `sol_plt_ini(isp_ini)%path`, linking the plant initialization record to the correct pathogen starting conditions. |
| `sol_plt_ini(isp_ini)%hmet` | When `sol_plt_ini(isp_ini)%hmetc` matches `hmet_soil_ini(ics)%name`. | Stores the matching heavy-metal initialization index in `sol_plt_ini(isp_ini)%hmet`, linking the plant initialization record to the correct heavy-metal starting conditions. |
| `sol_plt_ini(isp_ini)%salt` | When `sol_plt_ini(isp_ini)%saltc` matches `salt_soil_ini(ics)%name`. | Stores the matching salt initialization index in `sol_plt_ini(isp_ini)%salt`, linking the plant initialization record to the correct salt starting conditions. |
| `sol_plt_ini(isp_ini)%cs` | When `sol_plt_ini(isp_ini)%csc` matches `cs_soil_ini(ics)%name`. | Stores the matching constituent initialization index in `sol_plt_ini(isp_ini)%cs`, linking the plant initialization record to the correct generic constituent starting conditions. |
| `hru_db(i)%dbs%topo` | When `hru_db(i)%dbsc%topo` matches `topo_db(ith)%name`. | Sets `hru_db(i)%dbs%topo` to the matched topography table index so later erosion and landscape calculations can use numeric topography parameters. |
| `hru_db(i)%dbs%hyd` | When `hru_db(i)%dbsc%hyd` matches `hyd_db(ithyd)%name`. | Sets `hru_db(i)%dbs%hyd` to the matched hydrology table index so later flow and routing calculations can use numeric hydrology parameters. |
| `hru_db(i)%dbs%soil` | When `hru_db(i)%dbsc%soil` matches `soildb(isol)%s%snam`. | Sets `hru_db(i)%dbs%soil` to the matched soil profile index so later soil initialization and process routines can retrieve the correct soil database record. |
| `hru_db(i)%dbs%snow` | When `hru_db(i)%dbsc%snow` matches `snodb(isno)%name`. | Sets `hru_db(i)%dbs%snow` to the matched snow parameter index so later snowpack initialization can use the correct snow database record. |
| `hru_db(i)%dbs%field` | When `hru_db(i)%dbsc%field` matches `field_db(ifld)%name`. | Sets `hru_db(i)%dbs%field` to the matched field parameter index so later field-geometry and erosion routines can use the correct field database record. |

## File I/O

<!-- facts:io -->


## Lineage

`hru_read.f90` was introduced in `df07e3f` (2024-03-05, "init all") and has been changed in 7 non-merge commit(s) since, most recently `bd18ad4` (2025-11-24, "Pr 107 (#108)"). Lineage is reconstructed from commit metadata (SHA, date, subject); per-line diffs were unavailable in this build environment, so only the commits touching `hru_read.f90` are listed.

- `bd18ad4` (2025-11-24) — Pr 107 (#108)
- `29e2d36` (2025-10-29) — Bug fixes and changes related to water allocation
- `1c812c1` (2025-08-21) — Refactor soil-plant initialization and pesticide calculations
- `e18817a` (2024-10-08) — Refactor and enhance various modules and subroutines
- `39fabde` (2024-08-08) — Initialized varables with python script, corrected input data where integers where floats in two input files, trapped underflow errors in th…
- `df07e3f` (2024-03-05) — init all

## Review Notes

- Direct file I/O exists; verify file meanings and units before finalizing.
- warning: missing_doc: Procedure 'hru_read' has no extracted documentation comment.
- algorithm_steps revised: condensed the draft into 9 source-backed steps that follow the actual open/scan/rewind/load/close flow.
- `reservoir_data_module` is listed in the USE statements, but no resolved source references for it appear in the packet; its specific role in this routine is uncertain from the evidence provided.
- Lineage was reconstructed from file-level commit metadata; per-line diffs were unavailable in this environment (blobless clone), so line-span filtering was not applied.
