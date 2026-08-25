---
kind: io
source_symbols:
- reg_read_elements
title: '`ls_reg.ele`'
status: filled
source_hash: 986472f05abcaf8c
version_label: SWAT+ 62.0.0
---

**Primary target:** `reg_elem(:)` (array of `type landscape_region_elements`)  
**Read by:** [sym:reg_read_elements]

## Bottom Line

The file `ls_reg.ele` defines landscape region elements, which are spatial units such as HRUs (Hydrologic Response Units), land use units, or other object types used in the SWAT+ model for landscape cataloging and regional output.

It is an optional input file that is read by the `reg_read_elements` subroutine.

This file configures the spatial elements that compose landscape cataloging units and regions, including their names, areas, object types, and object type numbers.

| Module | Role for this file |
| --- | --- |
| [sym:input_file_module] | Provides the `in_regs` variable which contains the file path for `ele_reg` (the `ls_reg.ele` file) used to open and read this file. |
| [sym:maximum_data_module] | Provides `db_mx` which stores the maximum counts such as `reg_elem` array size and `lsu_reg` count used during allocation and indexing. |
| [sym:calibration_data_module] | Defines the derived type `landscape_region_elements` and the array `reg_elem` where each record from the file is stored. |
| [sym:landuse_data_module] | Provides `lsu_reg` and related land use group data structures that are allocated and referenced during reading and processing of elements. |
| [sym:hydrograph_module] | Used indirectly for hydrologic response unit (HRU) data referenced by elements, though no direct variables are read or written here. |
| [sym:hru_module] | Provides the `hru` type and `ihru` index used to assign HRU areas and numbers to regions based on element data. |
| [sym:output_landscape_module] | Provides output landscape data structures such as `region` which are allocated and populated with element and HRU information during reading. |

## File Variables

The `ls_reg.ele` file contains records describing landscape region elements, each with an identifier, name, area in hectares, object type, and an object type number. These records are read sequentially and stored into the `reg_elem` array of type `landscape_region_elements`.

| Col | Header | Target | Type | Units | Meaning |
| --- | --- | --- | --- | --- | --- |
| 2 |  | `reg_elem%name` | character(len=16) |  | Name identifier of the landscape region element |
| 3 |  | `reg_elem%ha` | real | hectares | Area of the region element in hectares |
| 4 |  | `reg_elem%obj` | integer |  | Object number identifier |
| 5 |  | `reg_elem%obtyp` | character (len=3) |  | Object type code such as 'hru', 'hru_lte', 'lsu', etc. |
| 6 |  | `reg_elem%obtypno` | integer |  | Object type number, e.g., number of HRU LTEs or first HRU LTE command |

## Sample

```text
1  ElementName1  12.5  hru  101
2  ElementName2  8.3   lsu  5
3  ElementName3  15.0  hru_lte  2
```

## Read Pattern

```fortran
open (107,file=in_regs%ele_reg)
read (107,*,iostat=eof) titldum
read (107,*,iostat=eof) header
read (107,*,iostat=eof) i
rewind (107)
backspace (107)
read (107,*,iostat=eof) k, reg_elem(i)%name, reg_elem(i)%ha, reg_elem(i)%obtyp, reg_elem(i)%obtypno
```

## I/O Operations

| Direction | Op | Unit | Statement |
| --- | --- | --- | --- |
| File setup | `open` | 107 | `open (107,file=in_regs%ele_reg)` |
| Input | `read` | 107 | `read (107,*,iostat=eof) titldum` |
| Input | `read` | 107 | `read (107,*,iostat=eof) header` |
| Input | `read` | 107 | `read (107,*,iostat=eof) i` |
| File control | `rewind` | 107 | `rewind (107)` |
| Input | `read` | 107 | `read (107,*,iostat=eof) titldum` |
| Input | `read` | 107 | `read (107,*,iostat=eof) header` |
| Input | `read` | 107 | `read (107,*,iostat=eof) i` |
| File control | `backspace` | 107 | `backspace (107)` |
| Input | `read` | 107 | `read (107,*,iostat=eof) k, reg_elem(i)%name, reg_elem(i)%ha, reg_elem(i)%obtyp, reg_elem(i)%obtypno` |
| File control | `close` | 107 | `close (107)` |

## Readers

| Procedure | Operations | Role |
| --- | --- | --- |
| [sym:reg_read_elements] | backspace, close, open, read, rewind | Reads the `ls_reg.ele` file to load landscape region elements into the `reg_elem` array. It opens the file, reads header lines, determines the maximum element index, allocates the `reg_elem` array, and then reads each element's data fields (name, area, object type, object type number). It also updates related landscape and region data structures with element counts and HRU assignments. |

## Review Notes

- Draft input-file overlay generated from static source facts; review and complete the remaining fields before promotion.
- The file is optional as indicated by the existence check and conditional reading in `reg_read_elements`.
- The `reg_read_elements` subroutine reads `ls_reg.ele` and populates the `reg_elem` array of type `landscape_region_elements`.
- The sample record format is inferred from the read statement and variable types; actual example records should be verified from a reference dataset.
