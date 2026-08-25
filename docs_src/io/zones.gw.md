---
kind: io
source_symbols:
- gwflow_read
title: '`zones.gw`'
status: filled
source_hash: 8956d621ce174994
version_label: SWAT+ 62.0.0
---

**Primary target:** zones  
**Read by:** [sym:gwflow_read]

## Bottom Line

zones.gw is a required input file that configures groundwater and streambed hydraulic property zones for the SWAT+ groundwater flow model.

It defines spatial zones for aquifer hydraulic conductivity, specific yield, streambed hydraulic conductivity, streambed thickness, and water table depth used in groundwater simulations.

The file is read by the `gwflow_read` subroutine, which loads these zone properties into arrays used by the groundwater flow model.

| Module | Role for this file |
| --- | --- |
| [sym:gwflow_module] | Provides groundwater flow related arrays and variables such as zones_aquK, zones_aquSy, zones_strK, zones_strbed, zones_Kt, zones_wt, and related zone counts (nzones_aquK, nzones_aquSy, nzones_strK, nzones_strbed, nzones_wt). |
| [sym:hydrograph_module] |  |
| [sym:sd_channel_module] |  |
| [sym:maximum_data_module] |  |
| [sym:hru_module] | Provides the `hru` derived type, though not directly referenced for zones.gw reading. |
| [sym:reservoir_data_module] | Provides `wet_dat` type, not directly used for zones.gw reading. |
| [sym:cs_data_module] |  |
| [sym:constituent_mass_module] | Provides `cs_db`, not directly used for zones.gw reading. |
| [sym:water_allocation_module] | Provides `canal`, not directly used for zones.gw reading. |
| [sym:utils] | Provides the `split_line` utility subroutine used for parsing lines during file reading. |

## File Variables

The zones.gw file contains multiple lines defining hydraulic property zones for groundwater and streambed parameters. Each line corresponds to a zone value for a specific property such as aquifer hydraulic conductivity or specific yield. The file is read sequentially by `gwflow_read` and the values are stored into allocatable arrays representing these zones.

| Col | Header | Target | Type | Units | Meaning |
| --- | --- | --- | --- | --- | --- |
| 1 | `Aquifer Hydraulic Conductivity Zone Values` | `zones_aquK` |  |  | Array storing hydraulic conductivity values for aquifer zones read from zones.gw. |
| 1 | `Aquifer Specific Yield Zone Values` | `zones_aquSy` |  |  | Array storing specific yield values for aquifer zones read from zones.gw. |
| 1 | `Streambed Hydraulic Conductivity Zone Values` | `zones_strK` |  |  | Array storing hydraulic conductivity values for streambed zones read from zones.gw. |
| 1 | `Streambed Thickness Zone Values` | `zones_strbed` |  |  | Array storing thickness values for streambed zones read from zones.gw. |
| 1 | `Water Table Depth Zone Values` | `zones_wt` |  |  | Array storing water table depth values for zones read from zones.gw. |

## Sample

```text
Example zones.gw content (values per line):
0.0012
0.15
0.0005
2.0
10.0
```

## Read Pattern

```fortran
open(in_gw,file='zones.gw')
read(in_gw,*) header
read(in_gw,*) header
read(in_gw,'(a)',iostat=eof) split_line_buf
rewind(in_gw)
read(in_gw,*) header
read(in_gw,*) header
read(in_gw,'(a)') split_line_buf
```

## I/O Operations

| Direction | Op | Unit | Statement |
| --- | --- | --- | --- |
| File setup | `open` | in_gw | `open(in_gw,file='zones.gw')` |
| Input | `read` | in_gw | `read(in_gw,*) header` |
| Input | `read` | in_gw | `read(in_gw,*) header` |
| Input | `read` | in_gw | `read(in_gw,'(a)',iostat=eof) split_line_buf` |
| File control | `rewind` | in_gw | `rewind(in_gw)` |
| Input | `read` | in_gw | `read(in_gw,*) header` |
| Input | `read` | in_gw | `read(in_gw,*) header` |
| Input | `read` | in_gw | `read(in_gw,'(a)') split_line_buf` |
| File control | `close` | in_gw | `close(in_gw)` |

## Readers

| Procedure | Operations | Role |
| --- | --- | --- |
| [sym:gwflow_read] | close, open, read, rewind | Reads the zones.gw file to load groundwater and streambed hydraulic property zones into arrays used by the groundwater flow model. |

## Review Notes

- Draft input-file overlay generated from static source facts; review and complete the remaining fields before promotion.
- The exact line-by-line parsing of zones.gw is not fully visible in the provided source snippet; assumptions about the arrays populated are based on module variables and typical groundwater zone usage.
- No explicit sample record block was found in the source; a minimal example is provided based on typical zone value lines.
