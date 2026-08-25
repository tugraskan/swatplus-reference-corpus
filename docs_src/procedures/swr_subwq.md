---
kind: procedure
symbol: swr_subwq
title: swr_subwq
status: filled
source_hash: ee4decf9959eb858
version_label: SWAT+ 62.0.0
uses:
  hru_module: Provides the runoff and sediment context used to compute HRU water-quality loadings
    and receives the resulting chl-a, CBOD, and dissolved-oxygen concentrations.
  organic_mineral_mass_module: Supplies the first-layer carbon percentage used to estimate
    organic carbon loading in runoff.
  climate_module: Supplies air temperature for the runoff-water temperature and dissolved-oxygen
    saturation estimate.
---

<!-- facts:header -->

swr_subwq computes HRU runoff loadings of chlorophyll-a, CBOD, and dissolved oxygen delivered to the main channel.

## Bottom Line

swr_subwq computes the HRU runoff-loading side of the Chapter 4 CBOD and Dissolved Oxygen pages by deriving chlorophyll-a, carbonaceous biological oxygen demand, and dissolved oxygen concentrations from runoff, sediment, nitrate, and organic carbon context.

It does not perform in-channel transformation; that channel-state half is implemented separately in ch_watqual4.

## Arguments

<!-- facts:arguments -->

## Where It Fits

hru_control calls swr_subwq immediately after total water yield qdr(j) is assembled and before constituent concentrations are converted for channel delivery, so it is the HRU runoff-loading kernel for these water-quality terms.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| Compute runoff water temperature | Builds runoff water temperature from mean air temperature and converts it to Kelvin for dissolved-oxygen saturation. |
| Estimate chlorophyll-a loading concentration | When water yield exists, computes tp from sediment organic nitrogen and runoff nitrate, then estimates chlorophyll-a as 0.1 times tp. |
| Compute runoff CBOD concentration | Estimates runoff organic carbon from first-layer soil carbon, enrichment ratio, and sediment yield, then converts it to CBOD concentration using the empirical factor 2.7. |
| Compute runoff dissolved oxygen concentration | Computes dissolved-oxygen saturation from runoff water temperature and then attenuates it exponentially using CBOD to derive doxq(j). |

## Modules Used

<!-- facts:uses -->

| Module | State touched | Key components |
| --- | --- | --- |
| [sym:hru_module] | `hru; ihru; qdr; sedorgn; surqno3; cbodu; doxq; chl_a; sedyld; enratio` | `HRU runoff yield, nutrient and sediment context, and water-quality loading outputs` |
| [sym:organic_mineral_mass_module] | `soil1` | `cbn(1)` |
| [sym:climate_module] | `w` | `tave` |

## Local Variables

<!-- facts:locals -->

## State Changes

| Target | When | Meaning |
| --- | --- | --- |
| `chl_a(j); cbodu(j); doxq(j)` | When qdr(j) > 1.e-4 | Stores the HRU runoff loading concentrations for chlorophyll-a, carbonaceous biological oxygen demand, and dissolved oxygen. |
| `chl_a(j); cbodu(j); doxq(j)` | When qdr(j) <= 1.e-4 | Zeros the HRU runoff water-quality loading concentrations when no meaningful water yield reaches the main channel. |

## File I/O

<!-- facts:io -->


## Theory Equations

| Eq. | Title | Formula | Implementation |
| --- | --- | --- | --- |
|  |  |  |  |
|  |  |  |  |
| 4:5.2.1 |  | $cbod_{surq}=\frac{2.7*orgC_{surq}}{Q_{surf}*area_{hru}}$ | Verified against SWAT+ 62.0.0 (swr_subwq.f90:91). cbodu = 2.7*org_c/(qdr*km)/10000.` — CBOD |
| 4:5.2.2 |  | $orgC_{surq}=1000*\frac{orgC_{surf}}{100}*sed*\varepsilon_{C:sed}$ | Verified against SWAT+ 62.0.0 (swr_subwq.f90:78). org_c = (cbn(1)/100.)*enratio*sedyld*1000.` (ε_C:sed = enratio) |
| 4:5.3.1 |  | $Ox_{surf}=Ox_{sat}-\kappa_1*cbod_{surq}*\frac{t_{ov}}{24}$ | Verified against SWAT+ 62.0.0 (swr_subwq.f90:103). doxq = soxy*exp(-0.1*cbodu)` — exponential DO depletion vs theory's linear `Ox_sat−κ1·cbod·t_ov/24 |

## Lineage

`swr_subwq.f90` was introduced in `df07e3f` (2024-03-05, "init all") and has been changed in 9 non-merge commit(s) since, most recently `dfce092` (2026-06-02, "move carbon activation to cswat = 2, reserve 1 for C-FARM"). Lineage is reconstructed from commit metadata (SHA, date, subject); per-line diffs were unavailable in this build environment, so only the commits touching `swr_subwq.f90` are listed.

- `dfce092` (2026-06-02) — move carbon activation to cswat = 2, reserve 1 for C-FARM
- `3389f29` (2026-04-22) — Numerous changes to account for the removal of the old cswat ==1 and moving cswat == 3 to cswat =1. Also some code formatting changes to get…
- `cb5de88` (2026-02-25) — changes made to run a cswat == 3 option and added a new subroutine named mgt_newtill_mix_3.f90
- `23142ed` (2025-10-29) — Water allocation now has explicit structured output objects and headers, with per-transfer (daily/monthly/yearly/avg) accumulators and CSV w…
- `889136d` (2025-02-03) — Fix typos
- `df07e3f` (2024-03-05) — init all

## Review Notes

- The routine also computes chlorophyll-a runoff loading, but the strongest Chapter 4 algae mapping remains ch_watqual4 because that page aligns with the QUAL2E in-channel algae equations rather than this loading approximation.
- The CBOD and dissolved-oxygen calculations here are empirical HRU loading estimates, not channel reaction equations.
- Lineage was reconstructed from file-level commit metadata; per-line diffs were unavailable in this environment (blobless clone), so line-span filtering was not applied.
- Equation GitBook links were resolved from `docs/equation_inventory/gitbook_theoretical_equations.csv` by equation id. These entries were left unlinked because the lookup was not unambiguous and guessing a theory page would be worse than leaving it blank: entry 0 carries no theory equation id, so there is nothing to look up; entry 1 carries no theory equation id, so there is nothing to look up.
