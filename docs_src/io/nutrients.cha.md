---
kind: io
source_symbols:
- ch_read_nut
title: '`nutrients.cha`'
status: filled
source_hash: 827dc3af7eac4c58
version_label: SWAT+ 62.0.0
---

**Primary target:** `ch_nut(:)` (array of `type channel_nut_data`)  
**Read by:** [sym:ch_read_nut]

## Bottom Line

`nutrients.cha` sets the in-stream water-quality (QUAL2E) parameters for each channel: organic N and P concentrations, algal growth and settling rates, nutrient and CBOD reaction-rate coefficients, and light/temperature factors.

The reader `ch_read_nut` reads a title line and a header line, counts the records, allocates `ch_nut(0:imax)`, then reads one full `channel_nut_data` record per channel. Any parameter left at or below zero is replaced with a QUAL2E default, and several rates are rescaled by the routing time step.

If `in_cha%nut` is missing or set to `"null"`, `ch_nut` is allocated with zero size and no channel nutrient parameters are loaded.

| Module | Role for this file |
| --- | --- |
| [sym:input_file_module] | Supplies `in_cha`; `in_cha%nut` holds the `nutrients.cha` filename opened on unit 105. |
| [sym:basin_module] | Imported by the reader; no specific symbol is used in the record read. |
| [sym:time_module] | Supplies `time%step`; day-based rates (`rs1`-`rs5`, `rk1`-`rk4`, `bc1`-`bc4`, `mumax`, `rhoq`) are divided by the step count for sub-daily routing. |
| [sym:maximum_data_module] | Supplies `db_mx`; the reader stores the channel-nutrient record count in `db_mx%ch_nut`. |
| [sym:channel_data_module] | Defines `type channel_nut_data` and the `ch_nut` array each record is read into. |

## File Variables

`nutrients.cha` has two header lines (a title line and a column-header line) followed by one record per channel. Each record is read as a full `channel_nut_data` value, so the columns are the type's fields in declaration order, starting with the record name. Any parameter read as <= 0 is replaced by the QUAL2E default shown in the Default column; several rate constants are additionally divided by the routing time step for sub-daily runs.

| Col | Header | Target | Type | Units | Meaning |
| --- | --- | --- | --- | --- | --- |
| 1 | `name` | `ch_nut%name` | character(len=16) |  | channel water-quality record name (header row per channel) |
| 2 | `onco` | `ch_nut%onco` | real | ppm | channel organic n concentration |
| 3 | `opco` | `ch_nut%opco` | real | ppm | channel organic p concentration |
| 4 | `rs1` | `ch_nut%rs1` | real | m/day or m/hr | local algal settling rate in reach at 20 deg C |
| 5 | `rs2` | `ch_nut%rs2` | real | (mg disP-P)/((m**2)*day) or (mg disP-P)/((m**2)*hr) | benthos source rate for dissolved phosphorus in the reach at 20 deg C |
| 6 | `rs3` | `ch_nut%rs3` | real | (mg NH4-N)/((m**2)*day) or (mg NH4-N)/((m**2)*hr) | benthos source rate for ammonia nitrogen in the reach at 20 deg C |
| 7 | `rs4` | `ch_nut%rs4` | real | 1/day or 1/hr | rate coefficient for organic nitrogen settling in the reach at 20 deg C |
| 8 | `rs5` | `ch_nut%rs5` | real | 1/day or 1/hr | org phos settling rate in reach at 20 deg C |
| 9 | `rs6` | `ch_nut%rs6` | real | 1/day | rate coeff for settling of arbitrary non-conservative constituent in reach |
| 10 | `rs7` | `ch_nut%rs7` | real | (mg ANC)/((m**2)*day) | benthal source rate for arbitrary non-conservative constituent in the reach |
| 11 | `rk1` | `ch_nut%rk1` | real | 1/day or 1/hr | CBOD deoxygenation rate coeff in reach at 20 deg C |
| 12 | `rk2` | `ch_nut%rk2` | real | 1/day or 1/hr | reaeration rate in accordance with Fickian diffusion in reach at 20 deg C |
| 13 | `rk3` | `ch_nut%rk3` | real | 1/day or 1/hr | rate of loss of CBOD due to settling in reach at 20 deg C |
| 14 | `rk4` | `ch_nut%rk4` | real | mg O2/((m**2)*day) or mg O2/((m**2)*hr) | sediment oxygen demand rate in the reach at 20 deg C |
| 15 | `rk5` | `ch_nut%rk5` | real | 1/day | coliform die-off rate in reach |
| 16 | `rk6` | `ch_nut%rk6` | real | 1/day | decay rate for arbitrary non-conservative constituent in reach |
| 17 | `bc1` | `ch_nut%bc1` | real | 1/hr | rate constant for biological oxidation of NH3 to NO2 in reach at 20 deg C |
| 18 | `bc2` | `ch_nut%bc2` | real | 1/hr | rate constant for biological oxidation of NO2 to NO3 in reach at 20 deg C |
| 19 | `bc3` | `ch_nut%bc3` | real | 1/hr | rate constant for hydrolysis of organic N to ammonia in reach at 20 deg C |
| 20 | `bc4` | `ch_nut%bc4` | real | 1/hr | rate constant for the decay of organic P to dissolved P in reach at 20 deg C |
| 21 | `lao` | `ch_nut%lao` | real | NA | Qual2E light-averaging option; only option 2 is currently available in SWAT+ |
| 22 | `igropt` | `ch_nut%igropt` | integer | none | Qual2E option for the local algal growth rate: 1=multiplicative, 2=limiting nutrient, 3=harmonic mean |
| 23 | `ai0` | `ch_nut%ai0` | real | ug chla/mg alg | ratio of chlorophyll-a to algal biomass |
| 24 | `ai1` | `ch_nut%ai1` | real | mg N/mg alg | fraction of algal biomass that is nitrogen |
| 25 | `ai2` | `ch_nut%ai2` | real | mg P/mg alg | fraction of algal biomass that is phosphorus |
| 26 | `ai3` | `ch_nut%ai3` | real | mg O2/mg alg | the rate of oxygen production per unit of algal photosynthesis |
| 27 | `ai4` | `ch_nut%ai4` | real | mg O2/mg alg | the rate of oxygen uptake per unit of algae respiration |
| 28 | `ai5` | `ch_nut%ai5` | real | mg O2/mg N | the rate of oxygen uptake per unit of NH3 nitrogen oxidation |
| 29 | `ai6` | `ch_nut%ai6` | real | mg O2/mg N | the rate of oxygen uptake per unit of NO2 nitrogen oxidation |
| 30 | `mumax` | `ch_nut%mumax` | real | 1/hr | maximum specific algal growth rate at 20 deg C |
| 31 | `rhoq` | `ch_nut%rhoq` | real | 1/day or 1/hr | algal respiration rate |
| 32 | `tfact` | `ch_nut%tfact` | real | none | fraction of heat-balance solar radiation that is photosynthetically active |
| 33 | `k_l` | `ch_nut%k_l` | real | MJ/(m2*hr) | half-saturation coefficient for light (read as kJ/(m2*min), converted to MJ/(m2*hr)) |
| 34 | `k_n` | `ch_nut%k_n` | real | mg N/L | michaelis-menton half-saturation constant for nitrogen |
| 35 | `k_p` | `ch_nut%k_p` | real | mg P/L | michaelis-menton half saturation constant for phosphorus |
| 36 | `lambda0` | `ch_nut%lambda0` | real | 1/m | non-algal portion of the light extinction coefficient |
| 37 | `lambda1` | `ch_nut%lambda1` | real | 1/(m*ug chla/L) | linear algal self-shading coefficient |
| 38 | `lambda2` | `ch_nut%lambda2` | real | (1/m)(ug chla/L)**(-2/3) | nonlinear algal self-shading coefficient |
| 39 | `p_n` | `ch_nut%p_n` | real | none | algal preference factor for ammonia |

## Sample

```text
Schematic of the record layout (field names in read order, not a specific dataset):

<title line>
name  onco opco rs1  rs2  rs3 rs4  rs5  rs6 rs7 rk1  rk2 rk3 rk4 rk5  rk6  bc1  bc2 bc3  bc4  lao igropt ai0 ai1  ai2   ai3 ai4 ai5 ai6 mumax rhoq tfact k_l  k_n  k_p   lambda0 lambda1 lambda2 p_n
nut1  0.0  0.0  1.0  .05  .5  .05  .05  2.5 2.5 1.71 1.0 2.0 0.0 1.71 1.71 .55  1.1 .21  .35  2   2      50. .08  .015  1.6 2.0 3.5 1.07 2.0  2.5  0.3  .75  .02  .025  1.0     .03     .054    0.5
```

## Read Pattern

```fortran
open (105,file=in_cha%nut)
read (105,*,iostat=eof) titldum
read (105,*,iostat=eof) header
rewind (105)
backspace (105)
read (105,*,iostat=eof) ch_nut(ich)
```

## I/O Operations

| Direction | Op | Unit | Statement |
| --- | --- | --- | --- |
| File setup | `open` | 105 | `open (105,file=in_cha%nut)` |
| Input | `read` | 105 | `read (105,*,iostat=eof) titldum` |
| Input | `read` | 105 | `read (105,*,iostat=eof) header` |
| Input | `read` | 105 | `read (105,*,iostat=eof) titldum` |
| File control | `rewind` | 105 | `rewind (105)` |
| Input | `read` | 105 | `read (105,*,iostat=eof) titldum` |
| Input | `read` | 105 | `read (105,*,iostat=eof) header` |
| Input | `read` | 105 | `read (105,*,iostat=eof) titldum` |
| File control | `backspace` | 105 | `backspace (105)` |
| Input | `read` | 105 | `read (105,*,iostat=eof) ch_nut(ich)` |
| File control | `close` | 105 | `close(105)` |

## Readers

| Procedure | Operations | Role |
| --- | --- | --- |
| [sym:ch_read_nut] | backspace, open, read | Opens `nutrients.cha` on unit 105, reads the title and header lines, counts records and allocates `ch_nut(0:imax)`, then reads one full `channel_nut_data` record per channel, applies QUAL2E defaults for non-positive parameters, converts `k_l` units, and rescales day-based rates by the routing time step. |

## Review Notes

- The reader's PURPOSE comment describes a lake water-quality (.lwq) file, but the routine actually reads the channel nutrient file `in_cha%nut` (`nutrients.cha`); the comment is stale.
- Any parameter read as <= 0 is overwritten with the QUAL2E default shown in the Default column (ch_read_nut.f90:44-95).
- `k_l` is read in kJ/(m2*min) and converted to MJ/(m2*hr) (multiplied by 1e-3 * 60).
- For sub-daily routing, day-based rates (`rs1`-`rs5`, `rk1`-`rk4`, `bc1`-`bc4`, `mumax`, `rhoq`) are divided by `time%step`.
- Records are indexed by read order (`ich`); there is no id column in the file.
- If `nutrients.cha` is missing or `null`, `ch_nut` is allocated with zero size.
