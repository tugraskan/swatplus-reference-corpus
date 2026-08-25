---
kind: procedure
symbol: pl_seed_gro
title: pl_seed_gro
status: filled
source_hash: 16f723f909173112
version_label: SWAT+ 62.0.0
args:
  j: '`j` is the HRU/object index. It selects which community entry (`pcom(j)`) and linked
    weather station (`ob(j)%wst`) this plant-growth update is applied to.'
locals:
  idp: Plant database index for the current plant (`pcom(j)%plcur(ipl)%idplt`), used to look
    up species parameters such as `hvsti` and `t_opt` from `pldb`.
  ajhi: Working harvest-index value. It begins as the potential harvest index from heat-unit
    progress, then is reduced or capped by stress adjustments before being written back to
    plant state.
  ajhi_min: Lower bound used in the water-stress harvest-index adjustment. It is set to half
    of the current potential harvest index so the stress curve cannot reduce HI below that
    midpoint.
  dhi: Daily change in harvest index, computed as the difference between the new adjusted
    HI and the previous stored HI value. This increment is what gets accumulated into `hi_adj`.
  temp_dif: Temperature difference between the plant's optimal temperature and the current
    weather-station mean temperature. It drives the temperature-stress adjustment branch.
  temp_adj: Temperature-stress factor derived from `temp_dif`. It is bounded to 0–1 and represents
    how strongly unfavorable temperature should suppress harvest-index change.
  etr: Plant water-use ratio used in the harvest-index adjustment. It is based on cumulative
    actual ET divided by cumulative potential ET and then transformed through a logistic stress
    curve.
  xyz: Scratch integer used only for the special `j == 985` branch. In the extracted source
    it is assigned `0` there and has no other visible effect.
uses:
  plant_data_module: '`plant_data_module` provides the plant-species database entry `pldb(idp)`,
    which supplies the harvest-index ceiling (`hvsti`) and optimum temperature (`t_opt`) that
    control both stress limits and temperature adjustment.'
  basin_module: '`basin_module` is imported by this procedure, but the extracted source does
    not show any referenced symbols from it. It matters because basin-level shared state can
    affect plant routines even when no specific variable is visible in this span.'
  hru_module: '`hru_module` supplies the active plant index `ipl` and the daily ET terms `ep_day`
    and `pet_day`. Those values are needed to accumulate plant water use and potential demand
    for the current HRU-day.'
  plant_module: '`plant_module` holds the active plant community state that this routine reads
    and updates: the current plant identity, accumulated PHU, harvest index, ET accumulators,
    and previous/adjusted harvest-index fields. Without this shared plant state the routine
    could not update seed growth for the correct plant.'
  carbon_module: '`carbon_module` is imported as part of the plant-growth state environment,
    but the extracted source shows no direct symbol use here. It matters because carbon bookkeeping
    is part of the broader plant-growth workflow this routine participates in.'
  organic_mineral_mass_module: '`organic_mineral_mass_module` is imported for shared mass-state
    types used in plant and residue processes, though no direct symbol from it appears in
    this excerpt. It matters because harvest-index updates feed later biomass and residue
    allocation.'
  climate_module: '`climate_module` provides the weather-station daily mean temperature `wst(iwst)%weat%tave`,
    which is compared with the plant''s optimal temperature to compute the temperature-stress
    factor.'
  hydrograph_module: '`hydrograph_module` provides the HRU/object connectivity lookup `ob(j)%wst`
    used to select the correct weather station index for the current object. That index links
    this plant routine to the appropriate climate record.'
---

<!-- facts:header -->

Updates seasonal seed/growth harvest index for a plant in one HRU. It accumulates plant ET after midseason, adjusts harvest index for water and temperature stress, and stores the adjusted index for later growth and partitioning steps.

## Bottom Line

`pl_seed_gro` is a plant-growth utility that recalculates the current harvest index for the active plant in HRU `j`. It starts from the potential harvest index curve based on heat-unit progress, then adjusts that value using accumulated actual vs. potential plant ET and a temperature-stress check tied to the weather station for the HRU.

The routine also maintains running plant-growth state: it adds daily ET totals to `plet` and `plpet`, updates `hi_prev` and `hi_adj`, and caps the adjusted harvest index at the species-specific maximum `hvsti`. The callers use this during transplanting, daily growth, and initialization so later partitioning and biomass/yield behavior can use the updated seed/growth state.

## Arguments

<!-- facts:arguments -->

## Where It Fits

This routine runs during plant initialization and daily plant growth, after upstream code has set the current plant (`ipl`), HRU/object mapping (`j`), and species parameters/initial plant state. `mgt_transplant`, `pl_grow`, and `plant_init` all prepare that context before calling it. Its results are used immediately by `pl_partition` and by later growth logic that depends on the updated `hi_prev`, `hi_adj`, `plet`, and `plpet` values.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. Load the plant and weather indices, then compute the potential harvest index. | The routine reads the current plant ID from `pcom(j)%plcur(ipl)%idplt`, maps the HRU to its weather station with `ob(j)%wst`, and computes `ajhi` from the plant's base harvest index and accumulated PHU using the logistic potential-harvest-index curve. |
| 2. Only proceed with ET-based updates after the plant is past early growth. | When `phuacc > 0.5`, the routine starts accumulating actual plant ET and potential plant ET into `plet` and `plpet`. Before that threshold, the seasonal seed-growth update is skipped. |
| 3. Convert accumulated ET into a water-stress ratio and adjust harvest index. | If potential ET is nontrivial, the routine computes `etr = 100*plet/plpet`, sets a midpoint lower bound `ajhi_min = ajhi/2`, and rescales `ajhi` with a logistic water-stress curve. The result is capped at the species maximum `pldb(idp)%hvsti`. |
| 4. Fall back to a default water-stress ratio when no potential ET has accumulated. | If `plpet` is too small to form a ratio, the routine sets `etr = 1.` so the later adjustment logic still has a defined value. |
| 5. Leave a special-case debug marker for HRU 985. | For `j == 985`, the routine assigns `xyz = 0`. The extracted source shows no other effect, so this appears to be a placeholder or debugging hook. |
| 6. Compute the daily harvest-index increment from the previous value. | The routine sets `dhi` to the difference between the newly adjusted harvest index and `hi_prev`, creating the daily increment that will be accumulated into `hi_adj`. |
| 7. Transform the ET ratio into a bounded stress factor. | `etr` is passed through the same logistic form and then clamped to the 0–1 range. This produces a bounded water-stress factor for later use in the routine. |
| 8. Compute the temperature-stress factor when the day is hotter than optimum late in the season. | The routine compares the species optimum temperature with the current station mean temperature. If the day is hotter than optimum and the crop has reached `phuacc > 0.7`, it computes `temp_adj` from an exponential decay and clamps it to 0–1; otherwise it leaves `temp_adj = 1.`. |
| 9. Update adjusted harvest index and persist the new previous value. | The routine adds `dhi` into `hi_adj`, caps `hi_adj` between 0 and `hvsti`, and stores the current `ajhi` into `hi_prev` for the next call. If the crop is not past the `phuacc > 0.5` gate, it resets `hi_prev` to zero instead. |
| 10. Return to the caller. | The subroutine ends after updating the plant state, leaving the caller to continue with partitioning or later growth steps. |

## Modules Used

<!-- facts:uses -->

| Module | State touched | Key components |
| --- | --- | --- |
| [sym:plant_data_module] | `pldb` | `pldb(idp)%hvsti, pldb(idp)%t_opt` |
| [sym:basin_module] | `basin_module` | `none resolved` |
| [sym:hru_module] | `ep_day, ipl, pet_day` |  |
| [sym:plant_module] | `pcom` | `pcom(j)%plcur(ipl)%idplt, pcom(j)%plcur(ipl)%harv_idx, pcom(j)%plcur(ipl)%phuacc, pcom(j)%plg(ipl)%plet, pcom(j)%plg(ipl)%plpet, pcom(j)%plg(ipl)%hi_prev, pcom(j)%plg(ipl)%hi_adj` |
| [sym:carbon_module] | `carbon_module` | `none resolved` |
| [sym:organic_mineral_mass_module] | `organic_mineral_mass_module` | `none resolved` |
| [sym:climate_module] | `wst` | `wst(iwst)%weat%tave` |
| [sym:hydrograph_module] | `ob, iwst` | `ob(j)%wst` |

## Local Variables

<!-- facts:locals -->

## State Changes

| Target | When | Meaning |
| --- | --- | --- |
| `iwst` | Always at entry, after `idp` is resolved from the current plant and `ob(j)%wst` is read. | `iwst` is set to the weather-station index for the current HRU/object so the routine can read the correct temperature record from `wst(iwst)`. |
| `pcom(j)%plg(ipl)%plet` | When `phuacc > 0.5`, the routine advances seasonal seed growth for the current day. | `plet` is increased by the day's actual plant ET (`ep_day`) so the routine keeps a running total of water actually used by the plant after midseason. |
| `pcom(j)%plg(ipl)%plpet` | When `phuacc > 0.5`, the routine advances seasonal seed growth for the current day. | `plpet` is increased by the day's potential plant ET (`pet_day`) so the routine keeps the corresponding demand total needed for the ET ratio. |
| `pcom(j)%plg(ipl)%hi_adj` | After the daily harvest-index increment is computed and before the routine exits the growth branch. | `hi_adj` accumulates the daily harvest-index change `dhi`, then is constrained to the range 0 to `hvsti` so later partitioning uses a physically bounded adjusted HI. |
| `pcom(j)%plg(ipl)%hi_prev` | On every call after `ajhi` is computed, or reset to zero when `phuacc <= 0.5`. | `hi_prev` stores the current harvest index for use on the next day; it is reset to zero before the plant reaches the PHU threshold and otherwise updated to the new adjusted `ajhi`. |

## File I/O

<!-- facts:io -->


## Theory Equations

| Eq. | Title | Formula | Implementation |
| --- | --- | --- | --- |
| 5:2.4.1 | Potential harvest index curve | $HI=HI_{opt}*\frac{100*fr_{PHU}}{(100*fr_{PHU}+exp[11.1-10*fr_{PHU}])}$ | ajhi = harv_idx*100*phuacc/(100*phuacc + exp(11.1 - 10*phuacc)). |
| 5:3.3.1 | Actual harvest index under water stress | $HI_{act}=(HI-HI_{min})*\frac{\gamma _{wu}}{\gamma _{wu}+exp[6.13-0.883*\gamma _{wu}]}+HI_{min}$ | ajhi is adjusted using the cumulative ET ratio etr and then limited by hvsti. This matches the page's logistic water-use adjustment concept, with an explicit cap at hvsti. |
| 5:3.3.2 | Cumulative water-use ratio for yield adjustment | $\gamma_{wu}=100*\frac{\sum^m_{i=1} E_a}{\sum ^m_{i=1} E_o}$ | etr = 100*plet/plpet, where plet and plpet accumulate actual and potential plant ET after midseason. |
| 5:2.4.2 | Yield from above-ground biomass when HI <= 1 | $yld=bio_{ag}*HI$ | Verified against SWAT+ 62.0.0 (pl_seed_gro.f90:44). if (ajhi > hvsti) ajhi = hvsti` — HI≤1 cap |
| 5:2.4.3 | Yield relation when harvest index exceeds 1 | $yld=bio*(1-\frac{1}{(1+HI)})$ | Verified against SWAT+ 62.0.0 (pl_seed_gro.f90:44). HI>1 clamp (same line) |

## Lineage

Resolved lineage shows four source changes for `pl_seed_gro`. The routine was introduced in commit `df07e3f` with the harvest-index and ET-stress logic. Commit `bd18ad4` added the external declaration `aunif` near the top of the file. Commit `39fabde` initialized the local variables `idp`, `ajhi`, `ajhi_min`, `dhi`, `temp_dif`, `temp_adj`, `etr`, and `xyz` with zero values. Commit `94b6dec` matches the original addition of the routine and its core logic; the diff snippet in the packet does not show a later behavior change beyond that initial implementation.

- Introduced `pl_seed_gro` with the PHU-gated ET accumulation, water-stress harvest-index adjustment, temperature-stress check, and `hi_prev`/`hi_adj` state updates.
- Added the `aunif` external declaration, though the extracted source excerpt does not show it being used in the routine body.
- Initialized all local working variables to zero to avoid undefined values in the harvest-index and stress calculations.

## Review Notes

- No direct file I/O was extracted for this procedure.
- warning: missing_doc: Procedure 'pl_seed_gro' has no extracted documentation comment.
- algorithm_steps revised: reordered the source-line steps to follow the actual control flow and merged the final return into a single terminal step.
- `basin_module`, `carbon_module`, and `organic_mineral_mass_module` are imported by the source but no direct candidate symbols from those modules were resolved in the extracted evidence; descriptions note that uncertainty instead of inventing specific references.
