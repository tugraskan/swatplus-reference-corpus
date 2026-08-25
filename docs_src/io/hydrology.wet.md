---
kind: io
source_symbols:
- wet_read_hyd
title: '`hydrology.wet`'
status: filled
source_hash: 4c0d4e12af970b21
version_label: SWAT+ 62.0.0
---

**Primary target:** `wet_hyddb(:)` (array of `type wetland_hyd_data`)  
**Read by:** [sym:wet_read_hyd]

## Bottom Line

The `hydrology.wet` input file configures wetland hydrology parameters for HRUs in the model.

It is optional; if the file does not exist or is set to "null", the wetland hydrology database is allocated empty.

The file is read by the `wet_read_hyd` subroutine, which populates the `wet_hyddb` array of `wetland_hyd_data` records.

| Module | Role for this file |
| --- | --- |
| [sym:basin_module] | Provides the `bsn_cc` variable used to check if groundwater flow modeling is enabled (e.g., `bsn_cc%gwflow`). |
| [sym:input_file_module] | Supplies the `in_res` variable that contains the filename for the `hydrology.wet` input file (`in_res%hyd_wet`). |
| [sym:maximum_data_module] | Provides the `db_mx` variable where the maximum number of wetland hydrology records (`db_mx%wet_hyd`) is stored. |
| [sym:reservoir_data_module] | Defines the `wetland_hyd_data` type and the `wet_hyddb` array where the wetland hydrology records are stored. |
| [sym:output_landscape_module] | Provides the `wet_hyd` array used for default value calculations during reading. |
| [sym:gwflow_module] | Provides variables and flags related to groundwater flow and wetland sediment thickness (`in_wet_cell`, `wet_thick`, `gw_wet_flag`, `out_gw`). |

## File Variables

The `hydrology.wet` file contains tabular data records describing wetland hydrology parameters for each HRU. Each record corresponds to one wetland and is read into an element of the `wet_hyddb` array of type `wetland_hyd_data`. The file has a header and title lines that are skipped during reading.

| Col | Header | Target | Type | Units | Meaning |
| --- | --- | --- | --- | --- | --- |
| 2 |  | `wet_hyddb%name` | character(len=25) |  | Wetland name identifier |
| 3 |  | `wet_hyddb%psa` | real | frac | Fraction of HRU area at principal spillway (i.e., when surface inlet riser flow starts) |
| 4 |  | `wet_hyddb%pdep` | real | mm | Average depth of water at principal spillway |
| 5 |  | `wet_hyddb%esa` | real | frac | Fraction of HRU area at emergency spillway (i.e., when water starts to spill into ditch) |
| 6 |  | `wet_hyddb%edep` | real | mm | Average depth of water at emergency spillway |
| 7 |  | `wet_hyddb%k` | real | mm/hr | Hydraulic conductivity of the wetland bottom |
| 8 |  | `wet_hyddb%evrsv` | real | none | Wetland evaporation coefficient |
| 9 |  | `wet_hyddb%acoef` | real | none | Volume-surface area coefficient for HRU impoundment |
| 10 |  | `wet_hyddb%bcoef` | real | none | Volume-depth coefficient for HRU impoundment |
| 11 |  | `wet_hyddb%ccoef` | real | none | Volume-depth coefficient for HRU impoundment |
| 12 |  | `wet_hyddb%frac` | real | none | Fraction of HRU that drains into impoundment |

## Sample

```text
Example record lines from a typical `hydrology.wet` file (excluding header lines):
wet001 0.08 150.0 0.12 225.0 0.01 0.7 1.0 1.0 1.0 0.5
wet002 0.10 140.0 0.15 210.0 0.02 0.65 1.1 1.0 1.0 0.6
```

## Read Pattern

```fortran
open (105,file=in_res%hyd_wet)
read (105,*,iostat=eof) titldum
read (105,*,iostat=eof) header
rewind (105)
backspace (105)
read (105,*,iostat=eof) wet_hyddb(ires)
```

## I/O Operations

| Direction | Op | Unit | Statement |
| --- | --- | --- | --- |
| File setup | `open` | 105 | `open (105,file=in_res%hyd_wet)` |
| Input | `read` | 105 | `read (105,*,iostat=eof) titldum` |
| Input | `read` | 105 | `read (105,*,iostat=eof) header` |
| Input | `read` | 105 | `read (105,*,iostat=eof) titldum` |
| File control | `rewind` | 105 | `rewind (105)` |
| Input | `read` | 105 | `read (105,*,iostat=eof) titldum` |
| Input | `read` | 105 | `read (105,*,iostat=eof) header` |
| Input | `read` | 105 | `read (105,*,iostat=eof) titldum` |
| File control | `backspace` | 105 | `backspace (105)` |
| Input | `read` | 105 | `read (105,*,iostat=eof) wet_hyddb(ires)` |
| File control | `close` | 105 | `close (105)` |

## Readers

| Procedure | Operations | Role |
| --- | --- | --- |
| [sym:wet_read_hyd] | backspace, close, open, read, rewind | Reads the `hydrology.wet` input file to populate the `wet_hyddb` array with wetland hydrology parameters. It first checks if the file exists and is not set to "null". If present, it counts the number of records, allocates the array, and reads each record. It applies default values for some fields if they are zero or missing. Additionally, if groundwater flow modeling is enabled and the `gw_wet_flag` is set, it reads wetland bottom sediment thickness from the separate `gwflow.wetland` file and updates the `wet_thick` array accordingly. |

## Review Notes

- Draft input-file overlay generated from static source facts; review and complete the remaining fields before promotion.
- The `wet_read_hyd` routine sets default values for `psa`, `esa`, and `evrsv` if they are zero or less after reading.
- The reader also optionally reads wetland bed thickness from `gwflow.wetland` if groundwater flow is enabled and the flag is set.
- No sample data records were found in the source; the sample read format is inferred from typical usage but should be verified with actual datasets.
