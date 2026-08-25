---
kind: io
source_symbols:
- basin_read_prm
title: '`parameters.bsn`'
status: filled
source_hash: 04ffee14e8c261b1
version_label: SWAT+ 62.0.0
---

**Primary target:** `bsn_prm(:)` (array of `type basin_parms`)  
**Read by:** [sym:basin_read_prm]

## Bottom Line

The `parameters.bsn` file contains basin-level parameters that configure hydrologic and biogeochemical processes at the subbasin scale in SWAT+.

It is read by the `basin_read_prm` subroutine, which loads these parameters into the `bsn_prm` array of `type basin_parms`.

The file is optional; the reader first checks if the file exists or is not set to "null" before attempting to read.

These parameters influence processes such as evapotranspiration thresholds, runoff lag times, nutrient cycling, erosion, and channel routing.

| Module | Role for this file |
| --- | --- |
| [sym:input_file_module] | Provides the `in_basin` variable which contains the filename `parms_bas` used to locate the `parameters.bsn` file. |
| [sym:basin_module] | Defines the `type basin_parms` used to store the basin parameters read from the file into the `bsn_prm` array. |

## File Variables

The file schema corresponds to the fields of `type basin_parms` defined in `basin_module`. Each record in the file maps directly to one element of the `bsn_prm` array, with fields representing various hydrologic and biogeochemical parameters for a subbasin.

| Col | Header | Target | Type | Units | Meaning |
| --- | --- | --- | --- | --- | --- |
| 2 |  | `bsn_prm%evlai` | real | none | leaf area index at which no evap occurs |
| 3 |  | `bsn_prm%ffcb` | real | none | initial soil water cont expressed as a fraction of fc |
| 4 |  | `bsn_prm%surlag` | real | days | surface runoff lag time (days) |
| 5 |  | `bsn_prm%adj_pkr` | real | none | peak rate adjustment factor in the subbasin |
| 6 |  | `bsn_prm%prf` | real |  | peak rate factor for peak rate equation |
| 7 |  | `bsn_prm%spcon` | real |  | not used |
| 8 |  | `bsn_prm%spexp` | real |  | not used |
| 9 |  | `bsn_prm%cmn` | real |  | rate factor for mineralization on active org N - 0.0003 -> 0.003 |
| 10 |  | `bsn_prm%n_updis` | real |  | nitrogen uptake dist parm |
| 11 |  | `bsn_prm%p_updis` | real |  | phosphorus uptake dist parm |
| 12 |  | `bsn_prm%nperco` | real |  | nitrate perc coeff (0-1) |
| 13 |  | `bsn_prm%pperco` | real |  | 0 = conc of nitrate in surface runoff is zero 1 = perc has same conc of nitrate as surf runoff phos perc coeff (0-1) |
| 14 |  | `bsn_prm%phoskd` | real |  | 0 = conc of sol P in surf runoff is zero 1 = percolate has some conc of sol P as surf runoff phos soil partitioning coef |
| 15 |  | `bsn_prm%psp` | real |  | phos availability index |
| 16 |  | `bsn_prm%rsdco` | real |  | residue decomposition coeff |
| 17 |  | `bsn_prm%percop` | real |  | pestcide perc coeff (0-1) |
| 18 |  | `bsn_prm%msk_co1` | real |  | calibration coeff to control impact of the storage |
| 19 |  | `bsn_prm%msk_co2` | real |  | time constant for the reach at bankfull depth calibration coefficient used to control impact of the |
| 20 |  | `bsn_prm%msk_x` | real |  | storage time constant for low flow (where low flow is when river is at 0.1 bankfull depth) upon the Km value calculated for the reach weighting factor control relative importance of inflow rate |
| 21 |  | `bsn_prm%nperco_lchtile` | real |  | and outflow rate in determining storage on reach n concentration coeff for tile flow and leach from bottom layer |
| 22 |  | `bsn_prm%evrch` | real |  | reach evaporation adjustment factor |
| 23 |  | `bsn_prm%scoef` | real |  | channel storage coefficient (0-1) |
| 24 |  | `bsn_prm%cdn` | real |  | denitrification exponential rate coefficient |
| 25 |  | `bsn_prm%sdnco` | real |  | denitrification threshold frac of field cap |
| 26 |  | `bsn_prm%bact_swf` | real |  | frac of manure containing active colony forming units |
| 27 |  | `bsn_prm%tb_adj` | real |  | adjustment factor for subdaily unit hydrograph basetime |
| 28 |  | `bsn_prm%cn_froz` | real |  | parameter for frozen soil adjustment on infiltraion/runoff |
| 29 |  | `bsn_prm%dorm_hr` | real |  | time threshold used to define dormant (hrs) |
| 30 |  | `bsn_prm%plaps` | real | mm/km | precipitation lapse rate: mm per km of elevation difference |
| 31 |  | `bsn_prm%tlaps` | real | deg C/km | temperature lapse rate: deg C per km of elevation difference |
| 32 |  | `bsn_prm%nfixmx` | real |  | max daily n-fixation (kg/ha) |
| 33 |  | `bsn_prm%decr_min` | real |  | minimum daily residue decay |
| 34 |  | `bsn_prm%rsd_covco` | real |  | residue cover factor for computing frac of cover |
| 35 |  | `bsn_prm%urb_init_abst` | real |  | maximum initial abstraction for urban areas when using Green and Ampt |
| 36 |  | `bsn_prm%petco_pmpt` | real |  | PET adjustment (%) for Penman-Montieth and Preiestly-Taylor methods |
| 37 |  | `bsn_prm%uhalpha` | real |  | alpha coeff for est unit hydrograph using gamma func |
| 38 |  | `bsn_prm%eros_spl` | real |  | coeff of splash erosion varying 0.9-3.1 |
| 39 |  | `bsn_prm%rill_mult` | real |  | rill erosion coefficient |
| 40 |  | `bsn_prm%eros_expo` | real |  | exponential coefficient for overland flow |
| 41 |  | `bsn_prm%c_factor` | real |  | scaling parameter for cover and management factor for |
| 42 |  | `bsn_prm%ch_d50` | real |  | overland flow erosion median particle diameter of main channel (mm) |
| 43 |  | `bsn_prm%co2` | real |  | co2 concentration at start of simulation (ppm) |
| 44 |  | `bsn_prm%day_lag_mx` | integer |  | max days to lag hydrographs for hru, ru and channels |
| 45 |  | `bsn_prm%igen` | integer |  | non-draining soils random generator code: |

## Sample

```text
Example record block from parameters.bsn (from a typical SWAT+ dataset):
 3.0 0.0 4.0 1.0 484.0 0.0 0.0 0.003 20.0 20.0 0.10 10.0 175.0 0.40 0.05 0.5 0.75 0.25 0.20 0.5 0.60 1.0 1.40 1.30 0.15 0.0 0.000862 -1.0 0.0 6.5 20.0 0.01 0.75 1.0 100.0 1.0 0.0 0.0 0.0 0.0 0.0 400.0 0 5
```

## Read Pattern

```fortran
open (107,file=in_basin%parms_bas)
read (107,*,iostat=eof) titldum
read (107,*,iostat=eof) header
read (107,*,iostat=eof) bsn_prm
```

## I/O Operations

| Direction | Op | Unit | Statement |
| --- | --- | --- | --- |
| File setup | `open` | 107 | `open (107,file=in_basin%parms_bas)` |
| Input | `read` | 107 | `read (107,*,iostat=eof) titldum` |
| Input | `read` | 107 | `read (107,*,iostat=eof) header` |
| Input | `read` | 107 | `read (107,*,iostat=eof) bsn_prm` |
| File control | `close` | 107 | `close(107)` |

## Readers

| Procedure | Operations | Role |
| --- | --- | --- |
| [sym:basin_read_prm] | open, read, close | Reads the `parameters.bsn` file if it exists and is not set to "null" in `in_basin%parms_bas`. It reads a title line, a header line, and then the basin parameters into the `bsn_prm` array of `type basin_parms`. |

## Review Notes

- Draft input-file overlay generated from static source facts; review and complete the remaining fields before promotion.
- The file is optional and only read if the filename is set and the file exists.
- The reader reads three lines: a title, a header, and then the basin parameters record.
- The `bsn_prm` array stores all parameters for each subbasin as defined in `basin_module`.
