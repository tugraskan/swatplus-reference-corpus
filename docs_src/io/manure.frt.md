---
kind: io
source_symbols:
- manure_parm_read
title: '`manure.frt`'
status: filled
source_hash: 9d3c4678df395276
version_label: SWAT+ 62.0.0
---

**Primary target:** `manure_db(:)` (array of `type manure_database`)  
**Read by:** [sym:manure_parm_read]

## Bottom Line

manure.frt is an optional input file that defines manure types and their associated chemical and biological constituents used in the SWAT+ model.

It configures manure parameter data stored in the `manure_db` array of `type manure_database`.

The file is read by the `manure_parm_read` subroutine.

| Module | Role for this file |
| --- | --- |
| [sym:input_file_module] | provides file existence inquiry and possibly file handling utilities used by `manure_parm_read`. |
| [sym:maximum_data_module] | provides the `db_mx` variable where the maximum number of manure parameters (`manureparm`) is stored after reading. |
| [sym:fertilizer_data_module] | provides the `manure_db` array of `type manure_database` where each manure record from manure.frt is stored. |

## File Variables

The manure.frt file contains records of manure types with associated chemical and biological constituent names and pointers. Each record is read into an element of the `manure_db` array, mapping file columns to fields in the `type manure_database`.

| Col | Header | Target | Type | Units | Meaning |
| --- | --- | --- | --- | --- | --- |
| 2 |  | `manure_db%name` | character (len=25) |  | name of manure type |
| 3 |  | `manure_db%org_min` | character (len=25) |  | sediment, carbon, and nutrients |
| 4 |  | `manure_db%pests` | character (len=25) |  | pesticides - ppm |
| 5 |  | `manure_db%paths` | character (len=25) |  | pathogens - cfu |
| 6 |  | `manure_db%hmets` | character (len=25) |  | heavy metals - ppm |
| 7 |  | `manure_db%salts` | character (len=25) |  | salt ions - ppm |
| 8 |  | `manure_db%constit` | character (len=25) |  | other constituents - ppm |
| 9 |  | `manure_db%descrip` | character (len=80) |  | description |
| 10 |  | `manure_db%iorg_min` | integer |  | sediment, carbon, and nutrients - pointer to |
| 11 |  | `manure_db%ipests` | integer |  | pesticides - pointer to |
| 12 |  | `manure_db%ipaths` | integer |  | pathogens - pointer to |
| 13 |  | `manure_db%imets` | integer |  | heavy metals - pointer to |
| 14 |  | `manure_db%isalts` | integer |  | salt ions - pointer to |
| 15 |  | `manure_db%iconstit` | integer |  | other constituents - pointer to |

## Sample

```text
Example record block from manure.frt:
  ManureTypeName OrgMinName PestsName PathsName HmetsName SaltsName ConstitName DescriptionText IorgMin IPESTS IPaths IMets ISalts IConstit
  (Each field corresponds to the respective character or integer fields in `manure_database`.)
```

## Read Pattern

```fortran
open (107,file="manure.frt")
read (107,*,iostat=eof) titldum
read (107,*,iostat=eof) header
do while (eof == 0)
  read (107,*,iostat=eof) titldum
  increment record count
end do
allocate manure_db array with size based on record count
rewind (107)
read (107,*,iostat=eof) titldum
read (107,*,iostat=eof) header
do it = 1, imax
  read (107,*,iostat=eof) manure_db(it)
end do
close (107)
```

## I/O Operations

| Direction | Op | Unit | Statement |
| --- | --- | --- | --- |
| File setup | `open` | 107 | `open (107,file="manure.frt")` |
| Input | `read` | 107 | `read (107,*,iostat=eof) titldum` |
| Input | `read` | 107 | `read (107,*,iostat=eof) header` |
| Input | `read` | 107 | `read (107,*,iostat=eof) titldum` |
| File control | `rewind` | 107 | `rewind (107)` |
| Input | `read` | 107 | `read (107,*,iostat=eof) titldum` |
| Input | `read` | 107 | `read (107,*,iostat=eof) header` |
| Input | `read` | 107 | `read (107,*,iostat=eof) manure_db(it)` |
| File control | `close` | 107 | `close (107)` |

## Readers

| Procedure | Operations | Role |
| --- | --- | --- |
| [sym:manure_parm_read] | close, open, read, rewind | Reads the manure.frt file to load manure parameter records into the `manure_db` array. It first counts the number of records by reading through the file, allocates the array accordingly, then rewinds and reads all manure records into memory. It also sets the maximum manure parameter count in `db_mx%manureparm`. |

## Review Notes

- Draft input-file overlay generated from static source facts; review and complete the remaining fields before promotion.
- manure.frt is optional; if missing or named 'null', an empty manure_db array is allocated.
- The file reading logic counts records by reading a dummy variable repeatedly before allocating the array.
- No sample data block was found in the source; the sample_read_format is a generic placeholder.
