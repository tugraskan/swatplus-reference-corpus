---
kind: io
source_symbols:
- recall_read_cs
title: '`cs_recall.rec`'
status: filled
source_hash: 27af90089d2a2725
version_label: SWAT+ 62.0.0
---

**Primary target:** `rec_cs(:)` (array of `type recall_cs_inputs`)  
**Read by:** [sym:recall_read_cs]

## Bottom Line

The file `cs_recall.rec` configures point source recall data for constituent mass inputs, specifying filenames and recall types (daily, monthly, annual) for each point source.

It is optional and read if the file exists or if the in-memory recall record is not null.

The reader subroutine `recall_read_cs` loads this file and reads associated point source data files referenced within it.

| Module | Role for this file |
| --- | --- |
| [sym:hydrograph_module] | Provides the `time` module variable `time%yrc` used to match simulation years when reading point source data files. |
| [sym:input_file_module] | No explicit variables or types from this module are directly referenced in `recall_read_cs`. |
| [sym:organic_mineral_mass_module] | No explicit variables or types from this module are directly referenced in `recall_read_cs`. |
| [sym:constituent_mass_module] | Defines the derived type `recall_cs_inputs` used for `rec_cs` array, and the `constituent_mass` type used in `rec_cs%hd_cs` allocation and initialization. |
| [sym:maximum_data_module] | No explicit variables or types from this module are directly referenced in `recall_read_cs`. |
| [sym:time_module] | Provides the `time` variable used to determine the current simulation year `time%yrc` for filtering recall data start year. |
| [sym:exco_module] | Referenced in a conditional block for type 4 recall files, possibly for crosswalk with exco file to get sequential number, but no explicit variables or calls are shown. |

## File Variables

Each record in `cs_recall.rec` corresponds to a point source recall input, stored in the array `rec_cs` of type `recall_cs_inputs`. The file lines contain an index followed by fields for name, recall type, filename, and later fields for start and end years and point source type, plus a nested constituent mass data structure allocated dynamically.

| Col | Header | Target | Type | Units | Meaning |
| --- | --- | --- | --- | --- | --- |
| 2 |  | `rec_cs%name` | character (len=16) |  | Name identifier for the point source recall input. |
| 3 |  | `rec_cs%typ` | integer |  | Recall type indicating temporal resolution: 1 = daily, 2 = monthly, 3 = annual. |
| 4 |  | `rec_cs%filename` | character(len=30) |  | Filename of the point source data file associated with this recall input. |
| 5 |  | `rec_cs%start_yr` | integer |  | Start year of the data coverage in the point source file. |
| 6 |  | `rec_cs%end_yr` | integer |  | End year of the data coverage in the point source file. |
| 7 |  | `rec_cs%pts_type` | integer |  | Point source type: 1 = originating within the watershed; 2 = originating outside the watershed. |
| 8 |  | `rec_cs%hd_cs` | type (constituent_mass) |  | Nested array of constituent mass data for each time step and year, dynamically allocated according to recall type and number of years. |

## Sample

```text
1 PointSource1 1 pts1.dat
2 PointSource2 2 pts2.dat
```

## Read Pattern

```fortran
open (107,file="cs_recall.rec")
read (107,*,iostat=eof) titldum
read (107,*,iostat=eof) header
read (107,*,iostat=eof) i
rewind (107)
backspace (107)
read (107,*,iostat = eof) k, rec_cs(i)%name, rec_cs(i)%typ, rec_cs(i)%filename
```

## I/O Operations

| Direction | Op | Unit | Statement |
| --- | --- | --- | --- |
| File setup | `open` | 107 | `open (107,file="cs_recall.rec")` |
| Input | `read` | 107 | `read (107,*,iostat=eof) titldum` |
| Input | `read` | 107 | `read (107,*,iostat=eof) header` |
| Input | `read` | 107 | `read (107,*,iostat=eof) i` |
| File control | `rewind` | 107 | `rewind (107)` |
| Input | `read` | 107 | `read (107,*,iostat=eof) titldum` |
| Input | `read` | 107 | `read (107,*,iostat=eof) header` |
| Input | `read` | 107 | `read (107,*,iostat=eof) i` |
| File control | `backspace` | 107 | `backspace (107)` |
| Input | `read` | 107 | `read (107,*,iostat = eof) k, rec_cs(i)%name, rec_cs(i)%typ, rec_cs(i)%filename` |
| File control | `close` | 107 | `close (107)` |

## Readers

| Procedure | Operations | Role |
| --- | --- | --- |
| [sym:recall_read_cs] | backspace, close, open, read, rewind | Reads the `cs_recall.rec` file to load point source recall input metadata and filenames, allocates arrays for constituent mass data, and reads associated point source data files to populate time series data for each recall input. |

## Review Notes

- Draft input-file overlay generated from static source facts; review and complete the remaining fields before promotion.
- The file `cs_recall.rec` is optional and read only if it exists or if the in-memory recall record is not null.
- The reader opens and reads the file twice: first to count the number of point source records, then to read their metadata and filenames.
- For each point source, the reader opens the associated data file and reads constituent mass data according to the recall type (daily, monthly, annual).
- The `hd_cs` field is dynamically allocated as a 2D array indexed by time step and year, with nested arrays of constituent mass values.
- The `pts_type` field is set based on the first line of the point source data file, distinguishing sources inside or outside the watershed.
- There is a conditional branch for recall type 4 that references the exco module, but no implementation details are provided.
- Sample record format is inferred but no official example data block is present in the source.
