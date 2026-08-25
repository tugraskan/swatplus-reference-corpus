---
kind: procedure
symbol: exco_read_hmet
title: exco_read_hmet
status: filled
source_hash: 0bb86e8c23daf866
version_label: SWAT+ 62.0.0
locals:
  titldum: Scratch character buffer used to read and skip record lines while counting and
    loading the heavy-metal export coefficient file.
  header: Scratch character buffer for the file header line after the initial title line is
    read from `exco_hmet.exc`.
  eof: I/O status flag from `read(...,iostat=eof)` calls; controls file scanning loops and
    exits when end-of-file is reached.
  imax: Counts how many heavy-metal export coefficient records are present in the file and
    is used to size the allocation arrays.
  ob1: Starting sequential object index for the exco object range copied into `obcs(iob)%hd(1)%hmet`.
  ob2: Ending sequential object index for the exco object range copied into `obcs(iob)%hd(1)%hmet`.
  i_exist: Logical flag returned by `inquire` to indicate whether the configured heavy-metal
    export file exists.
  iexco_hmet: Loop index over the heavy-metal export coefficient table and later the matched
    sequential heavy-metal record number.
  ii: Loop index used while rereading and storing the heavy-metal export coefficient records.
  ihmet: Inner loop index over heavy-metal constituent positions when reading one record into
    `exco_hmet(ii)%hmet`.
  iexco: Loop index over exco definitions in `exco_db` and the object property lookup range.
  iob: Loop index over exco object connectivity records whose hydrograph state is being populated.
uses:
  hydrograph_module: This module provides the spatial object indexing and object-property
    mapping used to identify the exco objects that should receive heavy-metal hydrograph values.
    `sp_ob1%exco` and `sp_ob%exco` define the object index range, while `ob(iob)%props` selects
    the exco database entry for each object; `obcs(iob)%hd` is the destination hydrograph
    storage that gets filled from the loaded heavy-metal table.
  input_file_module: '`in_exco%hmet` supplies the configured filename for the heavy-metal
    export coefficient file, so this module determines which file `exco_read_hmet` opens and
    reads.'
  organic_mineral_mass_module: The source imports this module, but no symbol from it is referenced
    in the extracted procedure body. It matters only as a retained dependency in the routine's
    `use` list, not as an active data source in the shown code.
  constituent_mass_module: This module owns the heavy-metal export coefficient arrays and
    the heavy-metal count used to size and fill them. `cs_db%num_metals` determines how many
    values are read per record, `exco_hmet(iexco_hmet)%hmet` stores those values, and `obcs(iob)%hd(1)%hmet`
    receives the selected heavy-metal hydrograph for each exco object.
  exco_module: '`exco_db` holds each export coefficient definition, including the configured
    heavy-metal filename in `exco_db(iexco)%hmet_file`. The routine compares those names to
    `exco_hmet_name` and stores the matched sequential position in `exco_hmet_num` so later
    object setup can find the right heavy-metal record quickly.'
  maximum_data_module: '`db_mx` stores the maximum loaded counts needed to drive allocation
    and loops. `db_mx%exco_hmet` becomes the number of heavy-metal records found in the file,
    and `db_mx%exco` bounds the exco definitions scanned during the name-to-index crosswalk.'
---

<!-- facts:header -->

Reads the heavy-metal export coefficient file for SWAT+ and maps each export coefficient record to the corresponding exco definitions and object hydrographs.

## Bottom Line

`exco_read_hmet` loads the heavy-metal component of the export-coefficient database from `in_exco%hmet` (`exco_hmet.exc`). It first counts how many records are present, allocates the heavy-metal arrays, then rereads the file to store each export coefficient name and its heavy-metal values.

After loading the file, the routine crosswalks `exco_db(iexco)%hmet_file` to the sequential heavy-metal table index in `exco_hmet_num(iexco)`, and then fills `obcs(iob)%hd(1)%hmet` for each exco object. That makes the heavy-metal export hydrographs available to later routing and constituent-mass calculations.

## Arguments

<!-- facts:arguments -->

## Where It Fits

This routine runs during export-coefficient database initialization, when `exco_db_read` calls it after the main exco file has already been read and `cs_db%num_metals` is known. Its results feed the heavy-metal export coefficient lookup tables and the object hydrograph assignments that later SWAT+ routing and constituent-mass routines use.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. Check input file availability | The routine inquires whether the configured heavy-metal export file exists and also allows processing when the configured name is not the sentinel value `null`. If neither condition is met, it skips the whole loading block. |
| 2. Open the file and count data rows | It opens unit 107 on `in_exco%hmet`, reads past the title and header lines, then loops through the remaining records to count how many heavy-metal export coefficient rows are present. |
| 3. Store the record count and allocate arrays | The counted row total is saved in `db_mx%exco_hmet`, then the routine allocates `exco_hmet`, each `exco_hmet(... )%hmet` vector, `exco_hmet_num`, and `exco_hmet_name` to hold the loaded records. |
| 4. Rewind and reread the file headers | The file is rewound to the start and the title and header lines are read again so the file pointer is reset before the structured data pass begins. |
| 5. Read each heavy-metal record | For each expected record, the routine reads a line to test for end-of-file, backs up one record, then reads the export coefficient name and all heavy-metal values into `exco_hmet_name(ii)` and `exco_hmet(ii)%hmet`. |
| 6. Close the input file | Once loading is complete, the routine closes unit 107 and exits the input-processing loop. |
| 7. Crosswalk exco definitions to heavy-metal records | It loops over all exco definitions and all loaded heavy-metal names, assigning `exco_hmet_num(iexco)` when `exco_db(iexco)%hmet_file` matches a loaded record name. |
| 8. Determine the exco object range | The routine derives the first and last sequential exco object indices from `sp_ob1%exco` and `sp_ob%exco` so it knows which object connectivity records need heavy-metal hydrographs. |
| 9. Fill object hydrographs | For each exco object, it looks up the associated exco definition through `ob(iob)%props`. If the object is mapped to `null`, it zeros `obcs(iob)%hd(1)%hmet`; otherwise it copies the matched heavy-metal vector from `exco_hmet(exco_hmet_num(iexco))%hmet` into the object hydrograph. |

## Modules Used

<!-- facts:uses -->

| Module | State touched | Key components |
| --- | --- | --- |
| [sym:hydrograph_module] | `sp_ob1, sp_ob, ob, hd` | `sp_ob1%exco, sp_ob%exco, ob(iob)%props` |
| [sym:input_file_module] | `in_exco` | `in_exco%hmet` |
| [sym:organic_mineral_mass_module] | `none resolved` | `none resolved` |
| [sym:constituent_mass_module] | `exco_hmet, cs_db, obcs` | `exco_hmet(iexco_hmet)%hmet, cs_db%num_metals, obcs(iob)%hd(1)%hmet` |
| [sym:exco_module] | `exco_db, exco_hmet_num, exco_hmet_name` | `exco_db(iexco)%hmet_file` |
| [sym:maximum_data_module] | `db_mx` | `db_mx%exco_hmet, db_mx%exco` |

## Local Variables

<!-- facts:locals -->

## State Changes

| Target | When | Meaning |
| --- | --- | --- |
| `db_mx%exco_hmet` | When `in_exco%hmet` exists or is not the sentinel `null`, and the file scan finds data rows. | Stores the number of heavy-metal export coefficient records discovered in the file so later allocations and loops know the table size. |
| `exco_hmet_num(iexco)` | When a loaded heavy-metal record name matches `exco_db(iexco)%hmet_file` during the crosswalk loop. | Stores the sequential index of the matching heavy-metal record for each exco definition so the object setup step can retrieve the right heavy-metal values efficiently. |
| `obcs(iob)%hd(1)%hmet` | For each exco object whose `exco_db(iexco)%hmet_file` is not `null`, after the crosswalk has resolved `exco_hmet_num(iexco)`. | Copies the selected heavy-metal export coefficient vector into the object hydrograph used by downstream routing and constituent-mass calculations; if the exco file is `null`, the array is set to zero instead. |

## File I/O

<!-- facts:io -->


## Lineage

Two resolved commits changed `exco_read_hmet`. The initial import commit `df07e3f` added the subroutine with the file-counting pass, allocation, record loading, name crosswalk, and object hydrograph assignment logic. Commit `39fabde` kept the algorithm unchanged but initialized local scalars and changed allocations to use `source = 0` for the heavy-metal arrays and `exco_hmet_num`, plus minor formatting cleanup in the final object assignment block.

- `df07e3f` introduced the routine and its heavy-metal file parsing workflow, including counting records, allocating storage, mapping `exco_db(iexco)%hmet_file` to `exco_hmet_num`, and copying values into `obcs(iob)%hd(1)%hmet`.
- `39fabde` did not change the routine's control flow, but it initialized local variables and zero-filled newly allocated storage to avoid undefined values before reads and assignments.

## Review Notes

- Direct file I/O exists; verify file meanings and units before finalizing.
- warning: missing_doc: Procedure 'exco_read_hmet' has no extracted documentation comment.
- organic_mineral_mass_module is imported but no referenced symbol was extracted from this routine; its practical role here is uncertain from the provided source.
