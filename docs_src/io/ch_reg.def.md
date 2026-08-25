---
kind: io
source_symbols:
- ch_read_elements
title: '`ch_reg.def`'
status: filled
source_hash: 481bf7e9d918ab29
version_label: SWAT+ 62.0.0
---

**Primary target:** `ccu_reg(:)` (array of `type landscape_units`)  
**Read by:** [sym:ch_read_elements]

## Bottom Line

The `ch_reg.def` file defines landscape cataloging units (regions) and their constituent elements for channel routing and calibration in SWAT+.

It is an optional input file that configures channel regions and their elements used in channel routing and calibration calculations.

The file is read by the `ch_read_elements` subroutine, which loads region-level and element-level data into the `ccu_reg` and `ccu_elem` arrays respectively.

| Module | Role for this file |
| --- | --- |
| [sym:input_file_module] | Provides the `in_regs` variable that contains the file path `def_cha_reg` for `ch_reg.def`. |
| [sym:maximum_data_module] | Provides the `db_mx` variable used to store the number of channel regions (`db_mx%cha_reg`). |
| [sym:calibration_data_module] | Defines the derived types `landscape_units` and `landscape_elements` used for `ccu_reg` and `ccu_elem` arrays, and variables like `ccu_cal` for calibration data. |
| [sym:hydrograph_module] | No direct variables or types from this module are explicitly referenced in `ch_read_elements` for reading `ch_reg.def`. |
| [sym:sd_channel_module] | No direct variables or types from this module are explicitly referenced in `ch_read_elements` for reading `ch_reg.def`. |

## File Variables

The `ch_reg.def` file contains records defining landscape cataloging units (regions) and their associated elements. Each region record includes a name, area in hectares, and counts of elements. Each element record includes identifiers, object types, and fractional area contributions within basin, response unit, and calibration region.

| Col | Header | Target | Type | Units | Meaning |
| --- | --- | --- | --- | --- | --- |
| 2 |  | `ccu_reg%name` | character(len=16) |  | name of region - (number of regions = db_mx%lsu_out) |
| 3 |  | `ccu_reg%area_ha` | real | hectares | area of landscape cataloging unit -hectares |
| 4 |  | `ccu_reg%num_tot` | integer |  | number of hru"s in each region |
| 5 |  | `ccu_reg%num` | integer |  | hru"s that are included in the region |
| 2 |  | `ccu_elem%name` | character(len=16) |  | Name of the element |
| 3 |  | `ccu_elem%obj` | integer |  | object number |
| 4 |  | `ccu_elem%obtyp` | character (len=3) |  | object type- 1=hru, 2=hru_lte, 11=export coef, etc |
| 5 |  | `ccu_elem%obtypno` | integer |  | 2-number of hru_lte"s or 1st hru_lte command |
| 6 |  | `ccu_elem%bsn_frac` | real |  | fraction of element in basin (expansion factor) |
| 7 |  | `ccu_elem%ru_frac` | real |  | fraction of element in ru (expansion factor) |
| 8 |  | `ccu_elem%reg_frac` | real |  | fraction of element in calibration region (expansion factor) |

## Sample

```text
1 RegionName1 1234.5 3 10 20 30
2 RegionName2 5678.9 2 40 50
1 ElementName1 1 1 0.5 0.3 0.2
2 ElementName2 2 2 0.6 0.4 0.3
```

## Read Pattern

```fortran
open (107,file=in_regs%def_cha_reg)
read (107,*,iostat=eof) titldum
read (107,*,iostat=eof) mreg
read (107,*,iostat=eof) header
read (107,*,iostat=eof) k, ccu_reg(i)%name, ccu_reg(i)%area_ha, nspu
backspace (107)
read (107,*,iostat=eof) k, ccu_reg(i)%name, ccu_reg(i)%area_ha, nspu, (elem_cnt(isp), isp = 1, nspu)
read (107,*,iostat=eof) i
rewind (107)
read (107,*,iostat=eof) k, ccu_elem(i)%name, ccu_elem(i)%obtyp, ccu_elem(i)%obtypno, ccu_elem(i)%bsn_frac, ccu_elem(i)%ru_frac, ccu_elem(i)%reg_frac
```

## I/O Operations

| Direction | Op | Unit | Statement |
| --- | --- | --- | --- |
| File setup | `open` | 107 | `open (107,file=in_regs%def_cha_reg)` |
| Input | `read` | 107 | `read (107,*,iostat=eof) titldum` |
| Input | `read` | 107 | `read (107,*,iostat=eof) mreg` |
| Input | `read` | 107 | `read (107,*,iostat=eof) header` |
| Input | `read` | 107 | `read (107,*,iostat=eof) k, ccu_reg(i)%name, ccu_reg(i)%area_ha, nspu` |
| File control | `backspace` | 107 | `backspace (107)` |
| Input | `read` | 107 | `read (107,*,iostat=eof) k, ccu_reg(i)%name, ccu_reg(i)%area_ha, nspu, (elem_cnt(isp), isp = 1, nspu)` |
| Input | `read` | 107 | `read (107,*,iostat=eof) titldum` |
| Input | `read` | 107 | `read (107,*,iostat=eof) header` |
| Input | `read` | 107 | `read (107,*,iostat=eof) i` |
| File control | `rewind` | 107 | `rewind (107)` |
| Input | `read` | 107 | `read (107,*,iostat=eof) titldum` |
| Input | `read` | 107 | `read (107,*,iostat=eof) header` |
| Input | `read` | 107 | `read (107,*,iostat=eof) i` |
| File control | `backspace` | 107 | `backspace (107)` |
| Input | `read` | 107 | `read (107,*,iostat=eof) k, ccu_elem(i)%name, ccu_elem(i)%obtyp, ccu_elem(i)%obtypno, ccu_elem(i)%bsn_frac, ccu_elem(i)%ru_frac, ccu_elem(i)%reg_frac` |
| File control | `close` | 107 | `close (107)` |

## Readers

| Procedure | Operations | Role |
| --- | --- | --- |
| [sym:ch_read_elements] | backspace, close, open, read, rewind | Reads the `ch_reg.def` file to load channel routing regions (`ccu_reg`) and their landscape elements (`ccu_elem`). It allocates arrays for channel scheduling and calibration, reads region metadata and element membership, and populates calibration variables accordingly. |

## Review Notes

- The `ch_reg.def` file is optional and used to define channel routing regions and their elements for calibration and output.
- The reader `ch_read_elements` uses several modules primarily for types and global variables related to input file paths, maximum data counts, and calibration data structures.
- No direct evidence was found for usage of `hydrograph_module` or `sd_channel_module` variables in reading this file; they may be used elsewhere in the reader or for side effects.
- The sample read format is inferred from the read statements and typical data layout; exact example records should be verified with reference datasets.
