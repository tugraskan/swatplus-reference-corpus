---
kind: procedure
symbol: res_read
title: res_read
status: filled
source_hash: 39a8e3a5056ed3cb
version_label: SWAT+ 62.0.0
locals:
  i: Loop counter used while scanning the input file and while iterating reservoir records.
  titldum: Temporary title line read from `reservoir.res` before the header and data rows
    are processed.
  header: Temporary header line read from `reservoir.res` after the title line.
  eof: '`iostat` status flag used to detect end-of-file or read errors while scanning and
    rereading `reservoir.res`.'
  imax: Counts how many reservoir data records are present so the routine can allocate `res_dat_c`
    and `res_dat` to the right size.
  i_exist: Logical flag from `inquire` indicating whether the configured reservoir input file
    exists.
  ires: Reservoir object index used to load and map one reservoir definition at a time.
  k: Leading record code or sequence token read ahead of each reservoir row before the full
    derived-type read.
  ihyd: Index used to search `res_hyddb` for the hydrology definition named in the input row.
  irel: Index used to search either `ctbl` or `dtbl_res` for the release table named in the
    input row.
  ised: Index used to search `res_sed` for the sediment definition named in the input row.
  inut: Index used to search `res_nut` for the nutrient definition named in the input row.
  isp_ini: Index used to search the reservoir initial-condition tables for the initial setup
    named in the input row.
  ics: General-purpose string-table index used to resolve initial organic-mineral, pesticide,
    and pathogen names against their lookup-name arrays.
uses:
  basin_module: '`basin_module` is used as a shared model-state dependency even though no
    specific symbol was resolved in the extracted references; it is part of the reservoir
    setup environment that this routine runs within.'
  input_file_module: '`input_file_module` provides `in_res%res`, the configured filename for
    the reservoir input deck. `res_read` uses that shared setting to decide which file to
    open.'
  maximum_data_module: '`maximum_data_module` supplies the `db_mx` counters that control allocation
    bounds and loop limits for every reservoir-related table loaded here, so the routine can
    size and iterate over the available inputs correctly.'
  reservoir_data_module: '`reservoir_data_module` holds both the raw character inputs and
    the resolved numeric/typed reservoir records. `res_read` fills these structures so later
    reservoir routines can work with indexes and parameter objects instead of names.'
  conditional_module: '`conditional_module` supplies the decision-table registry used when
    a reservoir release definition refers to a conditional release table. `res_read` matches
    the name to `dtbl_res` and records the table index.'
  hydrograph_module: '`hydrograph_module` provides the reservoir object count `sp_ob%res`
    that bounds the main per-reservoir loop, plus the shared reservoir hydrograph output storage
    that other reservoir routines expect to be populated from these definitions.'
  constituent_mass_module: '`constituent_mass_module` provides the name arrays used to translate
    reservoir initial-condition labels for pesticides and pathogens into the integer positions
    stored in `res_init`. That mapping is required before mass-state initialization can proceed.'
  reservoir_module: '`reservoir_module` owns the per-reservoir object records. `res_read`
    updates `res_ob(ires)%rel_tbl` so downstream reservoir behavior knows whether a release
    definition uses a decision table or a conditions table.'
  pesticide_data_module: '`pesticide_data_module` is imported because reservoir initial-condition
    processing can include pesticide-related state, and the routine needs access to the shared
    pesticide data definitions used elsewhere in reservoir setup.'
  res_salt_module: '`res_salt_module` is imported because the reservoir input system is extended
    for salt handling, and this routine participates in the shared reservoir loading sequence
    that prepares those salt-related structures.'
  res_cs_module: '`res_cs_module` is imported because reservoir loading is also wired for
    constituent-specific state, so this routine runs with the shared carbon/constituent reservoir
    definitions available to the model.'
  reservoir_conditions_module: '`reservoir_conditions_module` provides the condition-table
    registry used when a release name begins with `ctbl_`. `res_read` uses `ctbl(irel)%name`
    to resolve the release table and mark the reservoir as using a conditions table.'
---

<!-- facts:header -->

Reads and resolves reservoir definitions from `reservoir.res` into the shared reservoir databases and object state. It scans the file to size allocations, then maps each reservoir's named subsettings to numeric indexes and lookup records used by later reservoir and salt/constituent routines.

## Bottom Line

`res_read` is the reservoir-input loader. It opens the configured `reservoir.res` file, counts records to size `res_dat_c` and `res_dat`, then rereads the file to populate each reservoir's character-based inputs and translate those names into module indexes and parameter records.

The routine matters because later reservoir processing depends on the resolved identifiers it stores: initial-condition references, hydrology setup, release-table mode, sediment parameters, and nutrient parameters. If a name is not found, it writes a message to unit 9001 so the model can flag missing reservoir configuration.

## Arguments

<!-- facts:arguments -->

## Where It Fits

`res_read` runs during reservoir processing in `proc_res`, after `res_allo` and `res_objects` have prepared reservoir storage and object counts. Its results feed later reservoir initialization and reservoir-handling routines, especially `res_read_salt_cs` and `res_initial`, which depend on the resolved reservoir definitions it stores.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. Check whether reservoir input is available | The routine tests whether the configured reservoir file exists and is not set to the literal `null`. If the file is missing or disabled, it allocates one-element placeholder arrays for `res_dat_c` and `res_dat` and skips file reading. |
| 2. Count reservoir records | The routine opens `reservoir.res`, reads past the title and header lines, then loops through the remaining records to increment `imax` for each reservoir entry encountered. |
| 3. Store the record count and allocate data arrays | After counting records, the routine copies `imax` into `db_mx%res_dat` and allocates `res_dat_c(0:imax)` and `res_dat(0:imax)` to hold the reservoir character inputs and resolved reservoir data. |
| 4. Rewind and reread the file header | The file is rewound so the same `reservoir.res` content can be reread from the beginning. The title and header lines are read again to position the file for per-record loading. |
| 5. Load each raw reservoir record | For each counted reservoir record, the routine reads the reservoir index, backs up one record, then reads the full row into `k` and `res_dat_c(ires)`. This converts each file row into the character-based reservoir input structure. |
| 6. Resolve initial-condition references | For each reservoir object, the routine matches the input `init` name against `res_init_dat_c`, stores the matching index in `res_dat(ires)%init`, and translates the organic-mineral, pesticide, and pathogen names to indexes in `res_init`. Missing matches are written to unit 9001. |
| 7. Resolve hydrology and release definitions | The routine matches the reservoir hydrology name against `res_hyddb`, copies the matching hydrology record into `res_hyd(ires)`, and stores its index in `res_dat(ires)%hyd`. It then resolves the release name against either `ctbl` or `dtbl_res`, sets `res_dat(ires)%release`, and marks `res_ob(ires)%rel_tbl` as conditions-table or decision-table driven. |
| 8. Resolve sediment and nutrient parameters | The routine matches sediment and nutrient names against `res_sed` and `res_nut`, copies the corresponding records into `res_prm(ires)`, stores the selected indexes in `res_dat(ires)%sed` and `res_dat(ires)%nut`, and computes the sediment settling coefficient plus default settling fractions. |
| 9. Report unresolved reservoir links | After matching the supporting records, the routine writes diagnostic messages for any reservoir hydrology, release, sediment, or nutrient entry that remained unresolved. |
| 10. Close the reservoir file | The routine closes unit 105 for `reservoir.res` once loading is complete, then exits the read loop and returns. |

## Modules Used

<!-- facts:uses -->

| Module | State touched | Key components |
| --- | --- | --- |
| [sym:basin_module] | `basin_module state/types imported into the procedure scope` |  |
| [sym:input_file_module] | `in_res` | `in_res%res` |
| [sym:maximum_data_module] | `db_mx` | `db_mx%res_dat, db_mx%res_init, db_mx%om_water_init, db_mx%pestw_ini, db_mx%pathw_ini, db_mx%res_hyd, db_mx%ctbl_res, db_mx%dtbl_res, db_mx%res_sed, db_mx%res_nut` |
| [sym:reservoir_data_module] | `res_dat_c, res_init_dat_c, res_dat, res_init, res_hyddb, res_sed, res_prm, res_nut, res_hyd` | `res_dat_c(ires)%init, res_init_dat_c(isp_ini)%init, res_dat(ires)%init, res_init_dat_c(isp_ini)%org_min, res_init(isp_ini)%org_min, res_init_dat_c(isp_ini)%pest, res_init(isp_ini)%pest, res_init_dat_c(isp_ini)%path, res_init(isp_ini)%path, res_hyddb(ihyd)%name, res_dat_c(ires)%hyd, res_dat(ires)%hyd, res_dat_c(ires)%release(1:5), res_dat_c(ires)%release, res_dat(ires)%release, res_sed(ised)%name, res_dat_c(ires)%sed, res_prm(ires)%sed, res_prm(ires)%sed_stlr_co, res_dat(ires)%sed, res_prm(ires)%soln_stl_fr, res_prm(ires)%solp_stl_fr, res_nut(inut)%name, res_dat_c(ires)%nut, res_prm(ires)%nut, res_dat(ires)%nut` |
| [sym:conditional_module] | `dtbl_res` | `dtbl_res(irel)%name` |
| [sym:hydrograph_module] | `sp_ob, om_init_name, res` | `sp_ob%res` |
| [sym:constituent_mass_module] | `pest_init_name, path_init_name` |  |
| [sym:reservoir_module] | `res_ob` | `res_ob(ires)%rel_tbl` |
| [sym:pesticide_data_module] | `pesticide_data_module state/types imported into the procedure scope` |  |
| [sym:res_salt_module] | `res_salt_module state/types imported into the procedure scope` |  |
| [sym:res_cs_module] | `res_cs_module state/types imported into the procedure scope` |  |
| [sym:reservoir_conditions_module] | `ctbl, release` | `ctbl(irel)%name` |

## Local Variables

<!-- facts:locals -->

## State Changes

| Target | When | Meaning |
| --- | --- | --- |
| `db_mx%res_dat` | When `reservoir.res` exists and is not the literal `null`, after the first pass counts the file records. | Stores the number of reservoir records found in the input file so later reservoir setup can size loops and allocations from the actual file content. |
| `res_dat(ires)%init` | For each reservoir object whose `init` name matches an entry in `res_init_dat_c`. | Stores the resolved index of the matching reservoir initial-condition definition for that reservoir object. |
| `res_init(isp_ini)%org_min` | For each matched initial-condition entry whose organic-mineral name matches `om_init_name(ics)`. | Stores the index of the matched organic-mineral initial-condition dataset used to initialize reservoir water contents. |
| `res_init(isp_ini)%pest` | For each matched initial-condition entry whose pesticide name matches `pest_init_name(ics)`. | Stores the index of the matched pesticide initial-condition dataset used for reservoir startup conditions. |
| `res_init(isp_ini)%path` | For each matched initial-condition entry whose pathogen name matches `path_init_name(ics)`. | Stores the index of the matched pathogen initial-condition dataset used for reservoir startup conditions. |
| `res_hyd(ires)` | For each reservoir whose hydrology name matches an entry in `res_hyddb`. | Copies the full hydrology definition record into the reservoir's working hydrology state so later simulation code can use the resolved parameters. |
| `res_dat(ires)%hyd` | For each reservoir whose hydrology name matches `res_hyddb(ihyd)%name`. | Stores the integer index of the matched hydrology definition for the reservoir. |
| `res_dat(ires)%release` | When the reservoir release field names a conditions table or decision table and a matching table name is found. | Stores the resolved release-table index so the reservoir can reference the correct outflow control table later. |
| `res_ob(ires)%rel_tbl` | When the release name begins with `ctbl_` and matches a conditions-table name. | Marks the reservoir object as using a conditions table for release control instead of a decision table. |
| `res_prm(ires)%sed` | When a reservoir sediment name matches an entry in `res_sed`. | Copies the selected sediment parameter record into the reservoir's working parameter set. |
| `res_prm(ires)%sed_stlr_co` | When a reservoir sediment name matches an entry in `res_sed`. | Computes the sediment settling coefficient from the matched sediment particle-size parameter and stores it for later reservoir sediment calculations. |
| `res_dat(ires)%sed` | When a reservoir sediment name matches an entry in `res_sed`. | Stores the index of the matched sediment definition for the reservoir. |
| `res_prm(ires)%soln_stl_fr` | When a reservoir sediment record is resolved and the code assigns default settling fractions. | Sets the soluble nitrogen settling fraction default for that reservoir sediment setup. |
| `res_prm(ires)%solp_stl_fr` | When a reservoir sediment record is resolved and the code assigns default settling fractions. | Sets the soluble phosphorus settling fraction default for that reservoir sediment setup. |
| `res_prm(ires)%nut` | When a reservoir nutrient name matches an entry in `res_nut`. | Copies the matched nutrient parameter record into the reservoir's working parameter set. |
| `res_dat(ires)%nut` | When a reservoir nutrient name matches an entry in `res_nut`. | Stores the index of the matched nutrient definition for the reservoir. |

## File I/O

<!-- facts:io -->


## Lineage

Resolved lineage commits show four behavior changes in `res_read`: 39fabde initialized the local counters and character buffers; e18817a added storage of the resolved hydrology, sediment, and nutrient indexes plus the sediment settling coefficient; b3da29c added default soluble nutrient settling fractions after sediment resolution; and 88ac4f1 changed the main reservoir loop to iterate over `sp_ob%res` instead of `db_mx%res_dat`.

- 39fabde made the scan counters and temporary strings start from known values, which reduces dependence on uninitialized locals when the file is read and counted.
- e18817a expanded the procedure from name matching only to also storing resolved hydrology, sediment, and nutrient indexes in `res_dat`, and to computing `res_prm(ires)%sed_stlr_co` from sediment particle size.
- b3da29c added fixed defaults for `res_prm(ires)%soln_stl_fr` and `res_prm(ires)%solp_stl_fr` when a sediment record is selected.
- 88ac4f1 changed the per-reservoir initialization loop to use the spatial reservoir count `sp_ob%res`, aligning reading with the actual number of reservoir objects.

## Review Notes

- Direct file I/O exists; verify file meanings and units before finalizing.
- warning: missing_doc: Procedure 'res_read' has no extracted documentation comment.
- algorithm_steps revised: condensed the draft into 10 source-backed steps and used only line ranges visible in the provided source block.
- Source indicates `basin_module`, `pesticide_data_module`, `res_salt_module`, and `res_cs_module` were imported, but no concrete candidate symbols were resolved for those modules in the extracted references.
