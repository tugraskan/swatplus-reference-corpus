---
kind: io
source_symbols:
- cs_hru_read
title: '`cs_hru.ini`'
status: filled
source_hash: 6864457e685476cd
version_label: SWAT+ 62.0.0
---

**Primary target:** `cs_soil_ini(:)` (array of `type cs_soil_init_concentrations`)  
**Read by:** [sym:cs_hru_read]

## Bottom Line

The file `cs_hru.ini` configures initial concentrations of chemical or biological constituents in soil and on plants at the start of a simulation.

It is optional but if present, it is read by the `cs_hru_read` subroutine.

The file's data is stored in the array `cs_soil_ini` of derived type `cs_soil_init_concentrations`.

| Module | Role for this file |
| --- | --- |
| [sym:constituent_mass_module] | Provides the derived type `cs_soil_init_concentrations` and the array `cs_soil_ini` where the initial constituent concentrations are stored. |
| [sym:input_file_module] | Used for general input file handling, including variables like `db_mx` and `cs_db` that track database sizes and counts relevant to constituent data allocation. |
| [sym:maximum_data_module] | Used to allocate arrays and manage maximum data sizes for constituents in soil and plants within `cs_soil_ini`. |

## File Variables

The file consists of records each describing a constituent's initial concentration in soil and on plants. Each record is read into an element of the `cs_soil_ini` array, with fields for constituent name, soil concentration, and plant concentration.

| Col | Header | Target | Type | Units | Meaning |
| --- | --- | --- | --- | --- | --- |
| 2 |  | `cs_soil_ini%name` | character (len=16) |  | name of the constituent - points to constituent database |
| 3 |  | `cs_soil_ini%soil` | real | ppm | amount of constituent in soil at start of simulation |
| 4 |  | `cs_soil_ini%plt` | real | ppm or #cfu/m^2 | amount of constituent on plant at start of simulation |

## Sample

```text
Example record block from `cs_hru.ini` (format: name, soil concentration, plant concentration):
NITRATE          15.0  0.0
PHOSPHATE        10.0  0.0
BACTERIA         0.0   1000.0
```

## Read Pattern

```fortran
open (107,file="cs_hru.ini")
read (107,*,iostat=eof) titldum
read (107,*,iostat=eof) header
read (107,*,iostat=eof) header
read (107,*,iostat=eof) header
read (107,*,iostat=eof) header
read (107,*,iostat=eof) titldum
read (107,*,iostat=eof) titldum
read (107,*,iostat=eof) titldum
rewind (107)
read (107,*,iostat=eof) titldum
read (107,*,iostat=eof) header
read (107,*,iostat=eof) header
read (107,*,iostat=eof) header
read (107,*,iostat=eof) header
read (107,*,iostat=eof) cs_soil_ini(ics)%name
read (107,*,iostat=eof) cs_soil_ini(ics)%soil
read (107,*,iostat=eof) cs_soil_ini(ics)%plt
```

## I/O Operations

| Direction | Op | Unit | Statement |
| --- | --- | --- | --- |
| File setup | `open` | 107 | `open (107,file="cs_hru.ini")` |
| Input | `read` | 107 | `read (107,*,iostat=eof) titldum` |
| Input | `read` | 107 | `read (107,*,iostat=eof) header` |
| Input | `read` | 107 | `read (107,*,iostat=eof) header` |
| Input | `read` | 107 | `read (107,*,iostat=eof) header` |
| Input | `read` | 107 | `read (107,*,iostat=eof) header` |
| Input | `read` | 107 | `read (107,*,iostat=eof) titldum` |
| Input | `read` | 107 | `read (107,*,iostat=eof) titldum` |
| Input | `read` | 107 | `read (107,*,iostat=eof) titldum` |
| File control | `rewind` | 107 | `rewind (107)` |
| Input | `read` | 107 | `read (107,*,iostat=eof) titldum` |
| Input | `read` | 107 | `read (107,*,iostat=eof) header` |
| Input | `read` | 107 | `read (107,*,iostat=eof) header` |
| Input | `read` | 107 | `read (107,*,iostat=eof) header` |
| Input | `read` | 107 | `read (107,*,iostat=eof) header` |
| Input | `read` | 107 | `read (107,*,iostat=eof) cs_soil_ini(ics)%name` |
| Input | `read` | 107 | `read (107,*,iostat=eof) cs_soil_ini(ics)%soil` |
| Input | `read` | 107 | `read (107,*,iostat=eof) cs_soil_ini(ics)%plt` |
| File control | `close` | 107 | `close (107)` |

## Readers

| Procedure | Operations | Role |
| --- | --- | --- |
| [sym:cs_hru_read] | open, read, rewind, close | Reads the `cs_hru.ini` file if it exists, counts the number of constituent records, allocates the `cs_soil_ini` array accordingly, and loads initial constituent concentrations for soil and plants into `cs_soil_ini`. |

## Review Notes

- The file `cs_hru.ini` is optional and only read if it exists.
- The reader first scans the file to count records, then allocates arrays accordingly before reading data.
- The file format includes header lines that are skipped before reading data records.
- Units for soil concentrations are ppm; plant concentrations may be ppm or colony forming units per square meter (#cfu/m^2).
- No sample data was found in the source; the example is inferred from typical constituent names and units.
