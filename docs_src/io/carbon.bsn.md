---
kind: io
source_symbols:
- carbon_bsn_read
title: '`carbon.bsn`'
status: filled
source_hash: 62ee54373bdf61f2
version_label: SWAT+ 62.0.0
---

**Primary target:** `org_frac(:)` (array of `type organic_fractions`)  
**Read by:** [sym:carbon_bsn_read]

## Bottom Line

carbon.bsn is a required input file when carbon cycling is enabled (bsn_cc%cswat == 2).

It configures carbon cycling parameters including organic fractions, carbon loss coefficients, manure coefficients, and organic controls.

The primary reader for this file is the subroutine carbon_bsn_read, which also reads the companion file carbon_lyr.bsn for per-layer carbon coefficients.

Both carbon.bsn and carbon_lyr.bsn must be present and correctly formatted; the reader aborts if either is missing or malformed.

| Module | Role for this file |
| --- | --- |
| [sym:carbon_module] | Provides the target data structures org_frac (organic_fractions), cb_wtr_coef (carbon_water_coef), man_coef (manure_coef), org_con (organic_controls), and arrays carbdb and org_allo where data from carbon.bsn and carbon_lyr.bsn are stored. |
| [sym:basin_module] | Provides the in_basin variable which holds the file path for carbon.bsn and is used to derive the carbon_lyr.bsn filename. |
| [sym:tillage_data_module] | Provides variables till_eff_days, bio_consf, till_consf, bmix_a, bmix_b, bmix_c, tillmix_a, tillmix_b, tillmix_c which are read from carbon.bsn and stored for tillage and biomass mixing parameters. |
| [sym:plant_data_module] | No direct variables identified as read or stored from this module in carbon_bsn_read. |
| [sym:input_file_module] | Provides the in_basin variable used to locate the carbon.bsn input file. |

## File Variables

The carbon.bsn file contains a header and a single data row with 28 values that configure carbon cycling parameters including organic fractions, carbon loss coefficients, manure coefficients, tillage effects, and organic controls. The data is read into various derived types and variables defined in carbon_module and related modules.

| Col | Header | Target | Type | Units | Meaning |
| --- | --- | --- | --- | --- | --- |
| 7 |  | `org_frac%frac_seq` | real |  | fraction of total carbon the is sequestered carbon when initializing sequestered pools |
| 9 |  | `org_frac%frac_hum_microb` | real |  | fraction of carbon that is microbrial pool when initializing microbrial pools |
| 10 |  | `org_frac%frac_hum_slow` | real |  | fraction of carbon that is humas slow pool when initializing humus slow pools |
| 11 |  | `org_frac%frac_hum_passive` | real |  | fraction of carbon that is humas passive pool when initializing humas passive pools |
| 2 |  | `cb_wtr_coef%prmt_21` | real |  | KOC FOR CARBON LOSS IN WATER AND SEDIMENT(500._1500.) KD = KOC * C |
| 3 |  | `cb_wtr_coef%prmt_44` | real |  | RATIO OF SOLUBLE C CONCENTRATION IN RUNOFF TO PERCOLATE(0.1_1.) |
| 2 |  | `man_coef%rtof` | real | none | weighting factor used to partition the organic N & P concentration of septic effluent between the fresh organic and the stable organic pools |
| 3 |  | `man_coef%man_to_c` | real |  | conversion of manure solids to carbon |
| 14 |  | `org_con%tmpf` | integer |  | temperature factor approach used in cbn_zhang2 |
| 15 |  | `org_con%watf` | integer |  | water factor approach used in cbn_zhang2 |
| 11 |  | `org_con%tn` | real | real :: xbmt = 0.          ! | control on transformation of microbial biomass by soil texture and structure control on potential transformation of structural litter by lignin fraction The following three parameters resolve the shape of the temperature effect equation: minimum temperature bound |
| 12 |  | `org_con%top` | real | celsius | peak (optimum) temperature |
| 13 |  | `org_con%tx` | real | celsius | maximum temperature bound |
| 2 |  | `org_con%sut` | real |  | soil water control on biological processes |
| 3 |  | `org_con%cdg` | real |  | soil temperature control on biological processes |
| 4 |  | `org_con%cs` | real |  | combined factor controlling biological processes |
| 5 |  | `org_con%ox` | real |  | oxygen control on biological processes |
| 6 |  | `org_con%till_eff` | real |  | tillage effect |
| 7 |  | `org_con%x1` | real |  | tillage control on residue decomposition |
| 8 |  | `org_con%no3` | real |  | no3 as adjusted in cbn_zhang2 |
| 9 |  | `org_con%nh4` | real |  | nh4 as adjusted in cbn_zhang2 |
| 10 |  | `org_con%resp` | real |  | co2 respiration |
| 12 |  | `org_frac%lmf` | real | frac | fraction of the litter that is metabolic |
| 13 |  | `org_frac%lmnf` | real | kg kg-1 | fraction of metabolic litter that is N |
| 14 |  | `org_frac%lsf` | real | frac | fraction of the litter that is structural |
| 15 |  | `org_frac%lslf` | real | kg kg-1 | fraction of structural litter that is lignin |
| 16 |  | `org_frac%lsnf` | real | kg kg-1 | fraction of structural litter that is N |
| 17 |  | `org_frac%mathers_method` | logical |  | logical indicating whether to use the mathers_method to initialize humus slow pools |

## Sample

```text
Example carbon.bsn file snippet:
Title line (optional)
Column header line (optional)
0.95 0.02 0.54 0.44 1000.0 0.5 30 0.5 1 2 1 30 50 0.5 0.5 0.5 0.5 0.5 0.5 0.5 0.5 0.5 0.5 0.5 0.5 0.5 0.5 1
```

## Read Pattern

```fortran
open (107, file=in_basin%carbon_bsn, iostat=eof)
read (107, '(a)', iostat=eof) titldum
read (107, '(a)', iostat=eof) header
read (107, *, iostat=eof) org_frac%frac_seq, org_frac%frac_hum_microb, org_frac%frac_hum_slow, org_frac%frac_hum_passive, cb_wtr_coef%prmt_21, cb_wtr_coef%prmt_44, till_eff_days, man_coef%rtof, bio_consf, till_consf, org_con%tmpf, org_con%watf, org_con%tn, org_con%top, org_con%tx, bmix_a, bmix_b, bmix_c, tillmix_a, tillmix_b, tillmix_c, photo_degrade_factor, n_act_frac, cnr_cap, cnr_ref, cpr_cap, cpr_ref, mathers_int
read (107, '(a)', iostat=eof) titldum
read (107, '(a)', iostat=eof) header
read (107, *, iostat=eof) layer_id, r_hp_rate, r_hs_rate, r_microb_rate, r_meta_rate, r_str_rate, r_microb_top_rate, r_hs_hp, r_a1co2, r_asco2, r_apco2, r_abco2
```

## I/O Operations

| Direction | Op | Unit | Statement |
| --- | --- | --- | --- |
| File setup | `open` | 107 | `open (107, file=in_basin%carbon_bsn, iostat=eof)` |
| Input | `read` | 107 | `read (107, '(a)', iostat=eof) titldum` |
| Input | `read` | 107 | `read (107, '(a)', iostat=eof) header` |
| Input | `read` | 107 | `read (107, *, iostat=eof) org_frac%frac_seq,         org_frac%frac_hum_microb, org_frac%frac_hum_slow,    org_frac%frac_hum_passive, cb_wtr_coef%prmt_21,       cb_wtr_coef%prmt_44, till_eff_days,             man_coef%rtof, bio_consf,                 till_consf, org_con%tmpf,              org_con%watf, org_con%tn, org_con%top,   org_con%tx, bmix_a, bmix_b, bmix_c, tillmix_a, tillmix_b, tillmix_c, photo_degrade_factor, n_act_frac, cnr_cap, cnr_ref, cpr_cap, cpr_ref, mathers_int` |
| File control | `close` | 107 | `close (107)` |
| File control | `close` | 107 | `close (107)` |
| Input | `read` | 107 | `read (107, '(a)', iostat=eof) titldum` |
| Input | `read` | 107 | `read (107, '(a)', iostat=eof) header` |
| Input | `read` | 107 | `read (107, *, iostat=eof) layer_id, r_hp_rate, r_hs_rate, r_microb_rate, r_meta_rate, r_str_rate, r_microb_top_rate, r_hs_hp, r_a1co2, r_asco2, r_apco2, r_abco2` |
| File control | `close` | 107 | `close (107)` |
| File control | `close` | 107 | `close (107)` |

## Readers

| Procedure | Operations | Role |
| --- | --- | --- |
| [sym:carbon_bsn_read] | close, open, read | Reads carbon.bsn and the companion carbon_lyr.bsn files to populate carbon cycling parameters and per-layer carbon coefficients. It validates file existence and format, aborting on errors. It stores data into org_frac, cb_wtr_coef, man_coef, org_con, and arrays carbdb and org_allo. |

## Review Notes

- Draft input-file overlay generated from static source facts; review and complete the remaining fields before promotion.
- carbon.bsn must be present and correctly formatted when carbon cycling is enabled (bsn_cc%cswat == 2).
- carbon_lyr.bsn is derived from carbon.bsn filename and also required; it provides per-layer carbon decomposition coefficients.
- The reader aborts with error stop if either file is missing or malformed.
- No direct variables from plant_data_module are read or stored in this routine despite the module being used.
