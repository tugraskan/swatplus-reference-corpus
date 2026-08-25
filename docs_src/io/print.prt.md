---
kind: io
source_symbols:
- basin_print_codes_read
title: '`print.prt`'
status: filled
source_hash: dc8a548664eb8846
version_label: SWAT+ 62.0.0
---

**Primary target:** `pco(:)` (array of `type basin_print_codes`)  
**Read by:** [sym:basin_print_codes_read]

## Bottom Line

`print.prt` configures the print/output options for SWAT+ model runs, specifying which outputs are generated, their intervals, formats (CSV, NetCDF), and the time periods for which outputs are written. It is read by the `basin_print_codes_read` routine at model initialization. The file is required if output control is desired; if missing, default output settings are used. The file controls the content and frequency of model output for basin, region, HRU, channel, reservoir, aquifer, and other objects.

| Module | Role for this file |
| --- | --- |
| [sym:input_file_module] | Provides `in_sim%prt` (the filename for print.prt) and possibly other file path variables. |
| [sym:basin_module] | Supplies the `pco(:)` array of type `basin_print_codes`, which is the main target for all fields read from print.prt. |
| [sym:time_module] | Supplies `time%yrc` and `time%nbyr`, used for defaulting output start/end years if not set in print.prt. |

## File Variables

The `print.prt` file defines output control settings for the SWAT+ model. Each record in the file is mapped to fields in the `basin_print_codes` derived type (`pco(:)`), with each field controlling a specific output option, frequency, or object. The file is read sequentially, with each line or block corresponding to a group of output settings or intervals.

| Col | Header | Target | Type | Units | Meaning |
| --- | --- | --- | --- | --- | --- |
| 2 |  | `pco%day_print` | character (len=1) |  | Flag for daily print output (not actively used in current code). |
| 3 |  | `pco%day_print_over` | character (len=1) |  | Flag for daily print output override (not actively used in current code). |
| 4 |  | `pco%nyskip` | integer |  | number of years to skip output summarization |
| 5 |  | `pco%sw_init` | character (len=1) |  | n=sw not initialized, y=sw initialized for output (when hit nyskip) |
| 6 |  | `pco%day_start` | integer |  | DAILY START/END AND INTERVAL julian day to start printing output |
| 7 |  | `pco%day_end` | integer |  | julian day to end printing output |
| 8 |  | `pco%yrc_start` | integer |  | calendar year to start printing output |
| 9 |  | `pco%yrc_end` | integer |  | calendar year to end printing output |
| 10 |  | `pco%int_day` | integer |  | interval between daily printing |
| 11 |  | `pco%int_day_cur` | integer |  | current day since last print |
| 12 |  | `pco%aa_numint` | integer |  | AVE ANNUAL END YEARS number of print intervals for ave annual output |
| 13 |  | `pco%aa_yrs` | integer |  | end years for ave annual output |
| 14 |  | `pco%csvout` | character(len=1) |  | SPECIAL OUTPUTS code to print .csv files n=no print; y=print; |
| 15 |  | `pco%use_obj_labels` | character(len=1) |  | Flag to read print objects by label instead of fixed order; also used for carbon output code. |
| 16 |  | `pco%cdfout` | character(len=1) |  | code to print netcdf (cdf) files n=no print; y=print; |
| 17 |  | `pco%crop_yld` | character(len=1) |  | crop yields - a=average annual; y=yearly; b=both annual and yearly; n=no print |
| 18 |  | `pco%mgtout` | character(len=1) |  | management output file (mgt.out) (default ave annual-d,m,y,a input) |
| 19 |  | `pco%hydcon` | character(len=1) |  | hydrograph connect output file (hydcon.out) |
| 20 |  | `pco%fdcout` | character(len=1) |  | flow duration curve output n=no print; avann=print; NOT ACTIVE |
| 21 |  | `pco%wb_bsn` | type(print_interval) |  | BASIN water balance BASIN output |
| 22 |  | `pco%nb_bsn` | type(print_interval) |  | nutrient balance BASIN output |
| 23 |  | `pco%ls_bsn` | type(print_interval) |  | losses BASIN output |
| 24 |  | `pco%pw_bsn` | type(print_interval) |  | plant weather BASIN output |
| 25 |  | `pco%aqu_bsn` | type(print_interval) |  | aquifer BASIN output |
| 26 |  | `pco%res_bsn` | type(print_interval) |  | reservoir BASIN output |
| 27 |  | `pco%chan_bsn` | type(print_interval) |  | channel BASIN output |
| 28 |  | `pco%sd_chan_bsn` | type(print_interval) |  | SWAT-DEG channel BASIN output |
| 29 |  | `pco%recall_bsn` | type(print_interval) |  | recall BASIN output |
| 30 |  | `pco%wb_reg` | type(print_interval) |  | REGION water balance REGION output |
| 31 |  | `pco%nb_reg` | type(print_interval) |  | nutrient balance REGION output |
| 32 |  | `pco%ls_reg` | type(print_interval) |  | losses REGION output |
| 33 |  | `pco%pw_reg` | type(print_interval) |  | plant weather REGION output |
| 34 |  | `pco%aqu_reg` | type(print_interval) |  | aquifer REGION output |
| 35 |  | `pco%res_reg` | type(print_interval) |  | reservoir REGION output |
| 36 |  | `pco%sd_chan_reg` | type(print_interval) |  | SWAT-DEG channel REGION output |
| 37 |  | `pco%recall_reg` | type(print_interval) |  | recall REGION output |
| 38 |  | `pco%water_allo` | type(print_interval) |  | water allocation REGION output |
| 39 |  | `pco%wb_lsu` | type(print_interval) |  | LSU water balance LSU output |
| 40 |  | `pco%nb_lsu` | type(print_interval) |  | nutrient balance LSU output |
| 41 |  | `pco%ls_lsu` | type(print_interval) |  | losses LSU output |
| 42 |  | `pco%pw_lsu` | type(print_interval) |  | plant weather LSU output |
| 43 |  | `pco%wb_hru` | type(print_interval) |  | HRU water balance HRU output |
| 44 |  | `pco%nb_hru` | type(print_interval) |  | nutrient balance HRU output |
| 45 |  | `pco%ls_hru` | type(print_interval) |  | losses HRU output |
| 46 |  | `pco%pw_hru` | type(print_interval) |  | plant weather HRU output |
| 47 |  | `pco%cb_hru` | type(print_interval) |  | legacy carbon flag (kept for backward compat with print.prt readers; no longer referenced by writers) |
| 48 |  | `pco%cb_vars_hru` | type(print_interval) |  | legacy carbon variable flag (same) |
| 49 |  | `pco%cb_gl_hru` | type(print_interval) |  | per-family carbon output flags (10 rows) hru_carb_gl_* HRU C gain/loss |
| 50 |  | `pco%cb_trf_hru` | type(print_interval) |  | hru_scf_* HRU C transformations |
| 51 |  | `pco%cb_lyr_hru` | type(print_interval) |  | hru_cbn_lyr_* per-layer SOC totals + sequestered |
| 52 |  | `pco%cb_cpool_hru` | type(print_interval) |  | hru_cpool_stat_* per-layer C pools |
| 53 |  | `pco%cb_npool_hru` | type(print_interval) |  | hru_n_p_pool_stat_* per-layer N+P pools |
| 54 |  | `pco%cb_plt_hru` | type(print_interval) |  | hru_plc_stat_* plant C state |
| 55 |  | `pco%cb_flux_hru` | type(print_interval) |  | hru_cflux_stat_* per-layer flux diagnostic |
| 56 |  | `pco%cb_drv_hru` | type(print_interval) |  | hru_carb_drv_* per-layer drivers diagnostic |
| 57 |  | `pco%cb_dyn_hru` | type(print_interval) |  | hru_carb_dyn_* per-layer dynamics diagnostic |
| 58 |  | `pco%cb_snap_hru` | type(print_interval) |  | hru_soil_snap_* soil property snapshot |
| 59 |  | `pco%cb_gl_lsu` | type(print_interval) |  | LSU-level area-weighted aggregations (Option 1: HRU-aggregated families only) lsu_carb_gl_* LSU-area-weighted C gain/loss |
| 60 |  | `pco%cb_trf_lsu` | type(print_interval) |  | lsu_scf_* LSU-area-weighted C transformations |
| 61 |  | `pco%cb_plt_lsu` | type(print_interval) |  | lsu_plc_stat_* LSU-area-weighted plant C state |
| 62 |  | `pco%wb_sd` | type(print_interval) |  | HRU-LTE water balance SWAT-DEG output |
| 63 |  | `pco%nb_sd` | type(print_interval) |  | nutrient balance SWAT-DEG output |
| 64 |  | `pco%ls_sd` | type(print_interval) |  | losses SWAT-DEG output |
| 65 |  | `pco%pw_sd` | type(print_interval) |  | plant weather SWAT-DEG output |
| 66 |  | `pco%chan` | type(print_interval) |  | CHANNEL channel output |
| 67 |  | `pco%sd_chan` | type(print_interval) |  | CHANNEL_LTE swat deg (lte) channel output |
| 68 |  | `pco%aqu` | type(print_interval) |  | AQUIFER aqufier output |
| 69 |  | `pco%res` | type(print_interval) |  | RESERVOIR reservoir output |
| 70 |  | `pco%recall` | type(print_interval) |  | RECALL recall output |
| 71 |  | `pco%hyd` | type(print_interval) |  | HYDIN AND HYDOUT hydin_output and hydout_output |
| 72 |  | `pco%ru` | type(print_interval) |  | routing unit output |
| 73 |  | `pco%pest` | type(print_interval) |  | all constituents pesticide output files (hru, chan, res, basin_chan, basin_res, ...) |
| 74 |  | `pco%salt_basin` | type(print_interval) |  | basin_ls SALT (rtb salt) salt output for the basin |
| 75 |  | `pco%salt_hru` | type(print_interval) |  | salt output for HRUs |
| 76 |  | `pco%salt_ru` | type(print_interval) |  | salt output for routing units |
| 77 |  | `pco%salt_aqu` | type(print_interval) |  | salt output for aquifers |
| 78 |  | `pco%salt_chn` | type(print_interval) |  | salt output for channels |
| 79 |  | `pco%salt_res` | type(print_interval) |  | salt output for reservoirs |
| 80 |  | `pco%salt_wet` | type(print_interval) |  | salt output for reservoirs |
| 81 |  | `pco%cs_basin` | type(print_interval) |  | CONSTITUENTS (rtb cs) constituent output for the basin |
| 82 |  | `pco%cs_hru` | type(print_interval) |  | constituent output for HRUs |
| 83 |  | `pco%cs_ru` | type(print_interval) |  | constituent output for routing units |
| 84 |  | `pco%cs_aqu` | type(print_interval) |  | constituent output for aquifers |
| 85 |  | `pco%cs_chn` | type(print_interval) |  | constituent output for channels |
| 86 |  | `pco%cs_res` | type(print_interval) |  | constituent output for reservoirs |
| 87 |  | `pco%cs_wet` | type(print_interval) |  | constituent output for reservoirs |
| 88 |  | `pco%gwflow_wb` | type(print_interval) |  | gwflow cell + basin water balance (day/mon/yr/aa) |
| 89 |  | `pco%gwflow_flux` | type(print_interval) |  | gwflow canal, pond, tile, gwsw, chan obs diagnostic output |
| 90 |  | `pco%gwflow_heat` | type(print_interval) |  | gwflow basin heat balance output |
| 91 |  | `pco%gwflow_solute` | type(print_interval) |  | gwflow basin solute balance output |
| 92 |  | `pco%gwflow_obs` | type(print_interval) |  | gwflow observation well output |
| 93 |  | `pco%gwflow_pump` | type(print_interval) |  | gwflow HRU pumping output |

## Sample

```text
Title of file
Header line
0 1 2020 366 2025 1
Header line
2 2021 2022
Header line
n n n
Header line
a n n n
Header line
BASIN 1 1 1 1
BASIN 1 1 1 1
BASIN 1 1 1 1
BASIN 1 1 1 1
BASIN 1 1 1 1
BASIN 1 1 1 1
BASIN 1 1 1 1
BASIN 1 1 1 1
REGION 1 1 1 1
REGION 1 1 1 1
REGION 1 1 1 1
REGION 1 1 1 1
REGION 1 1 1 1
REGION 1 1 1 1
REGION 1 1 1 1
REGION 1 1 1 1
LSU 1 1 1 1
LSU 1 1 1 1
LSU 1 1 1 1
LSU 1 1 1 1
HRU 1 1 1 1
HRU 1 1 1 1
HRU 1 1 1 1
HRU 1 1 1 1
HRU-LTE 1 1 1 1
HRU-LTE 1 1 1 1
HRU-LTE 1 1 1 1
HRU-LTE 1 1 1 1
CHANNEL 1 1 1 1
CHANNEL-LTE 1 1 1 1
AQUIFER 1 1 1 1
RESERVOIR 1 1 1 1
RECALL 1 1 1 1
HYDIN 1 1 1 1
RU 1 1 1 1
PEST 1 1 1 1
SALT_BASIN 1 1 1 1
SALT_HRU 1 1 1 1
SALT_RU 1 1 1 1
SALT_AQU 1 1 1 1
SALT_CHN 1 1 1 1
SALT_RES 1 1 1 1
SALT_WET 1 1 1 1
CS_BASIN 1 1 1 1
CS_HRU 1 1 1 1
CS_RU 1 1 1 1
CS_AQU 1 1 1 1
CS_CHN 1 1 1 1
CS_RES 1 1 1 1
CS_WET 1 1 1 1
GWFLOW_WB 1 1 1 1
GWFLOW_FLUX 1 1 1 1
GWFLOW_HEAT 1 1 1 1
GWFLOW_SOLUTE 1 1 1 1
GWFLOW_OBS 1 1 1 1
GWFLOW_PUMP 1 1 1 1
```

## Read Pattern

```fortran
open (107,file=in_sim%prt)
read (107,*,iostat=eof) titldum
read (107,*,iostat=eof) header
read (107,*,iostat=eof) pco%nyskip, pco%day_start, pco%yrc_start, pco%day_end, pco%yrc_end, pco%int_day
read (107,*,iostat=eof) pco%aa_numint
backspace (107)
read (107,*,iostat=eof) pco%aa_numint, (pco%aa_yrs(ii), ii = 1, pco%aa_numint)
read (107,*,iostat=eof) pco%csvout, pco%use_obj_labels, pco%cdfout
read (107,*,iostat=eof) pco%crop_yld, pco%mgtout, pco%hydcon, pco%fdcout
read (107,*,iostat=eof) name, pco%wb_bsn%d, pco%wb_bsn%m, pco%wb_bsn%y, pco%wb_bsn%a
read (107,*,iostat=eof) name, pco%nb_bsn%d, pco%nb_bsn%m, pco%nb_bsn%y, pco%nb_bsn%a
read (107,*,iostat=eof) name, pco%ls_bsn%d, pco%ls_bsn%m, pco%ls_bsn%y, pco%ls_bsn%a
read (107,*,iostat=eof) name, pco%pw_bsn%d, pco%pw_bsn%m, pco%pw_bsn%y, pco%pw_bsn%a
read (107,*,iostat=eof) name, pco%aqu_bsn%d, pco%aqu_bsn%m, pco%aqu_bsn%y, pco%aqu_bsn%a
read (107,*,iostat=eof) name, pco%res_bsn%d, pco%res_bsn%m, pco%res_bsn%y, pco%res_bsn%a
read (107,*,iostat=eof) name, pco%chan_bsn%d, pco%chan_bsn%m, pco%chan_bsn%y, pco%chan_bsn%a
read (107,*,iostat=eof) name, pco%sd_chan_bsn%d, pco%sd_chan_bsn%m, pco%sd_chan_bsn%y, pco%sd_chan_bsn%a
read (107,*,iostat=eof) name, pco%recall_bsn%d, pco%recall_bsn%m, pco%recall_bsn%y, pco%recall_bsn%a
read (107,*,iostat=eof) name, pco%wb_reg%d, pco%wb_reg%m, pco%wb_reg%y, pco%wb_reg%a
read (107,*,iostat=eof) name, pco%nb_reg%d, pco%nb_reg%m, pco%nb_reg%y, pco%nb_reg%a
read (107,*,iostat=eof) name, pco%ls_reg%d, pco%ls_reg%m, pco%ls_reg%y, pco%ls_reg%a
read (107,*,iostat=eof) name, pco%pw_reg%d, pco%pw_reg%m, pco%pw_reg%y, pco%pw_reg%a
read (107,*,iostat=eof) name, pco%aqu_reg%d, pco%aqu_reg%m, pco%aqu_reg%y, pco%aqu_reg%a
read (107,*,iostat=eof) name, pco%res_reg%d, pco%res_reg%m, pco%res_reg%y, pco%res_reg%a
read (107,*,iostat=eof) name, pco%sd_chan_reg%d, pco%sd_chan_reg%m, pco%sd_chan_reg%y, pco%sd_chan_reg%a
read (107,*,iostat=eof) name, pco%recall_reg%d, pco%recall_reg%m, pco%recall_reg%y, pco%recall_reg%a
read (107,*,iostat=eof) name, pco%water_allo%d, pco%water_allo%m, pco%water_allo%y, pco%water_allo%a
read (107,*,iostat=eof) name, pco%wb_lsu%d, pco%wb_lsu%m, pco%wb_lsu%y, pco%wb_lsu%a
read (107,*,iostat=eof) name, pco%nb_lsu%d, pco%nb_lsu%m, pco%nb_lsu%y, pco%nb_lsu%a
read (107,*,iostat=eof) name, pco%ls_lsu%d, pco%ls_lsu%m, pco%ls_lsu%y, pco%ls_lsu%a
read (107,*,iostat=eof) name, pco%pw_lsu%d, pco%pw_lsu%m, pco%pw_lsu%y, pco%pw_lsu%a
read (107,*,iostat=eof) name, pco%wb_hru%d, pco%wb_hru%m, pco%wb_hru%y, pco%wb_hru%a
read (107,*,iostat=eof) name, pco%nb_hru%d, pco%nb_hru%m, pco%nb_hru%y, pco%nb_hru%a
read (107,*,iostat=eof) name, pco%ls_hru%d, pco%ls_hru%m, pco%ls_hru%y, pco%ls_hru%a
read (107,*,iostat=eof) name, pco%pw_hru%d, pco%pw_hru%m, pco%pw_hru%y, pco%pw_hru%a
read (107,*,iostat=eof) name, pco%wb_sd%d, pco%wb_sd%m, pco%wb_sd%y, pco%wb_sd%a
read (107,*,iostat=eof) name, pco%nb_sd%d, pco%nb_sd%m, pco%nb_sd%y, pco%nb_sd%a
read (107,*,iostat=eof) name, pco%ls_sd%d, pco%ls_sd%m, pco%ls_sd%y, pco%ls_sd%a
read (107,*,iostat=eof) name, pco%pw_sd%d, pco%pw_sd%m, pco%pw_sd%y, pco%pw_sd%a
read (107,*,iostat=eof) name, pco%chan%d, pco%chan%m, pco%chan%y, pco%chan%a
read (107,*,iostat=eof) name, pco%sd_chan%d, pco%sd_chan%m, pco%sd_chan%y, pco%sd_chan%a
read (107,*,iostat=eof) name, pco%aqu%d, pco%aqu%m, pco%aqu%y, pco%aqu%a
read (107,*,iostat=eof) name, pco%res%d, pco%res%m, pco%res%y, pco%res%a
read (107,*,iostat=eof) name, pco%recall%d, pco%recall%m, pco%recall%y, pco%recall%a
read (107,*,iostat=eof) name, pco%hyd%d, pco%hyd%m, pco%hyd%y, pco%hyd%a
read (107,*,iostat=eof) name, pco%ru%d, pco%ru%m, pco%ru%y, pco%ru%a
read (107,*,iostat=eof) name, pco%pest%d, pco%pest%m, pco%pest%y, pco%pest%a
read (107,*,iostat=eof) name, pco%salt_basin%d, pco%salt_basin%m, pco%salt_basin%y, pco%salt_basin%a
read (107,*,iostat=eof) name, pco%salt_hru%d, pco%salt_hru%m, pco%salt_hru%y, pco%salt_hru%a
read (107,*,iostat=eof) name, pco%salt_ru%d, pco%salt_ru%m, pco%salt_ru%y, pco%salt_ru%a
read (107,*,iostat=eof) name, pco%salt_aqu%d, pco%salt_aqu%m, pco%salt_aqu%y, pco%salt_aqu%a
read (107,*,iostat=eof) name, pco%salt_chn%d, pco%salt_chn%m, pco%salt_chn%y, pco%salt_chn%a
read (107,*,iostat=eof) name, pco%salt_res%d, pco%salt_res%m, pco%salt_res%y, pco%salt_res%a
read (107,*,iostat=eof) name, pco%salt_wet%d, pco%salt_wet%m, pco%salt_wet%y, pco%salt_wet%a
read (107,*,iostat=eof) name, pco%cs_basin%d, pco%cs_basin%m, pco%cs_basin%y, pco%cs_basin%a
read (107,*,iostat=eof) name, pco%cs_hru%d, pco%cs_hru%m, pco%cs_hru%y, pco%cs_hru%a
read (107,*,iostat=eof) name, pco%cs_ru%d, pco%cs_ru%m, pco%cs_ru%y, pco%cs_ru%a
read (107,*,iostat=eof) name, pco%cs_aqu%d, pco%cs_aqu%m, pco%cs_aqu%y, pco%cs_aqu%a
read (107,*,iostat=eof) name, pco%cs_chn%d, pco%cs_chn%m, pco%cs_chn%y, pco%cs_chn%a
read (107,*,iostat=eof) name, pco%cs_res%d, pco%cs_res%m, pco%cs_res%y, pco%cs_res%a
read (107,*,iostat=eof) name, pco%cs_wet%d, pco%cs_wet%m, pco%cs_wet%y, pco%cs_wet%a
read (107,*,iostat=eof) name, pco%gwflow_wb%d, pco%gwflow_wb%m, pco%gwflow_wb%y, pco%gwflow_wb%a
read (107,*,iostat=eof) name, pco%gwflow_flux%d, pco%gwflow_flux%m, pco%gwflow_flux%y, pco%gwflow_flux%a
read (107,*,iostat=eof) name, pco%gwflow_heat%d, pco%gwflow_heat%m, pco%gwflow_heat%y, pco%gwflow_heat%a
read (107,*,iostat=eof) name, pco%gwflow_solute%d, pco%gwflow_solute%m, pco%gwflow_solute%y, pco%gwflow_solute%a
read (107,*,iostat=eof) name, pco%gwflow_obs%d, pco%gwflow_obs%m, pco%gwflow_obs%y, pco%gwflow_obs%a
read (107,*,iostat=eof) name, pco%gwflow_pump%d, pco%gwflow_pump%m, pco%gwflow_pump%y, pco%gwflow_pump%a
```

## I/O Operations

| Direction | Op | Unit | Statement |
| --- | --- | --- | --- |
| File setup | `open` | 107 | `open (107,file=in_sim%prt)` |
| Input | `read` | 107 | `read (107,*,iostat=eof) titldum` |
| Input | `read` | 107 | `read (107,*,iostat=eof) header` |
| Input | `read` | 107 | `read (107,*,iostat=eof) pco%nyskip, pco%day_start, pco%yrc_start, pco%day_end, pco%yrc_end, pco%int_day` |
| Input | `read` | 107 | `read (107,*,iostat=eof) header` |
| Input | `read` | 107 | `read (107,*,iostat=eof) pco%aa_numint` |
| File control | `backspace` | 107 | `backspace (107)` |
| Input | `read` | 107 | `read (107,*,iostat=eof) pco%aa_numint, (pco%aa_yrs(ii), ii = 1, pco%aa_numint)` |
| Input | `read` | 107 | `read (107,*,iostat=eof) header` |
| Input | `read` | 107 | `read (107,*,iostat=eof) pco%csvout, pco%use_obj_labels, pco%cdfout` |
| Input | `read` | 107 | `read (107,*,iostat=eof) header` |
| Input | `read` | 107 | `read (107,*,iostat=eof) pco%crop_yld, pco%mgtout, pco%hydcon, pco%fdcout` |

## Readers

| Procedure | Operations | Role |
| --- | --- | --- |
| [sym:basin_print_codes_read] | backspace, close, open, read | Reads the `print.prt` file at model initialization, parses output control settings, and populates the `pco(:)` array of type `basin_print_codes` with all print/output options for the simulation. |

## Review Notes

- Some fields in `basin_print_codes` (e.g., day_print, day_print_over) are present in the type but not actively used in the current reader logic. The file is required for custom output control; if missing, defaults are set in code after reading. The sample read format is illustrative; actual files may vary in object order and presence depending on use_obj_labels and model setup.
