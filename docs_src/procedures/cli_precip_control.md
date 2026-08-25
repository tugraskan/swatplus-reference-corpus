---
kind: procedure
symbol: cli_precip_control
title: cli_precip_control
status: filled
source_hash: 2492b7753262e522
version_label: SWAT+ 62.0.0
args:
  istart: Offsets the current simulation day when looking up measured precipitation. The routine
    uses `time%day + istart` so the first call can initialize day state differently from later
    calls.
locals:
  iwgn: 'Weather-generator station index copied from `wst(iwst)%wco%wgn` and passed to `cli_pgen`/`cli_pgenhr`
    when simulated precipitation or missing data must be generated. Initial value: `0`.'
  ipg: 'Measured precipitation-gage index copied from `wst(iwst)%wco%pgage` and used to access
    `pcp(ipg)` record metadata and time series. Initial value: `0`.'
  ist: 'Subdaily time-step counter used to walk through `wst(iwst)%weat%ts_next` when precipitation
    is stored at subdaily resolution. Initial value: `0`.'
  yrs_to_start: 'Year offset from the precipitation record start year to the current simulation
    year; used to index measured daily precipitation and to detect out-of-range years. Initial
    value: `0`.'
  cur_day: 'Current day-of-year used to index measured precipitation records, adjusted by
    `istart` and wrapped to day 1 when the simulation crosses the end of the year. Initial
    value: `0`.'
  out_bounds: 'One-character flag that marks whether the current simulation date lies outside
    the measured precipitation record. Initial value: `''n''`.'
uses:
  climate_module: Provides the weather-station state and measured precipitation records that
    this routine updates or reads to build the next-day precipitation inputs.
  basin_module: No candidate outside references were resolved to this module in the provided
    evidence.
  time_module: Provides the current simulation day, year, and subdaily step count that determine
    whether precipitation is generated daily or subdaily and how measured records are indexed.
  hydrograph_module: Supplies the shared subdaily timestep array and the station loop index
    used by precipitation control and by the weather generator routines it calls.
  maximum_data_module: Provides the maximum number of weather stations so the routine can
    loop over all configured stations.
---

<!-- facts:header -->

Controls precipitation inputs for each weather station in SWAT+.

## Bottom Line

`cli_precip_control` advances each weather station's precipitation state one simulation day, either by promoting previously generated precipitation or by reading measured precipitation records and filling missing values with the weather generator. It also updates annual precipitation and potential ET accumulators used later in the climate workflow.

The routine is called from climate and time control setup code, so it sits at the point where simulation time, station metadata, and precipitation records are combined into the daily/subdaily weather state that downstream model components consume.

## Arguments

<!-- facts:arguments -->

## Where It Fits

Called during climate/time control initialization and daily stepping to prepare precipitation inputs before later weather and hydrology calculations use them. `climate_control` calls it for precipitation setup, and `time_control` calls it after initializing the simulation date so the first precipitation state is ready before the main yearly loop begins.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. Loop over stations | Iterate over every configured weather station. |
| 2. Promote prior precipitation | Move the previously generated precipitation and subdaily arrays into the current-day weather state, then clear the next-day precipitation buffer. |
| 3. Select station indices | Copy the station's weather-generator and precipitation-gage indices for use in the simulated and measured precipitation branches. |
| 4. Branch on precipitation source | Choose between simulated precipitation and measured precipitation based on the station's precipitation-gage code. |
| 5. Generate simulated precipitation | When the station is configured for simulated precipitation, call the daily generator and, for subdaily runs, call the hourly generator and sum the generated subdaily values into the next-day precipitation total. |
| 6. Check measured record bounds | For measured precipitation, compute the current record day and year offset, wrap the day at year end, and flag the record as out of bounds when the simulation extends beyond the available data range. |
| 7. Handle subdaily measured data | If measured precipitation is subdaily, initialize missing-data sentinels when out of bounds, copy each subdaily value into the next-day buffer, and fall back to precipitation generation if a missing subdaily value is encountered. |
| 8. Handle daily measured data | If measured precipitation is daily, assign the next-day precipitation from the record or a missing-data sentinel, then generate precipitation and count the missing day when the record value is invalid. |
| 9. Accumulate annual totals | When the call is part of an ongoing simulation, add current precipitation and potential ET to the station's annual accumulators used for later reporting. |

## Modules Used

<!-- facts:uses -->

| Module | State touched | Key components |
| --- | --- | --- |
| [sym:climate_module] | `wst, pcp` | `wst(iwst)%weat%precip, wst(iwst)%weat%precip_next, wst(iwst)%weat%ts, wst(iwst)%weat%ts_next, wst(iwst)%wco%wgn, wst(iwst)%wco%pgage, wst(iwst)%wco_c%pgage, wst(iwst)%weat%ts(:), pcp(ipg)%yrs_start, pcp(ipg)%start_day, pcp(ipg)%start_yr, pcp(ipg)%end_day, pcp(ipg)%end_yr, pcp(ipg)%tstep, wst(iwst)%weat%ts_next(ist), pcp(ipg)%tss, pcp(ipg)%ts(cur_day,yrs_to_start), pcp(ipg)%days_gen, wst(iwst)%precip_aa, wst(iwst)%pet_aa, wst(iwst)%weat%pet` |
| [sym:basin_module] | `none resolved from the context packet` |  |
| [sym:time_module] | `time` | `time%step, time%day, time%yrs, time%day_end_yr` |
| [sym:hydrograph_module] | `ts, iwst` |  |
| [sym:maximum_data_module] | `db_mx` | `db_mx%wst` |

## Local Variables

<!-- facts:locals -->

## State Changes

| Target | When | Meaning |
| --- | --- | --- |
| `wst(iwst)%weat%precip` | Always at the start of each station loop | Promoted from `precip_next` so the current-day precipitation state reflects the previously prepared value. |
| `wst(iwst)%weat%precip_next` | Always at the start of each station loop | Cleared to zero before new precipitation is generated or copied in for the next day. |
| `wst(iwst)%weat%ts` | Always at the start of each station loop | Copied from `ts_next` so the current-day subdaily precipitation array matches the previously prepared next-day array. |
| `wst(iwst)%weat%ts_next` | When simulated precipitation is used and `time%step > 1` | Filled by `cli_pgenhr` with generated subdaily rainfall amounts for the active station. |
| `wst(iwst)%weat%ts_next(ist)` | When simulated precipitation is used and `time%step > 1` | Populated by the hourly generator as part of the generated storm profile for each subdaily interval. |
| `pcp(ipg)%days_gen` | When measured daily precipitation is missing or out of bounds | Incremented after calling `cli_pgen` to count a generated replacement day. |
| `wst(iwst)%precip_aa` | When measured precipitation is out of bounds | Accumulated with current precipitation only when `istart > 0`, contributing to annual precipitation totals for later reporting. |
| `wst(iwst)%pet_aa` | When measured precipitation is out of bounds | Accumulated with current potential ET only when `istart > 0`, contributing to annual climate totals for later reporting. |

## File I/O

<!-- facts:io -->


## Lineage

`cli_precip_control.f90` was introduced in `df07e3f` (2024-03-05, "init all") and has been changed in 5 non-merge commit(s) since, most recently `bd18ad4` (2025-11-24, "Pr 107 (#108)"). Lineage is reconstructed from commit metadata (SHA, date, subject); per-line diffs were unavailable in this build environment, so only the commits touching `cli_precip_control.f90` are listed.

- `bd18ad4` (2025-11-24) — Pr 107 (#108)
- `f1e61a3` (2024-10-08) — fixed tabs
- `39fabde` (2024-08-08) — Initialized varables with python script, corrected input data where integers where floats in two input files, trapped underflow errors in th…
- `c7c8e22` (2024-05-30) — Added latest source code from bitbucket
- `df07e3f` (2024-03-05) — init all

## Review Notes

- No direct file I/O was extracted for this procedure.
- warning: missing_doc: Procedure 'cli_precip_control' has no extracted documentation comment.
- Lineage was reconstructed from file-level commit metadata; per-line diffs were unavailable in this environment (blobless clone), so line-span filtering was not applied.
