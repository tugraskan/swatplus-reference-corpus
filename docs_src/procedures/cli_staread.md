---
kind: procedure
symbol: cli_staread
title: cli_staread
status: filled
source_hash: c6fc21f9e26e6cad
version_label: SWAT+ 62.0.0
locals:
  titldum: Temporary 80-character scratch field used to read and skip title/data lines while
    counting and then rereading the file.
  header: Temporary 80-character scratch field used to read the file header line during the
    initial scan and rewind pass.
  eof: Iostat/status flag for each read from unit 107; negative values signal end-of-file
    or read failure and stop processing.
  imax: Counts how many weather-station records are present so the routine can size `wst`
    and `wst_n` before loading them.
  iwgn: Holds the weather-generator index pulled from the station record so the routine can
    initialize `tlag` from the matched generator data.
  i_exist: Logical existence check for `in_cli%weat_sta`; it controls whether the routine
    reads the configured file or falls back to minimal default allocation.
  i: Loop counter for the second pass that rereads each weather-station record and fills station
    state.
uses:
  input_file_module: The routine gets the climate list filename from `in_cli%weat_sta`, so
    `input_file_module` determines which file is opened or whether the name is the sentinel
    `null`.
  maximum_data_module: '`db_mx` provides the maximum-count bookkeeping that this routine updates
    or tests to size weather-station storage and to decide which linked climate file categories
    need name resolution.'
  climate_module: The weather-station and file-name arrays in `climate_module` are the target
    storage for parsed station names, linked codes, derived precipitation timing, and generator-based
    temperature lag values.
  time_module: '`time%step` controls the allocation length of subdaily precipitation arrays
    for each station, so it determines how much state is created per station.'
  hydrograph_module: '`iwst` is the shared hydrograph/weather-station index used elsewhere
    in the model, so this routine relies on the same station indexing convention when climate
    state is later consumed.'
---

<!-- facts:header -->

Reads the weather-station climate list file and builds the station lookup/state used by climate initialization.

## Bottom Line

cli_staread opens the configured weather-station list file (`weather-sta.cli` by default), counts the station records, allocates the station arrays, and reads each station name plus its code references into `climate_module` state.

It also resolves each station's linked weather generator and gage/file names against the corresponding climate file-name arrays, sets derived fields such as precipitation time-step count and temperature lag defaults, and logs missing references when a configured name cannot be matched.

## Arguments

<!-- facts:arguments -->

## Where It Fits

This routine runs during the read/setup phase inside `proc_read`, immediately after `cli_read_atmodep` and before later database and soil/plant initialization. Its results populate the shared climate-station tables and linked file indices that later weather, precipitation, temperature, humidity, wind, PET, and atmospheric deposition processing depends on.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. Initialize counters and check whether the weather-station file exists | Reset the end-of-file and record-count trackers, inquire on `in_cli%weat_sta`, and if the file is missing or explicitly set to `"null"`, allocate minimal placeholder station arrays instead of reading records. |
| 2. Scan the file once to count station records | Open unit 107 on the configured file, skip the title and header, then read through the remaining records to increment `imax` for each station entry found. |
| 3. Store the station count in shared maximum-data state | Copy the counted station total into `db_mx%wst` so the rest of the model knows how many weather stations were loaded. |
| 4. Allocate station arrays and per-station daily state | Allocate `wst` and `wst_n` to the counted size, then for each station allocate subdaily precipitation arrays using `time%step`, initialize precipitation history to `"dry"`, allocate a 6-element temperature lag vector, and seed that lag from the associated weather generator monthly values. |
| 5. Rewind the file and prepare for record loading | Rewind unit 107 and reread the title and header lines so the second pass starts from the first station record. |
| 6. Load each station record and copy the station name | Loop over each expected station, read and backspace over a scratch record to align on the full data row, then read the station name and character code block into `wst(i)%name` and `wst(i)%wco_c`; copy the name into `wst_n(i)`. |
| 7. Resolve linked weather-generator and gage references | For each optional climate file category, call `search` when the corresponding maximum count is positive to translate the character file name into an integer index, then write a missing-file message when a referenced category is not found and is not marked as simulated or null. |
| 8. Stop after the first successful pass through all station records | Exit the file-reading loop once the station records have been processed without hitting an error. |
| 9. Close the station list file | Close unit 107 and return to the caller. |

## Modules Used

<!-- facts:uses -->

| Module | State touched | Key components |
| --- | --- | --- |
| [sym:input_file_module] | `in_cli` | `in_cli%weat_sta` |
| [sym:maximum_data_module] | `db_mx` | `db_mx%wst, db_mx%wgnsta, db_mx%pcpfiles, db_mx%tmpfiles, db_mx%slrfiles, db_mx%rhfiles, db_mx%wndfiles, db_mx%petfiles, db_mx%atmodep` |
| [sym:climate_module] | `wst, wgn, wst_n, wgn_n, pcp_n, tmp_n, slr_n, hmd_n, wnd_n, petm_n, atmo_n, atmodep` | `wst(iwst)%weat%ts, wst(iwst)%weat%ts_next, wst(iwst)%weat%precip_prior_day, wst(iwst)%tlag(6), wst(iwst)%wco%wgn, wst(iwst)%tlag, wgn(iwgn)%tmpmn(1), wgn(iwgn)%tmpstdmx(1), wst(i)%name, wst(i)%wco_c, wst(i)%wco_c%wgn, wst(i)%wco%wgn, wst(i)%wco_c%pgage, wst(i)%wco%pgage, wst(i)%pcp_ts, wst(i)%wco_c%tgage, wst(i)%wco%tgage, wst(i)%wco_c%sgage, wst(i)%wco%sgage, wst(i)%wco_c%hgage, wst(i)%wco%hgage, wst(i)%wco_c%wgage, wst(i)%wco%wgage, wst(i)%wco_c%petgage, wst(i)%wco%petgage, wst(i)%wco_c%atmodep, wst(i)%wco%atmodep` |
| [sym:time_module] | `time` | `time%step` |
| [sym:hydrograph_module] | `iwst` |  |

## Local Variables

<!-- facts:locals -->

## State Changes

| Target | When | Meaning |
| --- | --- | --- |
| `db_mx%wst` | When the configured weather-station list exists and is not `"null"`, after the first pass counts records. | `db_mx%wst` is set to the number of station records found in `weather-sta.cli`, which later controls the station-array allocation and downstream climate loops. |
| `wst(iwst)%weat%precip_prior_day` | For each allocated station during the initialization loop, before the file is reread for full record loading. | `wst(iwst)%weat%precip_prior_day` is initialized to `"dry"` so each station starts with a neutral previous-day precipitation state. |
| `wst(iwst)%tlag` | For each allocated station during the initialization loop after `iwgn` is taken from the station's weather-generator code. | `wst(iwst)%tlag` is allocated to six days and filled with the average of the matched generator's first monthly minimum and maximum temperature values. |
| `wst_n(i)` | After the file's station count is known and before per-station data are read. | `wst_n(i)` is allocated alongside `wst` so the routine can store each station name separately from the structured station record. |
| `wst(i)%pcp_ts` | For each station as it is initialized from the loaded records. | `wst(i)%pcp_ts` is populated from the matched precipitation file's time-step metadata so later precipitation handling knows whether the station is daily or subdaily. |

## File I/O

<!-- facts:io -->


## Lineage

`cli_staread.f90` was introduced in `df07e3f` (2024-03-05, "init all") and has been changed in 6 non-merge commit(s) since, most recently `b9df6cf` (2026-04-01, "gwflow re-merge: host file guards, ch_temp component mixing restoration"). Lineage is reconstructed from commit metadata (SHA, date, subject); per-line diffs were unavailable in this build environment, so only the commits touching `cli_staread.f90` are listed.

- `b9df6cf` (2026-04-01) — gwflow re-merge: host file guards, ch_temp component mixing restoration
- `bd18ad4` (2025-11-24) — Pr 107 (#108)
- `39fabde` (2024-08-08) — Initialized varables with python script, corrected input data where integers where floats in two input files, trapped underflow errors in th…
- `f8bb6ec` (2024-07-25) — Manually coded init changes
- `c7c8e22` (2024-05-30) — Added latest source code from bitbucket
- `df07e3f` (2024-03-05) — init all

## Review Notes

- Direct file I/O exists; verify file meanings and units before finalizing.
- warning: missing_doc: Procedure 'cli_staread' has no extracted documentation comment.
- algorithm_steps revised: split the original scan/allocate/read summary into nine source-backed steps to match the file's two-pass read and per-station initialization logic.
- Source appears to contain a typographical spacing quirk at line 89 (`db_mx% petfiles`); the overlay describes the intended `db_mx%petfiles` dependency from the surrounding context.
- Lineage was reconstructed from file-level commit metadata; per-line diffs were unavailable in this environment (blobless clone), so line-span filtering was not applied.
