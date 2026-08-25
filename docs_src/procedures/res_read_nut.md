---
kind: procedure
symbol: res_read_nut
title: res_read_nut
status: filled
source_hash: 94dd4062679aa861
version_label: SWAT+ 62.0.0
locals:
  titldum: Temporary text holder for the file title line and for the first field of each data
    record while counting and reading.
  header: Temporary text holder for the file header line that follows the title line.
  eof: I/O status flag used with `iostat`; zero means reading continues, and a negative value
    is used to detect end-of-file and stop scanning.
  imax: Counts how many reservoir nutrient records are present in the file and becomes the
    upper bound for allocating `res_nut(0:imax)`.
  i_exist: Logical flag from `inquire` that tells the routine whether the configured nutrient
    file exists before attempting to open it.
  ires: Loop index for stepping through reservoir nutrient records during both record counting
    and record loading.
uses:
  input_file_module: '`input_file_module` provides `in_res%nut_res`, the configured path to
    the reservoir nutrient input file. The routine uses that path to decide whether to open
    `nutrients.res` or treat the input as missing or disabled.'
  maximum_data_module: '`maximum_data_module` holds `db_mx%res_nut`, the shared count of reservoir
    nutrient records. This routine computes that count so later reservoir setup code knows
    how many records were loaded and how large the `res_nut` array is.'
  reservoir_data_module: '`reservoir_data_module` owns the allocatable `res_nut` array and
    the nutrient-loss fields stored in each `reservoir_nut_data` record. This routine allocates
    the array, reads each record into it, and then adjusts the loaded settling and soluble
    loss rates for later simulation use.'
---

<!-- facts:header -->

Reads the reservoir nutrients input file and loads reservoir nutrient-process parameters into shared model state. It also counts records, allocates the reservoir nutrient array, and converts annual loss rates to daily values.

## Bottom Line

res_read_nut opens the reservoir nutrients input file named in `in_res%nut_res` (normally `nutrients.res`), scans it to determine how many reservoir records exist, stores that count in `db_mx%res_nut`, allocates `res_nut`, and then reads each reservoir nutrient record into the shared reservoir data module.

After loading the records, it converts the settling and soluble loss-rate fields from per-year to per-day by dividing `psetlr1`, `psetlr2`, `nsetlr1`, `nsetlr2`, `nsolr`, and `psolr` by 365. The resulting values are used later wherever reservoir nutrient behavior is simulated.

## Arguments

<!-- facts:arguments -->

## Where It Fits

This routine runs during reservoir setup in `proc_res`, after hydrology and sediment inputs are read and before reservoir initial conditions and other reservoir database inputs are processed. Its output defines the reservoir nutrient parameter set that later reservoir simulation code uses when computing nutrient settling and soluble loss behavior.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. Check whether the configured file exists | Initialize counters, query whether `in_res%nut_res` exists, and if the file is missing or named `null`, allocate a minimal `res_nut(0:0)` array and skip file reading. |
| 2. Open the nutrients file and read its title/header | Open unit 105 on `in_res%nut_res`, read the title line and header line, and stop early if either read reaches end-of-file. |
| 3. Count data records | Loop through the remaining lines, reading into `titldum` and incrementing `imax` for each reservoir nutrient record encountered until end-of-file. |
| 4. Save the record count and allocate storage | Store the record count in `db_mx%res_nut` and allocate `res_nut(0:imax)` so there is one array slot for each loaded reservoir nutrient record. |
| 5. Rewind and reread the file preamble | Rewind unit 105 and reread the title and header lines so the second pass starts from the beginning of the file. |
| 6. Load each reservoir nutrient record | For each reservoir index from 1 to `imax`, read a line to advance, backspace one record, and then read the structured `res_nut(ires)` record into shared state. |
| 7. Close the file and convert units | Close unit 105 and convert the loaded settling and soluble loss-rate fields from yearly values to daily values by dividing by 365 for every reservoir record. |

## Modules Used

<!-- facts:uses -->

| Module | State touched | Key components |
| --- | --- | --- |
| [sym:input_file_module] | `in_res` | `in_res%nut_res` |
| [sym:maximum_data_module] | `db_mx` | `db_mx%res_nut` |
| [sym:reservoir_data_module] | `res_nut` | `res_nut(ires)%psetlr1, res_nut(ires)%psetlr2, res_nut(ires)%nsetlr1, res_nut(ires)%nsetlr2, res_nut(ires)%nsolr, res_nut(ires)%psolr` |

## Local Variables

<!-- facts:locals -->

## State Changes

| Target | When | Meaning |
| --- | --- | --- |
| `db_mx%res_nut` | After the file scan finishes and `imax` has been counted from the input file. | `db_mx%res_nut` is updated to the number of reservoir nutrient records found in `nutrients.res`, so the rest of the model knows how many records were loaded. |
| `res_nut(ires)%psetlr1` | For each loaded reservoir record during the final conversion loop. | `res_nut(ires)%psetlr1` is converted from a yearly phosphorus settling loss rate to a daily rate by dividing by 365. |
| `res_nut(ires)%psetlr2` | For each loaded reservoir record during the final conversion loop. | `res_nut(ires)%psetlr2` is converted from a yearly phosphorus settling loss rate to a daily rate by dividing by 365. |
| `res_nut(ires)%nsetlr1` | For each loaded reservoir record during the final conversion loop. | `res_nut(ires)%nsetlr1` is converted from a yearly nitrogen settling loss rate to a daily rate by dividing by 365. |
| `res_nut(ires)%nsetlr2` | For each loaded reservoir record during the final conversion loop. | `res_nut(ires)%nsetlr2` is converted from a yearly nitrogen settling loss rate to a daily rate by dividing by 365. |
| `res_nut(ires)%nsolr` | For each loaded reservoir record during the final conversion loop. | `res_nut(ires)%nsolr` is converted from a yearly soluble nitrogen loss rate to a daily rate by dividing by 365. |
| `res_nut(ires)%psolr` | For each loaded reservoir record during the final conversion loop. | `res_nut(ires)%psolr` is converted from a yearly soluble phosphorus loss rate to a daily rate by dividing by 365. |

## File I/O

<!-- facts:io -->


## Lineage

Source-backed lineage resolves four commits affecting `res_read_nut`. The file was introduced in 94b6dec as a new subroutine that reads reservoir nutrient input, counts records, allocates `res_nut`, and converts the settling rates. 39fabde only initialized local variables (`titldum`, `header`, `eof`, `imax`, `ires`) without changing the algorithm. 1807dbb added unit conversion for `nsolr` and `psolr`, extending the final conversion loop. 889136d made only a comment typo fix in the purpose text.

- 94b6dec added the routine and established the full read/count/allocate/load workflow for reservoir nutrient inputs.
- 39fabde changed local-variable initialization only, making the procedure safer but not altering file-processing behavior.
- 1807dbb expanded the unit conversion step to include `nsolr` and `psolr`, so those rates are now converted from per-year to per-day like the settling rates.
- 889136d corrected a documentation typo in the purpose comment; it did not change execution behavior.

## Review Notes

- Direct file I/O exists; verify file meanings and units before finalizing.
- warning: missing_doc: Procedure 'res_read_nut' has no extracted documentation comment.
