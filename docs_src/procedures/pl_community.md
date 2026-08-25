---
kind: procedure
symbol: pl_community
title: pl_community
status: filled
source_hash: db042a97c1df8cfb
version_label: SWAT+ 62.0.0
locals:
  j: Current HRU index copied from `ihru`; selects the active community and mass records for
    this call.
  idp: Plant database index for the current plant; used to point `pl_db` at `pldb(idp)` and
    read extinction coefficient.
  npl_gro: Count of plants in the community that are currently growing (`gro == 'y'`).
  ip: Remembers the single growing plant index when only one plant is active; reused in the
    one-plant light branch.
  jpl: Inner loop counter used while comparing plant canopy heights during light-competition
    calculations.
  x1: Temporary canopy-height and extinction-weight term used in the multi-plant light-competition
    math.
  sum: Accumulator for normalized transmissivity across plants in the competition branch.
  sumf: Accumulator for weighted canopy interception terms used to scale light competition.
  sumle: Accumulator for total leaf-area extinction loading across the community.
  fi: Community interception factor derived from `sumle`; used in the competition branch before
    being overwritten later.
  comp_light: Light-competition mode flag; set to `'n'` here, so the non-competition branch
    is taken in this source.
uses:
  hru_module: Provides the active HRU index, the potential evapotranspiration scale, and the
    per-plant arrays that this routine fills for water uptake and light partitioning.
  soil_module: Imported by the routine, but no candidate outside references were resolved
    to this module in the context packet.
  plant_module: Holds the plant-community structure and per-plant growth/status fields that
    this routine reads to total LAI, determine active plants, and compute canopy height and
    light competition.
  plant_data_module: Provides the plant database record and extinction coefficient used to
    compute PAR and light interception.
  organic_mineral_mass_module: Supplies the per-plant and community biomass records that are
    summed into community totals.
  time_module: Imported by the routine, but no candidate outside references were resolved
    to this module in the context packet.
  climate_module: Provides daily solar radiation used to compute PAR.
---

<!-- facts:header -->

Computes daily plant-community partitioning for the current HRU. It totals leaf area and biomass, estimates per-plant water uptake capacity, and assigns daily PAR and light-competition factors.

## Bottom Line

`pl_community` is the plant-community daily bookkeeping routine for the current HRU. It uses the active HRU index, plant community state, plant database parameters, weather radiation, and biomass state to update community-level leaf area, canopy height, potential water uptake, and photosynthetically active radiation for each plant.

It matters because later plant growth and water-stress calculations depend on the per-plant values it sets up here. The routine is called from `hru_control` after the HRU-level daily setup, and it delegates water uptake distribution to `pl_waterup` for each growing plant.

## Arguments

<!-- facts:arguments -->

## Where It Fits

Called once per HRU from `hru_control` during the daily HRU processing sequence, after septic biozone work and before later HRU-level outputs and plant-growth accounting. It prepares plant-community partitioning values that downstream plant and water routines use.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. Set HRU context and clear PAR | Copy the active HRU index from `ihru` into `j` and zero the `par` array before any plant-community calculations. |
| 2. Sum community LAI | Reset `pcom(j)%lai_sum` and accumulate leaf area index across all plants in the community. |
| 3. Compute plant water share | For each plant, compute `epmax(ipl)` as a share of `ep_max` proportional to that plant’s LAI, or set it to zero when total LAI is negligible. |
| 4. Sum community biomass | Initialize the community mass totals from `orgz` and add each plant’s total, above-ground, leaf, stem, seed, and root mass into the community aggregates. |
| 5. Find tallest canopy | Scan all plants and store the maximum canopy height in `pcom(j)%cht_mx` for later PET-related use. |
| 6. Count growing plants | Loop over plants, call `pl_waterup` for each plant marked growing, count how many are active, and remember the last active index in `ip`. |
| 7. Select light mode | Set the competition flag to `'n'` and branch into the non-competition light calculation path in this source. |
| 8. Compute PAR without competition | For each active, non-dormant plant, point `pl_db` at its database record and compute `par(ipl)` from solar radiation and the plant extinction coefficient. |
| 9. Handle light competition | If competition mode were enabled, compute PAR using either the single-plant branch or the multi-plant canopy-shadowing branch with transmissivity and height factors. |

## Modules Used

<!-- facts:uses -->

| Module | State touched | Key components |
| --- | --- | --- |
| [sym:hru_module] | `epmax, par, translt, htfac, ep_max, ihru, ipl` |  |
| [sym:plant_module] | `pcom` | `pcom(j)%lai_sum, pcom(j)%npl, pcom(j)%plg(ipl)%lai, pcom(j)%cht_mx, pcom(j)%plg(ipl)%cht, pcom(j)%plcur(ipl)%gro, pcom(j)%plcur(ipl)%idorm, pcom(j)%plcur(ipl)%idplt, pcom(j)%plcur(ip)%idorm, pcom(j)%plcur(ip)%gro, pcom(j)%plcur(ip)%idplt, pcom(j)%plg(ip)%lai, pcom(j)%plg(jpl)%cht` |
| [sym:plant_data_module] | `pldb, pl_db` | `pldb(idp)%ext_coef` |
| [sym:organic_mineral_mass_module] | `pl_mass, orgz` | `pl_mass(j)%tot_com, pl_mass(j)%ab_gr_com, pl_mass(j)%leaf_com, pl_mass(j)%stem_com, pl_mass(j)%seed_com, pl_mass(j)%root_com, pl_mass(j)%tot(ipl), pl_mass(j)%ab_gr(ipl), pl_mass(j)%leaf(ipl), pl_mass(j)%stem(ipl), pl_mass(j)%seed(ipl), pl_mass(j)%root(ipl)` |
| [sym:climate_module] | `w` | `w%solrad` |

## Local Variables

<!-- facts:locals -->

## State Changes

| Target | When | Meaning |
| --- | --- | --- |
| `par` | Always at routine start | Cleared to zero for all plants before new daily PAR values are assigned. |
| `pcom(j)%lai_sum` | After summing plant LAI | Updated to the total leaf area index of all plants in the active community. |
| `epmax(ipl)` | When total LAI is positive | Set to the plant’s share of `ep_max` in proportion to its LAI; otherwise set to zero. |
| `pl_mass(j)%tot_com` | After biomass accumulation | Set to the community total biomass by summing all plant totals. |
| `pl_mass(j)%ab_gr_com` | After biomass accumulation | Set to the community above-ground biomass by summing all plant above-ground masses. |
| `pl_mass(j)%leaf_com` | After biomass accumulation | Set to the community leaf mass by summing all plant leaf masses. |
| `pl_mass(j)%stem_com` | After biomass accumulation | Set to the community stem mass by summing all plant stem masses. |
| `pl_mass(j)%seed_com` | After biomass accumulation | Set to the community seed mass by summing all plant seed masses. |
| `pl_mass(j)%root_com` | After biomass accumulation | Set to the community root mass by summing all plant root masses. |
| `pcom(j)%cht_mx` | After canopy scan | Set to the tallest canopy height among the plants in the community. |
| `pl_db` | For each growing plant before water uptake | Pointer associated with the current plant database record so extinction coefficient and related plant parameters can be read. |
| `par(ipl)` | For each active plant in the non-competition branch | Set to daily PAR for that plant using solar radiation, extinction coefficient, and its LAI. |
| `par(ip)` | For the single-plant competition branch | Set to daily PAR for the one active plant when only one plant is growing. |
| `translt` | In the multi-plant competition branch | Temporary transmissivity factors are built, normalized, and used to derive competition weighting. |
| `translt(ipl)` | In the multi-plant competition branch | Holds each plant’s normalized transmissivity weight during the canopy-shadowing calculation. |
| `htfac(ipl)` | In the multi-plant competition branch | Holds the height-competition factor before PAR is computed; the source then overwrites it with `1.` before final PAR assignment. |

## File I/O

<!-- facts:io -->


## Lineage

`pl_community.f90` was introduced in `df07e3f` (2024-03-05, "init all") and has been changed in 4 non-merge commit(s) since, most recently `bd18ad4` (2025-11-24, "Pr 107 (#108)"). Lineage is reconstructed from commit metadata (SHA, date, subject); per-line diffs were unavailable in this build environment, so only the commits touching `pl_community.f90` are listed.

- `bd18ad4` (2025-11-24) — Pr 107 (#108)
- `39fabde` (2024-08-08) — Initialized varables with python script, corrected input data where integers where floats in two input files, trapped underflow errors in th…
- `94b6dec` (2024-05-30) — Added latest source code from bitbucket
- `df07e3f` (2024-03-05) — init all

## Review Notes

- No direct file I/O was extracted for this procedure.
- warning: missing_doc: Procedure 'pl_community' has no extracted documentation comment.
- Lineage was reconstructed from file-level commit metadata; per-line diffs were unavailable in this environment (blobless clone), so line-span filtering was not applied.
