---
kind: procedure
symbol: pl_root_gro
title: pl_root_gro
status: filled
source_hash: 472dc42ca603e5df
version_label: SWAT+ 62.0.0
args:
  j: '`j` selects the HRU/plant-community entry to update; the routine reads `pcom(j)` and
    `soil(j)` and writes the resulting root depth and root fraction back into that same HRU’s
    active plant record.'
locals:
  idp: '`idp` is the plant database index for the active plant in HRU `j`; it is assigned
    from `pcom(j)%plcur(ipl)%idplt` and used to look up plant type, maximum root depth, maturity
    years, and root-to-shoot ratios in `pldb`.'
  rto: '`rto` stores the current-year-to-maturity ratio for perennial plants, computed as
    `curyr_mat / mat_yrs`, so the routine can linearly transition root fraction from `rsr1`
    to `rsr2` during early perennial growth.'
  phumax: '`phumax` holds the capped annual PHU accumulation used for root-fraction calculation,
    with `amin1(1., phuacc)` limiting the decline in root fraction to the first full unit
    of PHU progress.'
uses:
  plant_data_module: '`plant_data_module` provides the species parameters that drive both
    root depth and root mass logic: plant category (`typ`) decides annual versus perennial
    handling, `rdmx` scales potential root depth, `mat_yrs` controls perennial maturity progress,
    and `rsr1`/`rsr2` define the starting and ending root-to-shoot ratios.'
  basin_module: '`basin_module` matters because this routine is called within basin-level
    plant handling, and the plant-community state it updates must stay consistent with the
    basin’s active plant configuration for the current HRU.'
  hru_module: '`hru_module` supplies `ipl`, the active plant index within the HRU, so the
    routine updates the correct plant slot in `pcom(j)` rather than an unrelated community
    member.'
  plant_module: '`plant_module` holds the per-plant status and growth arrays that this routine
    reads and updates: it needs the current plant ID, PHU progress, maturity year, and the
    growth outputs `root_dep` and `root_frac` for the active community member.'
  carbon_module: '`carbon_module` is imported because root-growth routines in the plant system
    are part of biomass and carbon accounting, so the module is available even though this
    subroutine does not directly reference a carbon symbol in the shown lines.'
  organic_mineral_mass_module: '`organic_mineral_mass_module` is relevant because the resulting
    root fraction feeds later residue and soil-organic matter handling, even though no symbol
    from that module is directly used in the extracted body of this routine.'
  soil_module: '`soil_module` provides `soil(j)%zmx`, the soil-profile rooting-depth cap.
    The routine uses it to prevent plant root depth from extending below the soil’s maximum
    rooting zone.'
---

<!-- facts:header -->

Updates a plant’s rooting depth and root-to-shoot allocation for one HRU/plant slot.

## Bottom Line

`pl_root_gro` computes the current rooting depth and root mass fraction for the active plant in HRU `j`, using plant database parameters, the plant’s accumulated heat-unit progress, and the soil profile’s maximum rooting depth. It then calls `pl_rootfr` to redistribute the resulting root depth through the soil layers.

The routine treats annuals and perennials differently: annuals use accumulated PHU to grow roots and set root fraction, while perennials use year-to-maturity progress to move from `rsr1` toward `rsr2`. The results feed later root distribution, biomass partitioning, and plant growth initialization steps.

## Arguments

<!-- facts:arguments -->

## Where It Fits

`pl_root_gro` runs whenever the model needs to refresh a plant’s root state: after transplant initialization, during active plant growth, and during plant initialization when a plant is growing. Its inputs are prepared by the caller through `pcom(j)%plcur(ipl)` and the plant database entry for the current crop, and its outputs are then used by `pl_rootfr` and later growth/partitioning routines that depend on current root depth and root fraction.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. determine plant type | Fetch the active plant database index from `pcom(j)%plcur(ipl)%idplt`, then test whether the plant is one of the annual/tuber annual categories. This decides whether root depth should follow annual PHU progress or perennial PHU progress. |
| 2. compute annual root depth | For warm/cold annuals and annual tubers, compute rooting depth from current annual PHU accumulation times `2.5 * 1000 * rdmx`, giving a depth that grows with seasonal development. |
| 3. compute perennial root depth | For all other plant types, compute rooting depth from perennial PHU accumulation instead of annual PHU accumulation, using the same `2.5 * 1000 * rdmx` scaling. |
| 4. cap and floor root depth | Limit the calculated root depth so it cannot exceed the soil profile maximum rooting depth `soil(j)%zmx`, and force a minimum rooting depth of 25.4 mm. |
| 5. branch on perennial plants | If the plant database type is perennial, compute the root-to-shoot fraction using year-to-maturity progression; otherwise use the annual root-fraction rule. |
| 6. check maturity years | When a perennial has a positive maturity period, compute the fraction of maturity already reached as `curyr_mat / mat_yrs`. |
| 7. transition root fraction early | If the maturity ratio is below 0.2, linearly reduce root fraction from `rsr1` toward `rsr2` based on the fraction of the 20% maturity window completed. |
| 8. hold final perennial fraction | Once the perennial reaches 20% of its maturity period, set root fraction directly to the mature value `rsr2`. |
| 9. handle zero maturity years | If a perennial has no valid maturity-year value, fall back to the mature root-to-shoot ratio `rsr2` immediately. |
| 10. compute annual root fraction | For annuals, cap accumulated PHU at 1.0 with `amin1`, then linearly decline root fraction from `rsr1` to `rsr2` as PHU advances. |
| 11. distribute roots by layer | Call `pl_rootfr(j)` so the updated root depth is converted into a soil-layer root-fraction profile for the active plant. |
| 12. return | Exit after updating root depth, root mass fraction, and layer distribution for the active HRU plant. |

## Modules Used

<!-- facts:uses -->

| Module | State touched | Key components |
| --- | --- | --- |
| [sym:plant_data_module] | `pldb` | `pldb(idp)%typ, pldb(idp)%rdmx, pldb(idp)%mat_yrs, pldb(idp)%rsr1, pldb(idp)%rsr2` |
| [sym:basin_module] | `pcom` | `pcom(j), pcom(j)%plcur(ipl)%idplt, pcom(j)%plg(ipl)%root_dep, pcom(j)%plcur(ipl)%phuacc, pcom(j)%plcur(ipl)%phuacc_p, pcom(j)%plcur(ipl)%curyr_mat, pcom(j)%plg(ipl)%root_frac` |
| [sym:hru_module] | `ipl` |  |
| [sym:plant_module] | `pcom` | `pcom(j)%plcur(ipl)%idplt, pcom(j)%plg(ipl)%root_dep, pcom(j)%plcur(ipl)%phuacc, pcom(j)%plcur(ipl)%phuacc_p, pcom(j)%plcur(ipl)%curyr_mat, pcom(j)%plg(ipl)%root_frac` |
| [sym:carbon_module] | `carbon and organic_mineral_mass state are imported but not directly referenced in the extracted source span` |  |
| [sym:organic_mineral_mass_module] | `organic_mineral_mass state are imported but not directly referenced in the extracted source span` |  |
| [sym:soil_module] | `soil` | `soil(j)%zmx` |

## Local Variables

<!-- facts:locals -->

## State Changes

| Target | When | Meaning |
| --- | --- | --- |
| `pldb(idp)%typ` | When the active plant is an annual or perennial type selected by `pldb(idp)%typ`, `idp` is resolved from `pcom(j)%plcur(ipl)%idplt` at entry. | `pldb(idp)%typ` itself is not modified here; it is read as the plant-category switch that determines which root-growth formulas the routine applies. |
| `pcom(j)%plg(ipl)%root_dep` | Whenever the computed root depth exceeds the soil profile maximum or falls below the minimum rooting floor. | `pcom(j)%plg(ipl)%root_dep` is overwritten with a bounded rooting depth so the plant cannot root deeper than `soil(j)%zmx` or shallower than 25.4 mm. |
| `pcom(j)%plg(ipl)%root_frac` | After the annual/perennial branch computes the current root-to-shoot ratio from PHU or maturity progress. | `pcom(j)%plg(ipl)%root_frac` is updated to the plant’s current root fraction of total biomass so later partitioning and root-related processes use the current growth stage. |

## File I/O

<!-- facts:io -->


## Theory Equations

| Eq. | Title | Formula | Implementation |
| --- | --- | --- | --- |
| 5:2.1.21 | Root biomass fraction | $fr_{root}=0.40-0.20*fr_{PHU}$ | Annuals use root_frac = rsr1 - (rsr1-rsr2)*min(1, phuacc), a crop-parameterized linear decline rather than the fixed 0.40 - 0.20*frPHU relation. |
| 5:2.1.22 | Maximum root depth | $z_{root}=z_{root,mx}$ | Verified against SWAT+ 62.0.0 (pl_root_gro.f90:27). if (root_dep > zmx) root_dep = zmx |
| 5:2.1.23 | Root depth before 40% PHU | $z_{root}=2.5*fr_{PHU}*z_{root,mx}$ | Verified against SWAT+ 62.0.0 (pl_root_gro.f90:23). fr_PHU≤0.40: `root_dep = 2.5*phuacc*1000*rdmx |
| 5:2.1.24 | Root depth after 40% PHU | $z_{root}=z_{root,mx}$ | Verified against SWAT+ 62.0.0 (pl_root_gro.f90:23). fr_PHU>0.40: theory caps at rdmx; code keeps growing to 2.5·rdmx, bounded only by soil depth zmx (:27) |

## Lineage

`pl_root_gro.f90` was introduced in `df07e3f` (2024-03-05, "init all") and has been changed in 7 non-merge commit(s) since, most recently `c3a99cb` (2026-05-15, "Updated code to include root_mass in hru_cpool output and in jupyter notebook co…"). Lineage is reconstructed from commit metadata (SHA, date, subject); per-line diffs were unavailable in this build environment, so only the commits touching `pl_root_gro.f90` are listed.

- `c3a99cb` (2026-05-15) — Updated code to include root_mass in hru_cpool output and in jupyter notebook code. Removed hru_rsdc graphs from jupyter notebook.
- `3e18acf` (2026-02-17) — Integrate CENTURY residue/N updates and root-fraction tracking changes
- `2ee1889` (2025-11-17) — Cleanup of sine warnings.
- `e18817a` (2024-10-08) — Refactor and enhance various modules and subroutines
- `39fabde` (2024-08-08) — Initialized varables with python script, corrected input data where integers where floats in two input files, trapped underflow errors in th…
- `df07e3f` (2024-03-05) — init all

## Review Notes

- No direct file I/O was extracted for this procedure.
- warning: missing_doc: Procedure 'pl_root_gro' has no extracted documentation comment.
- algorithm_steps revised: condensed the branch structure into 12 concrete steps and kept each step anchored to visible source lines.
- Source context shows `carbon_module` and `organic_mineral_mass_module` are imported but not referenced by any symbol in the extracted body; their role here is inferred only from surrounding plant-growth architecture.
- Lineage was reconstructed from file-level commit metadata; per-line diffs were unavailable in this environment (blobless clone), so line-span filtering was not applied.
