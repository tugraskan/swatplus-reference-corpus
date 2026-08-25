---
kind: procedure
symbol: dr_read_om
title: dr_read_om
status: filled
source_hash: 12799e372d320411
version_label: SWAT+ 62.0.0
locals:
  titldum: Temporary text field used to read and discard title or record lines while scanning
    `dr_om.del`.
  header: Temporary header string read from `dr_om.del`; used to skip the file header before
    counting or loading data records.
  eof: I/O status flag for reads from unit 107; used to detect end-of-file and exit the scan/read
    loops.
  imax: Counts how many organic-matter delivery-ratio records are present in `dr_om.del`,
    and is later used to size arrays and set `db_mx%dr_om`.
  ob1: First spatial-object index for the delivery-ratio object block; set from `sp_ob1%dr`
    before assigning hydrographs.
  ob2: Last spatial-object index for the delivery-ratio object block; computed from `sp_ob1%dr
    + sp_ob%dr - 1`.
  i_exist: Logical result from `inquire` that tells whether the configured organic-matter
    delivery-ratio file exists on disk.
  ii: Loop index used to read each organic-matter record from `dr_om.del` after allocation.
  idr: Loop index over the main delivery-ratio database used to match each entry to an organic-matter
    record name.
  idr_om: Loop index over the organic-matter lookup table used to find the matching `dr_om_name`
    for each `dr_db(idr)%om_file`.
  iob: Loop index over the delivery-ratio spatial objects whose hydrograph slot is populated
    from the matched organic-matter record.
uses:
  dr_module: The `dr_module` arrays hold the organic-matter lookup names, the per-delivery-ratio
    mapping numbers, and the per-file metadata that this routine fills and later consults
    when matching `dr_db(idr)%om_file` to `dr_om_name(idr_om)`.
  constituent_mass_module: The `constituent_mass_module` matters because the routine stores
    the parsed organic-matter records into the shared `dr` constituent-mass delivery-ratio
    table, and that shared state is what later routines use when a delivery-ratio object needs
    its organic-matter hydrograph values.
  hydrograph_module: The `hydrograph_module` provides the delivery-ratio hydrograph arrays
    and object connectivity records that receive the final mapping. `sp_ob1%dr` and `sp_ob%dr`
    define the object range, `ob(iob)%props` selects which database entry to use, and `ob(iob)%hd(1)`
    is the hydrograph slot written here.
  input_file_module: The `input_file_module` provides `in_delr%om`, the configured path to
    the organic-matter delivery-ratio input file that this routine opens and reads.
  organic_mineral_mass_module: The `organic_mineral_mass_module` supplies the organic/mineral
    mass delivery-ratio state that is being loaded from `dr_om.del` and then assigned to object
    hydrographs.
  maximum_data_module: The `maximum_data_module` holds the maximum record counters used to
    size the lookup tables and drive later loops. `db_mx%dr_om` is set from the counted file
    records and `db_mx%dr` controls the cross-walk over the main delivery-ratio database.
---

<!-- facts:header -->

Reads the delivery-ratio organic-matter lookup file and maps those records onto delivery-ratio objects and hydrograph state.

## Bottom Line

dr_read_om loads the delivery-ratio organic-matter table from `dr_om.del`, first counting how many records it contains, then allocating storage and reading each name/value pair into module arrays. It also cross-walks those organic-matter names to the main delivery-ratio database so each delivery-ratio entry gets a sequential organic-matter index.

After the lookup table is loaded, the routine pushes the matched organic-matter hydrograph data onto the relevant spatial objects in `ob(:)%hd(1)`. That makes the delivery-ratio organic-matter settings available to later routing and constituent-mass behavior.

## Arguments

<!-- facts:arguments -->

## Where It Fits

This routine runs during delivery-ratio database setup, immediately after `dr_db_read` has finished preparing the delivery-ratio file metadata. Its results feed later delivery-ratio object setup, especially the object hydrograph values written into `ob(:)%hd(1)`.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. Check whether the organic-matter delivery-ratio file should be read | The routine inquires on `in_delr%om` and only proceeds when the file exists or the configured name is not `null`. |
| 2. Open and scan the file once to count data rows | It opens unit 107 on `in_delr%om`, skips the title and header lines, then reads through the remaining lines to count how many organic-matter records are present in `imax`. |
| 3. Save the record count and allocate storage | The counted size is stored in `db_mx%dr_om`, then arrays for `dr`, `dr_om_num`, and `dr_om_name` are allocated for indices `0:imax`. |
| 4. Rewind and reread the file for data loading | The file is rewound and the title/header lines are read again so the second pass starts at the first data record. |
| 5. Load each organic-matter record into shared state | For each record, the routine probes the line, backs up one record, and then reads the organic-matter name and the associated `dr` values into module arrays. |
| 6. Close the input file after loading completes | It closes unit 107 once the lookup table has been read successfully. |
| 7. Match main delivery-ratio records to organic-matter entries | The routine loops over each delivery-ratio database entry and finds the matching `dr_om_name` by comparing it to `dr_db(idr)%om_file`; when found, it stores the sequential lookup index in `dr_om_num(idr)`. |
| 8. Assign the matched hydrograph to each delivery-ratio object | Using the delivery-ratio object range from `sp_ob1%dr` to `sp_ob1%dr + sp_ob%dr - 1`, the routine looks up each object's property index, translates it through `dr_om_num`, and copies the corresponding `dr` hydrograph into `ob(iob)%hd(1)`. |
| 9. Return to the caller | The subroutine exits after all mappings and hydrograph assignments are complete. |

## Modules Used

<!-- facts:uses -->

| Module | State touched | Key components |
| --- | --- | --- |
| [sym:dr_module] | `dr_db, dr_om_num, dr_om_name` | `dr_db(idr)%om_file` |
| [sym:constituent_mass_module] | `dr, dr_db` | `dr(0:imax), dr(ii), dr(idr_om), dr_db(idr)` |
| [sym:hydrograph_module] | `sp_ob1, sp_ob, ob, dr, hd` | `sp_ob1%dr, sp_ob%dr, ob(iob)%props, ob(iob)%hd(1)` |
| [sym:input_file_module] | `in_delr` | `in_delr%om` |
| [sym:organic_mineral_mass_module] | `dr` | `dr(0:imax), dr(ii), dr(idr_om)` |
| [sym:maximum_data_module] | `db_mx` | `db_mx%dr_om, db_mx%dr` |

## Local Variables

<!-- facts:locals -->

## State Changes

| Target | When | Meaning |
| --- | --- | --- |
| `db_mx%dr_om` | When `dr_om.del` is present or the configured file name is not `null`, and the routine has counted the number of data records. | `db_mx%dr_om` is set to the number of organic-matter delivery-ratio records found in the input file so later loops know how many entries to read and match. |
| `dr_om_num(idr)` | During the cross-walk loop when `dr_db(idr)%om_file` exactly matches `dr_om_name(idr_om)`. | `dr_om_num(idr)` is updated to the sequential index of the matching organic-matter record so later code can translate each delivery-ratio database entry into the correct loaded `dr` data. |
| `ob(iob)%hd(1)` | Inside the object loop after `idr = ob(iob)%props` and `idr_om = dr_om_num(idr)` resolve to a valid loaded organic-matter record. | `ob(iob)%hd(1)` is assigned the matching delivery-ratio hydrograph record from `dr(idr_om)`, making the organic-matter response available on the spatial object. |

## File I/O

<!-- facts:io -->


## Lineage

Two resolved commits changed `dr_read_om`: `df07e3f` added the routine with the full file-scan, allocation, cross-walk, and hydrograph-population logic; `39fabde` made initialization and allocation cleanup changes by setting local scalars to default values and changing `dr_om_num` allocation to `source = 0`.

- df07e3f introduced `dr_read_om` and its data-loading workflow for `dr_om.del`, including counting records, allocating arrays, matching `dr_db(idr)%om_file` to `dr_om_name`, and copying hydrographs into `ob(iob)%hd(1)`.
- 39fabde initialized local scalars (`titldum`, `header`, `eof`, `imax`, `ob1`, `ob2`, `ii`, `idr`, `idr_om`, `iob`) and changed `allocate (dr_om_num(0:imax), source = 0)` so the lookup array starts with zero values.

## Review Notes

- Direct file I/O exists; verify file meanings and units before finalizing.
- warning: missing_doc: Procedure 'dr_read_om' has no extracted documentation comment.
