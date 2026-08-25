---
kind: io
source_symbols:
- wet_read_salt_cs
title: '`wetland.wet_cs`'
status: filled
source_hash: c43461398d15e551
version_label: SWAT+ 62.0.0
---

**Primary target:** `wet_dat_c_cs(:)` (array of `type reservoir_data_char_input_cs`)  
**Read by:** [sym:wet_read_salt_cs]

## Bottom Line

The file `wetland.wet_cs` is an optional input file that configures pesticide, weir, salt, and constituent input references for wetland reservoirs in the model. It is read by the `wet_read_salt_cs` subroutine, which populates the array `wet_dat_c_cs` with these character input references and updates corresponding indices in the main wetland data array `wet_dat`.

| Module | Role for this file |
| --- | --- |
| [sym:maximum_data_module] | provides the global dimension limits such as `db_mx%wet_dat`, `db_mx%res_salt`, and `db_mx%res_cs` used to allocate and loop over arrays. |
| [sym:reservoir_data_module] | provides the derived type `reservoir_data_char_input_cs` for `wet_dat_c_cs` and the main wetland data array `wet_dat` where resolved indices are stored. |
| [sym:constituent_mass_module] | provides the constituent salt data array `res_cs_data` used to resolve constituent input names to indices. |
| [sym:reservoir_module] | not directly referenced in this routine but likely related to reservoir data structures. |
| [sym:res_salt_module] | provides the salt data array `res_salt_data` used to resolve salt input names to indices. |
| [sym:res_cs_module] | provides the constituent salt data array `res_cs_data` used to resolve constituent input names to indices. |

## File Variables

Each record in `wetland.wet_cs` corresponds to a wetland reservoir input configuration, identified by an integer ID followed by four character fields representing pesticide, weir, salt, and constituent input references. These fields map to the derived type `reservoir_data_char_input_cs` and are stored in the array `wet_dat_c_cs`.

| Col | Header | Target | Type | Units | Meaning |
| --- | --- | --- | --- | --- | --- |
| 2 |  | `wet_dat_c_cs%pst` | character (len=25) |  | pesticide inputs-points to pesticide.res |
| 3 |  | `wet_dat_c_cs%weir` | character (len=25) |  | weir inputs-points to weir.res Jaehak 2022 |
| 4 |  | `wet_dat_c_cs%salt` | character (len=25) |  | salt inputs - points to salt_res rtb salt |
| 5 |  | `wet_dat_c_cs%cs` | character (len=25) |  | constituent inputs - points to cs_res rtb cs |

## Sample

```text
1 "pesticide.res" "weir.res" "salt_res" "cs_res"
```

## Read Pattern

```fortran
open(105,file="wetland.wet_cs")
read(105,*) header
read(105,*) header
do iwet = 1, db_mx%wet_dat
  read (105,*,iostat=eof) i
  if (eof < 0) exit
  backspace (105)
  read (105,*,iostat=eof) k, wet_dat_c_cs(iwet)
  if (eof < 0) exit
enddo
close(105)
```

## I/O Operations

| Direction | Op | Unit | Statement |
| --- | --- | --- | --- |
| File setup | `open` | 105 | `open(105,file="wetland.wet_cs")` |
| Input | `read` | 105 | `read(105,*) header` |
| Input | `read` | 105 | `read(105,*) header` |
| Input | `read` | 105 | `read (105,*,iostat=eof) i` |
| File control | `backspace` | 105 | `backspace (105)` |
| Input | `read` | 105 | `read (105,*,iostat=eof) k, wet_dat_c_cs(iwet)` |
| File control | `close` | 105 | `close(105)` |

## Readers

| Procedure | Operations | Role |
| --- | --- | --- |
| [sym:wet_read_salt_cs] | open, read, backspace, close | Reads the optional input file `wetland.wet_cs` to populate the array `wet_dat_c_cs` with character input references for pesticide, weir, salt, and constituent inputs for wetland reservoirs. It also resolves the salt and constituent names to indices in the main wetland data array `wet_dat` by matching names against `res_salt_data` and `res_cs_data`. |

## Review Notes

- The file `wetland.wet_cs` is optional and only read if it exists.
- The reader performs two header reads, presumably to skip header lines.
- The reader allocates `wet_dat_c_cs` to the maximum wetland data size `db_mx%wet_dat` before reading records.
- Each record starts with an integer ID followed by the character fields.
- The reader resolves salt and constituent names to indices by linear search in `res_salt_data` and `res_cs_data` arrays.
- No explicit error handling for missing matches is shown.
- The sample read format is inferred from the code and type declarations; no example data was found in the source.
