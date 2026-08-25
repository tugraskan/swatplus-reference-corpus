---
kind: procedure
symbol: salt_cha_read
title: salt_cha_read
status: filled
source_hash: bbbf28fbdbe6bbcc
version_label: SWAT+ 62.0.0
locals:
  titldum: Temporary character buffer used to read and discard the file title line and later
    re-read the first line when the file is rewound.
  header: Temporary character buffer used to read and discard the file header/column-description
    line before counting or loading data records.
  eof: I/O status flag from each `read`; zero means more input is available, and a negative
    value is used to stop at end-of-file.
  imax: Counter for the number of salt channel initialization records found in `salt_channel.ini`;
    later used to size `salt_cha_ini` and update `db_mx%salt_cha_ini`.
  i_exist: Logical flag from `inquire` indicating whether `salt_channel.ini` exists on disk
    before the routine attempts to read it.
  isalt: Loop index used when allocating the concentration vector for each `salt_cha_ini`
    entry.
  isalti: Loop index used when reading each salt name and concentration vector from `salt_channel.ini`
    into `salt_cha_ini`.
uses:
  constituent_mass_module: This module defines the global salt-initialization array and the
    constituent database that determines how many salt concentration values each channel record
    must store. `salt_cha_read` allocates and fills `salt_cha_ini` using `cs_db%num_salts`
    as the per-record vector size.
  input_file_module: This module is imported so the routine can use the shared input-file
    handling context while checking whether the `salt_channel.ini` input file is present before
    attempting to read it.
  maximum_data_module: This module holds the shared maximum-record counters. `salt_cha_read`
    stores the number of salt initialization rows it found into `db_mx%salt_cha_ini` so other
    routines can know the allocated size.
  channel_data_module: This module is part of the channel-state context that the salt channel
    initialization belongs to; the routine populates a channel-related initialization table
    that later channel code will consume.
  hydrograph_module: Hydrograph calculations operate on channel flow conditions that use the
    initialized channel salt state, so this module is part of the downstream context for the
    values loaded here.
  sd_channel_module: The salt initial conditions are tied to stream/channel representations
    used by the SD channel model, so this module matters to where the loaded concentrations
    will be applied later.
  organic_mineral_mass_module: This module is part of the broader constituent-mass system
    alongside salts; it matters because the salt initialization file is one of several mass-related
    initial-condition readers in the model.
---

<!-- facts:header -->

Reads initial salt concentrations for channel water from `salt_channel.ini` and loads them into the global salt-constituent database. It first counts how many records exist, then allocates storage and fills each salt name and concentration vector.

## Bottom Line

`salt_cha_read` is a file-reader/initializer for channel salt concentrations. It checks for `salt_channel.ini`, counts the data rows, sizes `db_mx%salt_cha_ini` and `salt_cha_ini`, then reads each record into the global initial-condition array.

The routine matters because later channel/salt calculations need a populated `salt_cha_ini` table and the correct number of salt initialization records. It also uses `cs_db%num_salts` to size each concentration vector so every salt ion gets an initial value slot.

## Arguments

<!-- facts:arguments -->

## Where It Fits

This routine runs during input initialization, after the salt constituent database has been set up enough to provide `cs_db%num_salts`. It prepares the salt-channel initial-condition table used later by channel constituent and transport behavior, and it updates the maximum-record counter so other routines know how many salt initialization entries exist.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. Check input file availability | The routine inquires whether `salt_channel.ini` exists and only proceeds with reading if the file is available or the configured file name test passes. |
| 2. Open the salt channel input file | It opens `salt_channel.ini` on unit 107 to begin a read pass over the file. |
| 3. Skip title and header lines | It reads the first two records into temporary variables `titldum` and `header`, which are not retained as model state. |
| 4. Count data records | It resets `imax` and loops through the remaining lines, counting each salt initialization record until end-of-file is reached. |
| 5. Save maximum record count | It stores the counted number of salt initialization rows into `db_mx%salt_cha_ini` for shared use by other model code. |
| 6. Allocate the top-level salt initialization array | It allocates `salt_cha_ini(imax)` so there is one initialization record slot for each row found in the input file. |
| 7. Allocate and zero each concentration vector | For every salt record, it allocates the `conc` array with length `cs_db%num_salts` and initializes the values to zero. |
| 8. Rewind the file for the data pass | It rewinds unit 107 so the file can be reread from the beginning. |
| 9. Reread the title and header lines | It reads the title and header a second time to position the file at the start of the data records. |
| 10. Load each salt record | It loops through the allocated slots and reads each salt name plus its full concentration vector into `salt_cha_ini(isalti)`. |
| 11. Close the file and finish | After the data are loaded, it closes unit 107, exits the open-file loop, and returns to the caller. |

## Modules Used

<!-- facts:uses -->

| Module | State touched | Key components |
| --- | --- | --- |
| [sym:constituent_mass_module] | `salt_cha_ini, cs_db` | `salt_cha_ini(isalt)%conc, cs_db%num_salts, salt_cha_ini(isalti)%name, salt_cha_ini(isalti)%conc` |
| [sym:input_file_module] | `i_exist` | `i_exist` |
| [sym:maximum_data_module] | `db_mx` | `db_mx%salt_cha_ini` |
| [sym:channel_data_module] | `none directly referenced in this routine` | `none directly referenced in this routine` |
| [sym:hydrograph_module] | `none directly referenced in this routine` | `none directly referenced in this routine` |
| [sym:sd_channel_module] | `none directly referenced in this routine` | `none directly referenced in this routine` |
| [sym:organic_mineral_mass_module] | `none directly referenced in this routine` | `none directly referenced in this routine` |

## Local Variables

<!-- facts:locals -->

## State Changes

| Target | When | Meaning |
| --- | --- | --- |
| `db_mx%salt_cha_ini` | After counting all data rows in `salt_channel.ini` and before allocating `salt_cha_ini` | The routine records the number of salt channel initialization entries found in the file so the model’s database-size metadata matches the actual input file length. |

## File I/O

<!-- facts:io -->


## Lineage

Two source-backed commits were resolved for `salt_cha_read`. The initial add in `df07e3f` introduced the full reader and its file-count / allocate / rewind / load workflow. Commit `39fabde` kept the same logic but initialized the local variables and changed the concentration allocation to zero-initialize the `conc` arrays with `source = 0.`.

- `df07e3f` added `salt_cha_read.f90` with the counting pass, allocation of `salt_cha_ini`, second-pass record loading, and `db_mx%salt_cha_ini` update.
- `39fabde` did not change the algorithm structure, but it initialized `titldum`, `header`, `eof`, `imax`, `isalt`, and `isalti`, and changed concentration allocation to zero-fill each `conc` array.

## Review Notes

- Direct file I/O exists; verify file meanings and units before finalizing.
- warning: missing_doc: Procedure 'salt_cha_read' has no extracted documentation comment.
- algorithm_steps revised: condensed the routine into 11 source-backed steps and split the scan/allocate/load phases to match the visible line structure.
- `input_file_module`, `channel_data_module`, `hydrograph_module`, `sd_channel_module`, and `organic_mineral_mass_module` are imported by the source but not directly referenced in the visible body; their relevance is inferred from module context rather than explicit symbol use.
