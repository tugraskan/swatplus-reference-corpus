---
kind: procedure
symbol: plantparm_init
title: plantparm_init
status: filled
source_hash: 91d6f45fb55179c6
version_label: SWAT+ 62.0.0
locals:
  ic: '`ic` is the loop counter that steps through each plant record from `1` to `db_mx%plantparm`.'
  c1: '`c1` holds the ambient CO2 reference value used as the first x-point when fitting the
    radiation-use-efficiency curve.'
  b1: '`b1` is a scratch value used as the first y-point for each curve fit, and later reused
    as a normalized fraction-difference term for nitrogen and phosphorus uptake fits.'
  b2: '`b2` is a scratch value used as the second y-point for curve fitting, and later reused
    as the second normalized uptake fit point for nitrogen and phosphorus.'
  b3: '`b3` is a scratch value used as the near-endpoint y-point for the nitrogen and phosphorus
    uptake curve fits.'
uses:
  basin_module: '`bsn_prm%rsdco` supplies the basin-level residue decomposition coefficient
    that becomes the plant residue default when a plant record has no plant-specific value,
    so basin configuration directly seeds plant parameter initialization.'
  maximum_data_module: '`db_mx%plantparm` gives the number of plant records to initialize,
    so this maximum-data state controls the loop bounds and determines how many `pldb` and
    `plcp` entries are processed.'
  plant_data_module: '`pldb` holds the raw plant database values that are checked, clamped,
    and converted into curve inputs, while `plcp` stores the derived coefficients that downstream
    growth and uptake routines read instead of recomputing them.'
---

<!-- facts:header -->

Initializes plant database entries by filling missing defaults and computing derived curve parameters for each plant record.

## Bottom Line

`plantparm_init` walks every plant entry in `pldb` and makes sure the plant database has usable values before the rest of the model uses it. It fills in defaults for missing or invalid inputs, adjusts a few out-of-range parameters, and then derives the curve-shape coefficients stored in `plcp`.

The routine matters because later plant-growth, biomass, nutrient-uptake, and stomatal-response behavior depends on the precomputed parameters it writes. `proc_db` calls it right after the plant parameter database is read, so the rest of the spatial-model setup sees normalized plant data rather than raw file values.

## Arguments

<!-- facts:arguments -->

## Where It Fits

`plantparm_init` runs during database setup after `plant_parm_read` has loaded the plant parameter table and before later database readers finish the broader initialization sequence. Its outputs are then used by plant-growth and uptake behavior throughout the model because the routine precomputes the shape parameters and corrected defaults those routines expect.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. Loop over every plant database record. | Iterate from `ic = 1` to `db_mx%plantparm` so each plant entry can be checked and initialized. |
| 2. Fill missing scalar defaults and clamp invalid values. | Set fallback values for biomass dieoff, light extinction, residue coefficients, USLE C, LAI limits, root-to-shoot ratios, aeration, and residue cover factors when the database values are missing or out of bounds. |
| 3. Apply plant-type-specific overrides. | Force tuber crops to have `rsr2 = 0.7`, and reduce harvest index to `0.02` when the stored harvest index is greater than `0.7`. |
| 4. Process only non-water plants with nonzero biomass-energy data. | Skip the derived-parameter work unless the plant has positive biomass-energy and is not the `WATR` land cover. |
| 5. Derive population-to-LAI curve coefficients when population anchors exist. | If `pop1 + pop2` is nontrivial, rescale the population inputs by `1001.`, then call `ascrv` with the population and LAI anchor points to populate `plcp(ic)%popsc1` and `plcp(ic)%popsc2`. |
| 6. Derive leaf-area development curve coefficients. | Call `ascrv` with the growth-fraction and maximum-LAI anchor points to compute `plcp(ic)%leaf1` and `plcp(ic)%leaf2`. |
| 7. Prepare the CO2 and biomass-energy points for radiation-use efficiency fitting. | Set ambient CO2 to `330.`, replace a `co2hi` value of `330.` with `660.`, and convert `bio_e` and `bioehi` to fraction form by multiplying by `.01`. |
| 8. Derive radiation-use efficiency curve coefficients. | Call `ascrv` with the ambient and elevated CO2 reference points to populate `plcp(ic)%ruc1` and `plcp(ic)%ruc2`. |
| 9. Store the log-transformed USLE C value for later use. | Compute `plcp(ic)%cvm` as `Log(pldb(ic)%usle_c)`. |
| 10. Repair nitrogen uptake anchors and derive nitrogen coefficients. | Ensure the nitrogen fraction anchors are separated, normalize them into `b1`, `b2`, and `b3`, then call `ascrv` to compute `plcp(ic)%nup1` and `plcp(ic)%nup2`. |
| 11. Repair phosphorus uptake anchors and derive phosphorus coefficients. | Apply the same separation and normalization logic to phosphorus fractions, then call `ascrv` to compute `plcp(ic)%pup1` and `plcp(ic)%pup2`. |
| 12. Compute the stomatal conductance slope parameter. | Set `plcp(ic)%vpd2` from `gmaxfr` and `vpdfr` using the slope formula `(1. - gmaxfr) / (vpdfr - 1.)`. |

## Modules Used

<!-- facts:uses -->

| Module | State touched | Key components |
| --- | --- | --- |
| [sym:basin_module] | `bsn_prm` | `bsn_prm%rsdco` |
| [sym:maximum_data_module] | `db_mx` | `db_mx%plantparm` |
| [sym:plant_data_module] | `pldb, plcp` | `pldb(ic)%bm_dieoff, pldb(ic)%ext_coef, pldb(ic)%rsdco_pl, pldb(ic)%usle_c, pldb(ic)%blai, pldb(ic)%rsr1, pldb(ic)%rsr2, pldb(ic)%aeration, pldb(ic)%rsd_pctcov, pldb(ic)%rsd_covfac, pldb(ic)%typ, pldb(ic)%hvsti, pldb(ic)%bio_e, pldb(ic)%plantnm, pldb(ic)%pop1, pldb(ic)%pop2, pldb(ic)%frlai2, plcp(ic)%popsc1, plcp(ic)%popsc2, pldb(ic)%laimx2, pldb(ic)%frgrw1, pldb(ic)%frgrw2, plcp(ic)%leaf1, plcp(ic)%leaf2, pldb(ic)%co2hi, pldb(ic)%bioehi, plcp(ic)%ruc1, plcp(ic)%ruc2, plcp(ic)%cvm, pldb(ic)%pltnfr1, pldb(ic)%pltnfr2, pldb(ic)%pltnfr3, plcp(ic)%nup2, pldb(ic)%pltpfr1, pldb(ic)%pltpfr2, pldb(ic)%pltpfr3, plcp(ic)%pup2, plcp(ic)%vpd2, pldb(ic)%gmaxfr, pldb(ic)%vpdfr` |

## Local Variables

<!-- facts:locals -->

## State Changes

| Target | When | Meaning |
| --- | --- | --- |
| `pldb(ic)%rsr2` | When `pldb(ic)%rsr2 <= 0.0`, and also when the record is a `warm_annual_tuber` or `cold_annual_tuber`. | `pldb(ic)%rsr2` is given a default root-to-shoot ratio of `0.2` if it was missing or nonpositive, but tuber crops override that with `0.7` because the routine explicitly sets a tuber-specific ratio. |
| `pldb(ic)%pop1` | When `pldb(ic)%bio_e > 0.` and `pldb(ic)%plantnm /= "WATR"`, and `pldb(ic)%pop1 + pldb(ic)%pop2 > 1.e-6`. | `pldb(ic)%pop1` is rescaled from the raw database units by dividing by `1001.` before the population-vs-LAI curve is fit, so the anchor point becomes compatible with the `ascrv` inputs. |
| `pldb(ic)%pop2` | When `pldb(ic)%bio_e > 0.` and `pldb(ic)%plantnm /= "WATR"`, and `pldb(ic)%pop1 + pldb(ic)%pop2 > 1.e-6`. | `pldb(ic)%pop2` is rescaled the same way as `pop1` before the curve fit, so both population anchors are converted to the normalized values expected by `ascrv`. |
| `plcp(ic)%cvm` | When `pldb(ic)%bio_e > 0.` and `pldb(ic)%plantnm /= "WATR"`. | `plcp(ic)%cvm` is set to the logarithm of `pldb(ic)%usle_c`, creating the coefficient used later by canopy-related calculations that depend on the plant's erosion cover response. |
| `pldb(ic)%pltnfr2` | When `pldb(ic)%bio_e > 0.` and `pldb(ic)%plantnm /= "WATR"`, after ensuring `pltnfr1` and `pltnfr2` are sufficiently separated. | `pldb(ic)%pltnfr2` is reduced slightly if it is too close to `pltnfr1`, so the nitrogen uptake fit has a valid spread between the first two anchor fractions. |
| `pldb(ic)%pltnfr3` | When `pldb(ic)%bio_e > 0.` and `pldb(ic)%plantnm /= "WATR"`, after ensuring `pltnfr2` and `pltnfr3` are sufficiently separated. | `pldb(ic)%pltnfr3` is reduced to `0.75 * pldb(ic)%pltnfr3` if the second and third nitrogen anchors are too close, which repairs bad input before the uptake curve is solved. |
| `pldb(ic)%pltpfr2` | When `pldb(ic)%bio_e > 0.` and `pldb(ic)%plantnm /= "WATR"`, after ensuring `pltpfr1` and `pltpfr2` are sufficiently separated. | `pldb(ic)%pltpfr2` is nudged downward by `0.0001` from `pltpfr1` if needed so the phosphorus uptake fit has distinct anchor values. |
| `pldb(ic)%pltpfr3` | When `pldb(ic)%bio_e > 0.` and `pldb(ic)%plantnm /= "WATR"`, after ensuring `pltpfr2` and `pltpfr3` are sufficiently separated. | `pldb(ic)%pltpfr3` is reduced to `0.75 * pldb(ic)%pltpfr3` if the phosphorus anchors are too close, repairing the input before the curve fit. |
| `plcp(ic)%vpd2` | When `pldb(ic)%bio_e > 0.` and `pldb(ic)%plantnm /= "WATR"`. | `plcp(ic)%vpd2` is computed from `gmaxfr` and `vpdfr` so the stomatal conductance response has the slope parameter needed by later growth calculations. |

## File I/O

<!-- facts:io -->


## Theory Equations

| Eq. | Title | Formula | Implementation |
| --- | --- | --- | --- |
| 5:2.1.5 | CO2 response parameter r1 | $r1=1n[\frac{CO_{2amb}}{(0.01*RUE_{amb})}-CO_{2amb}]+r_2*CO_{2amb}$ | Verified against SWAT+ 62.0.0 (plantparm_init.f90:62). r1 = `ruc1` from `ascrv` S-curve fit of the two (CO2,RUE) points |
| 5:2.1.6 | CO2 response parameter r2 | $r_2=\frac{(1n[\frac{CO_{2amb}}{(0.01*RUE_{amb})}-CO_{2amb}]-1n[\frac{CO_{2hi}}{(0.01*RUE_{hi})}-CO_{2hi}])}{CO_{2hi}-CO_{2amb}}$ | Verified against SWAT+ 62.0.0 (plantparm_init.f90:62). r2 = `ruc2` from same `ascrv` fit |
| 5:2.1.12 | Leaf-area curve parameter 1 | $\Box_1=1n[\frac{fr_{PHU,1}}{fr_{LAI,1}}-fr_{PHU,1}]+\Box_2*fr_{PHU,1}$ | Verified against SWAT+ 62.0.0 (plantparm_init.f90:46). LAI shape params via `ascrv(frlai1,frlai2,...) |
| 5:2.1.13 | Leaf-area curve parameter 2 | $\Box_2=\frac{(1n[\frac{fr_{PHU,1}}{fr_{LAI,1}}-fr_{PHU,1}]-1n[\frac{fr_{PHU,2}}{fr_{LAI,2}}-fr_{PHU,2}])}{fr_{PHU,2}-fr_{PHU,1}}$ | Verified against SWAT+ 62.0.0 (plantparm_init.f90:50). ascrv(laimx1,laimx2,frgrw1,...) |
| 5:2.3.2 | Nitrogen uptake curve parameter 1 | $n_1=1n[\frac{fr_{PHU,50\%}}{(1-\frac{(fr_{N,2}-fr_{N,3})}{(fr_{N,1}-fr_{N,3})})}-fr_{PHU,50\%}]+n_2*fr_{PHU,50\%}$ | Verified against SWAT+ 62.0.0 (plantparm_init.f90:76). n1 shape param from `ascrv(b2,b3,0.5,1.,nup1,nup2) |
| 5:2.3.3 | Nitrogen uptake curve parameter 2 | $n_2=\frac{(1n[\frac{fr_{PHU,50\%}}{(1-\frac{(fr_{N,2}-fr_{N,3})}{(fr_{N,1}-fr_{N,3})})}-fr_{PHU,50\%}]-1n[\frac{fr_{PHU,100\%}}{(1-\frac{(fr_{N,\sim3}-fr_{N,3})}{(fr_{N,1}-fr_{N,3})})}-fr_{PHU,100\%}])}{fr_{PHU,100\%}-fr_{PHU,50\%}}$ | Verified against SWAT+ 62.0.0 (plantparm_init.f90:76). n2 shape param (same ascrv call) |
| 5:2.3.20 | Phosphorus uptake curve parameter 1 | $p_1=1n[\frac{fr_{PHU,50\%}}{(1-\frac{(fr_{P,2}-fr_{P,3})}{fr_{P,1}-fr_{P,3})})}-fr_{PHU,50\%}]+p_2*fr_{PHU,50\%}$ | Verified against SWAT+ 62.0.0 (plantparm_init.f90:88). p1 shape param from `ascrv(...,pup1,pup2) |
| 5:2.3.21 | Phosphorus uptake curve parameter 2 | $p_2=\frac{(1n[\frac{fr_{PHU,50\%}}{(1-\frac{(fr_{P,2}-fr_{P,3})}{(fr_{P,1}-fr_{P,3})})}-fr_{PHU,50\%}]-1n[\frac{fr_{PHU,100\%}}{(1-\frac{(fr_{P,\sim3}-fr_{P,3})}{(fr_{P,1}-fr_{P,3})})}-fr_{PHU,100\%}])}{fr_{PHU,100\%}-fr_{PHU,50\%}}$ | Verified against SWAT+ 62.0.0 (plantparm_init.f90:88). p2 shape param (same ascrv call) |
| 4:1.1.11 | Cover and management factor C_USLE | $C_{USLE,mn}=1.463ln[C_{USLE,aa}]+0.1034$ | Verified against SWAT+ 62.0.0 (plantparm_init.f90:64). code sets `cvm = Log(usle_c)` directly; theory's `1.463·ln(C_aa)+0.1034` min-C conversion NOT applied |

## Lineage

`plantparm_init.f90` was introduced in `df07e3f` (2024-03-05, "init all") and has been changed in 5 non-merge commit(s) since, most recently `bd18ad4` (2025-11-24, "Pr 107 (#108)"). Lineage is reconstructed from commit metadata (SHA, date, subject); per-line diffs were unavailable in this build environment, so only the commits touching `plantparm_init.f90` are listed.

- `bd18ad4` (2025-11-24) — Pr 107 (#108)
- `f1e61a3` (2024-10-08) — fixed tabs
- `39fabde` (2024-08-08) — Initialized varables with python script, corrected input data where integers where floats in two input files, trapped underflow errors in th…
- `94b6dec` (2024-05-30) — Added latest source code from bitbucket
- `df07e3f` (2024-03-05) — init all

## Review Notes

- No direct file I/O was extracted for this procedure.
- warning: missing_doc: Procedure 'plantparm_init' has no extracted documentation comment.
- Lineage was reconstructed from file-level commit metadata; per-line diffs were unavailable in this environment (blobless clone), so line-span filtering was not applied.
