---
kind: procedure
symbol: soil_carbvar_write_legacy
title: soil_carbvar_write_legacy
status: filled
source_hash: 9a397c24d1a3eac8
version_label: SWAT+ 62.0.0
args:
  out_freq: Selects the output frequency label that is written with every record. The routine
    accepts the legacy two-character codes for daily, monthly, yearly, and average-annual
    output and maps them to the labels `day`, `mon`, `year`, or `av_ann` before writing.
locals:
  freq_label: Human-readable frequency tag attached to every output row after `out_freq` is
    decoded.
  j: Loop index for the HRU being written; it selects the soil profile, layer count, and matching
    object metadata.
  k: Loop index for the soil layer within the current HRU; it selects the layer-level carbon
    and mixing values to write.
  iob: Object index in `ob` for the current HRU; it is derived from `sp_ob1%hru` so the output
    row can include the correct GIS id and object name.
uses:
  basin_module: '`basin_module` provides `pco`, whose `csvout` flag controls whether a second
    CSV-formatted line is written for each output record.'
  carbon_module: '`carbon_module` defines the carbon-control and carbon-state component types
    embedded inside `soil1(j)%org_con_lr(k)`, `soil1(j)%org_allo_lr(k)`, `soil1(j)%org_ratio_lr(k)`,
    and `soil1(j)%org_tran_lr(k)`. Those values are the actual payload of the legacy carbon-variable
    files.'
  hydrograph_module: '`hydrograph_module` supplies the HRU counts and object metadata used
    to drive the loops and identify each record. `sp_ob%hru` sets how many HRUs are written,
    `sp_ob1%hru` converts the HRU loop index to the matching `ob` index, and `ob(iob)%name`
    tags each row with the object name.'
  organic_mineral_mass_module: '`organic_mineral_mass_module` provides the per-HRU layered
    soil-carbon container `soil1`. The routine reads its layer-wise carbon controls, allocation
    ratios, ratio outputs, transformation outputs, and mixing fractions so the legacy files
    capture the soil carbon state by layer.'
  calibration_data_module: '`calibration_data_module` contributes the simulation clock used
    in every row. The date fields distinguish when each HRU-layer record was written and are
    part of the legacy output schema.'
  soil_module: '`soil_module` provides the HRU soil profile, layer counts, physical layer
    depth, layer temperature, and tillage/mixing factors that are written alongside the carbon
    variables. Without this module the routine would not know how many layers to loop over
    or which soil-layer properties to report.'
---

<!-- facts:header -->

Writes legacy CSU soil carbon variable outputs for each HRU and soil layer. It reports layer depth, date, object identifiers, tillage/mixing factors, and carbon-related control values in text and optional CSV files.

## Bottom Line

This routine is a legacy output writer for soil carbon variables. For each HRU and each soil layer, it formats the current simulation date plus soil, carbon-control, and mixing state into a set of output records.

It writes one mandatory record stream and, when `pco%csvout` is enabled, parallel CSV records for the same variables. The routine is invoked from `command` only when legacy CSU carbon-variable printing is active (`bsn_cc%cswat == 2`) and the selected HRU print flags request the chosen frequency.

## Arguments

<!-- facts:arguments -->

## Where It Fits

This routine runs from `command` during the HRU output phase when legacy CSU carbon-variable printing is enabled (`bsn_cc%cswat == 2`) and the configured print intervals request the chosen frequency. It depends on upstream setup of print codes, the global simulation clock, HRU/object indexing, and fully initialized soil and carbon state; downstream, its records feed the legacy HRU carbon-variable output files used for analysis and validation.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. Decode the requested output frequency. | The routine maps the two-character `out_freq` code to a readable `freq_label` such as `day`, `mon`, `year`, or `av_ann`. |
| 2. Loop over HRUs and soil layers for the main carbon-variable file. | For every HRU and every soil layer, it writes the frequency label, layer depth, current date, HRU/object identifiers, layer carbon-control values, tillage/mixing factors, temperature, and mixing fraction to unit 8374. |
| 3. Optionally write CSV-formatted main carbon-variable records. | If `pco%csvout` is enabled, the same HRU-layer carbon-variable record is written again to unit 8375 using CSV formatting. |
| 4. Loop over HRUs and soil layers for organic-allocation outputs. | The routine writes the per-layer organic-allocation value `soil1(j)%org_allo_lr(k)` to unit 8376, and writes the CSV companion line to unit 8377 when CSV output is enabled. |
| 5. Loop over HRUs and soil layers for organic-ratio outputs. | The routine writes the per-layer organic-ratio value `soil1(j)%org_ratio_lr(k)` to unit 8378, and writes the CSV companion line to unit 8379 when CSV output is enabled. |
| 6. Loop over HRUs and soil layers for organic-transformation outputs. | The routine writes the per-layer organic-transformation value `soil1(j)%org_tran_lr(k)` to unit 8380, and writes the CSV companion line to unit 8381 when CSV output is enabled. |
| 7. Return to the caller. | The subroutine ends after all selected output records have been appended. |

## Modules Used

<!-- facts:uses -->

| Module | State touched | Key components |
| --- | --- | --- |
| [sym:basin_module] | `pco` | `pco%csvout` |
| [sym:carbon_module] | `soil1` | `soil1(j)%org_con_lr(k)%sut, soil1(j)%org_con_lr(k)%till_eff, soil1(j)%org_con_lr(k)%cdg, soil1(j)%org_con_lr(k)%ox, soil1(j)%org_con_lr(k)%cs, soil1(j)%org_con_lr(k)%no3, soil1(j)%org_con_lr(k)%nh4, soil1(j)%org_con_lr(k)%resp, soil1(j)%emix(k), soil1(j)%org_allo_lr(k), soil1(j)%org_ratio_lr(k), soil1(j)%org_tran_lr(k)` |
| [sym:hydrograph_module] | `sp_ob, sp_ob1, ob` | `sp_ob%hru, sp_ob1%hru, ob(iob)%name` |
| [sym:organic_mineral_mass_module] | `soil1` | `soil1(j)%org_con_lr(k)%sut, soil1(j)%org_con_lr(k)%till_eff, soil1(j)%org_con_lr(k)%cdg, soil1(j)%org_con_lr(k)%ox, soil1(j)%org_con_lr(k)%cs, soil1(j)%org_con_lr(k)%no3, soil1(j)%org_con_lr(k)%nh4, soil1(j)%org_con_lr(k)%resp, soil1(j)%emix(k), soil1(j)%org_allo_lr(k), soil1(j)%org_ratio_lr(k), soil1(j)%org_tran_lr(k)` |
| [sym:calibration_data_module] | `time` | `time%day, time%mo, time%day_mo, time%yrc` |
| [sym:soil_module] | `soil` | `soil(j)%nly, soil(j)%ly(k)%tillagef, soil(j)%ly(k)%bmix, soil(j)%ly(k)%tillagef_biomix, soil(j)%ly(k)%tillagef_tillmix, soil(j)%phys(k)%tmp` |

## Local Variables

<!-- facts:locals -->

## State Changes

| Target | When | Meaning |
| --- | --- | --- |
| `none extracted` | none extracted | No assignment targets were extracted automatically. |

## File I/O

<!-- facts:io -->


## Lineage

The procedure was added in commit 821a63e, which introduced `soil_carbvar_write_legacy` as a legacy CSU carbon output writer with the current set of HRU-layer text and optional CSV outputs. The resolved diff shows no later behavioral changes within the provided lineage evidence.

- 821a63e added the subroutine and its legacy CSU carbon-variable outputs, including the frequency-label mapping, HRU/layer loops, and paired text/CSV writes for carbon, allocation, ratio, and transformation variables.

## Review Notes

- Direct file I/O exists; verify file meanings and units before finalizing.
- warning: missing_doc: Procedure 'soil_carbvar_write_legacy' has no extracted documentation comment.
