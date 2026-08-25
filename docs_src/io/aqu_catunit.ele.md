---
kind: io
source_symbols:
- aqu_read_elements
title: '`aqu_catunit.ele`'
status: filled
source_hash: 2e139e69eda0a1d5
version_label: SWAT+ 62.0.0
---

**Primary target:** `acu_elem(:)` (array of `type landscape_elements`)  
**Read by:** [sym:aqu_read_elements]

## Bottom Line

The file `aqu_catunit.ele` configures landscape cataloging unit elements related to aquifer modeling in SWAT+.

It is optional and only read if present (checked by existence inquiry).

The primary reader that loads this file is `aqu_read_elements`.

| Module | Role for this file |
| --- | --- |
| [sym:input_file_module] | Provides the `in_regs` variable which holds file path strings such as `ele_aqu` used to open `aqu_catunit.ele`. |
| [sym:calibration_data_module] | Defines the derived type `landscape_elements` and the array `acu_elem` where the file records are stored. |
| [sym:hydrograph_module] | No direct variables or types from this module are used in `aqu_read_elements` for reading or storing this file. |
| [sym:aquifer_module] | No direct variables or types from this module are used in `aqu_read_elements` for reading or storing this file. |
| [sym:maximum_data_module] | No direct variables or types from this module are used in `aqu_read_elements` for reading or storing this file. |

## File Variables

The file `aqu_catunit.ele` contains records of landscape cataloging unit elements, each identified by an integer index and described by fields such as name, object number, object type, and fractional area coverage within basin, response unit, and calibration region. These records are read sequentially and stored into the array `acu_elem` of type `landscape_elements`.

| Col | Header | Target | Type | Units | Meaning |
| --- | --- | --- | --- | --- | --- |
| 2 |  | `acu_elem%name` | character(len=16) |  | element name |
| 3 |  | `acu_elem%obj` | integer |  | object number |
| 4 |  | `acu_elem%obtyp` | character (len=3) |  | object type - 1=hru, 2=hru_lte, 11=export coef, etc |
| 5 |  | `acu_elem%obtypno` | integer |  | 2-number of hru_lte's or 1st hru_lte command |
| 6 |  | `acu_elem%bsn_frac` | real |  | fraction of element in basin (expansion factor) |
| 7 |  | `acu_elem%ru_frac` | real |  | fraction of element in response unit (expansion factor) |
| 8 |  | `acu_elem%reg_frac` | real |  | fraction of element in calibration region (expansion factor) |

## Sample

```text
1 ElementName1 HRU 2 0.5 0.3 0.2
2 ElementName2 HRU_LTE 1 0.7 0.4 0.3
```

## Read Pattern

```fortran
open (107,file=in_regs%ele_aqu)
read (107,*,iostat=eof) titldum
read (107,*,iostat=eof) header
read (107,*,iostat=eof) i
rewind (107)
backspace (107)
read (107,*,iostat=eof) k, acu_elem(i)%name, acu_elem(i)%obtyp, acu_elem(i)%obtypno, acu_elem(i)%bsn_frac, acu_elem(i)%ru_frac, acu_elem(i)%reg_frac
```

## I/O Operations

| Direction | Op | Unit | Statement |
| --- | --- | --- | --- |
| File setup | `open` | 107 | `open (107,file=in_regs%ele_aqu)` |
| Input | `read` | 107 | `read (107,*,iostat=eof) titldum` |
| Input | `read` | 107 | `read (107,*,iostat=eof) header` |
| Input | `read` | 107 | `read (107,*,iostat=eof) i` |
| File control | `rewind` | 107 | `rewind (107)` |
| Input | `read` | 107 | `read (107,*,iostat=eof) titldum` |
| Input | `read` | 107 | `read (107,*,iostat=eof) header` |
| Input | `read` | 107 | `read (107,*,iostat=eof) i` |
| File control | `backspace` | 107 | `backspace (107)` |
| Input | `read` | 107 | `read (107,*,iostat=eof) k, acu_elem(i)%name, acu_elem(i)%obtyp, acu_elem(i)%obtypno, acu_elem(i)%bsn_frac, acu_elem(i)%ru_frac, acu_elem(i)%reg_frac` |
| File control | `close` | 107 | `close (107)` |

## Readers

| Procedure | Operations | Role |
| --- | --- | --- |
| [sym:aqu_read_elements] | backspace, close, open, read, rewind | Reads the `aqu_catunit.ele` file if it exists, determines the maximum element index, allocates the `acu_elem` array accordingly, and reads each element record into `acu_elem`. |

## Review Notes

- The file `aqu_catunit.ele` is optional and only read if present, as checked by the existence inquiry on `in_regs%ele_aqu`.
- The reader `aqu_read_elements` uses the `input_file_module` for file path variables and `calibration_data_module` for the `landscape_elements` type and `acu_elem` array.
- No direct usage of `hydrograph_module`, `aquifer_module`, or `maximum_data_module` variables or types is evident in reading or storing this file.
- Sample read format is inferred from the read statement and type fields; no explicit example data is in the source.
