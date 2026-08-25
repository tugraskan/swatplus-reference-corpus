# Modular Database to Source Field Map: SWAT+ 62.0.0

For each input file, which modular database column corresponds to which
SWAT+ source variable. The two sides use different names for the same
parameter -- the spreadsheet uses SWAT+ Editor database names, the source
uses Fortran names -- so the pairing is resolved through the editor schema
report rather than by matching names directly.

| Status | Meaning | Count |
|---|---|---:|
| `matched` | The spreadsheet row and a source field are the same parameter | 1313 |
| `spreadsheet_only` | Documented in the spreadsheet, no such field in the source | 590 |
| `source_only` | Read by the source, never documented in the spreadsheet | 669 |

Of the `spreadsheet_only` rows, 192 are marked `(structural)` in the table
below: the row's code-variable cell is blank or `*`, the spreadsheet's own marker for a
repeat-block header or file-level note rather than a single named field. These are not
counted as dropped or renamed parameters. The remaining `spreadsheet_only` rows are.

The spreadsheet's name for a parameter is also checked directly against the
Editor's real database columns (`editor_schema` in the editor-schema report),
independent of whether the source-side pairing above resolved:

| Editor check | Meaning | Count |
|---|---|---:|
| `verified` | This name is a real Editor database column | 1105 |
| `mismatch` | This name is not in the Editor database for this file | 620 |
| `unavailable` | This file has no Editor schema data to check against | 178 |

## Contents

- [`aqu_catunit.def`](#aqucatunitdef) - 4 matched, 2 spreadsheet-only, 1 source-only
- [`aqu_catunit.ele`](#aqucatunitele) - 6 matched, 1 spreadsheet-only, 1 source-only
- [`aqu_cha.lin`](#aquchalin) - 5 matched, 1 spreadsheet-only, 1 source-only
- [`aqu_reg.def`](#aquregdef) - 4 matched, 2 spreadsheet-only, 1 source-only
- [`aquifer.aqu`](#aquiferaqu) - 18 matched, 0 spreadsheet-only, 0 source-only
- [`aquifer.con`](#aquifercon) - 17 matched, 3 spreadsheet-only, 0 source-only
- [`atmodep.cli`](#atmodepcli) - 8 matched, 4 spreadsheet-only, 10 source-only
- [`bmpuser.str`](#bmpuserstr) - 8 matched, 2 spreadsheet-only, 0 source-only
- [`cal_parms.cal`](#calparmscal) - 5 matched, 2 spreadsheet-only, 0 source-only
- [`calibration.cal`](#calibrationcal) - 12 matched, 4 spreadsheet-only, 7 source-only
- [`carbon.bsn`](#carbonbsn) - 0 matched, 0 spreadsheet-only, 28 source-only
- [`cell_sol.gw`](#cellsolgw) - 0 matched, 0 spreadsheet-only, 2 source-only
- [`cells.gw`](#cellsgw) - 0 matched, 0 spreadsheet-only, 23 source-only
- [`ch_catunit.def`](#chcatunitdef) - 4 matched, 2 spreadsheet-only, 1 source-only
- [`ch_reg.def`](#chregdef) - 4 matched, 2 spreadsheet-only, 1 source-only
- [`ch_sed_budget.sft`](#chsedbudgetsft) - 9 matched, 2 spreadsheet-only, 0 source-only
- [`ch_sed_parms.sft`](#chsedparmssft) - 5 matched, 3 spreadsheet-only, 1 source-only
- [`chan-surf.lin`](#chan-surflin) - 4 matched, 2 spreadsheet-only, 1 source-only
- [`chancell.gw`](#chancellgw) - 0 matched, 0 spreadsheet-only, 5 source-only
- [`chandeg.con`](#chandegcon) - 16 matched, 4 spreadsheet-only, 1 source-only
- [`channel-lte.cha`](#channel-ltecha) - 6 matched, 1 spreadsheet-only, 0 source-only
- [`channel.cha`](#channelcha) - 6 matched, 1 spreadsheet-only, 0 source-only
- [`channel.con`](#channelcon) - 17 matched, 3 spreadsheet-only, 0 source-only
- [`chem_app.ops`](#chemappops) - 9 matched, 2 spreadsheet-only, 0 source-only
- [`cntable.lum`](#cntablelum) - 1 matched, 12 spreadsheet-only, 4 source-only
- [`co2_yr.dat`](#co2yrdat) - 0 matched, 0 spreadsheet-only, 3 source-only
- [`codes.bsn`](#codesbsn) - 23 matched, 3 spreadsheet-only, 3 source-only
- [`codes.sft`](#codessft) - 8 matched, 1 spreadsheet-only, 0 source-only
- [`cons_practice.lum`](#conspracticelum) - 7 matched, 2 spreadsheet-only, 0 source-only
- [`constituents.cs`](#constituentscs) - 4 matched, 6 spreadsheet-only, 6 source-only
- [`cs_aqu.ini`](#csaquini) - 0 matched, 0 spreadsheet-only, 2 source-only
- [`cs_atmo.cli`](#csatmocli) - 0 matched, 0 spreadsheet-only, 7 source-only
- [`cs_channel.ini`](#cschannelini) - 0 matched, 0 spreadsheet-only, 2 source-only
- [`cs_hru.ini`](#cshruini) - 0 matched, 0 spreadsheet-only, 3 source-only
- [`cs_recall.rec`](#csrecallrec) - 0 matched, 0 spreadsheet-only, 12 source-only
- [`delratio.con`](#delratiocon) - 16 matched, 4 spreadsheet-only, 1 source-only
- [`delratio.del`](#delratiodel) - 6 matched, 1 spreadsheet-only, 0 source-only
- [`dr_hmet.del`](#drhmetdel) - 0 matched, 4 spreadsheet-only, 2 source-only
- [`dr_om.del`](#dromdel) - 19 matched, 1 spreadsheet-only, 0 source-only
- [`dr_path.del`](#drpathdel) - 0 matched, 4 spreadsheet-only, 2 source-only
- [`dr_pest.del`](#drpestdel) - 0 matched, 4 spreadsheet-only, 2 source-only
- [`dr_salt.del`](#drsaltdel) - 0 matched, 4 spreadsheet-only, 2 source-only
- [`element.ccu`](#elementccu) - 0 matched, 0 spreadsheet-only, 7 source-only
- [`exco.con`](#excocon) - 17 matched, 3 spreadsheet-only, 0 source-only
- [`exco.exc`](#excoexc) - 6 matched, 1 spreadsheet-only, 3 source-only
- [`exco_hmet.exc`](#excohmetexc) - 1 matched, 3 spreadsheet-only, 1 source-only
- [`exco_om.exc`](#excoomexc) - 19 matched, 1 spreadsheet-only, 0 source-only
- [`exco_path.exc`](#excopathexc) - 1 matched, 3 spreadsheet-only, 1 source-only
- [`exco_pest.exc`](#excopestexc) - 1 matched, 3 spreadsheet-only, 1 source-only
- [`exco_salt.exc`](#excosaltexc) - 1 matched, 3 spreadsheet-only, 1 source-only
- [`fertilizer.frt`](#fertilizerfrt) - 6 matched, 2 spreadsheet-only, 0 source-only
- [`fertilizer.frt_cs`](#fertilizerfrtcs) - 0 matched, 0 spreadsheet-only, 4 source-only
- [`field.fld`](#fieldfld) - 4 matched, 1 spreadsheet-only, 0 source-only
- [`filterstrip.str`](#filterstripstr) - 5 matched, 2 spreadsheet-only, 0 source-only
- [`fire.ops`](#fireops) - 3 matched, 2 spreadsheet-only, 0 source-only
- [`flo_con.dtl`](#flocondtl) - 40 matched, 5 spreadsheet-only, 0 source-only
- [`floodplain.gw`](#floodplaingw) - 0 matched, 0 spreadsheet-only, 4 source-only
- [`grassedww.str`](#grassedwwstr) - 8 matched, 2 spreadsheet-only, 0 source-only
- [`graze.ops`](#grazeops) - 6 matched, 2 spreadsheet-only, 0 source-only
- [`gwflow.con`](#gwflowcon) - 0 matched, 0 spreadsheet-only, 17 source-only
- [`gwflow.wetland`](#gwflowwetland) - 0 matched, 0 spreadsheet-only, 2 source-only
- [`gwflow_canal.con`](#gwflowcanalcon) - 0 matched, 0 spreadsheet-only, 2 source-only
- [`harv.ops`](#harvops) - 5 matched, 1 spreadsheet-only, 0 source-only
- [`hmd.cli`](#hmdcli) - 0 matched, 1 spreadsheet-only, 2 source-only
- [`hmet_hru.ini`](#hmethruini) - 1 matched, 4 spreadsheet-only, 2 source-only
- [`hru-data.hru`](#hru-datahru) - 9 matched, 1 spreadsheet-only, 1 source-only
- [`hru-lte.con`](#hru-ltecon) - 17 matched, 3 spreadsheet-only, 0 source-only
- [`hru-lte.hru`](#hru-ltehru) - 35 matched, 0 spreadsheet-only, 0 source-only
- [`hru.con`](#hrucon) - 17 matched, 3 spreadsheet-only, 0 source-only
- [`hrucell.gw`](#hrucellgw) - 0 matched, 0 spreadsheet-only, 4 source-only
- [`hyd-sed-lte.cha`](#hyd-sed-ltecha) - 23 matched, 2 spreadsheet-only, 0 source-only
- [`hydrology.cha`](#hydrologycha) - 10 matched, 2 spreadsheet-only, 0 source-only
- [`hydrology.hyd`](#hydrologyhyd) - 14 matched, 2 spreadsheet-only, 1 source-only
- [`hydrology.res`](#hydrologyres) - 11 matched, 1 spreadsheet-only, 0 source-only
- [`hydrology.wet`](#hydrologywet) - 11 matched, 0 spreadsheet-only, 0 source-only
- [`initial.aqu`](#initialaqu) - 6 matched, 0 spreadsheet-only, 0 source-only
- [`initial.aqu_cs`](#initialaqucs) - 0 matched, 0 spreadsheet-only, 6 source-only
- [`initial.cha`](#initialcha) - 6 matched, 2 spreadsheet-only, 0 source-only
- [`initial.cha_cs`](#initialchacs) - 0 matched, 0 spreadsheet-only, 6 source-only
- [`initial.res`](#initialres) - 6 matched, 2 spreadsheet-only, 0 source-only
- [`irr.ops`](#irrops) - 8 matched, 2 spreadsheet-only, 0 source-only
- [`landuse.lum`](#landuselum) - 13 matched, 3 spreadsheet-only, 1 source-only
- [`ls_reg.def`](#lsregdef) - 4 matched, 3 spreadsheet-only, 3 source-only
- [`ls_reg.ele`](#lsregele) - 4 matched, 1 spreadsheet-only, 1 source-only
- [`ls_unit.def`](#lsunitdef) - 5 matched, 3 spreadsheet-only, 0 source-only
- [`ls_unit.ele`](#lsunitele) - 5 matched, 1 spreadsheet-only, 1 source-only
- [`lsucell.gw`](#lsucellgw) - 0 matched, 0 spreadsheet-only, 4 source-only
- [`lum.dtl`](#lumdtl) - 40 matched, 5 spreadsheet-only, 0 source-only
- [`management.sch`](#managementsch) - 10 matched, 8 spreadsheet-only, 1 source-only
- [`manure.frt`](#manurefrt) - 0 matched, 0 spreadsheet-only, 14 source-only
- [`manure_allo.mnu`](#manureallomnu) - 0 matched, 0 spreadsheet-only, 27 source-only
- [`manure_db.frt`](#manuredbfrt) - 0 matched, 0 spreadsheet-only, 8 source-only
- [`manure_om.frt`](#manureomfrt) - 0 matched, 0 spreadsheet-only, 9 source-only
- [`minerals.gw`](#mineralsgw) - 0 matched, 0 spreadsheet-only, 5 source-only
- [`nutrients.cha`](#nutrientscha) - 39 matched, 2 spreadsheet-only, 0 source-only
- [`nutrients.res`](#nutrientsres) - 13 matched, 1 spreadsheet-only, 0 source-only
- [`nutrients.rte`](#nutrientsrte) - 0 matched, 0 spreadsheet-only, 21 source-only
- [`nutrients.sol`](#nutrientssol) - 12 matched, 2 spreadsheet-only, 0 source-only
- [`object.cnt`](#objectcnt) - 21 matched, 0 spreadsheet-only, 0 source-only
- [`object.prt`](#objectprt) - 0 matched, 0 spreadsheet-only, 5 source-only
- [`om_osrc.wal`](#omosrcwal) - 0 matched, 0 spreadsheet-only, 19 source-only
- [`om_treat.wal`](#omtreatwal) - 0 matched, 0 spreadsheet-only, 19 source-only
- [`om_use.wal`](#omusewal) - 0 matched, 0 spreadsheet-only, 19 source-only
- [`om_water.ini`](#omwaterini) - 18 matched, 3 spreadsheet-only, 1 source-only
- [`out_src.wal`](#outsrcwal) - 0 matched, 0 spreadsheet-only, 8 source-only
- [`outlet.con`](#outletcon) - 11 matched, 9 spreadsheet-only, 6 source-only
- [`outputs.gw`](#outputsgw) - 0 matched, 0 spreadsheet-only, 3 source-only
- [`outside_rcv.wal`](#outsidercvwal) - 0 matched, 0 spreadsheet-only, 3 source-only
- [`ovn_table.lum`](#ovntablelum) - 7 matched, 1 spreadsheet-only, 0 source-only
- [`parameters.bsn`](#parametersbsn) - 42 matched, 3 spreadsheet-only, 2 source-only
- [`path_hru.ini`](#pathhruini) - 1 matched, 4 spreadsheet-only, 2 source-only
- [`path_water.ini`](#pathwaterini) - 1 matched, 4 spreadsheet-only, 2 source-only
- [`pathogens.pth`](#pathogenspth) - 17 matched, 3 spreadsheet-only, 1 source-only
- [`pcp.cli`](#pcpcli) - 0 matched, 1 spreadsheet-only, 2 source-only
- [`pest.com`](#pestcom) - 0 matched, 0 spreadsheet-only, 4 source-only
- [`pest_hru.ini`](#pesthruini) - 1 matched, 4 spreadsheet-only, 2 source-only
- [`pest_water.ini`](#pestwaterini) - 1 matched, 4 spreadsheet-only, 2 source-only
- [`pesticide.pes`](#pesticidepes) - 10 matched, 6 spreadsheet-only, 6 source-only
- [`pet.cli`](#petcli) - 0 matched, 1 spreadsheet-only, 2 source-only
- [`phreato.gw`](#phreatogw) - 0 matched, 0 spreadsheet-only, 2 source-only
- [`phreato_cell.gw`](#phreatocellgw) - 0 matched, 0 spreadsheet-only, 2 source-only
- [`plant.ini`](#plantini) - 11 matched, 3 spreadsheet-only, 0 source-only
- [`plant_gro.sft`](#plantgrosft) - 5 matched, 6 spreadsheet-only, 6 source-only
- [`plant_parms.sft`](#plantparmssft) - 6 matched, 5 spreadsheet-only, 6 source-only
- [`plants.plt`](#plantsplt) - 53 matched, 4 spreadsheet-only, 4 source-only
- [`pond_cell.gw`](#pondcellgw) - 0 matched, 0 spreadsheet-only, 3 source-only
- [`ponds.gw`](#pondsgw) - 0 matched, 0 spreadsheet-only, 12 source-only
- [`print.prt`](#printprt) - 13 matched, 214 spreadsheet-only, 6 source-only
- [`puddle.ops`](#puddleops) - 0 matched, 0 spreadsheet-only, 9 source-only
- [`pumpex.gw`](#pumpexgw) - 0 matched, 0 spreadsheet-only, 7 source-only
- [`rec_catunit.def`](#reccatunitdef) - 4 matched, 2 spreadsheet-only, 1 source-only
- [`rec_catunit.ele`](#reccatunitele) - 4 matched, 3 spreadsheet-only, 3 source-only
- [`rec_reg.def`](#recregdef) - 4 matched, 2 spreadsheet-only, 1 source-only
- [`recall.con`](#recallcon) - 13 matched, 7 spreadsheet-only, 4 source-only
- [`recall_db.rec`](#recalldbrec) - 0 matched, 0 spreadsheet-only, 20 source-only
- [`res_catunit.def`](#rescatunitdef) - 4 matched, 2 spreadsheet-only, 1 source-only
- [`res_catunit.ele`](#rescatunitele) - 5 matched, 2 spreadsheet-only, 2 source-only
- [`res_conds.dat`](#rescondsdat) - 0 matched, 0 spreadsheet-only, 3 source-only
- [`res_reg.def`](#resregdef) - 4 matched, 2 spreadsheet-only, 1 source-only
- [`res_rel.dtl`](#resreldtl) - 40 matched, 7 spreadsheet-only, 0 source-only
- [`rescell.gw`](#rescellgw) - 0 matched, 0 spreadsheet-only, 3 source-only
- [`reservoir.con`](#reservoircon) - 17 matched, 3 spreadsheet-only, 0 source-only
- [`reservoir.res`](#reservoirres) - 7 matched, 1 spreadsheet-only, 0 source-only
- [`reservoir.res_cs`](#reservoirrescs) - 0 matched, 0 spreadsheet-only, 5 source-only
- [`rout_unit.con`](#routunitcon) - 17 matched, 3 spreadsheet-only, 0 source-only
- [`rout_unit.def`](#routunitdef) - 4 matched, 2 spreadsheet-only, 0 source-only
- [`rout_unit.ele`](#routunitele) - 5 matched, 1 spreadsheet-only, 1 source-only
- [`rout_unit.rtu`](#routunitrtu) - 6 matched, 1 spreadsheet-only, 0 source-only
- [`salt_aqu.ini`](#saltaquini) - 0 matched, 0 spreadsheet-only, 3 source-only
- [`salt_atmo.cli`](#saltatmocli) - 0 matched, 0 spreadsheet-only, 7 source-only
- [`salt_channel.ini`](#saltchannelini) - 0 matched, 0 spreadsheet-only, 2 source-only
- [`salt_fertilizer.frt`](#saltfertilizerfrt) - 0 matched, 0 spreadsheet-only, 9 source-only
- [`salt_hru.ini`](#salthruini) - 1 matched, 4 spreadsheet-only, 2 source-only
- [`salt_recall.rec`](#saltrecallrec) - 0 matched, 0 spreadsheet-only, 12 source-only
- [`satbuffer.str`](#satbufferstr) - 0 matched, 0 spreadsheet-only, 6 source-only
- [`scen_dtl.upd`](#scendtlupd) - 0 matched, 0 spreadsheet-only, 3 source-only
- [`scen_lu.dtl`](#scenludtl) - 40 matched, 5 spreadsheet-only, 0 source-only
- [`sed_nut.cha`](#sednutcha) - 10 matched, 2 spreadsheet-only, 3 source-only
- [`sediment.cha`](#sedimentcha) - 24 matched, 2 spreadsheet-only, 0 source-only
- [`sediment.res`](#sedimentres) - 7 matched, 1 spreadsheet-only, 0 source-only
- [`septic.sep`](#septicsep) - 11 matched, 1 spreadsheet-only, 0 source-only
- [`septic.str`](#septicstr) - 28 matched, 1 spreadsheet-only, 0 source-only
- [`shade_factor.shf`](#shadefactorshf) - 0 matched, 0 spreadsheet-only, 3 source-only
- [`slr.cli`](#slrcli) - 0 matched, 1 spreadsheet-only, 2 source-only
- [`snow.sno`](#snowsno) - 9 matched, 1 spreadsheet-only, 0 source-only
- [`soil_plant.ini`](#soilplantini) - 7 matched, 2 spreadsheet-only, 1 source-only
- [`soils.sol`](#soilssol) - 21 matched, 4 spreadsheet-only, 0 source-only
- [`soils_lte.sol`](#soilsltesol) - 4 matched, 2 spreadsheet-only, 0 source-only
- [`solute.gw`](#solutegw) - 0 matched, 0 spreadsheet-only, 4 source-only
- [`sweep.ops`](#sweepops) - 3 matched, 2 spreadsheet-only, 0 source-only
- [`temperature.cha`](#temperaturecha) - 4 matched, 3 spreadsheet-only, 11 source-only
- [`tile.gw`](#tilegw) - 0 matched, 0 spreadsheet-only, 1 source-only
- [`tiledrain.str`](#tiledrainstr) - 9 matched, 2 spreadsheet-only, 0 source-only
- [`tillage.til`](#tillagetil) - 6 matched, 2 spreadsheet-only, 0 source-only
- [`time.sim`](#timesim) - 5 matched, 1 spreadsheet-only, 0 source-only
- [`tmp.cli`](#tmpcli) - 0 matched, 1 spreadsheet-only, 2 source-only
- [`topography.hyd`](#topographyhyd) - 6 matched, 1 spreadsheet-only, 0 source-only
- [`transplant.plt`](#transplantplt) - 0 matched, 0 spreadsheet-only, 6 source-only
- [`tvheads.gw`](#tvheadsgw) - 0 matched, 0 spreadsheet-only, 2 source-only
- [`urban.urb`](#urbanurb) - 11 matched, 2 spreadsheet-only, 0 source-only
- [`water_allocation.wro`](#waterallocationwro) - 5 matched, 44 spreadsheet-only, 13 source-only
- [`water_balance.sft`](#waterbalancesft) - 12 matched, 3 spreadsheet-only, 1 source-only
- [`water_canal.wal`](#watercanalwal) - 0 matched, 0 spreadsheet-only, 18 source-only
- [`water_pipe.wal`](#waterpipewal) - 0 matched, 0 spreadsheet-only, 7 source-only
- [`water_tower.wal`](#watertowerwal) - 0 matched, 0 spreadsheet-only, 5 source-only
- [`water_treat.wal`](#watertreatwal) - 0 matched, 0 spreadsheet-only, 14 source-only
- [`water_use.wal`](#waterusewal) - 0 matched, 0 spreadsheet-only, 14 source-only
- [`wb_parms.sft`](#wbparmssft) - 6 matched, 2 spreadsheet-only, 0 source-only
- [`weather-sta.cli`](#weather-stacli) - 9 matched, 0 spreadsheet-only, 0 source-only
- [`weather-wgn.cli`](#weather-wgncli) - 19 matched, 3 spreadsheet-only, 0 source-only
- [`weir.res`](#weirres) - 4 matched, 4 spreadsheet-only, 1 source-only
- [`wetland.wet`](#wetlandwet) - 7 matched, 3 spreadsheet-only, 0 source-only
- [`wetland.wet_cs`](#wetlandwetcs) - 0 matched, 0 spreadsheet-only, 5 source-only
- [`wnd.cli`](#wndcli) - 0 matched, 1 spreadsheet-only, 2 source-only
- [`zones.gw`](#zonesgw) - 0 matched, 0 spreadsheet-only, 5 source-only

## aqu_catunit.def

| Spreadsheet name | Type | Units | Range | Source name | Type | Description | Status | Editor DB name | Editor check |
|---|---|---|---|---|---|---|---|---|---|
| mreg | integer | - | - | - | - | aquifer cataloging units out numb | `spreadsheet_only` | - | `unavailable` |
| numb | integer | - | - | - | - | aquifer cataloging units out numb | `spreadsheet_only` | - | `unavailable` |
| acu_out_name | string | - | - | name | character | aquifer cataloging units out name | `matched` | - | `unavailable` |
| acu_out_area | numeric | - | - | area_ha | real | aquifer cataloging units out area | `matched` | - | `unavailable` |
| nspu | integer | - | - | nspu | integer | aquifer cataloging units out elements | `matched` | - | `unavailable` |
| elem | integer | - | - | elem_cnt | integer | aquifer cataloging units out elements | `matched` | - | `unavailable` |
| - | - | - | - | k | integer | - | `source_only` | - | - |

## aqu_catunit.ele

| Spreadsheet name | Type | Units | Range | Source name | Type | Description | Status | Editor DB name | Editor check |
|---|---|---|---|---|---|---|---|---|---|
| numb | integer | - | - | - | - | aquifer cataloging units numb | `spreadsheet_only` | - | `mismatch` |
| aqu_name | string | - | - | name | character | aquifer cataloging units name | `matched` | name | `verified` |
| aqu_obj_typ | string | - | - | obtyp | character | aquifer cataloging units object type | `matched` | - | `mismatch` |
| aqu_obj_typ_no | integer | - | - | obtypno | integer | aquifer cataloging units object type number | `matched` | - | `mismatch` |
| aqu_bsn_frac | numeric | - | - | bsn_frac | real | aquifer cataloging units basin fraction | `matched` | bsn_frac | `verified` |
| aqu_sub_frac | numeric | - | - | ru_frac | real | aquifer cataloging units subbasin fraction | `matched` | sub_frac | `verified` |
| aqu_reg_frac | numeric | - | - | reg_frac | real | aquifer cataloging units region fraction | `matched` | reg_frac | `verified` |
| - | - | - | - | k | integer | - | `source_only` | - | - |

## aqu_cha.lin

| Spreadsheet name | Type | Units | Range | Source name | Type | Description | Status | Editor DB name | Editor check |
|---|---|---|---|---|---|---|---|---|---|
| numb | integer | - | - | numb | integer | sequential number of link | `matched` | - | `unavailable` |
| name | string | - | - | name | character | name of channel surface link | `matched` | - | `unavailable` |
| elem_cnt | integer | - | - | elem_cnt | integer | element count | `matched` | - | `unavailable` |
| numb | integer | none | - | numb | integer | sequential number of link | `matched` | - | `unavailable` |
| elem_numb | integer | none | 1..10 | - | - | 1-10 number of element group | `spreadsheet_only` (structural) | - | `unavailable` |
| elem | integer | none | - | elem_cnt | integer | Element | `matched` | - | `unavailable` |
| - | - | - | - | nspu | integer | - | `source_only` | - | - |

## aqu_reg.def

| Spreadsheet name | Type | Units | Range | Source name | Type | Description | Status | Editor DB name | Editor check |
|---|---|---|---|---|---|---|---|---|---|
| mreg | integer | - | - | - | - | aquifer cataloging units regions numb | `spreadsheet_only` | - | `unavailable` |
| numb | integer | - | - | - | - | aquifer cataloging units regions numb | `spreadsheet_only` | - | `unavailable` |
| acu_reg_name | string | - | - | name | character | aquifer cataloging units regions name | `matched` | - | `unavailable` |
| acu_reg_area | numeric | - | - | area_ha | real | aquifer cataloging units regions area | `matched` | - | `unavailable` |
| nspu | integer | - | - | nspu | integer | aquifer cataloging units regions elements | `matched` | - | `unavailable` |
| elem | integer | - | - | elem_cnt | integer | aquifer cataloging units regions elements | `matched` | - | `unavailable` |
| - | - | - | - | k | integer | - | `source_only` | - | - |

## aquifer.aqu

| Spreadsheet name | Type | Units | Range | Source name | Type | Description | Status | Editor DB name | Editor check |
|---|---|---|---|---|---|---|---|---|---|
| id | integer | none | - | k | integer | Aquifer number | `matched` | id | `verified` |
| name | string | - | - | aqunm | character | Aquifer name | `matched` | name | `verified` |
| aqu_ini | string | - | - | aqu_ini | character | Initial aquifer data - points to name in initial .aqu | `matched` | - | `mismatch` |
| gw_flo | numeric | mm | 0..2 | flo | real | Initial groundwater flow | `matched` | gw_flo | `verified` |
| dep_bot | numeric | m | 0..10 | dep_bot | real | Depth-mid-slope surface to bottom of aquifer | `matched` | dep_bot | `verified` |
| dep_wt | numeric | m | 0..10 | dep_wt | real | Depth-mid-slope surface to water table (initial) | `matched` | dep_wt | `verified` |
| no3_n | numeric | ppm NO3-N | 0..1000 | no3 | real | Nitrate concentration in shallow aquifer converted to kg/ha | `matched` | no3_n | `verified` |
| sol_p | numeric | mg P/L | 0..1000 | minp | real | Mineral P concentration | `matched` | sol_p | `verified` |
| carbon | numeric | % | 0..15 | cbn | real | Organic carbon in aquifer | `matched` | carbon | `verified` |
| flo_dist | numeric | m | 0..1000 | flo_dist | real | Ave flow distance to stream or object | `matched` | flo_dist | `verified` |
| flo_max | numeric | mm | 0..2 | bf_max | real | Baseflow rate when entire area is contributing to baseflow | `matched` | bf_max | `verified` |
| alpha_bf | numeric | 1/days | 0..1 | alpha | real | Alpha factor for groundwater recession curve | `matched` | alpha_bf | `verified` |
| revap | integer | mm | 0..1 | revap_co | real | Fraction of pet to calculate revap | `matched` | revap | `verified` |
| rchg_dp | numeric | none | 0..1 | seep | real | Recharge to deep aquifer (the fraction of root zone percolation that reaches the deep aquifer) | `matched` | rchg_dp | `verified` |
| spec_yld | numeric | m^3/m^3 | 0..0.4 | spyld | real | Specific yield for shallow aquifer | `matched` | spec_yld | `verified` |
| hl_no3n | numeric | days | 0..200 | hlife_n | real | Half-life of NO3 in the shallow aquifer | `matched` | hl_no3n | `verified` |
| flo_min | numeric | m | 0..10 | flo_min | real | Minimum aquifer storage to allow return flow [m] | `matched` | flo_min | `verified` |
| revap_min | numeric | mm | 0..10 | revap_min | real | Threshold depth of water in shallow aquifer required to allow revap to occur | `matched` | revap_min | `verified` |

## aquifer.con

| Spreadsheet name | Type | Units | Range | Source name | Type | Description | Status | Editor DB name | Editor check |
|---|---|---|---|---|---|---|---|---|---|
| id | integer | none | - | num | integer | Aquifer number | `matched` | id | `verified` |
| name | string | - | - | name | character | Aquifer name | `matched` | name | `verified` |
| gis_id | string | - | - | gis_id | integer | GIS id | `matched` | gis_id | `verified` |
| area | numeric | ha | - | area_ha | real | Area | `matched` | area | `verified` |
| lat | numeric | dec degrees | -90..90 | lat | real | Latitude | `matched` | lat | `verified` |
| lon | numeric | dec degrees | -180..180 | long | real | Longitude | `matched` | lon | `verified` |
| elev | numeric | m | 1..7000 | elev | real | Elevation of aquifer | `matched` | elev | `verified` |
| aqu | integer | none | - | props | integer | Pointer to aquifer properties | `matched` | - | `mismatch` |
| wst | string | none | - | wst_c | character | Weather station number | `matched` | wst | `verified` |
| cst | integer | none | - | constit | integer | Pointer to constituent data (pesticides, pathogens, metals, salts) | `matched` | cst | `verified` |
| ovfl | numeric | none | - | props2 | integer | Pointer to the connections of spatial objects for overbank flooding | `matched` | ovfl | `verified` |
| rule | integer | none | - | ruleset | character | Pointer to ruleset for flow fraction of hydrograph | `matched` | rule | `verified` |
| out_tot | integer | none | 1..12 | src_tot | integer | Total number of outgoing hydrographs | `matched` | out_tot | `verified` |
| aqu_id | integer | none | - | - | - | Aquifer number | `spreadsheet_only` (structural) | - | `mismatch` |
| obj_numb | integer | none | 1..10 | - | - | Object number 1-10 | `spreadsheet_only` (structural) | - | `mismatch` |
| obj_typ | string | - | - | obtyp_out | character | Outflow object type | `matched` | obj_typ | `verified` |
| obj_id | integer | none | - | obtypno_out | integer | Outflow object identifier for specified type | `matched` | obj_id | `verified` |
| hyd_typ | string | - | - | htyp_out | character | Outflow hydrograph type | `matched` | hyd_typ | `verified` |
| frac | numeric | none | 0..1 | frac_out | real | Fraction of hydrograph sent to object | `matched` | frac | `verified` |
| description | string | none | - | - | - | - | `spreadsheet_only` (structural) | - | `mismatch` |

## atmodep.cli

| Spreadsheet name | Type | Units | Range | Source name | Type | Description | Status | Editor DB name | Editor check |
|---|---|---|---|---|---|---|---|---|---|
| id | integer | - | - | - | - | ID | `spreadsheet_only` | - | `mismatch` |
| num_sta | integer | - | - | num_sta | integer | total number of stations in the atmo datafile | `matched` | num_sta | `verified` |
| timestep | string | - | - | timestep | character | timestep of input data (aa, yr, mo) | `matched` | timestep | `verified` |
| mo_init | integer | - | - | mo_init | integer | initial month of input data | `matched` | mo_init | `verified` |
| yr_init | integer | - | - | yr_init | integer | initial year of input data | `matched` | yr_init | `verified` |
| num_aa | integer | - | - | - | - | number of average annual vals(0); years; months across | `spreadsheet_only` | - | `mismatch` |
| name | string | - | - | - | - | name of station | `spreadsheet_only` | - | `mismatch` |
| yr | integer | - | - | - | - | year | `spreadsheet_only` | - | `mismatch` |
| nh4_wet | numeric | - | - | nh4_rf | real | atmospheric deposition of nitrate for entire watershed | `matched` | nh4_rf | `verified` |
| no3_wet | numeric | - | - | no3_rf | real | atmospheric deposition of nh4 for entire watershed | `matched` | no3_rf | `verified` |
| nh4_dry | numeric | - | - | nh4_dry | real | nh4_dry (atmospheric dry deposition of ammonia) | `matched` | nh4_dry | `verified` |
| no3_dry | numeric | - | - | no3_dry | real | no3_dry (atmospheric dry deposition of nitrates) | `matched` | no3_dry | `verified` |
| - | - | - | - | num | integer | - | `source_only` | - | - |
| - | - | - | - | station_name | character | station name | `source_only` | - | - |
| - | - | - | - | nh4_rfmo | real | - | `source_only` | - | - |
| - | - | - | - | no3_rfmo | real | - | `source_only` | - | - |
| - | - | - | - | nh4_drymo | real | - | `source_only` | - | - |
| - | - | - | - | no3_drymo | real | - | `source_only` | - | - |
| - | - | - | - | nh4_rfyr | real | - | `source_only` | - | - |
| - | - | - | - | no3_rfyr | real | - | `source_only` | - | - |
| - | - | - | - | nh4_dryyr | real | - | `source_only` | - | - |
| - | - | - | - | no3_dryyr | real | - | `source_only` | - | - |

## bmpuser.str

| Spreadsheet name | Type | Units | Range | Source name | Type | Description | Status | Editor DB name | Editor check |
|---|---|---|---|---|---|---|---|---|---|
| id | - | - | - | - | - | ID | `spreadsheet_only` (structural) | - | `mismatch` |
| name | string | - | - | name | character | BMP name | `matched` | name | `verified` |
| description | string | - | - | - | - | Description, not used in the model | `spreadsheet_only` (structural) | - | `mismatch` |
| flag | integer | - | 1..2 | bmp_flag | integer | BMP flag (1=active;2=inactive) ArcSWAT 0 and 1 | `matched` | flag | `verified` |
| sed_eff | numeric | % | 0..100 | bmp_sed | real | Sediment removal by BMP | `matched` | sed_eff | `verified` |
| ptlp_eff | numeric | % | 0..100 | bmp_pp | real | Particulate P removal by BMP | `matched` | ptlp_eff | `verified` |
| solp_eff | numeric | % | 0..100 | bmp_sp | real | Soluble P removal by BMP | `matched` | solp_eff | `verified` |
| ptln_eff | numeric | % | 0..100 | bmp_pn | real | Particulate N removal by BMP | `matched` | ptln_eff | `verified` |
| soln_eff | numeric | % | 0..100 | bmp_sn | real | Soluble N removal by BMP | `matched` | soln_eff | `verified` |
| bact_eff | numeric | % | 0..100 | bmp_bac | real | Bacteria removal by BMP | `matched` | bact_eff | `verified` |

## cal_parms.cal

| Spreadsheet name | Type | Units | Range | Source name | Type | Description | Status | Editor DB name | Editor check |
|---|---|---|---|---|---|---|---|---|---|
| id | integer | - | - | - | - | ID | `spreadsheet_only` (structural) | - | `mismatch` |
| parm_cnt | string | - | - | - | - | total number of parameter changes | `spreadsheet_only` | - | `mismatch` |
| parm_name | string | - | - | name | character | parameter name (cn2, esco, awc, etc.) | `matched` | name | `verified` |
| obj_typ | string | - | - | ob_typ | character | object type the parm is associated with (hru,chan,res,..) | `matched` | obj_typ | `verified` |
| abs_min | numeric | - | - | absmin | real | minimum range for variable | `matched` | abs_min | `verified` |
| abs_max | numeric | - | - | absmax | real | maximum range for variable | `matched` | abs_max | `verified` |
| units | integer | - | - | units | character | units used for each parameter | `matched` | units | `verified` |

## calibration.cal

| Spreadsheet name | Type | Units | Range | Source name | Type | Description | Status | Editor DB name | Editor check |
|---|---|---|---|---|---|---|---|---|---|
| id | integer | - | - | - | - | ID | `spreadsheet_only` (structural) | - | `mismatch` |
| upd_cnt | string | - | - | - | - | Total number of calibration updates in the file | `spreadsheet_only` | - | `mismatch` |
| parm_name | string | - | - | name | character | parameter name (cn2, esco, awc, etc.) | `matched` | - | `mismatch` |
| chg_typ | string | - | - | chg_typ | character | type of change (absval,abschg,pctchg) | `matched` | chg_typ | `verified` |
| chg_val | numeric | - | - | val | real | value of change | `matched` | chg_val | `verified` |
| cond_tot | integer | - | - | conds | integer | number of conditions | `matched` | conds | `verified` |
| soil_lyr1 | integer | - | - | lyr1 | integer | first layer in range for soil vars (0 assumes all layers) | `matched` | soil_lyr1 | `verified` |
| soil_lyr2 | integer | - | - | lyr2 | integer | last layer in range for soil vars (0 assumes all layers) | `matched` | soil_lyr2 | `verified` |
| yr1 | integer | - | - | year1 | integer | first year for precip and temp | `matched` | yr1 | `verified` |
| yr2 | integer | - | - | year2 | integer | last year for precip and temp | `matched` | yr2 | `verified` |
| day1 | integer | - | - | day1 | integer | first day in range for precip and temp | `matched` | day1 | `verified` |
| day2 | integer | - | - | day2 | integer | last day in range for precip and temp | `matched` | day2 | `verified` |
| numb_tot | integer | - | - | num_tot | integer | total number of integers to be read | `matched` | - | `mismatch` |
| elem_cnt | integer | - | - | elem_cnt | integer | total number of elements modified | `matched` | - | `mismatch` |
| numb | integer | - | - | - | - | - | `spreadsheet_only` | - | `mismatch` |
| numb_cond | integer | - | - | - | - | - | `spreadsheet_only` | - | `mismatch` |
| - | - | - | - | range | character | - | `source_only` | - | - |
| - | - | - | - | var | character | - | `source_only` | - | - |
| - | - | - | - | val1 | real | lower bound of numerical condition | `source_only` | - | - |
| - | - | - | - | val2 | real | upper bound of numerical condition | `source_only` | - | - |
| - | - | - | - | alt | character | - | `source_only` | - | - |
| - | - | - | - | targ | real | - | `source_only` | - | - |
| - | - | - | - | targc | character | - | `source_only` | - | - |

## carbon.bsn

| Spreadsheet name | Type | Units | Range | Source name | Type | Description | Status | Editor DB name | Editor check |
|---|---|---|---|---|---|---|---|---|---|
| - | - | - | - | frac_seq | real | fraction of total carbon the is sequestered carbon when initializing sequestered pools | `source_only` | - | - |
| - | - | - | - | frac_hum_microb | real | fraction of carbon that is microbrial pool when initializing microbrial pools | `source_only` | - | - |
| - | - | - | - | frac_hum_slow | real | fraction of carbon that is humas slow pool when initializing humus slow pools | `source_only` | - | - |
| - | - | - | - | frac_hum_passive | real | fraction of carbon that is humas passive pool when initializing humas passive pools | `source_only` | - | - |
| - | - | - | - | prmt_21 | real | KOC FOR CARBON LOSS IN WATER AND SEDIMENT(500._1500.) KD = KOC * C | `source_only` | - | - |
| - | - | - | - | prmt_44 | real | RATIO OF SOLUBLE C CONCENTRATION IN RUNOFF TO PERCOLATE(0.1_1.) | `source_only` | - | - |
| - | - | - | - | till_eff_days | integer | - | `source_only` | - | - |
| - | - | none | - | rtof | real | weighting factor used to partition the organic N & P concentration of septic effluent between the fresh organic and the stable organic pools | `source_only` | - | - |
| - | - | - | - | bio_consf | real | - | `source_only` | - | - |
| - | - | - | - | till_consf | real | - | `source_only` | - | - |
| - | - | - | - | tmpf | integer | temperature factor approach used in cbn_zhang2 | `source_only` | - | - |
| - | - | - | - | watf | integer | water factor approach used in cbn_zhang2 | `source_only` | - | - |
| - | - | real :: xbmt = 0. ! | - | tn | real | control on transformation of microbial biomass by soil texture and structure real :: xlslf = 0. ! \|control on potential transformation of structural litter by lignin fraction The following three parameters resolve the shape of the temperature effect equation: celsius \|minimum temperature bound | `source_only` | - | - |
| - | - | celsius | - | top | real | peak (optimum) temperature | `source_only` | - | - |
| - | - | celsius | - | tx | real | maximum temperature bound | `source_only` | - | - |
| - | - | - | - | bmix_a | real | - | `source_only` | - | - |
| - | - | - | - | bmix_b | real | - | `source_only` | - | - |
| - | - | - | - | bmix_c | real | - | `source_only` | - | - |
| - | - | - | - | tillmix_a | real | - | `source_only` | - | - |
| - | - | - | - | tillmix_b | real | - | `source_only` | - | - |
| - | - | - | - | tillmix_c | real | - | `source_only` | - | - |
| - | - | - | - | photo_degrade_factor | real | - | `source_only` | - | - |
| - | - | - | - | n_act_frac | real | - | `source_only` | - | - |
| - | - | - | - | cnr_cap | real | - | `source_only` | - | - |
| - | - | - | - | cnr_ref | real | - | `source_only` | - | - |
| - | - | - | - | cpr_cap | real | - | `source_only` | - | - |
| - | - | - | - | cpr_ref | real | - | `source_only` | - | - |
| - | - | - | - | mathers_int | integer | - | `source_only` | - | - |

## cell_sol.gw

| Spreadsheet name | Type | Units | Range | Source name | Type | Description | Status | Editor DB name | Editor check |
|---|---|---|---|---|---|---|---|---|---|
| - | - | - | - | cell_id | integer | - | `source_only` | - | - |
| - | - | g/m3 | - | conc | real | solute concentration in groundwater | `source_only` | - | - |

## cells.gw

| Spreadsheet name | Type | Units | Range | Source name | Type | Description | Status | Editor DB name | Editor check |
|---|---|---|---|---|---|---|---|---|---|
| - | - | - | - | cell_id_in | integer | - | `source_only` | - | - |
| - | - | - | - | cell_name | character | - | `source_only` | - | - |
| - | - | - | - | cell_gis_id | integer | - | `source_only` | - | - |
| - | - | - | - | stat | integer | status (0=inactive; 1=active; 2=boundary) | `source_only` | - | - |
| - | - | m | - | elev | real | ground surface elevation | `source_only` | - | - |
| - | - | m | - | thck | real | aquifer thickness | `source_only` | - | - |
| - | - | - | - | K_zone | integer | - | `source_only` | - | - |
| - | - | - | - | Sy_zone | integer | - | `source_only` | - | - |
| - | - | - | - | delay | real | - | `source_only` | - | - |
| - | - | m | - | exdp | real | groundwater ET extinction depth | `source_only` | - | - |
| - | - | m | - | init | real | initial groundwater head (beginning of simulation) | `source_only` | - | - |
| - | - | m | - | xcrd | real | x coordinate of cell centroid | `source_only` | - | - |
| - | - | m | - | ycrd | real | y coordinate of cell centroid | `source_only` | - | - |
| - | - | m2 | - | area | real | surface area | `source_only` | - | - |
| - | - | - | - | cell_strK_over | real | - | `source_only` | - | - |
| - | - | - | - | cell_strthick_over | real | - | `source_only` | - | - |
| - | - | - | - | bc_type_array | real | - | `source_only` | - | - |
| - | - | - | - | cell_tile_depth_over | real | - | `source_only` | - | - |
| - | - | - | - | cell_tile_area_over | real | - | `source_only` | - | - |
| - | - | - | - | cell_tile_K_over | real | - | `source_only` | - | - |
| - | - | - | - | cell_row | integer | - | `source_only` | - | - |
| - | - | - | - | cell_col | integer | - | `source_only` | - | - |
| - | - | - | - | cell_init_temp | real | - | `source_only` | - | - |

## ch_catunit.def

| Spreadsheet name | Type | Units | Range | Source name | Type | Description | Status | Editor DB name | Editor check |
|---|---|---|---|---|---|---|---|---|---|
| mreg | integer | - | - | - | - | - | `spreadsheet_only` | - | `unavailable` |
| numb | integer | - | - | - | - | channel cataloging units out numb | `spreadsheet_only` | - | `unavailable` |
| ccu_out_name | string | - | - | name | character | channel cataloging units out name | `matched` | - | `unavailable` |
| ccu_out_area | numeric | - | - | area_ha | real | channel cataloging units out area | `matched` | - | `unavailable` |
| nspu | integer | - | - | nspu | integer | channel cataloging units out elements | `matched` | - | `unavailable` |
| elem | integer | - | - | elem_cnt | integer | channel cataloging units out elements | `matched` | - | `unavailable` |
| - | - | - | - | k | integer | - | `source_only` | - | - |

## ch_reg.def

| Spreadsheet name | Type | Units | Range | Source name | Type | Description | Status | Editor DB name | Editor check |
|---|---|---|---|---|---|---|---|---|---|
| mreg | integer | - | - | - | - | channel cataloging units regions numb | `spreadsheet_only` | - | `unavailable` |
| numb | integer | - | - | - | - | channel cataloging units regions numb | `spreadsheet_only` | - | `unavailable` |
| ccu_reg_name | string | - | - | name | character | channel cataloging units regions name | `matched` | - | `unavailable` |
| ccu_reg_area | numeric | - | - | area_ha | real | channel cataloging units regions area | `matched` | - | `unavailable` |
| nspu | integer | - | - | nspu | integer | channel cataloging units regions elements | `matched` | - | `unavailable` |
| elem | integer | - | - | elem_cnt | integer | channel cataloging units regions elements | `matched` | - | `unavailable` |
| - | - | - | - | k | integer | - | `source_only` | - | - |

## ch_sed_budget.sft

| Spreadsheet name | Type | Units | Range | Source name | Type | Description | Status | Editor DB name | Editor check |
|---|---|---|---|---|---|---|---|---|---|
| id | integer | - | - | - | - | ID | `spreadsheet_only` (structural) | - | `mismatch` |
| upd_cnt | string | - | - | - | - | Total number of stream order updates in the file | `spreadsheet_only` | - | `mismatch` |
| name | string | - | - | name | character | Regions calibration name | `matched` | name | `verified` |
| ord_numb | integer | - | - | ord_num | integer | Total number of stream order updates in following lines | `matched` | - | `mismatch` |
| nspu | integer | - | - | nspu | integer | The number of elements in following lines | `matched` | - | `mismatch` |
| elem_cnt | integer | - | - | elem_cnt | integer | - | `matched` | - | `mismatch` |
| order | string | - | - | name | character | Order name | `matched` | name | `verified` |
| cha_wide | numeric | mm/yr | - | chw | real | Channel widening | `matched` | cha_wide | `verified` |
| cha_dc_accr | numeric | mm/yr | - | chd | real | Channel down cutting or accretion | `matched` | cha_dc_accr | `verified` |
| head_cut | numeric | m/yr | - | hc | real | Head cut advance | `matched` | head_cut | `verified` |
| fp_accr | numeric | mm/yr | - | fpd | real | flood plain accretion | `matched` | fp_accr | `verified` |

## ch_sed_parms.sft

| Spreadsheet name | Type | Units | Range | Source name | Type | Description | Status | Editor DB name | Editor check |
|---|---|---|---|---|---|---|---|---|---|
| id | integer | - | - | - | - | ID | `spreadsheet_only` (structural) | - | `mismatch` |
| upd_cnt | string | - | - | - | - | total number of count | `spreadsheet_only` | - | `mismatch` |
| name | string | - | - | name | character | name | `matched` | name | `verified` |
| ch_typ | integer | - | - | - | - | type of change (absval,abschg,pctchg) | `spreadsheet_only` | - | `mismatch` |
| neg | integer | - | - | neg | real | negative limit of change | `matched` | neg | `verified` |
| pos | integer | - | - | pos | real | positive limit of change | `matched` | pos | `verified` |
| lo | string | - | - | lo | real | lower limit of parameter | `matched` | lo | `verified` |
| up | numeric | - | - | up | real | upper limit of paramete | `matched` | up | `verified` |
| - | - | - | - | chg_typ | character | type of change (absval,abschg,pctchg) | `source_only` | - | - |

## chan-surf.lin

| Spreadsheet name | Type | Units | Range | Source name | Type | Description | Status | Editor DB name | Editor check |
|---|---|---|---|---|---|---|---|---|---|
| mcha | integer | - | - | - | - | total number of channel links in file | `spreadsheet_only` | - | `unavailable` |
| id | integer | - | - | numb | integer | sequential number of link | `matched` | - | `unavailable` |
| name | string | - | - | name | character | name of channel surface link | `matched` | - | `unavailable` |
| nspu | integer | - | - | - | - | the total number of objects to follow | `spreadsheet_only` | - | `unavailable` |
| obj_typ | integer | - | - | obtyp | character | object type (1=hru,2-hru-lte,11=export coef, etc. | `matched` | - | `unavailable` |
| obj_typ_no | integer | - | - | obtypno | integer | number of hru_lte's | `matched` | - | `unavailable` |
| - | - | - | - | obj_tot | integer | number of objects (hru and/or ru) in the flood plain | `source_only` | - | - |

## chancell.gw

| Spreadsheet name | Type | Units | Range | Source name | Type | Description | Status | Editor DB name | Editor check |
|---|---|---|---|---|---|---|---|---|---|
| - | - | - | - | cell_id | integer | - | `source_only` | - | - |
| - | - | - | - | bed_elev | real | - | `source_only` | - | - |
| - | - | - | - | channel | integer | - | `source_only` | - | - |
| - | - | - | - | chan_length | real | - | `source_only` | - | - |
| - | - | - | - | chan_zone | integer | - | `source_only` | - | - |

## chandeg.con

| Spreadsheet name | Type | Units | Range | Source name | Type | Description | Status | Editor DB name | Editor check |
|---|---|---|---|---|---|---|---|---|---|
| id | integer | none | - | num | integer | Channel lite number | `matched` | id | `verified` |
| name | string | - | - | name | character | Channel lite name | `matched` | name | `verified` |
| gis_id | string | - | - | gis_id | integer | GIS id | `matched` | gis_id | `verified` |
| area | numeric | ha | - | area_ha | real | Area | `matched` | area | `verified` |
| lat | numeric | dec degrees | -90..90 | lat | real | Latitude | `matched` | lat | `verified` |
| lon | numeric | dec degrees | -180..180 | long | real | Longitude | `matched` | lon | `verified` |
| elev | numeric | m | 1..7000 | elev | real | Elevation of chandeg | `matched` | elev | `verified` |
| lcha | integer | none | - | - | - | Pointer to channel properties | `spreadsheet_only` | - | `mismatch` |
| wst | string | none | - | wst_c | character | Weather station number | `matched` | wst | `verified` |
| cst | integer | none | - | constit | integer | Pointer to constituent data (pesticides, pathogens, metals, salts) | `matched` | cst | `verified` |
| ovfl | numeric | none | - | props2 | integer | Pointer to the connections of spatial objects for overbank flooding | `matched` | ovfl | `verified` |
| rule | integer | none | - | ruleset | character | Pointer to ruleset for flow fraction of hydrograph | `matched` | rule | `verified` |
| out_tot | integer | none | 1..12 | src_tot | integer | Total number of outgoing hydrographs | `matched` | out_tot | `verified` |
| lcha_id | integer | none | - | - | - | Channel number | `spreadsheet_only` (structural) | - | `mismatch` |
| obj_numb | integer | none | 1..10 | - | - | Object number 1-10 | `spreadsheet_only` (structural) | - | `mismatch` |
| obj_typ | string | - | - | obtyp_out | character | Outflow object type | `matched` | obj_typ | `verified` |
| obj_id | integer | none | - | obtypno_out | integer | Outflow object identifier for specified type | `matched` | obj_id | `verified` |
| hyd_typ | string | - | - | htyp_out | character | Outflow hydrograph type | `matched` | hyd_typ | `verified` |
| frac | numeric | none | 0..1 | frac_out | real | Fraction of hydrograph sent to object | `matched` | frac | `verified` |
| description | string | none | - | - | - | - | `spreadsheet_only` (structural) | - | `mismatch` |
| - | - | - | - | props | integer | properties number from data base (ie hru.dat, sub.dat) - change props to data | `source_only` | - | - |

## channel-lte.cha

| Spreadsheet name | Type | Units | Range | Source name | Type | Description | Status | Editor DB name | Editor check |
|---|---|---|---|---|---|---|---|---|---|
| id | integer | - | - | k | integer | ID | `matched` | id | `verified` |
| name | string | - | - | name | character | channel-lte name | `matched` | name | `verified` |
| description | string | - | - | - | - | - | `spreadsheet_only` (structural) | - | `mismatch` |
| cha_ini | string | - | - | initc | character | initial channel crosswalked from initial.cha | `matched` | cha_ini | `verified` |
| cha_hyd | string | - | - | hydc | character | crosswalked from hyd-sed-lte.cha | `matched` | cha_hyd | `verified` |
| cha_sed | string | - | - | sedc | character | crosswalked from sediment.cha | `matched` | cha_sed | `verified` |
| cha_nut | string | - | - | nutc | character | crosswalked from nutrients.cha | `matched` | cha_nut | `verified` |

## channel.cha

| Spreadsheet name | Type | Units | Range | Source name | Type | Description | Status | Editor DB name | Editor check |
|---|---|---|---|---|---|---|---|---|---|
| id | integer | none | - | k | integer | Channel number | `matched` | id | `verified` |
| name | string | - | - | name | character | Channel name | `matched` | name | `verified` |
| description | string | - | - | - | - | Description, not used in the model | `spreadsheet_only` (structural) | - | `mismatch` |
| init | string | none | - | init | character | Pointer to channel initial parameter set | `matched` | - | `mismatch` |
| hyd | string | none | - | hyd | character | Pointer to channel hydrology parameter set | `matched` | - | `mismatch` |
| sed | string | none | - | sed | character | Pointer to channel sediment parameter set | `matched` | - | `mismatch` |
| nut | string | none | - | nut | character | Pointer to channnel nutrient parameters | `matched` | - | `mismatch` |

## channel.con

| Spreadsheet name | Type | Units | Range | Source name | Type | Description | Status | Editor DB name | Editor check |
|---|---|---|---|---|---|---|---|---|---|
| id | integer | none | - | num | integer | Channel number | `matched` | id | `verified` |
| name | string | - | - | name | character | Channel name | `matched` | name | `verified` |
| gis_id | string | - | - | gis_id | integer | GIS id | `matched` | gis_id | `verified` |
| area | numeric | ha | - | area_ha | real | Area | `matched` | area | `verified` |
| lat | numeric | dec degrees | -90..90 | lat | real | Latitude | `matched` | lat | `verified` |
| lon | numeric | dec degrees | -180..180 | long | real | Longitude | `matched` | lon | `verified` |
| elev | numeric | m | 1..7000 | elev | real | Elevation of channel | `matched` | elev | `verified` |
| cha | integer | none | - | props | integer | Pointer to channel properties | `matched` | - | `mismatch` |
| wst | string | none | - | wst_c | character | Weather station number | `matched` | wst | `verified` |
| cst | integer | none | - | constit | integer | Pointer to constituent data (pesticides, pathogens, metals, salts) | `matched` | cst | `verified` |
| ovfl | numeric | none | - | props2 | integer | Pointer to the connections of spatial objects for overbank flooding | `matched` | ovfl | `verified` |
| rule | integer | none | - | ruleset | character | Pointer to ruleset for flow fraction of hydrograph | `matched` | rule | `verified` |
| out_tot | integer | none | 1..12 | src_tot | integer | Total number of outgoing hydrographs | `matched` | out_tot | `verified` |
| cha_id | integer | none | - | - | - | Channel number | `spreadsheet_only` (structural) | - | `mismatch` |
| obj_numb | integer | none | 1..10 | - | - | Object number 1-10 | `spreadsheet_only` (structural) | - | `mismatch` |
| obj_typ | string | - | - | obtyp_out | character | Outflow object type | `matched` | obj_typ | `verified` |
| obj_id | integer | none | - | obtypno_out | integer | Outflow object identifier for specified type | `matched` | obj_id | `verified` |
| hyd_typ | string | - | - | htyp_out | character | Outflow hydrograph type | `matched` | hyd_typ | `verified` |
| frac | numeric | none | 0..1 | frac_out | real | Fraction of hydrograph sent to object | `matched` | frac | `verified` |
| description | string | none | - | - | - | - | `spreadsheet_only` (structural) | - | `mismatch` |

## chem_app.ops

| Spreadsheet name | Type | Units | Range | Source name | Type | Description | Status | Editor DB name | Editor check |
|---|---|---|---|---|---|---|---|---|---|
| id | - | - | - | - | - | ID | `spreadsheet_only` (structural) | - | `mismatch` |
| name | string | - | - | name | character | Chem application name | `matched` | name | `verified` |
| description | string | - | - | - | - | Description, not used in the model | `spreadsheet_only` (structural) | - | `mismatch` |
| chem_form | string | - | - | form | character | Chem form (solid; liquid) | `matched` | chem_form | `verified` |
| app_typ | string | - | - | op_typ | character | Oper type (spread;spray;inject;direct) | `matched` | app_typ | `verified` |
| app_eff | numeric | - | - | app_eff | real | Application efficiency | `matched` | app_eff | `verified` |
| foliar_eff | numeric | - | - | foliar_eff | real | Foliar effeciency | `matched` | foliar_eff | `verified` |
| inject_dp | numeric | mm | - | inject_dep | real | Injection depth | `matched` | inject_dp | `verified` |
| surf_frac | numeric | - | - | surf_frac | real | Surf frac amount in upper 10mm | `matched` | surf_frac | `verified` |
| drift_pot | numeric | - | - | drift_pot | real | Drift potential | `matched` | drift_pot | `verified` |
| aerial_unif | numeric | - | - | aerial_unif | real | Aerial uniformity | `matched` | aerial_unif | `verified` |

## cntable.lum

| Spreadsheet name | Type | Units | Range | Source name | Type | Description | Status | Editor DB name | Editor check |
|---|---|---|---|---|---|---|---|---|---|
| id | - | - | - | - | - | ID | `spreadsheet_only` (structural) | - | `mismatch` |
| name | string | none | - | name | character | Curve number class name | `matched` | name | `verified` |
| landuse | string | - | - | - | - | Land use | `spreadsheet_only` (structural) | - | `mismatch` |
| description | string | - | - | - | - | Long Name | `spreadsheet_only` (structural) | - | `mismatch` |
| treat | string | - | - | - | - | Treatment/Practice | `spreadsheet_only` | treat | `verified` |
| rsd_cov | string | - | - | - | - | Residue cover (y/n) | `spreadsheet_only` (structural) | - | `mismatch` |
| contour | string | - | - | - | - | Contor farming (y/n) | `spreadsheet_only` (structural) | - | `mismatch` |
| terrace | string | - | - | - | - | Terraces (y/n) | `spreadsheet_only` (structural) | - | `mismatch` |
| cond_cov | string | - | - | - | - | Condition of cover | `spreadsheet_only` | cond_cov | `verified` |
| cn_a | numeric | none | 30..100 | - | - | Curve number for hydrologic soil group A | `spreadsheet_only` | cn_a | `verified` |
| cn_b | numeric | none | 30..100 | - | - | Curve number for hydrologic soil group B | `spreadsheet_only` | cn_b | `verified` |
| cn_c | numeric | none | 30..100 | - | - | Curve number for hydrologic soil group C | `spreadsheet_only` | cn_c | `verified` |
| cn_d | numeric | none | 30..100 | - | - | Curve number for hydrologic soil group D | `spreadsheet_only` | cn_d | `verified` |
| - | - | - | - | cn(1) | real | curve number | `source_only` | - | - |
| - | - | - | - | cn(2) | real | curve number | `source_only` | - | - |
| - | - | - | - | cn(3) | real | curve number | `source_only` | - | - |
| - | - | - | - | cn(4) | real | curve number | `source_only` | - | - |

## co2_yr.dat

| Spreadsheet name | Type | Units | Range | Source name | Type | Description | Status | Editor DB name | Editor check |
|---|---|---|---|---|---|---|---|---|---|
| - | - | - | - | iyr | integer | - | `source_only` | - | - |
| - | - | - | - | co2 | real | - | `source_only` | - | - |
| - | - | - | - | yrs | integer | - | `source_only` | - | - |

## codes.bsn

| Spreadsheet name | Type | Units | Range | Source name | Type | Description | Status | Editor DB name | Editor check |
|---|---|---|---|---|---|---|---|---|---|
| id | - | - | - | - | - | ID | `spreadsheet_only` (structural) | - | `mismatch` |
| pet_file | string | - | - | petfile | character | potential et filename | `matched` | pet_file | `verified` |
| wq_file | string | - | - | wwqfile | character | watershed stream water quality filename | `matched` | wq_file | `verified` |
| pet | integer | - | 0..3 | pet | integer | potential ET method code | `matched` | pet | `verified` |
| event | integer | - | - | nam1 | integer | event code | `matched` | event | `verified` |
| crack | integer | - | 0..1 | crk | integer | crack flow code | `matched` | crack | `verified` |
| rtu_wq | integer | - | 0..1 | - | - | subbasin water quality code | `spreadsheet_only` | - | `mismatch` |
| sed_det | integer | - | 0..1 | sed_det | integer | max half-hour rainfall frac calc | `matched` | sed_det | `verified` |
| rte_cha | integer | - | 0..1 | rte | integer | water routing method | `matched` | rte_cha | `verified` |
| deg_cha | integer | - | 0..1 | deg | integer | channel degradation code | `matched` | deg_cha | `verified` |
| wq_cha | integer | - | 0..1 | wq | integer | stream water quality code | `matched` | wq_cha | `verified` |
| nostress | integer | - | 0..250 | nostress | integer | stress codes: 0=all stresses applied; 1-turn off stresses;2=turn off nutrient stress only | `matched` | nostress | `verified` |
| cn | integer | - | 0..1 | cn | integer | 0=call cal_soft_hyd_bfr(CEAP); 1=call cal_soft_hyd; | `matched` | cn | `verified` |
| c_fact | integer | - | 0..1 | cfac | integer | C-factor | `matched` | c_fact | `verified` |
| carbon | integer | - | 0..2 | cswat | integer | carbon code | `matched` | carbon | `verified` |
| lapse | integer | - | 0..1 | lapse | integer | precip and temp lapse rate control 0=do not adjust; 1=adjust for elevation; | `matched` | lapse | `verified` |
| uhyd | integer | - | 0..1 | uhyd | integer | Unit hydrograph method; 0=triangular UH; 1=gamma function UH; | `matched` | uhyd | `verified` |
| sed_cha | integer | - | 0..2 | sed_ch | integer | Instream sediment model | `matched` | sed_cha | `verified` |
| tiledrain | integer | - | 0..1 | tdrn | integer | tile drainage eq code | `matched` | tiledrain | `verified` |
| wtable | integer | - | 0..1 | wtdn | integer | water table depth algorithms code | `matched` | wtable | `verified` |
| soil_p | integer | - | 0..1 | sol_p_model | integer | 1 = new soil P model | `matched` | soil_p | `verified` |
| gampt | integer | - | - | gampt | integer | Initial abstraction on impervious cover (mm) | `matched` | gampt | `verified` |
| atmo_dep | integer | - | - | atmo | character | atmospheric deposition code | `matched` | atmo_dep | `verified` |
| stor_max | integer | - | 0..1 | smax | integer | max depressional storage selection code | `matched` | stor_max | `verified` |
| i_fpwet | integer | - | 0..1 | - | - | floodplain calculation code 0=off; 1=on; | `spreadsheet_only` | - | `mismatch` |
| gwflow | integer | - | 0..1 | gwflow | integer | code for using groundwater flow routines; 0=off; 1=on; | `matched` | gwflow | `verified` |
| - | - | - | - | swift_out | integer | 1 = compute flow in cracks write to SWIFT input file | `source_only` | - | - |
| - | - | - | - | qual2e | integer | 0 = instream nutrient routing using QUAL2E | `source_only` | - | - |
| - | - | - | - | idc_till | integer | 1 = Use dssat tillage method to use if cswat = 2 | `source_only` | - | - |

## codes.sft

| Spreadsheet name | Type | Units | Range | Source name | Type | Description | Status | Editor DB name | Editor check |
|---|---|---|---|---|---|---|---|---|---|
| id | integer | - | - | - | - | ID | `spreadsheet_only` (structural) | - | `mismatch` |
| landscape_yn | string | - | - | hyd_hru | character | (y/n) if y, calib at least one landscape process | `matched` | - | `mismatch` |
| hyd_yn | string | - | - | hyd_hrul | character | (y/n) if y, calib hydrologic bal by lu in each reg | `matched` | - | `mismatch` |
| plnt_yn | string | - | - | plt | character | (y/n), if y, calib plant growth by plant in each reg | `matched` | - | `mismatch` |
| sed_yn | string | - | >=1 | sed | character | (y/n) if y, calib sed yld by lu in each reg | `matched` | sed | `verified` |
| nut_yn | string | - | - | nut | character | (y/n) if y, calib nut bal by lu in each reg | `matched` | nut | `verified` |
| ch_sed_yn | string | - | 0..3500 | chsed | character | (y/n), if y, calib chan widening/bank accretion by stream order | `matched` | - | `mismatch` |
| ch_nut_yn | string | - | 0..8 | chnut | character | (y/n), if y, calib chan nut bal by stream order | `matched` | - | `mismatch` |
| res_yn | string | - | 0..1000 | res | character | (y/n), if y, calib res budgets by res | `matched` | res | `verified` |

## cons_practice.lum

| Spreadsheet name | Type | Units | Range | Source name | Type | Description | Status | Editor DB name | Editor check |
|---|---|---|---|---|---|---|---|---|---|
| id | - | - | - | - | - | ID | `spreadsheet_only` (structural) | - | `mismatch` |
| name | string | - | - | name | character | P factor Class Name | `matched` | name | `verified` |
| treat1 | string | - | - | pfac | real | Treatment 1 | `matched` | - | `mismatch` |
| treat2 | string | - | - | pfac | real | Treatment 2 | `matched` | - | `mismatch` |
| min_slp | numeric | - | - | pfac | real | min slope for class | `matched` | - | `mismatch` |
| max_slp | numeric | - | - | pfac | real | max slope for class | `matched` | - | `mismatch` |
| usle_p | numeric | - | - | pfac | real | usle p factor | `matched` | usle_p | `verified` |
| slp_len_max | numeric | - | - | sl_len_mx | real | maximum slope length | `matched` | slp_len_max | `verified` |
| description | string | none | - | - | - | description | `spreadsheet_only` (structural) | - | `mismatch` |

## constituents.cs

| Spreadsheet name | Type | Units | Range | Source name | Type | Description | Status | Editor DB name | Editor check |
|---|---|---|---|---|---|---|---|---|---|
| id | integer | - | - | - | - | ID | `spreadsheet_only` (structural) | - | `mismatch` |
| num_pests | string | - | - | num_pests | integer | number of pesticide constituent names to follow on next line | `matched` | num_pests | `verified` |
| pest_cs_db | string | - | - | - | - | name of pesticide community (pesticide.com) | `spreadsheet_only` | - | `mismatch` |
| num_paths | string | - | - | num_paths | integer | number of pathogen names to follow on next line | `matched` | num_paths | `verified` |
| path_cs_db | string | - | - | - | - | name of pathogen communit (pathogens.pth) | `spreadsheet_only` | - | `mismatch` |
| num_metals | string | - | - | num_metals | integer | number of heavy metal names to follow on next line | `matched` | num_metals | `verified` |
| metal_cs_db | string | - | - | - | - | name of heavy metals community () | `spreadsheet_only` | - | `mismatch` |
| num_salts | string | - | - | num_salts | integer | number of salt names to follow on next line | `matched` | num_salts | `verified` |
| salt_cs_db | string | - | - | - | - | name of salt community () | `spreadsheet_only` | - | `mismatch` |
| other_cs_db | string | - | - | - | - | name of other constituents community | `spreadsheet_only` | - | `mismatch` |
| - | - | - | - | pests | character | name of the pesticides- points to pesticide database | `source_only` | - | - |
| - | - | - | - | paths | character | name of the pathogens- points to pathogens database | `source_only` | - | - |
| - | - | - | - | metals | character | name of the heavy metals- points to heavy metals database | `source_only` | - | - |
| - | - | - | - | salts | character | name of the salts - points to salts database | `source_only` | - | - |
| - | - | - | - | num_cs | integer | number of other constituents simulated | `source_only` | - | - |
| - | - | - | - | cs | character | name of the constituents - points to cs database | `source_only` | - | - |

## cs_aqu.ini

| Spreadsheet name | Type | Units | Range | Source name | Type | Description | Status | Editor DB name | Editor check |
|---|---|---|---|---|---|---|---|---|---|
| - | - | - | - | name | character | name of the constituent - points to constituent database | `source_only` | - | - |
| - | - | ppm | - | aqu | real | concentration, sorbed mass at start of simulation | `source_only` | - | - |

## cs_atmo.cli

| Spreadsheet name | Type | Units | Range | Source name | Type | Description | Status | Editor DB name | Editor check |
|---|---|---|---|---|---|---|---|---|---|
| - | - | - | - | station_name | character | station name | `source_only` | - | - |
| - | - | - | - | rf | real | concentration in rainfall - mg/l | `source_only` | - | - |
| - | - | - | - | dry | real | dry deposition - kg/ha/yr | `source_only` | - | - |
| - | - | - | - | rfmo | real | - | `source_only` | - | - |
| - | - | - | - | drymo | real | - | `source_only` | - | - |
| - | - | - | - | rfyr | real | - | `source_only` | - | - |
| - | - | - | - | dryyr | real | - | `source_only` | - | - |

## cs_channel.ini

| Spreadsheet name | Type | Units | Range | Source name | Type | Description | Status | Editor DB name | Editor check |
|---|---|---|---|---|---|---|---|---|---|
| - | - | - | - | name | character | name of the constituent - points to salt ion database | `source_only` | - | - |
| - | - | g/m3 | - | conc | real | constituent concentration at start of simulation | `source_only` | - | - |

## cs_hru.ini

| Spreadsheet name | Type | Units | Range | Source name | Type | Description | Status | Editor DB name | Editor check |
|---|---|---|---|---|---|---|---|---|---|
| - | - | - | - | name | character | name of the constituent - points to constituent database | `source_only` | - | - |
| - | - | ppm | - | soil | real | amount of constituent in soil at start of simulation | `source_only` | - | - |
| - | - | ppm or #cfu/m^2 | - | plt | real | amount of constituent on plant at start of simulation | `source_only` | - | - |

## cs_recall.rec

| Spreadsheet name | Type | Units | Range | Source name | Type | Description | Status | Editor DB name | Editor check |
|---|---|---|---|---|---|---|---|---|---|
| - | - | - | - | k | integer | - | `source_only` | - | - |
| - | - | - | - | name | character | - | `source_only` | - | - |
| - | - | - | - | typ | integer | recall type - 1=day, 2=mon, 3=year | `source_only` | - | - |
| - | - | - | - | filename | character | filename | `source_only` | - | - |
| - | - | - | - | nbyr | integer | - | `source_only` | - | - |
| - | - | - | - | jday | integer | - | `source_only` | - | - |
| - | - | - | - | mo | integer | - | `source_only` | - | - |
| - | - | - | - | day_mo | integer | - | `source_only` | - | - |
| - | - | - | - | iyr | integer | - | `source_only` | - | - |
| - | - | - | - | ob_typ | character | - | `source_only` | - | - |
| - | - | - | - | ob_name | character | - | `source_only` | - | - |
| - | - | - | - | cs | real | constituent mass (kg/ha) | `source_only` | - | - |

## delratio.con

| Spreadsheet name | Type | Units | Range | Source name | Type | Description | Status | Editor DB name | Editor check |
|---|---|---|---|---|---|---|---|---|---|
| id | integer | none | - | num | integer | delivery ratio number | `matched` | id | `verified` |
| name | string | - | - | name | character | The name of the connect unit | `matched` | name | `verified` |
| gis_id | string | - | - | gis_id | integer | GIS id | `matched` | gis_id | `verified` |
| area | numeric | ha | - | area_ha | real | AREA | `matched` | area | `verified` |
| lat | numeric | dec degrees | -90..90 | lat | real | latitude | `matched` | lat | `verified` |
| lon | numeric | dec degrees | -180..180 | long | real | longitude | `matched` | lon | `verified` |
| elev | numeric | m | 1..7000 | elev | real | Elevation of DR | `matched` | elev | `verified` |
| dlr | integer | - | - | - | - | DEL OBJECT | `spreadsheet_only` | - | `mismatch` |
| wst | string | - | - | wst_c | character | weather station number | `matched` | wst | `verified` |
| cst | integer | - | - | constit | integer | Constituent data pointer to pesticides, pathogens, metals, salts | `matched` | cst | `verified` |
| ovfl | numeric | - | - | props2 | integer | Points to the connections of spatial objects for overbank flooding | `matched` | ovfl | `verified` |
| rule | integer | - | - | ruleset | character | Ruleset pointer for flow fraction of hydrograph | `matched` | rule | `verified` |
| out_tot | integer | - | 1..12 | src_tot | integer | Total number of outgoing objects | `matched` | out_tot | `verified` |
| dlr_id | integer | - | - | - | - | number | `spreadsheet_only` (structural) | - | `mismatch` |
| obj_numb | integer | - | 1..10 | - | - | Object number 1-10 | `spreadsheet_only` (structural) | - | `mismatch` |
| obj_typ | string | - | - | obtyp_out | character | Outflow object type | `matched` | obj_typ | `verified` |
| obj_id | integer | - | - | obtypno_out | integer | Outflow object identifier for specified type | `matched` | obj_id | `verified` |
| hyd_typ | string | - | - | htyp_out | character | Outflow hydrograph type | `matched` | hyd_typ | `verified` |
| frac | numeric | - | 0..1 | frac_out | real | Fraction of hydrograph set to object | `matched` | frac | `verified` |
| description | string | none | - | - | - | - | `spreadsheet_only` (structural) | - | `mismatch` |
| - | - | - | - | props | integer | properties number from data base (ie hru.dat, sub.dat) - change props to data | `source_only` | - | - |

## delratio.del

| Spreadsheet name | Type | Units | Range | Source name | Type | Description | Status | Editor DB name | Editor check |
|---|---|---|---|---|---|---|---|---|---|
| id | - | - | - | - | - | ID | `spreadsheet_only` (structural) | - | `mismatch` |
| name | string | - | - | name | character | name of dr | `matched` | name | `verified` |
| om_file | string | - | - | om_file | character | name of org_matter | `matched` | - | `mismatch` |
| pest_file | string | - | - | pest_file | character | name of pesticide | `matched` | - | `mismatch` |
| path_file | string | - | - | path_file | character | name of pathogen | `matched` | - | `mismatch` |
| hmet_file | string | - | - | hmet_file | character | name of heavy metal | `matched` | - | `mismatch` |
| salts_file | string | - | - | salts_file | character | name of salt | `matched` | - | `mismatch` |

## dr_hmet.del

| Spreadsheet name | Type | Units | Range | Source name | Type | Description | Status | Editor DB name | Editor check |
|---|---|---|---|---|---|---|---|---|---|
| id | - | - | - | - | - | ID | `spreadsheet_only` (structural) | - | `unavailable` |
| name | string | - | - | - | - | name of the delivery ratio heavy metals | `spreadsheet_only` | - | `unavailable` |
| hmet_dr_sol | numeric | - | - | - | - | soluble constituent mass | `spreadsheet_only` | - | `unavailable` |
| hmet_dr_sor | numeric | - | - | - | - | sorbed constituent mass | `spreadsheet_only` | - | `unavailable` |
| - | - | - | - | dr_hmet_name | character | - | `source_only` | - | - |
| - | - | - | - | hmet | real | heavy metals delivery | `source_only` | - | - |

## dr_om.del

| Spreadsheet name | Type | Units | Range | Source name | Type | Description | Status | Editor DB name | Editor check |
|---|---|---|---|---|---|---|---|---|---|
| id | - | - | - | - | - | ID | `spreadsheet_only` (structural) | - | `mismatch` |
| name | string | - | - | dr_om_name | character | name of the delivery ratio | `matched` | name | `verified` |
| flo | numeric | m^3 | - | flo | real | volume of water | `matched` | flo | `verified` |
| sed | numeric | metric ton | - | sed | real | sediment | `matched` | sed | `verified` |
| orgn | numeric | kg N | - | orgn | real | organic N | `matched` | orgn | `verified` |
| sedp | numeric | kg P | - | sedp | real | organic P | `matched` | sedp | `verified` |
| no3 | numeric | kg N | - | no3 | real | NO3-N | `matched` | no3 | `verified` |
| solp | numeric | kg P | - | solp | real | mineral (soluble P) | `matched` | solp | `verified` |
| chla | numeric | kg | - | chla | real | chlorophyll-a | `matched` | chla | `verified` |
| nh3 | numeric | kg N | - | nh3 | real | NH3 | `matched` | nh3 | `verified` |
| no2 | numeric | kg _N | - | no2 | real | NO2 | `matched` | no2 | `verified` |
| cbod | numeric | kg | - | cbod | real | carbonaceous biological oxygen demand | `matched` | cbod | `verified` |
| dox | numeric | kg | - | dox | real | dissolved oxygen | `matched` | dox | `verified` |
| san | numeric | tons | - | san | real | detached sand | `matched` | - | `mismatch` |
| sil | numeric | tons | - | sil | real | detached silt | `matched` | - | `mismatch` |
| cla | numeric | tons | - | cla | real | detached clay | `matched` | - | `mismatch` |
| sag | numeric | tons | - | sag | real | detached small ag | `matched` | sag | `verified` |
| lag | numeric | tons | - | lag | real | detached large ag | `matched` | lag | `verified` |
| grv | numeric | tons | - | grv | real | gravel | `matched` | - | `mismatch` |
| temp | numeric | deg c | - | temp | real | temperature | `matched` | - | `mismatch` |

## dr_path.del

| Spreadsheet name | Type | Units | Range | Source name | Type | Description | Status | Editor DB name | Editor check |
|---|---|---|---|---|---|---|---|---|---|
| id | - | - | - | - | - | ID | `spreadsheet_only` (structural) | - | `unavailable` |
| name | string | - | - | - | - | name of the delivery ratio pathogens | `spreadsheet_only` | - | `unavailable` |
| path_dr_sol | numeric | - | - | - | - | soluble constituent mass | `spreadsheet_only` | - | `unavailable` |
| path_dr_sor | numeric | - | - | - | - | sorbed constituent mass | `spreadsheet_only` | - | `unavailable` |
| - | - | - | - | dr_path_name | character | - | `source_only` | - | - |
| - | - | - | - | path | real | pathogen delivery | `source_only` | - | - |

## dr_pest.del

| Spreadsheet name | Type | Units | Range | Source name | Type | Description | Status | Editor DB name | Editor check |
|---|---|---|---|---|---|---|---|---|---|
| id | - | - | - | - | - | ID | `spreadsheet_only` (structural) | - | `unavailable` |
| name | string | - | - | - | - | name of the deliver ratio pests | `spreadsheet_only` | - | `unavailable` |
| pest_dr_sol | numeric | - | - | - | - | soluble constituent mass | `spreadsheet_only` | - | `unavailable` |
| pest_dr_sor | numeric | - | - | - | - | sorbed constituent mass | `spreadsheet_only` | - | `unavailable` |
| - | - | - | - | dr_pest_name | character | - | `source_only` | - | - |
| - | - | - | - | pest | real | pesticide delivery | `source_only` | - | - |

## dr_salt.del

| Spreadsheet name | Type | Units | Range | Source name | Type | Description | Status | Editor DB name | Editor check |
|---|---|---|---|---|---|---|---|---|---|
| id | - | - | - | - | - | ID | `spreadsheet_only` (structural) | - | `unavailable` |
| name | string | - | - | - | - | name of the delivery ratio salt | `spreadsheet_only` | - | `unavailable` |
| salt_dr_sol | numeric | - | - | - | - | soluble constituent mass | `spreadsheet_only` | - | `unavailable` |
| salt_dr_sor | numeric | - | - | - | - | sorbed constituent mass | `spreadsheet_only` | - | `unavailable` |
| - | - | - | - | dr_salt_name | character | - | `source_only` | - | - |
| - | - | - | - | salt | real | salts delivery | `source_only` | - | - |

## element.ccu

| Spreadsheet name | Type | Units | Range | Source name | Type | Description | Status | Editor DB name | Editor check |
|---|---|---|---|---|---|---|---|---|---|
| - | - | - | - | k | integer | - | `source_only` | - | - |
| - | - | - | - | name | character | - | `source_only` | - | - |
| - | - | - | - | obtyp | character | object type- 1=hru, 2=hru_lte, 11=export coef, etc | `source_only` | - | - |
| - | - | - | - | obtypno | integer | 2-number of hru_lte"s or 1st hru_lte command | `source_only` | - | - |
| - | - | - | - | bsn_frac | real | fraction of element in basin (expansion factor) | `source_only` | - | - |
| - | - | - | - | ru_frac | real | fraction of element in ru (expansion factor) | `source_only` | - | - |
| - | - | - | - | reg_frac | real | fraction of element in calibration region (expansion factor) | `source_only` | - | - |

## exco.con

| Spreadsheet name | Type | Units | Range | Source name | Type | Description | Status | Editor DB name | Editor check |
|---|---|---|---|---|---|---|---|---|---|
| id | integer | - | - | num | integer | number | `matched` | id | `verified` |
| name | string | - | - | name | character | The name of the connect unit | `matched` | name | `verified` |
| gis_id | string | - | - | gis_id | integer | GIS id | `matched` | gis_id | `verified` |
| area | numeric | ha | - | area_ha | real | AREA | `matched` | area | `verified` |
| lat | numeric | dec degrees | -90..90 | lat | real | latitude | `matched` | lat | `verified` |
| lon | numeric | dec degrees | -180..180 | long | real | longitude | `matched` | lon | `verified` |
| elev | numeric | m | 1..7000 | elev | real | Elevation of recall | `matched` | elev | `verified` |
| exco | integer | - | - | props | integer | EXCO OBJECT | `matched` | exco | `verified` |
| wst | string | - | - | wst_c | character | weather station name | `matched` | wst | `verified` |
| cst | integer | - | - | constit | integer | Constituent data pointer to pesticides, pathogens, metals, salts | `matched` | cst | `verified` |
| ovfl | numeric | - | - | props2 | integer | Points to the connections of spatial objects for overbank flooding | `matched` | ovfl | `verified` |
| rule | integer | - | - | ruleset | character | Ruleset pointer for flow fraction of hydrograph | `matched` | rule | `verified` |
| out_tot | integer | - | 1..12 | src_tot | integer | Total number of outgoing objects | `matched` | out_tot | `verified` |
| exco_id | integer | - | - | - | - | number | `spreadsheet_only` (structural) | - | `mismatch` |
| obj_numb | integer | - | 1..10 | - | - | Object number 1-10 | `spreadsheet_only` (structural) | - | `mismatch` |
| obj_typ | string | - | - | obtyp_out | character | Outflow object type | `matched` | obj_typ | `verified` |
| obj_id | integer | - | - | obtypno_out | integer | Outflow object identifier for specified type | `matched` | obj_id | `verified` |
| hyd_typ | string | - | - | htyp_out | character | Outflow hydrograph type | `matched` | hyd_typ | `verified` |
| frac | numeric | - | 0..1 | frac_out | real | Fraction of hydrograph set to object | `matched` | frac | `verified` |
| description | string | none | - | - | - | - | `spreadsheet_only` (structural) | - | `mismatch` |

## exco.exc

| Spreadsheet name | Type | Units | Range | Source name | Type | Description | Status | Editor DB name | Editor check |
|---|---|---|---|---|---|---|---|---|---|
| id | - | - | - | - | - | ID | `spreadsheet_only` (structural) | - | `mismatch` |
| name | string | - | - | name | character | name of exco | `matched` | name | `verified` |
| om_file | string | - | - | om_file | character | name of org_matter | `matched` | - | `mismatch` |
| pest_file | string | - | - | pest_file | character | name of pesticide | `matched` | - | `mismatch` |
| path_file | string | - | - | path_file | character | name of pathogen | `matched` | - | `mismatch` |
| hmet_file | string | - | - | hmet_file | character | name of heavy metal | `matched` | - | `mismatch` |
| salts_file | string | - | - | salts_file | character | name of salt | `matched` | - | `mismatch` |
| - | - | - | - | k | integer | - | `source_only` | - | - |
| - | - | - | - | constit_file | character | - | `source_only` | - | - |
| - | - | - | - | descrip | character | - | `source_only` | - | - |

## exco_hmet.exc

| Spreadsheet name | Type | Units | Range | Source name | Type | Description | Status | Editor DB name | Editor check |
|---|---|---|---|---|---|---|---|---|---|
| id | - | - | - | - | - | ID | `spreadsheet_only` (structural) | - | `mismatch` |
| name | string | - | - | exco_hmet_name | character | name of the exco heavy metals | `matched` | name | `verified` |
| hmet_sol | numeric | - | - | - | - | soluble constituent mass | `spreadsheet_only` | - | `mismatch` |
| hmet_sor | numeric | - | - | - | - | sorbed constituent mass | `spreadsheet_only` | - | `mismatch` |
| - | - | - | - | hmet | real | heavy metals hydrographs | `source_only` | - | - |

## exco_om.exc

| Spreadsheet name | Type | Units | Range | Source name | Type | Description | Status | Editor DB name | Editor check |
|---|---|---|---|---|---|---|---|---|---|
| id | - | - | - | - | - | ID | `spreadsheet_only` (structural) | - | `mismatch` |
| name | string | name | - | exco_om_name | character | name of the export coefficient | `matched` | name | `verified` |
| flo | numeric | m^3 | - | flo | real | volume of water | `matched` | flo | `verified` |
| sed | numeric | met tons | - | sed | real | sediment | `matched` | sed | `verified` |
| orgn | numeric | kg N | - | orgn | real | organic N | `matched` | orgn | `verified` |
| sedp | numeric | kg P | - | sedp | real | organic P | `matched` | sedp | `verified` |
| no3 | numeric | kg N | - | no3 | real | NO3-N | `matched` | no3 | `verified` |
| solp | numeric | kg P | - | solp | real | mineral (soluble P) | `matched` | solp | `verified` |
| chla | numeric | kg | - | chla | real | chlorophyll-a | `matched` | chla | `verified` |
| nh3 | numeric | kg N | - | nh3 | real | NH3 | `matched` | nh3 | `verified` |
| no2 | numeric | kg _N | - | no2 | real | NO2 | `matched` | no2 | `verified` |
| cbod | numeric | kg | - | cbod | real | carbonaceous biological oxygen demand | `matched` | cbod | `verified` |
| dox | numeric | kg | - | dox | real | dissolved oxygen | `matched` | dox | `verified` |
| san | numeric | tons | - | san | real | detached sand | `matched` | - | `mismatch` |
| sil | numeric | tons | - | sil | real | detached silt | `matched` | - | `mismatch` |
| cla | numeric | tons | - | cla | real | detached clay | `matched` | - | `mismatch` |
| sag | numeric | tons | - | sag | real | detached small ag | `matched` | sag | `verified` |
| lag | numeric | tons | - | lag | real | detached large ag | `matched` | lag | `verified` |
| grv | numeric | tons | - | grv | real | gravel | `matched` | - | `mismatch` |
| temp | numeric | deg c | - | temp | real | temperature | `matched` | - | `mismatch` |

## exco_path.exc

| Spreadsheet name | Type | Units | Range | Source name | Type | Description | Status | Editor DB name | Editor check |
|---|---|---|---|---|---|---|---|---|---|
| id | - | - | - | - | - | ID | `spreadsheet_only` (structural) | - | `mismatch` |
| name | string | - | - | exco_path_name | character | name of the exco pathogens | `matched` | name | `verified` |
| path_sol | numeric | - | - | - | - | soluble constituent mass | `spreadsheet_only` | - | `mismatch` |
| path_sor | numeric | - | - | - | - | sorbed constituent mass | `spreadsheet_only` | - | `mismatch` |
| - | - | - | - | path | real | pesticide hydrographs | `source_only` | - | - |

## exco_pest.exc

| Spreadsheet name | Type | Units | Range | Source name | Type | Description | Status | Editor DB name | Editor check |
|---|---|---|---|---|---|---|---|---|---|
| id | - | - | - | - | - | ID | `spreadsheet_only` (structural) | - | `mismatch` |
| name | string | - | - | exco_pest_name | character | name of the exco pest | `matched` | name | `verified` |
| pest_sol | numeric | - | - | - | - | soluble constituent mass | `spreadsheet_only` | - | `mismatch` |
| pest_sor | numeric | - | - | - | - | sorbed constituent mass | `spreadsheet_only` | - | `mismatch` |
| - | - | - | - | pest | real | pesticide hydrographs | `source_only` | - | - |

## exco_salt.exc

| Spreadsheet name | Type | Units | Range | Source name | Type | Description | Status | Editor DB name | Editor check |
|---|---|---|---|---|---|---|---|---|---|
| id | - | - | - | - | - | ID | `spreadsheet_only` (structural) | - | `mismatch` |
| name | string | - | - | exco_salt_name | character | name of the exco salts | `matched` | name | `verified` |
| salt_sol | numeric | - | - | - | - | soluble constituent mass | `spreadsheet_only` | - | `mismatch` |
| salt_sor | numeric | - | - | - | - | sorbed constituent mass | `spreadsheet_only` | - | `mismatch` |
| - | - | - | - | salt | real | salts hydrographs | `source_only` | - | - |

## fertilizer.frt

| Spreadsheet name | Type | Units | Range | Source name | Type | Description | Status | Editor DB name | Editor check |
|---|---|---|---|---|---|---|---|---|---|
| id | - | - | - | - | - | ID | `spreadsheet_only` (structural) | - | `mismatch` |
| name | string | - | - | fertnm | character | Fertilizer name | `matched` | name | `verified` |
| description | String | - | - | - | - | Description, not used in the model | `spreadsheet_only` (structural) | - | `mismatch` |
| min_n | numeric | fraction | 0..1 | fminn | real | Fraction of fertilizer that is mineral N (NO3+NH3) | `matched` | min_n | `verified` |
| min_p | numeric | fraction | 0..1 | fminp | real | Fraction of fertilizer that is mineral P | `matched` | min_p | `verified` |
| org_n | numeric | fraction | 0..1 | forgn | real | Fraction of fertilizer that is org N | `matched` | org_n | `verified` |
| org_p | numeric | fraction | 0..1 | forgp | real | Fraction of fertilizer that is org P | `matched` | org_p | `verified` |
| nh3_n | numeric | fraction | 0..1 | fnh3n | real | Fraction of mineral N content of fertilizer that is NH3 | `matched` | nh3_n | `verified` |

## fertilizer.frt_cs

| Spreadsheet name | Type | Units | Range | Source name | Type | Description | Status | Editor DB name | Editor check |
|---|---|---|---|---|---|---|---|---|---|
| - | - | - | - | fertnm | character | - | `source_only` | - | - |
| - | - | kg seo4/ha | - | seo4 | real | fertilizer load of seo4 (kg/ha) | `source_only` | - | - |
| - | - | kg seo3/ha | - | seo3 | real | fertilizer load of seo3 (kg/ha) | `source_only` | - | - |
| - | - | kg boron/ha | - | boron | real | fertilizer load of boron (kg/ha) | `source_only` | - | - |

## field.fld

| Spreadsheet name | Type | Units | Range | Source name | Type | Description | Status | Editor DB name | Editor check |
|---|---|---|---|---|---|---|---|---|---|
| id | - | - | - | - | - | ID | `spreadsheet_only` (structural) | - | `mismatch` |
| name | string | - | - | name | character | field name | `matched` | name | `verified` |
| len | numeric | - | - | length | real | field length | `matched` | len | `verified` |
| wd | numeric | - | - | wid | real | field width | `matched` | wd | `verified` |
| ang | numeric | - | - | ang | real | field angle | `matched` | ang | `verified` |

## filterstrip.str

| Spreadsheet name | Type | Units | Range | Source name | Type | Description | Status | Editor DB name | Editor check |
|---|---|---|---|---|---|---|---|---|---|
| id | - | - | - | - | - | ID | `spreadsheet_only` (structural) | - | `mismatch` |
| name | string | - | - | name | character | Filterstrip name | `matched` | name | `verified` |
| description | string | - | - | - | - | Description, not used in the model | `spreadsheet_only` (structural) | - | `mismatch` |
| flag | numeric | none | 0..1 | vfsi | integer | Initial SCS curve number II value | `matched` | flag | `verified` |
| fld_vfs | numeric | ratio | 0..300 | vfsratio | real | Contouring USLE P factor | `matched` | fld_vfs | `verified` |
| con_vfs | numeric | fraction | 0.25..0.75 | vfscon | real | fraction of the total runoff from the entire field | `matched` | con_vfs | `verified` |
| cha_q | numeric | % | 0..100 | vfsch | real | fraction of flow entering the most concentrated 10% of the VFS which is fully channelized | `matched` | cha_q | `verified` |

## fire.ops

| Spreadsheet name | Type | Units | Range | Source name | Type | Description | Status | Editor DB name | Editor check |
|---|---|---|---|---|---|---|---|---|---|
| id | - | - | - | - | - | ID | `spreadsheet_only` (structural) | - | `mismatch` |
| name | string | - | - | name | character | Fire name | `matched` | name | `verified` |
| description | string | - | - | - | - | Description, not used in the model | `spreadsheet_only` (structural) | - | `mismatch` |
| chg_cn2 | numeric | - | - | cn2_upd | real | Change in SCS curve number II value | `matched` | chg_cn2 | `verified` |
| frac_burn | numeric | fraction | 0..100 | fr_burn | real | Fraction burned | `matched` | frac_burn | `verified` |

## flo_con.dtl

| Spreadsheet name | Type | Units | Range | Source name | Type | Description | Status | Editor DB name | Editor check |
|---|---|---|---|---|---|---|---|---|---|
| id | - | - | - | - | - | ID | `spreadsheet_only` (structural) | - | `mismatch` |
| mdtbl | string | - | - | - | - | - | `spreadsheet_only` | - | `mismatch` |
| description | string | - | - | - | - | Description, not used in the model | `spreadsheet_only` (structural) | - | `mismatch` |
| dtbl_name | string | - | - | name | character | name of the decision table | `matched` | name | `verified` |
| conds | integer | - | - | conds | integer | number of conditions | `matched` | conds | `verified` |
| alts | integer | - | - | alts | integer | number of alternatives | `matched` | alts | `verified` |
| acts | integer | - | - | acts | integer | number of actions | `matched` | acts | `verified` |
| dtbl_name | string | - | - | name | character | name of the decision table | `matched` | name | `verified` |
| description | string | - | - | - | - | Description, not used in the model | `spreadsheet_only` (structural) | - | `mismatch` |
| cond_var | string | - | - | var | character | condition variable (ie volume, flow, sw, time, etc) | `matched` | var | `verified` |
| obj | string | - | - | ob | character | object variable (ie res, hru, canal, etc) | `matched` | obj | `verified` |
| obj_numb | integer | - | - | ob_num | integer | object number | `matched` | - | `mismatch` |
| lim_var | string | - | - | lim_var | character | limit variable (ie evol, pvol, fc, ul, etc) | `matched` | lim_var | `verified` |
| lim_op | string | - | - | lim_op | character | limit operator (*,+,-) | `matched` | lim_op | `verified` |
| lim_const | numeric | - | - | lim_const | real | limit constant | `matched` | lim_const | `verified` |
| alt1 | string | - | - | alt | character | condition alternatives | `matched` | alt | `verified` |
| alt2 | string | - | - | alt | character | condition alternatives | `matched` | alt | `verified` |
| alt3 | string | - | - | alt | character | condition alternatives | `matched` | alt | `verified` |
| alt4 | string | - | - | alt | character | condition alternatives | `matched` | alt | `verified` |
| alt5 | string | - | - | alt | character | condition alternatives | `matched` | alt | `verified` |
| alt6 | string | - | - | alt | character | condition alternatives | `matched` | alt | `verified` |
| alt7 | string | - | - | alt | character | condition alternatives | `matched` | alt | `verified` |
| alt8 | string | - | - | alt | character | condition alternatives | `matched` | alt | `verified` |
| alt9 | string | - | - | alt | character | condition alternatives | `matched` | alt | `verified` |
| alt10 | string | - | - | alt | character | condition alternatives | `matched` | alt | `verified` |
| dtbl_name | string | - | - | name | character | header for actions | `matched` | name | `verified` |
| description | string | - | - | - | - | Description, not used in the model | `spreadsheet_only` (structural) | - | `mismatch` |
| act_typ | string | - | - | typ | character | type of action | `matched` | act_typ | `verified` |
| obj | string | - | - | ob | character | action objects | `matched` | obj | `verified` |
| obj_num | string | - | - | ob_num | integer | action object number | `matched` | obj_num | `verified` |
| act_name | string | - | - | name | character | action name | `matched` | name | `verified` |
| act_option | string | - | - | option | character | action option | `matched` | option | `verified` |
| const | string | - | - | const | real | constant used for rate, days, etc. | `matched` | const | `verified` |
| const2 | string | - | - | const2 | real | constant used for rate, days, etc. | `matched` | const2 | `verified` |
| file_pointer | string | - | - | file_pointer | character | pointer for option (ie weir equation pointer) | `matched` | - | `mismatch` |
| out1 | string | - | - | act_outcomes | character | action outcomes ('y' to perform action; 'n' to not perform) | `matched` | - | `mismatch` |
| out2 | string | - | - | act_outcomes | character | action outcomes ('y' to perform action; 'n' to not perform) | `matched` | - | `mismatch` |
| out3 | string | - | - | act_outcomes | character | action outcomes ('y' to perform action; 'n' to not perform) | `matched` | - | `mismatch` |
| out4 | string | - | - | act_outcomes | character | action outcomes ('y' to perform action; 'n' to not perform) | `matched` | - | `mismatch` |
| out5 | string | - | - | act_outcomes | character | action outcomes ('y' to perform action; 'n' to not perform) | `matched` | - | `mismatch` |
| out6 | string | - | - | act_outcomes | character | action outcomes ('y' to perform action; 'n' to not perform) | `matched` | - | `mismatch` |
| out7 | string | - | - | act_outcomes | character | action outcomes ('y' to perform action; 'n' to not perform) | `matched` | - | `mismatch` |
| out8 | string | - | - | act_outcomes | character | action outcomes ('y' to perform action; 'n' to not perform) | `matched` | - | `mismatch` |
| out9 | string | - | - | act_outcomes | character | action outcomes ('y' to perform action; 'n' to not perform) | `matched` | - | `mismatch` |
| out10 | string | - | - | act_outcomes | character | action outcomes ('y' to perform action; 'n' to not perform) | `matched` | - | `mismatch` |

## floodplain.gw

| Spreadsheet name | Type | Units | Range | Source name | Type | Description | Status | Editor DB name | Editor check |
|---|---|---|---|---|---|---|---|---|---|
| - | - | - | - | gw_fp_cellid | integer | - | `source_only` | - | - |
| - | - | - | - | gw_fp_chanid | integer | - | `source_only` | - | - |
| - | - | - | - | gw_fp_K | real | - | `source_only` | - | - |
| - | - | - | - | gw_fp_area | real | - | `source_only` | - | - |

## grassedww.str

| Spreadsheet name | Type | Units | Range | Source name | Type | Description | Status | Editor DB name | Editor check |
|---|---|---|---|---|---|---|---|---|---|
| id | - | - | - | - | - | ID | `spreadsheet_only` (structural) | - | `mismatch` |
| name | string | - | - | name | character | Grassed waterway name | `matched` | name | `verified` |
| description | string | - | - | - | - | Description, not used in the model | `spreadsheet_only` (structural) | - | `mismatch` |
| flag | integer | none | 0..1 | grwat_i | integer | Grassed waterway flag (x=active;y=inactive) | `matched` | flag | `verified` |
| mann | numeric | none | 0.001..0.5 | grwat_n | real | Manning's n for grassed waterway | `matched` | mann | `verified` |
| sed_co | numeric | none | 0..1 | grwat_spcon | real | Sediment transport coefficient defined by user | `matched` | sed_co | `verified` |
| dp | numeric | m | 0..10 | grwat_d | real | Depth of grassed waterway | `matched` | dp | `verified` |
| wd | numeric | m | 0..1000 | grwat_w | real | Width of grassed waterway | `matched` | wd | `verified` |
| len | numeric | km | 0..10000 | grwat_l | real | Length of grassed waterway | `matched` | len | `verified` |
| slp | numeric | m/m | 0..1 | grwat_s | real | Slope of grassed waterway | `matched` | slp | `verified` |

## graze.ops

| Spreadsheet name | Type | Units | Range | Source name | Type | Description | Status | Editor DB name | Editor check |
|---|---|---|---|---|---|---|---|---|---|
| id | - | - | - | - | - | ID | `spreadsheet_only` (structural) | - | `mismatch` |
| name | string | - | - | name | character | Grazing operation name | `matched` | name | `verified` |
| description | string | - | - | - | - | Description, not used in the model | `spreadsheet_only` (structural) | - | `mismatch` |
| fert_name | string | - | - | fertnm | character | Fertilizer name for manure deposited during grazing | `matched` | - | `mismatch` |
| bm_eat | numeric | kg/ha | 0..500 | eat | real | Dry weight of biomass removed by grazing daily | `matched` | bm_eat | `verified` |
| bm_tramp | numeric | kg/ha | 0..500 | tramp | real | Dry weight of biomass removed by trampling daily | `matched` | bm_tramp | `verified` |
| man_amt | numeric | kg/ha | 0..500 | manure | real | Dry weight of manure deposited | `matched` | man_amt | `verified` |
| grz_bm_min | numeric | kg/ha | 0..5000 | biomin | real | Minimum plant biomass for grazing to occur | `matched` | grz_bm_min | `verified` |

## gwflow.con

| Spreadsheet name | Type | Units | Range | Source name | Type | Description | Status | Editor DB name | Editor check |
|---|---|---|---|---|---|---|---|---|---|
| - | - | - | - | num | integer | spatial object number- ie hru number corresponding to sequential command number | `source_only` | - | - |
| - | - | - | - | name | character | - | `source_only` | - | - |
| - | - | - | - | gis_id | integer | this is the first column in hru_dat (doesn"t have to be sequential) gis number for database purposes | `source_only` | - | - |
| - | - | - | - | area_ha | real | input drainag area - ha | `source_only` | - | - |
| - | - | - | - | lat | real | latitude (degrees) | `source_only` | - | - |
| - | - | - | - | long | real | longitude (degrees) | `source_only` | - | - |
| - | - | - | - | elev | real | elevation (m) | `source_only` | - | - |
| - | - | - | - | props | integer | properties number from data base (ie hru.dat, sub.dat) - change props to data | `source_only` | - | - |
| - | - | - | - | wst_c | character | weather station name | `source_only` | - | - |
| - | - | - | - | constit | integer | constituent data pointer to pesticides, pathogens, metals, salts | `source_only` | - | - |
| - | - | - | - | props2 | integer | overbank connectivity pointer to landscape units - change props2 to overbank | `source_only` | - | - |
| - | - | - | - | ruleset | character | points to the name of the dtbl in flo_con.dtl for out flow control | `source_only` | - | - |
| - | - | - | - | src_tot | integer | total number of outgoing (source) objects | `source_only` | - | - |
| - | - | - | - | obtyp_out | character | outflow object type (ie 1=hru, 2=sd_hru, 3=sub, 4=chan, etc) | `source_only` | - | - |
| - | - | - | - | obtypno_out | integer | outflow object type name | `source_only` | - | - |
| - | - | - | - | htyp_out | character | outflow hyd type (ie 1=tot, 2= recharge, 3=surf, etc) | `source_only` | - | - |
| - | - | - | - | frac_out | real | fraction of hydrograph | `source_only` | - | - |

## gwflow.wetland

| Spreadsheet name | Type | Units | Range | Source name | Type | Description | Status | Editor DB name | Editor check |
|---|---|---|---|---|---|---|---|---|---|
| - | - | - | - | wet_name | character | - | `source_only` | - | - |
| - | - | - | - | thick_val | real | - | `source_only` | - | - |

## gwflow_canal.con

| Spreadsheet name | Type | Units | Range | Source name | Type | Description | Status | Editor DB name | Editor check |
|---|---|---|---|---|---|---|---|---|---|
| - | - | - | - | canal_id | integer | - | `source_only` | - | - |
| - | - | - | - | obj_tot | integer | - | `source_only` | - | - |

## harv.ops

| Spreadsheet name | Type | Units | Range | Source name | Type | Description | Status | Editor DB name | Editor check |
|---|---|---|---|---|---|---|---|---|---|
| name | string | - | - | name | character | Harvest operation name | `matched` | name | `verified` |
| description | string | - | - | - | - | Description, not used in the model | `spreadsheet_only` (structural) | - | `mismatch` |
| harv_typ | string | none | - | typ | character | Harvest Type (grain;biomass;residue;tree;tuber) | `matched` | harv_typ | `verified` |
| harv_idx | numeric | fraction | 0..1 | hi_ovr | real | Harvest index target specified at harvest (kg/ha)/(kg/ha) | `matched` | harv_idx | `verified` |
| harv_eff | numeric | fraction | 0..1 | eff | real | Harvest efficiency | `matched` | harv_eff | `verified` |
| harv_bm_min | numeric | kg/ha | - | bm_min | real | Minimum biomass to allow harvest | `matched` | harv_bm_min | `verified` |

## hmd.cli

| Spreadsheet name | Type | Units | Range | Source name | Type | Description | Status | Editor DB name | Editor check |
|---|---|---|---|---|---|---|---|---|---|
| hmd_file | string | - | - | - | - | Relative humidity file names | `spreadsheet_only` | - | `unavailable` |
| - | - | - | - | hmd_n | character | - | `source_only` | - | - |
| - | - | - | - | filename | character | - | `source_only` | - | - |

## hmet_hru.ini

| Spreadsheet name | Type | Units | Range | Source name | Type | Description | Status | Editor DB name | Editor check |
|---|---|---|---|---|---|---|---|---|---|
| id | - | - | - | - | - | ID | `spreadsheet_only` (structural) | - | `unavailable` |
| name | string | - | - | name | character | name of the constituent - points to constituent database | `matched` | - | `unavailable` |
| description | string | - | - | - | - | - | `spreadsheet_only` (structural) | - | `unavailable` |
| hmet_hru_soil | numeric | - | - | - | - | amt of constituent in soil at start of simulation | `spreadsheet_only` | - | `unavailable` |
| hmet_hru_plt | numeric | - | - | - | - | amt of constituent on plant at start of simulation | `spreadsheet_only` | - | `unavailable` |
| - | - | ppm | - | soil | real | amount of constituent in soil at start of simulation | `source_only` | - | - |
| - | - | ppm or #cfu/m^2 | - | plt | real | amount of constituent on plant at start of simulation | `source_only` | - | - |

## hru-data.hru

| Spreadsheet name | Type | Units | Range | Source name | Type | Description | Status | Editor DB name | Editor check |
|---|---|---|---|---|---|---|---|---|---|
| id | integer | none | - | k | integer | HRU number | `matched` | id | `verified` |
| name | string | - | - | name | character | HRU name | `matched` | name | `verified` |
| description | string | - | - | - | - | Description, not used in the model | `spreadsheet_only` (structural) | - | `mismatch` |
| topo | string | none | - | topo | character | Pointer to topography parameter file | `matched` | topo | `verified` |
| hydro | string | none | - | hyd | character | Pointer to hydrology parameter file | `matched` | hydro | `verified` |
| soil | string | none | - | soil | character | Pointer to soil parameter file | `matched` | soil | `verified` |
| soil_ini | string | none | - | soil_plant_init | character | Pointer to soil nutrient parameter file | `matched` | soil_plant_init | `verified` |
| surf_stor | string | none | - | surf_stor | character | Pointer to surface storage parameter file | `matched` | surf_stor | `verified` |
| snow | string | none | - | snow | character | Pointer to snow parameter file | `matched` | snow | `verified` |
| field | string | none | - | field | character | Pointer to field parameter file | `matched` | field | `verified` |
| - | - | - | - | land_use_mgt | character | - | `source_only` | - | - |

## hru-lte.con

| Spreadsheet name | Type | Units | Range | Source name | Type | Description | Status | Editor DB name | Editor check |
|---|---|---|---|---|---|---|---|---|---|
| id | integer | none | - | num | integer | HRU lite number | `matched` | id | `verified` |
| name | string | - | - | name | character | HRU lite name | `matched` | name | `verified` |
| gis_id | string | - | - | gis_id | integer | HRU lite GIS id | `matched` | gis_id | `verified` |
| area | numeric | ha | - | area_ha | real | Area | `matched` | area | `verified` |
| lat | numeric | dec degrees | -90..90 | lat | real | Latitude | `matched` | lat | `verified` |
| lon | numeric | dec degrees | -180..180 | long | real | Longitude | `matched` | lon | `verified` |
| elev | numeric | m | 1..7000 | elev | real | Elevation of HRU-LTE | `matched` | elev | `verified` |
| lhru | integer | none | - | props | integer | Pointer to HRU lite properties | `matched` | - | `mismatch` |
| wst | string | none | - | wst_c | character | Weather station number | `matched` | wst | `verified` |
| cst | integer | none | - | constit | integer | Pointer to constituent data (pesticides, pathogens, metals, salts) | `matched` | cst | `verified` |
| ovfl | numeric | none | - | props2 | integer | Pointer to the connections of spatial objects for overbank flooding | `matched` | ovfl | `verified` |
| rule | integer | none | - | ruleset | character | Pointer to ruleset for flow fraction of hydrograph | `matched` | rule | `verified` |
| out_tot | integer | none | 1..12 | src_tot | integer | Total number of outgoing hydrographs | `matched` | out_tot | `verified` |
| lhru_id | integer | none | - | - | - | HRU lite number | `spreadsheet_only` (structural) | - | `mismatch` |
| obj_numb | integer | none | 1..10 | - | - | Object number 1-10 | `spreadsheet_only` (structural) | - | `mismatch` |
| obj_typ | string | - | - | obtyp_out | character | Outflow object type | `matched` | obj_typ | `verified` |
| obj_id | integer | none | - | obtypno_out | integer | Outflow object identifier for specified type | `matched` | obj_id | `verified` |
| hyd_typ | string | - | - | htyp_out | character | Outflow hydrograph type | `matched` | hyd_typ | `verified` |
| frac | numeric | none | 0..1 | frac_out | real | Fraction of hydrograph set to object | `matched` | frac | `verified` |
| description | string | none | - | - | - | - | `spreadsheet_only` (structural) | - | `mismatch` |

## hru-lte.hru

| Spreadsheet name | Type | Units | Range | Source name | Type | Description | Status | Editor DB name | Editor check |
|---|---|---|---|---|---|---|---|---|---|
| id | integer | none | - | k | integer | HRU lite number | `matched` | id | `verified` |
| name | string | - | - | name | character | HRU lite name | `matched` | name | `verified` |
| area | numeric | km^2 | - | dakm2 | real | HRU lite drainage area | `matched` | area | `verified` |
| cn2 | numeric | none | - | cn2 | real | Condition II curve number | `matched` | cn2 | `verified` |
| cn3_swf | numeric | none | - | cn3_swf | real | soil water factor for cn3 0=fc; 1=saturation(porosity) | `matched` | cn3_swf | `verified` |
| t_conc | numeric | min | - | tc | real | Time of concentration | `matched` | t_conc | `verified` |
| soil_dp | numeric | mm | - | soildep | real | Soil profile depth | `matched` | soil_dp | `verified` |
| perc_co | numeric | - | 0..6000 | perco | real | Soil percolation coefficient | `matched` | perc_co | `verified` |
| slp | numeric | m/m | 0..0.6 | slope | real | Land surface slope | `matched` | slp | `verified` |
| slp_len | numeric | m | - | slopelen | real | Land surface slope length | `matched` | slp_len | `verified` |
| et_co | numeric | - | - | etco | real | ET coefficient | `matched` | et_co | `verified` |
| aqu_sp_yld | numeric | mm | - | sy | real | Specific yield of the shallow aquifer | `matched` | aqu_sp_yld | `verified` |
| alpha_bf | numeric | 1/days | - | abf | real | Alpha factor of groundwater | `matched` | alpha_bf | `verified` |
| revap | numeric | mm | - | revapc | real | Revap coefficient amount of ET from shallow aquifer | `matched` | revap | `verified` |
| rchg_dp | numeric | mm | - | percc | real | Percolation coefficient from shallow to deep aquifer | `matched` | rchg_dp | `verified` |
| sw_init | numeric | none | - | sw | real | Initial soil water (fraction of available water capacity) | `matched` | sw_init | `verified` |
| aqu_init | numeric | mm | - | gw | real | Initial shallow aquifer storage | `matched` | aqu_init | `verified` |
| aqu_sh_flo | numeric | mm | - | gwflow | real | Initial shallow aquifer flow | `matched` | aqu_sh_flo | `verified` |
| aqu_dp_flo | numeric | mm | - | gwdeep | real | Initial deep aquifer flow | `matched` | aqu_dp_flo | `verified` |
| snow_h2o | numeric | mm | - | snow | real | Initial snow water equivalent | `matched` | snow_h2o | `verified` |
| lat | numeric | dec degrees | - | xlat | real | Latitude | `matched` | lat | `verified` |
| soil_text | string | none | - | text | character | Soil texture | `matched` | soil_text | `verified` |
| trop_flag | string | none | - | tropical | character | Tropical flag (0=non-tropical;1=tropical) | `matched` | trop_flag | `verified` |
| grow_start | string | none | - | igrow1 | character | Start of growing season for non-tropical/start of monsoon initialization period for tropical | `matched` | grow_start | `verified` |
| grow_end | string | none | - | igrow2 | character | End of growing season for non-tropical/end of monsoon initialization period for tropical | `matched` | grow_end | `verified` |
| plnt_typ | string | - | - | plant | character | Plant type (as listed in plants.plt) | `matched` | plnt_typ | `verified` |
| stress | numeric | frac | - | stress | real | Plant stress (pest,root restriction, soil quality..) | `matched` | stress | `verified` |
| pet_flag | string | none | - | ipet | character | Potential ET method | `matched` | pet_flag | `verified` |
| irr_flag | string | none | - | irr | character | Irrigation code (0=no irrigation;1=irrigation) | `matched` | irr_flag | `verified` |
| irr_src | string | none | - | irrsrc | character | Irrigation source (0=outside of basin;1=shallow aquifer;2=deep aquifer) | `matched` | irr_src | `verified` |
| t_drain | numeric | hr | - | tdrain | real | Design subsurface tile drain time hr | `matched` | t_drain | `verified` |
| usle_k | numeric | none | - | uslek | real | USLE soil erodibility factor K | `matched` | usle_k | `verified` |
| usle_c | numeric | none | - | uslec | real | USLE cover factor C | `matched` | usle_c | `verified` |
| usle_p | numeric | none | - | uslep | real | USLE equation support practice factor P | `matched` | usle_p | `verified` |
| usle_ls | numeric | none | - | uslels | real | USLE equation slope length and slope factor LS | `matched` | usle_ls | `verified` |

## hru.con

| Spreadsheet name | Type | Units | Range | Source name | Type | Description | Status | Editor DB name | Editor check |
|---|---|---|---|---|---|---|---|---|---|
| id | integer | none | - | num | integer | HRU number | `matched` | id | `verified` |
| name | string | - | - | name | character | HRU name | `matched` | name | `verified` |
| gis_id | string | - | - | gis_id | integer | HRU GIS id | `matched` | gis_id | `verified` |
| area | numeric | ha | - | area_ha | real | Area | `matched` | area | `verified` |
| lat | numeric | dec degrees | -90..90 | lat | real | Latitude | `matched` | lat | `verified` |
| lon | numeric | dec degrees | -180..180 | long | real | Longitude | `matched` | lon | `verified` |
| elev | numeric | m | 1..7000 | elev | real | Elevation of HRU | `matched` | elev | `verified` |
| hru | integer | none | - | props | integer | Pointer to HRU properties | `matched` | - | `mismatch` |
| wst | string | none | - | wst_c | character | Weather station number | `matched` | wst | `verified` |
| cst | integer | none | - | constit | integer | Pointer to constituent data (pesticides, pathogens, metals, salts) | `matched` | cst | `verified` |
| ovfl | integer | none | - | props2 | integer | Pointer to the connections of spatial objects for overbank flooding | `matched` | ovfl | `verified` |
| rule | integer | none | - | ruleset | character | Pointer to ruleset for flow fraction of hydrograph | `matched` | rule | `verified` |
| out_tot | integer | none | 1..12 | src_tot | integer | Total number of outgoing hydrographs | `matched` | out_tot | `verified` |
| hru_id | integer | none | - | - | - | HRU number | `spreadsheet_only` (structural) | - | `mismatch` |
| obj_numb | integer | none | 1..10 | - | - | Object number 1-10 | `spreadsheet_only` (structural) | - | `mismatch` |
| obj_typ | string | - | - | obtyp_out | character | Outflow object type | `matched` | obj_typ | `verified` |
| obj_id | integer | none | - | obtypno_out | integer | Outflow object identifier for specified type | `matched` | obj_id | `verified` |
| hyd_typ | string | - | - | htyp_out | character | Outflow hydrograph type | `matched` | hyd_typ | `verified` |
| frac | numeric | none | 0..1 | frac_out | real | Fraction of hydrograph set to object | `matched` | frac | `verified` |
| description | string | none | - | - | - | - | `spreadsheet_only` (structural) | - | `mismatch` |

## hrucell.gw

| Spreadsheet name | Type | Units | Range | Source name | Type | Description | Status | Editor DB name | Editor check |
|---|---|---|---|---|---|---|---|---|---|
| - | - | - | - | hru_id | integer | - | `source_only` | - | - |
| - | - | - | - | hru_area | real | - | `source_only` | - | - |
| - | - | - | - | hru_cells | integer | - | `source_only` | - | - |
| - | - | - | - | poly_area | real | - | `source_only` | - | - |

## hyd-sed-lte.cha

| Spreadsheet name | Type | Units | Range | Source name | Type | Description | Status | Editor DB name | Editor check |
|---|---|---|---|---|---|---|---|---|---|
| id | integer | - | - | - | - | ID | `spreadsheet_only` (structural) | - | `mismatch` |
| name | string | - | - | name | character | Channel lite name | `matched` | name | `verified` |
| order | string | - | - | order | integer | Stream order | `matched` | order | `verified` |
| description | string | - | - | - | - | Description, not used in the model | `spreadsheet_only` (structural) | - | `mismatch` |
| wd | numeric | m | - | chw | real | Channel lite width | `matched` | wd | `verified` |
| dp | numeric | m | - | chd | real | Channel lite depth | `matched` | dp | `verified` |
| slp | numeric | m/m | - | chs | real | Channel lite slope | `matched` | slp | `verified` |
| len | numeric | km | - | chl | real | Channel lite length | `matched` | len | `verified` |
| mann | numeric | none | - | chn | real | Channel lite Manning's n | `matched` | mann | `verified` |
| k | numeric | mm/h | - | chk | real | Channel lite bottom conductivity | `matched` | k | `verified` |
| erod_fact | numeric | none | - | bank_exp | real | Channel lite erodibility factor (0=non-erosive channel;1=no resistance to erosion) | `matched` | erod_fact | `verified` |
| cov_fact | numeric | 0.-1.0 | - | cov | real | Channel lite cover factor (0=channel is completely protected from erosion by cover;1=no vegetative cover on channel) | `matched` | cov_fact | `verified` |
| sinu | numeric | 1-3 | - | sinu | real | sinuousity-ratio of channel length and straight line length | `matched` | sinu | `verified` |
| eq_slp | numeric | m/m | - | vcr_coef | real | Channel lite equilibrium channel slope | `matched` | eq_slp | `verified` |
| d50 | numeric | mm | - | d50 | real | Channel lite median sediment size | `matched` | d50 | `verified` |
| clay | numeric | % | - | ch_clay | real | Channel lite clay percent of bank and bed | `matched` | clay | `verified` |
| carbon | numeric | % | - | carbon | real | Carbon percent of bank and bed | `matched` | carbon | `verified` |
| dry_bd | numeric | t/m3 | - | ch_bd | real | Channel lite dry bulk density | `matched` | dry_bd | `verified` |
| side_slp | numeric | - | - | chss | real | Channel lite side slope | `matched` | side_slp | `verified` |
| bankfull_flo | numeric | - | - | bankfull_flo | real | Bank full flow rate | `matched` | bankfull_flo | `verified` |
| fps | numeric | m/m | 1e-06..0.1 | fps | real | flood plain slope | `matched` | fps | `verified` |
| fpn | numeric | - | - | fpn | real | flood plain Manning's n | `matched` | fpn | `verified` |
| n_conc | numeric | mg/kg | 0..300 | n_conc | real | nitrogen concentation in channel bank | `matched` | n_conc | `verified` |
| p_conc | numeric | mg/kg | 0..200 | p_conc | real | phosphorus concentration in channel bank | `matched` | p_conc | `verified` |
| p_bio | numeric | frac | 0..0.9 | p_bio | real | fraction of p in bank that is bioavailable | `matched` | p_bio | `verified` |

## hydrology.cha

| Spreadsheet name | Type | Units | Range | Source name | Type | Description | Status | Editor DB name | Editor check |
|---|---|---|---|---|---|---|---|---|---|
| id | - | - | - | - | - | ID | `spreadsheet_only` (structural) | - | `mismatch` |
| name | string | - | - | name | character | Channel hydrology parameter set name | `matched` | name | `verified` |
| description | string | - | - | - | - | Description, not used in the model | `spreadsheet_only` (structural) | - | `mismatch` |
| wd | numeric | m | 0..1000 | w | real | Average width of main channel | `matched` | wd | `verified` |
| dp | numeric | m | 0..30 | d | real | Average depth of main channel | `matched` | dp | `verified` |
| slp | numeric | m/m | 0..10 | s | real | Average slope of main channel | `matched` | slp | `verified` |
| len | numeric | km | 0..500 | l | real | Main channel length in subbasin | `matched` | len | `verified` |
| mann | numeric | none | 0..0.3 | n | real | Manning's n value for the channel | `matched` | mann | `verified` |
| k | numeric | mm/hr | 0..500 | k | real | Effective hydraulic conductivity of channel alluvium | `matched` | k | `verified` |
| wdr | numeric | m/m | 0..10000 | wdr | real | Channel width to depth ratio | `matched` | wdr | `verified` |
| alpha_bnk | numeric | days | 0..1 | alpha_bnk | real | Alpha factor for bank storage recession curve | `matched` | alpha_bnk | `verified` |
| side_slp | numeric | ratio | 0..5 | side | real | Change in horizontal distance per unit vertical distance | `matched` | side_slp | `verified` |

## hydrology.hyd

| Spreadsheet name | Type | Units | Range | Source name | Type | Description | Status | Editor DB name | Editor check |
|---|---|---|---|---|---|---|---|---|---|
| id | - | - | - | - | - | ID | `spreadsheet_only` (structural) | - | `mismatch` |
| name | string | none | - | name | character | HRU hydrology parameter set name | `matched` | name | `verified` |
| lat_ttime | numeric | days | 0..180 | lat_ttime | real | Exponential of the lateral flow travel time | `matched` | lat_ttime | `verified` |
| lat_sed | numeric | g/L | 0..5000 | lat_sed | real | Sediment concentration in lateral flow | `matched` | lat_sed | `verified` |
| can_max | numeric | mm | 0..100 | canmx | real | Maximum canopy storage | `matched` | can_max | `verified` |
| esco | numeric | none | 0..1 | esco | real | Soil evaporation compensation factor | `matched` | esco | `verified` |
| epco | numeric | none | 0..1 | epco | real | Plant water uptake compensation factor | `matched` | epco | `verified` |
| orgn_enrich | numeric | none | 0..5 | erorgn | real | Organic N enrichment ratio, if left blank the model will calculate for every event | `matched` | orgn_enrich | `verified` |
| orgp_enrich | numeric | none | 0..5 | erorgp | real | Organic P enrichment ratio, if left blank the model will calculate for every event | `matched` | orgp_enrich | `verified` |
| cn3_swf | numeric | % | 0..1 | cn3_swf | real | Soil water at cn3 0=fc; .99=near saturation | `matched` | cn3_swf | `verified` |
| bio_mix | numeric | none | - | biomix | real | Biological mixing efficiency | `matched` | bio_mix | `verified` |
| perco | numeric | % | - | perco | real | percolation coefficient -adjusts soil moisture for perc to occur (1.0 = fc) | `matched` | perco | `verified` |
| lat_orgn | numeric | mg/L | 0..200 | lat_orgn | real | Organic N concentration in lateral flow | `matched` | lat_orgn | `verified` |
| lat_orgp | numeric | mg/L | 0..200 | lat_orgp | real | Organic P concentration in lateral flow | `matched` | lat_orgp | `verified` |
| harg_pet | numeric | - | - | - | - | Coefficient related to radiation used in Hargreaves equation | `spreadsheet_only` | - | `mismatch` |
| latq_co | numeric | none | 0..0 | latq_co | real | plant ET curve number coefficient | `matched` | latq_co | `verified` |
| - | - | none | - | pet_co | real | coefficient related to radiation used in Hargreaves equation | `source_only` | - | - |

## hydrology.res

| Spreadsheet name | Type | Units | Range | Source name | Type | Description | Status | Editor DB name | Editor check |
|---|---|---|---|---|---|---|---|---|---|
| id | - | - | - | - | - | ID | `spreadsheet_only` (structural) | - | `mismatch` |
| name | string | - | - | name | character | Reservoir hydrology name | `matched` | name | `verified` |
| yr_op | integer | none | 0..9999 | iyres | integer | Year of the simulation that the reservoir becomes operational | `matched` | yr_op | `verified` |
| mon_op | integer | none | 1..12 | mores | integer | Month the reservoir becomes operational | `matched` | mon_op | `verified` |
| area_ps | numeric | ha | 1..3000 | psa | real | Reservoir surface area when reservoir is filled to principal spillway | `matched` | area_ps | `verified` |
| vol_ps | numeric | 10^4 m^3 | 15..3000 | pvol | real | Volume of water needed to fill the reservoir to the principal spillway (read in as 10^4 m^3 and converted to m^3) | `matched` | vol_ps | `verified` |
| area_es | numeric | ha or frac | 1..1000 | esa | real | Reservoir surface area when reservoir is filled to emergency spillway | `matched` | area_es | `verified` |
| vol_es | numeric | 10^4 m^3 | 10..100 | evol | real | Volume of water needed to fill the reservoir to the emergency spillway (read in as 10^4 m^3 and converted to m^3) | `matched` | vol_es | `verified` |
| k | numeric | mm/hr | 0..1 | k | real | Hydraulic conductivity of the reservoir bottom | `matched` | k | `verified` |
| evap_co | numeric | none | 0..1 | evrsv | real | Lake evaporation coefficient | `matched` | evap_co | `verified` |
| shp_co1 | numeric | none | - | br1 | real | Shape coefficient for reservoirs (model estimates if zero) | `matched` | shp_co1 | `verified` |
| shp_co2 | numeric | none | - | br2 | real | Shape coefficient for reservoirs (model estimates if zero) | `matched` | shp_co2 | `verified` |

## hydrology.wet

| Spreadsheet name | Type | Units | Range | Source name | Type | Description | Status | Editor DB name | Editor check |
|---|---|---|---|---|---|---|---|---|---|
| name | string | - | - | name | character | hydrology wet name | `matched` | name | `verified` |
| hru_ps | numeric | frac | - | psa | real | frac of hru area at principal spillway | `matched` | hru_ps | `verified` |
| dp_ps | numeric | none | - | pdep | real | ave depth of water at principal spillway | `matched` | dp_ps | `verified` |
| hru_es | numeric | none | - | esa | real | frac of hru area at emergency spillway | `matched` | hru_es | `verified` |
| dp_es | numeric | none | - | edep | real | ave depth of water at emergency spillway | `matched` | dp_es | `verified` |
| k | numeric | none | - | k | real | hydraulic conductivity of the res bottom | `matched` | k | `verified` |
| evap | numeric | none | - | evrsv | real | lake evap coef | `matched` | evap | `verified` |
| vol_area_co | numeric | none | - | acoef | real | vol-surface area coef for hru impoundment | `matched` | vol_area_co | `verified` |
| vol_dp_a | numeric | none | - | bcoef | real | vol-depth coef for hru impoundment | `matched` | vol_dp_a | `verified` |
| vol_dp_b | numeric | none | - | ccoef | real | vol-depth coef for hru impoundment | `matched` | vol_dp_b | `verified` |
| hru_frac | numeric | none | - | frac | real | frac of hru that drains into impoundment | `matched` | hru_frac | `verified` |

## initial.aqu

| Spreadsheet name | Type | Units | Range | Source name | Type | Description | Status | Editor DB name | Editor check |
|---|---|---|---|---|---|---|---|---|---|
| name | string | - | - | name | character | Name of intial aquifer | `matched` | name | `verified` |
| org_min | string | - | - | org_min | character | Name of org-min | `matched` | org_min | `verified` |
| pest | string | - | - | pest | character | Name of pesticide | `matched` | pest | `verified` |
| path | string | - | - | path | character | Name of pathogens | `matched` | path | `verified` |
| hmet | string | - | - | hmet | character | Name of heavy metals | `matched` | hmet | `verified` |
| salt | string | - | - | salt | character | Name of salts | `matched` | salt | `verified` |

## initial.aqu_cs

| Spreadsheet name | Type | Units | Range | Source name | Type | Description | Status | Editor DB name | Editor check |
|---|---|---|---|---|---|---|---|---|---|
| - | - | - | - | name | character | xwalk with aqudb(iaqu)%aqu_ini | `source_only` | - | - |
| - | - | - | - | pest | character | points to initial pesticide input file | `source_only` | - | - |
| - | - | - | - | path | character | points to initial pathogen input file | `source_only` | - | - |
| - | - | - | - | hmet | character | points to initial heavy metals input file | `source_only` | - | - |
| - | - | - | - | salt | character | points to initial salt input file (salt_aqu.ini) | `source_only` | - | - |
| - | - | - | - | cs | character | points to initial constituent input file (cs_aqu.ini) | `source_only` | - | - |

## initial.cha

| Spreadsheet name | Type | Units | Range | Source name | Type | Description | Status | Editor DB name | Editor check |
|---|---|---|---|---|---|---|---|---|---|
| id | - | - | - | - | - | ID | `spreadsheet_only` (structural) | - | `mismatch` |
| name | string | - | - | name | character | Channel initial parameter set name | `matched` | name | `verified` |
| description | string | - | - | - | - | Description, not used in the model | `spreadsheet_only` (structural) | - | `mismatch` |
| ch_org_min | string | - | - | org_min | character | points to initial organic-mineral input file | `matched` | org_min | `verified` |
| ch_pest | string | - | - | pest | character | points to pesticide input file | `matched` | pest | `verified` |
| ch_path | string | - | - | path | character | points to pathogen input file | `matched` | path | `verified` |
| ch_hmet | string | - | - | hmet | character | points to heavy metal input file | `matched` | hmet | `verified` |
| ch_salt | string | - | - | salt | character | points to salt input file | `matched` | salt | `verified` |

## initial.cha_cs

| Spreadsheet name | Type | Units | Range | Source name | Type | Description | Status | Editor DB name | Editor check |
|---|---|---|---|---|---|---|---|---|---|
| - | - | - | - | name | character | - | `source_only` | - | - |
| - | - | - | - | pest | character | points to initial pesticide input file | `source_only` | - | - |
| - | - | - | - | path | character | points to initial pathogen input file | `source_only` | - | - |
| - | - | - | - | hmet | character | points to initial heavy metals input file | `source_only` | - | - |
| - | - | - | - | salt | character | points to initial salt input file | `source_only` | - | - |
| - | - | - | - | cs | character | points to initial constituent input file | `source_only` | - | - |

## initial.res

| Spreadsheet name | Type | Units | Range | Source name | Type | Description | Status | Editor DB name | Editor check |
|---|---|---|---|---|---|---|---|---|---|
| id | - | - | - | - | - | ID | `spreadsheet_only` (structural) | - | `mismatch` |
| name | string | - | - | init | character | Channel initial parameter set name | `matched` | name | `verified` |
| description | string | - | - | - | - | Description, not used in the model | `spreadsheet_only` (structural) | - | `mismatch` |
| res_org_min | string | - | - | org_min | character | points to initial organic-mineral input file | `matched` | org_min | `verified` |
| res_pest | string | - | - | pest | character | points to pesticide input file | `matched` | pest | `verified` |
| res_path | string | - | - | path | character | points to pathogen input file | `matched` | path | `verified` |
| res_hmet | string | - | - | hmet | character | points to heavy metal input file | `matched` | hmet | `verified` |
| res_salt | string | - | - | salt | character | points to salt input file | `matched` | salt | `verified` |

## irr.ops

| Spreadsheet name | Type | Units | Range | Source name | Type | Description | Status | Editor DB name | Editor check |
|---|---|---|---|---|---|---|---|---|---|
| id | - | - | - | - | - | ID | `spreadsheet_only` (structural) | - | `mismatch` |
| name | string | - | - | name | character | Irrigation operation name | `matched` | name | `verified` |
| description | string | - | - | - | - | Description, not used in the model | `spreadsheet_only` (structural) | - | `mismatch` |
| irr_amt | numeric | mm | 0..1 | amt_mm | real | irrigation application amount | `matched` | amt_mm | `verified` |
| irr_eff | numeric | - | 0..1 | eff | real | irrigation in-field efficiency | `matched` | eff_frac | `verified` |
| surq_rto | numeric | fraction | 0..100 | surq | real | surface runoff ratio | `matched` | sumq_frac | `verified` |
| irr_dep | numeric | mg/kg | - | dep_mm | real | depth of application for subsurface irrigation | `matched` | - | `mismatch` |
| irr_salt | numeric | mg/kg | - | salt | real | conc of total salt in irrigation | `matched` | - | `mismatch` |
| irr_no3n | numeric | mg/kg | - | no3 | real | conc of nitrate in irrigation | `matched` | - | `mismatch` |
| irr_po4 | numeric | mg/kg | - | po4 | real | conc of phosphate in irrigation | `matched` | - | `mismatch` |

## landuse.lum

| Spreadsheet name | Type | Units | Range | Source name | Type | Description | Status | Editor DB name | Editor check |
|---|---|---|---|---|---|---|---|---|---|
| id | - | - | - | - | - | ID | `spreadsheet_only` (structural) | - | `mismatch` |
| name | string | - | - | name | character | HRU landuse parameter set name | `matched` | name | `verified` |
| cal_grp | string | - | - | - | - | Calibration group | `spreadsheet_only` | - | `mismatch` |
| plnt_com | string | - | - | plant_cov | character | Pointer to plant community | `matched` | plnt_com | `verified` |
| mgt | string | - | - | mgt_ops | character | Pointer to management schedule | `matched` | mgt | `verified` |
| description | string | - | - | - | - | Description, not used in the model | `spreadsheet_only` (structural) | - | `mismatch` |
| cn2 | string | none | - | cn_lu | character | Pointer to curve number table | `matched` | cn2 | `verified` |
| cons_prac | string | none | 0..1 | cons_prac | character | USLE equation support practice (P) factor | `matched` | cons_prac | `verified` |
| urban | string | none | - | urb_lu | character | Pointer to urban database | `matched` | urban | `verified` |
| urb_ro | string | none | - | urb_ro | character | Urban runoff | `matched` | urb_ro | `verified` |
| ov_mann | string | none | - | ovn | character | Manning's n value for overland flow | `matched` | ov_mann | `verified` |
| tile | string | none | - | tiledrain | character | Pointer to tiledrain parameter set | `matched` | tile | `verified` |
| sep | string | none | - | septic | character | Pointer to septic system parameter set | `matched` | sep | `verified` |
| vfs | string | none | - | fstrip | character | Pointer to filterstrip parameter set | `matched` | vfs | `verified` |
| grww | string | none | - | grassww | character | Pointer to grassed waterways parameter set | `matched` | grww | `verified` |
| bmp | string | none | - | bmpuser | character | Pointer to best management practices parameter set | `matched` | bmp | `verified` |
| - | - | - | - | cal_group | character | calibration group (not currently used) | `source_only` | - | - |

## ls_reg.def

| Spreadsheet name | Type | Units | Range | Source name | Type | Description | Status | Editor DB name | Editor check |
|---|---|---|---|---|---|---|---|---|---|
| mreg | integer | - | - | - | - | landscape cataloging units regions define number | `spreadsheet_only` | - | `unavailable` |
| mlug | integer | - | - | - | - | landscape cataloging units regions define number | `spreadsheet_only` | - | `unavailable` |
| numb | integer | - | - | - | - | landscape cataloging units regions define number | `spreadsheet_only` | - | `unavailable` |
| reg_name | string | - | - | name | character | landscape cataloging units regions define name | `matched` | - | `unavailable` |
| reg_area | numeric | - | - | area_ha | real | landscape cataloging units regions define area | `matched` | - | `unavailable` |
| nspu | integer | - | - | nspu | integer | landscape cataloging units regions define elements | `matched` | - | `unavailable` |
| elem | integer | - | - | elem_cnt | integer | Element | `matched` | - | `unavailable` |
| - | - | - | - | k | integer | - | `source_only` | - | - |
| - | - | - | - | i | integer | - | `source_only` | - | - |
| - | - | - | - | num | integer | - | `source_only` | - | - |

## ls_reg.ele

| Spreadsheet name | Type | Units | Range | Source name | Type | Description | Status | Editor DB name | Editor check |
|---|---|---|---|---|---|---|---|---|---|
| id | integer | - | - | - | - | landscape cataloging units element number | `spreadsheet_only` | - | `unavailable` |
| name | string | - | - | name | character | landscape cataloging units element name | `matched` | - | `unavailable` |
| ha | - | - | - | ha | real | area of region element (ha) | `matched` | - | `unavailable` |
| obj_typ | string | - | - | obtyp | character | object type character | `matched` | - | `unavailable` |
| obj_typ_no | integer | - | - | obtypno | integer | object type | `matched` | - | `unavailable` |
| - | - | - | - | k | integer | - | `source_only` | - | - |

## ls_unit.def

| Spreadsheet name | Type | Units | Range | Source name | Type | Description | Status | Editor DB name | Editor check |
|---|---|---|---|---|---|---|---|---|---|
| id | integer | - | - | k | integer | - | `matched` | id | `verified` |
| lsu_numb | integer | - | - | - | - | landscape cataloging units define number | `spreadsheet_only` | - | `mismatch` |
| lsu_name | string | - | - | name | character | landscape cataloging units define name | `matched` | name | `verified` |
| area | numeric | - | - | area_ha | real | landscape cataloging units define area | `matched` | area | `verified` |
| elem_tot | integer | - | - | nspu | integer | landscape cataloging units define elements | `matched` | elem_tot | `verified` |
| lsu_numb | integer | none | - | - | - | landscape cataloging units define number | `spreadsheet_only` (structural) | - | `mismatch` |
| elem_numb | integer | none | 1..10 | - | - | 1-10 number of element group | `spreadsheet_only` (structural) | - | `mismatch` |
| elem | numeric | none | - | elem_cnt | integer | Element | `matched` | - | `mismatch` |

## ls_unit.ele

| Spreadsheet name | Type | Units | Range | Source name | Type | Description | Status | Editor DB name | Editor check |
|---|---|---|---|---|---|---|---|---|---|
| id | integer | - | - | - | - | landscape cataloging units element number | `spreadsheet_only` | id | `verified` |
| name | string | - | - | name | character | landscape cataloging units element name | `matched` | name | `verified` |
| obj_typ | string | - | - | obtyp | character | object type character | `matched` | obj_typ | `verified` |
| obj_typ_no | integer | - | - | obtypno | integer | object type | `matched` | obj_typ_no | `verified` |
| bsn_frac | numeric | - | - | bsn_frac | real | fraction of element in basin (expansion factor) | `matched` | bsn_frac | `verified` |
| ru_frac | numeric | - | - | ru_frac | real | fraction of element in ru (expansion factor) | `matched` | - | `mismatch` |
| - | - | - | - | k | integer | - | `source_only` | - | - |

## lsucell.gw

| Spreadsheet name | Type | Units | Range | Source name | Type | Description | Status | Editor DB name | Editor check |
|---|---|---|---|---|---|---|---|---|---|
| - | - | - | - | lsu | integer | - | `source_only` | - | - |
| - | - | - | - | lsu_area | real | - | `source_only` | - | - |
| - | - | - | - | lsu_cells | integer | - | `source_only` | - | - |
| - | - | - | - | poly_area | real | - | `source_only` | - | - |

## lum.dtl

| Spreadsheet name | Type | Units | Range | Source name | Type | Description | Status | Editor DB name | Editor check |
|---|---|---|---|---|---|---|---|---|---|
| id | - | - | - | - | - | id | `spreadsheet_only` (structural) | - | `mismatch` |
| mdtbl | string | - | - | - | - | - | `spreadsheet_only` | - | `mismatch` |
| description | string | - | - | - | - | Description, not used in the model | `spreadsheet_only` (structural) | - | `mismatch` |
| dtbl_name | string | - | - | name | character | name of the decision table | `matched` | name | `verified` |
| conds | integer | - | - | conds | integer | number of conditions | `matched` | conds | `verified` |
| alts | integer | - | - | alts | integer | number of alternatives | `matched` | alts | `verified` |
| acts | integer | - | - | acts | integer | number of actions | `matched` | acts | `verified` |
| dtbl_name | string | - | - | name | character | name of the decision table | `matched` | name | `verified` |
| description | string | - | - | - | - | Description, not used in the model | `spreadsheet_only` (structural) | - | `mismatch` |
| cond_var | string | - | - | var | character | condition variable (ie volume, flow, sw, time, etc) | `matched` | var | `verified` |
| obj | string | - | - | ob | character | object variable (ie res, hru, canal, etc) | `matched` | obj | `verified` |
| obj_numb | integer | - | - | ob_num | integer | object number | `matched` | - | `mismatch` |
| lim_var | string | - | - | lim_var | character | limit variable (ie evol, pvol, fc, ul, etc) | `matched` | lim_var | `verified` |
| lim_op | string | - | - | lim_op | character | limit operator (*,+,-) | `matched` | lim_op | `verified` |
| lim_const | numeric | - | - | lim_const | real | limit constant | `matched` | lim_const | `verified` |
| alt1 | string | - | - | alt | character | condition alternatives | `matched` | alt | `verified` |
| alt2 | string | - | - | alt | character | condition alternatives | `matched` | alt | `verified` |
| alt3 | string | - | - | alt | character | condition alternatives | `matched` | alt | `verified` |
| alt4 | string | - | - | alt | character | condition alternatives | `matched` | alt | `verified` |
| alt5 | string | - | - | alt | character | condition alternatives | `matched` | alt | `verified` |
| alt6 | string | - | - | alt | character | condition alternatives | `matched` | alt | `verified` |
| alt7 | string | - | - | alt | character | condition alternatives | `matched` | alt | `verified` |
| alt8 | string | - | - | alt | character | condition alternatives | `matched` | alt | `verified` |
| alt9 | string | - | - | alt | character | condition alternatives | `matched` | alt | `verified` |
| alt10 | string | - | - | alt | character | condition alternatives | `matched` | alt | `verified` |
| dtbl_name | string | - | - | name | character | header for actions | `matched` | name | `verified` |
| description | string | - | - | - | - | Description, not used in the model | `spreadsheet_only` | - | `mismatch` |
| act_typ | string | - | - | typ | character | type of action | `matched` | act_typ | `verified` |
| obj | string | - | - | ob | character | action objects | `matched` | obj | `verified` |
| obj_num | string | - | - | ob_num | integer | action object number | `matched` | obj_num | `verified` |
| act_name | string | - | - | name | character | action name | `matched` | name | `verified` |
| act_option | string | - | - | option | character | action option | `matched` | option | `verified` |
| const | string | - | - | const | real | constant used for rate, days, etc. | `matched` | const | `verified` |
| const2 | string | - | - | const2 | real | constant used for rate, days, etc. | `matched` | const2 | `verified` |
| file_pointer | string | - | - | file_pointer | character | pointer for option (ie weir equation pointer) | `matched` | - | `mismatch` |
| out1 | string | - | - | act_outcomes | character | action outcomes ('y' to perform action; 'n' to not perform) | `matched` | - | `mismatch` |
| out2 | string | - | - | act_outcomes | character | action outcomes ('y' to perform action; 'n' to not perform) | `matched` | - | `mismatch` |
| out3 | string | - | - | act_outcomes | character | action outcomes ('y' to perform action; 'n' to not perform) | `matched` | - | `mismatch` |
| out4 | string | - | - | act_outcomes | character | action outcomes ('y' to perform action; 'n' to not perform) | `matched` | - | `mismatch` |
| out5 | string | - | - | act_outcomes | character | action outcomes ('y' to perform action; 'n' to not perform) | `matched` | - | `mismatch` |
| out6 | string | - | - | act_outcomes | character | action outcomes ('y' to perform action; 'n' to not perform) | `matched` | - | `mismatch` |
| out7 | string | - | - | act_outcomes | character | action outcomes ('y' to perform action; 'n' to not perform) | `matched` | - | `mismatch` |
| out8 | string | - | - | act_outcomes | character | action outcomes ('y' to perform action; 'n' to not perform) | `matched` | - | `mismatch` |
| out9 | string | - | - | act_outcomes | character | action outcomes ('y' to perform action; 'n' to not perform) | `matched` | - | `mismatch` |
| out10 | string | - | - | act_outcomes | character | action outcomes ('y' to perform action; 'n' to not perform) | `matched` | - | `mismatch` |

## management.sch

| Spreadsheet name | Type | Units | Range | Source name | Type | Description | Status | Editor DB name | Editor check |
|---|---|---|---|---|---|---|---|---|---|
| id | - | - | - | - | - | ID | `spreadsheet_only` (structural) | - | `mismatch` |
| name | string | - | - | name | character | Management schedule name | `matched` | name | `verified` |
| description | string | - | - | - | - | Description of management schedule | `spreadsheet_only` (structural) | - | `mismatch` |
| ops_cnt | integer | - | - | num_ops | integer | Number of operations | `matched` | - | `mismatch` |
| auto_cnt | - | - | - | - | - | - | `spreadsheet_only` (structural) | - | `mismatch` |
| mgt_name | - | - | - | - | - | - | `spreadsheet_only` (structural) | - | `mismatch` |
| description | - | - | - | - | - | - | `spreadsheet_only` (structural) | - | `mismatch` |
| auto_name | string | - | - | auto_name | character | Number of auto names to follow | `matched` | - | `mismatch` |
| mgt_name | - | - | - | - | - | - | `spreadsheet_only` (structural) | - | `mismatch` |
| description | - | - | - | - | - | - | `spreadsheet_only` (structural) | - | `mismatch` |
| op_typ | string | - | - | op | character | Operation Type (plnt; harv;kill;hvkl;till;irr;fert;pest;graz;burn;swep;prtp;skip) + auto for all applic; | `matched` | op_typ | `verified` |
| mon | integer | none | 1..12 | mon | integer | Month of operation | `matched` | mon | `verified` |
| day | integer | none | 1..31 | day | integer | Day of Operation | `matched` | day | `verified` |
| hu_sch | numeric | none | - | husc | real | Heat unit schedule | `matched` | hu_sch | `verified` |
| op_data1 | string | - | - | op_char | character | Operation specific data 1 | `matched` | op_data1 | `verified` |
| op_data2 | string | - | - | op_plant | character | Operation specific data 2 | `matched` | op_data2 | `verified` |
| op_data3 | numeric | none | - | op3 | real | Override, applicable only to certain operation types | `matched` | op_data3 | `verified` |
| date | date | - | - | - | - | Full date used for database sorting of operations | `spreadsheet_only` (structural) | - | `mismatch` |
| - | - | - | - | num_autos | integer | - | `source_only` | - | - |

## manure.frt

| Spreadsheet name | Type | Units | Range | Source name | Type | Description | Status | Editor DB name | Editor check |
|---|---|---|---|---|---|---|---|---|---|
| - | - | - | - | name | character | name of manure type | `source_only` | - | - |
| - | - | - | - | org_min | character | sediment, carbon, and nutrients | `source_only` | - | - |
| - | - | - | - | pests | character | pesticides - ppm | `source_only` | - | - |
| - | - | - | - | paths | character | pathogens - cfu | `source_only` | - | - |
| - | - | - | - | hmets | character | heavy metals - ppm | `source_only` | - | - |
| - | - | - | - | salts | character | salt ions - ppm | `source_only` | - | - |
| - | - | - | - | constit | character | other constituents - ppm | `source_only` | - | - |
| - | - | - | - | descrip | character | description | `source_only` | - | - |
| - | - | - | - | iorg_min | integer | sediment, carbon, and nutrients - pointer to | `source_only` | - | - |
| - | - | - | - | ipests | integer | pesticides - pointer to | `source_only` | - | - |
| - | - | - | - | ipaths | integer | pathogens - pointer to | `source_only` | - | - |
| - | - | - | - | imets | integer | heavy metals - pointer to | `source_only` | - | - |
| - | - | - | - | isalts | integer | salt ions - pointer to | `source_only` | - | - |
| - | - | - | - | iconstit | integer | other constituents - pointer to | `source_only` | - | - |

## manure_allo.mnu

| Spreadsheet name | Type | Units | Range | Source name | Type | Description | Status | Editor DB name | Editor check |
|---|---|---|---|---|---|---|---|---|---|
| - | - | - | - | k | integer | - | `source_only` | - | - |
| - | - | - | - | mois_typ | character | wet or dry | `source_only` | - | - |
| - | - | - | - | manure_typ | character | points to fertilizer.frt | `source_only` | - | - |
| - | - | - | - | lat | real | latitude | `source_only` | - | - |
| - | - | - | - | long | real | longitude | `source_only` | - | - |
| - | - | - | - | stor_init | real | initial storage - tons | `source_only` | - | - |
| - | - | - | - | stor_max | real | maximum storage - tons | `source_only` | - | - |
| - | - | - | - | prod_mon(1) | real | average monthly manure produced - tons/month | `source_only` | - | - |
| - | - | - | - | prod_mon(2) | real | average monthly manure produced - tons/month | `source_only` | - | - |
| - | - | - | - | prod_mon(3) | real | average monthly manure produced - tons/month | `source_only` | - | - |
| - | - | - | - | prod_mon(4) | real | average monthly manure produced - tons/month | `source_only` | - | - |
| - | - | - | - | prod_mon(5) | real | average monthly manure produced - tons/month | `source_only` | - | - |
| - | - | - | - | prod_mon(6) | real | average monthly manure produced - tons/month | `source_only` | - | - |
| - | - | - | - | prod_mon(7) | real | average monthly manure produced - tons/month | `source_only` | - | - |
| - | - | - | - | prod_mon(8) | real | average monthly manure produced - tons/month | `source_only` | - | - |
| - | - | - | - | prod_mon(9) | real | average monthly manure produced - tons/month | `source_only` | - | - |
| - | - | - | - | prod_mon(10) | real | average monthly manure produced - tons/month | `source_only` | - | - |
| - | - | - | - | prod_mon(11) | real | average monthly manure produced - tons/month | `source_only` | - | - |
| - | - | - | - | prod_mon(12) | real | average monthly manure produced - tons/month | `source_only` | - | - |
| - | - | - | - | name | character | name of the water allocation object | `source_only` | - | - |
| - | - | - | - | rule_typ | character | rule type to allocate water | `source_only` | - | - |
| - | - | - | - | src_obs | integer | number of source objects | `source_only` | - | - |
| - | - | - | - | trn_obs | integer | number of demand objects | `source_only` | - | - |
| - | - | - | - | ob_typ | character | hru (for application) or muni (treatmentb) or divert (interbasin diversion) | `source_only` | - | - |
| - | - | - | - | ob_num | integer | number of the object type | `source_only` | - | - |
| - | - | - | - | dtbl | character | decision table name for manure/fert application | `source_only` | - | - |
| - | - | - | - | right | character | manure right (sr -senior or jr - junior right | `source_only` | - | - |

## manure_db.frt

| Spreadsheet name | Type | Units | Range | Source name | Type | Description | Status | Editor DB name | Editor check |
|---|---|---|---|---|---|---|---|---|---|
| - | - | - | - | name | character | name of manure type | `source_only` | - | - |
| - | - | - | - | org_min | character | sediment, carbon, and nutrients | `source_only` | - | - |
| - | - | - | - | pests | character | pesticides - ppm | `source_only` | - | - |
| - | - | - | - | paths | character | pathogens - cfu | `source_only` | - | - |
| - | - | - | - | hmets | character | heavy metals - ppm | `source_only` | - | - |
| - | - | - | - | salts | character | salt ions - ppm | `source_only` | - | - |
| - | - | - | - | constit | character | other constituents - ppm | `source_only` | - | - |
| - | - | - | - | descrip | character | description | `source_only` | - | - |

## manure_om.frt

| Spreadsheet name | Type | Units | Range | Source name | Type | Description | Status | Editor DB name | Editor check |
|---|---|---|---|---|---|---|---|---|---|
| - | - | - | - | name | character | Identifier used to crosswalk fertilizer entries, constructed from | `source_only` | - | - |
| - | - | kg water/(kg manure + kg_water) | - | frac_water | real | frac of manure which is water | `source_only` | - | - |
| - | - | kg C/kg frt | - | fcbn | real | frac of fert which is carbon | `source_only` | - | - |
| - | - | kg minN/kg frt | - | fminn | real | frac of fert which is mineral nitrogen (NO3+NH3) | `source_only` | - | - |
| - | - | kg minN/kg frt | - | fminp | real | frac of fert which is mineral phoshorus | `source_only` | - | - |
| - | - | kg orgN/kg frt | - | forgn | real | frac of fert which is org N | `source_only` | - | - |
| - | - | kg orgP/kg frt | - | forgp | real | frac of fert which is org P | `source_only` | - | - |
| - | - | kg NH3-N/kg N | - | fnh3n | real | frac of mineral N content of fert which is NH3 | `source_only` | - | - |
| - | - | na | - | description | character | description of manure type | `source_only` | - | - |

## minerals.gw

| Spreadsheet name | Type | Units | Range | Source name | Type | Description | Status | Editor DB name | Editor check |
|---|---|---|---|---|---|---|---|---|---|
| - | - | - | - | gw_nminl | integer | - | `source_only` | - | - |
| - | - | - | - | read_type | character | - | `source_only` | - | - |
| - | - | - | - | single_value | real | - | `source_only` | - | - |
| - | - | - | - | grid_val | real | - | `source_only` | - | - |
| - | - | - | - | fract | real | fraction of cell that is the salt mineral | `source_only` | - | - |

## nutrients.cha

| Spreadsheet name | Type | Units | Range | Source name | Type | Description | Status | Editor DB name | Editor check |
|---|---|---|---|---|---|---|---|---|---|
| id | - | - | - | - | - | ID | `spreadsheet_only` (structural) | - | `mismatch` |
| name | string | - | - | name | character | Channel nutrient parameter set name | `matched` | name | `verified` |
| description | string | - | - | - | - | Description, not used in the model | `spreadsheet_only` (structural) | - | `mismatch` |
| plt_n | numeric | ppm | 0..100 | onco | real | Channel organic N concentration | `matched` | plt_n | `verified` |
| ptl_p | numeric | ppm | 0..100 | opco | real | Channel organic P concentration | `matched` | ptl_p | `verified` |
| alg_stl | numeric | m/day or m/hr | 0.15..1.82 | rs1 | real | Local algal settling rate in reach | `matched` | alg_stl | `verified` |
| ben_disp | numeric | (m**2)*day or (mg disP-P)/((m**2)*hr) | 0.001..0.1 | rs2 | real | Benthos source rate for dissolved P in reach | `matched` | ben_disp | `verified` |
| ben_nh3n | numeric | (m**2)*day or (mg disP-P)/((m**2)*hr) | 0..1 | rs3 | real | Benthos source rate for NH3-N in reach | `matched` | ben_nh3n | `verified` |
| ptln_stl | numeric | 1/day or 1/hr | 0.001..0.1 | rs4 | real | Organic N settling rate in reach | `matched` | ptln_stl | `verified` |
| ptlp_stl | numeric | 1/day or 1/hr | 0.001..0.1 | rs5 | real | Organic P settling rate in reach | `matched` | ptlp_stl | `verified` |
| cst_stl | numeric | 1/day | 0.01..10 | rs6 | real | Arbitrary non-conservative constituent settling rate in reach | `matched` | cst_stl | `verified` |
| ben_cst | numeric | (mg ANC)/((m^2)*day) | 0.01..10 | rs7 | real | benthal source rate for arbitrary non-conservative constituent in reach | `matched` | ben_cst | `verified` |
| cbn_bod_co | numeric | 1/day or 1/hr | 0.02..3.4 | rk1 | real | CBOD deoxygenation rate in reach at 20 deg C | `matched` | cbn_bod_co | `verified` |
| air_rt | numeric | 1/day or 1/hr | 0..100 | rk2 | real | Reaeration rate in accordance with Fickian diffusion in reach at 20 deg C | `matched` | air_rt | `verified` |
| cbn_bod_stl | numeric | 1/day or 1/hr | -0.36..0.36 | rk3 | real | Rate of loss of CBOD due to settling in reach at 20 deg C | `matched` | cbn_bod_stl | `verified` |
| ben_bod | numeric | ((m**2)*day)\|at 20 deg C or mg O2/((m**2)*hr) | 0..100 | rk4 | real | Sediment oxygen demand rate in reach at 20 deg C | `matched` | ben_bod | `verified` |
| bact_die | numeric | 1/day | 0.05..4 | rk5 | real | Coliform die-off rate in reach | `matched` | bact_die | `verified` |
| cst_decay | numeric | 1/day | 0..10 | rk6 | real | Decay rate for arbitrary non-conservative constituent in reach | `matched` | cst_decay | `verified` |
| nh3n_no2n | numeric | 1/day or 1/hr | 0.1..1 | bc1 | real | Biological oxidation rate of NH3 to NO2 in reach at 20 deg C | `matched` | nh3n_no2n | `verified` |
| no2n_no3n | numeric | 1/day or 1/hr | 0.2..2 | bc2 | real | Biological oxidation rate of NO2 to NO3 in reach at 20 deg C | `matched` | no2n_no3n | `verified` |
| ptln_nh3n | numeric | 1/day or 1/hr | 0.2..0.4 | bc3 | real | Hydrolysis rate of organic N to ammonia in reach at 20 deg C | `matched` | ptln_nh3n | `verified` |
| ptlp_solp | numeric | 1/day or 1/hr | 0.01..0.7 | bc4 | real | Decay rate of organic P to dissolved P in reach at 20 deg C | `matched` | ptlp_solp | `verified` |
| q2e_lt | integer | none | 1..4 | lao | real | Qual2E light averaging option (1=one day/steady temp.;2=One day user value;3=hourly/steady temp.;4=hourly/single value) | `matched` | q2e_lt | `verified` |
| q2e_alg | integer | none | 1..3 | igropt | integer | Qual2E option for calculating the local specific growth rate of algae (1=multiplicative;2=limiting nutrient;3=harmonic mean) | `matched` | q2e_alg | `verified` |
| chla_alg | numeric | ug chla/mg alg | 10..100 | ai0 | real | Ratio of chlorophyll-a to algal biomass | `matched` | chla_alg | `verified` |
| alg_n | numeric | mg N/mg alg | 0.07..0.09 | ai1 | real | Fraction of algal biomass that is N | `matched` | alg_n | `verified` |
| alg_p | numeric | mg P/mg alg | 0.01..0.02 | ai2 | real | Fraction of algal biomass that is P | `matched` | alg_p | `verified` |
| alg_o2_prod | numeric | mg O2/mg alg | 1.4..1.8 | ai3 | real | Oxygen production rate per unit of algal photosynthesis | `matched` | alg_o2_prod | `verified` |
| alg_o2_resp | numeric | mg O2/mg alg | 1.6..2.3 | ai4 | real | Oxygen uptake rate per unit of algae respiration | `matched` | alg_o2_resp | `verified` |
| o2_nh3n | numeric | mg O2/mg N | 3..4 | ai5 | real | Oxygen uptake rate per unit of NH3 nitrogen oxidation | `matched` | o2_nh3n | `verified` |
| o2_no2n | numeric | mg O2/mg N | 1..1.14 | ai6 | real | Oxygen uptake rate per unit of NO2 nitrogen oxidation | `matched` | o2_no2n | `verified` |
| alg_grow | numeric | 1/day | 1..3 | mumax | real | Maximum specific algal growth rate | `matched` | alg_grow | `verified` |
| alg_resp | numeric | 1/day or 1/hr | 0.05..5 | rhoq | real | Algal respiration rate | `matched` | alg_resp | `verified` |
| slr_act | numeric | fraction | 0..1 | tfact | real | Fraction of solar radiation computed in the temperature heat balance that is photosynthetically active | `matched` | slr_act | `verified` |
| lt_co | numeric | MJ/(m^2*hr) | 0.223..1.135 | k_l | real | Half-saturation coefficient for light | `matched` | lt_co | `verified` |
| const_n | numeric | mg N/L | 0.01..0.3 | k_n | real | Michaelis-menton half-saturation constant for N | `matched` | const_n | `verified` |
| const_p | numeric | mg P/L | 0.001..0.05 | k_p | real | Michaelis-Menton half saturation constant for P | `matched` | const_p | `verified` |
| lt_nonalg | numeric | 1/m | 0..10 | lambda0 | real | Non-algal portion of the light extinction coefficient | `matched` | lt_nonalg | `verified` |
| alg_shd_l | numeric | 1/(m*ug chla/L) | 0.006..0.065 | lambda1 | real | Linear algal self-shading coefficient | `matched` | alg_shd_l | `verified` |
| alg_shd_nl | numeric | (1/m)(ug chla/L)^(-2/3) | 0..1 | lambda2 | real | Nonlinear algal self-shading coefficient | `matched` | alg_shd_nl | `verified` |
| nh3_pref | numeric | none | 0..1 | p_n | real | Algal preference factor for ammonia | `matched` | nh3_pref | `verified` |

## nutrients.res

| Spreadsheet name | Type | Units | Range | Source name | Type | Description | Status | Editor DB name | Editor check |
|---|---|---|---|---|---|---|---|---|---|
| id | - | - | - | - | - | ID | `spreadsheet_only` (structural) | - | `mismatch` |
| name | string | - | - | name | character | Reservoir nutrient name | `matched` | name | `verified` |
| mid_start | integer | none | 0..12 | ires1 | integer | Beginning month of mid-year nutrient settling "season" period | `matched` | mid_start | `verified` |
| mid_end | integer | none | 0..12 | ires2 | integer | Ending month of mid-year nutrient settling "season" period | `matched` | mid_end | `verified` |
| mid_n_stl | numeric | m/day | 1..15 | nsetlr1 | real | N settling rate for mid-year period (read in as m/year and converted to m/day) | `matched` | mid_n_stl | `verified` |
| n_stl | numeric | m/day | 1..15 | nsetlr2 | real | N settling rate for remainder of year (read in as m/year and converted to m/day) | `matched` | n_stl | `verified` |
| mid_p_stl | numeric | m/day | 2..20 | psetlr1 | real | P settling rate for mid-year period (read in as m/year and converted to m/day) | `matched` | mid_p_stl | `verified` |
| p_stl | numeric | m/day | 2..20 | psetlr2 | real | P settling rate for remainder of year (read in as m/year and converted to m/day) | `matched` | p_stl | `verified` |
| chla_co | numeric | none | 0..1 | nsolr | real | Chlorophyll-a production coefficient for reservoir | `matched` | chla_co | `verified` |
| secchi_co | numeric | none | 0.5..2 | psolr | real | Water clarity coefficient for reservoir | `matched` | secchi_co | `verified` |
| theta_n | numeric | none | - | theta_n | real | Temperature adjustment for nitrogen loss settling) | `matched` | theta_n | `verified` |
| theta_p | numeric | none | - | theta_p | real | Temperature adjustment for phosphorus loss (settling) | `matched` | theta_p | `verified` |
| n_min_stl | numeric | none | - | conc_nmin | real | Minimum nitrogen concentration for settling | `matched` | n_min_stl | `verified` |
| p_min_stl | numeric | none | - | conc_pmin | real | Minimum phosphorus concentration for settling | `matched` | p_min_stl | `verified` |

## nutrients.rte

| Spreadsheet name | Type | Units | Range | Source name | Type | Description | Status | Editor DB name | Editor check |
|---|---|---|---|---|---|---|---|---|---|
| - | - | - | - | name | character | - | `source_only` | - | - |
| - | - | m | - | len_inc | real | segment length for reduction | `source_only` | - | - |
| - | - | (mgN/m2/h)/ppm | - | no3_slp | real | slope of denitrification (y-axis) and inflow no3 (x-axis) | `source_only` | - | - |
| - | - | mgN/m2/h | - | no3_int | real | intercept of denitrification rate equation | `source_only` | - | - |
| - | - | (mgN/m2/h)/ppm | - | no3_slp_ob | real | slope of denitrification (y-axis) and inflow no3 (x-axis) | `source_only` | - | - |
| - | - | mgN/m2/h | - | no3_int_ob | real | intercept of denitrification rate equation | `source_only` | - | - |
| - | - | (mgN/m2/h)/ppm | - | no3_slp_ub | real | slope of denitrification (y-axis) and inflow no3 (x-axis) | `source_only` | - | - |
| - | - | mgN/m2/h | - | no3_int_ub | real | intercept of denitrification rate equation | `source_only` | - | - |
| - | - | (del ppm/ppm) | - | turb_slp | real | slope of turbidity reduction (y) and inflow turbidity (x) | `source_only` | - | - |
| - | - | ppm | - | turb_int | real | intecept of turbidity reduction equation | `source_only` | - | - |
| - | - | (del ppm/ppm) | - | tss_slp | real | slope of total suspended solids (y) and inflow turbidity (x) | `source_only` | - | - |
| - | - | ppm | - | tss_int | real | intecept of tss reduction equation | `source_only` | - | - |
| - | - | (del ppm/ppm) | - | tp_slp | real | slope of total P reduction (y) and turbidity reduction (x) | `source_only` | - | - |
| - | - | ppm | - | tp_int | real | intecept of total P reduction equation | `source_only` | - | - |
| - | - | (del ppm/ppm) | - | srp_slp | real | slope of soluble reactive P reduction (y) and total P reduction (x) | `source_only` | - | - |
| - | - | ppm | - | srp_int | real | intecept of soluble reactive P reduction equation | `source_only` | - | - |
| - | - | ppm | - | turb_tss_slp | real | slope of turbidity and total suspended solids (0.2-0.4) | `source_only` | - | - |
| - | - | ppm | - | no3_min_conc | real | minimum no3 concentration | `source_only` | - | - |
| - | - | ppm | - | tp_min_conc | real | minimum tp concentration | `source_only` | - | - |
| - | - | ppm | - | tss_min_conc | real | minimum tss concentration | `source_only` | - | - |
| - | - | ppm | - | srp_min_conc | real | minimum srp concentration | `source_only` | - | - |

## nutrients.sol

| Spreadsheet name | Type | Units | Range | Source name | Type | Description | Status | Editor DB name | Editor check |
|---|---|---|---|---|---|---|---|---|---|
| id | - | - | - | - | - | ID | `spreadsheet_only` (structural) | - | `mismatch` |
| name | string | - | - | name | character | Soil test (nutrient profile) name | `matched` | name | `verified` |
| description | string | - | - | - | - | Description, not used in the model | `spreadsheet_only` (structural) | - | `mismatch` |
| exp_co | numeric | - | 0.0005..0.002 | exp_co | real | Depth coefficient to adjust concentrations for depth | `matched` | exp_co | `verified` |
| lab_p | numeric | ppm | 0..20 | lab_p | real | Labile P in soil surface | `matched` | lab_p | `verified` |
| nitrate | numeric | ppm | 0..40 | nitrate | real | Nitrate N in soil surface | `matched` | nitrate | `verified` |
| fr_hum_act | numeric | 0-1 | 0..1 | fr_hum_act | real | Fraction of soil humus that is active | `matched` | fr_hum_act | `verified` |
| hum_c_n | numeric | ratio | 8..12 | hum_c_n | real | Humus C:N ratio | `matched` | hum_c_n | `verified` |
| hum_c_p | numeric | ratio | 70..90 | hum_c_p | real | Humus C:P ratio | `matched` | hum_c_p | `verified` |
| inorgp | numeric | ppm | 0..15 | inorgp | real | Inorganic P in soil surface-not currently used | `matched` | inorgp | `verified` |
| watersol_p | numeric | ppm | 0..0.5 | watersol_p | real | Water soluble P in soil surface-not currently used | `matched` | watersol_p | `verified` |
| h3a_p | numeric | ppm | 0..1 | h3a_p | real | H3a in soil surface-not currently used | `matched` | h3a_p | `verified` |
| mehlich_p | numeric | ppm | 0..5 | mehlich_p | real | Mehlich P in soil surface--not currently used | `matched` | mehlich_p | `verified` |
| bray_strong_p | numeric | ppm | 0..3 | bray_strong_p | real | Bray P in soil surface-not currently used | `matched` | bray_strong_p | `verified` |

## object.cnt

| Spreadsheet name | Type | Units | Range | Source name | Type | Description | Status | Editor DB name | Editor check |
|---|---|---|---|---|---|---|---|---|---|
| name | string | none | >=0 | name | character | name | `matched` | name | `verified` |
| ls_area | numeric | ha | >=0 | area_ls_ha | real | area of landscape, (all hrus) | `matched` | ls_area | `verified` |
| tot_area | numeric | ha | >=0 | area_tot_ha | real | total area | `matched` | tot_area | `verified` |
| obj | integer | none | >=0 | objs | integer | total number of objects or 1st object command | `matched` | obj | `verified` |
| hru | integer | none | >=0 | hru | integer | 1-number of hru's or 1st hru command | `matched` | hru | `verified` |
| lhru | integer | none | >=0 | hru_lte | integer | 2-number of hru_lte's or 1st hru_lte command | `matched` | lhru | `verified` |
| rtu | integer | none | >=0 | ru | integer | 3-number of routing units or 1st ru command | `matched` | rtu | `verified` |
| gwfl | integer | none | >=0 | gwflow | integer | 4-number of modparm's or 1st modparm command | `matched` | - | `mismatch` |
| aqu | integer | none | >=0 | aqu | integer | 5-number of aquifer's or 1st aquifer command | `matched` | aqu | `verified` |
| cha | integer | none | >=0 | chan | integer | 6-number of chan's or 1st chan command | `matched` | cha | `verified` |
| res | integer | none | >=0 | res | integer | 7-number of res's or 1st res command | `matched` | res | `verified` |
| rec | integer | none | >=0 | recall | integer | 8-number of recdays's or 1st recday command | `matched` | rec | `verified` |
| exco | integer | none | >=0 | exco | integer | 11-number of exco's or 1st export coeff command | `matched` | exco | `verified` |
| del | integer | none | >=0 | dr | integer | 12-number of dr's or 1st del ratio command | `matched` | - | `mismatch` |
| can | integer | none | >=0 | canal | integer | 13-number of canal's or 1st canal command | `matched` | can | `verified` |
| pmp | integer | none | >=0 | pump | integer | 14-number of pump's or 1st pump command | `matched` | pmp | `verified` |
| out | integer | none | >=0 | outlet | integer | 15-number of outlet's or 1st outlet command | `matched` | out | `verified` |
| lcha | integer | none | >=0 | chandeg | integer | 16-number of swat-deg channel's or 1st swat-deg channel command | `matched` | lcha | `verified` |
| aqu2d | integer | none | >=0 | aqu2d | integer | 17-number of 2D aquifer's or 1st 2D aquifer command | `matched` | aqu2d | `verified` |
| hrd | integer | none | >=0 | herd | integer | 17-number of herds or 1st 2D aquifer command | `matched` | hrd | `verified` |
| wro | integer | none | >=0 | wro | integer | 17-number of water right objects or 1st 2D aquifer command | `matched` | wro | `verified` |

## object.prt

| Spreadsheet name | Type | Units | Range | Source name | Type | Description | Status | Editor DB name | Editor check |
|---|---|---|---|---|---|---|---|---|---|
| - | - | - | - | k | integer | - | `source_only` | - | - |
| - | - | - | - | obtyp | character | object type: hru,hlt,hs,rxc,dr,out,sdc | `source_only` | - | - |
| - | - | - | - | obtypno | integer | object type number: 1=hru, 2=hru_lte, 3=channel | `source_only` | - | - |
| - | - | - | - | hydtyp | character | hydrograph type: tot,rhg,sur,lat,til | `source_only` | - | - |
| - | - | - | - | filename | character | file with hydrograph output from the object | `source_only` | - | - |

## om_osrc.wal

| Spreadsheet name | Type | Units | Range | Source name | Type | Description | Status | Editor DB name | Editor check |
|---|---|---|---|---|---|---|---|---|---|
| - | - | - | - | om_osrc_name | character | - | `source_only` | - | - |
| - | - | m^3 | - | flo | real | volume of water | `source_only` | - | - |
| - | - | metric tons | - | sed | real | sediment | `source_only` | - | - |
| - | - | kg N | - | orgn | real | organic N | `source_only` | - | - |
| - | - | kg P | - | sedp | real | organic P | `source_only` | - | - |
| - | - | kg N | - | no3 | real | NO3-N | `source_only` | - | - |
| - | - | kg P | - | solp | real | mineral (soluble P) | `source_only` | - | - |
| - | - | kg | - | chla | real | chlorophyll-a | `source_only` | - | - |
| - | - | kg N | - | nh3 | real | NH3 | `source_only` | - | - |
| - | - | kg N | - | no2 | real | NO2 | `source_only` | - | - |
| - | - | kg | - | cbod | real | carbonaceous biological oxygen demand | `source_only` | - | - |
| - | - | kg | - | dox | real | dissolved oxygen | `source_only` | - | - |
| - | - | tons | - | san | real | detached sand | `source_only` | - | - |
| - | - | tons | - | sil | real | detached silt | `source_only` | - | - |
| - | - | tons | - | cla | real | detached clay | `source_only` | - | - |
| - | - | tons | - | sag | real | detached small ag | `source_only` | - | - |
| - | - | tons | - | lag | real | detached large ag | `source_only` | - | - |
| - | - | tons | - | grv | real | gravel | `source_only` | - | - |
| - | - | deg c | - | temp | real | temperature | `source_only` | - | - |

## om_treat.wal

| Spreadsheet name | Type | Units | Range | Source name | Type | Description | Status | Editor DB name | Editor check |
|---|---|---|---|---|---|---|---|---|---|
| - | - | - | - | om_treat_name | character | - | `source_only` | - | - |
| - | - | m^3 | - | flo | real | volume of water | `source_only` | - | - |
| - | - | metric tons | - | sed | real | sediment | `source_only` | - | - |
| - | - | kg N | - | orgn | real | organic N | `source_only` | - | - |
| - | - | kg P | - | sedp | real | organic P | `source_only` | - | - |
| - | - | kg N | - | no3 | real | NO3-N | `source_only` | - | - |
| - | - | kg P | - | solp | real | mineral (soluble P) | `source_only` | - | - |
| - | - | kg | - | chla | real | chlorophyll-a | `source_only` | - | - |
| - | - | kg N | - | nh3 | real | NH3 | `source_only` | - | - |
| - | - | kg N | - | no2 | real | NO2 | `source_only` | - | - |
| - | - | kg | - | cbod | real | carbonaceous biological oxygen demand | `source_only` | - | - |
| - | - | kg | - | dox | real | dissolved oxygen | `source_only` | - | - |
| - | - | tons | - | san | real | detached sand | `source_only` | - | - |
| - | - | tons | - | sil | real | detached silt | `source_only` | - | - |
| - | - | tons | - | cla | real | detached clay | `source_only` | - | - |
| - | - | tons | - | sag | real | detached small ag | `source_only` | - | - |
| - | - | tons | - | lag | real | detached large ag | `source_only` | - | - |
| - | - | tons | - | grv | real | gravel | `source_only` | - | - |
| - | - | deg c | - | temp | real | temperature | `source_only` | - | - |

## om_use.wal

| Spreadsheet name | Type | Units | Range | Source name | Type | Description | Status | Editor DB name | Editor check |
|---|---|---|---|---|---|---|---|---|---|
| - | - | - | - | om_use_name | character | - | `source_only` | - | - |
| - | - | m^3 | - | flo | real | volume of water | `source_only` | - | - |
| - | - | metric tons | - | sed | real | sediment | `source_only` | - | - |
| - | - | kg N | - | orgn | real | organic N | `source_only` | - | - |
| - | - | kg P | - | sedp | real | organic P | `source_only` | - | - |
| - | - | kg N | - | no3 | real | NO3-N | `source_only` | - | - |
| - | - | kg P | - | solp | real | mineral (soluble P) | `source_only` | - | - |
| - | - | kg | - | chla | real | chlorophyll-a | `source_only` | - | - |
| - | - | kg N | - | nh3 | real | NH3 | `source_only` | - | - |
| - | - | kg N | - | no2 | real | NO2 | `source_only` | - | - |
| - | - | kg | - | cbod | real | carbonaceous biological oxygen demand | `source_only` | - | - |
| - | - | kg | - | dox | real | dissolved oxygen | `source_only` | - | - |
| - | - | tons | - | san | real | detached sand | `source_only` | - | - |
| - | - | tons | - | sil | real | detached silt | `source_only` | - | - |
| - | - | tons | - | cla | real | detached clay | `source_only` | - | - |
| - | - | tons | - | sag | real | detached small ag | `source_only` | - | - |
| - | - | tons | - | lag | real | detached large ag | `source_only` | - | - |
| - | - | tons | - | grv | real | gravel | `source_only` | - | - |
| - | - | deg c | - | temp | real | temperature | `source_only` | - | - |

## om_water.ini

| Spreadsheet name | Type | Units | Range | Source name | Type | Description | Status | Editor DB name | Editor check |
|---|---|---|---|---|---|---|---|---|---|
| id | integer | - | - | - | - | ID | `spreadsheet_only` (structural) | - | `mismatch` |
| name | string | - | - | - | - | - | `spreadsheet_only` | name | `verified` |
| description | string | - | - | - | - | - | `spreadsheet_only` (structural) | - | `mismatch` |
| vol | numeric | frac | - | flo | real | volume of water | `matched` | flo | `verified` |
| sed | numeric | ppm | - | sed | real | sediment | `matched` | sed | `verified` |
| part_n | numeric | ppm | - | orgn | real | organic N | `matched` | orgn | `verified` |
| part_p | numeric | ppm | - | sedp | real | organic P | `matched` | sedp | `verified` |
| no3 | numeric | ppm | - | no3 | real | NO3-N | `matched` | no3 | `verified` |
| solp | numeric | ppm | - | solp | real | mineral (soluble P) | `matched` | solp | `verified` |
| chl_a | numeric | ppm | - | chla | real | chlorophyll-a | `matched` | chl_a | `verified` |
| nh3 | numeric | ppm | - | nh3 | real | NH3 | `matched` | nh3 | `verified` |
| no2 | numeric | ppm | - | no2 | real | NO2 | `matched` | no2 | `verified` |
| cbn_bod | numeric | ppm | - | cbod | real | carbonaceous biological oxygen demand | `matched` | cbn_bod | `verified` |
| dis_ox | numeric | ppm | - | dox | real | dissolved oxygen | `matched` | dis_ox | `verified` |
| sand | numeric | ppm | - | san | real | detached sand | `matched` | san | `verified` |
| silt | numeric | ppm | - | sil | real | detached silt | `matched` | sil | `verified` |
| clay | numeric | ppm | - | cla | real | detached clay | `matched` | cla | `verified` |
| sm_ag | numeric | ppm | - | sag | real | detached small ag | `matched` | sag | `verified` |
| l_ag | numeric | ppm | - | lag | real | detached large ag | `matched` | lag | `verified` |
| grv | numeric | ppm | - | grv | real | gravel | `matched` | grv | `verified` |
| tmp | numeric | deg c | - | temp | real | temperature | `matched` | tmp | `verified` |
| - | - | - | - | om_init_name | character | - | `source_only` | - | - |

## out_src.wal

| Spreadsheet name | Type | Units | Range | Source name | Type | Description | Status | Editor DB name | Editor check |
|---|---|---|---|---|---|---|---|---|---|
| - | - | - | - | imax | integer | - | `source_only` | - | - |
| - | - | - | - | i | integer | - | `source_only` | - | - |
| - | - | - | - | name | character | name of outside basin source | `source_only` | - | - |
| - | - | - | - | stor_mx | real | m3 !maximum storage in plant | `source_only` | - | - |
| - | - | - | - | lag_days | real | days !treatement time - lag outflow | `source_only` | - | - |
| - | - | - | - | loss_fr | real | water loss during treament | `source_only` | - | - |
| - | - | - | - | pest | real | pesticide (kg/ha) | `source_only` | - | - |
| - | - | - | - | path | real | pathogen (cfu) | `source_only` | - | - |

## outlet.con

| Spreadsheet name | Type | Units | Range | Source name | Type | Description | Status | Editor DB name | Editor check |
|---|---|---|---|---|---|---|---|---|---|
| id | integer | - | - | - | - | outlet number | `spreadsheet_only` | - | `unavailable` |
| name | string | - | - | name | character | The name of the connect unit | `matched` | - | `unavailable` |
| gis_id | string | - | - | gis_id | integer | GIS id | `matched` | - | `unavailable` |
| area | numeric | ha | -180..180 | area_ha | real | AREA | `matched` | - | `unavailable` |
| lat | numeric | dec degrees | - | lat | real | latitude | `matched` | - | `unavailable` |
| lon | numeric | dec degrees | -90..90 | long | real | longitude | `matched` | - | `unavailable` |
| elev | numeric | m | 1..7000 | elev | real | Elevation of outlet | `matched` | - | `unavailable` |
| out | integer | - | - | - | - | OUT OBJECT | `spreadsheet_only` | - | `unavailable` |
| wst | string | - | - | - | - | weather station number | `spreadsheet_only` | - | `unavailable` |
| cst | integer | - | - | constit | integer | Constituent data pointer to pesticides, pathogens, metals, salts | `matched` | - | `unavailable` |
| ovfl | numeric | - | - | - | - | Points to the connections of spatial objects for overbank flooding | `spreadsheet_only` | - | `unavailable` |
| rule | integer | - | - | ruleset | character | Ruleset pointer for flow fraction of hydrograph | `matched` | - | `unavailable` |
| out_tot | integer | - | - | src_tot | integer | Total number of outgoing objects | `matched` | - | `unavailable` |
| out_id | integer | - | - | - | - | number | `spreadsheet_only` (structural) | - | `unavailable` |
| obj_numb | integer | - | 1..10 | - | - | Object number 1-10 | `spreadsheet_only` (structural) | - | `unavailable` |
| obj_typ | string | - | - | obtyp_out | character | Outflow object type | `matched` | - | `unavailable` |
| obj_id | integer | - | - | - | - | Outflow object identifier for specified type | `spreadsheet_only` | - | `unavailable` |
| hyd_typ | string | - | - | - | - | Outflow hydrograph type | `spreadsheet_only` | - | `unavailable` |
| frac | numeric | - | 0..1 | frac_out | real | Fraction of hydrograph set to object | `matched` | - | `unavailable` |
| description | string | none | - | - | - | - | `spreadsheet_only` (structural) | - | `unavailable` |
| - | - | - | - | num | integer | spatial object number- ie hru number corresponding to sequential command number | `source_only` | - | - |
| - | - | - | - | props | integer | properties number from data base (ie hru.dat, sub.dat) - change props to data | `source_only` | - | - |
| - | - | - | - | wst_c | character | weather station name | `source_only` | - | - |
| - | - | - | - | props2 | integer | overbank connectivity pointer to landscape units - change props2 to overbank | `source_only` | - | - |
| - | - | - | - | obtypno_out | integer | outflow object type name | `source_only` | - | - |
| - | - | - | - | htyp_out | character | outflow hyd type (ie 1=tot, 2= recharge, 3=surf, etc) | `source_only` | - | - |

## outputs.gw

| Spreadsheet name | Type | Units | Range | Source name | Type | Description | Status | Editor DB name | Editor check |
|---|---|---|---|---|---|---|---|---|---|
| - | - | - | - | combined_yrday | integer | - | `source_only` | - | - |
| - | - | - | - | gw_obs_cells_init | integer | - | `source_only` | - | - |
| - | - | - | - | gw_cell_obs_ss | integer | - | `source_only` | - | - |

## outside_rcv.wal

| Spreadsheet name | Type | Units | Range | Source name | Type | Description | Status | Editor DB name | Editor check |
|---|---|---|---|---|---|---|---|---|---|
| - | - | - | - | i | integer | - | `source_only` | - | - |
| - | - | - | - | name | character | name of outside basin receiving object | `source_only` | - | - |
| - | - | - | - | filename | character | name of outside basin receiving object | `source_only` | - | - |

## ovn_table.lum

| Spreadsheet name | Type | Units | Range | Source name | Type | Description | Status | Editor DB name | Editor check |
|---|---|---|---|---|---|---|---|---|---|
| name | - | - | - | name | character | ID | `matched` | name | `verified` |
| name | string | none | - | name | character | Overland Flow Mannings N Class name | `matched` | name | `verified` |
| landuse | string | none | - | name | character | Landcover classification | `matched` | name | `verified` |
| treat | string | none | - | name | character | Treatment/Practice | `matched` | name | `verified` |
| ovn_mean | numeric | - | - | ovn | real | overland flow mannings n = mean | `matched` | ovn_mean | `verified` |
| ovn_min | numeric | - | - | ovn_min | real | overland flow mannings n = min | `matched` | ovn_min | `verified` |
| ovn_max | numeric | - | - | ovn_max | real | overland flow mannings n = max | `matched` | ovn_max | `verified` |
| description | string | none | - | - | - | description | `spreadsheet_only` (structural) | - | `mismatch` |

## parameters.bsn

| Spreadsheet name | Type | Units | Range | Source name | Type | Description | Status | Editor DB name | Editor check |
|---|---|---|---|---|---|---|---|---|---|
| id | - | - | - | - | - | ID | `spreadsheet_only` (structural) | - | `mismatch` |
| lai_noevap | numeric | none | 0..1 | evlai | real | leaf area index at which no evap occurs | `matched` | lai_noevap | `verified` |
| sw_init | numeric | frac | 1..24 | ffcb | real | initial soil water cont expressed as a fraction of fc | `matched` | sw_init | `verified` |
| surq_lag | numeric | days | 0.5..2 | surlag | real | surface runoff lag time | `matched` | surq_lag | `verified` |
| adj_pkrt | numeric | none | 0..2 | adj_pkr | real | peak rate adjustment factor in the subbasin | `matched` | adj_pkrt | `verified` |
| adj_pkrt_sed | numeric | - | 0.0001..0.01 | prf | real | peak rate adjustment factor for sediment routing in the channel | `matched` | adj_pkrt_sed | `verified` |
| null | numeric | - | - | - | - | not used /place holder | `spreadsheet_only` | - | `mismatch` |
| null | numeric | - | - | - | - | not used /place holder | `spreadsheet_only` | - | `mismatch` |
| orgn_min | numeric | - | 0..100 | cmn | real | rate factor for mineralization on active org N | `matched` | orgn_min | `verified` |
| n_uptake | numeric | - | 0..100 | n_updis | real | nitrogen uptake dist parm | `matched` | n_uptake | `verified` |
| p_uptake | numeric | - | 0..1 | p_updis | real | phosphorus uptake dist parm | `matched` | p_uptake | `verified` |
| n_perc | numeric | - | 10..17.5 | nperco | real | nitrate perc coeff (0-1) 0 = conc of nitrate in surface runoff is zero;1 = perc has same conc of nitrate as surf runoff | `matched` | n_perc | `verified` |
| p_perc | numeric | - | 0..10 | pperco | real | phos perc coeff (0-1) 0 = conc of sol P in surf runoff is zero;1 = percolate has some conc of sol P as surf runoff | `matched` | p_perc | `verified` |
| p_soil | numeric | - | 100..250 | phoskd | real | phos soil partitioning coef | `matched` | p_soil | `verified` |
| p_avail | numeric | - | 0.02..0.7 | psp | real | phos availability index | `matched` | p_avail | `verified` |
| rsd_decomp | numeric | - | 0..0.03 | rsdco | real | residue decomposition coeff | `matched` | rsd_decomp | `verified` |
| pest_perc | numeric | - | 0..10 | percop | real | pestcide perc coeff (0-1) | `matched` | pest_perc | `verified` |
| msk_co1 | numeric | - | 0..10 | msk_co1 | real | calibration coeff to control impact of the storage time constant for the reach at bankfull depth | `matched` | msk_co1 | `verified` |
| msk_co2 | numeric | - | 0..0.3 | msk_co2 | real | calibration coefficient used to control impact of the storage time constant for low flow (where low flow is when river is at 0.1 bankfull depth) upon the Km value calculated for the reach | `matched` | msk_co2 | `verified` |
| msk_x | numeric | - | 0..1 | msk_x | real | weighting factor control relative importance of inflow rate and outflow rate in determining storage on reach | `matched` | msk_x | `verified` |
| np_lchtile | numeric | frac | 0..1 | nperco_lchtile | real | n concentration coeff for tile flow and leach from bottom layer | `matched` | nperco_lchtile | `verified` |
| evap_adj | numeric | - | 0..1 | evrch | real | reach evaporation adjustment factor | `matched` | evap_adj | `verified` |
| scoef | numeric | - | 0..3 | scoef | real | channel storage coefficient (0-1) | `matched` | scoef | `verified` |
| denit_exp | numeric | - | 0..1 | cdn | real | denitrification expoential rate coefficient | `matched` | denit_exp | `verified` |
| denit_frac | numeric | - | 0..1 | sdnco | real | denitrification threshold frac of field cap | `matched` | denit_frac | `verified` |
| man_bact | numeric | - | 0..1 | bact_swf | real | frac of manure containing active colony forming units | `matched` | man_bact | `verified` |
| adj_uhyd | numeric | - | - | tb_adj | real | adjustment factor for subdaily unit hydrograph basetime | `matched` | adj_uhyd | `verified` |
| cn_froz | numeric | - | 0..24 | cn_froz | real | parameter for frozen soil adjustment on infiltraion/runoff | `matched` | cn_froz | `verified` |
| dorm_hr | numeric | hrs | -2..0 | dorm_hr | real | time threshold used to define dormant (hrs) | `matched` | dorm_hr | `verified` |
| plaps | numeric | mm | -25..25 | plaps | real | precipitation lapse rate | `matched` | plaps | `verified` |
| tlaps | numeric | degc | 3..8 | tlaps | real | temperature lapse rate | `matched` | tlaps | `verified` |
| n_fix_max | numeric | kg/ha | 0..0.05 | nfixmx | real | max daily n-fixation | `matched` | n_fix_max | `verified` |
| rsd_decay | numeric | - | 0.1..0.5 | decr_min | real | minimum daily residue decay | `matched` | rsd_decay | `verified` |
| rsd_cover | numeric | - | 0..10 | rsd_covco | real | residue cover factor for computing frac of cover | `matched` | rsd_cover | `verified` |
| urb_init_abst | numeric | - | 0..1 | urb_init_abst | real | max initial abstrction for urban areas when using Green&Ampt | `matched` | urb_init_abst | `verified` |
| petco_pmpt | numeric | % | 0..1 | petco_pmpt | real | PET adjustment for Penman-Monteith/Preistley Taylor | `matched` | petco_pmpt | `verified` |
| uhyd_alpha | numeric | - | 0.9..3.1 | uhalpha | real | alpha coeff for est unit hydrograph using gamma func | `matched` | uhyd_alpha | `verified` |
| splash | numeric | - | 0.5..2 | eros_spl | real | coeff of splash erosion varying 0.9-3.1 | `matched` | splash | `verified` |
| rill | numeric | - | 1..3 | rill_mult | real | rill erosion coefficient | `matched` | rill | `verified` |
| surq_exp | numeric | - | 0.001..0.45 | eros_expo | real | exponential coeffcient for overland flow | `matched` | surq_exp | `verified` |
| cov_mgt | numeric | - | 10..100 | c_factor | real | scaling parameter for cover and management factor for overland flow erosion | `matched` | cov_mgt | `verified` |
| cha_d50 | numeric | mm | 1..5 | ch_d50 | real | median particle diameter of main channel | `matched` | cha_d50 | `verified` |
| co2 | numeric | - | 100..1000 | co2 | real | co2 concentration at start of simulation (ppm) | `matched` | co2 | `verified` |
| day_lag_mx | integer | days | 0..3 | day_lag_mx | integer | max days to lag hydrographs for hru,ru channels; | `matched` | - | `mismatch` |
| igen | integer | - | 0..1 | igen | integer | random generator code:0 = use default numbers;1 = generate new numbers in every simulation | `matched` | igen | `verified` |
| - | - | - | - | spcon | real | not used | `source_only` | - | - |
| - | - | - | - | spexp | real | not used | `source_only` | - | - |

## path_hru.ini

| Spreadsheet name | Type | Units | Range | Source name | Type | Description | Status | Editor DB name | Editor check |
|---|---|---|---|---|---|---|---|---|---|
| id | - | - | - | - | - | ID | `spreadsheet_only` (structural) | - | `mismatch` |
| name | string | - | - | name | character | initial pathogen name | `matched` | name | `verified` |
| description | string | - | - | - | - | - | `spreadsheet_only` (structural) | - | `mismatch` |
| path_hru_soil | numeric | - | - | - | - | amt of constituent in soil at start of simulation | `spreadsheet_only` | - | `mismatch` |
| path_hru_plt | numeric | - | - | - | - | amt of constituent on plant at start of simulation | `spreadsheet_only` | - | `mismatch` |
| - | - | ppm | - | soil | real | amount of constituent in soil at start of simulation | `source_only` | - | - |
| - | - | ppm or #cfu/m^2 | - | plt | real | amount of constituent on plant at start of simulation | `source_only` | - | - |

## path_water.ini

| Spreadsheet name | Type | Units | Range | Source name | Type | Description | Status | Editor DB name | Editor check |
|---|---|---|---|---|---|---|---|---|---|
| id | - | - | - | - | - | ID | `spreadsheet_only` (structural) | - | `mismatch` |
| name | string | - | - | path_init_name | character | - | `matched` | name | `verified` |
| description | string | - | - | - | - | - | `spreadsheet_only` (structural) | - | `mismatch` |
| path_water | numeric | - | - | - | - | amt of constituent in water at start of simulation | `spreadsheet_only` | - | `mismatch` |
| path_benthic | numeric | - | - | - | - | amt of constituent in benthic at start of simulation | `spreadsheet_only` | - | `mismatch` |
| - | - | ppm,fracitons | - | water | real | amount of constituents (dissolved, salt minerals) in aquifer at start of simulation | `source_only` | - | - |
| - | - | ppm or #cfu/m^2 | - | benthic | real | amount of constituent in benthic at start of simulation | `source_only` | - | - |

## pathogens.pth

| Spreadsheet name | Type | Units | Range | Source name | Type | Description | Status | Editor DB name | Editor check |
|---|---|---|---|---|---|---|---|---|---|
| id | - | - | - | - | - | ID | `spreadsheet_only` (structural) | - | `mismatch` |
| name | string | - | - | - | - | Bacteria name | `spreadsheet_only` | name | `verified` |
| die_sol | numeric | 1/day | - | do_soln | real | Die-off factor for persistent bacteria in soil solution | `matched` | die_sol | `verified` |
| grow_sol | numeric | 1/day | - | gr_soln | real | Growth factor for persistent bacteria in soil solution | `matched` | grow_sol | `verified` |
| die_srb | numeric | 1/day | - | do_sorb | real | Die-off factor for persistent bacteria adsorbed to soil particles | `matched` | die_srb | `verified` |
| grow_srb | numeric | 1/day | - | gr_sorb | real | Growth factor for persistent bacteria adsorbed to soil particles | `matched` | grow_srb | `verified` |
| sol_srb | numeric | none | - | kd | real | Bacteria partition coefficient between soluble and sorbed phase in surface runoff | `matched` | sol_srb | `verified` |
| tmp_adj | numeric | none | - | t_adj | real | Temperature adjustment factor for bacteria die-off/growth | `matched` | tmp_adj | `verified` |
| washoff | numeric | fraction | - | washoff | real | Fraction of persistent bacteria on foliage washed off by a rainfall event | `matched` | washoff | `verified` |
| die_plnt | numeric | 1/day | - | do_plnt | real | Die-off factor for persistent bacteria on foliage | `matched` | die_plnt | `verified` |
| grow_plnt | numeric | 1/day | - | gr_plnt | real | Growth factor for persistent bacteria on foliage | `matched` | grow_plnt | `verified` |
| frac_man | numeric | fraction | - | fr_manure | real | Fraction of manure containing active colony forming units | `matched` | frac_man | `verified` |
| perc_sol | numeric | none | - | perco | real | Bacteria percolation coefficient ratio of solution bacteria in surface layer | `matched` | perc_sol | `verified` |
| detect | numeric | cfu/m^2 | - | det_thrshd | real | Threshold detection level for less persistent bacteria | `matched` | detect | `verified` |
| die_cha | numeric | 1/day | - | do_stream | real | Die-off factor for persistent bacteria in streams 1/day | `matched` | die_cha | `verified` |
| grow_cha | numeric | 1/day | - | gr_stream | real | Growth factor for persistent bacteria in streams 1/day | `matched` | grow_cha | `verified` |
| die_res | numeric | 1/day | - | do_res | real | Die-off factor for less persistent bacteria in reservoirs 1/day | `matched` | die_res | `verified` |
| grow_res | numeric | 1/day | - | gr_res | real | Growth factor for less persistent bacteria in reservoirs 1/day | `matched` | grow_res | `verified` |
| swf | numeric | cfu | - | - | - | Fraction of manure containing active colony forming units | `spreadsheet_only` | swf | `verified` |
| conc_min | numeric | - | - | conc_min | real | minimum pathogen concentration | `matched` | conc_min | `verified` |
| - | - | - | - | pathnm | character | - | `source_only` | - | - |

## pcp.cli

| Spreadsheet name | Type | Units | Range | Source name | Type | Description | Status | Editor DB name | Editor check |
|---|---|---|---|---|---|---|---|---|---|
| pcp_file | string | - | - | - | - | Precipitation data file names | `spreadsheet_only` | - | `unavailable` |
| - | - | - | - | pcp_n | character | - | `source_only` | - | - |
| - | - | - | - | filename | character | - | `source_only` | - | - |

## pest.com

| Spreadsheet name | Type | Units | Range | Source name | Type | Description | Status | Editor DB name | Editor check |
|---|---|---|---|---|---|---|---|---|---|
| - | - | - | - | k | integer | - | `source_only` | - | - |
| - | - | - | - | name | character | - | `source_only` | - | - |
| - | - | - | - | typ | integer | recall type - 1=day, 2=mon, 3=year | `source_only` | - | - |
| - | - | - | - | filename | character | filename | `source_only` | - | - |

## pest_hru.ini

| Spreadsheet name | Type | Units | Range | Source name | Type | Description | Status | Editor DB name | Editor check |
|---|---|---|---|---|---|---|---|---|---|
| id | - | - | - | - | - | ID | `spreadsheet_only` (structural) | - | `mismatch` |
| name | string | - | - | name | character | Initial pest name | `matched` | name | `verified` |
| description | string | - | - | - | - | - | `spreadsheet_only` (structural) | - | `mismatch` |
| pest_hru_soil | numeric | - | - | - | - | amt of constituent in soil at start of simulation | `spreadsheet_only` | - | `mismatch` |
| pest_hru_plt | numeric | - | - | - | - | amt of constituent on plant at start of simulation | `spreadsheet_only` | - | `mismatch` |
| - | - | ppm | - | soil | real | amount of constituent in soil at start of simulation | `source_only` | - | - |
| - | - | ppm or #cfu/m^2 | - | plt | real | amount of constituent on plant at start of simulation | `source_only` | - | - |

## pest_water.ini

| Spreadsheet name | Type | Units | Range | Source name | Type | Description | Status | Editor DB name | Editor check |
|---|---|---|---|---|---|---|---|---|---|
| id | - | - | - | - | - | ID | `spreadsheet_only` (structural) | - | `mismatch` |
| name | string | - | - | pest_init_name | character | initial pest water name | `matched` | name | `verified` |
| description | string | - | - | - | - | - | `spreadsheet_only` (structural) | - | `mismatch` |
| pest_water | numeric | - | - | - | - | amt of constituent in water at start of simulation | `spreadsheet_only` | - | `mismatch` |
| pest_benthic | numeric | - | - | - | - | amt of constituent in benthic at start of simulation | `spreadsheet_only` | - | `mismatch` |
| - | - | ppm,fracitons | - | water | real | amount of constituents (dissolved, salt minerals) in aquifer at start of simulation | `source_only` | - | - |
| - | - | ppm or #cfu/m^2 | - | benthic | real | amount of constituent in benthic at start of simulation | `source_only` | - | - |

## pesticide.pes

| Spreadsheet name | Type | Units | Range | Source name | Type | Description | Status | Editor DB name | Editor check |
|---|---|---|---|---|---|---|---|---|---|
| id | - | - | - | - | - | ID | `spreadsheet_only` (structural) | - | `mismatch` |
| name | string | - | - | name | character | Pesticide name | `matched` | name | `verified` |
| description | string | - | - | - | - | Description, not used in the model | `spreadsheet_only` (structural) | - | `mismatch` |
| soil_ads | numeric | (mg/kg)/(mg/L) | 1..1e+09 | - | - | Soil adsorption coefficient normalized for soil organic carbon content | `spreadsheet_only` | soil_ads | `verified` |
| frac_wash | numeric | fraction | 0..1 | - | - | Fraction of pesticide on foliage that is washed off by rainfall event | `spreadsheet_only` | frac_wash | `verified` |
| hl_foliage | numeric | days | 0..10000 | - | - | Half-life of pesticide on foliage | `spreadsheet_only` | hl_foliage | `verified` |
| hl_soil | numeric | days | 0..100000 | - | - | Half-life of pesticide in soil | `spreadsheet_only` | hl_soil | `verified` |
| solub | numeric | mg/L (ppm) | >=0 | solub | real | Solubility of chemical in water | `matched` | solub | `verified` |
| aq_reac | numeric | Flow | >=0 | aq_hlife | real | Aquatic pesticide reaction coefficient | `matched` | aq_hlife | `verified` |
| aq_volat | numeric | m/day | >=0 | aq_volat | real | Aquatic volitization coefficient | `matched` | aq_volat | `verified` |
| mol_wt | numeric | g/mol | >=0 | mol_wt | real | Molecular weight to calculate mixing efficiency | `matched` | mol_wt | `verified` |
| aq_resus | numeric | m/day | >=0 | aq_resus | real | Aquatic resuspension velocity for pesticide sorbed to sediment | `matched` | aq_resus | `verified` |
| aq_settle | numeric | m/day | >=0 | aq_settle | real | Aquatic settling velocity for pesticide sorbed to sediment | `matched` | aq_settle | `verified` |
| ben_act_dep | numeric | m/day | >=0 | ben_act_dep | real | Depth of active benthic later | `matched` | ben_act_dep | `verified` |
| ben_bury | numeric | m/day | >=0 | ben_bury | real | Burial velocity in benthic sediment | `matched` | ben_bury | `verified` |
| ben_reac | numeric | 1/day | >=0 | ben_hlife | real | Reaction coefficient in benthic sediment | `matched` | ben_hlife | `verified` |
| - | - | (mL/g) | - | koc | real | soil adsorption coeff normalized for soil org carbon content | `source_only` | - | - |
| - | - | none | - | washoff | real | frac of pesticide on foliage which is washed off by rainfall event | `source_only` | - | - |
| - | - | days | - | foliar_hlife | real | half-life of pest on foliage | `source_only` | - | - |
| - | - | days | - | soil_hlife | real | half-life of pest in soil | `source_only` | - | - |
| - | - | none | - | pl_uptake | real | fraction taken up by plant | `source_only` | - | - |
| - | - | - | - | descrip | character | pesticide description | `source_only` | - | - |

## pet.cli

| Spreadsheet name | Type | Units | Range | Source name | Type | Description | Status | Editor DB name | Editor check |
|---|---|---|---|---|---|---|---|---|---|
| pet_file | string | - | - | - | - | PET file names | `spreadsheet_only` | - | `unavailable` |
| - | - | - | - | petm_n | character | - | `source_only` | - | - |
| - | - | - | - | filename | character | - | `source_only` | - | - |

## phreato.gw

| Spreadsheet name | Type | Units | Range | Source name | Type | Description | Status | Editor DB name | Editor check |
|---|---|---|---|---|---|---|---|---|---|
| - | - | - | - | gw_phyt_dep | real | - | `source_only` | - | - |
| - | - | - | - | gw_phyt_rate | real | - | `source_only` | - | - |

## phreato_cell.gw

| Spreadsheet name | Type | Units | Range | Source name | Type | Description | Status | Editor DB name | Editor check |
|---|---|---|---|---|---|---|---|---|---|
| - | - | - | - | gw_phyt_ids | integer | - | `source_only` | - | - |
| - | - | - | - | gw_phyt_area | real | - | `source_only` | - | - |

## plant.ini

| Spreadsheet name | Type | Units | Range | Source name | Type | Description | Status | Editor DB name | Editor check |
|---|---|---|---|---|---|---|---|---|---|
| id | integer | - | - | - | - | ID | `spreadsheet_only` (structural) | - | `mismatch` |
| name | string | - | - | name | character | Plant community name | `matched` | - | `mismatch` |
| description | string | - | - | - | - | Description, not used in the model | `spreadsheet_only` (structural) | - | `mismatch` |
| plnt_cnt | integer | none | >=1 | plants_com | integer | Plant count in community | `matched` | - | `mismatch` |
| rot_yr_ini | integer | - | - | rot_yr_ini | integer | initial rotation year | `matched` | rot_yr_ini | `verified` |
| plnt_com_name | string | - | - | - | - | Plant community name | `spreadsheet_only` (structural) | - | `mismatch` |
| plnt_name | string | - | - | cpnm | character | Plant name | `matched` | - | `mismatch` |
| lc_status | string | none | - | igro | character | Land cover status | `matched` | lc_status | `verified` |
| lai_init | numeric | m^2/m^2 | 0..8 | lai | real | Initial leaf area index | `matched` | lai_init | `verified` |
| bm_init | numeric | kg/ha | 0..1000 | bioms | real | Initial biomass | `matched` | bm_init | `verified` |
| phu_init | numeric | fraction | - | phuacc | real | Initial fraction of plant heat unit accumulated | `matched` | phu_init | `verified` |
| plnt_pop | numeric | - | - | pop | real | plant population | `matched` | plnt_pop | `verified` |
| yrs_init | numeric | years | - | fr_yrmat | real | Current age of crop in years | `matched` | yrs_init | `verified` |
| rsd_init | numeric | kg/ha | 0..10000 | rsdin | real | Initial residue cover | `matched` | rsd_init | `verified` |

## plant_gro.sft

| Spreadsheet name | Type | Units | Range | Source name | Type | Description | Status | Editor DB name | Editor check |
|---|---|---|---|---|---|---|---|---|---|
| id | integer | - | - | - | - | ID | `spreadsheet_only` (structural) | - | `mismatch` |
| - | string | - | - | - | - | - | `spreadsheet_only` | - | `mismatch` |
| name | string | - | - | name | character | cn2, terrace, landuse,mgt, etc | `matched` | name | `verified` |
| lum_numb | string | - | - | lum_num | integer | number of land uses in each region | `matched` | - | `mismatch` |
| nspu | numeric | - | - | nspu | integer | The number of elements in following lines | `matched` | - | `mismatch` |
| elem_cnt | numeric | - | - | elem_cnt | integer | - | `matched` | - | `mismatch` |
| order | string | - | - | name | character | Order name | `matched` | name | `verified` |
| cha_wide | numeric | - | - | - | - | Channel widening | `spreadsheet_only` | - | `mismatch` |
| cha_dc_accr | numeric | - | - | - | - | Channel down cutting or accretion | `spreadsheet_only` | - | `mismatch` |
| head_cut | numeric | - | - | - | - | Head cut advance | `spreadsheet_only` | - | `mismatch` |
| fp_accr | numeric | - | - | - | - | flood plain accretion | `spreadsheet_only` | - | `mismatch` |
| - | - | t/ha or t | - | yield | real | crop yield | `source_only` | - | - |
| - | - | t/ha or t | - | npp | real | net primary productivity (biomass) dry weight | `source_only` | - | - |
| - | - | - | - | lai_mx | real | maximum leaf area index | `source_only` | - | - |
| - | - | - | - | wstress | real | sum of water (drought) stress | `source_only` | - | - |
| - | - | - | - | astress | real | sum of water (aeration) stress | `source_only` | - | - |
| - | - | - | - | tstress | real | sum of temperature stress | `source_only` | - | - |

## plant_parms.sft

| Spreadsheet name | Type | Units | Range | Source name | Type | Description | Status | Editor DB name | Editor check |
|---|---|---|---|---|---|---|---|---|---|
| id | integer | - | - | - | - | ID | `spreadsheet_only` (structural) | - | `mismatch` |
| mchp | string | - | - | - | - | - | `spreadsheet_only` | - | `mismatch` |
| odr | integer | - | - | - | - | order | `spreadsheet_only` (structural) | - | `mismatch` |
| name | string | - | - | name | character | parameter name (cn2, esco, awc, etc.) | `matched` | name | `verified` |
| crop | string | - | - | - | - | Plant Code (soyb,frst) | `spreadsheet_only` | - | `mismatch` |
| chg_val | numeric | - | - | - | - | change value | `spreadsheet_only` | - | `mismatch` |
| chg_typ | string | - | - | chg_typ | character | type of change (absval,abschg,pctchg) | `matched` | chg_typ | `verified` |
| neg | numeric | - | - | neg | real | negative limit of change | `matched` | neg | `verified` |
| pos | numeric | - | - | pos | real | positive limit of change | `matched` | pos | `verified` |
| lo | numeric | - | - | lo | real | lower limit of parameter | `matched` | lo | `verified` |
| up | numeric | - | - | up | real | upper limit of paramete | `matched` | up | `verified` |
| - | - | - | - | lum_num | integer | number of land uses in each region | `source_only` | - | - |
| - | - | - | - | nspu | integer | - | `source_only` | - | - |
| - | - | - | - | elem_cnt | integer | - | `source_only` | - | - |
| - | - | - | - | parms | integer | number of plant parameters used in calibration | `source_only` | - | - |
| - | - | - | - | var | character | - | `source_only` | - | - |
| - | - | - | - | init_val | real | xwalk lum()%name with lscal()%lum()%name | `source_only` | - | - |

## plants.plt

| Spreadsheet name | Type | Units | Range | Source name | Type | Description | Status | Editor DB name | Editor check |
|---|---|---|---|---|---|---|---|---|---|
| id | - | - | - | - | - | ID | `spreadsheet_only` | id | `verified` |
| name | string | none | - | plantnm | character | Plant name | `matched` | name | `verified` |
| plnt_code | string | - | - | - | - | Plant name | `spreadsheet_only` (structural) | - | `mismatch` |
| description_db | string | - | - | - | - | Description, not used in the model | `spreadsheet_only` (structural) | - | `mismatch` |
| plnt_typ | string | none | - | typ | character | Crop/landcover category | `matched` | plnt_typ | `verified` |
| trig | string | none | - | trig | character | Phenology trigger | `matched` | - | `mismatch` |
| nfix_co | numeric | none | - | nfix_co | real | N fixation coefficient | `matched` | nfix_co | `verified` |
| days_mat | numeric | none | 0..300 | days_mat | integer | Days to maturity -if zero use hu for entire growing season; if negative value, considered to be heat units to mat; if positive, input is days to mat; | `matched` | days_mat | `verified` |
| bm_e | numeric | (kg/ha)/(MJ/m^2) | 10..90 | bio_e | real | Biomass-energy ratio | `matched` | bm_e | `verified` |
| harv_idx | numeric | fraction | 0.01..1.25 | hvsti | real | Harvest index: crop yield/aboveground biomass | `matched` | harv_idx | `verified` |
| lai_pot | numeric | m^2/m^2 | 0.5..10 | blai | real | Maximum (potential) leaf area index | `matched` | lai_pot | `verified` |
| frac_hu1 | numeric | fraction | 0..1 | frgrw1 | real | Fraction of the growing season heat units corresponding to the 1st point on optimal leaf area development curve | `matched` | frac_hu1 | `verified` |
| lai_max1 | numeric | fraction | 0..1 | laimx1 | real | Fraction of the maximum leaf area index corresponding to the 1st point on optimal leaf area development curve | `matched` | lai_max1 | `verified` |
| frac_hu2 | numeric | fraction | 0..1 | frgrw2 | real | Fraction of the growing season heat units corresponding to the 2nd point on optimal leaf area development curve | `matched` | frac_hu2 | `verified` |
| lai_max2 | numeric | fraction | 0..1 | laimx2 | real | Fraction of the maximum leaf area index corresponding to the 2nd point on optimal leaf area development curve | `matched` | lai_max2 | `verified` |
| hu_lai_decl | numeric | fraction | 0.15..1 | dlai | real | Fraction of growing season when leaf area declines | `matched` | hu_lai_decl | `verified` |
| dlai_rate | numeric | none | - | dlai_rate | real | Exponent that governs lai decline rate | `matched` | dlai_rate | `verified` |
| can_ht_max | numeric | m | 0.1..20 | chtmx | real | Maximum canopy height | `matched` | can_ht_max | `verified` |
| rt_dp_max | numeric | m | 0..3 | rdmx | real | Maximum root depth | `matched` | rt_dp_max | `verified` |
| tmp_opt | numeric | deg C | 11..38 | t_opt | real | Optimal temperature for plant growth | `matched` | tmp_opt | `verified` |
| tmp_base | numeric | deg C | 0..18 | t_base | real | Minimum temperture for plant growth | `matched` | tmp_base | `verified` |
| frac_n_yld | numeric | kg N/kg yield | 0.0015..0.075 | cnyld | real | Fraction of N in yield | `matched` | frac_n_yld | `verified` |
| frac_p_yld | numeric | kg P/kg yield | 0.0001..0.015 | cpyld | real | Fraction of P in yield | `matched` | frac_p_yld | `verified` |
| frac_n_em | numeric | kg N/kg biomass | 0.004..0.07 | pltnfr1 | real | Normal fraction of N in plant biomass at emergence | `matched` | frac_n_em | `verified` |
| frac_n_50 | numeric | kg N/kg biomass | 0.002..0.05 | pltnfr2 | real | Normal fraction of N in plant biomass at 50% maturity | `matched` | frac_n_50 | `verified` |
| frac_n_mat | numeric | kg N/kg biomass | 0.001..0.27 | pltnfr3 | real | Normal fraction of N in plant biomass at maturity | `matched` | frac_n_mat | `verified` |
| frac_p_em | numeric | kg P/kg biomass | 0.0005..0.01 | pltpfr1 | real | Normal fraction of P in plant biomass at emergence | `matched` | frac_p_em | `verified` |
| frac_p_50 | numeric | kg P/kg biomass | 0.0002..0.007 | pltpfr2 | real | Normal fraction of P in plant biomass at 50% maturity | `matched` | frac_p_50 | `verified` |
| frac_p_mat | numeric | kg P/kg biomass | 0.0003..0.00035 | pltpfr3 | real | Normal fraction of P in plant biomass at maturity | `matched` | frac_p_mat | `verified` |
| harv_idx_ws | numeric | (kg/ha)/(kg/ha) | -0.2..1.1 | wsyf | real | Harvest index that represents the lowest harvest index expected due to water stress | `matched` | harv_idx_ws | `verified` |
| usle_c_min | numeric | none | 0.001..0.5 | usle_c | real | Minimum value of the USLE C factor for water erosion | `matched` | usle_c_min | `verified` |
| stcon_max | numeric | m/s | 0..5 | gsi | real | Maximum stomatal conductance | `matched` | stcon_max | `verified` |
| vpd | numeric | kPa | 1.5..6 | vpdfr | real | Vapor pressure deficit at which FR_STCON_VPD is valid | `matched` | vpd | `verified` |
| frac_stcon | numeric | fraction | 0..1 | gmaxfr | real | Fraction of maximum stomatal conductance that is achieved at the vapor pressue deficit defined by VPD | `matched` | frac_stcon | `verified` |
| ru_vpd | numeric | none | 0..50 | wavp | real | Rate of decline in radiation use efficiency per unit increase in vapor pressure deficit | `matched` | ru_vpd | `verified` |
| co2_hi | numeric | μL CO2/L air | 100..1000 | co2hi | real | CO2 concentration higher than the ambient corresponding to the 2nd point on radiation use efficiency curve | `matched` | co2_hi | `verified` |
| bm_e_hi | numeric | kg/ha)/(MJ/m^2 | 5..100 | bioehi | real | Biomass-energy ratio when plant is in an environment with CO2 level equal to the value of CO2_HI | `matched` | bm_e_hi | `verified` |
| plnt_decomp | numeric | none | 0.01..0.099 | rsdco_pl | real | Plant residue decomposition coefficient | `matched` | plnt_decomp | `verified` |
| lai_min | numeric | m^2/m^2 | 0..0.99 | alai_min | real | Minimum LAI during winter dormant period | `matched` | lai_min | `verified` |
| bm_tree_acc | numeric | fraction | 0..1 | laixco_tree | real | Fraction of biomass accumulated each year | `matched` | bm_tree_acc | `verified` |
| yrs_mat | integer | years | 0..100 | mat_yrs | integer | Years to maturity | `matched` | yrs_mat | `verified` |
| bm_tree_max | numeric | metric tons/ha | 0..5000 | bmx_peren | real | Maximum biomass for forest (trees only) | `matched` | bm_tree_max | `verified` |
| ext_co | numeric | none | 0..2 | ext_coef | real | Light extinction coefficient | `matched` | ext_co | `verified` |
| leaf_tov_min | numeric | none | - | leaf_tov_min | real | Perennial leaf turnover rate with min stress | `matched` | - | `mismatch` |
| leaf_tov_max | numeric | none | - | leaf_tov_max | real | Perennial leaf turnover rate with max stress | `matched` | - | `mismatch` |
| bm_dieoff | numeric | fraction | 0..1 | bm_dieoff | real | Above ground biomass that dies off at dormancy | `matched` | bm_dieoff | `verified` |
| rt_st_beg | numeric | none | - | rsr1 | real | Root to shoot ratio at the beginning of the growing season | `matched` | rt_st_beg | `verified` |
| rt_st_end | numeric | none | - | rsr2 | real | Root to shoot ratio at the end of the growing season | `matched` | rt_st_end | `verified` |
| plnt_pop1 | numeric | plants/m^2 | - | pop1 | real | Plant population corresponding to the 1st point on the population LAI curve | `matched` | plnt_pop1 | `verified` |
| frac_lai1 | numeric | fraction | - | frlai1 | real | Fraction of the maximum leaf area index corresponding to the 1st point on the leaf area development curve | `matched` | frac_lai1 | `verified` |
| plnt_pop2 | numeric | plants/m^2 | - | pop2 | real | Plant population corresponding to the 2nd point on the population LAI curve | `matched` | plnt_pop2 | `verified` |
| frac_lai2 | numeric | fraction | - | frlai2 | real | Fraction of the maximum leaf area index corresponding to the 2nd point on the leaf area development curve | `matched` | frac_lai2 | `verified` |
| frac_sw_gro | numeric | fraction | - | frsw_gro | real | Fraction of field capacity to initiate growth of tropical plants during monsoon season | `matched` | frac_sw_gro | `verified` |
| aeration | numeric | none | - | aeration | real | Aeration stress factor | `matched` | aeration | `verified` |
| rsd_pctcov | numeric | none | 0.15..0.6 | rsd_pctcov | real | Resisude factor for precent cover equation | `matched` | rsd_pctcov | `verified` |
| rsd_covfac | numeric | none | 0.02..0.09 | rsd_covfac | real | Residue factor for surface cover (C factor) equation | `matched` | rsd_covfac | `verified` |
| description | string | none | - | - | - | Description of the plant | `spreadsheet_only` | - | `mismatch` |
| - | - | none | - | meta_frac | real | reads plants.plt avg_lig_frac | `source_only` | - | - |
| - | - | none | - | str_frac | real | reads plants.plt ab_lig_frac (used as above-ground lignin) | `source_only` | - | - |
| - | - | none | - | lig_frac | real | reads plants.plt bg_lig_frac (used as below-ground lignin) | `source_only` | - | - |
| - | - | - | - | pl_class | character | - | `source_only` | - | - |

## pond_cell.gw

| Spreadsheet name | Type | Units | Range | Source name | Type | Description | Status | Editor DB name | Editor check |
|---|---|---|---|---|---|---|---|---|---|
| - | - | - | - | dum_id | integer | - | `source_only` | - | - |
| - | - | - | - | cell_num | integer | - | `source_only` | - | - |
| - | - | - | - | dum4 | real | - | `source_only` | - | - |

## ponds.gw

| Spreadsheet name | Type | Units | Range | Source name | Type | Description | Status | Editor DB name | Editor check |
|---|---|---|---|---|---|---|---|---|---|
| - | - | - | - | id | integer | recharge pond id | `source_only` | - | - |
| - | - | m2 | - | area | real | recharge pond surface area | `source_only` | - | - |
| - | - | - | - | chan | integer | channel which provides water to the recharge pond | `source_only` | - | - |
| - | - | - | - | canal | integer | canal which provides water to the recharge pond | `source_only` | - | - |
| - | - | - | - | unl | integer | flag for outside source (1 = outside source) | `source_only` | - | - |
| - | - | m/d | - | bed_k | real | hydraulic conductivity of the pond bed sediments | `source_only` | - | - |
| - | - | - | - | wsta | integer | weather station id | `source_only` | - | - |
| - | - | - | - | evap_co | real | pond evaporation coefficient | `source_only` | - | - |
| - | - | - | - | yr_start | integer | - | `source_only` | - | - |
| - | - | - | - | mo_start | integer | - | `source_only` | - | - |
| - | - | - | - | dy_start | integer | - | `source_only` | - | - |
| - | - | g/m3 | - | unl_conc | real | solute concentrations for an outside water source | `source_only` | - | - |

## print.prt

| Spreadsheet name | Type | Units | Range | Source name | Type | Description | Status | Editor DB name | Editor check |
|---|---|---|---|---|---|---|---|---|---|
| n_yrs_skip | integer | none | - | nyskip | integer | Number of years to skip for output printing | `matched` | nyskip | `verified` |
| jd_start | integer | none | 0..366 | day_start | integer | Julian day to start printing output | `matched` | day_start | `verified` |
| yrc_start | integer | none | 0..0 | yrc_start | integer | Calendar year to start printing output | `matched` | yrc_start | `verified` |
| jd_end | integer | none | 0..366 | day_end | integer | Julian day to end printing output | `matched` | day_end | `verified` |
| yrc_end | integer | none | 0..2020 | yrc_end | integer | Calendar year to end printing output | `matched` | yrc_end | `verified` |
| interval | integer | none | - | int_day | integer | Interval between daily printing within period | `matched` | interval | `verified` |
| aa_int_cnt | integer | none | - | aa_numint | integer | Number of print intervals for average annual period | `matched` | - | `mismatch` |
| aa_int | integer | - | - | - | - | Number of print interval | `spreadsheet_only` (structural) | - | `mismatch` |
| aa_yrs | integer | none | - | - | - | End years for average annual periods | `spreadsheet_only` | - | `mismatch` |
| csvout | string | none | - | csvout | character | Character 'n' or 'y' print file | `matched` | csvout | `verified` |
| db_files | string | - | - | - | - | - | `spreadsheet_only` (structural) | - | `mismatch` |
| dbout | string | none | - | - | - | Character 'n' or 'y' print file | `spreadsheet_only` | - | `mismatch` |
| cdfout | string | none | - | cdfout | character | Character 'n' or 'y' print file | `matched` | cdfout | `verified` |
| crop_yld | string | none | - | crop_yld | character | Character a=prints ave ann (def); y=prints yearly; b=prints both ave ann and yearly; n== no print; | `matched` | crop_yld | `verified` |
| other | integer | - | - | - | - | Number of print interval | `spreadsheet_only` (structural) | - | `mismatch` |
| mgtout | string | none | - | mgtout | character | Character 'n' or 'y' print file | `matched` | mgtout | `verified` |
| hydcon | string | none | - | hydcon | character | Character 'n' or 'y' print file | `matched` | hydcon | `verified` |
| fdcout | string | none | - | fdcout | character | Character 'n' or 'y' print file | `matched` | fdcout | `verified` |
| obj_out | string | none | - | - | - | Spatial object and type of output | `spreadsheet_only` (structural) | - | `mismatch` |
| daily1 | string | none | - | - | - | Daily output yes or no | `spreadsheet_only` | - | `mismatch` |
| monthly1 | string | none | - | - | - | Monthly output yes or no | `spreadsheet_only` | - | `mismatch` |
| yearly1 | string | none | - | - | - | Yearly output yes or no | `spreadsheet_only` | - | `mismatch` |
| avann1 | string | none | - | - | - | Average annual output yes or no | `spreadsheet_only` | - | `mismatch` |
| daily2 | string | none | - | - | - | Daily output yes or no | `spreadsheet_only` | - | `mismatch` |
| monthly2 | string | none | - | - | - | Monthly output yes or no | `spreadsheet_only` | - | `mismatch` |
| yearly2 | string | none | - | - | - | Yearly output yes or no | `spreadsheet_only` | - | `mismatch` |
| avann2 | string | none | - | - | - | Average annual output yes or no | `spreadsheet_only` | - | `mismatch` |
| daily3 | string | none | - | - | - | Daily output yes or no | `spreadsheet_only` | - | `mismatch` |
| monthly3 | string | none | - | - | - | Monthly output yes or no | `spreadsheet_only` | - | `mismatch` |
| yearly3 | string | none | - | - | - | Yearly output yes or no | `spreadsheet_only` | - | `mismatch` |
| avann3 | string | none | - | - | - | Average annual output yes or no | `spreadsheet_only` | - | `mismatch` |
| daily4 | string | none | - | - | - | Daily output yes or no | `spreadsheet_only` | - | `mismatch` |
| monthly4 | string | none | - | - | - | Monthly output yes or no | `spreadsheet_only` | - | `mismatch` |
| yearly4 | string | none | - | - | - | Yearly output yes or no | `spreadsheet_only` | - | `mismatch` |
| avann4 | string | none | - | - | - | Average annual output yes or no | `spreadsheet_only` | - | `mismatch` |
| daily5 | string | none | - | - | - | Daily output yes or no | `spreadsheet_only` | - | `mismatch` |
| monthly5 | string | none | - | - | - | Monthly output yes or no | `spreadsheet_only` | - | `mismatch` |
| yearly5 | string | none | - | - | - | Yearly output yes or no | `spreadsheet_only` | - | `mismatch` |
| avann5 | string | none | - | - | - | Average annual output yes or no | `spreadsheet_only` | - | `mismatch` |
| daily6 | string | none | - | - | - | Daily output yes or no | `spreadsheet_only` | - | `mismatch` |
| monthly6 | string | none | - | - | - | Monthly output yes or no | `spreadsheet_only` | - | `mismatch` |
| yearly6 | string | none | - | - | - | Yearly output yes or no | `spreadsheet_only` | - | `mismatch` |
| avann6 | string | none | - | - | - | Average annual output yes or no | `spreadsheet_only` | - | `mismatch` |
| daily7 | string | none | - | - | - | Daily output yes or no | `spreadsheet_only` | - | `mismatch` |
| monthly7 | string | none | - | - | - | Monthly output yes or no | `spreadsheet_only` | - | `mismatch` |
| yearly7 | string | none | - | - | - | Yearly output yes or no | `spreadsheet_only` | - | `mismatch` |
| avann7 | string | none | - | - | - | Average annual output yes or no | `spreadsheet_only` | - | `mismatch` |
| daily8 | string | none | - | - | - | Daily output yes or no | `spreadsheet_only` | - | `mismatch` |
| monthly8 | string | none | - | - | - | Monthly output yes or no | `spreadsheet_only` | - | `mismatch` |
| yearly8 | string | none | - | - | - | Yearly output yes or no | `spreadsheet_only` | - | `mismatch` |
| avann8 | string | none | - | - | - | Average annual output yes or no | `spreadsheet_only` | - | `mismatch` |
| daily9 | string | none | - | - | - | Daily output yes or no | `spreadsheet_only` | - | `mismatch` |
| monthly9 | string | none | - | - | - | Monthly output yes or no | `spreadsheet_only` | - | `mismatch` |
| yearly9 | string | none | - | - | - | Yearly output yes or no | `spreadsheet_only` | - | `mismatch` |
| avann9 | string | none | - | - | - | Average annual output yes or no | `spreadsheet_only` | - | `mismatch` |
| daily10 | string | none | - | - | - | Daily output yes or no | `spreadsheet_only` | - | `mismatch` |
| monthly10 | string | none | - | - | - | Monthly output yes or no | `spreadsheet_only` | - | `mismatch` |
| yearly10 | string | none | - | - | - | Yearly output yes or no | `spreadsheet_only` | - | `mismatch` |
| avann10 | string | none | - | - | - | Average annual output yes or no | `spreadsheet_only` | - | `mismatch` |
| daily11 | string | none | - | - | - | Daily output yes or no | `spreadsheet_only` | - | `mismatch` |
| monthly11 | string | none | - | - | - | Monthly output yes or no | `spreadsheet_only` | - | `mismatch` |
| yearly11 | string | none | - | - | - | Yearly output yes or no | `spreadsheet_only` | - | `mismatch` |
| avann11 | string | none | - | - | - | Average annual output yes or no | `spreadsheet_only` | - | `mismatch` |
| daily12 | string | none | - | - | - | Daily output yes or no | `spreadsheet_only` | - | `mismatch` |
| monthly12 | string | none | - | - | - | Monthly output yes or no | `spreadsheet_only` | - | `mismatch` |
| yearly12 | string | none | - | - | - | Yearly output yes or no | `spreadsheet_only` | - | `mismatch` |
| avann12 | string | none | - | - | - | Average annual output yes or no | `spreadsheet_only` | - | `mismatch` |
| daily13 | string | none | - | - | - | Daily output yes or no | `spreadsheet_only` | - | `mismatch` |
| monthly13 | string | none | - | - | - | Monthly output yes or no | `spreadsheet_only` | - | `mismatch` |
| yearly13 | string | none | - | - | - | Yearly output yes or no | `spreadsheet_only` | - | `mismatch` |
| avann13 | string | none | - | - | - | Average annual output yes or no | `spreadsheet_only` | - | `mismatch` |
| daily14 | string | none | - | - | - | Daily output yes or no | `spreadsheet_only` | - | `mismatch` |
| monthly14 | string | none | - | - | - | Monthly output yes or no | `spreadsheet_only` | - | `mismatch` |
| yearly14 | string | none | - | - | - | Yearly output yes or no | `spreadsheet_only` | - | `mismatch` |
| avann14 | string | none | - | - | - | Average annual output yes or no | `spreadsheet_only` | - | `mismatch` |
| daily15 | string | none | - | - | - | Daily output yes or no | `spreadsheet_only` | - | `mismatch` |
| monthly15 | string | none | - | - | - | Monthly output yes or no | `spreadsheet_only` | - | `mismatch` |
| yearly15 | string | none | - | - | - | Yearly output yes or no | `spreadsheet_only` | - | `mismatch` |
| avann15 | string | none | - | - | - | Average annual output yes or no | `spreadsheet_only` | - | `mismatch` |
| daily17 | string | none | - | - | - | Daily output yes or no | `spreadsheet_only` | - | `mismatch` |
| monthly17 | string | none | - | - | - | Monthly output yes or no | `spreadsheet_only` | - | `mismatch` |
| yearly17 | string | none | - | - | - | Yearly output yes or no | `spreadsheet_only` | - | `mismatch` |
| avann17 | string | none | - | - | - | Average annual output yes or no | `spreadsheet_only` | - | `mismatch` |
| daily18 | string | none | - | - | - | Daily output yes or no | `spreadsheet_only` | - | `mismatch` |
| monthly18 | string | none | - | - | - | Monthly output yes or no | `spreadsheet_only` | - | `mismatch` |
| yearly18 | string | none | - | - | - | Yearly output yes or no | `spreadsheet_only` | - | `mismatch` |
| avann18 | string | none | - | - | - | Average annual output yes or no | `spreadsheet_only` | - | `mismatch` |
| daily16 | string | none | - | - | - | Daily output yes or no | `spreadsheet_only` | - | `mismatch` |
| monthly16 | string | none | - | - | - | Monthly output yes or no | `spreadsheet_only` | - | `mismatch` |
| yearly16 | string | none | - | - | - | Yearly output yes or no | `spreadsheet_only` | - | `mismatch` |
| avann16 | string | none | - | - | - | Average annual output yes or no | `spreadsheet_only` | - | `mismatch` |
| daily19 | string | none | - | - | - | Daily output yes or no | `spreadsheet_only` | - | `mismatch` |
| monthly19 | string | none | - | - | - | Monthly output yes or no | `spreadsheet_only` | - | `mismatch` |
| yearly19 | string | none | - | - | - | Yearly output yes or no | `spreadsheet_only` | - | `mismatch` |
| avann19 | string | none | - | - | - | Average annual output yes or no | `spreadsheet_only` | - | `mismatch` |
| daily20 | string | none | - | - | - | Daily output yes or no | `spreadsheet_only` | - | `mismatch` |
| monthly20 | string | none | - | - | - | Monthly output yes or no | `spreadsheet_only` | - | `mismatch` |
| yearly20 | string | none | - | - | - | Yearly output yes or no | `spreadsheet_only` | - | `mismatch` |
| avann20 | string | none | - | - | - | Average annual output yes or no | `spreadsheet_only` | - | `mismatch` |
| daily21 | string | none | - | - | - | Daily output yes or no | `spreadsheet_only` | - | `mismatch` |
| monthly21 | string | none | - | - | - | Monthly output yes or no | `spreadsheet_only` | - | `mismatch` |
| yearly21 | string | none | - | - | - | Yearly output yes or no | `spreadsheet_only` | - | `mismatch` |
| avann21 | string | none | - | - | - | Average annual output yes or no | `spreadsheet_only` | - | `mismatch` |
| daily22 | string | none | - | - | - | Daily output yes or no | `spreadsheet_only` | - | `mismatch` |
| monthly22 | string | none | - | - | - | Monthly output yes or no | `spreadsheet_only` | - | `mismatch` |
| yearly22 | string | none | - | - | - | Yearly output yes or no | `spreadsheet_only` | - | `mismatch` |
| avann22 | string | none | - | - | - | Average annual output yes or no | `spreadsheet_only` | - | `mismatch` |
| daily23 | string | none | - | - | - | Daily output yes or no | `spreadsheet_only` | - | `mismatch` |
| monthly23 | string | none | - | - | - | Monthly output yes or no | `spreadsheet_only` | - | `mismatch` |
| yearly23 | string | none | - | - | - | Yearly output yes or no | `spreadsheet_only` | - | `mismatch` |
| avann23 | string | none | - | - | - | Average annual output yes or no | `spreadsheet_only` | - | `mismatch` |
| daily24 | string | none | - | - | - | Daily output yes or no | `spreadsheet_only` | - | `mismatch` |
| monthly24 | string | none | - | - | - | Monthly output yes or no | `spreadsheet_only` | - | `mismatch` |
| yearly24 | string | none | - | - | - | Yearly output yes or no | `spreadsheet_only` | - | `mismatch` |
| avann24 | string | none | - | - | - | Average annual output yes or no | `spreadsheet_only` | - | `mismatch` |
| daily25 | string | none | - | - | - | Daily output yes or no | `spreadsheet_only` | - | `mismatch` |
| monthly25 | string | none | - | - | - | Monthly output yes or no | `spreadsheet_only` | - | `mismatch` |
| yearly25 | string | none | - | - | - | Yearly output yes or no | `spreadsheet_only` | - | `mismatch` |
| avann25 | string | none | - | - | - | Average annual output yes or no | `spreadsheet_only` | - | `mismatch` |
| daily26 | string | none | - | - | - | Daily output yes or no | `spreadsheet_only` | - | `mismatch` |
| monthly26 | string | none | - | - | - | Monthly output yes or no | `spreadsheet_only` | - | `mismatch` |
| yearly26 | string | none | - | - | - | Yearly output yes or no | `spreadsheet_only` | - | `mismatch` |
| avann26 | string | none | - | - | - | Average annual output yes or no | `spreadsheet_only` | - | `mismatch` |
| daily27 | string | none | - | - | - | Daily output yes or no | `spreadsheet_only` | - | `mismatch` |
| monthly27 | string | none | - | - | - | Monthly output yes or no | `spreadsheet_only` | - | `mismatch` |
| yearly27 | string | none | - | - | - | Yearly output yes or no | `spreadsheet_only` | - | `mismatch` |
| avann27 | string | none | - | - | - | Average annual output yes or no | `spreadsheet_only` | - | `mismatch` |
| daily28 | string | none | - | - | - | Daily output yes or no | `spreadsheet_only` | - | `mismatch` |
| monthly28 | string | none | - | - | - | Monthly output yes or no | `spreadsheet_only` | - | `mismatch` |
| yearly28 | string | none | - | - | - | Yearly output yes or no | `spreadsheet_only` | - | `mismatch` |
| avann28 | string | none | - | - | - | Average annual output yes or no | `spreadsheet_only` | - | `mismatch` |
| daily29 | string | none | - | - | - | Daily output yes or no | `spreadsheet_only` | - | `mismatch` |
| monthly29 | string | none | - | - | - | Monthly output yes or no | `spreadsheet_only` | - | `mismatch` |
| yearly29 | string | none | - | - | - | Yearly output yes or no | `spreadsheet_only` | - | `mismatch` |
| avann29 | string | none | - | - | - | Average annual output yes or no | `spreadsheet_only` | - | `mismatch` |
| daily30 | string | none | - | - | - | Daily output yes or no | `spreadsheet_only` | - | `mismatch` |
| monthly30 | string | none | - | - | - | Monthly output yes or no | `spreadsheet_only` | - | `mismatch` |
| yearly30 | string | none | - | - | - | Yearly output yes or no | `spreadsheet_only` | - | `mismatch` |
| avann30 | string | none | - | - | - | Average annual output yes or no | `spreadsheet_only` | - | `mismatch` |
| daily31 | string | none | - | - | - | Daily output yes or no | `spreadsheet_only` | - | `mismatch` |
| monthly31 | string | none | - | - | - | Monthly output yes or no | `spreadsheet_only` | - | `mismatch` |
| yearly31 | string | none | - | - | - | Yearly output yes or no | `spreadsheet_only` | - | `mismatch` |
| avann31 | string | none | - | - | - | Average annual output yes or no | `spreadsheet_only` | - | `mismatch` |
| daily32 | string | none | - | - | - | Daily output yes or no | `spreadsheet_only` | - | `mismatch` |
| monthly32 | string | none | - | - | - | Monthly output yes or no | `spreadsheet_only` | - | `mismatch` |
| yearly32 | string | none | - | - | - | Yearly output yes or no | `spreadsheet_only` | - | `mismatch` |
| avann32 | string | none | - | - | - | Average annual output yes or no | `spreadsheet_only` | - | `mismatch` |
| daily33 | string | none | - | - | - | Daily output yes or no | `spreadsheet_only` | - | `mismatch` |
| monthly33 | string | none | - | - | - | Monthly output yes or no | `spreadsheet_only` | - | `mismatch` |
| yearly33 | string | none | - | - | - | Yearly output yes or no | `spreadsheet_only` | - | `mismatch` |
| avann33 | string | none | - | - | - | Average annual output yes or no | `spreadsheet_only` | - | `mismatch` |
| daily34 | string | none | - | - | - | Daily output yes or no | `spreadsheet_only` | - | `mismatch` |
| monthly34 | string | none | - | - | - | Monthly output yes or no | `spreadsheet_only` | - | `mismatch` |
| yearly34 | string | none | - | - | - | Yearly output yes or no | `spreadsheet_only` | - | `mismatch` |
| avann34 | string | none | - | - | - | Average annual output yes or no | `spreadsheet_only` | - | `mismatch` |
| daily35 | string | none | - | - | - | Daily output yes or no | `spreadsheet_only` | - | `mismatch` |
| monthly35 | string | none | - | - | - | Monthly output yes or no | `spreadsheet_only` | - | `mismatch` |
| yearly35 | string | none | - | - | - | Yearly output yes or no | `spreadsheet_only` | - | `mismatch` |
| avann35 | string | none | - | - | - | Average annual output yes or no | `spreadsheet_only` | - | `mismatch` |
| daily36 | string | none | - | - | - | Daily output yes or no | `spreadsheet_only` | - | `mismatch` |
| monthly36 | string | none | - | - | - | Monthly output yes or no | `spreadsheet_only` | - | `mismatch` |
| yearly36 | string | none | - | - | - | Yearly output yes or no | `spreadsheet_only` | - | `mismatch` |
| avann36 | string | none | - | - | - | Average annual output yes or no | `spreadsheet_only` | - | `mismatch` |
| daily37 | string | none | - | - | - | Daily output yes or no | `spreadsheet_only` | - | `mismatch` |
| monthly37 | string | none | - | - | - | Monthly output yes or no | `spreadsheet_only` | - | `mismatch` |
| yearly37 | string | none | - | - | - | Yearly output yes or no | `spreadsheet_only` | - | `mismatch` |
| avann37 | string | none | - | - | - | Average annual output yes or no | `spreadsheet_only` | - | `mismatch` |
| daily38 | string | none | - | - | - | Daily output yes or no | `spreadsheet_only` | - | `mismatch` |
| monthly38 | string | none | - | - | - | Monthly output yes or no | `spreadsheet_only` | - | `mismatch` |
| yearly38 | string | none | - | - | - | Yearly output yes or no | `spreadsheet_only` | - | `mismatch` |
| aveann38 | string | none | - | - | - | Average annual output yes or no | `spreadsheet_only` | - | `mismatch` |
| daily39 | string | none | - | - | - | Daily output yes or no | `spreadsheet_only` | - | `mismatch` |
| monthly39 | string | none | - | - | - | Monthly output yes or no | `spreadsheet_only` | - | `mismatch` |
| yearly39 | string | none | - | - | - | Yearly output yes or no | `spreadsheet_only` | - | `mismatch` |
| aveann39 | string | none | - | - | - | Average annual output yes or no | `spreadsheet_only` | - | `mismatch` |
| daily40 | string | none | - | - | - | Daily output yes or no | `spreadsheet_only` | - | `mismatch` |
| monthly40 | string | none | - | - | - | Monthly output yes or no | `spreadsheet_only` | - | `mismatch` |
| yearly40 | string | none | - | - | - | Yearly output yes or no | `spreadsheet_only` | - | `mismatch` |
| aveann40 | string | none | - | - | - | Average annual output yes or no | `spreadsheet_only` | - | `mismatch` |
| daily41 | string | none | - | - | - | Daily output yes or no | `spreadsheet_only` | - | `mismatch` |
| monthly41 | string | none | - | - | - | Monthly output yes or no | `spreadsheet_only` | - | `mismatch` |
| yearly41 | string | none | - | - | - | Yearly output yes or no | `spreadsheet_only` | - | `mismatch` |
| aveann41 | string | none | - | - | - | Average annual output yes or no | `spreadsheet_only` | - | `mismatch` |
| daily42 | string | none | - | - | - | Daily output yes or no | `spreadsheet_only` | - | `mismatch` |
| monthly42 | string | none | - | - | - | Monthly output yes or no | `spreadsheet_only` | - | `mismatch` |
| yearly42 | string | none | - | - | - | Yearly output yes or no | `spreadsheet_only` | - | `mismatch` |
| aveann42 | string | none | - | - | - | Average annual output yes or no | `spreadsheet_only` | - | `mismatch` |
| daily43 | string | none | - | - | - | Daily output yes or no | `spreadsheet_only` | - | `mismatch` |
| monthly43 | string | none | - | - | - | Monthly output yes or no | `spreadsheet_only` | - | `mismatch` |
| yearly43 | string | none | - | - | - | Yearly output yes or no | `spreadsheet_only` | - | `mismatch` |
| aveann43 | string | none | - | - | - | Average annual output yes or no | `spreadsheet_only` | - | `mismatch` |
| daily44 | string | none | - | - | - | Daily output yes or no | `spreadsheet_only` | - | `mismatch` |
| monthly44 | string | none | - | - | - | Monthly output yes or no | `spreadsheet_only` | - | `mismatch` |
| yearly44 | string | none | - | - | - | Yearly output yes or no | `spreadsheet_only` | - | `mismatch` |
| aveann44 | string | none | - | - | - | Average annual output yes or no | `spreadsheet_only` | - | `mismatch` |
| daily45 | string | none | - | - | - | Daily output yes or no | `spreadsheet_only` | - | `mismatch` |
| monthly45 | string | none | - | - | - | Monthly output yes or no | `spreadsheet_only` | - | `mismatch` |
| yearly45 | string | none | - | - | - | Yearly output yes or no | `spreadsheet_only` | - | `mismatch` |
| aveann45 | string | none | - | - | - | Average annual output yes or no | `spreadsheet_only` | - | `mismatch` |
| daily46 | string | none | - | - | - | Daily output yes or no | `spreadsheet_only` | - | `mismatch` |
| monthly46 | string | none | - | - | - | Monthly output yes or no | `spreadsheet_only` | - | `mismatch` |
| yearly46 | string | none | - | - | - | Yearly output yes or no | `spreadsheet_only` | - | `mismatch` |
| aveann46 | string | none | - | - | - | Average annual output yes or no | `spreadsheet_only` | - | `mismatch` |
| daily47 | string | none | - | - | - | Daily output yes or no | `spreadsheet_only` | - | `mismatch` |
| monthly47 | string | none | - | - | - | Monthly output yes or no | `spreadsheet_only` | - | `mismatch` |
| yearly47 | string | none | - | - | - | Yearly output yes or no | `spreadsheet_only` | - | `mismatch` |
| aveann47 | string | none | - | - | - | Average annual output yes or no | `spreadsheet_only` | - | `mismatch` |
| daily48 | string | none | - | - | - | Daily output yes or no | `spreadsheet_only` | - | `mismatch` |
| monthly48 | string | none | - | - | - | Monthly output yes or no | `spreadsheet_only` | - | `mismatch` |
| yearly48 | string | none | - | - | - | Yearly output yes or no | `spreadsheet_only` | - | `mismatch` |
| aveann49 | string | none | - | - | - | Average annual output yes or no | `spreadsheet_only` | - | `mismatch` |
| daily50 | string | none | - | - | - | Daily output yes or no | `spreadsheet_only` | - | `mismatch` |
| monthly50 | string | none | - | - | - | Monthly output yes or no | `spreadsheet_only` | - | `mismatch` |
| yearly50 | string | none | - | - | - | Yearly output yes or no | `spreadsheet_only` | - | `mismatch` |
| aveann50 | string | none | - | - | - | Average annual output yes or no | `spreadsheet_only` | - | `mismatch` |
| daily51 | string | none | - | - | - | Daily output yes or no | `spreadsheet_only` | - | `mismatch` |
| monthly51 | string | none | - | - | - | Monthly output yes or no | `spreadsheet_only` | - | `mismatch` |
| yearly51 | string | none | - | - | - | Yearly output yes or no | `spreadsheet_only` | - | `mismatch` |
| aveann51 | string | none | - | - | - | Average annual output yes or no | `spreadsheet_only` | - | `mismatch` |
| daily52 | string | none | - | - | - | Daily output yes or no | `spreadsheet_only` | - | `mismatch` |
| monthly52 | string | none | - | - | - | Monthly output yes or no | `spreadsheet_only` | - | `mismatch` |
| yearly52 | string | none | - | - | - | Yearly output yes or no | `spreadsheet_only` | - | `mismatch` |
| aveann52 | string | none | - | - | - | Average annual output yes or no | `spreadsheet_only` | - | `mismatch` |
| daily53 | string | none | - | - | - | Daily output yes or no | `spreadsheet_only` | - | `mismatch` |
| monthly53 | string | none | - | - | - | Monthly output yes or no | `spreadsheet_only` | - | `mismatch` |
| yearly53 | string | none | - | - | - | Yearly output yes or no | `spreadsheet_only` | - | `mismatch` |
| aveann53 | string | none | - | - | - | Average annual output yes or no | `spreadsheet_only` | - | `mismatch` |
| - | - | - | - | use_obj_labels | character | character(len=1) :: carbout = "n" !! code to print carbon output; d = end of day; m = end of month; y = end of year; a = end of simulation; code to read in the print.prt print objects respecting the label of | `source_only` | - | - |
| - | - | - | - | name | character | - | `source_only` | - | - |
| - | - | - | - | d | character | - | `source_only` | - | - |
| - | - | - | - | m | character | - | `source_only` | - | - |
| - | - | - | - | y | character | - | `source_only` | - | - |
| - | - | - | - | a | character | - | `source_only` | - | - |

## puddle.ops

| Spreadsheet name | Type | Units | Range | Source name | Type | Description | Status | Editor DB name | Editor check |
|---|---|---|---|---|---|---|---|---|---|
| - | - | - | - | name | character | - | `source_only` | - | - |
| - | - | mm/h | - | wet_hc | real | hydraulic conductivity of upper layer of soil after puddling | `source_only` | - | - |
| - | - | ppm | - | sed | real | sediment concentration after puddling | `source_only` | - | - |
| - | - | ppm | - | orgn | real | organic N concentration after puddling | `source_only` | - | - |
| - | - | ppm | - | sedp | real | organic P concentration after puddling | `source_only` | - | - |
| - | - | ppm | - | no3 | real | NO3-N concentration after puddling | `source_only` | - | - |
| - | - | ppm | - | solp | real | mineral (soluble P) concentration after puddling | `source_only` | - | - |
| - | - | ppm | - | nh3 | real | NH3 concentration after puddling | `source_only` | - | - |
| - | - | ppm | - | no2 | real | NO2 concentration after puddling | `source_only` | - | - |

## pumpex.gw

| Spreadsheet name | Type | Units | Range | Source name | Type | Description | Status | Editor DB name | Editor check |
|---|---|---|---|---|---|---|---|---|---|
| - | - | - | - | header | character | - | `source_only` | - | - |
| - | - | - | - | pumpex_cell | integer | - | `source_only` | - | - |
| - | - | - | - | gw_pumpex_rates_tmp | real | - | `source_only` | - | - |
| - | - | - | - | pe_yr_s | integer | - | `source_only` | - | - |
| - | - | - | - | pe_dy_s | integer | - | `source_only` | - | - |
| - | - | - | - | pe_yr_e | integer | - | `source_only` | - | - |
| - | - | - | - | pe_dy_e | integer | - | `source_only` | - | - |

## rec_catunit.def

| Spreadsheet name | Type | Units | Range | Source name | Type | Description | Status | Editor DB name | Editor check |
|---|---|---|---|---|---|---|---|---|---|
| mreg | integer | - | - | - | - | - | `spreadsheet_only` | - | `unavailable` |
| numb | integer | - | - | - | - | point source cataloging unit numb define | `spreadsheet_only` | - | `unavailable` |
| pcu_out_name | string | - | - | name | character | point source cataloging unit name define | `matched` | - | `unavailable` |
| pcu_out_area | numeric | - | - | area_ha | real | point source cataloging unit area define | `matched` | - | `unavailable` |
| nspu | integer | - | - | nspu | integer | point source cataloging unit elements define | `matched` | - | `unavailable` |
| elem_cnt | integer | - | - | elem_cnt | integer | - | `matched` | - | `unavailable` |
| - | - | - | - | k | integer | - | `source_only` | - | - |

## rec_catunit.ele

| Spreadsheet name | Type | Units | Range | Source name | Type | Description | Status | Editor DB name | Editor check |
|---|---|---|---|---|---|---|---|---|---|
| numb | integer | - | - | - | - | point source cataloging unit numb | `spreadsheet_only` | - | `unavailable` |
| pcu_name | string | - | - | name | character | point source cataloging unit name | `matched` | - | `unavailable` |
| pcu_obj_typ | integer | - | - | obtyp | character | point source cataloging unit object type | `matched` | - | `unavailable` |
| pcu_obj_tyno | integer | - | - | obtypno | integer | point source cataloging unit object type number | `matched` | - | `unavailable` |
| pcu_bsn_frac | numeric | - | - | - | - | point source cataloging unit basin fraction | `spreadsheet_only` | - | `unavailable` |
| pcu_sub_frac | numeric | - | - | - | - | point source cataloging unit subbasin fraction | `spreadsheet_only` | - | `unavailable` |
| pcu_reg_frac | numeric | - | - | reg_frac | real | point source cataloging unit region fraction | `matched` | - | `unavailable` |
| - | - | - | - | k | integer | - | `source_only` | - | - |
| - | - | - | - | bsn_frac | real | fraction of element in basin (expansion factor) | `source_only` | - | - |
| - | - | - | - | ru_frac | real | fraction of element in ru (expansion factor) | `source_only` | - | - |

## rec_reg.def

| Spreadsheet name | Type | Units | Range | Source name | Type | Description | Status | Editor DB name | Editor check |
|---|---|---|---|---|---|---|---|---|---|
| mreg | integer | - | - | - | - | - | `spreadsheet_only` | - | `unavailable` |
| numb | integer | - | - | - | - | point source cataloging unit region numb | `spreadsheet_only` | - | `unavailable` |
| pcu_reg_name | string | - | - | name | character | point source cataloging unit region name | `matched` | - | `unavailable` |
| pcu_reg_area | numeric | - | - | area_ha | real | point source cataloging unit region area | `matched` | - | `unavailable` |
| nspu | integer | - | - | nspu | integer | point source cataloging unit region element | `matched` | - | `unavailable` |
| elem_cnt | integer | - | - | elem_cnt | integer | - | `matched` | - | `unavailable` |
| - | - | - | - | k | integer | - | `source_only` | - | - |

## recall.con

| Spreadsheet name | Type | Units | Range | Source name | Type | Description | Status | Editor DB name | Editor check |
|---|---|---|---|---|---|---|---|---|---|
| id | integer | - | - | - | - | number | `spreadsheet_only` | - | `unavailable` |
| name | string | - | - | name | character | The name of the connect unit | `matched` | - | `unavailable` |
| gis_id | string | - | - | gis_id | integer | GIS id | `matched` | - | `unavailable` |
| area | numeric | ha | - | area_ha | real | AREA | `matched` | - | `unavailable` |
| lat | numeric | dec degrees | -90..90 | lat | real | latitude | `matched` | - | `unavailable` |
| lon | numeric | dec degrees | -180..180 | long | real | longitude | `matched` | - | `unavailable` |
| elev | numeric | m | 1..7000 | elev | real | Elevation of recall | `matched` | - | `unavailable` |
| rec | integer | - | - | props | integer | recallOBJECT | `matched` | - | `unavailable` |
| wst | string | - | - | - | - | weather station number | `spreadsheet_only` | - | `unavailable` |
| cst | integer | - | - | constit | integer | Constituent data pointer to pesticides, pathogens, metals, salts | `matched` | - | `unavailable` |
| ovfl | numeric | - | - | props2 | integer | Points to the connections of spatial objects for overbank flooding | `matched` | - | `unavailable` |
| rule | integer | - | - | ruleset | character | Ruleset pointer for flow fraction of hydrograph | `matched` | - | `unavailable` |
| out_tot | integer | - | 1..12 | src_tot | integer | Total number of outgoing objects | `matched` | - | `unavailable` |
| rec_id | integer | - | - | - | - | number | `spreadsheet_only` (structural) | - | `unavailable` |
| obj_numb | integer | - | 1..10 | - | - | Object number 1-10 | `spreadsheet_only` (structural) | - | `unavailable` |
| obj_typ | string | - | - | obtyp_out | character | Outflow object type | `matched` | - | `unavailable` |
| obj_id | integer | - | - | - | - | Outflow object identifier for specified type | `spreadsheet_only` | - | `unavailable` |
| hyd_typ | string | - | - | - | - | Outflow hydrograph type | `spreadsheet_only` | - | `unavailable` |
| frac | numeric | - | 0..1 | frac_out | real | Fraction of hydrograph set to object | `matched` | - | `unavailable` |
| description | string | none | - | - | - | - | `spreadsheet_only` (structural) | - | `unavailable` |
| - | - | - | - | num | integer | spatial object number- ie hru number corresponding to sequential command number | `source_only` | - | - |
| - | - | - | - | wst_c | character | weather station name | `source_only` | - | - |
| - | - | - | - | obtypno_out | integer | outflow object type name | `source_only` | - | - |
| - | - | - | - | htyp_out | character | outflow hyd type (ie 1=tot, 2= recharge, 3=surf, etc) | `source_only` | - | - |

## recall_db.rec

| Spreadsheet name | Type | Units | Range | Source name | Type | Description | Status | Editor DB name | Editor check |
|---|---|---|---|---|---|---|---|---|---|
| - | - | - | - | k | integer | - | `source_only` | - | - |
| - | - | - | - | name | character | - | `source_only` | - | - |
| - | - | - | - | org_min.name | character | - | `source_only` | - | - |
| - | - | - | - | org_min.units | character | mass, conc | `source_only` | - | - |
| - | - | - | - | org_min.tstep | character | day, mo, yr | `source_only` | - | - |
| - | - | - | - | pest.name | character | - | `source_only` | - | - |
| - | - | - | - | pest.units | character | mass, conc | `source_only` | - | - |
| - | - | - | - | pest.tstep | character | day, mo, yr | `source_only` | - | - |
| - | - | - | - | path.name | character | - | `source_only` | - | - |
| - | - | - | - | path.units | character | mass, conc | `source_only` | - | - |
| - | - | - | - | path.tstep | character | day, mo, yr | `source_only` | - | - |
| - | - | - | - | hmet.name | character | - | `source_only` | - | - |
| - | - | - | - | hmet.units | character | mass, conc | `source_only` | - | - |
| - | - | - | - | hmet.tstep | character | day, mo, yr | `source_only` | - | - |
| - | - | - | - | salt.name | character | - | `source_only` | - | - |
| - | - | - | - | salt.units | character | mass, conc | `source_only` | - | - |
| - | - | - | - | salt.tstep | character | day, mo, yr | `source_only` | - | - |
| - | - | - | - | constit.name | character | - | `source_only` | - | - |
| - | - | - | - | constit.units | character | mass, conc | `source_only` | - | - |
| - | - | - | - | constit.tstep | character | day, mo, yr | `source_only` | - | - |

## res_catunit.def

| Spreadsheet name | Type | Units | Range | Source name | Type | Description | Status | Editor DB name | Editor check |
|---|---|---|---|---|---|---|---|---|---|
| mreg | integer | - | - | - | - | reservoir cataloging out numb | `spreadsheet_only` | - | `unavailable` |
| numb | integer | - | - | - | - | reservoir cataloging out numb | `spreadsheet_only` | - | `unavailable` |
| res_out_name | string | - | - | name | character | reservoir cataloging out name | `matched` | - | `unavailable` |
| res_out_area | numeric | - | - | area_ha | real | reservoir cataloging out area | `matched` | - | `unavailable` |
| nspu | integer | - | - | nspu | integer | reservoir cataloging out elments | `matched` | - | `unavailable` |
| elem | integer | - | - | elem_cnt | integer | - | `matched` | - | `unavailable` |
| - | - | - | - | k | integer | - | `source_only` | - | - |

## res_catunit.ele

| Spreadsheet name | Type | Units | Range | Source name | Type | Description | Status | Editor DB name | Editor check |
|---|---|---|---|---|---|---|---|---|---|
| numb | integer | - | - | - | - | reservoir cataloging units numb | `spreadsheet_only` | - | `unavailable` |
| rcu_name | string | - | - | name | character | reservoir cataloging units name | `matched` | - | `unavailable` |
| rcu_obj_typ | integer | - | - | obtyp | character | reservoir cataloging units object type | `matched` | - | `unavailable` |
| rcu_obj_typ_no | integer | - | - | obtypno | integer | reservoir cataloging units numb | `matched` | - | `unavailable` |
| rcu_bsn_frac | numeric | - | - | bsn_frac | real | reservoir cataloging units numb | `matched` | - | `unavailable` |
| rcu_sub_frac | numeric | - | - | - | - | reservoir cataloging units numb | `spreadsheet_only` | - | `unavailable` |
| rcu_reg_frac | numeric | - | - | reg_frac | real | reservoir cataloging units numb | `matched` | - | `unavailable` |
| - | - | - | - | k | integer | - | `source_only` | - | - |
| - | - | - | - | ru_frac | real | fraction of element in ru (expansion factor) | `source_only` | - | - |

## res_conds.dat

| Spreadsheet name | Type | Units | Range | Source name | Type | Description | Status | Editor DB name | Editor check |
|---|---|---|---|---|---|---|---|---|---|
| - | - | - | - | name | character | - | `source_only` | - | - |
| - | - | - | - | num_conds | integer | - | `source_only` | - | - |
| - | - | - | - | num_modules | integer | - | `source_only` | - | - |

## res_reg.def

| Spreadsheet name | Type | Units | Range | Source name | Type | Description | Status | Editor DB name | Editor check |
|---|---|---|---|---|---|---|---|---|---|
| mreg | integer | - | - | - | - | reservoir cataloging unit region define numb | `spreadsheet_only` | - | `unavailable` |
| numb | integer | - | - | - | - | reservoir cataloging unit region define numb | `spreadsheet_only` | - | `unavailable` |
| res_cal_name | string | - | - | name | character | reservoir cataloging unit region define name | `matched` | - | `unavailable` |
| res_cal_area | numeric | - | - | area_ha | real | reservoir cataloging unit region define area | `matched` | - | `unavailable` |
| nspu | integer | - | - | nspu | integer | reservoir cataloging unit region define element | `matched` | - | `unavailable` |
| elem | integer | - | - | elem_cnt | integer | - | `matched` | - | `unavailable` |
| - | - | - | - | k | integer | - | `source_only` | - | - |

## res_rel.dtl

| Spreadsheet name | Type | Units | Range | Source name | Type | Description | Status | Editor DB name | Editor check |
|---|---|---|---|---|---|---|---|---|---|
| id | - | - | - | - | - | ID | `spreadsheet_only` (structural) | - | `mismatch` |
| mdtbl | string | - | - | - | - | - | `spreadsheet_only` | - | `mismatch` |
| description | string | - | - | - | - | Description, not used in the model | `spreadsheet_only` (structural) | - | `mismatch` |
| dtbl_name | string | - | - | name | character | name of the decision table | `matched` | name | `verified` |
| conds | integer | - | - | conds | integer | number of conditions | `matched` | conds | `verified` |
| alts | integer | - | - | alts | integer | number of alternatives | `matched` | alts | `verified` |
| acts | integer | - | - | acts | integer | number of actions | `matched` | acts | `verified` |
| dtbl_name | string | - | - | name | character | name of the decision table | `matched` | name | `verified` |
| ord | integer | - | - | - | - | printing order | `spreadsheet_only` | - | `mismatch` |
| description | string | - | - | - | - | Description, not used in the model | `spreadsheet_only` (structural) | - | `mismatch` |
| cond_var | string | - | - | var | character | condition variable (ie volume, flow, sw, time, etc) | `matched` | var | `verified` |
| obj | string | - | - | ob | character | object variable (ie res, hru, canal, etc) | `matched` | obj | `verified` |
| obj_numb | integer | - | - | ob_num | integer | object number | `matched` | - | `mismatch` |
| lim_var | string | - | - | lim_var | character | limit variable (ie evol, pvol, fc, ul, etc) | `matched` | lim_var | `verified` |
| lim_op | string | - | - | lim_op | character | limit operator (*,+,-) | `matched` | lim_op | `verified` |
| lim_const | numeric | - | - | lim_const | real | limit constant | `matched` | lim_const | `verified` |
| alt1 | string | - | - | alt | character | condition alternatives | `matched` | alt | `verified` |
| alt2 | string | - | - | alt | character | condition alternatives | `matched` | alt | `verified` |
| alt3 | string | - | - | alt | character | condition alternatives | `matched` | alt | `verified` |
| alt4 | string | - | - | alt | character | condition alternatives | `matched` | alt | `verified` |
| alt5 | string | - | - | alt | character | condition alternatives | `matched` | alt | `verified` |
| alt6 | string | - | - | alt | character | condition alternatives | `matched` | alt | `verified` |
| alt7 | string | - | - | alt | character | condition alternatives | `matched` | alt | `verified` |
| alt8 | string | - | - | alt | character | condition alternatives | `matched` | alt | `verified` |
| alt9 | string | - | - | alt | character | condition alternatives | `matched` | alt | `verified` |
| alt10 | string | - | - | alt | character | condition alternatives | `matched` | alt | `verified` |
| dtbl_name | string | - | - | name | character | header for actions | `matched` | name | `verified` |
| ord | integer | - | - | - | - | printing order | `spreadsheet_only` | - | `mismatch` |
| description | string | - | - | - | - | Description, not used in the model | `spreadsheet_only` (structural) | - | `mismatch` |
| act_typ | string | - | - | typ | character | type of action | `matched` | act_typ | `verified` |
| obj | string | - | - | ob | character | action objects | `matched` | obj | `verified` |
| obj_num | string | - | - | ob_num | integer | action object number | `matched` | obj_num | `verified` |
| act_name | string | - | - | name | character | action name | `matched` | name | `verified` |
| act_option | string | - | - | option | character | action option | `matched` | option | `verified` |
| const | string | - | - | const | real | constant used for rate, days, etc. | `matched` | const | `verified` |
| const2 | string | - | - | const2 | real | constant used for rate, days, etc. | `matched` | const2 | `verified` |
| file_pointer | string | - | - | file_pointer | character | pointer for option (ie weir equation pointer) | `matched` | - | `mismatch` |
| out1 | string | - | - | act_outcomes | character | action outcomes ('y' to perform action; 'n' to not perform) | `matched` | - | `mismatch` |
| out2 | string | - | - | act_outcomes | character | action outcomes ('y' to perform action; 'n' to not perform) | `matched` | - | `mismatch` |
| out3 | string | - | - | act_outcomes | character | action outcomes ('y' to perform action; 'n' to not perform) | `matched` | - | `mismatch` |
| out4 | string | - | - | act_outcomes | character | action outcomes ('y' to perform action; 'n' to not perform) | `matched` | - | `mismatch` |
| out5 | string | - | - | act_outcomes | character | action outcomes ('y' to perform action; 'n' to not perform) | `matched` | - | `mismatch` |
| out6 | string | - | - | act_outcomes | character | action outcomes ('y' to perform action; 'n' to not perform) | `matched` | - | `mismatch` |
| out7 | string | - | - | act_outcomes | character | action outcomes ('y' to perform action; 'n' to not perform) | `matched` | - | `mismatch` |
| out8 | string | - | - | act_outcomes | character | action outcomes ('y' to perform action; 'n' to not perform) | `matched` | - | `mismatch` |
| out9 | string | - | - | act_outcomes | character | action outcomes ('y' to perform action; 'n' to not perform) | `matched` | - | `mismatch` |
| out10 | string | - | - | act_outcomes | character | action outcomes ('y' to perform action; 'n' to not perform) | `matched` | - | `mismatch` |

## rescell.gw

| Spreadsheet name | Type | Units | Range | Source name | Type | Description | Status | Editor DB name | Editor check |
|---|---|---|---|---|---|---|---|---|---|
| - | - | - | - | res_cell | integer | - | `source_only` | - | - |
| - | - | - | - | res_id | integer | - | `source_only` | - | - |
| - | - | - | - | res_stage | real | - | `source_only` | - | - |

## reservoir.con

| Spreadsheet name | Type | Units | Range | Source name | Type | Description | Status | Editor DB name | Editor check |
|---|---|---|---|---|---|---|---|---|---|
| id | integer | none | - | num | integer | Reservoir number | `matched` | id | `verified` |
| name | string | - | - | name | character | Reservoir name | `matched` | name | `verified` |
| gis_id | string | - | - | gis_id | integer | GIS id | `matched` | gis_id | `verified` |
| area | numeric | ha | - | area_ha | real | Area | `matched` | area | `verified` |
| lat | numeric | dec degrees | -90..90 | lat | real | Latitude | `matched` | lat | `verified` |
| lon | numeric | dec degrees | -180..180 | long | real | Longitude | `matched` | lon | `verified` |
| elev | numeric | m | 1..7000 | elev | real | Elevation of channel | `matched` | elev | `verified` |
| res | integer | none | - | props | integer | Pointer to reservoir properties | `matched` | - | `mismatch` |
| wst | string | none | - | wst_c | character | Weather station number | `matched` | wst | `verified` |
| cst | integer | none | - | constit | integer | Pointer to constituent data (pesticides, pathogens, metals, salts) | `matched` | cst | `verified` |
| ovfl | numeric | none | - | props2 | integer | Pointer to the connections of spatial objects for overbank flooding | `matched` | ovfl | `verified` |
| rule | integer | none | - | ruleset | character | Pointer to ruleset for flow fraction of hydrograph | `matched` | rule | `verified` |
| out_tot | integer | none | 1..12 | src_tot | integer | Total number of outgoing hydrographs | `matched` | out_tot | `verified` |
| res_id | integer | none | - | - | - | Reservoir number | `spreadsheet_only` (structural) | - | `mismatch` |
| obj_numb | integer | none | 1..10 | - | - | Object number 1-10 | `spreadsheet_only` (structural) | - | `mismatch` |
| obj_typ | string | - | - | obtyp_out | character | Outflow object type | `matched` | obj_typ | `verified` |
| obj_id | integer | none | - | obtypno_out | integer | Outflow object identifier for specified type | `matched` | obj_id | `verified` |
| hyd_typ | string | - | - | htyp_out | character | Outflow hydrograph type | `matched` | hyd_typ | `verified` |
| frac | numeric | none | 0..1 | frac_out | real | Fraction of hydrograph sent to object | `matched` | frac | `verified` |
| description | string | none | - | - | - | - | `spreadsheet_only` (structural) | - | `mismatch` |

## reservoir.res

| Spreadsheet name | Type | Units | Range | Source name | Type | Description | Status | Editor DB name | Editor check |
|---|---|---|---|---|---|---|---|---|---|
| id | string | none | - | k | integer | Reservoir number | `matched` | id | `verified` |
| name | string | - | - | name | character | Reservoir name | `matched` | name | `verified` |
| description | string | - | - | - | - | Description, not used in the model | `spreadsheet_only` (structural) | - | `mismatch` |
| init | string | none | - | init | character | Pointer to reservoir initial parameter set | `matched` | init | `verified` |
| hyd | string | none | - | hyd | character | Pointer to reservoir hydrology parameter set | `matched` | hyd | `verified` |
| rel | string | none | - | release | character | 0=simulated; 1=measured outflow | `matched` | rel | `verified` |
| sed | string | none | - | sed | character | Pointer to reservoir sediment parameter set | `matched` | sed | `verified` |
| nut | string | none | - | nut | character | Pointer to reservoir nutrient parameter set | `matched` | nut | `verified` |

## reservoir.res_cs

| Spreadsheet name | Type | Units | Range | Source name | Type | Description | Status | Editor DB name | Editor check |
|---|---|---|---|---|---|---|---|---|---|
| - | - | - | - | k | integer | - | `source_only` | - | - |
| - | - | - | - | pst | character | pesticide inputs-points to pesticide.res | `source_only` | - | - |
| - | - | - | - | weir | character | weir inputs-points to weir.res Jaehak 2022 | `source_only` | - | - |
| - | - | - | - | salt | character | salt inputs - points to salt_res rtb salt | `source_only` | - | - |
| - | - | - | - | cs | character | constituent inputs - points to cs_res rtb cs | `source_only` | - | - |

## rout_unit.con

| Spreadsheet name | Type | Units | Range | Source name | Type | Description | Status | Editor DB name | Editor check |
|---|---|---|---|---|---|---|---|---|---|
| id | integer | none | - | num | integer | Subbasin Number | `matched` | id | `verified` |
| name | string | - | - | name | character | Subbasin Name | `matched` | name | `verified` |
| gis_id | string | - | - | gis_id | integer | GIS id | `matched` | gis_id | `verified` |
| area | numeric | ha | - | area_ha | real | Area | `matched` | area | `verified` |
| lat | numeric | dec degrees | -90..90 | lat | real | Latitude | `matched` | lat | `verified` |
| lon | numeric | dec degrees | -180..180 | long | real | Longitude | `matched` | lon | `verified` |
| elev | numeric | m | 1..7000 | elev | real | Elevation of subbasin | `matched` | elev | `verified` |
| rtu | integer | none | - | props | integer | Pointer to subbasin properties | `matched` | - | `mismatch` |
| wst | string | none | - | wst_c | character | Weather station number | `matched` | wst | `verified` |
| cst | integer | none | - | constit | integer | Constituent data pointer to pesticides, pathogens, metals, salts | `matched` | cst | `verified` |
| ovfl | integer | none | - | props2 | integer | Points to the connections of spatial objects for overbank flooding | `matched` | ovfl | `verified` |
| rule | integer | none | - | ruleset | character | Ruleset pointer for flow fraction of hydrograph | `matched` | rule | `verified` |
| out_tot | integer | none | 1..12 | src_tot | integer | Outgoing object count | `matched` | out_tot | `verified` |
| rtu_id | integer | none | - | - | - | Subbasin number | `spreadsheet_only` (structural) | - | `mismatch` |
| obj_numb | integer | none | 1..10 | - | - | Object number 1-10 | `spreadsheet_only` (structural) | - | `mismatch` |
| obj_typ | string | - | - | obtyp_out | character | Outflow object type | `matched` | obj_typ | `verified` |
| obj_id | integer | none | - | obtypno_out | integer | Outflow object identifier for specified type | `matched` | obj_id | `verified` |
| hyd_typ | string | - | - | htyp_out | character | Outflow hydrograph type | `matched` | hyd_typ | `verified` |
| frac | numeric | none | 0..1 | frac_out | real | Fraction of hydrograph sent to object | `matched` | frac | `verified` |
| description | string | none | - | - | - | - | `spreadsheet_only` (structural) | - | `mismatch` |

## rout_unit.def

| Spreadsheet name | Type | Units | Range | Source name | Type | Description | Status | Editor DB name | Editor check |
|---|---|---|---|---|---|---|---|---|---|
| id | integer | none | - | numb | integer | Routing unit Number | `matched` | - | `unavailable` |
| name | string | - | - | name | character | Routing unit Name | `matched` | - | `unavailable` |
| elem_tot | integer | none | - | nspu | integer | Number of spatial elements groups defining the routing unit up to 10 | `matched` | - | `unavailable` |
| id | integer | none | - | - | - | Routing unit Number | `spreadsheet_only` (structural) | - | `unavailable` |
| elem_numb | integer | none | 1..10 | - | - | 1-10 number of element group | `spreadsheet_only` (structural) | - | `unavailable` |
| elem | integer | none | - | elem_cnt | integer | Element | `matched` | - | `unavailable` |

## rout_unit.ele

| Spreadsheet name | Type | Units | Range | Source name | Type | Description | Status | Editor DB name | Editor check |
|---|---|---|---|---|---|---|---|---|---|
| id | integer | none | - | k | integer | Element number | `matched` | id | `verified` |
| name | string | - | - | name | character | Element name | `matched` | name | `verified` |
| obj_typ | string | - | - | obtyp | character | Object type of element | `matched` | obj_typ | `verified` |
| obj_typ_no | integer | none | - | obtypno | integer | Object identifier for specified type of element | `matched` | - | `mismatch` |
| frac | numeric | none | 0..1 | frac | real | Fraction of routing unit represented by element | `matched` | frac | `verified` |
| del | string | none | - | - | - | points to dr's in delratio.dat | `spreadsheet_only` | - | `mismatch` |
| - | - | - | - | dr_name | character | name of dr in delratio.del | `source_only` | - | - |

## rout_unit.rtu

| Spreadsheet name | Type | Units | Range | Source name | Type | Description | Status | Editor DB name | Editor check |
|---|---|---|---|---|---|---|---|---|---|
| id | integer | none | - | k | integer | Subbasin number | `matched` | id | `verified` |
| name | string | - | - | name | character | Subbasin name | `matched` | name | `verified` |
| description | string | - | - | - | - | Description, not used in the model | `spreadsheet_only` (structural) | - | `mismatch` |
| def | string | none | - | elem_def | character | Pointer to subbasin definition parameter set | `matched` | - | `mismatch` |
| del | string | none | - | elem_dr | character | Delivery ratio definition | `matched` | - | `mismatch` |
| topo | string | none | - | toposub_db | character | Pointer to subbasin topography parameter set | `matched` | topo | `verified` |
| fld | string | none | - | field_db | character | Field database definition | `matched` | - | `mismatch` |

## salt_aqu.ini

| Spreadsheet name | Type | Units | Range | Source name | Type | Description | Status | Editor DB name | Editor check |
|---|---|---|---|---|---|---|---|---|---|
| - | - | - | - | name | character | name of the constituent - points to constituent database | `source_only` | - | - |
| - | - | g/m3 | - | conc | real | salt ion concentration at start of simulation | `source_only` | - | - |
| - | - | fractions | - | frac | real | salt mineral fractions at start of simulation | `source_only` | - | - |

## salt_atmo.cli

| Spreadsheet name | Type | Units | Range | Source name | Type | Description | Status | Editor DB name | Editor check |
|---|---|---|---|---|---|---|---|---|---|
| - | - | - | - | station_name | character | station name | `source_only` | - | - |
| - | - | - | - | rf | real | concentration in rainfall - mg/l | `source_only` | - | - |
| - | - | - | - | dry | real | dry deposition - kg/ha/yr | `source_only` | - | - |
| - | - | - | - | rfmo | real | - | `source_only` | - | - |
| - | - | - | - | drymo | real | - | `source_only` | - | - |
| - | - | - | - | rfyr | real | - | `source_only` | - | - |
| - | - | - | - | dryyr | real | - | `source_only` | - | - |

## salt_channel.ini

| Spreadsheet name | Type | Units | Range | Source name | Type | Description | Status | Editor DB name | Editor check |
|---|---|---|---|---|---|---|---|---|---|
| - | - | - | - | name | character | name of the constituent - points to salt ion database | `source_only` | - | - |
| - | - | g/m3 | - | conc | real | salt ion concentration at start of simulation | `source_only` | - | - |

## salt_fertilizer.frt

| Spreadsheet name | Type | Units | Range | Source name | Type | Description | Status | Editor DB name | Editor check |
|---|---|---|---|---|---|---|---|---|---|
| - | - | - | - | fertnm | character | - | `source_only` | - | - |
| - | - | kg so4/ha | - | so4 | real | fertilizer load of so4 (kg/ha) | `source_only` | - | - |
| - | - | kg ca/ha | - | ca | real | fertilizer load of ca (kg/ha) | `source_only` | - | - |
| - | - | kg mg/ha | - | mg | real | fertilizer load of mg (kg/ha) | `source_only` | - | - |
| - | - | kg na/ha | - | na | real | fertilizer load of na (kg/ha) | `source_only` | - | - |
| - | - | kg k/ha | - | k | real | fertilizer load of k (kg/ha) | `source_only` | - | - |
| - | - | kg cl/ha | - | cl | real | fertilizer load of cl (kg/ha) | `source_only` | - | - |
| - | - | kg co3/ha | - | co3 | real | fertilizer load of co3 (kg/ha) | `source_only` | - | - |
| - | - | kg hco3/ha | - | hco3 | real | fertilizer load of hco3 (kg/ha) | `source_only` | - | - |

## salt_hru.ini

| Spreadsheet name | Type | Units | Range | Source name | Type | Description | Status | Editor DB name | Editor check |
|---|---|---|---|---|---|---|---|---|---|
| id | - | - | - | - | - | ID | `spreadsheet_only` (structural) | - | `mismatch` |
| name | string | - | - | name | character | name of the constituent - points to constituent database | `matched` | name | `verified` |
| description | string | - | - | - | - | - | `spreadsheet_only` (structural) | - | `mismatch` |
| salt_hru_soil | numeric | - | - | - | - | amt of constituent in soil at start of simulation | `spreadsheet_only` | - | `mismatch` |
| salt_hru_plt | numeric | - | - | - | - | amt of constituent on plant at start of simulation | `spreadsheet_only` | - | `mismatch` |
| - | - | ppm | - | soil | real | amount of constituent in soil at start of simulation | `source_only` | - | - |
| - | - | ppm or #cfu/m^2 | - | plt | real | amount of constituent on plant at start of simulation | `source_only` | - | - |

## salt_recall.rec

| Spreadsheet name | Type | Units | Range | Source name | Type | Description | Status | Editor DB name | Editor check |
|---|---|---|---|---|---|---|---|---|---|
| - | - | - | - | k | integer | - | `source_only` | - | - |
| - | - | - | - | name | character | - | `source_only` | - | - |
| - | - | - | - | typ | integer | recall type - 1=day, 2=mon, 3=year | `source_only` | - | - |
| - | - | - | - | filename | character | filename | `source_only` | - | - |
| - | - | - | - | nbyr | integer | - | `source_only` | - | - |
| - | - | - | - | jday | integer | - | `source_only` | - | - |
| - | - | - | - | mo | integer | - | `source_only` | - | - |
| - | - | - | - | day_mo | integer | - | `source_only` | - | - |
| - | - | - | - | iyr | integer | - | `source_only` | - | - |
| - | - | - | - | ob_typ | character | - | `source_only` | - | - |
| - | - | - | - | ob_name | character | - | `source_only` | - | - |
| - | - | - | - | salt | real | salt ion mass (kg/ha) | `source_only` | - | - |

## satbuffer.str

| Spreadsheet name | Type | Units | Range | Source name | Type | Description | Status | Editor DB name | Editor check |
|---|---|---|---|---|---|---|---|---|---|
| - | - | - | - | name | character | - | `source_only` | - | - |
| - | - | - | - | hru_src | integer | source of tile inflow | `source_only` | - | - |
| - | - | - | - | frac_src | real | fration of source hru contributing to tile flow | `source_only` | - | - |
| - | - | - | - | flocon_dtbl | character | decision table to control flow into buffer hru | `source_only` | - | - |
| - | - | - | - | hru_rcv | integer | receiving (buffer) hru | `source_only` | - | - |
| - | - | - | - | lyr | integer | soil layer for incoming tile flow (0 = surface) | `source_only` | - | - |

## scen_dtl.upd

| Spreadsheet name | Type | Units | Range | Source name | Type | Description | Status | Editor DB name | Editor check |
|---|---|---|---|---|---|---|---|---|---|
| - | - | - | - | max_hits | integer | maximum number of times the table will be executed | `source_only` | - | - |
| - | - | - | - | typ | character | type of table- "lu_change" checks all hru; "hru_fr_change" sets all hru fractions | `source_only` | - | - |
| - | - | - | - | dtbl | character | points to ruleset in conditional.ctl for scheduling the update | `source_only` | - | - |

## scen_lu.dtl

| Spreadsheet name | Type | Units | Range | Source name | Type | Description | Status | Editor DB name | Editor check |
|---|---|---|---|---|---|---|---|---|---|
| id | - | - | - | - | - | ID | `spreadsheet_only` (structural) | - | `mismatch` |
| mdtbl | string | - | - | - | - | - | `spreadsheet_only` | - | `mismatch` |
| description | string | - | - | - | - | Description, not used in the model | `spreadsheet_only` (structural) | - | `mismatch` |
| dtbl_name | string | - | - | name | character | name of the decision table | `matched` | name | `verified` |
| conds | integer | - | - | conds | integer | number of conditions | `matched` | conds | `verified` |
| alts | integer | - | - | alts | integer | number of alternatives | `matched` | alts | `verified` |
| acts | integer | - | - | acts | integer | number of actions | `matched` | acts | `verified` |
| dtbl_name | string | - | - | name | character | name of the decision table | `matched` | name | `verified` |
| description | string | - | - | - | - | Description, not used in the model | `spreadsheet_only` (structural) | - | `mismatch` |
| cond_var | string | - | - | var | character | condition variable (ie volume, flow, sw, time, etc) | `matched` | var | `verified` |
| obj | string | - | - | ob | character | object variable (ie res, hru, canal, etc) | `matched` | obj | `verified` |
| obj_numb | integer | - | - | ob_num | integer | object number | `matched` | - | `mismatch` |
| lim_var | string | - | - | lim_var | character | limit variable (ie evol, pvol, fc, ul, etc) | `matched` | lim_var | `verified` |
| lim_op | string | - | - | lim_op | character | limit operator (*,+,-) | `matched` | lim_op | `verified` |
| lim_const | numeric | - | - | lim_const | real | limit constant | `matched` | lim_const | `verified` |
| alt1 | string | - | - | alt | character | condition alternatives | `matched` | alt | `verified` |
| alt2 | string | - | - | alt | character | condition alternatives | `matched` | alt | `verified` |
| alt3 | string | - | - | alt | character | condition alternatives | `matched` | alt | `verified` |
| alt4 | string | - | - | alt | character | condition alternatives | `matched` | alt | `verified` |
| alt5 | string | - | - | alt | character | condition alternatives | `matched` | alt | `verified` |
| alt6 | string | - | - | alt | character | condition alternatives | `matched` | alt | `verified` |
| alt7 | string | - | - | alt | character | condition alternatives | `matched` | alt | `verified` |
| alt8 | string | - | - | alt | character | condition alternatives | `matched` | alt | `verified` |
| alt9 | string | - | - | alt | character | condition alternatives | `matched` | alt | `verified` |
| alt10 | string | - | - | alt | character | condition alternatives | `matched` | alt | `verified` |
| dtbl_name | string | - | - | name | character | header for actions | `matched` | name | `verified` |
| description | string | - | - | - | - | Description, not used in the model | `spreadsheet_only` (structural) | - | `mismatch` |
| act_typ | string | - | - | typ | character | type of action | `matched` | act_typ | `verified` |
| obj | string | - | - | ob | character | action objects | `matched` | obj | `verified` |
| obj_num | string | - | - | ob_num | integer | action object number | `matched` | obj_num | `verified` |
| act_name | string | - | - | name | character | action name | `matched` | name | `verified` |
| act_option | string | - | - | option | character | action option | `matched` | option | `verified` |
| const | string | - | - | const | real | constant used for rate, days, etc. | `matched` | const | `verified` |
| const2 | string | - | - | const2 | real | constant used for rate, days, etc. | `matched` | const2 | `verified` |
| file_pointer | string | - | - | file_pointer | character | pointer for option (ie weir equation pointer) | `matched` | - | `mismatch` |
| out1 | string | - | - | act_outcomes | character | action outcomes ('y' to perform action; 'n' to not perform) | `matched` | - | `mismatch` |
| out2 | string | - | - | act_outcomes | character | action outcomes ('y' to perform action; 'n' to not perform) | `matched` | - | `mismatch` |
| out3 | string | - | - | act_outcomes | character | action outcomes ('y' to perform action; 'n' to not perform) | `matched` | - | `mismatch` |
| out4 | string | - | - | act_outcomes | character | action outcomes ('y' to perform action; 'n' to not perform) | `matched` | - | `mismatch` |
| out5 | string | - | - | act_outcomes | character | action outcomes ('y' to perform action; 'n' to not perform) | `matched` | - | `mismatch` |
| out6 | string | - | - | act_outcomes | character | action outcomes ('y' to perform action; 'n' to not perform) | `matched` | - | `mismatch` |
| out7 | string | - | - | act_outcomes | character | action outcomes ('y' to perform action; 'n' to not perform) | `matched` | - | `mismatch` |
| out8 | string | - | - | act_outcomes | character | action outcomes ('y' to perform action; 'n' to not perform) | `matched` | - | `mismatch` |
| out9 | string | - | - | act_outcomes | character | action outcomes ('y' to perform action; 'n' to not perform) | `matched` | - | `mismatch` |
| out10 | string | - | - | act_outcomes | character | action outcomes ('y' to perform action; 'n' to not perform) | `matched` | - | `mismatch` |

## sed_nut.cha

| Spreadsheet name | Type | Units | Range | Source name | Type | Description | Status | Editor DB name | Editor check |
|---|---|---|---|---|---|---|---|---|---|
| name | - | none | - | name | character | - | `matched` | - | `unavailable` |
| description | - | none | - | - | - | - | `spreadsheet_only` | - | `unavailable` |
| order | - | none | 0..4 | order | character | - | `matched` | - | `unavailable` |
| pk_rto | - | none | 0..0.6 | pk_rto | real | ratio of peak to mean daily flow in channel | `matched` | - | `unavailable` |
| fp_inun_days | - | none | 0..1 | fp_inun_days | real | number of days fllod plain is inundated after flood | `matched` | - | `unavailable` |
| n_sol_part | - | none | 1.1..1.9 | n_sol_part | real | instream nitrogen soluble to particulate transformation coefficient | `matched` | - | `unavailable` |
| p_sol_part | - | none | 1.1..1.9 | p_sol_part | real | instream phosphorus soluble to particulate transformation coefficient | `matched` | - | `unavailable` |
| n_dep_enr | - | none | 1.1..1.9 | n_dep_enr | real | enrichment of N in remaining water - deposition = 1/enrichment ratio | `matched` | - | `unavailable` |
| p_dep_enr | - | none | 1.1..1.9 | p_dep_enr | real | enrichment of P in remaining water - deposition = 1/enrichment ratio | `matched` | - | `unavailable` |
| arc_len_fr | - | none | 1.1..1.9 | arc_len_fr | real | fraction of arc length where bank erosion occurs | `matched` | - | `unavailable` |
| part_size | - | none | 1.1..1.9 | - | - | - | `spreadsheet_only` | - | `unavailable` |
| wash_bed_fr | - | none | 1.1..1.9 | wash_bed_fr | real | fraction of bank erosion that is washload | `matched` | - | `unavailable` |
| - | - | ratio | - | n_setl | real | ratio of amount of N settling and sediment settling | `source_only` | - | - |
| - | - | ratio | - | p_setl | real | ratio of amount of P settling and sediment settling | `source_only` | - | - |
| - | - | - | - | bed_exp | real | bed erosion exponential coefficient | `source_only` | - | - |

## sediment.cha

| Spreadsheet name | Type | Units | Range | Source name | Type | Description | Status | Editor DB name | Editor check |
|---|---|---|---|---|---|---|---|---|---|
| id | - | - | - | - | - | ID | `spreadsheet_only` (structural) | - | `mismatch` |
| name | string | - | - | name | character | Channel sediment parameter set name | `matched` | name | `verified` |
| description | string | - | - | - | - | Description, not used in the model | `spreadsheet_only` (structural) | - | `mismatch` |
| sed_eqn | integer | none | 0..4 | eqn | integer | Sediment routine methods (0=original SWAT method;1=Bagnold's;2=Kodatie;3=Molinas Wu;4=Yang) | `matched` | sed_eqn | `verified` |
| erod_fact | numeric | none | 0..0.6 | cov1 | real | Channel erodibility factor (if SED_EQN=0 (0=non-erosive channel;1=no resistance to erosion)) or channel bank vegetation coefficient for critical shear stress (if SED_EQN!=0) | `matched` | erod_fact | `verified` |
| cov_fact | numeric | none | 0..1 | cov2 | real | Channel cover factor (if SED_EQN=0 (0=channel is completely protected from erosion by cover;1=no vegetative cover on channel)) or channel bed vegetation coefficient for critical shear stress (if SED_EQN!=0) | `matched` | cov_fact | `verified` |
| bd_bnk | numeric | g/cc | 1.1..1.9 | bnk_bd | real | Bulk density of channel bank sediment (1.1-1.9) | `matched` | bd_bnk | `verified` |
| bd_bed | numeric | g/cc | 1.1..1.9 | bed_bd | real | Bulk density of channel bed sediment (1.1-1.9) | `matched` | bd_bed | `verified` |
| kd_bnk | numeric | cm^3/N-s | 0.001..3.75 | bnk_kd | real | Erodibility of channel bank sediment by jet test | `matched` | kd_bnk | `verified` |
| kd_bed | numeric | cm^3/N-s | 0.001..3.75 | bed_kd | real | Erodibility of channel bed sediment by jet test | `matched` | kd_bed | `verified` |
| d50_bnk | numeric | μm | 1..10000 | bnk_d50 | real | D50 (median) particle size diameter of channel bank sediment | `matched` | d50_bnk | `verified` |
| d50_bed | numeric | μm | 1..10000 | bed_d50 | real | D50 (median) particle size diameter of channel bed sediment | `matched` | d50_bed | `verified` |
| css_bnk | numeric | N/m^2 | 0..400 | tc_bnk | real | Critical shear stress of channel bank | `matched` | css_bnk | `verified` |
| css_bed | numeric | N/m^2 | 0..400 | tc_bed | real | Critical shear stress of channel bed | `matched` | css_bed | `verified` |
| erod1 | numeric | none | 0..1 | erod(1) | real | Channel erodibility factor Jan (0=non-erosive channel;1=no resistance to erosion) | `matched` | erod1 | `verified` |
| erod2 | numeric | none | 0..1 | erod(2) | real | Channel erodibility factor Feb (0=non-erosive channel;1=no resistance to erosion) | `matched` | erod2 | `verified` |
| erod3 | numeric | none | 0..1 | erod(3) | real | Channel erodibility factor Mar (0=non-erosive channel;1=no resistance to erosion) | `matched` | erod3 | `verified` |
| erod4 | numeric | none | 0..1 | erod(4) | real | Channel erodibility factor Apr (0=non-erosive channel;1=no resistance to erosion) | `matched` | erod4 | `verified` |
| erod5 | numeric | none | 0..1 | erod(5) | real | Channel erodibility factor May (0=non-erosive channel;1=no resistance to erosion) | `matched` | erod5 | `verified` |
| erod6 | numeric | none | 0..1 | erod(6) | real | Channel erodibility factor Jun (0=non-erosive channel;1=no resistance to erosion) | `matched` | erod6 | `verified` |
| erod7 | numeric | none | 0..1 | erod(7) | real | Channel erodibility factor Jul (0=non-erosive channel;1=no resistance to erosion) | `matched` | erod7 | `verified` |
| erod8 | numeric | none | 0..1 | erod(8) | real | Channel erodibility factor Aug (0=non-erosive channel;1=no resistance to erosion) | `matched` | erod8 | `verified` |
| erod9 | numeric | none | 0..1 | erod(9) | real | Channel erodibility factor Sep (0=non-erosive channel;1=no resistance to erosion) | `matched` | erod9 | `verified` |
| erod10 | numeric | none | 0..1 | erod(10) | real | Channel erodibility factor Oct (0=non-erosive channel;1=no resistance to erosion) | `matched` | erod10 | `verified` |
| erod11 | numeric | none | 0..1 | erod(11) | real | Channel erodibility factor Nov (0=non-erosive channel;1=no resistance to erosion) | `matched` | erod11 | `verified` |
| erod12 | numeric | none | 0..1 | erod(12) | real | Channel erodibility factor Dec (0=non-erosive channel;1=no resistance to erosion) | `matched` | erod12 | `verified` |

## sediment.res

| Spreadsheet name | Type | Units | Range | Source name | Type | Description | Status | Editor DB name | Editor check |
|---|---|---|---|---|---|---|---|---|---|
| id | - | - | - | - | - | ID | `spreadsheet_only` (structural) | - | `mismatch` |
| name | string | - | - | name | character | Reservoir sediment name | `matched` | name | `verified` |
| nsed | numeric | kg/L | 1..5000 | nsed | real | Normal amount of sediment in reservoir (read in as mg/L and convert to kg/L) | `matched` | - | `mismatch` |
| d50 | numeric | μm | - | d50 | real | D50 | `matched` | d50 | `verified` |
| carbon | numeric | % | - | carbon | real | Organic carbon in suspended and benthis sediment | `matched` | carbon | `verified` |
| bd | numeric | t/m^3 | - | bd | real | Bulk density of benthic sediment | `matched` | bd | `verified` |
| sed_stl | numeric | none | - | sed_stlr | real | Sediment settling rate | `matched` | sed_stl | `verified` |
| stl_vel | numeric | m/d | - | velsetlr | real | Sediment settling velocity | `matched` | stl_vel | `verified` |

## septic.sep

| Spreadsheet name | Type | Units | Range | Source name | Type | Description | Status | Editor DB name | Editor check |
|---|---|---|---|---|---|---|---|---|---|
| id | - | - | - | - | - | ID | `spreadsheet_only` (structural) | - | `mismatch` |
| name | string | - | - | sepnm | character | septic name | `matched` | name | `verified` |
| q_rate | numeric | m^3/d | 0..1 | qs | real | flow rate of the septic tank effluent per capita | `matched` | q_rate | `verified` |
| bod | numeric | mg/l | 0..300 | bodconcs | real | biological oxygen demand of the septic tank effluent | `matched` | bod | `verified` |
| tss | numeric | mg/l | 0..300 | tssconcs | real | concentration of total suspended solid in the septic tank effluent | `matched` | tss | `verified` |
| nh4_n | numeric | mg/l | >=0 | nh4concs | real | concentration of total phosphorus in the septic tank effluent | `matched` | nh4_n | `verified` |
| no3_n | numeric | mg/l | >=0 | no3concs | real | concentration of nitrate in the septic tank effluent | `matched` | no3_n | `verified` |
| no2_n | numeric | mg/l | >=0 | no2concs | real | concentration of nitrite in the septic tank effluent | `matched` | no2_n | `verified` |
| org_n | numeric | mg/l | >=0 | orgnconcs | real | concentration of organic nitrogen in the septic tank effluent | `matched` | org_n | `verified` |
| min_p | numeric | mg/l | >=0 | minps | real | concentration of mineral phosphorus in the septic tank effluent | `matched` | min_p | `verified` |
| org_p | numeric | mg/l | >=0 | orgps | real | concentration of organic phosphorus in the septic tank effluent | `matched` | org_p | `verified` |
| fcoli | numeric | mg/l | >=0 | fcolis | real | concentration of fecal coliform in the septic tank effluent | `matched` | fcoli | `verified` |

## septic.str

| Spreadsheet name | Type | Units | Range | Source name | Type | Description | Status | Editor DB name | Editor check |
|---|---|---|---|---|---|---|---|---|---|
| id | - | - | - | - | - | ID | `spreadsheet_only` (structural) | - | `mismatch` |
| name | string | - | - | name | character | Septic system name | `matched` | name | `verified` |
| typ | integer | none | - | typ | integer | Septic system type | `matched` | typ | `verified` |
| yr | integer | none | - | yr | integer | Year the septic system became operational | `matched` | yr | `verified` |
| operation | integer | none | - | opt | integer | Septic system operation flag (1=active,2=failing,0=not operated) | `matched` | operation | `verified` |
| residents | numeric | none | - | cap | real | Number of permanent residents in the house | `matched` | residents | `verified` |
| area | numeric | m^2 | - | area | real | Average area of drainfield of individual septic systems | `matched` | area | `verified` |
| t_fail | integer | days | - | tfail | integer | Time until failing systems gets fixed | `matched` | t_fail | `verified` |
| dp_bioz | numeric | mm | - | z | real | Depth to the top of the biozone layer from the ground surface | `matched` | dp_bioz | `verified` |
| thk_bioz | numeric | mm | - | thk | real | Thickness of biozone layer | `matched` | thk_bioz | `verified` |
| cha_dist | numeric | km | - | strm_dist | real | Distance from the septic system to the stream | `matched` | cha_dist | `verified` |
| sep_dens | numeric | none | - | density | real | Number of septic systems per square kilometer | `matched` | sep_dens | `verified` |
| bm_dens | numeric | kg/m^3 | - | bd | real | Density of biomass | `matched` | bm_dens | `verified` |
| bod_decay | numeric | m^3/day | - | bod_dc | real | BOD decay rate coefficient | `matched` | bod_decay | `verified` |
| bod_conv | numeric | - | - | bod_conv | real | Conversion factor representing the proportion of mass bacterial growth and mass BOD degraded in the STE | `matched` | bod_conv | `verified` |
| fc_lin | numeric | none | - | fc1 | real | Linear coefficient for calculation of field capacity in the biozone | `matched` | fc_lin | `verified` |
| fc_exp | numeric | none | - | fc2 | real | Exponential coefficient for calculation of field capacity in the biozone | `matched` | fc_exp | `verified` |
| fecal_decay | numeric | m^3/day | - | fecal | real | Fecal coliform bacteria decay rate coefficient | `matched` | fecal_decay | `verified` |
| tds_conv | numeric | none | - | plq | real | Conversion factor for plaque from TDS | `matched` | tds_conv | `verified` |
| mort | numeric | none | - | mrt | real | Mortality rate coefficient | `matched` | mort | `verified` |
| resp | numeric | none | - | rsp | real | Respiration rate coefficient | `matched` | resp | `verified` |
| slough1 | numeric | none | - | slg1 | real | Slough-off calibration parameter | `matched` | slough1 | `verified` |
| slough2 | numeric | none | - | slg2 | real | Slough-off calibration parameter | `matched` | slough2 | `verified` |
| nit | numeric | none | - | nitr | real | Nitrification rate coefficient | `matched` | nit | `verified` |
| denit | numeric | none | - | denitr | real | Denitrification rate coefficient | `matched` | denit | `verified` |
| p_sorp | numeric | L/kg | - | pdistrb | real | Linear P sorption distribution coefficient | `matched` | p_sorp | `verified` |
| p_sorp_max | numeric | mg P/kg soil | - | psorpmax | real | Maximum P sorption capacity | `matched` | p_sorp_max | `verified` |
| solp_slp | numeric | none | - | solpslp | real | Slope of the linear effluent soluble P equation | `matched` | solp_slp | `verified` |
| solp_int | numeric | none | - | solpintc | real | Intercept of the linear effluent soluble P eq | `matched` | solp_int | `verified` |

## shade_factor.shf

| Spreadsheet name | Type | Units | Range | Source name | Type | Description | Status | Editor DB name | Editor check |
|---|---|---|---|---|---|---|---|---|---|
| - | - | none | - | jday | integer | day of the year | `source_only` | - | - |
| - | - | none | - | lsu | integer | landscape unit | `source_only` | - | - |
| - | - | none | - | value | real | shade factor value | `source_only` | - | - |

## slr.cli

| Spreadsheet name | Type | Units | Range | Source name | Type | Description | Status | Editor DB name | Editor check |
|---|---|---|---|---|---|---|---|---|---|
| slr_file | string | - | - | - | - | Solar radiation file names | `spreadsheet_only` | - | `unavailable` |
| - | - | - | - | slr_n | character | - | `source_only` | - | - |
| - | - | - | - | filename | character | - | `source_only` | - | - |

## snow.sno

| Spreadsheet name | Type | Units | Range | Source name | Type | Description | Status | Editor DB name | Editor check |
|---|---|---|---|---|---|---|---|---|---|
| id | - | - | - | - | - | ID | `spreadsheet_only` (structural) | - | `mismatch` |
| name | string | - | - | name | character | Snow melt parameter set name | `matched` | name | `verified` |
| fall_tmp | numeric | deg C | -5..5 | falltmp | real | Snowfall temperature | `matched` | fall_tmp | `verified` |
| melt_tmp | numeric | deg C | -5..5 | melttmp | real | Snow melt base temperature | `matched` | melt_tmp | `verified` |
| melt_max | numeric | mm/deg C/day | 0..10 | meltmx | real | Maximum melt rate for snow during year (June 21) | `matched` | melt_max | `verified` |
| melt_min | numeric | mm/deg C/day | 0..10 | meltmn | real | Minimum melt rate for snow during year (Dec 21) | `matched` | melt_min | `verified` |
| tmp_lag | numeric | none | 0..1 | timp | real | Snow pack temperature lag factor | `matched` | tmp_lag | `verified` |
| snow_h2o | numeric | mm H20 | 0..500 | covmx | real | Minimum snow water content | `matched` | snow_h2o | `verified` |
| cov50 | numeric | none | 0..1 | cov50 | real | Fraction of SNOW_WC | `matched` | cov50 | `verified` |
| snow_init | numeric | mm H20 | 0..5 | init_mm | real | initial snow water content at start of simulation | `matched` | snow_init | `verified` |

## soil_plant.ini

| Spreadsheet name | Type | Units | Range | Source name | Type | Description | Status | Editor DB name | Editor check |
|---|---|---|---|---|---|---|---|---|---|
| id | integer | - | - | - | - | ID | `spreadsheet_only` (structural) | - | `mismatch` |
| name | string | - | - | name | character | - | `matched` | name | `verified` |
| description | string | - | - | - | - | - | `spreadsheet_only` (structural) | - | `mismatch` |
| sw_frac | integer | none | >=1 | sw_frac | real | - | `matched` | sw_frac | `verified` |
| nut | string | - | - | nutc | character | crosswalked with name in nutrients.sol | `matched` | - | `mismatch` |
| pest | string | - | - | pestc | character | crosswalked with name in pest_hru.ini | `matched` | pest | `verified` |
| path | string | - | - | pathc | character | crosswalked with name in path_hru.ini | `matched` | path | `verified` |
| salt | string | - | - | saltc | character | crosswalked with name in hmet_hru.ini | `matched` | salt | `verified` |
| hmet | string | - | - | hmetc | character | crosswalked with name from salt_hru.ini | `matched` | hmet | `verified` |
| - | - | - | - | csc | character | rtb cs | `source_only` | - | - |

## soils.sol

| Spreadsheet name | Type | Units | Range | Source name | Type | Description | Status | Editor DB name | Editor check |
|---|---|---|---|---|---|---|---|---|---|
| id | integer | - | - | - | - | ID | `spreadsheet_only` (structural) | - | `mismatch` |
| name | string | NA | - | snam | character | Soil name | `matched` | name | `verified` |
| description | string | - | - | - | - | Description, not used in the model | `spreadsheet_only` (structural) | - | `mismatch` |
| lay_cnt | integer | none | 1..10 | nly | integer | Layer count | `matched` | nly | `verified` |
| hyd_grp | string | NA | - | hydgrp | character | Hydrologic soil group | `matched` | hyd_grp | `verified` |
| dp_tot | numeric | mm | 0..3500 | zmx | real | Depth of soil | `matched` | dp_tot | `verified` |
| anion_excl | numeric | fraction | 0.01..1 | anion_excl | real | Fraction of porosity from which anions are excluded | `matched` | anion_excl | `verified` |
| perc_crk | numeric | mm H2O | 0..1 | crk | real | Percolation due to crack flow ArcSWAT: Crack volume potential of soil (m^3/m^3) | `matched` | perc_crk | `verified` |
| texture | string | - | - | texture | character | Soil texture | `matched` | texture | `verified` |
| soil_name | string | - | - | - | - | Soil name | `spreadsheet_only` (structural) | - | `mismatch` |
| lay_numb | integer | none | 1..10 | - | - | Layer number (1-10) | `spreadsheet_only` (structural) | - | `mismatch` |
| dp | numeric | mm | 0..3500 | z | real | Depth to bottom of layer | `matched` | dp | `verified` |
| bd | numeric | g/cm^3 | 0.9..2.5 | bd | real | bulk density of layer | `matched` | bd | `verified` |
| awc | numeric | mm/mm | 0..1 | awc | real | Available water capacity of soil layer | `matched` | awc | `verified` |
| soil_k | numeric | mm/hr | 0..2000 | k | real | Saturated hydraulic conductivity of soil layer | `matched` | soil_k | `verified` |
| carbon | numeric | % | 0.05..10 | cbn | real | Carbon in soil layer | `matched` | carbon | `verified` |
| clay | numeric | % | 0..100 | clay | real | Clay in soil layer | `matched` | clay | `verified` |
| silt | numeric | % | 0..100 | silt | real | Silt in soil layer | `matched` | silt | `verified` |
| sand | numeric | % | 0..100 | sand | real | Sand in soil layer | `matched` | sand | `verified` |
| rock | numeric | % | 0..100 | rock | real | Rock in soil layer | `matched` | rock | `verified` |
| alb | numeric | none | 0..0.25 | alb | real | Soil albedo when soil is moist | `matched` | alb | `verified` |
| usle_k | numeric | mm/hr | 0..0.65 | usle_k | real | USLE equation soil erodibility (K) factor | `matched` | usle_k | `verified` |
| ec | numeric | dS/m | 0..100 | ec | real | Electrical conductivity of soil layer | `matched` | ec | `verified` |
| caco3 | numeric | % | 0..65 | cal | real | CaCO3 in soil layer | `matched` | caco3 | `verified` |
| ph | numeric | none | 3..10 | ph | real | pH value of soil layer | `matched` | ph | `verified` |

## soils_lte.sol

| Spreadsheet name | Type | Units | Range | Source name | Type | Description | Status | Editor DB name | Editor check |
|---|---|---|---|---|---|---|---|---|---|
| id | - | - | - | - | - | id | `spreadsheet_only` (structural) | - | `mismatch` |
| name | string | - | - | texture | character | texture for lte soil | `matched` | name | `verified` |
| description | numeric | - | - | - | - | Description, not used in model | `spreadsheet_only` (structural) | - | `mismatch` |
| awc_lte | numeric | mm/mm | 0..1 | awc | real | available water capacity for lte soil | `matched` | awc | `verified` |
| por_lte | numeric | mm/mm | 0..1 | por | real | porosity for lte soil | `matched` | por | `verified` |
| scon_lte | numeric | mm/hr | 0..2000 | scon | real | saturated condcutivity for lte soil | `matched` | scon | `verified` |

## solute.gw

| Spreadsheet name | Type | Units | Range | Source name | Type | Description | Status | Editor DB name | Editor check |
|---|---|---|---|---|---|---|---|---|---|
| - | - | - | - | name | character | - | `source_only` | - | - |
| - | - | - | - | gwsol_sorb | real | - | `source_only` | - | - |
| - | - | - | - | gwsol_rctn | real | - | `source_only` | - | - |
| - | - | - | - | canal_out_conc | real | - | `source_only` | - | - |

## sweep.ops

| Spreadsheet name | Type | Units | Range | Source name | Type | Description | Status | Editor DB name | Editor check |
|---|---|---|---|---|---|---|---|---|---|
| id | - | - | - | - | - | ID | `spreadsheet_only` (structural) | - | `mismatch` |
| name | string | - | - | name | character | Street sweeping operation name | `matched` | name | `verified` |
| description | string | - | - | - | - | Description, not used in the model | `spreadsheet_only` (structural) | - | `mismatch` |
| swp_eff | numeric | fraction | 0..1 | eff | real | Removal efficiency of sweeping operation | `matched` | swp_eff | `verified` |
| frac_curb | numeric | fraction | 0..1 | fr_curb | real | Fraction of the curb length that is sweepable | `matched` | frac_curb | `verified` |

## temperature.cha

| Spreadsheet name | Type | Units | Range | Source name | Type | Description | Status | Editor DB name | Editor check |
|---|---|---|---|---|---|---|---|---|---|
| id | integer | - | - | - | - | ID | `spreadsheet_only` (structural) | - | `unavailable` |
| name | string | - | - | name | character | Channel lite name | `matched` | - | `unavailable` |
| sno_mlt | integer | none | - | sno_mlt | real | snow melt | `matched` | - | `unavailable` |
| gw | string | none | - | gw | real | groundwater | `matched` | - | `unavailable` |
| sur_lat | string | none | - | sur_lat | real | surface lat | `matched` | - | `unavailable` |
| bulk_co | numeric | m | - | - | - | bulk coefficient | `spreadsheet_only` | - | `unavailable` |
| air_lag | numeric | m | - | - | - | air lag | `spreadsheet_only` | - | `unavailable` |
| - | - | days | - | sno_lag | real | average air temperature lag to snowmelt (1-3) | `source_only` | - | - |
| - | - | days | - | gw_lag | real | average air temperature lag to gw flow (200-365) | `source_only` | - | - |
| - | - | days | - | surf_lag | real | average air temperature lag to surface runoff (2-5) | `source_only` | - | - |
| - | - | days | - | lat_lag | real | average air temperature lag to lateral flow (5-10) | `source_only` | - | - |
| - | - | none | - | lat_lag_coef | real | lat air lag coefficient | `source_only` | - | - |
| - | - | none | - | surf_lag_coef | real | surf air lag coefficient (used also for snow) | `source_only` | - | - |
| - | - | none | - | gw_lag_coef | real | gw air lag coefficient | `source_only` | - | - |
| - | - | none | - | hex_coef1 | real | calibrate dew point | `source_only` | - | - |
| - | - | none | - | hex_coef2 | real | calibrate channel geometry | `source_only` | - | - |
| - | - | none | - | sf_on | integer | shade factor file activation, 1= file, 0= take value from cal file | `source_only` | - | - |
| - | - | none | - | ssff | real | ssff value default 0.5, range 0-1 | `source_only` | - | - |

## tile.gw

| Spreadsheet name | Type | Units | Range | Source name | Type | Description | Status | Editor DB name | Editor check |
|---|---|---|---|---|---|---|---|---|---|
| - | - | - | - | tile | integer | tile drainage flag (0=no tile; 1=tile is present) | `source_only` | - | - |

## tiledrain.str

| Spreadsheet name | Type | Units | Range | Source name | Type | Description | Status | Editor DB name | Editor check |
|---|---|---|---|---|---|---|---|---|---|
| id | - | - | - | - | - | ID | `spreadsheet_only` (structural) | - | `mismatch` |
| name | string | - | - | name | character | Tile practice name | `matched` | name | `verified` |
| description | string | - | - | - | - | Description, not used in the model | `spreadsheet_only` (structural) | - | `mismatch` |
| dp | numeric | mm | 0..6000 | depth | real | Depth of drain tube from the soil surface | `matched` | dp | `verified` |
| t_fc | numeric | hrs | 0..100 | time | real | Time to drain soil to field capacity | `matched` | t_fc | `verified` |
| lag | numeric | hrs | 0..100 | lag | real | Drain tile lag time | `matched` | lag | `verified` |
| rad | numeric | mm | 3..40 | radius | real | Effective radius of drains | `matched` | rad | `verified` |
| dist | numeric | mm | 7600..30000 | dist | real | Distance between two drain tubes or tiles | `matched` | dist | `verified` |
| drain | numeric | mm/day | 10..51 | drain_co | real | Drainage coefficient | `matched` | drain | `verified` |
| pump | numeric | mm/hr | 0..10 | pumpcap | real | Pump capacity | `matched` | pump | `verified` |
| lat_ksat | numeric | none | 0.01..4 | latksat | real | Multiplication factor to determine lateral ksat from SWAT ksat input value | `matched` | lat_ksat | `verified` |

## tillage.til

| Spreadsheet name | Type | Units | Range | Source name | Type | Description | Status | Editor DB name | Editor check |
|---|---|---|---|---|---|---|---|---|---|
| id | - | - | - | - | - | ID | `spreadsheet_only` (structural) | - | `mismatch` |
| name | string | - | - | tillnm | character | Tillage name | `matched` | name | `verified` |
| description | string | - | - | - | - | Description, not used in the model | `spreadsheet_only` (structural) | - | `mismatch` |
| mix_eff | numeric | fraction | 0..1 | effmix | real | Mixing efficiency of tillage operation | `matched` | mix_eff | `verified` |
| mix_dp | numeric | mm | 0..750 | deptil | real | Depth of mixing caused by tillage | `matched` | mix_dp | `verified` |
| rough | numeric | mm | 0..200 | ranrns | real | Random roughness | `matched` | rough | `verified` |
| ridge_ht | numeric | mm | >=0 | ridge_ht | real | Ridge height | `matched` | ridge_ht | `verified` |
| ridge_sp | numeric | mm | >=0 | ridge_sp | real | Ridge interval (or row spacing) | `matched` | ridge_sp | `verified` |

## time.sim

| Spreadsheet name | Type | Units | Range | Source name | Type | Description | Status | Editor DB name | Editor check |
|---|---|---|---|---|---|---|---|---|---|
| id | integer | none | - | - | - | ID | `spreadsheet_only` (structural) | - | `mismatch` |
| day_start | integer | none | - | day_start | integer | Beginning Julian day of simulation | `matched` | day_start | `verified` |
| yrc_start | integer | none | - | yrc_start | integer | Beginning year of simulation (for example, 1980) | `matched` | yrc_start | `verified` |
| day_end | integer | none | - | day_end | integer | Ending Julian day of simulation | `matched` | day_end | `verified` |
| yrc_end | integer | none | - | yrc_end | integer | Ending Year of simulation | `matched` | yrc_end | `verified` |
| step | integer | none | - | step | integer | Timestep of simulation | `matched` | step | `verified` |

## tmp.cli

| Spreadsheet name | Type | Units | Range | Source name | Type | Description | Status | Editor DB name | Editor check |
|---|---|---|---|---|---|---|---|---|---|
| tmp_file | string | - | - | - | - | Maximum/minium temperature file names | `spreadsheet_only` | - | `unavailable` |
| - | - | - | - | tmp_n | character | - | `source_only` | - | - |
| - | - | - | - | filename | character | - | `source_only` | - | - |

## topography.hyd

| Spreadsheet name | Type | Units | Range | Source name | Type | Description | Status | Editor DB name | Editor check |
|---|---|---|---|---|---|---|---|---|---|
| id | - | - | - | - | - | ID | `spreadsheet_only` (structural) | - | `mismatch` |
| name | string | - | - | name | character | topography parameter set name | `matched` | name | `verified` |
| slp | numeric | m/m | >=0 | slope | real | Average slope steepness in HRU | `matched` | slp | `verified` |
| slp_len | numeric | m | >=0 | slope_len | real | Average slope length in HRU | `matched` | slp_len | `verified` |
| lat_len | numeric | m | >=0 | lat_len | real | Slope length for lateral subsurface flow | `matched` | lat_len | `verified` |
| dist_cha | numeric | m | 0..100000 | dis_stream | real | Average distance to stream | `matched` | dist_cha | `verified` |
| depos | numeric | - | >=0 | dep_co | real | Deposition coefficient | `matched` | depos | `verified` |

## transplant.plt

| Spreadsheet name | Type | Units | Range | Source name | Type | Description | Status | Editor DB name | Editor check |
|---|---|---|---|---|---|---|---|---|---|
| - | - | - | - | name | character | - | `source_only` | - | - |
| - | - | m**2/m**2 | - | lai | real | leaf area index | `source_only` | - | - |
| - | - | kg/ha | - | bioms | real | land cover/crop biomass | `source_only` | - | - |
| - | - | frac | - | phuacc | real | frac of plant heat unit acc. | `source_only` | - | - |
| - | - | years | - | fr_yrmat | real | fraction of current year of growth to years to maturity | `source_only` | - | - |
| - | - | plants/m^2 | - | pop | real | plant population | `source_only` | - | - |

## tvheads.gw

| Spreadsheet name | Type | Units | Range | Source name | Type | Description | Status | Editor DB name | Editor check |
|---|---|---|---|---|---|---|---|---|---|
| - | - | - | - | cell_id | integer | - | `source_only` | - | - |
| - | - | - | - | gw_tvh_vals | real | - | `source_only` | - | - |

## urban.urb

| Spreadsheet name | Type | Units | Range | Source name | Type | Description | Status | Editor DB name | Editor check |
|---|---|---|---|---|---|---|---|---|---|
| id | - | - | - | - | - | ID | `spreadsheet_only` (structural) | - | `mismatch` |
| name | string | - | - | urbnm | character | Urban name | `matched` | name | `verified` |
| description | string | - | - | - | - | Description, not used in the model | `spreadsheet_only` (structural) | - | `mismatch` |
| frac_imp | numeric | fraction | 0..1 | fimp | real | Fraction of HRU area that is impermeable | `matched` | frac_imp | `verified` |
| frac_dc_imp | numeric | fraction | 0..1 | fcimp | real | Fraction of HRU that is classified as directly connected impermeable | `matched` | frac_dc_imp | `verified` |
| curb_den | numeric | km/ha | 0..1 | curbden | real | Curb length density | `matched` | curb_den | `verified` |
| urb_wash | numeric | 1/mm | 0..1 | urbcoef | real | Wash-off coefficient for removal of contituents from an impermeable surface | `matched` | urb_wash | `verified` |
| dirt_max | numeric | kg/curb km | 0..2000 | dirtmx | real | Maximum amount of solids allowed to build up on impermeable surfaces | `matched` | dirt_max | `verified` |
| t_halfmax | numeric | days | 0..100 | thalf | real | Time for the amount of solids on impermeable areas to build up to 1/2 of maximum level | `matched` | t_halfmax | `verified` |
| conc_totn | numeric | mg/kg | 0..1000 | tnconc | real | Concentration of total N in suspended solid load from impermeable areas | `matched` | conc_totn | `verified` |
| conc_totp | numeric | mg/kg | 0..1000 | tpconc | real | Concentration of total P in suspended solid load from impermeable areas | `matched` | conc_totp | `verified` |
| conc_no3n | numeric | mg/kg | 0..50 | tno3conc | real | Concentration of NO3-N in suspended solid load from impermeable areas | `matched` | conc_no3n | `verified` |
| urb_cn | numeric | none | 30..100 | urbcn2 | real | Moisture condition II curve number for impermeable areas | `matched` | urb_cn | `verified` |

## water_allocation.wro

| Spreadsheet name | Type | Units | Range | Source name | Type | Description | Status | Editor DB name | Editor check |
|---|---|---|---|---|---|---|---|---|---|
| name | string | - | - | name | character | sequential number of link | `matched` | name | `verified` |
| rule_typ | string | - | - | rule_typ | character | rule type to allocate water | `matched` | rule_typ | `verified` |
| src_obs | integer | - | - | - | - | number of source objects | `spreadsheet_only` | src_obs | `verified` |
| dmd_obs | integer | - | - | - | - | number of demand objects | `spreadsheet_only` | dmd_obs | `verified` |
| cha_db | string | - | - | - | - | y-yes there is a channel object;n-no channel object (only 1 per water allocation object) | `spreadsheet_only` | - | `mismatch` |
| src_num | integer | - | - | src_num | integer | demand object number | `matched` | src_num | `verified` |
| ob_typ | string | - | - | - | - | reservoir(res),aquifer(aqu),unlimited groundwater source(gwu) | `spreadsheet_only` | - | `mismatch` |
| ob_num | integer | - | - | - | - | number of the object type | `spreadsheet_only` | - | `mismatch` |
| Jan_min | numeric | - | - | - | - | Jan - min chan flow(m3/s), min res level(frac prinicpal), max aqu depth(m) | `spreadsheet_only` | - | `mismatch` |
| Feb_min | numeric | - | - | - | - | Feb - min chan flow(m3/s), min res level(frac prinicpal), max aqu depth(m) | `spreadsheet_only` | - | `mismatch` |
| Mar_min | numeric | - | - | - | - | Mar - min chan flow(m3/s), min res level(frac prinicpal), max aqu depth(m) | `spreadsheet_only` | - | `mismatch` |
| Apr_min | numeric | - | - | - | - | Apr - min chan flow(m3/s), min res level(frac prinicpal), max aqu depth(m) | `spreadsheet_only` | - | `mismatch` |
| May_min | numeric | - | - | - | - | May - min chan flow(m3/s), min res level(frac prinicpal), max aqu depth(m) | `spreadsheet_only` | - | `mismatch` |
| Jun_min | numeric | - | - | - | - | Jun - min chan flow(m3/s), min res level(frac prinicpal), max aqu depth(m) | `spreadsheet_only` | - | `mismatch` |
| Jul_min | numeric | - | - | - | - | Jul - min chan flow(m3/s), min res level(frac prinicpal), max aqu depth(m) | `spreadsheet_only` | - | `mismatch` |
| Aug_min | numeric | - | - | - | - | Aug - min chan flow(m3/s), min res level(frac prinicpal), max aqu depth(m) | `spreadsheet_only` | - | `mismatch` |
| Sep_min | numeric | - | - | - | - | Sep - min chan flow(m3/s), min res level(frac prinicpal), max aqu depth(m) | `spreadsheet_only` | - | `mismatch` |
| Oct_min | numeric | - | - | - | - | Oct - min chan flow(m3/s), min res level(frac prinicpal), max aqu depth(m) | `spreadsheet_only` | - | `mismatch` |
| Nov_min | numeric | - | - | - | - | Nov - min chan flow(m3/s), min res level(frac prinicpal), max aqu depth(m) | `spreadsheet_only` | - | `mismatch` |
| Dec_min | numeric | - | - | - | - | Dec - min chan flow(m3/s), min res level(frac prinicpal), max aqu depth(m) | `spreadsheet_only` | - | `mismatch` |
| description | string | - | - | - | - | Description, not used in the model | `spreadsheet_only` (structural) | - | `mismatch` |
| numb | integer | - | - | - | - | demand object number | `spreadsheet_only` | - | `mismatch` |
| ob_typ | string | - | - | - | - | hru (for irrigation) or muni (municipal) or divert (interbasin diversion) | `spreadsheet_only` | - | `mismatch` |
| ob_num | integer | - | - | - | - | number of the object type | `spreadsheet_only` | - | `mismatch` |
| withdr | string | - | - | - | - | withdrawal type - ave_day or recall for muni and divert - irrig for hru | `spreadsheet_only` | withdr | `verified` |
| amount | numeric | - | - | amount | real | m3 per day for muni and mm for hru | `matched` | amount | `verified` |
| w_rt | string | - | - | right | character | water right (sr -senior or jr - junior right) | `matched` | right | `verified` |
| tr_typ | string | - | - | - | - | - | `spreadsheet_only` | - | `mismatch` |
| treat | string | - | - | - | - | - | `spreadsheet_only` | - | `mismatch` |
| rcv_ob | string | - | - | - | - | - | `spreadsheet_only` | - | `mismatch` |
| rcv_num | integer | - | - | - | - | - | `spreadsheet_only` | rcv_num | `verified` |
| rcv_dtl | string | - | - | - | - | - | `spreadsheet_only` | rcv_dtl | `verified` |
| srcs | string | - | - | - | - | total number objects to follow | `spreadsheet_only` | - | `mismatch` |
| scrc1 | integer | - | - | - | - | sequential source number as listed in wallo object | `spreadsheet_only` | - | `mismatch` |
| frac1 | integer | - | - | - | - | fraction of demand supplied by the source | `spreadsheet_only` | - | `mismatch` |
| comp1 | string | - | - | - | - | compensate from source if other sources are limiting (y/n) | `spreadsheet_only` | - | `mismatch` |
| scrc2 | integer | - | - | - | - | sequential source number as listed in wallo object | `spreadsheet_only` | - | `mismatch` |
| frac2 | integer | - | - | - | - | fraction of demand supplied by the source | `spreadsheet_only` | - | `mismatch` |
| comp2 | string | - | - | - | - | compensate from source if other sources are limiting (y/n) | `spreadsheet_only` | - | `mismatch` |
| scrc3 | integer | - | - | - | - | sequential source number as listed in wallo object | `spreadsheet_only` | - | `mismatch` |
| frac3 | integer | - | - | - | - | fraction of demand supplied by the source | `spreadsheet_only` | - | `mismatch` |
| comp3 | string | - | - | - | - | compensate from source if other sources are limiting (y/n) | `spreadsheet_only` | - | `mismatch` |
| scrc4 | integer | - | - | - | - | sequential source number as listed in wallo object | `spreadsheet_only` | - | `mismatch` |
| frac4 | integer | - | - | - | - | fraction of demand supplied by the source | `spreadsheet_only` | - | `mismatch` |
| comp4 | string | - | - | - | - | compensate from source if other sources are limiting (y/n) | `spreadsheet_only` | - | `mismatch` |
| scrc5 | integer | - | - | - | - | sequential source number as listed in wallo object | `spreadsheet_only` | - | `mismatch` |
| frac5 | integer | - | - | - | - | fraction of demand supplied by the source | `spreadsheet_only` | - | `mismatch` |
| comp5 | string | - | - | - | - | compensate from source if other sources are limiting (y/n) | `spreadsheet_only` | - | `mismatch` |
| description | string | - | - | - | - | Description, not used in the model | `spreadsheet_only` (structural) | - | `mismatch` |
| - | - | - | - | k | integer | - | `source_only` | - | - |
| - | - | - | - | trn_typ | character | transfer type - decision table, recall, ave daily | `source_only` | - | - |
| - | - | - | - | trn_typ_name | character | transfer type name of table or recall | `source_only` | - | - |
| - | - | - | - | dtbl_src | character | decision table name to allocate sources | `source_only` | - | - |
| - | - | - | - | typ | character | source object type | `source_only` | - | - |
| - | - | - | - | num | integer | number of the source object | `source_only` | - | - |
| - | - | - | - | conv_typ | character | conveyance type - pipe or pump | `source_only` | - | - |
| - | - | - | - | conv_num | integer | number of the conveyance object | `source_only` | - | - |
| - | - | - | - | dtbl_lim | character | decision table name to set withdrawal limit of the source object | `source_only` | - | - |
| - | - | - | - | wdraw_lim | real | actual withdrawal limit of source object (res-frac principal, aqu-max depth (m); cha-min flow (m3/s)) | `source_only` | - | - |
| - | - | - | - | frac | real | fraction of transfer supplied by the source | `source_only` | - | - |
| - | - | - | - | comp | character | compensate if other source objects are past withdrawal threshold (y/n) | `source_only` | - | - |
| - | - | - | - | trn_obs | integer | number of transfer objects | `source_only` | - | - |

## water_balance.sft

| Spreadsheet name | Type | Units | Range | Source name | Type | Description | Status | Editor DB name | Editor check |
|---|---|---|---|---|---|---|---|---|---|
| id | integer | - | - | - | - | ID | `spreadsheet_only` (structural) | - | `mismatch` |
| mreg | string | - | - | - | - | Total number of regions updates in the file | `spreadsheet_only` | - | `mismatch` |
| reg_name | string | - | - | name | character | name of region | `matched` | name | `verified` |
| lum_numb | integer | - | - | - | - | number of land uses in each region | `spreadsheet_only` | - | `mismatch` |
| cal_name | string | - | - | name | character | landuse name | `matched` | name | `verified` |
| surq_rto | numeric | - or m^3 | - | srr | real | surface runoff ratio | `matched` | surq_rto | `verified` |
| latq_rto | numeric | - or m^3 | - | lfr | real | lateral flow ratio | `matched` | latq_rto | `verified` |
| perc_rto | numeric | - or m^3 | - | pcr | real | percolation ratio | `matched` | perc_rto | `verified` |
| et_rto | numeric | - or m^3 | - | etr | real | et ratio | `matched` | et_rto | `verified` |
| tileq_rto | numeric | - or m^3 | - | tfr | real | tile flow ratio | `matched` | tileq_rto | `verified` |
| pet | numeric | - or m^3 | - | pet | real | ave annual potential et | `matched` | pet | `verified` |
| sed | numeric | t/ha or kg | - | sed | real | sediment yield | `matched` | sed | `verified` |
| wyld_rto | numeric | - or m^3 | - | wyr | real | water yield ration-total water yield/precip | `matched` | wyr | `verified` |
| bf_rto | numeric | - or m^3 | - | bfr | real | base flow ratio-base flow/precip-lat+prec+tile | `matched` | bfr | `verified` |
| solp | numeric | kg/ha or kg | - | solp | real | soluble p yield | `matched` | solp | `verified` |
| - | - | - | - | nlum | integer | number of land use and mgt in the region | `source_only` | - | - |

## water_canal.wal

| Spreadsheet name | Type | Units | Range | Source name | Type | Description | Status | Editor DB name | Editor check |
|---|---|---|---|---|---|---|---|---|---|
| - | - | - | - | imax | integer | - | `source_only` | - | - |
| - | - | - | - | i | integer | - | `source_only` | - | - |
| - | - | - | - | name | character | name of the canal | `source_only` | - | - |
| - | - | - | - | w_sta | character | name of nearby weather station | `source_only` | - | - |
| - | - | - | - | init | character | name of the intitial concentrations in canal | `source_only` | - | - |
| - | - | - | - | dtbl | character | name of decision table to determine canal outflow | `source_only` | - | - |
| - | - | - | - | ddown_days | real | days !days to drawdown the storage to zero | `source_only` | - | - |
| - | - | - | - | w | real | m !top width of canal | `source_only` | - | - |
| - | - | - | - | d | real | m !depth of canal | `source_only` | - | - |
| - | - | - | - | s | real | m !slope of canal | `source_only` | - | - |
| - | - | - | - | ss | real | m/m !side slope of trapezoidal canal | `source_only` | - | - |
| - | - | - | - | sat_con | real | to compute percolation from canal to groundwater | `source_only` | - | - |
| - | - | - | - | loss_fr | real | water loss during treament | `source_only` | - | - |
| - | - | - | - | bed_thick | real | m !bed sediment thickness for Darcy seepage (gwflow; 0 if not used) | `source_only` | - | - |
| - | - | - | - | div_id | integer | recall diversion ID (gwflow; 0 if wallo-routed) | `source_only` | - | - |
| - | - | - | - | day_beg | integer | Julian day canal begins operation (gwflow external; 0 otherwise) | `source_only` | - | - |
| - | - | - | - | day_end | integer | Julian day canal ends operation (gwflow external; 0 otherwise) | `source_only` | - | - |
| - | - | - | - | num_aqu | integer | number of aquifers | `source_only` | - | - |

## water_pipe.wal

| Spreadsheet name | Type | Units | Range | Source name | Type | Description | Status | Editor DB name | Editor check |
|---|---|---|---|---|---|---|---|---|---|
| - | - | - | - | imax | integer | - | `source_only` | - | - |
| - | - | - | - | i | integer | - | `source_only` | - | - |
| - | - | - | - | name | character | name of the water tower or pipe | `source_only` | - | - |
| - | - | - | - | stor_mx | real | m3 !maximum storage in plant | `source_only` | - | - |
| - | - | - | - | ddown_days | real | days !days to drawdown the storage to zero | `source_only` | - | - |
| - | - | - | - | loss_fr | real | water loss during treament | `source_only` | - | - |
| - | - | - | - | num_aqu | integer | number of aquifers | `source_only` | - | - |

## water_tower.wal

| Spreadsheet name | Type | Units | Range | Source name | Type | Description | Status | Editor DB name | Editor check |
|---|---|---|---|---|---|---|---|---|---|
| - | - | - | - | i | integer | - | `source_only` | - | - |
| - | - | - | - | name | character | name of the water tower or pipe | `source_only` | - | - |
| - | - | - | - | stor_mx | real | m3 !maximum storage in plant | `source_only` | - | - |
| - | - | - | - | ddown_days | real | days !days to drawdown the storage to zero | `source_only` | - | - |
| - | - | - | - | loss_fr | real | water loss during treament | `source_only` | - | - |

## water_treat.wal

| Spreadsheet name | Type | Units | Range | Source name | Type | Description | Status | Editor DB name | Editor check |
|---|---|---|---|---|---|---|---|---|---|
| - | - | - | - | imax | integer | - | `source_only` | - | - |
| - | - | - | - | i | integer | - | `source_only` | - | - |
| - | - | - | - | name | character | name of the water treatment plant | `source_only` | - | - |
| - | - | - | - | stor_mx | real | character (len=25) :: init = "" !name of the intitial concentrations in wtp storage m3 !maximum storage in plant | `source_only` | - | - |
| - | - | - | - | lag_days | real | days !treatement time - lag outflow | `source_only` | - | - |
| - | - | - | - | loss_fr | real | water loss during treament | `source_only` | - | - |
| - | - | - | - | org_min | character | sediment, carbon, and nutrients | `source_only` | - | - |
| - | - | - | - | pests | character | pesticides - ppm | `source_only` | - | - |
| - | - | - | - | paths | character | pathogens - cfu | `source_only` | - | - |
| - | - | - | - | salts | character | salt ions - ppm | `source_only` | - | - |
| - | - | - | - | constit | character | other constituents - ppm | `source_only` | - | - |
| - | - | - | - | descrip | character | description | `source_only` | - | - |
| - | - | - | - | pest | real | pesticide (kg/ha) | `source_only` | - | - |
| - | - | - | - | path | real | pathogen (cfu) | `source_only` | - | - |

## water_use.wal

| Spreadsheet name | Type | Units | Range | Source name | Type | Description | Status | Editor DB name | Editor check |
|---|---|---|---|---|---|---|---|---|---|
| - | - | - | - | imax | integer | - | `source_only` | - | - |
| - | - | - | - | i | integer | - | `source_only` | - | - |
| - | - | - | - | name | character | name of the water treatment plant | `source_only` | - | - |
| - | - | - | - | stor_mx | real | character (len=25) :: init = "" !name of the intitial concentrations in wtp storage m3 !maximum storage in plant | `source_only` | - | - |
| - | - | - | - | lag_days | real | days !treatement time - lag outflow | `source_only` | - | - |
| - | - | - | - | loss_fr | real | water loss during treament | `source_only` | - | - |
| - | - | - | - | org_min | character | sediment, carbon, and nutrients | `source_only` | - | - |
| - | - | - | - | pests | character | pesticides - ppm | `source_only` | - | - |
| - | - | - | - | paths | character | pathogens - cfu | `source_only` | - | - |
| - | - | - | - | salts | character | salt ions - ppm | `source_only` | - | - |
| - | - | - | - | constit | character | other constituents - ppm | `source_only` | - | - |
| - | - | - | - | descrip | character | description | `source_only` | - | - |
| - | - | - | - | pest | real | pesticide (kg/ha) | `source_only` | - | - |
| - | - | - | - | path | real | pathogen (cfu) | `source_only` | - | - |

## wb_parms.sft

| Spreadsheet name | Type | Units | Range | Source name | Type | Description | Status | Editor DB name | Editor check |
|---|---|---|---|---|---|---|---|---|---|
| id | integer | - | - | - | - | ID | `spreadsheet_only` (structural) | - | `mismatch` |
| mslp | string | - | - | - | - | Total number of parameter updates in the file | `spreadsheet_only` | - | `mismatch` |
| name | string | - | - | name | character | cn2, terrace, landuse,mgt, etc | `matched` | name | `verified` |
| chg_typ | string | - | - | chg_typ | character | type of change (absval,abschg,pctchg) | `matched` | chg_typ | `verified` |
| neg | numeric | - | - | neg | real | negative limit of change | `matched` | neg | `verified` |
| pos | numeric | - | - | pos | real | positive limit of change | `matched` | pos | `verified` |
| lo | numeric | - | - | lo | real | lower limit of parameter | `matched` | lo | `verified` |
| up | numeric | - | - | up | real | upper limit of paramete | `matched` | up | `verified` |

## weather-sta.cli

| Spreadsheet name | Type | Units | Range | Source name | Type | Description | Status | Editor DB name | Editor check |
|---|---|---|---|---|---|---|---|---|---|
| name | string | - | - | name | character | Weather station name | `matched` | name | `verified` |
| wgn | string | - | - | wgn | character | Pointer to weather generator parameter set | `matched` | wgn | `verified` |
| pcp | string | - | - | pgage | character | Precipitation 'sim' or gage name | `matched` | pcp | `verified` |
| tmp | string | - | - | tgage | character | Temperature 'sim' or gage name | `matched` | tmp | `verified` |
| slr | string | - | - | sgage | character | Solar rdiation 'sim' or gage name | `matched` | slr | `verified` |
| hmd | string | - | - | hgage | character | Relative humidity 'sim' or gage name | `matched` | hmd | `verified` |
| wnd | string | - | - | wgage | character | Wind speed 'sim' or gage name | `matched` | wnd | `verified` |
| pet | string | - | - | petgage | character | Potential evapotranspriation name | `matched` | pet | `verified` |
| atmo_dep | string | - | - | atmodep | character | Atmospheric deposition data file name | `matched` | atmo_dep | `verified` |

## weather-wgn.cli

| Spreadsheet name | Type | Units | Range | Source name | Type | Description | Status | Editor DB name | Editor check |
|---|---|---|---|---|---|---|---|---|---|
| id | string | - | - | - | - | ID | `spreadsheet_only` | - | `mismatch` |
| name | string | - | - | wgn_n | character | Weather generator name | `matched` | name | `verified` |
| lat | numeric | degree | -90..90 | lat | real | Latitude of weather station used to create statistical parameters | `matched` | lat | `verified` |
| lon | numeric | degree | -180..180 | long | real | Longitude of weather station used to create statistical parameters | `matched` | lon | `verified` |
| elev | numeric | m | 0..5000 | elev | real | Elevation of weather station used to create statistical parameters | `matched` | elev | `verified` |
| yrs | numeric | none | 5..100 | rain_yrs | real | Number of years of recorded maximum monthly 0.5 h rainfall data | `matched` | rain_yrs | `verified` |
| wgn_name | string | - | - | - | - | Weather generator name | `spreadsheet_only` (structural) | - | `mismatch` |
| month | integer | none | 0..12 | - | - | Month | `spreadsheet_only` (structural) | - | `mismatch` |
| tmp_max_ave | numeric | deg C | -30..50 | tmpmx | real | Average or mean daily maximum air temperature for month | `matched` | tmp_max_ave | `verified` |
| tmp_min_ave | numeric | deg C | -40..40 | tmpmn | real | Average or mean daily minimum air temperature for month | `matched` | tmp_min_ave | `verified` |
| tmp_max_sd | numeric | deg C | 0.1..100 | tmpstdmx | real | Standard deviation for daily maximum air temperature in month | `matched` | tmp_max_sd | `verified` |
| tmp_min_sd | numeric | deg C | 0.1..30 | tmpstdmn | real | Standard deviation for daily minimum air temperature in month | `matched` | tmp_min_sd | `verified` |
| pcp_ave | numeric | mm | 0..600 | pcpmm | real | Average or mean total monthly precipitation | `matched` | pcp_ave | `verified` |
| pcp_sd | numeric | mm/day | 0.1..50 | pcpstd | real | Standard deviation for the average daily precipitation | `matched` | pcp_sd | `verified` |
| pcp_skew | numeric | mm | -50..20 | pcpskw | real | Skew coefficient for the average daily precipitaiton | `matched` | pcp_skew | `verified` |
| wet_dry | numeric | none | 0..0.95 | pr_wd | real | Probability of a wet day after a dry day | `matched` | wet_dry | `verified` |
| wet_wet | numeric | none | 0..0.95 | pr_ww | real | Probability of a wet day after a wet day | `matched` | wet_wet | `verified` |
| pcp_days | numeric | day | 0..31 | pcpd | real | Average number of days of precipitation in a month | `matched` | pcp_days | `verified` |
| pcp_hhr | numeric | mm | 0..125 | rainhmx | real | Maximum 0.5 hour rainfall in entire period of record for month | `matched` | pcp_hhr | `verified` |
| slr_ave | numeric | MJ/m^2/day | 0..750 | solarav | real | Average daily solar radiation for the month | `matched` | slr_ave | `verified` |
| dew_ave | numeric | deg C | -50..25 | dewpt | real | Average daily dew point temperature for each month | `matched` | dew_ave | `verified` |
| wnd_ave | numeric | m/s | 0..100 | windav | real | Average wind speed for the month | `matched` | wnd_ave | `verified` |

## weir.res

| Spreadsheet name | Type | Units | Range | Source name | Type | Description | Status | Editor DB name | Editor check |
|---|---|---|---|---|---|---|---|---|---|
| id | - | - | - | - | - | ID | `spreadsheet_only` (structural) | - | `mismatch` |
| name | string | - | - | name | character | Reservoir weir name | `matched` | name | `verified` |
| numb_steps | integer | none | 1..24 | - | - | Number of time steps in day for weir routing | `spreadsheet_only` | - | `mismatch` |
| disch_co | numeric | none | - | c | real | Weir discharge coefficient | `matched` | - | `mismatch` |
| energy_co | numeric | m^0.5/day | 147000..153000 | k | real | Energy coefficient (broad crested=147,000;sharp crested=153,000) | `matched` | - | `mismatch` |
| weir_wd | numeric | m | - | w | real | Width of weir | `matched` | - | `mismatch` |
| vel_co | numeric | none | - | - | - | Velocity exponent coefficient for bedding material | `spreadsheet_only` | - | `mismatch` |
| dp_co | numeric | none | - | - | - | Depth exponent coefficient for bedding material | `spreadsheet_only` | - | `mismatch` |
| - | - | m | - | h | real | height of weir above bottoom of impoundment | `source_only` | - | - |

## wetland.wet

| Spreadsheet name | Type | Units | Range | Source name | Type | Description | Status | Editor DB name | Editor check |
|---|---|---|---|---|---|---|---|---|---|
| id | - | - | - | k | integer | ID | `matched` | id | `verified` |
| numb_steps | integer | - | - | - | - | numb of wetland.wet | `spreadsheet_only` | - | `mismatch` |
| name | string | - | - | name | character | Reservoir wetland name | `matched` | name | `verified` |
| description | string | - | - | - | - | Description, not used in the model | `spreadsheet_only` (structural) | - | `mismatch` |
| init | string | none | - | init | character | Pointer to reservoir wetland initial parameter set | `matched` | init | `verified` |
| hyd | string | none | - | hyd | character | Pointer to reservoir wetland hydrology parameter set | `matched` | hyd | `verified` |
| rel | string | none | - | release | character | 0=simulated; 1=measured outflow | `matched` | rel | `verified` |
| sed | string | none | - | sed | character | Pointer to reservoir wetland sediment parameter set | `matched` | sed | `verified` |
| nut | string | none | - | nut | character | Pointer to reservoir wetland nutrient parameter set | `matched` | nut | `verified` |
| lu_mgt | string | none | - | - | - | Pointer to landuse parameter file | `spreadsheet_only` | - | `mismatch` |

## wetland.wet_cs

| Spreadsheet name | Type | Units | Range | Source name | Type | Description | Status | Editor DB name | Editor check |
|---|---|---|---|---|---|---|---|---|---|
| - | - | - | - | k | integer | - | `source_only` | - | - |
| - | - | - | - | pst | character | pesticide inputs-points to pesticide.res | `source_only` | - | - |
| - | - | - | - | weir | character | weir inputs-points to weir.res Jaehak 2022 | `source_only` | - | - |
| - | - | - | - | salt | character | salt inputs - points to salt_res rtb salt | `source_only` | - | - |
| - | - | - | - | cs | character | constituent inputs - points to cs_res rtb cs | `source_only` | - | - |

## wnd.cli

| Spreadsheet name | Type | Units | Range | Source name | Type | Description | Status | Editor DB name | Editor check |
|---|---|---|---|---|---|---|---|---|---|
| wnd_file | string | - | - | - | - | Wind data file names | `spreadsheet_only` | - | `unavailable` |
| - | - | - | - | wnd_n | character | - | `source_only` | - | - |
| - | - | - | - | filename | character | - | `source_only` | - | - |

## zones.gw

| Spreadsheet name | Type | Units | Range | Source name | Type | Description | Status | Editor DB name | Editor check |
|---|---|---|---|---|---|---|---|---|---|
| - | - | - | - | zones_aquK | real | - | `source_only` | - | - |
| - | - | - | - | zones_aquSy | real | - | `source_only` | - | - |
| - | - | - | - | zones_strK | real | - | `source_only` | - | - |
| - | - | - | - | zones_strbed | real | - | `source_only` | - | - |
| - | - | - | - | zones_Kt | real | - | `source_only` | - | - |

