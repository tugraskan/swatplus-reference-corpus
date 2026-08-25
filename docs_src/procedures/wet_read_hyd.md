---
kind: procedure
symbol: wet_read_hyd
title: wet_read_hyd
status: filled
source_hash: a26778d2d6d69f35
version_label: SWAT+ 62.0.0
locals:
  titldum: Temporary character buffer used to read and discard the title or record label lines
    in `hydrology.wet` before the actual data records are processed.
  header: Temporary character buffer used to read and discard header lines in `hydrology.wet`
    and `gwflow.wetland`. It is not used as model state beyond skipping those rows.
  eof: I/O status flag for `read` statements. It is reset to 0 and used to detect end-of-file
    or read failure while counting records and loading data.
  imax: Counter for the number of wetland hydrology data records found in `hydrology.wet`;
    it becomes the allocation size and is copied to `db_mx%wet_hyd`.
  i_exist: Logical file-existence flag returned by `inquire`. It determines whether the configured
    wetland hydrology file or `gwflow.wetland` can be read.
  ires: Loop index for the wetland hydrology database records. It steps through each record
    when reading into `wet_hyddb(ires)`.
  dum1: Unused integer placeholder from an earlier file-reading pattern; in this version it
    is declared but not used in the body.
  hru_idx: HRU index parsed from the wetland name in `gwflow.wetland` so the routine can store
    thickness into the correct `wet_thick` element.
  idig: Character position of the first digit in `wet_name`, found with `scan`, so the trailing
    numeric HRU part can be read out of the name string.
  wet_name: Wetland identifier read from `gwflow.wetland` for each thickness record, such
    as a name with trailing digits that identify the HRU.
  thick_val: Thickness value read from `gwflow.wetland`; it is the bed thickness assigned
    to the parsed HRU index.
uses:
  basin_module: '`basin_module` supplies `bsn_cc%gwflow`, the switch that decides whether
    the gwflow-specific wetland thickness file should be consulted at all.'
  input_file_module: '`input_file_module` supplies `in_res%hyd_wet`, the configured path to
    the wetland hydrology input file that this routine opens and reads.'
  maximum_data_module: '`maximum_data_module` supplies `db_mx%wet_hyd`, which records how
    many wetland hydrology entries were found so array sizing and later processing match the
    file contents.'
  reservoir_data_module: '`reservoir_data_module` defines the wetland hydrology derived type
    and the allocatable arrays `wet_hyddb` and `wet_hyd` that hold wetland parameters such
    as `psa`, `pdep`, `esa`, and `evrsv`.'
  output_landscape_module: '`output_landscape_module` matters because `out_gw` is the output
    unit used to report when `gwflow.wetland` is found and bed thicknesses will be applied
    from that file.'
  gwflow_module: '`gwflow_module` matters because it provides the shared thickness array `wet_thick`,
    the gwflow activation flag `gw_wet_flag`, the input unit `in_wet_cell`, and the log unit
    `out_gw` used by the gwflow-specific file-processing branch.'
---

<!-- facts:header -->

Reads wetland hydrology input data and, when gwflow is active, optionally loads wetland bed thickness overrides from gwflow.wetland. It populates shared wetland hydrology arrays and the maximum-count tracker used by the rest of the model.

## Bottom Line

`wet_read_hyd` is a setup subroutine for wetland hydrology. It opens the file named by `in_res%hyd_wet`, counts data records to size the wetland hydrology database, rewinds, and then reads each record into `wet_hyddb(ires)` while filling in default values for missing spillway and evaporation settings.

If gwflow is enabled and `gwflow.wetland` exists, it also reads wetland-specific bed thickness values and stores them in `wet_thick(hru_idx)` by parsing the HRU index from the wetland name. Those shared arrays are then available to later wetland and groundwater flow calculations.

## Arguments

<!-- facts:arguments -->

## Where It Fits

This routine runs during wetland setup after the input-file paths and basin control flags have been initialized. It is the reader that prepares wetland hydrology parameters for later reservoir, wetland, and gwflow calculations, including optional wetland bed thickness values when gwflow is active.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. Initialize local buffers and counters | The routine declares temporary buffers, status flags, counters, and gwflow thickness-parsing variables, then resets `eof` and `imax` before any file access. |
| 2. Check whether the wetland hydrology file exists | It tests `in_res%hyd_wet` with `inquire` and, if the file is missing or set to `null`, allocates a minimal `wet_hyddb(0:0)` array and skips the file-reading path. |
| 3. Count wetland hydrology records | For an existing file, it opens unit 105, skips the title and header lines, then loops through the remaining records to increment `imax` until end-of-file is reached. |
| 4. Record the number of entries and allocate storage | It copies the record count to `db_mx%wet_hyd` and allocates `wet_hyddb(0:imax)` so the full wetland hydrology database can be loaded. |
| 5. Rewind and skip the file headers again | The routine rewinds unit 105 and rereads the title and header lines so the file is positioned at the first data record for the second pass. |
| 6. Load each wetland hydrology record | It loops from 1 to `imax`, reads a line to advance, backs up one record, and then reads the full derived-type record into `wet_hyddb(ires)`. |
| 7. Fill default wetland hydrology values when needed | After reading each record, it assigns fallback values for `psa`, `esa`, and `evrsv` when the file provides nonpositive values, using the loaded hydrology fields as the basis for those defaults. |
| 8. Close the wetland hydrology file | Once the records are loaded, it closes unit 105 and exits the file-reading loop. |
| 9. Check whether gwflow wetland thickness overrides are enabled | It only enters the thickness-reading branch when basin gwflow is active and `gw_wet_flag` is set, and it confirms that `gwflow.wetland` exists before reading it. |
| 10. Announce and open the gwflow wetland file | If the file is present, it writes a status message to `out_gw` and opens `gwflow.wetland` on `in_wet_cell` for reading. |
| 11. Skip gwflow wetland file headers | It reads two header lines from `gwflow.wetland` into `header` before processing data rows. |
| 12. Parse wetland names and thickness values | The routine reads each row as `wet_name` and `thick_val`, uses `scan` to locate the numeric suffix, reads that suffix into `hru_idx`, checks array bounds with `size(wet_thick)`, and stores the thickness into `wet_thick(hru_idx)` when valid. |
| 13. Close the gwflow wetland file | After processing all rows, it closes `in_wet_cell` and leaves the shared thickness array ready for later use. |
| 14. Return to caller | The subroutine ends after both reading phases complete. |

## Modules Used

<!-- facts:uses -->

| Module | State touched | Key components |
| --- | --- | --- |
| [sym:basin_module] | `bsn_cc` | `bsn_cc%gwflow` |
| [sym:input_file_module] | `in_res` | `in_res%hyd_wet` |
| [sym:maximum_data_module] | `db_mx` | `db_mx%wet_hyd` |
| [sym:reservoir_data_module] | `wet_hyddb, wet_hyd` | `wet_hyddb(ires)%psa, wet_hyd(ires)%pdep, wet_hyddb(ires)%esa, wet_hyd(ires)%psa, wet_hyddb(ires)%evrsv` |
| [sym:output_landscape_module] | `output_landscape_module` | `out_gw` |
| [sym:gwflow_module] | `in_wet_cell, wet_thick, gw_wet_flag, out_gw` | `in_wet_cell, wet_thick, gw_wet_flag, out_gw` |

## Local Variables

<!-- facts:locals -->

## State Changes

| Target | When | Meaning |
| --- | --- | --- |
| `db_mx%wet_hyd` | When `hydrology.wet` exists and data records are counted during the first pass through the file. | `db_mx%wet_hyd` is set to the number of wetland hydrology records found in the file so later allocation and processing know the database size. |
| `wet_thick(hru_idx)` | When `bsn_cc%gwflow == 1` and `gw_wet_flag == 1`, and `gwflow.wetland` contains a row whose parsed HRU index is within the bounds of `wet_thick`. | `wet_thick(hru_idx)` is updated with the thickness read from `gwflow.wetland`, overriding the default wetland bed thickness for that HRU. |

## File I/O

<!-- facts:io -->


## Lineage

Four resolved commits changed `wet_read_hyd`. The initial addition in `df07e3f` created the subroutine and its two-pass read of `hydrology.wet`, allocating `wet_hyd` and loading `wet_hyd(ires)` records. `96c2bfb` changed the allocation and load target from `wet_hyd` to `wet_hyddb` and updated the default assignments to operate on `wet_hyddb(ires)`. `39fabde` initialized the local counters and strings (`titldum`, `header`, `eof`, `imax`, `ires`, `dum1`) and corrected the indentation on the `open` statement. `3cc92b5` added the gwflow-specific thickness reader: new locals `hru_idx`, `idig`, `wet_name`, and `thick_val`, plus logic to read `gwflow.wetland`, parse wetland names, and assign `wet_thick` entries.

- df07e3f introduced the wetland hydrology reader and its record-counting/allocation pattern for the new file.
- 96c2bfb redirected storage to `wet_hyddb` and aligned the default-value logic with that array.
- 39fabde made the local bookkeeping variables explicitly initialized, reducing dependence on prior state before file reads.
- 3cc92b5 extended the routine to support gwflow wetland thickness overrides via `gwflow.wetland` and `wet_thick`.

## Review Notes

- Direct file I/O exists; verify file meanings and units before finalizing.
- warning: missing_doc: Procedure 'wet_read_hyd' has no extracted documentation comment.
- algorithm_steps revised: expanded the draft into 14 source-backed steps to separate file counting, allocation, reload, and gwflow override handling.
- `summary_variables[0].formula` is inferred from the assignment at line 43 and the preceding count loop; no other assignment to `db_mx%wet_hyd` appears in the provided source span.
