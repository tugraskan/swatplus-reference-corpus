---
kind: procedure
symbol: mgt_biomix
title: mgt_biomix
status: filled
source_hash: 0e0720f7379f9e65
version_label: SWAT+ 62.0.0
args:
  jj: '`jj` selects which HRU profile, plant community, residue pools, and soil layers are
    mixed; every array update in the routine is indexed by this HRU.'
  biomix_eff: '`biomix_eff` is the starting biological mixing efficiency. If it is effectively
    zero, the routine skips the mixing calculations; otherwise it becomes the base efficiency
    that is adjusted by temperature and depth before being applied to the soil layers.'
locals:
  fcgd: Holds the temperature-response function value returned by `fcgd(stemp)` and used to
    scale mixing efficiency when `org_con%tmpf` selects that response.
  bmix: Temporary per-layer biological mixing efficiency after consolidation and tillage-state
    rules are applied; it is the layer-specific mixing rate used in the temperature and depth
    weighting.
  l: Loop counter over soil layers, used to scan layers, detect the mixed depth limit, and
    later reconstitute the affected layers.
  kk: Tracks the bottom layer index used to initialize the effective mixing depth from the
    deepest soil layer.
  npmx: Stores `cs_db%num_pests`; the routine captures pesticide count but the pesticide mixing
    block is commented out here.
  lyr_exit: Marks the layer where the mixed-depth loop stops because the current layer lies
    below the biological mixing zone or no further mixing applies.
  avg_emix: Weighted average mixing efficiency across the mixed depth, used to compute how
    much of each layer is mixed and how much residue is transferred.
  emix: Per-layer effective mixing efficiency after temperature adjustment; accumulated into
    `emix_sum` and applied to soil and residue redistribution.
  emix_sum: Accumulator of layer-weighted effective mixing efficiency used to derive `avg_emix`
    for the mixing zone.
  dtil: Effective biological mixing depth in millimeters after applying the minimum of the
    soil depth and `bmix_depth`, and after any frozen-soil/depth adjustments.
  frac_mixed: Fraction of a layer's mass that is treated as mixed; used to weight transfers
    from the layer into the mixed pool and back into the layer.
  frac_non_mixed: Fraction of a layer that remains unchanged during reconstitution after mixing.
  sol_mass: Layer soil mass used to convert mixed fractions into mass-based contributions
    for each layer.
  sol_msm: Mass of each layer that is mixed within the biological mixing depth.
  sol_msn: Mass of each layer that is not mixed and therefore retained in place during reconstitution.
  frac_dep: Fraction of each layer depth that lies inside the biological mixing zone; used
    to scale partial-layer transfers for residue and organic pools.
  mix_clay: Mixed clay mass/amount accumulated from affected layers so the mixed layer clay
    content can be recomputed.
  mix_silt: Mixed silt mass/amount accumulated from affected layers so the mixed layer silt
    content can be recomputed.
  mix_sand: Mixed sand mass/amount accumulated from affected layers so the mixed layer sand
    content can be recomputed.
  mix_sw: Mixed soil-water amount accumulated from affected layers for reconstituting layer
    water storage.
  mix_rock: Declared but not updated in the visible source; it appears intended as a mixed
    rock-fragment accumulator, but this routine does not use it.
  mix_bd: Declared as a mixed bulk-density accumulator; the visible source leaves the bulk-density
    update commented out, so it is not actively used here.
  mix_rsd: Declared as a mixed residue accumulator; the visible source initializes it but
    does not use it in the shown mixing calculations.
  stemp: Caches the current layer temperature before calling the temperature-response function
    for mixing efficiency.
  consf: Consolidation factor used to reduce or scale the biological mixing depth when tillage
    is active and the layer is not at field capacity.
  bio_mix_event: Logical event flag passed to `mgt_tillfactor` to indicate that the current
    update is a biological-mixing event.
uses:
  tillage_data_module: '`tillage_data_module` supplies the mixing-depth and tillage-control
    parameters that govern how much biological mixing is allowed and how the layer-specific
    mixing factor is adjusted during tillage conditions.'
  basin_module: '`basin_module` matters because the routine reads the basin carbon-model switch
    through `bsn_cc%cswat`, which controls whether the carbon-oriented soil mixing workflow
    is active in the calling context.'
  organic_mineral_mass_module: '`organic_mineral_mass_module` defines the mixed organic/mineral
    pool types and the per-HRU soil and plant mass objects that are read and overwritten while
    residues, humus pools, and mineral nutrients are redistributed through the mixing depth.'
  soil_module: '`soil_module` holds the HRU soil profile, layer geometry, water state, texture,
    and per-layer biological-mixing fields that determine where mixing applies and how the
    soil layer state is reassembled afterward.'
  constituent_mass_module: '`constituent_mass_module` matters only because the routine captures
    the number of simulated pests in `cs_db%num_pests`; the corresponding pesticide mixing
    block is present but commented out in the source.'
  plant_module: '`plant_module` provides the HRU plant-community size through `pcom(jj)%npl`,
    which sets how many plant residue pools must be mixed and reconstituted for each affected
    layer.'
  plant_data_module: '`plant_data_module` is listed in the `use` statements, but the extracted
    source does not show any directly referenced symbols from it in this routine.'
  hru_module: '`hru_module` provides the HRU-level tillage timing and switch state in `tillage_days(jj)`
    and `tillage_switch(jj)`, which determine whether the biological mixing factor is reduced,
    zeroed, or left at its initial value for each layer.'
---

<!-- facts:header -->

Biological mixing routine that redistributes soil residue, organic pools, and nutrients through the tilled/mixed depth of an HRU. It also adjusts layer mixing factors and passes the resulting mixing state to tillage-factor bookkeeping.

## Bottom Line

`mgt_biomix` simulates biological mixing in a single HRU. Given the HRU index `jj` and a biological mixing efficiency, it computes an effective mixing depth, weights that mixing by soil temperature and soil condition, and then redistributes mineral N/P, organic matter pools, residue, and soil texture/water properties across the affected layers.

The routine starts from the current soil, plant, residue, and mass-balance state for the selected HRU, builds mixed-pool totals for the layers inside the mixing zone, then reconstitutes each layer with a mixed and non-mixed fraction. At the end it updates tillage/mixing factors through `mgt_tillfactor` so later residue and carbon routines can use the new layer state.

## Arguments

<!-- facts:arguments -->

## Where It Fits

This routine runs from `hru_control` when the basin carbon switch is set to the carbon/mixing workflow (`bsn_cc%cswat == 2`) and the HRU’s biological mixing efficiency is positive. `hru_control` has already prepared the HRU state, including soil, residue, and plant-community pools, and the results here feed later carbon and residue routines such as `cbn_surfrsd_decomp`, `cbn_rsd_transfer`, and `cbn_zhang2`.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. Initialize mixed-pool state and scratch arrays. | Read the pesticide count, mark this as a biological-mixing event, zero the mixed mineral and organic pools, reset the mixed-component accumulators, and allocate per-layer scratch arrays sized to the HRU soil profile. |
| 2. Skip work when biological mixing is disabled. | If `biomix_eff` is effectively zero, the routine bypasses the depth and layer calculations entirely; otherwise it sets the current deepest layer and effective mixing depth from the soil profile and `bmix_depth`. |
| 3. Limit the mixing depth and enter the mixed-zone processing. | Treat very deep mixing as a special case, then ensure the effective depth is not treated as a shallow near-zero layer by promoting small positive depths before layer traversal begins. |
| 4. Traverse soil layers and compute layer-specific mixing efficiency. | For each layer, adjust the layer mixing factor based on tillage timing and soil consolidation, then apply a temperature response to obtain `emix`. Accumulate a depth-weighted sum until the loop reaches the first layer below the mixing zone or finds a frozen layer. |
| 5. Derive the average mixing efficiency over the active depth. | Convert the accumulated layer-weighted mixing efficiency into `avg_emix`, which becomes the single mixing fraction applied to the mixed portion of the profile. |
| 6. Compute each layer’s soil mass and mixed/non-mixed masses. | For each affected layer, calculate total layer mass, the mixed mass, the remaining unmixed mass, and the fraction of the layer depth that lies inside the mixing zone. |
| 7. Accumulate mixed soil-water, texture, mineral, organic, and residue pools. | Use the mixed fraction and depth fraction to add each layer’s contribution into the mixed pools for water, texture, mineral N/P, total organic matter, humus and CENTURY pools, and per-plant residue pools, including surface residue. |
| 8. Reconstitute the affected soil layers from mixed and unmixed fractions. | Write back each layer’s mineral, organic, residue, and water pools as a blend of unchanged material and the mixed pool, while subtracting the transferred surface residue from the plant residue totals. |
| 9. Recompute the mixed soil texture and water state. | Update clay, silt, sand, and soil water storage for each mixed layer from the mixed-pool values; the bulk-density update is present but commented out. |
| 10. Record the event in tillage-factor bookkeeping and clean up. | Call `mgt_tillfactor` with the HRU, event flag, average efficiency, and effective depth, then deallocate the scratch arrays and return to the caller. |

## Modules Used

<!-- facts:uses -->

| Module | State touched | Key components |
| --- | --- | --- |
| [sym:tillage_data_module] | `tillage_days, tillage_switch, bmix_depth, bio_consf, org_con%tmpf` | `tillage_days(jj), tillage_switch(jj), bmix_depth, bio_consf, org_con%tmpf` |
| [sym:basin_module] | `cs_db, bsn_cc` | `cs_db%num_pests, bsn_cc%cswat` |
| [sym:organic_mineral_mass_module] | `mix_org, soil1, pl_mass, mix_mn, mnz, mix_mp, mpz` | `mix_org%tot, mix_org%rsd, mix_org%hact, mix_org%hsta, mix_org%hs, mix_org%hp, mix_org%microb, mix_org%str, mix_org%lig, mix_org%meta, mix_org%man, mix_org%water, soil1(jj)%mn(l), soil1(jj)%mp(l), soil1(jj)%tot(l), soil1(jj)%hact(l), soil1(jj)%hsta(l), soil1(jj)%hs(l), soil1(jj)%hp(l), soil1(jj)%microb(l), soil1(jj)%str(l), soil1(jj)%lig(l), soil1(jj)%meta(l), soil1(jj)%man(l), soil1(jj)%water(l), mix_org%rsd(ipl), mix_org%surf_rsd, soil1(jj)%pl(ipl)%rsd(l), pl_mass(jj)%rsd(ipl), pl_mass(jj)%rsd_tot` |
| [sym:soil_module] | `soil` | `soil(jj)%nly, soil(jj)%phys(l)%st, soil(jj)%phys(l)%fc, soil(jj)%ly(l)%bmix, soil(jj)%ly(l)%init_bmix, soil(jj)%phys(l)%tmp, soil(jj)%phys(l)%d, soil(jj)%phys(l)%thick, soil(jj)%phys(l-1)%d, soil(jj)%phys(1)%bd, soil(jj)%phys(l)%rock, soil(jj)%phys(l)%bd, soil(jj)%phys(l)%sand, soil(jj)%phys(l)%silt, soil(jj)%phys(l)%clay` |
| [sym:constituent_mass_module] | `cs_db` | `cs_db%num_pests` |
| [sym:plant_module] | `pcom` | `pcom(jj)%npl` |
| [sym:hru_module] | `tillage_days, tillage_switch` |  |

## Local Variables

<!-- facts:locals -->

## State Changes

| Target | When | Meaning |
| --- | --- | --- |
| `mix_mn` | When `biomix_eff > 1.e-6` and the routine is mixing soil layers within `dtil`. | `mix_mn` is rebuilt as the depth-weighted mixed mineral-nitrogen pool. It starts at `mnz` and is incremented by the mixed fraction from each affected layer so the mixed layer can be written back with a single averaged mineral-N amount. |
| `mix_mp` | When `biomix_eff > 1.e-6` and the routine is mixing soil layers within `dtil`. | `mix_mp` becomes the depth-weighted mixed mineral-phosphorus pool. It is accumulated from each mixed layer and then used to reconstitute `soil1(jj)%mp(l)`. |
| `mix_org%tot` | When `biomix_eff > 1.e-6` and the routine is mixing soil layers within `dtil`. | `mix_org%tot` stores the mixed total organic matter pool across all affected layers. The routine uses it later to replace each layer’s total organic content with a mixed and non-mixed blend. |
| `mix_org%rsd` | When `biomix_eff > 1.e-6` and the routine is mixing soil layers within `dtil`. | `mix_org%rsd(ipl)` accumulates mixed residue for each plant in the community. It receives the residue mixed from soil layers and the portion of surface residue moved into the soil. |
| `mix_org%hact` | When `biomix_eff > 1.e-6` and the routine is mixing soil layers within `dtil`. | `mix_org%hact` is the mixed active-humus pool built from all affected layers so the layer active humus can be rebalanced after mixing. |
| `mix_org%hsta` | When `biomix_eff > 1.e-6` and the routine is mixing soil layers within `dtil`. | `mix_org%hsta` is the mixed stable-humus pool used to redistribute stable humus across the affected soil layers. |
| `mix_org%hs` | When `biomix_eff > 1.e-6` and the routine is mixing soil layers within `dtil`. | `mix_org%hs` becomes the mixed slow-humus pool used in the CENTURY-style carbon update for the mixed soil zone. |
| `mix_org%hp` | When `biomix_eff > 1.e-6` and the routine is mixing soil layers within `dtil`. | `mix_org%hp` becomes the mixed passive-humus pool used in the CENTURY-style carbon update for the mixed soil zone. |
| `mix_org%microb` | When `biomix_eff > 1.e-6` and the routine is mixing soil layers within `dtil`. | `mix_org%microb` stores the mixed microbial biomass pool for the affected layers. |
| `mix_org%str` | When `biomix_eff > 1.e-6` and the routine is mixing soil layers within `dtil`. | `mix_org%str` stores the mixed structural-litter pool for the affected layers. |
| `mix_org%lig` | When `biomix_eff > 1.e-6` and the routine is mixing soil layers within `dtil`. | `mix_org%lig` stores the mixed lignin pool for the affected layers. |
| `mix_org%meta` | When `biomix_eff > 1.e-6` and the routine is mixing soil layers within `dtil`. | `mix_org%meta` stores the mixed metabolic-litter pool for the affected layers. |
| `mix_org%man` | When `biomix_eff > 1.e-6` and the routine is mixing soil layers within `dtil`. | `mix_org%man` stores the mixed manure pool for the affected layers. |
| `mix_org%water` | When `biomix_eff > 1.e-6` and the routine is mixing soil layers within `dtil`. | `mix_org%water` stores the mixed water-soluble organic pool for the affected layers. |
| `soil(jj)%ly(l)%bmix` | When `biomix_eff > 1.e-6` and the routine is mixing soil layers within `dtil`. | `soil(jj)%ly(l)%bmix` is updated from `init_bmix` using consolidation rules and then used as the layer’s biological mixing factor for this event. |
| `mix_org%rsd(ipl)` | When residue from layer `l` lies inside the active mixing depth. | `mix_org%rsd(ipl)` gains the fraction of each plant’s layer residue that is mixed into the soil, plus the corresponding surface residue contribution. |
| `mix_org%surf_rsd` | When surface residue is transferred into the mixed soil zone. | `mix_org%surf_rsd` records the amount of surface residue that is moved into the soil during this layer pass, and that same amount is later subtracted from the plant residue store. |
| `soil1(jj)%mn(l)` | When the layer is inside the effective mixing depth. | `soil1(jj)%mn(l)` is rewritten as the unmixed remainder plus the mixed mineral-N share so each layer ends with a rebalanced mineral-N pool. |
| `soil1(jj)%mp(l)` | When the layer is inside the effective mixing depth. | `soil1(jj)%mp(l)` is rewritten as the unmixed remainder plus the mixed mineral-P share so each layer ends with a rebalanced mineral-P pool. |
| `soil1(jj)%tot(l)` | When the layer is inside the effective mixing depth. | `soil1(jj)%tot(l)` is rewritten from the unmixed layer fraction and the mixed total-organic pool, transferring organic matter through the mixed depth. |
| `soil1(jj)%pl(ipl)%rsd(l)` | When the layer is inside the effective mixing depth. | `soil1(jj)%pl(ipl)%rsd(l)` is rewritten from the unmixed residue plus the mixed residue share for each plant, so residue is redistributed through the soil profile. |
| `pl_mass(jj)%rsd(ipl)` | When surface residue is moved into mixed layers during the plant-by-plant loop. | `pl_mass(jj)%rsd(ipl)` is reduced by the amount of surface residue transferred into the soil, keeping the HRU surface residue total consistent with the mixed layer additions. |
| `pl_mass(jj)%rsd_tot` | When surface residue is moved into mixed layers during the plant-by-plant loop. | `pl_mass(jj)%rsd_tot` is reduced alongside the individual plant residue pool so the community-level surface residue total matches the layer transfer. |
| `soil1(jj)%hact(l)` | When the layer is inside the effective mixing depth. | `soil1(jj)%hact(l)` is rewritten from the unmixed remainder plus the mixed active-humus share to preserve mass balance after biological mixing. |

## File I/O

<!-- facts:io -->


## Lineage

`mgt_biomix.f90` was introduced in `7fc6b1e` (2026-04-03, "changes to correctly mix surface soil residue.") and has been changed in 10 non-merge commit(s) since, most recently `a96057d` (2026-05-15, "Fixed issue of tillagef not being initialized to 0. in cbn_zhang2. Corrected mgt…"). Lineage is reconstructed from commit metadata (SHA, date, subject); per-line diffs were unavailable in this build environment, so only the commits touching `mgt_biomix.f90` are listed.

- `a96057d` (2026-05-15) — Fixed issue of tillagef not being initialized to 0. in cbn_zhang2. Corrected mgt_biomass to correctly reflect the potentional bio mixing for…
- `092aaf3` (2026-05-06) — added moisture consilidation factor to mgt_biomix and mgt_tillfactor
- `951fbd8` (2026-05-06) — Initial working of biomixing increasing after tillage event by moisture content consolidation.
- `00a94aa` (2026-05-06) — Removed the biomix linear increase.
- `3ee775a` (2026-04-30) — Limited biomix linear increase to 30 days. Added tmpf2 and tmpf3 to code to biomix to limit biomix by soil layer temperature. Added tillagef…
- `7fc6b1e` (2026-04-03) — changes to correctly mix surface soil residue.

## Review Notes

- No direct file I/O was extracted for this procedure.
- warning: missing_doc: Procedure 'mgt_biomix' has no extracted documentation comment.
- algorithm_steps revised: replaced the draft’s broad placeholder steps with source-backed workflow steps tied to the visible line ranges.
- tillage_data_module and plant_data_module appear in the use list, but the extracted source does not resolve distinct owned symbols for plant_data_module and repeats tillage_data_module; those entries are documented conservatively.
- mix_rock, mix_bd, and mix_rsd are declared but not actively used in the visible source beyond initialization or comments.
- Lineage was reconstructed from file-level commit metadata; per-line diffs were unavailable in this environment (blobless clone), so line-span filtering was not applied.
