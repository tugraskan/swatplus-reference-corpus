---
kind: io
source_symbols:
- gwflow_read
title: '`pumpex.gw`'
status: filled
source_hash: 8956d621ce174994
version_label: SWAT+ 62.0.0
---

**Primary target:** gwflow_module%pumpex(:)  
**Read by:** [sym:gwflow_read]

## Bottom Line

The file pumpex.gw configures external groundwater pumping rates and schedules for specific model cells.

It is optional and only needed if external groundwater pumping is simulated.

The reader routine gwflow_read loads this file and populates the pumpex array in gwflow_module.

| Module | Role for this file |
| --- | --- |
| [sym:gwflow_module] | Provides the pumpex derived type array where pumping cell indices and rates are stored. |
| [sym:hydrograph_module] |  |
| [sym:sd_channel_module] |  |
| [sym:maximum_data_module] |  |
| [sym:hru_module] |  |
| [sym:reservoir_data_module] |  |
| [sym:cs_data_module] |  |
| [sym:constituent_mass_module] |  |
| [sym:water_allocation_module] |  |
| [sym:utils] | Provides the split_line utility used elsewhere in gwflow_read but not specifically for pumpex.gw. |

## File Variables

The pumpex.gw file contains records specifying groundwater pumping cells and their pumping rates with associated start and end dates. Each record corresponds to one pumping cell with its parameters read into the pumpex array.

| Col | Header | Target | Type | Units | Meaning |
| --- | --- | --- | --- | --- | --- |
| 1 | `header` | `header` |  |  | A character string read as a header or label line from the pumpex.gw file, used for metadata or file structure verification. |
| 2 | `pumpex_cell` | `pumpex_cell` |  |  | Integer cell index identifying the groundwater cell where pumping is applied. |
| 3 | `gw_pumpex_rates_tmp` | `gw_pumpex_rates_tmp` |  |  | Real value specifying the pumping rate for the groundwater cell, typically in volume per time units. |
| 4 | `pe_yr_s` | `pe_yr_s` |  |  | Integer year marking the start date of the pumping schedule. |
| 5 | `pe_dy_s` | `pe_dy_s` |  |  | Integer day of year marking the start date of the pumping schedule. |
| 6 | `pe_yr_e` | `pe_yr_e` |  |  | Integer year marking the end date of the pumping schedule. |
| 7 | `pe_dy_e` | `pe_dy_e` |  |  | Integer day of year marking the end date of the pumping schedule. |

## Sample

```text
Example pumpex.gw record:
HEADER_LINE
123  0.005  2020  150  2020  300
```

## Read Pattern

```fortran
open(in_gw,file='pumpex.gw')
read(in_gw,*) header
read(in_gw,*,iostat=eof) header, pumpex_cell
rewind(in_gw)
read(in_gw,*,iostat=eof) header, pumpex_cell, gw_pumpex_rates_tmp, pe_yr_s, pe_dy_s, pe_yr_e, pe_dy_e
```

## I/O Operations

| Direction | Op | Unit | Statement |
| --- | --- | --- | --- |
| File setup | `open` | in_gw | `open(in_gw,file='pumpex.gw')` |
| Input | `read` | in_gw | `read(in_gw,*) header` |
| Input | `read` | in_gw | `read(in_gw,*) header` |
| Input | `read` | in_gw | `read(in_gw,*,iostat=eof) header, pumpex_cell` |
| File control | `rewind` | in_gw | `rewind(in_gw)` |
| Input | `read` | in_gw | `read(in_gw,*) header` |
| Input | `read` | in_gw | `read(in_gw,*) header` |
| Input | `read` | in_gw | `read(in_gw,*,iostat=eof) header, pumpex_cell, gw_pumpex_rates_tmp, pe_yr_s, pe_dy_s, pe_yr_e, pe_dy_e` |
| File control | `close` | in_gw | `close(in_gw)` |

## Readers

| Procedure | Operations | Role |
| --- | --- | --- |
| [sym:gwflow_read] | close, open, read, rewind | Reads the pumpex.gw file to load groundwater pumping cell indices, pumping rates, and pumping schedule start and end dates into the pumpex array in gwflow_module. |

## Review Notes

- Draft input-file overlay generated from static source facts; review and complete the remaining fields before promotion.
- The pumpex.gw file is optional and only read if external groundwater pumping is enabled in the model.
- The exact format of the header lines is not fully detailed in the source; assumed to be metadata or labels.
- No explicit error handling or validation of pumping cell indices or dates is visible in the source snippet.
