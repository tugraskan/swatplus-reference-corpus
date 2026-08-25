---
kind: io
source_symbols:
- aqu_read_elements
title: '`aqu_catunit.def`'
status: filled
source_hash: 2e139e69eda0a1d5
version_label: SWAT+ 62.0.0
---

**Primary target:** `acu_out(:)` and `acu_reg(:)` (arrays of `type landscape_units`)  
**Read by:** [sym:aqu_read_elements]

## Bottom Line

The file `aqu_catunit.def` defines landscape cataloging units (regions) for aquifer modeling, specifying their names, areas, and included HRUs (hydrologic response units).

It is an optional input file checked for existence before reading.

The primary reader for this file is the subroutine `aqu_read_elements`.

| Module | Role for this file |
| --- | --- |
| [sym:input_file_module] | Provides the `in_regs` variable which contains the file path strings `def_aqu` and `def_aqu_reg` used to open `aqu_catunit.def`. |
| [sym:calibration_data_module] | Provides the derived type `landscape_units` and the arrays `acu_out`, `acu_reg`, and `acu_cal` where the file data is stored and processed. |
| [sym:hydrograph_module] | Provides the `sp_ob` variable used to determine the number of HRUs (`sp_ob%hru`) and aquifers (`sp_ob%aqu`) when no subunits are specified in the file. |
| [sym:aquifer_module] | No direct variables or types from this module are explicitly used in `aqu_read_elements` for reading or storing this file. |
| [sym:maximum_data_module] | Provides the `db_mx` variable used to store counts of landscape cataloging units read from the file (`db_mx%aqu_out` and `db_mx%aqu_reg`). |

## File Variables

The file `aqu_catunit.def` contains records defining landscape cataloging units (regions) for aquifer modeling. Each record includes a region identifier, name, area in hectares, and the number of hydrologic response units (HRUs) or elements included in that region. The reader maps these records into arrays of `type landscape_units` (`acu_out` and `acu_reg`).

| Col | Header | Target | Type | Units | Meaning |
| --- | --- | --- | --- | --- | --- |
| 2 |  | `acu_out%name` | character(len=16) |  | name of region - (number of regions = db_mx%lsu_out) |
| 3 |  | `acu_out%area_ha` | real | hectares | area of landscape cataloging unit in hectares |
| 4 |  | `acu_out%num_tot` | integer |  | total number of HRUs or elements in the region |
| 5 |  | `acu_out%num` | integer |  | indices of HRUs included in the region |
| 2 |  | `acu_reg%name` | character(len=16) |  | name of region - (number of regions = db_mx%lsu_out) |
| 3 |  | `acu_reg%area_ha` | real | hectares | area of landscape cataloging unit in hectares |
| 4 |  | `acu_reg%num_tot` | integer |  | total number of HRUs or elements in the region |
| 5 |  | `acu_reg%num` | integer |  | indices of HRUs included in the region |

## Sample

```text
1 RegionA 1500.0 3 10 20 30
2 RegionB 2500.5 0
```

## Read Pattern

```fortran
open (107,file=in_regs%def_aqu)
read (107,*,iostat=eof) titldum
read (107,*,iostat=eof) mreg
read (107,*,iostat=eof) header
read (107,*,iostat=eof) k, acu_out(i)%name, acu_out(i)%area_ha, nspu
backspace (107)
read (107,*,iostat=eof) k, acu_out(i)%name, acu_out(i)%area_ha, nspu, (elem_cnt(isp), isp = 1, nspu)
read (107,*,iostat=eof) k, acu_reg(i)%name, acu_reg(i)%area_ha, nspu
read (107,*,iostat=eof) k, acu_reg(i)%name, acu_reg(i)%area_ha, nspu, (elem_cnt(isp), isp = 1, nspu)
```

## I/O Operations

| Direction | Op | Unit | Statement |
| --- | --- | --- | --- |
| File setup | `open` | 107 | `open (107,file=in_regs%def_aqu)` |
| Input | `read` | 107 | `read (107,*,iostat=eof) titldum` |
| Input | `read` | 107 | `read (107,*,iostat=eof) mreg` |
| Input | `read` | 107 | `read (107,*,iostat=eof) header` |
| Input | `read` | 107 | `read (107,*,iostat=eof) k, acu_out(i)%name, acu_out(i)%area_ha, nspu` |
| File control | `backspace` | 107 | `backspace (107)` |
| Input | `read` | 107 | `read (107,*,iostat=eof) k, acu_out(i)%name, acu_out(i)%area_ha, nspu, (elem_cnt(isp), isp = 1, nspu)` |
| File setup | `open` | 107 | `open (107,file=in_regs%def_aqu)` |
| Input | `read` | 107 | `read (107,*,iostat=eof) titldum` |
| Input | `read` | 107 | `read (107,*,iostat=eof) mreg` |
| Input | `read` | 107 | `read (107,*,iostat=eof) header` |
| Input | `read` | 107 | `read (107,*,iostat=eof) k, acu_reg(i)%name, acu_reg(i)%area_ha, nspu` |
| File control | `backspace` | 107 | `backspace (107)` |
| Input | `read` | 107 | `read (107,*,iostat=eof) k, acu_reg(i)%name, acu_reg(i)%area_ha, nspu, (elem_cnt(isp), isp = 1, nspu)` |

## Readers

| Procedure | Operations | Role |
| --- | --- | --- |
| [sym:aqu_read_elements] | open, read, backspace | Reads the `aqu_catunit.def` file to load landscape cataloging units (regions) into the arrays `acu_out` and `acu_reg`. It reads region counts, names, areas, and the number of subunits (HRUs or elements) included in each region, allocating arrays accordingly. It also initializes calibration structures and reads element data if available. |

## Review Notes

- The file `aqu_catunit.def` is optional and only read if it exists or the filename is not 'null'.
- If the number of subunits (nspu) is zero, all HRUs from `sp_ob%hru` are included by default.
- The reader also reads a related file `def_aqu_reg` for aquifer soft calibration or output regions, using the same file format and storing into `acu_reg`.
- The sample read format is inferred from the read statements and typical usage; no explicit example is present in the source.
- The reader allocates arrays and sets counts in `db_mx` to track the number of landscape units read.
