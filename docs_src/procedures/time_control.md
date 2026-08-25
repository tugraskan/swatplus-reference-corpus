---
kind: procedure
symbol: time_control
title: time_control
status: filled
source_hash: 70cfebf17b5ce757
version_label: SWAT+ 62.0.0
locals:
  j: HRU loop counter.
  julian_day: Julian-day loop counter within the year.
  id: Decision-table (scenario) index for conditional updates.
  isched: Management-schedule index.
  idp: Plant database index.
  iplt: Plant counter.
  iupd: Conditional-update counter.
  ipest: Pesticide counter.
  date_time: Wall-clock date/time array from `DATE_AND_TIME` (progress print).
  crop_yld_t_ha: Annual / average-annual basin crop yield (t/ha).
  sw_init: Initial soil water for the water-balance check.
  sno_init: Initial snow water for the water-balance check.
  iob: Spatial-object index passed to `actions`.
  iord: Stream-order index.
  curyr: Outer-loop simulation-year counter.
  mo: Current month (from `xmon`).
  day_mo: Current day of month (from `xmon`).
  imallo: Manure-allocation index.
  ires: Reservoir index.
  rnum: Channel count per stream order (>= 1 to avoid divide-by-zero).
uses:
  maximum_data_module: Provides the calendar/print state (`time`, `pco`) and the basin/HRU/object
    data the daily loop reads and the called routines need.
  calibration_data_module: Provides the calendar/print state (`time`, `pco`) and the basin/HRU/object
    data the daily loop reads and the called routines need.
  plant_data_module: Provides the calendar/print state (`time`, `pco`) and the basin/HRU/object
    data the daily loop reads and the called routines need.
  mgt_operations_module: Provides the calendar/print state (`time`, `pco`) and the basin/HRU/object
    data the daily loop reads and the called routines need.
  hru_module: Provides the calendar/print state (`time`, `pco`) and the basin/HRU/object data
    the daily loop reads and the called routines need.
  plant_module: Provides the calendar/print state (`time`, `pco`) and the basin/HRU/object
    data the daily loop reads and the called routines need.
  soil_module: Provides the calendar/print state (`time`, `pco`) and the basin/HRU/object
    data the daily loop reads and the called routines need.
  time_module: Provides the calendar/print state (`time`, `pco`) and the basin/HRU/object
    data the daily loop reads and the called routines need.
  climate_module: Provides the calendar/print state (`time`, `pco`) and the basin/HRU/object
    data the daily loop reads and the called routines need.
  basin_module: Provides the calendar/print state (`time`, `pco`) and the basin/HRU/object
    data the daily loop reads and the called routines need.
  sd_channel_module: Provides the calendar/print state (`time`, `pco`) and the basin/HRU/object
    data the daily loop reads and the called routines need.
  hru_lte_module: Provides the calendar/print state (`time`, `pco`) and the basin/HRU/object
    data the daily loop reads and the called routines need.
  hydrograph_module: Provides the calendar/print state (`time`, `pco`) and the basin/HRU/object
    data the daily loop reads and the called routines need.
  output_landscape_module: Provides the calendar/print state (`time`, `pco`) and the basin/HRU/object
    data the daily loop reads and the called routines need.
  conditional_module: Provides the calendar/print state (`time`, `pco`) and the basin/HRU/object
    data the daily loop reads and the called routines need.
  constituent_mass_module: Provides the calendar/print state (`time`, `pco`) and the basin/HRU/object
    data the daily loop reads and the called routines need.
  output_ls_pesticide_module: Provides the calendar/print state (`time`, `pco`) and the basin/HRU/object
    data the daily loop reads and the called routines need.
  water_body_module: Provides the calendar/print state (`time`, `pco`) and the basin/HRU/object
    data the daily loop reads and the called routines need.
  water_allocation_module: Provides the calendar/print state (`time`, `pco`) and the basin/HRU/object
    data the daily loop reads and the called routines need.
---

<!-- facts:header -->

Drives the main simulation time loop. It steps year by year and day by day, advancing the calendar (handling leap years), setting end-of-month/year/simulation and print flags, then calling the weather and routing routines (`climate_control`, `command`) for each day.

## Bottom Line

`time_control` is the outer simulation loop. For each year it sets the leap/non-leap day counts and start/end days, accumulates the print-year counters, and for each Julian day computes the month/day-of-month, sets the end-of-period and daily-print flags, initializes per-day HRU and water-allocation state, and reads/generates weather.

Within each day it applies conditional land-use/management resets (decision tables), then calls `command` to route every spatial object. It is invoked repeatedly by the soft-calibration controllers, so a full model run is one pass through this routine.

## Arguments

<!-- facts:arguments -->

## Where It Fits

The top-level daily driver, called by the calibration controllers (`calhard_control`, the `calsoft_*` routines) to run a full simulation. It owns the year/day loops and the calendar/print state in `time` and `pco`, and delegates the per-day physics to `climate_control` and `command`.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. Select output conditions | Part of the year/day time loop: advances the calendar, sets leap-year and print/end-of-period flags, initializes per-day state, and calls the weather and routing routines. |
| 2. Loop over output items | Part of the year/day time loop: advances the calendar, sets leap-year and print/end-of-period flags, initializes per-day state, and calls the weather and routing routines. |
| 3. Write output records | Part of the year/day time loop: advances the calendar, sets leap-year and print/end-of-period flags, initializes per-day state, and calls the weather and routing routines. |
| 4. Update output state | Part of the year/day time loop: advances the calendar, sets leap-year and print/end-of-period flags, initializes per-day state, and calls the weather and routing routines. |

## Modules Used

<!-- facts:uses -->

| Module | State touched | Key components |
| --- | --- | --- |
| [sym:maximum_data_module] | `db_mx` | `db_mx%cond_up, db_mx%mallo_db` |
| [sym:calibration_data_module] | `upd_cond` | `upd_cond(iupd)%cond_num` |
| [sym:plant_data_module] | `plts_bsn, pldb` | `pldb(idp)%typ, pldb(idp)%mat_yrs` |
| [sym:mgt_operations_module] | `sched` | `sched(isched)%num_ops` |
| [sym:hru_module] | `hru` | `hru(ihru)%mgt_ops, hru(ihru)%cur_op, hru(j)%hyd%biomix, hru(j)%mgt_ops, hru(j)%cur_op` |
| [sym:plant_module] | `bsn_crop_yld, bsn_crop_yld_aa, pcom` | `bsn_crop_yld(iplt)%yield, bsn_crop_yld(iplt)%area_ha, bsn_crop_yld_aa(iplt)%area_ha, bsn_crop_yld_aa(iplt)%yield, pcom(j)%npl, pcom(j)%plcur(ipl)%idplt, pcom(j)%plcur(ipl)%curyr_mat` |
| [sym:soil_module] | `no resolved imported state` |  |
| [sym:time_module] | `time` | `time%yrc, time%yrc_start, time%day_end_yr, time%yrs, time%day, time%day_start, time%mo, time%day_mo, time%nbyr, time%num_leap, time%day_end, time%yrs_prt, time%days_prt, time%yrc_tot, time%yrc_end, time%end_mo, time%end_yr, time%end_sim, time%end_aa_prt, time%prt_int_cur, time%yrs_prt_int` |
| [sym:climate_module] | `no resolved imported state` |  |
| [sym:basin_module] | `pco, bsn_cc, bsn_sedbud, bsn` | `pco%nyskip, pco%sw_init, pco%aa_numint, pco%aa_yrs, pco%day_print_over, pco%day_print, pco%day_start, pco%yrc_start, pco%day_end, pco%yrc_end, pco%int_day_cur, pco%int_day, pco%crop_yld, bsn_cc%cswat, bsn_sedbud%upland_t, bsn%area_ls_ha` |
| [sym:sd_channel_module] | `sd_ch, ch_morph_ord, ch_morph` | `sd_ch(ich)%order, ch_morph_ord(iord)%num, ch_morph(ich)%w_yr, ch_morph(ich)%ebank_m, sd_ch(ich)%chw, ch_morph(ich)%d_yr, ch_morph(ich)%ebtm_m, sd_ch(ich)%chd, ch_morph(ich)%fp_mm, ch_morph(ich)%fp_t` |
| [sym:hru_lte_module] | `no resolved imported state` |  |
| [sym:hydrograph_module] | `sp_ob, sp_ob1, ob` | `sp_ob%hru, sp_ob1%hru, ob(iob)%lat, sp_ob%hru_lte, sp_ob%chandeg` |
| [sym:output_landscape_module] | `hwb_y, bls_a` | `hwb_y(j)%sw_final, hwb_y(j)%sno_final, hwb_y(j)%sw_init, hwb_y(j)%sno_init, bls_a%sedyld` |
| [sym:conditional_module] | `no resolved imported state` |  |
| [sym:constituent_mass_module] | `cs_db` | `cs_db%num_pests` |
| [sym:output_ls_pesticide_module] | `hpestb_y` | `hpestb_y(j)%pest(ipest)` |
| [sym:water_body_module] | `no resolved imported state` |  |
| [sym:water_allocation_module] | `wallo` | `wallo(:)%tot` |

## Local Variables

<!-- facts:locals -->

## State Changes

| Target | When | Meaning |
| --- | --- | --- |
| `time%yrc` | At entry and per year. | Calendar year being simulated. `time%yrc = time%yrc_start` (then incremented at end of each year). |
| `time%day_end_yr` | Per year, leap-dependent. | Last Julian day simulated in the year. Set to `ndays_leap(13)`/`ndays_noleap(13)` (or the user end day in the final year). |
| `time%yrs` | At entry and per year. | Simulation-year counter (1-based). `time%yrs = 1` then `= curyr`. |
| `time%day` | Per day. | Current Julian day. `time%day = time%day_start` then `= julian_day`. |
| `time%mo` | Per day. | Current month. `time%mo = mo` from `xmon(time%day, mo, day_mo)`. |
| `time%day_mo` | Per day. | Current day of month. `time%day_mo = day_mo` from `xmon`. |
| `ndays` | Per year. | Days-per-month array for the current year. `ndays = ndays_leap` or `ndays_noleap` per the leap-year test. |
| `time%num_leap` | Per leap year; used to normalize average-annual printing. | Count of leap years simulated. `time%num_leap = time%num_leap + 1` on leap years. |
| `time%day_start` | Per year. | First simulated Julian day of the year. `time%day_start = 1` for years after the first. |
| `time%yrs_prt` | Per printed year; normalizes average-annual writes. | Accumulated print-period length for average-annual output. `time%yrs_prt = time%yrs_prt + (day_end_yr - day_start + 1)`; normalized at end of sim. |
| `time%days_prt` | Per printed year. | Accumulated printed days. `time%days_prt = time%days_prt + (day_end_yr - day_start + 1)`. |
| `pco%sw_init` | Once, after the skip years. | Flag that the initial soil water has been recorded. `pco%sw_init = "y"` after `basin_sw_init` runs. |
| `time%yrc_tot` | Per day (recomputed). | Total number of calendar years in the run. `time%yrc_tot = time%yrc_end - time%yrc_start + 1`. |
| `time%end_mo` | Per day. | End-of-month flag for output. `time%end_mo = 0`, then `1` when `time%day == ndays(time%mo+1)`. |
| `time%end_yr` | Per day. | End-of-year flag for output. `time%end_yr = 0`, then `1` when `time%day == time%day_end_yr`. |
| `time%end_sim` | Per day. | End-of-simulation flag. `time%end_sim = 0`, then `1` on the last day of the last year. |
| `time%end_aa_prt` | Per day / per interval. | Flag marking the end of an average-annual print interval. `time%end_aa_prt = 1` at the end of an average-annual print interval, else reset to 0. |
| `time%prt_int_cur` | Per interval. | Current average-annual print-interval index. `time%prt_int_cur = 0.` on reset, then `+ 1` after an interval ends. |
| `time%yrs_prt_int` | At interval end. | Normalized print-interval length for average-annual output. `time%yrs_prt_int = time%yrs_prt_int / (365. + num_leap/nbyr)` at interval end. |
| `pco%day_print` | Per day, within the print window. | Daily-output print switch. `pco%day_print = "y"` when the start day/year is reached; `"n"` after the end. |
| `pco%day_print_over` | Once printing ends. | Flag that daily printing is finished. `pco%day_print_over = "y"` once daily printing has ended. |
| `pco%int_day_cur` | Per day. | Day counter within the daily print interval. `pco%int_day_cur = pco%int_day_cur + 1` (wraps at `pco%int_day`). |
| `wallo(:)%tot` | Per day, before allocation runs. | Daily water-allocation totals (demand/withdrawal/unmet), reset. `wallo(:)%tot = walloz` (zeroed each day). |
| `d_tbl` | Per conditional update, in the daily loop. | Pointer to the active decision table for conditional land-use/management resets. `d_tbl => dtbl_scen(id)` for each conditional update. |

## File I/O

<!-- facts:io -->


## Lineage

`time_control.f90` was introduced in `df07e3f` (2024-03-05, "init all") and has been changed in 30 non-merge commit(s) since, most recently `4ce869c` (2026-06-13, "Fix channel morphology averaging crash on empty stream orders"). Lineage is reconstructed from commit metadata (SHA, date, subject); per-line diffs were unavailable in this build environment, so only the commits touching `time_control.f90` are listed.

- `4ce869c` (2026-06-13) — Fix channel morphology averaging crash on empty stream orders
- `d7ecb7a` (2026-05-07) — Added if (allocated(x) statements to prevent gfortran runtime errors in situations where water allocation is not being run.
- `f7e26d7` (2026-05-01) — Incremental improvements to pl_fert and pl_manure
- `fdd3206` (2026-04-29) — Update crop yield calculations to include year skip condition
- `f1d1ac1` (2026-04-22) — Hopefulle some finally cleanup to implement cswat == 3 to cswat = 1. Added/changed subroutines in external specificaitons due to subroutine…
- `df07e3f` (2024-03-05) — init all

## Review Notes

- Direct file I/O exists; verify file meanings and units before finalizing.
- warning: missing_doc: Procedure 'time_control' has no extracted documentation comment.
- Top-level time loop; state changes are calendar advancement and print/end-of-period flags. 5 use-imported modules had no specific symbol resolved.
- Lineage was reconstructed from file-level commit metadata; per-line diffs were unavailable in this environment (blobless clone), so line-span filtering was not applied.
