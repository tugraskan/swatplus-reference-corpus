---
kind: io
source_symbols:
- ch_read_elements
title: '`ch_catunit.def`'
status: filled
source_hash: 481bf7e9d918ab29
version_label: SWAT+ 62.0.0
---

**Primary target:** `ccu_out(:)` (array of `type landscape_units`)  
**Read by:** [sym:ch_read_elements]

## Bottom Line

`ch_catunit.def` is an input file defining landscape cataloging units (regions) for channel routing and calibration in SWAT+. It is required if channel regions are used for output or calibration. The file configures the landscape units' names, areas, and their associated hydrologic response units (HRUs). The reader `ch_read_elements` loads this file and populates the `ccu_out` array of `type landscape_units` with these data.

| Module | Role for this file |
| --- | --- |
| [sym:input_file_module] | Provides the `in_regs` variable which contains the filename `def_cha` that points to `ch_catunit.def`. |
| [sym:maximum_data_module] | Provides the `db_mx` variable which stores the number of landscape units `lsu_out` and the number of channel regions `cha_reg`. |
| [sym:calibration_data_module] | Defines the `type landscape_units` and the `ccu_out` array where the file data are stored. Also provides `ccu_cal` and `ccu_reg` used for calibration and region data. |
| [sym:hydrograph_module] | Provides `sp_ob` which contains counts of HRUs and channels used when no subunits are specified in the file. |
| [sym:sd_channel_module] | Provides `defunit_num` which is used to assign HRU numbers to landscape units after reading the element counts. |

## File Variables

The file `ch_catunit.def` contains records defining landscape cataloging units (regions) used for channel routing and calibration. Each record includes a region identifier, a name, the area in hectares, the number of subunits (HRUs) in the region, and optionally a list of element counts per subunit. These data are read sequentially and stored into the `ccu_out` array of `type landscape_units`.

| Col | Header | Target | Type | Units | Meaning |
| --- | --- | --- | --- | --- | --- |
| 2 |  | `ccu_out%name` | character(len=16) |  | name of region - (number of regions = db_mx%lsu_out) |
| 3 |  | `ccu_out%area_ha` | real |  | area of landscape cataloging unit -hectares |
| 4 |  | `ccu_out%num_tot` | integer |  | number of hru"s in each region |
| 5 |  | `ccu_out%num` | integer |  | hru"s that are included in the region |

## Sample

```text
1  RegionName      12345.67  3  10 20 30
2  AnotherRegion   23456.78  0
```

## Read Pattern

```fortran
open (107,file=in_regs%def_cha)
read (107,*,iostat=eof) titldum
read (107,*,iostat=eof) mreg
read (107,*,iostat=eof) header
read (107,*,iostat=eof) k, ccu_out(i)%name, ccu_out(i)%area_ha, nspu
backspace (107)
read (107,*,iostat=eof) k, ccu_out(i)%name, ccu_out(i)%area_ha, nspu, (elem_cnt(isp), isp = 1, nspu)
```

## I/O Operations

| Direction | Op | Unit | Statement |
| --- | --- | --- | --- |
| File setup | `open` | 107 | `open (107,file=in_regs%def_cha)` |
| Input | `read` | 107 | `read (107,*,iostat=eof) titldum` |
| Input | `read` | 107 | `read (107,*,iostat=eof) mreg` |
| Input | `read` | 107 | `read (107,*,iostat=eof) header` |
| Input | `read` | 107 | `read (107,*,iostat=eof) k, ccu_out(i)%name, ccu_out(i)%area_ha, nspu` |
| File control | `backspace` | 107 | `backspace (107)` |
| Input | `read` | 107 | `read (107,*,iostat=eof) k, ccu_out(i)%name, ccu_out(i)%area_ha, nspu, (elem_cnt(isp), isp = 1, nspu)` |

## Readers

| Procedure | Operations | Role |
| --- | --- | --- |
| [sym:ch_read_elements] | open, read, backspace | Reads the `ch_catunit.def` file to load landscape cataloging units into the `ccu_out` array. It reads the number of regions, then for each region reads its identifier, name, area, and number of subunits (HRUs). If subunits are specified, it reads their element counts and calls `define_unit_elements` to assign HRU numbers. If no subunits are specified, it assigns all HRUs in the region by default. This routine thus configures the model state related to channel landscape units. |

## Review Notes

- The file `ch_catunit.def` is required if channel regions are used for routing or calibration; otherwise, it may be omitted.
- The reader `ch_read_elements` uses `in_regs%def_cha` as the filename for this file.
- The sample read format is inferred from the read statements and typical usage but no explicit example record is present in the source.
- The `num` array in `ccu_out` stores HRU indices included in the region, assigned either from the file or defaulted from `sp_ob` counts.
- No explicit error handling or optional file behavior beyond existence check is visible in the source.
