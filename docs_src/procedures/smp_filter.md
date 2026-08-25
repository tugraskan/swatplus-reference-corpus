---
kind: procedure
symbol: smp_filter
title: smp_filter
status: filled
source_hash: df8daf76998ddad4
version_label: SWAT+ 62.0.0
locals:
  i: Integer work flag used only for the `if (i == 100)` check that resets `remove2` before
    processing; otherwise it is not part of the filter-strip calculations shown here.
  j: Loop/index variable for the current HRU. It is set from `ihru` and then used to reference
    the active HRU and its associated load arrays.
  k: Loop counter over simulated pesticides in `do k = 1, cs_db%num_pests`. It selects each
    pesticide balance record to be reduced.
  drain_vfs1: Drainage area contributing to filter-strip section 1, computed from the HRU
    area and the non-concentrated runoff fraction.
  drain_vfs2: Drainage area contributing to filter-strip section 2, computed from the concentrated-flow
    fraction and the HRU area.
  drain_vfs3: Drainage area for the fully channelized core portion of the filter strip, computed
    from `vfscon * vfsch * area_ha`. It is calculated but not used later in this routine.
  area_vfs1: Area assigned to filter-strip section 1, based on the HRU area and the 90% portion
    of the VFS ratio.
  area_vfs2: Area assigned to filter-strip section 2, based on the HRU area and the 10% portion
    of the VFS ratio.
  vfs_depth1: Runoff depth delivered to filter-strip section 1, computed from its drainage-area
    ratio times `surfq(j)`. It is the runoff-depth predictor used in the runoff-removal equation.
  vfs_depth2: Runoff depth delivered to filter-strip section 2, computed from its drainage-area
    ratio times `surfq(j)`. It is the runoff-depth predictor used in the second runoff-removal
    equation.
  vfs_sed1: Sediment loading on filter-strip section 1 in kg/m^2, derived from HRU sediment
    yield scaled by the section's drainage area and area.
  vfs_sed2: Sediment loading on filter-strip section 2 in kg/m^2, derived from HRU sediment
    yield scaled by the section's drainage area and area.
  surq_remove1: Runoff-removal percentage for filter-strip section 1, computed from `vfs_depth1`
    and soil Ksat and then clipped to 0-100%.
  surq_remove2: Runoff-removal percentage for filter-strip section 2, computed from `vfs_depth2`
    and soil Ksat and then clipped to 0-100%.
  surq_remove: Area-weighted average runoff-removal percentage across the two active filter-strip
    sections. It is later reused for pesticide runoff reduction.
  sed_remove1: Sediment-removal percentage for filter-strip section 1, computed from sediment
    loading and runoff removal and clipped to 0-100%.
  sed_remove2: Sediment-removal percentage for filter-strip section 2, computed from sediment
    loading and runoff removal and clipped to 0-100%.
  sed_remove: Area-weighted average sediment-removal percentage across the two filter-strip
    sections. It is later reused for pesticide sediment reduction.
  remove1: Reusable temporary percentage for section 1 in the organic-N, nitrate, particulate-P,
    and soluble-P removal equations.
  remove2: Reusable temporary percentage for section 2 in the organic-N, nitrate, and particulate-P
    calculations. In the soluble-P block the code assigns `remove21` instead of updating `remove2`,
    so the section-2 soluble-P fraction is not propagated through `remove2` there.
  sedtrap: Amount of sediment actually trapped by the filter strip after the routine updates
    `sedyld(j)`. It is then peeled off the sediment-associated constituent pools in order.
  xrem: Residual trapped sediment that remains after subtracting from one sediment class and
    must be carried forward to the next class in the priority chain.
  vfs_ratio1: Drainage-area-to-filter-area ratio for section 1. It scales runoff depth and
    sediment loading and is also the basis for the implemented VFS ratio equation.
  vfs_ratio2: Drainage-area-to-filter-area ratio for section 2. It scales runoff depth and
    sediment loading and is also the basis for the implemented VFS ratio equation.
  orgn_remove: Area-weighted average organic nitrogen removal percentage across the filter
    strip. It is applied to `sedorgn(j)`.
  surqno3_remove: Area-weighted average nitrate removal percentage across the filter strip.
    It is applied to `surqno3(j)`.
  partp_remove: Area-weighted average particulate phosphorus removal percentage across the
    filter strip. It is applied to `sedminpa(j)`, `sedminps(j)`, and `sedorgp(j)`.
  solp_remove: Area-weighted average soluble phosphorus removal percentage across the filter
    strip. It is applied to `surqsolp(j)`.
  remove21: Temporary section-2 soluble phosphorus removal percentage. It is assigned from
    `29.3 + 0.51 * surq_remove2`, but the subsequent clipping logic checks `remove2`, so this
    variable appears to be a separate local scratch value rather than the one used for clipping.
uses:
  basin_module: '`basin_module` matters because the procedure is written to operate within
    the basin-scale model state, even though this extraction did not resolve a specific basin
    variable that is read or written in the shown lines.'
  hru_module: '`hru_module` matters because the routine gets the active HRU index from `ihru`
    and reads/writes the HRU fields that define runoff geometry and the pollutant loads being
    reduced: `hru(j)%lumv%vfscon`, `hru(j)%area_ha`, `hru(j)%lumv%vfsch`, `hru(j)%lumv%vfsratio`,
    plus the shared arrays for runoff, sediment, and nutrient state.'
  soil_module: '`soil_module` matters because the runoff-removal equation uses the first soil
    layer''s saturated hydraulic conductivity (`k`) as a predictor of vegetative filter strip
    performance.'
  constituent_mass_module: '`constituent_mass_module` matters because `cs_db%num_pests` sets
    how many pesticide records the routine loops over when it applies runoff and sediment
    reductions to `hpestb_d(j)%pest(k)`.'
  time_module: '`time_module` matters because this routine is part of the daily HRU processing
    chain and depends on the model''s current-step shared state, even though no specific time
    variable was extracted in the provided lines.'
  output_ls_pesticide_module: '`output_ls_pesticide_module` matters because it holds `hpestb_d`,
    the pesticide-balance arrays whose `surq` and `sed` fields are scaled by the filter-strip
    runoff and sediment removals for every pesticide in the HRU.'
---

<!-- facts:header -->

Applies vegetative filter strip reductions to runoff, sediment, nutrients, and pesticide loads for the current HRU. It uses HRU, soil, and constituent state to estimate how much material the strip removes and then updates the shared daily load arrays.

## Bottom Line

`smp_filter` is the edge-of-field filter-strip routine. When an HRU has a vegetative filter strip and there is surface runoff, it partitions the HRU into two filter-strip sections, computes runoff depth and sediment loading for each section, estimates percentage removal for runoff and sediment, and then applies those removal percentages to sediment, organic nitrogen, nitrate, particulate phosphorus, soluble phosphorus, and pesticide runoff/sediment loads.

The routine matters because it directly reduces the outgoing constituent loads that later SWAT+ reporting and downstream routing use. It does not read or write files itself; instead it mutates shared HRU and pesticide-balance state in place for the current HRU selected by `ihru`.

## Arguments

<!-- facts:arguments -->

## Where It Fits

`smp_filter` runs during HRU management processing after `stor_surfstor` and `swr_substor`, and only when the active HRU has `vfsi > 0`. Its caller `hru_control` sets `ihru`/`j` context and then invokes this routine before any optional buffer-strip routine (`smp_buffer`) and before grass waterway reduction. The updated sediment, nutrient, and pesticide loads then feed the rest of the day's HRU output and routing calculations.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. Select the active HRU and clear a stale section-2 flag when needed. | The routine copies `ihru` into `j` and, if `i` equals 100, resets `remove2` to zero before any filter-strip calculations run. |
| 2. Skip the routine unless there is meaningful surface runoff. | All downstream filtering logic runs only when `surfq(j)` exceeds `.0001`; otherwise the routine returns without changing the pollutant state. |
| 3. Partition the HRU runoff source area into three VFS drainage sections and derive section areas. | The routine computes `drain_vfs1`, `drain_vfs2`, and `drain_vfs3` from the HRU's VFS fractions, then computes `area_vfs1` and `area_vfs2` from the HRU area and `vfsratio`. |
| 4. Convert drainage area to section-specific ratios and runoff depths. | It forms `vfs_ratio1` and `vfs_ratio2`, then multiplies each by the HRU runoff depth to get `vfs_depth1` and `vfs_depth2`. |
| 5. Compute sediment loading on each filter-strip section. | The routine scales HRU sediment yield by drainage area and filter area to obtain `vfs_sed1` and `vfs_sed2` in kg/m^2. |
| 6. Estimate runoff removal for each section from runoff depth and soil conductivity. | Using empirical equations, it computes `surq_remove1` and `surq_remove2` from `vfs_depth1`, `vfs_depth2`, and `soil(j)%phys(1)%k`, then clips each percentage to the 0-100 range. |
| 7. Average runoff removal across the filter strip. | The section percentages are combined with their drainage areas to form `surq_remove`, the area-weighted runoff-reduction percentage for the whole VFS. |
| 8. Estimate sediment removal and compute the trap mass. | The routine computes `sed_remove1` and `sed_remove2` from sediment loading and runoff removal, clips them, averages them into `sed_remove`, applies that reduction to `sedyld(j)`, and computes the trapped sediment mass in `sedtrap`. |
| 9. Remove trapped sediment from sediment-class pools in priority order. | `sedtrap` is subtracted first from `lagyld(j)`, then any leftover mass is carried through `sanyld(j)`, `sagyld(j)`, `silyld(j)`, and `clayld(j)`, with each pool clipped to zero via `Max`. |
| 10. Compute organic nitrogen removal and update `sedorgn(j)`. | Section-specific organic-N removal is computed from sediment removal, averaged into `orgn_remove`, and then applied to the organic nitrogen load array. |
| 11. Compute nitrate removal and update `surqno3(j)`. | The routine computes section-specific nitrate-removal percentages from runoff removal, averages them into `surqno3_remove`, and scales the surface-runoff nitrate load accordingly. |
| 12. Compute particulate phosphorus removal and update the sediment-bound P pools. | It derives particulate-P removal from sediment removal, averages it into `partP_remove`, and applies the same reduction to `sedminpa(j)`, `sedminps(j)`, and `sedorgp(j)`. |
| 13. Compute soluble phosphorus removal and update `surqsolp(j)`. | The routine calculates soluble-P removal from runoff removal, averages it into `solp_remove`, and scales the soluble phosphorus load in surface runoff. |
| 14. Loop over all simulated pesticides and apply runoff and sediment reductions. | For each pesticide index `k` from 1 to `cs_db%num_pests`, the routine reduces `hpestb_d(j)%pest(k)%surq` by `surq_remove` and `hpestb_d(j)%pest(k)%sed` by `sed_remove`. |

## Modules Used

<!-- facts:uses -->

| Module | State touched | Key components |
| --- | --- | --- |
| [sym:basin_module] | `basin_module state imported into the subroutine scope, but no specific basin components were resolved from the source packet.` | `None resolved in the packet.` |
| [sym:hru_module] | `hru, sedyld, surfq, lagyld, sanyld, sagyld, silyld, clayld, sedorgn, surqno3, sedminpa, sedminps, sedorgp, surqsolp, ihru` | `hru(j)%lumv%vfscon, hru(j)%area_ha, hru(j)%lumv%vfsch, hru(j)%lumv%vfsratio` |
| [sym:soil_module] | `soil state imported into the subroutine scope, with the active soil profile referenced through `soil(j)%phys(1)%k`.` | ``soil(j)%phys(1)%k`` |
| [sym:constituent_mass_module] | `cs_db` | `cs_db%num_pests` |
| [sym:time_module] | `time state imported into the subroutine scope, but no specific time component was resolved from the packet.` | `None resolved in the packet.` |
| [sym:output_ls_pesticide_module] | `hpestb_d` | `hpestb_d(j)%pest(k)%surq, hpestb_d(j)%pest(k)%sed` |

## Local Variables

<!-- facts:locals -->

## State Changes

| Target | When | Meaning |
| --- | --- | --- |
| `sedyld(j)` | When `surfq(j) > .0001` and after `sed_remove` is computed from the VFS equations. | `sedyld(j)` is reduced by the whole-strip sediment-removal percentage and then clipped to be nonnegative. This represents the remaining sediment leaving the HRU after the filter strip traps part of the load. |
| `lagyld(j)` | When trapped sediment remains after subtracting from `lagyld(j)` first. | `lagyld(j)` loses sediment-trapped mass before the routine moves on to other sediment classes. It is the first pool depleted in the sediment-priority chain. |
| `sanyld(j)` | When leftover trapped sediment remains after `lagyld(j)` is exhausted. | `sanyld(j)` is reduced by the remaining trapped mass. If that pool is not large enough, the residual is carried forward to the next sediment class. |
| `sagyld(j)` | When leftover trapped sediment remains after `sanyld(j)` is exhausted. | `sagyld(j)` is reduced by the remaining trapped mass, continuing the ordered depletion of sediment classes. |
| `silyld(j)` | When leftover trapped sediment remains after `sagyld(j)` is exhausted. | `silyld(j)` is reduced by the remaining trapped mass, so the trapped sediment is progressively assigned across finer sediment pools. |
| `clayld(j)` | When leftover trapped sediment remains after `silyld(j)` is exhausted. | `clayld(j)` is reduced by the final leftover trapped mass, and any negative result is prevented by clipping later with `Max`. |
| `sedorgn(j)` | When `surfq(j) > .0001` and `orgn_remove` is computed from the section removal equations. | `sedorgn(j)` is multiplied by the remaining fraction after organic-N removal, representing the portion of sediment-bound organic nitrogen that passes through the filter strip. |
| `surqno3(j)` | When `surfq(j) > .0001` and `surqno3_remove` is computed from the runoff-removal equations. | `surqno3(j)` is multiplied by the remaining fraction after nitrate removal, representing the nitrate still in surface runoff after the filter strip. |
| `sedminpa(j)` | When `surfq(j) > .0001` and `partP_remove` is computed from sediment removal. | `sedminpa(j)` is reduced by the particulate-P removal fraction because active mineral phosphorus is transported on sediment. |
| `sedminps(j)` | When `surfq(j) > .0001` and `partP_remove` is computed from sediment removal. | `sedminps(j)` is reduced by the particulate-P removal fraction because stable mineral phosphorus is transported on sediment. |
| `sedorgp(j)` | When `surfq(j) > .0001` and `partP_remove` is computed from sediment removal. | `sedorgp(j)` is reduced by the particulate-P removal fraction because organic phosphorus is sediment-associated in this routine. |
| `surqsolp(j)` | When `surfq(j) > .0001` and `solp_remove` is computed from runoff removal. | `surqsolp(j)` is reduced by the soluble-P removal fraction, representing dissolved phosphorus retained by the filter strip. |
| `hpestb_d(j)%pest(k)%surq` | When the routine loops over `k = 1, cs_db%num_pests`. | `hpestb_d(j)%pest(k)%surq` is reduced by the area-weighted runoff-removal percentage for each pesticide balance record. |
| `hpestb_d(j)%pest(k)%sed` | When the routine loops over `k = 1, cs_db%num_pests`. | `hpestb_d(j)%pest(k)%sed` is reduced by the area-weighted sediment-removal percentage for each pesticide balance record. |

## File I/O

<!-- facts:io -->


## Theory Equations

| Eq. | Title | Formula | Implementation |
| --- | --- | --- | --- |
| 6:5.1.1 | VFS runoff removal R_R | $R_R=75.8-10.8(ln(R_L)+25.9 ln(K_{SAT})$ | surq_remove1=75.8-10.8*Log(vfs_depth1)+25.9*Log(soil%phys(1)%k); vfs_depth=R_L (runoff depth mm), soil%phys(1)%k=K_SAT. Exact match. |
| 6:5.1.2 | VFS sediment removal S_R | $S_R(\%)=79.0-1.04 S_L+0.213R_R$ | sed_remove1=79.0-1.04*vfs_sed1+0.213*surq_remove1; vfs_sed=S_L (kg/mÂ²). Exact match. |
| 6:5.1.3 | Total N removal TN_R | $TN_R=0.036 S_R^{1.69}$ | remove1=0.036*sed_remove1**1.69. Exact match. |
| 6:5.1.4 | Nitrate N removal NN_R | $NN_R=39.4+0.584R_R$ | remove1=39.4+0.584*surq_remove1. Exact match. |
| 6:5.1.5 | Total P removal TP_R | $TP_R=0.90 S_R$ | FLAG: code coefficient is 0.903 (remove1=0.903*sed_remove1) vs theory's 0.90; minor discrepancy (~0.3%). |
| 6:5.1.6 | Soluble P removal DP_R | $DP_R=29.3+0.51R_R$ | remove1=29.3+0.51*surq_remove1. Exact match. |
| 6:5.1.7 | VFS drainage-area ratio section 1 | $DAFS_{ratio1}=DAFS_{ratio}(1-DF_{con})/0.9$ | Verified against SWAT+ 62.0.0 (smp_filter.f90:92). (VFS area *0.9) |
| 6:5.1.8 | VFS drainage-area ratio section 2 | $DAFS_{ratio2}=DAFS_{ratio}(1-CF_{frac})DF_{con}/0.1$ | Verified against SWAT+ 62.0.0 (smp_filter.f90:93). (VFS area *0.1) |

## Lineage

Resolved lineage evidence shows the routine was introduced in commit `df07e3f` and later adjusted in several small fixes. The source remained centered on the same VFS-filter calculation path, but later commits corrected variable initialization/formatting, fixed the section-2 sediment equation to use `surq_remove2`, and made a few comment/typo cleanups.

- `df07e3f` added the full `smp_filter` subroutine, including the filter-strip runoff, sediment, nutrient, and pesticide reduction logic.
- `39fabde` initialized the local scalars and cleaned up declarations/comments, changing the routine from uninitialized scratch variables to explicitly zeroed working state.
- `f1e61a3` normalized indentation and preserved the same calculation flow; the diff shows formatting-only edits with no behavioral change.
- `889136d` only corrected comment text from "constituants" to "constituents"; no code logic changed.
- `3ba1db9` changed `sed_remove2` to use `surq_remove2` instead of `surq_remove1`, fixing the section-2 sediment-removal calculation; the diff also only preserved the file ending newline.

## Review Notes

- No direct file I/O was extracted for this procedure.
- warning: missing_doc: Procedure 'smp_filter' has no extracted documentation comment.
- algorithm_steps revised: expanded the draft into 14 source-backed steps to reflect the actual calculation sequence and to cite only visible line numbers from `smp_filter.f90`.
- Source uncertainty: `i` is not assigned within the shown subroutine body except in the reset check; its upstream meaning is inferred only from that use.
- Source uncertainty: `remove21` is written in the soluble-P block while the clipping guard tests `remove2`; this looks like a likely typo, but the documentation reflects the source as shown.
