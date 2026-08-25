---
kind: io
source_symbols:
- rec_read_elements
title: '`rec_catunit.def`'
status: filled
source_hash: 4986560811349e04
version_label: SWAT+ 62.0.0
---

**Primary target:** `pcu_out(:)` (array of `type landscape_units`)  
**Read by:** [sym:rec_read_elements]

## Bottom Line

The file `rec_catunit.def` defines landscape cataloging units (regions) for the model, specifying their names, areas, and the HRUs (hydrologic response units) included in each region.

This file is optional; the reader checks for its existence before reading.

The reader subroutine `rec_read_elements` loads this file and stores its data into the `pcu_out` array of `type landscape_units`.

| Module | Role for this file |
| --- | --- |
| [sym:input_file_module] | provides the `in_regs` variable which contains the filename `def_psc` (mapped to `rec_catunit.def`) used to open and read the file. |
| [sym:maximum_data_module] | provides the `db_mx` variable used to store the number of regions read (`db_mx%rec_out`), and possibly other maximum dimension constants. |
| [sym:calibration_data_module] | provides the `pcu_out` array of `type landscape_units` where the file records are stored, and related arrays `pcu_cal` and `pcu_reg` used for region calibration and region data. |
| [sym:hydrograph_module] | provides the `sp_ob` variable used for HRU counts and recall counts when no subregions are defined. |

## File Variables

The file `rec_catunit.def` contains records defining landscape cataloging units (regions). Each record includes a region identifier, a name, area in hectares, the number of subregions (HRUs) included, and optionally a list of HRU counts per subregion. These records are read sequentially and stored into the `pcu_out` array of `type landscape_units`.

| Col | Header | Target | Type | Units | Meaning |
| --- | --- | --- | --- | --- | --- |
| 2 |  | `pcu_out%name` | character(len=16) |  | name of region - (number of regions = db_mx%lsu_out) |
| 3 |  | `pcu_out%area_ha` | real |  | area of landscape cataloging unit -hectares |
| 4 |  | `pcu_out%num_tot` | integer |  | number of hru"s in each region |
| 5 |  | `pcu_out%num` | integer |  | hru"s that are included in the region |

## Sample

```text
1 RegionName1       12345.67 3 10 20 30
2 RegionName2       23456.78 0
```

## Read Pattern

```fortran
open (107,file=in_regs%def_psc)
read (107,*,iostat=eof) titldum
read (107,*,iostat=eof) mreg
read (107,*,iostat=eof) header
read (107,*,iostat=eof) k, pcu_out(i)%name, pcu_out(i)%area_ha, nspu
backspace (107)
read (107,*,iostat=eof) k, pcu_out(i)%name, pcu_out(i)%area_ha, nspu, (elem_cnt(isp), isp = 1, nspu)
```

## I/O Operations

| Direction | Op | Unit | Statement |
| --- | --- | --- | --- |
| File setup | `open` | 107 | `open (107,file=in_regs%def_psc)` |
| Input | `read` | 107 | `read (107,*,iostat=eof) titldum` |
| Input | `read` | 107 | `read (107,*,iostat=eof) mreg` |
| Input | `read` | 107 | `read (107,*,iostat=eof) header` |
| Input | `read` | 107 | `read (107,*,iostat=eof) k, pcu_out(i)%name, pcu_out(i)%area_ha, nspu` |
| File control | `backspace` | 107 | `backspace (107)` |
| Input | `read` | 107 | `read (107,*,iostat=eof) k, pcu_out(i)%name, pcu_out(i)%area_ha, nspu, (elem_cnt(isp), isp = 1, nspu)` |

## Readers

| Procedure | Operations | Role |
| --- | --- | --- |
| [sym:rec_read_elements] | backspace, open, read | Reads the `rec_catunit.def` file (mapped from `in_regs%def_psc`) to load landscape cataloging units (regions) into the `pcu_out` array. It reads the number of regions, then for each region reads the region ID, name, area, and number of subregions (HRUs). If subregions exist, it reads their counts and calls `define_unit_elements` to set up element indices. If no subregions are defined, it assigns all HRUs to the region. This subroutine manages allocation and initialization of region data structures. |

## Review Notes

- Draft input-file overlay generated from static source facts; review and complete the remaining fields before promotion.
- The file `rec_catunit.def` is optional; the reader checks for its existence before reading.
- The sample read format is inferred from the read statements and typical data layout; no explicit example was found in the source.
