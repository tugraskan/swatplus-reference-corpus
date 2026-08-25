---
kind: io
source_symbols:
- manure_orgmin_read
title: '`manure_om.frt`'
status: filled
source_hash: 139595b8c6e50f78
version_label: SWAT+ 62.0.0
---

**Primary target:** `manure_om(:)` (array of `type manure_attributes`)  
**Read by:** [sym:manure_orgmin_read]

## Bottom Line

The file `manure_om.frt` contains manure organic matter properties used to characterize manure types in the model.

It is optional; if the file does not exist or is named "null", an empty manure_om array is allocated.

The reader subroutine `manure_orgmin_read` loads this file and populates the `manure_om` array with manure attributes.

| Module | Role for this file |
| --- | --- |
| [sym:input_file_module] | Provides the `db_mx` variable used to store the count of manure_om records read from the file. |
| [sym:maximum_data_module] | No specific types or variables from this module are directly referenced in the reader. |
| [sym:fertilizer_data_module] | Defines the derived type `manure_attributes` and the allocatable array `manure_om` into which the file data is read. |

## File Variables

The file `manure_om.frt` is a text input file containing records of manure organic matter attributes. Each record corresponds to one manure type and is read into an element of the `manure_om` array of derived type `manure_attributes`. The file begins with two header lines, followed by multiple data records with fields matching the components of `manure_attributes`.

| Col | Header | Target | Type | Units | Meaning |
| --- | --- | --- | --- | --- | --- |
| 2 |  | `manure_om%name` | character(len=64) |  | Identifier used to crosswalk fertilizer entries, constructed from |
| 3 |  | `manure_om%frac_water` | real |  | manure_region, manure_source, and manure_type frac of manure which is water |
| 4 |  | `manure_om%fcbn` | real | kg C/kg frt | fraction of fertilizer which is carbon |
| 5 |  | `manure_om%fminn` | real | kg minN/kg frt | fraction of fertilizer which is mineral nitrogen (NO3+NH3) |
| 6 |  | `manure_om%fminp` | real | kg minN/kg frt | fraction of fertilizer which is mineral phosphorus |
| 7 |  | `manure_om%forgn` | real | kg orgN/kg frt | fraction of fertilizer which is organic nitrogen |
| 8 |  | `manure_om%forgp` | real | kg orgP/kg frt | fraction of fertilizer which is organic phosphorus |
| 9 |  | `manure_om%fnh3n` | real | kg NH3-N/kg N | fraction of mineral nitrogen content of fertilizer which is NH3 |
| 10 |  | `manure_om%description` | character(len=64) | na | description of manure type |

## Sample

```text
Example record format (fields separated by spaces or tabs):
"CattleManure 0.6 0.4 0.02 0.01 0.005 0.03 0.002 0.1 Typical cattle manure"
```

## Read Pattern

```fortran
open (107,file="manure_om.frt")
read (107,*,iostat=eof) titldum
read (107,*,iostat=eof) header
rewind (107)
read (107,*,iostat=eof) manure_om(it)%name, manure_om(it)%frac_water, manure_om(it)%fcbn, manure_om(it)%fminn, manure_om(it)%fminp, manure_om(it)%forgn, manure_om(it)%forgp, manure_om(it)%fnh3n, manure_om(it)%description
```

## I/O Operations

| Direction | Op | Unit | Statement |
| --- | --- | --- | --- |
| File setup | `open` | 107 | `open (107,file="manure_om.frt")` |
| Input | `read` | 107 | `read (107,*,iostat=eof) titldum` |
| Input | `read` | 107 | `read (107,*,iostat=eof) header` |
| Input | `read` | 107 | `read (107,*,iostat=eof) titldum` |
| File control | `rewind` | 107 | `rewind (107)` |
| Input | `read` | 107 | `read (107,*,iostat=eof) titldum` |
| Input | `read` | 107 | `read (107,*,iostat=eof) header` |
| Input | `read` | 107 | `read (107,*,iostat=eof) manure_om(it)%name, manure_om(it)%frac_water, manure_om(it)%fcbn, manure_om(it)%fminn, manure_om(it)%fminp, manure_om(it)%forgn, manure_om(it)%forgp, manure_om(it)%fnh3n, manure_om(it)%description` |
| File control | `close` | 107 | `close (107)` |

## Readers

| Procedure | Operations | Role |
| --- | --- | --- |
| [sym:manure_orgmin_read] | close, open, read, rewind | Reads the manure_om.frt file, counts the number of manure records, allocates the manure_om array accordingly, and loads each manure attribute record into the array. If the file does not exist or is named "null", allocates an empty manure_om array. |

## Review Notes

- Draft input-file overlay generated from static source facts; review and complete the remaining fields before promotion.
- The file is optional; if missing or named "null", an empty manure_om array is allocated.
- The reader counts records by reading through the file after two header lines, then rewinds to read the data into the array.
- No sample data records were found in the source; the sample read format is a constructed example based on the declared variables.
