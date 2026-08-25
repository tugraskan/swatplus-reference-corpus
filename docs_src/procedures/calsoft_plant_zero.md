---
kind: procedure
symbol: calsoft_plant_zero
title: calsoft_plant_zero
status: filled
source_hash: 9dab56f34f9fad5f
version_label: SWAT+ 62.0.0
locals:
  ireg: Loop index over calibration regions (1 … db_mx%plcal_reg).
  ilum: Nested loop index over land uses within a region (1 … plcal(ireg)%lum_num).
uses:
  calibration_data_module: plcal stores all region- and land-use-specific plant calibration
    accumulators that must be zeroed before the next pass; plcal_z is the predefined structure
    containing zero values that is copied into each aa field.
  maximum_data_module: Provides the number of plant-calibration regions that bounds the outer
    loop.
---

<!-- facts:header -->

Clears all plant-calibration accumulators for every calibration region and land use before a new soft-calibration simulation pass.

## Bottom Line

calsoft_plant_zero is a housekeeping routine that runs at the start of a soft-calibration pass.  It walks through every plant-calibration region (db_mx%plcal_reg) and through every land-use entry held in plcal(ireg).  Inside that double loop it resets year counters, precipitation means, simulated and average-annual process totals, yields, and calibrated land-use area to zero or to the predefined zero-valued template plcal_z.

By returning all accumulators to a known clean state the routine guarantees that the next simulation can build fresh totals that are not contaminated by values from a previous run.  Nothing is returned directly—its effect is entirely through the module-level plcal array that the rest of the calibration system subsequently updates.

## Arguments

<!-- facts:arguments -->

## Where It Fits

Called from calsoft_plant just before a new soft-calibration simulation run begins (see calsoft_plant.f90 line 83).  calsoft_plant has already calculated isim and other control flags; calsoft_plant_zero then clears the accumulators so that subsequent calls to time_control and the main simulation can fill them with fresh values.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. Loop over regions | Start an outer loop that iterates once for every plant-calibration region (1 … db_mx%plcal_reg). |
| 2. Loop over land uses | Within each region, iterate over every land-use slot present in the region (1 … plcal(ireg)%lum_num). |
| 3. Zero calibration fields | Set nbyr, precip_aa, sim%yield and ha to 0 and copy the zero-template plcal_z into the aa average-annual structure, fully clearing the accumulator record for this land use. |
| 4. Return | Exit the subroutine after all regions and land uses have been processed. |

## Modules Used

<!-- facts:uses -->

| Module | State touched | Key components |
| --- | --- | --- |
| [sym:calibration_data_module] | `plcal, plcal_z` | `plcal(ireg)%lum_num, plcal(ireg)%lum(ilum)%nbyr, plcal(ireg)%lum(ilum)%precip_aa, plcal(ireg)%lum(ilum)%aa, plcal(ireg)%lum(ilum)%sim%yield, plcal(ireg)%lum(ilum)%ha` |
| [sym:maximum_data_module] | `db_mx` | `db_mx%plcal_reg` |

## Local Variables

<!-- facts:locals -->

## State Changes

| Target | When | Meaning |
| --- | --- | --- |
| `plcal(ireg)%lum(ilum)%nbyr` | For every region/land-use combination during the reset pass | Year counter set to 0 so that future accumulation starts fresh. |
| `plcal(ireg)%lum(ilum)%precip_aa` | Same loop iteration | Average annual precipitation reset to 0.0 mm. |
| `plcal(ireg)%lum(ilum)%aa` | Same loop iteration | Entire average-annual calibration structure overwritten with the zero template plcal_z. |
| `plcal(ireg)%lum(ilum)%sim%yield` | Same loop iteration | Simulated cumulative yield reset to 0 t or 0 t ha⁻¹. |
| `plcal(ireg)%lum(ilum)%ha` | Same loop iteration | Tracked land-use area reset to 0 ha. |

## File I/O

<!-- facts:io -->


## Lineage

Git history shows three commits that could affect this subroutine:
• 39fabde (2024-08-08) "Initialized variables with python script…" – likely touched many files but the exact impact on calsoft_plant_zero is unclear.
• c7c8e22 (2024-05-30) "Added latest source code from bitbucket" – bulk source import; origin of current file.
• df07e3f (2024-03-05) "init all" – initial population of repository.
No further lineage details were provided.

## Review Notes

- algorithm_steps revised: added explicit step for field reset and updated descriptions to match lines 13–17.
- No direct file I/O was extracted for this procedure.
- warning: missing_doc: Procedure 'calsoft_plant_zero' has no extracted documentation comment.
