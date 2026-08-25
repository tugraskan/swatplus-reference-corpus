---
kind: io
source_symbols:
- lsu_read_elements
title: '`ls_unit.ele`'
status: filled
source_hash: 01a1bc861a37e0bb
version_label: SWAT+ 62.0.0
---

**Primary target:** `lsu_elem(:)` (array of `type landscape_elements`)  
**Read by:** [sym:lsu_read_elements]

## Bottom Line

The `ls_unit.ele` file configures landscape cataloging unit elements, specifying their identifiers, types, and fractional contributions to basin, response unit, and calibration regions.

This file is optional and is read by the `lsu_read_elements` subroutine.

| Module | Role for this file |
| --- | --- |
| [sym:input_file_module] | provides the `in_regs` variable which contains the file path `ele_lsu` used to open the `ls_unit.ele` file. |
| [sym:maximum_data_module] | provides the `db_mx` variable which stores counts such as `db_mx%lsu_elem` for the number of elements read. |
| [sym:calibration_data_module] | provides the `lsu_elem` array of `type landscape_elements` where the file records are stored. |
| [sym:hydrograph_module] | no direct variables or types from this module are used for reading or storing this file in the `lsu_read_elements` routine. |
| [sym:output_landscape_module] | provides the `lsu_out` array and related landscape unit output structures, but these are not directly used for reading `ls_unit.ele`. |

## File Variables

The `ls_unit.ele` file contains records describing landscape elements, each with an identifier, type, and fractional area contributions. Each record is read into an element of the `lsu_elem` array of `type landscape_elements`.

| Col | Header | Target | Type | Units | Meaning |
| --- | --- | --- | --- | --- | --- |
| 2 |  | `lsu_elem%name` | character(len=16) |  | element name or identifier |
| 3 |  | `lsu_elem%obj` | integer |  | object number |
| 4 |  | `lsu_elem%obtyp` | character (len=3) |  | object type- 1=hru, 2=hru_lte, 11=export coef, etc |
| 5 |  | `lsu_elem%obtypno` | integer |  | 2-number of hru_lte's or 1st hru_lte command |
| 6 |  | `lsu_elem%bsn_frac` | real |  | fraction of element in basin (expansion factor) |
| 7 |  | `lsu_elem%ru_frac` | real |  | fraction of element in ru (expansion factor) |
| 8 |  | `lsu_elem%reg_frac` | real |  | fraction of element in calibration region (expansion factor) |

## Sample

```text
1 ELE001 HRU 1 0.75 0.60 0.80
2 ELE002 LTE 2 0.25 0.40 0.20
```

## Read Pattern

```fortran
open (107,file=in_regs%ele_lsu)
read (107,*,iostat=eof) titldum
read (107,*,iostat=eof) header
read (107,*,iostat=eof) i
rewind (107)
backspace (107)
read (107,*,iostat=eof) k, lsu_elem(i)%name, lsu_elem(i)%obtyp, lsu_elem(i)%obtypno, lsu_elem(i)%bsn_frac, lsu_elem(i)%ru_frac
```

## I/O Operations

| Direction | Op | Unit | Statement |
| --- | --- | --- | --- |
| File setup | `open` | 107 | `open (107,file=in_regs%ele_lsu)` |
| Input | `read` | 107 | `read (107,*,iostat=eof) titldum` |
| Input | `read` | 107 | `read (107,*,iostat=eof) header` |
| Input | `read` | 107 | `read (107,*,iostat=eof) i` |
| File control | `rewind` | 107 | `rewind (107)` |
| Input | `read` | 107 | `read (107,*,iostat=eof) titldum` |
| Input | `read` | 107 | `read (107,*,iostat=eof) header` |
| Input | `read` | 107 | `read (107,*,iostat=eof) i` |
| File control | `backspace` | 107 | `backspace (107)` |
| Input | `read` | 107 | `read (107,*,iostat=eof) k, lsu_elem(i)%name, lsu_elem(i)%obtyp, lsu_elem(i)%obtypno, lsu_elem(i)%bsn_frac, lsu_elem(i)%ru_frac` |
| File control | `close` | 107 | `close (107)` |

## Readers

| Procedure | Operations | Role |
| --- | --- | --- |
| [sym:lsu_read_elements] | backspace, close, open, read, rewind | Reads the `ls_unit.ele` file to populate the `lsu_elem` array with landscape element records, including their names, types, and fractional area contributions. |

## Review Notes

- Draft input-file overlay generated from static source facts; review and complete the remaining fields before promotion.
- The `reg_frac` field is declared in the type but is not explicitly read in the `lsu_read_elements` routine; this may indicate partial reading or a default value usage.
- The sample read format is inferred from typical record structure but no explicit example record was found in the source.
