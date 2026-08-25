---
kind: procedure
symbol: cli_read_atmodep
title: cli_read_atmodep
status: filled
source_hash: c9ec49c2b0cf3a97
version_label: SWAT+ 62.0.0
locals:
  titldum: Temporary buffer for the file title line read from `atmodep.cli` before the control
    values are parsed.
  header: Temporary buffer for the file header line read after the title line; it is discarded
    after validating that the file can be read.
  eof: I/O status flag used by each `read` to detect end-of-file or read failure and exit
    the parsing loop when the file is exhausted or malformed.
  iadep: Loop counter over atmospheric deposition stations while reading each station block
    into `atmodep(iadep)`.
  imo: Loop counter over monthly deposition values when the file timestep is monthly.
  iyr: Loop counter over yearly deposition values when the file timestep is yearly.
  imo_atmo: Tracks the current month while searching for the simulation start month inside
    a monthly deposition series.
  i_exist: Logical flag set by `inquire` to show whether the configured deposition file exists
    on disk.
  iyrc_atmo: Working year counter used while searching for the simulation start year inside
    a yearly or monthly deposition series.
uses:
  basin_module: The routine does not take a file name argument; it uses `in_cli%atmo_cli`
    from `basin_module` to decide which atmospheric deposition climate file to probe and open.
  input_file_module: The input-file module supplies the configured atmospheric deposition
    file name `in_cli%atmo_cli`, which is the direct source of the file path used by the `inquire`
    and `open` statements.
  climate_module: The climate module holds the deposition control record, the per-station
    deposition arrays, and the station-name array that this routine fills from the file, so
    it is the main target of the parsed data.
  time_module: The routine compares the deposition file's start year and month against `time%yrc_start`
    and `time%mo_start` to locate the initial offset inside the deposition series.
  maximum_data_module: The maximum-data module stores the number of atmospheric deposition
    stations discovered in the file so the rest of the model can know how many deposition
    entries were loaded.
---

<!-- facts:header -->

Reads the atmospheric deposition climate definition file and loads annual, monthly, or yearly deposition series into shared climate state. It also records how many deposition stations were found and aligns the time index to the simulation start year or month.

## Bottom Line

This routine opens the atmospheric deposition input file named by `in_cli%atmo_cli` and parses the file header plus the control record that defines how many stations exist, what timestep the data use, the starting year/month, and how many values follow. It then allocates `atmodep` and `atmo_n` and reads each station's deposition data into the shared climate module structures.

The routine matters because later model code depends on the populated `climate_module` deposition arrays and on the control fields `atmodep_cont%ts` and `atmodep_cont%first`, which mark where simulation time should begin inside the deposition series.

## Arguments

<!-- facts:arguments -->

## Where It Fits

This routine runs during the broader input-read phase, after `proc_read` has already started assembling climate and other database inputs. Its results feed later climate and deposition behavior because the model uses the loaded station definitions, timestep control values, and deposition series when applying atmospheric deposition during the simulation.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. Initialize locals and detect the configured file | The routine initializes its working variables, clears the end-of-file status, and uses `inquire` on `in_cli%atmo_cli` to determine whether the atmospheric deposition file exists and is usable. |
| 2. Handle the missing-file case | If the file is missing or named `null`, it allocates empty `atmodep` and `atmo_n` arrays and records zero atmospheric deposition stations in `db_mx%atmodep`. |
| 3. Open and read the file prologue | When the file exists, the routine opens unit 127 on `in_cli%atmo_cli` and reads the title, header, and control record that defines the station count, timestep, start year/month, and number of values per station. |
| 4. Align the deposition series to simulation start | Using `atmodep_cont%yr_init`, `atmodep_cont%mo_init`, `time%yrc_start`, and `time%mo_start`, the routine searches for the first matching year or month and stores the offset in `atmodep_cont%ts`, while clearing `atmodep_cont%first` when a match is found. |
| 5. Allocate station storage | The routine allocates `atmodep(0:atmodep_cont%num_sta)` and `atmo_n(atmodep_cont%num_sta)` so it has storage for each deposition station and its name. |
| 6. Read annual station data | If the timestep is `aa`, the routine reads each station name and the four annual deposition values for rainfall ammonium, rainfall nitrate, dry ammonium, and dry nitrate. |
| 7. Read monthly station data | If the timestep is `mo`, the routine allocates monthly deposition arrays for each station, reads the station name, and then reads monthly sequences for the four deposition components. |
| 8. Read yearly station data | If the timestep is `yr`, the routine allocates yearly deposition arrays for each station, reads the station name, and then reads yearly sequences for the four deposition components. |
| 9. Publish the station count and return | After the input loop ends, the routine stores the final station count in `db_mx%atmodep` and returns to the caller. |

## Modules Used

<!-- facts:uses -->

| Module | State touched | Key components |
| --- | --- | --- |
| [sym:basin_module] | `in_cli` | `in_cli%atmo_cli` |
| [sym:input_file_module] | `in_cli` | `in_cli%atmo_cli` |
| [sym:climate_module] | `atmodep_cont, atmodep, atmo_n` | `atmodep_cont%num_sta, atmodep_cont%timestep, atmodep_cont%mo_init, atmodep_cont%yr_init, atmodep_cont%num, atmodep_cont%ts, atmodep_cont%first, atmodep(iadep)%name, atmodep(iadep)%nh4_rf, atmodep(iadep)%no3_rf, atmodep(iadep)%nh4_dry, atmodep(iadep)%no3_dry, atmodep(iadep)%nh4_rfmo, atmodep(iadep)%no3_rfmo, atmodep(iadep)%nh4_drymo, atmodep(iadep)%no3_drymo, atmodep(iadep)%nh4_rfmo(imo), atmodep(iadep)%no3_rfmo(imo), atmodep(iadep)%nh4_drymo(imo), atmodep(iadep)%no3_drymo(imo), atmodep(iadep)%nh4_rfyr, atmodep(iadep)%no3_rfyr, atmodep(iadep)%nh4_dryyr, atmodep(iadep)%no3_dryyr, atmodep(iadep)%nh4_rfyr(iyr), atmodep(iadep)%no3_rfyr(iyr), atmodep(iadep)%nh4_dryyr(iyr), atmodep(iadep)%no3_dryyr(iyr)` |
| [sym:time_module] | `time` | `time%yrc_start, time%mo_start` |
| [sym:maximum_data_module] | `db_mx` | `db_mx%atmodep` |

## Local Variables

<!-- facts:locals -->

## State Changes

| Target | When | Meaning |
| --- | --- | --- |
| `db_mx%atmodep` | When the file is missing or named `null`, it is set to 0; otherwise it is set to the station count read from `atmodep.cli`. | This value records how many atmospheric deposition stations are available for the run so the rest of the model can size and validate deposition-related processing. |
| `atmodep_cont%ts` | When a yearly or monthly deposition start record matches the simulation start time, the routine sets `atmodep_cont%ts` to the matching index. | This stores the offset into the deposition series where the simulation should begin reading values. |
| `atmodep_cont%first` | When the searched simulation start year or month is found inside the deposition series, the routine changes `atmodep_cont%first` from 1 to 0. | This marks that the initial alignment search succeeded and the deposition series is no longer on its first pass. |
| `atmo_n(iadep)` | For each station record read from `atmodep.cli`, the routine sets `atmo_n(iadep)` equal to the station name just read. | This mirrors the station names into a separate character array used elsewhere as a compact list of atmospheric deposition station identifiers. |

## File I/O

<!-- facts:io -->


## Lineage

Two source-backed commits were resolved for `cli_read_atmodep`. The initial commit `df07e3f` introduced the routine with file existence checking, control-record parsing, time alignment, station allocation, data reads, and `db_mx%atmodep` assignment. Commit `39fabde` kept the logic but initialized the local scalars and changed the monthly and yearly array allocations to use `source = 0.` so the newly allocated deposition arrays start with zero values.

- df07e3f added the routine and its full read flow for atmospheric deposition input, including the shared control state and station arrays.
- 39fabde made the temporary locals explicitly initialized and zero-filled the monthly/yearly deposition arrays at allocation time.

## Review Notes

- Direct file I/O exists; verify file meanings and units before finalizing.
- warning: missing_doc: Procedure 'cli_read_atmodep' has no extracted documentation comment.
