---
kind: procedure
symbol: lcu_read_softcal
title: lcu_read_softcal
status: filled
source_hash: 5429c141bc967519
version_label: SWAT+ 62.0.0
locals:
  titldum: First line read from `water_balance.sft`; used as a title or label record that
    is skipped past before the numeric region count is read.
  header: Header marker line(s) in `water_balance.sft`; this routine reads it to advance through
    the file and again before each region's landuse calibration block.
  eof: IO status flag from each `read` on unit 107. Negative values stop the loop on end-of-file
    or read failure.
  imax: Initialized but not used in the extracted source logic; it appears to be a leftover
    counter placeholder for sizing or maximum-record tracking.
  i_exist: Logical result of `inquire(file=...,exist=i_exist)`; it gates whether the routine
    reads `water_balance.sft` or falls back to empty 0:0 allocations.
  mcal: Initialized but not used in the extracted source logic; it appears to be an unused
    calibration counter placeholder.
  mreg: Number of calibration regions read from `water_balance.sft`; it controls allocation
    sizes and the main region loop.
  ireg: Loop index over calibration regions in the file and in the `region`/`lscal` arrays.
  mlug: Temporary landuse count for the current region; set from `region(ireg)%nlum` and used
    to size landuse arrays.
  ilum: Loop index over landuse entries within the current region's calibration block.
uses:
  input_file_module: This module supplies the configured soft-calibration filename. `lcu_read_softcal`
    uses it to decide which input file to probe and open for reading.
  maximum_data_module: These maximum-data counters are updated from the file contents so other
    routines can know how many calibration regions exist and how many landuses are in the
    current region.
  calibration_data_module: 'This module holds the soft calibration database being populated
    here: region descriptors, landuse calibration records, calibration code switches, and
    the HRU/landuse mapping structures that are filled for basin-wide calibration.'
  hydrograph_module: '`sp_ob%hru` tells the routine how many HRUs exist when it builds the
    basin-wide region membership lists and HRU number arrays.'
  hru_module: '`ihru` is the loop counter used to enumerate HRUs while populating `region(ireg)%num`
    and `region(ireg)%hru_ha`.'
  hru_lte_module: This module is included with the calibration data definitions; its landscape-calibration
    types support the soft-calibration structures this routine allocates and fills, especially
    when the same calibration framework is used for HRU and HRU-LTE contexts.
  output_landscape_module: These output containers are allocated to the same region count
    so later landscape reporting can store annual water, nutrient, loss, and plant/weather
    summaries for each landuse within each region.
  basin_module: The basin landscape area is required to convert each HRU fraction into an
    absolute hectares value when the routine assigns basin-wide HRU areas.
---

<!-- facts:header -->

Reads the landscape soft-calibration file and builds region/landuse calibration storage used by later landscape and HRU calibration routines. It also initializes the regional output containers that track water balance, nutrient balance, losses, and plant/weather summaries.

## Bottom Line

`lcu_read_softcal` is a setup routine for soft landscape calibration. It checks whether `in_chg%water_balance_sft` exists, reads the file header and region blocks from unit 107, and allocates the `lscal` and `region` arrays to match the number of calibration regions listed in the file.

For each region, it records the region name and landuse count, allocates per-landuse calibration records, and reads the soft calibration measurements into `lscal(ireg)%lum(ilum)%meas`. When the calibration mode is not `cal_codes%hyd_hru == 'a'`, it converts the stored water-yield/baseflow inputs into the surface-runoff, baseflow, and lateral-flow ratios used by the model. For the basin-wide case, it also fills HRU membership and HRU area totals from `sp_ob%hru`, `bsn%area_ls_ha`, and `lsu_elem(ihru)%bsn_frac`, and it sizes the annual regional output arrays used later by landscape reporting.

## Arguments

<!-- facts:arguments -->

## Where It Fits

`lcu_read_softcal` runs during calibration setup inside `proc_cal`, after the soft calibration codes have been read by `calsoft_read_codes` and before other landscape/element readers such as `ls_read_lsparms_cal`. Its results feed later landscape calibration logic and regional output bookkeeping by defining the soft-calibration regions, their landuse measurements, and the basin-wide HRU mapping when needed.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. Initialize counters and check for the configured soft-calibration file | The routine resets `imax`, `mcal`, and `mreg`, then uses `inquire` on `in_chg%water_balance_sft` to see whether the file exists and is not set to the literal string `null`. |
| 2. Allocate empty calibration containers when no file is available | If the file is missing or disabled, it allocates single-element placeholder arrays `lscal(0:0)` and `region(0:0)` so later code can still reference the structures safely. |
| 3. Open the soft-calibration file and read its top records | Inside a read loop, the routine opens unit 107 on `water_balance.sft` and reads the title, region count, and section header, exiting on end-of-file or read failure. |
| 4. Size the regional calibration and output arrays | Using `mreg`, it allocates `lscal(0:mreg)`, `region(0:mreg)`, and the regional output arrays for water balance, nutrient balance, losses, and plant/weather summaries. |
| 5. Store the total number of calibration regions | The routine copies the region count into `db_mx%lsu_reg` so the global maximum-data state records how many landscape calibration regions are active. |
| 6. Read each region's name and landuse count | For each region, it reads `region(ireg)%name` and `region(ireg)%nlum`, stores the landuse count in `mlug`, and allocates the per-region landuse totals and `lscal(ireg)%lum` records. |
| 7. Allocate per-region output and initialize totals | The routine allocates `rwb_a(ireg)%lum`, `rnb_a(ireg)%lum`, `rls_a(ireg)%lum`, and `rpw_a(ireg)%lum`, then zeros the landuse total arrays for area and counts. |
| 8. Read landuse calibration measurements for the region | If the region contains landuses, it reads a header line and then loops over `ilum = 1, mlug`, reading each `lscal(ireg)%lum(ilum)%meas` record from the file. |
| 9. Convert hydrologic calibration inputs when required | When `cal_codes%hyd_hru` is not `a`, it transforms the stored `wyr` and `bfr` values into `srr`, `bfr`, and `lfr` so the calibration uses precipitation-based runoff and baseflow fractions. |
| 10. Populate basin-wide HRU mappings for basin calibration | If the region is the basin or the model is in single-region mode (`db_mx%lsu_reg == 1`), it sets `region(ireg)%num_tot` to `sp_ob%hru`, allocates the HRU index and area arrays, and fills each HRU number and hectares from `bsn%area_ls_ha` and `lsu_elem(ihru)%bsn_frac`. |
| 11. Finish after the first successful pass through the file | The loop exits after one pass, and the subroutine returns with the calibration structures and output containers initialized. |

## Modules Used

<!-- facts:uses -->

| Module | State touched | Key components |
| --- | --- | --- |
| [sym:input_file_module] | `in_chg` | `in_chg%water_balance_sft` |
| [sym:maximum_data_module] | `db_mx` | `db_mx%lsu_reg, db_mx%landuse` |
| [sym:calibration_data_module] | `region, lscal, cal_codes, lsu_elem` | `region(ireg)%name, region(ireg)%nlum, region(ireg)%lum_ha_tot(mlug), region(ireg)%lum_num_tot(mlug), lscal(ireg)%lum(mlug), region(ireg)%lum_ha_tot, region(ireg)%lum_num_tot, lscal(ireg)%lum(ilum)%meas, cal_codes%hyd_hru, lscal(ireg)%lum(ilum)%meas%srr, lscal(ireg)%lum(ilum)%meas%wyr, lscal(ireg)%lum(ilum)%meas%bfr, lscal(ireg)%lum(ilum)%meas%lfr, region(ireg)%num_tot, region(ireg)%num, region(ireg)%hru_ha, region(ireg)%num(ihru), region(ireg)%hru_ha(ihru), lsu_elem(ihru)%bsn_frac` |
| [sym:hydrograph_module] | `sp_ob` | `sp_ob%hru` |
| [sym:hru_module] | `ihru` |  |
| [sym:hru_lte_module] | `lscal_z` | `lscal_z` |
| [sym:output_landscape_module] | `rwb_a, rnb_a, rls_a, rpw_a, rwb_d, rwb_m, rwb_y, rnb_d, rnb_m, rnb_y, rls_d, rls_m, rls_y, rpw_d, rpw_m, rpw_y` | `rwb_a(ireg)%lum(mlug), rnb_a(ireg)%lum(mlug), rls_a(ireg)%lum(mlug), rpw_a(ireg)%lum(mlug)` |
| [sym:basin_module] | `bsn` | `bsn%area_ls_ha` |

## Local Variables

<!-- facts:locals -->

## State Changes

| Target | When | Meaning |
| --- | --- | --- |
| `db_mx%lsu_reg` | After reading the top-of-file region count from `water_balance.sft` | Stores the number of soft-calibration regions so downstream calibration code knows the active landscape-region extent. |
| `db_mx%landuse` | After reading each region record | Temporarily records the current region's landuse count, which is used to size that region's landuse calibration arrays. |
| `region(ireg)%lum_ha_tot` | After allocating a region's landuse totals | Creates and initializes the per-landuse area totals for the current calibration region, ready to be filled by later calibration or aggregation routines. |
| `region(ireg)%lum_num_tot` | After allocating a region's landuse totals | Creates and initializes the per-landuse count totals for the current calibration region. |
| `lscal(ireg)%lum(ilum)%meas%srr` | After reading one landuse measurement record and when `cal_codes%hyd_hru /= 'a'` | Derived from water-yield and baseflow fraction inputs so the calibration stores surface-runoff ratio on a precipitation basis. |
| `lscal(ireg)%lum(ilum)%meas%bfr` | After reading one landuse measurement record and when `cal_codes%hyd_hru /= 'a'` | Converted from a fraction of water yield to a fraction of precipitation, so the stored baseflow ratio matches the model's calibration convention. |
| `lscal(ireg)%lum(ilum)%meas%lfr` | After reading one landuse measurement record and when `cal_codes%hyd_hru /= 'a'` | Computed as a scaled fraction of the converted baseflow ratio, providing the lateral-flow calibration value used later by hydrologic calibration routines. |
| `region(ireg)%num_tot` | When the region is basin-wide or the model is in single-region mode | Set to the number of HRUs in `sp_ob%hru` so the basin region tracks all HRUs included in the calibration domain. |
| `region(ireg)%num(ihru)` | When the region is basin-wide or the model is in single-region mode | Filled with each HRU index so the basin region has an explicit membership list for every HRU. |
| `region(ireg)%hru_ha(ihru)` | When the region is basin-wide or the model is in single-region mode | Calculated from basin area times HRU basin fraction to store each HRU's area in hectares for the calibration region. |

## File I/O

<!-- facts:io -->


## Lineage

`lcu_read_softcal` was added in commit `df07e3f` as a new subroutine that reads soft landscape calibration data, allocates the regional calibration/output structures, and fills basin-wide HRU mappings. Commit `39fabde` changed the local variable declarations to initialize the scalars, and also split several combined `allocate` statements into separate lines; commit `f1e61a3` only adjusted whitespace/tab formatting.

- Added the initial `lcu_read_softcal` implementation that reads `water_balance.sft`, populates `lscal`/`region`, and allocates the regional output arrays.
- Initialized local scalars (`titldum`, `header`, `eof`, `imax`, `mcal`, `mreg`, `ireg`, `mlug`, `ilum`) to safe defaults and reformatted the regional output allocations into separate statements.
- Made a whitespace-only cleanup in the subroutine body without changing behavior.

## Review Notes

- Direct file I/O exists; verify file meanings and units before finalizing.
- warning: missing_doc: Procedure 'lcu_read_softcal' has no extracted documentation comment.
