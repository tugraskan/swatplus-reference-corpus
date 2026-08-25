---
kind: procedure
symbol: pl_fert
title: pl_fert
status: filled
source_hash: 323825045fe4e8a8
version_label: SWAT+ 62.0.0
args:
  ifrt: '`ifrt` selects the fertilizer/manure database record whose mineral and organic fractions
    are applied to the HRU.'
  frt_kg: '`frt_kg` is the total application rate in kg/ha; the routine multiplies it by fertilizer
    fractions and layer fractions to compute all pool additions.'
  fertop: '`fertop` selects the chemical application operation record that provides `surf_frac`,
    the fraction placed in the surface layer versus the second layer.'
locals:
  rtof: Stores the manure/organic partitioning factor used to divide organic material between
    fresh residue pools and stable humus pools; it is taken from `man_coef%rtof`.
  j: HRU index copied from `ihru` so the routine can update `soil1(j)` for the active HRU.
  l: Loop index for the two soil layers that receive the fertilizer application.
  fr_ly: Layer fraction of the applied fertilizer mass; set from `chemapp_db(fertop)%surf_frac`
    for layer 1 and its complement for layer 2.
  c_n_rto: Computed carbon-to-nitrogen ratio used only for organic fertilizer handling to
    estimate the metabolic fraction.
  meta_fr: Fraction of organic fertilizer routed to the metabolic litter pool; computed from
    `c_n_rto` and clipped to the 0.01 to 0.7 range.
  pool_fr: Intermediate fraction for organic pool allocation within the current layer, reused
    for slow humus, metabolic, structural, and lignin additions.
  organic_flag: Marks whether the current fertilizer has organic N or P and therefore should
    be treated as organic material in SWAT-C mode.
uses:
  mgt_operations_module: '`chemapp_db(fertop)%surf_frac` determines how much of the application
    enters the surface layer versus the second layer, so `pl_fert` cannot place the fertilizer
    correctly without this operation metadata.'
  fertilizer_data_module: '`fertdb(ifrt)` supplies the fertilizer composition fractions that
    drive every pool update: mineral N, mineral P, organic N, organic P, and the NH3 share
    of mineral N.'
  basin_module: '`bsn_cc%cswat` switches the routine between the legacy mineral/organic pool
    logic and the SWAT-C organic litter/humus logic, so it controls which state updates occur.'
  organic_mineral_mass_module: '`org_frt` and `soil1` are the shared organic-mass containers
    that receive the fertilizer mass and all layer-resolved pool additions, making them the
    core state updated by this routine.'
  hru_module: '`ihru` identifies which HRU in `soil1` is being updated, and the `fert*` variables
    store the daily fertilizer summary values used by downstream management output and HRU
    bookkeeping.'
---

<!-- facts:header -->

Applies a fertilizer or manure application to the current HRU, splitting the material between soil layers and nutrient pools based on operation settings and carbon-code mode.

## Bottom Line

`pl_fert` updates the current HRU's mineral N and P pools, total organic pools, and—when SWAT-C organic handling is active—fresh residue, slow humus, metabolic litter, structural litter, and lignin pools. It uses the fertilizer database fractions and the chemical-application surface fraction to split the applied mass between the top two soil layers.

The routine also refreshes the daily fertilizer summary variables (`fertno3`, `fertnh3`, `fertorgn`, `fertsolp`, `fertorgp`, `fertn`, `fertp`) that later management output and HRU bookkeeping depend on.

## Arguments

<!-- facts:arguments -->

## Where It Fits

This routine runs during management execution when a fertilizer or manure operation is being applied to the current HRU. Callers such as `actions`, `hru_control`, `mallo_control`, and `mgt_sched` prepare the fertilizer database index, application amount, and operation type before calling it. Its results feed later HRU accounting and management output through the `fert*` summary variables and the updated soil-organic pools.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. Initialize state and select current HRU. | Reset the organic fertilizer accumulator, zero the summary working variables, copy `ihru` into `j`, and load the manure partition factor from `man_coef%rtof`. |
| 2. Detect organic fertilizer in SWAT-C mode. | If the basin is using carbon code 2 and the selected fertilizer has organic N or P, mark the application as organic so later SWAT-C pool updates will run. |
| 3. Build organic fertilizer composition. | When the organic flag is set, populate `org_frt` with total mass, carbon, nitrogen, and phosphorus contents from the fertilizer database and compute the carbon-to-nitrogen ratio and metabolic fraction. |
| 4. Bound the metabolic fraction. | Clamp `meta_fr` to the 0.01 to 0.7 range so the organic split stays within model limits. |
| 5. Split the application across two layers. | Loop over the first two soil layers and assign each layer the surface fraction or its complement based on `chemapp_db(fertop)%surf_frac`. |
| 6. Add mineral N and P to each layer. | Increase layer nitrate, ammonium, and labile phosphorus by the layer fraction times the applied rate and fertilizer mineral fractions. |
| 7. Add total organic N and P to each layer. | Increase each layer's total organic N and P pools by the manure fraction, layer fraction, applied rate, and fertilizer organic fractions. |
| 8. Route organic fertilizer to legacy humus pools in carbon-off mode. | If carbon code 0 is active, send the fresh organic share to plant residue and the remainder to active humus, using the same layer fraction and `rtof` split. |
| 9. Route organic fertilizer to SWAT-C pools. | If carbon code 2 is active and the fertilizer is organic, add the stable share to total organic and slow humus, then partition the fresh share into metabolic, structural, and lignin pools. |
| 10. Continue through both layers. | Finish the two-layer loop after updating all applicable soil pools. |
| 11. Summarize fertilizer mass by nutrient form. | Compute daily totals for nitrate, ammonium, organic N, soluble P, organic P, and cumulative fertilizer N and P for later output and bookkeeping. |
| 12. Return to caller. | Exit after all soil pools and summary variables have been updated. |

## Modules Used

<!-- facts:uses -->

| Module | State touched | Key components |
| --- | --- | --- |
| [sym:mgt_operations_module] | `chemapp_db` | `chemapp_db(fertop)%surf_frac` |
| [sym:fertilizer_data_module] | `fertdb` | `fertdb(ifrt)%forgn, fertdb(ifrt)%forgp, fertdb(ifrt)%fminn, fertdb(ifrt)%fnh3n, fertdb(ifrt)%fminp` |
| [sym:basin_module] | `bsn_cc` | `bsn_cc%cswat` |
| [sym:organic_mineral_mass_module] | `org_frt, soil1` | `org_frt%m, org_frt%c, org_frt%n, org_frt%p, soil1(j)%mn(l)%no3, soil1(j)%mn(l)%nh4, soil1(j)%mp(l)%lab, soil1(j)%tot(l)%n, soil1(j)%tot(l)%p, soil1(j)%pl(1)%rsd(l)%n, soil1(j)%pl(1)%rsd(l)%p, soil1(j)%hact(l)%n, soil1(j)%hact(l)%p, soil1(j)%hsta(l)%p, soil1(j)%tot(l), soil1(j)%hs(l), soil1(j)%meta(l), soil1(j)%str(l), soil1(j)%lig(l)` |
| [sym:hru_module] | `ihru, fertn, fertp, fertnh3, fertno3, fertorgn, fertorgp, fertsolp` |  |

## Local Variables

<!-- facts:locals -->

## State Changes

| Target | When | Meaning |
| --- | --- | --- |
| `org_frt%m` | When `bsn_cc%cswat == 2` and the selected fertilizer contains organic N or P. | Stores the applied fertilizer mass in the organic-mass container so SWAT-C can distribute that material into soil organic pools. |
| `org_frt%c` | When `bsn_cc%cswat == 2` and the selected fertilizer contains organic N or P. | Sets the carbon content of `org_frt` from fertilizer organic-N fraction with a 10:1 C:N assumption so later organic pool allocations have a carbon mass to distribute. |
| `org_frt%n` | When `bsn_cc%cswat == 2` and the selected fertilizer contains organic N or P. | Stores the fertilizer's organic nitrogen mass in `org_frt` so the SWAT-C routine can distribute it across total organic, residue, and humus pools. |
| `org_frt%p` | When `bsn_cc%cswat == 2` and the selected fertilizer contains organic N or P. | Stores the fertilizer's organic phosphorus mass in `org_frt` so the SWAT-C routine can distribute it across total organic and residue pools. |
| `soil1(j)%mn(l)%no3` | For every call, in each of the first two soil layers. | Adds the mineral nitrate portion of the fertilizer to the layer's nitrate pool based on the surface-fraction split and the fertilizer's mineral-N and NH3 fractions. |
| `soil1(j)%mn(l)%nh4` | For every call, in each of the first two soil layers. | Adds the ammonium portion of the fertilizer's mineral nitrogen to the layer's ammonium pool using the same layer split. |
| `soil1(j)%mp(l)%lab` | For every call, in each of the first two soil layers. | Adds the soluble mineral phosphorus fraction to the layer's labile phosphorus pool. |
| `soil1(j)%tot(l)%n` | For every call, in each of the first two soil layers. | Increases the layer's total organic nitrogen pool by the organic-N amount that is routed to soil organic matter. |
| `soil1(j)%tot(l)%p` | For every call, in each of the first two soil layers. | Increases the layer's total organic phosphorus pool by the organic-P amount that is routed to soil organic matter. |
| `soil1(j)%pl(1)%rsd(l)%n` | When `bsn_cc%cswat == 0`, in each of the first two soil layers. | Adds the fresh organic-N share of the fertilizer to the plant residue pool used by the older mineralization formulation. |
| `soil1(j)%pl(1)%rsd(l)%p` | When `bsn_cc%cswat == 0`, in each of the first two soil layers. | Adds the fresh organic-P share of the fertilizer to the plant residue pool used by the older mineralization formulation. |
| `soil1(j)%hact(l)%n` | When `bsn_cc%cswat == 0`, in each of the first two soil layers. | Adds the stable organic-N share of the fertilizer to active humus in the old carbon formulation. |
| `soil1(j)%hact(l)%p` | When `bsn_cc%cswat == 0`, in each of the first two soil layers. | Adds the stable organic-P share of the fertilizer to the layer humus pool; the source line uses `hsta(l)%p` on the right-hand side, so the update is based on the stable P pool reference in the routine. |
| `soil1(j)%tot(l)` | When `bsn_cc%cswat == 2` and the fertilizer is organic. | Adds the stable organic share of the applied fertilizer to the layer's total organic mass container so the full organic load is preserved in SWAT-C accounting. |
| `soil1(j)%hs(l)` | When `bsn_cc%cswat == 2` and the fertilizer is organic. | Adds the stable organic share to slow humus, carrying the fertilizer's organic mass into the slowly cycling soil organic pool. |
| `soil1(j)%meta(l)` | When `bsn_cc%cswat == 2` and the fertilizer is organic. | Adds the metabolic share of the fertilizer to the metabolic litter pool after the `meta_fr` split is computed. |
| `soil1(j)%str(l)` | When `bsn_cc%cswat == 2` and the fertilizer is organic. | Adds the structural share of the fertilizer to the structural litter pool after the `meta_fr` split is computed. |
| `soil1(j)%lig(l)` | When `bsn_cc%cswat == 2` and the fertilizer is organic. | Adds lignin proportional to the structural pool, using 0.175 of the structural addition as the lignin increment. |
| `fertno3` | After the layer loop completes, for every call. | Stores the daily nitrate fertilizer total for HRU-level management output and bookkeeping. |
| `fertnh3` | After the layer loop completes, for every call. | Stores the daily ammonium fertilizer total for HRU-level management output and bookkeeping. |
| `fertorgn` | After the layer loop completes, for every call. | Stores the daily organic nitrogen fertilizer total for HRU-level management output and bookkeeping. |
| `fertsolp` | After the layer loop completes, for every call. | Stores the daily soluble phosphorus fertilizer total for HRU-level management output and bookkeeping. |
| `fertorgp` | After the layer loop completes, for every call. | Stores the daily organic phosphorus fertilizer total for HRU-level management output and bookkeeping. |
| `fertn` | After the layer loop completes, for every call. | Accumulates total fertilizer nitrogen applied in the HRU state so later management output and nutrient accounting can use it. |

## File I/O

<!-- facts:io -->


## Theory Equations

| Eq. | Title | Formula | Implementation |
| --- | --- | --- | --- |
| 6:1.7.1 | NO3 added from mineral N fraction | $NO3_{fert}=fert_{minN}*(1-fert_{NH4})*fert$ | Verified against SWAT+ 62.0.0 (pl_fert.f90:81). no3 += fr_ly*frt_kg*(1.-fnh3n)*fminn` — exact |
| 6:1.7.2 | NH4 added from mineral N fraction | $NH4_{fert}=fert_{minN}*fert_{NH4}*fert$ | Verified against SWAT+ 62.0.0 (pl_fert.f90:83). nh4 += fr_ly*frt_kg*fnh3n*fminn` — exact |
| 6:1.7.3 | Fresh organic N from fertilizer | $orgN_{frsh,fert}=0.5*fert_{orgN}*fert$ | Verified against SWAT+ 62.0.0 (pl_fert.f90:61). theory's 0.5 fresh/stable split replaced by C:N-dependent metabolic partition `meta_fr=.85-.018*c_n_rto` (cf. 6:1.7.6) |
| 6:1.7.4 | Active humus N from fertilizer | $orgN_{act,fert}=0.5*fert_{orgN}*fert$ | Verified against SWAT+ 62.0.0 (pl_fert.f90:61). 0.5 active-orgN split → C:N metabolic partition (cf. 6:1.7.3/6/7) |
| 6:1.7.5 | Solution P added from mineral P | $P_{solution,fert}=fert_{minP}*fert$ | Verified against SWAT+ 62.0.0 (pl_fert.f90:85). lab += fr_ly*frt_kg*fminp` — exact |
| 6:1.7.6 | Fresh organic P from fertilizer | $orgP_{frsh,fert}=0.5*fert_{orgP}*fert$ | Verified against SWAT+ 62.0.0 (pl_fert.f90). (0.5 org-P fert split) |
| 6:1.7.7 | Humified organic P from fertilizer | $orgP_{hum,fert}=0.5*fert_{orgP}*fert$ | Verified against SWAT+ 62.0.0 (pl_fert.f90:61). 0.5 humic-orgP split → same C:N partition |
| 6:1.7.8 | Ground cover gc for bacteria foliage application | $gc=\frac{1.99532-erfc[1.333*LAI-2]}{2.1}$ | gc = (1.99532-erfc[1.333*LAI-2])/2.1 not found in pl_fert.f90. No erfc calculation or bacteria-to-foliage partitioning exists in that routine. Bacteria from fertilizer may be in a dedicated subroutine not in the candidate list. |
| 6:1.7.9 | Less-persistent bacteria on foliage | $bact_{lp,fol}=\frac{gc*fr_{active}*fert_{lpbact}*fert}{10}$ | bact_lp_fol = gc*fr_active*fert_lpbact*fert/10 not found in pl_fert.f90 or any searched routine. |
| 6:1.7.10 | Persistent bacteria on foliage | $bact_{p,fol}=\frac{gc*fr_{active}*fert_{pbact}*fert}{10}$ | bact_p_fol = gc*fr_active*fert_pbact*fert/10 not found in pl_fert.f90 or any searched routine. |
| 6:1.7.11 | Less-persistent bacteria in solution | $bact_{lpsol,fert}=\frac{(1-gc)*fr_{active}*fert_{lpbact}*k_{bact}*fert}{10}$ | bact_lpsol_fert not found in pl_fert.f90 or any searched routine. |
| 6:1.7.12 | Less-persistent bacteria sorbed to soil | $bact_{lpsorb,fert}=\frac{(1-gc)*fr_{active}*fert_{lpbact}*(1-k_{bact})*fert}{10}$ | bact_lpsorb_fert not found in pl_fert.f90 or any searched routine. |
| 6:1.7.13 | Persistent bacteria in solution | $bact_{psol,fert}=\frac{(1-gc)*fr_{active}*fert_{pbact}*k_{bact}*fert}{10}$ | bact_psol_fert not found in pl_fert.f90 or any searched routine. |
| 6:1.7.14 | Persistent bacteria sorbed to soil | $bact_{psorb,fert}=\frac{(1-gc)*fr_{active}*fert_{pbact}*(1-k_{bact})*fert}{10}$ | bact_psorb_fert not found in pl_fert.f90 or any searched routine. |

## Lineage

Resolved lineage evidence shows three behavior-changing edits to `pl_fert`: one removed the old `man_coef%man_to_c` carbon assignment and replaced it with a fixed 10:1 carbon-to-nitrogen estimate for organic fertilizer; one corrected lignin handling by replacing a single assignment to `soil1(j)%lig(l)` with component-wise updates to `%m`, `%c`, `%n`, and `%p`; and one changed that lignin formula from a direct 0.175*organic-mass update to a fraction of the structural pool to avoid over-allocation.

- Replaced the organic-carbon source with a fixed 10:1 estimate and removed the unused `man_coef%man_to_c` assignment.
- Changed lignin updates from whole-object assignment to component-wise `%m`, `%c`, `%n`, and `%p` updates.
- Adjusted lignin allocation to derive from the structural pool instead of directly from the applied manure mass.

## Review Notes

- No direct file I/O was extracted for this procedure.
- warning: missing_doc: Procedure 'pl_fert' has no extracted documentation comment.
- algorithm_steps revised: condensed the routine into 12 higher-level steps aligned to the visible source blocks.
- Source line 102 assigns `soil1(j)%hact(l)%p = soil1(j)%hsta(l)%p + ...`; this looks inconsistent with the neighboring N update, but the overlay preserves the source as written.
