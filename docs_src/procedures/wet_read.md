---
kind: procedure
symbol: wet_read
title: wet_read
status: filled
source_hash: 30184e03cc98610b
version_label: SWAT+ 62.0.0
locals:
  titldum: Temporary character buffer for the file title line read from `wetland.wet` before
    the routine processes the rest of the file.
  header: Temporary character buffer for the header line read from `wetland.wet`; used to
    skip over the file's non-data header row(s).
  eof: I/O status flag for `read` operations. It is initialized to zero, becomes negative
    at end-of-file, and controls both the record-counting loop and the record-load loop.
  imax: Counts how many wetland data records are present in the file; later used to size the
    `wet_dat_c` and `wet_dat` arrays and stored in `db_mx%wet_dat`.
  i_exist: Logical flag set by `inquire` to indicate whether the configured wetland input
    file exists on disk.
  i: Scratch integer used while scanning the file to count records and again when rereading
    record numbers before backspacing and loading the full record.
  ires: Loop index for the wetland database records when filling `wet_dat_c(ires)` from the
    file.
  k: Scratch integer used to read the leading field on each wetland record before the full
    derived-type record is read into `wet_dat_c(ires)`.
uses:
  basin_module: '`basin_module` is imported by `wet_read`, so its shared basin-level state
    is part of the routine''s execution context even though no specific symbol from it is
    referenced in the visible source lines. It matters because this reader runs as part of
    the basin-wide initialization sequence that prepares shared model databases.'
  input_file_module: '`input_file_module` supplies `in_res%wet`, the configured path to `wetland.wet`.
    Without that module the routine would not know which wetland input file to open and scan.'
  maximum_data_module: '`maximum_data_module` supplies `db_mx%wet_dat`, the shared count of
    wetland database records. `wet_read` updates it after counting the file so later code
    can size loops and reference the loaded wetland database correctly.'
  reservoir_data_module: '`reservoir_data_module` provides the allocatable wetland data arrays
    `wet_dat_c` and `wet_dat` that this routine allocates and fills. Those arrays hold the
    parsed wetland definitions for later lookup and use.'
  reservoir_module: '`reservoir_module` is imported because wetland definitions are part of
    reservoir-related model state. The routine loads wetland database entries that later reservoir
    processing uses to connect wetland definitions to simulation objects.'
  hydrograph_module: '`hydrograph_module` matters because wetland definitions can be used
    by hydrograph-related reservoir/routing behavior later in the model, so the loaded wetland
    database must be available before hydrograph computations run.'
  constituent_mass_module: '`constituent_mass_module` matters because wetland routing can
    participate in constituent mass accounting; the wetland database loaded here is part of
    the shared state those calculations depend on.'
  pesticide_data_module: '`pesticide_data_module` matters because wetland setup is part of
    the reservoir system that can carry pesticide-related state downstream. Loading wetland
    definitions here ensures later pesticide accounting can resolve wetland-linked reservoir
    data.'
  res_salt_module: '`res_salt_module` matters because wetland reservoir definitions may be
    used in salt transport or salt state initialization later in the model, so the wetland
    database needs to be loaded first.'
  res_cs_module: '`res_cs_module` matters because wetland reservoir definitions can also feed
    carbon/constituent-specific reservoir state. This reader populates the shared wetland
    records needed by that later logic.'
---

<!-- facts:header -->

Reads the wetland definition file `wetland.wet`, counts wetland records, allocates wetland data arrays, and loads each record into shared reservoir database state.

## Bottom Line

`wet_read` is the wetland input reader for SWAT+. It checks whether the configured wetland file exists, counts the number of data records in `wetland.wet`, allocates `wet_dat_c` and `wet_dat`, and then rereads the file to populate the wetland character and numeric database entries.

This routine matters because later reservoir and routing code depends on `db_mx%wet_dat` and the loaded `wet_dat_c(ires)` / `wet_dat(ires)` arrays to identify and use wetland definitions.

## Arguments

<!-- facts:arguments -->

## Where It Fits

`wet_read` runs during model startup or input initialization after `in_res%wet` has been set by the input-file configuration. Its output is the shared wetland database (`wet_dat_c`, `wet_dat`, and `db_mx%wet_dat`) that later reservoir-related routines rely on to resolve wetland definitions.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. Check whether the wetland input file is available. | The routine uses `inquire` on `in_res%wet` to set `i_exist`. If the file is missing or the configured name is `'null'`, it allocates empty `wet_dat_c(0:0)` and `wet_dat(0:0)` arrays and skips file loading. |
| 2. Open and scan the wetland file to count data records. | When the file exists, unit 105 is opened on `in_res%wet`. The routine reads the title and header lines, then loops with `read(...,iostat=eof) i` until end-of-file to count wetland records in `imax`. |
| 3. Save the record count and allocate wetland database arrays. | The counted size is copied to `db_mx%wet_dat`, and the wetland character and numeric arrays are allocated to match `imax` records. |
| 4. Rewind the file and skip the title/header again. | The file is rewound so the second pass starts at the top. The routine rereads `titldum` and `header` to position the file at the first wetland data record. |
| 5. Load each wetland record into shared state. | For each record index `ires`, the routine reads a lead value into `i`, backspaces one record, and then reads `k, wet_dat_c(ires)` so the full wetland definition is stored in the wetland character database. |
| 6. Finalize the shared record count and close the file. | The routine confirms `db_mx%wet_dat = imax`, closes unit 105, and exits the file-processing loop. |
| 7. Return to the caller. | The subroutine ends after populating the shared wetland database. |

## Modules Used

<!-- facts:uses -->

| Module | State touched | Key components |
| --- | --- | --- |
| [sym:basin_module] | `basin_module` |  |
| [sym:input_file_module] | `in_res` | `in_res%wet` |
| [sym:maximum_data_module] | `db_mx` | `db_mx%wet_dat` |
| [sym:reservoir_data_module] | `wet_dat_c, wet_dat` |  |
| [sym:reservoir_module] | `reservoir_module` |  |
| [sym:hydrograph_module] | `hydrograph_module` |  |
| [sym:constituent_mass_module] | `constituent_mass_module` |  |
| [sym:pesticide_data_module] | `pesticide_data_module` |  |
| [sym:res_salt_module] | `res_salt_module` |  |
| [sym:res_cs_module] | `res_cs_module` |  |

## Local Variables

<!-- facts:locals -->

## State Changes

| Target | When | Meaning |
| --- | --- | --- |
| `db_mx%wet_dat` | When the configured wetland file exists and is not `'null'`, after the file has been scanned for record count. | `db_mx%wet_dat` is set to the number of wetland records found in `wetland.wet`, so other routines know how many wetland database entries were loaded and can loop over them safely. |

## File I/O

<!-- facts:io -->


## Lineage

Resolved lineage shows four commits affecting `wet_read`: 94b6dec introduced the reader with the file-counting, allocation, rewind, and record-loading flow; 96c2bfb refined the indentation and made the count/load pass structure explicit; 39fabde initialized local variables (`titldum`, `header`, `eof`, `imax`, and counters) to default values; fcf3891 removed unused counters and the `conditional_module` use statement, and added a later downstream block that maps wetland records into HRU and wetland initialization state. The resolved diffs do not show any behavioral change after the wetland file load in the visible span beyond those updates.

- 94b6dec: added the wetland file reader, including existence check, file counting, array allocation, rewind, and record loading into `wet_dat_c` and `wet_dat`.
- 96c2bfb: reorganized the file-scan and reload loops without changing the core wetland-read behavior.
- 39fabde: initialized the local scratch variables to explicit defaults before file processing begins.
- fcf3891: removed `conditional_module` and several unused counters from this routine, keeping the wetland read path focused on file loading and shared database sizing.

## Review Notes

- Direct file I/O exists; verify file meanings and units before finalizing.
- warning: missing_doc: Procedure 'wet_read' has no extracted documentation comment.
- algorithm_steps revised: merged and reordered the draft steps to match the actual two-pass read flow and the final close/return sequence.
- Source shows `search` declared as external but unused in the visible span; no guess made about its purpose.
- `basin_module`, `reservoir_module`, `hydrograph_module`, `constituent_mass_module`, `pesticide_data_module`, `res_salt_module`, and `res_cs_module` are imported but not explicitly referenced in the visible lines, so their roles are described from the procedure context rather than named symbols.
