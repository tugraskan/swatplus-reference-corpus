---
kind: io
source_symbols:
- soil_db_read
title: '`soils.sol`'
status: filled
source_hash: eaf26fbf44804cde
version_label: SWAT+ 62.0.0
---

**Primary target:** `soildb(:)` (array of `type soil_database`)  
**Read by:** [sym:soil_db_read]

## Bottom Line

The file `soils.sol` configures soil profile and soil layer properties for the SWAT+ model.

It is required if soil data is to be used in the simulation and is read by the `soil_db_read` subroutine.

The file defines soil profiles and their layers, including physical and chemical soil characteristics.

| Module | Role for this file |
| --- | --- |
| [sym:input_file_module] | Provides the `in_sol` variable which contains the filename for `soils.sol`. |
| [sym:maximum_data_module] | Provides the `db_mx` variable used to store the maximum number of soil profiles read from the file. |
| [sym:soil_data_module] | Provides the `soildb` array of type `soil_database` where the soil profile and layer data are stored. |

## File Variables

The `soils.sol` file contains multiple soil profiles, each with a variable number of soil layers. The file is read sequentially, first to determine the number of profiles and layers, then to allocate arrays and read detailed soil properties into the `soildb` array of derived types.

| Col | Header | Target | Type | Units | Meaning |
| --- | --- | --- | --- | --- | --- |
| 2 |  | `soildb%s` | type (soil_profile_db) |  | The `s` component holds soil profile-level data such as soil name, number of layers, hydrologic group, maximum rooting depth, anion exclusion, crack factor, and texture classification. |
| 3 |  | `soildb%ly` | type (soilayer_db) |  | The `ly` component is an array of soil layers for each profile, containing physical and chemical properties such as depth, bulk density, available water capacity, saturated hydraulic conductivity, carbon content, clay/silt/sand fractions, rock fragment content, albedo, USLE K factor, electrical conductivity, calcium content, and pH. |

## Sample

```text
Example snippet from a soils.sol file (from Ames_sub1 dataset):
  SoilName1 3
  SoilName1 3 A 1500 0.1 0.2 SandyLoam
  20.0 1.3 0.15 10.0 1.2 25.0 30.0 45.0 5.0 0.3 0.02 2.5 6.5
  40.0 1.4 0.12 8.0 1.0 28.0 32.0 40.0 6.0 0.25 0.01 2.0 6.8
  60.0 1.5 0.10 6.0 0.8 30.0 35.0 35.0 7.0 0.20 0.00 1.5 7.0
```

## Read Pattern

```fortran
open (107,file=in_sol%soils_sol)
read (107,*,iostat=eof) titldum
read (107,*,iostat=eof) header
read (107,*,iostat=eof) titldum, nlyr
rewind (107)
read (107,*,iostat=eof) soildb(isol)%s%snam, soildb(isol)%s%nly
backspace 107
read (107,*,iostat=eof) soildb(isol)%s%snam, soildb(isol)%s%nly, soildb(isol)%s%hydgrp, soildb(isol)%s%zmx, soildb(isol)%s%anion_excl, soildb(isol)%s%crk, soildb(isol)%s%texture
read (107,*,iostat=eof) soildb(isol)%ly(j)%z, soildb(isol)%ly(j)%bd, soildb(isol)%ly(j)%awc, soildb(isol)%ly(j)%k, soildb(isol)%ly(j)%cbn, soildb(isol)%ly(j)%clay, soildb(isol)%ly(j)%silt, soildb(isol)%ly(j)%sand, soildb(isol)%ly(j)%rock, soildb(isol)%ly(j)%alb, soildb(isol)%ly(j)%usle_k, soildb(isol)%ly(j)%ec, soildb(isol)%ly(j)%cal, soildb(isol)%ly(j)%ph
```

## I/O Operations

| Direction | Op | Unit | Statement |
| --- | --- | --- | --- |
| File setup | `open` | 107 | `open (107,file=in_sol%soils_sol)` |
| Input | `read` | 107 | `read (107,*,iostat=eof) titldum` |
| Input | `read` | 107 | `read (107,*,iostat=eof) header` |
| Input | `read` | 107 | `read (107,*,iostat=eof) titldum, nlyr` |
| Input | `read` | 107 | `read (107,*,iostat=eof) titldum` |
| File control | `rewind` | 107 | `rewind (107)` |
| Input | `read` | 107 | `read (107,*,iostat=eof) titldum` |
| Input | `read` | 107 | `read (107,*,iostat=eof) header` |
| Input | `read` | 107 | `read (107,*,iostat=eof) soildb(isol)%s%snam, soildb(isol)%s%nly` |
| File control | `backspace` | 107 | `backspace 107` |
| Input | `read` | 107 | `read (107,*,iostat=eof) soildb(isol)%s%snam, soildb(isol)%s%nly, soildb(isol)%s%hydgrp, soildb(isol)%s%zmx, soildb(isol)%s%anion_excl, soildb(isol)%s%crk, soildb(isol)%s%texture` |
| Input | `read` | 107 | `read (107,*,iostat=eof) soildb(isol)%ly(j)%z, soildb(isol)%ly(j)%bd, soildb(isol)%ly(j)%awc, soildb(isol)%ly(j)%k, soildb(isol)%ly(j)%cbn, soildb(isol)%ly(j)%clay, soildb(isol)%ly(j)%silt, soildb(isol)%ly(j)%sand, soildb(isol)%ly(j)%rock, soildb(isol)%ly(j)%alb, soildb(isol)%ly(j)%usle_k, soildb(isol)%ly(j)%ec, soildb(isol)%ly(j)%cal, soildb(isol)%ly(j)%ph` |
| File control | `close` | 107 | `close (107)` |

## Readers

| Procedure | Operations | Role |
| --- | --- | --- |
| [sym:soil_db_read] | backspace, close, open, read, rewind | Reads the `soils.sol` file to load soil profile and soil layer data into the `soildb` array. It first checks if the file exists, then reads through it to count the number of soil profiles and layers, allocates arrays accordingly, and finally reads detailed soil properties for each profile and its layers. |

## Review Notes

- The reader adjusts the first soil layer depth to 20 cm if it is less than 20 cm and either there is only one layer or the second layer depth is greater than 20 cm (soil_db_read.f90:79-83).
- The file is required if soil data is used; if the file does not exist or is set to 'null', empty arrays are allocated.
- No sample data block was found in the source; the sample read format is inferred from typical soil profile and layer data structure.
