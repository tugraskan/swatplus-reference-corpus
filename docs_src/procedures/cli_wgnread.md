---
kind: procedure
symbol: cli_wgnread
title: cli_wgnread
status: filled
source_hash: 208c1ad66c260d30
version_label: SWAT+ 62.0.0
locals:
  titldum: Scratch text buffer used to read and skip title or separator lines from `weather-wgn.cli`
    before the actual station data fields are consumed.
  header: Scratch text buffer for a header line in each station block; the routine reads it
    and discards it while stepping through the file format.
  iwgn: Loop index for the current weather-generator station being counted or loaded from
    the file.
  eof: I/O status flag used on reads from unit 114; negative values signal end-of-file and
    control when scanning or loading stops.
  imax: Counter that accumulates how many weather-generator station records are present in
    `weather-wgn.cli`; that count is later used to size the climate arrays.
  i_exist: Logical flag set by `inquire` to show whether the configured weather-generator
    file exists before the routine tries to read it.
  mo: Month index used while reading the 12 monthly climate rows for each station.
uses:
  input_file_module: '`in_cli%weat_wgn` supplies the configured path to the weather-generator
    input file, and the routine uses it both to test whether the file exists and to open the
    file for reading.'
  time_module: '`time%step` determines the second dimension of `frad`, so the routine needs
    the current simulation time-step setting to allocate the fractional radiation array at
    the correct resolution.'
  maximum_data_module: '`db_mx%wgnsta` stores the counted number of weather-generator stations
    after the scan; that shared maximum is how later climate code knows how many station records
    were loaded.'
  climate_module: '`climate_module` holds the weather-generator database and related random/climate
    state that this routine populates: station names in `wgn_n`, station records in `wgn`,
    copied originals in `wgn_orig`, derived parameters in `wgncur`, `wgnold`, and `wgn_pms`,
    and the random-seed arrays `rnd2`, `rnd3`, `rnd8`, `rnd9`, `rndseed`, and `idg` that climate
    initialization depends on.'
---

<!-- facts:header -->

Reads weather generator station data from `weather-wgn.cli` and loads it into climate module arrays. If the file is missing or set to `null`, it initializes a minimal default weather-generator state instead.

## Bottom Line

`cli_wgnread` is the climate-file loader for SWAT+ weather generator stations. It either builds a small default climate state when the configured file is absent or disabled, or it scans `weather-wgn.cli`, counts station records, allocates the weather-generator arrays, and reads each station's monthly climate parameters into `climate_module`.

After loading the station data, it calls `cli_initwgn` for each station so derived weather-generator parameters are computed and the climate state is ready for later simulation routines.

## Arguments

<!-- facts:arguments -->

## Where It Fits

This routine runs during initialization in `proc_date_time`, right after the date/time logging around weather-generator setup. Its results prepare the shared climate database that later weather and climate routines use when generating station-based weather inputs.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. Initialize counters and test the configured file | The routine clears `eof` and `imax`, then checks whether the configured weather-generator file exists and is not set to `null`. |
| 2. Build a minimal default climate state when no file is available | If the file is missing or disabled, it allocates one-element placeholder arrays for the weather-generator state, initializes the random arrays to zero, and calls `gcycl` to set up the seed mapping. |
| 3. Open the weather-generator file and start a scan pass | Otherwise the routine opens `weather-wgn.cli` on unit 114 and begins reading the file from the top to count station records. |
| 4. Count station blocks to determine array sizes | It loops through the file structure, skipping title/header lines and 12 monthly rows per station, incrementing `imax` once per station block. |
| 5. Save the station count for shared use | The counted station total is stored in `db_mx%wgnsta` so other modules know how many weather-generator stations were loaded. |
| 6. Allocate climate and random-state arrays | Using `imax` and `time%step`, it allocates the weather-generator records, names, parameter arrays, hourly radiation array, and random-number arrays, then zeroes the working state. |
| 7. Rewind and prepare for the data pass | The file is rewound, the initial title line is read again, and `gcycl` is called before station data are loaded. |
| 8. Read each station record and monthly climate data | For each station, it reads the station metadata row, the station header line, and then 12 monthly rows of temperature, precipitation, storm, solar, dewpoint, and wind statistics. |
| 9. Initialize derived weather-generator parameters | After each station is read, it calls `cli_initwgn(iwgn)` so the station's derived weather-generator parameters are computed. |
| 10. Finish file handling | The scan loop exits after successful loading and the routine closes unit 114. |

## Modules Used

<!-- facts:uses -->

| Module | State touched | Key components |
| --- | --- | --- |
| [sym:input_file_module] | `in_cli` | `in_cli%weat_wgn` |
| [sym:time_module] | `time` | `time%step` |
| [sym:maximum_data_module] | `db_mx` | `db_mx%wgnsta` |
| [sym:climate_module] | `wgn_n, wgn, wgn_orig, wgncur, wgnold, wgn_pms, frad, rnd2, rnd3, rnd8, rnd9, rndseed, idg` | `wgn(iwgn)%long, wgn(iwgn)%elev, wgn(iwgn)%rain_yrs, wgn(iwgn)%tmpmx(mo), wgn(iwgn)%tmpmn(mo), wgn(iwgn)%tmpstdmx(mo), wgn(iwgn)%tmpstdmn(mo), wgn(iwgn)%pcpmm(mo), wgn(iwgn)%pcpstd(mo), wgn(iwgn)%pcpskw(mo), wgn(iwgn)%pr_wd(mo), wgn(iwgn)%pr_ww(mo), wgn(iwgn)%pcpd(mo), wgn(iwgn)%rainhmx(mo), wgn(iwgn)%solarav(mo), wgn(iwgn)%dewpt(mo), wgn(iwgn)%windav(mo)` |

## Local Variables

<!-- facts:locals -->

## State Changes

| Target | When | Meaning |
| --- | --- | --- |
| `wgncur` | When the routine allocates the default 0:1 station arrays or the full `1:db_mx%wgnsta` arrays, and then zeroes them. | `wgncur` is reset and sized for weather-generator use so later climate routines start from a clean current-state buffer. |
| `wgnold` | When the routine allocates the default 0:1 station arrays or the full `1:db_mx%wgnsta` arrays, and then zeroes them. | `wgnold` is reset and sized as the previous-state buffer for weather-generator calculations used later in the climate workflow. |
| `db_mx%wgnsta` | After the file scan completes and `imax` has been counted from the station blocks. | `db_mx%wgnsta` is updated to the number of weather-generator stations found in `weather-wgn.cli`, making that count available to other modules. |
| `rnd2` | When the default or full climate random arrays are allocated and initialized to zero. | `rnd2` is created as the stream-2 random-number buffer used later by climate generation. |
| `rnd3` | When the default or full climate random arrays are allocated and initialized to zero. | `rnd3` is created as the stream-3 random-number buffer used later by climate generation. |
| `rnd8` | When the default or full climate random arrays are allocated and initialized to zero. | `rnd8` is created as the stream-8 random-number buffer used later by climate generation. |
| `rnd9` | When the default or full climate random arrays are allocated and initialized to zero. | `rnd9` is created as the stream-9 random-number buffer used later by climate generation. |
| `rndseed` | When the default or full climate random arrays are allocated and initialized to zero. | `rndseed` is created or reset as the seed table that `gcycl` and later climate routines use for weather-generation random streams. |

## File I/O

<!-- facts:io -->


## Lineage

`cli_wgnread.f90` was introduced in `df07e3f` (2024-03-05, "init all") and has been changed in 4 non-merge commit(s) since, most recently `bd18ad4` (2025-11-24, "Pr 107 (#108)"). Lineage is reconstructed from commit metadata (SHA, date, subject); per-line diffs were unavailable in this build environment, so only the commits touching `cli_wgnread.f90` are listed.

- `bd18ad4` (2025-11-24) — Pr 107 (#108)
- `39fabde` (2024-08-08) — Initialized varables with python script, corrected input data where integers where floats in two input files, trapped underflow errors in th…
- `c7c8e22` (2024-05-30) — Added latest source code from bitbucket
- `df07e3f` (2024-03-05) — init all

## Review Notes

- Direct file I/O exists; verify file meanings and units before finalizing.
- warning: missing_doc: Procedure 'cli_wgnread' has no extracted documentation comment.
- Lineage was reconstructed from file-level commit metadata; per-line diffs were unavailable in this environment (blobless clone), so line-span filtering was not applied.
