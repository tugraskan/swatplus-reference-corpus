---
kind: procedure
symbol: shade_factor_read
title: shade_factor_read
status: filled
source_hash: e21d9e274d8474a1
version_label: SWAT+ 62.0.0
locals:
  file: Unused local character variable; it is declared but never referenced in the shown
    routine.
  i: Unused local integer variable; it is declared but never referenced in the shown routine.
  idlsu: Loop counter for loading shade-factor records from the file into `shf_db(idlsu)`.
  titldum: Temporary string buffer used to read and discard title/label lines and to count
    data lines during the scan pass.
  header: Temporary string buffer used to read and discard the file header line before counting
    or loading data records.
  eof: IO status flag for each `read`; it controls loop termination and detects end-of-file
    or read failure.
  imax: Counts how many shade-factor data records are present and is then used to allocate
    `shf_db(0:imax)` and set `db_mx%shf`.
  i_exist: Logical flag set by `inquire` to indicate whether the configured shade-factor file
    exists before attempting to open it.
uses:
  input_file_module: The routine uses `input_file_module::in_shf%ssff_shf` to get the configured
    pathname for the shade-factor input file. Without that shared file-path state, it would
    not know which file to open.
  maximum_data_module: The routine updates `maximum_data_module::db_mx%shf` with the number
    of shade-factor records found. That shared count is how the rest of the model knows the
    size of the loaded shade-factor database.
  sd_channel_module: The shared `shf_db` array in `hydrograph_module` is the destination for
    the parsed shade-factor records. This routine allocates and fills it so other parts of
    the model can access the loaded data.
  hydrograph_module: The `hydrograph_module` owns the `shf_db` shade-factor database type
    and array. That module is the persistent storage location for the values this reader populates.
---

<!-- facts:header -->

Reads the shade-factor database file and loads its records into the shared `shf_db` array. It also counts how many records were found and stores that count in `db_mx%shf`.

## Bottom Line

`shade_factor_read` is a file reader for SWAT+ shade-factor input. It checks whether the configured `shade_factor.shf` path exists, sizes the shared `shf_db` allocation to match the number of data records, then reads each record into `shf_db(1:imax)`.

The routine matters because later model code can rely on `hydrograph_module::shf_db` and `maximum_data_module::db_mx%shf` to know how many shade-factor entries were loaded and to access the parsed shade-factor values.

## Arguments

<!-- facts:arguments -->

## Where It Fits

This routine runs during the input-reading phase, as called by `proc_read` after earlier database readers have prepared the model state. Its result is the loaded shade-factor database and record count, which later code can use when channel or hydrograph-related behavior needs shade-factor values.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. Initialize counters and check file availability | The routine starts with `eof` and `imax` set to zero, then uses `inquire` on `in_shf%ssff_shf` to determine whether the configured shade-factor file exists. If the file is missing or the path is the literal string `null`, it allocates a minimal `shf_db(0:0)` and skips file parsing. |
| 2. Open the shade-factor file and scan past the leading text | When the file is present, the routine opens unit 107 on `in_shf%ssff_shf`, reads the first line into `titldum`, then reads the next line into `header`. These reads consume the non-data text at the start of the file before counting records. |
| 3. Count how many data records exist | The routine loops while `eof == 0`, reading another line into `titldum` each time and incrementing `imax` for every successful record read. This produces the number of shade-factor data entries present in the file. |
| 4. Allocate storage sized to the record count | After counting, the routine allocates `shf_db(0:imax)` so the shared shade-factor database can hold every record that was found. |
| 5. Rewind and restart the file from the top | The file is rewound to the beginning and the title and header lines are read again. This resets the file position so the actual data can be loaded into the newly allocated array. |
| 6. Load each shade-factor record into shared state | The routine loops from `idlsu = 1` to `imax`, reading each data record into `shf_db(idlsu)`. The read stops early if an end-of-file condition occurs, otherwise all counted records are transferred into the shared database. |
| 7. Close the file and publish the record count | After the read pass, the routine closes unit 107 and stores `imax` in `db_mx%shf` so other code can know how many shade-factor entries were loaded. |

## Modules Used

<!-- facts:uses -->

| Module | State touched | Key components |
| --- | --- | --- |
| [sym:input_file_module] | `in_shf` | `in_shf%ssff_shf` |
| [sym:maximum_data_module] | `db_mx` | `db_mx%shf` |
| [sym:sd_channel_module] | `shf_db` | `shf_db(0:0), shf_db(0:imax), shf_db(idlsu)` |
| [sym:hydrograph_module] | `shf_db` |  |

## Local Variables

<!-- facts:locals -->

## State Changes

| Target | When | Meaning |
| --- | --- | --- |
| `db_mx%shf` | When the configured shade-factor file exists and is not the literal path `null`, the routine counts and loads its records; after the load, `db_mx%shf` is set to the counted record total `imax`. | `db_mx%shf` becomes the number of shade-factor records available in `shf_db`, which lets later routines size loops or validate accesses against the loaded database. |

## File I/O

<!-- facts:io -->


## Lineage

This procedure was introduced in the resolved lineage as a new source file in commit b9df6cf, which added the file-open, count-pass, rewind, load-pass, and final `db_mx%shf` assignment logic shown in the current source.

- b9df6cf added `shade_factor_read.f90` with the full read workflow: check the configured file path, count data lines to determine `imax`, allocate `shf_db`, reload records, and save the record count in `db_mx%shf`.

## Review Notes

- Direct file I/O exists; verify file meanings and units before finalizing.
- warning: missing_doc: Procedure 'shade_factor_read' has no extracted documentation comment.
