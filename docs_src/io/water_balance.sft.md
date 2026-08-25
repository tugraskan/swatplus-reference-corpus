---
kind: io
source_symbols:
- lcu_read_softcal
title: '`water_balance.sft`'
status: filled
source_hash: 5db1a0b9bb16e673
version_label: SWAT+ 62.0.0
---

**Primary target:** `region(:)` (array of `type cataloging_units`)  
**Read by:** [sym:lcu_read_softcal]

## Bottom Line

The file `water_balance.sft` contains soft calibration data for landscape units and land uses within regions, used to calibrate water balance parameters such as water yield and baseflow ratio.

It is optional and only read if the file exists and is not set to "null" in the configuration.

The primary reader for this file is the subroutine `lcu_read_softcal`.

| Module | Role for this file |
| --- | --- |
| [sym:input_file_module] | provides the input file path variable `in_chg%water_balance_sft` used to locate the `water_balance.sft` file. |
| [sym:maximum_data_module] | provides the global maximum data structure `db_mx` used to store the number of landscape cataloging units (`lsu_reg`) and land uses (`landuse`). |
| [sym:calibration_data_module] | provides the types `cataloging_units` (for `region`) and `soft_data_calib_landscape` (for `lscal`), as well as the global `db_mx` variable and related calibration data structures. |
| [sym:hydrograph_module] | used for hydrologic response unit indexing (`ihru`) and possibly related hydrograph data structures. |
| [sym:hru_module] | provides the `ihru` index used to loop over HRUs in the region. |
| [sym:hru_lte_module] | used for land type or land treatment effect data, indirectly related to calibration data storage. |
| [sym:output_landscape_module] | provides the output landscape data structures such as `rwb_d`, `rwb_m`, `rwb_y`, `rwb_a`, `rnb_d`, `rnb_m`, `rnb_y`, `rnb_a`, `rls_d`, `rls_m`, `rls_y`, `rls_a`, `rpw_d`, `rpw_m`, `rpw_y`, `rpw_a` which are allocated per region and land use for storing calibration results. |
| [sym:basin_module] | provides basin-level data such as `bsn%area_ls_ha` and `sp_ob%hru` used to assign HRU areas and counts to the region. |

## File Variables

The `water_balance.sft` file contains soft calibration data records for landscape cataloging units (regions) and their associated land uses. Each region record includes metadata such as name and number of land uses, followed by calibration measurements per land use. The file is read sequentially by `lcu_read_softcal` and mapped into arrays of `cataloging_units` and `soft_data_calib_landscape` types.

| Col | Header | Target | Type | Units | Meaning |
| --- | --- | --- | --- | --- | --- |
| 2 |  | `region%name` | character(len=16) |  | name of region - (number of regions = db_mx%lsu_reg) |
| 3 |  | `region%area_ha` | real |  | area of landscape cataloging unit -hectares |
| 4 |  | `region%num_tot` | integer |  | number of HRUs in each region |
| 5 |  | `region%num` | integer |  | HRUs that are included in the region |
| 6 |  | `region%nlum` | integer |  | number of land use and management units in the region |
| 7 |  | `region%lumc` | character(len=16) |  | land use groups |
| 8 |  | `region%lum_num` | integer |  | database number of land use in the region - dimensioned by land use in the region |
| 9 |  | `region%lum_num_tot` | integer |  | database number of land use in the region each year - dimensioned by land use in database |
| 10 |  | `region%lum_ha` | real |  | area (ha) of land use in the region - dimensioned by land use in the region |
| 11 |  | `region%lum_ha_tot` | real |  | sum of area (ha) of land use in the region each year - dimensioned by land use in database |
| 12 |  | `region%hru_ha` | real |  | area (ha) of HRUs in the region |
| 2 |  | `lscal%name` | character(len=16) |  | name of region - (number of regions = db_mx%lsu_reg) |
| 3 |  | `lscal%lum_num` | integer |  | number of land uses in each region |
| 4 |  | `lscal%num_tot` | integer |  | number of HRUs in each region |
| 5 |  | `lscal%num` | integer |  | HRUs that are included in the region |
| 6 |  | `lscal%num_reg` | integer |  | number of regions the soft data applies to |
| 7 |  | `lscal%reg` | character(len=16) |  | name of regions the soft data applies to |
| 8 |  | `lscal%ireg` | integer |  | index of regions the soft data applies to |
| 9 |  | `lscal%lum` | type (ls_calib_regions) |  | dimension for land uses within a region |

## Sample

```text
Example records from `water_balance.sft` (format inferred from reader):
Line 1: Title line (character*80)
Line 2: Number of regions (integer)
Line 3: Header line (character*80)
For each region:
  Line: region name (character*16), number of land uses (integer)
  Line: header line (character*80) if number of land uses > 0
  For each land use in region:
    Line: calibration measurements (read into lscal(ireg)%lum(ilum)%meas, format unspecified)
```

## Read Pattern

```fortran
open (107,file=in_chg%water_balance_sft)
read (107,*,iostat=eof) titldum
read (107,*,iostat=eof) mreg
read (107,*,iostat=eof) header
read (107,*,iostat=eof) region(ireg)%name, region(ireg)%nlum
read (107,*,iostat=eof) lscal(ireg)%lum(ilum)%meas
```

## I/O Operations

| Direction | Op | Unit | Statement |
| --- | --- | --- | --- |
| File setup | `open` | 107 | `open (107,file=in_chg%water_balance_sft)` |
| Input | `read` | 107 | `read (107,*,iostat=eof) titldum` |
| Input | `read` | 107 | `read (107,*,iostat=eof) mreg` |
| Input | `read` | 107 | `read (107,*,iostat=eof) header` |
| Input | `read` | 107 | `read (107,*,iostat=eof) region(ireg)%name, region(ireg)%nlum` |
| Input | `read` | 107 | `read (107,*,iostat=eof) header` |
| Input | `read` | 107 | `read (107,*,iostat=eof) lscal(ireg)%lum(ilum)%meas` |

## Readers

| Procedure | Operations | Role |
| --- | --- | --- |
| [sym:lcu_read_softcal] | open, read | Reads the `water_balance.sft` file if it exists and is not set to "null". It reads the number of regions, allocates arrays for regions and calibration data, then loops over each region reading its name and number of land uses. For each land use, it reads soft calibration measurements into `lscal(ireg)%lum(ilum)%meas`. It also allocates and initializes output arrays for water balance and nutrient balance results per region and land use. If the region is the entire basin (named "basin" or if only one region), it assigns HRU indices and areas to the region. |

## Review Notes

- Draft input-file overlay generated from static source facts; the file is optional and only read if it exists and is not set to "null".
- The exact format of the calibration measurements read into `lscal(ireg)%lum(ilum)%meas` is not detailed in the source and may require further inspection of the `ls_calib_regions` type or related modules.
- The file configures soft calibration parameters for water balance and related landscape units, supporting regional and land use level calibration.
