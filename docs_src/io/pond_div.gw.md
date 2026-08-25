---
kind: io
source_symbols:
- gwflow_read
title: '`pond_div.gw`'
status: filled
source_hash: 8956d621ce174994
version_label: SWAT+ 62.0.0
---

**Primary target:** gwflow_module.pond_div_gw  
**Read by:** [sym:gwflow_read]

## Bottom Line

The file pond_div.gw configures groundwater pond and diversion data used in the SWAT+ groundwater flow model.

It is an optional input file that provides parameters for groundwater pond and diversion features, influencing groundwater flow routing and storage.

The primary reader for this file is the subroutine gwflow_read, which opens and reads pond_div.gw to populate groundwater pond/diversion data structures.

| Module | Role for this file |
| --- | --- |
| [sym:gwflow_module] | Provides the derived type pond_div_gw and related groundwater flow data structures that gwflow_read populates from pond_div.gw. |
| [sym:hydrograph_module] | Used for hydrograph-related data structures that may be updated during groundwater flow reading. |
| [sym:sd_channel_module] | Used for channel cell and channel-related variables referenced during groundwater flow input processing. |
| [sym:maximum_data_module] | Provides maximum data constants or arrays used during groundwater flow input reading. |
| [sym:hru_module] | Provides the hru derived type and related hydrologic response unit data used or updated during groundwater flow reading. |
| [sym:reservoir_data_module] | Provides the wet_dat type and reservoir-related variables that may be referenced or updated during groundwater flow reading. |
| [sym:cs_data_module] | Provides constituent source data structures used during groundwater flow input processing. |
| [sym:constituent_mass_module] | Provides the cs_db derived type and constituent mass balance data used during groundwater flow reading. |
| [sym:water_allocation_module] | Provides the canal derived type and water allocation variables referenced during groundwater flow input reading. |
| [sym:utils] | Provides utility routines such as split_line used by gwflow_read to parse input lines. |

## File Variables

The pond_div.gw file consists of structured text records describing groundwater pond and diversion parameters. The gwflow_read subroutine reads this file line-by-line, parsing header and data lines into the pond_div_gw derived type arrays defined in gwflow_module.

| Col | Header | Target | Type | Units | Meaning |
| --- | --- | --- | --- | --- | --- |
| All columns | `header` | `header` |  |  | The header line read from pond_div.gw, typically containing metadata or column labels describing the groundwater pond/diversion data fields. |

## Sample

```text
Example pond_div.gw snippet:
PondID DivID Area Volume Stage ...
1      0     5000  10000  2.5   ...
2      1     3000  6000   1.8   ...
```

## Read Pattern

```fortran
open(in_ponds,file='pond_div.gw')
read(in_ponds,*) header
read(in_ponds,*) header
```

## I/O Operations

| Direction | Op | Unit | Statement |
| --- | --- | --- | --- |
| File setup | `open` | in_ponds | `open(in_ponds,file='pond_div.gw')` |
| Input | `read` | in_ponds | `read(in_ponds,*) header` |
| Input | `read` | in_ponds | `read(in_ponds,*) header` |

## Readers

| Procedure | Operations | Role |
| --- | --- | --- |
| [sym:gwflow_read] | open, read | The subroutine gwflow_read opens the pond_div.gw file and reads its contents to populate groundwater pond and diversion data structures in the gwflow_module. It parses header lines and data records to configure groundwater pond parameters used in groundwater flow simulations. |

## Review Notes

- Draft input-file overlay generated from static source facts; review and complete the remaining fields before promotion.
- The source code shows only the initial open and two header reads for pond_div.gw at lines 1994-1996; further reading and parsing logic for this file is implied but not visible in the provided snippet.
- The primary target pond_div_gw is inferred from the module usage and file name but not explicitly shown in the source lines provided.
