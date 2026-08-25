---
kind: procedure
symbol: cs_urban_read
title: cs_urban_read
status: filled
source_hash: f4e281fc4492adf0
version_label: SWAT+ 62.0.0
locals:
  titldum: Temporary line buffer used when counting data rows in `cs_urban`; it holds each
    record's first token during the end-of-file scan and is not used as model state.
  header: Scratch variable for the two header lines at the top of `cs_urban`; it is read twice
    before the data section is scanned and then reread after the rewind to skip the headers
    again.
  urb_type: Holds the urban land-use type name read from each data row; it is compared against
    `urbdb(iu)%urbnm` to find the matching urban database entry before concentrations are
    stored.
  i_exist: Logical flag set by `inquire` to indicate whether the `cs_urban` file exists; the
    routine only proceeds with reading if this flag is true.
  eof: I/O status code used to detect end-of-file while counting records in `cs_urban`; the
    scan loop stops when the read returns EOF.
  imax: Counts how many urban land-use records are present in `cs_urban`; it is later used
    to size the first dimension of `cs_urban_conc` and to bound the record-processing loop.
  itype: Outer loop counter over the urban records in the file after the rewind; it steps
    through each candidate urban land-use row.
  iu: Inner loop counter over the configured urban database entries (`db_mx%urban`); it searches
    for the `urb_type` match to identify which row of `cs_urban_conc` to fill.
  ics: Constituent index used in the implied-DO read that loads one concentration value per
    simulated constituent into `cs_urban_conc(iu,ics)`.
uses:
  maximum_data_module: '`db_mx%urban` supplies the number of urban land-use entries configured
    in the urban database, which sets the upper bound for matching `urb_type` values against
    `urbdb(iu)%urbnm`.'
  urban_data_module: '`urban_data_module` provides the urban database entries and their names,
    which are needed to match each `cs_urban` record''s `urb_type` to the correct urban land-use
    slot before concentrations are assigned.'
  constituent_mass_module: '`cs_db%num_cs` tells the routine how many constituent columns
    to expect in each urban record, and it also gates the entire read so the file is only
    processed when constituent simulation is enabled.'
  cs_module: '`cs_urban_conc` is the shared allocation that receives the urban constituent
    concentrations read from `cs_urban`; this routine creates and fills that table for later
    model use.'
---

<!-- facts:header -->

Reads the urban constituent concentration table from `cs_urban` and loads the concentrations into shared SWAT+ state. It sizes the urban lookup array from the file contents, then matches each urban land-use code against the urban database before storing constituent values.

## Bottom Line

`cs_urban_read` is the reader for the `cs_urban` input file, which supplies constituent concentrations for urban land-use types. If no other constituents are being simulated (`cs_db%num_cs <= 0`) or the file is missing, the routine simply skips the load; otherwise it opens the file, counts how many urban records it contains, allocates `cs_urban_conc`, and then reads the concentrations into that array.

The routine matters because the loaded `cs_urban_conc` table becomes the shared urban source-data lookup used later in the constituent routines. Each record is matched by urban type name (`urb_type` against `urbdb(iu)%urbnm`) so later calculations can pull the correct concentration set for each urban land-use category.

## Arguments

<!-- facts:arguments -->

## Where It Fits

This routine runs during the input-reading phase, when `proc_read` is assembling all constituent-related lookup tables before the simulation begins. Its results feed later urban constituent behavior by populating the shared urban concentration table used after input setup.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. Proceed only if constituent simulation is enabled | The routine first checks `cs_db%num_cs > 0`; if no other constituents are being simulated, it skips the urban constituent file entirely. |
| 2. Check whether the input file exists | It inquires for file `cs_urban` and stores the result in `i_exist`; only an existing file is processed. |
| 3. Open the file and skip its headers | The routine opens `cs_urban` on unit 5054 and reads the first two header lines into the scratch variable `header`. |
| 4. Count the number of urban data rows | It initializes `eof` and `imax`, then loops through the file with a formatted read into `titldum` until end-of-file is reached, incrementing `imax` for each data row found. |
| 5. Allocate and clear the urban concentration array | Using the counted row total and `cs_db%num_cs`, it allocates `cs_urban_conc(imax,cs_db%num_cs)` with zero source initialization and explicitly sets the array to zero. |
| 6. Rewind and skip the headers again | The file is rewound to the beginning, and the two header records are read again so the second pass starts at the first data row. |
| 7. Loop over each urban record and search for a database match | For each file row, the routine reads `urb_type` and scans all configured urban entries from `1` to `db_mx%urban` until it finds a matching urban name in `urbdb(iu)%urbnm`. |
| 8. Back up and read the matching concentration row | When a match is found, the file is backed up one record and reread so the full row can be loaded; the constituent values are stored into `cs_urban_conc(iu,ics)` for `ics=1,cs_db%num_cs`. |
| 9. Close the file and return | After all records are processed, the routine closes unit 5054 and returns to the caller. |

## Modules Used

<!-- facts:uses -->

| Module | State touched | Key components |
| --- | --- | --- |
| [sym:maximum_data_module] | `db_mx` | `db_mx%urban` |
| [sym:urban_data_module] | `urbdb` | `urbdb(iu)%urbnm` |
| [sym:constituent_mass_module] | `cs_db` | `cs_db%num_cs` |
| [sym:cs_module] | `cs_urban_conc` |  |

## Local Variables

<!-- facts:locals -->

## State Changes

| Target | When | Meaning |
| --- | --- | --- |
| `cs_urban_conc` | When `cs_db%num_cs > 0`, `cs_urban` exists, and a file row's `urb_type` matches `urbdb(iu)%urbnm` | The matching urban row in `cs_urban_conc` is filled with the constituent concentrations read from `cs_urban`; rows are initialized to zero first, then overwritten only for matched urban types. |

## File I/O

<!-- facts:io -->


## Lineage

Three source-backed commits were resolved for `cs_urban_read`. The file was added in `df07e3f` with the full reader logic. In `94b6dec`, the routine was introduced with the same core behavior as the current file, including the file existence check, header skipping, row counting, allocation, matching against `urbdb`, and loading `cs_urban_conc`. In `39fabde`, local variables were initialized and the allocation changed to `allocate(..., source = 0.)`, which also removed the need for a separate zeroing assumption. In `2ee1889`, only formatting changed at the end of the subroutine; the read logic was unchanged.

- `df07e3f` created the procedure and its current read workflow for urban constituent data.
- `94b6dec` established the end-to-end logic for counting rows, matching urban types, and filling `cs_urban_conc`.
- `39fabde` added explicit initialization for local scalars/strings and changed the allocation of `cs_urban_conc` to source-initialize values to zero.
- `2ee1889` made no behavioral change; it only cleaned trailing source formatting.

## Review Notes

- Direct file I/O exists; verify file meanings and units before finalizing.
- warning: missing_doc: Procedure 'cs_urban_read' has no extracted documentation comment.
- algorithm_steps revised: condensed the source logic into 9 steps to reflect the actual file-count/read/match flow and added the rewind/backspace pass explicitly.
- Source parsing for `urban_data_module` did not resolve a specific declaration snippet, so `outside_state[1].outside` is inferred from the matched urban name reference `urbdb(iu)%urbnm`.
