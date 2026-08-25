---
kind: io
source_symbols:
- cs_aqu_read
title: '`cs_aqu.ini`'
status: filled
source_hash: 4b3f784e30924c29
version_label: SWAT+ 62.0.0
---

**Primary target:** `cs_aqu_ini(:)` (array of `type cs_aqu_init_concentrations`)  
**Read by:** [sym:cs_aqu_read]

## Bottom Line

The file `cs_aqu.ini` provides initial concentrations of constituents sorbed in aquifers at the start of the simulation.

It is optional and only read if the file exists and is not named "null".

The reader subroutine `cs_aqu_read` loads this file, allocating and populating the array `cs_aqu_ini` with constituent names and their initial sorbed concentrations.

| Module | Role for this file |
| --- | --- |
| [sym:constituent_mass_module] | Provides the derived type `cs_aqu_init_concentrations` and the array `cs_aqu_ini` where the file data is stored. |
| [sym:input_file_module] | Used for input file handling and possibly related constants or utilities for reading input files. |
| [sym:maximum_data_module] | Provides the variable `db_mx%cs_ini` which stores the number of constituent records read from the file. |

## File Variables

The file `cs_aqu.ini` consists of multiple records each containing a constituent name and its initial sorbed concentration in the aquifer. These records are read into an array of derived type `cs_aqu_init_concentrations` named `cs_aqu_ini`.

| Col | Header | Target | Type | Units | Meaning |
| --- | --- | --- | --- | --- | --- |
| 2 |  | `cs_aqu_ini%name` | character (len=16) |  | name of the constituent - points to constituent database |
| 3 |  | `cs_aqu_ini%aqu` | real | ppm | concentration, sorbed mass at start of simulation |

## Sample

```text
Example records from `cs_aqu.ini` might look like:
"NITRATE         0.15"
"PHOSPHORUS      0.05"
"ORGANIC_CARBON  0.10"
Each line contains a constituent name (up to 16 characters) followed by its initial sorbed concentration in ppm.
```

## Read Pattern

```fortran
open (107,file="cs_aqu.ini")
read (107,*,iostat=eof) titldum
read (107,*,iostat=eof) header
read (107,*,iostat=eof) header
read (107,*,iostat=eof) titldum
rewind (107)
read (107,*,iostat=eof) titldum
read (107,*,iostat=eof) header
read (107,*,iostat=eof) header
read (107,*,iostat=eof) cs_aqu_ini(ics)%name,cs_aqu_ini(ics)%aqu
```

## I/O Operations

| Direction | Op | Unit | Statement |
| --- | --- | --- | --- |
| File setup | `open` | 107 | `open (107,file="cs_aqu.ini")` |
| Input | `read` | 107 | `read (107,*,iostat=eof) titldum` |
| Input | `read` | 107 | `read (107,*,iostat=eof) header` |
| Input | `read` | 107 | `read (107,*,iostat=eof) header` |
| Input | `read` | 107 | `read (107,*,iostat=eof) titldum` |
| File control | `rewind` | 107 | `rewind (107)` |
| Input | `read` | 107 | `read (107,*,iostat=eof) titldum` |
| Input | `read` | 107 | `read (107,*,iostat=eof) header` |
| Input | `read` | 107 | `read (107,*,iostat=eof) header` |
| Input | `read` | 107 | `read (107,*,iostat=eof) cs_aqu_ini(ics)%name,cs_aqu_ini(ics)%aqu` |
| File control | `close` | 107 | `close (107)` |

## Readers

| Procedure | Operations | Role |
| --- | --- | --- |
| [sym:cs_aqu_read] | open, read, rewind, close | Reads the `cs_aqu.ini` file if it exists and is not "null". It counts the number of constituent records, allocates the `cs_aqu_ini` array accordingly, allocates the `aqu` array inside each record, then reads constituent names and their initial sorbed concentrations into `cs_aqu_ini`. |

## Review Notes

- The file is optional and only read if it exists and is not named "null".
- The reader first counts the number of records by reading through the file, then rewinds and reads the data into allocated arrays.
- The `aqu` array inside each `cs_aqu_ini` element is allocated with size `cs_db%num_cs + cs_db%num_cs`, initialized to zero before reading actual values.
- No sample data was found in the source; the sample format is inferred from the read statement and type definitions.
