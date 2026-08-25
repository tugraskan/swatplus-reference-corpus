---
kind: procedure
symbol: nut_pminrl
title: nut_pminrl
status: filled
source_hash: 9cb13ec87cebb84d
version_label: SWAT+ 62.0.0
locals:
  bk: Fixed coefficient that scales exchange between the active and stable mineral phosphorus
    pools; the source notes it was changed from 0.0006 to 0.01.
  j: Current HRU index copied from `ihru` so the routine can work on the active HRU's soil
    and output records.
  l: Loop counter for the soil layer currently being processed.
  rto: Threshold ratio derived from the HRU phosphorus sorption parameter `hru(j)%nut%psp
    / (1. - hru(j)%nut%psp)`; used to compare labile and active mineral P.
  rmp1: Provisional transfer amount between labile and active mineral P in a soil layer before
    rate limiting and capping to available labile P.
  roc: Provisional transfer amount between active and stable mineral P in a soil layer before
    rate limiting and capping to available active P.
uses:
  basin_module: This basin-level phosphorus parameter was the original source of the labile-to-active
    exchange threshold, and the lineage shows the routine was later changed to use the HRU-specific
    `hru(j)%nut%psp` instead. The module still matters because the routine's documented history
    and phosphorus setup are tied to that basin parameter.
  organic_mineral_mass_module: These are the layer-resolved inorganic phosphorus pools that
    the routine reads, adjusts, and writes back. They are the direct state variables being
    balanced between labile, active mineral, and stable mineral forms.
  hru_module: '`ihru` identifies the current HRU, and `hru(j)%nut%psp` supplies the phosphorus
    sorption parameter used to compute the transfer threshold `rto`. The routine''s behavior
    depends on the active HRU''s nutrient settings, not a single basin-wide value.'
  soil_module: '`soil(j)%nly` sets the number of soil layers to process, so it determines
    how many layer-by-layer phosphorus exchanges the routine performs for the current HRU.'
  output_landscape_module: This module holds the HRU nutrient-balance output record that receives
    the accumulated transfer totals. These fields matter because later reporting uses them
    to show how much P moved between pool pairs during the timestep.
---

<!-- facts:header -->

Moves inorganic phosphorus among labile, active mineral, and stable mineral soil pools for the current HRU, using the HRU-specific sorption parameter to set the exchange threshold.

## Bottom Line

`nut_pminrl` updates inorganic phosphorus in each soil layer of the current HRU. It computes how much P should move between the labile and active mineral pools, then how much should move between the active and stable mineral pools, using the HRU's phosphorus sorption parameter and a fixed exchange coefficient.

The routine also prevents any of the affected pools from going negative and accumulates the layer transfers into `hnb_d(j)%lab_min_p` and `hnb_d(j)%act_sta_p` for nutrient-balance output. It is called from `hru_control` during HRU processing when the model is using the soil phosphorus model.

## Arguments

<!-- facts:arguments -->

## Where It Fits

This routine runs during HRU control after other nutrient routines have been called for the current HRU, and before the model moves on to later HRU-specific processes such as septic biozone handling. `hru_control` prepares the current HRU context through `ihru` and the HRU/soil state, and the results here feed both the soil phosphorus state and the nutrient-balance output used later in landscape reporting.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. select current HRU | Copy the active HRU index from `ihru` into `j` so all following reads and writes target the current HRU's state records. |
| 2. reset P balance totals | Zero the HRU nutrient-balance accumulators for labile-to-active and active-to-stable phosphorus transfers before processing layers. |
| 3. compute sorption threshold ratio | Compute `rto` from the HRU phosphorus sorption parameter so the labile and active mineral pools can be compared against the model's exchange threshold. |
| 4. loop over soil layers | Process every soil layer in the current HRU from the top layer through `soil(j)%nly`. |
| 5. compute labile-active transfer demand | Form `rmp1` as the difference between labile P and the active-mineral threshold scaled by `rto`, giving the provisional labile-to-active exchange amount. |
| 6. limit transfer direction and size | Apply a 0.1 multiplier when the provisional transfer is positive, a 0.6 multiplier when it is negative, then cap the result so it cannot exceed the available labile phosphorus. |
| 7. compute active-stable transfer demand | Form `roc` from the active and stable mineral pools using the fixed coefficient `bk`, then reduce negative values and cap the result so it cannot exceed the available active phosphorus. |
| 8. update stable pool and protect against underflow | Add the active-to-stable transfer to the stable pool, then clamp the pool to zero if rounding or subtraction would make it negative. |
| 9. update active pool and protect against underflow | Subtract the active-to-stable transfer and add the labile-to-active transfer, then clamp the active pool to zero if needed. |
| 10. update labile pool and protect against underflow | Subtract the labile-to-active transfer from the labile pool and clamp it to zero if the result goes negative. |
| 11. accumulate nutrient-balance outputs | Add the layer's labile-to-active and active-to-stable transfers to the HRU nutrient-balance totals for later reporting. |
| 12. finish routine | Return to the caller after all HRU soil layers have been processed. |

## Modules Used

<!-- facts:uses -->

| Module | State touched | Key components |
| --- | --- | --- |
| [sym:basin_module] | `bsn_prm` | `bsn_prm%psp` |
| [sym:organic_mineral_mass_module] | `soil1` | `soil1(j)%mp(l)%lab, soil1(j)%mp(l)%act, soil1(j)%mp(l)%sta` |
| [sym:hru_module] | `hru, ihru` | `hru(j)%nut%psp` |
| [sym:soil_module] | `soil` | `soil(j)%nly` |
| [sym:output_landscape_module] | `hnb_d` | `hnb_d(j)%lab_min_p, hnb_d(j)%act_sta_p` |

## Local Variables

<!-- facts:locals -->

## State Changes

| Target | When | Meaning |
| --- | --- | --- |
| `hnb_d(j)%lab_min_p` | For every soil layer processed in the current HRU, after `rmp1` is limited and before the layer loop ends. | Accumulates the net amount of phosphorus transferred from the labile pool to the active mineral pool across all layers in the HRU. This supports nutrient-balance reporting for the current timestep. |
| `hnb_d(j)%act_sta_p` | For every soil layer processed in the current HRU, after `roc` is limited and before the layer loop ends. | Accumulates the net amount of phosphorus transferred from the active mineral pool to the stable mineral pool across all layers in the HRU. This supports nutrient-balance reporting for the current timestep. |
| `soil1(j)%mp(l)%sta` | For each layer, after the active-to-stable transfer `roc` is computed and before the layer loop ends. | Increases by `roc`, representing phosphorus that becomes part of the stable mineral pool in that layer; the value is clamped to zero if the update would underflow. |
| `soil1(j)%mp(l)%act` | For each layer, after both `roc` and `rmp1` are computed and before the layer loop ends. | Decreases by `roc` and increases by `rmp1`, representing the net change to the active mineral pool; the value is clamped to zero if the update would underflow. |
| `soil1(j)%mp(l)%lab` | For each layer, after `rmp1` is computed and before the layer loop ends. | Decreases by `rmp1`, representing phosphorus moving out of the labile pool into the active mineral pool; the value is clamped to zero if the update would underflow. |

## File I/O

<!-- facts:io -->


## Theory Equations

| Eq. | Title | Formula | Implementation |
| --- | --- | --- | --- |
| 3:2.3.1 | Phosphorus availability index PAI definition | $pai=\frac{P_{solution,f}-P_{solution,i}}{fert_{min,P}}$ | Verified against SWAT+ 62.0.0 (nut_pminrl.f90). |
| 3:2.3.2 | P moves from solution to active mineral pool | $P_{solution,ly}>minP_{act,ly}*(\frac{pai}{1-pai})$ | rmp1=lab-act*rto; if>0 then rmp1*=0.1 (rate limiter); lab>act*(psp/(1-psp)) triggers transfer. Matches P_solution>minP_act*(pai/(1-pai)). |
| 3:2.3.3 | P moves from active mineral to solution pool | $P_{solution,ly}<minP_{act,ly}*(\frac{pai}{1-pai})$ | rmp1<0 when lab<act*rto; rmp1*=0.6 back-rate. Matches P_solution<threshold condition. |
| 3:2.3.4 | P moves from active to stable mineral pool | $minP_{sta,ly}<4*minP_{act,ly}$ | roc=bk*(4*act-sta); if>0 P flows act→sta. Matches minP_sta<4*minP_act condition. |
| 3:2.3.5 | P moves from stable to active mineral pool | $minP_{sta,ly}>4*minP_{act,ly}$ | roc<0 when sta>4*act; back-transfer rate*0.1. Matches minP_sta>4*minP_act condition. |

## Lineage

Three resolved commits changed `nut_pminrl`. The original implementation in df07e3f used the basin phosphorus sorption parameter `bsn_prm%psp`, initialized local variables without explicit zero values, and set `bk` to 0.0006. Commit 39fabde added explicit zero initialization for `j`, `l`, `rto`, `rmp1`, and `roc`, and changed `bk` to 0.01. Commit 06d4609 switched the threshold ratio from the basin-wide `bsn_prm%psp` to the HRU-specific `hru(j)%nut%psp` and added `hru` to the module import list.

- df07e3f introduced the routine with layer-wise labile/active/stable phosphorus transfers, nutrient-balance accumulation, and a basin-wide sorption threshold based on `bsn_prm%psp`.
- 39fabde made the locals explicitly initialized to zero and changed the active-to-stable exchange coefficient `bk` from 0.0006 to 0.01, which affects the rate of movement between active and stable mineral P pools.
- 06d4609 changed the control basis for `rto` from basin-wide phosphorus sorption to the current HRU's `hru(j)%nut%psp`, making the labile/active threshold HRU-specific instead of basin-wide.

## Review Notes

- No direct file I/O was extracted for this procedure.
- warning: missing_doc: Procedure 'nut_pminrl' has no extracted documentation comment.
