---
kind: io
source_symbols:
- rec_read_elements
title: '`rec_catunit.ele`'
status: filled
source_hash: 4986560811349e04
version_label: SWAT+ 62.0.0
---

**Primary target:** `pcu_elem(:)` (array of `type landscape_elements`)  
**Read by:** [sym:rec_read_elements]

## Bottom Line

The file `rec_catunit.ele` configures landscape cataloging unit elements, representing spatial units such as HRUs or LTEs with their fractional areas in basins, response units, and calibration regions.

It is an optional input file, read if present, and loaded by the `rec_read_elements` subroutine.

This file provides detailed element-level data that supports calibration and spatial aggregation in SWAT+.

| Module | Role for this file |
| --- | --- |
| [sym:input_file_module] | Provides the `in_regs` variable which holds file path strings such as `ele_psc` for the elements file. |
| [sym:maximum_data_module] | Provides `sp_ob` which contains counts like `hru` and `recall` used for default element allocations. |
| [sym:calibration_data_module] | Defines the `pcu_elem` array of `type landscape_elements` where the file records are stored. |
| [sym:hydrograph_module] | No direct variables or types from this module are used in reading or storing this file. |

## File Variables

The file `rec_catunit.ele` contains records of landscape elements, each with an ID, name, object type and number, and fractional area coverage in basin, response unit, and calibration region. These map directly to the `pcu_elem` array of `type landscape_elements` in Fortran.

| Col | Header | Target | Type | Units | Meaning |
| --- | --- | --- | --- | --- | --- |
| 2 |  | `pcu_elem%name` | character(len=16) |  | element name |
| 3 |  | `pcu_elem%obj` | integer |  | object number |
| 4 |  | `pcu_elem%obtyp` | character (len=3) |  | object type- 1=hru, 2=hru_lte, 11=export coef, etc |
| 5 |  | `pcu_elem%obtypno` | integer |  | 2-number of hru_lte"s or 1st hru_lte command |
| 6 |  | `pcu_elem%bsn_frac` | real |  | fraction of element in basin (expansion factor) |
| 7 |  | `pcu_elem%ru_frac` | real |  | fraction of element in ru (expansion factor) |
| 8 |  | `pcu_elem%reg_frac` | real |  | fraction of element in calibration region (expansion factor) |

## Sample

```text
1 ELE001 1 HRU 0 1.0 1.0 1.0
2 ELE002 2 LTE 5 0.8 0.7 0.9
```

## Read Pattern

```fortran
open (107,file=in_regs%ele_psc)
read (107,*,iostat=eof) titldum
read (107,*,iostat=eof) header
read (107,*,iostat=eof) i
rewind (107)
backspace (107)
read (107,*,iostat=eof) k, pcu_elem(i)%name, pcu_elem(i)%obtyp, pcu_elem(i)%obtypno, pcu_elem(i)%bsn_frac, pcu_elem(i)%ru_frac, pcu_elem(i)%reg_frac
```

## I/O Operations

| Direction | Op | Unit | Statement |
| --- | --- | --- | --- |
| File setup | `open` | 107 | `open (107,file=in_regs%ele_psc)` |
| Input | `read` | 107 | `read (107,*,iostat=eof) titldum` |
| Input | `read` | 107 | `read (107,*,iostat=eof) header` |
| Input | `read` | 107 | `read (107,*,iostat=eof) i` |
| File control | `rewind` | 107 | `rewind (107)` |
| File control | `backspace` | 107 | `backspace (107)` |
| Input | `read` | 107 | `read (107,*,iostat=eof) k, pcu_elem(i)%name, pcu_elem(i)%obtyp, pcu_elem(i)%obtypno, pcu_elem(i)%bsn_frac, pcu_elem(i)%ru_frac, pcu_elem(i)%reg_frac` |
| File control | `close` | 107 | `close (107)` |

## Readers

| Procedure | Operations | Role |
| --- | --- | --- |
| [sym:rec_read_elements] | backspace, close, open, read, rewind | Reads the `rec_catunit.ele` file if it exists, determines the number of elements, allocates the `pcu_elem` array accordingly, and loads each element record into `pcu_elem`. This subroutine integrates element data into the landscape cataloging units for calibration and spatial aggregation. |

## Review Notes

- Draft input-file overlay generated from static source facts; review and complete the remaining fields before promotion.
- The file is optional and read only if present, as indicated by the inquire and conditional open in `rec_read_elements`.
- The sample read format is inferred from the read statement and typical element records; no explicit example was found in the source.
- No direct use of hydrograph_module variables was found in the reading or storing of this file.
