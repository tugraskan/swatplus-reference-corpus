---
kind: io
source_symbols:
- res_read_elements
title: '`res_catunit.ele`'
status: filled
source_hash: 72133c280b3a7a48
version_label: SWAT+ 62.0.0
---

**Primary target:** `rcu_elem(:)` (array of `type landscape_elements`)  
**Read by:** [sym:res_read_elements]

## Bottom Line

The file `res_catunit.ele` defines landscape cataloging unit elements, specifying their names, object numbers, types, and fractional coverage within basins, routing units, and calibration regions.

It is an optional input file that configures the detailed element-level structure within reservoir cataloging units for calibration and routing purposes.

The primary reader for this file is the subroutine `res_read_elements`.

| Module | Role for this file |
| --- | --- |
| [sym:input_file_module] | Provides the file path variable `in_regs%ele_res` used to locate the `res_catunit.ele` file. |
| [sym:maximum_data_module] | Supplies the variable `db_mx` which stores counts such as `db_mx%res_out` and `db_mx%res_reg` related to reservoir cataloging units. |
| [sym:calibration_data_module] | Defines the derived type `landscape_elements` and the array `rcu_elem` where the file records are stored. |
| [sym:hydrograph_module] | Not directly referenced for reading or storing this file in the shown source. |
| [sym:reservoir_module] | Provides variables such as `rcu_out`, `rcu_cal`, and `rcu_reg` which are related to reservoir cataloging units and their elements. |

## File Variables

The `res_catunit.ele` file contains records describing landscape cataloging unit elements. Each record corresponds to an element stored in the `rcu_elem` array of type `landscape_elements`. The file columns map directly to the fields of this derived type, including element name, object number, object type, and fractional coverage within basin, routing unit, and calibration region.

| Col | Header | Target | Type | Units | Meaning |
| --- | --- | --- | --- | --- | --- |
| 2 |  | `rcu_elem%name` | character(len=16) |  | Element name identifier |
| 3 |  | `rcu_elem%obj` | integer |  | Object number |
| 4 |  | `rcu_elem%obtyp` | character (len=3) |  | Object type code (e.g., 1=hru, 2=hru_lte, 11=export coef) |
| 5 |  | `rcu_elem%obtypno` | integer |  | Number of hru_lte's or first hru_lte command |
| 6 |  | `rcu_elem%bsn_frac` | real |  | Fraction of element area within the basin (expansion factor) |
| 7 |  | `rcu_elem%ru_frac` | real |  | Fraction of element area within the routing unit (expansion factor) |
| 8 |  | `rcu_elem%reg_frac` | real |  | Fraction of element area within the calibration region (expansion factor) |

## Sample

```text
1  ElementName       1  1  0.75  0.80  0.90
```

## Read Pattern

```fortran
open (107,file=in_regs%ele_res)
read (107,*,iostat=eof) titldum
read (107,*,iostat=eof) header
read (107,*,iostat=eof) i
rewind (107)
backspace (107)
read (107,*,iostat=eof) k, rcu_elem(i)%name, rcu_elem(i)%obtyp, rcu_elem(i)%obtypno, rcu_elem(i)%bsn_frac, rcu_elem(i)%ru_frac, rcu_elem(i)%reg_frac
```

## I/O Operations

| Direction | Op | Unit | Statement |
| --- | --- | --- | --- |
| File setup | `open` | 107 | `open (107,file=in_regs%ele_res)` |
| Input | `read` | 107 | `read (107,*,iostat=eof) titldum` |
| Input | `read` | 107 | `read (107,*,iostat=eof) header` |
| Input | `read` | 107 | `read (107,*,iostat=eof) i` |
| File control | `rewind` | 107 | `rewind (107)` |
| File control | `backspace` | 107 | `backspace (107)` |
| Input | `read` | 107 | `read (107,*,iostat=eof) k, rcu_elem(i)%name, rcu_elem(i)%obtyp, rcu_elem(i)%obtypno, rcu_elem(i)%bsn_frac, rcu_elem(i)%ru_frac, rcu_elem(i)%reg_frac` |
| File control | `close` | 107 | `close (107)` |

## Readers

| Procedure | Operations | Role |
| --- | --- | --- |
| [sym:res_read_elements] | backspace, close, open, read, rewind | Reads the `res_catunit.ele` file to populate the `rcu_elem` array with landscape element records, mapping file columns to the `landscape_elements` type fields. |

## Review Notes

- Overlay fields are based strictly on the source code in `res_read_elements.f90` and the `landscape_elements` type definition.
- The file is optional as indicated by the existence check and conditional reading in `res_read_elements`.
- The sample read format is inferred from the read statement and type fields; actual example data should be verified from a reference dataset.
- No direct usage of `hydrograph_module` variables for this file was found in the reader source.
