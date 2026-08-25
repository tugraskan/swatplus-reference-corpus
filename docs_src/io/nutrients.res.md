---
kind: io
source_symbols:
- res_read_nut
title: '`nutrients.res`'
status: filled
source_hash: d9439971e17d1539
version_label: SWAT+ 62.0.0
---

**Primary target:** `res_nut(:)` (array of `type reservoir_nut_data`)  
**Read by:** [sym:res_read_nut]

## Bottom Line

The `nutrients.res` input file configures nutrient settling and loss parameters for reservoirs in the watershed.

It is optional; if the file does not exist or is set to "null", no nutrient data is loaded.

The file is read by the `res_read_nut` subroutine, which loads data into the `res_nut` array of `type reservoir_nut_data`.

| Module | Role for this file |
| --- | --- |
| [sym:input_file_module] | Provides the `in_res` variable which contains the filename `nut_res` for the nutrients.res input file. |
| [sym:maximum_data_module] | Provides the `db_mx` variable where `db_mx%res_nut` is set to the number of nutrient records read. |
| [sym:reservoir_data_module] | Defines the `type reservoir_nut_data` and the `res_nut` array where nutrient records are stored. |

## File Variables

The `nutrients.res` file contains tabular data describing nutrient settling and loss rates for reservoirs. Each record corresponds to one reservoir's nutrient parameters and is read into an element of the `res_nut` array of derived type `reservoir_nut_data`. The file includes a title line, a header line, and then multiple data records.

| Col | Header | Target | Type | Units | Meaning |
| --- | --- | --- | --- | --- | --- |
| 2 |  | `res_nut%name` | character(len=25) |  | Reservoir name identifier |
| 3 |  | `res_nut%ires1` | integer | none | Beginning month/day of mid-year nutrient settling season |
| 4 |  | `res_nut%ires2` | integer | none | Ending month/day of mid-year nutrient settling season |
| 5 |  | `res_nut%nsetlr1` | real | frac | Nitrogen mass loss rate during mid-year period (annual fraction) |
| 6 |  | `res_nut%nsetlr2` | real | frac | Nitrogen mass loss rate during remainder of year (annual fraction) |
| 7 |  | `res_nut%psetlr1` | real | frac | Phosphorus mass loss rate during mid-year period (annual fraction) |
| 8 |  | `res_nut%psetlr2` | real | frac | Phosphorus mass loss rate during remainder of year (annual fraction) |
| 9 |  | `res_nut%nsolr` | real | none | Loss rate for soluble nitrogen species (NO3, NH3, NO2) (annual fraction) |
| 10 |  | `res_nut%psolr` | real | none | Loss rate for soluble phosphorus (annual fraction) |
| 11 |  | `res_nut%theta_n` | real | none | Temperature adjustment factor for nitrogen loss (settling) |
| 12 |  | `res_nut%theta_p` | real | none | Temperature adjustment factor for phosphorus loss (settling) |
| 13 |  | `res_nut%conc_nmin` | real | ppm | Minimum nitrogen concentration threshold for settling |
| 14 |  | `res_nut%conc_pmin` | real | ppm | Minimum phosphorus concentration threshold for settling |

## Sample

```text
Example record format from nutrients.res (fields separated by spaces or tabs):
ReservoirName 3 9 0.05 0.02 0.04 0.01 0.9 0.8 1.1 1.0 0.1 0.01
```

## Read Pattern

```fortran
open (105,file=in_res%nut_res)
read (105,*,iostat=eof) titldum
read (105,*,iostat=eof) header
rewind (105)
backspace (105)
read (105,*,iostat=eof) res_nut(ires)
```

## I/O Operations

| Direction | Op | Unit | Statement |
| --- | --- | --- | --- |
| File setup | `open` | 105 | `open (105,file=in_res%nut_res)` |
| Input | `read` | 105 | `read (105,*,iostat=eof) titldum` |
| Input | `read` | 105 | `read (105,*,iostat=eof) header` |
| Input | `read` | 105 | `read (105,*,iostat=eof) titldum` |
| File control | `rewind` | 105 | `rewind (105)` |
| Input | `read` | 105 | `read (105,*,iostat=eof) titldum` |
| Input | `read` | 105 | `read (105,*,iostat=eof) header` |
| Input | `read` | 105 | `read (105,*,iostat=eof) titldum` |
| File control | `backspace` | 105 | `backspace (105)` |
| Input | `read` | 105 | `read (105,*,iostat=eof) res_nut(ires)` |
| File control | `close` | 105 | `close(105)` |

## Readers

| Procedure | Operations | Role |
| --- | --- | --- |
| [sym:res_read_nut] | backspace, close, open, read, rewind | Reads the `nutrients.res` file to load nutrient settling and loss parameters into the `res_nut` array. It first checks if the file exists and is not set to "null". If present, it counts the number of records, allocates the `res_nut` array accordingly, then reads each nutrient record into the array. It converts annual loss rates to daily rates after reading. |

## Review Notes

- Draft input-file overlay generated from static source facts; review and complete the remaining fields before promotion.
- The file is optional; if missing or set to "null", an empty `res_nut` array is allocated.
- Annual nutrient loss rates in the file are converted to daily rates by dividing by 365 in the reader.
- The source code comments mention the file as a lake water quality input file (.lwq), but the actual filename used is `nutrients.res` from `in_res%nut_res`.
