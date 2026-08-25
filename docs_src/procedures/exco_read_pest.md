---
kind: procedure
symbol: exco_read_pest
title: exco_read_pest
status: filled
source_hash: 728d4e83fd1ef7fe
version_label: SWAT+ 62.0.0
locals:
  titldum: Temporary 80-character string used to read and discard or probe lines while counting
    records and stepping through the file before the full row read.
  header: Temporary 80-character string used to read the file header line during the initial
    scan and again after rewinding before reading data rows.
  eof: I/O status flag from each `read`; it controls end-of-file and error exits while counting
    and loading records.
  imax: Counts how many pesticide export-coefficient records are present in `in_exco%pest`;
    it becomes the allocation size and `db_mx%exco_pest` value.
  ob1: First object index in the export-coefficient object range, taken from `sp_ob1%exco`
    before assigning hydrographs.
  ob2: Last object index in the export-coefficient object range, computed from `sp_ob1%exco
    + sp_ob%exco - 1`.
  i_exist: Logical result of the file existence check for `in_exco%pest`; it gates whether
    the routine attempts to read the pesticide export-coefficient file.
  iexco_pest: Loop index over pesticide export-coefficient rows and also the sequential lookup
    index stored in `exco_pest_num`.
  ii: Loop index used while reading each pesticide export-coefficient row into `exco_pest_name(ii)`
    and `exco_pest(ii)%pest`.
  ipest: Loop index over pesticide constituents inside each export-coefficient row when reading
    the pesticide coefficient vector.
  iexco: Loop index over export-coefficient database entries in `exco_db` during the name-to-sequential-number
    crosswalk and hydrograph assignment.
  iob: Loop index over object records in the export-coefficient object range while copying
    pesticide hydrographs into `obcs(iob)%hd(1)%pest`.
uses:
  hydrograph_module: This module supplies the spatial object and connectivity state that defines
    which export-coefficient objects are active (`sp_ob1%exco`, `sp_ob%exco`) and which parent
    object property each `iob` refers to (`ob(iob)%props`). Those indices determine the object
    range to update and which `exco_db` entry feeds each hydrograph copy.
  input_file_module: This module provides `in_exco%pest`, the configured filename for the
    pesticide export-coefficient input file. Without that shared input-path state, `exco_read_pest`
    would not know which file to open.
  organic_mineral_mass_module: This module defines the pesticide count that sizes each row
    (`cs_db%num_pests`), the allocated export-coefficient storage that receives those rows
    (`exco_pest`), and the hydrograph structure that gets populated from the matched row (`obcs(iob)%hd(1)%pest`).
  constituent_mass_module: This module holds the export-coefficient tables that `exco_read_pest`
    crosswalks. `exco_db(iexco)%pest_file` supplies the file name to match against `exco_pest_name`,
    and `exco_pest_num`/`exco_pest_name` store the resulting lookup so later routines can
    map from export-coefficient records to pesticide rows.
  exco_module: This module stores the total counts for each data-file family. `db_mx%exco_pest`
    is set here after counting the file rows, and `db_mx%exco` bounds the later crosswalk
    over all export-coefficient records.
  maximum_data_module: '`maximum_data_module` supplies `db_mx`, which is used to publish how
    many pesticide export-coefficient rows were loaded (`db_mx%exco_pest`) and how many export-coefficient
    records exist in total (`db_mx%exco`). Those counts bound the later crosswalk loop and
    the object-assign loop, so this module controls both allocation sizing and iteration limits
    here.'
---

<!-- facts:header -->

Reads the pesticide export-coefficient table for SWAT+ and crosswalks it to export-coefficient records. It also pushes the matched pesticide hydrographs into object constituent state for downstream routing.

## Bottom Line

`exco_read_pest` reads the pesticide export-coefficient list named by `in_exco%pest`, counts the data rows, allocates `exco_pest`/`exco_pest_name`/`exco_pest_num`, and stores the row count in `db_mx%exco_pest`. That gives the model a sequential pesticide export-coefficient table keyed by the file names listed in `exco_db`.

After the table is loaded, the routine crosswalks each export-coefficient database entry to its pesticide-file row number and then copies the matching pesticide hydrograph into `obcs(iob)%hd(1)%pest` for each export-coefficient object. If an export-coefficient record has `pest_file = 'null'`, the routine zeroes that hydrograph instead of copying data.

## Arguments

<!-- facts:arguments -->

## Where It Fits

This routine runs from `exco_db_read` after the export-coefficient master database has been read and after the pesticide count (`cs_db%num_pests`) is known. Its results are then used when the model needs pesticide export-coefficient lookups and when object hydrograph state is initialized for export-coefficient objects.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. Check input file availability | The routine queries whether `in_exco%pest` exists and also allows processing when the configured name is not the sentinel string `null`; only then does it enter the load loop. |
| 2. Open and scan the file to count rows | It opens unit 107 on `in_exco%pest`, reads and discards the title and header, then loops through the remaining records with `iostat=eof` to count data rows in `imax`. |
| 3. Publish the row count and allocate storage | The routine stores the count in `db_mx%exco_pest`, allocates `exco_pest(imax)`, allocates each `exco_pest(iexco_pest)%pest` vector to `cs_db%num_pests` with zero initialization, and allocates `exco_pest_num` and `exco_pest_name`. |
| 4. Rewind and reread the header | It rewinds unit 107 and rereads the title and header so the second pass starts from the beginning of the file data section. |
| 5. Read each pesticide export-coefficient record | For each expected row, the routine reads a probe token, backs up one record, and then reads the pesticide file name plus the full pesticide coefficient vector into `exco_pest_name(ii)` and `exco_pest(ii)%pest`. |
| 6. Close the pesticide file | It closes unit 107 after the data pass is complete. |
| 7. Crosswalk export-coefficient entries to pesticide rows | The routine loops through every export-coefficient record in `exco_db` and finds the matching pesticide file name in `exco_pest_name`, storing the corresponding sequential row number in `exco_pest_num`. |
| 8. Populate export-coefficient object hydrographs | It derives the export-coefficient object range from `sp_ob1%exco` and `sp_ob%exco`, then for each object either zeros `obcs(iob)%hd(1)%pest` when `exco_db(iexco)%pest_file` is `null` or copies the matched pesticide coefficient vector from `exco_pest` into that hydrograph state. |

## Modules Used

<!-- facts:uses -->

| Module | State touched | Key components |
| --- | --- | --- |
| [sym:hydrograph_module] | `sp_ob1, sp_ob, ob, hd` | `sp_ob1%exco, sp_ob%exco, ob(iob)%props` |
| [sym:input_file_module] | `in_exco` | `in_exco%pest` |
| [sym:organic_mineral_mass_module] | `cs_db, exco_pest, obcs` | `cs_db%num_pests, exco_pest(iexco_pest)%pest, obcs(iob)%hd(1)%pest` |
| [sym:constituent_mass_module] | `exco_pest, cs_db, obcs` | `exco_pest(iexco_pest)%pest, cs_db%num_pests, obcs(iob)%hd(1)%pest` |
| [sym:exco_module] | `exco_db, exco_pest_num, exco_pest_name` | `exco_db(iexco)%pest_file` |
| [sym:maximum_data_module] | `db_mx` | `db_mx%exco_pest, db_mx%exco` |

## Local Variables

<!-- facts:locals -->

## State Changes

| Target | When | Meaning |
| --- | --- | --- |
| `db_mx%exco_pest` | After counting the rows in `in_exco%pest` and before reading the table body. | `db_mx%exco_pest` is set to the number of pesticide export-coefficient records in the input file. That count is used to allocate arrays and to bound later loops over pesticide export-coefficient data. |
| `exco_pest_num(iexco)` | During the crosswalk loop when `exco_db(iexco)%pest_file` matches one of the loaded `exco_pest_name(iexco_pest)` entries. | `exco_pest_num(iexco)` is updated to the sequential row number for the matched pesticide file name, giving each export-coefficient record a lookup index into `exco_pest`. |
| `obcs(iob)%hd(1)%pest` | For each export-coefficient object `iob` when its parent export-coefficient file name is not `null`. | `obcs(iob)%hd(1)%pest` is filled with the pesticide coefficient vector from the matched `exco_pest` row so the object's pesticide hydrograph state is ready for later routing and constituent calculations. |

## File I/O

<!-- facts:io -->


## Lineage

Three resolved commits changed `exco_read_pest`. The initial add (`df07e3f`) introduced the subroutine and its full read/crosswalk/object-assignment logic. `f8bb6ec` changed the per-row pesticide allocation to initialize `exco_pest(iexco_pest)%pest` to zero on allocation. `39fabde` added zero initialization for the local scalars and switched `exco_pest_num(imax)` allocation to `source = 0`.

- df07e3f introduced the routine's file scan, sequential row counting, name crosswalk, and object hydrograph assignment behavior.
- f8bb6ec ensured each allocated pesticide coefficient vector starts at zero, preventing uninitialized values in `exco_pest(iexco_pest)%pest`.
- 39fabde initialized local working variables and zero-filled `exco_pest_num`, reducing dependence on implicit defaults.

## Review Notes

- Direct file I/O exists; verify file meanings and units before finalizing.
- warning: missing_doc: Procedure 'exco_read_pest' has no extracted documentation comment.
- organic_mineral_mass_module is imported but no extracted references from that module were resolved in the packet; its role here is uncertain from source alone.
