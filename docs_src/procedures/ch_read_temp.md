---
kind: procedure
symbol: ch_read_temp
title: ch_read_temp
status: filled
source_hash: 0ee639e39dbdb593
version_label: SWAT+ 62.0.0
locals:
  titldum: Scratch character buffer for reading the file title line and later per-record labels
    or row identifiers during the counting and load passes.
  header: Scratch character buffer for the second header line in temperature.cha; used to
    skip or validate the file header before counting and loading records.
  eof: I/O status flag from each formatted read; negative values terminate the scan or load
    loop at end-of-file.
  imax: Counter for the number of temperature data records found in temperature.cha; becomes
    the upper bound used to allocate w_temp and is copied to db_mx%w_temp.
  ich_temp: Loop index used to step through w_temp entries while rereading the file and filling
    each temperature record.
  i_exist: Logical flag set by inquire to indicate whether the configured temperature input
    file exists before the routine tries to open it.
uses:
  basin_module: basin-wide state can affect model initialization order, but this routine does
    not directly reference any basin_module variables in the extracted code, so its influence
    is indirect rather than explicit here.
  time_module: time_module matters because this routine is part of model setup that occurs
    before time-stepped simulation, but the extracted code does not directly use any time_module
    variable or type.
  input_file_module: input_file_module supplies in_cha%temp, the configured path to temperature.cha;
    without it, the routine would not know which file to inquire, open, and read.
  maximum_data_module: maximum_data_module provides db_mx%w_temp, the shared count of loaded
    temperature records that this routine sets after scanning the file.
  channel_data_module: channel_data_module owns the allocatable w_temp array that receives
    the parsed temperature records and is the main data structure filled by this routine.
  hydrograph_module: hydrograph_module is part of the shared channel/hydrograph data context
    that consumes channel setup information, but no direct hydrograph variable is touched
    in the extracted code.
---

<!-- facts:header -->

Reads channel water-temperature definitions from temperature.cha and loads them into the shared w_temp array.

## Bottom Line

ch_read_temp opens the channel temperature input file named by in_cha%temp, counts how many data records it contains, sizes the shared w_temp array accordingly, and then rereads the file to populate each water-temperature record. If the configured file is missing or set to "null", it creates a minimal w_temp(0:0) array instead of loading data.

The routine also records the number of loaded records in db_mx%w_temp so later channel and hydrograph logic can rely on the temperature database being allocated and filled before the rest of the model reads or uses channel temperature settings.

## Arguments

<!-- facts:arguments -->

## Where It Fits

This routine runs during model input processing, immediately after proc_read starts the suite of file readers. proc_read prepares the overall initialization sequence and then calls ch_read_temp before other readers that depend on channel database state. Its results matter for later channel and hydrograph setup because they establish how many temperature records exist and populate the shared w_temp array used by subsequent model logic.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. Check whether the configured temperature file exists | The routine uses inquire on in_cha%temp and, if the file is missing or the name is "null", allocates a minimal w_temp(0:0) array instead of trying to read channel temperature data. |
| 2. Open the temperature file and read past title/header records | The file on unit 105 is opened and the first two lines are read into titldum and header so the routine can skip file metadata before counting data rows. |
| 3. Count the available temperature records | The routine loops through the remaining file lines, reading titldum until eof signals the end of the file, and increments imax for each record encountered. |
| 4. Publish the record count and resize shared storage | The counted record total is stored in db_mx%w_temp, any existing w_temp allocation is removed, and a new w_temp(0:imax) array is allocated to hold all records. |
| 5. Rewind the file and reread the headers | The file is rewound and the title and header lines are read again so the second pass begins at the data section. |
| 6. Load each record into w_temp | For each expected record, the routine reads a line into titldum, backs up one record, and then reads the structured data into w_temp(ich_temp) until all records are loaded or eof is reached. |
| 7. Close the input file and return | After loading is complete, the routine closes unit 105 and exits. |

## Modules Used

<!-- facts:uses -->

| Module | State touched | Key components |
| --- | --- | --- |
| [sym:basin_module] | `basin_module state is imported implicitly, but no specific basin symbols are referenced in the extracted source.` |  |
| [sym:time_module] | `time_module state is imported implicitly, but no specific time symbols are referenced in the extracted source.` |  |
| [sym:input_file_module] | `in_cha` | `in_cha%temp` |
| [sym:maximum_data_module] | `db_mx` | `db_mx%w_temp` |
| [sym:channel_data_module] | `w_temp` |  |
| [sym:hydrograph_module] | `hydrograph_module state is imported implicitly, but no specific hydrograph symbols are referenced in the extracted source.` |  |

## Local Variables

<!-- facts:locals -->

## State Changes

| Target | When | Meaning |
| --- | --- | --- |
| `db_mx%w_temp` | When temperature.cha exists and is not set to "null", the routine sets db_mx%w_temp to the number of data records found during the scan pass. | This updates the shared maximum-data counter for channel water-temperature records so later code knows how many w_temp entries were loaded and should be available. |

## File I/O

<!-- facts:io -->


## Lineage

Resolved lineage shows four changes: the procedure was introduced in df07e3f, 39fabde initialized titldum, header, eof, and imax, b9df6cf added use time_module and renamed the loop counter to ich_temp while also changing the missing-file branch to allocate w_temp(0:0), and 2ee1889 made only a whitespace-only return-line cleanup.

- df07e3f created ch_read_temp with the current open/read/rewind/backspace/load workflow and the db_mx%w_temp assignment.
- 39fabde did not change behavior; it only initialized local scalars and strings to default values.
- b9df6cf changed behavior by adding the allocation in the missing-file branch and by renaming the loop counter to ich_temp to avoid a module-name conflict.
- 2ee1889 changed no runtime behavior; it only adjusted trailing whitespace near the return statement.

## Review Notes

- Direct file I/O exists; verify file meanings and units before finalizing.
- warning: missing_doc: Procedure 'ch_read_temp' has no extracted documentation comment.
