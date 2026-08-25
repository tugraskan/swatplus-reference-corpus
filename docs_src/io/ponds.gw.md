---
kind: io
source_symbols:
- gwflow_read
title: '`ponds.gw`'
status: filled
source_hash: 8956d621ce174994
version_label: SWAT+ 62.0.0
---

**Primary target:** gw_pond_info(:)  
**Read by:** [sym:gwflow_read]

## Bottom Line

The file ponds.gw configures groundwater recharge pond properties, including physical characteristics and solute concentrations, for the SWAT+ groundwater flow model.

It is an optional input file that, if present, is read by the gwflow_read procedure to populate the gw_pond_info derived type array.

This file sets initial and static parameters for recharge ponds used in groundwater flow and solute transport simulations.

| Module | Role for this file |
| --- | --- |
| [sym:gwflow_module] | Provides the gw_pond_info derived type array and gw_nsolute variable used to store pond properties and solute counts. |
| [sym:hydrograph_module] | No direct variables or types from this module are used for ponds.gw reading. |
| [sym:sd_channel_module] | No direct variables or types from this module are used for ponds.gw reading. |
| [sym:maximum_data_module] | No direct variables or types from this module are used for ponds.gw reading. |
| [sym:hru_module] | No direct variables or types from this module are used for ponds.gw reading. |
| [sym:reservoir_data_module] | No direct variables or types from this module are used for ponds.gw reading. |
| [sym:cs_data_module] | No direct variables or types from this module are used for ponds.gw reading. |
| [sym:constituent_mass_module] | Provides gw_nsolute, the number of solutes, used to dimension unl_conc arrays in gw_pond_info. |
| [sym:water_allocation_module] | No direct variables or types from this module are used for ponds.gw reading. |
| [sym:utils] | Provides the split_line utility, though not directly used in ponds.gw reading. |

## File Variables

The ponds.gw file contains tabular data describing groundwater recharge ponds, with each record representing one pond's properties and solute concentrations. The file is read line-by-line into the gw_pond_info derived type array, mapping each column to a specific pond attribute or metadata such as start date.

| Col | Header | Target | Type | Units | Meaning |
| --- | --- | --- | --- | --- | --- |
| 1 | `header` | `header` |  |  | A character string read from the file, typically representing a header or metadata line. |
| 1 | `dum_id` | `dum_id` |  |  | An integer read as a dummy ID used to detect end-of-file during reading. |
| 1 | `id` | `gw_pond_info(i)%id` |  |  | Unique identifier for each groundwater recharge pond. |
| 2 | `area` | `gw_pond_info(i)%area` |  |  | Surface area of the recharge pond, presumably in square meters. |
| 3 | `chan` | `gw_pond_info(i)%chan` |  |  | Channel number associated with the pond for routing or connectivity. |
| 4 | `canal` | `gw_pond_info(i)%canal` |  |  | Canal number associated with the pond, possibly for water allocation or flow. |
| 5 | `unl` | `gw_pond_info(i)%unl` |  |  | An integer flag indicating whether the pond is unlined (1) or lined (0). |
| 6 | `bed_k` | `gw_pond_info(i)%bed_k` |  |  | Hydraulic conductivity of the pond bed material. |
| 7 | `wsta` | `gw_pond_info(i)%wsta` |  |  | Water surface elevation or stage of the pond. |
| 8 | `evap_co` | `gw_pond_info(i)%evap_co` |  |  | Evaporation coefficient for the pond surface. |
| 9 | `yr_start` | `yr_start` |  |  | Starting year for pond data or simulation. |
| 10 | `mo_start` | `mo_start` |  |  | Starting month for pond data or simulation. |
| 11 | `dy_start` | `dy_start` |  |  | Starting day for pond data or simulation. |
| 12+ | `unl_conc(j)` | `(gw_pond_info(i)%unl_conc(j),j=1,gw_nsolute)` |  |  | Array of solute concentrations in the pond for each solute species. |

## Sample

```text
Header line 1 (e.g. descriptive text)
Header line 2 (e.g. column names)
1  500.0  3  2  1  0.0001  100.0  0.85  2020  1  1  0.0 0.0 0.0
2  750.0  5  1  0  0.0002  105.0  0.90  2020  1  1  0.1 0.05 0.0
```

## Read Pattern

```fortran
open(in_ponds,file='ponds.gw')
read(in_ponds,*) header
read(in_ponds,*) header
read(in_ponds,*,iostat=eof) dum_id
rewind(in_ponds)
read(in_ponds,*) header
read(in_ponds,*) header
read(in_ponds,*) gw_pond_info(i)%id, gw_pond_info(i)%area, gw_pond_info(i)%chan, gw_pond_info(i)%canal, gw_pond_info(i)%unl, gw_pond_info(i)%bed_k, gw_pond_info(i)%wsta, gw_pond_info(i)%evap_co, yr_start,mo_start,dy_start, (gw_pond_info(i)%unl_conc(j),j=1,gw_nsolute)
```

## I/O Operations

| Direction | Op | Unit | Statement |
| --- | --- | --- | --- |
| File setup | `open` | in_ponds | `open(in_ponds,file='ponds.gw')` |
| Input | `read` | in_ponds | `read(in_ponds,*) header` |
| Input | `read` | in_ponds | `read(in_ponds,*) header` |
| Input | `read` | in_ponds | `read(in_ponds,*,iostat=eof) dum_id` |
| File control | `rewind` | in_ponds | `rewind(in_ponds)` |
| Input | `read` | in_ponds | `read(in_ponds,*) header` |
| Input | `read` | in_ponds | `read(in_ponds,*) header` |
| Input | `read` | in_ponds | `read(in_ponds,*) gw_pond_info(i)%id, gw_pond_info(i)%area, gw_pond_info(i)%chan, gw_pond_info(i)%canal, gw_pond_info(i)%unl, gw_pond_info(i)%bed_k, gw_pond_info(i)%wsta, gw_pond_info(i)%evap_co, yr_start,mo_start,dy_start, (gw_pond_info(i)%unl_conc(j),j=1,gw_nsolute)` |
| File control | `close` | in_ponds | `close(in_ponds)` |

## Readers

| Procedure | Operations | Role |
| --- | --- | --- |
| [sym:gwflow_read] | close, open, read, rewind | The gwflow_read procedure reads the ponds.gw file to load groundwater recharge pond properties into the gw_pond_info array, including physical parameters and solute concentrations, for use in groundwater flow and solute transport modeling. |

## Review Notes

- Draft input-file overlay generated from static source facts; review and complete the remaining fields before promotion.
- The ponds.gw file is optional and read by gwflow_read to configure recharge pond properties in the groundwater flow model.
- The file format includes two header lines followed by pond records with fixed columns and a variable-length solute concentration array.
- No explicit units are given in source; typical units are inferred from SWAT+ conventions.
- The gw_pond_info derived type and gw_nsolute variable come from gwflow_module and constituent_mass_module respectively.
