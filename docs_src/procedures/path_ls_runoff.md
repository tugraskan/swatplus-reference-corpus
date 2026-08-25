---
kind: procedure
symbol: path_ls_runoff
title: path_ls_runoff
status: filled
source_hash: 0152a14abbeda49e
version_label: SWAT+ 62.0.0
uses:
  output_ls_pathogen_module: Receives the daily soluble runoff pathogen load and sediment-attached
    pathogen load for each pathogen.
  constituent_mass_module: Stores the first-layer pathogen mass and is reduced by the exported
    soluble and sediment-attached pathogen loads.
---

<!-- facts:header -->

path_ls_runoff computes soluble pathogen transport in surface runoff and pathogen transport attached to sediment from the first soil layer.

## Bottom Line

path_ls_runoff is the direct implementation target for the Chapter 4 Bacteria in Surface Runoff and Bacteria Attached to Sediment in Surface Runoff pages because it computes both soluble runoff transport and sediment-attached pathogen export in one routine.

The routine removes the exported pathogen mass from the first-layer soil pathogen store after each pathway calculation.

## Arguments

<!-- facts:arguments -->

## Where It Fits

hru_control calls path_ls_swrouting, then path_ls_runoff, then path_ls_process inside the pathogen-transport block, so this routine is the main HRU runoff/export step for landscape pathogen loss.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| Compute soluble pathogen transport in surface runoff | Computes hpath_bal(j)%path(ipath)%surq from first-layer pathogen mass, runoff qday, soil bulk density, layer depth, and pathogen kd, then subtracts that mass from the soil store. |
| Compute pathogen transported with sediment | When enratio > 0, computes sediment-attached pathogen concentration cpath and converts it to hpath_bal(j)%path(ipath)%sed using sediment yield and HRU area, then subtracts that mass from the soil store. |

## Modules Used

<!-- facts:uses -->

| Module | State touched | Key components |
| --- | --- | --- |
| [sym:output_ls_pathogen_module] | `hpath_bal` | `surq, sed` |
| [sym:constituent_mass_module] | `cs_soil` | `ly(1)%path(:)` |

## Local Variables

<!-- facts:locals -->

## State Changes

| Target | When | Meaning |
| --- | --- | --- |
| `hpath_bal(j)%path(ipath)%surq; hpath_bal(j)%path(ipath)%sed` | Every pathogen-routing call | Stores the soluble and sediment-attached pathogen loads exported from the HRU. |
| `cs_soil(j)%ly(1)%path(ipath)` | Every pathogen-routing call | Reduces the first-layer pathogen store by the soluble and sediment-attached exports. |

## File I/O

<!-- facts:io -->


## Theory Equations

| Eq. | Title | Formula | Implementation |
| --- | --- | --- | --- |
|  |  |  |  |
|  |  |  |  |
| 4:4.2.1 |  | $bact_{lp,sed}=0.0001*conc_{sedlpbact}*\frac{sed}{area_{hru}}*\varepsilon_{bact:sed}$ | Verified against SWAT+ 62.0.0 (path_ls_runoff.f90:35). (.0001*cpath*sedyld) |
| 4:4.2.2 |  | $bact_{p,sed}=0.0001*conc_{sedpbact}*\frac{sed}{area_{hru}}*\varepsilon_{bact:sed}$ | Verified against SWAT+ 62.0.0 (path_ls_runoff.f90:35). |
| 4:4.2.3 |  | $conc_{sedlpbact}=1000*\frac{bact_{lp,sorb}}{\rho_b*depth_{surf}}$ | Verified against SWAT+ 62.0.0 (path_ls_runoff.f90:34). cpath=(1-kd)*path*enratio/conv_wt` sorbed bacteria; lp/p consolidated to one pool |
| 4:4.2.4 |  | $conc_{sedpbact}=1000*\frac{bact_{p,sorb}}{\rho_b*depth_{surf}}$ | Verified against SWAT+ 62.0.0 (path_ls_runoff.f90:34). same line (p-bacteria consolidated) |
| 4:4.3.1 |  | $bact_{lp,surf}=(bact'_{lp,surf}+bact_{lp,surstor,i-1})*(1-exp[\frac{-surlag}{t_{conc}}])$ | Verified against SWAT+ 62.0.0 (path_ls_runoff.f90). (bacteria surf, lag) |
| 4:4.3.2 |  | $bact_{p,surf}=(bact'_{p,surf}+bact_{p,surstor,i-1})*(1-exp[\frac{-surlag}{t_{conc}}])$ | Verified against SWAT+ 62.0.0 (path_ls_runoff.f90:26). bacteria surface transport computed directly; the (1-exp(-surlag/tconc)) lag NOT applied to bacteria |
| 4:4.3.3 |  | $bact_{lp,sed}=(bact'_{lp,sed}+bact_{lp,sedstor,i-1})*(1-exp[\frac{-surlag}{t_{conc}}])$ | Verified against SWAT+ 62.0.0 (path_ls_runoff.f90). |
| 4:4.3.4 |  | $bact_{p,sed}=(bact'_{p,sed}+bact_{p,sedstor,i-1})*(1-exp[\frac{-surlag}{t_{conc}}])$ | Verified against SWAT+ 62.0.0 (path_ls_runoff.f90). |

## Lineage

`path_ls_runoff.f90` was introduced in `df07e3f` (2024-03-05, "init all") and has been changed in 3 non-merge commit(s) since, most recently `39fabde` (2024-08-08, "Initialized varables with python script, corrected input data where integers whe…"). Lineage is reconstructed from commit metadata (SHA, date, subject); per-line diffs were unavailable in this build environment, so only the commits touching `path_ls_runoff.f90` are listed.

- `39fabde` (2024-08-08) — Initialized varables with python script, corrected input data where integers where floats in two input files, trapped underflow errors in th…
- `94b6dec` (2024-05-30) — Added latest source code from bitbucket
- `df07e3f` (2024-03-05) — init all

## Review Notes

- The soluble-pathogen line clamps with Max(cs_soil(...), 0.) at line 29, which appears to overwrite the previous Min-based limit and may be a source bug; the overlay records the active implementation as written.
- This routine maps pathogen transport from the generic path data structures rather than a dedicated fecal-coliform-only variable.
- Lineage was reconstructed from file-level commit metadata; per-line diffs were unavailable in this environment (blobless clone), so line-span filtering was not applied.
- Equation GitBook links were resolved from `docs/equation_inventory/gitbook_theoretical_equations.csv` by equation id. These entries were left unlinked because the lookup was not unambiguous and guessing a theory page would be worse than leaving it blank: entry 0 carries no theory equation id, so there is nothing to look up; entry 1 carries no theory equation id, so there is nothing to look up.
