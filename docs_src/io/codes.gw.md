---
kind: io
source_symbols:
- gwflow_read
title: '`codes.gw`'
status: filled
source_hash: 8956d621ce174994
version_label: SWAT+ 62.0.0
---

**Primary target:** gwflow_module%gwflow_data  
**Read by:** [sym:gwflow_read]

## Bottom Line

The file `codes.gw` configures groundwater flow parameters and related groundwater model state for SWAT+. It is a required input file that provides essential groundwater flow data such as cell properties, aquifer zones, and transit times. The primary reader that loads and processes this file is the `gwflow_read` subroutine.

| Module | Role for this file |
| --- | --- |
| [sym:gwflow_module] | Provides the main groundwater flow data structures and variables that `gwflow_read` populates from `codes.gw`. |
| [sym:hydrograph_module] | Used for hydrograph separation arrays and output related to groundwater-surface water exchange. |
| [sym:sd_channel_module] | Used for channel cell information relevant to groundwater transit and exchange. |
| [sym:maximum_data_module] | Provides constants or maximum sizes used during reading and allocation. |
| [sym:hru_module] | Provides the `hru` derived type, which may be referenced for spatial units related to groundwater flow. |
| [sym:reservoir_data_module] | Provides reservoir data structures such as `wet_dat` that may be linked to groundwater flow. |
| [sym:cs_data_module] | Used for constituent mass and solute data relevant to groundwater solute transport. |
| [sym:constituent_mass_module] | Provides the `cs_db` data structure for constituent mass balance, used during groundwater solute reading. |
| [sym:water_allocation_module] | Provides canal data structures used when reading canal-related groundwater flow data. |
| [sym:utils] | Provides utility routines such as `split_line` used to parse variable-width input lines from `codes.gw`. |

## File Variables

The `codes.gw` file is a structured input file containing groundwater flow parameters, aquifer properties, transit times, and related spatial cell data. The `gwflow_read` subroutine reads this file line-by-line, parsing header lines and variable-width data lines into arrays and derived types defined primarily in `gwflow_module` and related modules.

| Col | Header | Target | Type | Units | Meaning |
| --- | --- | --- | --- | --- | --- |
| entire line | `header` | `header` |  |  | Reads a header line from the `codes.gw` file, typically containing metadata or column titles to guide subsequent parsing. |
| entire line | `data line` | `split_line_buf` |  |  | Reads a full data line as a string from the `codes.gw` file, which is then split into fields for parsing groundwater flow parameters. |

## Sample

```text
Example snippet from `codes.gw` (illustrative):
HEADER LINE: "CellID NumConn AquiferZone SyZone ..."
DATA LINE:   "1001 4 2 1 0.15 0.25 0.05 10.0 5.0 3.0 ..."
```

## Read Pattern

```fortran
open(in_gw,file='codes.gw')
read(in_gw,*) header
read(in_gw,'(a)') split_line_buf
```

## I/O Operations

| Direction | Op | Unit | Statement |
| --- | --- | --- | --- |
| File setup | `open` | in_gw | `open(in_gw,file='codes.gw')` |
| Input | `read` | in_gw | `read(in_gw,*) header` |
| Input | `read` | in_gw | `read(in_gw,'(a)') split_line_buf` |
| Input | `read` | in_gw | `read(in_gw,'(a)') split_line_buf` |
| File control | `close` | in_gw | `close(in_gw)` |

## Readers

| Procedure | Operations | Role |
| --- | --- | --- |
| [sym:gwflow_read] | open, read, close | The `gwflow_read` subroutine reads the `codes.gw` file to load groundwater flow parameters, aquifer and streambed properties, transit times, and related groundwater model state into the SWAT+ groundwater flow data structures. It parses header lines and variable-length data lines, allocating arrays and populating variables used throughout the groundwater flow simulation. |

## Review Notes

- Draft input-file overlay generated from static source facts; review and complete the remaining fields before promotion.
- The exact detailed format of `codes.gw` lines is not fully visible in the provided source snippet; the description is based on the reading pattern and variable usage in `gwflow_read`.
- The primary target is inferred as groundwater flow data structures in `gwflow_module` since the reader uses that module extensively and no other target is explicitly named.
