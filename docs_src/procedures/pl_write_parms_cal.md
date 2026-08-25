---
kind: procedure
symbol: pl_write_parms_cal
title: pl_write_parms_cal
status: filled
source_hash: f9634a49a912788e
version_label: SWAT+ 62.0.0
locals:
  eof: Loop/control flag initialized to zero, but no later source line in this routine uses
    it; it appears to be leftover bookkeeping.
  mreg: Loop/control counter initialized to zero, but it is not subsequently referenced in
    the shown source; it is effectively unused here.
  i: Outer loop index over plant calibration regions in `db_mx%plcal_reg`.
  ilum: Inner loop index over plant parameter records within a region.
  ilum_mx: Computed upper bound for the inner loop, set to `pl_prms(i)%lum_num * pl_prms(i)%parms`
    so the routine can visit every parameter slot for that region.
uses:
  maximum_data_module: '`db_mx%plcal_reg` supplies the total number of plant calibration regions
    to process and therefore controls how many region blocks are written to `plant_parms.cal`.'
  calibration_data_module: '`pl_prms` holds the plant-region names, land-use counts, parameter
    counts, parameter definitions, and the `init_val`, bounds, and variable names that are
    written and updated here; `plcal` provides the soft-calibration adjustment values that
    get merged into those plant parameter records.'
  hydrograph_module: The source shows `use hydrograph_module`, but no symbol from that module
    is referenced in the routine body, so it has no observable effect in the extracted code.
  input_file_module: The source shows `use input_file_module`, but no symbol from that module
    is referenced in the routine body, so it does not affect the file-writing logic shown
    here.
  plant_module: The source shows `use plant_module`, but no symbol from that module is referenced
    in the routine body; any influence would have to be indirect and is not visible in the
    extracted lines.
---

<!-- facts:header -->

Writes the calibrated plant parameter file `plant_parms.cal` from current plant calibration state. It copies region and parameter records from module data, applies soft-calibration adjustments, clamps them to bounds, and emits the result for later model runs.

## Bottom Line

`pl_write_parms_cal` creates the `plant_parms.cal` text file used to persist plant calibration settings. It opens the file, writes a short file header and the number of calibrated plant regions, then loops through each plant region and each parameter record to update `init_val` from soft-calibration values before writing the parameter record back out.

The routine matters because it turns in-memory calibration state into a file that downstream calibration or model setup steps can reuse. Its behavior is driven entirely by module state: plant-region metadata in `pl_prms`, adjustment values in `plcal`, and the maximum region count in `db_mx%plcal_reg`.

## Arguments

<!-- facts:arguments -->

## Where It Fits

This routine runs during soft-data calibration when plant calibration output is being assembled. `calsoft_control` checks the plant-calibration flag and calls `pl_write_parms_cal` after the calibration data structures have been loaded; the resulting `plant_parms.cal` file is then available for later calibration-related model setup or reuse.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. Open the plant calibration output file and write its file-level header. | Unit 107 is opened on `plant_parms.cal`, then the routine writes a title line, the number of calibration regions from `db_mx%plcal_reg`, and a placeholder `header` line. |
| 2. Iterate over each plant calibration region. | For each region index `i`, the routine writes region metadata from `pl_prms(i)`—the region name, land-use count, parameter count, and a trailing `0` field—then writes another `header` line. |
| 3. Determine whether the region has land-use parameters to process. | If `pl_prms(i)%lum_num` is positive, the routine computes `ilum_mx` as `pl_prms(i)%lum_num * pl_prms(i)%parms`, establishing how many parameter records belong to the region. |
| 4. Loop over each plant parameter record in the region. | The inner loop visits each `pl_prms(i)%prm(ilum)` entry and inspects its `var` field to decide which calibration adjustment applies. |
| 5. Apply a pest-stress adjustment when the record variable is `pest_stress`. | The routine adds `plcal(i)%lum(ilum)%prm%pest_stress` to the current `init_val`, then clamps the result to the record’s upper and lower bounds with `amin1` and `Max`. |
| 6. Load the `epco` calibration value when the record variable is `epco`. | The routine assigns `init_val` from `plcal(i)%lum(ilum-pl_prms(i)%lum_num)%prm%epco`, then bounds the value within `up` and `lo`. |
| 7. Apply a leaf-area adjustment when the record variable is `lai_pot`. | The routine adds `plcal(i)%lum(ilum-2*pl_prms(i)%lum_num)%prm%lai_pot` to `init_val` and clamps the result to the allowed bounds. |
| 8. Apply a harvest-index adjustment when the record variable is `harv_idx`. | The routine adds `plcal(i)%lum(ilum-3*pl_prms(i)%lum_num)%prm%harv_idx` to `init_val` and then applies the same upper and lower bound limits. |
| 9. Write the updated parameter record to the output file. | After the selected calibration update and clamping, the routine writes the full `pl_prms(i)%prm(ilum)` record to `plant_parms.cal`. |
| 10. Finish the loops, close the file, and return. | When all regions and parameter records are processed, the routine closes unit 107 and returns to the caller. |

## Modules Used

<!-- facts:uses -->

| Module | State touched | Key components |
| --- | --- | --- |
| [sym:maximum_data_module] | `db_mx` | `db_mx%plcal_reg` |
| [sym:calibration_data_module] | `pl_prms, plcal` | `pl_prms(i)%name, pl_prms(i)%lum_num, pl_prms(i)%parms, pl_prms(i)%prm(ilum)%var, pl_prms(i)%prm(ilum)%init_val, plcal(i)%lum(ilum)%prm%pest_stress, pl_prms(i)%prm(ilum)%up, pl_prms(i)%prm(ilum)%lo, pl_prms(i)%prm(ilum)` |
| [sym:hydrograph_module] | `NONE` | `NONE` |
| [sym:input_file_module] | `NONE` | `NONE` |
| [sym:plant_module] | `NONE` | `NONE` |

## Local Variables

<!-- facts:locals -->

## State Changes

| Target | When | Meaning |
| --- | --- | --- |
| `pl_prms(i)%prm(ilum)%init_val` | When `pl_prms(i)%lum_num > 0` and `pl_prms(i)%prm(ilum)%var` matches one of the handled calibration variables (`pest_stress`, `epco`, `lai_pot`, or `harv_idx`). | `pl_prms(i)%prm(ilum)%init_val` is updated from the current soft-calibration adjustment and then clipped to the record’s lower and upper limits so the written parameter stays within allowed bounds. |

## File I/O

<!-- facts:io -->


## Lineage

Resolved lineage commits show one substantive behavior change after the file was introduced: `39fabde` only initialized local integers `eof`, `mreg`, `i`, `ilum`, and `ilum_mx` at declaration time, without changing the file-writing logic. `94b6dec` introduced the routine in its current form, including the `plant_parms.cal` output format and the per-variable calibration adjustments.

- 39fabde: changed only local-variable initialization for `eof`, `mreg`, `i`, `ilum`, and `ilum_mx`; the write logic and calibration math stayed the same in the diff shown.
- 94b6dec: added `pl_write_parms_cal` and its current file-writing behavior, including region headers, variable-specific `init_val` adjustments, and the `plant_parms.cal` output file.

## Review Notes

- Direct file I/O exists; verify file meanings and units before finalizing.
- warning: missing_doc: Procedure 'pl_write_parms_cal' has no extracted documentation comment.
- algorithm_steps revised: reordered steps to follow the source from file open through return and expanded the loop/adjustment logic into discrete source-backed steps.
- `hydrograph_module`, `input_file_module`, and `plant_module` are listed as USE dependencies in the source, but no symbols from them are referenced in the extracted routine body; their effect is uncertain from this snippet alone.
