---
kind: io
source_symbols:
- gwflow_read
title: '`phreato.gw`'
status: filled
source_hash: 8956d621ce174994
version_label: SWAT+ 62.0.0
---

**Primary target:** gwflow_module groundwater flow state variables and parameters  
**Read by:** [sym:gwflow_read]

## Bottom Line

The file `phreato.gw` provides groundwater flow parameters and initial conditions for the SWAT+ groundwater flow model component.

It is an optional input file that configures aquifer properties, groundwater temperature, water table depth, and related parameters.

The primary reader for this file is the `gwflow_read` subroutine, which parses and stores the data into variables and arrays defined in the `gwflow_module` and related modules.

| Module | Role for this file |
| --- | --- |
| [sym:gwflow_module] | Provides groundwater flow state variables and arrays such as aquifer properties, groundwater temperature, water table depth, and related parameters that `gwflow_read` populates from `phreato.gw`. |
| [sym:hydrograph_module] | Imported but no direct evidence of variables used from this module for reading `phreato.gw` in the provided source snippet. |
| [sym:sd_channel_module] | Imported but no direct evidence of variables used from this module for reading `phreato.gw` in the provided source snippet. |
| [sym:maximum_data_module] | Imported but no direct evidence of variables used from this module for reading `phreato.gw` in the provided source snippet. |
| [sym:hru_module] | Imports the derived type `hru` but no direct evidence of its use for reading `phreato.gw` in the provided source snippet. |
| [sym:reservoir_data_module] | Imports `wet_dat` but no direct evidence of its use for reading `phreato.gw` in the provided source snippet. |
| [sym:cs_data_module] | Imported but no direct evidence of variables used from this module for reading `phreato.gw` in the provided source snippet. |
| [sym:constituent_mass_module] | Imports `cs_db` but no direct evidence of its use for reading `phreato.gw` in the provided source snippet. |
| [sym:water_allocation_module] | Imports `canal` but no direct evidence of its use for reading `phreato.gw` in the provided source snippet. |
| [sym:utils] | Imports the utility subroutine `split_line` which is used for parsing lines in other parts of `gwflow_read` but not directly shown for `phreato.gw` reading. |

## File Variables

The `phreato.gw` file contains groundwater flow parameters and initial conditions arranged in a structured text format. The `gwflow_read` subroutine reads this file line-by-line, extracting header lines and groundwater parameter values into corresponding Fortran variables and arrays.

| Col | Header | Target | Type | Units | Meaning |
| --- | --- | --- | --- | --- | --- |
| 1 | `Header lines` | `header` |  |  | The initial header lines read from the file, likely containing metadata or descriptive text for the groundwater parameter data section. |
| 1 | `Single value` | `single_value` |  |  | A single numeric value read after the headers, possibly a count or a key parameter used internally by the reader to control subsequent reading logic. |
| 1-2 | `Groundwater phytoplankton parameters` | `gw_phyt_dep(i)` |  |  | Groundwater phytoplankton depth values read per record, representing depth parameters for groundwater phytoplankton modeling. |
| 2 | `Groundwater phytoplankton rate` | `gw_phyt_rate(i)` |  |  | Groundwater phytoplankton rate values read per record, representing growth or decay rates for groundwater phytoplankton. |

## Sample

```text
Example lines from `phreato.gw` might look like:
"Groundwater Flow Parameters"
"Aquifer properties and initial conditions"
1.0
0.5 0.02
1.2 0.03
...
Where the first two lines are headers, followed by a single numeric value, then pairs of groundwater phytoplankton depth and rate values per record.
```

## Read Pattern

```fortran
open(in_gw,file='phreato.gw')
read(in_gw,*) header
read(in_gw,*) header
read(in_gw,*,iostat=eof) single_value
rewind(in_gw)
read(in_gw,*) header
read(in_gw,*) header
read(in_gw,*) gw_phyt_dep(i),gw_phyt_rate(i)
```

## I/O Operations

| Direction | Op | Unit | Statement |
| --- | --- | --- | --- |
| File setup | `open` | in_gw | `open(in_gw,file='phreato.gw')` |
| Input | `read` | in_gw | `read(in_gw,*) header` |
| Input | `read` | in_gw | `read(in_gw,*) header` |
| Input | `read` | in_gw | `read(in_gw,*,iostat=eof) single_value` |
| File control | `rewind` | in_gw | `rewind(in_gw)` |
| Input | `read` | in_gw | `read(in_gw,*) header` |
| Input | `read` | in_gw | `read(in_gw,*) header` |
| Input | `read` | in_gw | `read(in_gw,*) gw_phyt_dep(i),gw_phyt_rate(i)` |
| File control | `close` | in_gw | `close(in_gw)` |

## Readers

| Procedure | Operations | Role |
| --- | --- | --- |
| [sym:gwflow_read] | open, read, rewind, close | The `gwflow_read` subroutine reads the `phreato.gw` file to load groundwater flow parameters and initial conditions into the model's groundwater flow state variables. It handles file opening, reading header and data lines, rewinding for multiple passes, and closing the file. |

## Review Notes

- Draft input-file overlay generated from static source facts; review and complete the remaining fields before promotion.
- The exact detailed mapping of all groundwater parameters read from `phreato.gw` is not fully visible in the provided source snippet; the overlay covers the visible read operations and inferred purpose.
- The `gw_phyt_dep` and `gw_phyt_rate` variables appear to be groundwater phytoplankton parameters but the source context is limited; this interpretation is based on variable naming and read patterns.
