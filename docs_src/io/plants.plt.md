---
kind: io
source_symbols:
- plant_parm_read
title: '`plants.plt`'
status: filled
source_hash: bf026e9174980917
version_label: SWAT+ 62.0.0
---

**Primary target:** `pldb(:)` (array of `type plant_db`)  
**Read by:** [sym:plant_parm_read]

## Bottom Line

`plants.plt` is the plant/land-cover parameter database. Each record defines one plant or land-cover type with its growth, leaf-area, light and nutrient-uptake, temperature, and residue parameters used by the plant-growth model.

The reader `plant_parm_read` reads a title line and a header line, counts the records, allocates `pldb(0:imax)`, then reads each record as a full `plant_db` value (optionally followed by a plant-class token).

The file is required for plant growth: if `in_parmdb%plants_plt` is missing or `null`, `pldb` is allocated with zero size.

| Module | Role for this file |
| --- | --- |
| [sym:plant_data_module] | Defines `type plant_db` and the `pldb` array each record is read into (also `pl_class` for the optional trailing class token). |
| [sym:input_file_module] | Supplies `in_parmdb`; `in_parmdb%plants_plt` holds the `plants.plt` filename opened on unit 104. |
| [sym:maximum_data_module] | Supplies `db_mx`; the reader stores the plant-record count in `db_mx%plantparm`. |

## File Variables

`plants.plt` has a title line and a column-header line followed by one record per plant or land-cover type. Each record is read as a full `plant_db` value, so the columns are the type's fields in declaration order beginning with the plant name. A record may carry an extra trailing plant-class token read into `pl_class`.

| Col | Header | Target | Type | Units | Meaning |
| --- | --- | --- | --- | --- | --- |
| 1 | `plantnm` | `pldb%plantnm` | character(len=40) | none | crop name |
| 2 | `typ` | `pldb%typ` | character(len=18) | none | plant category warm_annual cold_annual warm_annual_tuber cold_annual_tuber perennial |
| 3 | `trig` | `pldb%trig` | character(len=18) | none | phenology trigger moisture_gro temp_gro |
| 4 | `nfix_co` | `pldb%nfix_co` | real | none | n fixation coefficient (0.5 legume; 0 non-legume) |
| 5 | `days_mat` | `pldb%days_mat` | integer | days | days to maturity - if zero use hu for entire growing season |
| 6 | `bio_e` | `pldb%bio_e` | real | (kg/ha/(MJ/m**2) | biomass-energy ratio |
| 7 | `hvsti` | `pldb%hvsti` | real | (kg/ha)/(kg/ha) | harvest index: crop yield/aboveground biomass |
| 8 | `blai` | `pldb%blai` | real | none | max (potential) leaf area index |
| 9 | `frgrw1` | `pldb%frgrw1` | real | none | fraction of the growing season corresponding to the 1st point on optimal leaf area development curve |
| 10 | `laimx1` | `pldb%laimx1` | real | none | frac of max leaf area index corresponding to the 1st point on optimal leaf area development curve |
| 11 | `frgrw2` | `pldb%frgrw2` | real | none | fraction of the growing season corresponding to the 2nd point on optimal leaf area development curve |
| 12 | `laimx2` | `pldb%laimx2` | real | none | fraction of max leaf area index corresponding to the 2nd point on optimal leaf area development curve |
| 13 | `dlai` | `pldb%dlai` | real | none | frac of growing season when leaf are declines |
| 14 | `dlai_rate` | `pldb%dlai_rate` | real | none | exponent that governs lai decline rate |
| 15 | `chtmx` | `pldb%chtmx` | real | m | maximum canopy height |
| 16 | `rdmx` | `pldb%rdmx` | real | m | maximum root depth |
| 17 | `t_opt` | `pldb%t_opt` | real | deg C | optimal temp for plant growth |
| 18 | `t_base` | `pldb%t_base` | real | deg C | minimum temp for plant growth |
| 19 | `cnyld` | `pldb%cnyld` | real | kg N/kg yld | frac of nitrogen in yield |
| 20 | `cpyld` | `pldb%cpyld` | real | kg P/kg yld | frac of phosphorus in yield |
| 21 | `pltnfr1` | `pldb%pltnfr1` | real | kg N/kg biomass | nitrogen uptake parm #1 |
| 22 | `pltnfr2` | `pldb%pltnfr2` | real | kg N/kg biomass | nitrogen uptake parm #2 |
| 23 | `pltnfr3` | `pldb%pltnfr3` | real | kg N/kg/biomass | nitrogen uptake parm #3 |
| 24 | `pltpfr1` | `pldb%pltpfr1` | real | kg P/kg/biomass | phoshorus uptake parm #1 |
| 25 | `pltpfr2` | `pldb%pltpfr2` | real | kg P/kg/biomass | phoshorus uptake parm #2 |
| 26 | `pltpfr3` | `pldb%pltpfr3` | real | kg P/kg/biomass | phoshorus uptake parm #3 |
| 27 | `wsyf` | `pldb%wsyf` | real | (kg/ha)/(kg/ha) | value of harvest index bet 0 and HVSTI |
| 28 | `usle_c` | `pldb%usle_c` | real | none | minimum value of the USLE C factor for water erosion |
| 29 | `gsi` | `pldb%gsi` | real | m/s | maximum stomatal conductance |
| 30 | `vpdfr` | `pldb%vpdfr` | real | kPa | vapor pressure deficit at which GMAXFR is valid |
| 31 | `gmaxfr` | `pldb%gmaxfr` | real | none | fraction of max stomatal conductance that is |
| 32 | `wavp` | `pldb%wavp` | real |  | achieved at the vapor pressure deficit defined by VPDFR rate of decline in radiation use efficiency |
| 33 | `co2hi` | `pldb%co2hi` | real | uL CO2/L air | CO2 concentration higher than the ambient corresponding |
| 34 | `bioehi` | `pldb%bioehi` | real |  | to the 2nd point on radiation use efficiency curve biomass-energy ratio when plant is in an environment with |
| 35 | `rsdco_pl` | `pldb%rsdco_pl` | real |  | CO2 level equal to the value of CO2HI. plant residue decomposition coeff |
| 36 | `alai_min` | `pldb%alai_min` | real | m**2/m**2 | min LAI during winter dormant period |
| 37 | `laixco_tree` | `pldb%laixco_tree` | real | none | coefficient to estimate max lai during tree growth |
| 38 | `mat_yrs` | `pldb%mat_yrs` | integer | years | years to maturity |
| 39 | `bmx_peren` | `pldb%bmx_peren` | real | metric tons/ha | max biomass for forest |
| 40 | `ext_coef` | `pldb%ext_coef` | real |  | light extinction coefficient |
| 41 | `leaf_tov_min` | `pldb%leaf_tov_min` | real | months | perennial leaf turnover rate with minimum stress (complete turnover in 12 mon) |
| 42 | `leaf_tov_max` | `pldb%leaf_tov_max` | real | months | perennial leaf turnover rate with maximum stress (complete turnover in 3 mon) |
| 43 | `bm_dieoff` | `pldb%bm_dieoff` | real | frac | above ground biomass that dies off at dormancy |
| 44 | `rsr1` | `pldb%rsr1` | real | real :: leaf_frac_mx             !frac | max fraction of above ground biomass that is leaf (assume constant over life of perennial) initial root to shoot ratio at the beg of growing season |
| 45 | `rsr2` | `pldb%rsr2` | real | frac | root to shoot ratio at the end of the growing season |
| 46 | `pop1` | `pldb%pop1` | real | plants/m^2 | plant population corresponding to the 1st point on the |
| 47 | `frlai1` | `pldb%frlai1` | real |  | population lai curve frac of max leaf area index corresponding to the 1st |
| 48 | `pop2` | `pldb%pop2` | real |  | point on the leaf area development curve plant population corresponding to the 2nd point on the |
| 49 | `frlai2` | `pldb%frlai2` | real |  | population lai curve frac of max leaf area index corresponding to the 2nd |
| 50 | `frsw_gro` | `pldb%frsw_gro` | real |  | point on the leaf area development curve 30 day sum of P-PET to initiate growth of tropical |
| 51 | `aeration` | `pldb%aeration` | real |  | plants during monsoon season - pcom()%plcur()%iseason aeration stress factor |
| 52 | `rsd_pctcov` | `pldb%rsd_pctcov` | real |  | residue factor for percent cover equation |
| 53 | `rsd_covfac` | `pldb%rsd_covfac` | real |  | residue factor for surface cover (C factor) equation |
| 54 | `res_part_fracs` | `pldb%res_part_fracs` | type (residue_partition_fracs) |  | character(len=45) :: desc = "unknown" |

## Sample

```text
Schematic of the record layout (field names in read order, not a specific dataset):

<title line>
plantnm  typ  trig  nfix_co  days_mat  bm_e  harv_idx  lai_pot ...  (plant_db fields in order)
agrl     warm  1     0.0      110       15.0  0.76      5.0     ...
```

## Read Pattern

```fortran
open (104,file=in_parmdb%plants_plt)
read (104,*,iostat=eof) titldum
read (104,*,iostat=eof) header
rewind (104)
read (104,*,iostat=eof) pldb(ic)
read (104,*,iostat=eof) pldb(ic), pl_class(ic)
```

## I/O Operations

| Direction | Op | Unit | Statement |
| --- | --- | --- | --- |
| File setup | `open` | 104 | `open (104,file=in_parmdb%plants_plt)` |
| Input | `read` | 104 | `read (104,*,iostat=eof) titldum` |
| Input | `read` | 104 | `read (104,*,iostat=eof) header` |
| Input | `read` | 104 | `read (104,*,iostat=eof) titldum` |
| File control | `rewind` | 104 | `rewind (104)` |
| Input | `read` | 104 | `read (104,*,iostat=eof) titldum` |
| Input | `read` | 104 | `read (104,*,iostat=eof) header` |
| Input | `read` | 104 | `read (104,*,iostat=eof) pldb(ic)` |
| Input | `read` | 104 | `read (104,*,iostat=eof) pldb(ic), pl_class(ic)` |
| File control | `close` | 104 | `close (104)` |

## Readers

| Procedure | Operations | Role |
| --- | --- | --- |
| [sym:plant_parm_read] | backspace, open, read | Opens `plants.plt` on unit 104, reads the title and header, counts records and allocates `pldb(0:imax)`, then reads each record as a full `plant_db` value (with an optional trailing plant-class token) into `pldb(ic)`. |

## Review Notes

- Each record is read as a whole `plant_db` value; columns are the type fields in declaration order.
- A record may include a trailing plant-class token, read as `pldb(ic), pl_class(ic)` when present.
- Records are indexed by read order; there is no id column in the file.
- If `plants.plt` is missing or `null`, `pldb` is allocated with zero size.
