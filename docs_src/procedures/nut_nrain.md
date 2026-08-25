---
kind: procedure
symbol: nut_nrain
title: nut_nrain
status: filled
source_hash: ba4ed6091f9c8b63
version_label: SWAT+ 62.0.0
locals:
  iadep: Index into the `atmodep` array for the atmospheric deposition station assigned to
    the current HRU's weather station. Set from `wst(iwst)%wco%atmodep` at line 41 and used
    on lines 49, 51, 55, 57, 62, and 64 to access per-station deposition concentrations and
    rates.
  j: HRU number for the current simulation step, assigned from the module-level `ihru` at
    line 38. Used as the array subscript into `hru`, `soil1`, and `hnb_d` throughout the routine.
  iob: Object connectivity index for HRU `j`. Set from `hru(j)%obj_no` at line 39 and used
    at line 40 to look up the weather station number `ob(iob)%wst`.
  ist: Time-series record index pointing to the current atmospheric deposition station's active
    data record. Read from `atmodep_cont%ts` at line 42. Guards the monthly and annual branches
    via the condition on line 46 and indexes the per-month or per-year deposition arrays.
  const: Number of days in the current calendar month. Computed at line 48 as `float(ndays(time%mo+1)
    - ndays(time%mo))`. Used only in the monthly ("mo") branch to convert the monthly dry-deposition
    rate into a per-day amount.
uses:
  basin_module: Provides the `ndays` cumulative-day-of-year lookup array and the `time` structure
    with the current month index `time%mo`. Both are used at line 48 to compute the number
    of days in the current calendar month, which is needed to distribute the monthly dry-deposition
    rate into a per-day amount in the "mo" timestep branch.
  organic_mineral_mass_module: Provides the `soil1` per-HRU soil profile mass array. `nut_nrain`
    increments the mineral NO3 and NH4 concentrations in the first (top) soil layer (`mn(1)%no3`
    and `mn(1)%nh4`) by the computed daily atmospheric deposition amounts, making deposited
    nitrogen immediately available to subsequent nitrogen-cycle routines.
  hydrograph_module: Provides the `ob` object-connectivity array and the module-level scalar
    `iwst`. The routine writes `iwst = ob(iob)%wst` at line 40 to resolve the weather station
    number for the current HRU's parent object, enabling the subsequent `wst(iwst)%wco%atmodep`
    lookup that identifies the atmospheric deposition station index.
  hru_module: Provides `ihru` (the current HRU loop counter set by `hru_control`) and the
    `hru` array. The routine sets `j = ihru` at line 38 and reads `iob = hru(j)%obj_no` at
    line 39 to identify the object-connectivity record that links this HRU to its weather
    station.
  climate_module: Provides all atmospheric deposition input data. `wst(iwst)%wco%atmodep`
    yields the deposition station index; `atmodep_cont` supplies the configured timestep mode
    and validity bounds; `atmodep(iadep)` holds per-station NO3/NH4 rainfall concentration
    and dry-deposition rate fields for each supported timestep resolution; and `w%precip`
    supplies the current day's rainfall depth used in the wet-deposition formula.
  output_landscape_module: Provides `hnb_d`, the per-HRU daily nutrient-balance output accumulator.
    `nut_nrain` stores the total daily atmospheric NO3 and NH4 deposition amounts into `hnb_d(j)%no3atmo`
    and `hnb_d(j)%nh4atmo`, which are subsequently aggregated into monthly (`hnb_m`) and annual
    (`hnb_y`) output arrays for the HRU nutrient-balance report.
---

<!-- facts:header -->

`nut_nrain` applies atmospheric nitrogen deposition—both wet (rainfall-dissolved) and dry—to the top soil layer of the current HRU for each simulated day. It dispatches into monthly, annual, or long-term-average data paths based on the configured deposition timestep.

## Bottom Line

Each day, `nut_nrain` calculates the NO3 and NH4 contributed by atmospheric deposition to the first soil layer of the active HRU and adds those amounts to the mineral nitrogen pools. The routine navigates a lookup chain—HRU → object connectivity → weather station → atmospheric deposition station—to identify the correct deposition parameter record (`atmodep`). It then selects one of three calculation branches depending on whether the deposition input data are supplied at a monthly ("mo"), annual ("yr"), or long-term-average ("aa") timestep as declared in `atmodep_cont%timestep`.

For wet deposition the formula is `0.01 × concentration_mg_per_L × daily_precip_mm`, which converts to kg N/ha. For dry deposition, the annual or monthly rate is divided by the number of days in the period (days in the current month for "mo", 365 for "yr" and "aa") to obtain a daily increment. Both wet and dry components are summed into `hnb_d(j)%no3atmo` and `hnb_d(j)%nh4atmo` for output tracking, and are immediately added to `soil1(j)%mn(1)%no3` and `soil1(j)%mn(1)%nh4`. The "aa" branch is outside the `ist` validity guard and always executes when `timestep == "aa"`; the "mo" and "yr" branches execute only when a valid station time-series index is present.

## Arguments

<!-- facts:arguments -->

## Where It Fits

`nut_nrain` is called once per day for each active HRU from `hru_control` (line 542), after phosphorus-sediment nutrient routines (`nut_psed`) and before nitrogen leaching (`nut_nlch`). By the time it executes, `hru_control` has set `ihru` to the current HRU number, the weather engine has populated `w%precip` with the day's precipitation, and the atmospheric deposition input arrays have been loaded at model startup. Its outputs—incremented `soil1(j)%mn(1)%no3` and `soil1(j)%mn(1)%nh4`—are consumed immediately by `nut_nlch` and the nitrification, denitrification, and plant-uptake routines that follow in the same daily HRU loop.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. setup | Resolves the HRU-to-deposition-station lookup chain. Sets `j = ihru`, `iob = hru(j)%obj_no`, `iwst = ob(iob)%wst`, `iadep = wst(iwst)%wco%atmodep`, and `ist = atmodep_cont%ts`. Writing to the module-level `iwst` at line 40 updates the shared weather-station cursor used by other routines in the same HRU loop. |
| 2. guard | Checks that `ist` is a valid time-series index (`ist > 0 .and. ist <= atmodep_cont%num`). If false—meaning no active station-specific monthly or annual deposition record exists—the monthly and annual branches are skipped. The long-term-average ("aa") branch at line 61 is outside this guard and always executes when `timestep == "aa"`. |
| 3. monthly branch | When `atmodep_cont%timestep == "mo"`, computes `const = float(ndays(time%mo+1) - ndays(time%mo))` (days in current month, line 48). Sets `hnb_d(j)%no3atmo = .01 * atmodep(iadep)%no3_rfmo(ist) * w%precip + atmodep(iadep)%no3_drymo(ist) / const` (line 49) and increments `soil1(j)%mn(1)%no3` (line 50). Repeats the same pattern for NH4 using `nh4_rfmo` and `nh4_drymo` (lines 51-52). |
| 4. annual branch | When `atmodep_cont%timestep == "yr"`, sets `hnb_d(j)%no3atmo = .01 * atmodep(iadep)%no3_rfyr(ist) * w%precip + atmodep(iadep)%no3_dryyr(ist) / 365.` (line 55) and increments `soil1(j)%mn(1)%no3` (line 56). Repeats for NH4 using `nh4_rfyr` and `nh4_dryyr` (lines 57-58). |
| 5. long-term-average branch | Outside the `ist` guard. When `atmodep_cont%timestep == "aa"`, sets `hnb_d(j)%no3atmo = .01 * atmodep(iadep)%no3_rf * w%precip + atmodep(iadep)%no3_dry / 365.` (line 62) and increments `soil1(j)%mn(1)%no3` (line 63). Repeats for NH4 using `nh4_rf` and `nh4_dry` (lines 64-65). Uses scalar long-term-average constants rather than indexed time-series arrays. |
| 6. return | Returns control to `hru_control`, which immediately calls `nut_nlch` for nitrogen leaching using the updated `soil1(j)%mn(1)%no3` and `soil1(j)%mn(1)%nh4` pools. |

## Modules Used

<!-- facts:uses -->

| Module | State touched | Key components |
| --- | --- | --- |
| [sym:basin_module] | `ndays, time` | `ndays(time%mo + 1), ndays(time%mo), time%mo` |
| [sym:organic_mineral_mass_module] | `soil1` | `soil1(j)%mn(1)%no3, soil1(j)%mn(1)%nh4` |
| [sym:hydrograph_module] | `ob, iwst` | `ob(iob)%wst` |
| [sym:hru_module] | `hru, ihru` | `hru(j)%obj_no` |
| [sym:climate_module] | `wst, atmodep_cont, atmodep, w` | `wst(iwst)%wco%atmodep, atmodep_cont%ts, atmodep_cont%num, atmodep_cont%timestep, atmodep(iadep)%no3_rfmo(ist), w%precip, atmodep(iadep)%no3_drymo(ist), atmodep(iadep)%nh4_rfmo(ist), atmodep(iadep)%nh4_drymo(ist), atmodep(iadep)%no3_rfyr(ist), atmodep(iadep)%no3_dryyr(ist), atmodep(iadep)%nh4_rfyr(ist), atmodep(iadep)%nh4_dryyr(ist), atmodep(iadep)%no3_rf, atmodep(iadep)%no3_dry, atmodep(iadep)%nh4_rf, atmodep(iadep)%nh4_dry` |
| [sym:output_landscape_module] | `hnb_d` | `hnb_d(j)%no3atmo, hnb_d(j)%nh4atmo` |

## Local Variables

<!-- facts:locals -->

## State Changes

| Target | When | Meaning |
| --- | --- | --- |
| `iwst` | Unconditionally at entry (line 40) | Set to `ob(iob)%wst`, identifying the weather station associated with the current HRU's parent object. Acts as the index for the `wst(iwst)%wco%atmodep` dereference on the next line and remains set for any other routine in the same HRU loop that reads the module-level `iwst`. |
| `hnb_d(j)%no3atmo` | timestep == "mo" (line 49), timestep == "yr" (line 55), or timestep == "aa" (line 62) | Receives the computed daily atmospheric NO3 input (kg N/ha) for HRU `j`, combining wet-deposition (`0.01 × concentration × precip`) and dry-deposition (`rate / days_in_period`) components. Carries the value forward to the output reporting accumulator. |
| `soil1(j)%mn(1)%no3` | timestep == "mo" (line 50), timestep == "yr" (line 56), or timestep == "aa" (line 63) | Incremented by `hnb_d(j)%no3atmo`, adding the day's total atmospheric NO3 input to the mineral nitrate pool in the first soil layer of HRU `j`. Makes deposited NO3 available to leaching and other nitrogen-cycle routines in the same daily step. |
| `hnb_d(j)%nh4atmo` | timestep == "mo" (line 51), timestep == "yr" (line 57), or timestep == "aa" (line 64) | Receives the computed daily atmospheric NH4 input (kg N/ha) for HRU `j`, combining wet and dry components. Carries the value forward to the output reporting accumulator. |
| `soil1(j)%mn(1)%nh4` | timestep == "mo" (line 52), timestep == "yr" (line 58), or timestep == "aa" (line 65) | Incremented by `hnb_d(j)%nh4atmo`, adding the day's total atmospheric NH4 input to the mineral ammonium pool in the first soil layer of HRU `j`. Makes deposited NH4 available to nitrification and plant uptake routines in the same daily step. |

## File I/O

<!-- facts:io -->


## Theory Equations

| Eq. | Title | Formula | Implementation |
| --- | --- | --- | --- |
| 3:1.5.1 | Nitrate from rainfall wet deposition | $NO_{3rain}=0.01*R_{NO3}*R_{day}$ | no3atmo+=0.01*R_NO3_conc*precip (all three timestep modes). Exact match for NO3_rain=0.01*R_NO3*R_day. |
| 3:1.5.2 | Ammonium from rainfall wet deposition | $NH_{4rain}=0.01*R_{NH4}*R_{day}$ | nh4atmo+=0.01*R_NH4_conc*precip. Exact match for NH4_rain=0.01*R_NH4*R_day. |
| 3:1.5.3 | NO3 dry deposition to top soil layer | $NO_{3_{ly=1}}=NO_{3_{ly=1}}+NO_{3_{drydep}}$ | Verified against SWAT+ 62.0.0 (nut_nrain.f90:49). no3atmo = .01*no3_rfmo*precip + no3_drymo/const`; added to layer 1 (:50) |
| 3:1.5.4 | NH4 dry deposition to top soil layer | $NH_{4_{ly=1}}=NH_{4_{ly=1}}+NH_{4_{drydep}}$ | nh4atmo includes nh4_dry/ndays; added to mn(1)%nh4 (lines 52,58,65). Matches NH4_ly1=NH4_ly1+NH4_drydep. |

## Lineage

Three source-backed commits touch `nut_nrain.f90:1-69`. The most recent (39fabde, 2024-08-08) ran a Python script to initialize variables, corrected input data where integers were used as floats in two input files, trapped underflow errors in three files, and updated test output data; its specific effect on `nut_nrain` is unclear from the commit subject. Commit 94b6dec (2024-05-30) added the latest source from a Bitbucket mirror; the specific changes to `nut_nrain` relative to the prior state are unclear. Commit df07e3f (2024-03-05) performed an all-variable initialization pass; specific changes to this routine are unclear from the subject.

- {'commit': '39fabde', 'date': '2024-08-08', 'subject': 'Initialized varables with python script, corrected input data where integers where floats in two input files, trapped underflow errors in three files where an exp function was done on too negative of a number and updated the data/Ames_sub1 output data to reflect the input data changes against the intel complied version.', 'impact': 'Variable initialization and input data corrections; the specific impact on `nut_nrain` is unclear from the commit subject.'}
- {'commit': '94b6dec', 'date': '2024-05-30', 'subject': 'Added latest source code from bitbucket', 'impact': 'Full source import from Bitbucket mirror; the specific changes to `nut_nrain` relative to the prior state are unclear from the commit subject.'}
- {'commit': 'df07e3f', 'date': '2024-03-05', 'subject': 'init all', 'impact': 'All-variable initialization pass; the specific changes to `nut_nrain` are unclear from the commit subject.'}

## Review Notes

- No direct file I/O was extracted for this procedure.
- warning: missing_doc: Procedure 'nut_nrain' has no extracted documentation comment.
- algorithm_steps revised: added step 1 (setup lines 38-42) which the parser omitted; expanded steps 2-5 to describe branch content rather than just the if-condition; corrected core_graph to show that the 'aa' branch (line 61) is outside the ist validity guard from line 46, not nested within it; reduced parser's 5 steps to 6 clearer steps.
- basin_module: `ndays` and `time%mo` (used at line 48) are not listed in the resolved outside-reference ownership table. They appear in the candidate outside references as `time%mo` only. Ownership assigned to `basin_module` by elimination; a human reviewer should confirm these symbols originate there.
- The 'mo' and 'yr' deposition branches are independent if-statements (not else-if), meaning both checks execute when ist is valid. In practice they are mutually exclusive because `atmodep_cont%timestep` holds one value per model run, but the code does not use else-if.
