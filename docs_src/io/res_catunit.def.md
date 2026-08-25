---
kind: io
source_symbols:
- res_read_elements
title: '`res_catunit.def`'
status: filled
source_hash: 72133c280b3a7a48
version_label: SWAT+ 62.0.0
---

**Primary target:** `rcu_out(:)` (array of `type landscape_units`)  
**Read by:** [sym:res_read_elements]

## Bottom Line

The file `res_catunit.def` defines landscape cataloging units (regions) used in the model, specifying their names, areas, and the HRUs (hydrologic response units) included in each region.

This file is optional and is read by the `res_read_elements` subroutine.

It configures the model state related to landscape units for reservoir and regional hydrologic calculations.

| Module | Role for this file |
| --- | --- |
| [sym:input_file_module] | Provides the `in_regs` variable which contains file paths such as `def_res` for this input file. |
| [sym:maximum_data_module] | Provides the `db_mx` variable used to store counts such as `res_out` and `res_reg` for the number of regions read. |
| [sym:calibration_data_module] | Defines the `type landscape_units` and arrays `rcu_out`, `rcu_cal`, and `rcu_reg` where the file data is stored. |
| [sym:hydrograph_module] | Provides the `sp_ob` variable which contains counts like `hru` and `res` used for allocation when no subunits are specified. |
| [sym:reservoir_module] | No direct variables or types from this module are visibly used in the reader for this file. |

## File Variables

The file `res_catunit.def` contains records defining landscape cataloging units (regions). Each record includes a region identifier, name, area in hectares, the number of subunits (HRUs) in the region, and optionally a list of HRU indices included in the region. These map to the `rcu_out` array of `type landscape_units` in the model.

| Col | Header | Target | Type | Units | Meaning |
| --- | --- | --- | --- | --- | --- |
| 2 |  | `rcu_out%name` | character(len=16) |  | name of region - (number of regions = db_mx%lsu_out) |
| 3 |  | `rcu_out%area_ha` | real |  | area of landscape cataloging unit -hectares |
| 4 |  | `rcu_out%num_tot` | integer |  | number of hru"s in each region |
| 5 |  | `rcu_out%num` | integer |  | hru"s that are included in the region |

## Sample

```text
1 Basin1 1500.0 3 10 20 30
2 Basin2 2500.0 0
```

## Read Pattern

```fortran
open (107,file=in_regs%def_res)
read (107,*,iostat=eof) titldum
read (107,*,iostat=eof) mreg
read (107,*,iostat=eof) header
read (107,*,iostat=eof) k, rcu_out(i)%name, rcu_out(i)%area_ha, nspu
backspace (107)
read (107,*,iostat=eof) k, rcu_out(i)%name, rcu_out(i)%area_ha, nspu, (elem_cnt(isp), isp = 1, nspu)
```

## I/O Operations

| Direction | Op | Unit | Statement |
| --- | --- | --- | --- |
| File setup | `open` | 107 | `open (107,file=in_regs%def_res)` |
| Input | `read` | 107 | `read (107,*,iostat=eof) titldum` |
| Input | `read` | 107 | `read (107,*,iostat=eof) mreg` |
| Input | `read` | 107 | `read (107,*,iostat=eof) header` |
| Input | `read` | 107 | `read (107,*,iostat=eof) k, rcu_out(i)%name, rcu_out(i)%area_ha, nspu` |
| File control | `backspace` | 107 | `backspace (107)` |
| Input | `read` | 107 | `read (107,*,iostat=eof) k, rcu_out(i)%name, rcu_out(i)%area_ha, nspu, (elem_cnt(isp), isp = 1, nspu)` |

## Readers

| Procedure | Operations | Role |
| --- | --- | --- |
| [sym:res_read_elements] | backspace, open, read | Reads the `res_catunit.def` file to load landscape cataloging units (regions) into the `rcu_out` array of `type landscape_units`. It reads region metadata including name, area, and the number of HRUs, then reads the list of HRUs included in each region if specified. It also sets up related calibration and reservoir region arrays. |

## Review Notes

- Draft input-file overlay generated from static source facts; review and complete the remaining fields before promotion.
- The file is optional as indicated by the existence check and conditional reading in `res_read_elements`.
- The sample read format is inferred from the read statements and typical data structure; actual example records should be verified from a real dataset.
