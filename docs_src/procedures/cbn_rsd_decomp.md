---
kind: procedure
symbol: cbn_rsd_decomp
title: cbn_rsd_decomp
status: filled
source_hash: 711ffa067e833e74
version_label: SWAT+ 62.0.0
locals:
  j: HRU index copied from `ihru`; it selects which element of `soil`, `soil1`, `pcom`, and
    `hnb_d` this routine updates.
  k: Soil-layer loop counter; it identifies the layer being processed within the current HRU.
  rmn1: Temporary amount of nitrogen transferred from fresh organic residue into nitrate and
    active organic pools; declared for residue mineralization bookkeeping, but not used in
    the extracted code path.
  rmp: Temporary amount of phosphorus transferred from fresh organic residue into labile and
    organic pools; declared for residue mineralization bookkeeping, but not used in the extracted
    code path.
  xx: Scratch variable used for intermediate calculations, first for soil temperature in the
    exponential temperature response and then for the product of temperature and water stress
    factors.
  csf: Combined soil temperature/soil water decomposition factor, computed as the square root
    of the temperature-water product and used to scale residue decay.
  cnr: Carbon-to-nitrogen ratio of the fresh residue in the current plant/layer, capped before
    being converted to a decay factor.
  cnrf: C:N ratio reduction factor; it converts the residue C:N ratio into a multiplier that
    limits decomposition when residue is N-poor.
  cpr: Carbon-to-phosphorus ratio of the fresh residue in the current plant/layer, capped
    before being converted to a decay factor.
  cprf: C:P ratio reduction factor; it converts the residue C:P ratio into a multiplier that
    limits decomposition when residue is P-poor.
  ca: Overall residue quality factor formed as the minimum of the C:N factor, C:P factor,
    and 1.0; it limits decomposition by the most restrictive nutrient ratio.
  decr: Daily residue decay fraction before multiplication by residue mass; it combines residue
    coefficient, nutrient quality, and environment factors and is bounded by basin minimum
    and 1.0.
  ipl: Plant-community loop counter; it selects the current plant in `pcom(j)` whose residue
    is being decomposed.
  idp: Plant database index taken from the current plant status; it is used to look up the
    residue decomposition coefficient in `pldb`.
  cdg: Soil temperature response factor derived from the layer temperature; it is multiplied
    with soil water response to form the combined decomposition factor.
  sut: Soil water response factor derived from layer storage relative to field capacity; it
    is multiplied with the temperature factor to form the combined decomposition factor.
uses:
  septic_data_module: The source uses `use septic_data_module`, but the extracted lines do
    not show any resolved symbol from that module being referenced in the routine body, so
    its specific role here is uncertain from the available evidence.
  basin_module: '`bsn_prm%decr_min` sets the floor on the residue decay fraction, so basin-wide
    carbon settings control how little decomposition can occur on a day.'
  organic_mineral_mass_module: '`organic_mineral_mass_module` supplies the residue and soil
    organic-matter containers that this routine directly updates: residue is removed from
    `soil1(j)%pl(ipl)%rsd(k)` and redistributed into `soil1(j)%meta(k)`, `soil1(j)%str(k)`,
    `soil1(j)%lig(k)`, and related N and P pools.'
  hru_module: '`ihru` identifies the active HRU. The routine copies it into `j` and then uses
    that index to select the matching soil profile, plant community, residue pools, and daily
    output record.'
  soil_module: '`soil(j)%nly` controls how many soil layers are processed, while `soil(j)%phys(k)%tmp`
    and `soil(j)%phys(k)%fc` provide the temperature and field-capacity inputs used to compute
    the daily decomposition environment factor.'
  plant_module: '`pcom(j)%npl` controls how many plants are visited in the current HRU, and
    `pcom(j)%plcur(ipl)%idplt` identifies which plant database record supplies the residue
    decomposition coefficient for each plant.'
  plant_data_module: '`pldb(idp)%rsdco_pl` is the plant-specific residue decomposition coefficient,
    and `cswat_1_part_fracs(idp)%meta_frac_blg`, `%str_frac_blg`, and `%lig_frac_blg` provide
    the below-ground partitioning fractions used to distribute decomposed residue into metabolic,
    structural, and lignin pools.'
  output_landscape_module: '`hnb_d(j)` holds the HRU daily nutrient-balance outputs that this
    routine zeroes before accumulation, so residue-driven transfers can be reported consistently
    in later output processing.'
  carbon_module: '`cnr_cap`, `cnr_ref`, `cpr_cap`, and `cpr_ref` parameterize the residue-quality
    response curves that turn residue C:N and C:P ratios into decomposition-limiting factors.'
---

<!-- facts:header -->

Computes daily residue decomposition and organic matter mineralization for one HRU. It partitions residue loss into soil carbon, nitrogen, and phosphorus pool updates while applying temperature, water, and C:N/C:P constraints.

## Bottom Line

This subroutine walks the soil layers of the current HRU and, for each plant in the community, computes how much fresh residue decomposes on that day. It uses soil temperature, soil water, residue C:N and C:P ratios, the plant residue decomposition coefficient, and a basin minimum decay limit to decide the decay fraction.

The decomposed residue is removed from the plant residue pool and added to metabolic, structural, and lignin soil organic pools, with corresponding N and P transfers. It also resets daily HRU nutrient-balance trackers in `hnb_d(j)` so downstream accounting can report residue-driven nitrogen and phosphorus movement.

## Arguments

<!-- facts:arguments -->

## Where It Fits

This routine runs during daily HRU residue and soil-organic-matter updating, after `ihru`, soil state, plant community membership, and plant database lookups are available. It depends on those upstream state holders to compute decomposition and then feeds updated residue, soil organic pools, and daily nutrient-balance state into later carbon, nitrogen, phosphorus, and output accounting.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. Select the active HRU and clear daily output accumulators | Copies `ihru` into `j` and zeroes the HRU daily nutrient-balance fields in `hnb_d(j)` so this day's residue-driven transfers start from a clean slate. |
| 2. Loop over each soil layer and each plant in the community | Processes every layer in `soil(j)` and every plant in `pcom(j)` to apply residue decomposition wherever plant residue exists in that layer. |
| 3. Gate decomposition on positive soil temperature | Skips mineralization in cold layers and only evaluates residue decay when `soil(j)%phys(k)%tmp` is above zero. |
| 4. Compute soil moisture and temperature factors | Calculates a water factor from storage relative to field capacity, a temperature factor from layer temperature, clamps both to minimum values, and combines them into `csf`. |
| 5. Derive residue-quality factors from C:N and C:P ratios | Forms residue C:N and C:P ratios from `soil1(j)%pl(ipl)%rsd(k)`, caps them with `cnr_cap` and `cpr_cap`, converts them to response factors, and selects the most limiting factor in `ca`. |
| 6. Look up the plant-specific residue coefficient and compute decay | Uses the current plant's `idplt` to fetch `pldb(idp)%rsdco_pl`, multiplies it by `ca` and `csf`, bounds the result by `bsn_prm%decr_min` and 1.0, and scales the residue mass into `decomp`. |
| 7. Remove decomposed residue from the fresh residue pools | Subtracts `decomp` from the plant residue object and total residue pool for the layer, then clips tiny remaining mass, carbon, nitrogen, and phosphorus values to zero to avoid underflow. |
| 8. Add decomposed mass and carbon to soil organic pools | Distributes `decomp%m` and `decomp%c` into the metabolic, structural, and lignin pools using `cswat_1_part_fracs(idp)` below-ground fractions. |
| 9. Partition nitrogen from decomposed residue into soil pools | Computes metabolic and structural nitrogen shares from residue C and N, stores the metabolic share in `rsd_meta%n`, adds it to the metabolic pool, derives the structural share in `rsd_str%n`, and sends a lignin fraction of that structural nitrogen to `soil1(j)%lig(k)%n`. |
| 10. Partition phosphorus from decomposed residue into soil pools | Computes metabolic phosphorus in `rsd_meta%p`, adds it to the metabolic pool, derives structural phosphorus in `rsd_str%p`, and sends a lignin fraction of that structural phosphorus to `soil1(j)%lig(k)%p`. |
| 11. Finish the nested loops and return | Exits the temperature gate, completes the plant and layer loops, and returns to the caller with updated residue and soil-organic state. |

## Modules Used

<!-- facts:uses -->

| Module | State touched | Key components |
| --- | --- | --- |
| [sym:septic_data_module] | `septic_data_module state or types` |  |
| [sym:basin_module] | `bsn_prm` | `bsn_prm%decr_min` |
| [sym:organic_mineral_mass_module] | `soil1, decomp, rsd_meta, rsd_str, lig_frac` | `soil1(j)%pl(ipl)%rsd(k)%n, soil1(j)%pl(ipl)%rsd(k)%c, soil1(j)%pl(ipl)%rsd(k)%p, soil1(j)%pl(ipl)%rsd(k), soil1(j)%rsd_tot(k), soil1(j)%pl(ipl)%rsd(k)%m, soil1(j)%meta(k)%m, decomp%m, soil1(j)%str(k)%m, soil1(j)%lig(k)%m, soil1(j)%meta(k)%c, decomp%c, soil1(j)%str(k)%c, soil1(j)%lig(k)%c, rsd_meta%n, decomp%n, soil1(j)%meta(k)%n, rsd_str%n, soil1(j)%str(k)%n, soil1(j)%lig(k)%n, rsd_meta%p, decomp%p, soil1(j)%meta(k)%p, rsd_str%p, soil1(j)%str(k)%p, soil1(j)%lig(k)%p` |
| [sym:hru_module] | `ihru` |  |
| [sym:soil_module] | `soil` | `soil(j)%nly, soil(j)%phys(k)%tmp, soil(j)%phys(k)%fc` |
| [sym:plant_module] | `pcom` | `pcom(j)%npl, pcom(j)%plcur(ipl)%idplt` |
| [sym:plant_data_module] | `pldb, cswat_1_part_fracs` | `pldb(idp)%rsdco_pl, cswat_1_part_fracs(idp)%meta_frac_blg, cswat_1_part_fracs(idp)%str_frac_blg, cswat_1_part_fracs(idp)%lig_frac_blg` |
| [sym:output_landscape_module] | `hnb_d` | `hnb_d(j)%act_nit_n, hnb_d(j)%org_lab_p, hnb_d(j)%act_sta_n, hnb_d(j)%denit, hnb_d(j)%rsd_nitorg_n, hnb_d(j)%rsd_laborg_p` |
| [sym:carbon_module] | `cnr_cap, cnr_ref, cpr_cap, cpr_ref` |  |

## Local Variables

<!-- facts:locals -->

## State Changes

| Target | When | Meaning |
| --- | --- | --- |
| `hnb_d(j)%act_nit_n` | After `j = ihru`, before the layer/plant loops begin. | `hnb_d(j)%act_nit_n` is reset to zero so the routine can accumulate today's nitrogen transfer from active organic pools later in the HRU accounting chain. |
| `hnb_d(j)%org_lab_p` | After `j = ihru`, before the layer/plant loops begin. | `hnb_d(j)%org_lab_p` is reset to zero so today's phosphorus movement from organic to labile pools can be accumulated from scratch. |
| `hnb_d(j)%act_sta_n` | After `j = ihru`, before the layer/plant loops begin. | `hnb_d(j)%act_sta_n` is reset to zero so today's active-to-stable nitrogen transfer can be accumulated consistently. |
| `hnb_d(j)%denit` | After `j = ihru`, before the layer/plant loops begin. | `hnb_d(j)%denit` is reset to zero as part of clearing the HRU daily nitrogen-balance diagnostics before residue decomposition is tallied. |
| `hnb_d(j)%rsd_nitorg_n` | After `j = ihru`, before the layer/plant loops begin. | `hnb_d(j)%rsd_nitorg_n` is reset to zero so residue-to-nitrogen transfer can be accumulated for the current day only. |
| `hnb_d(j)%rsd_laborg_p` | After `j = ihru`, before the layer/plant loops begin. | `hnb_d(j)%rsd_laborg_p` is reset to zero so residue-to-phosphorus transfer can be accumulated for the current day only. |
| `decomp` | When a layer is warm enough for decomposition and the residue decay fraction is computed. | `decomp` becomes the amount of residue mass, carbon, nitrogen, and phosphorus removed from `soil1(j)%pl(ipl)%rsd(k)` for this plant and layer. |
| `soil1(j)%pl(ipl)%rsd(k)` | When `soil(j)%phys(k)%tmp > 0.` and the computed decay fraction is applied. | `soil1(j)%pl(ipl)%rsd(k)` is reduced by `decomp`, representing the fresh residue that decomposed during the day. |
| `soil1(j)%rsd_tot(k)` | When `soil(j)%phys(k)%tmp > 0.` and the computed decay fraction is applied. | `soil1(j)%rsd_tot(k)` is reduced by the same decomposed residue mass so the layer-total residue pool stays consistent with the plant-specific residue pool. |
| `soil1(j)%meta(k)%m` | When `soil(j)%phys(k)%tmp > 0.` and residue carbon is redistributed. | `soil1(j)%meta(k)%m` increases by the metabolic fraction of decomposed residue mass, adding fresh litter to the metabolic soil pool. |
| `soil1(j)%str(k)%m` | When `soil(j)%phys(k)%tmp > 0.` and residue carbon is redistributed. | `soil1(j)%str(k)%m` increases by the structural fraction of decomposed residue mass, adding fresh litter to the structural soil pool. |
| `soil1(j)%lig(k)%m` | When `soil(j)%phys(k)%tmp > 0.` and residue carbon is redistributed. | `soil1(j)%lig(k)%m` increases by the lignin fraction of decomposed residue mass, adding resistant litter to the lignin soil pool. |
| `soil1(j)%meta(k)%c` | When `soil(j)%phys(k)%tmp > 0.` and residue carbon is redistributed. | `soil1(j)%meta(k)%c` increases by the metabolic share of decomposed carbon. |
| `soil1(j)%str(k)%c` | When `soil(j)%phys(k)%tmp > 0.` and residue carbon is redistributed. | `soil1(j)%str(k)%c` increases by the structural share of decomposed carbon. |
| `soil1(j)%lig(k)%c` | When `soil(j)%phys(k)%tmp > 0.` and residue carbon is redistributed. | `soil1(j)%lig(k)%c` increases by the lignin share of decomposed carbon. |
| `rsd_meta%n` | When metabolic nitrogen is solved for a warm layer. | `rsd_meta%n` stores the metabolic nitrogen portion of the decomposed residue, or zero if the metabolic pool carbon is too small for the calculation. |
| `soil1(j)%meta(k)%n` | When metabolic nitrogen is solved for a warm layer. | `soil1(j)%meta(k)%n` increases by the metabolic nitrogen share from decomposed residue. |
| `rsd_str%n` | When structural and lignin nitrogen are solved for a warm layer. | `rsd_str%n` stores the structural nitrogen portion of the decomposed residue. |
| `soil1(j)%str(k)%n` | When structural and lignin nitrogen are solved for a warm layer. | `soil1(j)%str(k)%n` increases by the structural nitrogen share from decomposed residue. |
| `soil1(j)%lig(k)%n` | When structural nitrogen is split into lignin-associated nitrogen. | `soil1(j)%lig(k)%n` increases by the lignin fraction of the structural nitrogen share. |
| `rsd_meta%p` | When metabolic phosphorus is solved for a warm layer. | `rsd_meta%p` stores the metabolic phosphorus portion of the decomposed residue, or zero if the metabolic pool carbon is too small for the calculation. |
| `soil1(j)%meta(k)%p` | When metabolic phosphorus is solved for a warm layer. | `soil1(j)%meta(k)%p` increases by the metabolic phosphorus share from decomposed residue. |
| `rsd_str%p` | When structural and lignin phosphorus are solved for a warm layer. | `rsd_str%p` stores the structural phosphorus portion of the decomposed residue. |
| `soil1(j)%str(k)%p` | When structural and lignin phosphorus are solved for a warm layer. | `soil1(j)%str(k)%p` increases by the structural phosphorus share from decomposed residue. |

## File I/O

<!-- facts:io -->


## Theory Equations

| Eq. | Title | Formula | Implementation |
| --- | --- | --- | --- |
| 3:2.2.10 | P mineralized from fresh organic (80% to labile) | $P_{minf,ly}=0.8*\delta_{ntr,ly}*orgP_{frsh,ly}$ | Verified against SWAT+ 62.0.0 (cbn_rsd_decomp.f90). (0.8 residue-P min) |
| 3:2.2.11 | P moving to stable organic pool (20%) | $P_{dec,ly}=0.2*\delta_{ntr,ly}*orgP_{frsh,ly}$ | Verified against SWAT+ 62.0.0 (cbn_rsd_decomp.f90). (0.2 residue-P decomp) |

## Lineage

Source-backed lineage commits were resolved. The routine originally used fixed C:N and C:P caps and reference values, then later moved those constants into `carbon_module`; it also changed the residue-partition source from `cswat_3_part_fracs` to `cswat_1_part_fracs`, corrected a subtraction bug so `rsd_tot` is reduced by `decomp`, and added/retained the use of `transfer` vs. `decomp` in the residue-to-soil allocation logic before finally standardizing the carbon-ratio constants to module inputs.

- bc7755a replaced hard-coded residue C:N/C:P caps and reference values with `carbon_module` constants (`cnr_cap`, `cnr_ref`, `cpr_cap`, `cpr_ref`) and updated the decay-factor formulas to use them.
- fc00a75 switched the below-ground residue partition fractions used for soil pool allocation from `cswat_3_part_fracs` to `cswat_1_part_fracs`.
- 0d9fe7b corrected `soil1(j)%rsd_tot(k)` to subtract `decomp` and changed the soil-organic pool additions to use `decomp` instead of `transfer` in that revision.
- a3ae724 introduced the `soil1(j)%rsd_tot(k)` subtraction and replaced the commented-out legacy residue partitioning lines with explicit `cswat_3_part_fracs`-based transfers.

## Review Notes

- No direct file I/O was extracted for this procedure.
- warning: missing_doc: Procedure 'cbn_rsd_decomp' has no extracted documentation comment.
- algorithm_steps revised: merged the nested-loop and state-update view into 11 source-backed steps that follow the actual execution order.
- The source declares `septic_data_module` but the extracted routine body does not show a resolved symbol from it, so its specific effect here is uncertain from the available evidence.
