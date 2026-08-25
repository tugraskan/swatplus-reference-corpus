---
kind: procedure
symbol: mgt_transplant
title: mgt_transplant
status: filled
source_hash: 0ccce27024773921
version_label: SWAT+ 62.0.0
args:
  itrans: Selects which transplant database record in transpl() supplies the initial plant
    heat units, biomass, maturity timing, and population settings used to initialize the active
    plant.
locals:
  j: HRU index copied from ihru so the routine can update the current hydrologic response
    unit's active plant records.
  icom: Plant-community index taken from hru(j)%plant_cov to choose the active community record
    in pcom and pcomdb.
  idp: Plant database index taken from the current plant status idplt so the routine can read
    species parameters from pldb and plcp.
  xx: Temporary copy of transpl(itrans)%pop used in the LAI population scaling equation when
    transplant population is nonzero.
  laimx_pop: Temporary result for potential maximum LAI after adjusting the species LAI cap
    by transplant population.
uses:
  hru_module: This module supplies the current HRU index and plant-community linkage that
    identify which active plant slot is being transplanted. The routine reads hru(j)%plant_cov
    to locate the community, uses ihru to target the active HRU, and uses ipl to address the
    plant slot within that HRU.
  plant_module: This module holds the active plant status, growth, and mass records that are
    rewritten by the transplant setup. mgt_transplant copies transplant database values into
    pcom(j)%plcur, pcom(j)%plg, and pcom(j)%plm so the current plant starts with the correct
    heat-unit, maturity, LAI, and biomass fractions.
  plant_data_module: This module provides the transplant database record, species parameter
    tables, and community lookup needed to parameterize the transplant. mgt_transplant reads
    transpl, plcp, pcomdb, and pldb to map the requested transplant to species-specific heat-unit,
    LAI, population, and nutrient-allocation coefficients.
  organic_mineral_mass_module: This module stores the plant biomass pools that are initialized
    here. mgt_transplant sets pl_mass(j)%tot(ipl)%m and then calls biomass partitioning routines
    that depend on the total plant mass to populate the root and seed compartments consistently.
---

<!-- facts:header -->

Initializes a transplant operation for the active HRU plant. It loads transplant database values into the current plant state, sets biomass and nutrient fractions, and then rebuilds root, seed, and partitioned biomass pools.

## Bottom Line

mgt_transplant applies a named transplant record to the current HRU/plant slot. It copies transplant heat-unit, biomass, population, and timing settings into the active plant community, then derives leaf-area potential and starting C/N/P partitioning for that plant.

This matters because a transplant operation needs the plant state to start in a consistent, simulation-ready condition before later growth, stress, and harvest routines run. The routine also triggers the plant biomass initialization helpers so the active plant’s root, seed, and partition pools match the transplant setup.

## Arguments

<!-- facts:arguments -->

## Where It Fits

This routine runs when a management action or schedule requests a transplant operation for the current HRU. actions sets up the active plant state and passes d_tbl%act_app(iac) as the transplant record, while mgt_sched looks up the transplant name in the management database and passes the matching transplant index. The results are then used by later plant-growth and output behavior, including the plant mass, LAI potential, and status values written to management output.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. check transplant population | If the requested transplant population is essentially zero, set potential LAI to the species maximum blai. Otherwise, scale blai by population using the population response curve so small or sparse transplants start with a reduced potential leaf area. |
| 2. set active HRU and plant indices | Copy the current HRU index from ihru into j, use hru(j)%plant_cov to find the active plant community in icom, and read the current plant database id into idp from pcom(j)%plcur(ipl)%idplt. |
| 3. copy transplant heat units | Load the starting heat-unit fraction from transpl(itrans)%phuacc and compute the perennial heat-unit fraction phuacc_p from the transplant’s maturity fraction, current plant maturity state, and transplant heat-unit setting. Use those values to compute laimxfr and laimxfr_p from species leaf-shape parameters. |
| 4. initialize biomass mass | Set the active plant total biomass to transpl(itrans)%bioms, then compute the current-year maturity counter from the transplant maturity fraction and plant database maturity years, forcing it to be at least 1. |
| 5. reset plant identity and nutrient fractions | Replace the current plant status idplt with the community database plant id, then compute phosphorus and nitrogen fractions from species uptake curves and the transplant heat-unit fraction so the active biomass has appropriate initial nutrient ratios. |
| 6. store potential LAI from population | Convert the transplant population into a temporary scale factor when population is nonzero, calculate laimx_pop, and assign it to pcom(j)%plcur(ipl)%lai_pot. |
| 7. initialize root, seed, and partition pools | Call pl_root_gro, pl_seed_gro, and pl_partition with init code 1 so the active plant’s biomass pools are rebuilt from the transplant starting condition. |
| 8. return | Exit the routine after transplant state, LAI potential, and biomass partitioning have been initialized. |

## Modules Used

<!-- facts:uses -->

| Module | State touched | Key components |
| --- | --- | --- |
| [sym:hru_module] | `hru, ihru, ipl` | `hru(j)%plant_cov` |
| [sym:plant_module] | `pcom` | `pcom(j)%plcur(ipl)%idplt, pcom(j)%plcur(ipl)%phuacc, pcom(j)%plcur(ipl)%phuacc_p, pcom(j)%plcur(ipl)%phumat, pcom(j)%plcur(ipl)%phumat_p, pcom(j)%plg(ipl)%laimxfr, pcom(j)%plg(ipl)%laimxfr_p, pcom(j)%plcur(ipl)%curyr_mat, pcom(j)%plm(ipl)%p_fr, pcom(j)%plm(ipl)%n_fr, pcom(j)%plcur(ipl)%lai_pot` |
| [sym:plant_data_module] | `transpl, plcp, pcomdb, pldb` | `transpl(itrans)%phuacc, transpl(itrans)%fr_yrmat, plcp(idp)%leaf2, transpl(itrans)%bioms, pcomdb(icom)%pl(ipl)%db_num, pldb(idp)%pltpfr1, pldb(idp)%pltpfr3, plcp(idp)%pup2, pldb(idp)%pltnfr1, pldb(idp)%pltnfr3, plcp(idp)%nup2, transpl(itrans)%pop, pldb(idp)%blai, plcp(idp)%popsc2` |
| [sym:organic_mineral_mass_module] | `pl_mass` | `pl_mass(j)%tot(ipl)%m, pl_mass(j)%tot(ipl)%n` |

## Local Variables

<!-- facts:locals -->

## State Changes

| Target | When | Meaning |
| --- | --- | --- |
| `pcom(j)%plcur(ipl)%phuacc` | Always, after the current HRU and plant slot are resolved. | Copies the transplant heat-unit fraction into the active plant status so the crop starts with the requested developmental stage. |
| `pcom(j)%plcur(ipl)%phuacc_p` | Always, after the current HRU and plant slot are resolved. | Stores the derived perennial heat-unit fraction for the active plant, based on the transplant record and maturity timing, so later perennial growth logic has the correct starting point. |
| `pcom(j)%plg(ipl)%laimxfr` | Always, after idp is resolved and species leaf parameters are available. | Sets the active plant’s transfer fraction for leaf area development using the species leaf-shape curve and the transplant heat-unit fraction. |
| `pcom(j)%plg(ipl)%laimxfr_p` | Always, after idp is resolved and species leaf parameters are available. | Stores the leaf-area transfer fraction evaluated at the perennial heat-unit state so the active plant has both current and prior transfer values. |
| `pl_mass(j)%tot(ipl)%m` | Always, when the transplant record supplies biomass. | Initializes the active plant’s total biomass pool to the transplant biomass so later partitioning routines can allocate roots, seed, and above-ground mass from the correct starting total. |
| `pcom(j)%plcur(ipl)%curyr_mat` | Always, after transplant maturity fraction and species maturity years are available. | Sets the current-year maturity counter from transplant timing so the active plant reflects how many years remain or are implied by the transplant stage. |
| `pcom(j)%plcur(ipl)%idplt` | Always, after the active community lookup is known. | Replaces the active plant database id with the plant id from the community database so the transplanted plant points to the correct plant definition. |
| `pcom(j)%plm(ipl)%p_fr` | Always, after the phosphorus uptake parameters are available. | Computes the active plant phosphorus fraction from species uptake parameters and transplant heat-unit state so biomass nutrient content matches the transplant stage. |
| `pl_mass(j)%tot(ipl)%n` | Always, after total biomass and nitrogen fraction are available. | Initializes total plant nitrogen mass as total biomass times the nitrogen fraction, providing the starting N pool for the transplanted plant. |
| `pcom(j)%plm(ipl)%n_fr` | Always, after the nitrogen uptake parameters are available. | Computes the active plant nitrogen fraction from species uptake parameters and transplant heat-unit state so biomass nitrogen content matches the transplant stage. |
| `pcom(j)%plcur(ipl)%lai_pot` | Always, after transplant population has been evaluated. | Stores the potential maximum LAI for the active plant based on transplant population and species blai, limiting canopy development immediately after transplanting. |

## File I/O

<!-- facts:io -->


## Lineage

`mgt_transplant.f90` was introduced in `df07e3f` (2024-03-05, "init all") and has been changed in 5 non-merge commit(s) since, most recently `bd18ad4` (2025-11-24, "Pr 107 (#108)"). Lineage is reconstructed from commit metadata (SHA, date, subject); per-line diffs were unavailable in this build environment, so only the commits touching `mgt_transplant.f90` are listed.

- `bd18ad4` (2025-11-24) — Pr 107 (#108)
- `e18817a` (2024-10-08) — Refactor and enhance various modules and subroutines
- `39fabde` (2024-08-08) — Initialized varables with python script, corrected input data where integers where floats in two input files, trapped underflow errors in th…
- `94b6dec` (2024-05-30) — Added latest source code from bitbucket
- `df07e3f` (2024-03-05) — init all

## Review Notes

- No direct file I/O was extracted for this procedure.
- warning: missing_doc: Procedure 'mgt_transplant' has no extracted documentation comment.
- algorithm_steps revised: reordered and expanded the steps to match the source flow and to use only real line citations from mgt_transplant.f90.
- Source-derived behavior is certain for the visible lines, but the external callees' detailed contracts come from completed overlay snippets rather than this source file.
- Lineage was reconstructed from file-level commit metadata; per-line diffs were unavailable in this environment (blobless clone), so line-span filtering was not applied.
