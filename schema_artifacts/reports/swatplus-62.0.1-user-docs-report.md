# User documentation vs SWAT+ 62.0.1 input files

- Source: `release_62_0_1` @ `97ca231e22b29356b9891e057238fa3c68809da5`
- Docs: `SWATPlus-user-documentation` @ `a6730da20b8eaad18c92e4a15c6a0885c2e41c06`
- Editor column names: `swatplus-62.0.0-field-map.json`
- Example file headers: `refdata/` (Ames_sub1, Osu_1hru) @ `97ca231e22b2`

Checks page coverage, field names and order, types, and field links. A file without its own page is compared with a shared table when a section page lists it and points to one (the `*.con` files share `'object'.con`). *Named only* means the docs name the file (usually in the `file.cio` list) but no page describes it; *no page* means it is not mentioned at all. Units, ranges, defaults, and descriptions are not compared. Non-flat layouts are checked for a page only. *Names to check* means the only difference is a field name that matches neither the Fortran variable, a known Editor column, nor an example file's header at that position; the docs may well be right.

## Summary

| Status | Files |
| --- | --- |
| match | 30 |
| differs | 19 |
| names_to_check | 20 |
| no_field_table | 3 |
| named_only | 44 |
| no_page | 67 |
| not_compared | 15 |
| **total input files read by 62.0.1** | 198 |

- Tables with broken field links: 0
- Docs pages for files not in the 62.0.1 input schema: 12

## Tables that differ from the source (19)

- **`aquifer.con`**: `io-docs/introduction-1/connectivity/hru.con/README.md` (shared table, listed on `io-docs/introduction-1/connectivity/README.md`): 17 docs rows, 17 source fields (repeating group)
  - position 8: docs `hru`, source `props`
  - type of `rule`: docs integer, source character
- **`chandeg.con`**: `io-docs/introduction-1/connectivity/hru.con/README.md` (shared table, listed on `io-docs/introduction-1/connectivity/README.md`): 17 docs rows, 17 source fields (repeating group)
  - position 8: docs `hru`, source `props`
  - type of `rule`: docs integer, source character
- **`codes.bsn`**: `io-docs/introduction-1/basin-1/codes.bsn/README.md`: 25 docs rows, 26 source fields
  - missing from docs: `idc_till`
- **`delratio.con`**: `io-docs/introduction-1/connectivity/hru.con/README.md` (shared table, listed on `io-docs/introduction-1/connectivity/README.md`): 17 docs rows, 17 source fields (repeating group)
  - position 8: docs `hru`, source `props`
  - type of `rule`: docs integer, source character
- **`exco.con`**: `io-docs/introduction-1/connectivity/hru.con/README.md` (shared table, listed on `io-docs/introduction-1/connectivity/README.md`): 17 docs rows, 17 source fields (repeating group)
  - position 8: docs `hru`, source `exco (props)`
  - type of `rule`: docs integer, source character
- **`hru-lte.con`**: `io-docs/introduction-1/connectivity/hru.con/README.md` (shared table, listed on `io-docs/introduction-1/connectivity/README.md`): 17 docs rows, 17 source fields (repeating group)
  - position 8: docs `hru`, source `props`
  - type of `rule`: docs integer, source character
- **`hru.con`**: `io-docs/introduction-1/connectivity/hru.con/README.md`: 17 docs rows, 17 source fields (repeating group)
  - type of `rule`: docs integer, source character
  - names confirmed by an example file header: `hru` (source `props`)
- **`hyd-sed-lte.cha`**: `io-docs/introduction-1/channels/hyd-sed-lte.cha/README.md`: 22 docs rows, 23 source fields
  - missing from docs: `order`, `bankfull_flo`
  - not read by the source: `bed_load`
- **`ls_unit.def`**: `io-docs/introduction-1/landscape-units/ls_unit.def/README.md`: 4 docs rows, 5 source fields (repeating group)
  - missing from docs: `area (area_ha)`, `elem_cnt`
  - not read by the source: `elements`
- **`nutrients.cha`**: `io-docs/introduction-1/channels/nutrients.cha/README.md`: 39 docs rows, 39 source fields
  - position 3: docs `plt_p`, source `ptl_p (opco)`
  - position 13: docs `cbn_bod___stl`, source `cbn_bod_stl (rk3)`
  - type of `q2e_lt`: docs integer, source real
- **`pesticide.pes`**: `io-docs/introduction-1/databases/pesticide.pes/README.md`: 14 docs rows, 18 source fields
  - missing from docs: `pl_uptake`, `harvest_sink`, `resistance_n`, `descrip`
  - position 7: docs `aq_reac`, source `aq_hlife`
  - position 14: docs `ben_reac`, source `ben_hlife`
  - names confirmed by an example file header: `soil_ads` (source `koc`), `frac_wash` (source `washoff`), `hl_foliage` (source `foliar_hlife`), `hl_soil` (source `soil_hlife`)
- **`plants.plt`**: `io-docs/introduction-1/databases/plants.plt/README.md`: 53 docs rows, 57 source fields
  - missing from docs: `meta_frac`, `str_frac`, `lig_frac`, `pl_class`
  - type of `days_mat`: docs real, source integer
  - names confirmed by an example file header: `gro_trig` (source `trig`)
- **`print.prt`**: `io-docs/introduction-1/simulation-settings/print.prt/README.md`: 19 docs rows, 6 source fields
  - not read by the source: `aa_int_cnt`, `csvout`, `dbout`, `cdfout`, `crop_yld`, `mgtout`, `hydcon`, `fdcout`, `object`, `daily`, `monthly`, `yearly`, `avann`
- **`recall_db.rec`**: `io-docs/introduction-1/point-sources-and-inlets/recall.rec/README.md`: 20 docs rows, 9 source fields
  - not read by the source: `path_unit`, `path_tstep`, `hmet_name`, `hmet_unit`, `hmet_tstep`, `salt_name`, `salt_unit`, `salt_tstep`, `cst_name`, `cst_unit`, `cst_tstep`
  - position 1: docs `id`, source `k`
  - position 3: docs `om_name`, source `org_min`
  - position 4: docs `om_unit`, source `pest`
  - position 5: docs `om_tstep`, source `path`
  - position 6: docs `pest_name`, source `hmet`
  - position 7: docs `pest_unit`, source `salt`
  - position 8: docs `pest_tstep`, source `constit`
  - position 9: docs `path_name`, source `descrip`
- **`reservoir.con`**: `io-docs/introduction-1/connectivity/hru.con/README.md` (shared table, listed on `io-docs/introduction-1/connectivity/README.md`): 17 docs rows, 17 source fields (repeating group)
  - position 8: docs `hru`, source `props`
  - type of `rule`: docs integer, source character
- **`rout_unit.con`**: `io-docs/introduction-1/connectivity/hru.con/README.md` (shared table, listed on `io-docs/introduction-1/connectivity/README.md`): 17 docs rows, 17 source fields (repeating group)
  - position 8: docs `hru`, source `props`
  - type of `rule`: docs integer, source character
- **`soil_plant.ini`**: `io-docs/introduction-1/initialization/soil_plant.ini/README.md`: 7 docs rows, 8 source fields
  - missing from docs: `csc`
  - out of order: `hmet`
  - names confirmed by an example file header: `nutrients` (source `nutc`)
- **`topography.hyd`**: `io-docs/introduction-1/hydrology/topography.hyd/README.md`: 6 docs rows, 6 source fields
  - type of `depos`: docs integer, source real
- **`weather-sta.cli`**: `io-docs/introduction-1/climate/weather-sta.cli/README.md`: 10 docs rows, 9 source fields
  - not read by the source: `wnd_dir`
  - out of order: `atmo_dep`

## Tables whose field names need a check (20)

- **`bmpuser.str`**: `io-docs/introduction-1/structural-practices/bmpuser.str/README.md`: 8 docs rows, 8 source fields
  - position 2: docs `flag_bmp`, source `flag (bmp_flag)`
- **`cal_parms.cal`**: `io-docs/introduction-1/calibration/cal_parms.cal.md`: 5 docs rows, 5 source fields
  - position 5: docs `unit`, source `units`
- **`channel-lte.cha`**: `io-docs/introduction-1/channels/channel-lte.cha/README.md`: 6 docs rows, 6 source fields
  - position 3: docs `ini`, source `cha_ini (initc)`
  - position 4: docs `hyd`, source `cha_hyd (hydc)`
  - position 5: docs `sed`, source `cha_sed (sedc)`
  - position 6: docs `nut`, source `cha_nut (nutc)`
- **`codes.sft`**: `io-docs/introduction-1/calibration/codes.sft.md`: 8 docs rows, 8 source fields
  - position 2: docs `hyd_hrulte`, source `hyd_hrul`
- **`filterstrip.str`**: `io-docs/introduction-1/structural-practices/filterstrip.str/README.md`: 5 docs rows, 5 source fields
  - position 2: docs `flag_fs`, source `flag (vfsi)`
- **`grassedww.str`**: `io-docs/introduction-1/structural-practices/grassedww.str/README.md`: 8 docs rows, 8 source fields
  - position 2: docs `flag_grww`, source `flag (grwat_i)`
- **`graze.ops`**: `io-docs/introduction-1/management-practices/graze.ops/README.md`: 6 docs rows, 6 source fields
  - position 2: docs `fertname`, source `fertnm`
- **`hru-lte.hru`**: `io-docs/introduction-1/hydrologic-response-units/hru-lte.hru/README.md`: 35 docs rows, 35 source fields
  - position 8: docs `perco_co`, source `perc_co (perco)`
  - position 20: docs `snow_h20`, source `snow_h2o (snow)`
- **`hydrology.hyd`**: `io-docs/introduction-1/hydrology/hydrology.hyd/README.md`: 15 docs rows, 15 source fields
  - position 2: docs `lat_time`, source `lat_ttime`
- **`irr.ops`**: `io-docs/introduction-1/management-practices/irr.ops/README.md`: 8 docs rows, 8 source fields
  - position 2: docs `irr_eff`, source `amt_mm`
  - position 3: docs `surq_rto`, source `eff_frac (eff)`
  - position 4: docs `irr_amt`, source `sumq_frac (surq)`
  - position 5: docs `irr_dep`, source `dep_mm`
  - position 6: docs `irr_salt`, source `salt`
  - position 7: docs `irr_no3n`, source `no3`
  - position 8: docs `irr_po4`, source `po4`
- **`landuse.lum`**: `io-docs/introduction-1/landuse-and-management/landuse.lum/README.md`: 14 docs rows, 14 source fields
  - position 2: docs `cal_grp`, source `cal_group`
- **`ls_unit.ele`**: `io-docs/introduction-1/landscape-units/ls_unit.ele/README.md`: 6 docs rows, 6 source fields
  - position 6: docs `lsu_frac`, source `ru_frac`
  - names confirmed by an example file header: `id` (source `k`)
- **`object.cnt`**: `io-docs/introduction-1/simulation-settings/object.cnt.md`: 21 docs rows, 21 source fields
  - position 8: docs `gwfl`, source `gwflow`
  - names confirmed by an example file header: `dlr` (source `dr`)
- **`object.prt`**: `io-docs/introduction-1/simulation-settings/object.prt/README.md`: 5 docs rows, 5 source fields
  - position 1: docs `id`, source `k`
  - position 2: docs `obj_typ`, source `obtyp`
  - position 3: docs `obj_typ_no`, source `obtypno`
  - position 4: docs `hyd_typ`, source `hydtyp`
- **`om_water.ini`**: `io-docs/introduction-1/initialization/om_water.ini/README.md`: 19 docs rows, 19 source fields
  - position 2: docs `vol`, source `flo`
  - position 4: docs `part_n`, source `orgn`
  - position 5: docs `part_p`, source `sedp`
  - position 13: docs `sand`, source `san`
  - position 14: docs `silt`, source `sil`
  - position 15: docs `clay`, source `cla`
  - position 16: docs `sm_ag`, source `sag`
  - position 17: docs `l_ag`, source `lag`
  - position 18: docs `gvl`, source `grv`
  - names confirmed by an example file header: `name` (source `om_init_name`)
- **`outlet.con`**: `io-docs/introduction-1/connectivity/hru.con/README.md` (shared table, listed on `io-docs/introduction-1/connectivity/README.md`): 17 docs rows, 17 source fields (repeating group)
  - position 1: docs `id`, source `num`
  - position 4: docs `area`, source `area_ha`
  - position 6: docs `lon`, source `long`
  - position 8: docs `hru`, source `props`
  - position 9: docs `wst`, source `wst_c`
  - position 10: docs `cst`, source `constit`
  - position 11: docs `ovfl`, source `props2`
  - position 12: docs `rule`, source `ruleset`
  - position 13: docs `out_tot`, source `src_tot`
  - position 14: docs `obj_typ`, source `obtyp_out`
  - position 15: docs `obj_id`, source `obtypno_out`
  - position 16: docs `hyd_typ`, source `htyp_out`
  - position 17: docs `frac`, source `frac_out`
- **`ovn_table.lum`**: `io-docs/introduction-1/landuse-and-management/ovn_table.lum/README.md`: 4 docs rows, 4 source fields
  - position 1: docs `name_ovn`, source `name`
- **`recall.con`**: `io-docs/introduction-1/connectivity/hru.con/README.md` (shared table, listed on `io-docs/introduction-1/connectivity/README.md`): 17 docs rows, 17 source fields (repeating group)
  - position 1: docs `id`, source `num`
  - position 4: docs `area`, source `area_ha`
  - position 6: docs `lon`, source `long`
  - position 8: docs `hru`, source `props`
  - position 10: docs `cst`, source `constit`
  - position 11: docs `ovfl`, source `props2`
  - position 12: docs `rule`, source `ruleset`
  - position 14: docs `obj_typ`, source `obtyp_out`
  - position 15: docs `obj_id`, source `obtypno_out`
  - position 16: docs `hyd_typ`, source `htyp_out`
  - position 17: docs `frac`, source `frac_out`
  - names confirmed by an example file header: `wst` (source `wst_c`), `out_tot` (source `src_tot`)
- **`septic.str`**: `io-docs/introduction-1/structural-practices/septic.str/README.md`: 28 docs rows, 28 source fields
  - position 17: docs `fecal_delay`, source `fecal_decay (fecal)`
- **`weir.res`**: `io-docs/introduction-1/reservoirs/weir.res/README.md`: 5 docs rows, 5 source fields
  - position 4: docs `width`, source `w`
  - position 5: docs `height`, source `h`
  - names confirmed by an example file header: `linear_c` (source `c`), `exp_k` (source `k`)

## Named in the docs, but no page describes them (44)

- `aqu_catunit.def`: named on `io-docs/introduction-1/master-file-file.cio.md`
- `aqu_catunit.ele`: named on `io-docs/introduction-1/master-file-file.cio.md`
- `aqu_reg.def`: named on `io-docs/introduction-1/master-file-file.cio.md`
- `ch_catunit.def`: named on `io-docs/introduction-1/master-file-file.cio.md`
- `ch_reg.def`: named on `io-docs/introduction-1/master-file-file.cio.md`
- `ch_sed_budget.sft`: named on `io-docs/introduction-1/master-file-file.cio.md` (marked *currently not used*)
- `ch_sed_parms.sft`: named on `io-docs/introduction-1/master-file-file.cio.md` (marked *currently not used*)
- `chan-surf.lin`: named on `io-docs/introduction-1/master-file-file.cio.md`
- `channel.cha`: named on `io-docs/introduction-1/master-file-file.cio.md` (marked *currently not used*)
- `channel.con`: named on `io-docs/introduction-1/master-file-file.cio.md` (marked *currently not used*)
- `dr_hmet.del`: named on `io-docs/introduction-1/master-file-file.cio.md` (marked *currently not used*)
- `dr_om.del`: named on `io-docs/introduction-1/master-file-file.cio.md` (marked *currently not used*)
- `dr_path.del`: named on `io-docs/introduction-1/master-file-file.cio.md` (marked *currently not used*)
- `dr_pest.del`: named on `io-docs/introduction-1/master-file-file.cio.md` (marked *currently not used*)
- `dr_salt.del`: named on `io-docs/introduction-1/master-file-file.cio.md` (marked *currently not used*)
- `exco.exc`: named on `io-docs/introduction-1/master-file-file.cio.md`
- `exco_hmet.exc`: named on `io-docs/introduction-1/master-file-file.cio.md` (marked *currently not used*)
- `exco_om.exc`: named on `io-docs/introduction-1/master-file-file.cio.md`
- `exco_path.exc`: named on `io-docs/introduction-1/master-file-file.cio.md` (marked *currently not used*)
- `exco_pest.exc`: named on `io-docs/introduction-1/master-file-file.cio.md` (marked *currently not used*)
- `exco_salt.exc`: named on `io-docs/introduction-1/master-file-file.cio.md` (marked *currently not used*)
- `flo_con.dtl`: named on `io-docs/introduction-1/decision-tables/README.md`, `io-docs/introduction-1/master-file-file.cio.md`
- `gwflow.con`: named on `io-docs/introduction-1/master-file-file.cio.md`
- `hmet_hru.ini`: named on `io-docs/introduction-1/initialization/pest_water.ini.md`, `io-docs/introduction-1/master-file-file.cio.md` (marked *currently not used*)
- `hydrology.cha`: named on `io-docs/introduction-1/master-file-file.cio.md` (marked *currently not used*)
- `ls_reg.def`: named on `io-docs/introduction-1/master-file-file.cio.md`
- `ls_reg.ele`: named on `io-docs/introduction-1/master-file-file.cio.md`
- `path_hru.ini`: named on `io-docs/introduction-1/initialization/pest_water.ini.md`, `io-docs/introduction-1/master-file-file.cio.md` (marked *currently not used*)
- `path_water.ini`: named on `io-docs/introduction-1/master-file-file.cio.md` (marked *currently not used*)
- `pathogens.pth`: named on `io-docs/introduction-1/master-file-file.cio.md` (marked *currently not used*)
- `pet.cli`: named on `io-docs/introduction-1/climate/weather-sta.cli/pet.md`
- `plant_gro.sft`: named on `io-docs/introduction-1/master-file-file.cio.md`
- `plant_parms.sft`: named on `io-docs/introduction-1/master-file-file.cio.md`
- `rec_catunit.def`: named on `io-docs/introduction-1/master-file-file.cio.md`
- `rec_catunit.ele`: named on `io-docs/introduction-1/master-file-file.cio.md`
- `rec_reg.def`: named on `io-docs/introduction-1/master-file-file.cio.md`
- `res_catunit.def`: named on `io-docs/introduction-1/master-file-file.cio.md`
- `res_catunit.ele`: named on `io-docs/introduction-1/master-file-file.cio.md`
- `res_reg.def`: named on `io-docs/introduction-1/master-file-file.cio.md`
- `res_rel.dtl`: named on `io-docs/introduction-1/decision-tables/README.md`, `io-docs/introduction-1/master-file-file.cio.md`, `io-docs/introduction-1/reservoirs/README.md`
- `scen_lu.dtl`: named on `io-docs/introduction-1/decision-tables/README.md`, `io-docs/introduction-1/master-file-file.cio.md`
- `sediment.cha`: named on `io-docs/introduction-1/master-file-file.cio.md` (marked *currently not used*)
- `soils_lte.sol`: named on `io-docs/introduction-1/master-file-file.cio.md` (marked *currently not used*)
- `temperature.cha`: named on `io-docs/introduction-1/master-file-file.cio.md`

## Input files not mentioned anywhere in the docs (67)

- `atmodep.cli` (runtime arity)
- `carbon.bsn` (flat)
- `cell_sol.gw` (runtime arity)
- `cells.gw` (flat)
- `chancell.gw` (flat)
- `co2_yr.dat` (flat)
- `cs_aqu.ini` (runtime arity)
- `cs_atmo.cli` (runtime arity)
- `cs_channel.ini` (runtime arity)
- `cs_hru.ini` (runtime arity)
- `cs_recall.rec` (runtime arity)
- `delratio.del` (flat)
- `element.ccu` (flat)
- `fertilizer.frt_cs` (flat)
- `floodplain.gw` (flat)
- `gwflow.wetland` (flat)
- `gwflow_canal.con` (runtime arity)
- `hrucell.gw` (flat)
- `initial.aqu_cs` (flat)
- `initial.cha_cs` (flat)
- `lsucell.gw` (flat)
- `manure.frt` (unresolved)
- `manure_allo.mnu` (flat)
- `manure_db.frt` (flat)
- `manure_om.frt` (flat)
- `minerals.gw` (runtime arity)
- `nutrients.rte` (flat)
- `om_osrc.wal` (flat)
- `om_treat.wal` (flat)
- `om_use.wal` (flat)
- `outputs.gw` (flat)
- `outside_rcv.wal` (flat)
- `outside_src.wal` (runtime arity)
- `pest.com` (flat)
- `phreato.gw` (flat)
- `phreato_cell.gw` (flat)
- `place_of_use.wro` (multi record)
- `point_of_diver.wro` (flat)
- `pond_cell.gw` (flat)
- `ponds.gw` (runtime arity)
- `puddle.ops` (flat)
- `pumpex.gw` (flat)
- `res_conds.dat` (flat)
- `rescell.gw` (flat)
- `reservoir.res_cs` (flat)
- `salt_aqu.ini` (flat)
- `salt_atmo.cli` (runtime arity)
- `salt_channel.ini` (runtime arity)
- `salt_fertilizer.frt` (flat)
- `salt_recall.rec` (runtime arity)
- `satbuffer.str` (flat)
- `scen_dtl.upd` (flat)
- `sed_nut.cha` (flat)
- `shade_factor.shf` (flat)
- `solute.gw` (flat)
- `tile.gw` (flat)
- `transplant.ops` (flat)
- `tvheads.gw` (runtime arity)
- `water_canal.wal` (runtime arity)
- `water_hru_irr.wal` (multi record)
- `water_pipe.wal` (runtime arity)
- `water_tower.wal` (flat)
- `water_treat.wal` (runtime arity)
- `water_use.wal` (runtime arity)
- `wetland.wet_cs` (flat)
- `wtps_wuses.wal` (multi section)
- `zones.gw` (flat)

## Pages without a Field table (3)

- `aqu_cha.lin`: `io-docs/introduction-1/connectivity/aqu_cha.lin.md`
- `water_balance.sft`: `io-docs/introduction-1/calibration/water_balance.sft.md`
- `wb_parms.sft`: `io-docs/introduction-1/calibration/wb_parms.sft.md`

## Pages not compared (non-flat layout) (15)

- `calibration.cal` (multi record): `io-docs/introduction-1/calibration/calibration.cal.md`
- `constituents.cs` (multi section): `io-docs/introduction-1/constituents/constituents.cs.md`
- `hmd.cli` (multi section): `io-docs/introduction-1/climate/hmd.cli-and-humidity-data-files.md`
- `lum.dtl` (decision tables): `io-docs/introduction-1/decision-tables/lum.dtl/README.md`
- `management.sch` (multi record): `io-docs/introduction-1/landuse-and-management/management.sch/README.md`
- `pcp.cli` (multi section): `io-docs/introduction-1/climate/pcp.cli-and-precipitation-data-files.md`
- `pest_hru.ini` (runtime arity): `io-docs/introduction-1/initialization/pest_hru.ini.md`
- `pest_water.ini` (runtime arity): `io-docs/introduction-1/initialization/pest_water.ini.md`
- `plant.ini` (multi record): `io-docs/introduction-1/landuse-and-management/plant.ini/README.md`
- `salt_hru.ini` (runtime arity): `io-docs/introduction-1/initialization/salt_hru.ini.md`
- `slr.cli` (multi section): `io-docs/introduction-1/climate/slr.cli-and-solar-radiation-data-files.md`
- `soils.sol` (multi record): `io-docs/introduction-1/soils/soils.sol/README.md`
- `tmp.cli` (multi section): `io-docs/introduction-1/climate/tmp.cli-and-temperature-data-files.md`
- `weather-wgn.cli` (multi record): `io-docs/introduction-1/climate/weather-wgn.cli/README.md`
- `wnd.cli` (multi section): `io-docs/introduction-1/climate/wnd.cli-and-wind-speed-data-files.md`

## Tables that match (30)

- `aquifer.aqu`
- `chem_app.ops`
- `cntable.lum`
- `cons_practice.lum`
- `fertilizer.frt`
- `field.fld`
- `fire.ops`
- `harv.ops`
- `hru-data.hru`
- `hydrology.res`
- `hydrology.wet`
- `initial.aqu`
- `initial.cha`
- `initial.res`
- `nutrients.res`
- `nutrients.sol`
- `parameters.bsn`
- `reservoir.res`
- `rout_unit.def`
- `rout_unit.ele`
- `rout_unit.rtu`
- `sediment.res`
- `septic.sep`
- `snow.sno`
- `sweep.ops`
- `tiledrain.str`
- `tillage.til`
- `time.sim`
- `urban.urb`
- `wetland.wet`

## Docs pages for files not in the 62.0.1 input schema

Renamed or removed files, user-named files, or files the schema does not model (such as `file.cio`).

- `io-docs/introduction-1/carbon/carb_coefs.cbn.md` (names `carb_coefs.cbn`)
- `io-docs/introduction-1/climate/atmo.cli/README.md` (names `atmo.cli`)
- `io-docs/introduction-1/connectivity/chan_surf.lin.md` (names `chan_surf.lin`; near-identical input file: `chan-surf.lin`)
- `io-docs/introduction-1/initialization/salt_water.ini.md` (names `salt_water.ini`)
- `io-docs/introduction-1/master-file-file.cio.md` (names `file.cio, master-file-file.cio`)
- `io-docs/introduction-1/point-sources-and-inlets/cst_filename.rec.md` (names `cst_filename.rec`)
- `io-docs/introduction-1/point-sources-and-inlets/filename.rec.md` (names `filename.rec`)
- `io-docs/introduction-1/point-sources-and-inlets/hmet_filename.rec.md` (names `hmet_filename.rec`)
- `io-docs/introduction-1/point-sources-and-inlets/path_filename.rec.md` (names `path_filename.rec`)
- `io-docs/introduction-1/point-sources-and-inlets/pest_filename.rec.md` (names `pest_filename.rec`)
- `io-docs/introduction-1/point-sources-and-inlets/salt_filename.rec.md` (names `salt_filename.rec`)
- `io-docs/introduction-1/water-allocation/water_allocation.wro/README.md` (names `water_allocation.wro`)
