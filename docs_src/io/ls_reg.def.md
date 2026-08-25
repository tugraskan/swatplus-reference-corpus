---
kind: io
source_symbols:
- reg_read_elements
title: '`ls_reg.def`'
status: filled
source_hash: 986472f05abcaf8c
version_label: SWAT+ 62.0.0
---

**Primary target:** `lum_grp(:)` (array of `type land_use_mgt_groups`)  
**Read by:** [sym:reg_read_elements]

## Bottom Line

The file `ls_reg.def` defines landscape cataloging units (regions) and their land use groups for SWAT+.

It is used to configure regional landscape units and their associated land use management groups for soft calibration and output.

This file is optional and is read by the `reg_read_elements` subroutine.

| Module | Role for this file |
| --- | --- |
| [sym:input_file_module] | Provides `in_regs` which contains the file paths `def_reg` and `ele_reg` used to open `ls_reg.def` and related element files. |
| [sym:maximum_data_module] | Provides `db_mx` which stores maximum counts such as `db_mx%lsu_reg` and `db_mx%landuse` that are set during reading. |
| [sym:calibration_data_module] | Provides the `lsu_reg` array of type `landscape_units` where region records are stored. |
| [sym:landuse_data_module] | Provides the `lum_grp` array of type `land_use_mgt_groups` where land use group records are stored. |
| [sym:hydrograph_module] | Used but no direct variables or types from this module are assigned in this reader. |
| [sym:hru_module] | Provides `hru` and `ihru` types used to assign HRU areas and numbers within regions. |
| [sym:output_landscape_module] | Provides arrays such as `region`, `rwb_d`, `rwb_m`, `rwb_y`, `rwb_a`, `rnb_d`, `rnb_m`, `rnb_y`, `rnb_a`, `rls_d`, `rls_m`, `rls_y`, `rls_a`, `rpw_d`, `rpw_m`, `rpw_y`, `rpw_a` which are allocated and initialized for regional output. |

## File Variables

The `ls_reg.def` file contains definitions of landscape cataloging units (regions) and their associated land use management groups. The file is read sequentially with records mapped into arrays of derived types `lum_grp` (land use groups) and `lsu_reg` (landscape units). Each record includes identifiers, names, areas, and counts of HRUs or elements within regions.

| Col | Header | Target | Type | Units | Meaning |
| --- | --- | --- | --- | --- | --- |
| 2 |  | `lum_grp%num` | integer |  | Identifier number for the land use management group |
| 3 |  | `lum_grp%name` | character(len=40) |  | Name of the land use group |
| 2 |  | `lsu_reg%name` | character(len=16) |  | Name of the landscape cataloging unit (region) |
| 3 |  | `lsu_reg%area_ha` | real | hectares | Area of the landscape cataloging unit in hectares |
| 4 |  | `lsu_reg%num_tot` | integer |  | Total number of HRUs or elements in the region |
| 5 |  | `lsu_reg%num` | integer |  | Array of HRU or element identifiers included in the region |

## Sample

```text
Example snippet from `ls_reg.def` (format inferred from source reads):
Title line (string)
Number of regions (mreg), number of land use groups (mlug)
Region ID, land use group number, land use group names (mlug entries)
Header line (string)
Region index, region name, region area (ha), number of subunits (nspu)
Region index, region name, region area (ha), number of subunits (nspu), element counts per subunit
```

## Read Pattern

```fortran
open (107,file=in_regs%def_reg)
read (107,*,iostat=eof) titldum
read (107,*,iostat=eof) mreg, mlug
backspace (107)
read (107,*,iostat=eof) i, lum_grp%num, (lum_grp%name(ilum), ilum = 1, mlug)
read (107,*,iostat=eof) header
read (107,*,iostat=eof) k, lsu_reg(i)%name, lsu_reg(i)%area_ha, nspu
read (107,*,iostat=eof) k, lsu_reg(i)%name, lsu_reg(i)%area_ha, nspu, (elem_cnt(isp), isp = 1, nspu)
```

## I/O Operations

| Direction | Op | Unit | Statement |
| --- | --- | --- | --- |
| File setup | `open` | 107 | `open (107,file=in_regs%def_reg)` |
| Input | `read` | 107 | `read (107,*,iostat=eof) titldum` |
| Input | `read` | 107 | `read (107,*,iostat=eof) mreg, mlug` |
| File control | `backspace` | 107 | `backspace (107)` |
| Input | `read` | 107 | `read (107,*,iostat=eof) i, lum_grp%num, (lum_grp%name(ilum), ilum = 1, mlug)` |
| Input | `read` | 107 | `read (107,*,iostat=eof) header` |
| Input | `read` | 107 | `read (107,*,iostat=eof) k, lsu_reg(i)%name, lsu_reg(i)%area_ha, nspu` |
| File control | `backspace` | 107 | `backspace (107)` |
| Input | `read` | 107 | `read (107,*,iostat=eof) k, lsu_reg(i)%name, lsu_reg(i)%area_ha, nspu, (elem_cnt(isp), isp = 1, nspu)` |

## Readers

| Procedure | Operations | Role |
| --- | --- | --- |
| [sym:reg_read_elements] | open, read, backspace, close | Reads the `ls_reg.def` file to load landscape cataloging units (regions) and their land use groups into memory. It allocates arrays for regions, land use groups, and regional output structures, and sets up HRU mappings within regions. |

## Review Notes

- The file `ls_reg.def` is optional and used to define landscape cataloging units and their land use groups for regional soft calibration and output.
- The reader `reg_read_elements` handles reading this file and allocates associated arrays and output structures.
- The exact format of the file is inferred from the read statements; no explicit sample data was found in the source.
- The source code uses backspace to reread some records, indicating a multi-pass read pattern.
- Some variables and arrays such as `region`, `rwb_a`, `rnb_a`, `rls_a`, and `rpw_a` are allocated per region and per land use group for output bookkeeping.
- The reader also reads element counts per subunit and sets up HRU mappings within regions.
- No explicit error handling or mandatory file presence is enforced; the file is read only if it exists or is not set to "null".
