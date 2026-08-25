---
kind: procedure
symbol: aqu_read_init_cs
title: aqu_read_init_cs
status: filled
source_hash: 1fc89689f11b3d3e
version_label: SWAT+ 62.0.0
locals:
  titldum: Temporary title/label line read from `initial.aqu_cs`; used to skip over non-data
    lines during the counting and loading passes.
  header: Temporary header line read from `initial.aqu_cs`; used to skip the file header before
    reading record data.
  eof: I/O status flag for `read` calls; it is tested to detect end-of-file and stop scanning
    or loading records.
  imax: Counts how many initialization records are in `initial.aqu_cs` and later controls
    allocation and loop bounds for `aqu_init_dat_c_cs`.
  i_exist: Logical flag set by `inquire` to tell whether `initial.aqu_cs` exists before attempting
    to open it.
  iaqu: Loop index over initialization records in `aqu_init_dat_c_cs` when reading the file
    and when loading each record.
  ictr: Loop index over constituent-initial-condition database entries in `cs_aqu_ini`.
  isp_ini: Loop index over aquifer initial crosswalk entries in `aqu_init_dat_c_cs` when matching
    aquifer names to initial file names.
  idat: Holds the aquifer object’s database property index from `ob(iob)%props`; assigned
    during per-aquifer setup.
  iaq: Loop index over aquifer objects being initialized, from 1 to `sp_ob%aqu`.
  iob: Maps the aquifer object index into the global object array `ob`; set from `sp_ob1%aqu
    + iaq - 1`.
  ipest: Loop index over pesticides within an aquifer when assigning initial pesticide mass.
  ipath: Loop index over pathogens within an aquifer when assigning initial pathogen mass.
  isalt: Loop index over salt ions or salt mineral fractions when assigning initial salt state.
  ics: General loop index over the various initial-condition lookup tables and constituent
    arrays.
  iaqdb: Aquifer database index derived from `ob(iob)%props` and used to look up aquifer-specific
    settings such as `aqu_ini`, `dep_bot`, and `spyld`.
  gw_volume: Computed groundwater volume for the aquifer object; used to convert concentration
    values into total aquifer mass.
  aqu_volume: Computed bulk aquifer material volume; used with bulk density to estimate aquifer
    mass for sorbed constituents.
  aqu_bd: Assumed aquifer bulk density constant used to convert aquifer material volume to
    mass.
  aqu_mass: Estimated total aquifer material mass used to convert sorbed concentration to
    sorbed mass.
  mass_sorbed: Temporary mass of sorbed constituent in the aquifer before converting to area-based
    units.
uses:
  basin_module: The routine uses the existence flag to decide whether `initial.aqu_cs` can
    be opened and processed at all, so this module matters for file-availability control.
  input_file_module: This module is the source of the configured input-file name being checked
    and read, so it anchors the file-specific setup for aquifer initial constituent data.
  maximum_data_module: These limits bound how many initial pesticide, pathogen, salt, and
    constituent entries are searched when matching the aquifer crosswalk names to the corresponding
    initial-condition tables.
  aquifer_module: These aquifer-state structures provide the object-level geometry and aquifer
    crosswalk fields needed to compute groundwater volume, select the right initial-condition
    record, and apply the resulting values back onto each aquifer object.
  aqu_pesticide_module: The pesticide initial concentrations come from the pesticide initial-condition
    table in this module, and those concentrations are converted into aquifer pesticide mass
    here.
  hydrograph_module: The routine needs the aquifer object count, the first aquifer object
    index, and each object’s properties and area to iterate over aquifers and convert concentrations
    into area-based masses.
  constituent_mass_module: This module owns the constituent-count metadata, aquifer constituent
    state arrays, and the initial-condition tables that supply the actual values written into
    `cs_aqu` for pesticides, pathogens, salts, and generic constituents.
---

<!-- facts:header -->

Reads the aquifer initial constituent setup file and uses it to populate initial pesticide, pathogen, salt, and constituent mass states for each aquifer object.

## Bottom Line

`aqu_read_init_cs` loads the aquifer constituent crosswalk file `initial.aqu_cs` and uses it to match each aquifer object to the correct initial pesticide, pathogen, salt, and constituent input tables. It is the setup routine that turns name-based initialization records into the numeric starting masses and concentrations stored in `cs_aqu`.

The routine matters because it seeds aquifer starting conditions before simulation time begins. It computes aquifer groundwater volume, aquifer material volume, and sorbed-mass conversions so later aquifer transport and mass-balance calculations have initial state in the shared aquifer constituent arrays.

## Arguments

<!-- facts:arguments -->

## Where It Fits

`aqu_read_init_cs` runs inside `proc_aqu` after the other aquifer-reading routines have prepared the aquifer and constituent databases. It uses the `initial.aqu_cs` crosswalk to seed per-aquifer pesticide, pathogen, salt, and constituent starting conditions that later aquifer simulation steps depend on.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. Check whether `initial.aqu_cs` exists and reset scan counters. | The routine clears `eof` and `imax`, then uses `inquire` on `initial.aqu_cs` to set `i_exist` and only enters the file-loading block when the file is present. |
| 2. Open the crosswalk file and count data records. | It opens unit 105 on `initial.aqu_cs`, reads the title and header lines, then loops through the remaining records and increments `imax` for each record until end-of-file. |
| 3. Allocate storage for the crosswalk records. | Once the number of records is known, it allocates `aqu_init_dat_c_cs(imax)` to hold every initialization-name mapping from the file. |
| 4. Rewind and read the crosswalk records into memory. | The routine rewinds unit 105, skips the title and header again, and reads each record into `aqu_init_dat_c_cs(iaqu)` so later matching can use the loaded names. |
| 5. Close the input file after loading. | It closes unit 105 once the crosswalk table has been read. |
| 6. Loop over each aquifer object and compute geometry-dependent quantities. | For every aquifer object, it gets the object and database indices, computes groundwater volume from storage and area, computes aquifer-material volume from area, depth, and specific yield, then assumes a bulk density of 2000 kg/m3 and converts volume to aquifer mass. |
| 7. Match aquifer names and initialize pesticide mass. | It searches the loaded crosswalk for the aquifer's `name` and then searches pesticide initialization names; when both match, it copies pesticide water concentrations from `pest_water_ini(ics)%water(ipest)` into `cs_aqu(iaq)%pest(ipest)` using the aquifer depth conversion. |
| 8. Match aquifer names and initialize pathogens. | It repeats the crosswalk match for pathogen initialization and copies soil pathogen values from `path_soil_ini(ics)%soil(ipath)` into `cs_aqu(iaq)%path(ipath)`. |
| 9. Initialize salt concentrations and salt masses when salts are simulated. | If `cs_db%num_salts > 0`, it matches the aquifer's salt crosswalk, copies dissolved salt concentrations into `cs_aqu(iaq)%saltc(isalt)`, converts them to mass in `cs_aqu(iaq)%salt(isalt)`, and stores mineral fractions in `cs_aqu(iaq)%salt_min(isalt)`. |
| 10. Initialize generic aquifer constituents when constituents are simulated. | If `cs_db%num_cs > 0`, it matches the aquifer's constituent crosswalk, copies dissolved concentrations into `cs_aqu(iaq)%csc(ics)`, converts them to mass in `cs_aqu(iaq)%cs(ics)`, copies sorbed concentrations into `cs_aqu(iaq)%csc_sorb(ics)`, and converts sorbed concentration to sorbed mass per area in `cs_aqu(iaq)%cs_sorb(ics)`. |
| 11. Finish after all aquifers are processed. | After the aquifer loop completes, the routine returns to its caller. |

## Modules Used

<!-- facts:uses -->

| Module | State touched | Key components |
| --- | --- | --- |
| [sym:basin_module] | `i_exist` | `i_exist` |
| [sym:input_file_module] | `initial.aqu_cs` | `initial.aqu_cs` |
| [sym:maximum_data_module] | `db_mx` | `db_mx%pestw_ini, db_mx%pathw_ini, db_mx%salt_gw_ini, db_mx%cs_ini` |
| [sym:aquifer_module] | `aqu_d, aqudb, aqu_dat, aqu_init_dat_c_cs` | `aqu_d(iaq)%stor, aqudb(iaqdb)%dep_bot, aqu_dat(iaq)%spyld, aqu_init_dat_c_cs(isp_ini)%name, aqudb(iaq)%aqu_ini, aqu_init_dat_c_cs(isp_ini)%pest, aqudb(iaq)%dep_bot, aqu_init_dat_c_cs(isp_ini)%path, aqu_init_dat_c_cs(iaq)%salt, aqu_init_dat_c_cs(iaq)%cs` |
| [sym:aqu_pesticide_module] | `pest_water_ini` | `pest_water_ini(ics)%water(ipest)` |
| [sym:hydrograph_module] | `sp_ob, sp_ob1, ob, aqu` | `sp_ob%aqu, sp_ob1%aqu, ob(iob)%props, ob(iob)%area_ha` |
| [sym:constituent_mass_module] | `cs_db, cs_aqu, pest_water_ini, path_soil_ini, salt_aqu_ini, cs_aqu_ini, pest_init_name, path_init_name` | `cs_db%num_pests, cs_aqu(iaq)%pest(ipest), pest_water_ini(ics)%water(ipest), cs_db%num_paths, cs_aqu(iaq)%path(ipath), path_soil_ini(ics)%soil(ipath), cs_db%num_salts, salt_aqu_ini(ics)%name, cs_aqu(iaq)%saltc(isalt), salt_aqu_ini(ics)%conc(isalt), cs_aqu(iaq)%salt(isalt), cs_aqu(iaq)%salt_min(isalt), salt_aqu_ini(ics)%frac(isalt), cs_db%num_cs, cs_aqu_ini(ictr)%name, cs_aqu(iaq)%csc(ics), cs_aqu_ini(ictr)%aqu(ics), cs_aqu(iaq)%cs(ics), cs_aqu(iaq)%csc_sorb(ics), cs_aqu_ini(ictr)%aqu, cs_aqu(iaq)%cs_sorb(ics)` |

## Local Variables

<!-- facts:locals -->

## State Changes

| Target | When | Meaning |
| --- | --- | --- |
| `cs_aqu(iaq)%pest(ipest)` | When an aquifer’s `aqu_ini` name matches an entry in `aqu_init_dat_c_cs` and that entry’s `pest` name matches `pest_init_name(ics)` | Sets `cs_aqu(iaq)%pest(ipest)` to the initial pesticide mass derived from `pest_water_ini(ics)%water(ipest)` and aquifer depth, so the aquifer starts with pesticide loading in mass-per-area units. |
| `cs_aqu(iaq)%path(ipath)` | When an aquifer’s `aqu_ini` name matches an entry in `aqu_init_dat_c_cs` and that entry’s `path` name matches `path_init_name(ics)` | Copies `path_soil_ini(ics)%soil(ipath)` into `cs_aqu(iaq)%path(ipath)`, seeding the aquifer with the initial pathogen values from the lookup table. |
| `cs_aqu(iaq)%saltc(isalt)` | When `cs_db%num_salts > 0` and `aqu_init_dat_c_cs(iaq)%salt` matches `salt_aqu_ini(ics)%name` | Writes salt ion concentrations into `cs_aqu(iaq)%saltc(isalt)` and converts them to total salt mass in `cs_aqu(iaq)%salt(isalt)` using groundwater volume. |
| `cs_aqu(iaq)%salt(isalt)` | When `cs_db%num_salts > 0` and `aqu_init_dat_c_cs(iaq)%salt` matches `salt_aqu_ini(ics)%name` | Stores the initial mineral-salt mass for the aquifer in `cs_aqu(iaq)%salt_min(isalt)` from the salt fraction table. |
| `cs_aqu(iaq)%salt_min(isalt)` | When `cs_db%num_cs > 0` and `aqu_init_dat_c_cs(iaq)%cs` matches `cs_aqu_ini(ictr)%name` | Sets dissolved constituent concentration in `cs_aqu(iaq)%csc(ics)` and total constituent mass in `cs_aqu(iaq)%cs(ics)` from the aquifer initial-condition table. |
| `cs_aqu(iaq)%csc(ics)` | When `cs_db%num_cs > 0` and `aqu_init_dat_c_cs(iaq)%cs` matches `cs_aqu_ini(ictr)%name` | Stores sorbed constituent concentration in `cs_aqu(iaq)%csc_sorb(ics)` and converts it to sorbed mass per area in `cs_aqu(iaq)%cs_sorb(ics)` using the estimated aquifer mass and object area. |
| `cs_aqu(iaq)%cs(ics)` | Within the constituent-matching block for each `ics` | The routine computes a temporary `mass_sorbed` value from sorbed concentration and aquifer mass before normalizing it by area into `cs_aqu(iaq)%cs_sorb(ics)`. |
| `cs_aqu(iaq)%csc_sorb(ics)` | When `cs_db%num_cs > 0` and `aqu_init_dat_c_cs(iaq)%cs == cs_aqu_ini(ictr)%name` for a given aquifer/constituent crosswalk match. | `cs_aqu(iaq)%csc_sorb(ics)` stores the sorbed constituent concentration loaded from the aquifer constituent initial-condition table. It changes here so the aquifer starts with the prescribed sorbed concentration for each simulated constituent. |
| `cs_aqu(iaq)%cs_sorb(ics)` | When `cs_db%num_cs > 0` and `aqu_init_dat_c_cs(iaq)%cs == cs_aqu_ini(ictr)%name` for a given aquifer/constituent crosswalk match. | `cs_aqu(iaq)%cs_sorb(ics)` stores the sorbed constituent mass per hectare computed from the loaded sorbed concentration, aquifer mass, and area. It changes here to seed the aquifer's initial sorbed-mass inventory for later transport and balance calculations. |

## File I/O

<!-- facts:io -->


## Lineage

Three resolved commits changed `aqu_read_init_cs`: df07e3f introduced the new subroutine and its file-reading/initialization logic; 16e54aa revised the pathogen section to nest the pathogen lookup inside the aquifer-name match loop; and 39fabde initialized the local scalar variables to zero/default values. bd18ad4 later removed unused local counters (`i`, `init`, `idb`, `ini`, `init_aqu`) and cleaned the end-of-subroutine formatting without changing the routine’s logic.

- df07e3f added the entire `aqu_read_init_cs` routine, including the `initial.aqu_cs` scan/allocate/rewind/read workflow and the aquifer initialization loops for pesticides, pathogens, salts, and other constituents.
- 16e54aa changed pathogen initialization to require the aquifer-name crosswalk match before selecting `path_soil_ini`, so pathogen seeding now follows the same aquifer-level name matching used for pesticides.
- 39fabde initialized the routine's local scalars to safe defaults before file processing begins, reducing dependence on uninitialized values during file counting and state setup.
- bd18ad4 removed unused local counters from the declaration block without changing the file-reading or aquifer-initialization logic.

## Review Notes

- Direct file I/O exists; verify file meanings and units before finalizing.
- warning: missing_doc: Procedure 'aqu_read_init_cs' has no extracted documentation comment.
