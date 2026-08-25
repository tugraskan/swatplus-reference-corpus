---
kind: io
source_symbols:
- res_read_elements
title: '`res_reg.def`'
status: filled
source_hash: 72133c280b3a7a48
version_label: SWAT+ 62.0.0
---

**Primary target:** `rcu_cal(:)` (array of `type cataloging_units`)  
**Read by:** [sym:res_read_elements]

## Bottom Line

The file `res_reg.def` defines reservoir cataloging units (regions) used for reservoir calibration and output grouping.

It is optional and only read if the file exists or is specified in the input registry `in_regs%def_res_reg`.

The reader `res_read_elements` loads this file, storing data into the array `rcu_cal` of type `cataloging_units`.

| Module | Role for this file |
| --- | --- |
| [sym:input_file_module] | Provides the input file path variables such as `in_regs%def_res_reg` used to locate `res_reg.def`. |
| [sym:maximum_data_module] | Provides the global maximum data structure `db_mx` which stores counts like `db_mx%res_reg` for number of reservoir regions. |
| [sym:calibration_data_module] | Defines the derived type `cataloging_units` and the array `rcu_cal` where the file data is stored. |
| [sym:hydrograph_module] | Provides the spatial object `sp_ob` used for counts like `sp_ob%hru` and `sp_ob%res` to allocate arrays. |
| [sym:reservoir_module] | Provides reservoir-related data structures and variables used in the reading and processing of reservoir cataloging units. |

## File Variables

The file `res_reg.def` contains records defining reservoir cataloging units (regions) for calibration and output purposes. Each record corresponds to one cataloging unit and is read into an element of the `rcu_cal` array of type `cataloging_units`. The file format includes a header block followed by multiple records with fields such as name, area, number of HRUs, and land use information.

| Col | Header | Target | Type | Units | Meaning |
| --- | --- | --- | --- | --- | --- |
| 2 |  | `rcu_cal%name` | character(len=16) |  | name of region - (number of regions = db_mx%lsu_reg) |
| 3 |  | `rcu_cal%area_ha` | real | hectares | area of landscape cataloging unit -hectares |
| 4 |  | `rcu_cal%num_tot` | integer |  | number of hru"s in each region |
| 5 |  | `rcu_cal%num` | integer |  | hru"s that are included in the region |
| 6 |  | `rcu_cal%nlum` | integer |  | number of land use and mgt in the region |
| 7 |  | `rcu_cal%lumc` | character(len=16) |  | land use groups |
| 8 |  | `rcu_cal%lum_num` | integer |  | db number of land use in the region - dimensioned by lum in the region |
| 9 |  | `rcu_cal%lum_num_tot` | integer |  | db number of land use in the region each year- dimensioned by lum in database |
| 10 |  | `rcu_cal%lum_ha` | real | hectares | area (ha) of land use in the region - dimensioned by lum in the region |
| 11 |  | `rcu_cal%lum_ha_tot` | real | hectares | sum of area (ha) of land use in the region each year- dimensioned by lum in database |
| 12 |  | `rcu_cal%hru_ha` | real | hectares | area (ha) of hrus in the region |

## Sample

```text
Example record block from `res_reg.def` (fields separated by spaces):
1 RegionA 1500.0 5 10 20 30 40 50 60 70 80
Where fields correspond to: record id, name, area_ha, num_tot, num array, nlum, lumc, lum_num, lum_num_tot, lum_ha, lum_ha_tot, hru_ha
```

## Read Pattern

```fortran
open (107,file=in_regs%def_res_reg)
read (107,*,iostat=eof) titldum
read (107,*,iostat=eof) mreg
read (107,*,iostat=eof) header
read (107,*,iostat=eof) k, rcu_cal(i)%name, rcu_cal(i)%area_ha, nspu
backspace (107)
read (107,*,iostat=eof) k, rcu_cal(i)%name, rcu_cal(i)%area_ha, nspu, (elem_cnt(isp), isp = 1, nspu)
```

## I/O Operations

| Direction | Op | Unit | Statement |
| --- | --- | --- | --- |
| File setup | `open` | 107 | `open (107,file=in_regs%def_res_reg)` |
| Input | `read` | 107 | `read (107,*,iostat=eof) titldum` |
| Input | `read` | 107 | `read (107,*,iostat=eof) mreg` |
| Input | `read` | 107 | `read (107,*,iostat=eof) header` |
| Input | `read` | 107 | `read (107,*,iostat=eof) k, rcu_cal(i)%name, rcu_cal(i)%area_ha, nspu` |
| File control | `backspace` | 107 | `backspace (107)` |
| Input | `read` | 107 | `read (107,*,iostat=eof) k, rcu_cal(i)%name, rcu_cal(i)%area_ha, nspu, (elem_cnt(isp), isp = 1, nspu)` |

## Readers

| Procedure | Operations | Role |
| --- | --- | --- |
| [sym:res_read_elements] | backspace, open, read | Reads the reservoir cataloging units definition file `res_reg.def` if it exists, parsing header information and multiple records into the array `rcu_cal` of type `cataloging_units`. It handles allocation of arrays for HRUs and land use counts per region, and sets global counts in `db_mx%res_reg`. |

## Review Notes

- Draft input-file overlay generated from static source facts; review and complete the remaining fields before promotion.
- The file `res_reg.def` is optional and only read if it exists or is specified in the input registry.
- The reader `res_read_elements` uses `in_regs%def_res_reg` to locate this file and reads reservoir cataloging unit data into `rcu_cal`.
- The file format includes a header block and multiple records with fields for region name, area, HRU counts, and land use data.
- The sample read format example is illustrative; actual data format may vary and should be verified with real datasets.
