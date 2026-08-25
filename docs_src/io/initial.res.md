---
kind: io
source_symbols:
- res_read_init
title: '`initial.res`'
status: filled
source_hash: 30dc21cef30862a9
version_label: SWAT+ 62.0.0
---

**Primary target:** `res_init_dat_c(:)` (array of `type reservoir_init_data_char`)  
**Read by:** [sym:res_read_init]

## Bottom Line

The file `initial.res` configures initial reservoir data points for the model, specifying paths to various initial condition input files such as organic-mineral, pesticide, pathogen, heavy metals, and salt data.

This file is optional; if it does not exist or is set to "null", the model allocates empty arrays for reservoir initialization.

The primary reader for this file is the subroutine `res_read_init`.

| Module | Role for this file |
| --- | --- |
| [sym:basin_module] | Provides the `in_res` variable which contains the filename for the initial reservoir data file (`init_res`). |
| [sym:input_file_module] | Used for general input file handling and possibly for file existence checks. |
| [sym:maximum_data_module] | Provides the `db_mx` variable which stores the maximum number of reservoir initial data records (`res_init`). |
| [sym:reservoir_data_module] | Defines the derived type `reservoir_init_data_char` and the arrays `res_init_dat_c`, `res_init`, and `wet_init` used to store the initial reservoir data read from the file. |

## File Variables

The file `initial.res` consists of records each corresponding to an instance of the derived type `reservoir_init_data_char`. Each record contains character fields pointing to initial data files for reservoir conditions, such as organic-mineral, pesticide, pathogen, heavy metals, and salt inputs.

| Col | Header | Target | Type | Units | Meaning |
| --- | --- | --- | --- | --- | --- |
| 2 |  | `res_init_dat_c%init` | character (len=25) |  | initial data-points to initial.cha |
| 3 |  | `res_init_dat_c%org_min` | character (len=25) |  | points to initial organic-mineral input file |
| 4 |  | `res_init_dat_c%pest` | character (len=25) |  | points to initial pesticide input file |
| 5 |  | `res_init_dat_c%path` | character (len=25) |  | points to initial pathogen input file |
| 6 |  | `res_init_dat_c%hmet` | character (len=25) |  | points to initial heavy metals input file |
| 7 |  | `res_init_dat_c%salt` | character (len=25) |  | points to initial salt input file |

## Sample

```text
Example record format (fields are character strings of length 25):
  <record_id> <init> <org_min> <pest> <path> <hmet> <salt>
Where each field after the record id is a filename or identifier for the respective initial data input.
```

## Read Pattern

```fortran
open (105,file=in_res%init_res)
read (105,*,iostat=eof) titldum
read (105,*,iostat=eof) header
rewind (105)
read (105,*,iostat=eof) res_init_dat_c(ires)
```

## I/O Operations

| Direction | Op | Unit | Statement |
| --- | --- | --- | --- |
| File setup | `open` | 105 | `open (105,file=in_res%init_res)` |
| Input | `read` | 105 | `read (105,*,iostat=eof) titldum` |
| Input | `read` | 105 | `read (105,*,iostat=eof) header` |
| Input | `read` | 105 | `read (105,*,iostat=eof) titldum` |
| File control | `rewind` | 105 | `rewind (105)` |
| Input | `read` | 105 | `read (105,*,iostat=eof) titldum` |
| Input | `read` | 105 | `read (105,*,iostat=eof) header` |
| Input | `read` | 105 | `read (105,*,iostat=eof) res_init_dat_c(ires)` |
| File control | `close` | 105 | `close (105)` |

## Readers

| Procedure | Operations | Role |
| --- | --- | --- |
| [sym:res_read_init] | close, open, read, rewind | Reads the `initial.res` file to load initial reservoir data points into arrays `res_init_dat_c`, `res_init`, and `wet_init`. It first checks if the file exists or is set to "null"; if not, it allocates empty arrays. Otherwise, it counts the number of records, allocates arrays accordingly, rewinds the file, and reads the data records into the typed array. |

## Review Notes

- Draft input-file overlay generated from static source facts; review and complete the remaining fields before promotion.
- The file is optional as indicated by the existence check and null string test in `res_read_init`.
- The exact format of the file beyond the typed record is not shown; the sample read format is inferred from the type and read statements.
- No sample data records were found in the source; users should consult example datasets for concrete samples.
