---
kind: procedure
symbol: dr_read_salt
title: dr_read_salt
status: filled
source_hash: 6c91b11cfda870b9
version_label: SWAT+ 62.0.0
locals:
  titldum: Temporary line buffer used to read and skip title/header or record-name lines from
    `dr_salt.del` before the actual data row is parsed.
  header: Temporary line buffer used to capture the second header line in `dr_salt.del` during
    the file scan and reload passes.
  eof: I/O status flag for `read` statements; it is tested for end-of-file or read failure
    to stop scanning and loading the input file.
  imax: Counts how many salt delivery-ratio records are present in `dr_salt.del`; this determines
    allocation sizes for the salt tables and name/index arrays.
  ob1: First sequential object index for the delivery-ratio object range, taken from `sp_ob1%dr`
    before copying salt fractions into object hydrographs.
  ob2: Last sequential object index for the delivery-ratio object range, computed from `sp_ob1%dr
    + sp_ob%dr - 1` to bound the hydrograph update loop.
  i_exist: Logical flag from `inquire` indicating whether the configured salt-delivery file
    is present on disk.
  idr_salt: Loop index over salt delivery-ratio records while allocating tables, building
    the delivery-ratio crosswalk, and looking up the matching salt set.
  ii: Loop index used when rereading `dr_salt.del` to load each salt-set name and its salt
    fraction vector into memory.
  isalt: Inner loop index over the salt constituents in a record; it walks from 1 to `cs_db%num_salts`
    while reading the fraction list.
  idr: Loop index over delivery-ratio database entries in `dr_db`; it is used to match each
    DR file’s `salts_file` against the loaded salt-set names.
  iob: Loop index over spatial delivery-ratio objects; it is used to locate each object’s
    properties record and assign the corresponding salt hydrograph values.
uses:
  hydrograph_module: '`hydrograph_module` provides the spatial object counters and connectivity
    needed to know which delivery-ratio objects exist (`sp_ob1%dr`, `sp_ob%dr`), and `ob(iob)%props`
    gives the properties-table index that selects the correct salt delivery record for each
    object. `hd` is the destination hydrograph storage that receives the salt fractions.'
  dr_module: '`dr_module` holds the delivery-ratio database entries and the per-constituent
    lookup arrays. `dr_db(idr)%salts_file` is the file-name key that must be matched to the
    loaded salt-set names, and `dr_salt_num`/`dr_salt_name` store the crosswalk results used
    later in the object update.'
  input_file_module: '`input_file_module` supplies `in_delr%salt`, the configured path for
    the salt delivery-ratio input file. This is the file that `dr_read_salt` opens, scans,
    rewinds, and closes.'
  organic_mineral_mass_module: '`organic_mineral_mass_module` is listed in the routine’s uses
    list, but no candidate outside references from that module were resolved in the extracted
    source. It may be included for shared constituent/mass definitions or module-wide context
    even though no direct symbol use was captured here.'
  constituent_mass_module: '`constituent_mass_module` defines the salt-delivery storage and
    the number of salt constituents. `dr_salt(idr_salt)%salt` holds each loaded salt fraction
    vector, `cs_db%num_salts` tells the reader how many values to read per record, and `obcs(iob)%hd(1)%salt`
    is where those values are copied for each spatial object.'
  maximum_data_module: '`maximum_data_module` stores file-size counters. `db_mx%dr_salt` is
    set to the number of salt delivery records found in the file, and `db_mx%dr` is used later
    to loop across all delivery-ratio database entries when building the crosswalk.'
---

<!-- facts:header -->

Reads the salt delivery-ratio database file, counts and loads its records, then maps each delivery-ratio definition to the matching salt set and copies those salt fractions into object hydrographs.

## Bottom Line

`dr_read_salt` is the salt-specific delivery-ratio reader. It opens the file named by `in_delr%salt`, counts the data rows, allocates storage for the salt delivery-ratio table, and then reads each salt set name plus its salt fractions into `dr_salt` and `dr_salt_name`.

After loading the table, the routine crosswalks `dr_db(idr)%salts_file` to the loaded salt-set names so each delivery-ratio entry gets a sequential salt index in `dr_salt_num`. It then uses each object’s `props` value to copy the chosen salt fractions into `obcs(iob)%hd(1)%salt`, which is the hydrograph state later used for salt transport.

## Arguments

<!-- facts:arguments -->

## Where It Fits

This routine runs during delivery-ratio database initialization, after `dr_db_read` has already loaded the other constituent-type tables and confirmed that salts are enabled (`cs_db%num_salts > 0`). Its results are used immediately to map each delivery-ratio entry to a salt-set index and to populate the salt hydrographs attached to spatial delivery-ratio objects.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. Check whether the salt file should be read | The routine probes `in_delr%salt` with `inquire` and only enters the reader if the file exists or the configured name is not the sentinel value `"null"`. |
| 2. Open and scan the file to count data rows | It opens unit 107 on the salt file, reads and skips the title and header lines, then loops through the remaining records with `read(...,iostat=eof)` to count how many salt delivery-ratio rows exist in `imax`. |
| 3. Store the discovered record count | The counted record total is written to `db_mx%dr_salt` so the rest of the model knows how many salt delivery-ratio definitions were loaded. |
| 4. Allocate arrays for the salt database | The routine allocates `dr_salt`, allocates each `dr_salt(idr_salt)%salt` vector to length `cs_db%num_salts`, and creates the parallel `dr_salt_num` and `dr_salt_name` arrays needed for cross-referencing. |
| 5. Rewind and reread the file from the top | After allocation, it rewinds unit 107 and rereads the title and header lines so the file pointer is positioned at the first data row. |
| 6. Load each salt-set record | For each loaded record, it peeks with a read, backs up one record, then reads the salt-set name plus `cs_db%num_salts` salt fractions into `dr_salt_name(ii)` and `dr_salt(ii)%salt`. |
| 7. Close the salt input file | Once all salt records are loaded, unit 107 is closed and the file-loading loop is exited. |
| 8. Match delivery-ratio entries to salt-set names | The routine loops over `db_mx%dr` delivery-ratio definitions and finds the matching salt-set name in `dr_salt_name`; when a match is found, it stores the salt-set index in `dr_salt_num(idr)`. |
| 9. Copy salt fractions into object hydrographs | Using the object range defined by `sp_ob1%dr` and `sp_ob%dr`, the routine looks up each object’s property number, converts it through `dr_salt_num`, and assigns the matching `dr_salt(... )%salt` vector to `obcs(iob)%hd(1)%salt`. |
| 10. Return to the caller | The subroutine exits after the salt delivery-ratio data and object hydrographs have been updated. |

## Modules Used

<!-- facts:uses -->

| Module | State touched | Key components |
| --- | --- | --- |
| [sym:hydrograph_module] | `sp_ob1, sp_ob, ob, hd` | `sp_ob1%dr, sp_ob%dr, ob(iob)%props` |
| [sym:dr_module] | `dr_db, dr_salt_num, dr_salt_name` | `dr_db(idr)%salts_file` |
| [sym:input_file_module] | `in_delr` | `in_delr%salt` |
| [sym:organic_mineral_mass_module] | `dr_salt, cs_db, obcs` | `dr_salt(idr_salt)%salt, cs_db%num_salts, obcs(iob)%hd(1)%salt` |
| [sym:constituent_mass_module] | `dr_salt, cs_db, obcs` | `dr_salt(idr_salt)%salt, cs_db%num_salts, obcs(iob)%hd(1)%salt` |
| [sym:maximum_data_module] | `db_mx` | `db_mx%dr_salt, db_mx%dr` |

## Local Variables

<!-- facts:locals -->

## State Changes

| Target | When | Meaning |
| --- | --- | --- |
| `db_mx%dr_salt` | When `in_delr%salt` is available and the file scan completes, `imax` is assigned to `db_mx%dr_salt`. | This records how many salt delivery-ratio definitions were found in the input file so later loops and allocations use the correct size. |
| `dr_salt_num(idr)` | When a `dr_db(idr)%salts_file` value matches one of the loaded `dr_salt_name` entries, `dr_salt_num(idr)` is set to that matching index. | This creates a fast lookup from a delivery-ratio database entry to the corresponding salt delivery table row. |
| `obcs(iob)%hd(1)%salt` | When the object loop runs for each delivery-ratio object between `ob1` and `ob2`, `obcs(iob)%hd(1)%salt` is assigned from the matched `dr_salt(idr_salt)%salt` vector. | This loads each object’s salt hydrograph with the delivery-ratio salt fractions selected through the object’s properties record. |

## File I/O

<!-- facts:io -->


## Lineage

Three resolved commits changed `dr_read_salt`. The initial addition in df07e3f introduced the subroutine with file scanning, allocation, crosswalk, and hydrograph assignment logic. Commit f8bb6ec changed the salt-vector allocation so each `dr_salt(idr_salt)%salt` array is initialized with `source = 0.`. Commit 39fabde initialized local scalars/strings with default values and changed `dr_salt_num` allocation to `source = 0`.

- df07e3f added the full `dr_read_salt` subroutine, including the `inquire`/`open`/`read` scan of `in_delr%salt`, allocation of `dr_salt`, the `dr_db` to `dr_salt_name` crosswalk, and the assignment into `obcs(iob)%hd(1)%salt`.
- f8bb6ec changed the `dr_salt(idr_salt)%salt` allocation so each salt vector is zero-initialized at allocation time.
- 39fabde initialized `titldum`, `header`, `eof`, `imax`, `ob1`, `ob2`, `idr_salt`, `ii`, `isalt`, `idr`, and `iob`, and zero-initialized `dr_salt_num` during allocation.

## Review Notes

- Direct file I/O exists; verify file meanings and units before finalizing.
- warning: missing_doc: Procedure 'dr_read_salt' has no extracted documentation comment.
- algorithm_steps revised: condensed the scan/read sequence into distinct counting, allocation, reload, and population steps to match the visible source line flow.
- organic_mineral_mass_module is listed in the uses clause, but no resolved outside-state symbols from that module were captured in the extracted evidence.
