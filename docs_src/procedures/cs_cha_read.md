---
kind: procedure
symbol: cs_cha_read
title: cs_cha_read
status: filled
source_hash: da699246c2d4fa2d
version_label: SWAT+ 62.0.0
locals:
  titldum: A scratch line buffer used to read and discard header or name rows while scanning
    `cs_channel.ini` and `cs_streamobs`.
  header: A second scratch buffer for the labeled header line in `cs_channel.ini`; it is read
    to step past the file’s heading before data rows are counted and loaded.
  eof: I/O status flag from `read(...,iostat=eof)` that signals end-of-file or other read
    termination while scanning the input files.
  imax: Counts how many channel-constituent initialization records are present in `cs_channel.ini`,
    and is then used as the allocation size for `cs_cha_ini`.
  i_exist: Logical result from `inquire(file=...,exist=i_exist)` that tells whether `cs_channel.ini`
    or `cs_streamobs` exists before the routine proceeds.
  ics: Loop index used when allocating the concentration array for each channel record in
    `cs_cha_ini`.
  i: Loop index used to read each selected stream-observation channel number into `cs_str_obs`.
  icsi: Loop index used to read each channel name and concentration vector from `cs_channel.ini`
    into `cs_cha_ini`.
uses:
  constituent_mass_module: This module owns the channel constituent initialization array and
    the daily-output selection state that `cs_cha_read` fills. `cs_db%num_cs` supplies the
    number of constituent values to allocate for each channel, `cs_cha_ini` stores the per-channel
    names and concentrations read from `cs_channel.ini`, and `cs_str_obs`, `cs_str_nobs`,
    and `cs_obs_file` control and retain the optional daily stream-observation channel list.
  input_file_module: '`cs_cha_read` uses `inquire(file=...,exist=i_exist)` to test whether
    the configured input files are present before attempting to open them. The imported file-input
    state matters because the routine’s control flow depends on whether those files exist.'
  maximum_data_module: '`db_mx%cs_cha_ini` records how many channel initial-condition rows
    were found in `cs_channel.ini`. That maximum-count metadata is used by the model to track
    how much `cs_cha_ini` storage was populated.'
  channel_data_module: This module is imported by the routine and is part of the channel-data
    context that the loaded constituent initial conditions apply to. Its channel-related state
    matters because the concentrations being read are for channels, not generic constituents.
  hydrograph_module: The routine prepares channel-related constituent inputs that will later
    be carried with routed flow and daily channel outputs. Hydrologic state matters because
    these concentrations are meant to align with channel simulation and output workflows.
  sd_channel_module: The routine is part of the channel setup sequence, and this module provides
    channel-domain state that the constituent initialization must be consistent with. That
    matters because the loaded concentrations are tied to channel simulation state.
  organic_mineral_mass_module: Channel constituent initialization feeds the broader mass-transport
    system. This module matters because the concentrations read here are part of the model’s
    mass state that downstream transport and output routines depend on.
---

<!-- facts:header -->

Reads channel constituent initial concentrations from `cs_channel.ini` and, if enabled, channel selection data from `cs_streamobs`. It also writes a small `cs_streamobs_output` header file that lists the selected channels and output column meanings.

## Bottom Line

`cs_cha_read` is a setup routine for channel constituent mass data. It counts and loads initial constituent concentrations for channels from `cs_channel.ini`, stores the count in `db_mx%cs_cha_ini`, and allocates/populates `cs_cha_ini` with each constituent name and concentration list.

If daily channel output is enabled through `cs_obs_file`, the routine also reads the channel list from `cs_streamobs`, stores that list in `cs_str_obs`, and creates `cs_streamobs_output` with human-readable column labels for downstream daily output.

## Arguments

<!-- facts:arguments -->

## Where It Fits

`cs_cha_read` runs during model initialization after the constituent-count database and input-file state are available, because it needs `cs_db%num_cs` to size each channel concentration vector and `cs_obs_file` to decide whether daily channel-output selection should be loaded. It prepares `db_mx%cs_cha_ini`, `cs_cha_ini`, `cs_str_nobs`, and `cs_str_obs`, which later channel-constituent simulation and daily output routines depend on.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. Initialize local flags and counters | The routine declares scratch strings, counters, and the file-existence flag, then sets `eof` to zero so later reads can use it as an I/O status indicator. |
| 2. Check for the channel initial-condition file | It tests whether `cs_channel.ini` exists and only enters the file-reading block when the file is present or the configured name is not the null placeholder. |
| 3. Open and scan `cs_channel.ini` | The routine opens `cs_channel.ini`, reads past the title and header lines, then loops through the remaining records with `titldum` to count how many channel initialization rows are present. |
| 4. Store the counted record total | It copies the counted record total into `db_mx%cs_cha_ini` so the model’s maximum-data bookkeeping knows how many channel initial-condition entries were read. |
| 5. Allocate channel initial-condition storage | The routine allocates `cs_cha_ini(imax)` and then allocates each `cs_cha_ini(ics)%conc` array to length `cs_db%num_cs`, initializing concentrations to zero. |
| 6. Rewind and reload the channel data | After rewinding `cs_channel.ini`, it rereads the title and header lines and then loads each channel name plus concentration vector into `cs_cha_ini(icsi)`. |
| 7. Close the channel input file | It closes `cs_channel.ini` once all channel initialization records have been loaded. |
| 8. Check whether daily channel output is enabled | The routine queries `cs_streamobs` for existence but only proceeds with the stream-observation list when `cs_obs_file == 1`. |
| 9. Read selected stream-observation channels | It opens `cs_streamobs`, skips the first line, reads `cs_str_nobs`, allocates `cs_str_obs`, loads each selected channel number, and then closes the file. |
| 10. Write the stream-observation descriptor file | When daily output is enabled, it opens `cs_streamobs_output` and writes a title, explanatory column labels, and the selected channel list so downstream output has a readable header. |
| 11. Return to the caller | The subroutine ends after all available constituent and stream-observation setup is complete. |

## Modules Used

<!-- facts:uses -->

| Module | State touched | Key components |
| --- | --- | --- |
| [sym:constituent_mass_module] | `cs_cha_ini, cs_db, cs_str_obs, cs_obs_file, cs_str_nobs` | `cs_cha_ini(ics)%conc, cs_db%num_cs, cs_cha_ini(icsi)%name, cs_cha_ini(icsi)%conc` |
| [sym:input_file_module] | `input file state and file-control helpers used to locate configured input files` | `i_exist` |
| [sym:maximum_data_module] | `db_mx` | `db_mx%cs_cha_ini` |
| [sym:channel_data_module] | `channel state and channel indexing data` | `none resolved` |
| [sym:hydrograph_module] | `hydrologic routing state` | `none resolved` |
| [sym:sd_channel_module] | `specialized channel-state data for the model` | `none resolved` |
| [sym:organic_mineral_mass_module] | `organic and mineral mass state used by constituent transport` | `none resolved` |

## Local Variables

<!-- facts:locals -->

## State Changes

| Target | When | Meaning |
| --- | --- | --- |
| `db_mx%cs_cha_ini` | When `cs_channel.ini` is present and successfully scanned, and before the file is closed | The routine updates the stored maximum count of channel constituent initialization records to the number of data rows found in `cs_channel.ini`. |

## File I/O

<!-- facts:io -->


## Lineage

Two source-backed lineage commits were resolved. The original file was introduced in `df07e3f` with the full channel-constituent reader and stream-observation output header logic. Commit `39fabde` did not change the routine’s control flow, but it initialized local scalars (`titldum`, `header`, `eof`, `imax`, `ics`, `i`, `icsi`) and changed the allocations to zero-initialize `cs_cha_ini(ics)%conc` and `cs_str_obs` with `source = 0`.

- `df07e3f` added `cs_cha_read` as a new setup routine that reads `cs_channel.ini`, stores the count in `db_mx%cs_cha_ini`, loads `cs_cha_ini`, and optionally reads `cs_streamobs` before writing `cs_streamobs_output`.
- `39fabde` improved initialization safety by giving the local scratch variables default values and by zero-filling the allocated concentration and stream-observation arrays.

## Review Notes

- Direct file I/O exists; verify file meanings and units before finalizing.
- warning: missing_doc: Procedure 'cs_cha_read' has no extracted documentation comment.
- input_file_module is imported but no specific symbol ownership was resolved from the packet beyond file-existence checking via inquire.
- channel_data_module, hydrograph_module, sd_channel_module, and organic_mineral_mass_module were imported but no direct symbol references were resolved in the packet; their role is inferred from the routine’s channel-constituent setup context.
- algorithm_steps revised: combined the draft’s overlapping count/read/allocate phases into a line-faithful sequence matching the source flow and added the return step explicitly.
- `cs_obs_file` is checked to gate the optional stream-observation setup, but the routine also performs `inquire(file="cs_streamobs",exist=i_exist)` without using `i_exist` in that branch; preserve this behavior as written.
- The source shows unit 107 reused for both `cs_channel.ini` and `cs_streamobs`; this is intentional in the routine but worth noting for documentation.
