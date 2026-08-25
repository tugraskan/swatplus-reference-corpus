---
kind: procedure
symbol: salt_roadsalt_read
title: salt_roadsalt_read
status: filled
source_hash: 9722aa63d44643ae
version_label: SWAT+ 62.0.0
locals:
  salt_ion: Short salt-ion code read from each record in `salt_road`; it identifies which
    salt ion the following loading value belongs to.
  station_name: Station name header read from the file before each station's salt data block;
    it marks the start of the next station record set.
  eof: End-of-file/status counter initialized but not used in the extracted source segment.
  iadep: Loop counter over atmospheric deposition stations in `rdapp_salt`.
  imo: Loop counter used when reading monthly salt values into `roadmo`.
  iyr: Loop counter used when reading yearly salt values into `roadyr` and when filling daily
    year-indexed loads into `roadday`.
  i_exist: Logical flag set by `inquire` to determine whether the `salt_road` input file is
    present before opening it.
  isalt: Loop counter over salt ions within each station's `salt` array.
  year_index: Calendar year being processed in the yearly redistribution loop; initialized
    from `atmodep_cont%yr_init` and incremented each annual record.
  yr_weat: Weather-year index used to access precipitation and temperature time-series arrays
    for the current calendar year.
  year_days: Number of days in the current year, set to 365 or 366 depending on leap year
    status.
  iday: Day-of-year loop counter used to scan weather data and assign daily salt loads.
  day_flag: Per-day flag array marking days identified as snowy days for the current year.
  day_precip: Daily precipitation value taken from `pcp` for the current day and weather year.
  day_temp: Daily mean temperature derived from `tmp` and `tmp%ts2`; used to decide whether
    precipitation is snow.
  year_precip: Accumulated precipitation on snowy days for the current year; used to normalize
    daily fractions.
  day_fraction: Fraction of the annual salt load assigned to the current snowy day, based
    on that day's precipitation divided by total snowy-day precipitation.
uses:
  basin_module: The source imports `basin_module`, but the extracted lines do not show any
    basin-module symbol actually being referenced in this routine. It matters as a shared
    dependency in the routine's interface, but the specific basin state used here is uncertain
    from the provided extract.
  input_file_module: The source imports `input_file_module`, but no resolved symbol from that
    module appears in the extracted body. It likely provides shared input-file control used
    elsewhere in the read workflow, but the exact state is not visible in the packet.
  climate_module: This module provides the atmospheric-deposition control and storage that
    this reader populates. `atmodep_cont` selects the timestep (`aa`, `mo`, or `yr`), supplies
    the number of stations, the number of records, and the starting year, while `pcp`, `tmp`,
    and `rdapp_salt` hold the precipitation/temperature series and the road-salt arrays that
    this routine fills.
  time_module: The starting calendar year from `time%yrc_start` determines whether yearly
    road-salt loadings can be distributed to daily values using climate data or must be zeroed
    because the precipitation record is not available yet.
  maximum_data_module: The module is imported by the routine, but the extracted source lines
    do not show any referenced symbol from `maximum_data_module`. Its presence indicates a
    broader shared-data dependency, but no concrete use is visible here.
  constituent_mass_module: This module supplies `cs_db%num_salts`, which controls whether
    the routine runs at all and how many salt-ion records are read and allocated per station.
---

<!-- facts:header -->

Reads road-salt application data from `salt_road` and loads it into the road-salt climate database. For yearly input, it also partitions annual salt loadings into daily values using precipitation and temperature.

## Bottom Line

`salt_roadsalt_read` loads road-salt application data for atmospheric deposition stations. It only does work when salt ions are enabled (`cs_db%num_salts > 0`) and the `salt_road` file exists, then reads station-level salt loadings into `rdapp_salt`.

The routine handles three input formats selected by `atmodep_cont%timestep`: annual (`aa`), monthly (`mo`), and yearly (`yr`). In yearly mode it also redistributes each annual salt load to daily values by identifying snowy days from precipitation and temperature, then allocating the yearly load across those days in proportion to daily snowfall precipitation.

## Arguments

<!-- facts:arguments -->

## Where It Fits

This routine runs during the model input-reading phase, after atmospheric-deposition station metadata have been read by `cli_read_atmodep_salt` and before downstream salt simulation routines need road-salt loads. Its results populate the shared `rdapp_salt` database that later climate/salt processing uses for annual, monthly, or daily road-salt application.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. Check whether salt loading data should be processed | The routine first requires `cs_db%num_salts > 0`, then uses `inquire(file='salt_road',exist=i_exist)` to see whether the road-salt input file is present. If either prerequisite fails, it skips the reader body. |
| 2. Open the road-salt file and discard header records | When the file exists, the routine opens unit 5051 on `salt_road` and reads four blank/unstructured records before parsing data records. |
| 3. Allocate the station container | The routine allocates `rdapp_salt(0:atmodep_cont%num_sta)` so there is storage for each atmospheric-deposition station plus index 0. |
| 4. Loop over atmospheric-deposition stations | For each station index `iadep`, the routine allocates `rdapp_salt(iadep)%salt(cs_db%num_salts)` so each salt ion has its own road-salt record. |
| 5. Read annual road-salt loads when timestep is annual | If `atmodep_cont%timestep == 'aa'`, the routine reads the station name and then reads one annual loading value per salt ion into `rdapp_salt(iadep)%salt(isalt)%road`. |
| 6. Read monthly road-salt loads when timestep is monthly | If `atmodep_cont%timestep == 'mo'`, the routine reads the station name, allocates `roadmo(atmodep_cont%num)` for each salt ion, and reads a monthly loading series into that array. |
| 7. Read yearly road-salt loads when timestep is yearly | If `atmodep_cont%timestep == 'yr'`, the routine reads the station name, allocates `roadyr(atmodep_cont%num)` for each salt ion, and reads the yearly loading series into that array. |
| 8. Prepare daily arrays for yearly redistribution | Still in yearly mode, the routine allocates `roadday(366,atmodep_cont%num)` for each salt ion and clears the array to zero before redistribution begins. |
| 9. Set the year counter and weather-year index | The routine initializes `year_index` from `atmodep_cont%yr_init` and starts the weather-year counter `yr_weat` at 1. |
| 10. Determine the number of days in each modeled year | For each modeled year, the routine checks `mod(year_index,4)` and sets `year_days` to 366 for leap years or 365 otherwise. |
| 11. Build a snowy-day mask from precipitation and temperature | For years at or after `time%yrc_start`, the routine scans each day, pulls daily precipitation from `pcp(iadep)%ts(iday,yr_weat)` and mean temperature from `tmp(iadep)%ts(iday,yr_weat)` and `tmp(iadep)%ts2(iday,yr_weat)`, then flags days with precipitation and subfreezing temperature as snowy days while accumulating their precipitation in `year_precip`. |
| 12. Split the annual load across snowy days | The routine revisits the flagged days, computes each day’s share as `pcp(iadep)%ts(iday,yr_weat) / year_precip`, and assigns that fraction of `roadyr(iyr)` to `roadday(iday,iyr)` for every salt ion. |
| 13. Zero daily values for years without precipitation data | For modeled years earlier than `time%yrc_start`, the routine fills the corresponding `roadday(iday,iyr)` entries with zero because the redistribution logic lacks climate data. |
| 14. Advance the year index and continue | After each modeled year the routine increments `year_index`, and after all years it moves on to the next station before returning. |

## Modules Used

<!-- facts:uses -->

| Module | State touched | Key components |
| --- | --- | --- |
| [sym:basin_module] | `basin_module state` |  |
| [sym:input_file_module] | `input_file_module state` |  |
| [sym:climate_module] | `atmodep_cont, rdapp_salt, pcp, tmp` | `atmodep_cont%num_sta, rdapp_salt(iadep)%salt, atmodep_cont%timestep, rdapp_salt(iadep)%salt(isalt)%roadmo, atmodep_cont%num, rdapp_salt(iadep)%salt(isalt)%roadyr, rdapp_salt(iadep)%salt(isalt)%roadday, atmodep_cont%yr_init, pcp(iadep)%ts(iday,yr_weat), tmp(iadep)%ts(iday,yr_weat), tmp(iadep)%ts2(iday,yr_weat), rdapp_salt(iadep)%salt(isalt)%roadday(iday,iyr), rdapp_salt(iadep)%salt(isalt)%roadyr(iyr)` |
| [sym:time_module] | `time` | `time%yrc_start` |
| [sym:maximum_data_module] | `maximum_data_module state` |  |
| [sym:constituent_mass_module] | `cs_db` | `cs_db%num_salts` |

## Local Variables

<!-- facts:locals -->

## State Changes

| Target | When | Meaning |
| --- | --- | --- |
| `rdapp_salt(iadep)%salt(isalt)%roadday` | When `atmodep_cont%timestep == 'yr'` and `year_index >= time%yrc_start`, after snowfall days are identified and `day_fraction` is computed. | `rdapp_salt(iadep)%salt(isalt)%roadday` is populated with daily road-salt amounts derived from the annual yearly-series input. It changes because the routine converts the stored yearly load into day-by-day application values for later climate-driven use. |
| `rdapp_salt(iadep)%salt(isalt)%roadday(iday,iyr)` | When `atmodep_cont%timestep == 'yr'` and `day_flag(iday) == 1`, inside the snowfall redistribution loop. | `rdapp_salt(iadep)%salt(isalt)%roadday(iday,iyr)` receives the fraction of `roadyr(iyr)` assigned to that snowy day. It changes so downstream model code can access a daily road-salt loading rather than only the annual total. |

## File I/O

<!-- facts:io -->


## Lineage

Resolved lineage shows four commits affecting `salt_roadsalt_read`. The initial addition in `df07e3f` introduced the full reader, including file opening, allocation, timestep-specific reads, and yearly redistribution. `35b029c` made only a whitespace cleanup near the end of the file. `94b6dec` imported the source with the same behavior as the initial file. `39fabde` initialized local variables and changed formatting/spacing in declarations and allocation syntax without changing the reader's algorithm. `2ee1889` removed several now-unused local variables (`file`, `titldum`, `header`, `imo_atmo`, `iyrc_atmo`, `imonth`, `dum`) and kept the core read logic unchanged.

- df07e3f added the full procedure body: input gating on `cs_db%num_salts`, opening `salt_road`, reading annual/monthly/yearly records, allocating `rdapp_salt`, and redistributing yearly road-salt loads to daily values.
- 39fabde initialized local scalars and strings and reformatted an allocation statement, but it did not alter how the routine reads or distributes road-salt data.
- 2ee1889 removed unused local declarations, shrinking the variable set while leaving the parsing and redistribution algorithm intact.
- 35b029c only adjusted trailing whitespace near `return`; it did not change procedure behavior.

## Review Notes

- Direct file I/O exists; verify file meanings and units before finalizing.
- warning: missing_doc: Procedure 'salt_roadsalt_read' has no extracted documentation comment.
- algorithm_steps revised: replaced the coarse draft with a 14-step source-backed sequence to match the actual read/allocate/redistribute control flow.
- Some imported modules (`basin_module`, `input_file_module`, `maximum_data_module`) are present in the USE list but no concrete symbol from them is visible in the extracted body; their exact runtime role here is uncertain from the provided evidence.
