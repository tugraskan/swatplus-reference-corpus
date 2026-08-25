---
kind: procedure
symbol: cbn_surfrsd_decomp
title: cbn_surfrsd_decomp
status: filled
source_hash: 82d9d7f74caef487
version_label: SWAT+ 62.0.0
locals:
  j: HRU index selected from `ihru`; the routine uses it to access the current HRU's plant,
    soil, residue, and output state.
  rmn1: Temporary accumulator for nitrogen moving from fresh residue toward mineral/active
    pools. In this source it is reset inside the loop, but the extracted code does not show
    it being used afterward.
  rmp: Temporary accumulator for phosphorus moving from fresh residue toward labile/organic
    pools. In this source it is reset inside the loop, but the extracted code does not show
    it being used afterward.
  xx: 'Scratch variable for intermediate calculations: first holds the surface soil temperature
    for the temperature response curve, then holds the product of temperature and moisture
    factors before taking the square root for `csf`.'
  csf: Combined soil temperature and moisture stress factor used to scale the residue decomposition
    rate.
  cnr: Current residue carbon-to-nitrogen ratio for the active plant residue being processed;
    it is capped before computing the C:N response factor.
  cnrf: Carbon:nitrogen response factor that reduces residue decomposition when residue C:N
    is high.
  cpr: Current residue carbon-to-phosphorus ratio for the active plant residue being processed;
    it is capped before computing the C:P response factor.
  cprf: Carbon:phosphorus response factor that reduces residue decomposition when residue
    C:P is high.
  ca: Combined residue-quality multiplier formed as the minimum of the C:N factor, C:P factor,
    and 1.0.
  decr: Daily residue decay fraction computed from the plant residue coefficient, quality
    multiplier, and climate/soil stress factor, then bounded by the basin minimum and 1.0.
  ipl: Loop index over plants in the current HRU's plant community.
  idp: Plant database index taken from the current plant status entry; used to look up residue-decomposition
    coefficients for the active plant.
  cdg: Temperature response factor for residue decomposition, computed from surface soil temperature.
  sut: Soil water response factor for residue decomposition, computed from surface soil water
    relative to field capacity and floored at 0.05.
uses:
  septic_data_module: The procedure `use`s this module, but the extracted source does not
    show any referenced symbols from it, so it does not appear to influence the visible calculation
    directly.
  basin_module: '`bsn_prm%decr_min` supplies the basin-wide minimum daily residue decay rate.
    The routine enforces this floor when it computes `decr`, so basin settings control the
    lower bound on decomposition even under poor conditions.'
  organic_mineral_mass_module: These residue and soil organic-mass structures are the central
    storage the routine updates. `pl_mass(j)%rsd(ipl)` and `pl_mass(j)%rsd_tot` hold fresh
    residue being depleted, `photo_decomp` and `decomp` are temporary transfer pools, and
    `soil1(j)%meta(1)`, `soil1(j)%str(1)`, and `soil1(j)%lig(1)` receive the decomposed material.
  hru_module: '`ihru` identifies which HRU is being processed. The routine copies it into
    `j` so every update is applied to the current HRU''s residue, soil, plant, and output
    records.'
  soil_module: '`soil(j)%phys(1)%tmp` determines whether surface residue decomposition proceeds
    at all, and `soil(j)%phys(1)%fc` is used in the moisture-factor calculation. Together
    they control the climate/soil stress term that scales decay.'
  plant_module: '`pcom(j)%npl` sets the number of plants to iterate over, and `pcom(j)%plcur(ipl)%idplt`
    identifies the plant database record whose residue decomposition coefficient is used for
    that plant''s residue.'
  plant_data_module: '`pldb(idp)%rsdco_pl` provides the plant-specific residue decomposition
    coefficient, while `cswat_1_part_fracs(idp)%meta_frac_abg`, `%str_frac_abg`, and `%lig_frac_abg`
    provide the partitioning fractions used when decomposed residue is transferred into the
    soil organic pools. `photo_degrade_factor` supplies the fixed fraction used for the initial
    photodegradation loss.'
  output_landscape_module: '`hnb_d(j)` stores the HRU-level nutrient-balance diagnostics that
    this routine resets at the start of the calculation. Those fields track residue-related
    N and P transfers and therefore need to be cleared before daily accounting begins.'
  carbon_module: The carbon-ratio caps and references set the response curves used to convert
    residue C:N and C:P ratios into decomposition penalties. They control how strongly poor
    residue quality suppresses the daily decay rate.
---

<!-- facts:header -->

Computes daily surface-residue decomposition and associated carbon, nitrogen, and phosphorus transfers for one HRU. It updates residue pools, soil organic matter pools, and nutrient-balance diagnostics based on temperature, moisture, residue quality, and plant-specific decomposition coefficients.

## Bottom Line

cbn_surfrsd_decomp runs once for the current HRU and loops through each plant community residue pool. For each plant, it first applies a small photo-degradation loss, then — when surface soil temperature is above freezing — computes a combined temperature/moisture stress factor plus C:N and C:P quality factors to determine how much of the remaining residue decomposes that day.

The routine reduces fresh residue mass in `pl_mass(j)%rsd(ipl)` and `pl_mass(j)%rsd_tot`, accumulates photo-degraded carbon in `hrc_d(j)%emit_c`, and moves the decomposed residue into the surface soil organic pools `soil1(j)%meta(1)`, `soil1(j)%str(1)`, and `soil1(j)%lig(1)`. It also zeroes several HRU nutrient-balance tracking fields before the loop so the calling workflow can sum daily residue-related transfers cleanly.

## Arguments

<!-- facts:arguments -->

## Where It Fits

This routine runs inside `hru_control` during the CSWAT=2 surface-residue decomposition path, after the HRU index and daily state have been established and after biomass mixing if enabled. Its results feed the later residue-transfer and mineralization steps in the same HRU update sequence, so the residue pools, soil organic pools, and carbon-emission bookkeeping must be updated here before the rest of the daily carbon/nutrient processing continues.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. Bind the current HRU and clear daily residue-transfer diagnostics. | The routine copies `ihru` into `j` and zeroes the HRU output fields used to accumulate daily residue-related nitrogen and phosphorus transfers. |
| 2. Loop over each plant residue pool in the current HRU. | The routine processes each plant community member one at a time so residue decomposition can be computed with plant-specific residue parameters. |
| 3. Apply photodegradation to the surface residue pool. | A fixed fraction of each plant's residue is removed as photo-degraded material, the residue pools are reduced, and the lost carbon is counted in `hrc_d(j)%emit_c` so the carbon balance remains explicit. |
| 4. Gate the remaining decomposition on surface soil temperature. | If the surface soil is above freezing, the routine computes a moisture factor from soil water and field capacity, then computes a temperature response factor from surface temperature and combines them into `csf`. |
| 5. Compute residue quality penalties from C:N and C:P. | The routine derives residue C:N and C:P ratios when the pools contain enough N or P, caps those ratios at basin-controlled limits, and converts them into reduction factors before combining them into the quality multiplier `ca`. |
| 6. Look up the plant-specific decay coefficient and compute daily decay. | Using the active plant's database entry, the routine multiplies the plant residue coefficient by the combined quality and climate factors, enforces the basin minimum and a maximum of 1.0, and applies the resulting fraction to the residue pool. |
| 7. Clamp tiny residue mass components to zero and move decomposed residue into soil organic pools. | After updating the residue pool, the routine removes underflow-prone near-zero component values and adds the decomposed residue to the surface soil metabolic, structural, and lignin pools using plant-specific partition fractions. |
| 8. Leave nutrient partitioning comments in place and continue to the next plant. | The routine documents intended N and P partitioning logic but the active extracted code does not assign those commented terms; it then ends the plant loop and returns to the caller. |

## Modules Used

<!-- facts:uses -->

| Module | State touched | Key components |
| --- | --- | --- |
| [sym:septic_data_module] | `septic_data_module state is imported but no candidate reference from that module was resolved in the extracted source.` |  |
| [sym:basin_module] | `bsn_prm` | `bsn_prm%decr_min` |
| [sym:organic_mineral_mass_module] | `pl_mass, photo_decomp, soil1, decomp` | `pl_mass(j)%rsd(ipl), pl_mass(j)%rsd_tot, photo_decomp%c, pl_mass(j)%rsd(ipl)%n, pl_mass(j)%rsd(ipl)%c, pl_mass(j)%rsd(ipl)%p, pl_mass(j)%rsd(ipl)%m, soil1(j)%meta(1), soil1(j)%str(1), soil1(j)%lig(1)` |
| [sym:hru_module] | `ihru` |  |
| [sym:soil_module] | `soil` | `soil(j)%phys(1)%tmp, soil(j)%phys(1)%fc` |
| [sym:plant_module] | `pcom` | `pcom(j)%npl, pcom(j)%plcur(ipl)%idplt` |
| [sym:plant_data_module] | `pldb, cswat_1_part_fracs, photo_degrade_factor` | `pldb(idp)%rsdco_pl, cswat_1_part_fracs(idp)%meta_frac_abg, cswat_1_part_fracs(idp)%str_frac_abg, cswat_1_part_fracs(idp)%lig_frac_abg` |
| [sym:output_landscape_module] | `hnb_d` | `hnb_d(j)%act_nit_n, hnb_d(j)%org_lab_p, hnb_d(j)%act_sta_n, hnb_d(j)%denit, hnb_d(j)%rsd_nitorg_n, hnb_d(j)%rsd_laborg_p` |
| [sym:carbon_module] | `cnr_cap, cnr_ref, cpr_cap, cpr_ref` |  |

## Local Variables

<!-- facts:locals -->

## State Changes

| Target | When | Meaning |
| --- | --- | --- |
| `hnb_d(j)%act_nit_n` | Each plant residue is processed, and `photo_decomp` is computed before the temperature gate. | `hnb_d(j)%act_nit_n` is cleared at the start of the HRU update so the day's residue-related nitrogen accounting begins from zero before any subsequent summing elsewhere in the workflow. |
| `hnb_d(j)%org_lab_p` | Each plant residue is processed, and `photo_decomp` is computed before the temperature gate. | `hnb_d(j)%org_lab_p` is cleared so the routine can contribute fresh daily residue-to-labile-phosphorus accounting without carrying values from earlier calls. |
| `hnb_d(j)%act_sta_n` | Each plant residue is processed, and `photo_decomp` is computed before the temperature gate. | `hnb_d(j)%act_sta_n` is cleared so active-to-stable nitrogen transfer bookkeeping for this HRU starts at zero for the day. |
| `hnb_d(j)%denit` | Each plant residue is processed, and `photo_decomp` is computed before the temperature gate. | `hnb_d(j)%denit` is cleared so the HRU's daily nitrogen-loss diagnostics do not retain stale values when residue decomposition is recomputed. |
| `hnb_d(j)%rsd_nitorg_n` | Each plant residue is processed, and `photo_decomp` is computed before the temperature gate. | `hnb_d(j)%rsd_nitorg_n` is cleared so surface-residue nitrogen transfer can be accumulated cleanly during the current day's processing. |
| `hnb_d(j)%rsd_laborg_p` | Each plant residue is processed, and `photo_decomp` is computed before the temperature gate. | `hnb_d(j)%rsd_laborg_p` is cleared so surface-residue phosphorus transfer can be accumulated cleanly during the current day's processing. |
| `photo_decomp` | On every plant iteration, before the soil-temperature test. | `photo_decomp` is assigned the photodegraded portion of the current plant's residue. Its carbon is immediately counted as an emission and the residue pool is reduced by the same amount. |
| `pl_mass(j)%rsd(ipl)` | On every plant iteration, after `photo_decomp` and after the decay fraction `decr` are computed. | `pl_mass(j)%rsd(ipl)` is reduced first by photodegradation and then by the main decay fraction, so the active residue pool shrinks as decomposition proceeds. |
| `pl_mass(j)%rsd_tot` | On every plant iteration when residue is removed by photodegradation or decay. | `pl_mass(j)%rsd_tot` is decremented to keep the HRU-level total fresh residue pool consistent with the per-plant residue losses. |
| `hrc_d(j)%emit_c` | Whenever photodegradation removes residue carbon from `pl_mass(j)%rsd(ipl)`. | `hrc_d(j)%emit_c` increases by the carbon content of `photo_decomp`, recording the photodegraded residue carbon as an emitted carbon term. |
| `decomp` | After climate and residue-quality factors are computed and the basin minimum decay floor is enforced. | `decomp` stores the actual mass, carbon, nitrogen, and phosphorus removed from the current residue pool for transfer into soil organic matter. |
| `soil1(j)%meta(1)` | When the current surface soil temperature is above zero and the main residue decay fraction has been applied. | `soil1(j)%meta(1)` receives the metabolic fraction of decomposed residue, increasing the surface soil metabolic organic pool. |
| `soil1(j)%str(1)` | When the current surface soil temperature is above zero and the main residue decay fraction has been applied. | `soil1(j)%str(1)` receives the structural fraction of decomposed residue, increasing the surface soil structural organic pool. |
| `soil1(j)%lig(1)` | When the current surface soil temperature is above zero and the main residue decay fraction has been applied. | `soil1(j)%lig(1)` receives the lignin fraction of decomposed residue, increasing the surface soil lignin organic pool. |

## File I/O

<!-- facts:io -->


## Lineage

Three resolved commits changed `cbn_surfrsd_decomp`. In 08d78c9, the routine dropped `isep` from the `hru_module` import. In d98c126, it was reworked to use `ihru` as the HRU index, introduced `photo_decomp` handling, and began subtracting photodegraded residue before the main decomposition logic. In bc7755a, the routine added `carbon_module` imports, changed `ipl` and `idp` to integers, booked `photo_decomp%c` into `hrc_d(j)%emit_c`, switched the C:N and C:P caps/references to module constants, and removed the local `nactfr` variable.

- 08d78c9: removed the unused `isep` import from `hru_module` so the routine only depends on `ihru` from that module.
- d98c126: established the current surface-residue decomposition structure, including `photo_decomp` subtraction before the main decay calculation and use of `ihru` to select the HRU.
- bc7755a: made decomposition parameters data-driven via `carbon_module`, corrected loop/index types for `ipl` and `idp`, and recorded photodegraded carbon in `hrc_d(j)%emit_c`.

## Review Notes

- No direct file I/O was extracted for this procedure.
- warning: missing_doc: Procedure 'cbn_surfrsd_decomp' has no extracted documentation comment.
