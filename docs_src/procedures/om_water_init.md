---
kind: procedure
symbol: om_water_init
title: om_water_init
status: filled
source_hash: 649a9a33f85bb9f8
version_label: SWAT+ 62.0.0
locals:
  titldum: Scratch character buffer for reading and skipping title or data lines while counting
    and loading om_water.ini.
  header: Scratch character buffer for reading and skipping the header line in om_water.ini
    before the actual data records.
  eof: I/O status flag for read operations; zero means continue, negative values signal end-of-file
    and stop the scan or load loop.
  imax: Counts how many om_water.ini data records are present so the routine can size the
    output arrays and set db_mx%om_water_init.
  i_exist: Logical flag from inquire that tells whether the configured om_water input file
    exists before the routine tries to open it.
  ichi: Loop counter used during the second pass to index each loaded organic-matter water
    record.
uses:
  basin_module: This configuration value supplies the filename for the initialization input.
    The routine cannot count or load records unless it knows which om_water file to open,
    and it also checks for the literal "null" to disable file-based initialization.
  input_file_module: input_file_module holds the in_init configuration object, including the
    om_water filename that controls whether this routine opens a real file or falls back to
    empty placeholder arrays.
  maximum_data_module: maximum_data_module provides db_mx%om_water_init, the shared counter
    where this routine publishes the number of om_water.ini records so later allocation and
    downstream code can use the size.
  channel_data_module: channel_data_module is listed as a used module in the source context,
    and the routine depends on the shared initialization arrays declared there to store the
    names and hydrologic output records loaded from om_water.ini.
  hydrograph_module: 'hydrograph_module matters because it defines the shared data structures
    this routine fills: om_init_name stores identifiers and om_init_water stores hyd_output
    records read from the file.'
  sd_channel_module: sd_channel_module is imported by the routine, so its state is part of
    the broader initialization context even though no specific symbol from it is resolved
    in the extracted references. It matters because this initializer runs alongside other
    channel-related setup that consumes shared water initialization data.
  constituent_mass_module: constituent_mass_module is imported because the om_water initialization
    participates in model state setup that can affect constituent mass handling later, even
    though no specific resolved symbol from this module appears in the extracted references.
---

<!-- facts:header -->

Initializes the organic matter water input dataset from om_water.ini. It counts records, sizes shared arrays, then loads names and hydrologic output entries into module state for later model use.

## Bottom Line

om_water_init sets up the organic-matter-in-water initialization data used by SWAT+ when reading the optional om_water.ini file. If the configured file is missing or set to "null", it creates 1-element placeholder arrays; otherwise it scans the file to count data rows, stores that count in db_mx%om_water_init, allocates om_init_name and om_init_water to match, and then rereads the file to load each record.

The routine uses the file header/title lines to skip non-data content, then repositions the file with rewind and backspace so each data line can be parsed into the name string and hyd_output record. The resulting arrays are shared module state that downstream code can use for organic-matter water initialization.

## Arguments

<!-- facts:arguments -->

## Where It Fits

This routine runs during model initialization, after the input-file configuration in in_init is available and before later hydrologic and constituent-processing code needs the organic-matter water lookup arrays. Its results matter because db_mx%om_water_init and the om_init_name/om_init_water arrays define how many records exist and what values are available for subsequent initialization and channel-related setup.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. Initialize counters and scratch variables | Sets up blank scratch strings, clears the end-of-file status, resets the record counter imax to zero, and initializes the loop counter ichi. |
| 2. Check whether om_water.ini is available | Uses inquire on in_init%om_water and also checks for the sentinel value "null"; if the file is unavailable or disabled, the routine allocates one-element placeholder arrays and stops the file-loading path. |
| 3. Open the configured input file | Loops into the file-processing branch, opens unit 105 on the configured om_water.ini path, and reads the first record as a title line. |
| 4. Read past the header and count data rows | Skips the header line, then keeps reading dummy records until end-of-file to count how many data rows are present, incrementing imax for each line. |
| 5. Publish the record count | Stores the counted row total in db_mx%om_water_init so the rest of the model can know how many om_water records exist. |
| 6. Allocate storage for the data records | Allocates om_init_water and om_init_name with bounds 0:imax so the arrays match the number of records found in the file. |
| 7. Rewind and skip file prologue again | Rewinds unit 105 to the start of om_water.ini and rereads the title and header lines so the file is positioned at the first data record. |
| 8. Load each record into shared arrays | Loops over each expected record, reads a line into titldum to advance to the record, backs up one record, then reads the name and hyd_output value into om_init_name(ichi) and om_init_water(ichi). |
| 9. Close the file and exit | Closes unit 105, leaves the file-processing loop, and returns from the subroutine. |

## Modules Used

<!-- facts:uses -->

| Module | State touched | Key components |
| --- | --- | --- |
| [sym:basin_module] | `in_init` | `in_init%om_water` |
| [sym:input_file_module] | `in_init` | `in_init%om_water` |
| [sym:maximum_data_module] | `db_mx` | `db_mx%om_water_init` |
| [sym:channel_data_module] | `om_init_water, om_init_name` | `om_init_name(0:0), om_init_water(0:0), om_init_name(0:imax), om_init_water(0:imax), om_init_name(ichi), om_init_water(ichi)` |
| [sym:hydrograph_module] | `om_init_water, om_init_name` |  |
| [sym:sd_channel_module] | `om_init_name, om_init_water` | `om_init_name(0:0), om_init_water(0:0), om_init_name(0:imax), om_init_water(0:imax), om_init_name(ichi), om_init_water(ichi)` |
| [sym:constituent_mass_module] | `om_init_name, om_init_water` | `om_init_name(0:0), om_init_water(0:0), om_init_name(0:imax), om_init_water(0:imax), om_init_name(ichi), om_init_water(ichi)` |

## Local Variables

<!-- facts:locals -->

## State Changes

| Target | When | Meaning |
| --- | --- | --- |
| `db_mx%om_water_init` | When om_water.ini exists and is not the literal "null". | db_mx%om_water_init is set to the number of data rows found in om_water.ini. This shared count becomes the basis for allocating and iterating through om_init_name and om_init_water. |

## File I/O

<!-- facts:io -->


## Lineage

Three source-lineage commits were resolved for om_water_init. The initial addition in df07e3f created the subroutine with its file-scan, allocation, rewind, and record-load logic. Commit 94b6dec reintroduced the same routine from the latest source import with no behavioral change visible in the diff excerpt. Commit 39fabde changed only local variable initialization by assigning default values to titldum, header, eof, imax, and ichi; the file-processing logic remained the same.

- 39fabde: initialized local scratch variables in the subroutine header, reducing dependence on separate assignment lines for titldum, header, eof, imax, and ichi.
- 94b6dec: imported the routine into the current source tree with the same file-counting, allocation, rewind, and load flow visible in the diff.
- df07e3f: added om_water_init and its full om_water.ini scanning/loading behavior.

## Review Notes

- Direct file I/O exists; verify file meanings and units before finalizing.
- warning: missing_doc: Procedure 'om_water_init' has no extracted documentation comment.
- basin_module, channel_data_module, sd_channel_module, and constituent_mass_module are imported in the source but no candidate symbols were resolved from them in the extracted references; some outside_state entries therefore describe their relevance at module level rather than naming a specific symbol.
