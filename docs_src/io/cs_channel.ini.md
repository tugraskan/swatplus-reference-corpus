---
kind: io
source_symbols:
- cs_cha_read
title: '`cs_channel.ini`'
status: filled
source_hash: a60268cbfb2b6ba5
version_label: SWAT+ 62.0.0
---

**Primary target:** `cs_cha_ini(:)` (array of `type cs_cha_init_concentrations`)  
**Read by:** [sym:cs_cha_read]

## Bottom Line

The file `cs_channel.ini` provides initial constituent concentrations for channels at the start of the simulation.

It is optional and only read if the file exists.

The reader subroutine `cs_cha_read` loads this file into the array `cs_cha_ini` of derived type `cs_cha_init_concentrations`.

| Module | Role for this file |
| --- | --- |
| [sym:constituent_mass_module] | Provides the derived type `cs_cha_init_concentrations` and the array `cs_cha_ini` where the file data is stored. |
| [sym:input_file_module] | Used for general input file handling and possibly for file existence inquiry. |
| [sym:maximum_data_module] | Provides the variable `db_mx%cs_cha_ini` to store the number of records read from the file. |
| [sym:channel_data_module] | No direct variables or types explicitly assigned from this module in the reader. |
| [sym:hydrograph_module] | No direct variables or types explicitly assigned from this module in the reader. |
| [sym:sd_channel_module] | No direct variables or types explicitly assigned from this module in the reader. |
| [sym:organic_mineral_mass_module] | No direct variables or types explicitly assigned from this module in the reader. |

## File Variables

The file `cs_channel.ini` consists of multiple records each specifying a constituent name and its initial concentration in the channel at simulation start. Each record maps to an element of the array `cs_cha_ini` of type `cs_cha_init_concentrations`.

| Col | Header | Target | Type | Units | Meaning |
| --- | --- | --- | --- | --- | --- |
| 2 |  | `cs_cha_ini%name` | character (len=16) |  | name of the constituent - points to salt ion database |
| 3 |  | `cs_cha_ini%conc` | real | g/m3 | constituent concentration at start of simulation |

## Sample

```text
Example record block from `cs_channel.ini`:
  SO4      0.05
  NO3      0.02
  Cl       0.01
```

## Read Pattern

```fortran
open (107,file="cs_channel.ini")
read (107,*,iostat=eof) titldum
read (107,*,iostat=eof) header
rewind (107)
read (107,*,iostat=eof) cs_cha_ini(icsi)%name,cs_cha_ini(icsi)%conc
```

## I/O Operations

| Direction | Op | Unit | Statement |
| --- | --- | --- | --- |
| File setup | `open` | 107 | `open (107,file="cs_channel.ini")` |
| Input | `read` | 107 | `read (107,*,iostat=eof) titldum` |
| Input | `read` | 107 | `read (107,*,iostat=eof) header` |
| Input | `read` | 107 | `read (107,*,iostat=eof) titldum` |
| File control | `rewind` | 107 | `rewind (107)` |
| Input | `read` | 107 | `read (107,*,iostat=eof) titldum` |
| Input | `read` | 107 | `read (107,*,iostat=eof) header` |
| Input | `read` | 107 | `read (107,*,iostat=eof) cs_cha_ini(icsi)%name,cs_cha_ini(icsi)%conc` |
| File control | `close` | 107 | `close (107)` |

## Readers

| Procedure | Operations | Role |
| --- | --- | --- |
| [sym:cs_cha_read] | open, read, rewind, close | Reads the file `cs_channel.ini` if it exists, counts the number of constituent records, allocates the array `cs_cha_ini` accordingly, and reads each constituent's name and initial concentration into this array. |

## Review Notes

- The file `cs_channel.ini` is optional and only read if it exists, as checked by `inquire`.
- The reader first counts the number of records by reading through the file, then rewinds and reads the data into allocated arrays.
- No explicit header format or detailed sample data was found in the source; the example is inferred from typical constituent name and concentration pairs.
- The reader uses multiple modules but only `constituent_mass_module` and `maximum_data_module` provide directly referenced variables or types for this file.
- The reader also handles other files (`cs_streamobs`) unrelated to this input file.
