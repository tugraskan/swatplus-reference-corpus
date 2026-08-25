---
kind: procedure
symbol: hru_urbanhr
title: hru_urbanhr
status: filled
source_hash: fb9fe90edb1acce2
version_label: SWAT+ 62.0.0
locals:
  sus_sol: Suspended-solids load in the urban runoff event, computed from the amount of dirt
    washed off streets and then used to derive TSS loading.
  tn: Total nitrogen associated with the washed-off suspended solids; it is converted from
    suspended solids concentration and used to update urban nitrogen runoff load.
  tp: Total phosphorus associated with the washed-off suspended solids; it is converted from
    suspended solids concentration and used to update urban phosphorus runoff load.
  urbk: Urban wash-off coefficient for the current subdaily step, derived from the urban database
    coefficient and runoff intensity.
  dirto: Street-dirt buildup at the start of the time step before wash-off is applied.
  j: Current HRU index, copied from `ihru` so the routine can read and update the correct
    HRU state.
  qdt: Subdaily urban runoff intensity in mm/hr, computed from `ubnrunoff(k)` and the model
    time-step length.
  k: Loop counter over the subdaily time steps in the day.
  tno3: Nitrate nitrogen associated with the washed-off suspended solids; it is converted
    from the urban database concentration and used to update surface NO3 load.
uses:
  hru_module: '`hru_module` provides the HRU identity, urban land-use code, subdaily urban
    runoff and load arrays, sweep scheduling state, plant-competition flags, and the initial
    abstraction store that this routine reads and updates for the selected HRU.'
  plant_module: '`plant_module` supplies plant-status state used to decide whether sweeping
    is tied to dormant-season heat-unit progress or to current plant heat-unit accumulation
    when a sweep schedule is not active.'
  urban_data_module: '`urban_data_module` supplies the urban parameter record for the HRU''s
    urban land-use code, including buildup limits, wash-off rate, and constituent concentrations
    that control the load calculations.'
  climate_module: '`climate_module` is imported here because this routine is part of the climate-driven
    daily/subdaily simulation context, even though no candidate symbol from that module is
    referenced in the extracted lines.'
  time_module: '`time_module` provides the current subdaily discretization and simulation
    day needed to loop through the day, convert runoff to an hourly intensity, and decide
    whether a scheduled street sweep can occur.'
---

<!-- facts:header -->

Computes subdaily urban HRU loadings with a buildup/wash-off routine and triggers street sweeping when conditions are met.

## Bottom Line

`hru_urbanhr` updates urban impervious-surface buildup and wash-off for each subdaily time step. It uses HRU land-use settings, urban parameter values, runoff intensity, and the current simulation day to compute solids loading and associated nitrogen/phosphorus loads.

When there is enough runoff, it converts the current street dirt buildup into washed-off TSS and nutrient loads, updates the buildup timer, and stores the resulting loads back into shared HRU state. When runoff is absent, it advances buildup time and may call `hru_sweep` to simulate street sweeping based on a scheduled sweep date or plant-growth thresholds.

## Arguments

<!-- facts:arguments -->

## Where It Fits

`hru_control` calls this routine for HRUs whose land use has `urb_lu > 0` when the simulation is running with more than one time step per day (`time%step > 1`). `hru_urbanhr` prepares the subdaily urban runoff and load state used later by the HRU sediment and runoff-storage routines, and its sweep decisions affect the urban buildup state carried into later calls.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. Select the active HRU and its urban land use. | The routine copies the current HRU index from `ihru` into `j` and looks up the HRU's urban land-use code as `ulu = hru(j)%luse%urb_lu` so later calculations can use the correct urban parameter set and shared HRU arrays. |
| 2. Loop over each subdaily time step. | The routine iterates from `k = 1` to `time%step`, processing urban buildup and wash-off separately for each subdaily interval. |
| 3. Compute the subdaily runoff intensity and test for runoff-driven wash-off. | It converts `ubnrunoff(k)` to a runoff intensity `qdt` in mm/hr and treats the interval as a rainy/wash-off event when `qdt > 0.025` and `surfq(j) > 0.1`. |
| 4. Reconstruct the pre-wash dirt load and the wash-off rate. | The routine resets `dirt` and `dirto`, computes the starting curb dirt load from `urbdb(ulu)%dirtmx` and `twash(j)`, builds the wash-off coefficient `urbk` from `urbdb(ulu)%urbcoef` and `qdt`, and applies exponential decay to get the dirt remaining after wash-off. |
| 5. Limit tiny remaining dirt and back-calculate the new buildup time. | If the remaining dirt is negligible it is forced to zero, then `twash(j)` is reset and recomputed as the equivalent buildup time corresponding to the post-wash dirt amount. |
| 6. Convert washed-off dirt into solids and nutrient loads. | The routine clears `sus_sol`, `tn`, `tp`, and `tno3`, then calculates suspended solids from the dirt removed and converts that mass into total nitrogen, total phosphorus, and nitrate nitrogen using the urban concentration parameters. |
| 7. Write the event loads back to the HRU state. | It stores the TSS event load in `ubntss(k)` and updates the surface runoff nutrient state arrays using the urban impervious fraction `urbdb(ulu)%fimp` so only the connected impervious portion contributes to the HRU-wide runoff loads. |
| 8. Advance buildup when there is no effective surface runoff. | When runoff is too small for wash-off, the routine increases `twash(j)` by the fraction of a day represented by the current time step so dirt buildup continues to accumulate. |
| 9. Check whether street sweeping should run during the no-runoff branch. | If a sweep date has been reached, or if a nonzero sweep threshold has been exceeded by either `phubase(j)` or `pcom(j)%plcur(1)%phuacc` depending on whether plant growth is active, the routine calls `hru_sweep`. |
| 10. Reset the temporary solids accumulator for the next subdaily step. | The routine clears `sus_sol` again before leaving the loop body so the next interval starts from a clean temporary solids state. |
| 11. Reduce impervious initial abstraction by the day's evaporation share. | After each subdaily interval, it subtracts `etday / time%step` from `init_abstrc(j)` and floors the value at zero so impervious water storage declines with evapotranspiration. |
| 12. After the loop, apply the final no-runoff sweep gate. | When final surface runoff is below the threshold, the routine repeats the sweep-date and plant-threshold checks and may call `hru_sweep` one more time before returning. |

## Modules Used

<!-- facts:uses -->

| Module | State touched | Key components |
| --- | --- | --- |
| [sym:hru_module] | `hru, twash, surqno3, sedorgn, sedorgp, surqsolp, ubnrunoff, surfq, ubntss, isweep, phusw, phubase, init_abstrc, ihru, ulu, etday, ipl` | `hru(j)%luse%urb_lu` |
| [sym:plant_module] | `pcom` | `pcom(j)%plcur(ipl)%gro, pcom(j)%plcur(1)%phuacc` |
| [sym:urban_data_module] | `urbdb` | `urbdb(ulu)%dirtmx, urbdb(ulu)%urbcoef, urbdb(ulu)%tnconc, urbdb(ulu)%tpconc, urbdb(ulu)%tno3conc, urbdb(ulu)%fimp` |
| [sym:climate_module] | `time` | `time%step, time%dtm, time%day` |
| [sym:time_module] | `time` | `time%step, time%dtm, time%day` |

## Local Variables

<!-- facts:locals -->

## State Changes

| Target | When | Meaning |
| --- | --- | --- |
| `ulu` | When the current HRU is urban (`ulu = hru(j)%luse%urb_lu`) and a sweep is triggered by `isweep(j) > 0 .and. time%day >= isweep(j)` or by the plant-heat-unit condition in the no-runoff branch. | `ulu` changes once at the start of the routine to cache the urban land-use index for the active HRU; it does not vary afterward and is used to select the correct row in `urbdb`. |
| `dirt` | When runoff is large enough for wash-off (`qdt > 0.025 .and. surfq(j) > 0.1`) and the routine reconstructs the pre-wash dirt load. | `dirt` holds the remaining curb dirt after exponential wash-off; it is a local working value used to derive the new buildup time and event loads. |
| `twash(j)` | During the runoff branch after wash-off is computed, using `twash(j) = urbdb(ulu)%thalf * dirt / (urbdb(ulu)%dirtmx - dirt)`; otherwise it is advanced by `time%dtm / 1440.` in the no-runoff branch. | `twash(j)` tracks how long dirt has been building on the impervious surface. It is shortened to match the post-wash dirt amount during runoff and increased during dry intervals. |
| `ubntss(k)` | When runoff wash-off occurs, `ubntss(k) = (.001*sus_sol*hru(j)%area_ha)*urbdb(ulu)%fimp`. | `ubntss(k)` stores the subdaily total suspended solids load from the urban impervious fraction for the current time step. |
| `surqno3(j)` | When runoff wash-off occurs, `surqno3(j) = tno3 * urbdb(ulu)%fimp + surqno3(j) * (1. - urbdb(ulu)%fimp)`. | `surqno3(j)` is blended so the urban impervious fraction contributes the event nitrate load while the remaining fraction retains its prior value. |
| `sedorgn(j)` | When runoff wash-off occurs, `sedorgn(j) = (tn - tno3) * urbdb(ulu)%fimp + sedorgn(j) * (1. - urbdb(ulu)%fimp)`. | `sedorgn(j)` is updated to include the organic nitrogen portion associated with washed-off urban solids on the connected impervious area. |
| `sedorgp(j)` | When runoff wash-off occurs, `sedorgp(j) = .75 * tp * urbdb(ulu)%fimp + sedorgp(j) * (1. - urbdb(ulu)%fimp)`. | `sedorgp(j)` is updated to include the organic phosphorus portion associated with washed-off urban solids on the connected impervious area. |
| `surqsolp(j)` | When runoff wash-off occurs, `surqsolp(j) = .25 * tp * urbdb(ulu)%fimp + surqsolp(j) * (1. - urbdb(ulu)%fimp)`. | `surqsolp(j)` is updated to include the soluble phosphorus portion associated with washed-off urban solids on the connected impervious area. |
| `init_abstrc(j)` | Every subdaily interval, after the runoff/no-runoff branch and before the loop advances again: `init_abstrc(j) = init_abstrc(j) - etday / time%step`, then clamped with `max(0., init_abstrc(j))`. | `init_abstrc(j)` is the impervious initial abstraction store; it is depleted by the day's evapotranspiration share so the HRU's available abstraction decreases over the day. |

## File I/O

<!-- facts:io -->


## Lineage

`hru_urbanhr.f90` was introduced in `df07e3f` (2024-03-05, "init all") and has been changed in 5 non-merge commit(s) since, most recently `bd18ad4` (2025-11-24, "Pr 107 (#108)"). Lineage is reconstructed from commit metadata (SHA, date, subject); per-line diffs were unavailable in this build environment, so only the commits touching `hru_urbanhr.f90` are listed.

- `bd18ad4` (2025-11-24) — Pr 107 (#108)
- `f1e61a3` (2024-10-08) — fixed tabs
- `39fabde` (2024-08-08) — Initialized varables with python script, corrected input data where integers where floats in two input files, trapped underflow errors in th…
- `94b6dec` (2024-05-30) — Added latest source code from bitbucket
- `df07e3f` (2024-03-05) — init all

## Review Notes

- No direct file I/O was extracted for this procedure.
- warning: missing_doc: Procedure 'hru_urbanhr' has no extracted documentation comment.
- algorithm_steps revised: merged the repeated final sweep logic into the step list as a distinct final check and kept the subdaily loop steps aligned to the visible source lines.
- The source contains a repeated street-sweeping block after the loop (lines 147-162) that mirrors the in-loop no-runoff sweep logic; the documentation treats it as an additional final gate because that is what the extracted source shows.
- Lineage was reconstructed from file-level commit metadata; per-line diffs were unavailable in this environment (blobless clone), so line-span filtering was not applied.
