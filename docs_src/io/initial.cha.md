---
kind: io
source_symbols:
- ch_read_init
title: '`initial.cha`'
status: filled
source_hash: 41fadf04504eb931
version_label: SWAT+ 62.0.0
---

**Primary target:** `ch_init(:)` (array of `type channel_init_datafiles`)  
**Read by:** [sym:ch_read_init]

## Bottom Line

The file `initial.cha` is an optional input file that configures initial channel-related organic, pesticide, pathogen, heavy metal, and salt data files for the SWAT+ model.

It is read by the `ch_read_init` subroutine, which loads its records into the array `ch_init` of type `channel_init_datafiles`.

| Module | Role for this file |
| --- | --- |
| [sym:basin_module] | provides the variable `db_mx` which stores the count of channel initialization records read from the file. |
| [sym:input_file_module] | provides the variable `in_cha` which contains the filename `in_cha%init` for the `initial.cha` input file. |
| [sym:maximum_data_module] | provides constants or limits used for allocation sizing (e.g., `db_mx%ch_init`), controlling the size of the `ch_init` and `sd_init` arrays. |
| [sym:channel_data_module] | provides the derived type `channel_init_datafiles` and the arrays `ch_init` where the file records are stored. |
| [sym:sd_channel_module] | provides the array `sd_init` which is allocated alongside `ch_init` but not directly read from the file. |

## File Variables

The `initial.cha` file consists of records that map channel initialization data files for various substances. Each record corresponds to one `channel_init_datafiles` instance, with fields specifying filenames for organic-mineral, pesticide, pathogen, heavy metals, and salt initial data.

| Col | Header | Target | Type | Units | Meaning |
| --- | --- | --- | --- | --- | --- |
| 2 |  | `ch_init%name` | character(len=16) |  | Identifier name for the channel initialization record |
| 3 |  | `ch_init%org_min` | character(len=16) |  | points to initial organic-mineral input file |
| 4 |  | `ch_init%pest` | character(len=16) |  | points to initial pesticide input file |
| 5 |  | `ch_init%path` | character(len=16) |  | points to initial pathogen input file |
| 6 |  | `ch_init%hmet` | character(len=16) |  | points to initial heavy metals input file |
| 7 |  | `ch_init%salt` | character(len=16) |  | points to initial salt input file |

## Sample

```text
Example record from `initial.cha` (from Ames_sub1 dataset):
  default  org_min_file  pest_file  path_file  hmet_file  salt_file
```

## Read Pattern

```fortran
open (105,file=in_cha%init)
read (105,*,iostat=eof) titldum
read (105,*,iostat=eof) header
rewind (105)
read (105,*,iostat=eof) ch_init(ich)
```

## I/O Operations

| Direction | Op | Unit | Statement |
| --- | --- | --- | --- |
| File setup | `open` | 105 | `open (105,file=in_cha%init)` |
| Input | `read` | 105 | `read (105,*,iostat=eof) titldum` |
| Input | `read` | 105 | `read (105,*,iostat=eof) header` |
| Input | `read` | 105 | `read (105,*,iostat=eof) titldum` |
| File control | `rewind` | 105 | `rewind (105)` |
| Input | `read` | 105 | `read (105,*,iostat=eof) titldum` |
| Input | `read` | 105 | `read (105,*,iostat=eof) header` |
| Input | `read` | 105 | `read (105,*,iostat=eof) ch_init(ich)` |
| File control | `close` | 105 | `close (105)` |

## Readers

| Procedure | Operations | Role |
| --- | --- | --- |
| [sym:ch_read_init] | close, open, read, rewind | Reads the `initial.cha` file if it exists and is not set to "null". It counts the number of channel initialization records, allocates the `ch_init` and `sd_init` arrays accordingly, then reads all records into `ch_init`. |

## Review Notes

- Draft input-file overlay generated from static source facts; review and complete the remaining fields before promotion.
- The file `initial.cha` is optional; if missing or set to "null", empty arrays are allocated.
- The `name` field's exact semantic meaning is not explicitly documented in source; assumed to be an identifier for the record.
