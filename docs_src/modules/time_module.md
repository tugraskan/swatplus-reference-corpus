---
kind: module
symbol: time_module
title: time_module
status: filled
source_hash: 5f5bedaa8a70b683
version_label: SWAT+ 62.0.0
variables:
  cal_sim: character label naming the calibration/simulation mode; initialized to `" Original
    Simulation"` in this module and consumed by calibration and basin output routines that
    write or annotate simulation state.
  cal_adj: real scalar calibration adjustment flag/value; initialized to `0.0` here and used
    by calibration routines that compare or adjust model parameters and outputs.
  yrs_print: real scalar average-annual print divisor; initialized to `0.` here and used by
    routines that normalize accumulated totals into average-annual values.
  ndays: integer month-end Julian day lookup table for leap-year logic and month-length calculations;
    initialized here and used by many output routines to convert month totals to averages.
  ndays_leap: integer month-end Julian day lookup table for leap-year calculations; initialized
    here and used when routines need leap-year month boundaries.
  ndays_noleap: integer month-end Julian day lookup table for non-leap-year calculations;
    initialized here and used when routines need non-leap month boundaries.
  ndmo: integer array of cumulative days accrued in each month since the simulation began;
    initialized to zero here and used as a month accumulator for timing logic.
  time: shared `time_current` record holding the active simulation calendar, boundaries, and
    print intervals; initialized with default component values here and updated by `time_control`/`time_read`
    before being consumed by model processes and output routines.
  time_init: shared `time_current` record preserving the initial time state; initialized with
    default component values here and used by time-control logic to seed the running `time`
    record.
type_components:
  time_current:
    day_print: one-character print flag for daily timing/printing control
    day: current day of simulation
    mo: current month of simulation
    mo_start: starting month
    yrc: current calendar year
    yrc_start: starting calendar year
    yrc_end: ending calendar year
    yrs: current sequential year
    day_mo: day of month (1-31)
    end_mo: set to 1 if end of month
    end_yr: set to 1 if end of year
    end_sim: set to 1 if end of simulation
    end_aa_prt: set to 1 if end of simulation
    day_start: beginning julian day of simulation
    day_end_yr: ending julian day of each year
    day_end: input ending julian day of simulation
    nbyr: number of years of simulation run
    step: number of time steps in a day for rainfall, runoff and routing
    dtm: 0 = daily; 1=increment(12 hrs); 24=hourly; 96=15 mins; 1440=minute; time step in
      minutes for rainfall, runoff and routing
    days_prt: number of days for average annual printing for entire time period
    yrs_prt: number of years for average annual printing for entire time period
    yrs_prt_int: number of years for average annual printing for printing interval- pco%aa_yrs()
    num_leap: number of leap years in simulation for average annual printing
    prt_int_cur: current average annual print interval
    yrc_tot: total years counted in the simulation clock
type_summaries:
  time_current: Shared simulation date, boundary, and print-control record used across SWAT+
    processes.
---

<!-- facts:header -->

`time_module` owns the shared simulation clock, calendar labels, run-length counters, and derived time record used throughout SWAT+ for initialization, routing, climate file alignment, calibration, and all period-based output. The module itself is a declaration container: its state is populated and updated by `time_control`, `time_read`, and other setup routines, then consumed by many daily/monthly/yearly output and process routines.

## Contained Procedures And Types

<!-- facts:members -->

## Module Variables

<!-- facts:variables -->

## Derived Types

<!-- facts:types -->



## Initialization

This module only declares shared state and the `time_current` type; it contains no procedures. Startup and control routines populate the state, especially `time_control`, `time_read`, `basin_print_codes_read`, `basin_sw_init`, `allocate_parms`, and many process/output routines that read the record.

## Populated By

| Reader | Input file | Target | Behavior |
| --- | --- | --- | --- |
| [sym:actions] | `unit_2612, unit_3612` | `cal_sim, cal_adj, yrs_print, ndays, ndays_leap, ndays_noleap` | Uses shared time state while writing management-output records; the evidence shows `time%yrc`, `time%mo`, and `time%day_mo` are written to management output, so the module provides the current simulation date for action reporting. |
| [sym:aqu_cs_output] | `unit_6060, unit_6061, unit_6062, unit_6063, unit_6064, unit_6065, unit_6066, unit_6067` | `cal_sim, cal_adj, yrs_print, ndays, ndays_leap, ndays_noleap` | Reads shared time state to stamp aquifer constituent output and to detect month, year, and simulation-end boundaries for averaging and resetting accumulators. |
| [sym:aqu_pesticide_output] | `unit_3008, unit_3012, unit_3009, unit_3013, unit_3010, unit_3014, unit_3011, unit_3015` | `cal_sim, cal_adj, yrs_print, ndays, ndays_leap, ndays_noleap` | Uses the current simulation date and end-of-month/end-of-year flags to write aquifer pesticide summaries and roll monthly totals into yearly and average-annual records. |
| [sym:aqu_salt_output] | `unit_5060, unit_5061, unit_5062, unit_5063, unit_5064, unit_5065, unit_5066, unit_5067` | `cal_sim, cal_adj, yrs_print, ndays, ndays_leap, ndays_noleap` | Uses shared time fields to label aquifer salt reports and to trigger monthly, yearly, and end-of-simulation averaging branches. |
| [sym:aquifer_output] | `unit_2520, unit_2524, unit_2521, unit_2525, unit_2522, unit_2526, unit_2523, unit_2527` | `cal_sim, cal_adj, yrs_print, ndays, ndays_leap, ndays_noleap` | Uses `time` to write daily aquifer state and to average monthly and yearly storage, depth-to-water, and nitrate values before final simulation output. |
| [sym:basin_aqu_pest_output] | `unit_3000, unit_3004, unit_3001, unit_3005, unit_3002, unit_3006, unit_3003, unit_3007` | `cal_sim, cal_adj, yrs_print, ndays, ndays_leap, ndays_noleap` | Uses the shared time record to control basin aquifer pesticide daily reporting and month/year rollups. |
| [sym:basin_aquifer_output] | `unit_2090, unit_2094, unit_2091, unit_2095, unit_2092, unit_2096, unit_2093, unit_2097` | `cal_sim, cal_adj, yrs_print, ndays, ndays_leap, ndays_noleap` | Uses `time` to stamp basin aquifer reports and to normalize monthly and yearly basin aquifer totals. |
| [sym:basin_ch_pest_output] | `unit_2832, unit_2836, unit_2833, unit_2837, unit_2834, unit_2838, unit_2835, unit_2839` | `cal_sim, cal_adj, yrs_print, ndays, ndays_leap, ndays_noleap` | Uses the simulation calendar and period-end flags to write basin channel pesticide totals and convert monthly and yearly accumulators to averages. |
| [sym:basin_chanbud_output] | `unit_2128, unit_2132, unit_2129, unit_2133, unit_2130, unit_2134, unit_2131, unit_2135` | `cal_sim, cal_adj, yrs_print, ndays, ndays_leap, ndays_noleap` | Uses `time` to decide when basin sediment-budget totals are written and when month/year accumulators are reset or averaged. |
| [sym:basin_chanmorph_output] | `unit_2120, unit_2124, unit_2121, unit_2125, unit_2122, unit_2126, unit_2123, unit_2127` | `cal_sim, cal_adj, yrs_print, ndays, ndays_leap, ndays_noleap` | Uses the current simulation date and print-interval flags to finalize basin channel-morphology summaries at month, year, and simulation end. |
| [sym:basin_channel_output] | `unit_2110, unit_2114, unit_2111, unit_2115, unit_2112, unit_2116, unit_2113, unit_2117` | `cal_sim, cal_adj, yrs_print, ndays, ndays_leap, ndays_noleap` | Uses the shared time state to label basin channel output and to roll daily values into monthly, yearly, and average-annual totals. |
| [sym:basin_ls_pest_output] | `unit_2864, unit_2868, unit_2865, unit_2869, unit_2866, unit_2870, unit_2867, unit_2871` | `cal_sim, cal_adj, yrs_print, ndays, ndays_leap, ndays_noleap` | Uses the simulation clock and period-end flags to aggregate basin landscape pesticide totals into daily, monthly, yearly, and average-annual outputs. |

## Key Consumers

The main consumers fall into a few groups: setup/control routines that seed the shared clock (`time_control`, `time_read`, `basin_print_codes_read`, `basin_sw_init`), calendar-aware climate readers and generators (`cli_*` routines, `climate_control`), management and calibration routines that need the current date or print interval (`actions`, `cal_conditions`, `calsoft_*`, `mgt_*`), and a large family of output routines that use the same time flags to decide when to write daily, monthly, yearly, or average-annual records.

| Consumer | Uses | Effect |
| --- | --- | --- |
| [sym:aqu_cs_output] | time_module | The `time` state determines which reporting branches run and provides the date fields written to every record. Its end-of-month, end-of-year, and end-of-simulation flags gate monthly, yearly, and average-annual outputs, while its calendar fields label each output row. |
| [sym:aqu_pesticide_output] | time_module | `time_module` supplies all timestamp and period-boundary flags used to decide when to write daily, monthly, yearly, and end-of-simulation pesticide summaries. The routine depends on `time%day`, `time%mo`, `time%day_mo`, `time%yrc`, `time%end_mo`, `time%end_yr`, `time%day_end_yr`, `time%end_sim`, `time%yrs_prt`, and `time%days_prt` to label output and to trigger period rollups. |
| [sym:aqu_salt_output] | time_module | The time state determines which reporting branches run and supplies the date fields written to each record. `time%end_mo`, `time%end_yr`, and `time%end_sim` gate monthly, yearly, and average-annual output, while the day/month/year fields are included in every output line. |
| [sym:aquifer_output] | time_module | The `time` state supplies the current day, month, and year labels written to every record, plus the end-of-month, end-of-year, and end-of-simulation flags that control which reporting branches run. `time%yrs_prt` is also needed to compute the final average annual aquifer output. |
| [sym:basin_aqu_pest_output] | time_module | `time_module` supplies the calendar and period-end flags that gate each output branch. The routine uses these values to decide whether to write daily, monthly, yearly, or average-annual pesticide summaries and to stamp each record with the current date. |
| [sym:basin_aquifer_output] | time_module | The routine depends on `time` to know the current simulation date and to detect period boundaries. Those flags control whether daily, monthly, yearly, or average-annual aquifer summaries are written and when accumulated values are normalized or reset. |
| [sym:basin_ch_pest_output] | time_module | The `time` object controls all period boundaries and the timestamp written to output: daily printing depends on `time%day`, `time%mo`, `time%day_mo`, and `time%yrc`, while monthly, yearly, and end-of-simulation branches depend on `time%end_mo`, `time%end_yr`, `time%day_end_yr`, `time%end_sim`, `time%yrs_prt`, and `time%days_prt`. |
| [sym:basin_chanbud_output] | time_module | The time state tells this routine which reporting boundary has been reached: daily print timing, end-of-month, end-of-year, and end-of-simulation all gate the different output branches. The same time fields also supply the date stamp written into each record and the years-per-print divisor used for average annual output. |
| [sym:basin_chanmorph_output] | time_module | The routine keys all reporting decisions off the current simulation date and end-of-period flags from `time`. It needs `time%day`, `time%mo`, `time%day_mo`, and `time%yrc` to label each record, and it uses `time%end_mo`, `time%end_yr`, `time%end_sim`, `time%day_end_yr`, `time%yrs_prt`, and `time%days_prt` to decide when monthly, yearly, and average-annual basin summaries should be finalized and normalized. |
| [sym:basin_channel_output] | time_module | The `time` state tells the routine what kind of reporting boundary it is on. `time%day`, `time%mo`, `time%day_mo`, and `time%yrc` are written into every record, while `time%end_mo`, `time%end_yr`, `time%end_sim`, and `time%yrs_prt` decide when monthly, yearly, and average-annual basin channel totals should be finalized and written. |
| [sym:basin_ls_pest_output] | time_module | `time_module` provides the simulation clock and end-of-period flags that control when each summary is written and when accumulated daily values roll up into monthly, yearly, and average-annual totals. |
| [sym:basin_output] | time_module | `time` controls every reporting branch in this routine: it supplies the current day, month, year, end-of-month/end-of-year/end-of-simulation flags, and averaging factors used to decide when basin records are written and how annual values are normalized. |
| [sym:basin_print_codes_read] | time_module | Current simulation year and run length are used to fill default start and end years when `pco%yrc_start` or `pco%yrc_end` is left unset in `print.prt`. |
| [sym:basin_recall_output] | time_module | This routine uses the current simulation date and end-of-period flags from `time` to decide when to write daily, monthly, yearly, and average-annual recall outputs, and it uses `time%yrs_prt` to compute the final average annual value. |
| [sym:basin_res_pest_output] | time_module | The current simulation date and end-of-period flags control when daily, monthly, yearly, and end-of-simulation outputs are emitted and when accumulators are rolled forward or reset. |
| [sym:basin_reservoir_output] | time_module | `time_module` provides the simulation clock and end-of-period flags that control when each reporting block runs. The routine uses the current day, month, day-of-month, and year in every record, then checks `time%end_mo`, `time%end_yr`, `time%end_sim`, and `time%yrs_prt` to decide when to summarize monthly, yearly, and average-annual reservoir outputs. |
| [sym:basin_sdchannel_output] | time_module | The `time_module` controls when each output block runs. `time%day`, `time%mo`, `time%day_mo`, and `time%yrc` provide the date fields written to each record, while `time%end_mo`, `time%end_yr`, `time%end_sim`, `time%day_end_yr`, and `time%yrs_prt` decide when month-end, year-end, and average-annual summaries should be produced and how the annual average is normalized. |
| [sym:ch_cs_output] | time_module | `time_module` supplies the simulation clock fields that control when monthly, yearly, and end-of-simulation reports are written. The routine uses `time%day`, `time%mo`, `time%day_mo`, `time%yrc`, `time%end_mo`, `time%end_yr`, `time%end_sim`, `time%day_end_yr`, and `time%nbyr` to stamp output and decide when to roll accumulators forward. |
| [sym:ch_read_nut] | time_module | The routing time-step value controls unit conversion for several rate parameters. `ch_read_nut` divides daily or per-day coefficients by `time%step` so the stored values match hourly or subdaily routing when applicable. |
| [sym:ch_salt_output] | time_module | `time` controls when each output block runs (`end_mo`, `end_yr`, `end_sim`) and provides the date fields written to every record. It also provides `day_end_yr` and `nbyr`, which are used to compute average monthly and average annual values. |
| [sym:cha_pesticide_output] | time_module | The `time` state controls every reporting gate in this routine: daily output uses the current day counters, monthly and yearly output depend on end-of-period flags, and average-annual output depends on end-of-simulation and the number of years printed. |
| [sym:channel_output] | time_module | `time_module` supplies the simulation clock and end-of-period flags that determine when channel output is emitted and when period totals are rolled up. The routine prints `time%day`, `time%mo`, `time%day_mo`, and `time%yrc`, and it branches on `time%end_mo`, `time%end_yr`, `time%end_sim`, and `time%yrs_prt` to decide monthly, yearly, and average-annual handling. |
| [sym:cli_hmeas] | time_module | `time_module` provides the simulation calendar start values `time%yrc` and `time%day_start`, which the routine uses to decide where the loaded humidity series begins relative to the simulation window. |
| [sym:cli_petmeas] | time_module | The current simulation year and starting day determine where measured PET loading should begin. `cli_petmeas` compares file dates against `time%yrc` and `time%day_start` to skip records before the model start. |

## Lineage

`time_module.f90` was introduced in `df07e3f` (2024-03-05, "init all") and has been changed in 5 non-merge commit(s) since, most recently `889136d` (2025-02-03, "Fix typos"). Lineage is reconstructed from commit metadata (SHA, date, subject); per-line diffs were unavailable in this build environment, so only the commits touching `time_module.f90` are listed.

- `889136d` (2025-02-03) — Fix typos
- `568154c` (2024-10-08) — Increase length of various character variables
- `39fabde` (2024-08-08) — Initialized varables with python script, corrected input data where integers where floats in two input files, trapped underflow errors in th…
- `94b6dec` (2024-05-30) — Added latest source code from bitbucket
- `df07e3f` (2024-03-05) — init all

## Review Notes

- Module `time_module` has no contained procedures; it is a shared declaration module only.
- Reader rows are representative of the many importers; the full importer appendix is preserved separately in `all_importers`.
- No resolved lineage commits were available for this source span.
- `time_current.yrc_tot` is declared in the source but has no inline comment; its exact intended meaning is not stated in the extracted source.
- Lineage was reconstructed from file-level commit metadata; per-line diffs were unavailable in this environment (blobless clone), so line-span filtering was not applied.
