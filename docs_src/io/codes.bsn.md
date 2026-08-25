---
kind: io
source_symbols:
- basin_read_cc
title: '`codes.bsn`'
status: filled
source_hash: cac4daf4ba7a91fa
version_label: SWAT+ 62.0.0
---

**Primary target:** `bsn_cc(:)` (array of `type basin_control_codes`)  
**Read by:** [sym:basin_read_cc]

## Bottom Line

The `codes.bsn` input file configures basin-level control parameters for the SWAT+ model, including potential evapotranspiration methods, flow routing, carbon modeling, and nutrient stress options.

This file is optional and is read if it exists or if the filename is not "null".

The primary reader that loads this file is the `basin_read_cc` subroutine.

| Module | Role for this file |
| --- | --- |
| [sym:input_file_module] | Provides the `in_basin` variable which contains the filename `codes_bas` pointing to the `codes.bsn` file to be read. |
| [sym:basin_module] | Defines the `type basin_control_codes` and the variable `bsn_cc` where the file data is stored. |

## File Variables

The `codes.bsn` file schema maps directly to the `type basin_control_codes` in `basin_module`. Each record corresponds to one `bsn_cc` instance, with fields representing various basin control codes and filenames used by the model.

| Col | Header | Target | Type | Units | Meaning |
| --- | --- | --- | --- | --- | --- |
| 2 |  | `bsn_cc%petfile` | character(len=16) |  | character(len=16) :: update !! pointer to basin updates in schedule.upd potential et filename |
| 3 |  | `bsn_cc%wwqfile` | character(len=16) |  | watershed stream water quality filename |
| 4 |  | `bsn_cc%pet` | integer |  | potential ET method code |
| 5 |  | `bsn_cc%nam1` | integer |  | 0 = Priestley-Taylor 1 = Penman-Monteith 2 = Hargreaves method not used |
| 6 |  | `bsn_cc%crk` | integer |  | crack flow code |
| 7 |  | `bsn_cc%swift_out` | integer |  | 1 = compute flow in cracks write to SWIFT input file |
| 8 |  | `bsn_cc%sed_det` | integer |  | 0 = do not write 1 = write to swift_hru.inp peak rate method |
| 9 |  | `bsn_cc%rte` | integer |  | 0 = NRCS dimensionless hydrograph with PRF 1 = half hour rainfall intensity method water routing method |
| 10 |  | `bsn_cc%deg` | integer |  | 0 variable storage method 1 Muskingum method not used |
| 11 |  | `bsn_cc%wq` | integer |  | not used |
| 12 |  | `bsn_cc%nostress` | integer |  | redefined to the sequence number -- changed to no nutrient stress |
| 13 |  | `bsn_cc%cn` | integer |  | 0 = all stresses applied 1 = turn off all plant stress 2 = turn off nutrient plant stress only not used |
| 14 |  | `bsn_cc%cfac` | integer |  | not used |
| 15 |  | `bsn_cc%cswat` | integer |  | carbon code: 0 = off (static), 1 = C-FARM (reserved, |
| 16 |  | `bsn_cc%lapse` | integer |  | not implemented), 2 = dynamic CENTURY/SWAT-C model. numbering aligned with legacy SWAT as directed by Srinivasan. = 0 Static soil carbon (old mineralization routines) = 1 C-FARM one carbon pool model = 2 Century model precip and temperature lapse rate control |
| 17 |  | `bsn_cc%uhyd` | integer |  | 0 = do not adjust for elevation 1 = adjust for elevation Unit hydrograph method: |
| 18 |  | `bsn_cc%sed_ch` | integer |  | 0 = triangular UH 1 = gamma function UH not used |
| 19 |  | `bsn_cc%tdrn` | integer |  | tile drainage eq code |
| 20 |  | `bsn_cc%wtdn` | integer |  | 0 = tile flow using drawdown days equation 1 = tile flow using drainmod equations shallow water table depth algorithms code |
| 21 |  | `bsn_cc%sol_p_model` | integer |  | 0 = depth using orig water table depth routine - fill to upper limit 1 = depth using drainmod water table depth routine 0 = original soil P model in SWAT documentation |
| 22 |  | `bsn_cc%gampt` | integer |  | 1 = new soil P model in Vadas and White (2010) 0 = curve number; 1 = Green and Ampt |
| 23 |  | `bsn_cc%atmo` | character(len=1) |  | not used |
| 24 |  | `bsn_cc%smax` | integer |  | not used |
| 25 |  | `bsn_cc%qual2e` | integer |  | 0 = instream nutrient routing using QUAL2E |
| 26 |  | `bsn_cc%gwflow` | integer |  | 1 = instream nutrient routing using QUAL2E - with simplified nutrient transformations 0 = gwflow module not active; 1 = gwflow module active |
| 27 |  | `bsn_cc%idc_till` | integer |  | 1 = Use dssat tillage method to use if cswat = 2 |

## Sample

```text
Example record block from codes.bsn (from Ames_sub1 dataset):
  "Basin Control Parameters Title Line"
  "Header information line"
  '         pet.cli' '' 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 0 0 0 0 0 0 'a' 0 0 0 0 3
```

## Read Pattern

```fortran
open (107,file=in_basin%codes_bas)
read (107,*,iostat=eof) titldum
read (107,*,iostat=eof) header
read (107,*,iostat=eof) bsn_cc
```

## I/O Operations

| Direction | Op | Unit | Statement |
| --- | --- | --- | --- |
| File setup | `open` | 107 | `open (107,file=in_basin%codes_bas)` |
| Input | `read` | 107 | `read (107,*,iostat=eof) titldum` |
| Input | `read` | 107 | `read (107,*,iostat=eof) header` |
| Input | `read` | 107 | `read (107,*,iostat=eof) bsn_cc` |
| File control | `close` | 107 | `close(107)` |

## Readers

| Procedure | Operations | Role |
| --- | --- | --- |
| [sym:basin_read_cc] | close, open, read | Reads the `codes.bsn` file if it exists or if the filename is not "null", loading basin control parameters into the `bsn_cc` variable. It reads a title line, a header line, and then the main basin control record. If the potential evapotranspiration method code (`bsn_cc%pet`) equals 3, it opens and reads additional PET data from the 'pet.cli' file. |

## Review Notes

- Draft input-file overlay generated from static source facts; review and complete the remaining fields before promotion.
- The `basin_read_cc` subroutine conditionally reads an additional PET file 'pet.cli' if `bsn_cc%pet` equals 3, indicating specialized PET input handling.
- The file is optional as it is read only if it exists or the filename is not "null".
- The sample read format is inferred from typical usage and the source code structure; no explicit example record was found in the source.
