---
kind: procedure
symbol: exco_read_path
title: exco_read_path
status: filled
source_hash: c3f8daf9bd0ddea6
version_label: SWAT+ 62.0.0
locals:
  titldum: Scratch title/string buffer used to read and skip record lines while counting and
    then loading records from `exco_path.exc`.
  header: Scratch header/string buffer used to read and skip the second header line in `exco_path.exc`
    before scanning data rows.
  eof: I/O status flag for reads from unit 107; controls loop exit when the file reaches end-of-file
    or a read fails.
  imax: Counts how many export-coefficient path records are present in `exco_path.exc`; later
    used to size arrays and bound loops.
  ob1: First export-coefficient object index in the hydrograph object range, computed from
    `sp_ob1%exco`.
  ob2: Last export-coefficient object index in the hydrograph object range, computed from
    `sp_ob1%exco + sp_ob%exco - 1`.
  i_exist: Logical result from `inquire` that reports whether the configured path file exists
    on disk.
  iexco_path: Loop index over the read path definitions in `exco_path.exc` and later over
    the allocated path lookup arrays.
  ii: Loop index used during the second file pass to read each named path record into arrays.
  ipath: Loop index over constituent-path columns within a single path record.
  iexco: Loop index over export-coefficient database entries in `exco_db` while crosswalking
    file names to path indices and assigning hydrographs.
  iob: Loop index over export-coefficient object instances in `ob`/`obcs` when assigning the
    final hydrograph path arrays.
uses:
  hydrograph_module: '`hydrograph_module` supplies the spatial object bounds and object connectivity
    needed to find which export-coefficient objects should receive the loaded pathogen-path
    hydrograph, and it holds the target `ob(iob)%props` and `obcs(iob)%hd(1)%path` state that
    this routine updates.'
  input_file_module: '`input_file_module` provides `in_exco%path`, the configured filename
    for the export-coefficient path input; without it, the routine would not know which file
    to open.'
  organic_mineral_mass_module: '`organic_mineral_mass_module` is imported here because this
    procedure operates in the export-coefficient reading sequence that is coordinated with
    the other constituent modules; its inclusion ensures the shared constituent-mass infrastructure
    is available even though no candidate state from this module is directly referenced in
    the extracted source.'
  constituent_mass_module: '`constituent_mass_module` owns the pathogen-path arrays and constituent
    counts that determine how many values are read per record and where the per-path hydrograph
    is stored, so it is central to building and applying the path lookup tables.'
  exco_module: '`exco_module` owns the export-coefficient file list and the path-name crosswalk
    arrays; this routine fills `exco_path_name`/`exco_path_num` so later code can match each
    export-coefficient definition to the correct path record.'
  maximum_data_module: '`maximum_data_module` holds `db_mx`, which stores the discovered count
    of path records and the number of export-coefficient files; this routine updates those
    maxima so later loops know the available sizes.'
---

<!-- facts:header -->

Reads export-coefficient pathogen path data from exco_path.exc, builds the in-memory path lookup tables, and attaches the resulting hydrograph paths to export-coefficient objects.

## Bottom Line

`exco_read_path` loads the pathogen-path section of the export-coefficient database. It counts the data rows in `in_exco%path`, allocates `exco_path`, `exco_path_num`, and `exco_path_name`, then rereads the file to store each path name and its constituent-path values.

After the lookup tables are built, the routine crosswalks `exco_db(iexco)%path_file` to the sequential path index and copies the matching `exco_path(... )%path` array into `obcs(iob)%hd(1)%path` for each export-coefficient object. That makes the configured pathogen path hydrographs available to later routing and mass-balance logic.

## Arguments

<!-- facts:arguments -->

## Where It Fits

This routine runs during export-coefficient database initialization, called by `exco_db_read` after the main export-coefficient file has been processed and after other constituent-specific readers such as `exco_read_om`. Its results are later used when export-coefficient objects are assigned pathogen path hydrographs through `obcs(iob)%hd(1)%path`.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. Check input file availability | The routine tests whether `in_exco%path` exists and also allows the configured filename to drive the read path if it is not the literal string `null`. |
| 2. Open and count data rows | It opens unit 107 on the configured file, skips the title and header lines, then scans the remaining records to count how many pathogen-path entries are present. |
| 3. Record the discovered path count | The counted row total is stored in `db_mx%exco_path` so later loops and allocations know how many path definitions exist. |
| 4. Allocate lookup storage | It allocates the `exco_path` array, each `exco_path(iexco_path)%path` vector sized to `cs_db%num_paths`, plus `exco_path_num` and `exco_path_name` for the crosswalk metadata. |
| 5. Rewind and reread file headers | The file is rewound and the title and header lines are read again so the second pass starts from the beginning of the data section. |
| 6. Load each path record | For each discovered record, the routine reads a line to position the file, backspaces, then reads the path name and all constituent-path values into the allocated arrays. |
| 7. Close the input file | Unit 107 is closed after the path data have been loaded. |
| 8. Crosswalk export-coefficient file names to path indices | The routine loops through `exco_db` and matches each `path_file` name to a loaded path name, storing the matching sequential index in `exco_path_num(iexco)`. |
| 9. Attach hydrograph paths to export-coefficient objects | Using `sp_ob1%exco`, `sp_ob%exco`, and each object's `ob(iob)%props`, the routine assigns either zeros for `path_file == 'null'` or the matched `exco_path(... )%path` array into `obcs(iob)%hd(1)%path`. |

## Modules Used

<!-- facts:uses -->

| Module | State touched | Key components |
| --- | --- | --- |
| [sym:hydrograph_module] | `sp_ob1, sp_ob, ob, hd` | `sp_ob1%exco, sp_ob%exco, ob(iob)%props` |
| [sym:input_file_module] | `in_exco` | `in_exco%path` |
| [sym:organic_mineral_mass_module] | `cs_db, exco_path, obcs` | `cs_db%num_paths, exco_path(iexco_path)%path, obcs(iob)%hd(1)%path` |
| [sym:constituent_mass_module] | `exco_path, cs_db, obcs` | `exco_path(iexco_path)%path, cs_db%num_paths, obcs(iob)%hd(1)%path` |
| [sym:exco_module] | `exco_db, exco_path_num, exco_path_name` | `exco_db(iexco)%path_file` |
| [sym:maximum_data_module] | `db_mx` | `db_mx%exco_path, db_mx%exco` |

## Local Variables

<!-- facts:locals -->

## State Changes

| Target | When | Meaning |
| --- | --- | --- |
| `db_mx%exco_path` | When `in_exco%path` exists or is not the literal `null`, and the file scan finds data rows. | The routine stores the number of export-coefficient path records discovered in the input file so later allocations and loops can use the exact path count. |
| `exco_path_num(iexco)` | During the crosswalk loop for each `iexco` whose `exco_db(iexco)%path_file` matches a loaded `exco_path_name(iexco_path)`. | The routine records which sequential path row belongs to each export-coefficient definition, enabling later object assignment by index instead of by name. |
| `obcs(iob)%hd(1)%path` | For each export-coefficient object `iob` where `exco_db(iexco)%path_file` is not `null` and the matching path index has been found. | The routine copies the loaded pathogen-path hydrograph into the object's constituent hydrograph slot; if the file name is `null`, it clears the path array to zeros instead. |

## File I/O

<!-- facts:io -->


## Lineage

Three resolved commits changed `exco_read_path`. The initial addition (`df07e3f`) introduced the routine, its file scan, allocation, crosswalk, and hydrograph assignment logic. Commit `f8bb6ec` changed the object-assignment branch formatting and, more importantly, made the copied path array zero-initialized during allocation. Commit `39fabde` initialized the local scratch variables and changed `exco_path_num` allocation to be zero-filled.

- `df07e3f` established the full `exco_read_path` workflow: file scan, allocation, name crosswalk, and assignment into `obcs(iob)%hd(1)%path`.
- `f8bb6ec` ensured `exco_path(iexco_path)%path` was allocated with `source = 0.`, so path arrays start with defined zeros before file values are loaded.
- `39fabde` initialized the local string and index variables and changed `exco_path_num` to allocate with `source = 0`, reducing uninitialized-state risk before the read and crosswalk loops.

## Review Notes

- Direct file I/O exists; verify file meanings and units before finalizing.
- warning: missing_doc: Procedure 'exco_read_path' has no extracted documentation comment.
- organic_mineral_mass_module is imported but no direct symbols from it were resolved in the extracted source; its inclusion is likely for broader constituent-reader consistency.
