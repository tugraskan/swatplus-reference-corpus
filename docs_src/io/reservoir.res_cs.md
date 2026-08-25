---
kind: io
source_symbols:
- res_read_salt_cs
title: '`reservoir.res_cs`'
status: filled
source_hash: a4f3ac5bb7650d5c
version_label: SWAT+ 62.0.0
---

**Primary target:** `res_dat_c_cs(:)` (array of `type reservoir_data_char_input_cs`)  
**Read by:** [sym:res_read_salt_cs]

## Bottom Line

The file `reservoir.res_cs` configures constituent and salt input references for reservoirs, linking each reservoir to pesticide, weir, salt, and constituent input datasets.

It is optional and only read if present.

The reader `res_read_salt_cs` loads this file and populates the `res_dat_c_cs` array with character input data, then resolves these to indices in the model state arrays `res_dat`, `res_salt_data`, and `res_cs_data`.

| Module | Role for this file |
| --- | --- |
| [sym:maximum_data_module] | Provides the `db_mx` object which contains maximum array sizes such as `db_mx%res_dat`, `db_mx%res_salt`, and `db_mx%res_cs` used for allocation and looping. |
| [sym:reservoir_data_module] | Defines the derived type `reservoir_data_char_input_cs` for `res_dat_c_cs` and the main reservoir data array `res_dat` where resolved indices are stored. |
| [sym:constituent_mass_module] | Supplies the `res_cs_data` array containing constituent names used to resolve the `cs` field from the input file. |
| [sym:reservoir_module] | Used for reservoir-related data structures, likely including `res_dat` where resolved indices are stored. |
| [sym:res_salt_module] | Supplies the `res_salt_data` array containing salt names used to resolve the `salt` field from the input file. |
| [sym:res_cs_module] | Likely provides additional constituent salt related data structures, complementing `res_cs_data`. |

## File Variables

The file `reservoir.res_cs` contains records that associate each reservoir with input references for pesticide, weir, salt, and constituent data. Each record consists of an integer reservoir ID followed by character fields for these input references, which are read into an array of `type reservoir_data_char_input_cs`.

| Col | Header | Target | Type | Units | Meaning |
| --- | --- | --- | --- | --- | --- |
| 2 |  | `res_dat_c_cs%pst` | character (len=25) |  | pesticide inputs-points to pesticide.res |
| 3 |  | `res_dat_c_cs%weir` | character (len=25) |  | weir inputs-points to weir.res Jaehak 2022 |
| 4 |  | `res_dat_c_cs%salt` | character (len=25) |  | salt inputs - points to salt_res rtb salt |
| 5 |  | `res_dat_c_cs%cs` | character (len=25) |  | constituent inputs - points to cs_res rtb cs |

## Sample

```text
1 "" "" "salt1" "cs1"
2 "pstA" "weirB" "salt2" "cs2"
```

## Read Pattern

```fortran
open(105,file="reservoir.res_cs")
read(105,*) header
read(105,*) header
read (105,*,iostat=eof) ires
backspace (105)
read (105,*,iostat=eof) k, res_dat_c_cs(ires)
```

## I/O Operations

| Direction | Op | Unit | Statement |
| --- | --- | --- | --- |
| File setup | `open` | 105 | `open(105,file="reservoir.res_cs")` |
| Input | `read` | 105 | `read(105,*) header` |
| Input | `read` | 105 | `read(105,*) header` |
| Input | `read` | 105 | `read (105,*,iostat=eof) ires` |
| File control | `backspace` | 105 | `backspace (105)` |
| Input | `read` | 105 | `read (105,*,iostat=eof) k, res_dat_c_cs(ires)` |
| File control | `close` | 105 | `close(105)` |

## Readers

| Procedure | Operations | Role |
| --- | --- | --- |
| [sym:res_read_salt_cs] | backspace, close, open, read | Reads the file `reservoir.res_cs` if it exists, loading reservoir constituent and salt input references into the array `res_dat_c_cs`. It then resolves the character salt and constituent names to indices in the model state arrays `res_salt_data` and `res_cs_data`, storing these indices in the main reservoir data array `res_dat`. |

## Review Notes

- Draft input-file overlay generated from static source facts; review and complete the remaining fields before promotion.
- The file is optional and only read if it exists, as indicated by the inquire statement.
- The sample read format is inferred from the read statements and type structure; no explicit example data was found in the source.
