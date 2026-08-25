---
kind: procedure
symbol: cli_read_atmodep_salt
title: cli_read_atmodep_salt
status: filled
source_hash: a16b7fe0b0ce2cb8
version_label: SWAT+ 62.0.0
locals:
  salt_ion: Temporary 4-character label read from each data row in `salt_atmo.cli`; it identifies
    the salt ion name or code associated with the value(s) on that row.
  station_name: Temporary station label read from the file header for each station block;
    the routine reads it before loading that station’s salt deposition series.
  eof: Declared end-of-file indicator, but it is only initialized and not used in the extracted
    source.
  iadep: Loop counter over atmospheric deposition stations in `atmodep_salt`, from 1 to `atmodep_cont%num_sta`.
  imo: Loop counter over monthly deposition positions when filling `rfmo` and `drymo` arrays.
  iyr: Loop counter over yearly deposition positions when filling `rfyr` and `dryyr` arrays.
  i_exist: Logical flag set by `inquire` to test whether `salt_atmo.cli` exists before the
    file is opened and parsed.
  isalt: Loop counter over salt ions for each station, from 1 to `cs_db%num_salts`.
uses:
  basin_module: '`cs_db%num_salts` controls whether the routine does anything at all and determines
    how many salt-ion records must be read and how many per-salt storage slots must be allocated.'
  input_file_module: The file-existence test decides whether `salt_atmo.cli` is opened and
    parsed; if the file is missing, the routine leaves the salt-atmospheric deposition flag
    unchanged and skips data loading.
  climate_module: '`climate_module` provides the shared atmospheric-deposition control and
    storage that this routine populates. `atmodep_cont%num_sta` sets the station loop bound,
    `atmodep_cont%timestep` selects annual/monthly/yearly parsing, `atmodep_cont%num` sets
    the number of monthly or yearly values to read, `atmodep_salt(iadep)%salt` is the per-station/per-salt
    storage being allocated and filled, and `salt_atmo` is the module flag set to indicate
    that salt atmospheric deposition input was found.'
  time_module: '`time_module` matters because the deposition file format is organized by timestep,
    and this routine branches on the current time resolution to decide whether to read average
    annual, monthly, or yearly deposition arrays.'
  maximum_data_module: '`maximum_data_module` matters because it supplies the configured limits
    used to size the deposition data structures; the routine allocates storage based on the
    maximum number of stations and time slices it must hold.'
  constituent_mass_module: '`constituent_mass_module` provides `cs_db%num_salts`, which is
    the simulation-wide count of salt ions. That count determines whether salt atmospheric
    deposition should be read and how many salt records to expect per station.'
---

<!-- facts:header -->

Reads the salt atmospheric deposition control file and loads wet/dry salt deposition values for each station and salt ion.

## Bottom Line

`cli_read_atmodep_salt` is a file-reader for `salt_atmo.cli`. If the simulation includes salt ions, it checks whether the file exists, marks salt-atmospheric deposition as enabled, and then loads station-by-station deposition data into `atmodep_salt` for the timestep requested in `atmodep_cont%timestep`.

The routine supports average annual, monthly, and yearly deposition formats. It allocates per-station and per-salt arrays sized from `atmodep_cont%num_sta`, `atmodep_cont%num`, and `cs_db%num_salts`, then fills rainfall concentration and dry deposition fields that later climate/deposition code can use.

## Arguments

<!-- facts:arguments -->

## Where It Fits

This routine runs during input processing, after `proc_read` has already set the atmospheric-deposition control state that determines station count, timestep, and series length. Its populated `atmodep_salt` arrays and `salt_atmo` flag are then available to later climate/deposition calculations that use salt rainfall concentration and dry deposition inputs.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. Skip processing when there are no salt ions | The routine first checks `cs_db%num_salts`; if no salt ions are simulated, it does not attempt to read the atmospheric deposition file. |
| 2. Test whether the salt deposition file exists | It uses `inquire` to see whether `salt_atmo.cli` is present and, if so, marks the shared `salt_atmo` flag as enabled. |
| 3. Open the file and skip header commentary | It opens `salt_atmo.cli` on unit 5050 and reads past the initial non-data lines before parsing station records. |
| 4. Allocate station-level storage | It allocates `atmodep_salt(0:atmodep_cont%num_sta)` and starts a loop over all atmospheric deposition stations. |
| 5. Allocate salt storage for each station | For each station, it allocates `atmodep_salt(iadep)%salt(cs_db%num_salts)` so each salt ion has a storage slot. |
| 6. Read average-annual values when requested | If `atmodep_cont%timestep` is `aa`, the routine reads the station name and then reads wet rainfall concentration and dry deposition values for each salt ion. |
| 7. Read monthly values when requested | If `atmodep_cont%timestep` is `mo`, it reads the station name, allocates monthly wet and dry arrays sized by `atmodep_cont%num`, and fills them from the file. |
| 8. Read yearly values when requested | If `atmodep_cont%timestep` is `yr`, it reads the station name, allocates yearly wet and dry arrays sized by `atmodep_cont%num`, and fills them from the file. |
| 9. Advance to the next station and finish | After all station blocks are processed, the routine exits the conditionals, closes unit 5050, and returns to the caller. |

## Modules Used

<!-- facts:uses -->

| Module | State touched | Key components |
| --- | --- | --- |
| [sym:basin_module] | `cs_db` | `cs_db%num_salts` |
| [sym:input_file_module] | `i_exist` | `i_exist` |
| [sym:climate_module] | `atmodep_cont, atmodep_salt, salt_atmo` | `atmodep_cont%num_sta, atmodep_salt(iadep)%salt, atmodep_cont%timestep, atmodep_salt(iadep)%salt(isalt)%rfmo, atmodep_cont%num, atmodep_salt(iadep)%salt(isalt)%drymo, atmodep_salt(iadep)%salt(isalt)%rfyr, atmodep_salt(iadep)%salt(isalt)%dryyr` |
| [sym:time_module] | `atmodep_cont, atmodep_salt` | `atmodep_cont%num_sta, atmodep_cont%timestep, atmodep_cont%num, atmodep_salt(iadep)%salt(isalt)%rfmo, atmodep_salt(iadep)%salt(isalt)%drymo, atmodep_salt(iadep)%salt(isalt)%rfyr, atmodep_salt(iadep)%salt(isalt)%dryyr` |
| [sym:maximum_data_module] | `atmodep_cont, atmodep_salt` | `atmodep_cont%num_sta, atmodep_cont%num, atmodep_cont%timestep, atmodep_salt(iadep)%salt` |
| [sym:constituent_mass_module] | `cs_db` | `cs_db%num_salts` |

## Local Variables

<!-- facts:locals -->

## State Changes

| Target | When | Meaning |
| --- | --- | --- |
| `salt_atmo` | When `cs_db%num_salts > 0`, `salt_atmo.cli` exists, and the file is successfully read. | The routine sets `salt_atmo` to `"y"` to record that salt atmospheric deposition input is available and has been loaded. |

## File I/O

<!-- facts:io -->


## Lineage

The procedure was introduced in df07e3f with the full `salt_atmo.cli` reader, including file existence checking, header skipping, station allocation, and annual/monthly/yearly deposition parsing. Later commits were non-behavioral for this routine: 39fabde mainly standardized initialization and added `source = 0.` to array allocations, 2ee1889 removed unused local declarations, and f1e61a3 fixed whitespace in a comment block.

- df07e3f added the routine and its complete parsing logic for salt atmospheric deposition.
- 39fabde initialized local variables and made monthly/yearly array allocations zero-filled with `source = 0.`.
- 2ee1889 removed unused local variables `file`, `titldum`, `header`, `imo_atmo`, and `iyrc_atmo` from the routine.
- f1e61a3 only changed whitespace in the yearly section comment area; no functional behavior changed.

## Review Notes

- Direct file I/O exists; verify file meanings and units before finalizing.
- warning: missing_doc: Procedure 'cli_read_atmodep_salt' has no extracted documentation comment.
- algorithm_steps revised: reduced the draft from 4 coarse steps to 9 source-faithful steps aligned to the actual control flow and read blocks.
- The source shows `close(5050)` outside the `if(i_exist)` block, so the routine closes the unit even if the file was not opened; this is preserved in the description but may be worth reviewing.
