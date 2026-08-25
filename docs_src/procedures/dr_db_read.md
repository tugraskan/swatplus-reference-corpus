---
kind: procedure
symbol: dr_db_read
title: dr_db_read
status: filled
source_hash: 6debdd24f9d9377b
version_label: SWAT+ 62.0.0
locals:
  titldum: Scratch text buffer used to read and skip title or label lines from `delratio.del`
    before the actual data records are counted and loaded.
  header: Scratch text buffer used to read the file header line from `delratio.del` during
    both the counting pass and the data-loading pass.
  eof: I/O status flag from the `read` statements. A negative value ends the scan or load
    loop at end-of-file; zero means the read succeeded.
  imax: Counts how many delivery-ratio data records are present in `delratio.del`, excluding
    the skipped title/header lines. The routine uses it to size `dr_db` and to set `db_mx%dr`.
  i_exist: Logical flag set by `inquire` to report whether the configured delivery-ratio file
    exists on disk.
  ii: Loop index used to read each delivery-ratio record into `dr_db(ii)` after the array
    has been allocated.
uses:
  dr_module: '`dr_module` provides the shared allocatable database array `dr_db` that this
    routine sizes and fills from `delratio.del`, making the loaded delivery-ratio definitions
    available to later model setup.'
  input_file_module: '`input_file_module` supplies `in_delr%del_ratio`, the configured path
    to the delivery-ratio input file. Without that path, this routine would not know which
    file to inquire, open, and read.'
  constituent_mass_module: '`constituent_mass_module` supplies the simulated constituent counts
    that control whether the companion delivery-ratio tables for pests, pathogens, metals,
    and salts should be loaded after the main database is read.'
  maximum_data_module: '`maximum_data_module` holds `db_mx%dr`, the shared record-count used
    by downstream routines to know how many delivery-ratio database entries were loaded and
    to size later crosswalk logic.'
---

<!-- facts:header -->

Reads the delivery-ratio database file and then loads the constituent-specific delivery-ratio lookup tables that depend on it. It establishes the counts and shared arrays used later by hydro-connect and constituent transport setup.

## Bottom Line

`dr_db_read` is the delivery-ratio database loader for SWAT+. It opens the configured `delratio.del` file, counts and reads the main delivery-ratio records into `dr_db`, stores the record count in `db_mx%dr`, and then closes the file.

After the base database is loaded, it calls the constituent-specific readers for organic matter, pesticides, pathogens, heavy metals, and salts. Those follow-on reads only run when the corresponding simulated constituent counts in `cs_db` are nonzero, so this routine is the gatekeeper for all delivery-ratio lookup data.

## Arguments

<!-- facts:arguments -->

## Where It Fits

This routine runs during `hyd_connect` after the delivery-ratio connect file has been read and the model has determined that delivery-ratio objects exist. It prepares the shared delivery-ratio database and all constituent-specific lookup tables that later routing and hydrograph setup depend on.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. Check whether the configured delivery-ratio file should be read | The routine inquires whether `in_delr%del_ratio` exists and then tests the filename against the sentinel string `"null"`. If the file exists or the name is not `null`, it proceeds with loading. |
| 2. Open the delivery-ratio file and count data records | The routine opens unit 107 on `in_delr%del_ratio`, reads and skips the leading title and header lines, then loops through the remaining records to count them in `imax` until end-of-file is reached. |
| 3. Store the record count and allocate the shared database array | The routine copies the counted record total into `db_mx%dr` and allocates `dr_db(imax)` so the delivery-ratio records can be stored in shared module state. |
| 4. Rewind the file and reload the data section | The routine rewinds unit 107, rereads the title and header lines, and then reads each delivery-ratio record into `dr_db(ii)` for `ii = 1, imax`. |
| 5. Close the file after the main database load completes | The routine closes unit 107, exits the surrounding load block, and leaves the shared database array populated for later use. |
| 6. Load organic-matter delivery-ratio data | The routine calls `dr_read_om` to load the organic-matter delivery-ratio lookup data after the base delivery-ratio database is available. |
| 7. Load pesticide delivery-ratio data when pesticides are simulated | If `cs_db%num_pests > 0`, the routine calls `dr_read_pest` so pesticide delivery-ratio data are initialized only when the model includes pesticides. |
| 8. Load pathogen delivery-ratio data when pathogens are simulated | If `cs_db%num_paths > 0`, the routine calls `dr_path_read` so pathogen delivery-ratio data are initialized only for active pathogen simulations. |
| 9. Load heavy-metal delivery-ratio data when metals are simulated | If `cs_db%num_metals > 0`, the routine calls `dr_read_hmet` to bring in heavy-metal delivery-ratio coefficients and mappings. |
| 10. Load salt delivery-ratio data when salts are simulated | If `cs_db%num_salts > 0`, the routine calls `dr_read_salt` so salt delivery-ratio fractions are available for object hydrograph setup. |

## Modules Used

<!-- facts:uses -->

| Module | State touched | Key components |
| --- | --- | --- |
| [sym:dr_module] | `dr_db` |  |
| [sym:input_file_module] | `in_delr` | `in_delr%del_ratio` |
| [sym:constituent_mass_module] | `cs_db` | `cs_db%num_pests, cs_db%num_paths, cs_db%num_metals, cs_db%num_salts` |
| [sym:maximum_data_module] | `db_mx` | `db_mx%dr` |

## Local Variables

<!-- facts:locals -->

## State Changes

| Target | When | Meaning |
| --- | --- | --- |
| `db_mx%dr` | When the configured delivery-ratio file is present or the filename is not `"null"`, the routine sets `db_mx%dr = imax` after counting the data rows in `delratio.del`. | `db_mx%dr` becomes the shared count of delivery-ratio database records loaded from the main file. Later routines use this count to size loops and crosswalk delivery-ratio entries. |

## File I/O

<!-- facts:io -->


## Lineage

`dr_db_read.f90` was introduced in `df07e3f` (2024-03-05, "init all") and has been changed in 4 non-merge commit(s) since, most recently `bd18ad4` (2025-11-24, "Pr 107 (#108)"). Lineage is reconstructed from commit metadata (SHA, date, subject); per-line diffs were unavailable in this build environment, so only the commits touching `dr_db_read.f90` are listed.

- `bd18ad4` (2025-11-24) — Pr 107 (#108)
- `39fabde` (2024-08-08) — Initialized varables with python script, corrected input data where integers where floats in two input files, trapped underflow errors in th…
- `94b6dec` (2024-05-30) — Added latest source code from bitbucket
- `df07e3f` (2024-03-05) — init all

## Review Notes

- Direct file I/O exists; verify file meanings and units before finalizing.
- warning: missing_doc: Procedure 'dr_db_read' has no extracted documentation comment.
- No resolved lineage commits for dr_db_read.f90:1-63.
- Lineage was reconstructed from file-level commit metadata; per-line diffs were unavailable in this environment (blobless clone), so line-span filtering was not applied.
