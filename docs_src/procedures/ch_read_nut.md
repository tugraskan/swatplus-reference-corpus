---
kind: procedure
symbol: ch_read_nut
title: ch_read_nut
status: filled
source_hash: 63e1fa63c90053f9
version_label: SWAT+ 62.0.0
locals:
  eof: I/O status flag for the file reads on unit 105. It is initialized to 0, then used with
    `iostat=` to detect end-of-file or read failure while scanning and loading `nutrients.cha`.
  imax: Counts how many channel nutrient records are found in `nutrients.cha` during the first
    pass. The routine uses it to size `ch_nut(0:imax)` and to assign `db_mx%ch_nut`.
  titldum: Temporary string used to read and discard title or record-label lines while scanning
    `nutrients.cha` and before backing up to reread a full data record.
  header: Temporary string used to capture the file header line after the title line during
    the initial scan and the second pass.
  i_exist: Logical flag set by `inquire` to indicate whether the configured nutrient input
    file exists before attempting to open it.
  ich: Loop counter for the record-loading pass. It indexes the current `ch_nut(ich)` entry
    being populated and normalized.
uses:
  input_file_module: This module provides `in_cha%nut`, the configured filename for the channel
    nutrient input file. `ch_read_nut` uses that path to decide whether the file can be read
    and to open the correct file on unit 105.
  basin_module: This module holds the shared maximum/size bookkeeping for data tables. `ch_read_nut`
    stores the number of nutrient records it found in `db_mx%ch_nut` so later code can use
    the correct allocation and loop bounds.
  time_module: The routing time-step value controls unit conversion for several rate parameters.
    `ch_read_nut` divides daily or per-day coefficients by `time%step` so the stored values
    match hourly or subdaily routing when applicable.
  maximum_data_module: This shared maximum-data structure receives the record count for the
    nutrient table. That count is part of the model's global file-size bookkeeping and is
    used to size or validate downstream access to `ch_nut`.
  channel_data_module: This module defines the `ch_nut` array and the `channel_nut_data` components
    that are filled from each file record. `ch_read_nut` allocates the array, reads each record
    into `ch_nut(ich)`, and then overwrites missing or zero values with defaults before unit
    conversion.
---

<!-- facts:header -->

Reads and initializes channel nutrient / water-quality parameters from `nutrients.cha` into the shared `ch_nut` array.

## Bottom Line

`ch_read_nut` loads the channel nutrient parameter set used by SWAT+ channel water-quality calculations. It checks whether the configured input file exists, counts the records, allocates `ch_nut`, then rereads the file and stores each record in `ch_nut(ich)`.

After each record is read, the routine supplies defaults for missing or nonpositive values and converts several parameters to the model's routing time step using `time%step`. It also records the number of channel nutrient entries in `db_mx%ch_nut` so later channel and routing routines know how many parameter records are available.

## Arguments

<!-- facts:arguments -->

## Where It Fits

This routine runs during channel setup in `proc_cha`, after the other channel input readers have been called and before later channel initialization and routing steps proceed. Its results populate the shared channel nutrient parameter table that downstream channel water-quality calculations rely on.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. Initialize status and check file presence | The routine resets `eof` and `imax`, checks whether `in_cha%nut` exists, and if the file is missing or named `null` it allocates a one-element placeholder `ch_nut(0:0)` and stops the file-reading path. |
| 2. Open the nutrient file and count data rows | It opens unit 105 on `in_cha%nut`, reads and skips the title and header lines, then loops through the remaining records to count how many nutrient entries are present in the file. |
| 3. Save record count and allocate storage | The counted record total is stored in `db_mx%ch_nut`, and `ch_nut(0:imax)` is allocated so there is room for every nutrient record plus the zero index used by the array declaration. |
| 4. Rewind and reread file headers | The file is rewound to the beginning, and the title and header lines are read again so the second pass starts at the first data record. |
| 5. Loop over each nutrient record | For each expected record, the routine reads and backs up over one line, then reads the full record into `ch_nut(ich)`. |
| 6. Apply defaults for missing parameter values | After a record is loaded, the routine fills any nonpositive values with built-in defaults for `lao`, `igropt`, `ai0` through `ai6`, `mumax`, `rhoq`, `tfact`, `k_l`, `k_n`, `k_p`, `lambda0` through `lambda2`, and `p_n`. |
| 7. Convert light and growth-rate units | It converts `k_l` from kJ/(m2*min) to MJ/(m2*hr) and divides `mumax` and `rhoq` by `time%step` so the rates match the model's routing time-step convention. |
| 8. Apply default sediment and reaction coefficients | The routine fills missing values for `rs1` through `rs7`, `rk1` through `rk6`, and `bc1` through `bc4` with the embedded defaults used by SWAT+ channel nutrient calculations. |
| 9. Convert per-day coefficients for subdaily routing | It divides `rs1` through `rs5`, `rk1` through `rk4`, and `bc1` through `bc4` by `time%step` so the loaded rates are scaled to the current routing interval. |
| 10. Finish and close the file | After the record loop completes, the routine exits the file-reading block, closes unit 105, and returns to the caller. |

## Modules Used

<!-- facts:uses -->

| Module | State touched | Key components |
| --- | --- | --- |
| [sym:input_file_module] | `in_cha` | `in_cha%nut` |
| [sym:basin_module] | `db_mx` | `db_mx%ch_nut` |
| [sym:time_module] | `time` | `time%step` |
| [sym:maximum_data_module] | `db_mx` | `db_mx%ch_nut` |
| [sym:channel_data_module] | `ch_nut` | `ch_nut(ich)%lao, ch_nut(ich)%igropt, ch_nut(ich)%ai0, ch_nut(ich)%ai1, ch_nut(ich)%ai2, ch_nut(ich)%ai3, ch_nut(ich)%ai4, ch_nut(ich)%ai5, ch_nut(ich)%ai6, ch_nut(ich)%mumax, ch_nut(ich)%rhoq, ch_nut(ich)%tfact, ch_nut(ich)%k_l, ch_nut(ich)%k_n, ch_nut(ich)%k_p, ch_nut(ich)%lambda0, ch_nut(ich)%lambda1, ch_nut(ich)%lambda2, ch_nut(ich)%p_n, ch_nut(ich)%rs1, ch_nut(ich)%rs2, ch_nut(ich)%rs3, ch_nut(ich)%rs4, ch_nut(ich)%rs5, ch_nut(ich)%rs6, ch_nut(ich)%rs7, ch_nut(ich)%rk1, ch_nut(ich)%rk2, ch_nut(ich)%rk4, ch_nut(ich)%rk5, ch_nut(ich)%rk6, ch_nut(ich)%bc1, ch_nut(ich)%bc2, ch_nut(ich)%bc3, ch_nut(ich)%bc4, ch_nut(ich)%rk3` |

## Local Variables

<!-- facts:locals -->

## State Changes

| Target | When | Meaning |
| --- | --- | --- |
| `db_mx%ch_nut` | When the nutrient file is present and the routine has counted the records in the first pass. | `db_mx%ch_nut` is set to the number of channel nutrient records found in `nutrients.cha`, giving the rest of the model the table size to use for later loops and allocations. |
| `ch_nut(ich)%k_l` | When a record is read and `ch_nut(ich)%k_l` is missing or nonpositive, then it is normalized and converted to model units. | `ch_nut(ich)%k_l` is populated with the half-saturation coefficient for light, defaulted to 0.75 if needed, and converted from kJ/(m2*min) to MJ/(m2*hr). |
| `ch_nut(ich)%mumax` | When a record is read and `ch_nut(ich)%mumax` is missing or nonpositive, then the value is corrected and scaled. | `ch_nut(ich)%mumax` stores the maximum specific algal growth rate for the channel record, defaulted to 2.0 and divided by `time%step` so it matches the routing interval. |
| `ch_nut(ich)%rhoq` | When a record is read and `ch_nut(ich)%rhoq` is missing or nonpositive, then the value is corrected and scaled. | `ch_nut(ich)%rhoq` stores the algal respiration rate, defaulted to 2.5 and divided by `time%step` to match the current time-step convention. |
| `ch_nut(ich)%rs1` | When a record is read and `ch_nut(ich)%rs1` is missing or nonpositive, or after any valid value is loaded. | `ch_nut(ich)%rs1` holds the local algal settling rate in the reach; the routine supplies 1.0 if needed and scales it by `time%step` for subdaily routing. |
| `ch_nut(ich)%rs2` | When a record is read and `ch_nut(ich)%rs2` is missing or nonpositive, or after any valid value is loaded. | `ch_nut(ich)%rs2` holds the benthos source rate for dissolved phosphorus; the routine supplies 0.05 if needed and scales it by `time%step`. |
| `ch_nut(ich)%rs3` | When a record is read and `ch_nut(ich)%rs3` is missing or nonpositive, or after any valid value is loaded. | `ch_nut(ich)%rs3` holds the benthos source rate for ammonia nitrogen; the routine supplies 0.5 if needed and scales it by `time%step`. |
| `ch_nut(ich)%rs4` | When a record is read and `ch_nut(ich)%rs4` is missing or nonpositive, or after any valid value is loaded. | `ch_nut(ich)%rs4` holds the rate coefficient for organic nitrogen settling; the routine supplies 0.05 if needed and scales it by `time%step`. |
| `ch_nut(ich)%rs5` | When a record is read and `ch_nut(ich)%rs5` is missing or nonpositive, or after any valid value is loaded. | `ch_nut(ich)%rs5` holds the organic phosphorus settling rate; the routine supplies 0.05 if needed and scales it by `time%step`. |
| `ch_nut(ich)%rk1` | When a record is read and `ch_nut(ich)%rk1` is missing or nonpositive, or after any valid value is loaded. | `ch_nut(ich)%rk1` stores the CBOD deoxygenation rate coefficient; the routine supplies 1.71 if needed and scales it by `time%step`. |
| `ch_nut(ich)%rk2` | When a record is read and `ch_nut(ich)%rk2` is missing or nonpositive, or after any valid value is loaded. | `ch_nut(ich)%rk2` stores the reaeration rate coefficient; the routine supplies 1.0 if needed and scales it by `time%step`. |
| `ch_nut(ich)%rk3` | When a record is read and `ch_nut(ich)%rk3` is read from the file and then adjusted for routing time step. | `ch_nut(ich)%rk3` stores the rate of loss of CBOD due to settling; the routine divides it by `time%step` during the subdaily scaling pass. |
| `ch_nut(ich)%rk4` | When a record is read and `ch_nut(ich)%rk4` is missing or nonpositive, or after any valid value is loaded. | `ch_nut(ich)%rk4` stores the sediment oxygen demand rate; the routine supplies 2.0 if needed and scales it by `time%step`. |
| `ch_nut(ich)%bc1` | When a record is read and `ch_nut(ich)%bc1` is missing or nonpositive, or after any valid value is loaded. | `ch_nut(ich)%bc1` stores the rate constant for oxidation of NH3 to NO2; the routine supplies 0.55 if needed and scales it by `time%step`. |
| `ch_nut(ich)%bc2` | When a record is read and `ch_nut(ich)%bc2` is missing or nonpositive, or after any valid value is loaded. | `ch_nut(ich)%bc2` stores the rate constant for oxidation of NO2 to NO3; the routine supplies 1.1 if needed and scales it by `time%step`. |
| `ch_nut(ich)%bc3` | When a record is read and `ch_nut(ich)%bc3` is missing or nonpositive, or after any valid value is loaded. | `ch_nut(ich)%bc3` stores the rate constant for hydrolysis of organic N to ammonia; the routine supplies 0.21 if needed and scales it by `time%step`. |
| `ch_nut(ich)%bc4` | When a record is read and `ch_nut(ich)%bc4` is missing or nonpositive, or after any valid value is loaded. | `ch_nut(ich)%bc4` stores the rate constant for decay of organic P to dissolved P; the routine supplies 0.35 if needed and scales it by `time%step`. |

## File I/O

<!-- facts:io -->


## Lineage

Resolved lineage shows three source changes for `ch_read_nut`: it was added in `df07e3f`, later `39fabde` initialized the local control variables (`eof`, `imax`, `titldum`, `header`, `ich`) and kept the existing zeroing assignments, and `889136d` only corrected a typo in the embedded documentation comment from "occuring" to "occurring".

- df07e3f added the full routine and its file-reading, allocation, defaulting, and time-step scaling logic.
- 39fabde initialized the local variables in the declaration block, changing the procedure's starting state for `eof`, `imax`, `titldum`, `header`, and `ich`.
- 889136d changed only the comment text in the routine header and did not alter executable behavior.

## Review Notes

- Direct file I/O exists; verify file meanings and units before finalizing.
- warning: missing_doc: Procedure 'ch_read_nut' has no extracted documentation comment.
