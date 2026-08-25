---
kind: io
source_symbols:
- wet_read
title: '`wetland.wet`'
status: filled
source_hash: 324021b6634e671e
version_label: SWAT+ 62.0.0
---

**Primary target:** `wet_dat_c(:)` (array of `type reservoir_data_char_input`)  
**Read by:** [sym:wet_read]

## Bottom Line

The file `wetland.wet` configures reservoir wetland data inputs for the SWAT+ model.

It is optional: if the file does not exist or is set to "null", empty arrays are allocated.

The reader routine `wet_read` loads this file and populates the `wet_dat_c` array of type `reservoir_data_char_input`.

| Module | Role for this file |
| --- | --- |
| [sym:basin_module] | Provides the `in_res` variable which contains the filename for the wetland input file (`in_res%wet`). |
| [sym:input_file_module] | Likely provides input file handling utilities or constants used by `wet_read` (not explicitly referenced in the source lines). |
| [sym:maximum_data_module] | Provides `db_mx` which stores the maximum number of wetland data records (`db_mx%wet_dat`). |
| [sym:reservoir_data_module] | Defines the derived type `reservoir_data_char_input` and the arrays `wet_dat_c` and `wet_dat` where the file data is stored. |
| [sym:reservoir_module] | Likely related to reservoir state or operations, used indirectly by `wet_read` (no direct variable usage visible). |
| [sym:hydrograph_module] | Imported but no direct usage visible in `wet_read`. |
| [sym:constituent_mass_module] | Imported but no direct usage visible in `wet_read`. |
| [sym:pesticide_data_module] | Imported but no direct usage visible in `wet_read`. |
| [sym:res_salt_module] | Imported but no direct usage visible in `wet_read`. |
| [sym:res_cs_module] | Imported but no direct usage visible in `wet_read`. |

## File Variables

The `wetland.wet` file consists of multiple records each describing reservoir wetland data with character fields. Each record is read into an element of the `wet_dat_c` array of type `reservoir_data_char_input`, which holds named references to related input files for initial conditions, hydrology, release, sediment, and nutrient inputs.

| Col | Header | Target | Type | Units | Meaning |
| --- | --- | --- | --- | --- | --- |
| 2 |  | `wet_dat_c%name` | character (len=25) |  | Name identifier for the wetland reservoir data record. |
| 3 |  | `wet_dat_c%init` | character (len=25) |  | Initial data points file reference, pointing to initial.res. |
| 4 |  | `wet_dat_c%hyd` | character (len=25) |  | Hydrology input file reference, pointing to hydrology.res. |
| 5 |  | `wet_dat_c%release` | character (len=25) |  | Flag indicating release type: 0 for simulated, 1 for measured outflow. |
| 6 |  | `wet_dat_c%sed` | character (len=25) |  | Sediment input file reference, pointing to sediment.res. |
| 7 |  | `wet_dat_c%nut` | character (len=25) |  | Nutrient input file reference, pointing to nutrient.res. |

## Sample

```text
Example record format (fields separated by spaces or tabs):
1 reservoir_name initial.res hydrology.res 0 sediment.res nutrient.res
```

## Read Pattern

```fortran
open (105,file=in_res%wet)
read (105,*,iostat=eof) titldum
read (105,*,iostat=eof) header
read (105,*,iostat=eof) i
rewind (105)
read (105,*,iostat = eof) titldum
backspace (105)
read (105,*,iostat=eof) k, wet_dat_c(ires)
```

## I/O Operations

| Direction | Op | Unit | Statement |
| --- | --- | --- | --- |
| File setup | `open` | 105 | `open (105,file=in_res%wet)` |
| Input | `read` | 105 | `read (105,*,iostat=eof) titldum` |
| Input | `read` | 105 | `read (105,*,iostat=eof) header` |
| Input | `read` | 105 | `read (105,*,iostat=eof) i` |
| File control | `rewind` | 105 | `rewind (105)` |
| Input | `read` | 105 | `read (105,*,iostat = eof) titldum` |
| Input | `read` | 105 | `read (105,*,iostat=eof) header` |
| Input | `read` | 105 | `read (105,*,iostat=eof) i` |
| File control | `backspace` | 105 | `backspace (105)` |
| Input | `read` | 105 | `read (105,*,iostat=eof) k, wet_dat_c(ires)` |
| File control | `close` | 105 | `close (105)` |

## Readers

| Procedure | Operations | Role |
| --- | --- | --- |
| [sym:wet_read] | backspace, close, open, read, rewind | Reads the `wetland.wet` input file if it exists and is not set to "null". It counts the number of records, allocates arrays accordingly, and reads each record into the `wet_dat_c` array of type `reservoir_data_char_input`. If the file is missing or set to "null", it allocates empty arrays. |

## Review Notes

- Draft input-file overlay generated from static source facts; review and complete the remaining fields before promotion.
- The file is optional as indicated by the existence check and allocation of empty arrays if missing or set to "null".
- The `wet_read` routine reads the file header and counts records before reading data, ensuring proper allocation.
- No sample data records were found in the source; the sample format is inferred from the read pattern and type definition.
