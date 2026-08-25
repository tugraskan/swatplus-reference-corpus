---
kind: procedure
symbol: exco_read_om
title: exco_read_om
status: filled
source_hash: 0823996b5075c575
version_label: SWAT+ 62.0.0
locals:
  titldum: Scratch character buffer used to read and discard the title line and the first
    pass's record markers.
  header: Scratch character buffer used to read and discard the header lines before the data
    records are counted or loaded.
  eof: Iostat/status flag for file reads; 0 means continue, negative values terminate the
    loop or routine at end-of-file.
  imax: Counts how many organic-matter export coefficient data records are present so the
    arrays can be sized and `db_mx%exco_om` can be set.
  ob1: Declared for the later hydrograph assignment block, but that block is commented out
    in the current source so `ob1` is unused here.
  ob2: Declared for the later hydrograph assignment block, but that block is commented out
    in the current source so `ob2` is unused here.
  i_exist: Logical flag from `inquire` that tells whether the configured input file exists
    on disk.
  ii: Loop index for loading each data record into the allocated arrays.
  iexco: Declared for the commented-out hydrograph crosswalk logic; not used in the active
    code path.
  iexco_om: Declared for the commented-out hydrograph crosswalk logic; not used in the active
    code path.
  iob: Declared for the commented-out hydrograph assignment loop; not used in the active code
    path.
uses:
  hydrograph_module: The `exco` array in `hydrograph_module` is the target storage for the
    organic-matter export coefficient records. This routine allocates and fills that shared
    array so the values are available to the rest of the model.
  input_file_module: '`input_file_module` supplies `in_exco%om`, the configured path to the
    organic-matter export coefficient file. The routine depends on that setting to decide
    which file to open and read.'
  organic_mineral_mass_module: These module arrays store the organic-matter export-coefficient
    name list and its numeric cross-reference. `exco_read_om` allocates and populates them
    from the file so later code can resolve names to records.
  constituent_mass_module: The `exco` array holds the actual export-coefficient objects being
    read. The routine allocates it and assigns each record into the shared hydrograph state.
  maximum_data_module: '`db_mx%exco_om` is the shared maximum-count field for this file category.
    The routine sets it to the number of records found so later readers and model setup code
    know the database size.'
  exco_module: '`exco_module` provides the allocatable name and index arrays used to store
    the loaded organic-matter export-coefficient records. Those arrays are the persistent
    lookup tables this routine fills.'
---

<!-- facts:header -->

Reads the organic-matter export coefficient table from `exco_om.exc` and loads it into shared SWAT+ state. It also records how many entries were found so later model setup can size and cross-reference the data.

## Bottom Line

`exco_read_om` is the reader for the export-coefficient file used by the organic-matter branch of the exco database. It opens `in_exco%om` (`exco_om.exc` by default), skips the title and header lines, counts the data records, then rewinds and loads each name/value pair into `exco_om_name` and `exco` while saving the record count in `db_mx%exco_om`.

That loaded table is part of the shared export-coefficient database prepared by `exco_db_read`. Other routines can use the populated arrays to map organic-matter export coefficient names to their coefficient records, and the final count lets the model know how many entries were available.

## Arguments

<!-- facts:arguments -->

## Where It Fits

This routine runs during export-coefficient database initialization, immediately after `exco_db_read` has finished the main `exco` file. Its results matter to any later code that needs the organic-matter export-coefficient table, because it supplies the shared count and arrays used for lookup and downstream hydrograph setup.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. Check input file availability | The routine tests whether the configured organic-matter export-coefficient file exists, or whether the configured file name is not the sentinel value `null`. If neither condition is true, the read block is skipped. |
| 2. Open the configured file and skip the preamble | It opens unit 107 on `in_exco%om`, reads and discards the title line, then reads and discards two header lines before attempting to count data records. |
| 3. Count the data records | The routine resets `imax` to zero and loops through the remaining records, incrementing `imax` once per data line until end-of-file is reached. |
| 4. Save the record count for the database | It copies the counted record total into `db_mx%exco_om` so the shared maximum-data state reflects the file size. |
| 5. Allocate the shared arrays | Using the counted size, it allocates the shared export-coefficient value array and the companion name and numeric cross-reference arrays. |
| 6. Rewind and skip the preamble again | After rewinding unit 107, it rereads and discards the same title and header lines so the file pointer is positioned at the first data record. |
| 7. Load each export-coefficient record | The routine loops over each record, reads the organic-matter export-coefficient name and value into `exco_om_name(ii)` and `exco(ii)`, and stops if an end-of-file condition occurs. |
| 8. Close the file and exit the read block | It closes unit 107 and exits the surrounding `do` block, leaving the loaded arrays and count available to later routines. |

## Modules Used

<!-- facts:uses -->

| Module | State touched | Key components |
| --- | --- | --- |
| [sym:hydrograph_module] | `exco` |  |
| [sym:input_file_module] | `in_exco` | `in_exco%om` |
| [sym:organic_mineral_mass_module] | `exco_om_num, exco_om_name` |  |
| [sym:constituent_mass_module] | `exco` |  |
| [sym:maximum_data_module] | `db_mx` | `db_mx%exco_om` |
| [sym:exco_module] | `exco_om_num, exco_om_name` |  |

## Local Variables

<!-- facts:locals -->

## State Changes

| Target | When | Meaning |
| --- | --- | --- |
| `db_mx%exco_om` | When `in_exco%om` exists or is not equal to the sentinel string `null`, the routine counts the file records and assigns that count to `db_mx%exco_om`. | `db_mx%exco_om` changes because the routine has determined how many organic-matter export-coefficient entries are present in `exco_om.exc`. That count is needed to size and iterate the shared arrays that hold the loaded database. |

## File I/O

<!-- facts:io -->


## Lineage

Four resolved commits touched `exco_read_om`. The initial addition in `df07e3f` introduced the reader, file-counting logic, array allocation, and the final hydrograph crosswalk block. Commit `39fabde` initialized the local scalars and changed `exco_om_num` allocation to use `source = 0`. Commit `e18817a` only adjusted a comment and kept the same allocation and rewind logic. Commit `080211e` changed the behavior more substantially by adding a third header read, switching the allocations from `0:imax` to `imax`, and removing the active crosswalk/backspace block in favor of commented code.

- df07e3f established the organic-matter export-coefficient reader and the original post-read crosswalk into hydrograph state.
- 39fabde made the local variables explicitly initialized and zero-filled `exco_om_num` on allocation.
- e18817a only changed a comment on the `exco` allocation line, with no functional change in the diff shown.
- 080211e changed file parsing and allocation behavior by adding an extra header read, switching array bounds to 1-based allocation, and removing the active hydrograph crosswalk logic from execution.

## Review Notes

- Direct file I/O exists; verify file meanings and units before finalizing.
- warning: missing_doc: Procedure 'exco_read_om' has no extracted documentation comment.
- The currently active source has the hydrograph crosswalk block commented out; the lineage evidence shows it was active in earlier revisions.
- The source uses three header reads before counting and loading records in the resolved HEAD revision.
