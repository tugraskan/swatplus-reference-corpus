---
kind: io
source_symbols:
- sep_read
title: '`septic.str`'
status: filled
source_hash: 9230439020fda755
version_label: SWAT+ 62.0.0
---

**Primary target:** `sep(:)` (array of `type septic_system`)  
**Read by:** [sym:sep_read]

## Bottom Line

The file `septic.str` configures the parameters of individual septic systems used in the SWAT+ model.

It is optional, as the reader checks for file existence and allocates an empty array if missing or set to "null".

The reader subroutine `sep_read` loads this file, reading each record into the array `sep` of type `septic_system`.

| Module | Role for this file |
| --- | --- |
| [sym:input_file_module] | provides the input file name string `in_str%septic_str` used to locate the `septic.str` file. |
| [sym:maximum_data_module] | provides the global data structure `db_mx` where `db_mx%septic` is set to the number of septic records read. |
| [sym:septic_data_module] | defines the derived type `septic_system` and the array `sep` where each record from the file is stored. |

## File Variables

The `septic.str` file contains tabular data records describing individual septic system parameters. Each record corresponds to one `septic_system` instance, with fields mapped directly to the components of the derived type `septic_system` declared in `septic_data_module`.

| Col | Header | Target | Type | Units | Meaning |
| --- | --- | --- | --- | --- | --- |
| 2 |  | `sep%name` | character(len=13) |  | name identifier of the septic system |
| 3 |  | `sep%typ` | integer | none | septic system type |
| 4 |  | `sep%yr` | integer |  | year the septic system became operational |
| 5 |  | `sep%opt` | integer | none | Septic system operation flag (1=active, 2=failing, 0=not operated) |
| 6 |  | `sep%cap` | real | none | number of permanent residents in the house |
| 7 |  | `sep%area` | real | m^2 | average area of drainfield of individual septic systems |
| 8 |  | `sep%tfail` | integer | days | time until failing systems get fixed |
| 9 |  | `sep%z` | real | mm | depth to the top of the biozone layer from the ground surface |
| 10 |  | `sep%thk` | real | mm | thickness of biozone layer |
| 11 |  | `sep%strm_dist` | real | km | distance to the stream from the septic system |
| 12 |  | `sep%density` | real |  | number of septic systems per square kilometer |
| 13 |  | `sep%bd` | real | kg/m^3 | density of biomass |
| 14 |  | `sep%bod_dc` | real | m^3/day | BOD decay rate coefficient |
| 15 |  | `sep%bod_conv` | real |  | conversion factor representing the proportion of mass |
| 16 |  | `sep%fc1` | real |  | linear coefficient for calculation of field capacity in the biozone; related to bacterial growth and mass BOD degraded in the STE |
| 17 |  | `sep%fc2` | real | none | exponential coefficient for calculation of field capacity in the biozone |
| 18 |  | `sep%fecal` | real | m^3/day | fecal coliform bacteria decay rate coefficient |
| 19 |  | `sep%plq` | real | none | conversion factor for plaque from total dissolved solids (TDS) |
| 20 |  | `sep%mrt` | real | none | mortality rate coefficient |
| 21 |  | `sep%rsp` | real | none | respiration rate coefficient |
| 22 |  | `sep%slg1` | real | none | slough-off calibration parameter |
| 23 |  | `sep%slg2` | real | none | slough-off calibration parameter |
| 24 |  | `sep%nitr` | real | none | nitrification rate coefficient |
| 25 |  | `sep%denitr` | real | none | denitrification rate coefficient |
| 26 |  | `sep%pdistrb` | real | (L/kg) | linear phosphorus sorption distribution coefficient |
| 27 |  | `sep%psorpmax` | real | (mg P/kg Soil) | maximum phosphorus sorption capacity |
| 28 |  | `sep%solpslp` | real |  | slope of the linear effluent soluble phosphorus equation |
| 29 |  | `sep%solpintc` | real |  | intercept of the linear effluent soluble phosphorus equation |

## Sample

```text
Example record format from `septic.str` (fields correspond to `septic_system` type, excluding leading record id):
"Septic01" 1 1995 1 4 150.0 30 500.0 100.0 0.5 10.0 300.0 0.1 0.05 0.8 0.2 0.01 0.5 0.02 0.01 0.03 0.1 0.2 0.05 0.04 0.03 0.001 10.0 0.5 0.1
```

## Read Pattern

```fortran
open (172,file=in_str%septic_str)
read (172,*,iostat=eof) titldum
read (172,*,iostat=eof) header
read (172,*,iostat=eof) titldum
rewind (172)
read (172,*,iostat=eof) titldum
read (172,*,iostat=eof) header
read (172,*,iostat=eof) sep(isep)
```

## I/O Operations

| Direction | Op | Unit | Statement |
| --- | --- | --- | --- |
| File setup | `open` | 172 | `open (172,file=in_str%septic_str)` |
| Input | `read` | 172 | `read (172,*,iostat=eof) titldum` |
| Input | `read` | 172 | `read (172,*,iostat=eof) header` |
| Input | `read` | 172 | `read (172,*,iostat=eof) titldum` |
| File control | `rewind` | 172 | `rewind (172)` |
| Input | `read` | 172 | `read (172,*,iostat=eof) titldum` |
| Input | `read` | 172 | `read (172,*,iostat=eof) header` |
| Input | `read` | 172 | `read(172,*,iostat=eof) sep(isep)` |
| File control | `close` | 172 | `close(172)` |

## Readers

| Procedure | Operations | Role |
| --- | --- | --- |
| [sym:sep_read] | open, read, rewind, close | Reads the `septic.str` input file if it exists and is not set to "null". It first counts the number of records to allocate the `sep` array, then reads each septic system record into `sep`. If the file does not exist or is set to "null", it allocates an empty `sep` array. It also sets `db_mx%septic` to the number of records read. |

## Review Notes

- Draft input-file overlay generated from static source facts; review and complete the remaining fields before promotion.
