---
kind: procedure
symbol: salt_urban_read
title: salt_urban_read
status: filled
source_hash: 2ce65facef0989fd
version_label: SWAT+ 62.0.0
locals:
  titldum: Temporary line buffer used while scanning `salt_urban`; it reads each data row
    once to count how many urban salt records are present, and later is reused as the record
    buffer for the actual concentration read.
  header: Temporary buffer for the first two header lines in `salt_urban`; the routine reads
    and then discards these lines before scanning or loading the data rows.
  urb_type: Holds the urban land-use type name read from each `salt_urban` record so it can
    be matched against `urbdb(iu)%urbnm` before concentrations are stored.
  i_exist: Logical flag set by `inquire` to indicate whether the `salt_urban` file is present,
    controlling whether the routine proceeds with file reading.
  eof: Iostat/end-of-file status code for the record-counting scan. It starts at 0 and is
    updated by the `read(...,iostat=eof)` loop to detect the end of `salt_urban`.
  imax: Counts how many urban salt records are found in `salt_urban`; this count is then used
    to allocate the first dimension of `salt_urban_conc` and to bound the later record loop.
  itype: Loop counter that steps through each urban salt record after the file is rewound,
    one record per expected urban land-use entry.
  iu: Loop counter over `db_mx%urban`, used to search the loaded urban database for a land-use
    name that matches the current `urb_type` record.
  isalt: Loop counter over salt ions, used to fill one concentration value per ion into `salt_urban_conc(iu,isalt)`
    when a matching urban land-use type is found.
uses:
  maximum_data_module: The maximum-data module provides `db_mx%urban`, the number of urban
    land-use types stored in `urban.urb`. That limit is needed for the inner match loop so
    the routine can search all urban entries without guessing the database size.
  urban_data_module: The urban data module supplies the urban land-use database that this
    routine matches against. `urbdb(iu)%urbnm` is the stored land-use name for each urban
    type, and the routine uses it to find which row in `salt_urban` belongs to which urban
    database entry.
  constituent_mass_module: The constituent-mass module provides `cs_db%num_salts`, the number
    of salt ions simulated. That value determines whether the routine should run at all and
    how many concentration columns to read and allocate for each urban type.
  salt_module: The salt module owns `salt_urban_conc`, the shared 2-D table that stores the
    loaded urban salt concentrations. This routine allocates and fills that table so later
    salt routines can use the values.
---

<!-- facts:header -->

Reads and stores salt-ion concentration values for each urban land-use type from the `salt_urban` input file. The routine only runs when salt ions are being simulated and leaves the results in shared urban salt concentration storage.

## Bottom Line

salt_urban_read is the setup routine that loads the urban salt lookup table from the `salt_urban` file. It first checks whether salt simulation is active and whether the file exists, then counts the number of urban records, allocates `salt_urban_conc`, and fills each urban type's salt-ion concentrations from the file.

The result is shared module state that later salt/urban calculations can use when an urban land-use type is matched to `urban.urb`. If no salts are simulated or the file is absent, the routine does not populate the table.

## Arguments

<!-- facts:arguments -->

## Where It Fits

This routine runs during model input reading, after `proc_read` has already reached the salt-input section and before later salt calculations need urban concentration lookup values. It prepares the urban salt table that other parts of the salt model use when they need the concentrations associated with a matched urban land-use type.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. Skip work when no salts are simulated | The routine first checks `cs_db%num_salts`; if no salt ions are being simulated, it does not read the urban salt file or allocate storage. |
| 2. Confirm the input file exists | It tests whether the `salt_urban` file is present and only proceeds when `i_exist` is true. |
| 3. Open the file and skip headers | It opens unit 5054 on `salt_urban` and reads the first two header lines into a temporary character buffer. |
| 4. Count urban salt records | It scans the file record by record with `iostat=eof`, counting each data line in `imax` until end-of-file is reached. |
| 5. Allocate and clear the concentration table | It allocates `salt_urban_conc(imax,cs_db%num_salts)` and initializes the array contents to zero. |
| 6. Rewind and reread headers | It rewinds the file to the beginning and rereads the two header records so the second pass starts from the first data row. |
| 7. Loop over each data record | For each expected urban record, it reads the land-use name, searches the urban database for a matching `urbdb(iu)%urbnm`, backs up one record when a match is found, and then rereads the full line to load the salt-ion concentrations into `salt_urban_conc(iu,isalt)`. |
| 8. Close the file and return | After the optional read block finishes, the routine closes unit 5054 and returns to the caller. |

## Modules Used

<!-- facts:uses -->

| Module | State touched | Key components |
| --- | --- | --- |
| [sym:maximum_data_module] | `db_mx` | `db_mx%urban` |
| [sym:urban_data_module] | `urbdb` | `urbdb(iu)%urbnm` |
| [sym:constituent_mass_module] | `cs_db` | `cs_db%num_salts` |
| [sym:salt_module] | `salt_urban_conc` |  |

## Local Variables

<!-- facts:locals -->

## State Changes

| Target | When | Meaning |
| --- | --- | --- |
| `salt_urban_conc` | When `cs_db%num_salts > 0` and the `salt_urban` file exists, after the matching urban type is found in the loading loop. | `salt_urban_conc(iu,isalt)` is filled with the concentration values read from the matching `salt_urban` record for each urban land-use type and salt ion; unmatched entries remain at their zero initialization. |

## File I/O

<!-- facts:io -->


## Lineage

Resolved lineage shows three behavior-relevant changes. The procedure was introduced in df07e3f as a new reader for urban salt concentrations. In 35b029c, only formatting changed at the end of the file; the algorithm and data handling stayed the same. In 39fabde, the local variables were given explicit initial values and the urban concentration allocation was changed to `allocate(..., source = 0.)`, which also zero-initializes the table at allocation time.

- df07e3f added the entire `salt_urban_read` routine, including the file existence check, record counting, allocation, and urban-type matching logic.
- 39fabde initialized the local control variables and changed the allocation to `allocate (salt_urban_conc(imax,cs_db%num_salts), source = 0.)`, ensuring the table starts with zeroed values.

## Review Notes

- Direct file I/O exists; verify file meanings and units before finalizing.
- warning: missing_doc: Procedure 'salt_urban_read' has no extracted documentation comment.
