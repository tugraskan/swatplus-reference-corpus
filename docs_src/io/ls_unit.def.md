---
kind: io
source_symbols:
- lsu_read_elements
title: '`ls_unit.def`'
status: filled
source_hash: 01a1bc861a37e0bb
version_label: SWAT+ 62.0.0
---

**Primary target:** `lsu_out(:)` (array of `type landscape_units`)  
**Read by:** [sym:lsu_read_elements]

## Bottom Line

The file `ls_unit.def` defines landscape cataloging units (regions or subbasins) for the SWAT+ model.

It is an optional input file checked for existence before reading.

The file configures the landscape units' names, areas, and associated HRU counts, which are stored in the `lsu_out` array.

The primary reader for this file is the subroutine `lsu_read_elements`.

| Module | Role for this file |
| --- | --- |
| [sym:input_file_module] | Provides the `in_regs` variable that contains the filename `def_lsu` for this input file. |
| [sym:maximum_data_module] | Provides the `db_mx` variable that stores the total number of landscape units (`lsu_out`) and elements (`lsu_elem`). |
| [sym:calibration_data_module] | Defines the `type landscape_units` and the `lsu_out` array where the file data is stored. |
| [sym:hydrograph_module] | Provides hydrologic response unit (HRU) related arrays allocated for each landscape unit during reading. |
| [sym:output_landscape_module] | Provides output arrays related to landscape water balance allocated per landscape unit. |

## File Variables

The `ls_unit.def` file contains records defining landscape cataloging units, each with a name, area in hectares, total number of HRUs, and a list of HRUs included in the unit. These records are read sequentially and stored into the `lsu_out` array of `type landscape_units`.

| Col | Header | Target | Type | Units | Meaning |
| --- | --- | --- | --- | --- | --- |
| 2 |  | `lsu_out%name` | character(len=16) |  | name of region - (number of regions = db_mx%lsu_out) |
| 3 |  | `lsu_out%area_ha` | real |  | area of landscape cataloging unit -hectares |
| 4 |  | `lsu_out%num_tot` | integer |  | number of hru"s in each region |
| 5 |  | `lsu_out%num` | integer |  | hru"s that are included in the region |

## Sample

```text
1 basin1           1234.56 3
1 basin1           1234.56 3 10 20 30
2 basin2           789.01  2
2 basin2           789.01  2 40 50
```

## Read Pattern

```fortran
open (107,file=in_regs%def_lsu)
read (107,*,iostat=eof) titldum
read (107,*,iostat=eof) mlsu
read (107,*,iostat=eof) header
read (107,*,iostat=eof) k, lsu_out(i)%name, lsu_out(i)%area_ha, nspu
backspace (107)
read (107,*,iostat=eof) k, lsu_out(i)%name, lsu_out(i)%area_ha, nspu, (elem_cnt(isp), isp = 1, nspu)
```

## I/O Operations

| Direction | Op | Unit | Statement |
| --- | --- | --- | --- |
| File setup | `open` | 107 | `open (107,file=in_regs%def_lsu)` |
| Input | `read` | 107 | `read (107,*,iostat=eof) titldum` |
| Input | `read` | 107 | `read (107,*,iostat=eof) mlsu` |
| Input | `read` | 107 | `read (107,*,iostat=eof) header` |
| Input | `read` | 107 | `read (107,*,iostat=eof) k, lsu_out(i)%name, lsu_out(i)%area_ha, nspu` |
| File control | `backspace` | 107 | `backspace (107)` |
| Input | `read` | 107 | `read (107,*,iostat=eof) k, lsu_out(i)%name, lsu_out(i)%area_ha, nspu, (elem_cnt(isp), isp = 1, nspu)` |

## Readers

| Procedure | Operations | Role |
| --- | --- | --- |
| [sym:lsu_read_elements] | open, read, backspace | Reads the `ls_unit.def` file to load landscape cataloging units into the `lsu_out` array, including their names, areas, and HRU membership counts. It also allocates related hydrologic and output arrays per landscape unit. |

## Review Notes

- The file `ls_unit.def` is optional and only read if it exists or is not set to "null".
- The reader allocates arrays for landscape units and related hydrologic response units (HRUs) based on the file contents.
- The sample read format is inferred from the read statements and typical usage; exact example data was not found in the source.
- The reader also reads a secondary file `ele_lsu` for element-level data, but that is outside the scope of this input file overlay.
