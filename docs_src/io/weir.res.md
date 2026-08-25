---
kind: io
source_symbols:
- res_read_weir
title: '`weir.res`'
status: filled
source_hash: de048848734b6115
version_label: SWAT+ 62.0.0
---

**Primary target:** `res_weir(:)` (array of `type reservoir_weir_outflow`)  
**Read by:** [sym:res_read_weir]

## Bottom Line

The file `weir.res` configures reservoir weir outflow parameters used in the hydrologic modeling of reservoirs.

It is optional; if the file does not exist or is set to "null", no weir outflow data is loaded and the `res_weir` array is allocated empty.

The reader subroutine `res_read_weir` loads this file and populates the `res_weir` array with `reservoir_weir_outflow` records.

| Module | Role for this file |
| --- | --- |
| [sym:input_file_module] | Provides the `in_res` variable which contains the file path for `weir_res` used to open the input file. |
| [sym:maximum_data_module] | Provides the `db_mx` variable where the maximum number of weir records (`res_weir`) is stored in `db_mx%res_weir`. |
| [sym:reservoir_data_module] | Defines the derived type `reservoir_weir_outflow` and the allocatable array `res_weir` where the file data is stored. |

## File Variables

The `weir.res` file contains records of reservoir weir outflow parameters. Each record corresponds to one weir and is read into an element of the `res_weir` array of type `reservoir_weir_outflow`. The file format includes header lines followed by data lines matching the fields of the derived type.

| Col | Header | Target | Type | Units | Meaning |
| --- | --- | --- | --- | --- | --- |
| 2 |  | `res_weir%name` | character(len=25) |  | Name identifier of the weir |
| 3 |  | `res_weir%c` | real | none | weir discharge linear coefficient |
| 4 |  | `res_weir%k` | real | none | weir discharge exponential coefficient |
| 5 |  | `res_weir%w` | real | m | width |
| 6 |  | `res_weir%h` | real | m | height of weir above bottom of impoundment |

## Sample

```text
Example record lines from a typical `weir.res` file might look like:
  "Weir1" 1.84 2.6 2.5 0.0
  "Weir2" 2.0 2.5 3.0 0.1
```

## Read Pattern

```fortran
open (105,file=in_res%weir_res)
read (105,*,iostat=eof) titldum
read (105,*,iostat=eof) header
rewind (105)
backspace (105)
read (105,*,iostat=eof) res_weir(ires)
```

## I/O Operations

| Direction | Op | Unit | Statement |
| --- | --- | --- | --- |
| File setup | `open` | 105 | `open (105,file=in_res%weir_res)` |
| Input | `read` | 105 | `read (105,*,iostat=eof) titldum` |
| Input | `read` | 105 | `read (105,*,iostat=eof) header` |
| Input | `read` | 105 | `read (105,*,iostat=eof) titldum` |
| File control | `rewind` | 105 | `rewind (105)` |
| Input | `read` | 105 | `read (105,*,iostat=eof) titldum` |
| Input | `read` | 105 | `read (105,*,iostat=eof) header` |
| Input | `read` | 105 | `read (105,*,iostat=eof) titldum` |
| File control | `backspace` | 105 | `backspace (105)` |
| Input | `read` | 105 | `read (105,*,iostat=eof) res_weir(ires)` |
| File control | `close` | 105 | `close(105)` |

## Readers

| Procedure | Operations | Role |
| --- | --- | --- |
| [sym:res_read_weir] | backspace, close, open, read, rewind | Reads the `weir.res` input file, parses header lines, counts the number of weir records, allocates the `res_weir` array accordingly, and reads each weir record into the array of type `reservoir_weir_outflow`. |

## Review Notes

- The source code comments in `res_read_weir` mention lake water quality input file (.lwq), which appears unrelated to `weir.res`. This is likely a copy-paste comment error and should not be relied upon for `weir.res` meaning.
- The file `weir.res` is optional and if missing or set to "null", the `res_weir` array is allocated empty.
- The reader counts the number of records by reading lines after the header, then rewinds and reads the data into the typed array.
- No sample data lines were found in the source; the sample format is inferred from the type declaration and typical usage.
