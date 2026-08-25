---
kind: procedure
symbol: nut_pminrl2
title: nut_pminrl2
status: filled
source_hash: 693ab9ba90ede081
version_label: SWAT+ 62.0.0
locals:
  j: HRU index copied from `ihru`; it selects the current HRU record in `soil`, `soil1`, and
    `hnb_d` that this subroutine updates.
  l: Loop counter for soil layers within the current HRU, running from 1 to `soil(j)%nly`.
  rto: The target active-to-solution ratio implied by the current PSP value, computed as `psp
    / (1. - psp)` and used to gauge imbalance between labile and active pools.
  rmp1: The net labile-to-active phosphorus imbalance in kg P/ha, later adjusted by a dynamic
    transfer coefficient and wetness before being applied to the pools.
  roc: The net active-to-stable phosphorus transfer in kg P/ha, computed from the active/stable
    ratio and a calcium-based rate coefficient, then moderated by wetness.
  wetness: A 0.25-to-1.0 scaling factor derived from soil water storage relative to field
    capacity; it reduces phosphorus movement in dry layers.
  base: An intermediate value used when computing the active-to-stable transfer rate coefficient
    `varc`.
  vara: Intermediate coefficient for the labile-to-active transfer rate; it is computed from
    PSP with an exponential decay expression.
  varb: Exponent used with `a_days` to smooth the labile-to-active transfer rate over time
    since the last positive imbalance.
  varc: Intermediate coefficient for the active-to-labile transfer rate; it is derived from
    `base` and then bounded before scaling `rmp1`.
  as_p_coeff: Active-to-stable phosphorus rate coefficient based on layer calcium content
    (`soil(j)%ly(l)%cal`), capped to a narrow range before scaling `roc`.
  solp: Labile phosphorus concentration in mg/kg, computed from `soil1(j)%mp(l)%lab` and the
    layer conversion weight; it feeds PSP and the total-P limit check.
  actpp: Active mineral phosphorus concentration in mg/kg, computed from `soil1(j)%mp(l)%act`
    and used to estimate the active/stable ratio and total P.
  stap: Stable mineral phosphorus concentration in mg/kg, computed from `soil1(j)%mp(l)%sta`
    and used in the total P limit check.
  arate: Dynamic labile-to-active transfer coefficient, smoothed from `vara` and `a_days`
    and then bounded before scaling `rmp1`.
  ssp: Estimated active/stable phosphorus ratio used to compute `roc`, smoothed against the
    stored prior-day value and bounded to measured-data limits.
  psp: Phosphorus saturation ratio for the layer, estimated from clay, solution P, and organic
    carbon, then bounded and smoothed against yesterday’s stored value.
uses:
  basin_module: '`basin_module` is needed because the routine is called in the HRU processing
    context and relies on basin-level model state to be consistent with the current watershed
    run; the packet shows no specific resolved symbols from this module, so only its general
    role in the model state is certain.'
  organic_mineral_mass_module: '`organic_mineral_mass_module` supplies the layered mineral
    phosphorus storage for the current HRU. `nut_pminrl2` reads and updates `soil1(j)%mp(l)%lab`,
    `act`, and `sta` to move phosphorus among pools, and uses `soil1(j)%cbn(l)` in the PSP
    estimate.'
  hru_module: '`hru_module` provides `ihru`, which identifies the HRU whose soil and output
    records are being updated. Without `ihru`, the routine would not know which `soil1`, `soil`,
    and `hnb_d` entries to modify.'
  output_landscape_module: '`output_landscape_module` provides the daily nutrient-balance
    output record `hnb_d`. The routine accumulates layer transfers into `hnb_d(j)%lab_min_p`
    and `hnb_d(j)%act_sta_p` so downstream reporting can summarize phosphorus movement for
    the current HRU.'
  soil_module: '`soil_module` provides the soil-layer geometry and hydraulic/chemical properties
    that control the calculations. `soil(j)%nly`, `conv_wt`, `clay`, `cal`, `st`, `fc`, `psp_store`,
    `ssp_store`, `a_days`, `b_days`, and `watp` determine how concentrations are computed,
    how transfer rates are smoothed, and how wetness limits movement.'
  time_module: '`time_module` supplies the simulation day and year. The routine uses `time%day`
    and `time%yrs` to reset the P-imbalance counters at the start of the simulation so the
    smoothing terms begin from a clean state.'
---

<!-- facts:header -->

Updates labile, active, and stable soil phosphorus pools for the current HRU using the alternate phosphorus model of Vadas and White (2010). It also accumulates daily HRU phosphorus flux totals for reporting.

## Bottom Line

`nut_pminrl2` loops through every soil layer in the current HRU and moves phosphorus among the labile, active mineral, and stable mineral pools. It first protects against zero or negative pool values, converts the pools to comparable units, estimates a phosphorus saturation ratio from soil properties, and smooths that ratio against the previous day’s stored value.

The routine then computes two transfers: labile to active when the solution/active balance favors that direction, and active to stable using a calcium-carbonate-based coefficient and a smoothed active/stable ratio. Both transfers are moderated by soil wetness, constrained so total phosphorus stays below a hard upper limit, written back to `soil1` and `soil`, and accumulated into `hnb_d(j)%lab_min_p` and `hnb_d(j)%act_sta_p` for output tracking.

## Arguments

<!-- facts:arguments -->

## Where It Fits

This routine runs inside `hru_control` when `bsn_cc%sol_P_model == 1`, after other HRU nutrient/carbon process routines have prepared the daily state. It uses the current HRU, soil, and time state to update phosphorus pools, and its results feed daily phosphorus accounting in `hnb_d` as well as later soil-water-linked phosphorus behavior through the updated `soil1` and `soil` records.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. Select the current HRU and initialize daily nutrient-balance totals. | Copies `ihru` into `j`, clears `hnb_d(j)%lab_min_p` and `hnb_d(j)%act_sta_p`, and starts the layer loop over `soil(j)%nly`. |
| 2. Prevent zero or negative phosphorus pools from entering the math. | Raises any nonpositive labile, active, or stable pool in `soil1(j)%mp(l)` to a small floor of `1.e-6` so the ratios and logs stay defined. |
| 3. Convert pool masses to comparable layer concentrations. | Computes `solp`, `actpp`, and `stap` from the three mineral phosphorus pools using the layer conversion weight `soil(j)%phys(l)%conv_wt`. |
| 4. Estimate and smooth the phosphorus saturation ratio. | Calculates PSP from clay, solution P, and organic carbon; bounds it to the allowed range; smooths it with `soil(j)%ly(l)%psp_store` if present; and stores the result back for tomorrow's smoothing step. |
| 5. Reset the imbalance counters on the first simulation day. | On day 1 of year 1, clears `soil(j)%ly(l)%a_days` and `soil(j)%ly(l)%b_days` so the dynamic rate history starts at zero. |
| 6. Compute the labile-to-active transfer amount and adjust it for timing history. | Derives `rto` and the initial imbalance `rmp1`, then when the layer is net labile-rich computes `vara`, `varb`, and `arate`, bounds the coefficient, scales `rmp1`, and updates `a_days`/`b_days`. |
| 7. Compute the active-to-labile transfer amount and adjust it for timing history. | When the layer is net active-rich, limits `rmp1`, computes `base` and `varc`, bounds the coefficient, scales the transfer, resets `a_days`, and increments `b_days`. |
| 8. Estimate the active-to-stable transfer coefficient and ratio. | Calculates `as_p_coeff` from layer calcium, estimates `ssp` from active phosphorus and `rto`, bounds and smooths `ssp`, computes `roc`, and stores the smoothed ratio in `soil(j)%ly(l)%ssp_store`. |
| 9. Reduce transfers when the layer is dry. | Computes wetness from soil water and field capacity, limits it to 0.25-1.0, and scales both `rmp1` and `roc` so dry layers move less phosphorus. |
| 10. Apply the pool updates only when total P stays below the hard cap. | If total layer P is below 10000 mg/kg, updates stable, active, and labile pools by `roc` and `rmp1` and clips any negative result back to zero. |
| 11. Update water-soluble P and daily output totals for the layer. | Sets `soil(j)%ly(l)%watp` from the labile pool and accumulates the layer fluxes into the HRU daily output record `hnb_d(j)`. |
| 12. Finish the HRU layer loop and return. | Ends the layer iteration and returns to the caller after all HRU layers have been processed. |
| 13. algorithm_steps revised: merged the repeated labile/active transfer handling into separate forward and reverse flux steps and kept the stable-flux, wetness, and pool-update phases distinct. | The source is organized around three coupled phosphorus transformations plus wetness and cap checks, so the steps were re-grouped to match the model logic rather than the original line block breaks. |

## Modules Used

<!-- facts:uses -->

| Module | State touched | Key components |
| --- | --- | --- |
| [sym:basin_module] | `ihru` |  |
| [sym:organic_mineral_mass_module] | `soil1` | `soil1(j)%mp(l)%lab, soil1(j)%mp(l)%act, soil1(j)%mp(l)%sta, soil1(j)%cbn(l)` |
| [sym:hru_module] | `ihru` |  |
| [sym:output_landscape_module] | `hnb_d` | `hnb_d(j)%lab_min_p, hnb_d(j)%act_sta_p` |
| [sym:soil_module] | `soil` | `soil(j)%nly, soil(j)%phys(l)%conv_wt, soil(j)%phys(l)%clay, soil(j)%ly(l)%psp_store, soil(j)%ly(l)%a_days, soil(j)%ly(l)%b_days, soil(j)%ly(l)%cal, soil(j)%ly(l)%ssp_store, soil(j)%phys(l)%st, soil(j)%phys(l)%fc, soil(j)%ly(l)%watp` |
| [sym:time_module] | `time` | `time%day, time%yrs` |

## Local Variables

<!-- facts:locals -->

## State Changes

| Target | When | Meaning |
| --- | --- | --- |
| `hnb_d(j)%lab_min_p` | Each layer when daily fluxes are reset at the top of the routine. | `hnb_d(j)%lab_min_p` is cleared to start a new daily accumulation of labile-to-active phosphorus movement for the current HRU. |
| `hnb_d(j)%act_sta_p` | Each layer when daily fluxes are reset at the top of the routine. | `hnb_d(j)%act_sta_p` is cleared to start a new daily accumulation of active-to-stable phosphorus movement for the current HRU. |
| `soil(j)%ly(l)%psp_store` | When `soil(j)%ly(l)%psp_store > 0.` and the layer PSP is smoothed. | `soil(j)%ly(l)%psp_store` is overwritten with today's PSP so the next day can form a 30-day smoothing average. |
| `soil(j)%ly(l)%a_days` | On the first simulation day (`time%day == 1` and `time%yrs == 1`). | `soil(j)%ly(l)%a_days` is reset to zero so the labile-to-active transfer history starts from the beginning of the run. |
| `soil(j)%ly(l)%b_days` | When the layer has a net active-rich imbalance (`rmp1 < 0.`). | `soil(j)%ly(l)%b_days` is incremented because the layer has spent another day with active phosphorus in excess of labile phosphorus. |
| `soil(j)%ly(l)%ssp_store` | When `soil(j)%ly(l)%ssp_store > 0.` and today's SSP is smoothed. | `soil(j)%ly(l)%ssp_store` is updated to preserve the smoothed active/stable ratio for tomorrow's calculation. |
| `soil1(j)%mp(l)%sta` | If total layer phosphorus is below `10000.` mg/kg. | `soil1(j)%mp(l)%sta` receives the active-to-stable transfer `roc`, unless the result would go negative, in which case it is clipped to zero. |
| `soil1(j)%mp(l)%act` | If total layer phosphorus is below `10000.` mg/kg. | `soil1(j)%mp(l)%act` is reduced by `roc` and adjusted by `rmp1`; the value is clipped at zero if the update would make it negative. |
| `soil1(j)%mp(l)%lab` | If total layer phosphorus is below `10000.` mg/kg. | `soil1(j)%mp(l)%lab` is reduced by `rmp1`, with a zero floor to prevent negative labile phosphorus after the transfer. |
| `soil(j)%ly(l)%watp` | Each layer after wetness scaling and the total-P cap check. | `soil(j)%ly(l)%watp` is set from the updated labile pool so layer water-soluble phosphorus tracks the current mineral phosphorus state. |

## File I/O

<!-- facts:io -->


## Lineage

`nut_pminrl2` was added in commit df07e3f as a new subroutine implementing the alternate phosphorus model. Commit 94b6dec preserved the same logic but adjusted the source text and line count when the file was imported from Bitbucket, and 39fabde and f1e61a3 only changed initializer formatting and whitespace/tab alignment without altering the algorithm.

- df07e3f introduced the full labile-active-stable phosphorus transformation routine, including PSP/SSP smoothing, wetness scaling, and daily HRU output accumulation.
- 94b6dec re-imported the file with one extra line of source spacing but did not change the computational behavior.
- 39fabde added default zero initializers to local scalars such as `j`, `l`, `rto`, `rmp1`, `roc`, `wetness`, `base`, `vara`, `varb`, `varc`, `as_p_coeff`, `solp`, `actpp`, `stap`, `arate`, `ssp`, and `psp`.
- f1e61a3 only normalized tabs and spacing in comments and aligned declarations; it did not change model calculations.

## Review Notes

- No direct file I/O was extracted for this procedure.
- warning: missing_doc: Procedure 'nut_pminrl2' has no extracted documentation comment.
- algorithm_steps revised: merged and regrouped the source blocks into model phases while keeping real source line citations.
- `basin_module` has no resolved candidate outside references in the packet; its role here is inferred only from the import and caller context.
- The calculated `solp`, `actpp`, and `stap` values in the source do not include the `* 1000000.` factor shown in an older lineage diff; the current line-numbered source is the evidence used here.
