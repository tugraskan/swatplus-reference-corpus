---
kind: procedure
symbol: mgt_tillfactor
title: mgt_tillfactor
status: filled
source_hash: 253f7adc2ebbf714
version_label: SWAT+ 62.0.0
args:
  jj: Selects the HRU whose soil profile and layer states are updated; the routine loops over
    `soil(jj)%nly` and reads and writes the matching `soil(jj)` layer entries.
  bio_mix_event: Chooses the biological-mixing branch when true and the tillage-mixing branch
    when false; it changes which coefficients are used and which layer factor is updated.
  emix: Carries the current mixing efficiency into the layer calculations and is reduced for
    partially mixed layers; the updated value is used to stop work once no further layers
    are affected.
  dtil: Sets the mixing depth threshold in millimeters, so the routine can decide whether
    a layer is fully mixed, partially mixed, or not mixed at all.
locals:
  l: Loop counter over soil layers in the selected HRU.
  m1: Fixed constant used in the empirical inverse tillage-factor equation; set to 1 before
    evaluating the logistic form.
  m2: Fixed constant used in the empirical inverse tillage-factor equation; set to 2 before
    evaluating the logistic form.
  xx: Temporary result holder for the inverted mixing calculation; it combines the intermediate
    terms before adding `emix` to form `csdr`.
  zz: Texture-based scaling term for the current layer, computed from clay content with either
    biological-mix or tillage-mix coefficients.
  yy: Normalized tillage factor used as the input to the inverse calculation; for tillage
    mixing it is based on the existing `tillagef_tillmix`, while for biological mixing it
    is forced to zero.
  xx1: First intermediate term in the empirical inverse solution for recovering `csdr` from
    `yy`.
  xx2: Second intermediate term in the empirical inverse solution for recovering `csdr` from
    `yy`, with an upper cap applied for safety.
  csdr: Recovered cumulative soil disturbance rating for the current layer, formed from the
    inverted factor plus the current mixing efficiency.
  consf: Moisture consolidation factor used to damp tillage mixing when `tillage_days(jj)
    > 0`, based on soil water status relative to field capacity.
  frac_mixed: Fraction of the current layer that is actually mixed when the tillage depth
    cuts through the layer; it is used to scale down the tillage-mixing factor for partial
    layers.
uses:
  soil_module: '`soil_module` holds the HRU soil profile and layer state that this routine
    reads and updates, including layer depths, thickness, temperature, water state, and the
    tillage-factor fields being produced.'
  basin_module: '`basin_module` is imported here but no resolved outside references from it
    were identified in the evidence packet, so its specific state contribution to this routine
    is uncertain from the available context.'
  hru_module: '`hru_module` provides the HRU-level tillage schedule and geometry inputs that
    tell this routine whether a tillage event is active and how deep it extends for the selected
    HRU.'
  tillage_data_module: '`tillage_data_module` supplies the coefficients and consolidation
    constant used in the empirical equations that convert clay content and soil moisture into
    layer mixing factors.'
  utils: '`utils` matters because `mgt_tillfactor` calls `exp_w` to evaluate exponentials
    safely when computing the inverse and forward tillage-factor equations.'
---

<!-- facts:header -->

Calculates daily tillage-mixing factors for each soil layer in an HRU. It separates biological mixing from tillage mixing, adjusts partial-layer mixing by depth, and stores the layer factors used later by residue and carbon routines.

## Bottom Line

`mgt_tillfactor` walks the soil layers for one HRU and updates the per-layer tillage response factors that control how strongly each layer is mixed on that day. It uses the requested mixing depth `dtil`, the current mixing efficiency `emix`, soil texture and temperature, and whether the event is biological mixing or tillage mixing to compute the layer-specific factors.

The routine matters because it turns a mixing event into the state carried forward by `soil(jj)%ly(l)%tillagef_biomix`, `soil(jj)%ly(l)%tillagef_tillmix`, and their sum `soil(jj)%ly(l)%tillagef`. Those values are then available to later soil-carbon and residue processes that need to know how much mixing occurred in each layer.

## Arguments

<!-- facts:arguments -->

## Where It Fits

This routine is called after a biological mixing or tillage-mixing event has been set up by `mgt_biomix` or `mgt_newtillmix_cswat1`, which provide `jj`, `bio_mix_event`, `emix`, and `dtil`. Its results feed the downstream soil-carbon/residue behavior that depends on per-layer mixing factors.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. Loop through HRU soil layers | The routine iterates from the top layer to `soil(jj)%nly` for the selected HRU, processing each layer in depth order. |
| 2. Adjust mixing for full, partial, or unmixed layers | For each layer, it compares the layer-bottom depth to `dtil`. Fully mixed layers keep `emix`, partially mixed layers scale `emix` by the fraction of the layer below the mixing depth, and deeper layers set `emix` to zero and stop contributing. |
| 3. Compute the texture scaling term | It calculates `zz` from clay content using biomix coefficients when `bio_mix_event` is true, or tillage-mix coefficients otherwise. For tillage mixing it also normalizes the existing `tillagef_tillmix` to obtain `yy`. |
| 4. Recover the disturbance rating from the current factor | If `yy` is large enough, the routine uses the empirical inverse equations with `exp_w` to estimate the cumulative disturbance rating `xx`, then combines it with `emix` to form `csdr`. |
| 5. Update biomix or tillmix factors | It sets biomix to zero when a biological event occurs in frozen soil, otherwise it computes either `tillagef_biomix` or `tillagef_tillmix` with the logistic response. For partial tillage layers, it scales `tillagef_tillmix` by the mixed fraction. |
| 6. Apply moisture consolidation to tillage mixing | When the HRU has active tillage days, the routine computes a moisture consolidation factor from soil storage relative to field capacity, reduces `tillagef_tillmix` accordingly, and zeros out very small values. |
| 7. Store the combined layer factor | The routine writes the final per-layer total as the sum of tillage-mix and biological-mix factors so later processes can use a single combined value. |

## Modules Used

<!-- facts:uses -->

| Module | State touched | Key components |
| --- | --- | --- |
| [sym:soil_module] | `soil` | `soil(jj)%nly, soil(jj)%phys(l)%d, soil(jj)%phys(l-1)%d, soil(jj)%phys(l)%thick, soil(jj)%ly(l)%tillagef_tillmix, soil(jj)%phys(l)%tmp, soil(jj)%ly(l)%tillagef_biomix, soil(jj)%phys(l)%st, soil(jj)%phys(l)%fc, soil(jj)%ly(l)%tillagef` |
| [sym:basin_module] | `tillage_days, tillage_depth, tillage_switch` | `tillage_days(jj), tillage_days, tillage_depth, tillage_switch` |
| [sym:hru_module] | `tillage_days, tillage_depth, tillage_switch` |  |
| [sym:tillage_data_module] | `bmix_a, bmix_b, bmix_c, tillmix_a, tillmix_b, tillmix_c, till_consf` |  |
| [sym:utils] | `exp_w` | `exp_w` |

## Local Variables

<!-- facts:locals -->

## State Changes

| Target | When | Meaning |
| --- | --- | --- |
| `soil(jj)%ly(l)%tillagef_biomix` | When `bio_mix_event` is true and `soil(jj)%phys(l)%tmp <= 0.`, the routine sets `soil(jj)%ly(l)%tillagef_biomix` to zero. | `tillagef_biomix` is cleared for frozen-soil biological-mixing conditions, preventing biomix from accumulating in layers that should not biologically mix on that day. |
| `soil(jj)%ly(l)%tillagef_tillmix` | When `bio_mix_event` is false and `soil(jj)%phys(l)%tmp > 0.`, the routine computes `soil(jj)%ly(l)%tillagef_tillmix` from the logistic response and, if the layer is only partially mixed, multiplies it by `frac_mixed`. | `tillagef_tillmix` is updated to reflect the current tillage event, then reduced for partial penetration so only the mixed fraction of the layer contributes. |
| `soil(jj)%ly(l)%tillagef` | After the biomix/tillmix update path completes for a layer with positive temperature, the routine sets `soil(jj)%ly(l)%tillagef = soil(jj)%ly(l)%tillagef_tillmix + soil(jj)%ly(l)%tillagef_biomix`. | `tillagef` becomes the combined per-layer mixing factor used as the layer's total disturbance response for subsequent model calculations. |

## File I/O

<!-- facts:io -->


## Lineage

Four resolved commits changed `mgt_tillfactor`. The newest commit (`bc7755a`) replaced hard-coded biomix and tillmix coefficient variables with values imported from `tillage_data_module`. Earlier commits added the HRU tillage-state imports and renamed the partial-layer accumulator to `frac_mixed` (`092aaf3`), split biomix and tillmix handling into separate layer fields and added the moisture consolidation adjustment (`1b2a997`), added a clamp on the second exponential term (`0a27862`), and fixed the order of `yy` and `zz` calculation in the tillmix branch (`aadf467`).

- bc7755a: substituted module-provided `bmix_a/bmix_b/bmix_c` and `tillmix_a/tillmix_b/tillmix_c` for the older local coefficient names in the two `zz` formulas.
- 092aaf3: imported `tillage_days`, `tillage_depth`, and `tillage_switch`; removed the local HRU index variable; renamed the partial-layer fraction variable to `frac_mixed`; and changed the layer loop to use `jj` directly.
- 1b2a997: changed the routine to keep biomix and tillmix in separate fields, zero biomix for biomix events at the point it had been accumulated previously, and sum the two fields into the total tillage factor.
- 0a27862: added a cap of `10.` to `xx2` after `exp_w(0.64 + 0.64 * yy ** 10.)` to avoid oversized inverse-calculation results.
- aadf467: moved the tillmix `yy` calculation to occur after the tillmix `zz` formula is computed.

## Review Notes

- No direct file I/O was extracted for this procedure.
- warning: missing_doc: Procedure 'mgt_tillfactor' has no extracted documentation comment.
- basin_module is imported in the source, but no resolved outside references from that module were identified in the evidence packet.
- outside_state[1] uses `hru_module` symbols; the previous placeholder module label was incorrect for those references.
- algorithm_steps revised: expanded the core algorithm to match the source-line sequence and added separate steps for the partial-depth adjustment, factor inversion, factor updates, moisture consolidation, and final sum.
