---
kind: io
source_symbols:
- gwflow_read
title: '`phreato_cell.gw`'
status: filled
source_hash: 8956d621ce174994
version_label: SWAT+ 62.0.0
---

**Primary target:** gwflow_module.phreato_cell(:)  
**Read by:** [sym:gwflow_read]

## Bottom Line

The file phreato_cell.gw configures groundwater phreatophyte cell data for the SWAT+ groundwater flow model.

It is an optional input file that provides cell IDs and associated phreatophyte area fractions used to represent groundwater evapotranspiration.

The primary reader for this file is the gwflow_read subroutine, which reads and stores this data into arrays in the gwflow_module.

| Module | Role for this file |
| --- | --- |
| [sym:gwflow_module] | Provides the phreato_cell derived type array and arrays gw_phyt_ids and gw_phyt_area where the file data is stored. |
| [sym:hydrograph_module] |  |
| [sym:sd_channel_module] |  |
| [sym:maximum_data_module] |  |
| [sym:hru_module] |  |
| [sym:reservoir_data_module] |  |
| [sym:cs_data_module] |  |
| [sym:constituent_mass_module] |  |
| [sym:water_allocation_module] |  |
| [sym:utils] | Provides the split_line utility used for parsing lines in other input files, though not directly in this file's reading. |

## File Variables

The phreato_cell.gw file contains groundwater phreatophyte cell data with a header line followed by records of cell IDs and associated phreatophyte area fractions. The gwflow_read subroutine reads this file line-by-line, storing the cell IDs and area fractions into arrays for groundwater evapotranspiration modeling.

| Col | Header | Target | Type | Units | Meaning |
| --- | --- | --- | --- | --- | --- |
| 1 | `header` | `header` |  |  | The first two lines read as header lines containing metadata or column headers, which are skipped or stored as character strings but not parsed further. |
| 1 | `cell_id` | `cell_id` |  |  | Each cell_id read corresponds to a groundwater cell identifier representing a spatial grid cell with phreatophyte vegetation. |
| 1 | `gw_phyt_ids(i)` | `gw_phyt_ids(i)` |  |  | The groundwater phreatophyte cell IDs are read again after rewinding the file and stored in the gw_phyt_ids array for use in groundwater evapotranspiration calculations. |
| 2 | `gw_phyt_area(i)` | `gw_phyt_area(i)` |  |  | The groundwater phreatophyte area fractions corresponding to each cell ID are read and stored in the gw_phyt_area array, representing the fraction of the cell area covered by phreatophytes. |

## Sample

```text
Header line 1 (metadata or description)
Header line 2 (column titles)
12345
12345 0.35
67890 0.50
13579 0.20
```

## Read Pattern

```fortran
open(in_gw,file='phreato_cell.gw')
read(in_gw,*) header
read(in_gw,*) header
read(in_gw,*,iostat=eof) cell_id
rewind(in_gw)
read(in_gw,*) header
read(in_gw,*) header
read(in_gw,*) gw_phyt_ids(i),gw_phyt_area(i)
```

## I/O Operations

| Direction | Op | Unit | Statement |
| --- | --- | --- | --- |
| File setup | `open` | in_gw | `open(in_gw,file='phreato_cell.gw')` |
| Input | `read` | in_gw | `read(in_gw,*) header` |
| Input | `read` | in_gw | `read(in_gw,*) header` |
| Input | `read` | in_gw | `read(in_gw,*,iostat=eof) cell_id` |
| File control | `rewind` | in_gw | `rewind(in_gw)` |
| Input | `read` | in_gw | `read(in_gw,*) header` |
| Input | `read` | in_gw | `read(in_gw,*) header` |
| Input | `read` | in_gw | `read(in_gw,*) gw_phyt_ids(i),gw_phyt_area(i)` |
| File control | `close` | in_gw | `close(in_gw)` |

## Readers

| Procedure | Operations | Role |
| --- | --- | --- |
| [sym:gwflow_read] | open, read, rewind, close | The gwflow_read subroutine reads the phreato_cell.gw file to load groundwater phreatophyte cell IDs and their associated area fractions into arrays used by the groundwater flow model to represent groundwater evapotranspiration. |

## Review Notes

- Draft input-file overlay generated from static source facts; review and complete the remaining fields before promotion.
- The file appears optional as there is no error handling for missing file in the snippet; the reader reads header lines twice and rewinds before reading data, indicating a two-pass read pattern.
- Module usage for most modules is empty because this file's data is stored mainly in gwflow_module arrays; utils module is used elsewhere in gwflow_read but not directly for this file.
