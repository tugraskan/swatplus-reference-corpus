---
kind: io
source_symbols:
- readcio_read
title: '`file.cio`'
status: filled
source_hash: 83eb83bdd567cb07
version_label: SWAT+ 62.0.0
---

**Primary target:** the `in_*` filename registries in `input_file_module` (e.g. `in_sim`, `in_cha`, `in_aqu`, ...)  
**Read by:** [sym:readcio_read]

## Bottom Line

`file.cio` is the master control file that names every other SWAT+ input file. Each line is a category label followed by the filenames for that group, which the reader stores into the matching `in_*` registry in `input_file_module`.

The reader `readcio_read` reads a title line, then reads one line per input category into `in_sim`, `in_basin`, `in_cli`, ... `in_regs`, five weather directory-path lines, and a final output-path line. Every other reader later resolves its filename from these registries.

The file is required: if `file.cio` does not exist the model has no input-file map. A filename of `null` in any slot tells the corresponding reader to skip that file.

| Module | Role for this file |
| --- | --- |
| [sym:input_file_module] | Defines the `in_*` filename registries (`in_sim`, `in_basin`, ...); each `file.cio` line is read into one registry so downstream readers can resolve their filenames. |
| [sym:output_path_module] | Provides `init_output_path`; the final line's path is normalized and stored for output writers. |

## File Variables

`file.cio` has one title line followed by one line per input category. Each line starts with a label and lists the filenames for that group, read as a whole `input_*` record into the matching `in_*` registry. The table below shows each line, the registry it fills, and the default files it carries. The last five category lines are measured-weather directory paths, and the final line is the output directory path.

| Col | Header | Target | Type | Units | Meaning |
| --- | --- | --- | --- | --- | --- |
| 1 | `simulation` | `in_sim` |  |  | simulation control and constituent files — default files: `time.sim`, `print.prt`, `object.prt`, `object.cnt`, `constituents.cs` |
| 2 | `basin` | `in_basin` |  |  | basin codes and parameters — default files: `codes.bsn`, `parameters.bsn`, `carbon.bsn` |
| 3 | `climate` | `in_cli` |  |  | weather stations, generators, and measured-weather registries — default files: `weather-sta.cli`, `weather-wgn.cli`, `pet.cli`, `pcp.cli`, `tmp.cli`, `slr.cli`, `hmd.cli`, `wnd.cli`, `atmodep.cli` |
| 4 | `connect` | `in_con` |  |  | spatial-object connectivity files — default files: `hru.con`, `hru-lte.con`, `rout_unit.con`, `gwflow.con`, `aquifer.con`, `aquifer2d.con`, `channel.con`, `reservoir.con`, `recall.con`, `exco.con`, `delratio.con`, `outlet.con`, `chandeg.con` |
| 5 | `channel` | `in_cha` |  |  | channel definition and process files — default files: `initial.cha`, `channel.cha`, `hydrology.cha`, `sediment.cha`, `nutrients.cha`, `channel-lte.cha`, `hyd-sed-lte.cha`, `temperature.cha` |
| 6 | `reservoir` | `in_res` |  |  | reservoir definition and process files — default files: `initial.res`, `reservoir.res`, `hydrology.res`, `sediment.res`, `nutrients.res`, `weir.res`, `wetland.wet`, `hydrology.wet` |
| 7 | `routing_unit` | `in_ru` |  |  | routing-unit definition, elements, and delivery — default files: `rout_unit.def`, `rout_unit.ele`, `rout_unit.rtu`, `rout_unit.dr` |
| 8 | `hru` | `in_hru` |  |  | HRU data files — default files: `hru-data.hru`, `hru-lte.hru` |
| 9 | `exco` | `in_exco` |  |  | export-coefficient object files — default files: `exco.exc`, `exco_om.exc`, `exco_pest.exc`, `exco_path.exc`, `exco_hmet.exc`, `exco_salt.exc` |
| 10 | `recall` | `in_rec` |  |  | recall (point-source/time-series) file — default files: `recall.rec` |
| 11 | `delratio` | `in_delr` |  |  | delivery-ratio object files — default files: `delratio.del`, `dr_om.del`, `dr_pest.del`, `dr_path.del`, `dr_hmet.del`, `dr_salt.del` |
| 12 | `aquifer` | `in_aqu` |  |  | aquifer definition and initial-condition files — default files: `initial.aqu`, `aquifer.aqu` |
| 13 | `herd` | `in_herd` |  |  | animal/herd/ranch files — default files: `animal.hrd`, `herd.hrd`, `ranch.hrd` |
| 14 | `water_rights` | `in_watrts` |  |  | water-allocation and water-rights files — default files: `water_allocation.wro`, `element.wro`, `water_rights.wro` |
| 15 | `link` | `in_link` |  |  | channel-surface and aquifer-channel link files — default files: `chan-surf.lin`, `aqu_cha.lin` |
| 16 | `hydrology` | `in_hyd` |  |  | hydrology, topography, and field files — default files: `hydrology.hyd`, `topography.hyd`, `field.fld` |
| 17 | `structural` | `in_str` |  |  | structural-practice (BMP) files — default files: `tiledrain.str`, `septic.str`, `filterstrip.str`, `grassedww.str`, `bmpuser.str` |
| 18 | `parm_db` | `in_parmdb` |  |  | parameter databases (plants, fertilizer, tillage, pesticide, ...) — default files: `plants.plt`, `fertilizer.frt`, `tillage.til`, `pesticide.pes`, `pathogens.pth`, `metals.mtl`, `salt.slt`, `urban.urb`, `septic.sep`, `snow.sno` |
| 19 | `ops` | `in_ops` |  |  | management operation files — default files: `harv.ops`, `graze.ops`, `irr.ops`, `chem_app.ops`, `fire.ops`, `sweep.ops` |
| 20 | `lum` | `in_lum` |  |  | land-use management and schedule files — default files: `landuse.lum`, `management.sch`, `cntable.lum`, `cons_practice.lum`, `ovn_table.lum` |
| 21 | `chg` | `in_chg` |  |  | calibration parameter and soft-calibration files — default files: `cal_parms.cal`, `calibration.cal`, `codes.sft`, `wb_parms.sft`, `water_balance.sft`, `ch_sed_budget.sft`, `ch_sed_parms.sft`, `plant_parms.sft`, `plant_gro.sft` |
| 22 | `init` | `in_init` |  |  | initial-condition files — default files: `plant.ini`, `soil_plant.ini`, `om_water.ini`, `pest_hru.ini`, `pest_water.ini`, `path_hru.ini`, `path_water.ini`, `hmet_hru.ini`, `hmet_water.ini`, `salt_hru.ini`, `salt_water.ini` |
| 23 | `soils` | `in_sol` |  |  | soil database files — default files: `soils.sol`, `nutrients.sol`, `soils_lte.sol` |
| 24 | `decision_table` | `in_cond` |  |  | decision-table (conditional) files — default files: `lum.dtl`, `res_rel.dtl`, `scen_lu.dtl`, `flo_con.dtl` |
| 25 | `regions` | `in_regs` |  |  | landscape-unit and region definition/element files — default files: `ls_unit.ele`, `ls_unit.def`, `ls_reg.ele`, `ls_reg.def`, `ls_cal.reg`, `ch_catunit.ele`, `ch_catunit.def`, `ch_reg.def`, `aqu_catunit.ele`, `aqu_catunit.def`, `aqu_reg.def`, `res_catunit.ele`, `res_catunit.def`, `res_reg.def`, `rec_catunit.ele`, `rec_catunit.def`, `rec_reg.def` |
| 26 | `path_pcp` | `in_path_pcp` |  |  | directory path for measured precipitation files (weather directory path; no file list) |
| 27 | `path_tmp` | `in_path_tmp` |  |  | directory path for measured temperature files (weather directory path; no file list) |
| 28 | `path_slr` | `in_path_slr` |  |  | directory path for measured solar-radiation files (weather directory path; no file list) |
| 29 | `path_hmd` | `in_path_hmd` |  |  | directory path for measured humidity files (weather directory path; no file list) |
| 30 | `path_wnd` | `in_path_wnd` |  |  | directory path for measured wind files (weather directory path; no file list) |
| 31 | `output_path` | `out_path_value` | character(len=256) |  | output directory path; parsed from the line label and passed to `init_output_path` (blank/null uses the current directory) |

## Sample

```text
Schematic (label + filenames per line; default file names shown):

<title line>
simulation      time.sim  print.prt  object.prt  object.cnt  constituents.cs
basin           codes.bsn  parameters.bsn  carbon.bsn
climate         weather-sta.cli  weather-wgn.cli  pet.cli  pcp.cli  tmp.cli  slr.cli ...
...
channel         initial.cha  channel.cha  hydrology.cha  sediment.cha  nutrients.cha  channel-lte.cha ...
...
path_pcp        <precip directory path>
output_path     <output directory path>
```

## Read Pattern

```fortran
open (107,file="file.cio")
read (107,*) titldum
read (107,*,iostat=eof) name, in_sim
read (107,*,iostat=eof) name, in_basin
read (107,*,iostat=eof) name, in_cli
read (107,*,iostat=eof) name, in_con
read (107,*,iostat=eof) name, in_cha
read (107,*,iostat=eof) name, in_res
read (107,*,iostat=eof) name, in_ru
read (107,*,iostat=eof) name, in_hru
read (107,*,iostat=eof) name, in_exco
read (107,*,iostat=eof) name, in_rec
read (107,*,iostat=eof) name, in_delr
read (107,*,iostat=eof) name, in_aqu
read (107,*,iostat=eof) name, in_herd
read (107,*,iostat=eof) name, in_watrts
read (107,*,iostat=eof) name, in_link
read (107,*,iostat=eof) name, in_hyd
read (107,*,iostat=eof) name, in_str
read (107,*,iostat=eof) name, in_parmdb
read (107,*,iostat=eof) name, in_ops
read (107,*,iostat=eof) name, in_lum
read (107,*,iostat=eof) name, in_chg
read (107,*,iostat=eof) name, in_init
read (107,*,iostat=eof) name, in_sol
read (107,*,iostat=eof) name, in_cond
read (107,*,iostat=eof) name, in_regs
read (107,*,iostat=eof) name, in_path_pcp
read (107,*,iostat=eof) name, in_path_tmp
read (107,*,iostat=eof) name, in_path_slr
read (107,*,iostat=eof) name, in_path_hmd
read (107,*,iostat=eof) name, in_path_wnd
read (107,'(A)',iostat=eof) line_buffer
```

## I/O Operations

| Direction | Op | Unit | Statement |
| --- | --- | --- | --- |
| File setup | `open` | 107 | `open (107,file="file.cio")` |
| Input | `read` | 107 | `read (107,*) titldum` |
| Input | `read` | 107 | `read (107,*,iostat=eof) name, in_sim` |
| Input | `read` | 107 | `read (107,*,iostat=eof) name, in_basin` |
| Input | `read` | 107 | `read (107,*,iostat=eof) name, in_cli` |
| Input | `read` | 107 | `read (107,*,iostat=eof) name, in_con` |
| Input | `read` | 107 | `read (107,*,iostat=eof) name, in_cha` |
| Input | `read` | 107 | `read (107,*,iostat=eof) name, in_res` |
| Input | `read` | 107 | `read (107,*,iostat=eof) name, in_ru` |
| Input | `read` | 107 | `read (107,*,iostat=eof) name, in_hru` |
| Input | `read` | 107 | `read (107,*,iostat=eof) name, in_exco` |
| Input | `read` | 107 | `read (107,*,iostat=eof) name, in_rec` |
| Input | `read` | 107 | `read (107,*,iostat=eof) name, in_delr` |
| Input | `read` | 107 | `read (107,*,iostat=eof) name, in_aqu` |
| Input | `read` | 107 | `read (107,*,iostat=eof) name, in_herd` |
| Input | `read` | 107 | `read (107,*,iostat=eof) name, in_watrts` |
| Input | `read` | 107 | `read (107,*,iostat=eof) name, in_link` |
| Input | `read` | 107 | `read (107,*,iostat=eof) name, in_hyd` |
| Input | `read` | 107 | `read (107,*,iostat=eof) name, in_str` |
| Input | `read` | 107 | `read (107,*,iostat=eof) name, in_parmdb` |
| Input | `read` | 107 | `read (107,*,iostat=eof) name, in_ops` |
| Input | `read` | 107 | `read (107,*,iostat=eof) name, in_lum` |
| Input | `read` | 107 | `read (107,*,iostat=eof) name, in_chg` |
| Input | `read` | 107 | `read (107,*,iostat=eof) name, in_init` |
| Input | `read` | 107 | `read (107,*,iostat=eof) name, in_sol` |
| Input | `read` | 107 | `read (107,*,iostat=eof) name, in_cond` |
| Input | `read` | 107 | `read (107,*,iostat=eof) name, in_regs` |
| Input | `read` | 107 | `read (107,*,iostat=eof) name, in_path_pcp` |
| Input | `read` | 107 | `read (107,*,iostat=eof) name, in_path_tmp` |
| Input | `read` | 107 | `read (107,*,iostat=eof) name, in_path_slr` |
| Input | `read` | 107 | `read (107,*,iostat=eof) name, in_path_hmd` |
| Input | `read` | 107 | `read (107,*,iostat=eof) name, in_path_wnd` |
| Input | `read` | 107 | `read (107,'(A)',iostat=eof) line_buffer` |
| File control | `close` | 107 | `close (107)` |

## Readers

| Procedure | Operations | Role |
| --- | --- | --- |
| [sym:readcio_read] | open, read | Opens `file.cio`, reads the title line, then reads each category line into its `in_*` registry (`in_sim` ... `in_regs`), five measured-weather directory-path lines, and a final output-path line which it hands to `init_output_path`. |

## Review Notes

- Each category line is read as a whole `input_*` record, so a line holds all filenames for that group in a fixed order; the leading label token is read into a throwaway `name`.
- The five `in_path_*` lines are measured-weather directory paths, not files; they carry no default filenames.
- The output-path line is read with a full-line read (not list-directed) to preserve spaces and avoid `/` terminating the value, then parsed after the label.
- A slot set to `null` signals the corresponding reader to skip that file.
- The read loop is wrapped in `do i = 1, 31`, but a single pass reads all categories and then exits.
