---
kind: io
source_symbols:
- rec_read_elements
title: '`rec_reg.def`'
status: filled
source_hash: 4986560811349e04
version_label: SWAT+ 62.0.0
---

**Primary target:** `pcu_reg(:)` (array of `type landscape_units`)  
**Read by:** [sym:rec_read_elements]

## Bottom Line

The file `rec_reg.def` defines landscape cataloging units (regions) for recall soft calibration and output by type in SWAT+.

It is optional and only read if the file exists or is not set to "null".

The reader subroutine `rec_read_elements` loads this file and stores its data into the `pcu_reg` array of `type landscape_units`.

| Module | Role for this file |
| --- | --- |
| [sym:input_file_module] | provides the `in_regs` variable which holds file path strings such as `def_psc_reg` for this input file. |
| [sym:maximum_data_module] | provides the `db_mx` variable, which stores counts such as `rec_reg` and `rec_out` used to track number of regions read. |
| [sym:calibration_data_module] | provides the `pcu_reg` array of `type landscape_units` where the file records are stored, and `pcu_cal` array used for calibration state variables. |
| [sym:hydrograph_module] | provides the `sp_ob` variable which contains `recall` and `hru` counts used when no subunits are specified in the file. |

## File Variables

The file `rec_reg.def` contains records defining landscape cataloging units (regions) for recall calibration and output. Each record includes a region identifier, name, area in hectares, number of subunits, and a list of element counts representing HRUs included in the region. These map to fields in the `pcu_reg` array of `type landscape_units`.

| Col | Header | Target | Type | Units | Meaning |
| --- | --- | --- | --- | --- | --- |
| 2 |  | `pcu_reg%name` | character(len=16) |  | name of region - (number of regions = db_mx%lsu_out) |
| 3 |  | `pcu_reg%area_ha` | real |  | area of landscape cataloging unit -hectares |
| 4 |  | `pcu_reg%num_tot` | integer |  | number of hru"s in each region |
| 5 |  | `pcu_reg%num` | integer |  | hru"s that are included in the region |

## Sample

```text
1 RegionName1 1500.0 3 10 20 30
2 RegionName2 2300.5 0
```

## Read Pattern

```fortran
open (107,file=in_regs%def_psc_reg)
read (107,*,iostat=eof) titldum
read (107,*,iostat=eof) mreg
read (107,*,iostat=eof) header
read (107,*,iostat=eof) k, pcu_reg(i)%name, pcu_reg(i)%area_ha, nspu
backspace (107)
read (107,*,iostat=eof) k, pcu_reg(i)%name, pcu_reg(i)%area_ha, nspu, (elem_cnt(isp), isp = 1, nspu)
```

## I/O Operations

| Direction | Op | Unit | Statement |
| --- | --- | --- | --- |
| File setup | `open` | 107 | `open (107,file=in_regs%def_psc_reg)` |
| Input | `read` | 107 | `read (107,*,iostat=eof) titldum` |
| Input | `read` | 107 | `read (107,*,iostat=eof) mreg` |
| Input | `read` | 107 | `read (107,*,iostat=eof) header` |
| Input | `read` | 107 | `read (107,*,iostat=eof) k, pcu_reg(i)%name, pcu_reg(i)%area_ha, nspu` |
| File control | `backspace` | 107 | `backspace (107)` |
| Input | `read` | 107 | `read (107,*,iostat=eof) k, pcu_reg(i)%name, pcu_reg(i)%area_ha, nspu, (elem_cnt(isp), isp = 1, nspu)` |

## Readers

| Procedure | Operations | Role |
| --- | --- | --- |
| [sym:rec_read_elements] | backspace, open, read | Reads the `rec_reg.def` file if it exists, parsing landscape cataloging unit records into the `pcu_reg` array. It reads the region count, then for each region reads its identifier, name, area, number of subunits, and the list of HRU element counts. It allocates and initializes arrays to store these elements and sets up calibration state accordingly. |

## Review Notes

- The file `rec_reg.def` is optional and only read if present or not set to "null".
- If the number of subunits (nspu) is zero, all HRUs are included in the region by default using `sp_ob%recall`.
- The reader `rec_read_elements` uses `define_unit_elements` to map subunits to element numbers.
- The sample read format is inferred from the read statements and typical usage but no explicit example is in the source.
- No discrepancies found between source and manual references for this file.
