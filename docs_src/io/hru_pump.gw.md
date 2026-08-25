---
kind: io
source_symbols:
- gwflow_read
title: '`hru_pump.gw`'
status: filled
source_hash: 8956d621ce174994
version_label: SWAT+ 62.0.0
---

**Primary target:** hru_pump_ids(:)  
**Read by:** [sym:gwflow_read]

## Bottom Line

The file 'hru_pump.gw' provides external groundwater pumping observation data for HRUs (Hydrologic Response Units).

It is read optionally by the 'gwflow_read' subroutine if present, to configure pumping rates or IDs associated with HRUs for groundwater flow modeling.

| Module | Role for this file |
| --- | --- |
| [sym:gwflow_module] | Provides groundwater flow related variables and state arrays that 'gwflow_read' updates when reading 'hru_pump.gw'. |
| [sym:hydrograph_module] | Used for hydrograph and flow routing data structures, indirectly related to groundwater flow but not specifically for this file. |
| [sym:sd_channel_module] | Handles channel and stream data structures, not directly used for 'hru_pump.gw' reading. |
| [sym:maximum_data_module] | Supplies maximum data constants or arrays, not specifically referenced for this file. |
| [sym:hru_module] | Provides the 'hru' derived type and arrays that store HRU properties, including pumping information loaded from 'hru_pump.gw'. |
| [sym:reservoir_data_module] | Manages reservoir data structures, unrelated to this file. |
| [sym:cs_data_module] | Constituent source data, not used for this file. |
| [sym:constituent_mass_module] | Constituent mass balance data, not used for this file. |
| [sym:water_allocation_module] | Water allocation structures like canals, not used for this file. |
| [sym:utils] | Provides utility routines such as 'split_line' used in parsing input files generally. |

## File Variables

The 'hru_pump.gw' file contains a count of HRU pumping observations followed by a list of HRU pump IDs. The 'gwflow_read' routine reads this file to populate arrays that track which HRUs have groundwater pumping observations.

| Col | Header | Target | Type | Units | Meaning |
| --- | --- | --- | --- | --- | --- |
| 1 | `num_hru_pump_obs` | `num_hru_pump_obs` |  |  | The number of HRU pumping observation records present in the 'hru_pump.gw' file, indicating how many HRUs have groundwater pumping data. |
| 1 | `hru_pump_ids(i)` | `hru_pump_ids(i)` |  |  | The list of HRU IDs that correspond to groundwater pumping observations, used to link pumping data to specific HRUs in the model. |

## Sample

```text
3
101
205
309
```

## Read Pattern

```fortran
open(in_hru_pump_obs,file='hru_pump.gw')
read(in_hru_pump_obs,*)
read(in_hru_pump_obs,*) num_hru_pump_obs
read(in_hru_pump_obs,*) hru_pump_ids(i)
```

## I/O Operations

| Direction | Op | Unit | Statement |
| --- | --- | --- | --- |
| File setup | `open` | in_hru_pump_obs | `open(in_hru_pump_obs,file='hru_pump.gw')` |
| Input | `read` | in_hru_pump_obs | `read(in_hru_pump_obs,*)` |
| Input | `read` | in_hru_pump_obs | `read(in_hru_pump_obs,*) num_hru_pump_obs` |
| Input | `read` | in_hru_pump_obs | `read(in_hru_pump_obs,*) hru_pump_ids(i)` |

## Readers

| Procedure | Operations | Role |
| --- | --- | --- |
| [sym:gwflow_read] | open, read | Reads the 'hru_pump.gw' file to load the number of HRU pumping observations and the list of HRU IDs with groundwater pumping. This configures the groundwater pumping state for HRUs in the model. |

## Review Notes

- Draft input-file overlay generated from static source facts; review and complete the remaining fields before promotion.
- The 'hru_pump.gw' file is optional and only read if present, as indicated by conditional file existence checks in 'gwflow_read'.
- No detailed sample records were found in the source; the sample read format is inferred from the read statements and typical HRU ID values.
