---
kind: io
source_symbols:
- recall_read
title: '`pest.com`'
status: filled
source_hash: efa29e2983324ff9
version_label: SWAT+ 62.0.0
---

**Primary target:** `rec_pest(:)` (array of `type recall_pesticide_inputs`)  
**Read by:** [sym:recall_read]

## Bottom Line

The file `pest.com` configures pesticide recall input data for the SWAT+ model.

It is optional and read if it exists.

The primary reader that loads this file is the `recall_read` subroutine.

| Module | Role for this file |
| --- | --- |
| [sym:hydrograph_module] | Provides hydrological flow variables and types used for reading and storing recall hydrological data. |
| [sym:input_file_module] | Supplies input file handling utilities and possibly file-related constants used by `recall_read`. |
| [sym:organic_mineral_mass_module] | Provides types and variables related to organic mineral mass used in recall data structures. |
| [sym:constituent_mass_module] | Defines the `type recall_pesticide_inputs` and related variables such as `rec_pest` used to store pesticide recall data. |
| [sym:maximum_data_module] | Provides maximum data limits and constants used for array allocations and loops in `recall_read`. |
| [sym:time_module] | Supplies time-related variables such as `time%yrc` and `time%nbyr` used to manage recall data time steps and years. |
| [sym:exco_module] | Provides variables and types related to exco (external coefficients) used in recall data processing. |
| [sym:recall_module] | Defines the `recall` and `recall_db` data structures that store recall hydrological and pesticide data read from files. |

## File Variables

The `pest.com` file consists of records describing pesticide recall inputs, each mapped to an element of the `rec_pest` array of type `recall_pesticide_inputs`. Each record includes a name, number of elements, recall type, filename, and associated hydrological output data.

| Col | Header | Target | Type | Units | Meaning |
| --- | --- | --- | --- | --- | --- |
| 2 |  | `rec_pest%name` | character (len=16) |  | Name identifier for the pesticide recall input record. |
| 3 |  | `rec_pest%num` | integer |  | Number of elements associated with this pesticide recall input. |
| 4 |  | `rec_pest%typ` | integer |  | Recall type indicating the time step: 1=day, 2=month, 3=year. |
| 5 |  | `rec_pest%filename` | character(len=13) |  | Filename of the pesticide recall data file to be read. |
| 6 |  | `rec_pest%hd_pest` | type (constituent_mass) |  | Hydrological output data associated with the pesticide recall input; units are in cubic meters per second (cms) and milligrams per liter (mg/L). |

## Sample

```text
1 PESTNAME        5 1 pestfile.dat
2 PESTNAME2       3 2 pestfile2.dat
```

## Read Pattern

```fortran
open (107,file="pest.com")
read (107,*,iostat=eof) titldum
read (107,*,iostat=eof) header
read (107,*,iostat=eof) i
rewind (107)
read (107,*,iostat=eof) ipestcom_db
backspace (107)
read (107,*,iostat = eof) k, rec_pest(i)%name, rec_pest(i)%typ, rec_pest(i)%filename
```

## I/O Operations

| Direction | Op | Unit | Statement |
| --- | --- | --- | --- |
| File setup | `open` | 107 | `open (107,file="pest.com")` |
| Input | `read` | 107 | `read (107,*,iostat=eof) titldum` |
| Input | `read` | 107 | `read (107,*,iostat=eof) header` |
| Input | `read` | 107 | `read (107,*,iostat=eof) i` |
| File control | `rewind` | 107 | `rewind (107)` |
| Input | `read` | 107 | `read (107,*,iostat=eof) titldum` |
| Input | `read` | 107 | `read (107,*,iostat=eof) header` |
| Input | `read` | 107 | `read (107,*,iostat=eof) ipestcom_db` |
| Input | `read` | 107 | `read (107,*,iostat=eof) i` |
| File control | `backspace` | 107 | `backspace (107)` |
| Input | `read` | 107 | `read (107,*,iostat = eof) k, rec_pest(i)%name, rec_pest(i)%typ, rec_pest(i)%filename` |
| File control | `close` | 107 | `close (107)` |

## Readers

| Procedure | Operations | Role |
| --- | --- | --- |
| [sym:recall_read] | backspace, close, open, read, rewind | Reads the pesticide recall input file `pest.com` if it exists, parsing its header and records into the `rec_pest` array of `type recall_pesticide_inputs`. It allocates memory for and reads associated hydrological data files referenced by each pesticide record. |

## Review Notes

- Draft input-file overlay generated from static source facts; review and complete the remaining fields before promotion.
