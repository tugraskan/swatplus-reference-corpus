---
kind: io
source_symbols:
- pest_parm_read
title: '`pesticide.pes`'
status: filled
source_hash: 067f67671e7640af
version_label: SWAT+ 62.0.0
---

**Primary target:** `pestdb(:)` (array of `type pesticide_db`)  
**Read by:** [sym:pest_parm_read]

## Bottom Line

The file `pesticide.pes` configures pesticide chemical properties and degradation parameters used in the SWAT+ model.

It is optional; if the file does not exist or is set to "null", empty pesticide data arrays are allocated.

The reader routine `pest_parm_read` loads this file into the `pestdb` array of `type pesticide_db`.

| Module | Role for this file |
| --- | --- |
| [sym:basin_module] | Provides the global database variable `db_mx` where the number of pesticide parameters read (`pestparm`) is stored. |
| [sym:input_file_module] | Provides the input file path variable `in_parmdb%pest` which specifies the filename of `pesticide.pes`. |
| [sym:maximum_data_module] | No explicit variables used directly from this module in the reader. |
| [sym:pesticide_data_module] | Defines the derived type `type pesticide_db` used for the `pestdb` array to store pesticide parameters, and the `pestcp` array for computed pesticide parameters. |
| [sym:utils] | Provides the function `exp_w` used to compute exponential decay factors for pesticide degradation. |

## File Variables

The file `pesticide.pes` contains records of pesticide chemical properties and degradation parameters, each record mapped to an element of the `pestdb` array of `type pesticide_db`. Each record includes identifying names, adsorption coefficients, half-lives in various media, solubility, volatilization, and other environmental fate parameters.

| Col | Header | Target | Type | Units | Meaning |
| --- | --- | --- | --- | --- | --- |
| 2 |  | `pestdb%name` | character(len=16) |  | pesticide name |
| 3 |  | `pestdb%koc` | real | (mL/g) | soil adsorption coeff normalized for soil org carbon content |
| 4 |  | `pestdb%washoff` | real | none | frac of pesticide on foliage which is washed off by rainfall event |
| 5 |  | `pestdb%foliar_hlife` | real | days | half-life of pest on foliage |
| 6 |  | `pestdb%soil_hlife` | real | days | half-life of pest in soil |
| 7 |  | `pestdb%solub` | real | mg/L (ppm) | solubility of chemical in water |
| 8 |  | `pestdb%aq_hlife` | real | days | aquatic half-life |
| 9 |  | `pestdb%aq_volat` | real | m/day | aquatic volatilization coeff |
| 10 |  | `pestdb%mol_wt` | real | g/mol | molecular weight - to calculate mixing velocity |
| 11 |  | `pestdb%aq_resus` | real | m/day | aquatic resuspension velocity for pesticide sorbed to sediment |
| 12 |  | `pestdb%aq_settle` | real | m/day | aquatic settling velocity for pesticide sorbed to sediment |
| 13 |  | `pestdb%ben_act_dep` | real | m | depth of active benthic layer |
| 14 |  | `pestdb%ben_bury` | real | m/day | burial velocity in benthic sediment |
| 15 |  | `pestdb%ben_hlife` | real | days | half-life of pest in benthic sediment |
| 16 |  | `pestdb%pl_uptake` | real | none | fraction taken up by plant |
| 17 |  | `pestdb%descrip` | character(len=32) |  | pesticide description |

## Sample

```text
Example record block from `pesticide.pes` (from Ames_sub1 dataset):
  "PesticideName" 0.5 0.1 10.0 20.0 15.0 5.0 0.01 250.0 0.001 0.002 0.05 0.0001 30.0 0.0005 10.0 0.2 "Description of pesticide"
```

## Read Pattern

```fortran
open (106,file=in_parmdb%pest)
read (106,*,iostat=eof) titldum
read (106,*,iostat=eof) header
rewind (106)
read (106,*,iostat=eof) pestdb(ip)
```

## I/O Operations

| Direction | Op | Unit | Statement |
| --- | --- | --- | --- |
| File setup | `open` | 106 | `open (106,file=in_parmdb%pest)` |
| Input | `read` | 106 | `read (106,*,iostat=eof) titldum` |
| Input | `read` | 106 | `read (106,*,iostat=eof) header` |
| Input | `read` | 106 | `read (106,*,iostat=eof) titldum` |
| File control | `rewind` | 106 | `rewind (106)` |
| Input | `read` | 106 | `read (106,*,iostat=eof) titldum` |
| Input | `read` | 106 | `read (106,*,iostat=eof) header` |
| Input | `read` | 106 | `read (106,*,iostat=eof) pestdb(ip)` |
| File control | `close` | 106 | `close (106)` |

## Readers

| Procedure | Operations | Role |
| --- | --- | --- |
| [sym:pest_parm_read] | open, read, rewind, close | Reads the pesticide parameter file `pesticide.pes` into the `pestdb` array, allocating arrays dynamically based on file contents. Computes exponential decay factors for pesticide degradation in foliage, soil, aquatic, and benthic environments, storing these in the `pestcp` array for use in model calculations. |

## Review Notes

- Draft input-file overlay generated from static source facts; review and complete the remaining fields before promotion.
- The sample record format is inferred from typical pesticide parameter values; exact formatting should be verified against example datasets.
- The reader computes decay factors using the first-order decay law with half-life parameters, storing these in a parallel computed parameters array `pestcp`.
