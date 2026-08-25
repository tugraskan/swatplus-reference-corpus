---
kind: procedure
symbol: ero_pkq
title: ero_pkq
status: filled
source_hash: a4d7f871dff1f96c
version_label: SWAT+ 62.0.0
locals:
  j: '`j` is the active HRU index copied from `ihru`, so the routine can read the current
    HRU''s connectivity, area, and time of concentration.'
  altc: '`altc` holds the half-hour rainfall fraction transformed into the alpha_tc adjustment
    used in the intensity-based peak runoff calculation.'
  qp_cfs: '`qp_cfs` is the intermediate peak flow computed in cubic feet per second on the
    NRCS/PRF branch before converting to `qp_cms`.'
  iob: '`iob` stores the object-connectivity index for the current HRU, letting the routine
    find the linked weather station through `ob(iob)%wst`.'
  xx: '`xx` is the logarithmic exponent argument used to compute `altc` from `wst(iwst)%weat%precip_half_hr`.'
uses:
  hru_module: '`hru_module` matters because the routine needs the current HRU record to identify
    which HRU is active, get its object number, area, and conversion factor, and read the
    shared runoff and concentration state that the peak-rate formula updates.'
  hydrograph_module: '`hydrograph_module` matters because it links the HRU to its weather
    station through `ob(iob)%wst`, which is required to read the half-hour precipitation fraction
    used on the sediment-detachment branch.'
  climate_module: '`climate_module` matters because the half-hour rainfall fraction comes
    from the weather station record `wst(iwst)%weat%precip_half_hr`, and that value controls
    the alpha_tc-based peak runoff calculation.'
  basin_module: '`basin_module` matters because `bsn_cc%sed_det` selects the peak-rate method
    and `bsn_prm%prf` supplies the peak rate factor used by the NRCS dimensionless hydrograph
    branch.'
---

<!-- facts:header -->

Computes HRU peak runoff rate, choosing between a half-hour rainfall intensity method and an NRCS dimensionless hydrograph method.

## Bottom Line

This routine calculates the daily peak runoff rate for the current HRU and stores it in `qp_cms`. Which formula it uses depends on `bsn_cc%sed_det`: the half-hour rainfall intensity path uses `wst(iwst)%weat%precip_half_hr`, `tconc(j)`, and `hru(j)%km`, while the alternate path uses `bsn_prm%prf`, `hru(j)%area_ha`, `qday`, and `tconc(j)`.

It matters because `surface` only calls later sediment-erosion routines when both `qday` and the computed `qp_cms` are large enough. So this subroutine is the gatekeeper for peak-flow-dependent erosion calculations.

## Arguments

<!-- facts:arguments -->

## Where It Fits

This routine runs during surface runoff processing after `surface` assigns `qday` for the current HRU and checks that runoff is present. `surface` prepares the active HRU context, then `ero_pkq` computes `qp_cms`; later erosion routines in `surface` depend on that result because they only run when `qday` and `qp_cms` are both above the threshold.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. Load current HRU context. | Copy the active HRU number from `ihru` into `j`, then use `hru(j)%obj_no` to locate the connected hydrologic object and `ob(iob)%wst` to locate the linked weather station. |
| 2. Select peak-rate method. | Branch on `bsn_cc%sed_det` to choose the peak runoff calculation method: sediment-detachment mode uses the rainfall-intensity path, otherwise the routine uses the NRCS dimensionless hydrograph with PRF. |
| 3. Compute alpha_tc from half-hour rainfall fraction. | For the rainfall-intensity branch, transform `wst(iwst)%weat%precip_half_hr` with `xx = 2 * tconc(j) * log(1 - precip_half_hr)` and `altc = 1 - exp(xx)`. |
| 4. Compute peak runoff on intensity branch. | Use `altc`, `qday`, `tconc(j)`, and `hru(j)%km` to calculate `qp_cms` in cubic meters per second. |
| 5. Compute NRCS peak flow and convert units. | For the alternate branch, compute `qp_cfs` from `bsn_prm%prf`, `hru(j)%area_ha`, `qday`, and `tconc(j)`, then convert the result to `qp_cms` by dividing by 35.3. |
| 6. Return updated peak flow. | Exit after storing the selected peak runoff rate in shared state for later erosion calculations. |

## Modules Used

<!-- facts:uses -->

| Module | State touched | Key components |
| --- | --- | --- |
| [sym:hru_module] | `hru, tconc, ihru, qp_cms, qday` | `hru(j)%obj_no, hru(j)%km, hru(j)%area_ha` |
| [sym:hydrograph_module] | `ob, iwst` | `ob(iob)%wst` |
| [sym:climate_module] | `wst` | `wst(iwst)%weat%precip_half_hr` |
| [sym:basin_module] | `bsn_cc, bsn_prm` | `bsn_cc%sed_det, bsn_prm%prf` |

## Local Variables

<!-- facts:locals -->

## State Changes

| Target | When | Meaning |
| --- | --- | --- |
| `iwst` | When `bsn_cc%sed_det == 1` and the rainfall-intensity branch is taken. | `iwst` is updated to the weather-station index attached to the current HRU's object connectivity, so the routine can read `wst(iwst)%weat%precip_half_hr` for the alpha_tc calculation. |
| `qp_cms` | When `bsn_cc%sed_det == 1` the routine sets `qp_cms = altc * qday / tconc(j)` and converts it with `qp_cms = qp_cms * hru(j)%km / 3.6`; otherwise it sets `qp_cms = qp_cfs / 35.3` after computing `qp_cfs` from PRF. | `qp_cms` is overwritten with the current HRU's peak runoff rate in cubic meters per second, using whichever peak-rate method the basin control code selects. |

## File I/O

<!-- facts:io -->


## Theory Equations

| Eq. | Title | Formula | Implementation |
| --- | --- | --- | --- |
| 2:1.3.1 | Peak runoff rate | $q_{peak}=\frac{C*i*Area}{3.6}$ | qp_cms = alpha_tc*qday*area/(3.6*tconc) is the modified rational form using runoff volume rather than rainfall intensity times a separate runoff coefficient. |
| 2:1.3.15 | Runoff coefficient | $C=\frac{Q_{surf}}{R_{day}}$ | C = Qsurf/Rday is implicit because qday already represents runoff depth; the modified rational calculation does not store C separately. |
| 2:1.3.16 | Rainfall intensity over tc | $i=\frac{R_{tc}}{t_{conc}}$ | Intensity is implicit in qp_cms = alpha_tc*qday/tconc; the code does not store a separate itc variable. |
| 2:1.3.17 | Rainfall depth over tc | $R_{tc}=\alpha_{tc}*R_{day}$ | Rtc = alpha_tc*Rday is embedded in the alpha_tc calculation and the runoff-based peak-rate formula. |
| 2:1.3.18 | Minimum alpha_tc relation | $\alpha_{tc,min}=\frac{R_{tc}}{R_{day}}=\frac{i*t_{conc}}{i_{24}*24}=\frac{t_{conc}}{24}$ | The printed alpha_tc,min = tconc/24 lower-bound relationship is not coded directly in the peak-runoff routine. |
| 2:1.3.19 | alpha_tc from half-hour rainfall fraction | $\alpha_{tc}=1-exp[2*t_{conc}*ln(1-\alpha_{0.5})]$ | alpha_tc = 1 - exp(2*tconc*ln(1 - alpha_0.5)). Conditional: computed only when bsn_cc%sed_det == 1 (half-hour rainfall-intensity peak-rate option); else an NRCS dimensionless-hydrograph/PRF method is used. |
| 2:1.3.20 | Modified rational formula | $q_{peak}=\frac{\alpha_{tc}*Q_{surf}*Area}{3.6*t_{conc}}$ | qp_cms = alpha_tc*qday*area/(3.6*tconc). Conditional: active only when bsn_cc%sed_det == 1; the else branch (ero_pkq.f90:49-54) uses an NRCS dimensionless-hydrograph/PRF method not present in the theory page. |
| 2:1.5.4 | Flow duration from runoff and peak runoff | $dur_{flw}=\frac{Q_{surf}*Area}{3.6*q_{peak}}$ | The transmission-loss section's dur_flw formula is not formed explicitly in the active transmission-loss routines. The Lane transmission-loss regression (2:1.5.1-5.9) is not implemented anywhere; see section_2_1_surface_runoff.md. |

## Lineage

Resolved source-backed lineage shows two behavior changes after the original addition. The initial commit `df07e3f` added `ero_pkq` as a peak-runoff subroutine using a single modified rational calculation. Commit `39fabde` only initialized the local variables `j`, `altc`, `qp_cfs`, `iob`, and `xx` to zero. Commit `b7d6041` introduced the current conditional branch on `bsn_cc%sed_det`, keeping the half-hour rainfall-intensity path and moving the NRCS PRF calculation into the `else` branch.

- df07e3f introduced `ero_pkq` with a single modified rational peak-runoff calculation driven by `qday`, `tconc`, `hru(j)%area_ha`, and `bsn_prm%prf`.
- 39fabde changed only local-variable initialization for `j`, `altc`, `qp_cfs`, `iob`, and `xx`; it did not alter the peak-runoff logic.
- b7d6041 added conditional method selection with `bsn_cc%sed_det`, preserving the rainfall-intensity formula on the true branch and moving the PRF-based NRCS calculation to the false branch.

## Review Notes

- No direct file I/O was extracted for this procedure.
- warning: missing_doc: Procedure 'ero_pkq' has no extracted documentation comment.
