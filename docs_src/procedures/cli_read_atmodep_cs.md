---
kind: procedure
symbol: cli_read_atmodep_cs
title: cli_read_atmodep_cs
status: filled
source_hash: dab49cfba6f8e3fa
version_label: SWAT+ 62.0.0
locals:
  eof: End-of-file status flag initialized to 0, but not used in the visible source to control
    reading.
  iadep: Loop counter over atmospheric deposition stations; selects which `atmodep_cs(iadep)`
    record is being filled.
  imo: Loop counter over month positions when reading monthly wet or dry deposition arrays.
  iyr: Loop counter over year positions when reading yearly wet or dry deposition arrays.
  i_exist: Logical flag set by `inquire` to indicate whether `cs_atmo.cli` is present before
    attempting to open it.
  ics: Loop counter over simulated constituents; selects which constituent entry within each
    station is read or allocated.
  station_name: Temporary holder for the station-name field read from `cs_atmo.cli` before
    the numeric deposition values for that station.
uses:
  basin_module: The source shows `use basin_module`, but no resolved symbols from it were
    extracted in the packet. It matters because the routine depends on shared basin-level
    model state being available in the program unit, even though the specific basin symbols
    used here were not resolved from the evidence.
  input_file_module: The routine imports `input_file_module`, but no resolved symbols from
    that module were extracted. It matters because this reader is part of the centralized
    input-file workflow, so the module connection is relevant even if the exact file-control
    symbol was not identified from the packet.
  climate_module: This module provides the shared atmospheric-deposition control and storage
    that this reader fills. `atmodep_cont` supplies the station count, timestep, and record
    count that determine the read pattern, `atmodep_cs` is the target array populated for
    each station and constituent, and `cs_atmo` is the flag set when constituent atmospheric
    deposition input is found.
  time_module: The source imports `time_module`, but no specific symbols were resolved from
    it in the packet. It still matters because this reader branches on timestep-dependent
    input layouts (`aa`, `mo`, `yr`), so time-related model state is part of the surrounding
    dependency set even if the exact imported names were not extracted.
  maximum_data_module: The routine imports `maximum_data_module`, but no concrete symbols
    were resolved from it in the packet. It matters as part of the model-wide sizing context
    used by input readers, even though the exact maximum-data symbol was not identified here.
  constituent_mass_module: This module provides `cs_db%num_cs`, the count of simulated constituent
    substances. The routine uses that count to decide whether to process `cs_atmo.cli` at
    all and how many constituent records to allocate and read for each station.
---

<!-- facts:header -->

Reads atmospheric deposition inputs for simulated constituent substances from `cs_atmo.cli`. It sizes per-station/per-constituent storage and loads wet and dry deposition values for annual, monthly, or yearly timestep formats.

## Bottom Line

This routine runs only when constituents are being simulated (`cs_db%num_cs > 0`) and `cs_atmo.cli` exists. It marks constituent atmospheric deposition input as present, opens the file, skips the header lines, and then reads deposition data station by station into the shared `atmodep_cs` structure.

The file format depends on `atmodep_cont%timestep`: annual mode reads one wet concentration and one dry deposition value per constituent, monthly mode reads arrays of monthly wet and dry values, and yearly mode reads arrays of yearly wet and dry values. The data loaded here is used later by the climate/deposition workflow wherever constituent atmospheric deposition is applied.

## Arguments

<!-- facts:arguments -->

## Where It Fits

This reader is called from `proc_read` during the model input phase, after other constituent-related input readers have already run and established the counts and control values it needs. Its results populate the atmospheric-deposition constituent arrays that later climate and deposition calculations can use during simulation.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. Require simulated constituents and locate the file | The routine first checks whether any constituent substances are being simulated (`cs_db%num_cs > 0`). If so, it tests for `cs_atmo.cli` with `inquire`; when the file exists it sets `cs_atmo = "y"` to record that constituent atmospheric deposition input is present. |
| 2. Open the deposition input file and skip its header | The routine opens unit 5050 on `cs_atmo.cli` and reads three records without using them, which skips the file commentary or header lines before the data section. |
| 3. Allocate station-level deposition storage | It allocates the `atmodep_cs` array for all stations using `atmodep_cont%num_sta`, then allocates each station's constituent array to the number of simulated constituents in `cs_db%num_cs`. |
| 4. Read annual constituent deposition values when timestep is annual | If `atmodep_cont%timestep == "aa"`, the routine reads a station name and then reads one wet concentration (`rf`) and one dry deposition value (`dry`) per constituent for that station. |
| 5. Read monthly constituent deposition arrays when timestep is monthly | If `atmodep_cont%timestep == "mo"`, the routine reads a station name, allocates monthly wet and dry arrays sized by `atmodep_cont%num`, and then reads one full monthly series for each constituent into `rfmo` and `drymo`. |
| 6. Read yearly constituent deposition arrays when timestep is yearly | If `atmodep_cont%timestep == "yr"`, the routine reads a station name, allocates yearly wet and dry arrays sized by `atmodep_cont%num`, and then reads one full yearly series for each constituent into `rfyr` and `dryyr`. |
| 7. Finish the station loop and close the file | After all stations are processed, the routine exits the file-present block, closes unit 5050, and returns to the caller. |

## Modules Used

<!-- facts:uses -->

| Module | State touched | Key components |
| --- | --- | --- |
| [sym:basin_module] | `basin_module` |  |
| [sym:input_file_module] | `input_file_module` |  |
| [sym:climate_module] | `atmodep_cont, atmodep_cs, cs_atmo` | `atmodep_cont%num_sta, atmodep_cs(iadep)%cs, atmodep_cont%timestep, atmodep_cs(iadep)%cs(ics)%rfmo, atmodep_cont%num, atmodep_cs(iadep)%cs(ics)%drymo, atmodep_cs(iadep)%cs(ics)%rfyr, atmodep_cs(iadep)%cs(ics)%dryyr` |
| [sym:time_module] | `time_module` |  |
| [sym:maximum_data_module] | `maximum_data_module` |  |
| [sym:constituent_mass_module] | `cs_db` | `cs_db%num_cs` |

## Local Variables

<!-- facts:locals -->

## State Changes

| Target | When | Meaning |
| --- | --- | --- |
| `cs_atmo` | When `cs_db%num_cs > 0` and `cs_atmo.cli` exists. | `cs_atmo` changes from its default "n" to "y" to mark that constituent atmospheric deposition input has been found and loaded. |

## File I/O

<!-- facts:io -->


## Lineage

The procedure was introduced in df07e3f as a new reader for constituent atmospheric deposition input. Subsequent changes initialized local variables more defensively in 39fabde, then 2ee1889 removed unused local declarations, and f1e61a3 made formatting-only whitespace cleanup. The later diffs in the resolved lineage do not show behavioral changes to the read logic itself.

- df07e3f added the entire `cli_read_atmodep_cs` routine and its file-reading/allocation logic for constituent atmospheric deposition input.
- 39fabde initialized local variables such as `eof`, `iadep`, `imo`, `iyr`, `ics`, and `station_name`, and added `source = 0.` to the monthly and yearly array allocations shown in the diff.
- 2ee1889 removed unused local declarations (`file`, `titldum`, `header`, `imo_atmo`, `iyrc_atmo`) without changing the read logic.
- f1e61a3 only adjusted whitespace in the source file.

## Review Notes

- Direct file I/O exists; verify file meanings and units before finalizing.
- warning: missing_doc: Procedure 'cli_read_atmodep_cs' has no extracted documentation comment.
- algorithm_steps revised: collapsed the draft into 7 source-backed steps aligned to the visible control flow.
- The packet resolves `basin_module`, `input_file_module`, `time_module`, and `maximum_data_module` only as imports; no specific symbols from those modules were extracted, so their `outside` fields are left empty.
