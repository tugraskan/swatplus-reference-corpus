---
kind: io
source_symbols:
- res_read_sed
title: '`sediment.res`'
status: filled
source_hash: 9ece929d578c623c
version_label: SWAT+ 62.0.0
---

**Primary target:** `res_sed(:)` (array of `type reservoir_sed_data`)  
**Read by:** [sym:res_read_sed]

## Bottom Line

The file `sediment.res` provides sediment-related parameters for reservoirs, configuring initial sediment properties such as concentration, particle size, organic carbon content, bulk density, and settling characteristics.

It is optional; if the file does not exist or is set to "null", no sediment data is allocated.

The reader subroutine `res_read_sed` loads this file and populates the `res_sed` array of `type reservoir_sed_data`.

| Module | Role for this file |
| --- | --- |
| [sym:input_file_module] | Provides the `in_res` variable which contains the filename `sed_res` for the sediment input file. |
| [sym:maximum_data_module] | Provides the `db_mx` variable where `db_mx%res_sed` stores the number of sediment records read. |
| [sym:reservoir_data_module] | Defines the `type reservoir_sed_data` and the `res_sed` array that stores the sediment data read from the file. |

## File Variables

The `sediment.res` file consists of multiple records each describing sediment properties for a reservoir. Each record is read into an element of the `res_sed` array of derived type `reservoir_sed_data`. The file format includes a leading record identifier followed by columns matching the fields of `reservoir_sed_data`.

| Col | Header | Target | Type | Units | Meaning |
| --- | --- | --- | --- | --- | --- |
| 2 |  | `res_sed%name` | character(len=25) |  | Reservoir name or sediment record identifier |
| 3 |  | `res_sed%nsed` | real | kg/L | Normal amount of sediment in the reservoir (read in as mg/L and converted to kg/L) |
| 4 |  | `res_sed%d50` | real | um | Median particle size of suspended and benthic sediment |
| 5 |  | `res_sed%carbon` | real | % | Organic carbon content in suspended and benthic sediment |
| 6 |  | `res_sed%bd` | real | t/m^3 | Bulk density of benthic sediment |
| 7 |  | `res_sed%sed_stlr` | real | none | Sediment settling rate |
| 8 |  | `res_sed%velsetlr` | real | m/d | Sediment settling velocity |

## Sample

```text
Example record format (fields separated by spaces or tabs):
RecordID Name Nsed D50 Carbon Bd Sed_Stlr VelSetlr
1 Reservoir1 0.005 50.0 2.5 1.3 0.01 0.1
```

## Read Pattern

```fortran
open (105,file=in_res%sed_res)
read (105,*,iostat=eof) titldum
read (105,*,iostat=eof) header
rewind (105)
backspace (105)
read (105,*,iostat=eof) res_sed(ires)
```

## I/O Operations

| Direction | Op | Unit | Statement |
| --- | --- | --- | --- |
| File setup | `open` | 105 | `open (105,file=in_res%sed_res)` |
| Input | `read` | 105 | `read (105,*,iostat=eof) titldum` |
| Input | `read` | 105 | `read (105,*,iostat=eof) header` |
| Input | `read` | 105 | `read (105,*,iostat=eof) titldum` |
| File control | `rewind` | 105 | `rewind (105)` |
| Input | `read` | 105 | `read (105,*,iostat=eof) titldum` |
| Input | `read` | 105 | `read (105,*,iostat=eof) header` |
| Input | `read` | 105 | `read (105,*,iostat=eof) titldum` |
| File control | `backspace` | 105 | `backspace (105)` |
| Input | `read` | 105 | `read (105,*,iostat=eof) res_sed(ires)` |
| File control | `close` | 105 | `close(105)` |

## Readers

| Procedure | Operations | Role |
| --- | --- | --- |
| [sym:res_read_sed] | backspace, close, open, read, rewind | Reads the sediment properties file `sediment.res` if it exists and is not set to "null". It counts the number of sediment records, allocates the `res_sed` array accordingly, then reads each sediment record into `res_sed`. If the file is missing or set to "null", it allocates an empty `res_sed` array. |

## Review Notes

- Draft input-file overlay generated from static source facts; review and complete the remaining fields before promotion.
- The subroutine `res_read_sed` uses a loop to count records by reading a dummy variable repeatedly before allocating the array and reading actual records.
- The file is optional; if missing or set to "null", an empty array is allocated.
- The file format includes header lines and record identifiers before the actual sediment data records.
- No sample data records were found in the source; the sample read format is inferred from the type fields.
