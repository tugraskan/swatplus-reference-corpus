---
kind: io
source_symbols:
- salt_cha_read
title: '`salt_channel.ini`'
status: filled
source_hash: 03fe98fee7802d35
version_label: SWAT+ 62.0.0
---

**Primary target:** `salt_cha_ini(:)` (array of `type salt_cha_init_concentrations`)  
**Read by:** [sym:salt_cha_read]

## Bottom Line

The file `salt_channel.ini` configures the initial salt ion concentrations in channel flow for the SWAT+ model.

It is optional and read if present by the `salt_cha_read` subroutine.

Each record specifies a salt constituent name and its initial concentration in g/m3.

| Module | Role for this file |
| --- | --- |
| [sym:constituent_mass_module] | Provides the derived type `salt_cha_init_concentrations` and the array `salt_cha_ini` where the file data is stored. |
| [sym:input_file_module] | Used for file existence inquiry and possibly input file handling conventions. |
| [sym:maximum_data_module] | Provides `db_mx%salt_cha_ini` which stores the number of salt constituents read from the file. |
| [sym:channel_data_module] | No direct variables or types used from this module in the reader. |
| [sym:hydrograph_module] | No direct variables or types used from this module in the reader. |
| [sym:sd_channel_module] | No direct variables or types used from this module in the reader. |
| [sym:organic_mineral_mass_module] | No direct variables or types used from this module in the reader. |

## File Variables

The file consists of records each containing a salt constituent name and its initial concentration in the channel. These map to the `salt_cha_ini` array of `type salt_cha_init_concentrations` where each element holds a `name` and a `conc` value.

| Col | Header | Target | Type | Units | Meaning |
| --- | --- | --- | --- | --- | --- |
| 2 |  | `salt_cha_ini%name` | character (len=16) |  | name of the constituent - points to salt ion database |
| 3 |  | `salt_cha_ini%conc` | real | g/m3 | salt ion concentration at start of simulation |

## Sample

```text
Example record lines from a typical `salt_channel.ini` file might look like:
  NaCl  10.5
  CaCO3 5.0
  MgSO4 3.2
where each line contains the salt constituent name (up to 16 characters) followed by its initial concentration in g/m3.
```

## Read Pattern

```fortran
open (107,file="salt_channel.ini")
read (107,*,iostat=eof) titldum
read (107,*,iostat=eof) header
rewind (107)
read (107,*,iostat=eof) salt_cha_ini(isalti)%name,salt_cha_ini(isalti)%conc
```

## I/O Operations

| Direction | Op | Unit | Statement |
| --- | --- | --- | --- |
| File setup | `open` | 107 | `open (107,file="salt_channel.ini")` |
| Input | `read` | 107 | `read (107,*,iostat=eof) titldum` |
| Input | `read` | 107 | `read (107,*,iostat=eof) header` |
| Input | `read` | 107 | `read (107,*,iostat=eof) titldum` |
| File control | `rewind` | 107 | `rewind (107)` |
| Input | `read` | 107 | `read (107,*,iostat=eof) titldum` |
| Input | `read` | 107 | `read (107,*,iostat=eof) header` |
| Input | `read` | 107 | `read (107,*,iostat=eof) salt_cha_ini(isalti)%name,salt_cha_ini(isalti)%conc` |
| File control | `close` | 107 | `close (107)` |

## Readers

| Procedure | Operations | Role |
| --- | --- | --- |
| [sym:salt_cha_read] | close, open, read, rewind | Reads the `salt_channel.ini` file if it exists, counts the number of salt constituent records, allocates the `salt_cha_ini` array accordingly, and reads each constituent's name and initial concentration into this array. |

## Review Notes

- The file is optional and read only if it exists.
- The reader first counts records by reading through the file, then rewinds and reads data into allocated arrays.
- No explicit error handling for malformed lines is present.
- The sample read format is inferred from typical salt constituent names and concentrations, as no example dataset was provided.
