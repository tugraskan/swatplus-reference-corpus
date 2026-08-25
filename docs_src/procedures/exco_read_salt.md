---
kind: procedure
symbol: exco_read_salt
title: exco_read_salt
status: filled
source_hash: d1d1184d77ac09a5
version_label: SWAT+ 62.0.0
locals:
  titldum: Scratch string used to read and discard title or data lines while counting records
    and re-reading the file; it also serves as a probe read for end-of-file conditions.
  header: Scratch string used to read and discard the file header line before counting or
    loading the salt records.
  eof: I/O status flag returned by each `read`; negative values signal end-of-file and control
    early exits, while zero means more records remain.
  imax: Counter for the number of salt export-coefficient records found in the file; it becomes
    the allocation size for the salt tables.
  ob1: Lower bound of the exco object range whose hydrograph salt outputs are assigned in
    the final mapping loop.
  ob2: Upper bound of the exco object range whose hydrograph salt outputs are assigned in
    the final mapping loop.
  i_exist: File-existence flag from `inquire`; it tells the routine whether the configured
    salt input file is present before attempting to read it.
  iexco_salt: Loop index over the salt export-coefficient records and later over the matched
    salt table entries.
  ii: Loop index used while reading each salt record from the file into `exco_salt_name` and
    `exco_salt`.
  isalt: Inner loop index over the salt constituent positions within one salt coefficient
    record.
  iexco: Loop index over exco database entries while cross-walking each exco record to its
    salt file and later assigning object hydrographs.
  iob: Loop index over hydrograph objects from `ob1` to `ob2` that receive the resolved salt
    hydrograph values.
uses:
  hydrograph_module: This module provides the spatial exco object bounds and per-object property
    links needed to decide which hydrograph outputs should receive salt coefficients. `sp_ob1%exco`
    and `sp_ob%exco` define the object range, while `ob(iob)%props` selects the exco database
    entry for each object.
  input_file_module: This module supplies the configured input filename. `in_exco%salt` tells
    the routine which salt export-coefficient file to inquire, open, rewind, and read.
  organic_mineral_mass_module: This module holds the salt constituent count and the salt coefficient
    storage. `cs_db%num_salts` sets the per-record array length, and `exco_salt(iexco_salt)%salt`
    is the target array that receives the parsed salt coefficients.
  maximum_data_module: This module stores the maximum number of records seen in the salt export
    file. `db_mx%exco_salt` is set from the counted lines and later drives the loops that
    populate salt tables and resolve mappings; `db_mx%exco` bounds the cross-walk over all
    exco entries.
  exco_module: This module holds the exco database and the resolved salt file names. `exco_db(iexco)%salts_file`
    is compared against each loaded salt table name to assign the correct sequential salt-table
    index.
  constituent_mass_module: This module contains the salt hydrograph arrays that are populated
    from the selected export coefficients. `exco_salt(iexco_salt)%salt` supplies the values
    copied to `obcs(iob)%hd(1)%salt` for exco objects whose salt file is not `null`, and `cs_db%num_salts`
    determines how many salt values are transferred.
---

<!-- facts:header -->

Reads the salt export-coefficient input file, builds the salt coefficient database, and cross-walks those coefficients onto exco objects and hydrologic outputs.

## Bottom Line

exco_read_salt loads salt export coefficient data from the file named in `in_exco%salt`. It first counts the data rows, allocates storage for the salt coefficient tables, then rereads the file to store each salt profile name and its salt values.

After loading the tables, it matches each exco record's `salts_file` name to the sequential salt table number and copies the resolved salt coefficient array into the exco-related hydrograph output `obcs(iob)%hd(1)%salt`. If an exco record has `salts_file == 'null'`, the routine leaves that hydrograph salt output at zero.

## Arguments

<!-- facts:arguments -->

## Where It Fits

This routine runs during export-coefficient database loading, when `exco_db_read` has already set up the overall exco metadata and calls the constituent-specific readers. Its results are then used to cross-walk exco salt-file names to sequential salt tables and to assign each exco object's salt hydrograph output.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. Check input file availability | The routine inquires whether the configured salt export file exists and only proceeds when the file is present or the configured filename is not the literal `null`. |
| 2. Open and probe the file | It opens unit 107 on the salt file, reads and discards the title and header lines, then loops through the remaining records to count how many salt coefficient entries are available. |
| 3. Save record count and allocate storage | The counted record total is stored in `db_mx%exco_salt`, then the routine allocates the salt coefficient array, the per-exco salt index array, and the salt-name array sized to that total. Each salt coefficient record's constituent array is allocated to `cs_db%num_salts` and initialized to zero. |
| 4. Rewind and reread the file structure | The file is rewound so the routine can reread the title and header lines from the beginning before loading the actual records. |
| 5. Load each salt coefficient record | For each expected salt record, the routine probes the next line, backs up one record, then reads the salt export name and its full set of salt coefficient values into the allocated arrays. |
| 6. Close the salt file | Once the salt tables are loaded, the routine closes unit 107 and leaves the file-reading loop. |
| 7. Cross-walk exco records to salt tables | The routine compares each exco database entry's `salts_file` name against the loaded salt names and stores the matching sequential table number in `exco_salt_num(iexco)`. |
| 8. Determine the exco object range | It computes the first and last exco object indices from `sp_ob1%exco` and `sp_ob%exco` so the hydrograph assignment loop covers all exco objects. |
| 9. Assign hydrograph salt outputs | For each exco object, the routine looks up its exco database record through `ob(iob)%props`; if the salt file is `null`, it zeroes `obcs(iob)%hd(1)%salt`, otherwise it copies the matching salt coefficient array into that hydrograph slot. |
| 10. Return to caller | The routine exits after the salt database and hydrograph assignments have been completed. |

## Modules Used

<!-- facts:uses -->

| Module | State touched | Key components |
| --- | --- | --- |
| [sym:hydrograph_module] | `sp_ob1, sp_ob, ob, hd` | `sp_ob1%exco, sp_ob%exco, ob(iob)%props` |
| [sym:input_file_module] | `in_exco` | `in_exco%salt` |
| [sym:organic_mineral_mass_module] | `cs_db, exco_salt` | `cs_db%num_salts, exco_salt(iexco_salt)%salt` |
| [sym:maximum_data_module] | `db_mx` | `db_mx%exco_salt, db_mx%exco` |
| [sym:exco_module] | `exco_db, exco_salt_num, exco_salt_name` | `exco_db(iexco)%salts_file` |
| [sym:constituent_mass_module] | `exco_salt, cs_db, obcs` | `exco_salt(iexco_salt)%salt, cs_db%num_salts, obcs(iob)%hd(1)%salt` |

## Local Variables

<!-- facts:locals -->

## State Changes

| Target | When | Meaning |
| --- | --- | --- |
| `db_mx%exco_salt` | When the configured salt file exists or the configured name is not `null`, and after the file scan counts the loaded records. | `db_mx%exco_salt` is set to the number of salt export-coefficient records found in the file. That count controls allocation and all later loops over salt tables. |
| `exco_salt_num(iexco)` | During the cross-walk loop, when `exco_db(iexco)%salts_file` exactly matches one of the loaded names in `exco_salt_name(iexco_salt)`. | `exco_salt_num(iexco)` is set to the sequential index of the matching salt table so later object hydrograph assignment can find the correct coefficient array for each exco entry. |
| `obcs(iob)%hd(1)%salt` | During the final object loop, when the exco record for `ob(iob)%props` has a `salts_file` value that is not `null`. | `obcs(iob)%hd(1)%salt` is copied from the matched salt coefficient array so the exco object's constituent hydrograph carries the loaded salt export coefficients. |

## File I/O

<!-- facts:io -->


## Lineage

Resolved lineage shows three behavior-changing commits. The initial addition commit `df07e3f` created `exco_read_salt` with file probing, record counting, allocation, record loading, cross-walking, and hydrograph assignment. Commit `f8bb6ec` changed the salt allocation and final null-file handling by initializing salt arrays to zero and keeping the `null` branch assignment formatting consistent. Commit `39fabde` initialized local scalars and changed `allocate (exco_salt_num(imax))` to zero-initialized allocation.

- df07e3f introduced the subroutine and its full salt-file loading workflow, including the cross-walk from exco file names to salt-table indices and the final hydrograph assignment.
- f8bb6ec changed salt storage initialization so each per-table salt array is allocated with `source = 0.`, and it preserved the explicit zeroing of `obcs(iob)%hd(1)%salt` when an exco record points to `null`.
- 39fabde initialized the local working scalars to zero and made `exco_salt_num` allocation source-initialized, reducing reliance on later assignment before use.

## Review Notes

- Direct file I/O exists; verify file meanings and units before finalizing.
- warning: missing_doc: Procedure 'exco_read_salt' has no extracted documentation comment.
