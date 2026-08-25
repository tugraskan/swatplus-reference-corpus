---
kind: io
source_symbols:
- recall_read_salt
title: '`salt_recall.rec`'
status: filled
source_hash: ee6880d3aadd36a0
version_label: SWAT+ 62.0.0
---

**Primary target:** `rec_salt(:)` (array of `type recall_salt_inputs`)  
**Read by:** [sym:recall_read_salt]

## Bottom Line

The file `salt_recall.rec` configures point source salt input data for the SWAT+ model, specifying salt input time series by name, type (daily, monthly, annual), and filename.

It is optional and only read if present.

The reader subroutine `recall_read_salt` loads this file and populates the `rec_salt` array with metadata and allocates associated salt balance arrays.

| Module | Role for this file |
| --- | --- |
| [sym:hydrograph_module] | Provides `cs_db` which contains `num_salts` used to allocate salt arrays. |
| [sym:input_file_module] | No direct variables used in `recall_read_salt` from this module are evident in the source. |
| [sym:organic_mineral_mass_module] | No direct variables used in `recall_read_salt` from this module are evident in the source. |
| [sym:constituent_mass_module] | Defines the derived type `recall_salt_inputs` used for `rec_salt` and the type `constituent_mass` used for `hd_salt` salt concentration arrays. |
| [sym:maximum_data_module] | No direct variables used in `recall_read_salt` from this module are evident in the source. |
| [sym:time_module] | Provides the current simulation year `time%yrc` used to find the start year in the salt input files. |
| [sym:exco_module] | Referenced in a conditional for type 4 salt recall files (not implemented in this source), presumably for crosswalk with exco file. |

## File Variables

Each record in `salt_recall.rec` corresponds to a point source salt input configuration, read into an element of the `rec_salt` array of type `recall_salt_inputs`. The file columns include the salt input name, recall type (daily, monthly, annual), the filename of the detailed salt input data, and metadata such as start and end years and point source type.

| Col | Header | Target | Type | Units | Meaning |
| --- | --- | --- | --- | --- | --- |
| 2 |  | `rec_salt%name` | character (len=16) |  | Name identifier for the salt input point source |
| 3 |  | `rec_salt%typ` | integer |  | Recall type indicating temporal resolution: 1=daily, 2=monthly, 3=annual |
| 4 |  | `rec_salt%filename` | character(len=30) |  | Filename of the detailed salt input data file for this point source |
| 5 |  | `rec_salt%start_yr` | integer |  | Start year of the salt input data time series |
| 6 |  | `rec_salt%end_yr` | integer |  | End year of the salt input data time series |
| 7 |  | `rec_salt%pts_type` | integer |  | Point source type: 1 = originating within watershed, 2 = from outside watershed |
| 8 |  | `rec_salt%hd_salt` | type (constituent_mass) |  | Array of salt constituent mass data indexed by time steps and years, dynamically allocated according to recall type and number of years |

## Sample

```text
1 SaltInput1 1 saltinput1.dat
2 SaltInput2 2 saltinput2.dat
3 SaltInput3 3 saltinput3.dat
```

## Read Pattern

```fortran
open (107,file="salt_recall.rec")
read (107,*,iostat=eof) titldum
read (107,*,iostat=eof) header
read (107,*,iostat=eof) i
rewind (107)
backspace (107)
read (107,*,iostat = eof) k, rec_salt(i)%name, rec_salt(i)%typ, rec_salt(i)%filename
```

## I/O Operations

| Direction | Op | Unit | Statement |
| --- | --- | --- | --- |
| File setup | `open` | 107 | `open (107,file="salt_recall.rec")` |
| Input | `read` | 107 | `read (107,*,iostat=eof) titldum` |
| Input | `read` | 107 | `read (107,*,iostat=eof) header` |
| Input | `read` | 107 | `read (107,*,iostat=eof) i` |
| File control | `rewind` | 107 | `rewind (107)` |
| Input | `read` | 107 | `read (107,*,iostat=eof) titldum` |
| Input | `read` | 107 | `read (107,*,iostat=eof) header` |
| Input | `read` | 107 | `read (107,*,iostat=eof) i` |
| File control | `backspace` | 107 | `backspace (107)` |
| Input | `read` | 107 | `read (107,*,iostat = eof) k, rec_salt(i)%name, rec_salt(i)%typ, rec_salt(i)%filename` |
| File control | `close` | 107 | `close (107)` |

## Readers

| Procedure | Operations | Role |
| --- | --- | --- |
| [sym:recall_read_salt] | backspace, close, open, read, rewind | Reads the `salt_recall.rec` file to load metadata for salt point source inputs into the `rec_salt` array, allocates salt balance arrays for daily, monthly, and annual time series, and reads detailed salt constituent data from the referenced salt input files. |

## Review Notes

- The file `salt_recall.rec` is optional and only processed if it exists.
- The reader dynamically allocates arrays for salt constituent data based on the number of salts in `cs_db` and the recall type (daily, monthly, annual).
- Type 4 recall salt files are mentioned but not implemented in this source.
- Sample read format is inferred from the read statements and typical usage but no explicit example block is present in the source.
