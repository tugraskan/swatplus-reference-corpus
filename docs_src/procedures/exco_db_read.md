---
kind: procedure
symbol: exco_db_read
title: exco_db_read
status: filled
source_hash: 9da81ae35f4c10c5
version_label: SWAT+ 62.0.0
locals:
  titldum: Scratch string used to read and discard title lines and the leading integer field
    when counting or loading records from `exco.exc`.
  header: Scratch string used to skip the header lines in `exco.exc` before the record count
    and record-loading passes.
  eof: I/O status flag for the sequential reads from unit 107; a negative value ends the scan
    when end-of-file is reached.
  imax: Holds the number of export-coefficient records found in `exco.exc`; this becomes the
    upper bound for allocating and loading `exco_db`.
  i_exist: Logical flag set by `inquire` to show whether the configured export-coefficient
    file exists.
  i: Loop/record index read from the file before backing up and loading the full export-coefficient
    row into `exco_db(i)`.
  ii: Loop counter for the initial record-count scan and the subsequent load loop over `1:imax`.
  k: Leading integer field read alongside each export-coefficient record; it is consumed to
    populate the database row with `exco_db(i)`.
uses:
  exco_module: This module owns the allocatable `exco_db` array that stores the loaded export-coefficient
    records. `exco_db_read` sizes and fills that shared database, so the module must be in
    scope for allocation and assignment.
  constituent_mass_module: The constituent-count fields determine which follow-on export-coefficient
    tables need to be read. `exco_db_read` uses these counts to decide whether to call the
    pesticide, pathogen, heavy-metal, and salt readers after the base table is loaded.
  input_file_module: This module supplies `in_exco%exco`, the configured path to the export-coefficient
    input file. `exco_db_read` uses that path for the `inquire`, `open`, and all reads on
    unit 107.
  maximum_data_module: This module holds `db_mx%exco`, the shared count of export-coefficient
    records. `exco_db_read` updates it after counting records so later code can size and reference
    the loaded export-coefficient database.
---

<!-- facts:header -->

Reads the export-coefficient database from the configured `exco.exc` file, counts and loads its records, then dispatches to the constituent-specific readers. It also stores the record count in shared model state for later sizing and crosswalks.

## Bottom Line

`exco_db_read` is the top-level loader for export-coefficient database data. It opens the configured `exco.exc` file, scans past the title/header rows, counts how many export-coefficient records are present, allocates `exco_db`, and then reads each record into shared module state.

After the base export-coefficient table is loaded, the routine calls the organic-matter, pesticide, pathogen, heavy-metal, and salt readers so the full export-coefficient dataset is available before later SWAT+ setup and routing code runs.

## Arguments

<!-- facts:arguments -->

## Where It Fits

This routine runs during model initialization, after the input-file module has provided the configured export-coefficient file names. Its results feed later SWAT+ setup because the loaded `exco_db` array and `db_mx%exco` count are used before the constituent-specific export-coefficient readers and downstream routing/constituent handling.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. Check whether the export-coefficient file should be read | The routine inquires for the configured export-coefficient file and only enters the loading logic if the file exists or the configured name is not the sentinel value `null`. |
| 2. Open the file and scan past the preamble | It opens `in_exco%exco` on unit 107, reads and discards the title and header lines, and exits early if end-of-file is encountered during the scan. |
| 3. Count the data records | The routine resets `imax` and then loops through the remaining lines, incrementing `imax` for each record until end-of-file is reached. |
| 4. Save the record count for shared use | It stores the counted record total in `db_mx%exco` so later code can size and reference the export-coefficient database. |
| 5. Allocate the export-coefficient database | The routine allocates `exco_db(0:imax)` to hold the loaded export-coefficient rows. |
| 6. Rewind and rescan the file preamble | It rewinds the file and rereads the title and header lines so the next pass starts from the beginning of the data section. |
| 7. Load each export-coefficient record | For each record, it reads the row identifier, backs up one record, and then reads the full row into `exco_db(i)`. |
| 8. Close the file after loading | After the base database is loaded, it closes unit 107 and leaves the file-reading loop. |
| 9. Load organic-matter export-coefficient data | The routine calls `exco_read_om` to populate organic-matter export-coefficient state from the corresponding input source. |
| 10. Conditionally load pesticide data | If `cs_db%num_pests` is greater than zero, it calls `exco_read_pest` so pesticide export-coefficient data are loaded only when pesticides are simulated. |
| 11. Conditionally load pathogen/path data | If `cs_db%num_paths` is greater than zero, it calls `exco_read_path` to load pathogen/path export-coefficient data. |
| 12. Conditionally load heavy-metal data | If `cs_db%num_metals` is greater than zero, it calls `exco_read_hmet` to load heavy-metal export-coefficient data. |
| 13. Conditionally load salt data | If `cs_db%num_salts` is greater than zero, it calls `exco_read_salt` so salt export-coefficient data are available when salts are simulated. |
| 14. Return to the caller | The subroutine ends after all applicable export-coefficient databases have been loaded. |

## Modules Used

<!-- facts:uses -->

| Module | State touched | Key components |
| --- | --- | --- |
| [sym:exco_module] | `exco_db` |  |
| [sym:constituent_mass_module] | `cs_db` | `cs_db%num_pests, cs_db%num_paths, cs_db%num_metals, cs_db%num_salts` |
| [sym:input_file_module] | `in_exco` | `in_exco%exco` |
| [sym:maximum_data_module] | `db_mx` | `db_mx%exco` |

## Local Variables

<!-- facts:locals -->

## State Changes

| Target | When | Meaning |
| --- | --- | --- |
| `db_mx%exco` | When the configured export-coefficient file is processed and its data-record count has been determined. | `db_mx%exco` is updated to the number of export-coefficient rows found in `exco.exc`, giving later code the size of the loaded database and the upper bound used to allocate and populate `exco_db`. |

## File I/O

<!-- facts:io -->


## Lineage

`exco_db_read.f90` was introduced in `df07e3f` (2024-03-05, "init all") and has been changed in 5 non-merge commit(s) since, most recently `080211e` (2026-03-09, "water allocation operating properly"). Lineage is reconstructed from commit metadata (SHA, date, subject); per-line diffs were unavailable in this build environment, so only the commits touching `exco_db_read.f90` are listed.

- `080211e` (2026-03-09) — water allocation operating properly
- `bd18ad4` (2025-11-24) — Pr 107 (#108)
- `39fabde` (2024-08-08) — Initialized varables with python script, corrected input data where integers where floats in two input files, trapped underflow errors in th…
- `94b6dec` (2024-05-30) — Added latest source code from bitbucket
- `df07e3f` (2024-03-05) — init all

## Review Notes

- Direct file I/O exists; verify file meanings and units before finalizing.
- warning: missing_doc: Procedure 'exco_db_read' has no extracted documentation comment.
- Lineage was reconstructed from file-level commit metadata; per-line diffs were unavailable in this environment (blobless clone), so line-span filtering was not applied.
