# SWAT+ Output Contract Changes

Source-level output change report: which files SWAT+ opens for writing, and the fields each write statement emits. Filenames are resolved from the same defaults used for inputs; a resolved default can still be overridden by runtime configuration. Outputs carry no schema certification, so entries here are not schema-reviewed.

## Summary

- Added output files: **15**
- Removed output files: **1**
- Changed write contracts: **11**
- Possible renames or replacements: **1**
- Candidate open/write blocks with unresolved filenames: **60**
- Newly unresolved units in the candidate: **0**

## Coverage

SWAT+ opens most output units in a header or initialisation routine and writes to them from other files. Unit-to-filename binding is per-file, so a unit opened elsewhere cannot be named here and is counted as unresolved rather than reported under a `unit_NNN` pseudo-filename. This report therefore covers the writes below and not the rest; widening it needs project-wide unit binding in the parser.

- Output files resolved to a filename: **687**
- Write statements covered: **4377**
- Units whose filename is unresolved: **60**
- Write statements not covered: **234**

## Added outputs

### `bsn_sedbud.txt`

- Source expression(s): _none captured_

- Procedure: `header_sd_channel`
- Writer: `header_sd_channel.f90`
- Match: source_output
- Resolved default filename(s): `bsn_sedbud.txt`

| Line | Role | Condition | Fields written |
| --- | --- | --- | --- |
| 302 | data | `if (sp_ob%chandeg > 0) then` | `bsn%name`, `prog` |
| 303 | data | `if (sp_ob%chandeg > 0) then` | `ch_sed_bud_hdr` |
| 304 | data | `if (sp_ob%chandeg > 0) then` | `ch_sed_bud_hdr_units` |


- Procedure: `time_control`
- Writer: `time_control.f90`
- Match: source_output
- Resolved default filename(s): `bsn_sedbud.txt`

| Line | Role | Condition | Fields written |
| --- | --- | --- | --- |
| 476 | data | `None` | `bsn_sedbud` |

### `chanbud.txt`

- Source expression(s): _none captured_

- Procedure: `header_sd_channel`
- Writer: `header_sd_channel.f90`
- Match: source_output
- Resolved default filename(s): `chanbud.txt`

| Line | Role | Condition | Fields written |
| --- | --- | --- | --- |
| 282 | data | `if (sp_ob%chandeg > 0) then` | `bsn%name`, `prog` |
| 283 | data | `if (sp_ob%chandeg > 0) then` | `ch_bud_hdr` |
| 284 | data | `if (sp_ob%chandeg > 0) then` | `ch_bud_hdr_units` |


- Procedure: `time_control`
- Writer: `time_control.f90`
- Match: source_output
- Resolved default filename(s): `chanbud.txt`

| Line | Role | Condition | Fields written |
| --- | --- | --- | --- |
| 426 | data | `do ich = 1, sp_ob%chandeg` | `ich`, `ob(iob)%name`, `ob(iob)%area_ha`, `sd_ch(ich)%chl`, `sd_ch(ich)%chw`, `sd_ch(ich)%chd`, `ch_morph(ich)` |

### `chanbud_order.txt`

- Source expression(s): _none captured_

- Procedure: `header_sd_channel`
- Writer: `header_sd_channel.f90`
- Match: source_output
- Resolved default filename(s): `chanbud_order.txt`

| Line | Role | Condition | Fields written |
| --- | --- | --- | --- |
| 292 | data | `if (sp_ob%chandeg > 0) then` | `bsn%name`, `prog` |
| 293 | data | `if (sp_ob%chandeg > 0) then` | `ch_bud_order_hdr` |
| 294 | data | `if (sp_ob%chandeg > 0) then` | `ch_bud_order_hdr_units` |


- Procedure: `time_control`
- Writer: `time_control.f90`
- Match: source_output
- Resolved default filename(s): `chanbud_order.txt`

| Line | Role | Condition | Fields written |
| --- | --- | --- | --- |
| 454 | data | `if (sp_ob%chandeg > 0) then > do iord = 1, 12` | `iord`, `ch_morph_ord(iord)` |

### `recall(irec)%filename`

- Source expression(s): `"SWIFT/" // trim(adjustl(recall(irec)%filename))`

- Procedure: `swift_output`
- Writer: `swift_output.f90`
- Match: source_output
- Resolved default filename(s): `recall(irec)%filename`
- Source filename expression(s): `"SWIFT/" // trim(adjustl(recall(irec)%filename))`

| Line | Role | Condition | Fields written |
| --- | --- | --- | --- |
| 268 | data | `do irec = 1, db_mx%recalldb_max` | `" AVE ANNUAL RECALL FILE  "`, `recall(irec)%filename` |
| 269 | data | `do irec = 1, db_mx%recalldb_max` | `"     1    1    1     1    type    "`, `recall(irec)%filename`, `rec_a(irec)%flo`, `rec_a(irec)%sed`, `rec_a(irec)%orgn`, `rec_a(irec)%sedp`, `rec_a(irec)%no3`, `rec_a(irec)%solp`, `rec_a(irec)%nh3`, `rec_a(irec)%no2` |

### `wallo_treat_aa.csv`

- Source expression(s): _none captured_

- Procedure: `header_water_allocation`
- Writer: `header_water_allocation.f90`
- Match: source_output
- Resolved default filename(s): `wallo_treat_aa.csv`

| Line | Role | Condition | Fields written |
| --- | --- | --- | --- |
| 186 | data | `if (pco%water_allo%a == "y") then > if (pco%csvout == "y") then` | `bsn%name`, `prog` |
| 187 | data | `if (pco%water_allo%a == "y") then > if (pco%csvout == "y") then` | `wallo_use_hdr` |
| 188 | data | `if (pco%water_allo%a == "y") then > if (pco%csvout == "y") then` | `wallo_use_hdr_units` |


- Procedure: `wallo_treat_output`
- Writer: `wallo_treat_output.f90`
- Match: source_output
- Resolved default filename(s): `wallo_treat_aa.csv`

| Line | Role | Condition | Fields written |
| --- | --- | --- | --- |
| 73 | data | `do itrt = 1, wtps > if (time%end_sim == 1) then > if (pco%water_allo%a == "y") then > if (pco%csvout == "y") then` | `time%mo`, `time%day_mo`, `time%yrc`, `itrt`, `om_treat_name(itrt)`, `wal_tr_oma(itrt)` |

### `wallo_treat_aa.txt`

- Source expression(s): _none captured_

- Procedure: `header_water_allocation`
- Writer: `header_water_allocation.f90`
- Match: source_output
- Resolved default filename(s): `wallo_treat_aa.txt`

| Line | Role | Condition | Fields written |
| --- | --- | --- | --- |
| 180 | data | `if (pco%water_allo%a == "y") then` | `bsn%name`, `prog` |
| 181 | data | `if (pco%water_allo%a == "y") then` | `wallo_use_hdr` |
| 182 | data | `if (pco%water_allo%a == "y") then` | `wallo_use_hdr_units` |


- Procedure: `wallo_treat_output`
- Writer: `wallo_treat_output.f90`
- Match: source_output
- Resolved default filename(s): `wallo_treat_aa.txt`

| Line | Role | Condition | Fields written |
| --- | --- | --- | --- |
| 70 | data | `do itrt = 1, wtps > if (time%end_sim == 1) then > if (pco%water_allo%a == "y") then` | `time%mo`, `time%day_mo`, `time%yrc`, `itrt`, `om_treat_name(itrt)`, `wal_tr_oma(itrt)` |

### `wallo_treat_day.csv`

- Source expression(s): _none captured_

- Procedure: `header_water_allocation`
- Writer: `header_water_allocation.f90`
- Match: source_output
- Resolved default filename(s): `wallo_treat_day.csv`

| Line | Role | Condition | Fields written |
| --- | --- | --- | --- |
| 141 | data | `if (pco%water_allo%d == "y") then > if (pco%csvout == "y") then` | `bsn%name`, `prog` |
| 142 | data | `if (pco%water_allo%d == "y") then > if (pco%csvout == "y") then` | `wallo_use_hdr` |
| 143 | data | `if (pco%water_allo%d == "y") then > if (pco%csvout == "y") then` | `wallo_use_hdr_units` |


- Procedure: `wallo_treat_output`
- Writer: `wallo_treat_output.f90`
- Match: source_output
- Resolved default filename(s): `wallo_treat_day.csv`

| Line | Role | Condition | Fields written |
| --- | --- | --- | --- |
| 22 | data | `do itrt = 1, wtps > if (pco%water_allo%d == "y") then > if (pco%csvout == "y") then` | `time%mo`, `time%day_mo`, `time%yrc`, `itrt`, `om_treat_name(itrt)`, `wal_tr_omd(itrt)` |

### `wallo_treat_day.txt`

- Source expression(s): _none captured_

- Procedure: `header_water_allocation`
- Writer: `header_water_allocation.f90`
- Match: source_output
- Resolved default filename(s): `wallo_treat_day.txt`

| Line | Role | Condition | Fields written |
| --- | --- | --- | --- |
| 135 | data | `if (pco%water_allo%d == "y") then` | `bsn%name`, `prog` |
| 136 | data | `if (pco%water_allo%d == "y") then` | `wallo_use_hdr` |
| 137 | data | `if (pco%water_allo%d == "y") then` | `wallo_use_hdr_units` |


- Procedure: `wallo_treat_output`
- Writer: `wallo_treat_output.f90`
- Match: source_output
- Resolved default filename(s): `wallo_treat_day.txt`

| Line | Role | Condition | Fields written |
| --- | --- | --- | --- |
| 19 | data | `do itrt = 1, wtps > if (pco%water_allo%d == "y") then` | `time%day`, `time%mo`, `time%day_mo`, `time%yrc`, `itrt`, `om_treat_name(itrt)`, `wal_tr_omd(itrt)` |

### `wallo_treat_mon.csv`

- Source expression(s): _none captured_

- Procedure: `header_water_allocation`
- Writer: `header_water_allocation.f90`
- Match: source_output
- Resolved default filename(s): `wallo_treat_mon.csv`

| Line | Role | Condition | Fields written |
| --- | --- | --- | --- |
| 156 | data | `if (pco%water_allo%m == "y") then > if (pco%csvout == "y") then` | `bsn%name`, `prog` |
| 157 | data | `if (pco%water_allo%m == "y") then > if (pco%csvout == "y") then` | `wallo_use_hdr` |
| 158 | data | `if (pco%water_allo%m == "y") then > if (pco%csvout == "y") then` | `wallo_use_hdr_units` |


- Procedure: `wallo_treat_output`
- Writer: `wallo_treat_output.f90`
- Match: source_output
- Resolved default filename(s): `wallo_treat_mon.csv`

| Line | Role | Condition | Fields written |
| --- | --- | --- | --- |
| 38 | data | `do itrt = 1, wtps > if (time%end_mo == 1) then > if (pco%water_allo%m == "y") then > if (pco%csvout == "y") then` | `time%mo`, `time%day_mo`, `time%yrc`, `itrt`, `om_treat_name(itrt)`, `wal_tr_omm(itrt)` |

### `wallo_treat_mon.txt`

- Source expression(s): _none captured_

- Procedure: `header_water_allocation`
- Writer: `header_water_allocation.f90`
- Match: source_output
- Resolved default filename(s): `wallo_treat_mon.txt`

| Line | Role | Condition | Fields written |
| --- | --- | --- | --- |
| 150 | data | `if (pco%water_allo%m == "y") then` | `bsn%name`, `prog` |
| 151 | data | `if (pco%water_allo%m == "y") then` | `wallo_use_hdr` |
| 152 | data | `if (pco%water_allo%m == "y") then` | `wallo_use_hdr_units` |


- Procedure: `wallo_treat_output`
- Writer: `wallo_treat_output.f90`
- Match: source_output
- Resolved default filename(s): `wallo_treat_mon.txt`

| Line | Role | Condition | Fields written |
| --- | --- | --- | --- |
| 35 | data | `do itrt = 1, wtps > if (time%end_mo == 1) then > if (pco%water_allo%m == "y") then` | `time%mo`, `time%day_mo`, `time%yrc`, `itrt`, `om_treat_name(itrt)`, `wal_tr_omm(itrt)` |

### `wallo_treat_yr.txt`

- Source expression(s): _none captured_

- Procedure: `header_water_allocation`
- Writer: `header_water_allocation.f90`
- Match: source_output
- Resolved default filename(s): `wallo_treat_yr.txt`

| Line | Role | Condition | Fields written |
| --- | --- | --- | --- |
| 165 | data | `if (pco%water_allo%y == "y") then` | `bsn%name`, `prog` |
| 166 | data | `if (pco%water_allo%y == "y") then` | `wallo_use_hdr` |
| 167 | data | `if (pco%water_allo%y == "y") then` | `wallo_use_hdr_units` |


- Procedure: `wallo_treat_output`
- Writer: `wallo_treat_output.f90`
- Match: source_output
- Resolved default filename(s): `wallo_treat_yr.txt`

| Line | Role | Condition | Fields written |
| --- | --- | --- | --- |
| 52 | data | `do itrt = 1, wtps > if (time%end_yr == 1) then > if (pco%water_allo%y == "y") then` | `time%mo`, `time%day_mo`, `time%yrc`, `itrt`, `om_treat_name(itrt)`, `wal_tr_omy(itrt)` |

### `wallo_use_aa.txt`

- Source expression(s): _none captured_

- Procedure: `header_water_allocation`
- Writer: `header_water_allocation.f90`
- Match: source_output
- Resolved default filename(s): `wallo_use_aa.txt`

| Line | Role | Condition | Fields written |
| --- | --- | --- | --- |
| 119 | data | `if (pco%water_allo%a == "y") then` | `bsn%name`, `prog` |
| 120 | data | `if (pco%water_allo%a == "y") then` | `wallo_use_hdr` |
| 121 | data | `if (pco%water_allo%a == "y") then` | `wallo_use_hdr_units` |


- Procedure: `wallo_use_output`
- Writer: `wallo_use_output.f90`
- Match: source_output
- Resolved default filename(s): `wallo_use_aa.txt`

| Line | Role | Condition | Fields written |
| --- | --- | --- | --- |
| 71 | data | `do iuse = 1, wuses > if (time%end_sim == 1) then > if (pco%water_allo%a == "y") then` | `time%mo`, `time%day_mo`, `time%yrc`, `om_use_name(iuse)`, `iuse`, `wal_use_oma(iuse)` |

### `wallo_use_day.txt`

- Source expression(s): _none captured_

- Procedure: `header_water_allocation`
- Writer: `header_water_allocation.f90`
- Match: source_output
- Resolved default filename(s): `wallo_use_day.txt`

| Line | Role | Condition | Fields written |
| --- | --- | --- | --- |
| 74 | data | `if (pco%water_allo%d == "y") then` | `bsn%name`, `prog` |
| 75 | data | `if (pco%water_allo%d == "y") then` | `wallo_use_hdr` |
| 76 | data | `if (pco%water_allo%d == "y") then` | `wallo_use_hdr_units` |


- Procedure: `wallo_use_output`
- Writer: `wallo_use_output.f90`
- Match: source_output
- Resolved default filename(s): `wallo_use_day.txt`

| Line | Role | Condition | Fields written |
| --- | --- | --- | --- |
| 19 | data | `do iuse = 1, wuses > if (pco%water_allo%d == "y") then` | `time%day`, `time%mo`, `time%day_mo`, `time%yrc`, `om_use_name(iuse)`, `iuse`, `wal_use_omd(iuse)` |

### `wallo_use_mon.txt`

- Source expression(s): _none captured_

- Procedure: `header_water_allocation`
- Writer: `header_water_allocation.f90`
- Match: source_output
- Resolved default filename(s): `wallo_use_mon.txt`

| Line | Role | Condition | Fields written |
| --- | --- | --- | --- |
| 89 | data | `if (pco%water_allo%m == "y") then` | `bsn%name`, `prog` |
| 90 | data | `if (pco%water_allo%m == "y") then` | `wallo_use_hdr` |
| 91 | data | `if (pco%water_allo%m == "y") then` | `wallo_use_hdr_units` |


- Procedure: `wallo_use_output`
- Writer: `wallo_use_output.f90`
- Match: source_output
- Resolved default filename(s): `wallo_use_mon.txt`

| Line | Role | Condition | Fields written |
| --- | --- | --- | --- |
| 35 | data | `do iuse = 1, wuses > if (time%end_mo == 1) then > if (pco%water_allo%m == "y") then` | `time%mo`, `time%day_mo`, `time%yrc`, `om_use_name(iuse)`, `iuse`, `wal_use_omm(iuse)` |

### `wallo_use_yr.txt`

- Source expression(s): _none captured_

- Procedure: `header_water_allocation`
- Writer: `header_water_allocation.f90`
- Match: source_output
- Resolved default filename(s): `wallo_use_yr.txt`

| Line | Role | Condition | Fields written |
| --- | --- | --- | --- |
| 104 | data | `if (pco%water_allo%y == "y") then` | `bsn%name`, `prog` |
| 105 | data | `if (pco%water_allo%y == "y") then` | `wallo_use_hdr` |
| 106 | data | `if (pco%water_allo%y == "y") then` | `wallo_use_hdr_units` |


- Procedure: `wallo_use_output`
- Writer: `wallo_use_output.f90`
- Match: source_output
- Resolved default filename(s): `wallo_use_yr.txt`

| Line | Role | Condition | Fields written |
| --- | --- | --- | --- |
| 53 | data | `do iuse = 1, wuses > if (time%end_yr == 1) then > if (pco%water_allo%y == "y") then` | `time%mo`, `time%day_mo`, `time%yrc`, `om_use_name(iuse)`, `iuse`, `wal_use_omy(iuse)` |


## Removed outputs

### `recall_db(irec)%name`

- Source expression(s): `"SWIFT/" // trim(adjustl(recall_db(irec)%name))`

- Procedure: `swift_output`
- Writer: `swift_output.f90`
- Match: source_output
- Resolved default filename(s): `recall_db(irec)%name`
- Source filename expression(s): `"SWIFT/" // trim(adjustl(recall_db(irec)%name))`

| Line | Role | Condition | Fields written |
| --- | --- | --- | --- |
| 268 | data | `do irec = 1, db_mx%recalldb_max` | `" AVE ANNUAL RECALL FILE  "`, `recall_db(irec)%name` |
| 269 | data | `do irec = 1, db_mx%recalldb_max` | `"     1    1    1     1    type    "`, `recall_db(irec)%name`, `rec_a(irec)%flo`, `rec_a(irec)%sed`, `rec_a(irec)%orgn`, `rec_a(irec)%sedp`, `rec_a(irec)%no3`, `rec_a(irec)%solp`, `rec_a(irec)%nh3`, `rec_a(irec)%no2` |


## Changed output write contracts

### `SWIFT/recall.swf`

- Review needed: yes
- Writer procedures changed: no
- Write-block count changed: no
- Write conditions changed: no
- Write roles changed: no
- Base flattened write order: `"         ID            NAME              REC_TYP         FILENAME"`, `irec`, `recall_db(irec)%org_min%name`, `recall_db(irec)%org_min%units`, `recall_db(irec)%org_min%tstep`
- Candidate flattened write order: `"         ID            NAME              REC_TYP         FILENAME"`, `irec`, `recall(irec)%filename`, `recall(irec)%typ`

#### Write-order edits

- `replace` at base index 2 / candidate index 2: removed `recall_db(irec)%org_min%name`, `recall_db(irec)%org_min%units`, `recall_db(irec)%org_min%tstep`; added `recall(irec)%filename`, `recall(irec)%typ`

#### Base write structure

- Source expression(s): `"SWIFT/recall.swf"`

- Procedure: `swift_output`
- Writer: `swift_output.f90`
- Match: source_output
- Resolved default filename(s): `SWIFT/recall.swf`
- Source filename expression(s): `"SWIFT/recall.swf"`

| Line | Role | Condition | Fields written |
| --- | --- | --- | --- |
| 262 | data | `None` | `"         ID            NAME              REC_TYP         FILENAME"` |
| 264 | data | `do irec = 1, db_mx%recalldb_max` | `irec`, `recall_db(irec)%org_min%name`, `recall_db(irec)%org_min%units`, `recall_db(irec)%org_min%tstep` |


#### Candidate write structure

- Source expression(s): `"SWIFT/recall.swf"`

- Procedure: `swift_output`
- Writer: `swift_output.f90`
- Match: source_output
- Resolved default filename(s): `SWIFT/recall.swf`
- Source filename expression(s): `"SWIFT/recall.swf"`

| Line | Role | Condition | Fields written |
| --- | --- | --- | --- |
| 262 | data | `None` | `"         ID            NAME              REC_TYP         FILENAME"` |
| 264 | data | `do irec = 1, db_mx%recalldb_max` | `irec`, `recall(irec)%filename`, `recall(irec)%typ` |

### `files_out.out`

- Review needed: yes
- Writer procedures changed: no
- Write-block count changed: no
- Write conditions changed: yes
- Write roles changed: yes
- Base flattened write order: `"HRU                       hru_cbn_lyr.txt"`, `"HRU                       hru_cbn_lyr.csv"`, `"HRU                       hru_seq_lyr.txt"`, `"HRU                       hru_seq_lyr.csv"`, `"HRU                       hru_n_p_pool_stat.txt"`, `"HRU                       hru_n_p_pool_stat.csv"`, `"HRU                       hru_begsim_soil_prop.txt"`, `"HRU                       hru_begsim_soil_prop.csv"`, `"HRU                       hru_endsim_soil_prop.txt"`, `"HRU                       hru_endsim_soil_prop.csv"`, `"HRU                       hru_plc_stat.txt"`, `"HRU                       hru_plc_stat.csv"`, `"HRU                       hru_cflux_stat.txt"`, `"HRU                       hru_cflux_stat.csv"`, `"HRU                       hru_cpool_stat.txt"`, `"HRU                       hru_cpool_stat.csv"`, `"HRU                       hru_carbvars.txt"`, `"HRU                       hru_carbvars.csv"`, `"HRU                       hru_org_allo_vars.txt"`, `"HRU                       hru_org_allo_vars.csv"`, `"HRU                       hru_org_ratio_vars.txt"`, `"HRU                       hru_org_ratio_vars.csv"`, `"HRU                       hru_org_trans_vars.txt"`, `"HRU                       hru_org_trans_vars.csv"`, `"BASIN                     basin_carbon_all.txt"`, `"AQUIFER                   aquifer_day.txt"`, `"AQUIFER                   aquifer_day.csv"`, `"AQUIFER                   aquifer_mon.txt"`, `"AQUIFER                   aquifer_mon.csv"`, `"AQUIFER                   aquifer_yr.txt"`, `"AQUIFER                   aquifer_yr.csv"`, `"AQUIFER                   aquifer_aa.txt"`, `"AQUIFER                   aquifer_aa.csv"`, `"CHANNEL                   channel_day.txt"`, `"CHANNEL                   channel_day.csv"`, `"CHANNEL                   channel_mon.txt"`, `"CHANNEL                   channel_mon.csv"`, `"CHANNEL                   channel_yr.txt"`, `"CHANNEL                   channel_yr.csv"`, `"CHANNEL                   channel_aa.txt"`, `"CHANNEL                   channel_aa.csv"`, `"HYDIN_PESTS               hydin_pests_day.txt"`, `"HYDIN_PESTS               hydin_pests_day.csv"`, `"HYDIN_PATHS               hydin_paths_day.txt"`, `"HYDIN_PATHS               hydin_paths_day.csv"`, `"HYDIN_METALS              hydin_metals_day.txt"`, `"HYDIN_METALS              hydin_metals_day.csv"`, `"HYDIN_SALTS               hydin_salts_day.txt"`, `"HYDIN_SALTS               hydin_salts_day.csv"`, `"HYDIN_PESTS               hydin_pests_mon.txt"`, `"HYDIN_PESTS               hydin_pests_mon.csv"`, `"HYDIN_PATHS               hydin_paths_mon.txt"`, `"HYDIN_PATHS               hydin_paths_mon.csv"`, `"HYDIN_METALS              hydin_metals_mon.txt"`, `"HYDIN_METALS              hydin_metals_mon.csv"`, `"HYDIN_SALTS               hydin_salts_mon.txt"`, `"HYDIN_SALTS               hydin_salts_mon.csv"`, `"HYDIN_PESTS               hydin_pests_yr.txt"`, `"HYDIN_PESTS               hydin_pests_yr.csv"`, `"HYDIN_PATHS               hydin_paths_yr.txt"`, `"HYDIN_PATHS               hydin_paths_yr.csv"`, `"HYDIN_METALS              hydin_metals_yr.txt"`, `"HYDIN_METALS              hydin_metals_yr.csv"`, `"HYDIN_SALTS               hydin_salts_yr.txt"`, `"HYDIN_SALTS               hydin_salts_yr.csv"`, `"HYDIN_PESTS               hydin_pests_aa.txt"`, `"HYDIN_PESTS               hydin_pests_aa.csv"`, `"HYDIN_PATHS               hydin_paths_aa.txt"`, `"HYDIN_PATHS               hydin_paths_aa.csv"`, `"HYDIN_METALS              hydin_metals_aa.txt"`, `"HYDIN_METALS              hydin_metals_aa.csv"`, `"HYDIN_SALTS               hydin_salts_aa.txt"`, `"HYDIN_SALTS               hydin_salts_aa.csv"`, `"HYDOUT_PESTS              hydout_pests_day.txt"`, `"HYDOUT_PESTS              hydout_pests_day.csv"`, `"HYDOUT_PATHS              hydout_paths_day.txt"`, `"HYDOUT_PATHS              hydout_paths_day.csv"`, `"HYDOUT_METALS             hydout_metals_day.txt"`, `"HYDOUT_METALS             hydout_metals_day.csv"`, `"HYDOUT_SALTS              hydout_salts_day.txt"`, `"HYDOUT_SALTS              hydout_salts_day.csv"`, `"HYDOUT_PESTS              hydout_pests_mon.txt"`, `"HYDOUT_PESTS              hydout_pests_mon.csv"`, `"HYDOUT_PATHS              hydout_paths_mon.txt"`, `"HYDOUT_PATHS              hydout_paths_mon.csv"`, `"HYDOUT_METALS             hydout_metals_mon.txt"`, `"HYDOUT_METALS             hydout_metals_mon.csv"`, `"HYDOUT_SALTS              hydout_salts_mon.txt"`, `"HYDOUT_SALTS              hydout_salts_mon.csv"`, `"HYDOUT_PESTS              hydout_pests_yr.txt"`, `"HYDOUT_PESTS              hydout_pests_yr.csv"`, `"HYDOUT_PATHS              hydout_paths_yr.txt"`, `"HYDOUT_PATHS              hydout_paths_yr.csv"`, `"HYDOUT_METALS             hydout_metals_yr.txt"`, `"HYDOUT_METALS             hydout_metals_yr.csv"`, `"HYDOUT_SALTS              hydout_salts_yr.txt"`, `"HYDOUT_SALTS              hydout_salts_yr.csv"`, `"HYDOUT_PESTS              hydout_pests_aa.txt"`, `"HYDOUT_PESTS              hydout_pests_aa.csv"`, `"HYDOUT_PATHS              hydout_paths_aa.txt"`, `"HYDOUT_PATHS              hydout_paths_aa.csv"`, `"HYDOUT_METALS             hydout_metals_aa.txt"`, `"HYDOUT_METALS             hydout_metals_aa.csv"`, `"HYDOUT_SALTS              hydout_salts_aa.txt"`, `"HYDOUT_SALTS              hydout_salts_aa.csv"`, `"HYDCON                    hydcon.out"`, `"HYDCON                    hydcon.csv"`, `"HYDOUT                    hydout_day.txt"`, `"HYDOUT                    hydout_day.csv"`, `"HYDOUT                    hydout_mon.txt"`, `"HYDOUT                    hydout_mon.csv"`, `"HYDOUT                    hydout_yr.txt"`, `"HYDOUT                    hydout_yr.csv"`, `"HYDOUT                    hydout_aa.txt"`, `"HYDOUT                    hydout_aa.csv"`, `"HYDIN                     hydin_day.txt"`, `"HYDIN                     hydin_day.csv"`, `"HYDIN                     hydin_mon.txt"`, `"HYDIN                     hydin_mon.csv"`, `"HYDIN                     hydin_yr.txt"`, `"HYDIN                     hydin_yr.csv"`, `"HYDIN                     hydin_aa.txt"`, `"HYDIN                     hydin_aa.csv"`, `"DEPO                      deposition_day.txt"`, `"DEPO                      deposition_day.csv"`, `"DEPO                      deposition_mon.txt"`, `"DEPO                      deposition_mon.csv"`, `"DEPO                      deposition_yr.txt"`, `"DEPO                      deposition_yr.csv"`, `"DEPO                      deposition_aa.txt"`, `"DEPO                      deposition_aa.csv"`, `"DTBL                      lu_change_out.txt"`, `"MGT                       mgt_out.txt"`, `"HRU_PATH                  hru_path_day.txt"`, `"HRU_PATH                  hru_path_day.csv"`, `"HRU_PATH                  hru_path_mon.txt"`, `"HRU_PATH                  hru_path_mon.csv"`, `"HRU_PATH                  hru_path_yr.txt"`, `"HRU_PATH                  hru_path_yr.csv"`, `"HRU_PATH                  hru_path_aa.txt"`, `"HRU_PATH                  hru_path_aa.csv"`, `"HRU_PEST                  hru_pest_day.txt"`, `"HRU_PEST                  hru_pest_day.csv"`, `"HRU_PEST                  hru_pest_mon.txt"`, `"HRU_PEST                  hru_pest_mon.csv"`, `"HRU_PEST                  hru_pest_yr.txt"`, `"HRU_PEST                  hru_pest_yr.csv"`, `"HRU_PEST                  hru_pest_aa.txt"`, `"HRU_PEST                  hru_pest_aa.csv"`, `"CHANNEL_PEST              channel_pest_day.txt"`, `"CHANNEL_PEST              channel_pest_day.csv"`, `"CHANNEL_PEST              channel_pest_mon.txt"`, `"CHANNEL_PEST              channel_pest_mon.csv"`, `"CHANNEL_PEST              channel_pest_yr.txt"`, `"CHANNEL_PEST              channel_pest_yr.csv"`, `"CHANNEL_PEST              channel_pest_aa.txt"`, `"CHANNEL_PEST              channel_pest_aa.csv"`, `"RESERVOIR_PEST            reservoir_pest_day.txt"`, `"RESERVOIR_PEST            reservoir_pest_day.csv"`, `"RESERVOIR_PEST            reservoir_pest_mon.txt"`, `"RESERVOIR_PEST            reservoir_pest_mon.csv"`, `"RESERVOIR_PEST            reservoir_pest_yr.txt"`, `"RESERVOIR_PEST            reservoir_pest_yr.csv"`, `"RESERVOIR_PEST            reservoir_pest_aa.txt"`, `"RESERVOIR_PEST            reservoir_pest_aa.csv"`, `"BASIN_AQUIFER_PEST        basin_aqu_pest_day.txt"`, `"BASIN_AQUIFER_PEST        basin_aqu_pest_day.csv"`, `"BASIN_AQUIFER_PEST        basin_aqu_pest_mon.txt"`, `"BASIN_AQUIFER_PEST        basin_aqu_pest_mon.csv"`, `"BASIN_AQUIFER_PEST        basin_aqu_pest_yr.txt"`, `"BASIN_AQUIFER_PEST        basin_aqu_pest_yr.csv"`, `"BASIN_AQUIFER_PEST        basin_aqu_pest_aa.txt"`, `"BASIN_AQUIFER_PEST        basin_aqu_pest_aa.csv"`, `"AQUIFER_PEST              aquifer_pest_day.txt"`, `"AQUIFER_PEST              aquifer_pest_day.csv"`, `"AQUIFER_PEST              aquifer_pest_mon.txt"`, `"AQUIFER_PEST              aquifer_pest_mon.csv"`, `"AQUIFER_PEST              aquifer_pest_yr.txt"`, `"AQUIFER_PEST              aquifer_pest_yr.csv"`, `"AQUIFER_PEST              aquifer_pest_aa.txt"`, `"AQUIFER_PEST              aquifer_pest_aa.csv"`, `"BASIN_CH_PEST             basin_ch_pest_day.txt"`, `"BASIN_CH_PEST             reservoir_pest_day.csv"`, `"BASIN_CH_PEST             basin_ch_pest_mon.txt"`, `"BASIN_CH_PEST             basin_ch_pest_mon.csv"`, `"BASIN_CH_PEST             basin_ch_pest_yr.txt"`, `"BASIN_CH_PEST             basin_ch_pest_yr.csv"`, `"BASIN_CH_PEST             basin_ch_pest_aa.txt"`, `"BASIN_CH_PEST             basin_ch_pest_aa.csv"`, `"BASIN_RES_PEST            basin_res_pest_day.txt"`, `"BASIN_RES_PEST          reservoir_pest_day.csv"`, `"BASIN_RES_PEST            basin_res_pest_mon.txt"`, `"BASIN_RES_PEST            basin_res_pest_mon.csv"`, `"BASIN_RES_PEST            basin_res_pest_yr.txt"`, `"BASIN_RES_PEST            basin_res_pest_yr.csv"`, `"BASIN_RES_PEST            basin_res_pest_aa.txt"`, `"BASIN_RES_PEST            basin_res_pest_aa.csv"`, `"BASIN_LS_PEST             basin_ls_pest_day.txt"`, `"BASIN_LS_PEST             basin_ls_pest_day.csv"`, `"BASIN_LS_PEST             basin_ls_pest_mon.txt"`, `"BASIN_LS_PEST             basin_ls_pest_mon.csv"`, `"BASIN_LS_PEST             basin_ls_pest_yr.txt"`, `"BASIN_LS_PEST             basin_ls_pest_yr.csv"`, `"BASIN_LS_PEST             basin_ls_pest_aa.txt"`, `"BASIN_LS_PEST             basin_ls_pest_aa.csv"`, `"RES                       reservoir_day.txt"`, `"RES                       reservoir_day.csv"`, `"RES                       reservoir_mon.txt"`, `"RES                       reservoir_yr.txt"`, `"RES                       reservoir_yr.csv"`, `"RES                       reservoir_aa.txt"`, `"RES                       reservoir_aa.csv"`, `"SWAT-DEG_CHANNEL         channel_sd_subday.txt"`, `"SWAT-DEG_CHANNEL          channel_sd_subday.csv"`, `"SWAT-DEG_CHANNEL          channel_sd_day.txt"`, `"SWAT-DEG_CHANNEL          channel_sd_day.csv"`, `"SWAT-DEG_CHANNEL          channel_sd_mon.txt"`, `"SWAT-DEG_CHANNEL          channel_sd_mon.csv"`, `"SWAT-DEG_CHANNEL          channel_sd_yr.txt"`, `"SWAT-DEG_CHANNEL          channel_sd_yr.csv"`, `"SWAT-DEG_CHANNEL          channel_sd_aa.txt"`, `"SWAT-DEG_CHANNEL          channel_sd_aa.csv"`, `"SWAT-DEG_CHANNEL_MORPH    channel_sdmorph_day.txt"`, `"SWAT-DEG_CHANNEL_MORPH    channel_sdmorph_day.csv"`, `"SWAT-DEG_CHANNEL_MORPH    channel_sdmorph_mon.txt"`, `"SWAT-DEG_CHANNEL_MORPH    channel_sdmorph_mon.csv"`, `"SWAT-DEG_CHANNEL_MORPH    channel_sdmorph_yr.txt"`, `"SWAT-DEG_CHANNEL_MORPH    channel_sdmorph_yr.csv"`, `"SWAT-DEG_CHANNEL_MORPH    channel_sdmorph_aa.txt"`, `"SWAT-DEG_CHANNEL_MORPH    channel_sdmorph_aa.csv"`, `"SWAT_DEG_CHAN_BUD         sd_chanbud_day.txt"`, `"SWAT_DEG_CHAN_BUD         sd_chanbud_day.csv"`, `"SWAT_DEG_CHAN_BUD         sd_chanbud_mon.txt"`, `"SWAT_DEG_CHAN_BUD         sd_chanbud_mon.csv"`, `"SWAT_DEG_CHAN_BUD         sd_chanbud_yr.txt"`, `"SWAT_DEG_CHAN_BUD         sd_chanbud_yr.csv"`, `"SWAT_DEG_CHAN_BUD         sd_chanbud_aa.txt"`, `"SWAT_DEG_CHAN_BUD         sd_chanbud_aa.csv"`, `"HRU_ORGC                  hru_orgc.txt"`, `"WATER_ALLOCATION          water_allo_day.txt"`, `"WATER_ALLOCATION          water_allo_day.csv"`, `"WATER_ALLOCATION          water_allo_mon.txt"`, `"WATER_ALLOCATION          water_allo_mon.csv"`, `"WATER_ALLOCATION          water_allo_yr.txt"`, `"WATER_ALLOCATION          water_allo_yr.csv"`, `"WATER_ALLOCATION          water_allo_aa.txt"`, `"WATER_ALLOCATION          water_allo_aa.csv"`, `"RES_WET                   wetland_day.txt"`, `"RES_WET                   wetland_day.csv"`, `"RES_WET                   wetland_mon.txt"`, `"RES_WET                   wetland_mon.csv"`, `"RES_WET                   wetland_yr.txt"`, `"RES_WET                   wetland_yr.csv"`, `"RES_WET                   wetland_aa.txt"`, `"RES_WET                   wetland_aa.csv"`, `"FDC                       flow_duration_curve.out"`, `"HRU_SOFT_CALIB_OUT        hru-out.cal"`, `"BASIN_AQUIFER             basin_aqu_day.txt"`, `"BASIN_AQUIFER             basin_aqu_day.csv"`, `"BASIN_AQUIFER             basin_aqu_mon.txt"`, `"BASIN_AQUIFER             basin_aqu_mon.csv"`, `"BASIN_AQUIFER             basin_aqu_yr.txt"`, `"BASIN_AQUIFER             basin_aqu_yr.csv"`, `"BASIN_AQUIFER             basin_aqu_aa.txt"`, `"BASIN_AQUIFER             basin_aqu_aa.csv"`, `"BASIN_RESERVOIR           basin_res_day.txt"`, `"BASIN_RESERVOIR           basin_res_day.csv"`, `"BASIN_RESERVOIR           basin_res_mon.txt"`, `"BASIN_RESERVOIR           basin_res_mon.csv"`, `"BASIN_RESERVOIR           basin_res_yr.txt"`, `"BASIN_RESERVOIR           basin_res_yr.csv"`, `"BASIN_RESERVOIR           basin_res_aa.txt"`, `"BASIN_RESERVOIR           basin_res_aa.csv"`, `"RECALL                    recall_day.txt"`, `"RECALL                    recall_day.csv"`, `"RECALL                    recall_mon.txt"`, `"RECALL                    recall_mon.csv"`, `"RECALL                    recall_yr.txt"`, `"RECALL                    recall_yr.csv"`, `"RECALL_AA                 recall_aa.txt"`, `"RECALL                    recall_aa.csv"`, `"BASIN_CHANNEL             basin_cha_day.txt"`, `"BASIN_CHANNEL             basin_cha_day.txt"`, `"BASIN_CHANNEL             basin_cha_mon.txt"`, `"BASIN_CHANNEL             basin_cha_mon.txt"`, `"BASIN_CHANNEL             basin_cha_yr.txt"`, `"BASIN_CHANNEL             basin_cha_yr.csv"`, `"BASIN_CHANNEL             basin_cha_aa.txt"`, `"BASIN_CHANNEL             basin_cha_aa.csv"`, `"BASIN_SWAT_DEG_CHANNEL    basin_sd_cha_day.txt"`, `"BASIN_SWAT_DEG_CHANNEL    basin_sd_cha_day.csv"`, `"BASIN_SWAT_DEG_CHANNEL    basin_sd_cha_mon.txt"`, `"BASIN_SWAT_DEG_CHANNEL    basin_sd_cha_mon.csv"`, `"BASIN_SWAT_DEG_CHANNEL    basin_sd_cha_yr.txt"`, `"BASIN_SWAT_DEG_CHANNEL    basin_sd_cha_yr.csv"`, `"BASIN_SWAT_DEG_CHANNEL    basin_sd_cha_aa.txt"`, `"BASIN_SWAT_DEG_CHANNEL    basin_sd_cha_aa.csv"`, `"BASIN_SWAT_DEG_CHAN_MORPH basin_sd_chamorph_day.txt"`, `"BASIN_SWAT_DEG_CHAN_MORPH basin_sd_chamorph_day.csv"`, `"BASIN_SWAT_DEG_CHAN_MORPH basin_sd_chamorph_mon.txt"`, `"BASIN_SWAT_DEG_CHAN_MORPH basin_sd_chamorph_mon.csv"`, `"BASIN_SWAT_DEG_CHAN_MORPH basin_sd_chamorph_yr.txt"`, `"BASIN_SWAT_DEG_CHAN_MORPH basin_sd_chamorph_yr.csv"`, `"BASIN_SWAT_DEG_CHAN_MORPH basin_sd_chamorph_aa.txt"`, `"BASIN_SWAT_DEG_CHAN_MORPH basin_sd_chamorph_aa.csv"`, `"BASIN_SWAT_DEG_CHAN_BUD   basin_sd_chanbud_day.txt"`, `"BASIN_SWAT_DEG_CHAN_BUD   basin_sd_chanbud_day.csv"`, `"BASIN_SWAT_DEG_CHAN_BUD   basin_sd_chanbud_mon.txt"`, `"BASIN_SWAT_DEG_CHAN_BUD   basin_sd_chanbud_mon.csv"`, `"BASIN_SWAT_DEG_CHAN_BUD   basin_sd_chanbud_yr.txt"`, `"BASIN_SWAT_DEG_CHAN_BUD   basin_sd_chanbud_yr.csv"`, `"BASIN_SWAT_DEG_CHAN_BUD   basin_sd_chanbud_aa.txt"`, `"BASIN_SWAT_DEG_CHAN_BUD   basin_sd_chanbud_aa.csv"`, `"BASIN_RECALL              basin_psc_day.txt"`, `"BASIN_RECALL              basin_psc_day.csv"`, `"BASIN_RECALL              basin_psc_mon.txt"`, `"BASIN_RECALL              basin_psc_mon.csv"`, `"BASIN_RECALL              basin_psc_yr.txt"`, `"BASIN_RECALL              basin_psc_yr.csv"`, `"BASIN_RECALL_AA           basin_psc_aa.txt"`, `"BASIN_RECALL_AA           basin_psc_aa.csv"`, `"ROUTING_UNITS             ru_day.txt"`, `"ROUTING_UNITS             ru_day.csv"`, `"ROUTING_UNITS             ru_mon.txt"`, `"ROUTING_UNITS             ru_mon.csv"`, `"ROUTING_UNITS             ru_yr.txt"`, `"ROUTING_UNITS             ru_yr.csv"`, `"ROUTING_UNITS             ru_aa.txt"`, `"ROUTING_UNITS             ru_aa.csv"`, `"YLD                       yield.out"`, `"YLD                       yield.csv"`, `"BASIN_CROP_YLD            basin_crop_yld_yr.txt"`, `"BASIN_CROP_YLD            basin_crop_yld_aa.txt"`, `"HRU                       hru_wb_day.txt"`, `"HRU                       hru_wb_day.csv"`, `"HRU                       hru_wb_mon.txt"`, `"HRU                       hru_wb_mon.csv"`, `"HRU                       hru_wb_yr.txt"`, `"HRU                       hru_wb_yr.csv"`, `"HRU                       hru_wb_aa.txt"`, `"HRU                       hru_wb_aa.csv"`, `"HRU                       hru_nb_day.txt"`, `"HRU                       hru_nb_day.csv"`, `"HRU                       hru_ncycle_day.txt"`, `"HRU                       hru_ncycle_day.csv"`, `"HRU                       hru_ncycle_mon.txt"`, `"HRU                       hru_ncycle_mon.csv"`, `"HRU                       hru_ncycle_yr.txt"`, `"HRU                       hru_ncycle_yr.csv"`, `"HRU                       hru_ncycle_aa.txt"`, `"HRU                       hru_ncycle_aa.csv"`, `"HRU                       hru_nb_mon.txt"`, `"HRU                       hru_nb_mon.csv"`, `"HRU                       hru_nb_yr.txt"`, `"HRU                       hru_nb_yr.csv"`, `"HRU                       hru_nb_aa.txt"`, `"HRU                       hru_nb_aa.csv"`, `"HRU                       hru_carb_gl_day.txt"`, `"HRU                       hru_carb_gl_day.csv"`, `"HRU                       hru_carb_gl_mon.txt"`, `"HRU                       hru_carb_gl_mon.csv"`, `"HRU                       hru_carb_gl_yr.txt"`, `"HRU                       hru_carb_gl_yr.csv"`, `"HRU                       hru_carb_gl_aa.txt"`, `"HRU                       hru_carb_gl_aa.csv"`, `"HRU                       hru_scf_day.txt"`, `"HRU                       hru_scf_day.csv"`, `"HRU                       hru_scf_mon.txt"`, `"HRU                       hru_scf_mon.csv"`, `"HRU                       hru_scf_yr.txt"`, `"HRU                       hru_scf_yr.csv"`, `"HRU                       hru_scf_aa.txt"`, `"HRU                       hru_scf_aa.csv"`, `"HRU                       hru_ls_day.txt"`, `"HRU                       hru_ls_day.csv"`, `"HRU                       hru_ls_mon.txt"`, `"HRU                       hru_ls_mon.csv"`, `"HRU                       hru_ls_yr.txt"`, `"HRU                       hru_ls_yr.csv"`, `"HRU                       hru_ls_aa.txt"`, `"HRU                       hru_ls_aa.csv"`, `"HRU                       hru_pw_day.txt"`, `"HRU                       hru_pw_day.csv"`, `"HRU                       hru_pw_mon.txt"`, `"HRU                       hru_pw_mon.csv"`, `"HRU                       hru_pw_yr.txt"`, `"HRU                       hru_pw_yr.csv"`, `"HRU                       hru_pw_aa.txt"`, `"HRU                       hru_pw_aa.csv"`, `"SWAT-DEG                  hru-lte_wb_day.txt"`, `"SWAT-DEG                  hru-lte_wb_day.csv"`, `"SWAT-DEG                  hru-lte_wb_mon.txt"`, `"SWAT-DEG                  hru-lte_wb_mon.csv"`, `"SWAT-DEG                  hru-lte_wb_yr.txt"`, `"SWAT-DEG                  hru-lte_wb_yr.csv"`, `"SWAT-DEG                  hru-lte_wb_aa.txt"`, `"SWAT-DEG                  hru-lte_wb_aa.csv"`, `"SWAT-DEG                  hru-lte_ls_day.txt"`, `"SWAT-DEG                  hru-lte_ls_day.csv"`, `"SWAT-DEG                  hru-lte_ls_mon.txt"`, `"SWAT-DEG                  hru-lte_ls_mon.csv"`, `"SWAT-DEG                  hru-lte_ls_yr.txt"`, `"SWAT-DEG                  hru-lte_ls_yr.csv"`, `"SWAT-DEG                  hru-lte_ls_aa.txt"`, `"SWAT-DEG                  hru-lte_ls_aa.csv"`, `"SWAT-DEG                  hru-lte_pw_day.txt"`, `"SWAT-DEG                  hru-lte_pw_day.csv"`, `"SWAT-DEG                  hru-lte_pw_mon.txt"`, `"SWAT-DEG                  hru-lte_pw_mon.csv"`, `"SWAT-DEG                  hru-lte_pw_yr.txt"`, `"SWAT-DEG                  hru-lte_pw_yr.csv"`, `"SWAT-DEG                  hru-lte_pw_aa.txt"`, `"SWAT-DEG                  hru-lte_pw_aa.csv"`, `"ROUTING_UNIT              lsunit_wb_day.txt"`, `"ROUTING_UNIT              lsunit_wb_day.csv"`, `"ROUTING_UNIT              lsunit_wb_mon.txt"`, `"ROUTING_UNIT              lsunit_wb_mon.csv"`, `"ROUTING_UNIT              lsunit_wb_yr.txt"`, `"ROUTING_UNIT              lsunit_wb_yr.csv"`, `"ROUTING_UNIT              lsunit_wb_aa.txt"`, `"ROUTING_UNIT              lsunit_wb_aa.csv"`, `"ROUTING_UNIT              lsunit_nb_day.txt"`, `"ROUTING_UNIT              lsunit_nb_day.csv"`, `"ROUTING_UNIT              lsunit_nb_mon.txt"`, `"ROUTING_UNIT              lsunit_nb_mon.csv"`, `"ROUTING_UNIT              lsunit_nb_yr.txt"`, `"ROUTING_UNIT              lsunit_nb_yr.csv"`, `"ROUTING_UNIT              lsunit_nb_aa.txt"`, `"ROUTING_UNIT              lsunit_nb_aa.csv"`, `"ROUTING_UNIT              lsunit_ls_day.txt"`, `"ROUTING_UNIT              lsunit_ls_day.csv"`, `"ROUTING_UNIT              lsunit_ls_mon.txt"`, `"ROUTING_UNIT              lsunit_ls_mon.csv"`, `"ROUTING_UNIT              lsunit_ls_yr.txt"`, `"ROUTING_UNIT              lsunit_ls_yr.csv"`, `"ROUTING_UNIT              lsunit_ls_aa.txt"`, `"ROUTING_UNIT              lsunit_ls_aa.csv"`, `"ROUTING_UNIT              lsunit_pw_day.txt"`, `"ROUTING_UNIT              lsunit_pw_day.csv"`, `"ROUTING_UNIT              lsunit_pw_mon.txt"`, `"ROUTING_UNIT              lsunit_pw_mon.csv"`, `"ROUTING_UNIT              lsunit_pw_yr.txt"`, `"ROUTING_UNIT              lsunit_pw_yr.csv"`, `"ROUTING_UNIT              lsunit_pw_aa.txt"`, `"ROUTING_UNIT              lsunit_pw_aa.csv"`, `"BASIN                     basin_wb_day.txt"`, `"BASIN                     basin_wb_day.csv"`, `"BASIN                     basin_wb_mon.txt"`, `"BASIN                     basin_wb_mon.csv"`, `"BASIN                     basin_wb_yr.txt"`, `"BASIN                     basin_wb_yr.csv"`, `"BASIN                     basin_wb_aa.txt"`, `"BASIN                     basin_wb_aa.csv"`, `"BASIN                     basin_nb_day.txt"`, `"BASIN                     basin_nb_day.csv"`, `"BASIN                     basin_nb_mon.txt"`, `"BASIN                     basin_nb_mon.csv"`, `"BASIN                     basin_nb_yr.txt"`, `"BASIN                     basin_nb_yr.csv"`, `"BASIN                     basin_nb_aa.txt"`, `"BASIN                     basin_nb_aa.csv"`, `"BASIN                     basin_ls_day.txt"`, `"BASIN                     basin_ls_day.csv"`, `"BASIN                     basin_ls_mon.txt"`, `"BASIN                     basin_ls_mon.csv"`, `"BASIN                     basin_ls_yr.txt"`, `"BASIN                     basin_ls_yr.csv"`, `"BASIN                     basin_ls_aa.txt"`, `"BASIN                     basin_ls_aa.csv"`, `"BASIN                     basin_pw_day.txt"`, `"BASIN                     basin_pw_day.csv"`, `"BASIN                     basin_pw_mon.txt"`, `"BASIN                     basin_pw_mon.csv"`, `"BASIN                     basin_pw_yr.txt"`, `"BASIN                     basin_pw_yr.csv"`, `"BASIN                     basin_pw_aa.txt"`, `"BASIN                     basin_pw_aa.csv"`, `"CROP                      crop_yld_yr.txt"`, `"CROP                      crop_yld_yr.csv"`, `"CROP                      crop_yld_aa.txt"`, `"CROP                      crop_yld_aa.csv"`, `"LSU                       lsu_carb_gl_day.txt"`, `"LSU                       lsu_carb_gl_day.csv"`, `"LSU                       lsu_carb_gl_mon.txt"`, `"LSU                       lsu_carb_gl_mon.csv"`, `"LSU                       lsu_carb_gl_yr.txt"`, `"LSU                       lsu_carb_gl_yr.csv"`, `"LSU                       lsu_carb_gl_aa.txt"`, `"LSU                       lsu_carb_gl_aa.csv"`, `"LSU                       lsu_scf_day.txt"`, `"LSU                       lsu_scf_day.csv"`, `"LSU                       lsu_scf_mon.txt"`, `"LSU                       lsu_scf_mon.csv"`, `"LSU                       lsu_scf_yr.txt"`, `"LSU                       lsu_scf_yr.csv"`, `"LSU                       lsu_scf_aa.txt"`, `"LSU                       lsu_scf_aa.csv"`, `"LSU                       lsu_plc_stat_day.txt"`, `"LSU                       lsu_plc_stat_day.csv"`, `"LSU                       lsu_plc_stat_mon.txt"`, `"LSU                       lsu_plc_stat_mon.csv"`, `"LSU                       lsu_plc_stat_yr.txt"`, `"LSU                       lsu_plc_stat_yr.csv"`, `"LSU                       lsu_plc_stat_aa.txt"`, `"LSU                       lsu_plc_stat_aa.csv"`, `"HRU                       " // trim(fname_txt)`, `"HRU                       " // trim(fname_csv)`, `"HRU                       " // trim(fname_txt)`, `"HRU                       " // trim(fname_csv)`, `"HRU                       " // trim(fname_txt)`, `"HRU                       " // trim(fname_csv)`, `"files_out.out - OUTPUT FILES WRITTEN"`, `"CHK                       checker.out"`
- Candidate flattened write order: `"HRU                       hru_cbn_lyr.txt"`, `"HRU                       hru_cbn_lyr.csv"`, `"HRU                       hru_seq_lyr.txt"`, `"HRU                       hru_seq_lyr.csv"`, `"HRU                       hru_n_p_pool_stat.txt"`, `"HRU                       hru_n_p_pool_stat.csv"`, `"HRU                       hru_begsim_soil_prop.txt"`, `"HRU                       hru_begsim_soil_prop.csv"`, `"HRU                       hru_endsim_soil_prop.txt"`, `"HRU                       hru_endsim_soil_prop.csv"`, `"HRU                       hru_plc_stat.txt"`, `"HRU                       hru_plc_stat.csv"`, `"HRU                       hru_cflux_stat.txt"`, `"HRU                       hru_cflux_stat.csv"`, `"HRU                       hru_cpool_stat.txt"`, `"HRU                       hru_cpool_stat.csv"`, `"HRU                       hru_carbvars.txt"`, `"HRU                       hru_carbvars.csv"`, `"HRU                       hru_org_allo_vars.txt"`, `"HRU                       hru_org_allo_vars.csv"`, `"HRU                       hru_org_ratio_vars.txt"`, `"HRU                       hru_org_ratio_vars.csv"`, `"HRU                       hru_org_trans_vars.txt"`, `"HRU                       hru_org_trans_vars.csv"`, `"BASIN                     basin_carbon_all.txt"`, `"AQUIFER                   aquifer_day.txt"`, `"AQUIFER                   aquifer_day.csv"`, `"AQUIFER                   aquifer_mon.txt"`, `"AQUIFER                   aquifer_mon.csv"`, `"AQUIFER                   aquifer_yr.txt"`, `"AQUIFER                   aquifer_yr.csv"`, `"AQUIFER                   aquifer_aa.txt"`, `"AQUIFER                   aquifer_aa.csv"`, `"CHANNEL                   channel_day.txt"`, `"CHANNEL                   channel_day.csv"`, `"CHANNEL                   channel_mon.txt"`, `"CHANNEL                   channel_mon.csv"`, `"CHANNEL                   channel_yr.txt"`, `"CHANNEL                   channel_yr.csv"`, `"CHANNEL                   channel_aa.txt"`, `"CHANNEL                   channel_aa.csv"`, `"HYDIN_PESTS               hydin_pests_day.txt"`, `"HYDIN_PESTS               hydin_pests_day.csv"`, `"HYDIN_PATHS               hydin_paths_day.txt"`, `"HYDIN_PATHS               hydin_paths_day.csv"`, `"HYDIN_METALS              hydin_metals_day.txt"`, `"HYDIN_METALS              hydin_metals_day.csv"`, `"HYDIN_SALTS               hydin_salts_day.txt"`, `"HYDIN_SALTS               hydin_salts_day.csv"`, `"HYDIN_PESTS               hydin_pests_mon.txt"`, `"HYDIN_PESTS               hydin_pests_mon.csv"`, `"HYDIN_PATHS               hydin_paths_mon.txt"`, `"HYDIN_PATHS               hydin_paths_mon.csv"`, `"HYDIN_METALS              hydin_metals_mon.txt"`, `"HYDIN_METALS              hydin_metals_mon.csv"`, `"HYDIN_SALTS               hydin_salts_mon.txt"`, `"HYDIN_SALTS               hydin_salts_mon.csv"`, `"HYDIN_PESTS               hydin_pests_yr.txt"`, `"HYDIN_PESTS               hydin_pests_yr.csv"`, `"HYDIN_PATHS               hydin_paths_yr.txt"`, `"HYDIN_PATHS               hydin_paths_yr.csv"`, `"HYDIN_METALS              hydin_metals_yr.txt"`, `"HYDIN_METALS              hydin_metals_yr.csv"`, `"HYDIN_SALTS               hydin_salts_yr.txt"`, `"HYDIN_SALTS               hydin_salts_yr.csv"`, `"HYDIN_PESTS               hydin_pests_aa.txt"`, `"HYDIN_PESTS               hydin_pests_aa.csv"`, `"HYDIN_PATHS               hydin_paths_aa.txt"`, `"HYDIN_PATHS               hydin_paths_aa.csv"`, `"HYDIN_METALS              hydin_metals_aa.txt"`, `"HYDIN_METALS              hydin_metals_aa.csv"`, `"HYDIN_SALTS               hydin_salts_aa.txt"`, `"HYDIN_SALTS               hydin_salts_aa.csv"`, `"HYDOUT_PESTS              hydout_pests_day.txt"`, `"HYDOUT_PESTS              hydout_pests_day.csv"`, `"HYDOUT_PATHS              hydout_paths_day.txt"`, `"HYDOUT_PATHS              hydout_paths_day.csv"`, `"HYDOUT_METALS             hydout_metals_day.txt"`, `"HYDOUT_METALS             hydout_metals_day.csv"`, `"HYDOUT_SALTS              hydout_salts_day.txt"`, `"HYDOUT_SALTS              hydout_salts_day.csv"`, `"HYDOUT_PESTS              hydout_pests_mon.txt"`, `"HYDOUT_PESTS              hydout_pests_mon.csv"`, `"HYDOUT_PATHS              hydout_paths_mon.txt"`, `"HYDOUT_PATHS              hydout_paths_mon.csv"`, `"HYDOUT_METALS             hydout_metals_mon.txt"`, `"HYDOUT_METALS             hydout_metals_mon.csv"`, `"HYDOUT_SALTS              hydout_salts_mon.txt"`, `"HYDOUT_SALTS              hydout_salts_mon.csv"`, `"HYDOUT_PESTS              hydout_pests_yr.txt"`, `"HYDOUT_PESTS              hydout_pests_yr.csv"`, `"HYDOUT_PATHS              hydout_paths_yr.txt"`, `"HYDOUT_PATHS              hydout_paths_yr.csv"`, `"HYDOUT_METALS             hydout_metals_yr.txt"`, `"HYDOUT_METALS             hydout_metals_yr.csv"`, `"HYDOUT_SALTS              hydout_salts_yr.txt"`, `"HYDOUT_SALTS              hydout_salts_yr.csv"`, `"HYDOUT_PESTS              hydout_pests_aa.txt"`, `"HYDOUT_PESTS              hydout_pests_aa.csv"`, `"HYDOUT_PATHS              hydout_paths_aa.txt"`, `"HYDOUT_PATHS              hydout_paths_aa.csv"`, `"HYDOUT_METALS             hydout_metals_aa.txt"`, `"HYDOUT_METALS             hydout_metals_aa.csv"`, `"HYDOUT_SALTS              hydout_salts_aa.txt"`, `"HYDOUT_SALTS              hydout_salts_aa.csv"`, `"HYDCON                    hydcon.out"`, `"HYDCON                    hydcon.csv"`, `"HYDOUT                    hydout_day.txt"`, `"HYDOUT                    hydout_day.csv"`, `"HYDOUT                    hydout_mon.txt"`, `"HYDOUT                    hydout_mon.csv"`, `"HYDOUT                    hydout_yr.txt"`, `"HYDOUT                    hydout_yr.csv"`, `"HYDOUT                    hydout_aa.txt"`, `"HYDOUT                    hydout_aa.csv"`, `"HYDIN                     hydin_day.txt"`, `"HYDIN                     hydin_day.csv"`, `"HYDIN                     hydin_mon.txt"`, `"HYDIN                     hydin_mon.csv"`, `"HYDIN                     hydin_yr.txt"`, `"HYDIN                     hydin_yr.csv"`, `"HYDIN                     hydin_aa.txt"`, `"HYDIN                     hydin_aa.csv"`, `"DEPO                      deposition_day.txt"`, `"DEPO                      deposition_day.csv"`, `"DEPO                      deposition_mon.txt"`, `"DEPO                      deposition_mon.csv"`, `"DEPO                      deposition_yr.txt"`, `"DEPO                      deposition_yr.csv"`, `"DEPO                      deposition_aa.txt"`, `"DEPO                      deposition_aa.csv"`, `"DTBL                      lu_change_out.txt"`, `"MGT                       mgt_out.txt"`, `"HRU_PATH                  hru_path_day.txt"`, `"HRU_PATH                  hru_path_day.csv"`, `"HRU_PATH                  hru_path_mon.txt"`, `"HRU_PATH                  hru_path_mon.csv"`, `"HRU_PATH                  hru_path_yr.txt"`, `"HRU_PATH                  hru_path_yr.csv"`, `"HRU_PATH                  hru_path_aa.txt"`, `"HRU_PATH                  hru_path_aa.csv"`, `"HRU_PEST                  hru_pest_day.txt"`, `"HRU_PEST                  hru_pest_day.csv"`, `"HRU_PEST                  hru_pest_mon.txt"`, `"HRU_PEST                  hru_pest_mon.csv"`, `"HRU_PEST                  hru_pest_yr.txt"`, `"HRU_PEST                  hru_pest_yr.csv"`, `"HRU_PEST                  hru_pest_aa.txt"`, `"HRU_PEST                  hru_pest_aa.csv"`, `"CHANNEL_PEST              channel_pest_day.txt"`, `"CHANNEL_PEST              channel_pest_day.csv"`, `"CHANNEL_PEST              channel_pest_mon.txt"`, `"CHANNEL_PEST              channel_pest_mon.csv"`, `"CHANNEL_PEST              channel_pest_yr.txt"`, `"CHANNEL_PEST              channel_pest_yr.csv"`, `"CHANNEL_PEST              channel_pest_aa.txt"`, `"CHANNEL_PEST              channel_pest_aa.csv"`, `"RESERVOIR_PEST            reservoir_pest_day.txt"`, `"RESERVOIR_PEST            reservoir_pest_day.csv"`, `"RESERVOIR_PEST            reservoir_pest_mon.txt"`, `"RESERVOIR_PEST            reservoir_pest_mon.csv"`, `"RESERVOIR_PEST            reservoir_pest_yr.txt"`, `"RESERVOIR_PEST            reservoir_pest_yr.csv"`, `"RESERVOIR_PEST            reservoir_pest_aa.txt"`, `"RESERVOIR_PEST            reservoir_pest_aa.csv"`, `"BASIN_AQUIFER_PEST        basin_aqu_pest_day.txt"`, `"BASIN_AQUIFER_PEST        basin_aqu_pest_day.csv"`, `"BASIN_AQUIFER_PEST        basin_aqu_pest_mon.txt"`, `"BASIN_AQUIFER_PEST        basin_aqu_pest_mon.csv"`, `"BASIN_AQUIFER_PEST        basin_aqu_pest_yr.txt"`, `"BASIN_AQUIFER_PEST        basin_aqu_pest_yr.csv"`, `"BASIN_AQUIFER_PEST        basin_aqu_pest_aa.txt"`, `"BASIN_AQUIFER_PEST        basin_aqu_pest_aa.csv"`, `"AQUIFER_PEST              aquifer_pest_day.txt"`, `"AQUIFER_PEST              aquifer_pest_day.csv"`, `"AQUIFER_PEST              aquifer_pest_mon.txt"`, `"AQUIFER_PEST              aquifer_pest_mon.csv"`, `"AQUIFER_PEST              aquifer_pest_yr.txt"`, `"AQUIFER_PEST              aquifer_pest_yr.csv"`, `"AQUIFER_PEST              aquifer_pest_aa.txt"`, `"AQUIFER_PEST              aquifer_pest_aa.csv"`, `"BASIN_CH_PEST             basin_ch_pest_day.txt"`, `"BASIN_CH_PEST             reservoir_pest_day.csv"`, `"BASIN_CH_PEST             basin_ch_pest_mon.txt"`, `"BASIN_CH_PEST             basin_ch_pest_mon.csv"`, `"BASIN_CH_PEST             basin_ch_pest_yr.txt"`, `"BASIN_CH_PEST             basin_ch_pest_yr.csv"`, `"BASIN_CH_PEST             basin_ch_pest_aa.txt"`, `"BASIN_CH_PEST             basin_ch_pest_aa.csv"`, `"BASIN_RES_PEST            basin_res_pest_day.txt"`, `"BASIN_RES_PEST          reservoir_pest_day.csv"`, `"BASIN_RES_PEST            basin_res_pest_mon.txt"`, `"BASIN_RES_PEST            basin_res_pest_mon.csv"`, `"BASIN_RES_PEST            basin_res_pest_yr.txt"`, `"BASIN_RES_PEST            basin_res_pest_yr.csv"`, `"BASIN_RES_PEST            basin_res_pest_aa.txt"`, `"BASIN_RES_PEST            basin_res_pest_aa.csv"`, `"BASIN_LS_PEST             basin_ls_pest_day.txt"`, `"BASIN_LS_PEST             basin_ls_pest_day.csv"`, `"BASIN_LS_PEST             basin_ls_pest_mon.txt"`, `"BASIN_LS_PEST             basin_ls_pest_mon.csv"`, `"BASIN_LS_PEST             basin_ls_pest_yr.txt"`, `"BASIN_LS_PEST             basin_ls_pest_yr.csv"`, `"BASIN_LS_PEST             basin_ls_pest_aa.txt"`, `"BASIN_LS_PEST             basin_ls_pest_aa.csv"`, `"RES                       reservoir_day.txt"`, `"RES                       reservoir_day.csv"`, `"RES                       reservoir_mon.txt"`, `"RES                       reservoir_yr.txt"`, `"RES                       reservoir_yr.csv"`, `"RES                       reservoir_aa.txt"`, `"RES                       reservoir_aa.csv"`, `"SWAT-DEG_CHANNEL         channel_sd_subday.txt"`, `"SWAT-DEG_CHANNEL          channel_sd_subday.csv"`, `"SWAT-DEG_CHANNEL          channel_sd_day.txt"`, `"SWAT-DEG_CHANNEL          channel_sd_day.csv"`, `"SWAT-DEG_CHANNEL          channel_sd_mon.txt"`, `"SWAT-DEG_CHANNEL          channel_sd_mon.csv"`, `"SWAT-DEG_CHANNEL          channel_sd_yr.txt"`, `"SWAT-DEG_CHANNEL          channel_sd_yr.csv"`, `"SWAT-DEG_CHANNEL          channel_sd_aa.txt"`, `"SWAT-DEG_CHANNEL          channel_sd_aa.csv"`, `"SWAT-DEG_CHANNEL_MORPH    channel_sdmorph_day.txt"`, `"SWAT-DEG_CHANNEL_MORPH    channel_sdmorph_day.csv"`, `"SWAT-DEG_CHANNEL_MORPH    channel_sdmorph_mon.txt"`, `"SWAT-DEG_CHANNEL_MORPH    channel_sdmorph_mon.csv"`, `"SWAT-DEG_CHANNEL_MORPH    channel_sdmorph_yr.txt"`, `"SWAT-DEG_CHANNEL_MORPH    channel_sdmorph_yr.csv"`, `"SWAT-DEG_CHANNEL_MORPH    channel_sdmorph_aa.txt"`, `"SWAT-DEG_CHANNEL_MORPH    channel_sdmorph_aa.csv"`, `"SWAT_DEG_CHAN_BUD         sd_chanbud_day.txt"`, `"SWAT_DEG_CHAN_BUD         sd_chanbud_day.csv"`, `"SWAT_DEG_CHAN_BUD         sd_chanbud_mon.txt"`, `"SWAT_DEG_CHAN_BUD         sd_chanbud_mon.csv"`, `"SWAT_DEG_CHAN_BUD         sd_chanbud_yr.txt"`, `"SWAT_DEG_CHAN_BUD         sd_chanbud_yr.csv"`, `"SWAT_DEG_CHAN_BUD         sd_chanbud_aa.txt"`, `"SWAT_DEG_CHAN_BUD         sd_chanbud_aa.csv"`, `"SWAT_DEG_CHANBUD        chanbud.txt"`, `"CHANBUD_ORDER         chanbud_order.txt"`, `"BASIN SEDBUD          bsn_sedbud.txt"`, `"HRU_ORGC                  hru_orgc.txt"`, `"WATER_ALLOCATION          water_allo_day.txt"`, `"WATER_ALLOCATION          water_allo_day.csv"`, `"WATER_ALLOCATION          water_allo_mon.txt"`, `"WATER_ALLOCATION          water_allo_mon.csv"`, `"WATER_ALLOCATION          water_allo_yr.txt"`, `"WATER_ALLOCATION          water_allo_yr.csv"`, `"WATER_ALLOCATION          water_allo_aa.txt"`, `"WATER_ALLOCATION          water_allo_aa.csv"`, `"WATER_ALLOCATION          wallo_use_day.txt"`, `"WATER_ALLOCATION          wallo_use_day.csv"`, `"WATER_ALLOCATION          wallo_use_mon.txt"`, `"WATER_ALLOCATION          wallo_use_mon.csv"`, `"WATER_ALLOCATION          wallo_use_yr.txt"`, `"WATER_ALLOCATION          wallo_use_yr.csv"`, `"WATER_ALLOCATION          wallo_use_aa.txt"`, `"WATER_ALLOCATION          wallo_use_aa.csv"`, `"WATER_ALLOCATION          wallo_treat_day.txt"`, `"WATER_ALLOCATION          wallo_treat_day.csv"`, `"WATER_ALLOCATION          wallo_treat_mon.txt"`, `"WATER_ALLOCATION          wallo_treat_mon.csv"`, `"WATER_ALLOCATION          wallo_treat_yr.txt"`, `"WATER_ALLOCATION          wallo_treat_yr.csv"`, `"WATER_ALLOCATION          wallo_treat_aa.txt"`, `"WATER_ALLOCATION          wallo_treat_aa.csv"`, `"RES_WET                   wetland_day.txt"`, `"RES_WET                   wetland_day.csv"`, `"RES_WET                   wetland_mon.txt"`, `"RES_WET                   wetland_mon.csv"`, `"RES_WET                   wetland_yr.txt"`, `"RES_WET                   wetland_yr.csv"`, `"RES_WET                   wetland_aa.txt"`, `"RES_WET                   wetland_aa.csv"`, `"FDC                       flow_duration_curve.out"`, `"HRU_SOFT_CALIB_OUT        hru-out.cal"`, `"BASIN_AQUIFER             basin_aqu_day.txt"`, `"BASIN_AQUIFER             basin_aqu_day.csv"`, `"BASIN_AQUIFER             basin_aqu_mon.txt"`, `"BASIN_AQUIFER             basin_aqu_mon.csv"`, `"BASIN_AQUIFER             basin_aqu_yr.txt"`, `"BASIN_AQUIFER             basin_aqu_yr.csv"`, `"BASIN_AQUIFER             basin_aqu_aa.txt"`, `"BASIN_AQUIFER             basin_aqu_aa.csv"`, `"BASIN_RESERVOIR           basin_res_day.txt"`, `"BASIN_RESERVOIR           basin_res_day.csv"`, `"BASIN_RESERVOIR           basin_res_mon.txt"`, `"BASIN_RESERVOIR           basin_res_mon.csv"`, `"BASIN_RESERVOIR           basin_res_yr.txt"`, `"BASIN_RESERVOIR           basin_res_yr.csv"`, `"BASIN_RESERVOIR           basin_res_aa.txt"`, `"BASIN_RESERVOIR           basin_res_aa.csv"`, `"RECALL                    recall_day.txt"`, `"RECALL                    recall_day.csv"`, `"RECALL                    recall_mon.txt"`, `"RECALL                    recall_mon.csv"`, `"RECALL                    recall_yr.txt"`, `"RECALL                    recall_yr.csv"`, `"RECALL_AA                 recall_aa.txt"`, `"RECALL                    recall_aa.csv"`, `"BASIN_CHANNEL             basin_cha_day.txt"`, `"BASIN_CHANNEL             basin_cha_day.txt"`, `"BASIN_CHANNEL             basin_cha_mon.txt"`, `"BASIN_CHANNEL             basin_cha_mon.txt"`, `"BASIN_CHANNEL             basin_cha_yr.txt"`, `"BASIN_CHANNEL             basin_cha_yr.csv"`, `"BASIN_CHANNEL             basin_cha_aa.txt"`, `"BASIN_CHANNEL             basin_cha_aa.csv"`, `"BASIN_SWAT_DEG_CHANNEL    basin_sd_cha_day.txt"`, `"BASIN_SWAT_DEG_CHANNEL    basin_sd_cha_day.csv"`, `"BASIN_SWAT_DEG_CHANNEL    basin_sd_cha_mon.txt"`, `"BASIN_SWAT_DEG_CHANNEL    basin_sd_cha_mon.csv"`, `"BASIN_SWAT_DEG_CHANNEL    basin_sd_cha_yr.txt"`, `"BASIN_SWAT_DEG_CHANNEL    basin_sd_cha_yr.csv"`, `"BASIN_SWAT_DEG_CHANNEL    basin_sd_cha_aa.txt"`, `"BASIN_SWAT_DEG_CHANNEL    basin_sd_cha_aa.csv"`, `"BASIN_SWAT_DEG_CHAN_MORPH basin_sd_chamorph_day.txt"`, `"BASIN_SWAT_DEG_CHAN_MORPH basin_sd_chamorph_day.csv"`, `"BASIN_SWAT_DEG_CHAN_MORPH basin_sd_chamorph_mon.txt"`, `"BASIN_SWAT_DEG_CHAN_MORPH basin_sd_chamorph_mon.csv"`, `"BASIN_SWAT_DEG_CHAN_MORPH basin_sd_chamorph_yr.txt"`, `"BASIN_SWAT_DEG_CHAN_MORPH basin_sd_chamorph_yr.csv"`, `"BASIN_SWAT_DEG_CHAN_MORPH basin_sd_chamorph_aa.txt"`, `"BASIN_SWAT_DEG_CHAN_MORPH basin_sd_chamorph_aa.csv"`, `"BASIN_SWAT_DEG_CHAN_BUD   basin_sd_chanbud_day.txt"`, `"BASIN_SWAT_DEG_CHAN_BUD   basin_sd_chanbud_day.csv"`, `"BASIN_SWAT_DEG_CHAN_BUD   basin_sd_chanbud_mon.txt"`, `"BASIN_SWAT_DEG_CHAN_BUD   basin_sd_chanbud_mon.csv"`, `"BASIN_SWAT_DEG_CHAN_BUD   basin_sd_chanbud_yr.txt"`, `"BASIN_SWAT_DEG_CHAN_BUD   basin_sd_chanbud_yr.csv"`, `"BASIN_SWAT_DEG_CHAN_BUD   basin_sd_chanbud_aa.txt"`, `"BASIN_SWAT_DEG_CHAN_BUD   basin_sd_chanbud_aa.csv"`, `"BASIN_RECALL              basin_psc_day.txt"`, `"BASIN_RECALL              basin_psc_day.csv"`, `"BASIN_RECALL              basin_psc_mon.txt"`, `"BASIN_RECALL              basin_psc_mon.csv"`, `"BASIN_RECALL              basin_psc_yr.txt"`, `"BASIN_RECALL              basin_psc_yr.csv"`, `"BASIN_RECALL_AA           basin_psc_aa.txt"`, `"BASIN_RECALL_AA           basin_psc_aa.csv"`, `"ROUTING_UNITS             ru_day.txt"`, `"ROUTING_UNITS             ru_day.csv"`, `"ROUTING_UNITS             ru_mon.txt"`, `"ROUTING_UNITS             ru_mon.csv"`, `"ROUTING_UNITS             ru_yr.txt"`, `"ROUTING_UNITS             ru_yr.csv"`, `"ROUTING_UNITS             ru_aa.txt"`, `"ROUTING_UNITS             ru_aa.csv"`, `"YLD                       yield.out"`, `"YLD                       yield.csv"`, `"BASIN_CROP_YLD            basin_crop_yld_yr.txt"`, `"BASIN_CROP_YLD            basin_crop_yld_aa.txt"`, `"HRU                       hru_wb_day.txt"`, `"HRU                       hru_wb_day.csv"`, `"HRU                       hru_wb_mon.txt"`, `"HRU                       hru_wb_mon.csv"`, `"HRU                       hru_wb_yr.txt"`, `"HRU                       hru_wb_yr.csv"`, `"HRU                       hru_wb_aa.txt"`, `"HRU                       hru_wb_aa.csv"`, `"HRU                       hru_nb_day.txt"`, `"HRU                       hru_nb_day.csv"`, `"HRU                       hru_ncycle_day.txt"`, `"HRU                       hru_ncycle_day.csv"`, `"HRU                       hru_ncycle_mon.txt"`, `"HRU                       hru_ncycle_mon.csv"`, `"HRU                       hru_ncycle_yr.txt"`, `"HRU                       hru_ncycle_yr.csv"`, `"HRU                       hru_ncycle_aa.txt"`, `"HRU                       hru_ncycle_aa.csv"`, `"HRU                       hru_nb_mon.txt"`, `"HRU                       hru_nb_mon.csv"`, `"HRU                       hru_nb_yr.txt"`, `"HRU                       hru_nb_yr.csv"`, `"HRU                       hru_nb_aa.txt"`, `"HRU                       hru_nb_aa.csv"`, `"HRU                       hru_carb_gl_day.txt"`, `"HRU                       hru_carb_gl_day.csv"`, `"HRU                       hru_carb_gl_mon.txt"`, `"HRU                       hru_carb_gl_mon.csv"`, `"HRU                       hru_carb_gl_yr.txt"`, `"HRU                       hru_carb_gl_yr.csv"`, `"HRU                       hru_carb_gl_aa.txt"`, `"HRU                       hru_carb_gl_aa.csv"`, `"HRU                       hru_scf_day.txt"`, `"HRU                       hru_scf_day.csv"`, `"HRU                       hru_scf_mon.txt"`, `"HRU                       hru_scf_mon.csv"`, `"HRU                       hru_scf_yr.txt"`, `"HRU                       hru_scf_yr.csv"`, `"HRU                       hru_scf_aa.txt"`, `"HRU                       hru_scf_aa.csv"`, `"HRU                       hru_ls_day.txt"`, `"HRU                       hru_ls_day.csv"`, `"HRU                       hru_ls_mon.txt"`, `"HRU                       hru_ls_mon.csv"`, `"HRU                       hru_ls_yr.txt"`, `"HRU                       hru_ls_yr.csv"`, `"HRU                       hru_ls_aa.txt"`, `"HRU                       hru_ls_aa.csv"`, `"HRU                       hru_pw_day.txt"`, `"HRU                       hru_pw_day.csv"`, `"HRU                       hru_pw_mon.txt"`, `"HRU                       hru_pw_mon.csv"`, `"HRU                       hru_pw_yr.txt"`, `"HRU                       hru_pw_yr.csv"`, `"HRU                       hru_pw_aa.txt"`, `"HRU                       hru_pw_aa.csv"`, `"SWAT-DEG                  hru-lte_wb_day.txt"`, `"SWAT-DEG                  hru-lte_wb_day.csv"`, `"SWAT-DEG                  hru-lte_wb_mon.txt"`, `"SWAT-DEG                  hru-lte_wb_mon.csv"`, `"SWAT-DEG                  hru-lte_wb_yr.txt"`, `"SWAT-DEG                  hru-lte_wb_yr.csv"`, `"SWAT-DEG                  hru-lte_wb_aa.txt"`, `"SWAT-DEG                  hru-lte_wb_aa.csv"`, `"SWAT-DEG                  hru-lte_ls_day.txt"`, `"SWAT-DEG                  hru-lte_ls_day.csv"`, `"SWAT-DEG                  hru-lte_ls_mon.txt"`, `"SWAT-DEG                  hru-lte_ls_mon.csv"`, `"SWAT-DEG                  hru-lte_ls_yr.txt"`, `"SWAT-DEG                  hru-lte_ls_yr.csv"`, `"SWAT-DEG                  hru-lte_ls_aa.txt"`, `"SWAT-DEG                  hru-lte_ls_aa.csv"`, `"SWAT-DEG                  hru-lte_pw_day.txt"`, `"SWAT-DEG                  hru-lte_pw_day.csv"`, `"SWAT-DEG                  hru-lte_pw_mon.txt"`, `"SWAT-DEG                  hru-lte_pw_mon.csv"`, `"SWAT-DEG                  hru-lte_pw_yr.txt"`, `"SWAT-DEG                  hru-lte_pw_yr.csv"`, `"SWAT-DEG                  hru-lte_pw_aa.txt"`, `"SWAT-DEG                  hru-lte_pw_aa.csv"`, `"ROUTING_UNIT              lsunit_wb_day.txt"`, `"ROUTING_UNIT              lsunit_wb_day.csv"`, `"ROUTING_UNIT              lsunit_wb_mon.txt"`, `"ROUTING_UNIT              lsunit_wb_mon.csv"`, `"ROUTING_UNIT              lsunit_wb_yr.txt"`, `"ROUTING_UNIT              lsunit_wb_yr.csv"`, `"ROUTING_UNIT              lsunit_wb_aa.txt"`, `"ROUTING_UNIT              lsunit_wb_aa.csv"`, `"ROUTING_UNIT              lsunit_nb_day.txt"`, `"ROUTING_UNIT              lsunit_nb_day.csv"`, `"ROUTING_UNIT              lsunit_nb_mon.txt"`, `"ROUTING_UNIT              lsunit_nb_mon.csv"`, `"ROUTING_UNIT              lsunit_nb_yr.txt"`, `"ROUTING_UNIT              lsunit_nb_yr.csv"`, `"ROUTING_UNIT              lsunit_nb_aa.txt"`, `"ROUTING_UNIT              lsunit_nb_aa.csv"`, `"ROUTING_UNIT              lsunit_ls_day.txt"`, `"ROUTING_UNIT              lsunit_ls_day.csv"`, `"ROUTING_UNIT              lsunit_ls_mon.txt"`, `"ROUTING_UNIT              lsunit_ls_mon.csv"`, `"ROUTING_UNIT              lsunit_ls_yr.txt"`, `"ROUTING_UNIT              lsunit_ls_yr.csv"`, `"ROUTING_UNIT              lsunit_ls_aa.txt"`, `"ROUTING_UNIT              lsunit_ls_aa.csv"`, `"ROUTING_UNIT              lsunit_pw_day.txt"`, `"ROUTING_UNIT              lsunit_pw_day.csv"`, `"ROUTING_UNIT              lsunit_pw_mon.txt"`, `"ROUTING_UNIT              lsunit_pw_mon.csv"`, `"ROUTING_UNIT              lsunit_pw_yr.txt"`, `"ROUTING_UNIT              lsunit_pw_yr.csv"`, `"ROUTING_UNIT              lsunit_pw_aa.txt"`, `"ROUTING_UNIT              lsunit_pw_aa.csv"`, `"BASIN                     basin_wb_day.txt"`, `"BASIN                     basin_wb_day.csv"`, `"BASIN                     basin_wb_mon.txt"`, `"BASIN                     basin_wb_mon.csv"`, `"BASIN                     basin_wb_yr.txt"`, `"BASIN                     basin_wb_yr.csv"`, `"BASIN                     basin_wb_aa.txt"`, `"BASIN                     basin_wb_aa.csv"`, `"BASIN                     basin_nb_day.txt"`, `"BASIN                     basin_nb_day.csv"`, `"BASIN                     basin_nb_mon.txt"`, `"BASIN                     basin_nb_mon.csv"`, `"BASIN                     basin_nb_yr.txt"`, `"BASIN                     basin_nb_yr.csv"`, `"BASIN                     basin_nb_aa.txt"`, `"BASIN                     basin_nb_aa.csv"`, `"BASIN                     basin_ls_day.txt"`, `"BASIN                     basin_ls_day.csv"`, `"BASIN                     basin_ls_mon.txt"`, `"BASIN                     basin_ls_mon.csv"`, `"BASIN                     basin_ls_yr.txt"`, `"BASIN                     basin_ls_yr.csv"`, `"BASIN                     basin_ls_aa.txt"`, `"BASIN                     basin_ls_aa.csv"`, `"BASIN                     basin_pw_day.txt"`, `"BASIN                     basin_pw_day.csv"`, `"BASIN                     basin_pw_mon.txt"`, `"BASIN                     basin_pw_mon.csv"`, `"BASIN                     basin_pw_yr.txt"`, `"BASIN                     basin_pw_yr.csv"`, `"BASIN                     basin_pw_aa.txt"`, `"BASIN                     basin_pw_aa.csv"`, `"CROP                      crop_yld_yr.txt"`, `"CROP                      crop_yld_yr.csv"`, `"CROP                      crop_yld_aa.txt"`, `"CROP                      crop_yld_aa.csv"`, `"LSU                       lsu_carb_gl_day.txt"`, `"LSU                       lsu_carb_gl_day.csv"`, `"LSU                       lsu_carb_gl_mon.txt"`, `"LSU                       lsu_carb_gl_mon.csv"`, `"LSU                       lsu_carb_gl_yr.txt"`, `"LSU                       lsu_carb_gl_yr.csv"`, `"LSU                       lsu_carb_gl_aa.txt"`, `"LSU                       lsu_carb_gl_aa.csv"`, `"LSU                       lsu_scf_day.txt"`, `"LSU                       lsu_scf_day.csv"`, `"LSU                       lsu_scf_mon.txt"`, `"LSU                       lsu_scf_mon.csv"`, `"LSU                       lsu_scf_yr.txt"`, `"LSU                       lsu_scf_yr.csv"`, `"LSU                       lsu_scf_aa.txt"`, `"LSU                       lsu_scf_aa.csv"`, `"LSU                       lsu_plc_stat_day.txt"`, `"LSU                       lsu_plc_stat_day.csv"`, `"LSU                       lsu_plc_stat_mon.txt"`, `"LSU                       lsu_plc_stat_mon.csv"`, `"LSU                       lsu_plc_stat_yr.txt"`, `"LSU                       lsu_plc_stat_yr.csv"`, `"LSU                       lsu_plc_stat_aa.txt"`, `"LSU                       lsu_plc_stat_aa.csv"`, `"HRU                       " // trim(fname_txt)`, `"HRU                       " // trim(fname_csv)`, `"HRU                       " // trim(fname_txt)`, `"HRU                       " // trim(fname_csv)`, `"HRU                       " // trim(fname_txt)`, `"HRU                       " // trim(fname_csv)`, `"files_out.out - OUTPUT FILES WRITTEN"`, `"CHK                       checker.out"`

#### Write-order edits

- `insert` at base index 238 / candidate index 238: removed _no fields captured_; added `"SWAT_DEG_CHANBUD        chanbud.txt"`, `"CHANBUD_ORDER         chanbud_order.txt"`, `"BASIN SEDBUD          bsn_sedbud.txt"`
- `insert` at base index 247 / candidate index 250: removed _no fields captured_; added `"WATER_ALLOCATION          wallo_use_day.txt"`, `"WATER_ALLOCATION          wallo_use_day.csv"`, `"WATER_ALLOCATION          wallo_use_mon.txt"`, `"WATER_ALLOCATION          wallo_use_mon.csv"`, `"WATER_ALLOCATION          wallo_use_yr.txt"`, `"WATER_ALLOCATION          wallo_use_yr.csv"`, `"WATER_ALLOCATION          wallo_use_aa.txt"`, `"WATER_ALLOCATION          wallo_use_aa.csv"`, `"WATER_ALLOCATION          wallo_treat_day.txt"`, `"WATER_ALLOCATION          wallo_treat_day.csv"`, `"WATER_ALLOCATION          wallo_treat_mon.txt"`, `"WATER_ALLOCATION          wallo_treat_mon.csv"`, `"WATER_ALLOCATION          wallo_treat_yr.txt"`, `"WATER_ALLOCATION          wallo_treat_yr.csv"`, `"WATER_ALLOCATION          wallo_treat_aa.txt"`, `"WATER_ALLOCATION          wallo_treat_aa.csv"`

#### Base write structure

- Source expression(s): _none captured_

- Procedure: `carbon_legacy_open`
- Writer: `carbon_legacy_module.f90`
- Match: source_output
- Resolved default filename(s): `files_out.out`

| Line | Role | Condition | Fields written |
| --- | --- | --- | --- |
| 480 | data | `if (pco%cb_hru%d /= "n" .or. pco%cb_hru%m /= "n"  .or. pco%cb_hru%y /= "n") then` | `"HRU                       hru_cbn_lyr.txt"` |
| 484 | data | `if (pco%cb_hru%d /= "n" .or. pco%cb_hru%m /= "n"  .or. pco%cb_hru%y /= "n") then > if (pco%csvout == "y") then` | `"HRU                       hru_cbn_lyr.csv"` |
| 489 | data | `if (pco%cb_hru%d /= "n" .or. pco%cb_hru%m /= "n"  .or. pco%cb_hru%y /= "n") then` | `"HRU                       hru_seq_lyr.txt"` |
| 493 | data | `if (pco%cb_hru%d /= "n" .or. pco%cb_hru%m /= "n"  .or. pco%cb_hru%y /= "n") then > if (pco%csvout == "y") then` | `"HRU                       hru_seq_lyr.csv"` |
| 500 | data | `if (pco%cb_hru%d /= "n" .or. pco%cb_hru%m /= "n"  .or. pco%cb_hru%y /= "n") then` | `"HRU                       hru_n_p_pool_stat.txt"` |
| 506 | data | `if (pco%cb_hru%d /= "n" .or. pco%cb_hru%m /= "n"  .or. pco%cb_hru%y /= "n") then > if (pco%csvout == "y") then` | `"HRU                       hru_n_p_pool_stat.csv"` |
| 514 | data | `if (pco%cb_hru%d /= "n" .or. pco%cb_hru%m /= "n"  .or. pco%cb_hru%y /= "n") then > if (cbn_diagnostics .eqv. .true.) then` | `"HRU                       hru_begsim_soil_prop.txt"` |
| 519 | data | `if (pco%cb_hru%d /= "n" .or. pco%cb_hru%m /= "n"  .or. pco%cb_hru%y /= "n") then > if (cbn_diagnostics .eqv. .true.) then > if (pco%csvout == "y") then` | `"HRU                       hru_begsim_soil_prop.csv"` |
| 526 | data | `if (pco%cb_hru%d /= "n" .or. pco%cb_hru%m /= "n"  .or. pco%cb_hru%y /= "n") then > if (cbn_diagnostics .eqv. .true.) then` | `"HRU                       hru_endsim_soil_prop.txt"` |
| 531 | data | `if (pco%cb_hru%d /= "n" .or. pco%cb_hru%m /= "n"  .or. pco%cb_hru%y /= "n") then > if (cbn_diagnostics .eqv. .true.) then > if (pco%csvout == "y") then` | `"HRU                       hru_endsim_soil_prop.csv"` |
| 545 | data | `if (pco%cb_hru%d /= "n" .or. pco%cb_hru%m /= "n"  .or. pco%cb_hru%y /= "n") then > if (cbn_diagnostics .eqv. .true.) then > if (bsn_cc%cswat == 2 ) then > if (pco%cb_hru%d /= "n" .or. pco%cb_hru%m /= "n" .or. pco%cb_hru%y /= "n" .or. pco%cb_hru%a /= "n") then` | `"HRU                       hru_plc_stat.txt"` |
| 551 | data | `if (pco%cb_hru%d /= "n" .or. pco%cb_hru%m /= "n"  .or. pco%cb_hru%y /= "n") then > if (cbn_diagnostics .eqv. .true.) then > if (bsn_cc%cswat == 2 ) then > if (pco%cb_hru%d /= "n" .or. pco%cb_hru%m /= "n" .or. pco%cb_hru%y /= "n" .or. pco%cb_hru%a /= "n") then > if (pco%csvout == "y") then` | `"HRU                       hru_plc_stat.csv"` |
| 558 | data | `if (pco%cb_hru%d /= "n" .or. pco%cb_hru%m /= "n"  .or. pco%cb_hru%y /= "n") then > if (cbn_diagnostics .eqv. .true.) then > if (bsn_cc%cswat == 2 ) then > if (pco%cb_hru%d /= "n" .or. pco%cb_hru%m /= "n" .or. pco%cb_hru%y /= "n" .or. pco%cb_hru%a /= "n") then` | `"HRU                       hru_cflux_stat.txt"` |
| 564 | data | `if (pco%cb_hru%d /= "n" .or. pco%cb_hru%m /= "n"  .or. pco%cb_hru%y /= "n") then > if (cbn_diagnostics .eqv. .true.) then > if (bsn_cc%cswat == 2 ) then > if (pco%cb_hru%d /= "n" .or. pco%cb_hru%m /= "n" .or. pco%cb_hru%y /= "n" .or. pco%cb_hru%a /= "n") then > if (pco%csvout == "y") then` | `"HRU                       hru_cflux_stat.csv"` |
| 571 | data | `if (pco%cb_hru%d /= "n" .or. pco%cb_hru%m /= "n"  .or. pco%cb_hru%y /= "n") then > if (cbn_diagnostics .eqv. .true.) then > if (bsn_cc%cswat == 2 ) then > if (pco%cb_hru%d /= "n" .or. pco%cb_hru%m /= "n" .or. pco%cb_hru%y /= "n" .or. pco%cb_hru%a /= "n") then` | `"HRU                       hru_cpool_stat.txt"` |
| 577 | data | `if (pco%cb_hru%d /= "n" .or. pco%cb_hru%m /= "n"  .or. pco%cb_hru%y /= "n") then > if (cbn_diagnostics .eqv. .true.) then > if (bsn_cc%cswat == 2 ) then > if (pco%cb_hru%d /= "n" .or. pco%cb_hru%m /= "n" .or. pco%cb_hru%y /= "n" .or. pco%cb_hru%a /= "n") then > if (pco%csvout == "y") then` | `"HRU                       hru_cpool_stat.csv"` |
| 591 | data | `if (bsn_cc%cswat == 2 ) then > if (pco%cb_vars_hru%d /= "n" .or. pco%cb_vars_hru%m /= "n"  .or. pco%cb_vars_hru%y /= "n" ) then` | `"HRU                       hru_carbvars.txt"` |
| 596 | data | `if (bsn_cc%cswat == 2 ) then > if (pco%cb_vars_hru%d /= "n" .or. pco%cb_vars_hru%m /= "n"  .or. pco%cb_vars_hru%y /= "n" ) then > if (pco%csvout == "y") then` | `"HRU                       hru_carbvars.csv"` |
| 603 | data | `if (bsn_cc%cswat == 2 ) then > if (pco%cb_vars_hru%d /= "n" .or. pco%cb_vars_hru%m /= "n"  .or. pco%cb_vars_hru%y /= "n" ) then` | `"HRU                       hru_org_allo_vars.txt"` |
| 608 | data | `if (bsn_cc%cswat == 2 ) then > if (pco%cb_vars_hru%d /= "n" .or. pco%cb_vars_hru%m /= "n"  .or. pco%cb_vars_hru%y /= "n" ) then > if (pco%csvout == "y") then` | `"HRU                       hru_org_allo_vars.csv"` |
| 615 | data | `if (bsn_cc%cswat == 2 ) then > if (pco%cb_vars_hru%d /= "n" .or. pco%cb_vars_hru%m /= "n"  .or. pco%cb_vars_hru%y /= "n" ) then` | `"HRU                       hru_org_ratio_vars.txt"` |
| 620 | data | `if (bsn_cc%cswat == 2 ) then > if (pco%cb_vars_hru%d /= "n" .or. pco%cb_vars_hru%m /= "n"  .or. pco%cb_vars_hru%y /= "n" ) then > if (pco%csvout == "y") then` | `"HRU                       hru_org_ratio_vars.csv"` |
| 628 | data | `if (bsn_cc%cswat == 2 ) then > if (pco%cb_vars_hru%d /= "n" .or. pco%cb_vars_hru%m /= "n"  .or. pco%cb_vars_hru%y /= "n" ) then` | `"HRU                       hru_org_trans_vars.txt"` |
| 634 | data | `if (bsn_cc%cswat == 2 ) then > if (pco%cb_vars_hru%d /= "n" .or. pco%cb_vars_hru%m /= "n"  .or. pco%cb_vars_hru%y /= "n" ) then > if (pco%csvout == "y") then` | `"HRU                       hru_org_trans_vars.csv"` |
| 648 | data | `if (pco%cb_hru%d /= "n" .or. pco%cb_hru%m /= "n" .or. pco%cb_hru%y /= "n" .or. pco%cb_hru%a /= "n") then > if (pco%nb_hru%a == "y") then` | `"BASIN                     basin_carbon_all.txt"` |


- Procedure: `header_aquifer`
- Writer: `header_aquifer.f90`
- Match: source_output
- Resolved default filename(s): `files_out.out`

| Line | Role | Condition | Fields written |
| --- | --- | --- | --- |
| 17 | data | `if (sp_ob%aqu > 0) then > if (pco%aqu%d == "y") then` | `"AQUIFER                   aquifer_day.txt"` |
| 23 | data | `if (sp_ob%aqu > 0) then > if (pco%aqu%d == "y") then > if (pco%csvout == "y") then` | `"AQUIFER                   aquifer_day.csv"` |
| 34 | data | `if (sp_ob%aqu > 0) then > if (pco%aqu%m == "y") then` | `"AQUIFER                   aquifer_mon.txt"` |
| 40 | data | `if (sp_ob%aqu > 0) then > if (pco%aqu%m == "y") then > if (pco%csvout == "y") then` | `"AQUIFER                   aquifer_mon.csv"` |
| 51 | data | `if (sp_ob%aqu > 0) then > if (pco%aqu%y == "y") then` | `"AQUIFER                   aquifer_yr.txt"` |
| 57 | data | `if (sp_ob%aqu > 0) then > if (pco%aqu%y == "y") then > if (pco%csvout == "y") then` | `"AQUIFER                   aquifer_yr.csv"` |
| 68 | data | `if (sp_ob%aqu > 0) then > if (pco%aqu%a == "y") then` | `"AQUIFER                   aquifer_aa.txt"` |
| 74 | data | `if (sp_ob%aqu > 0) then > if (pco%aqu%a == "y") then > if (pco%csvout == "y") then` | `"AQUIFER                   aquifer_aa.csv"` |


- Procedure: `header_channel`
- Writer: `header_channel.f90`
- Match: source_output
- Resolved default filename(s): `files_out.out`

| Line | Role | Condition | Fields written |
| --- | --- | --- | --- |
| 30 | data | `if (sp_ob%chan > 0) then > if (pco%chan%d == "y") then` | `"CHANNEL                   channel_day.txt"` |
| 36 | data | `if (sp_ob%chan > 0) then > if (pco%chan%d == "y") then > if (pco%csvout == "y")  then` | `"CHANNEL                   channel_day.csv"` |
| 47 | data | `if (sp_ob%chan > 0) then > if (pco%chan%m == "y") then` | `"CHANNEL                   channel_mon.txt"` |
| 53 | data | `if (sp_ob%chan > 0) then > if (pco%chan%m == "y") then > if (pco%csvout == "y") then` | `"CHANNEL                   channel_mon.csv"` |
| 64 | data | `if (sp_ob%chan > 0) then > if (pco%chan%y == "y") then` | `"CHANNEL                   channel_yr.txt"` |
| 70 | data | `if (sp_ob%chan > 0) then > if (pco%chan%y == "y") then > if (pco%csvout == "y")  then` | `"CHANNEL                   channel_yr.csv"` |
| 81 | data | `if (sp_ob%chan > 0) then > if (pco%chan%a == "y") then` | `"CHANNEL                   channel_aa.txt"` |
| 87 | data | `if (sp_ob%chan > 0) then > if (pco%chan%a == "y") then > if (pco%csvout == "y") then` | `"CHANNEL                   channel_aa.csv"` |


- Procedure: `header_cs`
- Writer: `header_cs.f90`
- Match: source_output
- Resolved default filename(s): `files_out.out`

| Line | Role | Condition | Fields written |
| --- | --- | --- | --- |
| 18 | data | `if (pco%hyd%d == "y") then > if (cs_db%num_pests > 0) then` | `"HYDIN_PESTS               hydin_pests_day.txt"` |
| 23 | data | `if (pco%hyd%d == "y") then > if (cs_db%num_pests > 0) then > if (pco%csvout == "y") then` | `"HYDIN_PESTS               hydin_pests_day.csv"` |
| 31 | data | `if (pco%hyd%d == "y") then > if (cs_db%num_paths > 0) then` | `"HYDIN_PATHS               hydin_paths_day.txt"` |
| 36 | data | `if (pco%hyd%d == "y") then > if (cs_db%num_paths > 0) then > if (pco%csvout == "y") then` | `"HYDIN_PATHS               hydin_paths_day.csv"` |
| 44 | data | `if (pco%hyd%d == "y") then > if (cs_db%num_metals > 0) then` | `"HYDIN_METALS              hydin_metals_day.txt"` |
| 49 | data | `if (pco%hyd%d == "y") then > if (cs_db%num_metals > 0) then > if (pco%csvout == "y") then` | `"HYDIN_METALS              hydin_metals_day.csv"` |
| 57 | data | `if (pco%hyd%d == "y") then > if (cs_db%num_salts > 0) then` | `"HYDIN_SALTS               hydin_salts_day.txt"` |
| 62 | data | `if (pco%hyd%d == "y") then > if (cs_db%num_salts > 0) then > if (pco%csvout == "y") then` | `"HYDIN_SALTS               hydin_salts_day.csv"` |
| 73 | data | `if (pco%hyd%m == "y") then > if (cs_db%num_pests > 0) then` | `"HYDIN_PESTS               hydin_pests_mon.txt"` |
| 78 | data | `if (pco%hyd%m == "y") then > if (cs_db%num_pests > 0) then > if (pco%csvout == "y") then` | `"HYDIN_PESTS               hydin_pests_mon.csv"` |
| 87 | data | `if (pco%hyd%m == "y") then > if (cs_db%num_paths > 0) then` | `"HYDIN_PATHS               hydin_paths_mon.txt"` |
| 92 | data | `if (pco%hyd%m == "y") then > if (cs_db%num_paths > 0) then > if (pco%csvout == "y") then` | `"HYDIN_PATHS               hydin_paths_mon.csv"` |
| 100 | data | `if (pco%hyd%m == "y") then > if (cs_db%num_metals > 0) then` | `"HYDIN_METALS              hydin_metals_mon.txt"` |
| 105 | data | `if (pco%hyd%m == "y") then > if (cs_db%num_metals > 0) then > if (pco%csvout == "y") then` | `"HYDIN_METALS              hydin_metals_mon.csv"` |
| 113 | data | `if (pco%hyd%m == "y") then > if (cs_db%num_salts > 0) then` | `"HYDIN_SALTS               hydin_salts_mon.txt"` |
| 118 | data | `if (pco%hyd%m == "y") then > if (cs_db%num_salts > 0) then > if (pco%csvout == "y") then` | `"HYDIN_SALTS               hydin_salts_mon.csv"` |
| 130 | data | `if (pco%hyd%y == "y") then > if (cs_db%num_pests > 0) then` | `"HYDIN_PESTS               hydin_pests_yr.txt"` |
| 135 | data | `if (pco%hyd%y == "y") then > if (cs_db%num_pests > 0) then > if (pco%csvout == "y") then` | `"HYDIN_PESTS               hydin_pests_yr.csv"` |
| 143 | data | `if (pco%hyd%y == "y") then > if (cs_db%num_paths > 0) then` | `"HYDIN_PATHS               hydin_paths_yr.txt"` |
| 148 | data | `if (pco%hyd%y == "y") then > if (cs_db%num_paths > 0) then > if (pco%csvout == "y") then` | `"HYDIN_PATHS               hydin_paths_yr.csv"` |
| 156 | data | `if (pco%hyd%y == "y") then > if (cs_db%num_metals > 0) then` | `"HYDIN_METALS              hydin_metals_yr.txt"` |
| 161 | data | `if (pco%hyd%y == "y") then > if (cs_db%num_metals > 0) then > if (pco%csvout == "y") then` | `"HYDIN_METALS              hydin_metals_yr.csv"` |
| 169 | data | `if (pco%hyd%y == "y") then > if (cs_db%num_salts > 0) then` | `"HYDIN_SALTS               hydin_salts_yr.txt"` |
| 174 | data | `if (pco%hyd%y == "y") then > if (cs_db%num_salts > 0) then > if (pco%csvout == "y") then` | `"HYDIN_SALTS               hydin_salts_yr.csv"` |
| 185 | data | `if (pco%hyd%a == "y") then > if (cs_db%num_pests > 0) then` | `"HYDIN_PESTS               hydin_pests_aa.txt"` |
| 190 | data | `if (pco%hyd%a == "y") then > if (cs_db%num_pests > 0) then > if (pco%csvout == "y") then` | `"HYDIN_PESTS               hydin_pests_aa.csv"` |
| 198 | data | `if (pco%hyd%a == "y") then > if (cs_db%num_paths > 0) then` | `"HYDIN_PATHS               hydin_paths_aa.txt"` |
| 203 | data | `if (pco%hyd%a == "y") then > if (cs_db%num_paths > 0) then > if (pco%csvout == "y") then` | `"HYDIN_PATHS               hydin_paths_aa.csv"` |
| 211 | data | `if (pco%hyd%a == "y") then > if (cs_db%num_metals > 0) then` | `"HYDIN_METALS              hydin_metals_aa.txt"` |
| 216 | data | `if (pco%hyd%a == "y") then > if (cs_db%num_metals > 0) then > if (pco%csvout == "y") then` | `"HYDIN_METALS              hydin_metals_aa.csv"` |
| 224 | data | `if (pco%hyd%a == "y") then > if (cs_db%num_salts > 0) then` | `"HYDIN_SALTS               hydin_salts_aa.txt"` |
| 229 | data | `if (pco%hyd%a == "y") then > if (cs_db%num_salts > 0) then > if (pco%csvout == "y") then` | `"HYDIN_SALTS               hydin_salts_aa.csv"` |
| 242 | data | `if (pco%hyd%d == "y") then > if (cs_db%num_pests > 0) then` | `"HYDOUT_PESTS              hydout_pests_day.txt"` |
| 247 | data | `if (pco%hyd%d == "y") then > if (cs_db%num_pests > 0) then > if (pco%csvout == "y") then` | `"HYDOUT_PESTS              hydout_pests_day.csv"` |
| 253 | data | `if (pco%hyd%d == "y") then > if (cs_db%num_paths > 0) then` | `"HYDOUT_PATHS              hydout_paths_day.txt"` |
| 260 | data | `if (pco%hyd%d == "y") then > if (cs_db%num_paths > 0) then > if (pco%csvout == "y") then` | `"HYDOUT_PATHS              hydout_paths_day.csv"` |
| 266 | data | `if (pco%hyd%d == "y") then > if (cs_db%num_metals > 0) then` | `"HYDOUT_METALS             hydout_metals_day.txt"` |
| 271 | data | `if (pco%hyd%d == "y") then > if (cs_db%num_metals > 0) then > if (pco%csvout == "y") then` | `"HYDOUT_METALS             hydout_metals_day.csv"` |
| 279 | data | `if (pco%hyd%d == "y") then > if (cs_db%num_salts > 0) then` | `"HYDOUT_SALTS              hydout_salts_day.txt"` |
| 284 | data | `if (pco%hyd%d == "y") then > if (cs_db%num_salts > 0) then > if (pco%csvout == "y") then` | `"HYDOUT_SALTS              hydout_salts_day.csv"` |
| 295 | data | `if (pco%hyd%m == "y") then > if (cs_db%num_pests > 0) then` | `"HYDOUT_PESTS              hydout_pests_mon.txt"` |
| 300 | data | `if (pco%hyd%m == "y") then > if (cs_db%num_pests > 0) then > if (pco%csvout == "y") then` | `"HYDOUT_PESTS              hydout_pests_mon.csv"` |
| 308 | data | `if (pco%hyd%m == "y") then > if (cs_db%num_paths > 0) then` | `"HYDOUT_PATHS              hydout_paths_mon.txt"` |
| 313 | data | `if (pco%hyd%m == "y") then > if (cs_db%num_paths > 0) then > if (pco%csvout == "y") then` | `"HYDOUT_PATHS              hydout_paths_mon.csv"` |
| 321 | data | `if (pco%hyd%m == "y") then > if (cs_db%num_metals > 0) then` | `"HYDOUT_METALS             hydout_metals_mon.txt"` |
| 326 | data | `if (pco%hyd%m == "y") then > if (cs_db%num_metals > 0) then > if (pco%csvout == "y") then` | `"HYDOUT_METALS             hydout_metals_mon.csv"` |
| 334 | data | `if (pco%hyd%m == "y") then > if (cs_db%num_salts > 0) then` | `"HYDOUT_SALTS              hydout_salts_mon.txt"` |
| 339 | data | `if (pco%hyd%m == "y") then > if (cs_db%num_salts > 0) then > if (pco%csvout == "y") then` | `"HYDOUT_SALTS              hydout_salts_mon.csv"` |
| 351 | data | `if (pco%hyd%y == "y") then > if (cs_db%num_pests > 0) then` | `"HYDOUT_PESTS              hydout_pests_yr.txt"` |
| 356 | data | `if (pco%hyd%y == "y") then > if (cs_db%num_pests > 0) then > if (pco%csvout == "y") then` | `"HYDOUT_PESTS              hydout_pests_yr.csv"` |
| 364 | data | `if (pco%hyd%y == "y") then > if (cs_db%num_paths > 0) then` | `"HYDOUT_PATHS              hydout_paths_yr.txt"` |
| 369 | data | `if (pco%hyd%y == "y") then > if (cs_db%num_paths > 0) then > if (pco%csvout == "y") then` | `"HYDOUT_PATHS              hydout_paths_yr.csv"` |
| 377 | data | `if (pco%hyd%y == "y") then > if (cs_db%num_metals > 0) then` | `"HYDOUT_METALS             hydout_metals_yr.txt"` |
| 382 | data | `if (pco%hyd%y == "y") then > if (cs_db%num_metals > 0) then > if (pco%csvout == "y") then` | `"HYDOUT_METALS             hydout_metals_yr.csv"` |
| 390 | data | `if (pco%hyd%y == "y") then > if (cs_db%num_salts > 0) then` | `"HYDOUT_SALTS              hydout_salts_yr.txt"` |
| 395 | data | `if (pco%hyd%y == "y") then > if (cs_db%num_salts > 0) then > if (pco%csvout == "y") then` | `"HYDOUT_SALTS              hydout_salts_yr.csv"` |
| 406 | data | `if (pco%hyd%a == "y") then > if (cs_db%num_pests > 0) then` | `"HYDOUT_PESTS              hydout_pests_aa.txt"` |
| 411 | data | `if (pco%hyd%a == "y") then > if (cs_db%num_pests > 0) then > if (pco%csvout == "y") then` | `"HYDOUT_PESTS              hydout_pests_aa.csv"` |
| 419 | data | `if (pco%hyd%a == "y") then > if (cs_db%num_paths > 0) then` | `"HYDOUT_PATHS              hydout_paths_aa.txt"` |
| 424 | data | `if (pco%hyd%a == "y") then > if (cs_db%num_paths > 0) then > if (pco%csvout == "y") then` | `"HYDOUT_PATHS              hydout_paths_aa.csv"` |
| 432 | data | `if (pco%hyd%a == "y") then > if (cs_db%num_metals > 0) then` | `"HYDOUT_METALS             hydout_metals_aa.txt"` |
| 437 | data | `if (pco%hyd%a == "y") then > if (cs_db%num_metals > 0) then > if (pco%csvout == "y") then` | `"HYDOUT_METALS             hydout_metals_aa.csv"` |
| 445 | data | `if (pco%hyd%a == "y") then > if (cs_db%num_salts > 0) then` | `"HYDOUT_SALTS              hydout_salts_aa.txt"` |
| 450 | data | `if (pco%hyd%a == "y") then > if (cs_db%num_salts > 0) then > if (pco%csvout == "y") then` | `"HYDOUT_SALTS              hydout_salts_aa.csv"` |


- Procedure: `header_hyd`
- Writer: `header_hyd.f90`
- Match: source_output
- Resolved default filename(s): `files_out.out`

| Line | Role | Condition | Fields written |
| --- | --- | --- | --- |
| 11 | data | `if (pco%hydcon == "y") then` | `"HYDCON                    hydcon.out"` |
| 14 | data | `if (pco%hydcon == "y") then > if (pco%csvout == "y") then` | `"HYDCON                    hydcon.csv"` |
| 24 | data | `if (pco%hyd%d == "y") then` | `"HYDOUT                    hydout_day.txt"` |
| 30 | data | `if (pco%hyd%d == "y") then > if (pco%csvout == "y") then` | `"HYDOUT                    hydout_day.csv"` |
| 39 | data | `if (pco%hyd%m == "y") then` | `"HYDOUT                    hydout_mon.txt"` |
| 45 | data | `if (pco%hyd%m == "y") then > if (pco%csvout == "y") then` | `"HYDOUT                    hydout_mon.csv"` |
| 54 | data | `if (pco%hyd%y == "y") then` | `"HYDOUT                    hydout_yr.txt"` |
| 60 | data | `if (pco%hyd%y == "y") then > if (pco%csvout == "y") then` | `"HYDOUT                    hydout_yr.csv"` |
| 69 | data | `if (pco%hyd%a == "y") then` | `"HYDOUT                    hydout_aa.txt"` |
| 75 | data | `if (pco%hyd%a == "y") then > if (pco%csvout == "y") then` | `"HYDOUT                    hydout_aa.csv"` |
| 86 | data | `if (pco%hyd%d == "y") then` | `"HYDIN                     hydin_day.txt"` |
| 92 | data | `if (pco%hyd%d == "y") then > if (pco%csvout == "y") then` | `"HYDIN                     hydin_day.csv"` |
| 101 | data | `if (pco%hyd%m == "y") then` | `"HYDIN                     hydin_mon.txt"` |
| 107 | data | `if (pco%hyd%m == "y") then > if (pco%csvout == "y") then` | `"HYDIN                     hydin_mon.csv"` |
| 116 | data | `if (pco%hyd%y == "y") then` | `"HYDIN                     hydin_yr.txt"` |
| 122 | data | `if (pco%hyd%y == "y") then > if (pco%csvout == "y") then` | `"HYDIN                     hydin_yr.csv"` |
| 131 | data | `if (pco%hyd%a == "y") then` | `"HYDIN                     hydin_aa.txt"` |
| 137 | data | `if (pco%hyd%a == "y") then > if (pco%csvout == "y") then` | `"HYDIN                     hydin_aa.csv"` |
| 148 | data | `if (pco%hyd%d == "y") then` | `"DEPO                      deposition_day.txt"` |
| 154 | data | `if (pco%hyd%d == "y") then > if (pco%csvout == "y") then` | `"DEPO                      deposition_day.csv"` |
| 164 | data | `if (pco%hyd%m == "y") then` | `"DEPO                      deposition_mon.txt"` |
| 170 | data | `if (pco%hyd%m == "y") then > if (pco%csvout == "y") then` | `"DEPO                      deposition_mon.csv"` |
| 180 | data | `if (pco%hyd%y == "y") then` | `"DEPO                      deposition_yr.txt"` |
| 186 | data | `if (pco%hyd%y == "y") then > if (pco%csvout == "y") then` | `"DEPO                      deposition_yr.csv"` |
| 196 | data | `if (pco%hyd%a == "y") then` | `"DEPO                      deposition_aa.txt"` |
| 202 | data | `if (pco%hyd%a == "y") then > if (pco%csvout == "y") then` | `"DEPO                      deposition_aa.csv"` |


- Procedure: `header_lu_change`
- Writer: `header_lu_change.f90`
- Match: source_output
- Resolved default filename(s): `files_out.out`

| Line | Role | Condition | Fields written |
| --- | --- | --- | --- |
| 13 | data | `None` | `"DTBL                      lu_change_out.txt"` |


- Procedure: `header_mgt`
- Writer: `header_mgt.f90`
- Match: source_output
- Resolved default filename(s): `files_out.out`

| Line | Role | Condition | Fields written |
| --- | --- | --- | --- |
| 13 | data | `if (pco%mgtout == "y") then` | `"MGT                       mgt_out.txt"` |


- Procedure: `header_path`
- Writer: `header_path.f90`
- Match: source_output
- Resolved default filename(s): `files_out.out`

| Line | Role | Condition | Fields written |
| --- | --- | --- | --- |
| 15 | data | `if (pco%wb_hru%d == "y" .and. cs_db%num_tot > 0) then` | `"HRU_PATH                  hru_path_day.txt"` |
| 22 | data | `if (pco%wb_hru%d == "y" .and. cs_db%num_tot > 0) then > if (pco%csvout == "y") then` | `"HRU_PATH                  hru_path_day.csv"` |
| 30 | data | `if (pco%wb_hru%m == "y" .and. cs_db%num_tot > 0) then` | `"HRU_PATH                  hru_path_mon.txt"` |
| 37 | data | `if (pco%wb_hru%m == "y" .and. cs_db%num_tot > 0) then > if (pco%csvout == "y") then` | `"HRU_PATH                  hru_path_mon.csv"` |
| 45 | data | `if (pco%wb_hru%y == "y" .and. cs_db%num_tot > 0) then` | `"HRU_PATH                  hru_path_yr.txt"` |
| 52 | data | `if (pco%wb_hru%y == "y" .and. cs_db%num_tot > 0) then > if (pco%csvout == "y") then` | `"HRU_PATH                  hru_path_yr.csv"` |
| 60 | data | `if (pco%wb_hru%a == "y" .and. cs_db%num_tot > 0) then` | `"HRU_PATH                  hru_path_aa.txt"` |
| 67 | data | `if (pco%wb_hru%a == "y" .and. cs_db%num_tot > 0) then > if (pco%csvout == "y") then` | `"HRU_PATH                  hru_path_aa.csv"` |


- Procedure: `header_pest`
- Writer: `header_pest.f90`
- Match: source_output
- Resolved default filename(s): `files_out.out`

| Line | Role | Condition | Fields written |
| --- | --- | --- | --- |
| 20 | data | `if (sp_ob%hru > 0) then > if (pco%pest%d == "y" .and. cs_db%num_tot > 0) then` | `"HRU_PEST                  hru_pest_day.txt"` |
| 27 | data | `if (sp_ob%hru > 0) then > if (pco%pest%d == "y" .and. cs_db%num_tot > 0) then > if (pco%csvout == "y") then` | `"HRU_PEST                  hru_pest_day.csv"` |
| 35 | data | `if (sp_ob%hru > 0) then > if (pco%pest%m == "y" .and. cs_db%num_tot > 0 ) then` | `"HRU_PEST                  hru_pest_mon.txt"` |
| 42 | data | `if (sp_ob%hru > 0) then > if (pco%pest%m == "y" .and. cs_db%num_tot > 0 ) then > if (pco%csvout == "y") then` | `"HRU_PEST                  hru_pest_mon.csv"` |
| 50 | data | `if (sp_ob%hru > 0) then > if (pco%pest%y == "y" .and. cs_db%num_tot > 0) then` | `"HRU_PEST                  hru_pest_yr.txt"` |
| 57 | data | `if (sp_ob%hru > 0) then > if (pco%pest%y == "y" .and. cs_db%num_tot > 0) then > if (pco%csvout == "y") then` | `"HRU_PEST                  hru_pest_yr.csv"` |
| 65 | data | `if (sp_ob%hru > 0) then > if (pco%pest%a == "y" .and. cs_db%num_tot > 0) then` | `"HRU_PEST                  hru_pest_aa.txt"` |
| 72 | data | `if (sp_ob%hru > 0) then > if (pco%pest%a == "y" .and. cs_db%num_tot > 0) then > if (pco%csvout == "y") then` | `"HRU_PEST                  hru_pest_aa.csv"` |
| 84 | data | `if (sp_ob%chandeg > 0) then > if (pco%pest%d == "y" .and. cs_db%num_tot > 0) then` | `"CHANNEL_PEST              channel_pest_day.txt"` |
| 91 | data | `if (sp_ob%chandeg > 0) then > if (pco%pest%d == "y" .and. cs_db%num_tot > 0) then > if (pco%csvout == "y") then` | `"CHANNEL_PEST              channel_pest_day.csv"` |
| 99 | data | `if (sp_ob%chandeg > 0) then > if (pco%pest%m == "y" .and. cs_db%num_tot > 0 ) then` | `"CHANNEL_PEST              channel_pest_mon.txt"` |
| 106 | data | `if (sp_ob%chandeg > 0) then > if (pco%pest%m == "y" .and. cs_db%num_tot > 0 ) then > if (pco%csvout == "y") then` | `"CHANNEL_PEST              channel_pest_mon.csv"` |
| 114 | data | `if (sp_ob%chandeg > 0) then > if (pco%pest%y == "y" .and. cs_db%num_tot > 0) then` | `"CHANNEL_PEST              channel_pest_yr.txt"` |
| 121 | data | `if (sp_ob%chandeg > 0) then > if (pco%pest%y == "y" .and. cs_db%num_tot > 0) then > if (pco%csvout == "y") then` | `"CHANNEL_PEST              channel_pest_yr.csv"` |
| 129 | data | `if (sp_ob%chandeg > 0) then > if (pco%pest%a == "y" .and. cs_db%num_tot > 0) then` | `"CHANNEL_PEST              channel_pest_aa.txt"` |
| 136 | data | `if (sp_ob%chandeg > 0) then > if (pco%pest%a == "y" .and. cs_db%num_tot > 0) then > if (pco%csvout == "y") then` | `"CHANNEL_PEST              channel_pest_aa.csv"` |
| 148 | data | `if (sp_ob%res > 0) then > if (pco%pest%d == "y" .and. cs_db%num_tot > 0) then` | `"RESERVOIR_PEST            reservoir_pest_day.txt"` |
| 155 | data | `if (sp_ob%res > 0) then > if (pco%pest%d == "y" .and. cs_db%num_tot > 0) then > if (pco%csvout == "y") then` | `"RESERVOIR_PEST            reservoir_pest_day.csv"` |
| 163 | data | `if (sp_ob%res > 0) then > if (pco%pest%m == "y" .and. cs_db%num_tot > 0 ) then` | `"RESERVOIR_PEST            reservoir_pest_mon.txt"` |
| 170 | data | `if (sp_ob%res > 0) then > if (pco%pest%m == "y" .and. cs_db%num_tot > 0 ) then > if (pco%csvout == "y") then` | `"RESERVOIR_PEST            reservoir_pest_mon.csv"` |
| 178 | data | `if (sp_ob%res > 0) then > if (pco%pest%y == "y" .and. cs_db%num_tot > 0) then` | `"RESERVOIR_PEST            reservoir_pest_yr.txt"` |
| 185 | data | `if (sp_ob%res > 0) then > if (pco%pest%y == "y" .and. cs_db%num_tot > 0) then > if (pco%csvout == "y") then` | `"RESERVOIR_PEST            reservoir_pest_yr.csv"` |
| 193 | data | `if (sp_ob%res > 0) then > if (pco%pest%a == "y" .and. cs_db%num_tot > 0) then` | `"RESERVOIR_PEST            reservoir_pest_aa.txt"` |
| 200 | data | `if (sp_ob%res > 0) then > if (pco%pest%a == "y" .and. cs_db%num_tot > 0) then > if (pco%csvout == "y") then` | `"RESERVOIR_PEST            reservoir_pest_aa.csv"` |
| 212 | data | `if (sp_ob%aqu > 0) then > if (pco%pest%d == "y" .and. cs_db%num_tot > 0) then` | `"BASIN_AQUIFER_PEST        basin_aqu_pest_day.txt"` |
| 219 | data | `if (sp_ob%aqu > 0) then > if (pco%pest%d == "y" .and. cs_db%num_tot > 0) then > if (pco%csvout == "y") then` | `"BASIN_AQUIFER_PEST        basin_aqu_pest_day.csv"` |
| 227 | data | `if (sp_ob%aqu > 0) then > if (pco%pest%m == "y" .and. cs_db%num_tot > 0 ) then` | `"BASIN_AQUIFER_PEST        basin_aqu_pest_mon.txt"` |
| 234 | data | `if (sp_ob%aqu > 0) then > if (pco%pest%m == "y" .and. cs_db%num_tot > 0 ) then > if (pco%csvout == "y") then` | `"BASIN_AQUIFER_PEST        basin_aqu_pest_mon.csv"` |
| 242 | data | `if (sp_ob%aqu > 0) then > if (pco%pest%y == "y" .and. cs_db%num_tot > 0) then` | `"BASIN_AQUIFER_PEST        basin_aqu_pest_yr.txt"` |
| 249 | data | `if (sp_ob%aqu > 0) then > if (pco%pest%y == "y" .and. cs_db%num_tot > 0) then > if (pco%csvout == "y") then` | `"BASIN_AQUIFER_PEST        basin_aqu_pest_yr.csv"` |
| 257 | data | `if (sp_ob%aqu > 0) then > if (pco%pest%a == "y" .and. cs_db%num_tot > 0) then` | `"BASIN_AQUIFER_PEST        basin_aqu_pest_aa.txt"` |
| 264 | data | `if (sp_ob%aqu > 0) then > if (pco%pest%a == "y" .and. cs_db%num_tot > 0) then > if (pco%csvout == "y") then` | `"BASIN_AQUIFER_PEST        basin_aqu_pest_aa.csv"` |
| 276 | data | `if (sp_ob%aqu > 0) then > if (pco%pest%d == "y" .and. cs_db%num_tot > 0) then` | `"AQUIFER_PEST              aquifer_pest_day.txt"` |
| 283 | data | `if (sp_ob%aqu > 0) then > if (pco%pest%d == "y" .and. cs_db%num_tot > 0) then > if (pco%csvout == "y") then` | `"AQUIFER_PEST              aquifer_pest_day.csv"` |
| 291 | data | `if (sp_ob%aqu > 0) then > if (pco%pest%m == "y" .and. cs_db%num_tot > 0 ) then` | `"AQUIFER_PEST              aquifer_pest_mon.txt"` |
| 298 | data | `if (sp_ob%aqu > 0) then > if (pco%pest%m == "y" .and. cs_db%num_tot > 0 ) then > if (pco%csvout == "y") then` | `"AQUIFER_PEST              aquifer_pest_mon.csv"` |
| 306 | data | `if (sp_ob%aqu > 0) then > if (pco%pest%y == "y" .and. cs_db%num_tot > 0) then` | `"AQUIFER_PEST              aquifer_pest_yr.txt"` |
| 313 | data | `if (sp_ob%aqu > 0) then > if (pco%pest%y == "y" .and. cs_db%num_tot > 0) then > if (pco%csvout == "y") then` | `"AQUIFER_PEST              aquifer_pest_yr.csv"` |
| 321 | data | `if (sp_ob%aqu > 0) then > if (pco%pest%a == "y" .and. cs_db%num_tot > 0) then` | `"AQUIFER_PEST              aquifer_pest_aa.txt"` |
| 328 | data | `if (sp_ob%aqu > 0) then > if (pco%pest%a == "y" .and. cs_db%num_tot > 0) then > if (pco%csvout == "y") then` | `"AQUIFER_PEST              aquifer_pest_aa.csv"` |
| 340 | data | `if (sp_ob%chandeg > 0) then > if (pco%pest%d == "y" .and. cs_db%num_tot > 0) then` | `"BASIN_CH_PEST             basin_ch_pest_day.txt"` |
| 347 | data | `if (sp_ob%chandeg > 0) then > if (pco%pest%d == "y" .and. cs_db%num_tot > 0) then > if (pco%csvout == "y") then` | `"BASIN_CH_PEST             reservoir_pest_day.csv"` |
| 355 | data | `if (sp_ob%chandeg > 0) then > if (pco%pest%m == "y" .and. cs_db%num_tot > 0 ) then` | `"BASIN_CH_PEST             basin_ch_pest_mon.txt"` |
| 362 | data | `if (sp_ob%chandeg > 0) then > if (pco%pest%m == "y" .and. cs_db%num_tot > 0 ) then > if (pco%csvout == "y") then` | `"BASIN_CH_PEST             basin_ch_pest_mon.csv"` |
| 370 | data | `if (sp_ob%chandeg > 0) then > if (pco%pest%y == "y" .and. cs_db%num_tot > 0) then` | `"BASIN_CH_PEST             basin_ch_pest_yr.txt"` |
| 377 | data | `if (sp_ob%chandeg > 0) then > if (pco%pest%y == "y" .and. cs_db%num_tot > 0) then > if (pco%csvout == "y") then` | `"BASIN_CH_PEST             basin_ch_pest_yr.csv"` |
| 385 | data | `if (sp_ob%chandeg > 0) then > if (pco%pest%a == "y" .and. cs_db%num_tot > 0) then` | `"BASIN_CH_PEST             basin_ch_pest_aa.txt"` |
| 392 | data | `if (sp_ob%chandeg > 0) then > if (pco%pest%a == "y" .and. cs_db%num_tot > 0) then > if (pco%csvout == "y") then` | `"BASIN_CH_PEST             basin_ch_pest_aa.csv"` |
| 404 | data | `if (sp_ob%res > 0) then > if (pco%pest%d == "y" .and. cs_db%num_tot > 0) then` | `"BASIN_RES_PEST            basin_res_pest_day.txt"` |
| 411 | data | `if (sp_ob%res > 0) then > if (pco%pest%d == "y" .and. cs_db%num_tot > 0) then > if (pco%csvout == "y") then` | `"BASIN_RES_PEST          reservoir_pest_day.csv"` |
| 419 | data | `if (sp_ob%res > 0) then > if (pco%pest%m == "y" .and. cs_db%num_tot > 0 ) then` | `"BASIN_RES_PEST            basin_res_pest_mon.txt"` |
| 426 | data | `if (sp_ob%res > 0) then > if (pco%pest%m == "y" .and. cs_db%num_tot > 0 ) then > if (pco%csvout == "y") then` | `"BASIN_RES_PEST            basin_res_pest_mon.csv"` |
| 434 | data | `if (sp_ob%res > 0) then > if (pco%pest%y == "y" .and. cs_db%num_tot > 0) then` | `"BASIN_RES_PEST            basin_res_pest_yr.txt"` |
| 441 | data | `if (sp_ob%res > 0) then > if (pco%pest%y == "y" .and. cs_db%num_tot > 0) then > if (pco%csvout == "y") then` | `"BASIN_RES_PEST            basin_res_pest_yr.csv"` |
| 449 | data | `if (sp_ob%res > 0) then > if (pco%pest%a == "y" .and. cs_db%num_tot > 0) then` | `"BASIN_RES_PEST            basin_res_pest_aa.txt"` |
| 456 | data | `if (sp_ob%res > 0) then > if (pco%pest%a == "y" .and. cs_db%num_tot > 0) then > if (pco%csvout == "y") then` | `"BASIN_RES_PEST            basin_res_pest_aa.csv"` |
| 468 | data | `if (sp_ob%hru > 0) then > if (pco%pest%d == "y" .and. cs_db%num_tot > 0) then` | `"BASIN_LS_PEST             basin_ls_pest_day.txt"` |
| 475 | data | `if (sp_ob%hru > 0) then > if (pco%pest%d == "y" .and. cs_db%num_tot > 0) then > if (pco%csvout == "y") then` | `"BASIN_LS_PEST             basin_ls_pest_day.csv"` |
| 483 | data | `if (sp_ob%hru > 0) then > if (pco%pest%m == "y" .and. cs_db%num_tot > 0 ) then` | `"BASIN_LS_PEST             basin_ls_pest_mon.txt"` |
| 490 | data | `if (sp_ob%hru > 0) then > if (pco%pest%m == "y" .and. cs_db%num_tot > 0 ) then > if (pco%csvout == "y") then` | `"BASIN_LS_PEST             basin_ls_pest_mon.csv"` |
| 498 | data | `if (sp_ob%hru > 0) then > if (pco%pest%y == "y" .and. cs_db%num_tot > 0) then` | `"BASIN_LS_PEST             basin_ls_pest_yr.txt"` |
| 505 | data | `if (sp_ob%hru > 0) then > if (pco%pest%y == "y" .and. cs_db%num_tot > 0) then > if (pco%csvout == "y") then` | `"BASIN_LS_PEST             basin_ls_pest_yr.csv"` |
| 513 | data | `if (sp_ob%hru > 0) then > if (pco%pest%a == "y" .and. cs_db%num_tot > 0) then` | `"BASIN_LS_PEST             basin_ls_pest_aa.txt"` |
| 520 | data | `if (sp_ob%hru > 0) then > if (pco%pest%a == "y" .and. cs_db%num_tot > 0) then > if (pco%csvout == "y") then` | `"BASIN_LS_PEST             basin_ls_pest_aa.csv"` |


- Procedure: `header_reservoir`
- Writer: `header_reservoir.f90`
- Match: source_output
- Resolved default filename(s): `files_out.out`

| Line | Role | Condition | Fields written |
| --- | --- | --- | --- |
| 17 | data | `if (pco%res%d == "y" .and. sp_ob%res > 0 ) then` | `"RES                       reservoir_day.txt"` |
| 25 | data | `if (pco%res%d == "y" .and. sp_ob%res > 0 ) then > if (pco%csvout == "y") then` | `"RES                       reservoir_day.csv"` |
| 32 | data | `if (pco%res%m == "y" .and. sp_ob%res > 0 ) then` | `"RES                       reservoir_mon.txt"` |
| 47 | data | `if (pco%res%y == "y" .and. sp_ob%res > 0 ) then` | `"RES                       reservoir_yr.txt"` |
| 55 | data | `if (pco%res%y == "y" .and. sp_ob%res > 0 ) then > if (pco%csvout == "y") then` | `"RES                       reservoir_yr.csv"` |
| 64 | data | `if (pco%res%a == "y" .and. sp_ob%res > 0) then` | `"RES                       reservoir_aa.txt"` |
| 70 | data | `if (pco%res%a == "y" .and. sp_ob%res > 0) then > if (pco%csvout == "y") then` | `"RES                       reservoir_aa.csv"` |


- Procedure: `header_sd_channel`
- Writer: `header_sd_channel.f90`
- Match: source_output
- Resolved default filename(s): `files_out.out`

| Line | Role | Condition | Fields written |
| --- | --- | --- | --- |
| 19 | data | `if (sp_ob%chandeg > 0) then > if (pco%sd_chan%d == "y") then > if (time%step > 1) then` | `"SWAT-DEG_CHANNEL         channel_sd_subday.txt"` |
| 25 | data | `if (sp_ob%chandeg > 0) then > if (pco%sd_chan%d == "y") then > if (time%step > 1) then > if (pco%csvout == "y") then` | `"SWAT-DEG_CHANNEL          channel_sd_subday.csv"` |
| 33 | data | `if (sp_ob%chandeg > 0) then > if (pco%sd_chan%d == "y") then` | `"SWAT-DEG_CHANNEL          channel_sd_day.txt"` |
| 45 | data | `if (sp_ob%chandeg > 0) then > if (pco%sd_chan%d == "y") then > if (pco%csvout == "y") then` | `"SWAT-DEG_CHANNEL          channel_sd_day.csv"` |
| 62 | data | `if (sp_ob%chandeg > 0) then > if (pco%sd_chan%m == "y") then` | `"SWAT-DEG_CHANNEL          channel_sd_mon.txt"` |
| 75 | data | `if (sp_ob%chandeg > 0) then > if (pco%sd_chan%m == "y") then > if (pco%csvout == "y") then` | `"SWAT-DEG_CHANNEL          channel_sd_mon.csv"` |
| 92 | data | `if (sp_ob%chandeg > 0) then > if (pco%sd_chan%y == "y") then` | `"SWAT-DEG_CHANNEL          channel_sd_yr.txt"` |
| 105 | data | `if (sp_ob%chandeg > 0) then > if (pco%sd_chan%y == "y") then > if (pco%csvout == "y") then` | `"SWAT-DEG_CHANNEL          channel_sd_yr.csv"` |
| 122 | data | `if (sp_ob%chandeg > 0) then > if (pco%sd_chan%a == "y") then` | `"SWAT-DEG_CHANNEL          channel_sd_aa.txt"` |
| 135 | data | `if (sp_ob%chandeg > 0) then > if (pco%sd_chan%a == "y") then > if (pco%csvout == "y") then` | `"SWAT-DEG_CHANNEL          channel_sd_aa.csv"` |
| 154 | data | `if (sp_ob%chandeg > 0) then > if (pco%sd_chan%d == "y") then` | `"SWAT-DEG_CHANNEL_MORPH    channel_sdmorph_day.txt"` |
| 160 | data | `if (sp_ob%chandeg > 0) then > if (pco%sd_chan%d == "y") then > if (pco%csvout == "y") then` | `"SWAT-DEG_CHANNEL_MORPH    channel_sdmorph_day.csv"` |
| 171 | data | `if (sp_ob%chandeg > 0) then > if (pco%sd_chan%m == "y") then` | `"SWAT-DEG_CHANNEL_MORPH    channel_sdmorph_mon.txt"` |
| 177 | data | `if (sp_ob%chandeg > 0) then > if (pco%sd_chan%m == "y") then > if (pco%csvout == "y") then` | `"SWAT-DEG_CHANNEL_MORPH    channel_sdmorph_mon.csv"` |
| 188 | data | `if (sp_ob%chandeg > 0) then > if (pco%sd_chan%y == "y") then` | `"SWAT-DEG_CHANNEL_MORPH    channel_sdmorph_yr.txt"` |
| 194 | data | `if (sp_ob%chandeg > 0) then > if (pco%sd_chan%y == "y") then > if (pco%csvout == "y") then` | `"SWAT-DEG_CHANNEL_MORPH    channel_sdmorph_yr.csv"` |
| 205 | data | `if (sp_ob%chandeg > 0) then > if (pco%sd_chan%a == "y") then` | `"SWAT-DEG_CHANNEL_MORPH    channel_sdmorph_aa.txt"` |
| 211 | data | `if (sp_ob%chandeg > 0) then > if (pco%sd_chan%a == "y") then > if (pco%csvout == "y") then` | `"SWAT-DEG_CHANNEL_MORPH    channel_sdmorph_aa.csv"` |
| 223 | data | `if (pco%sd_chan%d == "y") then` | `"SWAT_DEG_CHAN_BUD         sd_chanbud_day.txt"` |
| 229 | data | `if (pco%sd_chan%d == "y") then > if (pco%csvout == "y") then` | `"SWAT_DEG_CHAN_BUD         sd_chanbud_day.csv"` |
| 238 | data | `if (pco%sd_chan%m == "y") then` | `"SWAT_DEG_CHAN_BUD         sd_chanbud_mon.txt"` |
| 244 | data | `if (pco%sd_chan%m == "y") then > if (pco%csvout == "y") then` | `"SWAT_DEG_CHAN_BUD         sd_chanbud_mon.csv"` |
| 253 | data | `if (pco%sd_chan%y == "y") then` | `"SWAT_DEG_CHAN_BUD         sd_chanbud_yr.txt"` |
| 259 | data | `if (pco%sd_chan%y == "y") then > if (pco%csvout == "y") then` | `"SWAT_DEG_CHAN_BUD         sd_chanbud_yr.csv"` |
| 268 | data | `if (pco%sd_chan%a == "y") then` | `"SWAT_DEG_CHAN_BUD         sd_chanbud_aa.txt"` |
| 274 | data | `if (pco%sd_chan%a == "y") then > if (pco%csvout == "y") then` | `"SWAT_DEG_CHAN_BUD         sd_chanbud_aa.csv"` |


- Procedure: `header_snutc`
- Writer: `header_snutc.f90`
- Match: source_output
- Resolved default filename(s): `files_out.out`

| Line | Role | Condition | Fields written |
| --- | --- | --- | --- |
| 13 | data | `if (sp_ob%hru > 0) then` | `"HRU_ORGC                  hru_orgc.txt"` |


- Procedure: `header_water_allocation`
- Writer: `header_water_allocation.f90`
- Match: source_output
- Resolved default filename(s): `files_out.out`

| Line | Role | Condition | Fields written |
| --- | --- | --- | --- |
| 17 | data | `if (db_mx%wallo_db > 0) then > if (pco%water_allo%d == "y") then` | `"WATER_ALLOCATION          water_allo_day.txt"` |
| 23 | data | `if (db_mx%wallo_db > 0) then > if (pco%water_allo%d == "y") then > if (pco%csvout == "y") then` | `"WATER_ALLOCATION          water_allo_day.csv"` |
| 34 | data | `if (db_mx%wallo_db > 0) then > if (pco%water_allo%m == "y") then` | `"WATER_ALLOCATION          water_allo_mon.txt"` |
| 40 | data | `if (db_mx%wallo_db > 0) then > if (pco%water_allo%m == "y") then > if (pco%csvout == "y") then` | `"WATER_ALLOCATION          water_allo_mon.csv"` |
| 51 | data | `if (db_mx%wallo_db > 0) then > if (pco%water_allo%y == "y") then` | `"WATER_ALLOCATION          water_allo_yr.txt"` |
| 57 | data | `if (db_mx%wallo_db > 0) then > if (pco%water_allo%y == "y") then > if (pco%csvout == "y") then` | `"WATER_ALLOCATION          water_allo_yr.csv"` |
| 68 | data | `if (db_mx%wallo_db > 0) then > if (pco%water_allo%a == "y") then` | `"WATER_ALLOCATION          water_allo_aa.txt"` |
| 74 | data | `if (db_mx%wallo_db > 0) then > if (pco%water_allo%a == "y") then > if (pco%csvout == "y") then` | `"WATER_ALLOCATION          water_allo_aa.csv"` |


- Procedure: `header_wetland`
- Writer: `header_wetland.f90`
- Match: source_output
- Resolved default filename(s): `files_out.out`

| Line | Role | Condition | Fields written |
| --- | --- | --- | --- |
| 14 | data | `if (pco%res%d == "y") then` | `"RES_WET                   wetland_day.txt"` |
| 22 | data | `if (pco%res%d == "y") then > if (pco%csvout == "y") then` | `"RES_WET                   wetland_day.csv"` |
| 30 | data | `if (pco%res%m == "y") then` | `"RES_WET                   wetland_mon.txt"` |
| 38 | data | `if (pco%res%m == "y") then > if (pco%csvout == "y") then` | `"RES_WET                   wetland_mon.csv"` |
| 46 | data | `if (pco%res%y == "y") then` | `"RES_WET                   wetland_yr.txt"` |
| 54 | data | `if (pco%res%y == "y") then > if (pco%csvout == "y") then` | `"RES_WET                   wetland_yr.csv"` |
| 65 | data | `if (pco%res%a == "y") then` | `"RES_WET                   wetland_aa.txt"` |
| 72 | data | `if (pco%res%a == "y") then > if (pco%csvout == "y") then` | `"RES_WET                   wetland_aa.csv"` |


- Procedure: `header_write`
- Writer: `header_write.f90`
- Match: source_output
- Resolved default filename(s): `files_out.out`

| Line | Role | Condition | Fields written |
| --- | --- | --- | --- |
| 19 | data | `if (pco%fdcout == "y") then` | `"FDC                       flow_duration_curve.out"` |
| 28 | data | `if (cal_soft == "y") then` | `"HRU_SOFT_CALIB_OUT        hru-out.cal"` |
| 64 | data | `if (pco%aqu_bsn%d == "y") then` | `"BASIN_AQUIFER             basin_aqu_day.txt"` |
| 70 | data | `if (pco%aqu_bsn%d == "y") then > if (pco%csvout == "y") then` | `"BASIN_AQUIFER             basin_aqu_day.csv"` |
| 79 | data | `if (pco%aqu_bsn%m == "y") then` | `"BASIN_AQUIFER             basin_aqu_mon.txt"` |
| 85 | data | `if (pco%aqu_bsn%m == "y") then > if (pco%csvout == "y") then` | `"BASIN_AQUIFER             basin_aqu_mon.csv"` |
| 94 | data | `if (pco%aqu_bsn%y == "y") then` | `"BASIN_AQUIFER             basin_aqu_yr.txt"` |
| 100 | data | `if (pco%aqu_bsn%y == "y") then > if (pco%csvout == "y") then` | `"BASIN_AQUIFER             basin_aqu_yr.csv"` |
| 109 | data | `if (pco%aqu_bsn%a == "y") then` | `"BASIN_AQUIFER             basin_aqu_aa.txt"` |
| 115 | data | `if (pco%aqu_bsn%a == "y") then > if (pco%csvout == "y") then` | `"BASIN_AQUIFER             basin_aqu_aa.csv"` |
| 126 | data | `if (pco%res_bsn%d == "y") then` | `"BASIN_RESERVOIR           basin_res_day.txt"` |
| 132 | data | `if (pco%res_bsn%d == "y") then > if (pco%csvout == "y") then` | `"BASIN_RESERVOIR           basin_res_day.csv"` |
| 141 | data | `if (pco%res_bsn%m == "y") then` | `"BASIN_RESERVOIR           basin_res_mon.txt"` |
| 147 | data | `if (pco%res_bsn%m == "y") then > if (pco%csvout == "y") then` | `"BASIN_RESERVOIR           basin_res_mon.csv"` |
| 156 | data | `if (pco%res_bsn%y == "y") then` | `"BASIN_RESERVOIR           basin_res_yr.txt"` |
| 162 | data | `if (pco%res_bsn%y == "y") then > if (pco%csvout == "y") then` | `"BASIN_RESERVOIR           basin_res_yr.csv"` |
| 171 | data | `if (pco%res_bsn%a == "y") then` | `"BASIN_RESERVOIR           basin_res_aa.txt"` |
| 177 | data | `if (pco%res_bsn%a == "y") then > if (pco%csvout == "y") then` | `"BASIN_RESERVOIR           basin_res_aa.csv"` |
| 188 | data | `if (pco%recall%d == "y") then` | `"RECALL                    recall_day.txt"` |
| 194 | data | `if (pco%recall%d == "y") then > if (pco%csvout == "y") then` | `"RECALL                    recall_day.csv"` |
| 203 | data | `if (pco%recall%m == "y") then` | `"RECALL                    recall_mon.txt"` |
| 209 | data | `if (pco%recall%m == "y") then > if (pco%csvout == "y") then` | `"RECALL                    recall_mon.csv"` |
| 218 | data | `if (pco%recall%y == "y") then` | `"RECALL                    recall_yr.txt"` |
| 224 | data | `if (pco%recall%y == "y") then > if (pco%csvout == "y") then` | `"RECALL                    recall_yr.csv"` |
| 233 | data | `if (pco%recall%a == "y") then` | `"RECALL_AA                 recall_aa.txt"` |
| 239 | data | `if (pco%recall%a == "y") then > if (pco%csvout == "y") then` | `"RECALL                    recall_aa.csv"` |
| 251 | data | `if (pco%chan_bsn%d == "y") then` | `"BASIN_CHANNEL             basin_cha_day.txt"` |
| 257 | data | `if (pco%chan_bsn%d == "y") then > if (pco%csvout == "y") then` | `"BASIN_CHANNEL             basin_cha_day.txt"` |
| 266 | data | `if (pco%chan_bsn%m == "y") then` | `"BASIN_CHANNEL             basin_cha_mon.txt"` |
| 272 | data | `if (pco%chan_bsn%m == "y") then > if (pco%csvout == "y") then` | `"BASIN_CHANNEL             basin_cha_mon.txt"` |
| 281 | data | `if (pco%chan_bsn%y == "y") then` | `"BASIN_CHANNEL             basin_cha_yr.txt"` |
| 287 | data | `if (pco%chan_bsn%y == "y") then > if (pco%csvout == "y") then` | `"BASIN_CHANNEL             basin_cha_yr.csv"` |
| 296 | data | `if (pco%chan_bsn%a == "y") then` | `"BASIN_CHANNEL             basin_cha_aa.txt"` |
| 302 | data | `if (pco%chan_bsn%a == "y") then > if (pco%csvout == "y") then` | `"BASIN_CHANNEL             basin_cha_aa.csv"` |
| 313 | data | `if (pco%sd_chan_bsn%d == "y") then` | `"BASIN_SWAT_DEG_CHANNEL    basin_sd_cha_day.txt"` |
| 319 | data | `if (pco%sd_chan_bsn%d == "y") then > if (pco%csvout == "y") then` | `"BASIN_SWAT_DEG_CHANNEL    basin_sd_cha_day.csv"` |
| 328 | data | `if (pco%sd_chan_bsn%m == "y") then` | `"BASIN_SWAT_DEG_CHANNEL    basin_sd_cha_mon.txt"` |
| 334 | data | `if (pco%sd_chan_bsn%m == "y") then > if (pco%csvout == "y") then` | `"BASIN_SWAT_DEG_CHANNEL    basin_sd_cha_mon.csv"` |
| 343 | data | `if (pco%sd_chan_bsn%y == "y") then` | `"BASIN_SWAT_DEG_CHANNEL    basin_sd_cha_yr.txt"` |
| 349 | data | `if (pco%sd_chan_bsn%y == "y") then > if (pco%csvout == "y") then` | `"BASIN_SWAT_DEG_CHANNEL    basin_sd_cha_yr.csv"` |
| 358 | data | `if (pco%sd_chan_bsn%a == "y") then` | `"BASIN_SWAT_DEG_CHANNEL    basin_sd_cha_aa.txt"` |
| 364 | data | `if (pco%sd_chan_bsn%a == "y") then > if (pco%csvout == "y") then` | `"BASIN_SWAT_DEG_CHANNEL    basin_sd_cha_aa.csv"` |
| 376 | data | `if (pco%sd_chan_bsn%d == "y") then` | `"BASIN_SWAT_DEG_CHAN_MORPH basin_sd_chamorph_day.txt"` |
| 382 | data | `if (pco%sd_chan_bsn%d == "y") then > if (pco%csvout == "y") then` | `"BASIN_SWAT_DEG_CHAN_MORPH basin_sd_chamorph_day.csv"` |
| 391 | data | `if (pco%sd_chan_bsn%m == "y") then` | `"BASIN_SWAT_DEG_CHAN_MORPH basin_sd_chamorph_mon.txt"` |
| 397 | data | `if (pco%sd_chan_bsn%m == "y") then > if (pco%csvout == "y") then` | `"BASIN_SWAT_DEG_CHAN_MORPH basin_sd_chamorph_mon.csv"` |
| 406 | data | `if (pco%sd_chan_bsn%y == "y") then` | `"BASIN_SWAT_DEG_CHAN_MORPH basin_sd_chamorph_yr.txt"` |
| 412 | data | `if (pco%sd_chan_bsn%y == "y") then > if (pco%csvout == "y") then` | `"BASIN_SWAT_DEG_CHAN_MORPH basin_sd_chamorph_yr.csv"` |
| 421 | data | `if (pco%sd_chan_bsn%a == "y") then` | `"BASIN_SWAT_DEG_CHAN_MORPH basin_sd_chamorph_aa.txt"` |
| 427 | data | `if (pco%sd_chan_bsn%a == "y") then > if (pco%csvout == "y") then` | `"BASIN_SWAT_DEG_CHAN_MORPH basin_sd_chamorph_aa.csv"` |
| 438 | data | `if (pco%sd_chan_bsn%d == "y") then` | `"BASIN_SWAT_DEG_CHAN_BUD   basin_sd_chanbud_day.txt"` |
| 444 | data | `if (pco%sd_chan_bsn%d == "y") then > if (pco%csvout == "y") then` | `"BASIN_SWAT_DEG_CHAN_BUD   basin_sd_chanbud_day.csv"` |
| 453 | data | `if (pco%sd_chan_bsn%m == "y") then` | `"BASIN_SWAT_DEG_CHAN_BUD   basin_sd_chanbud_mon.txt"` |
| 459 | data | `if (pco%sd_chan_bsn%m == "y") then > if (pco%csvout == "y") then` | `"BASIN_SWAT_DEG_CHAN_BUD   basin_sd_chanbud_mon.csv"` |
| 468 | data | `if (pco%sd_chan_bsn%y == "y") then` | `"BASIN_SWAT_DEG_CHAN_BUD   basin_sd_chanbud_yr.txt"` |
| 474 | data | `if (pco%sd_chan_bsn%y == "y") then > if (pco%csvout == "y") then` | `"BASIN_SWAT_DEG_CHAN_BUD   basin_sd_chanbud_yr.csv"` |
| 483 | data | `if (pco%sd_chan_bsn%a == "y") then` | `"BASIN_SWAT_DEG_CHAN_BUD   basin_sd_chanbud_aa.txt"` |
| 489 | data | `if (pco%sd_chan_bsn%a == "y") then > if (pco%csvout == "y") then` | `"BASIN_SWAT_DEG_CHAN_BUD   basin_sd_chanbud_aa.csv"` |
| 501 | data | `if (pco%recall_bsn%d == "y") then` | `"BASIN_RECALL              basin_psc_day.txt"` |
| 507 | data | `if (pco%recall_bsn%d == "y") then > if (pco%csvout == "y") then` | `"BASIN_RECALL              basin_psc_day.csv"` |
| 516 | data | `if (pco%recall_bsn%m == "y") then` | `"BASIN_RECALL              basin_psc_mon.txt"` |
| 522 | data | `if (pco%recall_bsn%m == "y") then > if (pco%csvout == "y") then` | `"BASIN_RECALL              basin_psc_mon.csv"` |
| 531 | data | `if (pco%recall_bsn%y == "y") then` | `"BASIN_RECALL              basin_psc_yr.txt"` |
| 537 | data | `if (pco%recall_bsn%y == "y") then > if (pco%csvout == "y") then` | `"BASIN_RECALL              basin_psc_yr.csv"` |
| 546 | data | `if (pco%recall_bsn%a == "y") then` | `"BASIN_RECALL_AA           basin_psc_aa.txt"` |
| 552 | data | `if (pco%recall_bsn%a == "y") then > if (pco%csvout == "y") then` | `"BASIN_RECALL_AA           basin_psc_aa.csv"` |
| 564 | data | `if (pco%ru%d == "y") then` | `"ROUTING_UNITS             ru_day.txt"` |
| 570 | data | `if (pco%ru%d == "y") then > if (pco%csvout == "y") then` | `"ROUTING_UNITS             ru_day.csv"` |
| 579 | data | `if (pco%ru%m == "y") then` | `"ROUTING_UNITS             ru_mon.txt"` |
| 585 | data | `if (pco%ru%m == "y") then > if (pco%csvout == "y") then` | `"ROUTING_UNITS             ru_mon.csv"` |
| 594 | data | `if (pco%ru%y == "y") then` | `"ROUTING_UNITS             ru_yr.txt"` |
| 600 | data | `if (pco%ru%y == "y") then > if (pco%csvout == "y") then` | `"ROUTING_UNITS             ru_yr.csv"` |
| 609 | data | `if (pco%ru%a == "y") then` | `"ROUTING_UNITS             ru_aa.txt"` |
| 615 | data | `if (pco%ru%a == "y") then > if (pco%csvout == "y") then` | `"ROUTING_UNITS             ru_aa.csv"` |


- Procedure: `header_yield`
- Writer: `header_yield.f90`
- Match: source_output
- Resolved default filename(s): `files_out.out`

| Line | Role | Condition | Fields written |
| --- | --- | --- | --- |
| 12 | data | `if (pco%mgtout == "y") then` | `"YLD                       yield.out"` |
| 15 | data | `if (pco%mgtout == "y") then > if (pco%csvout == "y") then` | `"YLD                       yield.csv"` |
| 25 | data | `if (sp_ob%hru > 0 .and. (pco%crop_yld == "y" .or. pco%crop_yld == "b")) then` | `"BASIN_CROP_YLD            basin_crop_yld_yr.txt"` |
| 29 | data | `if (sp_ob%hru > 0 .and. (pco%crop_yld == "y" .or. pco%crop_yld == "b")) then` | `"BASIN_CROP_YLD            basin_crop_yld_aa.txt"` |


- Procedure: `output_landscape_init`
- Writer: `output_landscape_init.f90`
- Match: source_output
- Resolved default filename(s): `files_out.out`

| Line | Role | Condition | Fields written |
| --- | --- | --- | --- |
| 41 | data | `if (sp_ob%hru > 0) then > if (pco%wb_hru%d == "y") then` | `"HRU                       hru_wb_day.txt"` |
| 48 | data | `if (sp_ob%hru > 0) then > if (pco%wb_hru%d == "y") then > if (pco%csvout == "y") then` | `"HRU                       hru_wb_day.csv"` |
| 58 | data | `if (sp_ob%hru > 0) then > if (pco%wb_hru%m == "y") then` | `"HRU                       hru_wb_mon.txt"` |
| 65 | data | `if (sp_ob%hru > 0) then > if (pco%wb_hru%m == "y") then > if (pco%csvout == "y") then` | `"HRU                       hru_wb_mon.csv"` |
| 75 | data | `if (sp_ob%hru > 0) then > if (pco%wb_hru%y == "y") then` | `"HRU                       hru_wb_yr.txt"` |
| 81 | data | `if (sp_ob%hru > 0) then > if (pco%wb_hru%y == "y") then > if (pco%csvout == "y") then` | `"HRU                       hru_wb_yr.csv"` |
| 91 | data | `if (sp_ob%hru > 0) then > if (pco%wb_hru%a == "y") then` | `"HRU                       hru_wb_aa.txt"` |
| 97 | data | `if (sp_ob%hru > 0) then > if (pco%wb_hru%a == "y") then > if (pco%csvout == "y") then` | `"HRU                       hru_wb_aa.csv"` |
| 107 | data | `if (sp_ob%hru > 0) then > if (pco%nb_hru%d == "y") then` | `"HRU                       hru_nb_day.txt"` |
| 113 | data | `if (sp_ob%hru > 0) then > if (pco%nb_hru%d == "y") then > if (pco%csvout == "y") then` | `"HRU                       hru_nb_day.csv"` |
| 123 | data | `if (sp_ob%hru > 0) then > if (pco%nb_hru%d == "y") then` | `"HRU                       hru_ncycle_day.txt"` |
| 129 | data | `if (sp_ob%hru > 0) then > if (pco%nb_hru%d == "y") then > if (pco%csvout == "y") then` | `"HRU                       hru_ncycle_day.csv"` |
| 138 | data | `if (sp_ob%hru > 0) then > if (pco%nb_hru%m == "y") then` | `"HRU                       hru_ncycle_mon.txt"` |
| 144 | data | `if (sp_ob%hru > 0) then > if (pco%nb_hru%m == "y") then > if (pco%csvout == "y") then` | `"HRU                       hru_ncycle_mon.csv"` |
| 153 | data | `if (sp_ob%hru > 0) then > if (pco%nb_hru%y == "y") then` | `"HRU                       hru_ncycle_yr.txt"` |
| 159 | data | `if (sp_ob%hru > 0) then > if (pco%nb_hru%y == "y") then > if (pco%csvout == "y") then` | `"HRU                       hru_ncycle_yr.csv"` |
| 168 | data | `if (sp_ob%hru > 0) then > if (pco%nb_hru%a == "y") then` | `"HRU                       hru_ncycle_aa.txt"` |
| 174 | data | `if (sp_ob%hru > 0) then > if (pco%nb_hru%a == "y") then > if (pco%csvout == "y") then` | `"HRU                       hru_ncycle_aa.csv"` |
| 184 | data | `if (sp_ob%hru > 0) then > if (pco%nb_hru%m == "y") then` | `"HRU                       hru_nb_mon.txt"` |
| 190 | data | `if (sp_ob%hru > 0) then > if (pco%nb_hru%m == "y") then > if (pco%csvout == "y") then` | `"HRU                       hru_nb_mon.csv"` |
| 199 | data | `if (sp_ob%hru > 0) then > if (pco%nb_hru%y == "y") then` | `"HRU                       hru_nb_yr.txt"` |
| 205 | data | `if (sp_ob%hru > 0) then > if (pco%nb_hru%y == "y") then > if (pco%csvout == "y") then` | `"HRU                       hru_nb_yr.csv"` |
| 214 | data | `if (sp_ob%hru > 0) then > if (pco%nb_hru%a == "y") then` | `"HRU                       hru_nb_aa.txt"` |
| 220 | data | `if (sp_ob%hru > 0) then > if (pco%nb_hru%a == "y") then > if (pco%csvout == "y") then` | `"HRU                       hru_nb_aa.csv"` |
| 230 | data | `if (sp_ob%hru > 0) then > if (pco%cb_gl_hru%d == "y") then` | `"HRU                       hru_carb_gl_day.txt"` |
| 236 | data | `if (sp_ob%hru > 0) then > if (pco%cb_gl_hru%d == "y") then > if (pco%csvout == "y") then` | `"HRU                       hru_carb_gl_day.csv"` |
| 245 | data | `if (sp_ob%hru > 0) then > if (pco%cb_gl_hru%m == "y") then` | `"HRU                       hru_carb_gl_mon.txt"` |
| 251 | data | `if (sp_ob%hru > 0) then > if (pco%cb_gl_hru%m == "y") then > if (pco%csvout == "y") then` | `"HRU                       hru_carb_gl_mon.csv"` |
| 260 | data | `if (sp_ob%hru > 0) then > if (pco%cb_gl_hru%y == "y") then` | `"HRU                       hru_carb_gl_yr.txt"` |
| 266 | data | `if (sp_ob%hru > 0) then > if (pco%cb_gl_hru%y == "y") then > if (pco%csvout == "y") then` | `"HRU                       hru_carb_gl_yr.csv"` |
| 275 | data | `if (sp_ob%hru > 0) then > if (pco%cb_gl_hru%a == "y") then` | `"HRU                       hru_carb_gl_aa.txt"` |
| 281 | data | `if (sp_ob%hru > 0) then > if (pco%cb_gl_hru%a == "y") then > if (pco%csvout == "y") then` | `"HRU                       hru_carb_gl_aa.csv"` |
| 293 | data | `if (sp_ob%hru > 0) then > if (pco%cb_trf_hru%d == "y") then` | `"HRU                       hru_scf_day.txt"` |
| 299 | data | `if (sp_ob%hru > 0) then > if (pco%cb_trf_hru%d == "y") then > if (pco%csvout == "y") then` | `"HRU                       hru_scf_day.csv"` |
| 308 | data | `if (sp_ob%hru > 0) then > if (pco%cb_trf_hru%m == "y") then` | `"HRU                       hru_scf_mon.txt"` |
| 314 | data | `if (sp_ob%hru > 0) then > if (pco%cb_trf_hru%m == "y") then > if (pco%csvout == "y") then` | `"HRU                       hru_scf_mon.csv"` |
| 323 | data | `if (sp_ob%hru > 0) then > if (pco%cb_trf_hru%y == "y") then` | `"HRU                       hru_scf_yr.txt"` |
| 329 | data | `if (sp_ob%hru > 0) then > if (pco%cb_trf_hru%y == "y") then > if (pco%csvout == "y") then` | `"HRU                       hru_scf_yr.csv"` |
| 338 | data | `if (sp_ob%hru > 0) then > if (pco%cb_trf_hru%a == "y") then` | `"HRU                       hru_scf_aa.txt"` |
| 344 | data | `if (sp_ob%hru > 0) then > if (pco%cb_trf_hru%a == "y") then > if (pco%csvout == "y") then` | `"HRU                       hru_scf_aa.csv"` |
| 435 | data | `if (sp_ob%hru > 0) then > if (pco%ls_hru%d == "y") then` | `"HRU                       hru_ls_day.txt"` |
| 441 | data | `if (sp_ob%hru > 0) then > if (pco%ls_hru%d == "y") then > if (pco%csvout == "y") then` | `"HRU                       hru_ls_day.csv"` |
| 453 | data | `if (sp_ob%hru > 0) then > if (pco%ls_hru%m == "y") then` | `"HRU                       hru_ls_mon.txt"` |
| 459 | data | `if (sp_ob%hru > 0) then > if (pco%ls_hru%m == "y") then > if (pco%csvout == "y") then` | `"HRU                       hru_ls_mon.csv"` |
| 468 | data | `if (sp_ob%hru > 0) then > if (pco%ls_hru%y == "y") then` | `"HRU                       hru_ls_yr.txt"` |
| 474 | data | `if (sp_ob%hru > 0) then > if (pco%ls_hru%y == "y") then > if (pco%csvout == "y") then` | `"HRU                       hru_ls_yr.csv"` |
| 483 | data | `if (sp_ob%hru > 0) then > if (pco%ls_hru%a == "y") then` | `"HRU                       hru_ls_aa.txt"` |
| 489 | data | `if (sp_ob%hru > 0) then > if (pco%ls_hru%a == "y") then > if (pco%csvout == "y") then` | `"HRU                       hru_ls_aa.csv"` |
| 499 | data | `if (sp_ob%hru > 0) then > if (pco%pw_hru%d == "y") then` | `"HRU                       hru_pw_day.txt"` |
| 505 | data | `if (sp_ob%hru > 0) then > if (pco%pw_hru%d == "y") then > if (pco%csvout == "y") then` | `"HRU                       hru_pw_day.csv"` |
| 514 | data | `if (sp_ob%hru > 0) then > if (pco%pw_hru%m == "y") then` | `"HRU                       hru_pw_mon.txt"` |
| 520 | data | `if (sp_ob%hru > 0) then > if (pco%pw_hru%m == "y") then > if (pco%csvout == "y") then` | `"HRU                       hru_pw_mon.csv"` |
| 529 | data | `if (sp_ob%hru > 0) then > if (pco%pw_hru%y == "y") then` | `"HRU                       hru_pw_yr.txt"` |
| 535 | data | `if (sp_ob%hru > 0) then > if (pco%pw_hru%y == "y") then > if (pco%csvout == "y") then` | `"HRU                       hru_pw_yr.csv"` |
| 544 | data | `if (sp_ob%hru > 0) then > if (pco%pw_hru%a == "y") then` | `"HRU                       hru_pw_aa.txt"` |
| 550 | data | `if (sp_ob%hru > 0) then > if (pco%pw_hru%a == "y") then > if (pco%csvout == "y") then` | `"HRU                       hru_pw_aa.csv"` |
| 563 | data | `if (sp_ob%hru_lte > 0) then > if (pco%wb_sd%d == "y") then` | `"SWAT-DEG                  hru-lte_wb_day.txt"` |
| 569 | data | `if (sp_ob%hru_lte > 0) then > if (pco%wb_sd%d == "y") then > if (pco%csvout == "y") then` | `"SWAT-DEG                  hru-lte_wb_day.csv"` |
| 579 | data | `if (sp_ob%hru_lte > 0) then > if (pco%wb_sd%m == "y") then` | `"SWAT-DEG                  hru-lte_wb_mon.txt"` |
| 585 | data | `if (sp_ob%hru_lte > 0) then > if (pco%wb_sd%m == "y") then > if (pco%csvout == "y") then` | `"SWAT-DEG                  hru-lte_wb_mon.csv"` |
| 596 | data | `if (sp_ob%hru_lte > 0) then > if (sp_ob%hru_lte > 0) then > if (pco%wb_sd%y == "y") then` | `"SWAT-DEG                  hru-lte_wb_yr.txt"` |
| 602 | data | `if (sp_ob%hru_lte > 0) then > if (sp_ob%hru_lte > 0) then > if (pco%wb_sd%y == "y") then > if (pco%csvout == "y") then` | `"SWAT-DEG                  hru-lte_wb_yr.csv"` |
| 613 | data | `if (sp_ob%hru_lte > 0) then > if (pco%wb_sd%a == "y") then` | `"SWAT-DEG                  hru-lte_wb_aa.txt"` |
| 619 | data | `if (sp_ob%hru_lte > 0) then > if (pco%wb_sd%a == "y") then > if (pco%csvout == "y") then` | `"SWAT-DEG                  hru-lte_wb_aa.csv"` |
| 641 | data | `if (sp_ob%hru_lte > 0) then > if (pco%ls_sd%d == "y") then` | `"SWAT-DEG                  hru-lte_ls_day.txt"` |
| 647 | data | `if (sp_ob%hru_lte > 0) then > if (pco%ls_sd%d == "y") then > if (pco%csvout == "y") then` | `"SWAT-DEG                  hru-lte_ls_day.csv"` |
| 656 | data | `if (sp_ob%hru_lte > 0) then > if (pco%ls_sd%m == "y") then` | `"SWAT-DEG                  hru-lte_ls_mon.txt"` |
| 662 | data | `if (sp_ob%hru_lte > 0) then > if (pco%ls_sd%m == "y") then > if (pco%csvout == "y") then` | `"SWAT-DEG                  hru-lte_ls_mon.csv"` |
| 671 | data | `if (sp_ob%hru_lte > 0) then > if (pco%ls_sd%y == "y") then` | `"SWAT-DEG                  hru-lte_ls_yr.txt"` |
| 677 | data | `if (sp_ob%hru_lte > 0) then > if (pco%ls_sd%y == "y") then > if (pco%csvout == "y") then` | `"SWAT-DEG                  hru-lte_ls_yr.csv"` |
| 686 | data | `if (sp_ob%hru_lte > 0) then > if (pco%ls_sd%a == "y") then` | `"SWAT-DEG                  hru-lte_ls_aa.txt"` |
| 692 | data | `if (sp_ob%hru_lte > 0) then > if (pco%ls_sd%a == "y") then > if (pco%csvout == "y") then` | `"SWAT-DEG                  hru-lte_ls_aa.csv"` |
| 703 | data | `if (sp_ob%hru_lte > 0) then > if (pco%pw_sd%d == "y") then` | `"SWAT-DEG                  hru-lte_pw_day.txt"` |
| 709 | data | `if (sp_ob%hru_lte > 0) then > if (pco%pw_sd%d == "y") then > if (pco%csvout == "y") then` | `"SWAT-DEG                  hru-lte_pw_day.csv"` |
| 718 | data | `if (sp_ob%hru_lte > 0) then > if (pco%pw_sd%m == "y") then` | `"SWAT-DEG                  hru-lte_pw_mon.txt"` |
| 724 | data | `if (sp_ob%hru_lte > 0) then > if (pco%pw_sd%m == "y") then > if (pco%csvout == "y") then` | `"SWAT-DEG                  hru-lte_pw_mon.csv"` |
| 733 | data | `if (sp_ob%hru_lte > 0) then > if (pco%pw_sd%y == "y") then` | `"SWAT-DEG                  hru-lte_pw_yr.txt"` |
| 739 | data | `if (sp_ob%hru_lte > 0) then > if (pco%pw_sd%y == "y") then > if (pco%csvout == "y") then` | `"SWAT-DEG                  hru-lte_pw_yr.csv"` |
| 748 | data | `if (sp_ob%hru_lte > 0) then > if (pco%pw_sd%a == "y") then` | `"SWAT-DEG                  hru-lte_pw_aa.txt"` |
| 754 | data | `if (sp_ob%hru_lte > 0) then > if (pco%pw_sd%a == "y") then > if (pco%csvout == "y") then` | `"SWAT-DEG                  hru-lte_pw_aa.csv"` |
| 766 | data | `if (db_mx%lsu_out > 0) then > if (pco%wb_lsu%d == "y") then` | `"ROUTING_UNIT              lsunit_wb_day.txt"` |
| 772 | data | `if (db_mx%lsu_out > 0) then > if (pco%wb_lsu%d == "y") then > if (pco%csvout == "y") then` | `"ROUTING_UNIT              lsunit_wb_day.csv"` |
| 782 | data | `if (db_mx%lsu_out > 0) then > if (pco%wb_lsu%m == "y") then` | `"ROUTING_UNIT              lsunit_wb_mon.txt"` |
| 788 | data | `if (db_mx%lsu_out > 0) then > if (pco%wb_lsu%m == "y") then > if (pco%csvout == "y") then` | `"ROUTING_UNIT              lsunit_wb_mon.csv"` |
| 798 | data | `if (db_mx%lsu_out > 0) then > if (sp_ob%ru > 0) then > if (pco%wb_lsu%y == "y") then` | `"ROUTING_UNIT              lsunit_wb_yr.txt"` |
| 804 | data | `if (db_mx%lsu_out > 0) then > if (sp_ob%ru > 0) then > if (pco%wb_lsu%y == "y") then > if (pco%csvout == "y") then` | `"ROUTING_UNIT              lsunit_wb_yr.csv"` |
| 814 | data | `if (db_mx%lsu_out > 0) then > if (pco%wb_lsu%a == "y") then` | `"ROUTING_UNIT              lsunit_wb_aa.txt"` |
| 820 | data | `if (db_mx%lsu_out > 0) then > if (pco%wb_lsu%a == "y") then > if (pco%csvout == "y") then` | `"ROUTING_UNIT              lsunit_wb_aa.csv"` |
| 830 | data | `if (db_mx%lsu_out > 0) then > if (pco%nb_lsu%d == "y") then` | `"ROUTING_UNIT              lsunit_nb_day.txt"` |
| 836 | data | `if (db_mx%lsu_out > 0) then > if (pco%nb_lsu%d == "y") then > if (pco%csvout == "y") then` | `"ROUTING_UNIT              lsunit_nb_day.csv"` |
| 845 | data | `if (db_mx%lsu_out > 0) then > if (pco%nb_lsu%m == "y") then` | `"ROUTING_UNIT              lsunit_nb_mon.txt"` |
| 851 | data | `if (db_mx%lsu_out > 0) then > if (pco%nb_lsu%m == "y") then > if (pco%csvout == "y") then` | `"ROUTING_UNIT              lsunit_nb_mon.csv"` |
| 860 | data | `if (db_mx%lsu_out > 0) then > if (pco%nb_lsu%y == "y") then` | `"ROUTING_UNIT              lsunit_nb_yr.txt"` |
| 866 | data | `if (db_mx%lsu_out > 0) then > if (pco%nb_lsu%y == "y") then > if (pco%csvout == "y") then` | `"ROUTING_UNIT              lsunit_nb_yr.csv"` |
| 875 | data | `if (db_mx%lsu_out > 0) then > if (pco%nb_lsu%a == "y") then` | `"ROUTING_UNIT              lsunit_nb_aa.txt"` |
| 881 | data | `if (db_mx%lsu_out > 0) then > if (pco%nb_lsu%a == "y") then > if (pco%csvout == "y") then` | `"ROUTING_UNIT              lsunit_nb_aa.csv"` |
| 891 | data | `if (db_mx%lsu_out > 0) then > if (pco%ls_lsu%d == "y") then` | `"ROUTING_UNIT              lsunit_ls_day.txt"` |
| 897 | data | `if (db_mx%lsu_out > 0) then > if (pco%ls_lsu%d == "y") then > if (pco%csvout == "y") then` | `"ROUTING_UNIT              lsunit_ls_day.csv"` |
| 906 | data | `if (db_mx%lsu_out > 0) then > if (pco%ls_lsu%m == "y") then` | `"ROUTING_UNIT              lsunit_ls_mon.txt"` |
| 912 | data | `if (db_mx%lsu_out > 0) then > if (pco%ls_lsu%m == "y") then > if (pco%csvout == "y") then` | `"ROUTING_UNIT              lsunit_ls_mon.csv"` |
| 921 | data | `if (db_mx%lsu_out > 0) then > if (pco%ls_lsu%y == "y") then` | `"ROUTING_UNIT              lsunit_ls_yr.txt"` |
| 927 | data | `if (db_mx%lsu_out > 0) then > if (pco%ls_lsu%y == "y") then > if (pco%csvout == "y") then` | `"ROUTING_UNIT              lsunit_ls_yr.csv"` |
| 936 | data | `if (db_mx%lsu_out > 0) then > if (pco%ls_lsu%a == "y") then` | `"ROUTING_UNIT              lsunit_ls_aa.txt"` |
| 942 | data | `if (db_mx%lsu_out > 0) then > if (pco%ls_lsu%a == "y") then > if (pco%csvout == "y") then` | `"ROUTING_UNIT              lsunit_ls_aa.csv"` |
| 952 | data | `if (db_mx%lsu_out > 0) then > if (pco%pw_lsu%d == "y") then` | `"ROUTING_UNIT              lsunit_pw_day.txt"` |
| 958 | data | `if (db_mx%lsu_out > 0) then > if (pco%pw_lsu%d == "y") then > if (pco%csvout == "y") then` | `"ROUTING_UNIT              lsunit_pw_day.csv"` |
| 968 | data | `if (db_mx%lsu_out > 0) then > if (pco%pw_lsu%m == "y") then` | `"ROUTING_UNIT              lsunit_pw_mon.txt"` |
| 974 | data | `if (db_mx%lsu_out > 0) then > if (pco%pw_lsu%m == "y") then > if (pco%csvout == "y") then` | `"ROUTING_UNIT              lsunit_pw_mon.csv"` |
| 983 | data | `if (db_mx%lsu_out > 0) then > if (pco%pw_lsu%y == "y") then` | `"ROUTING_UNIT              lsunit_pw_yr.txt"` |
| 989 | data | `if (db_mx%lsu_out > 0) then > if (pco%pw_lsu%y == "y") then > if (pco%csvout == "y") then` | `"ROUTING_UNIT              lsunit_pw_yr.csv"` |
| 998 | data | `if (db_mx%lsu_out > 0) then > if (pco%pw_lsu%a == "y") then` | `"ROUTING_UNIT              lsunit_pw_aa.txt"` |
| 1004 | data | `if (db_mx%lsu_out > 0) then > if (pco%pw_lsu%a == "y") then > if (pco%csvout == "y") then` | `"ROUTING_UNIT              lsunit_pw_aa.csv"` |
| 1015 | data | `if (pco%wb_bsn%d == "y") then` | `"BASIN                     basin_wb_day.txt"` |
| 1021 | data | `if (pco%wb_bsn%d == "y") then > if (pco%csvout == "y") then` | `"BASIN                     basin_wb_day.csv"` |
| 1030 | data | `if (pco%wb_bsn%m == "y") then` | `"BASIN                     basin_wb_mon.txt"` |
| 1036 | data | `if (pco%wb_bsn%m == "y") then > if (pco%csvout == "y") then` | `"BASIN                     basin_wb_mon.csv"` |
| 1045 | data | `if (pco%wb_bsn%y == "y") then` | `"BASIN                     basin_wb_yr.txt"` |
| 1051 | data | `if (pco%wb_bsn%y == "y") then > if (pco%csvout == "y") then` | `"BASIN                     basin_wb_yr.csv"` |
| 1060 | data | `if (pco%wb_bsn%a == "y") then` | `"BASIN                     basin_wb_aa.txt"` |
| 1066 | data | `if (pco%wb_bsn%a == "y") then > if (pco%csvout == "y") then` | `"BASIN                     basin_wb_aa.csv"` |
| 1076 | data | `if (pco%nb_bsn%d == "y") then` | `"BASIN                     basin_nb_day.txt"` |
| 1082 | data | `if (pco%nb_bsn%d == "y") then > if (pco%csvout == "y") then` | `"BASIN                     basin_nb_day.csv"` |
| 1091 | data | `if (pco%nb_bsn%m == "y") then` | `"BASIN                     basin_nb_mon.txt"` |
| 1097 | data | `if (pco%nb_bsn%m == "y") then > if (pco%csvout == "y") then` | `"BASIN                     basin_nb_mon.csv"` |
| 1106 | data | `if (pco%nb_bsn%y == "y") then` | `"BASIN                     basin_nb_yr.txt"` |
| 1112 | data | `if (pco%nb_bsn%y == "y") then > if (pco%csvout == "y") then` | `"BASIN                     basin_nb_yr.csv"` |
| 1121 | data | `if (pco%nb_bsn%a == "y") then` | `"BASIN                     basin_nb_aa.txt"` |
| 1127 | data | `if (pco%nb_bsn%a == "y") then > if (pco%csvout == "y") then` | `"BASIN                     basin_nb_aa.csv"` |
| 1137 | data | `if (pco%ls_bsn%d == "y") then` | `"BASIN                     basin_ls_day.txt"` |
| 1143 | data | `if (pco%ls_bsn%d == "y") then > if (pco%csvout == "y") then` | `"BASIN                     basin_ls_day.csv"` |
| 1152 | data | `if (pco%ls_bsn%m == "y") then` | `"BASIN                     basin_ls_mon.txt"` |
| 1158 | data | `if (pco%ls_bsn%m == "y") then > if (pco%csvout == "y") then` | `"BASIN                     basin_ls_mon.csv"` |
| 1167 | data | `if (pco%ls_bsn%y == "y") then` | `"BASIN                     basin_ls_yr.txt"` |
| 1173 | data | `if (pco%ls_bsn%y == "y") then > if (pco%csvout == "y") then` | `"BASIN                     basin_ls_yr.csv"` |
| 1182 | data | `if (pco%ls_bsn%a == "y") then` | `"BASIN                     basin_ls_aa.txt"` |
| 1188 | data | `if (pco%ls_bsn%a == "y") then > if (pco%csvout == "y") then` | `"BASIN                     basin_ls_aa.csv"` |
| 1198 | data | `if (pco%pw_bsn%d == "y") then` | `"BASIN                     basin_pw_day.txt"` |
| 1204 | data | `if (pco%pw_bsn%d == "y") then > if (pco%csvout == "y") then` | `"BASIN                     basin_pw_day.csv"` |
| 1213 | data | `if (pco%pw_bsn%m == "y") then` | `"BASIN                     basin_pw_mon.txt"` |
| 1219 | data | `if (pco%pw_bsn%m == "y") then > if (pco%csvout == "y") then` | `"BASIN                     basin_pw_mon.csv"` |
| 1228 | data | `if (pco%pw_bsn%y == "y") then` | `"BASIN                     basin_pw_yr.txt"` |
| 1234 | data | `if (pco%pw_bsn%y == "y") then > if (pco%csvout == "y") then` | `"BASIN                     basin_pw_yr.csv"` |
| 1243 | data | `if (pco%pw_bsn%a == "y") then` | `"BASIN                     basin_pw_aa.txt"` |
| 1249 | data | `if (pco%pw_bsn%a == "y") then > if (pco%csvout == "y") then` | `"BASIN                     basin_pw_aa.csv"` |
| 1259 | data | `if (pco%crop_yld == "y" .or. pco%crop_yld == "b") then` | `"CROP                      crop_yld_yr.txt"` |
| 1264 | data | `if (pco%crop_yld == "y" .or. pco%crop_yld == "b") then > if (pco%csvout == "y") then` | `"CROP                      crop_yld_yr.csv"` |
| 1273 | data | `if (pco%crop_yld == "a" .or. pco%crop_yld == "b") then` | `"CROP                      crop_yld_aa.txt"` |
| 1278 | data | `if (pco%crop_yld == "a" .or. pco%crop_yld == "b") then > if (pco%csvout == "y") then` | `"CROP                      crop_yld_aa.csv"` |
| 1297 | data | `if (db_mx%lsu_out > 0) then > if (pco%cb_gl_lsu%d == "y") then` | `"LSU                       lsu_carb_gl_day.txt"` |
| 1303 | data | `if (db_mx%lsu_out > 0) then > if (pco%cb_gl_lsu%d == "y") then > if (pco%csvout == "y") then` | `"LSU                       lsu_carb_gl_day.csv"` |
| 1311 | data | `if (db_mx%lsu_out > 0) then > if (pco%cb_gl_lsu%m == "y") then` | `"LSU                       lsu_carb_gl_mon.txt"` |
| 1317 | data | `if (db_mx%lsu_out > 0) then > if (pco%cb_gl_lsu%m == "y") then > if (pco%csvout == "y") then` | `"LSU                       lsu_carb_gl_mon.csv"` |
| 1325 | data | `if (db_mx%lsu_out > 0) then > if (pco%cb_gl_lsu%y == "y") then` | `"LSU                       lsu_carb_gl_yr.txt"` |
| 1331 | data | `if (db_mx%lsu_out > 0) then > if (pco%cb_gl_lsu%y == "y") then > if (pco%csvout == "y") then` | `"LSU                       lsu_carb_gl_yr.csv"` |
| 1339 | data | `if (db_mx%lsu_out > 0) then > if (pco%cb_gl_lsu%a == "y") then` | `"LSU                       lsu_carb_gl_aa.txt"` |
| 1345 | data | `if (db_mx%lsu_out > 0) then > if (pco%cb_gl_lsu%a == "y") then > if (pco%csvout == "y") then` | `"LSU                       lsu_carb_gl_aa.csv"` |
| 1355 | data | `if (db_mx%lsu_out > 0) then > if (pco%cb_trf_lsu%d == "y") then` | `"LSU                       lsu_scf_day.txt"` |
| 1361 | data | `if (db_mx%lsu_out > 0) then > if (pco%cb_trf_lsu%d == "y") then > if (pco%csvout == "y") then` | `"LSU                       lsu_scf_day.csv"` |
| 1369 | data | `if (db_mx%lsu_out > 0) then > if (pco%cb_trf_lsu%m == "y") then` | `"LSU                       lsu_scf_mon.txt"` |
| 1375 | data | `if (db_mx%lsu_out > 0) then > if (pco%cb_trf_lsu%m == "y") then > if (pco%csvout == "y") then` | `"LSU                       lsu_scf_mon.csv"` |
| 1383 | data | `if (db_mx%lsu_out > 0) then > if (pco%cb_trf_lsu%y == "y") then` | `"LSU                       lsu_scf_yr.txt"` |
| 1389 | data | `if (db_mx%lsu_out > 0) then > if (pco%cb_trf_lsu%y == "y") then > if (pco%csvout == "y") then` | `"LSU                       lsu_scf_yr.csv"` |
| 1397 | data | `if (db_mx%lsu_out > 0) then > if (pco%cb_trf_lsu%a == "y") then` | `"LSU                       lsu_scf_aa.txt"` |
| 1403 | data | `if (db_mx%lsu_out > 0) then > if (pco%cb_trf_lsu%a == "y") then > if (pco%csvout == "y") then` | `"LSU                       lsu_scf_aa.csv"` |
| 1412 | data | `if (db_mx%lsu_out > 0) then > if (pco%cb_plt_lsu%d == "y") then` | `"LSU                       lsu_plc_stat_day.txt"` |
| 1417 | data | `if (db_mx%lsu_out > 0) then > if (pco%cb_plt_lsu%d == "y") then > if (pco%csvout == "y") then` | `"LSU                       lsu_plc_stat_day.csv"` |
| 1424 | data | `if (db_mx%lsu_out > 0) then > if (pco%cb_plt_lsu%m == "y") then` | `"LSU                       lsu_plc_stat_mon.txt"` |
| 1429 | data | `if (db_mx%lsu_out > 0) then > if (pco%cb_plt_lsu%m == "y") then > if (pco%csvout == "y") then` | `"LSU                       lsu_plc_stat_mon.csv"` |
| 1436 | data | `if (db_mx%lsu_out > 0) then > if (pco%cb_plt_lsu%y == "y") then` | `"LSU                       lsu_plc_stat_yr.txt"` |
| 1441 | data | `if (db_mx%lsu_out > 0) then > if (pco%cb_plt_lsu%y == "y") then > if (pco%csvout == "y") then` | `"LSU                       lsu_plc_stat_yr.csv"` |
| 1448 | data | `if (db_mx%lsu_out > 0) then > if (pco%cb_plt_lsu%a == "y") then` | `"LSU                       lsu_plc_stat_aa.txt"` |
| 1453 | data | `if (db_mx%lsu_out > 0) then > if (pco%cb_plt_lsu%a == "y") then > if (pco%csvout == "y") then` | `"LSU                       lsu_plc_stat_aa.csv"` |
| 1475 | data | `None` | `"HRU                       " // trim(fname_txt)` |
| 1480 | data | `if (pco%csvout == "y") then` | `"HRU                       " // trim(fname_csv)` |
| 1492 | data | `None` | `"HRU                       " // trim(fname_txt)` |
| 1497 | data | `if (pco%csvout == "y") then` | `"HRU                       " // trim(fname_csv)` |
| 1512 | data | `None` | `"HRU                       " // trim(fname_txt)` |
| 1517 | data | `if (pco%csvout == "y") then` | `"HRU                       " // trim(fname_csv)` |


- Procedure: `proc_bsn`
- Writer: `proc_bsn.f90`
- Match: source_output
- Resolved default filename(s): `files_out.out`

| Line | Role | Condition | Fields written |
| --- | --- | --- | --- |
| 16 | data | `None` | `"files_out.out - OUTPUT FILES WRITTEN"` |


- Procedure: `proc_hru`
- Writer: `proc_hru.f90`
- Match: source_output
- Resolved default filename(s): `files_out.out`

| Line | Role | Condition | Fields written |
| --- | --- | --- | --- |
| 61 | data | `if (sp_ob%hru > 0) then` | `"CHK                       checker.out"` |


#### Candidate write structure

- Source expression(s): _none captured_

- Procedure: `carbon_legacy_open`
- Writer: `carbon_legacy_module.f90`
- Match: source_output
- Resolved default filename(s): `files_out.out`

| Line | Role | Condition | Fields written |
| --- | --- | --- | --- |
| 480 | data | `if (pco%cb_hru%d /= "n" .or. pco%cb_hru%m /= "n"  .or. pco%cb_hru%y /= "n") then` | `"HRU                       hru_cbn_lyr.txt"` |
| 484 | data | `if (pco%cb_hru%d /= "n" .or. pco%cb_hru%m /= "n"  .or. pco%cb_hru%y /= "n") then > if (pco%csvout == "y") then` | `"HRU                       hru_cbn_lyr.csv"` |
| 489 | data | `if (pco%cb_hru%d /= "n" .or. pco%cb_hru%m /= "n"  .or. pco%cb_hru%y /= "n") then` | `"HRU                       hru_seq_lyr.txt"` |
| 493 | data | `if (pco%cb_hru%d /= "n" .or. pco%cb_hru%m /= "n"  .or. pco%cb_hru%y /= "n") then > if (pco%csvout == "y") then` | `"HRU                       hru_seq_lyr.csv"` |
| 500 | data | `if (pco%cb_hru%d /= "n" .or. pco%cb_hru%m /= "n"  .or. pco%cb_hru%y /= "n") then` | `"HRU                       hru_n_p_pool_stat.txt"` |
| 506 | data | `if (pco%cb_hru%d /= "n" .or. pco%cb_hru%m /= "n"  .or. pco%cb_hru%y /= "n") then > if (pco%csvout == "y") then` | `"HRU                       hru_n_p_pool_stat.csv"` |
| 514 | data | `if (pco%cb_hru%d /= "n" .or. pco%cb_hru%m /= "n"  .or. pco%cb_hru%y /= "n") then > if (cbn_diagnostics .eqv. .true.) then` | `"HRU                       hru_begsim_soil_prop.txt"` |
| 519 | data | `if (pco%cb_hru%d /= "n" .or. pco%cb_hru%m /= "n"  .or. pco%cb_hru%y /= "n") then > if (cbn_diagnostics .eqv. .true.) then > if (pco%csvout == "y") then` | `"HRU                       hru_begsim_soil_prop.csv"` |
| 526 | data | `if (pco%cb_hru%d /= "n" .or. pco%cb_hru%m /= "n"  .or. pco%cb_hru%y /= "n") then > if (cbn_diagnostics .eqv. .true.) then` | `"HRU                       hru_endsim_soil_prop.txt"` |
| 531 | data | `if (pco%cb_hru%d /= "n" .or. pco%cb_hru%m /= "n"  .or. pco%cb_hru%y /= "n") then > if (cbn_diagnostics .eqv. .true.) then > if (pco%csvout == "y") then` | `"HRU                       hru_endsim_soil_prop.csv"` |
| 545 | data | `if (pco%cb_hru%d /= "n" .or. pco%cb_hru%m /= "n"  .or. pco%cb_hru%y /= "n") then > if (cbn_diagnostics .eqv. .true.) then > if (bsn_cc%cswat == 2 ) then > if (pco%cb_hru%d /= "n" .or. pco%cb_hru%m /= "n" .or. pco%cb_hru%y /= "n" .or. pco%cb_hru%a /= "n") then` | `"HRU                       hru_plc_stat.txt"` |
| 551 | data | `if (pco%cb_hru%d /= "n" .or. pco%cb_hru%m /= "n"  .or. pco%cb_hru%y /= "n") then > if (cbn_diagnostics .eqv. .true.) then > if (bsn_cc%cswat == 2 ) then > if (pco%cb_hru%d /= "n" .or. pco%cb_hru%m /= "n" .or. pco%cb_hru%y /= "n" .or. pco%cb_hru%a /= "n") then > if (pco%csvout == "y") then` | `"HRU                       hru_plc_stat.csv"` |
| 558 | data | `if (pco%cb_hru%d /= "n" .or. pco%cb_hru%m /= "n"  .or. pco%cb_hru%y /= "n") then > if (cbn_diagnostics .eqv. .true.) then > if (bsn_cc%cswat == 2 ) then > if (pco%cb_hru%d /= "n" .or. pco%cb_hru%m /= "n" .or. pco%cb_hru%y /= "n" .or. pco%cb_hru%a /= "n") then` | `"HRU                       hru_cflux_stat.txt"` |
| 564 | data | `if (pco%cb_hru%d /= "n" .or. pco%cb_hru%m /= "n"  .or. pco%cb_hru%y /= "n") then > if (cbn_diagnostics .eqv. .true.) then > if (bsn_cc%cswat == 2 ) then > if (pco%cb_hru%d /= "n" .or. pco%cb_hru%m /= "n" .or. pco%cb_hru%y /= "n" .or. pco%cb_hru%a /= "n") then > if (pco%csvout == "y") then` | `"HRU                       hru_cflux_stat.csv"` |
| 571 | data | `if (pco%cb_hru%d /= "n" .or. pco%cb_hru%m /= "n"  .or. pco%cb_hru%y /= "n") then > if (cbn_diagnostics .eqv. .true.) then > if (bsn_cc%cswat == 2 ) then > if (pco%cb_hru%d /= "n" .or. pco%cb_hru%m /= "n" .or. pco%cb_hru%y /= "n" .or. pco%cb_hru%a /= "n") then` | `"HRU                       hru_cpool_stat.txt"` |
| 577 | data | `if (pco%cb_hru%d /= "n" .or. pco%cb_hru%m /= "n"  .or. pco%cb_hru%y /= "n") then > if (cbn_diagnostics .eqv. .true.) then > if (bsn_cc%cswat == 2 ) then > if (pco%cb_hru%d /= "n" .or. pco%cb_hru%m /= "n" .or. pco%cb_hru%y /= "n" .or. pco%cb_hru%a /= "n") then > if (pco%csvout == "y") then` | `"HRU                       hru_cpool_stat.csv"` |
| 591 | data | `if (bsn_cc%cswat == 2 ) then > if (pco%cb_vars_hru%d /= "n" .or. pco%cb_vars_hru%m /= "n"  .or. pco%cb_vars_hru%y /= "n" ) then` | `"HRU                       hru_carbvars.txt"` |
| 596 | data | `if (bsn_cc%cswat == 2 ) then > if (pco%cb_vars_hru%d /= "n" .or. pco%cb_vars_hru%m /= "n"  .or. pco%cb_vars_hru%y /= "n" ) then > if (pco%csvout == "y") then` | `"HRU                       hru_carbvars.csv"` |
| 603 | data | `if (bsn_cc%cswat == 2 ) then > if (pco%cb_vars_hru%d /= "n" .or. pco%cb_vars_hru%m /= "n"  .or. pco%cb_vars_hru%y /= "n" ) then` | `"HRU                       hru_org_allo_vars.txt"` |
| 608 | data | `if (bsn_cc%cswat == 2 ) then > if (pco%cb_vars_hru%d /= "n" .or. pco%cb_vars_hru%m /= "n"  .or. pco%cb_vars_hru%y /= "n" ) then > if (pco%csvout == "y") then` | `"HRU                       hru_org_allo_vars.csv"` |
| 615 | data | `if (bsn_cc%cswat == 2 ) then > if (pco%cb_vars_hru%d /= "n" .or. pco%cb_vars_hru%m /= "n"  .or. pco%cb_vars_hru%y /= "n" ) then` | `"HRU                       hru_org_ratio_vars.txt"` |
| 620 | data | `if (bsn_cc%cswat == 2 ) then > if (pco%cb_vars_hru%d /= "n" .or. pco%cb_vars_hru%m /= "n"  .or. pco%cb_vars_hru%y /= "n" ) then > if (pco%csvout == "y") then` | `"HRU                       hru_org_ratio_vars.csv"` |
| 628 | data | `if (bsn_cc%cswat == 2 ) then > if (pco%cb_vars_hru%d /= "n" .or. pco%cb_vars_hru%m /= "n"  .or. pco%cb_vars_hru%y /= "n" ) then` | `"HRU                       hru_org_trans_vars.txt"` |
| 634 | data | `if (bsn_cc%cswat == 2 ) then > if (pco%cb_vars_hru%d /= "n" .or. pco%cb_vars_hru%m /= "n"  .or. pco%cb_vars_hru%y /= "n" ) then > if (pco%csvout == "y") then` | `"HRU                       hru_org_trans_vars.csv"` |
| 648 | data | `if (pco%cb_hru%d /= "n" .or. pco%cb_hru%m /= "n" .or. pco%cb_hru%y /= "n" .or. pco%cb_hru%a /= "n") then > if (pco%nb_hru%a == "y") then` | `"BASIN                     basin_carbon_all.txt"` |


- Procedure: `header_aquifer`
- Writer: `header_aquifer.f90`
- Match: source_output
- Resolved default filename(s): `files_out.out`

| Line | Role | Condition | Fields written |
| --- | --- | --- | --- |
| 17 | data | `if (sp_ob%aqu > 0) then > if (pco%aqu%d == "y") then` | `"AQUIFER                   aquifer_day.txt"` |
| 23 | data | `if (sp_ob%aqu > 0) then > if (pco%aqu%d == "y") then > if (pco%csvout == "y") then` | `"AQUIFER                   aquifer_day.csv"` |
| 34 | data | `if (sp_ob%aqu > 0) then > if (pco%aqu%m == "y") then` | `"AQUIFER                   aquifer_mon.txt"` |
| 40 | data | `if (sp_ob%aqu > 0) then > if (pco%aqu%m == "y") then > if (pco%csvout == "y") then` | `"AQUIFER                   aquifer_mon.csv"` |
| 51 | data | `if (sp_ob%aqu > 0) then > if (pco%aqu%y == "y") then` | `"AQUIFER                   aquifer_yr.txt"` |
| 57 | data | `if (sp_ob%aqu > 0) then > if (pco%aqu%y == "y") then > if (pco%csvout == "y") then` | `"AQUIFER                   aquifer_yr.csv"` |
| 68 | data | `if (sp_ob%aqu > 0) then > if (pco%aqu%a == "y") then` | `"AQUIFER                   aquifer_aa.txt"` |
| 74 | data | `if (sp_ob%aqu > 0) then > if (pco%aqu%a == "y") then > if (pco%csvout == "y") then` | `"AQUIFER                   aquifer_aa.csv"` |


- Procedure: `header_channel`
- Writer: `header_channel.f90`
- Match: source_output
- Resolved default filename(s): `files_out.out`

| Line | Role | Condition | Fields written |
| --- | --- | --- | --- |
| 30 | data | `if (sp_ob%chan > 0) then > if (pco%chan%d == "y") then` | `"CHANNEL                   channel_day.txt"` |
| 36 | data | `if (sp_ob%chan > 0) then > if (pco%chan%d == "y") then > if (pco%csvout == "y")  then` | `"CHANNEL                   channel_day.csv"` |
| 47 | data | `if (sp_ob%chan > 0) then > if (pco%chan%m == "y") then` | `"CHANNEL                   channel_mon.txt"` |
| 53 | data | `if (sp_ob%chan > 0) then > if (pco%chan%m == "y") then > if (pco%csvout == "y") then` | `"CHANNEL                   channel_mon.csv"` |
| 64 | data | `if (sp_ob%chan > 0) then > if (pco%chan%y == "y") then` | `"CHANNEL                   channel_yr.txt"` |
| 70 | data | `if (sp_ob%chan > 0) then > if (pco%chan%y == "y") then > if (pco%csvout == "y")  then` | `"CHANNEL                   channel_yr.csv"` |
| 81 | data | `if (sp_ob%chan > 0) then > if (pco%chan%a == "y") then` | `"CHANNEL                   channel_aa.txt"` |
| 87 | data | `if (sp_ob%chan > 0) then > if (pco%chan%a == "y") then > if (pco%csvout == "y") then` | `"CHANNEL                   channel_aa.csv"` |


- Procedure: `header_cs`
- Writer: `header_cs.f90`
- Match: source_output
- Resolved default filename(s): `files_out.out`

| Line | Role | Condition | Fields written |
| --- | --- | --- | --- |
| 18 | data | `if (pco%hyd%d == "y") then > if (cs_db%num_pests > 0) then` | `"HYDIN_PESTS               hydin_pests_day.txt"` |
| 23 | data | `if (pco%hyd%d == "y") then > if (cs_db%num_pests > 0) then > if (pco%csvout == "y") then` | `"HYDIN_PESTS               hydin_pests_day.csv"` |
| 31 | data | `if (pco%hyd%d == "y") then > if (cs_db%num_paths > 0) then` | `"HYDIN_PATHS               hydin_paths_day.txt"` |
| 36 | data | `if (pco%hyd%d == "y") then > if (cs_db%num_paths > 0) then > if (pco%csvout == "y") then` | `"HYDIN_PATHS               hydin_paths_day.csv"` |
| 44 | data | `if (pco%hyd%d == "y") then > if (cs_db%num_metals > 0) then` | `"HYDIN_METALS              hydin_metals_day.txt"` |
| 49 | data | `if (pco%hyd%d == "y") then > if (cs_db%num_metals > 0) then > if (pco%csvout == "y") then` | `"HYDIN_METALS              hydin_metals_day.csv"` |
| 57 | data | `if (pco%hyd%d == "y") then > if (cs_db%num_salts > 0) then` | `"HYDIN_SALTS               hydin_salts_day.txt"` |
| 62 | data | `if (pco%hyd%d == "y") then > if (cs_db%num_salts > 0) then > if (pco%csvout == "y") then` | `"HYDIN_SALTS               hydin_salts_day.csv"` |
| 73 | data | `if (pco%hyd%m == "y") then > if (cs_db%num_pests > 0) then` | `"HYDIN_PESTS               hydin_pests_mon.txt"` |
| 78 | data | `if (pco%hyd%m == "y") then > if (cs_db%num_pests > 0) then > if (pco%csvout == "y") then` | `"HYDIN_PESTS               hydin_pests_mon.csv"` |
| 87 | data | `if (pco%hyd%m == "y") then > if (cs_db%num_paths > 0) then` | `"HYDIN_PATHS               hydin_paths_mon.txt"` |
| 92 | data | `if (pco%hyd%m == "y") then > if (cs_db%num_paths > 0) then > if (pco%csvout == "y") then` | `"HYDIN_PATHS               hydin_paths_mon.csv"` |
| 100 | data | `if (pco%hyd%m == "y") then > if (cs_db%num_metals > 0) then` | `"HYDIN_METALS              hydin_metals_mon.txt"` |
| 105 | data | `if (pco%hyd%m == "y") then > if (cs_db%num_metals > 0) then > if (pco%csvout == "y") then` | `"HYDIN_METALS              hydin_metals_mon.csv"` |
| 113 | data | `if (pco%hyd%m == "y") then > if (cs_db%num_salts > 0) then` | `"HYDIN_SALTS               hydin_salts_mon.txt"` |
| 118 | data | `if (pco%hyd%m == "y") then > if (cs_db%num_salts > 0) then > if (pco%csvout == "y") then` | `"HYDIN_SALTS               hydin_salts_mon.csv"` |
| 130 | data | `if (pco%hyd%y == "y") then > if (cs_db%num_pests > 0) then` | `"HYDIN_PESTS               hydin_pests_yr.txt"` |
| 135 | data | `if (pco%hyd%y == "y") then > if (cs_db%num_pests > 0) then > if (pco%csvout == "y") then` | `"HYDIN_PESTS               hydin_pests_yr.csv"` |
| 143 | data | `if (pco%hyd%y == "y") then > if (cs_db%num_paths > 0) then` | `"HYDIN_PATHS               hydin_paths_yr.txt"` |
| 148 | data | `if (pco%hyd%y == "y") then > if (cs_db%num_paths > 0) then > if (pco%csvout == "y") then` | `"HYDIN_PATHS               hydin_paths_yr.csv"` |
| 156 | data | `if (pco%hyd%y == "y") then > if (cs_db%num_metals > 0) then` | `"HYDIN_METALS              hydin_metals_yr.txt"` |
| 161 | data | `if (pco%hyd%y == "y") then > if (cs_db%num_metals > 0) then > if (pco%csvout == "y") then` | `"HYDIN_METALS              hydin_metals_yr.csv"` |
| 169 | data | `if (pco%hyd%y == "y") then > if (cs_db%num_salts > 0) then` | `"HYDIN_SALTS               hydin_salts_yr.txt"` |
| 174 | data | `if (pco%hyd%y == "y") then > if (cs_db%num_salts > 0) then > if (pco%csvout == "y") then` | `"HYDIN_SALTS               hydin_salts_yr.csv"` |
| 185 | data | `if (pco%hyd%a == "y") then > if (cs_db%num_pests > 0) then` | `"HYDIN_PESTS               hydin_pests_aa.txt"` |
| 190 | data | `if (pco%hyd%a == "y") then > if (cs_db%num_pests > 0) then > if (pco%csvout == "y") then` | `"HYDIN_PESTS               hydin_pests_aa.csv"` |
| 198 | data | `if (pco%hyd%a == "y") then > if (cs_db%num_paths > 0) then` | `"HYDIN_PATHS               hydin_paths_aa.txt"` |
| 203 | data | `if (pco%hyd%a == "y") then > if (cs_db%num_paths > 0) then > if (pco%csvout == "y") then` | `"HYDIN_PATHS               hydin_paths_aa.csv"` |
| 211 | data | `if (pco%hyd%a == "y") then > if (cs_db%num_metals > 0) then` | `"HYDIN_METALS              hydin_metals_aa.txt"` |
| 216 | data | `if (pco%hyd%a == "y") then > if (cs_db%num_metals > 0) then > if (pco%csvout == "y") then` | `"HYDIN_METALS              hydin_metals_aa.csv"` |
| 224 | data | `if (pco%hyd%a == "y") then > if (cs_db%num_salts > 0) then` | `"HYDIN_SALTS               hydin_salts_aa.txt"` |
| 229 | data | `if (pco%hyd%a == "y") then > if (cs_db%num_salts > 0) then > if (pco%csvout == "y") then` | `"HYDIN_SALTS               hydin_salts_aa.csv"` |
| 242 | data | `if (pco%hyd%d == "y") then > if (cs_db%num_pests > 0) then` | `"HYDOUT_PESTS              hydout_pests_day.txt"` |
| 247 | data | `if (pco%hyd%d == "y") then > if (cs_db%num_pests > 0) then > if (pco%csvout == "y") then` | `"HYDOUT_PESTS              hydout_pests_day.csv"` |
| 253 | data | `if (pco%hyd%d == "y") then > if (cs_db%num_paths > 0) then` | `"HYDOUT_PATHS              hydout_paths_day.txt"` |
| 260 | data | `if (pco%hyd%d == "y") then > if (cs_db%num_paths > 0) then > if (pco%csvout == "y") then` | `"HYDOUT_PATHS              hydout_paths_day.csv"` |
| 266 | data | `if (pco%hyd%d == "y") then > if (cs_db%num_metals > 0) then` | `"HYDOUT_METALS             hydout_metals_day.txt"` |
| 271 | data | `if (pco%hyd%d == "y") then > if (cs_db%num_metals > 0) then > if (pco%csvout == "y") then` | `"HYDOUT_METALS             hydout_metals_day.csv"` |
| 279 | data | `if (pco%hyd%d == "y") then > if (cs_db%num_salts > 0) then` | `"HYDOUT_SALTS              hydout_salts_day.txt"` |
| 284 | data | `if (pco%hyd%d == "y") then > if (cs_db%num_salts > 0) then > if (pco%csvout == "y") then` | `"HYDOUT_SALTS              hydout_salts_day.csv"` |
| 295 | data | `if (pco%hyd%m == "y") then > if (cs_db%num_pests > 0) then` | `"HYDOUT_PESTS              hydout_pests_mon.txt"` |
| 300 | data | `if (pco%hyd%m == "y") then > if (cs_db%num_pests > 0) then > if (pco%csvout == "y") then` | `"HYDOUT_PESTS              hydout_pests_mon.csv"` |
| 308 | data | `if (pco%hyd%m == "y") then > if (cs_db%num_paths > 0) then` | `"HYDOUT_PATHS              hydout_paths_mon.txt"` |
| 313 | data | `if (pco%hyd%m == "y") then > if (cs_db%num_paths > 0) then > if (pco%csvout == "y") then` | `"HYDOUT_PATHS              hydout_paths_mon.csv"` |
| 321 | data | `if (pco%hyd%m == "y") then > if (cs_db%num_metals > 0) then` | `"HYDOUT_METALS             hydout_metals_mon.txt"` |
| 326 | data | `if (pco%hyd%m == "y") then > if (cs_db%num_metals > 0) then > if (pco%csvout == "y") then` | `"HYDOUT_METALS             hydout_metals_mon.csv"` |
| 334 | data | `if (pco%hyd%m == "y") then > if (cs_db%num_salts > 0) then` | `"HYDOUT_SALTS              hydout_salts_mon.txt"` |
| 339 | data | `if (pco%hyd%m == "y") then > if (cs_db%num_salts > 0) then > if (pco%csvout == "y") then` | `"HYDOUT_SALTS              hydout_salts_mon.csv"` |
| 351 | data | `if (pco%hyd%y == "y") then > if (cs_db%num_pests > 0) then` | `"HYDOUT_PESTS              hydout_pests_yr.txt"` |
| 356 | data | `if (pco%hyd%y == "y") then > if (cs_db%num_pests > 0) then > if (pco%csvout == "y") then` | `"HYDOUT_PESTS              hydout_pests_yr.csv"` |
| 364 | data | `if (pco%hyd%y == "y") then > if (cs_db%num_paths > 0) then` | `"HYDOUT_PATHS              hydout_paths_yr.txt"` |
| 369 | data | `if (pco%hyd%y == "y") then > if (cs_db%num_paths > 0) then > if (pco%csvout == "y") then` | `"HYDOUT_PATHS              hydout_paths_yr.csv"` |
| 377 | data | `if (pco%hyd%y == "y") then > if (cs_db%num_metals > 0) then` | `"HYDOUT_METALS             hydout_metals_yr.txt"` |
| 382 | data | `if (pco%hyd%y == "y") then > if (cs_db%num_metals > 0) then > if (pco%csvout == "y") then` | `"HYDOUT_METALS             hydout_metals_yr.csv"` |
| 390 | data | `if (pco%hyd%y == "y") then > if (cs_db%num_salts > 0) then` | `"HYDOUT_SALTS              hydout_salts_yr.txt"` |
| 395 | data | `if (pco%hyd%y == "y") then > if (cs_db%num_salts > 0) then > if (pco%csvout == "y") then` | `"HYDOUT_SALTS              hydout_salts_yr.csv"` |
| 406 | data | `if (pco%hyd%a == "y") then > if (cs_db%num_pests > 0) then` | `"HYDOUT_PESTS              hydout_pests_aa.txt"` |
| 411 | data | `if (pco%hyd%a == "y") then > if (cs_db%num_pests > 0) then > if (pco%csvout == "y") then` | `"HYDOUT_PESTS              hydout_pests_aa.csv"` |
| 419 | data | `if (pco%hyd%a == "y") then > if (cs_db%num_paths > 0) then` | `"HYDOUT_PATHS              hydout_paths_aa.txt"` |
| 424 | data | `if (pco%hyd%a == "y") then > if (cs_db%num_paths > 0) then > if (pco%csvout == "y") then` | `"HYDOUT_PATHS              hydout_paths_aa.csv"` |
| 432 | data | `if (pco%hyd%a == "y") then > if (cs_db%num_metals > 0) then` | `"HYDOUT_METALS             hydout_metals_aa.txt"` |
| 437 | data | `if (pco%hyd%a == "y") then > if (cs_db%num_metals > 0) then > if (pco%csvout == "y") then` | `"HYDOUT_METALS             hydout_metals_aa.csv"` |
| 445 | data | `if (pco%hyd%a == "y") then > if (cs_db%num_salts > 0) then` | `"HYDOUT_SALTS              hydout_salts_aa.txt"` |
| 450 | data | `if (pco%hyd%a == "y") then > if (cs_db%num_salts > 0) then > if (pco%csvout == "y") then` | `"HYDOUT_SALTS              hydout_salts_aa.csv"` |


- Procedure: `header_hyd`
- Writer: `header_hyd.f90`
- Match: source_output
- Resolved default filename(s): `files_out.out`

| Line | Role | Condition | Fields written |
| --- | --- | --- | --- |
| 11 | data | `if (pco%hydcon == "y") then` | `"HYDCON                    hydcon.out"` |
| 14 | data | `if (pco%hydcon == "y") then > if (pco%csvout == "y") then` | `"HYDCON                    hydcon.csv"` |
| 24 | data | `if (pco%hyd%d == "y") then` | `"HYDOUT                    hydout_day.txt"` |
| 30 | data | `if (pco%hyd%d == "y") then > if (pco%csvout == "y") then` | `"HYDOUT                    hydout_day.csv"` |
| 39 | data | `if (pco%hyd%m == "y") then` | `"HYDOUT                    hydout_mon.txt"` |
| 45 | data | `if (pco%hyd%m == "y") then > if (pco%csvout == "y") then` | `"HYDOUT                    hydout_mon.csv"` |
| 54 | data | `if (pco%hyd%y == "y") then` | `"HYDOUT                    hydout_yr.txt"` |
| 60 | data | `if (pco%hyd%y == "y") then > if (pco%csvout == "y") then` | `"HYDOUT                    hydout_yr.csv"` |
| 69 | data | `if (pco%hyd%a == "y") then` | `"HYDOUT                    hydout_aa.txt"` |
| 75 | data | `if (pco%hyd%a == "y") then > if (pco%csvout == "y") then` | `"HYDOUT                    hydout_aa.csv"` |
| 86 | data | `if (pco%hyd%d == "y") then` | `"HYDIN                     hydin_day.txt"` |
| 92 | data | `if (pco%hyd%d == "y") then > if (pco%csvout == "y") then` | `"HYDIN                     hydin_day.csv"` |
| 101 | data | `if (pco%hyd%m == "y") then` | `"HYDIN                     hydin_mon.txt"` |
| 107 | data | `if (pco%hyd%m == "y") then > if (pco%csvout == "y") then` | `"HYDIN                     hydin_mon.csv"` |
| 116 | data | `if (pco%hyd%y == "y") then` | `"HYDIN                     hydin_yr.txt"` |
| 122 | data | `if (pco%hyd%y == "y") then > if (pco%csvout == "y") then` | `"HYDIN                     hydin_yr.csv"` |
| 131 | data | `if (pco%hyd%a == "y") then` | `"HYDIN                     hydin_aa.txt"` |
| 137 | data | `if (pco%hyd%a == "y") then > if (pco%csvout == "y") then` | `"HYDIN                     hydin_aa.csv"` |
| 148 | data | `if (pco%hyd%d == "y") then` | `"DEPO                      deposition_day.txt"` |
| 154 | data | `if (pco%hyd%d == "y") then > if (pco%csvout == "y") then` | `"DEPO                      deposition_day.csv"` |
| 164 | data | `if (pco%hyd%m == "y") then` | `"DEPO                      deposition_mon.txt"` |
| 170 | data | `if (pco%hyd%m == "y") then > if (pco%csvout == "y") then` | `"DEPO                      deposition_mon.csv"` |
| 180 | data | `if (pco%hyd%y == "y") then` | `"DEPO                      deposition_yr.txt"` |
| 186 | data | `if (pco%hyd%y == "y") then > if (pco%csvout == "y") then` | `"DEPO                      deposition_yr.csv"` |
| 196 | data | `if (pco%hyd%a == "y") then` | `"DEPO                      deposition_aa.txt"` |
| 202 | data | `if (pco%hyd%a == "y") then > if (pco%csvout == "y") then` | `"DEPO                      deposition_aa.csv"` |


- Procedure: `header_lu_change`
- Writer: `header_lu_change.f90`
- Match: source_output
- Resolved default filename(s): `files_out.out`

| Line | Role | Condition | Fields written |
| --- | --- | --- | --- |
| 13 | data | `None` | `"DTBL                      lu_change_out.txt"` |


- Procedure: `header_mgt`
- Writer: `header_mgt.f90`
- Match: source_output
- Resolved default filename(s): `files_out.out`

| Line | Role | Condition | Fields written |
| --- | --- | --- | --- |
| 13 | data | `if (pco%mgtout == "y") then` | `"MGT                       mgt_out.txt"` |


- Procedure: `header_path`
- Writer: `header_path.f90`
- Match: source_output
- Resolved default filename(s): `files_out.out`

| Line | Role | Condition | Fields written |
| --- | --- | --- | --- |
| 15 | data | `if (pco%wb_hru%d == "y" .and. cs_db%num_tot > 0) then` | `"HRU_PATH                  hru_path_day.txt"` |
| 22 | data | `if (pco%wb_hru%d == "y" .and. cs_db%num_tot > 0) then > if (pco%csvout == "y") then` | `"HRU_PATH                  hru_path_day.csv"` |
| 30 | data | `if (pco%wb_hru%m == "y" .and. cs_db%num_tot > 0) then` | `"HRU_PATH                  hru_path_mon.txt"` |
| 37 | data | `if (pco%wb_hru%m == "y" .and. cs_db%num_tot > 0) then > if (pco%csvout == "y") then` | `"HRU_PATH                  hru_path_mon.csv"` |
| 45 | data | `if (pco%wb_hru%y == "y" .and. cs_db%num_tot > 0) then` | `"HRU_PATH                  hru_path_yr.txt"` |
| 52 | data | `if (pco%wb_hru%y == "y" .and. cs_db%num_tot > 0) then > if (pco%csvout == "y") then` | `"HRU_PATH                  hru_path_yr.csv"` |
| 60 | data | `if (pco%wb_hru%a == "y" .and. cs_db%num_tot > 0) then` | `"HRU_PATH                  hru_path_aa.txt"` |
| 67 | data | `if (pco%wb_hru%a == "y" .and. cs_db%num_tot > 0) then > if (pco%csvout == "y") then` | `"HRU_PATH                  hru_path_aa.csv"` |


- Procedure: `header_pest`
- Writer: `header_pest.f90`
- Match: source_output
- Resolved default filename(s): `files_out.out`

| Line | Role | Condition | Fields written |
| --- | --- | --- | --- |
| 20 | data | `if (sp_ob%hru > 0) then > if (pco%pest%d == "y" .and. cs_db%num_tot > 0) then` | `"HRU_PEST                  hru_pest_day.txt"` |
| 27 | data | `if (sp_ob%hru > 0) then > if (pco%pest%d == "y" .and. cs_db%num_tot > 0) then > if (pco%csvout == "y") then` | `"HRU_PEST                  hru_pest_day.csv"` |
| 35 | data | `if (sp_ob%hru > 0) then > if (pco%pest%m == "y" .and. cs_db%num_tot > 0 ) then` | `"HRU_PEST                  hru_pest_mon.txt"` |
| 42 | data | `if (sp_ob%hru > 0) then > if (pco%pest%m == "y" .and. cs_db%num_tot > 0 ) then > if (pco%csvout == "y") then` | `"HRU_PEST                  hru_pest_mon.csv"` |
| 50 | data | `if (sp_ob%hru > 0) then > if (pco%pest%y == "y" .and. cs_db%num_tot > 0) then` | `"HRU_PEST                  hru_pest_yr.txt"` |
| 57 | data | `if (sp_ob%hru > 0) then > if (pco%pest%y == "y" .and. cs_db%num_tot > 0) then > if (pco%csvout == "y") then` | `"HRU_PEST                  hru_pest_yr.csv"` |
| 65 | data | `if (sp_ob%hru > 0) then > if (pco%pest%a == "y" .and. cs_db%num_tot > 0) then` | `"HRU_PEST                  hru_pest_aa.txt"` |
| 72 | data | `if (sp_ob%hru > 0) then > if (pco%pest%a == "y" .and. cs_db%num_tot > 0) then > if (pco%csvout == "y") then` | `"HRU_PEST                  hru_pest_aa.csv"` |
| 84 | data | `if (sp_ob%chandeg > 0) then > if (pco%pest%d == "y" .and. cs_db%num_tot > 0) then` | `"CHANNEL_PEST              channel_pest_day.txt"` |
| 91 | data | `if (sp_ob%chandeg > 0) then > if (pco%pest%d == "y" .and. cs_db%num_tot > 0) then > if (pco%csvout == "y") then` | `"CHANNEL_PEST              channel_pest_day.csv"` |
| 99 | data | `if (sp_ob%chandeg > 0) then > if (pco%pest%m == "y" .and. cs_db%num_tot > 0 ) then` | `"CHANNEL_PEST              channel_pest_mon.txt"` |
| 106 | data | `if (sp_ob%chandeg > 0) then > if (pco%pest%m == "y" .and. cs_db%num_tot > 0 ) then > if (pco%csvout == "y") then` | `"CHANNEL_PEST              channel_pest_mon.csv"` |
| 114 | data | `if (sp_ob%chandeg > 0) then > if (pco%pest%y == "y" .and. cs_db%num_tot > 0) then` | `"CHANNEL_PEST              channel_pest_yr.txt"` |
| 121 | data | `if (sp_ob%chandeg > 0) then > if (pco%pest%y == "y" .and. cs_db%num_tot > 0) then > if (pco%csvout == "y") then` | `"CHANNEL_PEST              channel_pest_yr.csv"` |
| 129 | data | `if (sp_ob%chandeg > 0) then > if (pco%pest%a == "y" .and. cs_db%num_tot > 0) then` | `"CHANNEL_PEST              channel_pest_aa.txt"` |
| 136 | data | `if (sp_ob%chandeg > 0) then > if (pco%pest%a == "y" .and. cs_db%num_tot > 0) then > if (pco%csvout == "y") then` | `"CHANNEL_PEST              channel_pest_aa.csv"` |
| 148 | data | `if (sp_ob%res > 0) then > if (pco%pest%d == "y" .and. cs_db%num_tot > 0) then` | `"RESERVOIR_PEST            reservoir_pest_day.txt"` |
| 155 | data | `if (sp_ob%res > 0) then > if (pco%pest%d == "y" .and. cs_db%num_tot > 0) then > if (pco%csvout == "y") then` | `"RESERVOIR_PEST            reservoir_pest_day.csv"` |
| 163 | data | `if (sp_ob%res > 0) then > if (pco%pest%m == "y" .and. cs_db%num_tot > 0 ) then` | `"RESERVOIR_PEST            reservoir_pest_mon.txt"` |
| 170 | data | `if (sp_ob%res > 0) then > if (pco%pest%m == "y" .and. cs_db%num_tot > 0 ) then > if (pco%csvout == "y") then` | `"RESERVOIR_PEST            reservoir_pest_mon.csv"` |
| 178 | data | `if (sp_ob%res > 0) then > if (pco%pest%y == "y" .and. cs_db%num_tot > 0) then` | `"RESERVOIR_PEST            reservoir_pest_yr.txt"` |
| 185 | data | `if (sp_ob%res > 0) then > if (pco%pest%y == "y" .and. cs_db%num_tot > 0) then > if (pco%csvout == "y") then` | `"RESERVOIR_PEST            reservoir_pest_yr.csv"` |
| 193 | data | `if (sp_ob%res > 0) then > if (pco%pest%a == "y" .and. cs_db%num_tot > 0) then` | `"RESERVOIR_PEST            reservoir_pest_aa.txt"` |
| 200 | data | `if (sp_ob%res > 0) then > if (pco%pest%a == "y" .and. cs_db%num_tot > 0) then > if (pco%csvout == "y") then` | `"RESERVOIR_PEST            reservoir_pest_aa.csv"` |
| 212 | data | `if (sp_ob%aqu > 0) then > if (pco%pest%d == "y" .and. cs_db%num_tot > 0) then` | `"BASIN_AQUIFER_PEST        basin_aqu_pest_day.txt"` |
| 219 | data | `if (sp_ob%aqu > 0) then > if (pco%pest%d == "y" .and. cs_db%num_tot > 0) then > if (pco%csvout == "y") then` | `"BASIN_AQUIFER_PEST        basin_aqu_pest_day.csv"` |
| 227 | data | `if (sp_ob%aqu > 0) then > if (pco%pest%m == "y" .and. cs_db%num_tot > 0 ) then` | `"BASIN_AQUIFER_PEST        basin_aqu_pest_mon.txt"` |
| 234 | data | `if (sp_ob%aqu > 0) then > if (pco%pest%m == "y" .and. cs_db%num_tot > 0 ) then > if (pco%csvout == "y") then` | `"BASIN_AQUIFER_PEST        basin_aqu_pest_mon.csv"` |
| 242 | data | `if (sp_ob%aqu > 0) then > if (pco%pest%y == "y" .and. cs_db%num_tot > 0) then` | `"BASIN_AQUIFER_PEST        basin_aqu_pest_yr.txt"` |
| 249 | data | `if (sp_ob%aqu > 0) then > if (pco%pest%y == "y" .and. cs_db%num_tot > 0) then > if (pco%csvout == "y") then` | `"BASIN_AQUIFER_PEST        basin_aqu_pest_yr.csv"` |
| 257 | data | `if (sp_ob%aqu > 0) then > if (pco%pest%a == "y" .and. cs_db%num_tot > 0) then` | `"BASIN_AQUIFER_PEST        basin_aqu_pest_aa.txt"` |
| 264 | data | `if (sp_ob%aqu > 0) then > if (pco%pest%a == "y" .and. cs_db%num_tot > 0) then > if (pco%csvout == "y") then` | `"BASIN_AQUIFER_PEST        basin_aqu_pest_aa.csv"` |
| 276 | data | `if (sp_ob%aqu > 0) then > if (pco%pest%d == "y" .and. cs_db%num_tot > 0) then` | `"AQUIFER_PEST              aquifer_pest_day.txt"` |
| 283 | data | `if (sp_ob%aqu > 0) then > if (pco%pest%d == "y" .and. cs_db%num_tot > 0) then > if (pco%csvout == "y") then` | `"AQUIFER_PEST              aquifer_pest_day.csv"` |
| 291 | data | `if (sp_ob%aqu > 0) then > if (pco%pest%m == "y" .and. cs_db%num_tot > 0 ) then` | `"AQUIFER_PEST              aquifer_pest_mon.txt"` |
| 298 | data | `if (sp_ob%aqu > 0) then > if (pco%pest%m == "y" .and. cs_db%num_tot > 0 ) then > if (pco%csvout == "y") then` | `"AQUIFER_PEST              aquifer_pest_mon.csv"` |
| 306 | data | `if (sp_ob%aqu > 0) then > if (pco%pest%y == "y" .and. cs_db%num_tot > 0) then` | `"AQUIFER_PEST              aquifer_pest_yr.txt"` |
| 313 | data | `if (sp_ob%aqu > 0) then > if (pco%pest%y == "y" .and. cs_db%num_tot > 0) then > if (pco%csvout == "y") then` | `"AQUIFER_PEST              aquifer_pest_yr.csv"` |
| 321 | data | `if (sp_ob%aqu > 0) then > if (pco%pest%a == "y" .and. cs_db%num_tot > 0) then` | `"AQUIFER_PEST              aquifer_pest_aa.txt"` |
| 328 | data | `if (sp_ob%aqu > 0) then > if (pco%pest%a == "y" .and. cs_db%num_tot > 0) then > if (pco%csvout == "y") then` | `"AQUIFER_PEST              aquifer_pest_aa.csv"` |
| 340 | data | `if (sp_ob%chandeg > 0) then > if (pco%pest%d == "y" .and. cs_db%num_tot > 0) then` | `"BASIN_CH_PEST             basin_ch_pest_day.txt"` |
| 347 | data | `if (sp_ob%chandeg > 0) then > if (pco%pest%d == "y" .and. cs_db%num_tot > 0) then > if (pco%csvout == "y") then` | `"BASIN_CH_PEST             reservoir_pest_day.csv"` |
| 355 | data | `if (sp_ob%chandeg > 0) then > if (pco%pest%m == "y" .and. cs_db%num_tot > 0 ) then` | `"BASIN_CH_PEST             basin_ch_pest_mon.txt"` |
| 362 | data | `if (sp_ob%chandeg > 0) then > if (pco%pest%m == "y" .and. cs_db%num_tot > 0 ) then > if (pco%csvout == "y") then` | `"BASIN_CH_PEST             basin_ch_pest_mon.csv"` |
| 370 | data | `if (sp_ob%chandeg > 0) then > if (pco%pest%y == "y" .and. cs_db%num_tot > 0) then` | `"BASIN_CH_PEST             basin_ch_pest_yr.txt"` |
| 377 | data | `if (sp_ob%chandeg > 0) then > if (pco%pest%y == "y" .and. cs_db%num_tot > 0) then > if (pco%csvout == "y") then` | `"BASIN_CH_PEST             basin_ch_pest_yr.csv"` |
| 385 | data | `if (sp_ob%chandeg > 0) then > if (pco%pest%a == "y" .and. cs_db%num_tot > 0) then` | `"BASIN_CH_PEST             basin_ch_pest_aa.txt"` |
| 392 | data | `if (sp_ob%chandeg > 0) then > if (pco%pest%a == "y" .and. cs_db%num_tot > 0) then > if (pco%csvout == "y") then` | `"BASIN_CH_PEST             basin_ch_pest_aa.csv"` |
| 404 | data | `if (sp_ob%res > 0) then > if (pco%pest%d == "y" .and. cs_db%num_tot > 0) then` | `"BASIN_RES_PEST            basin_res_pest_day.txt"` |
| 411 | data | `if (sp_ob%res > 0) then > if (pco%pest%d == "y" .and. cs_db%num_tot > 0) then > if (pco%csvout == "y") then` | `"BASIN_RES_PEST          reservoir_pest_day.csv"` |
| 419 | data | `if (sp_ob%res > 0) then > if (pco%pest%m == "y" .and. cs_db%num_tot > 0 ) then` | `"BASIN_RES_PEST            basin_res_pest_mon.txt"` |
| 426 | data | `if (sp_ob%res > 0) then > if (pco%pest%m == "y" .and. cs_db%num_tot > 0 ) then > if (pco%csvout == "y") then` | `"BASIN_RES_PEST            basin_res_pest_mon.csv"` |
| 434 | data | `if (sp_ob%res > 0) then > if (pco%pest%y == "y" .and. cs_db%num_tot > 0) then` | `"BASIN_RES_PEST            basin_res_pest_yr.txt"` |
| 441 | data | `if (sp_ob%res > 0) then > if (pco%pest%y == "y" .and. cs_db%num_tot > 0) then > if (pco%csvout == "y") then` | `"BASIN_RES_PEST            basin_res_pest_yr.csv"` |
| 449 | data | `if (sp_ob%res > 0) then > if (pco%pest%a == "y" .and. cs_db%num_tot > 0) then` | `"BASIN_RES_PEST            basin_res_pest_aa.txt"` |
| 456 | data | `if (sp_ob%res > 0) then > if (pco%pest%a == "y" .and. cs_db%num_tot > 0) then > if (pco%csvout == "y") then` | `"BASIN_RES_PEST            basin_res_pest_aa.csv"` |
| 468 | data | `if (sp_ob%hru > 0) then > if (pco%pest%d == "y" .and. cs_db%num_tot > 0) then` | `"BASIN_LS_PEST             basin_ls_pest_day.txt"` |
| 475 | data | `if (sp_ob%hru > 0) then > if (pco%pest%d == "y" .and. cs_db%num_tot > 0) then > if (pco%csvout == "y") then` | `"BASIN_LS_PEST             basin_ls_pest_day.csv"` |
| 483 | data | `if (sp_ob%hru > 0) then > if (pco%pest%m == "y" .and. cs_db%num_tot > 0 ) then` | `"BASIN_LS_PEST             basin_ls_pest_mon.txt"` |
| 490 | data | `if (sp_ob%hru > 0) then > if (pco%pest%m == "y" .and. cs_db%num_tot > 0 ) then > if (pco%csvout == "y") then` | `"BASIN_LS_PEST             basin_ls_pest_mon.csv"` |
| 498 | data | `if (sp_ob%hru > 0) then > if (pco%pest%y == "y" .and. cs_db%num_tot > 0) then` | `"BASIN_LS_PEST             basin_ls_pest_yr.txt"` |
| 505 | data | `if (sp_ob%hru > 0) then > if (pco%pest%y == "y" .and. cs_db%num_tot > 0) then > if (pco%csvout == "y") then` | `"BASIN_LS_PEST             basin_ls_pest_yr.csv"` |
| 513 | data | `if (sp_ob%hru > 0) then > if (pco%pest%a == "y" .and. cs_db%num_tot > 0) then` | `"BASIN_LS_PEST             basin_ls_pest_aa.txt"` |
| 520 | data | `if (sp_ob%hru > 0) then > if (pco%pest%a == "y" .and. cs_db%num_tot > 0) then > if (pco%csvout == "y") then` | `"BASIN_LS_PEST             basin_ls_pest_aa.csv"` |


- Procedure: `header_reservoir`
- Writer: `header_reservoir.f90`
- Match: source_output
- Resolved default filename(s): `files_out.out`

| Line | Role | Condition | Fields written |
| --- | --- | --- | --- |
| 17 | data | `if (pco%res%d == "y" .and. sp_ob%res > 0 ) then` | `"RES                       reservoir_day.txt"` |
| 25 | data | `if (pco%res%d == "y" .and. sp_ob%res > 0 ) then > if (pco%csvout == "y") then` | `"RES                       reservoir_day.csv"` |
| 32 | data | `if (pco%res%m == "y" .and. sp_ob%res > 0 ) then` | `"RES                       reservoir_mon.txt"` |
| 47 | data | `if (pco%res%y == "y" .and. sp_ob%res > 0 ) then` | `"RES                       reservoir_yr.txt"` |
| 55 | data | `if (pco%res%y == "y" .and. sp_ob%res > 0 ) then > if (pco%csvout == "y") then` | `"RES                       reservoir_yr.csv"` |
| 64 | data | `if (pco%res%a == "y" .and. sp_ob%res > 0) then` | `"RES                       reservoir_aa.txt"` |
| 70 | data | `if (pco%res%a == "y" .and. sp_ob%res > 0) then > if (pco%csvout == "y") then` | `"RES                       reservoir_aa.csv"` |


- Procedure: `header_sd_channel`
- Writer: `header_sd_channel.f90`
- Match: source_output
- Resolved default filename(s): `files_out.out`

| Line | Role | Condition | Fields written |
| --- | --- | --- | --- |
| 19 | data | `if (sp_ob%chandeg > 0) then > if (pco%sd_chan%d == "y") then > if (time%step > 1) then` | `"SWAT-DEG_CHANNEL         channel_sd_subday.txt"` |
| 25 | data | `if (sp_ob%chandeg > 0) then > if (pco%sd_chan%d == "y") then > if (time%step > 1) then > if (pco%csvout == "y") then` | `"SWAT-DEG_CHANNEL          channel_sd_subday.csv"` |
| 33 | data | `if (sp_ob%chandeg > 0) then > if (pco%sd_chan%d == "y") then` | `"SWAT-DEG_CHANNEL          channel_sd_day.txt"` |
| 45 | data | `if (sp_ob%chandeg > 0) then > if (pco%sd_chan%d == "y") then > if (pco%csvout == "y") then` | `"SWAT-DEG_CHANNEL          channel_sd_day.csv"` |
| 62 | data | `if (sp_ob%chandeg > 0) then > if (pco%sd_chan%m == "y") then` | `"SWAT-DEG_CHANNEL          channel_sd_mon.txt"` |
| 75 | data | `if (sp_ob%chandeg > 0) then > if (pco%sd_chan%m == "y") then > if (pco%csvout == "y") then` | `"SWAT-DEG_CHANNEL          channel_sd_mon.csv"` |
| 92 | data | `if (sp_ob%chandeg > 0) then > if (pco%sd_chan%y == "y") then` | `"SWAT-DEG_CHANNEL          channel_sd_yr.txt"` |
| 105 | data | `if (sp_ob%chandeg > 0) then > if (pco%sd_chan%y == "y") then > if (pco%csvout == "y") then` | `"SWAT-DEG_CHANNEL          channel_sd_yr.csv"` |
| 122 | data | `if (sp_ob%chandeg > 0) then > if (pco%sd_chan%a == "y") then` | `"SWAT-DEG_CHANNEL          channel_sd_aa.txt"` |
| 135 | data | `if (sp_ob%chandeg > 0) then > if (pco%sd_chan%a == "y") then > if (pco%csvout == "y") then` | `"SWAT-DEG_CHANNEL          channel_sd_aa.csv"` |
| 154 | data | `if (sp_ob%chandeg > 0) then > if (pco%sd_chan%d == "y") then` | `"SWAT-DEG_CHANNEL_MORPH    channel_sdmorph_day.txt"` |
| 160 | data | `if (sp_ob%chandeg > 0) then > if (pco%sd_chan%d == "y") then > if (pco%csvout == "y") then` | `"SWAT-DEG_CHANNEL_MORPH    channel_sdmorph_day.csv"` |
| 171 | data | `if (sp_ob%chandeg > 0) then > if (pco%sd_chan%m == "y") then` | `"SWAT-DEG_CHANNEL_MORPH    channel_sdmorph_mon.txt"` |
| 177 | data | `if (sp_ob%chandeg > 0) then > if (pco%sd_chan%m == "y") then > if (pco%csvout == "y") then` | `"SWAT-DEG_CHANNEL_MORPH    channel_sdmorph_mon.csv"` |
| 188 | data | `if (sp_ob%chandeg > 0) then > if (pco%sd_chan%y == "y") then` | `"SWAT-DEG_CHANNEL_MORPH    channel_sdmorph_yr.txt"` |
| 194 | data | `if (sp_ob%chandeg > 0) then > if (pco%sd_chan%y == "y") then > if (pco%csvout == "y") then` | `"SWAT-DEG_CHANNEL_MORPH    channel_sdmorph_yr.csv"` |
| 205 | data | `if (sp_ob%chandeg > 0) then > if (pco%sd_chan%a == "y") then` | `"SWAT-DEG_CHANNEL_MORPH    channel_sdmorph_aa.txt"` |
| 211 | data | `if (sp_ob%chandeg > 0) then > if (pco%sd_chan%a == "y") then > if (pco%csvout == "y") then` | `"SWAT-DEG_CHANNEL_MORPH    channel_sdmorph_aa.csv"` |
| 223 | data | `if (pco%sd_chan%d == "y") then` | `"SWAT_DEG_CHAN_BUD         sd_chanbud_day.txt"` |
| 229 | data | `if (pco%sd_chan%d == "y") then > if (pco%csvout == "y") then` | `"SWAT_DEG_CHAN_BUD         sd_chanbud_day.csv"` |
| 238 | data | `if (pco%sd_chan%m == "y") then` | `"SWAT_DEG_CHAN_BUD         sd_chanbud_mon.txt"` |
| 244 | data | `if (pco%sd_chan%m == "y") then > if (pco%csvout == "y") then` | `"SWAT_DEG_CHAN_BUD         sd_chanbud_mon.csv"` |
| 253 | data | `if (pco%sd_chan%y == "y") then` | `"SWAT_DEG_CHAN_BUD         sd_chanbud_yr.txt"` |
| 259 | data | `if (pco%sd_chan%y == "y") then > if (pco%csvout == "y") then` | `"SWAT_DEG_CHAN_BUD         sd_chanbud_yr.csv"` |
| 268 | data | `if (pco%sd_chan%a == "y") then` | `"SWAT_DEG_CHAN_BUD         sd_chanbud_aa.txt"` |
| 274 | data | `if (pco%sd_chan%a == "y") then > if (pco%csvout == "y") then` | `"SWAT_DEG_CHAN_BUD         sd_chanbud_aa.csv"` |
| 285 | data | `if (sp_ob%chandeg > 0) then` | `"SWAT_DEG_CHANBUD        chanbud.txt"` |
| 295 | data | `if (sp_ob%chandeg > 0) then` | `"CHANBUD_ORDER         chanbud_order.txt"` |
| 305 | data | `if (sp_ob%chandeg > 0) then` | `"BASIN SEDBUD          bsn_sedbud.txt"` |


- Procedure: `header_snutc`
- Writer: `header_snutc.f90`
- Match: source_output
- Resolved default filename(s): `files_out.out`

| Line | Role | Condition | Fields written |
| --- | --- | --- | --- |
| 13 | data | `if (sp_ob%hru > 0) then` | `"HRU_ORGC                  hru_orgc.txt"` |


- Procedure: `header_water_allocation`
- Writer: `header_water_allocation.f90`
- Match: source_output
- Resolved default filename(s): `files_out.out`

| Line | Role | Condition | Fields written |
| --- | --- | --- | --- |
| 16 | data | `if (pco%water_allo%d == "y") then` | `"WATER_ALLOCATION          water_allo_day.txt"` |
| 22 | data | `if (pco%water_allo%d == "y") then > if (pco%csvout == "y") then` | `"WATER_ALLOCATION          water_allo_day.csv"` |
| 31 | data | `if (pco%water_allo%m == "y") then` | `"WATER_ALLOCATION          water_allo_mon.txt"` |
| 37 | data | `if (pco%water_allo%m == "y") then > if (pco%csvout == "y") then` | `"WATER_ALLOCATION          water_allo_mon.csv"` |
| 46 | data | `if (pco%water_allo%y == "y") then` | `"WATER_ALLOCATION          water_allo_yr.txt"` |
| 52 | data | `if (pco%water_allo%y == "y") then > if (pco%csvout == "y") then` | `"WATER_ALLOCATION          water_allo_yr.csv"` |
| 61 | data | `if (pco%water_allo%a == "y") then` | `"WATER_ALLOCATION          water_allo_aa.txt"` |
| 67 | data | `if (pco%water_allo%a == "y") then > if (pco%csvout == "y") then` | `"WATER_ALLOCATION          water_allo_aa.csv"` |
| 77 | data | `if (pco%water_allo%d == "y") then` | `"WATER_ALLOCATION          wallo_use_day.txt"` |
| 83 | data | `if (pco%water_allo%d == "y") then > if (pco%csvout == "y") then` | `"WATER_ALLOCATION          wallo_use_day.csv"` |
| 92 | data | `if (pco%water_allo%m == "y") then` | `"WATER_ALLOCATION          wallo_use_mon.txt"` |
| 98 | data | `if (pco%water_allo%m == "y") then > if (pco%csvout == "y") then` | `"WATER_ALLOCATION          wallo_use_mon.csv"` |
| 107 | data | `if (pco%water_allo%y == "y") then` | `"WATER_ALLOCATION          wallo_use_yr.txt"` |
| 113 | data | `if (pco%water_allo%y == "y") then > if (pco%csvout == "y") then` | `"WATER_ALLOCATION          wallo_use_yr.csv"` |
| 122 | data | `if (pco%water_allo%a == "y") then` | `"WATER_ALLOCATION          wallo_use_aa.txt"` |
| 128 | data | `if (pco%water_allo%a == "y") then > if (pco%csvout == "y") then` | `"WATER_ALLOCATION          wallo_use_aa.csv"` |
| 138 | data | `if (pco%water_allo%d == "y") then` | `"WATER_ALLOCATION          wallo_treat_day.txt"` |
| 144 | data | `if (pco%water_allo%d == "y") then > if (pco%csvout == "y") then` | `"WATER_ALLOCATION          wallo_treat_day.csv"` |
| 153 | data | `if (pco%water_allo%m == "y") then` | `"WATER_ALLOCATION          wallo_treat_mon.txt"` |
| 159 | data | `if (pco%water_allo%m == "y") then > if (pco%csvout == "y") then` | `"WATER_ALLOCATION          wallo_treat_mon.csv"` |
| 168 | data | `if (pco%water_allo%y == "y") then` | `"WATER_ALLOCATION          wallo_treat_yr.txt"` |
| 174 | data | `if (pco%water_allo%y == "y") then > if (pco%csvout == "y") then` | `"WATER_ALLOCATION          wallo_treat_yr.csv"` |
| 183 | data | `if (pco%water_allo%a == "y") then` | `"WATER_ALLOCATION          wallo_treat_aa.txt"` |
| 189 | data | `if (pco%water_allo%a == "y") then > if (pco%csvout == "y") then` | `"WATER_ALLOCATION          wallo_treat_aa.csv"` |


- Procedure: `header_wetland`
- Writer: `header_wetland.f90`
- Match: source_output
- Resolved default filename(s): `files_out.out`

| Line | Role | Condition | Fields written |
| --- | --- | --- | --- |
| 14 | data | `if (pco%res%d == "y") then` | `"RES_WET                   wetland_day.txt"` |
| 22 | data | `if (pco%res%d == "y") then > if (pco%csvout == "y") then` | `"RES_WET                   wetland_day.csv"` |
| 30 | data | `if (pco%res%m == "y") then` | `"RES_WET                   wetland_mon.txt"` |
| 38 | data | `if (pco%res%m == "y") then > if (pco%csvout == "y") then` | `"RES_WET                   wetland_mon.csv"` |
| 46 | data | `if (pco%res%y == "y") then` | `"RES_WET                   wetland_yr.txt"` |
| 54 | data | `if (pco%res%y == "y") then > if (pco%csvout == "y") then` | `"RES_WET                   wetland_yr.csv"` |
| 65 | data | `if (pco%res%a == "y") then` | `"RES_WET                   wetland_aa.txt"` |
| 72 | data | `if (pco%res%a == "y") then > if (pco%csvout == "y") then` | `"RES_WET                   wetland_aa.csv"` |


- Procedure: `header_write`
- Writer: `header_write.f90`
- Match: source_output
- Resolved default filename(s): `files_out.out`

| Line | Role | Condition | Fields written |
| --- | --- | --- | --- |
| 19 | data | `if (pco%fdcout == "y") then` | `"FDC                       flow_duration_curve.out"` |
| 28 | data | `if (cal_soft == "y") then` | `"HRU_SOFT_CALIB_OUT        hru-out.cal"` |
| 64 | data | `if (pco%aqu_bsn%d == "y") then` | `"BASIN_AQUIFER             basin_aqu_day.txt"` |
| 70 | data | `if (pco%aqu_bsn%d == "y") then > if (pco%csvout == "y") then` | `"BASIN_AQUIFER             basin_aqu_day.csv"` |
| 79 | data | `if (pco%aqu_bsn%m == "y") then` | `"BASIN_AQUIFER             basin_aqu_mon.txt"` |
| 85 | data | `if (pco%aqu_bsn%m == "y") then > if (pco%csvout == "y") then` | `"BASIN_AQUIFER             basin_aqu_mon.csv"` |
| 94 | data | `if (pco%aqu_bsn%y == "y") then` | `"BASIN_AQUIFER             basin_aqu_yr.txt"` |
| 100 | data | `if (pco%aqu_bsn%y == "y") then > if (pco%csvout == "y") then` | `"BASIN_AQUIFER             basin_aqu_yr.csv"` |
| 109 | data | `if (pco%aqu_bsn%a == "y") then` | `"BASIN_AQUIFER             basin_aqu_aa.txt"` |
| 115 | data | `if (pco%aqu_bsn%a == "y") then > if (pco%csvout == "y") then` | `"BASIN_AQUIFER             basin_aqu_aa.csv"` |
| 126 | data | `if (pco%res_bsn%d == "y") then` | `"BASIN_RESERVOIR           basin_res_day.txt"` |
| 132 | data | `if (pco%res_bsn%d == "y") then > if (pco%csvout == "y") then` | `"BASIN_RESERVOIR           basin_res_day.csv"` |
| 141 | data | `if (pco%res_bsn%m == "y") then` | `"BASIN_RESERVOIR           basin_res_mon.txt"` |
| 147 | data | `if (pco%res_bsn%m == "y") then > if (pco%csvout == "y") then` | `"BASIN_RESERVOIR           basin_res_mon.csv"` |
| 156 | data | `if (pco%res_bsn%y == "y") then` | `"BASIN_RESERVOIR           basin_res_yr.txt"` |
| 162 | data | `if (pco%res_bsn%y == "y") then > if (pco%csvout == "y") then` | `"BASIN_RESERVOIR           basin_res_yr.csv"` |
| 171 | data | `if (pco%res_bsn%a == "y") then` | `"BASIN_RESERVOIR           basin_res_aa.txt"` |
| 177 | data | `if (pco%res_bsn%a == "y") then > if (pco%csvout == "y") then` | `"BASIN_RESERVOIR           basin_res_aa.csv"` |
| 188 | data | `if (pco%recall%d == "y") then` | `"RECALL                    recall_day.txt"` |
| 194 | data | `if (pco%recall%d == "y") then > if (pco%csvout == "y") then` | `"RECALL                    recall_day.csv"` |
| 203 | data | `if (pco%recall%m == "y") then` | `"RECALL                    recall_mon.txt"` |
| 209 | data | `if (pco%recall%m == "y") then > if (pco%csvout == "y") then` | `"RECALL                    recall_mon.csv"` |
| 218 | data | `if (pco%recall%y == "y") then` | `"RECALL                    recall_yr.txt"` |
| 224 | data | `if (pco%recall%y == "y") then > if (pco%csvout == "y") then` | `"RECALL                    recall_yr.csv"` |
| 233 | data | `if (pco%recall%a == "y") then` | `"RECALL_AA                 recall_aa.txt"` |
| 239 | data | `if (pco%recall%a == "y") then > if (pco%csvout == "y") then` | `"RECALL                    recall_aa.csv"` |
| 251 | data | `if (pco%chan_bsn%d == "y") then` | `"BASIN_CHANNEL             basin_cha_day.txt"` |
| 257 | data | `if (pco%chan_bsn%d == "y") then > if (pco%csvout == "y") then` | `"BASIN_CHANNEL             basin_cha_day.txt"` |
| 266 | data | `if (pco%chan_bsn%m == "y") then` | `"BASIN_CHANNEL             basin_cha_mon.txt"` |
| 272 | data | `if (pco%chan_bsn%m == "y") then > if (pco%csvout == "y") then` | `"BASIN_CHANNEL             basin_cha_mon.txt"` |
| 281 | data | `if (pco%chan_bsn%y == "y") then` | `"BASIN_CHANNEL             basin_cha_yr.txt"` |
| 287 | data | `if (pco%chan_bsn%y == "y") then > if (pco%csvout == "y") then` | `"BASIN_CHANNEL             basin_cha_yr.csv"` |
| 296 | data | `if (pco%chan_bsn%a == "y") then` | `"BASIN_CHANNEL             basin_cha_aa.txt"` |
| 302 | data | `if (pco%chan_bsn%a == "y") then > if (pco%csvout == "y") then` | `"BASIN_CHANNEL             basin_cha_aa.csv"` |
| 313 | data | `if (pco%sd_chan_bsn%d == "y") then` | `"BASIN_SWAT_DEG_CHANNEL    basin_sd_cha_day.txt"` |
| 319 | data | `if (pco%sd_chan_bsn%d == "y") then > if (pco%csvout == "y") then` | `"BASIN_SWAT_DEG_CHANNEL    basin_sd_cha_day.csv"` |
| 328 | data | `if (pco%sd_chan_bsn%m == "y") then` | `"BASIN_SWAT_DEG_CHANNEL    basin_sd_cha_mon.txt"` |
| 334 | data | `if (pco%sd_chan_bsn%m == "y") then > if (pco%csvout == "y") then` | `"BASIN_SWAT_DEG_CHANNEL    basin_sd_cha_mon.csv"` |
| 343 | data | `if (pco%sd_chan_bsn%y == "y") then` | `"BASIN_SWAT_DEG_CHANNEL    basin_sd_cha_yr.txt"` |
| 349 | data | `if (pco%sd_chan_bsn%y == "y") then > if (pco%csvout == "y") then` | `"BASIN_SWAT_DEG_CHANNEL    basin_sd_cha_yr.csv"` |
| 358 | data | `if (pco%sd_chan_bsn%a == "y") then` | `"BASIN_SWAT_DEG_CHANNEL    basin_sd_cha_aa.txt"` |
| 364 | data | `if (pco%sd_chan_bsn%a == "y") then > if (pco%csvout == "y") then` | `"BASIN_SWAT_DEG_CHANNEL    basin_sd_cha_aa.csv"` |
| 376 | data | `if (pco%sd_chan_bsn%d == "y") then` | `"BASIN_SWAT_DEG_CHAN_MORPH basin_sd_chamorph_day.txt"` |
| 382 | data | `if (pco%sd_chan_bsn%d == "y") then > if (pco%csvout == "y") then` | `"BASIN_SWAT_DEG_CHAN_MORPH basin_sd_chamorph_day.csv"` |
| 391 | data | `if (pco%sd_chan_bsn%m == "y") then` | `"BASIN_SWAT_DEG_CHAN_MORPH basin_sd_chamorph_mon.txt"` |
| 397 | data | `if (pco%sd_chan_bsn%m == "y") then > if (pco%csvout == "y") then` | `"BASIN_SWAT_DEG_CHAN_MORPH basin_sd_chamorph_mon.csv"` |
| 406 | data | `if (pco%sd_chan_bsn%y == "y") then` | `"BASIN_SWAT_DEG_CHAN_MORPH basin_sd_chamorph_yr.txt"` |
| 412 | data | `if (pco%sd_chan_bsn%y == "y") then > if (pco%csvout == "y") then` | `"BASIN_SWAT_DEG_CHAN_MORPH basin_sd_chamorph_yr.csv"` |
| 421 | data | `if (pco%sd_chan_bsn%a == "y") then` | `"BASIN_SWAT_DEG_CHAN_MORPH basin_sd_chamorph_aa.txt"` |
| 427 | data | `if (pco%sd_chan_bsn%a == "y") then > if (pco%csvout == "y") then` | `"BASIN_SWAT_DEG_CHAN_MORPH basin_sd_chamorph_aa.csv"` |
| 438 | data | `if (pco%sd_chan_bsn%d == "y") then` | `"BASIN_SWAT_DEG_CHAN_BUD   basin_sd_chanbud_day.txt"` |
| 444 | data | `if (pco%sd_chan_bsn%d == "y") then > if (pco%csvout == "y") then` | `"BASIN_SWAT_DEG_CHAN_BUD   basin_sd_chanbud_day.csv"` |
| 453 | data | `if (pco%sd_chan_bsn%m == "y") then` | `"BASIN_SWAT_DEG_CHAN_BUD   basin_sd_chanbud_mon.txt"` |
| 459 | data | `if (pco%sd_chan_bsn%m == "y") then > if (pco%csvout == "y") then` | `"BASIN_SWAT_DEG_CHAN_BUD   basin_sd_chanbud_mon.csv"` |
| 468 | data | `if (pco%sd_chan_bsn%y == "y") then` | `"BASIN_SWAT_DEG_CHAN_BUD   basin_sd_chanbud_yr.txt"` |
| 474 | data | `if (pco%sd_chan_bsn%y == "y") then > if (pco%csvout == "y") then` | `"BASIN_SWAT_DEG_CHAN_BUD   basin_sd_chanbud_yr.csv"` |
| 483 | data | `if (pco%sd_chan_bsn%a == "y") then` | `"BASIN_SWAT_DEG_CHAN_BUD   basin_sd_chanbud_aa.txt"` |
| 489 | data | `if (pco%sd_chan_bsn%a == "y") then > if (pco%csvout == "y") then` | `"BASIN_SWAT_DEG_CHAN_BUD   basin_sd_chanbud_aa.csv"` |
| 501 | data | `if (pco%recall_bsn%d == "y") then` | `"BASIN_RECALL              basin_psc_day.txt"` |
| 507 | data | `if (pco%recall_bsn%d == "y") then > if (pco%csvout == "y") then` | `"BASIN_RECALL              basin_psc_day.csv"` |
| 516 | data | `if (pco%recall_bsn%m == "y") then` | `"BASIN_RECALL              basin_psc_mon.txt"` |
| 522 | data | `if (pco%recall_bsn%m == "y") then > if (pco%csvout == "y") then` | `"BASIN_RECALL              basin_psc_mon.csv"` |
| 531 | data | `if (pco%recall_bsn%y == "y") then` | `"BASIN_RECALL              basin_psc_yr.txt"` |
| 537 | data | `if (pco%recall_bsn%y == "y") then > if (pco%csvout == "y") then` | `"BASIN_RECALL              basin_psc_yr.csv"` |
| 546 | data | `if (pco%recall_bsn%a == "y") then` | `"BASIN_RECALL_AA           basin_psc_aa.txt"` |
| 552 | data | `if (pco%recall_bsn%a == "y") then > if (pco%csvout == "y") then` | `"BASIN_RECALL_AA           basin_psc_aa.csv"` |
| 564 | data | `if (pco%ru%d == "y") then` | `"ROUTING_UNITS             ru_day.txt"` |
| 570 | data | `if (pco%ru%d == "y") then > if (pco%csvout == "y") then` | `"ROUTING_UNITS             ru_day.csv"` |
| 579 | data | `if (pco%ru%m == "y") then` | `"ROUTING_UNITS             ru_mon.txt"` |
| 585 | data | `if (pco%ru%m == "y") then > if (pco%csvout == "y") then` | `"ROUTING_UNITS             ru_mon.csv"` |
| 594 | data | `if (pco%ru%y == "y") then` | `"ROUTING_UNITS             ru_yr.txt"` |
| 600 | data | `if (pco%ru%y == "y") then > if (pco%csvout == "y") then` | `"ROUTING_UNITS             ru_yr.csv"` |
| 609 | data | `if (pco%ru%a == "y") then` | `"ROUTING_UNITS             ru_aa.txt"` |
| 615 | data | `if (pco%ru%a == "y") then > if (pco%csvout == "y") then` | `"ROUTING_UNITS             ru_aa.csv"` |


- Procedure: `header_yield`
- Writer: `header_yield.f90`
- Match: source_output
- Resolved default filename(s): `files_out.out`

| Line | Role | Condition | Fields written |
| --- | --- | --- | --- |
| 12 | data | `if (pco%mgtout == "y") then` | `"YLD                       yield.out"` |
| 15 | data | `if (pco%mgtout == "y") then > if (pco%csvout == "y") then` | `"YLD                       yield.csv"` |
| 25 | data | `if (sp_ob%hru > 0 .and. (pco%crop_yld == "y" .or. pco%crop_yld == "b")) then` | `"BASIN_CROP_YLD            basin_crop_yld_yr.txt"` |
| 29 | data | `if (sp_ob%hru > 0 .and. (pco%crop_yld == "y" .or. pco%crop_yld == "b")) then` | `"BASIN_CROP_YLD            basin_crop_yld_aa.txt"` |


- Procedure: `output_landscape_init`
- Writer: `output_landscape_init.f90`
- Match: source_output
- Resolved default filename(s): `files_out.out`

| Line | Role | Condition | Fields written |
| --- | --- | --- | --- |
| 41 | data | `if (sp_ob%hru > 0) then > if (pco%wb_hru%d == "y") then` | `"HRU                       hru_wb_day.txt"` |
| 48 | data | `if (sp_ob%hru > 0) then > if (pco%wb_hru%d == "y") then > if (pco%csvout == "y") then` | `"HRU                       hru_wb_day.csv"` |
| 58 | data | `if (sp_ob%hru > 0) then > if (pco%wb_hru%m == "y") then` | `"HRU                       hru_wb_mon.txt"` |
| 65 | data | `if (sp_ob%hru > 0) then > if (pco%wb_hru%m == "y") then > if (pco%csvout == "y") then` | `"HRU                       hru_wb_mon.csv"` |
| 75 | data | `if (sp_ob%hru > 0) then > if (pco%wb_hru%y == "y") then` | `"HRU                       hru_wb_yr.txt"` |
| 81 | data | `if (sp_ob%hru > 0) then > if (pco%wb_hru%y == "y") then > if (pco%csvout == "y") then` | `"HRU                       hru_wb_yr.csv"` |
| 91 | data | `if (sp_ob%hru > 0) then > if (pco%wb_hru%a == "y") then` | `"HRU                       hru_wb_aa.txt"` |
| 97 | data | `if (sp_ob%hru > 0) then > if (pco%wb_hru%a == "y") then > if (pco%csvout == "y") then` | `"HRU                       hru_wb_aa.csv"` |
| 107 | data | `if (sp_ob%hru > 0) then > if (pco%nb_hru%d == "y") then` | `"HRU                       hru_nb_day.txt"` |
| 113 | data | `if (sp_ob%hru > 0) then > if (pco%nb_hru%d == "y") then > if (pco%csvout == "y") then` | `"HRU                       hru_nb_day.csv"` |
| 123 | data | `if (sp_ob%hru > 0) then > if (pco%nb_hru%d == "y") then` | `"HRU                       hru_ncycle_day.txt"` |
| 129 | data | `if (sp_ob%hru > 0) then > if (pco%nb_hru%d == "y") then > if (pco%csvout == "y") then` | `"HRU                       hru_ncycle_day.csv"` |
| 138 | data | `if (sp_ob%hru > 0) then > if (pco%nb_hru%m == "y") then` | `"HRU                       hru_ncycle_mon.txt"` |
| 144 | data | `if (sp_ob%hru > 0) then > if (pco%nb_hru%m == "y") then > if (pco%csvout == "y") then` | `"HRU                       hru_ncycle_mon.csv"` |
| 153 | data | `if (sp_ob%hru > 0) then > if (pco%nb_hru%y == "y") then` | `"HRU                       hru_ncycle_yr.txt"` |
| 159 | data | `if (sp_ob%hru > 0) then > if (pco%nb_hru%y == "y") then > if (pco%csvout == "y") then` | `"HRU                       hru_ncycle_yr.csv"` |
| 168 | data | `if (sp_ob%hru > 0) then > if (pco%nb_hru%a == "y") then` | `"HRU                       hru_ncycle_aa.txt"` |
| 174 | data | `if (sp_ob%hru > 0) then > if (pco%nb_hru%a == "y") then > if (pco%csvout == "y") then` | `"HRU                       hru_ncycle_aa.csv"` |
| 184 | data | `if (sp_ob%hru > 0) then > if (pco%nb_hru%m == "y") then` | `"HRU                       hru_nb_mon.txt"` |
| 190 | data | `if (sp_ob%hru > 0) then > if (pco%nb_hru%m == "y") then > if (pco%csvout == "y") then` | `"HRU                       hru_nb_mon.csv"` |
| 199 | data | `if (sp_ob%hru > 0) then > if (pco%nb_hru%y == "y") then` | `"HRU                       hru_nb_yr.txt"` |
| 205 | data | `if (sp_ob%hru > 0) then > if (pco%nb_hru%y == "y") then > if (pco%csvout == "y") then` | `"HRU                       hru_nb_yr.csv"` |
| 214 | data | `if (sp_ob%hru > 0) then > if (pco%nb_hru%a == "y") then` | `"HRU                       hru_nb_aa.txt"` |
| 220 | data | `if (sp_ob%hru > 0) then > if (pco%nb_hru%a == "y") then > if (pco%csvout == "y") then` | `"HRU                       hru_nb_aa.csv"` |
| 230 | data | `if (sp_ob%hru > 0) then > if (pco%cb_gl_hru%d == "y") then` | `"HRU                       hru_carb_gl_day.txt"` |
| 236 | data | `if (sp_ob%hru > 0) then > if (pco%cb_gl_hru%d == "y") then > if (pco%csvout == "y") then` | `"HRU                       hru_carb_gl_day.csv"` |
| 245 | data | `if (sp_ob%hru > 0) then > if (pco%cb_gl_hru%m == "y") then` | `"HRU                       hru_carb_gl_mon.txt"` |
| 251 | data | `if (sp_ob%hru > 0) then > if (pco%cb_gl_hru%m == "y") then > if (pco%csvout == "y") then` | `"HRU                       hru_carb_gl_mon.csv"` |
| 260 | data | `if (sp_ob%hru > 0) then > if (pco%cb_gl_hru%y == "y") then` | `"HRU                       hru_carb_gl_yr.txt"` |
| 266 | data | `if (sp_ob%hru > 0) then > if (pco%cb_gl_hru%y == "y") then > if (pco%csvout == "y") then` | `"HRU                       hru_carb_gl_yr.csv"` |
| 275 | data | `if (sp_ob%hru > 0) then > if (pco%cb_gl_hru%a == "y") then` | `"HRU                       hru_carb_gl_aa.txt"` |
| 281 | data | `if (sp_ob%hru > 0) then > if (pco%cb_gl_hru%a == "y") then > if (pco%csvout == "y") then` | `"HRU                       hru_carb_gl_aa.csv"` |
| 293 | data | `if (sp_ob%hru > 0) then > if (pco%cb_trf_hru%d == "y") then` | `"HRU                       hru_scf_day.txt"` |
| 299 | data | `if (sp_ob%hru > 0) then > if (pco%cb_trf_hru%d == "y") then > if (pco%csvout == "y") then` | `"HRU                       hru_scf_day.csv"` |
| 308 | data | `if (sp_ob%hru > 0) then > if (pco%cb_trf_hru%m == "y") then` | `"HRU                       hru_scf_mon.txt"` |
| 314 | data | `if (sp_ob%hru > 0) then > if (pco%cb_trf_hru%m == "y") then > if (pco%csvout == "y") then` | `"HRU                       hru_scf_mon.csv"` |
| 323 | data | `if (sp_ob%hru > 0) then > if (pco%cb_trf_hru%y == "y") then` | `"HRU                       hru_scf_yr.txt"` |
| 329 | data | `if (sp_ob%hru > 0) then > if (pco%cb_trf_hru%y == "y") then > if (pco%csvout == "y") then` | `"HRU                       hru_scf_yr.csv"` |
| 338 | data | `if (sp_ob%hru > 0) then > if (pco%cb_trf_hru%a == "y") then` | `"HRU                       hru_scf_aa.txt"` |
| 344 | data | `if (sp_ob%hru > 0) then > if (pco%cb_trf_hru%a == "y") then > if (pco%csvout == "y") then` | `"HRU                       hru_scf_aa.csv"` |
| 435 | data | `if (sp_ob%hru > 0) then > if (pco%ls_hru%d == "y") then` | `"HRU                       hru_ls_day.txt"` |
| 441 | data | `if (sp_ob%hru > 0) then > if (pco%ls_hru%d == "y") then > if (pco%csvout == "y") then` | `"HRU                       hru_ls_day.csv"` |
| 453 | data | `if (sp_ob%hru > 0) then > if (pco%ls_hru%m == "y") then` | `"HRU                       hru_ls_mon.txt"` |
| 459 | data | `if (sp_ob%hru > 0) then > if (pco%ls_hru%m == "y") then > if (pco%csvout == "y") then` | `"HRU                       hru_ls_mon.csv"` |
| 468 | data | `if (sp_ob%hru > 0) then > if (pco%ls_hru%y == "y") then` | `"HRU                       hru_ls_yr.txt"` |
| 474 | data | `if (sp_ob%hru > 0) then > if (pco%ls_hru%y == "y") then > if (pco%csvout == "y") then` | `"HRU                       hru_ls_yr.csv"` |
| 483 | data | `if (sp_ob%hru > 0) then > if (pco%ls_hru%a == "y") then` | `"HRU                       hru_ls_aa.txt"` |
| 489 | data | `if (sp_ob%hru > 0) then > if (pco%ls_hru%a == "y") then > if (pco%csvout == "y") then` | `"HRU                       hru_ls_aa.csv"` |
| 499 | data | `if (sp_ob%hru > 0) then > if (pco%pw_hru%d == "y") then` | `"HRU                       hru_pw_day.txt"` |
| 505 | data | `if (sp_ob%hru > 0) then > if (pco%pw_hru%d == "y") then > if (pco%csvout == "y") then` | `"HRU                       hru_pw_day.csv"` |
| 514 | data | `if (sp_ob%hru > 0) then > if (pco%pw_hru%m == "y") then` | `"HRU                       hru_pw_mon.txt"` |
| 520 | data | `if (sp_ob%hru > 0) then > if (pco%pw_hru%m == "y") then > if (pco%csvout == "y") then` | `"HRU                       hru_pw_mon.csv"` |
| 529 | data | `if (sp_ob%hru > 0) then > if (pco%pw_hru%y == "y") then` | `"HRU                       hru_pw_yr.txt"` |
| 535 | data | `if (sp_ob%hru > 0) then > if (pco%pw_hru%y == "y") then > if (pco%csvout == "y") then` | `"HRU                       hru_pw_yr.csv"` |
| 544 | data | `if (sp_ob%hru > 0) then > if (pco%pw_hru%a == "y") then` | `"HRU                       hru_pw_aa.txt"` |
| 550 | data | `if (sp_ob%hru > 0) then > if (pco%pw_hru%a == "y") then > if (pco%csvout == "y") then` | `"HRU                       hru_pw_aa.csv"` |
| 563 | data | `if (sp_ob%hru_lte > 0) then > if (pco%wb_sd%d == "y") then` | `"SWAT-DEG                  hru-lte_wb_day.txt"` |
| 569 | data | `if (sp_ob%hru_lte > 0) then > if (pco%wb_sd%d == "y") then > if (pco%csvout == "y") then` | `"SWAT-DEG                  hru-lte_wb_day.csv"` |
| 579 | data | `if (sp_ob%hru_lte > 0) then > if (pco%wb_sd%m == "y") then` | `"SWAT-DEG                  hru-lte_wb_mon.txt"` |
| 585 | data | `if (sp_ob%hru_lte > 0) then > if (pco%wb_sd%m == "y") then > if (pco%csvout == "y") then` | `"SWAT-DEG                  hru-lte_wb_mon.csv"` |
| 596 | data | `if (sp_ob%hru_lte > 0) then > if (sp_ob%hru_lte > 0) then > if (pco%wb_sd%y == "y") then` | `"SWAT-DEG                  hru-lte_wb_yr.txt"` |
| 602 | data | `if (sp_ob%hru_lte > 0) then > if (sp_ob%hru_lte > 0) then > if (pco%wb_sd%y == "y") then > if (pco%csvout == "y") then` | `"SWAT-DEG                  hru-lte_wb_yr.csv"` |
| 613 | data | `if (sp_ob%hru_lte > 0) then > if (pco%wb_sd%a == "y") then` | `"SWAT-DEG                  hru-lte_wb_aa.txt"` |
| 619 | data | `if (sp_ob%hru_lte > 0) then > if (pco%wb_sd%a == "y") then > if (pco%csvout == "y") then` | `"SWAT-DEG                  hru-lte_wb_aa.csv"` |
| 641 | data | `if (sp_ob%hru_lte > 0) then > if (pco%ls_sd%d == "y") then` | `"SWAT-DEG                  hru-lte_ls_day.txt"` |
| 647 | data | `if (sp_ob%hru_lte > 0) then > if (pco%ls_sd%d == "y") then > if (pco%csvout == "y") then` | `"SWAT-DEG                  hru-lte_ls_day.csv"` |
| 656 | data | `if (sp_ob%hru_lte > 0) then > if (pco%ls_sd%m == "y") then` | `"SWAT-DEG                  hru-lte_ls_mon.txt"` |
| 662 | data | `if (sp_ob%hru_lte > 0) then > if (pco%ls_sd%m == "y") then > if (pco%csvout == "y") then` | `"SWAT-DEG                  hru-lte_ls_mon.csv"` |
| 671 | data | `if (sp_ob%hru_lte > 0) then > if (pco%ls_sd%y == "y") then` | `"SWAT-DEG                  hru-lte_ls_yr.txt"` |
| 677 | data | `if (sp_ob%hru_lte > 0) then > if (pco%ls_sd%y == "y") then > if (pco%csvout == "y") then` | `"SWAT-DEG                  hru-lte_ls_yr.csv"` |
| 686 | data | `if (sp_ob%hru_lte > 0) then > if (pco%ls_sd%a == "y") then` | `"SWAT-DEG                  hru-lte_ls_aa.txt"` |
| 692 | data | `if (sp_ob%hru_lte > 0) then > if (pco%ls_sd%a == "y") then > if (pco%csvout == "y") then` | `"SWAT-DEG                  hru-lte_ls_aa.csv"` |
| 703 | data | `if (sp_ob%hru_lte > 0) then > if (pco%pw_sd%d == "y") then` | `"SWAT-DEG                  hru-lte_pw_day.txt"` |
| 709 | data | `if (sp_ob%hru_lte > 0) then > if (pco%pw_sd%d == "y") then > if (pco%csvout == "y") then` | `"SWAT-DEG                  hru-lte_pw_day.csv"` |
| 718 | data | `if (sp_ob%hru_lte > 0) then > if (pco%pw_sd%m == "y") then` | `"SWAT-DEG                  hru-lte_pw_mon.txt"` |
| 724 | data | `if (sp_ob%hru_lte > 0) then > if (pco%pw_sd%m == "y") then > if (pco%csvout == "y") then` | `"SWAT-DEG                  hru-lte_pw_mon.csv"` |
| 733 | data | `if (sp_ob%hru_lte > 0) then > if (pco%pw_sd%y == "y") then` | `"SWAT-DEG                  hru-lte_pw_yr.txt"` |
| 739 | data | `if (sp_ob%hru_lte > 0) then > if (pco%pw_sd%y == "y") then > if (pco%csvout == "y") then` | `"SWAT-DEG                  hru-lte_pw_yr.csv"` |
| 748 | data | `if (sp_ob%hru_lte > 0) then > if (pco%pw_sd%a == "y") then` | `"SWAT-DEG                  hru-lte_pw_aa.txt"` |
| 754 | data | `if (sp_ob%hru_lte > 0) then > if (pco%pw_sd%a == "y") then > if (pco%csvout == "y") then` | `"SWAT-DEG                  hru-lte_pw_aa.csv"` |
| 766 | data | `if (db_mx%lsu_out > 0) then > if (pco%wb_lsu%d == "y") then` | `"ROUTING_UNIT              lsunit_wb_day.txt"` |
| 772 | data | `if (db_mx%lsu_out > 0) then > if (pco%wb_lsu%d == "y") then > if (pco%csvout == "y") then` | `"ROUTING_UNIT              lsunit_wb_day.csv"` |
| 782 | data | `if (db_mx%lsu_out > 0) then > if (pco%wb_lsu%m == "y") then` | `"ROUTING_UNIT              lsunit_wb_mon.txt"` |
| 788 | data | `if (db_mx%lsu_out > 0) then > if (pco%wb_lsu%m == "y") then > if (pco%csvout == "y") then` | `"ROUTING_UNIT              lsunit_wb_mon.csv"` |
| 798 | data | `if (db_mx%lsu_out > 0) then > if (sp_ob%ru > 0) then > if (pco%wb_lsu%y == "y") then` | `"ROUTING_UNIT              lsunit_wb_yr.txt"` |
| 804 | data | `if (db_mx%lsu_out > 0) then > if (sp_ob%ru > 0) then > if (pco%wb_lsu%y == "y") then > if (pco%csvout == "y") then` | `"ROUTING_UNIT              lsunit_wb_yr.csv"` |
| 814 | data | `if (db_mx%lsu_out > 0) then > if (pco%wb_lsu%a == "y") then` | `"ROUTING_UNIT              lsunit_wb_aa.txt"` |
| 820 | data | `if (db_mx%lsu_out > 0) then > if (pco%wb_lsu%a == "y") then > if (pco%csvout == "y") then` | `"ROUTING_UNIT              lsunit_wb_aa.csv"` |
| 830 | data | `if (db_mx%lsu_out > 0) then > if (pco%nb_lsu%d == "y") then` | `"ROUTING_UNIT              lsunit_nb_day.txt"` |
| 836 | data | `if (db_mx%lsu_out > 0) then > if (pco%nb_lsu%d == "y") then > if (pco%csvout == "y") then` | `"ROUTING_UNIT              lsunit_nb_day.csv"` |
| 845 | data | `if (db_mx%lsu_out > 0) then > if (pco%nb_lsu%m == "y") then` | `"ROUTING_UNIT              lsunit_nb_mon.txt"` |
| 851 | data | `if (db_mx%lsu_out > 0) then > if (pco%nb_lsu%m == "y") then > if (pco%csvout == "y") then` | `"ROUTING_UNIT              lsunit_nb_mon.csv"` |
| 860 | data | `if (db_mx%lsu_out > 0) then > if (pco%nb_lsu%y == "y") then` | `"ROUTING_UNIT              lsunit_nb_yr.txt"` |
| 866 | data | `if (db_mx%lsu_out > 0) then > if (pco%nb_lsu%y == "y") then > if (pco%csvout == "y") then` | `"ROUTING_UNIT              lsunit_nb_yr.csv"` |
| 875 | data | `if (db_mx%lsu_out > 0) then > if (pco%nb_lsu%a == "y") then` | `"ROUTING_UNIT              lsunit_nb_aa.txt"` |
| 881 | data | `if (db_mx%lsu_out > 0) then > if (pco%nb_lsu%a == "y") then > if (pco%csvout == "y") then` | `"ROUTING_UNIT              lsunit_nb_aa.csv"` |
| 891 | data | `if (db_mx%lsu_out > 0) then > if (pco%ls_lsu%d == "y") then` | `"ROUTING_UNIT              lsunit_ls_day.txt"` |
| 897 | data | `if (db_mx%lsu_out > 0) then > if (pco%ls_lsu%d == "y") then > if (pco%csvout == "y") then` | `"ROUTING_UNIT              lsunit_ls_day.csv"` |
| 906 | data | `if (db_mx%lsu_out > 0) then > if (pco%ls_lsu%m == "y") then` | `"ROUTING_UNIT              lsunit_ls_mon.txt"` |
| 912 | data | `if (db_mx%lsu_out > 0) then > if (pco%ls_lsu%m == "y") then > if (pco%csvout == "y") then` | `"ROUTING_UNIT              lsunit_ls_mon.csv"` |
| 921 | data | `if (db_mx%lsu_out > 0) then > if (pco%ls_lsu%y == "y") then` | `"ROUTING_UNIT              lsunit_ls_yr.txt"` |
| 927 | data | `if (db_mx%lsu_out > 0) then > if (pco%ls_lsu%y == "y") then > if (pco%csvout == "y") then` | `"ROUTING_UNIT              lsunit_ls_yr.csv"` |
| 936 | data | `if (db_mx%lsu_out > 0) then > if (pco%ls_lsu%a == "y") then` | `"ROUTING_UNIT              lsunit_ls_aa.txt"` |
| 942 | data | `if (db_mx%lsu_out > 0) then > if (pco%ls_lsu%a == "y") then > if (pco%csvout == "y") then` | `"ROUTING_UNIT              lsunit_ls_aa.csv"` |
| 952 | data | `if (db_mx%lsu_out > 0) then > if (pco%pw_lsu%d == "y") then` | `"ROUTING_UNIT              lsunit_pw_day.txt"` |
| 958 | data | `if (db_mx%lsu_out > 0) then > if (pco%pw_lsu%d == "y") then > if (pco%csvout == "y") then` | `"ROUTING_UNIT              lsunit_pw_day.csv"` |
| 968 | data | `if (db_mx%lsu_out > 0) then > if (pco%pw_lsu%m == "y") then` | `"ROUTING_UNIT              lsunit_pw_mon.txt"` |
| 974 | data | `if (db_mx%lsu_out > 0) then > if (pco%pw_lsu%m == "y") then > if (pco%csvout == "y") then` | `"ROUTING_UNIT              lsunit_pw_mon.csv"` |
| 983 | data | `if (db_mx%lsu_out > 0) then > if (pco%pw_lsu%y == "y") then` | `"ROUTING_UNIT              lsunit_pw_yr.txt"` |
| 989 | data | `if (db_mx%lsu_out > 0) then > if (pco%pw_lsu%y == "y") then > if (pco%csvout == "y") then` | `"ROUTING_UNIT              lsunit_pw_yr.csv"` |
| 998 | data | `if (db_mx%lsu_out > 0) then > if (pco%pw_lsu%a == "y") then` | `"ROUTING_UNIT              lsunit_pw_aa.txt"` |
| 1004 | data | `if (db_mx%lsu_out > 0) then > if (pco%pw_lsu%a == "y") then > if (pco%csvout == "y") then` | `"ROUTING_UNIT              lsunit_pw_aa.csv"` |
| 1015 | data | `if (pco%wb_bsn%d == "y") then` | `"BASIN                     basin_wb_day.txt"` |
| 1021 | data | `if (pco%wb_bsn%d == "y") then > if (pco%csvout == "y") then` | `"BASIN                     basin_wb_day.csv"` |
| 1030 | data | `if (pco%wb_bsn%m == "y") then` | `"BASIN                     basin_wb_mon.txt"` |
| 1036 | data | `if (pco%wb_bsn%m == "y") then > if (pco%csvout == "y") then` | `"BASIN                     basin_wb_mon.csv"` |
| 1045 | data | `if (pco%wb_bsn%y == "y") then` | `"BASIN                     basin_wb_yr.txt"` |
| 1051 | data | `if (pco%wb_bsn%y == "y") then > if (pco%csvout == "y") then` | `"BASIN                     basin_wb_yr.csv"` |
| 1060 | data | `if (pco%wb_bsn%a == "y") then` | `"BASIN                     basin_wb_aa.txt"` |
| 1066 | data | `if (pco%wb_bsn%a == "y") then > if (pco%csvout == "y") then` | `"BASIN                     basin_wb_aa.csv"` |
| 1076 | data | `if (pco%nb_bsn%d == "y") then` | `"BASIN                     basin_nb_day.txt"` |
| 1082 | data | `if (pco%nb_bsn%d == "y") then > if (pco%csvout == "y") then` | `"BASIN                     basin_nb_day.csv"` |
| 1091 | data | `if (pco%nb_bsn%m == "y") then` | `"BASIN                     basin_nb_mon.txt"` |
| 1097 | data | `if (pco%nb_bsn%m == "y") then > if (pco%csvout == "y") then` | `"BASIN                     basin_nb_mon.csv"` |
| 1106 | data | `if (pco%nb_bsn%y == "y") then` | `"BASIN                     basin_nb_yr.txt"` |
| 1112 | data | `if (pco%nb_bsn%y == "y") then > if (pco%csvout == "y") then` | `"BASIN                     basin_nb_yr.csv"` |
| 1121 | data | `if (pco%nb_bsn%a == "y") then` | `"BASIN                     basin_nb_aa.txt"` |
| 1127 | data | `if (pco%nb_bsn%a == "y") then > if (pco%csvout == "y") then` | `"BASIN                     basin_nb_aa.csv"` |
| 1137 | data | `if (pco%ls_bsn%d == "y") then` | `"BASIN                     basin_ls_day.txt"` |
| 1143 | data | `if (pco%ls_bsn%d == "y") then > if (pco%csvout == "y") then` | `"BASIN                     basin_ls_day.csv"` |
| 1152 | data | `if (pco%ls_bsn%m == "y") then` | `"BASIN                     basin_ls_mon.txt"` |
| 1158 | data | `if (pco%ls_bsn%m == "y") then > if (pco%csvout == "y") then` | `"BASIN                     basin_ls_mon.csv"` |
| 1167 | data | `if (pco%ls_bsn%y == "y") then` | `"BASIN                     basin_ls_yr.txt"` |
| 1173 | data | `if (pco%ls_bsn%y == "y") then > if (pco%csvout == "y") then` | `"BASIN                     basin_ls_yr.csv"` |
| 1182 | data | `if (pco%ls_bsn%a == "y") then` | `"BASIN                     basin_ls_aa.txt"` |
| 1188 | data | `if (pco%ls_bsn%a == "y") then > if (pco%csvout == "y") then` | `"BASIN                     basin_ls_aa.csv"` |
| 1198 | data | `if (pco%pw_bsn%d == "y") then` | `"BASIN                     basin_pw_day.txt"` |
| 1204 | data | `if (pco%pw_bsn%d == "y") then > if (pco%csvout == "y") then` | `"BASIN                     basin_pw_day.csv"` |
| 1213 | data | `if (pco%pw_bsn%m == "y") then` | `"BASIN                     basin_pw_mon.txt"` |
| 1219 | data | `if (pco%pw_bsn%m == "y") then > if (pco%csvout == "y") then` | `"BASIN                     basin_pw_mon.csv"` |
| 1228 | data | `if (pco%pw_bsn%y == "y") then` | `"BASIN                     basin_pw_yr.txt"` |
| 1234 | data | `if (pco%pw_bsn%y == "y") then > if (pco%csvout == "y") then` | `"BASIN                     basin_pw_yr.csv"` |
| 1243 | data | `if (pco%pw_bsn%a == "y") then` | `"BASIN                     basin_pw_aa.txt"` |
| 1249 | data | `if (pco%pw_bsn%a == "y") then > if (pco%csvout == "y") then` | `"BASIN                     basin_pw_aa.csv"` |
| 1259 | data | `if (pco%crop_yld == "y" .or. pco%crop_yld == "b") then` | `"CROP                      crop_yld_yr.txt"` |
| 1264 | data | `if (pco%crop_yld == "y" .or. pco%crop_yld == "b") then > if (pco%csvout == "y") then` | `"CROP                      crop_yld_yr.csv"` |
| 1273 | data | `if (pco%crop_yld == "a" .or. pco%crop_yld == "b") then` | `"CROP                      crop_yld_aa.txt"` |
| 1278 | data | `if (pco%crop_yld == "a" .or. pco%crop_yld == "b") then > if (pco%csvout == "y") then` | `"CROP                      crop_yld_aa.csv"` |
| 1297 | data | `if (db_mx%lsu_out > 0) then > if (pco%cb_gl_lsu%d == "y") then` | `"LSU                       lsu_carb_gl_day.txt"` |
| 1303 | data | `if (db_mx%lsu_out > 0) then > if (pco%cb_gl_lsu%d == "y") then > if (pco%csvout == "y") then` | `"LSU                       lsu_carb_gl_day.csv"` |
| 1311 | data | `if (db_mx%lsu_out > 0) then > if (pco%cb_gl_lsu%m == "y") then` | `"LSU                       lsu_carb_gl_mon.txt"` |
| 1317 | data | `if (db_mx%lsu_out > 0) then > if (pco%cb_gl_lsu%m == "y") then > if (pco%csvout == "y") then` | `"LSU                       lsu_carb_gl_mon.csv"` |
| 1325 | data | `if (db_mx%lsu_out > 0) then > if (pco%cb_gl_lsu%y == "y") then` | `"LSU                       lsu_carb_gl_yr.txt"` |
| 1331 | data | `if (db_mx%lsu_out > 0) then > if (pco%cb_gl_lsu%y == "y") then > if (pco%csvout == "y") then` | `"LSU                       lsu_carb_gl_yr.csv"` |
| 1339 | data | `if (db_mx%lsu_out > 0) then > if (pco%cb_gl_lsu%a == "y") then` | `"LSU                       lsu_carb_gl_aa.txt"` |
| 1345 | data | `if (db_mx%lsu_out > 0) then > if (pco%cb_gl_lsu%a == "y") then > if (pco%csvout == "y") then` | `"LSU                       lsu_carb_gl_aa.csv"` |
| 1355 | data | `if (db_mx%lsu_out > 0) then > if (pco%cb_trf_lsu%d == "y") then` | `"LSU                       lsu_scf_day.txt"` |
| 1361 | data | `if (db_mx%lsu_out > 0) then > if (pco%cb_trf_lsu%d == "y") then > if (pco%csvout == "y") then` | `"LSU                       lsu_scf_day.csv"` |
| 1369 | data | `if (db_mx%lsu_out > 0) then > if (pco%cb_trf_lsu%m == "y") then` | `"LSU                       lsu_scf_mon.txt"` |
| 1375 | data | `if (db_mx%lsu_out > 0) then > if (pco%cb_trf_lsu%m == "y") then > if (pco%csvout == "y") then` | `"LSU                       lsu_scf_mon.csv"` |
| 1383 | data | `if (db_mx%lsu_out > 0) then > if (pco%cb_trf_lsu%y == "y") then` | `"LSU                       lsu_scf_yr.txt"` |
| 1389 | data | `if (db_mx%lsu_out > 0) then > if (pco%cb_trf_lsu%y == "y") then > if (pco%csvout == "y") then` | `"LSU                       lsu_scf_yr.csv"` |
| 1397 | data | `if (db_mx%lsu_out > 0) then > if (pco%cb_trf_lsu%a == "y") then` | `"LSU                       lsu_scf_aa.txt"` |
| 1403 | data | `if (db_mx%lsu_out > 0) then > if (pco%cb_trf_lsu%a == "y") then > if (pco%csvout == "y") then` | `"LSU                       lsu_scf_aa.csv"` |
| 1412 | data | `if (db_mx%lsu_out > 0) then > if (pco%cb_plt_lsu%d == "y") then` | `"LSU                       lsu_plc_stat_day.txt"` |
| 1417 | data | `if (db_mx%lsu_out > 0) then > if (pco%cb_plt_lsu%d == "y") then > if (pco%csvout == "y") then` | `"LSU                       lsu_plc_stat_day.csv"` |
| 1424 | data | `if (db_mx%lsu_out > 0) then > if (pco%cb_plt_lsu%m == "y") then` | `"LSU                       lsu_plc_stat_mon.txt"` |
| 1429 | data | `if (db_mx%lsu_out > 0) then > if (pco%cb_plt_lsu%m == "y") then > if (pco%csvout == "y") then` | `"LSU                       lsu_plc_stat_mon.csv"` |
| 1436 | data | `if (db_mx%lsu_out > 0) then > if (pco%cb_plt_lsu%y == "y") then` | `"LSU                       lsu_plc_stat_yr.txt"` |
| 1441 | data | `if (db_mx%lsu_out > 0) then > if (pco%cb_plt_lsu%y == "y") then > if (pco%csvout == "y") then` | `"LSU                       lsu_plc_stat_yr.csv"` |
| 1448 | data | `if (db_mx%lsu_out > 0) then > if (pco%cb_plt_lsu%a == "y") then` | `"LSU                       lsu_plc_stat_aa.txt"` |
| 1453 | data | `if (db_mx%lsu_out > 0) then > if (pco%cb_plt_lsu%a == "y") then > if (pco%csvout == "y") then` | `"LSU                       lsu_plc_stat_aa.csv"` |
| 1475 | data | `None` | `"HRU                       " // trim(fname_txt)` |
| 1480 | data | `if (pco%csvout == "y") then` | `"HRU                       " // trim(fname_csv)` |
| 1492 | data | `None` | `"HRU                       " // trim(fname_txt)` |
| 1497 | data | `if (pco%csvout == "y") then` | `"HRU                       " // trim(fname_csv)` |
| 1512 | data | `None` | `"HRU                       " // trim(fname_txt)` |
| 1517 | data | `if (pco%csvout == "y") then` | `"HRU                       " // trim(fname_csv)` |


- Procedure: `proc_bsn`
- Writer: `proc_bsn.f90`
- Match: source_output
- Resolved default filename(s): `files_out.out`

| Line | Role | Condition | Fields written |
| --- | --- | --- | --- |
| 16 | data | `None` | `"files_out.out - OUTPUT FILES WRITTEN"` |


- Procedure: `proc_hru`
- Writer: `proc_hru.f90`
- Match: source_output
- Resolved default filename(s): `files_out.out`

| Line | Role | Condition | Fields written |
| --- | --- | --- | --- |
| 61 | data | `if (sp_ob%hru > 0) then` | `"CHK                       checker.out"` |

### `mgt_out.txt`

- Review needed: yes
- Writer procedures changed: yes
- Write-block count changed: no
- Write conditions changed: yes
- Write roles changed: yes
- Base flattened write order: `j`, `time%yrc`, `time%mo`, `time%day_mo`, `d_tbl%act(iac)%name`, `"IRRIGATE"`, `phubase(j)`, `pcom(j)%plcur(ipl)%phuacc`, `soil(j)%sw`, `pl_mass(j)%tot(ipl)%m`, `pl_mass(j)%rsd_tot%m`, `sol_sumno3(j)`, `sol_sumsolp(j)`, `irrig(j)%applied`, `j`, `time%yrc`, `time%mo`, `time%day_mo`, `d_tbl%act(iac)%name`, `"IRRIG_trn"`, `phubase(j)`, `pcom(j)%plcur(ipl)%phuacc`, `soil(j)%sw`, `pl_mass(j)%tot(ipl)%m`, `pl_mass(j)%rsd_tot%m`, `sol_sumno3(j)`, `sol_sumsolp(j)`, `irrop_db(irrop)%amt_mm`, `j`, `time%yrc`, `time%mo`, `time%day_mo`, `d_tbl%act(iac)%name`, `"PADDY IRRIGATION"`, `irrig(j)%applied`, `j`, `time%yrc`, `time%mo`, `time%day_mo`, `d_tbl%act(iac)%name`, `"IRRIGATE"`, `phubase(j)`, `pcom(j)%plcur(ipl)%phuacc`, `soil(j)%sw`, `pl_mass(j)%tot(ipl)%m`, `pl_mass(j)%rsd_tot`, `sol_sumno3(j)`, `sol_sumsolp(j)`, `irrig(j)%applied`, `j`, `time%yrc`, `time%mo`, `time%day_mo`, `mgt%op_char`, `" FERT-WET"`, `phubase(j)`, `pcom(j)%plcur(ipl)%phuacc`, `soil(j)%sw`, `pl_mass(j)%tot(ipl)%m`, `pl_mass(j)%rsd_tot%m`, `sol_sumno3(j)`, `sol_sumsolp(j)`, `frt_kg`, `fertno3`, `fertnh3`, `fertorgn`, `fertsolp`, `fertorgp`, `j`, `time%yrc`, `time%mo`, `time%day_mo`, `mgt%op_char`, `"    FERT "`, `phubase(j)`, `pcom(j)%plcur(ipl)%phuacc`, `soil(j)%sw`, `pl_mass(j)%tot(ipl)%m`, `pl_mass(j)%rsd_tot%m`, `sol_sumno3(j)`, `sol_sumsolp(j)`, `frt_kg`, `fertno3`, `fertnh3`, `fertorgn`, `fertsolp`, `fertorgp`, `j`, `time%yrc`, `time%mo`, `time%day_mo`, `mgt%op_char`, `" MANURE "`, `phubase(j)`, `pcom(j)%plcur(ipl)%phuacc`, `soil(j)%sw`, `pl_mass(j)%tot(ipl)%m`, `pl_mass(j)%rsd_tot%m`, `sol_sumno3(j)`, `sol_sumsolp(j)`, `frt_kg`, `fertno3`, `fertnh3`, `fertorgn`, `fertsolp`, `fertorgp`, `j`, `time%yrc`, `time%mo`, `time%day_mo`, `tilldb(idtill)%tillnm`, `"    TILLAGE"`, `phubase(j)`, `pcom(j)%plcur(ipl)%phuacc`, `soil(j)%sw`, `pl_mass(j)%tot(ipl)%m`, `pl_mass(j)%rsd_tot%m`, `sol_sumno3(j)`, `sol_sumsolp(j)`, `tilldb(idtill)%effmix`, `j`, `time%yrc`, `time%mo`, `time%day_mo`, `pldb(idp)%plantnm`, `"TRANSPLANT"`, `phubase(j)`, `pcom(j)%plcur(ipl)%phuacc`, `soil(ihru)%sw`, `pl_mass(j)%tot(ipl)%m`, `pl_mass(j)%rsd_tot%m`, `sol_sumno3(j)`, `sol_sumsolp(j)`, `pcom(j)%plg(ipl)%lai`, `pcom(j)%plcur(ipl)%lai_pot`, `j`, `time%yrc`, `time%mo`, `time%day_mo`, `pldb(idp)%plantnm`, `"    PLANT"`, `phubase(j)`, `pcom(j)%plcur(ipl)%phuacc`, `soil(ihru)%sw`, `pl_mass(j)%tot(ipl)%m`, `pl_mass(j)%rsd_tot%m`, `sol_sumno3(j)`, `sol_sumsolp(j)`, `pcom(j)%plg(ipl)%lai`, `pcom(j)%plcur(ipl)%lai_pot`, `j`, `time%yrc`, `time%mo`, `time%day_mo`, `pldb(idp)%plantnm`, `"    PLANT_ALREADY_GROWING"`, `phubase(j)`, `pcom(j)%plcur(ipl)%phuacc`, `soil(j)%sw`, `pl_mass(j)%tot(ipl)%m`, `pl_mass(j)%rsd_tot%m`, `sol_sumno3(j)`, `sol_sumsolp(j)`, `pcom(j)%plg(ipl)%lai`, `pcom(j)%plcur(ipl)%lai_pot`, `j`, `time%yrc`, `time%mo`, `time%day_mo`, `pldb(idp)%plantnm`, `"    HARVEST"`, `phubase(j)`, `pcom(j)%plcur(ipl)%phuacc`, `soil(j)%sw`, `biomass`, `pl_mass(j)%rsd_tot%m`, `sol_sumno3(j)`, `sol_sumsolp(j)`, `pl_yield%m`, `pcom(j)%plstr(ipl)%sum_n`, `pcom(j)%plstr(ipl)%sum_p`, `pcom(j)%plstr(ipl)%sum_tmp`, `pcom(j)%plstr(ipl)%sum_w`, `pcom(j)%plstr(ipl)%sum_a`, `j`, `time%yrc`, `time%mo`, `time%day_mo`, `pldb(idp)%plantnm`, `"         KILL"`, `phubase(j)`, `pcom(j)%plcur(ipl)%phuacc`, `soil(j)%sw`, `biomass`, `pl_mass(j)%rsd_tot%m`, `sol_sumno3(j)`, `sol_sumsolp(j)`, `yield`, `pcom(j)%plstr(ipl)%sum_n`, `pcom(j)%plstr(ipl)%sum_p`, `pcom(j)%plstr(ipl)%sum_tmp`, `pcom(j)%plstr(ipl)%sum_w`, `pcom(j)%plstr(ipl)%sum_a`, `j`, `time%yrc`, `time%mo`, `time%day_mo`, `pldb(idp)%plantnm`, `"    HARV/KILL"`, `phubase(j)`, `pcom(j)%plcur(ipl)%phuacc`, `soil(j)%sw`, `biomass`, `pl_mass(j)%rsd_tot%m`, `sol_sumno3(j)`, `sol_sumsolp(j)`, `pl_yield%m`, `pcom(j)%plstr(ipl)%sum_n`, `pcom(j)%plstr(ipl)%sum_p`, `pcom(j)%plstr(ipl)%sum_tmp`, `pcom(j)%plstr(ipl)%sum_w`, `pcom(j)%plstr(ipl)%sum_a`, `j`, `time%yrc`, `time%mo`, `time%day_mo`, `d_tbl%act(iac)%option`, `"    PEST "`, `phubase(j)`, `pcom(j)%plcur(ipl)%phuacc`, `soil(j)%sw`, `pl_mass(j)%tot(ipl)%m`, `pl_mass(j)%rsd_tot%m`, `sol_sumno3(j)`, `sol_sumsolp(j)`, `pest_kg`, `j`, `time%yrc`, `time%mo`, `time%day_mo`, `tilldb(idtill)%tillnm`, `"  DRAIN_CONTROL"`, `phubase(j)`, `pcom(j)%plcur(1)%phuacc`, `soil(j)%sw`, `pl_mass(j)%tot(1)%m`, `pl_mass(j)%rsd_tot%m`, `sol_sumno3(j)`, `sol_sumsolp(j)`, `hru(j)%lumv%sdr_dep`, `j`, `time%yrc`, `time%mo`, `time%day_mo`, `d_tbl%act(iac)%name`, `"IMPOUND OFF"`, `j`, `time%yrc`, `time%mo`, `time%day_mo`, `d_tbl%act(iac)%name`, `"IMPOUND ON"`, `j`, `time%yrc`, `time%mo`, `time%day_mo`, `d_tbl%act(iac)%name`, `"RESET WEIR HEIGHT (m)"`, `wet_ob(j)%weir_hgt`, `j`, `time%yrc`, `time%mo`, `time%day_mo`, `d_tbl%act(iac)%name`, `"PUDDLE"`, `j`, `time%yrc`, `time%mo`, `time%day_mo`, `d_tbl%act(iac)%name`, `"    BURN"`, `phubase(j)`, `pcom(j)%plcur(ipl)%phuacc`, `soil(j)%sw`, `pl_mass(j)%tot(ipl)%m`, `pl_mass(j)%rsd_tot%m`, `sol_sumno3(j)`, `sol_sumsolp(j)`, `j`, `time%yrc`, `time%mo`, `time%day_mo`, `d_tbl%act(iac)%name`, `"    CNUP"`, `phubase(j)`, `pcom(j)%plcur(ipl)%phuacc`, `soil(j)%sw`, `pl_mass(j)%tot(ipl)%m`, `pl_mass(j)%rsd_tot%m`, `sol_sumno3(j)`, `sol_sumsolp(j)`, `cn_prev`, `cn2(j)`, `bsn%name`, `prog`, `mgt_hdr`, `mgt_hdr_unt1`, `j`, `time%yrc`, `time%mo`, `time%day_mo`, `fertdb(ifrt)%fertnm`, `"    MANU"`, `phubase(j)`, `pcom(j)%plcur(ipl)%phuacc`, `soil(j)%sw`, `pl_mass(j)%tot(ipl)%m`, `pl_mass(j)%rsd_tot%m`, `sol_sumno3(j)`, `sol_sumsolp(j)`, `frt_kg`, `fertno3`, `fertnh3`, `fertorgn`, `fertsolp`, `fertorgp`, `j`, `time%yrc`, `time%mo`, `time%day_mo`, `pldb(idp)%plantnm`, `"TRANSPLANT "`, `phubase(j)`, `pcom(j)%plcur(ipl)%phuacc`, `soil(j)%sw`, `pl_mass(j)%tot(ipl)%m`, `pl_mass(j)%rsd_tot%m`, `sol_sumno3(j)`, `sol_sumsolp(j)`, `pcom(j)%plg(ipl)%lai`, `pcom(j)%plcur(ipl)%lai_pot`, `j`, `time%yrc`, `time%mo`, `time%day_mo`, `pldb(idp)%plantnm`, `"    PLANT "`, `phubase(j)`, `pcom(j)%plcur(ipl)%phuacc`, `soil(j)%sw`, `pl_mass(j)%tot(ipl)%m`, `pl_mass(j)%rsd_tot%m`, `sol_sumno3(j)`, `sol_sumsolp(j)`, `pcom(j)%plg(ipl)%lai`, `pcom(j)%plcur(ipl)%lai_pot`, `j`, `time%yrc`, `time%mo`, `time%day_mo`, `pldb(idp)%plantnm`, `"    PLANT_ALREADY_GROWING"`, `phubase(j)`, `pcom(j)%plcur(ipl)%phuacc`, `soil(j)%sw`, `pl_mass(j)%tot(ipl)%m`, `pl_mass(j)%rsd_tot%m`, `sol_sumno3(j)`, `sol_sumsolp(j)`, `pcom(j)%plg(ipl)%lai`, `pcom(j)%plcur(ipl)%lai_pot`, `j`, `time%yrc`, `time%mo`, `time%day_mo`, `pldb(idp)%plantnm`, `"    HARVEST "`, `phubase(j)`, `pcom(j)%plcur(ipl)%phuacc`, `soil(j)%sw`, `biomass`, `pl_mass(j)%rsd_tot%m`, `sol_sumno3(j)`, `sol_sumsolp(j)`, `pl_yield%m`, `pcom(j)%plstr(ipl)%sum_n`, `pcom(j)%plstr(ipl)%sum_p`, `pcom(j)%plstr(ipl)%sum_tmp`, `pcom(j)%plstr(ipl)%sum_w`, `pcom(j)%plstr(ipl)%sum_a`, `j`, `time%yrc`, `time%mo`, `time%day_mo`, `pldb(idp)%plantnm`, `"    HARVEST "`, `phubase(j)`, `pcom(j)%plcur(ipl)%phuacc`, `soil(j)%sw`, `biomass`, `pl_mass(j)%rsd_tot%m`, `sol_sumno3(j)`, `sol_sumsolp(j)`, `pl_yield%m`, `pcom(j)%plstr(ipl)%sum_n`, `pcom(j)%plstr(ipl)%sum_p`, `pcom(j)%plstr(ipl)%sum_tmp`, `pcom(j)%plstr(ipl)%sum_w`, `pcom(j)%plstr(ipl)%sum_a`, `j`, `time%yrc`, `time%mo`, `time%day_mo`, `pldb(idp)%plantnm`, `"    KILL "`, `phubase(j)`, `pcom(j)%plcur(ipl)%phuacc`, `soil(j)%sw`, `biomass`, `pl_mass(j)%rsd_tot%m`, `sol_sumno3(j)`, `sol_sumsolp(j)`, `pl_yield%m`, `pcom(j)%plstr(ipl)%sum_n`, `pcom(j)%plstr(ipl)%sum_p`, `pcom(j)%plstr(ipl)%sum_tmp`, `pcom(j)%plstr(ipl)%sum_w`, `pcom(j)%plstr(ipl)%sum_a`, `j`, `time%yrc`, `time%mo`, `time%day_mo`, `pldb(idp)%plantnm`, `"    HARV/KILL "`, `phubase(j)`, `pcom(j)%plcur(ipl)%phuacc`, `soil(j)%sw`, `biomass`, `pl_mass(j)%rsd_tot%m`, `sol_sumno3(j)`, `sol_sumsolp(j)`, `pl_yield%m`, `pcom(j)%plstr(ipl)%sum_n`, `pcom(j)%plstr(ipl)%sum_p`, `pcom(j)%plstr(ipl)%sum_tmp`, `pcom(j)%plstr(ipl)%sum_w`, `pcom(j)%plstr(ipl)%sum_a`, `j`, `time%yrc`, `time%mo`, `time%day_mo`, `tilldb(idtill)%tillnm`, `"    TILLAGE "`, `phubase(j)`, `pcom(j)%plcur(ipl)%phuacc`, `soil(j)%sw`, `pl_mass(j)%tot(ipl)%m`, `pl_mass(j)%rsd_tot%m`, `sol_sumno3(j)`, `sol_sumsolp(j)`, `tilldb(idtill)%effmix`, `j`, `time%yrc`, `time%mo`, `time%day_mo`, `irrop_db(irrop)%name`, `"IRRIGATE "`, `phubase(j)`, `pcom(j)%plcur(ipl)%phuacc`, `soil(j)%sw`, `pl_mass(j)%tot(ipl)%m`, `pl_mass(j)%rsd_tot%m`, `sol_sumno3(j)`, `sol_sumsolp(j)`, `irrig(j)%applied`, `irrig(j)%runoff`, `j`, `time%yrc`, `time%mo`, `time%day_mo`, `mgt%op_char`, `" FERT-WET"`, `phubase(j)`, `pcom(j)%plcur(ipl)%phuacc`, `soil(j)%sw`, `pl_mass(j)%tot(ipl)%m`, `pl_mass(j)%rsd_tot%m`, `sol_sumno3(j)`, `sol_sumsolp(j)`, `frt_kg`, `fertno3`, `fertnh3`, `fertorgn`, `fertsolp`, `fertorgp`, `j`, `time%yrc`, `time%mo`, `time%day_mo`, `mgt%op_char`, `"    FERT "`, `phubase(j)`, `pcom(j)%plcur(ipl)%phuacc`, `soil(j)%sw`, `pl_mass(j)%tot(ipl)%m`, `pl_mass(j)%rsd_tot%m`, `sol_sumno3(j)`, `sol_sumsolp(j)`, `frt_kg`, `fertno3`, `fertnh3`, `fertorgn`, `fertsolp`, `fertorgp`, `j`, `time%yrc`, `time%mo`, `time%day_mo`, `mgt%op_char`, `" MANURE "`, `phubase(j)`, `pcom(j)%plcur(ipl)%phuacc`, `soil(j)%sw`, `pl_mass(j)%tot(ipl)%m`, `pl_mass(j)%rsd_tot%m`, `sol_sumno3(j)`, `sol_sumsolp(j)`, `frt_kg`, `fertno3`, `fertnh3`, `fertorgn`, `fertsolp`, `fertorgp`, `j`, `time%yrc`, `time%mo`, `time%day_mo`, `mgt%op_char`, `"    PEST "`, `phubase(j)`, `pcom(j)%plcur(ipl)%phuacc`, `soil(j)%sw`, `pl_mass(j)%tot(ipl)%m`, `pl_mass(j)%rsd_tot%m`, `sol_sumno3(j)`, `sol_sumsolp(j)`, `pest_kg`, `j`, `time%yrc`, `time%mo`, `time%day_mo`, `mgt%op_char`, `"    GRAZE "`, `phubase(j)`, `pcom(j)%plcur(ipl)%phuacc`, `soil(j)%sw`, `pl_mass(j)%tot(ipl)%m`, `pl_mass(j)%rsd_tot%m`, `sol_sumno3(j)`, `sol_sumsolp(j)`, `grazeop_db(mgt%op1)%eat`, `grazeop_db(mgt%op1)%manure`, `j`, `time%yrc`, `time%mo`, `time%day_mo`, `mgt%op_char`, `"    CNUP "`, `phubase(j)`, `pcom(j)%plcur(ipl)%phuacc`, `soil(j)%sw`, `pl_mass(j)%tot(ipl)%m`, `pl_mass(j)%rsd_tot%m`, `sol_sumno3(j)`, `sol_sumsolp(j)`, `mgt%op3`, `cn2(j)`, `j`, `time%yrc`, `time%mo`, `time%day_mo`, `mgt%op_char`, `"    BURN "`, `phubase(j)`, `pcom(j)%plcur(ipl)%phuacc`, `soil(j)%sw`, `pl_mass(j)%tot(ipl)%m`, `pl_mass(j)%rsd_tot%m`, `sol_sumno3(j)`, `sol_sumsolp(j)`, `j`, `time%yrc`, `time%mo`, `time%day_mo`, `mgt%op_char`, `"STREET_SWEEP "`, `phubase(j)`, `pcom(j)%plcur(ipl)%phuacc`, `soil(j)%sw`, `pl_mass(j)%tot(ipl)%m`, `pl_mass(j)%rsd_tot%m`, `sol_sumno3(j)`, `sol_sumsolp(j)`, `j`, `time%yrc`, `time%mo`, `time%day_mo`, `pldb(idp)%plantnm`, `"  DRAIN_CONTROL"`, `phubase(j)`, `pcom(j)%plcur(j)%phuacc`, `soil(j)%sw`, `pl_mass(j)%tot(j)%m`, `pl_mass(j)%rsd_tot%m`, `sol_sumno3(j)`, `sol_sumsolp(j)`, `hru(j)%lumv%sdr_dep`, `j`, `time%yrc`, `time%mo`, `time%day_mo`, `mgt%op_char`, `"RESET WEIR HEIGHT (m)"`, `wet_ob(j)%weir_hgt`, `j`, `time%yrc`, `time%mo`, `time%day_mo`, `mgt%op_char`, `"BEGIN/ADJUST PADDY IRRIGATION"`, `hru(j)%irr_hmax`, `j`, `time%yrc`, `time%mo`, `time%day_mo`, `mgt%op_char`, `"BEGIN/ADJUST PADDY IRRIGATION"`, `hru(j)%irr_hmax`, `j`, `time%yrc`, `time%mo`, `time%day_mo`, `mgt%op_char`, `"STOP PADDY IRRIGATION"`, `hru(j)%irr_hmax`, `j`, `time%yrc`, `time%mo`, `time%day_mo`, `mgt%op_char`, `"BEGIN_PADDY_IRRIGATION "`, `phubase(j)`, `pcom(j)%plcur(ipl)%phuacc`, `soil(j)%sw`, `pl_mass(j)%tot(ipl)%m`, `pl_mass(j)%rsd_tot%m`, `sol_sumno3(j)`, `sol_sumsolp(j)`, `mgt%op3`, `mgt%op4`, `j`, `time%yrc`, `time%mo`, `time%day_mo`, `mgt%op_char`, `"IRRIGATE "`, `phubase(j)`, `pcom(j)%plcur(ipl)%phuacc`, `soil(j)%sw`, `pl_mass(j)%tot(ipl)%m`, `pl_mass(j)%rsd_tot%m`, `sol_sumno3(j)`, `sol_sumsolp(j)`, `irrig(j)%applied`, `irrig(j)%runoff`, `j`, `time%yrc`, `time%mo`, `time%day_mo`, `mgt%op_char`, `"PUDDLE"`, `j`, `time%yrc`, `time%mo`, `time%day_mo`, `wallo(iwallo)%name`, `"IRRIGATE"`, `phubase(j)`, `pcom(j)%plcur(1)%phuacc`, `soil(j)%sw`, `pl_mass(j)%tot(1)%m`, `pl_mass(j)%rsd_tot%m`, `sol_sumno3(j)`, `sol_sumsolp(j)`, `irrig(j)%applied`
- Candidate flattened write order: `j`, `time%yrc`, `time%mo`, `time%day_mo`, `d_tbl%act(iac)%name`, `"IRRIGATE"`, `phubase(j)`, `pcom(j)%plcur(ipl)%phuacc`, `soil(j)%sw`, `pl_mass(j)%tot(ipl)%m`, `pl_mass(j)%rsd_tot%m`, `sol_sumno3(j)`, `sol_sumsolp(j)`, `irrig(j)%applied`, `j`, `time%yrc`, `time%mo`, `time%day_mo`, `d_tbl%act(iac)%name`, `"IRRIG_trn"`, `phubase(j)`, `pcom(j)%plcur(ipl)%phuacc`, `soil(j)%sw`, `pl_mass(j)%tot(ipl)%m`, `pl_mass(j)%rsd_tot%m`, `sol_sumno3(j)`, `sol_sumsolp(j)`, `irrop_db(irrop)%amt_mm`, `j`, `time%yrc`, `time%mo`, `time%day_mo`, `d_tbl%act(iac)%name`, `"PADDY IRRIGATION"`, `irrig(j)%applied`, `j`, `time%yrc`, `time%mo`, `time%day_mo`, `d_tbl%act(iac)%name`, `"IRRIGATE"`, `phubase(j)`, `pcom(j)%plcur(ipl)%phuacc`, `soil(j)%sw`, `pl_mass(j)%tot(ipl)%m`, `pl_mass(j)%rsd_tot`, `sol_sumno3(j)`, `sol_sumsolp(j)`, `irrig(j)%applied`, `j`, `time%yrc`, `time%mo`, `time%day_mo`, `mgt%op_char`, `" FERT-WET"`, `phubase(j)`, `pcom(j)%plcur(ipl)%phuacc`, `soil(j)%sw`, `pl_mass(j)%tot(ipl)%m`, `pl_mass(j)%rsd_tot%m`, `sol_sumno3(j)`, `sol_sumsolp(j)`, `frt_kg`, `fertno3`, `fertnh3`, `fertorgn`, `fertsolp`, `fertorgp`, `j`, `time%yrc`, `time%mo`, `time%day_mo`, `mgt%op_char`, `"    FERT "`, `phubase(j)`, `pcom(j)%plcur(ipl)%phuacc`, `soil(j)%sw`, `pl_mass(j)%tot(ipl)%m`, `pl_mass(j)%rsd_tot%m`, `sol_sumno3(j)`, `sol_sumsolp(j)`, `frt_kg`, `fertno3`, `fertnh3`, `fertorgn`, `fertsolp`, `fertorgp`, `j`, `time%yrc`, `time%mo`, `time%day_mo`, `mgt%op_char`, `" MANURE "`, `phubase(j)`, `pcom(j)%plcur(ipl)%phuacc`, `soil(j)%sw`, `pl_mass(j)%tot(ipl)%m`, `pl_mass(j)%rsd_tot%m`, `sol_sumno3(j)`, `sol_sumsolp(j)`, `frt_kg`, `fertno3`, `fertnh3`, `fertorgn`, `fertsolp`, `fertorgp`, `j`, `time%yrc`, `time%mo`, `time%day_mo`, `tilldb(idtill)%tillnm`, `"    TILLAGE"`, `phubase(j)`, `pcom(j)%plcur(ipl)%phuacc`, `soil(j)%sw`, `pl_mass(j)%tot(ipl)%m`, `pl_mass(j)%rsd_tot%m`, `sol_sumno3(j)`, `sol_sumsolp(j)`, `tilldb(idtill)%effmix`, `j`, `time%yrc`, `time%mo`, `time%day_mo`, `pldb(idp)%plantnm`, `"    PLANT"`, `phubase(j)`, `pcom(j)%plcur(ipl)%phuacc`, `soil(ihru)%sw`, `pl_mass(j)%tot(ipl)%m`, `pl_mass(j)%rsd_tot%m`, `sol_sumno3(j)`, `sol_sumsolp(j)`, `pcom(j)%plg(ipl)%lai`, `pcom(j)%plcur(ipl)%lai_pot`, `j`, `time%yrc`, `time%mo`, `time%day_mo`, `pldb(idp)%plantnm`, `"TRANSPLANT"`, `phubase(j)`, `pcom(j)%plcur(ipl)%phuacc`, `soil(ihru)%sw`, `pl_mass(j)%tot(ipl)%m`, `pl_mass(j)%rsd_tot%m`, `sol_sumno3(j)`, `sol_sumsolp(j)`, `pcom(j)%plg(ipl)%lai`, `pcom(j)%plcur(ipl)%lai_pot`, `j`, `time%yrc`, `time%mo`, `time%day_mo`, `pldb(idp)%plantnm`, `"    PLANT"`, `phubase(j)`, `pcom(j)%plcur(ipl)%phuacc`, `soil(ihru)%sw`, `pl_mass(j)%tot(ipl)%m`, `pl_mass(j)%rsd_tot%m`, `sol_sumno3(j)`, `sol_sumsolp(j)`, `pcom(j)%plg(ipl)%lai`, `pcom(j)%plcur(ipl)%lai_pot`, `j`, `time%yrc`, `time%mo`, `time%day_mo`, `pldb(idp)%plantnm`, `"    PLANT_ALREADY_GROWING"`, `phubase(j)`, `pcom(j)%plcur(ipl)%phuacc`, `soil(j)%sw`, `pl_mass(j)%tot(ipl)%m`, `pl_mass(j)%rsd_tot%m`, `sol_sumno3(j)`, `sol_sumsolp(j)`, `pcom(j)%plg(ipl)%lai`, `pcom(j)%plcur(ipl)%lai_pot`, `j`, `time%yrc`, `time%mo`, `time%day_mo`, `pldb(idp)%plantnm`, `"    HARVEST"`, `phubase(j)`, `pcom(j)%plcur(ipl)%phuacc`, `soil(j)%sw`, `biomass`, `pl_mass(j)%rsd_tot%m`, `sol_sumno3(j)`, `sol_sumsolp(j)`, `pl_yield%m`, `pcom(j)%plstr(ipl)%sum_n`, `pcom(j)%plstr(ipl)%sum_p`, `pcom(j)%plstr(ipl)%sum_tmp`, `pcom(j)%plstr(ipl)%sum_w`, `pcom(j)%plstr(ipl)%sum_a`, `j`, `time%yrc`, `time%mo`, `time%day_mo`, `pldb(idp)%plantnm`, `"         KILL"`, `phubase(j)`, `pcom(j)%plcur(ipl)%phuacc`, `soil(j)%sw`, `biomass`, `pl_mass(j)%rsd_tot%m`, `sol_sumno3(j)`, `sol_sumsolp(j)`, `yield`, `pcom(j)%plstr(ipl)%sum_n`, `pcom(j)%plstr(ipl)%sum_p`, `pcom(j)%plstr(ipl)%sum_tmp`, `pcom(j)%plstr(ipl)%sum_w`, `pcom(j)%plstr(ipl)%sum_a`, `j`, `time%yrc`, `time%mo`, `time%day_mo`, `pldb(idp)%plantnm`, `"    HARV/KILL"`, `phubase(j)`, `pcom(j)%plcur(ipl)%phuacc`, `soil(j)%sw`, `biomass`, `pl_mass(j)%rsd_tot%m`, `sol_sumno3(j)`, `sol_sumsolp(j)`, `pl_yield%m`, `pcom(j)%plstr(ipl)%sum_n`, `pcom(j)%plstr(ipl)%sum_p`, `pcom(j)%plstr(ipl)%sum_tmp`, `pcom(j)%plstr(ipl)%sum_w`, `pcom(j)%plstr(ipl)%sum_a`, `j`, `time%yrc`, `time%mo`, `time%day_mo`, `d_tbl%act(iac)%option`, `"    PEST "`, `phubase(j)`, `pcom(j)%plcur(ipl)%phuacc`, `soil(j)%sw`, `pl_mass(j)%tot(ipl)%m`, `pl_mass(j)%rsd_tot%m`, `sol_sumno3(j)`, `sol_sumsolp(j)`, `pest_kg`, `j`, `time%yrc`, `time%mo`, `time%day_mo`, `tilldb(idtill)%tillnm`, `"  DRAIN_CONTROL"`, `phubase(j)`, `pcom(j)%plcur(1)%phuacc`, `soil(j)%sw`, `pl_mass(j)%tot(1)%m`, `pl_mass(j)%rsd_tot%m`, `sol_sumno3(j)`, `sol_sumsolp(j)`, `hru(j)%lumv%sdr_dep`, `j`, `time%yrc`, `time%mo`, `time%day_mo`, `d_tbl%act(iac)%name`, `"IMPOUND OFF"`, `j`, `time%yrc`, `time%mo`, `time%day_mo`, `d_tbl%act(iac)%name`, `"IMPOUND ON"`, `j`, `time%yrc`, `time%mo`, `time%day_mo`, `d_tbl%act(iac)%name`, `"RESET WEIR HEIGHT (m)"`, `wet_ob(j)%weir_hgt`, `j`, `time%yrc`, `time%mo`, `time%day_mo`, `d_tbl%act(iac)%name`, `"PUDDLE"`, `j`, `time%yrc`, `time%mo`, `time%day_mo`, `d_tbl%act(iac)%name`, `"    BURN"`, `phubase(j)`, `pcom(j)%plcur(ipl)%phuacc`, `soil(j)%sw`, `pl_mass(j)%tot(ipl)%m`, `pl_mass(j)%rsd_tot%m`, `sol_sumno3(j)`, `sol_sumsolp(j)`, `j`, `time%yrc`, `time%mo`, `time%day_mo`, `d_tbl%act(iac)%name`, `"    CNUP"`, `phubase(j)`, `pcom(j)%plcur(ipl)%phuacc`, `soil(j)%sw`, `pl_mass(j)%tot(ipl)%m`, `pl_mass(j)%rsd_tot%m`, `sol_sumno3(j)`, `sol_sumsolp(j)`, `cn_prev`, `cn2(j)`, `bsn%name`, `prog`, `mgt_hdr`, `mgt_hdr_unt1`, `j`, `time%yrc`, `time%mo`, `time%day_mo`, `fertdb(ifrt)%fertnm`, `"    MANU"`, `phubase(j)`, `pcom(j)%plcur(ipl)%phuacc`, `soil(j)%sw`, `pl_mass(j)%tot(ipl)%m`, `pl_mass(j)%rsd_tot%m`, `sol_sumno3(j)`, `sol_sumsolp(j)`, `frt_kg`, `fertno3`, `fertnh3`, `fertorgn`, `fertsolp`, `fertorgp`, `j`, `time%yrc`, `time%mo`, `time%day_mo`, `pldb(idp)%plantnm`, `"TRANSPLANT "`, `phubase(j)`, `pcom(j)%plcur(ipl)%phuacc`, `soil(j)%sw`, `pl_mass(j)%tot(ipl)%m`, `pl_mass(j)%rsd_tot%m`, `sol_sumno3(j)`, `sol_sumsolp(j)`, `pcom(j)%plg(ipl)%lai`, `pcom(j)%plcur(ipl)%lai_pot`, `j`, `time%yrc`, `time%mo`, `time%day_mo`, `pldb(idp)%plantnm`, `"    PLANT "`, `phubase(j)`, `pcom(j)%plcur(ipl)%phuacc`, `soil(j)%sw`, `pl_mass(j)%tot(ipl)%m`, `pl_mass(j)%rsd_tot%m`, `sol_sumno3(j)`, `sol_sumsolp(j)`, `pcom(j)%plg(ipl)%lai`, `pcom(j)%plcur(ipl)%lai_pot`, `j`, `time%yrc`, `time%mo`, `time%day_mo`, `pldb(idp)%plantnm`, `"    PLANT_ALREADY_GROWING"`, `phubase(j)`, `pcom(j)%plcur(ipl)%phuacc`, `soil(j)%sw`, `pl_mass(j)%tot(ipl)%m`, `pl_mass(j)%rsd_tot%m`, `sol_sumno3(j)`, `sol_sumsolp(j)`, `pcom(j)%plg(ipl)%lai`, `pcom(j)%plcur(ipl)%lai_pot`, `j`, `time%yrc`, `time%mo`, `time%day_mo`, `pldb(idp)%plantnm`, `"    HARVEST "`, `phubase(j)`, `pcom(j)%plcur(ipl)%phuacc`, `soil(j)%sw`, `biomass`, `pl_mass(j)%rsd_tot%m`, `sol_sumno3(j)`, `sol_sumsolp(j)`, `pl_yield%m`, `pcom(j)%plstr(ipl)%sum_n`, `pcom(j)%plstr(ipl)%sum_p`, `pcom(j)%plstr(ipl)%sum_tmp`, `pcom(j)%plstr(ipl)%sum_w`, `pcom(j)%plstr(ipl)%sum_a`, `j`, `time%yrc`, `time%mo`, `time%day_mo`, `pldb(idp)%plantnm`, `"    HARVEST "`, `phubase(j)`, `pcom(j)%plcur(ipl)%phuacc`, `soil(j)%sw`, `biomass`, `pl_mass(j)%rsd_tot%m`, `sol_sumno3(j)`, `sol_sumsolp(j)`, `pl_yield%m`, `pcom(j)%plstr(ipl)%sum_n`, `pcom(j)%plstr(ipl)%sum_p`, `pcom(j)%plstr(ipl)%sum_tmp`, `pcom(j)%plstr(ipl)%sum_w`, `pcom(j)%plstr(ipl)%sum_a`, `j`, `time%yrc`, `time%mo`, `time%day_mo`, `pldb(idp)%plantnm`, `"    KILL "`, `phubase(j)`, `pcom(j)%plcur(ipl)%phuacc`, `soil(j)%sw`, `biomass`, `pl_mass(j)%rsd_tot%m`, `sol_sumno3(j)`, `sol_sumsolp(j)`, `pl_yield%m`, `pcom(j)%plstr(ipl)%sum_n`, `pcom(j)%plstr(ipl)%sum_p`, `pcom(j)%plstr(ipl)%sum_tmp`, `pcom(j)%plstr(ipl)%sum_w`, `pcom(j)%plstr(ipl)%sum_a`, `j`, `time%yrc`, `time%mo`, `time%day_mo`, `pldb(idp)%plantnm`, `"    HARV/KILL "`, `phubase(j)`, `pcom(j)%plcur(ipl)%phuacc`, `soil(j)%sw`, `biomass`, `pl_mass(j)%rsd_tot%m`, `sol_sumno3(j)`, `sol_sumsolp(j)`, `pl_yield%m`, `pcom(j)%plstr(ipl)%sum_n`, `pcom(j)%plstr(ipl)%sum_p`, `pcom(j)%plstr(ipl)%sum_tmp`, `pcom(j)%plstr(ipl)%sum_w`, `pcom(j)%plstr(ipl)%sum_a`, `j`, `time%yrc`, `time%mo`, `time%day_mo`, `tilldb(idtill)%tillnm`, `"    TILLAGE "`, `phubase(j)`, `pcom(j)%plcur(ipl)%phuacc`, `soil(j)%sw`, `pl_mass(j)%tot(ipl)%m`, `pl_mass(j)%rsd_tot%m`, `sol_sumno3(j)`, `sol_sumsolp(j)`, `tilldb(idtill)%effmix`, `j`, `time%yrc`, `time%mo`, `time%day_mo`, `irrop_db(irrop)%name`, `"IRRIGATE "`, `phubase(j)`, `pcom(j)%plcur(ipl)%phuacc`, `soil(j)%sw`, `pl_mass(j)%tot(ipl)%m`, `pl_mass(j)%rsd_tot%m`, `sol_sumno3(j)`, `sol_sumsolp(j)`, `irrig(j)%applied`, `irrig(j)%runoff`, `j`, `time%yrc`, `time%mo`, `time%day_mo`, `mgt%op_char`, `" FERT-WET"`, `phubase(j)`, `pcom(j)%plcur(ipl)%phuacc`, `soil(j)%sw`, `pl_mass(j)%tot(ipl)%m`, `pl_mass(j)%rsd_tot%m`, `sol_sumno3(j)`, `sol_sumsolp(j)`, `frt_kg`, `fertno3`, `fertnh3`, `fertorgn`, `fertsolp`, `fertorgp`, `j`, `time%yrc`, `time%mo`, `time%day_mo`, `mgt%op_char`, `"    FERT "`, `phubase(j)`, `pcom(j)%plcur(ipl)%phuacc`, `soil(j)%sw`, `pl_mass(j)%tot(ipl)%m`, `pl_mass(j)%rsd_tot%m`, `sol_sumno3(j)`, `sol_sumsolp(j)`, `frt_kg`, `fertno3`, `fertnh3`, `fertorgn`, `fertsolp`, `fertorgp`, `j`, `time%yrc`, `time%mo`, `time%day_mo`, `mgt%op_char`, `" MANURE "`, `phubase(j)`, `pcom(j)%plcur(ipl)%phuacc`, `soil(j)%sw`, `pl_mass(j)%tot(ipl)%m`, `pl_mass(j)%rsd_tot%m`, `sol_sumno3(j)`, `sol_sumsolp(j)`, `frt_kg`, `fertno3`, `fertnh3`, `fertorgn`, `fertsolp`, `fertorgp`, `j`, `time%yrc`, `time%mo`, `time%day_mo`, `mgt%op_char`, `"    PEST "`, `phubase(j)`, `pcom(j)%plcur(ipl)%phuacc`, `soil(j)%sw`, `pl_mass(j)%tot(ipl)%m`, `pl_mass(j)%rsd_tot%m`, `sol_sumno3(j)`, `sol_sumsolp(j)`, `pest_kg`, `j`, `time%yrc`, `time%mo`, `time%day_mo`, `mgt%op_char`, `"    GRAZE "`, `phubase(j)`, `pcom(j)%plcur(ipl)%phuacc`, `soil(j)%sw`, `pl_mass(j)%tot(ipl)%m`, `pl_mass(j)%rsd_tot%m`, `sol_sumno3(j)`, `sol_sumsolp(j)`, `grazeop_db(mgt%op1)%eat`, `grazeop_db(mgt%op1)%manure`, `j`, `time%yrc`, `time%mo`, `time%day_mo`, `mgt%op_char`, `"    CNUP "`, `phubase(j)`, `pcom(j)%plcur(ipl)%phuacc`, `soil(j)%sw`, `pl_mass(j)%tot(ipl)%m`, `pl_mass(j)%rsd_tot%m`, `sol_sumno3(j)`, `sol_sumsolp(j)`, `mgt%op3`, `cn2(j)`, `j`, `time%yrc`, `time%mo`, `time%day_mo`, `mgt%op_char`, `"    BURN "`, `phubase(j)`, `pcom(j)%plcur(ipl)%phuacc`, `soil(j)%sw`, `pl_mass(j)%tot(ipl)%m`, `pl_mass(j)%rsd_tot%m`, `sol_sumno3(j)`, `sol_sumsolp(j)`, `j`, `time%yrc`, `time%mo`, `time%day_mo`, `mgt%op_char`, `"STREET_SWEEP "`, `phubase(j)`, `pcom(j)%plcur(ipl)%phuacc`, `soil(j)%sw`, `pl_mass(j)%tot(ipl)%m`, `pl_mass(j)%rsd_tot%m`, `sol_sumno3(j)`, `sol_sumsolp(j)`, `j`, `time%yrc`, `time%mo`, `time%day_mo`, `pldb(idp)%plantnm`, `"  DRAIN_CONTROL"`, `phubase(j)`, `pcom(j)%plcur(j)%phuacc`, `soil(j)%sw`, `pl_mass(j)%tot(j)%m`, `pl_mass(j)%rsd_tot%m`, `sol_sumno3(j)`, `sol_sumsolp(j)`, `hru(j)%lumv%sdr_dep`, `j`, `time%yrc`, `time%mo`, `time%day_mo`, `mgt%op_char`, `"RESET WEIR HEIGHT (m)"`, `wet_ob(j)%weir_hgt`, `j`, `time%yrc`, `time%mo`, `time%day_mo`, `mgt%op_char`, `"BEGIN/ADJUST PADDY IRRIGATION"`, `hru(j)%irr_hmax`, `j`, `time%yrc`, `time%mo`, `time%day_mo`, `mgt%op_char`, `"BEGIN/ADJUST PADDY IRRIGATION"`, `hru(j)%irr_hmax`, `j`, `time%yrc`, `time%mo`, `time%day_mo`, `mgt%op_char`, `"STOP PADDY IRRIGATION"`, `hru(j)%irr_hmax`, `j`, `time%yrc`, `time%mo`, `time%day_mo`, `mgt%op_char`, `"BEGIN_PADDY_IRRIGATION "`, `phubase(j)`, `pcom(j)%plcur(ipl)%phuacc`, `soil(j)%sw`, `pl_mass(j)%tot(ipl)%m`, `pl_mass(j)%rsd_tot%m`, `sol_sumno3(j)`, `sol_sumsolp(j)`, `mgt%op3`, `mgt%op4`, `j`, `time%yrc`, `time%mo`, `time%day_mo`, `mgt%op_char`, `"IRRIGATE "`, `phubase(j)`, `pcom(j)%plcur(ipl)%phuacc`, `soil(j)%sw`, `pl_mass(j)%tot(ipl)%m`, `pl_mass(j)%rsd_tot%m`, `sol_sumno3(j)`, `sol_sumsolp(j)`, `irrig(j)%applied`, `irrig(j)%runoff`, `j`, `time%yrc`, `time%mo`, `time%day_mo`, `mgt%op_char`, `"PUDDLE"`, `j`, `time%yrc`, `time%mo`, `time%day_mo`, `"WATER ALLO"`, `"IRRIGATE"`, `phubase(j)`, `pcom(j)%plcur(1)%phuacc`, `soil(j)%sw`, `pl_mass(j)%tot(1)%m`, `pl_mass(j)%rsd_tot%m`, `sol_sumno3(j)`, `sol_sumsolp(j)`, `irrig(j)%applied`

#### Write-order edits

- `insert` at base index 120 / candidate index 120: removed _no fields captured_; added `j`, `time%yrc`, `time%mo`, `time%day_mo`, `pldb(idp)%plantnm`, `"    PLANT"`, `phubase(j)`, `pcom(j)%plcur(ipl)%phuacc`, `soil(ihru)%sw`, `pl_mass(j)%tot(ipl)%m`, `pl_mass(j)%rsd_tot%m`, `sol_sumno3(j)`, `sol_sumsolp(j)`, `pcom(j)%plg(ipl)%lai`, `pcom(j)%plcur(ipl)%lai_pot`
- `replace` at base index 685 / candidate index 700: removed `wallo(iwallo)%name`; added `"WATER ALLO"`

#### Base write structure

- Source expression(s): _none captured_

- Procedure: `actions`
- Writer: `actions.f90`
- Match: source_output
- Resolved default filename(s): `mgt_out.txt`

| Line | Role | Condition | Fields written |
| --- | --- | --- | --- |
| 154 | data | `do iac = 1, d_tbl%acts > if (action == "y") then > select case (d_tbl%act(iac)%typ) / case ("irr_demand") > if (d_tbl%act(iac)%name=='ponding') then / else > if (pcom(j)%dtbl(idtbl)%num_actions(iac) <= Int(d_tbl%act(iac)%const2)) then > if (pco%mgtout == "y") then` | `j`, `time%yrc`, `time%mo`, `time%day_mo`, `d_tbl%act(iac)%name`, `"IRRIGATE"`, `phubase(j)`, `pcom(j)%plcur(ipl)%phuacc`, `soil(j)%sw`, `pl_mass(j)%tot(ipl)%m`, `pl_mass(j)%rsd_tot%m`, `sol_sumno3(j)`, `sol_sumsolp(j)`, `irrig(j)%applied` |
| 161 | data | `do iac = 1, d_tbl%acts > if (action == "y") then > select case (d_tbl%act(iac)%typ) / case ("irr_demand") > if (d_tbl%act(iac)%name=='ponding') then / else > if (pcom(j)%dtbl(idtbl)%num_actions(iac) <= Int(d_tbl%act(iac)%const2)) then / else > if (pco%mgtout == "y") then` | `j`, `time%yrc`, `time%mo`, `time%day_mo`, `d_tbl%act(iac)%name`, `"IRRIG_trn"`, `phubase(j)`, `pcom(j)%plcur(ipl)%phuacc`, `soil(j)%sw`, `pl_mass(j)%tot(ipl)%m`, `pl_mass(j)%rsd_tot%m`, `sol_sumno3(j)`, `sol_sumsolp(j)`, `irrop_db(irrop)%amt_mm` |
| 282 | data | `do iac = 1, d_tbl%acts > if (action == "y") then > select case (d_tbl%act(iac)%typ) / case ("irrigate") > if (pcom(j)%dtbl(idtbl)%num_actions(iac) <= Int(d_tbl%act(iac)%const2)) then > if (d_tbl%act(iac)%name=='ponding') then > if (pco%mgtout == "y") then` | `j`, `time%yrc`, `time%mo`, `time%day_mo`, `d_tbl%act(iac)%name`, `"PADDY IRRIGATION"`, `irrig(j)%applied` |
| 286 | data | `do iac = 1, d_tbl%acts > if (action == "y") then > select case (d_tbl%act(iac)%typ) / case ("irrigate") > if (pcom(j)%dtbl(idtbl)%num_actions(iac) <= Int(d_tbl%act(iac)%const2)) then > if (d_tbl%act(iac)%name=='ponding') then / else > if (pco%mgtout == "y") then` | `j`, `time%yrc`, `time%mo`, `time%day_mo`, `d_tbl%act(iac)%name`, `"IRRIGATE"`, `phubase(j)`, `pcom(j)%plcur(ipl)%phuacc`, `soil(j)%sw`, `pl_mass(j)%tot(ipl)%m`, `pl_mass(j)%rsd_tot`, `sol_sumno3(j)`, `sol_sumsolp(j)`, `irrig(j)%applied` |
| 312 | data | `do iac = 1, d_tbl%acts > if (action == "y") then > select case (d_tbl%act(iac)%typ) / case ("fertilize") > if (pcom(j)%dtbl(idtbl)%num_actions(iac) <= Int(d_tbl%act(iac)%const2)) then > if (wet(j)%flo > 0. .and. chemapp_db(ifertop)%surf_frac == 1) then > if (pco%mgtout == "y") then` | `j`, `time%yrc`, `time%mo`, `time%day_mo`, `mgt%op_char`, `" FERT-WET"`, `phubase(j)`, `pcom(j)%plcur(ipl)%phuacc`, `soil(j)%sw`, `pl_mass(j)%tot(ipl)%m`, `pl_mass(j)%rsd_tot%m`, `sol_sumno3(j)`, `sol_sumsolp(j)`, `frt_kg`, `fertno3`, `fertnh3`, `fertorgn`, `fertsolp`, `fertorgp` |
| 320 | data | `do iac = 1, d_tbl%acts > if (action == "y") then > select case (d_tbl%act(iac)%typ) / case ("fertilize") > if (pcom(j)%dtbl(idtbl)%num_actions(iac) <= Int(d_tbl%act(iac)%const2)) then > if (wet(j)%flo > 0. .and. chemapp_db(ifertop)%surf_frac == 1) then / else > if (pco%mgtout == "y") then` | `j`, `time%yrc`, `time%mo`, `time%day_mo`, `mgt%op_char`, `"    FERT "`, `phubase(j)`, `pcom(j)%plcur(ipl)%phuacc`, `soil(j)%sw`, `pl_mass(j)%tot(ipl)%m`, `pl_mass(j)%rsd_tot%m`, `sol_sumno3(j)`, `sol_sumsolp(j)`, `frt_kg`, `fertno3`, `fertnh3`, `fertorgn`, `fertsolp`, `fertorgp` |
| 346 | data | `do iac = 1, d_tbl%acts > if (action == "y") then > select case (d_tbl%act(iac)%typ) / case ("manure") > if (pcom(j)%dtbl(idtbl)%num_actions(iac) <= Int(d_tbl%act(iac)%const2)) then > if (pco%mgtout == "y") then` | `j`, `time%yrc`, `time%mo`, `time%day_mo`, `mgt%op_char`, `" MANURE "`, `phubase(j)`, `pcom(j)%plcur(ipl)%phuacc`, `soil(j)%sw`, `pl_mass(j)%tot(ipl)%m`, `pl_mass(j)%rsd_tot%m`, `sol_sumno3(j)`, `sol_sumsolp(j)`, `frt_kg`, `fertno3`, `fertnh3`, `fertorgn`, `fertsolp`, `fertorgp` |
| 377 | data | `do iac = 1, d_tbl%acts > if (action == "y") then > select case (d_tbl%act(iac)%typ) / case ("till") > if (pcom(j)%dtbl(idtbl)%num_actions(iac) <= Int(d_tbl%act(iac)%const2)) then > if (pco%mgtout == "y") then` | `j`, `time%yrc`, `time%mo`, `time%day_mo`, `tilldb(idtill)%tillnm`, `"    TILLAGE"`, `phubase(j)`, `pcom(j)%plcur(ipl)%phuacc`, `soil(j)%sw`, `pl_mass(j)%tot(ipl)%m`, `pl_mass(j)%rsd_tot%m`, `sol_sumno3(j)`, `sol_sumsolp(j)`, `tilldb(idtill)%effmix` |
| 414 | data | `do iac = 1, d_tbl%acts > if (action == "y") then > select case (d_tbl%act(iac)%typ) / case ("plant") > do ipl = 1, pcom(j)%npl > if (d_tbl%act(iac)%option == pcomdb(icom)%pl(ipl)%cpnm) then > if (pcom(j)%plcur(ipl)%gro == "n") then > if (d_tbl%act_app(iac) > 0) then > if (pco%mgtout == "y") then` | `j`, `time%yrc`, `time%mo`, `time%day_mo`, `pldb(idp)%plantnm`, `"TRANSPLANT"`, `phubase(j)`, `pcom(j)%plcur(ipl)%phuacc`, `soil(ihru)%sw`, `pl_mass(j)%tot(ipl)%m`, `pl_mass(j)%rsd_tot%m`, `sol_sumno3(j)`, `sol_sumsolp(j)`, `pcom(j)%plg(ipl)%lai`, `pcom(j)%plcur(ipl)%lai_pot` |
| 421 | data | `do iac = 1, d_tbl%acts > if (action == "y") then > select case (d_tbl%act(iac)%typ) / case ("plant") > do ipl = 1, pcom(j)%npl > if (d_tbl%act(iac)%option == pcomdb(icom)%pl(ipl)%cpnm) then > if (pcom(j)%plcur(ipl)%gro == "n") then > if (d_tbl%act_app(iac) > 0) then / else > if (pco%mgtout == "y") then` | `j`, `time%yrc`, `time%mo`, `time%day_mo`, `pldb(idp)%plantnm`, `"    PLANT"`, `phubase(j)`, `pcom(j)%plcur(ipl)%phuacc`, `soil(ihru)%sw`, `pl_mass(j)%tot(ipl)%m`, `pl_mass(j)%rsd_tot%m`, `sol_sumno3(j)`, `sol_sumsolp(j)`, `pcom(j)%plg(ipl)%lai`, `pcom(j)%plcur(ipl)%lai_pot` |
| 430 | data | `do iac = 1, d_tbl%acts > if (action == "y") then > select case (d_tbl%act(iac)%typ) / case ("plant") > do ipl = 1, pcom(j)%npl > if (d_tbl%act(iac)%option == pcomdb(icom)%pl(ipl)%cpnm) then > if (pcom(j)%plcur(ipl)%gro == "n") then / else > if (pco%mgtout ==  "y") then` | `j`, `time%yrc`, `time%mo`, `time%day_mo`, `pldb(idp)%plantnm`, `"    PLANT_ALREADY_GROWING"`, `phubase(j)`, `pcom(j)%plcur(ipl)%phuacc`, `soil(j)%sw`, `pl_mass(j)%tot(ipl)%m`, `pl_mass(j)%rsd_tot%m`, `sol_sumno3(j)`, `sol_sumsolp(j)`, `pcom(j)%plg(ipl)%lai`, `pcom(j)%plcur(ipl)%lai_pot` |
| 514 | data | `do iac = 1, d_tbl%acts > if (action == "y") then > select case (d_tbl%act(iac)%typ) / case ("harvest") > if (pcom(j)%dtbl(idtbl)%num_actions(iac) <= Int(d_tbl%act(iac)%const2)) then > do ipl = 1, pcom(j)%npl > if (d_tbl%act(iac)%option == pcomdb(icom)%pl(ipl)%cpnm .or. d_tbl%act(iac)%option == "all") then > if (pco%mgtout == "y") then` | `j`, `time%yrc`, `time%mo`, `time%day_mo`, `pldb(idp)%plantnm`, `"    HARVEST"`, `phubase(j)`, `pcom(j)%plcur(ipl)%phuacc`, `soil(j)%sw`, `biomass`, `pl_mass(j)%rsd_tot%m`, `sol_sumno3(j)`, `sol_sumsolp(j)`, `pl_yield%m`, `pcom(j)%plstr(ipl)%sum_n`, `pcom(j)%plstr(ipl)%sum_p`, `pcom(j)%plstr(ipl)%sum_tmp`, `pcom(j)%plstr(ipl)%sum_w`, `pcom(j)%plstr(ipl)%sum_a` |
| 544 | data | `do iac = 1, d_tbl%acts > if (action == "y") then > select case (d_tbl%act(iac)%typ) / case ("kill") > if (pcom(j)%dtbl(idtbl)%num_actions(iac) <= Int(d_tbl%act(iac)%const2)) then > do ipl = 1, pcom(j)%npl > if (d_tbl%act(iac)%option == pcomdb(icom)%pl(ipl)%cpnm .or. d_tbl%act(iac)%option == "all") then > if (pco%mgtout == "y") then` | `j`, `time%yrc`, `time%mo`, `time%day_mo`, `pldb(idp)%plantnm`, `"         KILL"`, `phubase(j)`, `pcom(j)%plcur(ipl)%phuacc`, `soil(j)%sw`, `biomass`, `pl_mass(j)%rsd_tot%m`, `sol_sumno3(j)`, `sol_sumsolp(j)`, `yield`, `pcom(j)%plstr(ipl)%sum_n`, `pcom(j)%plstr(ipl)%sum_p`, `pcom(j)%plstr(ipl)%sum_tmp`, `pcom(j)%plstr(ipl)%sum_w`, `pcom(j)%plstr(ipl)%sum_a` |
| 632 | data | `do iac = 1, d_tbl%acts > if (action == "y") then > select case (d_tbl%act(iac)%typ) / case ("harvest_kill") > if (pcom(j)%dtbl(idtbl)%num_actions(iac) <= Int(d_tbl%act(iac)%const2)) then > do ipl = 1, pcom(j)%npl > if (d_tbl%act(iac)%option == pcomdb(icom)%pl(ipl)%cpnm .or. d_tbl%act(iac)%option == "all") then > if (pco%mgtout == "y") then` | `j`, `time%yrc`, `time%mo`, `time%day_mo`, `pldb(idp)%plantnm`, `"    HARV/KILL"`, `phubase(j)`, `pcom(j)%plcur(ipl)%phuacc`, `soil(j)%sw`, `biomass`, `pl_mass(j)%rsd_tot%m`, `sol_sumno3(j)`, `sol_sumsolp(j)`, `pl_yield%m`, `pcom(j)%plstr(ipl)%sum_n`, `pcom(j)%plstr(ipl)%sum_p`, `pcom(j)%plstr(ipl)%sum_tmp`, `pcom(j)%plstr(ipl)%sum_w`, `pcom(j)%plstr(ipl)%sum_a` |
| 694 | data | `do iac = 1, d_tbl%acts > if (action == "y") then > select case (d_tbl%act(iac)%typ) / case ("pest_apply") > if (pcom(j)%dtbl(idtbl)%num_actions(iac) <= Int(d_tbl%act(iac)%const2)) then > if (pco%mgtout == "y") then` | `j`, `time%yrc`, `time%mo`, `time%day_mo`, `d_tbl%act(iac)%option`, `"    PEST "`, `phubase(j)`, `pcom(j)%plcur(ipl)%phuacc`, `soil(j)%sw`, `pl_mass(j)%tot(ipl)%m`, `pl_mass(j)%rsd_tot%m`, `sol_sumno3(j)`, `sol_sumsolp(j)`, `pest_kg` |
| 842 | data | `do iac = 1, d_tbl%acts > if (action == "y") then > select case (d_tbl%act(iac)%typ) / case ("tiledep_control") > if (pcom(j)%dtbl(idtbl)%num_actions(iac) <= Int(d_tbl%act(iac)%const2)) then > if (pco%mgtout == "y") then` | `j`, `time%yrc`, `time%mo`, `time%day_mo`, `tilldb(idtill)%tillnm`, `"  DRAIN_CONTROL"`, `phubase(j)`, `pcom(j)%plcur(1)%phuacc`, `soil(j)%sw`, `pl_mass(j)%tot(1)%m`, `pl_mass(j)%rsd_tot%m`, `sol_sumno3(j)`, `sol_sumsolp(j)`, `hru(j)%lumv%sdr_dep` |
| 875 | data | `do iac = 1, d_tbl%acts > if (action == "y") then > select case (d_tbl%act(iac)%typ) / case ("impound_off") > if (pco%mgtout == "y") then` | `j`, `time%yrc`, `time%mo`, `time%day_mo`, `d_tbl%act(iac)%name`, `"IMPOUND OFF"` |
| 893 | data | `do iac = 1, d_tbl%acts > if (action == "y") then > select case (d_tbl%act(iac)%typ) / case ("impound_on") > if (pco%mgtout == "y") then` | `j`, `time%yrc`, `time%mo`, `time%day_mo`, `d_tbl%act(iac)%name`, `"IMPOUND ON"` |
| 913 | data | `do iac = 1, d_tbl%acts > if (action == "y") then > select case (d_tbl%act(iac)%typ) / case ("weir_height") > if (pco%mgtout == "y") then` | `j`, `time%yrc`, `time%mo`, `time%day_mo`, `d_tbl%act(iac)%name`, `"RESET WEIR HEIGHT (m)"`, `wet_ob(j)%weir_hgt` |
| 954 | data | `do iac = 1, d_tbl%acts > if (action == "y") then > select case (d_tbl%act(iac)%typ) / case ("puddle") > if (pcom(j)%dtbl(idtbl)%num_actions(iac) <= Int(d_tbl%act(iac)%const2)) then > if (pco%mgtout == "y") then` | `j`, `time%yrc`, `time%mo`, `time%day_mo`, `d_tbl%act(iac)%name`, `"PUDDLE"` |
| 1219 | data | `do iac = 1, d_tbl%acts > if (action == "y") then > select case (d_tbl%act(iac)%typ) / case ("burn") > if (pcom(j)%dtbl(idtbl)%num_actions(iac) <= Int(d_tbl%act(iac)%const2)) then > if (pco%mgtout == "y") then` | `j`, `time%yrc`, `time%mo`, `time%day_mo`, `d_tbl%act(iac)%name`, `"    BURN"`, `phubase(j)`, `pcom(j)%plcur(ipl)%phuacc`, `soil(j)%sw`, `pl_mass(j)%tot(ipl)%m`, `pl_mass(j)%rsd_tot%m`, `sol_sumno3(j)`, `sol_sumsolp(j)` |
| 1237 | data | `do iac = 1, d_tbl%acts > if (action == "y") then > select case (d_tbl%act(iac)%typ) / case ("cn_update") > if (pcom(j)%dtbl(idtbl)%num_actions(iac) <= Int(d_tbl%act(iac)%const2)) then > if (pco%mgtout == "y") then` | `j`, `time%yrc`, `time%mo`, `time%day_mo`, `d_tbl%act(iac)%name`, `"    CNUP"`, `phubase(j)`, `pcom(j)%plcur(ipl)%phuacc`, `soil(j)%sw`, `pl_mass(j)%tot(ipl)%m`, `pl_mass(j)%rsd_tot%m`, `sol_sumno3(j)`, `sol_sumsolp(j)`, `cn_prev`, `cn2(j)` |


- Procedure: `header_mgt`
- Writer: `header_mgt.f90`
- Match: source_output
- Resolved default filename(s): `mgt_out.txt`

| Line | Role | Condition | Fields written |
| --- | --- | --- | --- |
| 10 | data | `if (pco%mgtout == "y") then` | `bsn%name`, `prog` |
| 11 | data | `if (pco%mgtout == "y") then` | `mgt_hdr` |
| 12 | data | `if (pco%mgtout == "y") then` | `mgt_hdr_unt1` |


- Procedure: `mallo_control`
- Writer: `mallo_control.f90`
- Match: source_output
- Resolved default filename(s): `mgt_out.txt`

| Line | Role | Condition | Fields written |
| --- | --- | --- | --- |
| 70 | data | `do itrn = 1, mallo(imallo)%trn_obs > if (mallo(imallo)%trn(itrn)%manure_amt%app_t_ha > 0. .and. frt_kg > mallo(imallo)%src(isrc)%bal_d%stor) then > if (pco%mgtout == "y") then` | `j`, `time%yrc`, `time%mo`, `time%day_mo`, `fertdb(ifrt)%fertnm`, `"    MANU"`, `phubase(j)`, `pcom(j)%plcur(ipl)%phuacc`, `soil(j)%sw`, `pl_mass(j)%tot(ipl)%m`, `pl_mass(j)%rsd_tot%m`, `sol_sumno3(j)`, `sol_sumsolp(j)`, `frt_kg`, `fertno3`, `fertnh3`, `fertorgn`, `fertsolp`, `fertorgp` |


- Procedure: `mgt_sched`
- Writer: `mgt_sched.f90`
- Match: source_output
- Resolved default filename(s): `mgt_out.txt`

| Line | Role | Condition | Fields written |
| --- | --- | --- | --- |
| 112 | data | `select case (mgt%op) / case ("plnt") > do ipl = 1, pcom(j)%npl > if (mgt%op_char == pcomdb(icom)%pl(ipl)%cpnm) then > if (pcom(j)%plcur(ipl)%gro == "n") then > if (itr > 0) then > if (pco%mgtout ==  "y") then` | `j`, `time%yrc`, `time%mo`, `time%day_mo`, `pldb(idp)%plantnm`, `"TRANSPLANT "`, `phubase(j)`, `pcom(j)%plcur(ipl)%phuacc`, `soil(j)%sw`, `pl_mass(j)%tot(ipl)%m`, `pl_mass(j)%rsd_tot%m`, `sol_sumno3(j)`, `sol_sumsolp(j)`, `pcom(j)%plg(ipl)%lai`, `pcom(j)%plcur(ipl)%lai_pot` |
| 119 | data | `select case (mgt%op) / case ("plnt") > do ipl = 1, pcom(j)%npl > if (mgt%op_char == pcomdb(icom)%pl(ipl)%cpnm) then > if (pcom(j)%plcur(ipl)%gro == "n") then > if (itr > 0) then / else > if (pco%mgtout ==  "y") then` | `j`, `time%yrc`, `time%mo`, `time%day_mo`, `pldb(idp)%plantnm`, `"    PLANT "`, `phubase(j)`, `pcom(j)%plcur(ipl)%phuacc`, `soil(j)%sw`, `pl_mass(j)%tot(ipl)%m`, `pl_mass(j)%rsd_tot%m`, `sol_sumno3(j)`, `sol_sumsolp(j)`, `pcom(j)%plg(ipl)%lai`, `pcom(j)%plcur(ipl)%lai_pot` |
| 128 | data | `select case (mgt%op) / case ("plnt") > do ipl = 1, pcom(j)%npl > if (mgt%op_char == pcomdb(icom)%pl(ipl)%cpnm) then > if (pcom(j)%plcur(ipl)%gro == "n") then / else > if (pco%mgtout ==  "y") then` | `j`, `time%yrc`, `time%mo`, `time%day_mo`, `pldb(idp)%plantnm`, `"    PLANT_ALREADY_GROWING"`, `phubase(j)`, `pcom(j)%plcur(ipl)%phuacc`, `soil(j)%sw`, `pl_mass(j)%tot(ipl)%m`, `pl_mass(j)%rsd_tot%m`, `sol_sumno3(j)`, `sol_sumsolp(j)`, `pcom(j)%plg(ipl)%lai`, `pcom(j)%plcur(ipl)%lai_pot` |
| 213 | data | `select case (mgt%op) / case ("harv") > do ipl = 1, pcom(j)%npl > if (pcom(j)%plcur(ipl)%gro == "y") then > if (mgt%op_char == pcomdb(icom)%pl(ipl)%cpnm .or. mgt%op_char == "all") then > if (pco%mgtout == "y") then` | `j`, `time%yrc`, `time%mo`, `time%day_mo`, `pldb(idp)%plantnm`, `"    HARVEST "`, `phubase(j)`, `pcom(j)%plcur(ipl)%phuacc`, `soil(j)%sw`, `biomass`, `pl_mass(j)%rsd_tot%m`, `sol_sumno3(j)`, `sol_sumsolp(j)`, `pl_yield%m`, `pcom(j)%plstr(ipl)%sum_n`, `pcom(j)%plstr(ipl)%sum_p`, `pcom(j)%plstr(ipl)%sum_tmp`, `pcom(j)%plstr(ipl)%sum_w`, `pcom(j)%plstr(ipl)%sum_a` |
| 234 | data | `select case (mgt%op) / case ("harv") > do ipl = 1, pcom(j)%npl > if (pcom(j)%plcur(ipl)%gro == "y") then / else > if (mgt%op_char == pcomdb(icom)%pl(ipl)%cpnm .or. mgt%op_char == "all") then > if (pco%mgtout == "y") then` | `j`, `time%yrc`, `time%mo`, `time%day_mo`, `pldb(idp)%plantnm`, `"    HARVEST "`, `phubase(j)`, `pcom(j)%plcur(ipl)%phuacc`, `soil(j)%sw`, `biomass`, `pl_mass(j)%rsd_tot%m`, `sol_sumno3(j)`, `sol_sumsolp(j)`, `pl_yield%m`, `pcom(j)%plstr(ipl)%sum_n`, `pcom(j)%plstr(ipl)%sum_p`, `pcom(j)%plstr(ipl)%sum_tmp`, `pcom(j)%plstr(ipl)%sum_w`, `pcom(j)%plstr(ipl)%sum_a` |
| 254 | data | `select case (mgt%op) / case ("kill") > do ipl = 1, pcom(j)%npl > if (pcom(j)%plcur(ipl)%gro == "y") then > if (mgt%op_char == pcomdb(icom)%pl(ipl)%cpnm .or. mgt%op_char == "all") then > if (pco%mgtout == "y") then` | `j`, `time%yrc`, `time%mo`, `time%day_mo`, `pldb(idp)%plantnm`, `"    KILL "`, `phubase(j)`, `pcom(j)%plcur(ipl)%phuacc`, `soil(j)%sw`, `biomass`, `pl_mass(j)%rsd_tot%m`, `sol_sumno3(j)`, `sol_sumsolp(j)`, `pl_yield%m`, `pcom(j)%plstr(ipl)%sum_n`, `pcom(j)%plstr(ipl)%sum_p`, `pcom(j)%plstr(ipl)%sum_tmp`, `pcom(j)%plstr(ipl)%sum_w`, `pcom(j)%plstr(ipl)%sum_a` |
| 324 | data | `select case (mgt%op) / case ("hvkl") > do ipl = 1, pcom(j)%npl > if (pcom(j)%plcur(ipl)%gro == "y") then > if (mgt%op_char == pcomdb(icom)%pl(ipl)%cpnm .or. mgt%op_char == "all") then > if (pco%mgtout == "y") then` | `j`, `time%yrc`, `time%mo`, `time%day_mo`, `pldb(idp)%plantnm`, `"    HARV/KILL "`, `phubase(j)`, `pcom(j)%plcur(ipl)%phuacc`, `soil(j)%sw`, `biomass`, `pl_mass(j)%rsd_tot%m`, `sol_sumno3(j)`, `sol_sumsolp(j)`, `pl_yield%m`, `pcom(j)%plstr(ipl)%sum_n`, `pcom(j)%plstr(ipl)%sum_p`, `pcom(j)%plstr(ipl)%sum_tmp`, `pcom(j)%plstr(ipl)%sum_w`, `pcom(j)%plstr(ipl)%sum_a` |
| 353 | data | `select case (mgt%op) / case ("till") > if (pco%mgtout == "y") then` | `j`, `time%yrc`, `time%mo`, `time%day_mo`, `tilldb(idtill)%tillnm`, `"    TILLAGE "`, `phubase(j)`, `pcom(j)%plcur(ipl)%phuacc`, `soil(j)%sw`, `pl_mass(j)%tot(ipl)%m`, `pl_mass(j)%rsd_tot%m`, `sol_sumno3(j)`, `sol_sumsolp(j)`, `tilldb(idtill)%effmix` |
| 370 | data | `select case (mgt%op) / case ("irrm") > if (pco%mgtout == "y") then` | `j`, `time%yrc`, `time%mo`, `time%day_mo`, `irrop_db(irrop)%name`, `"IRRIGATE "`, `phubase(j)`, `pcom(j)%plcur(ipl)%phuacc`, `soil(j)%sw`, `pl_mass(j)%tot(ipl)%m`, `pl_mass(j)%rsd_tot%m`, `sol_sumno3(j)`, `sol_sumsolp(j)`, `irrig(j)%applied`, `irrig(j)%runoff` |
| 385 | data | `select case (mgt%op) / case ("fert") > if (wet(j)%flo>0.) then > if (pco%mgtout == "y") then` | `j`, `time%yrc`, `time%mo`, `time%day_mo`, `mgt%op_char`, `" FERT-WET"`, `phubase(j)`, `pcom(j)%plcur(ipl)%phuacc`, `soil(j)%sw`, `pl_mass(j)%tot(ipl)%m`, `pl_mass(j)%rsd_tot%m`, `sol_sumno3(j)`, `sol_sumsolp(j)`, `frt_kg`, `fertno3`, `fertnh3`, `fertorgn`, `fertsolp`, `fertorgp` |
| 395 | data | `select case (mgt%op) / case ("fert") > if (wet(j)%flo>0.) then / else > if (pco%mgtout == "y") then` | `j`, `time%yrc`, `time%mo`, `time%day_mo`, `mgt%op_char`, `"    FERT "`, `phubase(j)`, `pcom(j)%plcur(ipl)%phuacc`, `soil(j)%sw`, `pl_mass(j)%tot(ipl)%m`, `pl_mass(j)%rsd_tot%m`, `sol_sumno3(j)`, `sol_sumsolp(j)`, `frt_kg`, `fertno3`, `fertnh3`, `fertorgn`, `fertsolp`, `fertorgp` |
| 411 | data | `select case (mgt%op) / case ("manu") > if (pco%mgtout == "y") then` | `j`, `time%yrc`, `time%mo`, `time%day_mo`, `mgt%op_char`, `" MANURE "`, `phubase(j)`, `pcom(j)%plcur(ipl)%phuacc`, `soil(j)%sw`, `pl_mass(j)%tot(ipl)%m`, `pl_mass(j)%rsd_tot%m`, `sol_sumno3(j)`, `sol_sumsolp(j)`, `frt_kg`, `fertno3`, `fertnh3`, `fertorgn`, `fertsolp`, `fertorgp` |
| 434 | data | `select case (mgt%op) / case ("pest") > if (pco%mgtout == "y") then` | `j`, `time%yrc`, `time%mo`, `time%day_mo`, `mgt%op_char`, `"    PEST "`, `phubase(j)`, `pcom(j)%plcur(ipl)%phuacc`, `soil(j)%sw`, `pl_mass(j)%tot(ipl)%m`, `pl_mass(j)%rsd_tot%m`, `sol_sumno3(j)`, `sol_sumsolp(j)`, `pest_kg` |
| 447 | data | `select case (mgt%op) / case ("graz") > if (pco%mgtout == "y") then` | `j`, `time%yrc`, `time%mo`, `time%day_mo`, `mgt%op_char`, `"    GRAZE "`, `phubase(j)`, `pcom(j)%plcur(ipl)%phuacc`, `soil(j)%sw`, `pl_mass(j)%tot(ipl)%m`, `pl_mass(j)%rsd_tot%m`, `sol_sumno3(j)`, `sol_sumsolp(j)`, `grazeop_db(mgt%op1)%eat`, `grazeop_db(mgt%op1)%manure` |
| 461 | data | `select case (mgt%op) / case ("cnup") > if (pco%mgtout == "y") then` | `j`, `time%yrc`, `time%mo`, `time%day_mo`, `mgt%op_char`, `"    CNUP "`, `phubase(j)`, `pcom(j)%plcur(ipl)%phuacc`, `soil(j)%sw`, `pl_mass(j)%tot(ipl)%m`, `pl_mass(j)%rsd_tot%m`, `sol_sumno3(j)`, `sol_sumsolp(j)`, `mgt%op3`, `cn2(j)` |
| 472 | data | `select case (mgt%op) / case ("burn") > if (pco%mgtout == "y") then > do ipl = 1, pcom(j)%npl` | `j`, `time%yrc`, `time%mo`, `time%day_mo`, `mgt%op_char`, `"    BURN "`, `phubase(j)`, `pcom(j)%plcur(ipl)%phuacc`, `soil(j)%sw`, `pl_mass(j)%tot(ipl)%m`, `pl_mass(j)%rsd_tot%m`, `sol_sumno3(j)`, `sol_sumsolp(j)` |
| 485 | data | `select case (mgt%op) / case ("swep") > if (pco%mgtout == "y") then` | `j`, `time%yrc`, `time%mo`, `time%day_mo`, `mgt%op_char`, `"STREET_SWEEP "`, `phubase(j)`, `pcom(j)%plcur(ipl)%phuacc`, `soil(j)%sw`, `pl_mass(j)%tot(ipl)%m`, `pl_mass(j)%rsd_tot%m`, `sol_sumno3(j)`, `sol_sumsolp(j)` |
| 502 | data | `select case (mgt%op) / case ("dwm") > if (pco%mgtout ==  "y") then` | `j`, `time%yrc`, `time%mo`, `time%day_mo`, `pldb(idp)%plantnm`, `"  DRAIN_CONTROL"`, `phubase(j)`, `pcom(j)%plcur(j)%phuacc`, `soil(j)%sw`, `pl_mass(j)%tot(j)%m`, `pl_mass(j)%rsd_tot%m`, `sol_sumno3(j)`, `sol_sumsolp(j)`, `hru(j)%lumv%sdr_dep` |
| 525 | data | `select case (mgt%op) / case ("weir") > if (pco%mgtout == "y") then` | `j`, `time%yrc`, `time%mo`, `time%day_mo`, `mgt%op_char`, `"RESET WEIR HEIGHT (m)"`, `wet_ob(j)%weir_hgt` |
| 542 | data | `select case (mgt%op) / case ("irrp") > if (mgt%op3 < 0) then > if (hru(j)%irr_hmax>0) then > if (pco%mgtout == "y") then` | `j`, `time%yrc`, `time%mo`, `time%day_mo`, `mgt%op_char`, `"BEGIN/ADJUST PADDY IRRIGATION"`, `hru(j)%irr_hmax` |
| 551 | data | `select case (mgt%op) / case ("irrp") > if (mgt%op3 < 0) then / else > if (mgt%op3 > 0) then > if (pco%mgtout == "y") then` | `j`, `time%yrc`, `time%mo`, `time%day_mo`, `mgt%op_char`, `"BEGIN/ADJUST PADDY IRRIGATION"`, `hru(j)%irr_hmax` |
| 557 | data | `select case (mgt%op) / case ("irrp") > if (mgt%op3 < 0) then / else > if (mgt%op3 > 0) then / else > if (pco%mgtout == "y") then` | `j`, `time%yrc`, `time%mo`, `time%day_mo`, `mgt%op_char`, `"STOP PADDY IRRIGATION"`, `hru(j)%irr_hmax` |
| 565 | data | `select case (mgt%op) / case ("irrp") > if (pco%mgtout == "y") then` | `j`, `time%yrc`, `time%mo`, `time%day_mo`, `mgt%op_char`, `"BEGIN_PADDY_IRRIGATION "`, `phubase(j)`, `pcom(j)%plcur(ipl)%phuacc`, `soil(j)%sw`, `pl_mass(j)%tot(ipl)%m`, `pl_mass(j)%rsd_tot%m`, `sol_sumno3(j)`, `sol_sumsolp(j)`, `mgt%op3`, `mgt%op4` |
| 583 | data | `select case (mgt%op) / case ("irpm") > if (pco%mgtout == "y") then` | `j`, `time%yrc`, `time%mo`, `time%day_mo`, `mgt%op_char`, `"IRRIGATE "`, `phubase(j)`, `pcom(j)%plcur(ipl)%phuacc`, `soil(j)%sw`, `pl_mass(j)%tot(ipl)%m`, `pl_mass(j)%rsd_tot%m`, `sol_sumno3(j)`, `sol_sumsolp(j)`, `irrig(j)%applied`, `irrig(j)%runoff` |
| 618 | data | `select case (mgt%op) / case ("pudl") > if (pco%mgtout == "y") then` | `j`, `time%yrc`, `time%mo`, `time%day_mo`, `mgt%op_char`, `"PUDDLE"` |


- Procedure: `wallo_control`
- Writer: `wallo_control.f90`
- Match: source_output
- Resolved default filename(s): `mgt_out.txt`

| Line | Role | Condition | Fields written |
| --- | --- | --- | --- |
| 119 | data | `if (wallod_out(iwallo)%trn(itrn)%trn_flo > 0.) then > select case (wallo(iwallo)%trn(itrn)%rcv%typ) / case ("hru") > if (wallo(iwallo)%trn(itrn)%withdr_tot > 0.) then > if (pco%mgtout == "y") then` | `j`, `time%yrc`, `time%mo`, `time%day_mo`, `wallo(iwallo)%name`, `"IRRIGATE"`, `phubase(j)`, `pcom(j)%plcur(1)%phuacc`, `soil(j)%sw`, `pl_mass(j)%tot(1)%m`, `pl_mass(j)%rsd_tot%m`, `sol_sumno3(j)`, `sol_sumsolp(j)`, `irrig(j)%applied` |


#### Candidate write structure

- Source expression(s): _none captured_

- Procedure: `actions`
- Writer: `actions.f90`
- Match: source_output
- Resolved default filename(s): `mgt_out.txt`

| Line | Role | Condition | Fields written |
| --- | --- | --- | --- |
| 156 | data | `do iac = 1, d_tbl%acts > if (action == "y") then > select case (d_tbl%act(iac)%typ) / case ("irr_demand") > if (d_tbl%act(iac)%name=='ponding') then / else > if (pcom(j)%dtbl(idtbl)%num_actions(iac) <= Int(d_tbl%act(iac)%const2)) then > if (pco%mgtout == "y") then` | `j`, `time%yrc`, `time%mo`, `time%day_mo`, `d_tbl%act(iac)%name`, `"IRRIGATE"`, `phubase(j)`, `pcom(j)%plcur(ipl)%phuacc`, `soil(j)%sw`, `pl_mass(j)%tot(ipl)%m`, `pl_mass(j)%rsd_tot%m`, `sol_sumno3(j)`, `sol_sumsolp(j)`, `irrig(j)%applied` |
| 163 | data | `do iac = 1, d_tbl%acts > if (action == "y") then > select case (d_tbl%act(iac)%typ) / case ("irr_demand") > if (d_tbl%act(iac)%name=='ponding') then / else > if (pcom(j)%dtbl(idtbl)%num_actions(iac) <= Int(d_tbl%act(iac)%const2)) then / else > if (pco%mgtout == "y") then` | `j`, `time%yrc`, `time%mo`, `time%day_mo`, `d_tbl%act(iac)%name`, `"IRRIG_trn"`, `phubase(j)`, `pcom(j)%plcur(ipl)%phuacc`, `soil(j)%sw`, `pl_mass(j)%tot(ipl)%m`, `pl_mass(j)%rsd_tot%m`, `sol_sumno3(j)`, `sol_sumsolp(j)`, `irrop_db(irrop)%amt_mm` |
| 327 | data | `do iac = 1, d_tbl%acts > if (action == "y") then > select case (d_tbl%act(iac)%typ) / case ("irrigate") > if (pcom(j)%dtbl(idtbl)%num_actions(iac) <= Int(d_tbl%act(iac)%const2)) then > if (d_tbl%act(iac)%name=='ponding') then > if (pco%mgtout == "y") then` | `j`, `time%yrc`, `time%mo`, `time%day_mo`, `d_tbl%act(iac)%name`, `"PADDY IRRIGATION"`, `irrig(j)%applied` |
| 331 | data | `do iac = 1, d_tbl%acts > if (action == "y") then > select case (d_tbl%act(iac)%typ) / case ("irrigate") > if (pcom(j)%dtbl(idtbl)%num_actions(iac) <= Int(d_tbl%act(iac)%const2)) then > if (d_tbl%act(iac)%name=='ponding') then / else > if (pco%mgtout == "y") then` | `j`, `time%yrc`, `time%mo`, `time%day_mo`, `d_tbl%act(iac)%name`, `"IRRIGATE"`, `phubase(j)`, `pcom(j)%plcur(ipl)%phuacc`, `soil(j)%sw`, `pl_mass(j)%tot(ipl)%m`, `pl_mass(j)%rsd_tot`, `sol_sumno3(j)`, `sol_sumsolp(j)`, `irrig(j)%applied` |
| 357 | data | `do iac = 1, d_tbl%acts > if (action == "y") then > select case (d_tbl%act(iac)%typ) / case ("fertilize") > if (pcom(j)%dtbl(idtbl)%num_actions(iac) <= Int(d_tbl%act(iac)%const2)) then > if (wet(j)%flo > 0. .and. chemapp_db(ifertop)%surf_frac == 1) then > if (pco%mgtout == "y") then` | `j`, `time%yrc`, `time%mo`, `time%day_mo`, `mgt%op_char`, `" FERT-WET"`, `phubase(j)`, `pcom(j)%plcur(ipl)%phuacc`, `soil(j)%sw`, `pl_mass(j)%tot(ipl)%m`, `pl_mass(j)%rsd_tot%m`, `sol_sumno3(j)`, `sol_sumsolp(j)`, `frt_kg`, `fertno3`, `fertnh3`, `fertorgn`, `fertsolp`, `fertorgp` |
| 365 | data | `do iac = 1, d_tbl%acts > if (action == "y") then > select case (d_tbl%act(iac)%typ) / case ("fertilize") > if (pcom(j)%dtbl(idtbl)%num_actions(iac) <= Int(d_tbl%act(iac)%const2)) then > if (wet(j)%flo > 0. .and. chemapp_db(ifertop)%surf_frac == 1) then / else > if (pco%mgtout == "y") then` | `j`, `time%yrc`, `time%mo`, `time%day_mo`, `mgt%op_char`, `"    FERT "`, `phubase(j)`, `pcom(j)%plcur(ipl)%phuacc`, `soil(j)%sw`, `pl_mass(j)%tot(ipl)%m`, `pl_mass(j)%rsd_tot%m`, `sol_sumno3(j)`, `sol_sumsolp(j)`, `frt_kg`, `fertno3`, `fertnh3`, `fertorgn`, `fertsolp`, `fertorgp` |
| 391 | data | `do iac = 1, d_tbl%acts > if (action == "y") then > select case (d_tbl%act(iac)%typ) / case ("manure") > if (pcom(j)%dtbl(idtbl)%num_actions(iac) <= Int(d_tbl%act(iac)%const2)) then > if (pco%mgtout == "y") then` | `j`, `time%yrc`, `time%mo`, `time%day_mo`, `mgt%op_char`, `" MANURE "`, `phubase(j)`, `pcom(j)%plcur(ipl)%phuacc`, `soil(j)%sw`, `pl_mass(j)%tot(ipl)%m`, `pl_mass(j)%rsd_tot%m`, `sol_sumno3(j)`, `sol_sumsolp(j)`, `frt_kg`, `fertno3`, `fertnh3`, `fertorgn`, `fertsolp`, `fertorgp` |
| 422 | data | `do iac = 1, d_tbl%acts > if (action == "y") then > select case (d_tbl%act(iac)%typ) / case ("till", "tillage") > if (pcom(j)%dtbl(idtbl)%num_actions(iac) <= Int(d_tbl%act(iac)%const2)) then > if (pco%mgtout == "y") then` | `j`, `time%yrc`, `time%mo`, `time%day_mo`, `tilldb(idtill)%tillnm`, `"    TILLAGE"`, `phubase(j)`, `pcom(j)%plcur(ipl)%phuacc`, `soil(j)%sw`, `pl_mass(j)%tot(ipl)%m`, `pl_mass(j)%rsd_tot%m`, `sol_sumno3(j)`, `sol_sumsolp(j)`, `tilldb(idtill)%effmix` |
| 460 | data | `do iac = 1, d_tbl%acts > if (action == "y") then > select case (d_tbl%act(iac)%typ) / case ("plant") > do ipl = 1, pcom(j)%npl > if (d_tbl%act(iac)%option == pcomdb(icom)%pl(ipl)%cpnm) then > if (pcom(j)%plcur(ipl)%gro == "n") then > if (pco%mgtout == "y") then` | `j`, `time%yrc`, `time%mo`, `time%day_mo`, `pldb(idp)%plantnm`, `"    PLANT"`, `phubase(j)`, `pcom(j)%plcur(ipl)%phuacc`, `soil(ihru)%sw`, `pl_mass(j)%tot(ipl)%m`, `pl_mass(j)%rsd_tot%m`, `sol_sumno3(j)`, `sol_sumsolp(j)`, `pcom(j)%plg(ipl)%lai`, `pcom(j)%plcur(ipl)%lai_pot` |
| 465 | data | `do iac = 1, d_tbl%acts > if (action == "y") then > select case (d_tbl%act(iac)%typ) / case ("plant") > do ipl = 1, pcom(j)%npl > if (d_tbl%act(iac)%option == pcomdb(icom)%pl(ipl)%cpnm) then > if (pcom(j)%plcur(ipl)%gro == "n") then > if (pco%mgtout == "y") then > if (pco%mgtout == "y") then` | `j`, `time%yrc`, `time%mo`, `time%day_mo`, `pldb(idp)%plantnm`, `"TRANSPLANT"`, `phubase(j)`, `pcom(j)%plcur(ipl)%phuacc`, `soil(ihru)%sw`, `pl_mass(j)%tot(ipl)%m`, `pl_mass(j)%rsd_tot%m`, `sol_sumno3(j)`, `sol_sumsolp(j)`, `pcom(j)%plg(ipl)%lai`, `pcom(j)%plcur(ipl)%lai_pot` |
| 472 | data | `do iac = 1, d_tbl%acts > if (action == "y") then > select case (d_tbl%act(iac)%typ) / case ("plant") > do ipl = 1, pcom(j)%npl > if (d_tbl%act(iac)%option == pcomdb(icom)%pl(ipl)%cpnm) then > if (pcom(j)%plcur(ipl)%gro == "n") then > if (pco%mgtout == "y") then / else > if (pco%mgtout == "y") then` | `j`, `time%yrc`, `time%mo`, `time%day_mo`, `pldb(idp)%plantnm`, `"    PLANT"`, `phubase(j)`, `pcom(j)%plcur(ipl)%phuacc`, `soil(ihru)%sw`, `pl_mass(j)%tot(ipl)%m`, `pl_mass(j)%rsd_tot%m`, `sol_sumno3(j)`, `sol_sumsolp(j)`, `pcom(j)%plg(ipl)%lai`, `pcom(j)%plcur(ipl)%lai_pot` |
| 481 | data | `do iac = 1, d_tbl%acts > if (action == "y") then > select case (d_tbl%act(iac)%typ) / case ("plant") > do ipl = 1, pcom(j)%npl > if (d_tbl%act(iac)%option == pcomdb(icom)%pl(ipl)%cpnm) then > if (pcom(j)%plcur(ipl)%gro == "n") then / else > if (pco%mgtout ==  "y") then` | `j`, `time%yrc`, `time%mo`, `time%day_mo`, `pldb(idp)%plantnm`, `"    PLANT_ALREADY_GROWING"`, `phubase(j)`, `pcom(j)%plcur(ipl)%phuacc`, `soil(j)%sw`, `pl_mass(j)%tot(ipl)%m`, `pl_mass(j)%rsd_tot%m`, `sol_sumno3(j)`, `sol_sumsolp(j)`, `pcom(j)%plg(ipl)%lai`, `pcom(j)%plcur(ipl)%lai_pot` |
| 565 | data | `do iac = 1, d_tbl%acts > if (action == "y") then > select case (d_tbl%act(iac)%typ) / case ("harvest") > if (pcom(j)%dtbl(idtbl)%num_actions(iac) <= Int(d_tbl%act(iac)%const2)) then > do ipl = 1, pcom(j)%npl > if (d_tbl%act(iac)%option == pcomdb(icom)%pl(ipl)%cpnm .or. d_tbl%act(iac)%option == "all") then > if (pco%mgtout == "y") then` | `j`, `time%yrc`, `time%mo`, `time%day_mo`, `pldb(idp)%plantnm`, `"    HARVEST"`, `phubase(j)`, `pcom(j)%plcur(ipl)%phuacc`, `soil(j)%sw`, `biomass`, `pl_mass(j)%rsd_tot%m`, `sol_sumno3(j)`, `sol_sumsolp(j)`, `pl_yield%m`, `pcom(j)%plstr(ipl)%sum_n`, `pcom(j)%plstr(ipl)%sum_p`, `pcom(j)%plstr(ipl)%sum_tmp`, `pcom(j)%plstr(ipl)%sum_w`, `pcom(j)%plstr(ipl)%sum_a` |
| 595 | data | `do iac = 1, d_tbl%acts > if (action == "y") then > select case (d_tbl%act(iac)%typ) / case ("kill") > if (pcom(j)%dtbl(idtbl)%num_actions(iac) <= Int(d_tbl%act(iac)%const2)) then > do ipl = 1, pcom(j)%npl > if (d_tbl%act(iac)%option == pcomdb(icom)%pl(ipl)%cpnm .or. d_tbl%act(iac)%option == "all") then > if (pco%mgtout == "y") then` | `j`, `time%yrc`, `time%mo`, `time%day_mo`, `pldb(idp)%plantnm`, `"         KILL"`, `phubase(j)`, `pcom(j)%plcur(ipl)%phuacc`, `soil(j)%sw`, `biomass`, `pl_mass(j)%rsd_tot%m`, `sol_sumno3(j)`, `sol_sumsolp(j)`, `yield`, `pcom(j)%plstr(ipl)%sum_n`, `pcom(j)%plstr(ipl)%sum_p`, `pcom(j)%plstr(ipl)%sum_tmp`, `pcom(j)%plstr(ipl)%sum_w`, `pcom(j)%plstr(ipl)%sum_a` |
| 683 | data | `do iac = 1, d_tbl%acts > if (action == "y") then > select case (d_tbl%act(iac)%typ) / case ("harvest_kill") > if (pcom(j)%dtbl(idtbl)%num_actions(iac) <= Int(d_tbl%act(iac)%const2)) then > do ipl = 1, pcom(j)%npl > if (d_tbl%act(iac)%option == pcomdb(icom)%pl(ipl)%cpnm .or. d_tbl%act(iac)%option == "all") then > if (pco%mgtout == "y") then` | `j`, `time%yrc`, `time%mo`, `time%day_mo`, `pldb(idp)%plantnm`, `"    HARV/KILL"`, `phubase(j)`, `pcom(j)%plcur(ipl)%phuacc`, `soil(j)%sw`, `biomass`, `pl_mass(j)%rsd_tot%m`, `sol_sumno3(j)`, `sol_sumsolp(j)`, `pl_yield%m`, `pcom(j)%plstr(ipl)%sum_n`, `pcom(j)%plstr(ipl)%sum_p`, `pcom(j)%plstr(ipl)%sum_tmp`, `pcom(j)%plstr(ipl)%sum_w`, `pcom(j)%plstr(ipl)%sum_a` |
| 745 | data | `do iac = 1, d_tbl%acts > if (action == "y") then > select case (d_tbl%act(iac)%typ) / case ("pest_apply") > if (pcom(j)%dtbl(idtbl)%num_actions(iac) <= Int(d_tbl%act(iac)%const2)) then > if (pco%mgtout == "y") then` | `j`, `time%yrc`, `time%mo`, `time%day_mo`, `d_tbl%act(iac)%option`, `"    PEST "`, `phubase(j)`, `pcom(j)%plcur(ipl)%phuacc`, `soil(j)%sw`, `pl_mass(j)%tot(ipl)%m`, `pl_mass(j)%rsd_tot%m`, `sol_sumno3(j)`, `sol_sumsolp(j)`, `pest_kg` |
| 880 | data | `do iac = 1, d_tbl%acts > if (action == "y") then > select case (d_tbl%act(iac)%typ) / case ("tiledep_control") > if (pcom(j)%dtbl(idtbl)%num_actions(iac) <= Int(d_tbl%act(iac)%const2)) then > if (pco%mgtout == "y") then` | `j`, `time%yrc`, `time%mo`, `time%day_mo`, `tilldb(idtill)%tillnm`, `"  DRAIN_CONTROL"`, `phubase(j)`, `pcom(j)%plcur(1)%phuacc`, `soil(j)%sw`, `pl_mass(j)%tot(1)%m`, `pl_mass(j)%rsd_tot%m`, `sol_sumno3(j)`, `sol_sumsolp(j)`, `hru(j)%lumv%sdr_dep` |
| 895 | data | `do iac = 1, d_tbl%acts > if (action == "y") then > select case (d_tbl%act(iac)%typ) / case ("impound_off") > if (pco%mgtout == "y") then` | `j`, `time%yrc`, `time%mo`, `time%day_mo`, `d_tbl%act(iac)%name`, `"IMPOUND OFF"` |
| 913 | data | `do iac = 1, d_tbl%acts > if (action == "y") then > select case (d_tbl%act(iac)%typ) / case ("impound_on") > if (pco%mgtout == "y") then` | `j`, `time%yrc`, `time%mo`, `time%day_mo`, `d_tbl%act(iac)%name`, `"IMPOUND ON"` |
| 933 | data | `do iac = 1, d_tbl%acts > if (action == "y") then > select case (d_tbl%act(iac)%typ) / case ("weir_height") > if (pco%mgtout == "y") then` | `j`, `time%yrc`, `time%mo`, `time%day_mo`, `d_tbl%act(iac)%name`, `"RESET WEIR HEIGHT (m)"`, `wet_ob(j)%weir_hgt` |
| 974 | data | `do iac = 1, d_tbl%acts > if (action == "y") then > select case (d_tbl%act(iac)%typ) / case ("puddle") > if (pcom(j)%dtbl(idtbl)%num_actions(iac) <= Int(d_tbl%act(iac)%const2)) then > if (pco%mgtout == "y") then` | `j`, `time%yrc`, `time%mo`, `time%day_mo`, `d_tbl%act(iac)%name`, `"PUDDLE"` |
| 1239 | data | `do iac = 1, d_tbl%acts > if (action == "y") then > select case (d_tbl%act(iac)%typ) / case ("burn") > if (pcom(j)%dtbl(idtbl)%num_actions(iac) <= Int(d_tbl%act(iac)%const2)) then > if (pco%mgtout == "y") then` | `j`, `time%yrc`, `time%mo`, `time%day_mo`, `d_tbl%act(iac)%name`, `"    BURN"`, `phubase(j)`, `pcom(j)%plcur(ipl)%phuacc`, `soil(j)%sw`, `pl_mass(j)%tot(ipl)%m`, `pl_mass(j)%rsd_tot%m`, `sol_sumno3(j)`, `sol_sumsolp(j)` |
| 1257 | data | `do iac = 1, d_tbl%acts > if (action == "y") then > select case (d_tbl%act(iac)%typ) / case ("cn_update") > if (pcom(j)%dtbl(idtbl)%num_actions(iac) <= Int(d_tbl%act(iac)%const2)) then > if (pco%mgtout == "y") then` | `j`, `time%yrc`, `time%mo`, `time%day_mo`, `d_tbl%act(iac)%name`, `"    CNUP"`, `phubase(j)`, `pcom(j)%plcur(ipl)%phuacc`, `soil(j)%sw`, `pl_mass(j)%tot(ipl)%m`, `pl_mass(j)%rsd_tot%m`, `sol_sumno3(j)`, `sol_sumsolp(j)`, `cn_prev`, `cn2(j)` |


- Procedure: `header_mgt`
- Writer: `header_mgt.f90`
- Match: source_output
- Resolved default filename(s): `mgt_out.txt`

| Line | Role | Condition | Fields written |
| --- | --- | --- | --- |
| 10 | data | `if (pco%mgtout == "y") then` | `bsn%name`, `prog` |
| 11 | data | `if (pco%mgtout == "y") then` | `mgt_hdr` |
| 12 | data | `if (pco%mgtout == "y") then` | `mgt_hdr_unt1` |


- Procedure: `mallo_control`
- Writer: `mallo_control.f90`
- Match: source_output
- Resolved default filename(s): `mgt_out.txt`

| Line | Role | Condition | Fields written |
| --- | --- | --- | --- |
| 70 | data | `do itrn = 1, mallo(imallo)%trn_obs > if (mallo(imallo)%trn(itrn)%manure_amt%app_t_ha > 0. .and. frt_kg > mallo(imallo)%src(isrc)%bal_d%stor) then > if (pco%mgtout == "y") then` | `j`, `time%yrc`, `time%mo`, `time%day_mo`, `fertdb(ifrt)%fertnm`, `"    MANU"`, `phubase(j)`, `pcom(j)%plcur(ipl)%phuacc`, `soil(j)%sw`, `pl_mass(j)%tot(ipl)%m`, `pl_mass(j)%rsd_tot%m`, `sol_sumno3(j)`, `sol_sumsolp(j)`, `frt_kg`, `fertno3`, `fertnh3`, `fertorgn`, `fertsolp`, `fertorgp` |


- Procedure: `mgt_sched`
- Writer: `mgt_sched.f90`
- Match: source_output
- Resolved default filename(s): `mgt_out.txt`

| Line | Role | Condition | Fields written |
| --- | --- | --- | --- |
| 112 | data | `select case (mgt%op) / case ("plnt") > do ipl = 1, pcom(j)%npl > if (mgt%op_char == pcomdb(icom)%pl(ipl)%cpnm) then > if (pcom(j)%plcur(ipl)%gro == "n") then > if (itr > 0) then > if (pco%mgtout ==  "y") then` | `j`, `time%yrc`, `time%mo`, `time%day_mo`, `pldb(idp)%plantnm`, `"TRANSPLANT "`, `phubase(j)`, `pcom(j)%plcur(ipl)%phuacc`, `soil(j)%sw`, `pl_mass(j)%tot(ipl)%m`, `pl_mass(j)%rsd_tot%m`, `sol_sumno3(j)`, `sol_sumsolp(j)`, `pcom(j)%plg(ipl)%lai`, `pcom(j)%plcur(ipl)%lai_pot` |
| 119 | data | `select case (mgt%op) / case ("plnt") > do ipl = 1, pcom(j)%npl > if (mgt%op_char == pcomdb(icom)%pl(ipl)%cpnm) then > if (pcom(j)%plcur(ipl)%gro == "n") then > if (itr > 0) then / else > if (pco%mgtout ==  "y") then` | `j`, `time%yrc`, `time%mo`, `time%day_mo`, `pldb(idp)%plantnm`, `"    PLANT "`, `phubase(j)`, `pcom(j)%plcur(ipl)%phuacc`, `soil(j)%sw`, `pl_mass(j)%tot(ipl)%m`, `pl_mass(j)%rsd_tot%m`, `sol_sumno3(j)`, `sol_sumsolp(j)`, `pcom(j)%plg(ipl)%lai`, `pcom(j)%plcur(ipl)%lai_pot` |
| 128 | data | `select case (mgt%op) / case ("plnt") > do ipl = 1, pcom(j)%npl > if (mgt%op_char == pcomdb(icom)%pl(ipl)%cpnm) then > if (pcom(j)%plcur(ipl)%gro == "n") then / else > if (pco%mgtout ==  "y") then` | `j`, `time%yrc`, `time%mo`, `time%day_mo`, `pldb(idp)%plantnm`, `"    PLANT_ALREADY_GROWING"`, `phubase(j)`, `pcom(j)%plcur(ipl)%phuacc`, `soil(j)%sw`, `pl_mass(j)%tot(ipl)%m`, `pl_mass(j)%rsd_tot%m`, `sol_sumno3(j)`, `sol_sumsolp(j)`, `pcom(j)%plg(ipl)%lai`, `pcom(j)%plcur(ipl)%lai_pot` |
| 213 | data | `select case (mgt%op) / case ("harv") > do ipl = 1, pcom(j)%npl > if (pcom(j)%plcur(ipl)%gro == "y") then > if (mgt%op_char == pcomdb(icom)%pl(ipl)%cpnm .or. mgt%op_char == "all") then > if (pco%mgtout == "y") then` | `j`, `time%yrc`, `time%mo`, `time%day_mo`, `pldb(idp)%plantnm`, `"    HARVEST "`, `phubase(j)`, `pcom(j)%plcur(ipl)%phuacc`, `soil(j)%sw`, `biomass`, `pl_mass(j)%rsd_tot%m`, `sol_sumno3(j)`, `sol_sumsolp(j)`, `pl_yield%m`, `pcom(j)%plstr(ipl)%sum_n`, `pcom(j)%plstr(ipl)%sum_p`, `pcom(j)%plstr(ipl)%sum_tmp`, `pcom(j)%plstr(ipl)%sum_w`, `pcom(j)%plstr(ipl)%sum_a` |
| 234 | data | `select case (mgt%op) / case ("harv") > do ipl = 1, pcom(j)%npl > if (pcom(j)%plcur(ipl)%gro == "y") then / else > if (mgt%op_char == pcomdb(icom)%pl(ipl)%cpnm .or. mgt%op_char == "all") then > if (pco%mgtout == "y") then` | `j`, `time%yrc`, `time%mo`, `time%day_mo`, `pldb(idp)%plantnm`, `"    HARVEST "`, `phubase(j)`, `pcom(j)%plcur(ipl)%phuacc`, `soil(j)%sw`, `biomass`, `pl_mass(j)%rsd_tot%m`, `sol_sumno3(j)`, `sol_sumsolp(j)`, `pl_yield%m`, `pcom(j)%plstr(ipl)%sum_n`, `pcom(j)%plstr(ipl)%sum_p`, `pcom(j)%plstr(ipl)%sum_tmp`, `pcom(j)%plstr(ipl)%sum_w`, `pcom(j)%plstr(ipl)%sum_a` |
| 254 | data | `select case (mgt%op) / case ("kill") > do ipl = 1, pcom(j)%npl > if (pcom(j)%plcur(ipl)%gro == "y") then > if (mgt%op_char == pcomdb(icom)%pl(ipl)%cpnm .or. mgt%op_char == "all") then > if (pco%mgtout == "y") then` | `j`, `time%yrc`, `time%mo`, `time%day_mo`, `pldb(idp)%plantnm`, `"    KILL "`, `phubase(j)`, `pcom(j)%plcur(ipl)%phuacc`, `soil(j)%sw`, `biomass`, `pl_mass(j)%rsd_tot%m`, `sol_sumno3(j)`, `sol_sumsolp(j)`, `pl_yield%m`, `pcom(j)%plstr(ipl)%sum_n`, `pcom(j)%plstr(ipl)%sum_p`, `pcom(j)%plstr(ipl)%sum_tmp`, `pcom(j)%plstr(ipl)%sum_w`, `pcom(j)%plstr(ipl)%sum_a` |
| 324 | data | `select case (mgt%op) / case ("hvkl") > do ipl = 1, pcom(j)%npl > if (pcom(j)%plcur(ipl)%gro == "y") then > if (mgt%op_char == pcomdb(icom)%pl(ipl)%cpnm .or. mgt%op_char == "all") then > if (pco%mgtout == "y") then` | `j`, `time%yrc`, `time%mo`, `time%day_mo`, `pldb(idp)%plantnm`, `"    HARV/KILL "`, `phubase(j)`, `pcom(j)%plcur(ipl)%phuacc`, `soil(j)%sw`, `biomass`, `pl_mass(j)%rsd_tot%m`, `sol_sumno3(j)`, `sol_sumsolp(j)`, `pl_yield%m`, `pcom(j)%plstr(ipl)%sum_n`, `pcom(j)%plstr(ipl)%sum_p`, `pcom(j)%plstr(ipl)%sum_tmp`, `pcom(j)%plstr(ipl)%sum_w`, `pcom(j)%plstr(ipl)%sum_a` |
| 353 | data | `select case (mgt%op) / case ("till") > if (pco%mgtout == "y") then` | `j`, `time%yrc`, `time%mo`, `time%day_mo`, `tilldb(idtill)%tillnm`, `"    TILLAGE "`, `phubase(j)`, `pcom(j)%plcur(ipl)%phuacc`, `soil(j)%sw`, `pl_mass(j)%tot(ipl)%m`, `pl_mass(j)%rsd_tot%m`, `sol_sumno3(j)`, `sol_sumsolp(j)`, `tilldb(idtill)%effmix` |
| 370 | data | `select case (mgt%op) / case ("irrm") > if (pco%mgtout == "y") then` | `j`, `time%yrc`, `time%mo`, `time%day_mo`, `irrop_db(irrop)%name`, `"IRRIGATE "`, `phubase(j)`, `pcom(j)%plcur(ipl)%phuacc`, `soil(j)%sw`, `pl_mass(j)%tot(ipl)%m`, `pl_mass(j)%rsd_tot%m`, `sol_sumno3(j)`, `sol_sumsolp(j)`, `irrig(j)%applied`, `irrig(j)%runoff` |
| 385 | data | `select case (mgt%op) / case ("fert") > if (wet(j)%flo>0.) then > if (pco%mgtout == "y") then` | `j`, `time%yrc`, `time%mo`, `time%day_mo`, `mgt%op_char`, `" FERT-WET"`, `phubase(j)`, `pcom(j)%plcur(ipl)%phuacc`, `soil(j)%sw`, `pl_mass(j)%tot(ipl)%m`, `pl_mass(j)%rsd_tot%m`, `sol_sumno3(j)`, `sol_sumsolp(j)`, `frt_kg`, `fertno3`, `fertnh3`, `fertorgn`, `fertsolp`, `fertorgp` |
| 395 | data | `select case (mgt%op) / case ("fert") > if (wet(j)%flo>0.) then / else > if (pco%mgtout == "y") then` | `j`, `time%yrc`, `time%mo`, `time%day_mo`, `mgt%op_char`, `"    FERT "`, `phubase(j)`, `pcom(j)%plcur(ipl)%phuacc`, `soil(j)%sw`, `pl_mass(j)%tot(ipl)%m`, `pl_mass(j)%rsd_tot%m`, `sol_sumno3(j)`, `sol_sumsolp(j)`, `frt_kg`, `fertno3`, `fertnh3`, `fertorgn`, `fertsolp`, `fertorgp` |
| 411 | data | `select case (mgt%op) / case ("manu") > if (pco%mgtout == "y") then` | `j`, `time%yrc`, `time%mo`, `time%day_mo`, `mgt%op_char`, `" MANURE "`, `phubase(j)`, `pcom(j)%plcur(ipl)%phuacc`, `soil(j)%sw`, `pl_mass(j)%tot(ipl)%m`, `pl_mass(j)%rsd_tot%m`, `sol_sumno3(j)`, `sol_sumsolp(j)`, `frt_kg`, `fertno3`, `fertnh3`, `fertorgn`, `fertsolp`, `fertorgp` |
| 434 | data | `select case (mgt%op) / case ("pest") > if (pco%mgtout == "y") then` | `j`, `time%yrc`, `time%mo`, `time%day_mo`, `mgt%op_char`, `"    PEST "`, `phubase(j)`, `pcom(j)%plcur(ipl)%phuacc`, `soil(j)%sw`, `pl_mass(j)%tot(ipl)%m`, `pl_mass(j)%rsd_tot%m`, `sol_sumno3(j)`, `sol_sumsolp(j)`, `pest_kg` |
| 447 | data | `select case (mgt%op) / case ("graz") > if (pco%mgtout == "y") then` | `j`, `time%yrc`, `time%mo`, `time%day_mo`, `mgt%op_char`, `"    GRAZE "`, `phubase(j)`, `pcom(j)%plcur(ipl)%phuacc`, `soil(j)%sw`, `pl_mass(j)%tot(ipl)%m`, `pl_mass(j)%rsd_tot%m`, `sol_sumno3(j)`, `sol_sumsolp(j)`, `grazeop_db(mgt%op1)%eat`, `grazeop_db(mgt%op1)%manure` |
| 461 | data | `select case (mgt%op) / case ("cnup") > if (pco%mgtout == "y") then` | `j`, `time%yrc`, `time%mo`, `time%day_mo`, `mgt%op_char`, `"    CNUP "`, `phubase(j)`, `pcom(j)%plcur(ipl)%phuacc`, `soil(j)%sw`, `pl_mass(j)%tot(ipl)%m`, `pl_mass(j)%rsd_tot%m`, `sol_sumno3(j)`, `sol_sumsolp(j)`, `mgt%op3`, `cn2(j)` |
| 472 | data | `select case (mgt%op) / case ("burn") > if (pco%mgtout == "y") then > do ipl = 1, pcom(j)%npl` | `j`, `time%yrc`, `time%mo`, `time%day_mo`, `mgt%op_char`, `"    BURN "`, `phubase(j)`, `pcom(j)%plcur(ipl)%phuacc`, `soil(j)%sw`, `pl_mass(j)%tot(ipl)%m`, `pl_mass(j)%rsd_tot%m`, `sol_sumno3(j)`, `sol_sumsolp(j)` |
| 485 | data | `select case (mgt%op) / case ("swep") > if (pco%mgtout == "y") then` | `j`, `time%yrc`, `time%mo`, `time%day_mo`, `mgt%op_char`, `"STREET_SWEEP "`, `phubase(j)`, `pcom(j)%plcur(ipl)%phuacc`, `soil(j)%sw`, `pl_mass(j)%tot(ipl)%m`, `pl_mass(j)%rsd_tot%m`, `sol_sumno3(j)`, `sol_sumsolp(j)` |
| 502 | data | `select case (mgt%op) / case ("dwm") > if (pco%mgtout ==  "y") then` | `j`, `time%yrc`, `time%mo`, `time%day_mo`, `pldb(idp)%plantnm`, `"  DRAIN_CONTROL"`, `phubase(j)`, `pcom(j)%plcur(j)%phuacc`, `soil(j)%sw`, `pl_mass(j)%tot(j)%m`, `pl_mass(j)%rsd_tot%m`, `sol_sumno3(j)`, `sol_sumsolp(j)`, `hru(j)%lumv%sdr_dep` |
| 525 | data | `select case (mgt%op) / case ("weir") > if (pco%mgtout == "y") then` | `j`, `time%yrc`, `time%mo`, `time%day_mo`, `mgt%op_char`, `"RESET WEIR HEIGHT (m)"`, `wet_ob(j)%weir_hgt` |
| 542 | data | `select case (mgt%op) / case ("irrp") > if (mgt%op3 < 0) then > if (hru(j)%irr_hmax>0) then > if (pco%mgtout == "y") then` | `j`, `time%yrc`, `time%mo`, `time%day_mo`, `mgt%op_char`, `"BEGIN/ADJUST PADDY IRRIGATION"`, `hru(j)%irr_hmax` |
| 551 | data | `select case (mgt%op) / case ("irrp") > if (mgt%op3 < 0) then / else > if (mgt%op3 > 0) then > if (pco%mgtout == "y") then` | `j`, `time%yrc`, `time%mo`, `time%day_mo`, `mgt%op_char`, `"BEGIN/ADJUST PADDY IRRIGATION"`, `hru(j)%irr_hmax` |
| 557 | data | `select case (mgt%op) / case ("irrp") > if (mgt%op3 < 0) then / else > if (mgt%op3 > 0) then / else > if (pco%mgtout == "y") then` | `j`, `time%yrc`, `time%mo`, `time%day_mo`, `mgt%op_char`, `"STOP PADDY IRRIGATION"`, `hru(j)%irr_hmax` |
| 565 | data | `select case (mgt%op) / case ("irrp") > if (pco%mgtout == "y") then` | `j`, `time%yrc`, `time%mo`, `time%day_mo`, `mgt%op_char`, `"BEGIN_PADDY_IRRIGATION "`, `phubase(j)`, `pcom(j)%plcur(ipl)%phuacc`, `soil(j)%sw`, `pl_mass(j)%tot(ipl)%m`, `pl_mass(j)%rsd_tot%m`, `sol_sumno3(j)`, `sol_sumsolp(j)`, `mgt%op3`, `mgt%op4` |
| 583 | data | `select case (mgt%op) / case ("irpm") > if (pco%mgtout == "y") then` | `j`, `time%yrc`, `time%mo`, `time%day_mo`, `mgt%op_char`, `"IRRIGATE "`, `phubase(j)`, `pcom(j)%plcur(ipl)%phuacc`, `soil(j)%sw`, `pl_mass(j)%tot(ipl)%m`, `pl_mass(j)%rsd_tot%m`, `sol_sumno3(j)`, `sol_sumsolp(j)`, `irrig(j)%applied`, `irrig(j)%runoff` |
| 618 | data | `select case (mgt%op) / case ("pudl") > if (pco%mgtout == "y") then` | `j`, `time%yrc`, `time%mo`, `time%day_mo`, `mgt%op_char`, `"PUDDLE"` |


- Procedure: `wallo_pou_deliv`
- Writer: `wallo_pou_deliv.f90`
- Match: source_output
- Resolved default filename(s): `mgt_out.txt`

| Line | Role | Condition | Fields written |
| --- | --- | --- | --- |
| 73 | data | `select case (pou(ipou)%typ) / case ("irr") > do ird = 1, pou(ipou)%irr%hru_num > if (irrig(j)%demand < water_avail) then > if (pco%mgtout == "y") then` | `j`, `time%yrc`, `time%mo`, `time%day_mo`, `"WATER ALLO"`, `"IRRIGATE"`, `phubase(j)`, `pcom(j)%plcur(1)%phuacc`, `soil(j)%sw`, `pl_mass(j)%tot(1)%m`, `pl_mass(j)%rsd_tot%m`, `sol_sumno3(j)`, `sol_sumsolp(j)`, `irrig(j)%applied` |

### `water_allo_aa.csv`

- Review needed: yes
- Writer procedures changed: yes
- Write-block count changed: yes
- Write conditions changed: yes
- Write roles changed: yes
- Base flattened write order: `bsn%name`, `prog`, `wallo_hdr`, `wallo_hdr_units`, `time%day`, `time%mo`, `time%day_mo`, `time%yrc`, `itrn`, `wallo(iwallo)%trn(itrn)%trn_typ`, `wallo(iwallo)%trn(itrn)%num`, `wallo(iwallo)%trn(itrn)%num`, `wallo(iwallo)%trn(itrn)%num`, `(wallo(iwallo)%trn(itrn)%src(isrc)%typ, wallo(iwallo)%trn(itrn)%src(isrc)%num, walloa_out(iwallo)%trn(itrn)%src(isrc), isrc = 1, wallo(iwallo)%trn(itrn)%src_num)`, `time%mo`, `time%day_mo`, `time%yrc`, `itrt`, `om_treat_name(itrt)`, `wal_tr_oma(itrt)`, `time%day`, `time%mo`, `time%day_mo`, `time%yrc`, `itrn`, `wallo(iwallo)%trn(itrn)%trn_typ`, `wallo(iwallo)%trn(itrn)%num`, `wallo(iwallo)%trn(itrn)%num`, `wallo(iwallo)%trn(itrn)%num`, `(wallo(iwallo)%trn(itrn)%src(isrc)%typ, wallo(iwallo)%trn(itrn)%src(isrc)%num, wal_oma(iwallo)%trn(itrn)%src(isrc)%hd, isrc = 1, wallo(iwallo)%trn(itrn)%src_num)`, `time%mo`, `time%day_mo`, `time%yrc`, `iuse`, `om_use_name(iuse)`, `wal_use_oma(iuse)`
- Candidate flattened write order: `bsn%name`, `prog`, `wallo_hdr`, `wallo_hdr_units`, `time%day`, `time%mo`, `time%day_mo`, `"POU "`, `ipou`, `time%yrc`, `ipou`, `pou(ipou)%name`, `poua_met(ipou)%duty_tot%duty`, `poua_met(ipou)%duty_tot%deliv`, `"     POD "`, `ipod`, `poua_met(ipou)%pod(ipod)%duty`, `poua_met(ipou)%pod(ipod)%deliv`, `poua_om(ipou)%pod(ipod)`, `"     POR "`, `ipor`, `poua_om(ipou)%por(ipor)`

#### Write-order edits

- `insert` at base index 7 / candidate index 7: removed _no fields captured_; added `"POU "`, `ipou`
- `replace` at base index 8 / candidate index 10: removed `itrn`, `wallo(iwallo)%trn(itrn)%trn_typ`, `wallo(iwallo)%trn(itrn)%num`, `wallo(iwallo)%trn(itrn)%num`, `wallo(iwallo)%trn(itrn)%num`, `(wallo(iwallo)%trn(itrn)%src(isrc)%typ, wallo(iwallo)%trn(itrn)%src(isrc)%num, walloa_out(iwallo)%trn(itrn)%src(isrc), isrc = 1, wallo(iwallo)%trn(itrn)%src_num)`, `time%mo`, `time%day_mo`, `time%yrc`, `itrt`, `om_treat_name(itrt)`, `wal_tr_oma(itrt)`, `time%day`, `time%mo`, `time%day_mo`, `time%yrc`, `itrn`, `wallo(iwallo)%trn(itrn)%trn_typ`, `wallo(iwallo)%trn(itrn)%num`, `wallo(iwallo)%trn(itrn)%num`, `wallo(iwallo)%trn(itrn)%num`, `(wallo(iwallo)%trn(itrn)%src(isrc)%typ, wallo(iwallo)%trn(itrn)%src(isrc)%num, wal_oma(iwallo)%trn(itrn)%src(isrc)%hd, isrc = 1, wallo(iwallo)%trn(itrn)%src_num)`, `time%mo`, `time%day_mo`, `time%yrc`, `iuse`, `om_use_name(iuse)`, `wal_use_oma(iuse)`; added `ipou`, `pou(ipou)%name`, `poua_met(ipou)%duty_tot%duty`, `poua_met(ipou)%duty_tot%deliv`, `"     POD "`, `ipod`, `poua_met(ipou)%pod(ipod)%duty`, `poua_met(ipou)%pod(ipod)%deliv`, `poua_om(ipou)%pod(ipod)`, `"     POR "`, `ipor`, `poua_om(ipou)%por(ipor)`

#### Base write structure

- Source expression(s): _none captured_

- Procedure: `header_water_allocation`
- Writer: `header_water_allocation.f90`
- Match: source_output
- Resolved default filename(s): `water_allo_aa.csv`

| Line | Role | Condition | Fields written |
| --- | --- | --- | --- |
| 71 | data | `if (db_mx%wallo_db > 0) then > if (pco%water_allo%a == "y") then > if (pco%csvout == "y") then` | `bsn%name`, `prog` |
| 72 | data | `if (db_mx%wallo_db > 0) then > if (pco%water_allo%a == "y") then > if (pco%csvout == "y") then` | `wallo_hdr` |
| 73 | data | `if (db_mx%wallo_db > 0) then > if (pco%water_allo%a == "y") then > if (pco%csvout == "y") then` | `wallo_hdr_units` |


- Procedure: `wallo_allo_output`
- Writer: `wallo_allo_output.f90`
- Match: source_output
- Resolved default filename(s): `water_allo_aa.csv`

| Line | Role | Condition | Fields written |
| --- | --- | --- | --- |
| 111 | data | `do itrn = 1, wallo(iwallo)%trn_obs > if (time%end_sim == 1) then > if (pco%water_allo%a == "y") then > if (pco%csvout == "y") then` | `time%day`, `time%mo`, `time%day_mo`, `time%yrc`, `itrn`, `wallo(iwallo)%trn(itrn)%trn_typ`, `wallo(iwallo)%trn(itrn)%num`, `wallo(iwallo)%trn(itrn)%num`, `wallo(iwallo)%trn(itrn)%num`, `(wallo(iwallo)%trn(itrn)%src(isrc)%typ, wallo(iwallo)%trn(itrn)%src(isrc)%num, walloa_out(iwallo)%trn(itrn)%src(isrc), isrc = 1, wallo(iwallo)%trn(itrn)%src_num)` |


- Procedure: `wallo_treat_output`
- Writer: `wallo_treat_output.f90`
- Match: source_output
- Resolved default filename(s): `water_allo_aa.csv`

| Line | Role | Condition | Fields written |
| --- | --- | --- | --- |
| 71 | data | `do itrt = 1, db_mx%wtp > if (time%end_sim == 1) then > if (pco%water_allo%a == "y") then > if (pco%csvout == "y") then` | `time%mo`, `time%day_mo`, `time%yrc`, `itrt`, `om_treat_name(itrt)`, `wal_tr_oma(itrt)` |


- Procedure: `wallo_trn_output`
- Writer: `wallo_trn_output.f90`
- Match: source_output
- Resolved default filename(s): `water_allo_aa.csv`

| Line | Role | Condition | Fields written |
| --- | --- | --- | --- |
| 111 | data | `do itrn = 1, wallo(iwallo)%trn_obs > if (time%end_sim == 1) then > if (pco%water_allo%a == "y") then > if (pco%csvout == "y") then` | `time%day`, `time%mo`, `time%day_mo`, `time%yrc`, `itrn`, `wallo(iwallo)%trn(itrn)%trn_typ`, `wallo(iwallo)%trn(itrn)%num`, `wallo(iwallo)%trn(itrn)%num`, `wallo(iwallo)%trn(itrn)%num`, `(wallo(iwallo)%trn(itrn)%src(isrc)%typ, wallo(iwallo)%trn(itrn)%src(isrc)%num, wal_oma(iwallo)%trn(itrn)%src(isrc)%hd, isrc = 1, wallo(iwallo)%trn(itrn)%src_num)` |


- Procedure: `wallo_use_output`
- Writer: `wallo_use_output.f90`
- Match: source_output
- Resolved default filename(s): `water_allo_aa.csv`

| Line | Role | Condition | Fields written |
| --- | --- | --- | --- |
| 71 | data | `do iuse = 1, db_mx%uses > if (time%end_sim == 1) then > if (pco%water_allo%a == "y") then > if (pco%csvout == "y") then` | `time%mo`, `time%day_mo`, `time%yrc`, `iuse`, `om_use_name(iuse)`, `wal_use_oma(iuse)` |


#### Candidate write structure

- Source expression(s): _none captured_

- Procedure: `header_water_allocation`
- Writer: `header_water_allocation.f90`
- Match: source_output
- Resolved default filename(s): `water_allo_aa.csv`

| Line | Role | Condition | Fields written |
| --- | --- | --- | --- |
| 64 | data | `if (pco%water_allo%a == "y") then > if (pco%csvout == "y") then` | `bsn%name`, `prog` |
| 65 | data | `if (pco%water_allo%a == "y") then > if (pco%csvout == "y") then` | `wallo_hdr` |
| 66 | data | `if (pco%water_allo%a == "y") then > if (pco%csvout == "y") then` | `wallo_hdr_units` |


- Procedure: `wallo_pou_output`
- Writer: `wallo_pou_output.f90`
- Match: source_output
- Resolved default filename(s): `water_allo_aa.csv`

| Line | Role | Condition | Fields written |
| --- | --- | --- | --- |
| 209 | data | `if (time%end_sim == 1 .and. time%yrs_prt > 0) then > if (pco%water_allo%a == "y") then > if (pco%csvout == "y") then` | `time%day`, `time%mo`, `time%day_mo`, `"POU "`, `ipou`, `time%yrc`, `ipou`, `pou(ipou)%name`, `poua_met(ipou)%duty_tot%duty`, `poua_met(ipou)%duty_tot%deliv` |
| 213 | data | `if (time%end_sim == 1 .and. time%yrs_prt > 0) then > if (pco%water_allo%a == "y") then > if (pco%csvout == "y") then > do ipod = 1, pou(ipou)%pods` | `"     POD "`, `ipod`, `poua_met(ipou)%pod(ipod)%duty`, `poua_met(ipou)%pod(ipod)%deliv`, `poua_om(ipou)%pod(ipod)` |
| 217 | data | `if (time%end_sim == 1 .and. time%yrs_prt > 0) then > if (pco%water_allo%a == "y") then > if (pco%csvout == "y") then > do ipor = 1, pou(ipou)%pors` | `"     POR "`, `ipor`, `poua_om(ipou)%por(ipor)` |

### `water_allo_aa.txt`

- Review needed: yes
- Writer procedures changed: yes
- Write-block count changed: yes
- Write conditions changed: yes
- Write roles changed: yes
- Base flattened write order: `bsn%name`, `prog`, `wallo_hdr`, `wallo_hdr_units`, `time%day`, `time%mo`, `time%day_mo`, `time%yrc`, `itrn`, `wallo(iwallo)%trn(itrn)%trn_typ`, `wallo(iwallo)%trn(itrn)%num`, `wallo(iwallo)%trn(itrn)%num`, `wallo(iwallo)%trn(itrn)%num`, `(wallo(iwallo)%trn(itrn)%src(isrc)%typ, wallo(iwallo)%trn(itrn)%src(isrc)%num, walloa_out(iwallo)%trn(itrn)%src(isrc), isrc = 1, wallo(iwallo)%trn(itrn)%src_num)`, `time%mo`, `time%day_mo`, `time%yrc`, `itrt`, `om_treat_name(itrt)`, `wal_tr_oma(itrt)`, `time%day`, `time%mo`, `time%day_mo`, `time%yrc`, `itrn`, `wallo(iwallo)%trn(itrn)%trn_typ`, `wallo(iwallo)%trn(itrn)%num`, `wallo(iwallo)%trn(itrn)%num`, `wallo(iwallo)%trn(itrn)%num`, `(wallo(iwallo)%trn(itrn)%src(isrc)%typ, wallo(iwallo)%trn(itrn)%src(isrc)%num, wal_oma(iwallo)%trn(itrn)%src(isrc)%hd, isrc = 1, wallo(iwallo)%trn(itrn)%src_num)`, `time%mo`, `time%day_mo`, `time%yrc`, `iuse`, `om_use_name(iuse)`, `wal_use_oma(iuse)`
- Candidate flattened write order: `bsn%name`, `prog`, `wallo_hdr`, `wallo_hdr_units`, `time%day`, `time%mo`, `time%day_mo`, `time%yrc`, `"POU "`, `ipou`, `pou(ipou)%name`, `poua_met(ipou)%duty_tot%duty`, `poua_met(ipou)%duty_tot%deliv`, `"                 POD "`, `ipod`, `poua_met(ipou)%pod(ipod)%duty`, `poua_met(ipou)%pod(ipod)%deliv`, `poua_om(ipou)%pod(ipod)`, `"                 POR "`, `ipor`, `poua_om(ipou)%por(ipor)`

#### Write-order edits

- `replace` at base index 8 / candidate index 8: removed `itrn`, `wallo(iwallo)%trn(itrn)%trn_typ`, `wallo(iwallo)%trn(itrn)%num`, `wallo(iwallo)%trn(itrn)%num`, `wallo(iwallo)%trn(itrn)%num`, `(wallo(iwallo)%trn(itrn)%src(isrc)%typ, wallo(iwallo)%trn(itrn)%src(isrc)%num, walloa_out(iwallo)%trn(itrn)%src(isrc), isrc = 1, wallo(iwallo)%trn(itrn)%src_num)`, `time%mo`, `time%day_mo`, `time%yrc`, `itrt`, `om_treat_name(itrt)`, `wal_tr_oma(itrt)`, `time%day`, `time%mo`, `time%day_mo`, `time%yrc`, `itrn`, `wallo(iwallo)%trn(itrn)%trn_typ`, `wallo(iwallo)%trn(itrn)%num`, `wallo(iwallo)%trn(itrn)%num`, `wallo(iwallo)%trn(itrn)%num`, `(wallo(iwallo)%trn(itrn)%src(isrc)%typ, wallo(iwallo)%trn(itrn)%src(isrc)%num, wal_oma(iwallo)%trn(itrn)%src(isrc)%hd, isrc = 1, wallo(iwallo)%trn(itrn)%src_num)`, `time%mo`, `time%day_mo`, `time%yrc`, `iuse`, `om_use_name(iuse)`, `wal_use_oma(iuse)`; added `"POU "`, `ipou`, `pou(ipou)%name`, `poua_met(ipou)%duty_tot%duty`, `poua_met(ipou)%duty_tot%deliv`, `"                 POD "`, `ipod`, `poua_met(ipou)%pod(ipod)%duty`, `poua_met(ipou)%pod(ipod)%deliv`, `poua_om(ipou)%pod(ipod)`, `"                 POR "`, `ipor`, `poua_om(ipou)%por(ipor)`

#### Base write structure

- Source expression(s): _none captured_

- Procedure: `header_water_allocation`
- Writer: `header_water_allocation.f90`
- Match: source_output
- Resolved default filename(s): `water_allo_aa.txt`

| Line | Role | Condition | Fields written |
| --- | --- | --- | --- |
| 65 | data | `if (db_mx%wallo_db > 0) then > if (pco%water_allo%a == "y") then` | `bsn%name`, `prog` |
| 66 | data | `if (db_mx%wallo_db > 0) then > if (pco%water_allo%a == "y") then` | `wallo_hdr` |
| 67 | data | `if (db_mx%wallo_db > 0) then > if (pco%water_allo%a == "y") then` | `wallo_hdr_units` |


- Procedure: `wallo_allo_output`
- Writer: `wallo_allo_output.f90`
- Match: source_output
- Resolved default filename(s): `water_allo_aa.txt`

| Line | Role | Condition | Fields written |
| --- | --- | --- | --- |
| 105 | data | `do itrn = 1, wallo(iwallo)%trn_obs > if (time%end_sim == 1) then > if (pco%water_allo%a == "y") then` | `time%day`, `time%mo`, `time%day_mo`, `time%yrc`, `itrn`, `wallo(iwallo)%trn(itrn)%trn_typ`, `wallo(iwallo)%trn(itrn)%num`, `wallo(iwallo)%trn(itrn)%num`, `wallo(iwallo)%trn(itrn)%num`, `(wallo(iwallo)%trn(itrn)%src(isrc)%typ, wallo(iwallo)%trn(itrn)%src(isrc)%num, walloa_out(iwallo)%trn(itrn)%src(isrc), isrc = 1, wallo(iwallo)%trn(itrn)%src_num)` |


- Procedure: `wallo_treat_output`
- Writer: `wallo_treat_output.f90`
- Match: source_output
- Resolved default filename(s): `water_allo_aa.txt`

| Line | Role | Condition | Fields written |
| --- | --- | --- | --- |
| 68 | data | `do itrt = 1, db_mx%wtp > if (time%end_sim == 1) then > if (pco%water_allo%a == "y") then` | `time%mo`, `time%day_mo`, `time%yrc`, `itrt`, `om_treat_name(itrt)`, `wal_tr_oma(itrt)` |


- Procedure: `wallo_trn_output`
- Writer: `wallo_trn_output.f90`
- Match: source_output
- Resolved default filename(s): `water_allo_aa.txt`

| Line | Role | Condition | Fields written |
| --- | --- | --- | --- |
| 105 | data | `do itrn = 1, wallo(iwallo)%trn_obs > if (time%end_sim == 1) then > if (pco%water_allo%a == "y") then` | `time%day`, `time%mo`, `time%day_mo`, `time%yrc`, `itrn`, `wallo(iwallo)%trn(itrn)%trn_typ`, `wallo(iwallo)%trn(itrn)%num`, `wallo(iwallo)%trn(itrn)%num`, `wallo(iwallo)%trn(itrn)%num`, `(wallo(iwallo)%trn(itrn)%src(isrc)%typ, wallo(iwallo)%trn(itrn)%src(isrc)%num, wal_oma(iwallo)%trn(itrn)%src(isrc)%hd, isrc = 1, wallo(iwallo)%trn(itrn)%src_num)` |


- Procedure: `wallo_use_output`
- Writer: `wallo_use_output.f90`
- Match: source_output
- Resolved default filename(s): `water_allo_aa.txt`

| Line | Role | Condition | Fields written |
| --- | --- | --- | --- |
| 68 | data | `do iuse = 1, db_mx%uses > if (time%end_sim == 1) then > if (pco%water_allo%a == "y") then` | `time%mo`, `time%day_mo`, `time%yrc`, `iuse`, `om_use_name(iuse)`, `wal_use_oma(iuse)` |


#### Candidate write structure

- Source expression(s): _none captured_

- Procedure: `header_water_allocation`
- Writer: `header_water_allocation.f90`
- Match: source_output
- Resolved default filename(s): `water_allo_aa.txt`

| Line | Role | Condition | Fields written |
| --- | --- | --- | --- |
| 58 | data | `if (pco%water_allo%a == "y") then` | `bsn%name`, `prog` |
| 59 | data | `if (pco%water_allo%a == "y") then` | `wallo_hdr` |
| 60 | data | `if (pco%water_allo%a == "y") then` | `wallo_hdr_units` |


- Procedure: `wallo_pou_output`
- Writer: `wallo_pou_output.f90`
- Match: source_output
- Resolved default filename(s): `water_allo_aa.txt`

| Line | Role | Condition | Fields written |
| --- | --- | --- | --- |
| 198 | data | `if (time%end_sim == 1 .and. time%yrs_prt > 0) then > if (pco%water_allo%a == "y") then` | `time%day`, `time%mo`, `time%day_mo`, `time%yrc`, `"POU "`, `ipou`, `pou(ipou)%name`, `poua_met(ipou)%duty_tot%duty`, `poua_met(ipou)%duty_tot%deliv` |
| 201 | data | `if (time%end_sim == 1 .and. time%yrs_prt > 0) then > if (pco%water_allo%a == "y") then > do ipod = 1, pou(ipou)%pods` | `"                 POD "`, `ipod`, `poua_met(ipou)%pod(ipod)%duty`, `poua_met(ipou)%pod(ipod)%deliv`, `poua_om(ipou)%pod(ipod)` |
| 205 | data | `if (time%end_sim == 1 .and. time%yrs_prt > 0) then > if (pco%water_allo%a == "y") then > do ipor = 1, pou(ipou)%pors` | `"                 POR "`, `ipor`, `poua_om(ipou)%por(ipor)` |

### `water_allo_day.csv`

- Review needed: yes
- Writer procedures changed: yes
- Write-block count changed: yes
- Write conditions changed: yes
- Write roles changed: yes
- Base flattened write order: `bsn%name`, `prog`, `wallo_hdr`, `wallo_hdr_units`, `time%day`, `time%mo`, `time%day_mo`, `time%yrc`, `itrn`, `wallo(iwallo)%trn(itrn)%trn_typ`, `wallo(iwallo)%trn(itrn)%num`, `wallo(iwallo)%trn(itrn)%num`, `wallo(iwallo)%trn(itrn)%num`, `(wallo(iwallo)%trn(itrn)%src(isrc)%typ, wallo(iwallo)%trn(itrn)%src(isrc)%num, wallod_out(iwallo)%trn(itrn)%src(isrc), isrc = 1, wallo(iwallo)%trn(itrn)%src_num)`, `time%mo`, `time%day_mo`, `time%yrc`, `itrt`, `om_treat_name(itrt)`, `wal_tr_omd(itrt)`, `time%day`, `time%mo`, `time%day_mo`, `time%yrc`, `itrn`, `wallo(iwallo)%trn(itrn)%trn_typ`, `wallo(iwallo)%trn(itrn)%num`, `wallo(iwallo)%trn(itrn)%num`, `wallo(iwallo)%trn(itrn)%num`, `(wallo(iwallo)%trn(itrn)%src(isrc)%typ, wallo(iwallo)%trn(itrn)%src(isrc)%num, wal_omd(iwallo)%trn(itrn)%src(isrc)%hd, isrc = 1, wallo(iwallo)%trn(itrn)%src_num)`, `time%mo`, `time%day_mo`, `time%yrc`, `iuse`, `om_use_name(iuse)`, `wal_use_omd(iuse)`
- Candidate flattened write order: `bsn%name`, `prog`, `wallo_hdr`, `wallo_hdr_units`, `time%day`, `time%mo`, `time%day_mo`, `ipou`, `"POU "`, `time%yrc`, `ipou`, `pou(ipou)%name`, `poud_met(ipou)%duty_tot%duty`, `poud_met(ipou)%duty_tot%deliv`, `"     POD "`, `ipod`, `poud_met(ipou)%pod(ipod)%duty`, `poud_met(ipou)%pod(ipod)%deliv`, `poud_om(ipou)%pod(ipod)`, `" POR "`, `ipor`, `poud_om(ipou)%por(ipor)`

#### Write-order edits

- `insert` at base index 7 / candidate index 7: removed _no fields captured_; added `ipou`, `"POU "`
- `replace` at base index 8 / candidate index 10: removed `itrn`, `wallo(iwallo)%trn(itrn)%trn_typ`, `wallo(iwallo)%trn(itrn)%num`, `wallo(iwallo)%trn(itrn)%num`, `wallo(iwallo)%trn(itrn)%num`, `(wallo(iwallo)%trn(itrn)%src(isrc)%typ, wallo(iwallo)%trn(itrn)%src(isrc)%num, wallod_out(iwallo)%trn(itrn)%src(isrc), isrc = 1, wallo(iwallo)%trn(itrn)%src_num)`, `time%mo`, `time%day_mo`, `time%yrc`, `itrt`, `om_treat_name(itrt)`, `wal_tr_omd(itrt)`, `time%day`, `time%mo`, `time%day_mo`, `time%yrc`, `itrn`, `wallo(iwallo)%trn(itrn)%trn_typ`, `wallo(iwallo)%trn(itrn)%num`, `wallo(iwallo)%trn(itrn)%num`, `wallo(iwallo)%trn(itrn)%num`, `(wallo(iwallo)%trn(itrn)%src(isrc)%typ, wallo(iwallo)%trn(itrn)%src(isrc)%num, wal_omd(iwallo)%trn(itrn)%src(isrc)%hd, isrc = 1, wallo(iwallo)%trn(itrn)%src_num)`, `time%mo`, `time%day_mo`, `time%yrc`, `iuse`, `om_use_name(iuse)`, `wal_use_omd(iuse)`; added `ipou`, `pou(ipou)%name`, `poud_met(ipou)%duty_tot%duty`, `poud_met(ipou)%duty_tot%deliv`, `"     POD "`, `ipod`, `poud_met(ipou)%pod(ipod)%duty`, `poud_met(ipou)%pod(ipod)%deliv`, `poud_om(ipou)%pod(ipod)`, `" POR "`, `ipor`, `poud_om(ipou)%por(ipor)`

#### Base write structure

- Source expression(s): _none captured_

- Procedure: `header_water_allocation`
- Writer: `header_water_allocation.f90`
- Match: source_output
- Resolved default filename(s): `water_allo_day.csv`

| Line | Role | Condition | Fields written |
| --- | --- | --- | --- |
| 20 | data | `if (db_mx%wallo_db > 0) then > if (pco%water_allo%d == "y") then > if (pco%csvout == "y") then` | `bsn%name`, `prog` |
| 21 | data | `if (db_mx%wallo_db > 0) then > if (pco%water_allo%d == "y") then > if (pco%csvout == "y") then` | `wallo_hdr` |
| 22 | data | `if (db_mx%wallo_db > 0) then > if (pco%water_allo%d == "y") then > if (pco%csvout == "y") then` | `wallo_hdr_units` |


- Procedure: `wallo_allo_output`
- Writer: `wallo_allo_output.f90`
- Match: source_output
- Resolved default filename(s): `water_allo_day.csv`

| Line | Role | Condition | Fields written |
| --- | --- | --- | --- |
| 30 | data | `do itrn = 1, wallo(iwallo)%trn_obs > if (pco%water_allo%d == "y") then > if (pco%csvout == "y") then` | `time%day`, `time%mo`, `time%day_mo`, `time%yrc`, `itrn`, `wallo(iwallo)%trn(itrn)%trn_typ`, `wallo(iwallo)%trn(itrn)%num`, `wallo(iwallo)%trn(itrn)%num`, `wallo(iwallo)%trn(itrn)%num`, `(wallo(iwallo)%trn(itrn)%src(isrc)%typ, wallo(iwallo)%trn(itrn)%src(isrc)%num, wallod_out(iwallo)%trn(itrn)%src(isrc), isrc = 1, wallo(iwallo)%trn(itrn)%src_num)` |


- Procedure: `wallo_treat_output`
- Writer: `wallo_treat_output.f90`
- Match: source_output
- Resolved default filename(s): `water_allo_day.csv`

| Line | Role | Condition | Fields written |
| --- | --- | --- | --- |
| 21 | data | `do itrt = 1, db_mx%wtp > if (pco%water_allo%d == "y") then > if (pco%csvout == "y") then` | `time%mo`, `time%day_mo`, `time%yrc`, `itrt`, `om_treat_name(itrt)`, `wal_tr_omd(itrt)` |


- Procedure: `wallo_trn_output`
- Writer: `wallo_trn_output.f90`
- Match: source_output
- Resolved default filename(s): `water_allo_day.csv`

| Line | Role | Condition | Fields written |
| --- | --- | --- | --- |
| 30 | data | `do itrn = 1, wallo(iwallo)%trn_obs > if (pco%water_allo%d == "y") then > if (pco%csvout == "y") then` | `time%day`, `time%mo`, `time%day_mo`, `time%yrc`, `itrn`, `wallo(iwallo)%trn(itrn)%trn_typ`, `wallo(iwallo)%trn(itrn)%num`, `wallo(iwallo)%trn(itrn)%num`, `wallo(iwallo)%trn(itrn)%num`, `(wallo(iwallo)%trn(itrn)%src(isrc)%typ, wallo(iwallo)%trn(itrn)%src(isrc)%num, wal_omd(iwallo)%trn(itrn)%src(isrc)%hd, isrc = 1, wallo(iwallo)%trn(itrn)%src_num)` |


- Procedure: `wallo_use_output`
- Writer: `wallo_use_output.f90`
- Match: source_output
- Resolved default filename(s): `water_allo_day.csv`

| Line | Role | Condition | Fields written |
| --- | --- | --- | --- |
| 21 | data | `do iuse = 1, db_mx%uses > if (pco%water_allo%d == "y") then > if (pco%csvout == "y") then` | `time%mo`, `time%day_mo`, `time%yrc`, `iuse`, `om_use_name(iuse)`, `wal_use_omd(iuse)` |


#### Candidate write structure

- Source expression(s): _none captured_

- Procedure: `header_water_allocation`
- Writer: `header_water_allocation.f90`
- Match: source_output
- Resolved default filename(s): `water_allo_day.csv`

| Line | Role | Condition | Fields written |
| --- | --- | --- | --- |
| 19 | data | `if (pco%water_allo%d == "y") then > if (pco%csvout == "y") then` | `bsn%name`, `prog` |
| 20 | data | `if (pco%water_allo%d == "y") then > if (pco%csvout == "y") then` | `wallo_hdr` |
| 21 | data | `if (pco%water_allo%d == "y") then > if (pco%csvout == "y") then` | `wallo_hdr_units` |


- Procedure: `wallo_pou_output`
- Writer: `wallo_pou_output.f90`
- Match: source_output
- Resolved default filename(s): `water_allo_day.csv`

| Line | Role | Condition | Fields written |
| --- | --- | --- | --- |
| 40 | data | `if (pco%water_allo%d == "y") then > if (pco%csvout == "y") then` | `time%day`, `time%mo`, `time%day_mo`, `ipou`, `"POU "`, `time%yrc`, `ipou`, `pou(ipou)%name`, `poud_met(ipou)%duty_tot%duty`, `poud_met(ipou)%duty_tot%deliv` |
| 44 | data | `if (pco%water_allo%d == "y") then > if (pco%csvout == "y") then > do ipod = 1, pou(ipou)%pods` | `"     POD "`, `ipod`, `poud_met(ipou)%pod(ipod)%duty`, `poud_met(ipou)%pod(ipod)%deliv`, `poud_om(ipou)%pod(ipod)` |
| 48 | data | `if (pco%water_allo%d == "y") then > if (pco%csvout == "y") then > do ipor = 1, pou(ipou)%pors` | `" POR "`, `ipor`, `poud_om(ipou)%por(ipor)` |

### `water_allo_day.txt`

- Review needed: yes
- Writer procedures changed: yes
- Write-block count changed: yes
- Write conditions changed: yes
- Write roles changed: yes
- Base flattened write order: `bsn%name`, `prog`, `wallo_hdr`, `wallo_hdr_units`, `time%day`, `time%mo`, `time%day_mo`, `time%yrc`, `itrn`, `wallo(iwallo)%trn(itrn)%trn_typ`, `wallo(iwallo)%trn(itrn)%num`, `wallo(iwallo)%trn(itrn)%num`, `wallo(iwallo)%trn(itrn)%num`, `(wallo(iwallo)%trn(itrn)%src(isrc)%typ, wallo(iwallo)%trn(itrn)%src(isrc)%num, wallod_out(iwallo)%trn(itrn)%src(isrc), isrc = 1, wallo(iwallo)%trn(itrn)%src_num)`, `time%day`, `time%mo`, `time%day_mo`, `time%yrc`, `itrt`, `om_treat_name(itrt)`, `wal_tr_omd(itrt)`, `time%day`, `time%mo`, `time%day_mo`, `time%yrc`, `itrn`, `wallo(iwallo)%trn(itrn)%trn_typ`, `wallo(iwallo)%trn(itrn)%num`, `wallo(iwallo)%trn(itrn)%num`, `wallo(iwallo)%trn(itrn)%num`, `(wallo(iwallo)%trn(itrn)%src(isrc)%typ, wallo(iwallo)%trn(itrn)%src(isrc)%num, wal_omd(iwallo)%trn(itrn)%src(isrc)%hd, isrc = 1, wallo(iwallo)%trn(itrn)%src_num)`, `time%day`, `time%mo`, `time%day_mo`, `time%yrc`, `iuse`, `om_use_name(iuse)`, `wal_use_omd(iuse)`
- Candidate flattened write order: `bsn%name`, `prog`, `wallo_hdr`, `wallo_hdr_units`, `time%day`, `time%mo`, `time%day_mo`, `time%yrc`, `ipou`, `"POU "`, `pou(ipou)%name`, `poud_met(ipou)%duty_tot%duty`, `poud_met(ipou)%duty_tot%deliv`, `"                 POD "`, `ipod`, `poud_met(ipou)%pod(ipod)%duty`, `poud_met(ipou)%pod(ipod)%deliv`, `poud_om(ipou)%pod(ipod)`, `"                 POR "`, `ipor`, `poud_om(ipou)%por(ipor)`

#### Write-order edits

- `replace` at base index 8 / candidate index 8: removed `itrn`, `wallo(iwallo)%trn(itrn)%trn_typ`, `wallo(iwallo)%trn(itrn)%num`, `wallo(iwallo)%trn(itrn)%num`, `wallo(iwallo)%trn(itrn)%num`, `(wallo(iwallo)%trn(itrn)%src(isrc)%typ, wallo(iwallo)%trn(itrn)%src(isrc)%num, wallod_out(iwallo)%trn(itrn)%src(isrc), isrc = 1, wallo(iwallo)%trn(itrn)%src_num)`, `time%day`, `time%mo`, `time%day_mo`, `time%yrc`, `itrt`, `om_treat_name(itrt)`, `wal_tr_omd(itrt)`, `time%day`, `time%mo`, `time%day_mo`, `time%yrc`, `itrn`, `wallo(iwallo)%trn(itrn)%trn_typ`, `wallo(iwallo)%trn(itrn)%num`, `wallo(iwallo)%trn(itrn)%num`, `wallo(iwallo)%trn(itrn)%num`, `(wallo(iwallo)%trn(itrn)%src(isrc)%typ, wallo(iwallo)%trn(itrn)%src(isrc)%num, wal_omd(iwallo)%trn(itrn)%src(isrc)%hd, isrc = 1, wallo(iwallo)%trn(itrn)%src_num)`, `time%day`, `time%mo`, `time%day_mo`, `time%yrc`, `iuse`, `om_use_name(iuse)`, `wal_use_omd(iuse)`; added `ipou`, `"POU "`, `pou(ipou)%name`, `poud_met(ipou)%duty_tot%duty`, `poud_met(ipou)%duty_tot%deliv`, `"                 POD "`, `ipod`, `poud_met(ipou)%pod(ipod)%duty`, `poud_met(ipou)%pod(ipod)%deliv`, `poud_om(ipou)%pod(ipod)`, `"                 POR "`, `ipor`, `poud_om(ipou)%por(ipor)`

#### Base write structure

- Source expression(s): _none captured_

- Procedure: `header_water_allocation`
- Writer: `header_water_allocation.f90`
- Match: source_output
- Resolved default filename(s): `water_allo_day.txt`

| Line | Role | Condition | Fields written |
| --- | --- | --- | --- |
| 14 | data | `if (db_mx%wallo_db > 0) then > if (pco%water_allo%d == "y") then` | `bsn%name`, `prog` |
| 15 | data | `if (db_mx%wallo_db > 0) then > if (pco%water_allo%d == "y") then` | `wallo_hdr` |
| 16 | data | `if (db_mx%wallo_db > 0) then > if (pco%water_allo%d == "y") then` | `wallo_hdr_units` |


- Procedure: `wallo_allo_output`
- Writer: `wallo_allo_output.f90`
- Match: source_output
- Resolved default filename(s): `water_allo_day.txt`

| Line | Role | Condition | Fields written |
| --- | --- | --- | --- |
| 24 | data | `do itrn = 1, wallo(iwallo)%trn_obs > if (pco%water_allo%d == "y") then` | `time%day`, `time%mo`, `time%day_mo`, `time%yrc`, `itrn`, `wallo(iwallo)%trn(itrn)%trn_typ`, `wallo(iwallo)%trn(itrn)%num`, `wallo(iwallo)%trn(itrn)%num`, `wallo(iwallo)%trn(itrn)%num`, `(wallo(iwallo)%trn(itrn)%src(isrc)%typ, wallo(iwallo)%trn(itrn)%src(isrc)%num, wallod_out(iwallo)%trn(itrn)%src(isrc), isrc = 1, wallo(iwallo)%trn(itrn)%src_num)` |


- Procedure: `wallo_treat_output`
- Writer: `wallo_treat_output.f90`
- Match: source_output
- Resolved default filename(s): `water_allo_day.txt`

| Line | Role | Condition | Fields written |
| --- | --- | --- | --- |
| 18 | data | `do itrt = 1, db_mx%wtp > if (pco%water_allo%d == "y") then` | `time%day`, `time%mo`, `time%day_mo`, `time%yrc`, `itrt`, `om_treat_name(itrt)`, `wal_tr_omd(itrt)` |


- Procedure: `wallo_trn_output`
- Writer: `wallo_trn_output.f90`
- Match: source_output
- Resolved default filename(s): `water_allo_day.txt`

| Line | Role | Condition | Fields written |
| --- | --- | --- | --- |
| 24 | data | `do itrn = 1, wallo(iwallo)%trn_obs > if (pco%water_allo%d == "y") then` | `time%day`, `time%mo`, `time%day_mo`, `time%yrc`, `itrn`, `wallo(iwallo)%trn(itrn)%trn_typ`, `wallo(iwallo)%trn(itrn)%num`, `wallo(iwallo)%trn(itrn)%num`, `wallo(iwallo)%trn(itrn)%num`, `(wallo(iwallo)%trn(itrn)%src(isrc)%typ, wallo(iwallo)%trn(itrn)%src(isrc)%num, wal_omd(iwallo)%trn(itrn)%src(isrc)%hd, isrc = 1, wallo(iwallo)%trn(itrn)%src_num)` |


- Procedure: `wallo_use_output`
- Writer: `wallo_use_output.f90`
- Match: source_output
- Resolved default filename(s): `water_allo_day.txt`

| Line | Role | Condition | Fields written |
| --- | --- | --- | --- |
| 18 | data | `do iuse = 1, db_mx%uses > if (pco%water_allo%d == "y") then` | `time%day`, `time%mo`, `time%day_mo`, `time%yrc`, `iuse`, `om_use_name(iuse)`, `wal_use_omd(iuse)` |


#### Candidate write structure

- Source expression(s): _none captured_

- Procedure: `header_water_allocation`
- Writer: `header_water_allocation.f90`
- Match: source_output
- Resolved default filename(s): `water_allo_day.txt`

| Line | Role | Condition | Fields written |
| --- | --- | --- | --- |
| 13 | data | `if (pco%water_allo%d == "y") then` | `bsn%name`, `prog` |
| 14 | data | `if (pco%water_allo%d == "y") then` | `wallo_hdr` |
| 15 | data | `if (pco%water_allo%d == "y") then` | `wallo_hdr_units` |


- Procedure: `wallo_pou_output`
- Writer: `wallo_pou_output.f90`
- Match: source_output
- Resolved default filename(s): `water_allo_day.txt`

| Line | Role | Condition | Fields written |
| --- | --- | --- | --- |
| 29 | data | `if (pco%water_allo%d == "y") then` | `time%day`, `time%mo`, `time%day_mo`, `time%yrc`, `ipou`, `"POU "`, `pou(ipou)%name`, `poud_met(ipou)%duty_tot%duty`, `poud_met(ipou)%duty_tot%deliv` |
| 32 | data | `if (pco%water_allo%d == "y") then > do ipod = 1, pou(ipou)%pods` | `"                 POD "`, `ipod`, `poud_met(ipou)%pod(ipod)%duty`, `poud_met(ipou)%pod(ipod)%deliv`, `poud_om(ipou)%pod(ipod)` |
| 36 | data | `if (pco%water_allo%d == "y") then > do ipor = 1, pou(ipou)%pors` | `"                 POR "`, `ipor`, `poud_om(ipou)%por(ipor)` |

### `water_allo_mon.csv`

- Review needed: yes
- Writer procedures changed: yes
- Write-block count changed: yes
- Write conditions changed: yes
- Write roles changed: yes
- Base flattened write order: `bsn%name`, `prog`, `wallo_hdr`, `wallo_hdr_units`, `time%day`, `time%mo`, `time%day_mo`, `time%yrc`, `itrn`, `wallo(iwallo)%trn(itrn)%trn_typ`, `wallo(iwallo)%trn(itrn)%num`, `wallo(iwallo)%trn(itrn)%num`, `wallo(iwallo)%trn(itrn)%num`, `(wallo(iwallo)%trn(itrn)%src(isrc)%typ, wallo(iwallo)%trn(itrn)%src(isrc)%num, wallom_out(iwallo)%trn(itrn)%src(isrc), isrc = 1, wallo(iwallo)%trn(itrn)%src_num)`, `time%mo`, `time%day_mo`, `time%yrc`, `itrt`, `om_treat_name(itrt)`, `wal_tr_omm(itrt)`, `time%day`, `time%mo`, `time%day_mo`, `time%yrc`, `itrn`, `wallo(iwallo)%trn(itrn)%trn_typ`, `wallo(iwallo)%trn(itrn)%num`, `wallo(iwallo)%trn(itrn)%num`, `wallo(iwallo)%trn(itrn)%num`, `(wallo(iwallo)%trn(itrn)%src(isrc)%typ, wallo(iwallo)%trn(itrn)%src(isrc)%num, wal_omm(iwallo)%trn(itrn)%src(isrc)%hd, isrc = 1, wallo(iwallo)%trn(itrn)%src_num)`, `time%mo`, `time%day_mo`, `time%yrc`, `iuse`, `om_use_name(iuse)`, `wal_use_omm(iuse)`
- Candidate flattened write order: `bsn%name`, `prog`, `wallo_hdr`, `wallo_hdr_units`, `time%day`, `time%mo`, `time%day_mo`, `"POU "`, `ipou`, `time%yrc`, `ipou`, `pou(ipou)%name`, `poum_met(ipou)%duty_tot%duty`, `poum_met(ipou)%duty_tot%deliv`, `"     POD "`, `ipod`, `poum_met(ipou)%pod(ipod)%duty`, `poum_met(ipou)%pod(ipod)%deliv`, `poum_om(ipou)%pod(ipod)`, `"     POR "`, `ipor`, `poum_om(ipou)%por(ipor)`

#### Write-order edits

- `insert` at base index 7 / candidate index 7: removed _no fields captured_; added `"POU "`, `ipou`
- `replace` at base index 8 / candidate index 10: removed `itrn`, `wallo(iwallo)%trn(itrn)%trn_typ`, `wallo(iwallo)%trn(itrn)%num`, `wallo(iwallo)%trn(itrn)%num`, `wallo(iwallo)%trn(itrn)%num`, `(wallo(iwallo)%trn(itrn)%src(isrc)%typ, wallo(iwallo)%trn(itrn)%src(isrc)%num, wallom_out(iwallo)%trn(itrn)%src(isrc), isrc = 1, wallo(iwallo)%trn(itrn)%src_num)`, `time%mo`, `time%day_mo`, `time%yrc`, `itrt`, `om_treat_name(itrt)`, `wal_tr_omm(itrt)`, `time%day`, `time%mo`, `time%day_mo`, `time%yrc`, `itrn`, `wallo(iwallo)%trn(itrn)%trn_typ`, `wallo(iwallo)%trn(itrn)%num`, `wallo(iwallo)%trn(itrn)%num`, `wallo(iwallo)%trn(itrn)%num`, `(wallo(iwallo)%trn(itrn)%src(isrc)%typ, wallo(iwallo)%trn(itrn)%src(isrc)%num, wal_omm(iwallo)%trn(itrn)%src(isrc)%hd, isrc = 1, wallo(iwallo)%trn(itrn)%src_num)`, `time%mo`, `time%day_mo`, `time%yrc`, `iuse`, `om_use_name(iuse)`, `wal_use_omm(iuse)`; added `ipou`, `pou(ipou)%name`, `poum_met(ipou)%duty_tot%duty`, `poum_met(ipou)%duty_tot%deliv`, `"     POD "`, `ipod`, `poum_met(ipou)%pod(ipod)%duty`, `poum_met(ipou)%pod(ipod)%deliv`, `poum_om(ipou)%pod(ipod)`, `"     POR "`, `ipor`, `poum_om(ipou)%por(ipor)`

#### Base write structure

- Source expression(s): _none captured_

- Procedure: `header_water_allocation`
- Writer: `header_water_allocation.f90`
- Match: source_output
- Resolved default filename(s): `water_allo_mon.csv`

| Line | Role | Condition | Fields written |
| --- | --- | --- | --- |
| 37 | data | `if (db_mx%wallo_db > 0) then > if (pco%water_allo%m == "y") then > if (pco%csvout == "y") then` | `bsn%name`, `prog` |
| 38 | data | `if (db_mx%wallo_db > 0) then > if (pco%water_allo%m == "y") then > if (pco%csvout == "y") then` | `wallo_hdr` |
| 39 | data | `if (db_mx%wallo_db > 0) then > if (pco%water_allo%m == "y") then > if (pco%csvout == "y") then` | `wallo_hdr_units` |


- Procedure: `wallo_allo_output`
- Writer: `wallo_allo_output.f90`
- Match: source_output
- Resolved default filename(s): `water_allo_mon.csv`

| Line | Role | Condition | Fields written |
| --- | --- | --- | --- |
| 56 | data | `do itrn = 1, wallo(iwallo)%trn_obs > if (time%end_mo == 1) then > if (pco%water_allo%m == "y") then > if (pco%csvout == "y") then` | `time%day`, `time%mo`, `time%day_mo`, `time%yrc`, `itrn`, `wallo(iwallo)%trn(itrn)%trn_typ`, `wallo(iwallo)%trn(itrn)%num`, `wallo(iwallo)%trn(itrn)%num`, `wallo(iwallo)%trn(itrn)%num`, `(wallo(iwallo)%trn(itrn)%src(isrc)%typ, wallo(iwallo)%trn(itrn)%src(isrc)%num, wallom_out(iwallo)%trn(itrn)%src(isrc), isrc = 1, wallo(iwallo)%trn(itrn)%src_num)` |


- Procedure: `wallo_treat_output`
- Writer: `wallo_treat_output.f90`
- Match: source_output
- Resolved default filename(s): `water_allo_mon.csv`

| Line | Role | Condition | Fields written |
| --- | --- | --- | --- |
| 37 | data | `do itrt = 1, db_mx%wtp > if (time%end_mo == 1) then > if (pco%water_allo%m == "y") then > if (pco%csvout == "y") then` | `time%mo`, `time%day_mo`, `time%yrc`, `itrt`, `om_treat_name(itrt)`, `wal_tr_omm(itrt)` |


- Procedure: `wallo_trn_output`
- Writer: `wallo_trn_output.f90`
- Match: source_output
- Resolved default filename(s): `water_allo_mon.csv`

| Line | Role | Condition | Fields written |
| --- | --- | --- | --- |
| 56 | data | `do itrn = 1, wallo(iwallo)%trn_obs > if (time%end_mo == 1) then > if (pco%water_allo%m == "y") then > if (pco%csvout == "y") then` | `time%day`, `time%mo`, `time%day_mo`, `time%yrc`, `itrn`, `wallo(iwallo)%trn(itrn)%trn_typ`, `wallo(iwallo)%trn(itrn)%num`, `wallo(iwallo)%trn(itrn)%num`, `wallo(iwallo)%trn(itrn)%num`, `(wallo(iwallo)%trn(itrn)%src(isrc)%typ, wallo(iwallo)%trn(itrn)%src(isrc)%num, wal_omm(iwallo)%trn(itrn)%src(isrc)%hd, isrc = 1, wallo(iwallo)%trn(itrn)%src_num)` |


- Procedure: `wallo_use_output`
- Writer: `wallo_use_output.f90`
- Match: source_output
- Resolved default filename(s): `water_allo_mon.csv`

| Line | Role | Condition | Fields written |
| --- | --- | --- | --- |
| 37 | data | `do iuse = 1, db_mx%uses > if (time%end_mo == 1) then > if (pco%water_allo%m == "y") then > if (pco%csvout == "y") then` | `time%mo`, `time%day_mo`, `time%yrc`, `iuse`, `om_use_name(iuse)`, `wal_use_omm(iuse)` |


#### Candidate write structure

- Source expression(s): _none captured_

- Procedure: `header_water_allocation`
- Writer: `header_water_allocation.f90`
- Match: source_output
- Resolved default filename(s): `water_allo_mon.csv`

| Line | Role | Condition | Fields written |
| --- | --- | --- | --- |
| 34 | data | `if (pco%water_allo%m == "y") then > if (pco%csvout == "y") then` | `bsn%name`, `prog` |
| 35 | data | `if (pco%water_allo%m == "y") then > if (pco%csvout == "y") then` | `wallo_hdr` |
| 36 | data | `if (pco%water_allo%m == "y") then > if (pco%csvout == "y") then` | `wallo_hdr_units` |


- Procedure: `wallo_pou_output`
- Writer: `wallo_pou_output.f90`
- Match: source_output
- Resolved default filename(s): `water_allo_mon.csv`

| Line | Role | Condition | Fields written |
| --- | --- | --- | --- |
| 96 | data | `if (time%end_mo == 1) then > if (pco%water_allo%m == "y") then > if (pco%csvout == "y") then` | `time%day`, `time%mo`, `time%day_mo`, `"POU "`, `ipou`, `time%yrc`, `ipou`, `pou(ipou)%name`, `poum_met(ipou)%duty_tot%duty`, `poum_met(ipou)%duty_tot%deliv` |
| 100 | data | `if (time%end_mo == 1) then > if (pco%water_allo%m == "y") then > if (pco%csvout == "y") then > do ipod = 1, pou(ipou)%pods` | `"     POD "`, `ipod`, `poum_met(ipou)%pod(ipod)%duty`, `poum_met(ipou)%pod(ipod)%deliv`, `poum_om(ipou)%pod(ipod)` |
| 104 | data | `if (time%end_mo == 1) then > if (pco%water_allo%m == "y") then > if (pco%csvout == "y") then > do ipor = 1, pou(ipou)%pors` | `"     POR "`, `ipor`, `poum_om(ipou)%por(ipor)` |

### `water_allo_mon.txt`

- Review needed: yes
- Writer procedures changed: yes
- Write-block count changed: yes
- Write conditions changed: yes
- Write roles changed: yes
- Base flattened write order: `bsn%name`, `prog`, `wallo_hdr`, `wallo_hdr_units`, `time%day`, `time%mo`, `time%day_mo`, `time%yrc`, `itrn`, `wallo(iwallo)%trn(itrn)%trn_typ`, `wallo(iwallo)%trn(itrn)%num`, `wallo(iwallo)%trn(itrn)%num`, `wallo(iwallo)%trn(itrn)%num`, `(wallo(iwallo)%trn(itrn)%src(isrc)%typ, wallo(iwallo)%trn(itrn)%src(isrc)%num, wallom_out(iwallo)%trn(itrn)%src(isrc), isrc = 1, wallo(iwallo)%trn(itrn)%src_num)`, `time%mo`, `time%day_mo`, `time%yrc`, `itrt`, `om_treat_name(itrt)`, `wal_tr_omm(itrt)`, `time%day`, `time%mo`, `time%day_mo`, `time%yrc`, `itrn`, `wallo(iwallo)%trn(itrn)%trn_typ`, `wallo(iwallo)%trn(itrn)%num`, `wallo(iwallo)%trn(itrn)%num`, `wallo(iwallo)%trn(itrn)%num`, `(wallo(iwallo)%trn(itrn)%src(isrc)%typ, wallo(iwallo)%trn(itrn)%src(isrc)%num, wal_omm(iwallo)%trn(itrn)%src(isrc)%hd, isrc = 1, wallo(iwallo)%trn(itrn)%src_num)`, `time%mo`, `time%day_mo`, `time%yrc`, `iuse`, `om_use_name(iuse)`, `wal_use_omm(iuse)`
- Candidate flattened write order: `bsn%name`, `prog`, `wallo_hdr`, `wallo_hdr_units`, `time%day`, `time%mo`, `time%day_mo`, `time%yrc`, `"POU "`, `ipou`, `pou(ipou)%name`, `poum_met(ipou)%duty_tot%duty`, `poum_met(ipou)%duty_tot%deliv`, `"                 POD "`, `ipod`, `poum_met(ipou)%pod(ipod)%duty`, `poum_met(ipou)%pod(ipod)%deliv`, `poum_om(ipou)%pod(ipod)`, `"                 POR "`, `ipor`, `poum_om(ipou)%por(ipor)`

#### Write-order edits

- `replace` at base index 8 / candidate index 8: removed `itrn`, `wallo(iwallo)%trn(itrn)%trn_typ`, `wallo(iwallo)%trn(itrn)%num`, `wallo(iwallo)%trn(itrn)%num`, `wallo(iwallo)%trn(itrn)%num`, `(wallo(iwallo)%trn(itrn)%src(isrc)%typ, wallo(iwallo)%trn(itrn)%src(isrc)%num, wallom_out(iwallo)%trn(itrn)%src(isrc), isrc = 1, wallo(iwallo)%trn(itrn)%src_num)`, `time%mo`, `time%day_mo`, `time%yrc`, `itrt`, `om_treat_name(itrt)`, `wal_tr_omm(itrt)`, `time%day`, `time%mo`, `time%day_mo`, `time%yrc`, `itrn`, `wallo(iwallo)%trn(itrn)%trn_typ`, `wallo(iwallo)%trn(itrn)%num`, `wallo(iwallo)%trn(itrn)%num`, `wallo(iwallo)%trn(itrn)%num`, `(wallo(iwallo)%trn(itrn)%src(isrc)%typ, wallo(iwallo)%trn(itrn)%src(isrc)%num, wal_omm(iwallo)%trn(itrn)%src(isrc)%hd, isrc = 1, wallo(iwallo)%trn(itrn)%src_num)`, `time%mo`, `time%day_mo`, `time%yrc`, `iuse`, `om_use_name(iuse)`, `wal_use_omm(iuse)`; added `"POU "`, `ipou`, `pou(ipou)%name`, `poum_met(ipou)%duty_tot%duty`, `poum_met(ipou)%duty_tot%deliv`, `"                 POD "`, `ipod`, `poum_met(ipou)%pod(ipod)%duty`, `poum_met(ipou)%pod(ipod)%deliv`, `poum_om(ipou)%pod(ipod)`, `"                 POR "`, `ipor`, `poum_om(ipou)%por(ipor)`

#### Base write structure

- Source expression(s): _none captured_

- Procedure: `header_water_allocation`
- Writer: `header_water_allocation.f90`
- Match: source_output
- Resolved default filename(s): `water_allo_mon.txt`

| Line | Role | Condition | Fields written |
| --- | --- | --- | --- |
| 31 | data | `if (db_mx%wallo_db > 0) then > if (pco%water_allo%m == "y") then` | `bsn%name`, `prog` |
| 32 | data | `if (db_mx%wallo_db > 0) then > if (pco%water_allo%m == "y") then` | `wallo_hdr` |
| 33 | data | `if (db_mx%wallo_db > 0) then > if (pco%water_allo%m == "y") then` | `wallo_hdr_units` |


- Procedure: `wallo_allo_output`
- Writer: `wallo_allo_output.f90`
- Match: source_output
- Resolved default filename(s): `water_allo_mon.txt`

| Line | Role | Condition | Fields written |
| --- | --- | --- | --- |
| 50 | data | `do itrn = 1, wallo(iwallo)%trn_obs > if (time%end_mo == 1) then > if (pco%water_allo%m == "y") then` | `time%day`, `time%mo`, `time%day_mo`, `time%yrc`, `itrn`, `wallo(iwallo)%trn(itrn)%trn_typ`, `wallo(iwallo)%trn(itrn)%num`, `wallo(iwallo)%trn(itrn)%num`, `wallo(iwallo)%trn(itrn)%num`, `(wallo(iwallo)%trn(itrn)%src(isrc)%typ, wallo(iwallo)%trn(itrn)%src(isrc)%num, wallom_out(iwallo)%trn(itrn)%src(isrc), isrc = 1, wallo(iwallo)%trn(itrn)%src_num)` |


- Procedure: `wallo_treat_output`
- Writer: `wallo_treat_output.f90`
- Match: source_output
- Resolved default filename(s): `water_allo_mon.txt`

| Line | Role | Condition | Fields written |
| --- | --- | --- | --- |
| 34 | data | `do itrt = 1, db_mx%wtp > if (time%end_mo == 1) then > if (pco%water_allo%m == "y") then` | `time%mo`, `time%day_mo`, `time%yrc`, `itrt`, `om_treat_name(itrt)`, `wal_tr_omm(itrt)` |


- Procedure: `wallo_trn_output`
- Writer: `wallo_trn_output.f90`
- Match: source_output
- Resolved default filename(s): `water_allo_mon.txt`

| Line | Role | Condition | Fields written |
| --- | --- | --- | --- |
| 50 | data | `do itrn = 1, wallo(iwallo)%trn_obs > if (time%end_mo == 1) then > if (pco%water_allo%m == "y") then` | `time%day`, `time%mo`, `time%day_mo`, `time%yrc`, `itrn`, `wallo(iwallo)%trn(itrn)%trn_typ`, `wallo(iwallo)%trn(itrn)%num`, `wallo(iwallo)%trn(itrn)%num`, `wallo(iwallo)%trn(itrn)%num`, `(wallo(iwallo)%trn(itrn)%src(isrc)%typ, wallo(iwallo)%trn(itrn)%src(isrc)%num, wal_omm(iwallo)%trn(itrn)%src(isrc)%hd, isrc = 1, wallo(iwallo)%trn(itrn)%src_num)` |


- Procedure: `wallo_use_output`
- Writer: `wallo_use_output.f90`
- Match: source_output
- Resolved default filename(s): `water_allo_mon.txt`

| Line | Role | Condition | Fields written |
| --- | --- | --- | --- |
| 34 | data | `do iuse = 1, db_mx%uses > if (time%end_mo == 1) then > if (pco%water_allo%m == "y") then` | `time%mo`, `time%day_mo`, `time%yrc`, `iuse`, `om_use_name(iuse)`, `wal_use_omm(iuse)` |


#### Candidate write structure

- Source expression(s): _none captured_

- Procedure: `header_water_allocation`
- Writer: `header_water_allocation.f90`
- Match: source_output
- Resolved default filename(s): `water_allo_mon.txt`

| Line | Role | Condition | Fields written |
| --- | --- | --- | --- |
| 28 | data | `if (pco%water_allo%m == "y") then` | `bsn%name`, `prog` |
| 29 | data | `if (pco%water_allo%m == "y") then` | `wallo_hdr` |
| 30 | data | `if (pco%water_allo%m == "y") then` | `wallo_hdr_units` |


- Procedure: `wallo_pou_output`
- Writer: `wallo_pou_output.f90`
- Match: source_output
- Resolved default filename(s): `water_allo_mon.txt`

| Line | Role | Condition | Fields written |
| --- | --- | --- | --- |
| 85 | data | `if (time%end_mo == 1) then > if (pco%water_allo%m == "y") then` | `time%day`, `time%mo`, `time%day_mo`, `time%yrc`, `"POU "`, `ipou`, `pou(ipou)%name`, `poum_met(ipou)%duty_tot%duty`, `poum_met(ipou)%duty_tot%deliv` |
| 88 | data | `if (time%end_mo == 1) then > if (pco%water_allo%m == "y") then > do ipod = 1, pou(ipou)%pods` | `"                 POD "`, `ipod`, `poum_met(ipou)%pod(ipod)%duty`, `poum_met(ipou)%pod(ipod)%deliv`, `poum_om(ipou)%pod(ipod)` |
| 92 | data | `if (time%end_mo == 1) then > if (pco%water_allo%m == "y") then > do ipor = 1, pou(ipou)%pors` | `"                 POR "`, `ipor`, `poum_om(ipou)%por(ipor)` |

### `water_allo_yr.csv`

- Review needed: yes
- Writer procedures changed: yes
- Write-block count changed: yes
- Write conditions changed: yes
- Write roles changed: yes
- Base flattened write order: `bsn%name`, `prog`, `wallo_hdr`, `wallo_hdr_units`, `time%day`, `time%mo`, `time%day_mo`, `time%yrc`, `itrn`, `wallo(iwallo)%trn(itrn)%trn_typ`, `wallo(iwallo)%trn(itrn)%num`, `wallo(iwallo)%trn(itrn)%num`, `wallo(iwallo)%trn(itrn)%num`, `(wallo(iwallo)%trn(itrn)%src(isrc)%typ, wallo(iwallo)%trn(itrn)%src(isrc)%num, walloy_out(iwallo)%trn(itrn)%src(isrc), isrc = 1, wallo(iwallo)%trn(itrn)%src_num)`, `time%mo`, `time%day_mo`, `time%yrc`, `itrt`, `om_treat_name(itrt)`, `wal_tr_omy(itrt)`, `time%day`, `time%mo`, `time%day_mo`, `time%yrc`, `itrn`, `wallo(iwallo)%trn(itrn)%trn_typ`, `wallo(iwallo)%trn(itrn)%num`, `wallo(iwallo)%trn(itrn)%num`, `wallo(iwallo)%trn(itrn)%num`, `(wallo(iwallo)%trn(itrn)%src(isrc)%typ, wallo(iwallo)%trn(itrn)%src(isrc)%num, wal_omy(iwallo)%trn(itrn)%src(isrc)%hd, isrc = 1, wallo(iwallo)%trn(itrn)%src_num)`, `time%mo`, `time%day_mo`, `time%yrc`, `iuse`, `om_use_name(iuse)`, `wal_use_omy(iuse)`
- Candidate flattened write order: `bsn%name`, `prog`, `wallo_hdr`, `wallo_hdr_units`, `time%day`, `time%mo`, `time%day_mo`, `"POU "`, `ipou`, `time%yrc`, `ipou`, `pou(ipou)%name`, `pouy_met(ipou)%duty_tot%duty`, `pouy_met(ipou)%duty_tot%deliv`, `"     POD "`, `ipod`, `pouy_met(ipou)%pod(ipod)%duty`, `pouy_met(ipou)%pod(ipod)%deliv`, `pouy_om(ipou)%pod(ipod)`, `"     POR "`, `ipor`, `pouy_om(ipou)%por(ipor)`

#### Write-order edits

- `insert` at base index 7 / candidate index 7: removed _no fields captured_; added `"POU "`, `ipou`
- `replace` at base index 8 / candidate index 10: removed `itrn`, `wallo(iwallo)%trn(itrn)%trn_typ`, `wallo(iwallo)%trn(itrn)%num`, `wallo(iwallo)%trn(itrn)%num`, `wallo(iwallo)%trn(itrn)%num`, `(wallo(iwallo)%trn(itrn)%src(isrc)%typ, wallo(iwallo)%trn(itrn)%src(isrc)%num, walloy_out(iwallo)%trn(itrn)%src(isrc), isrc = 1, wallo(iwallo)%trn(itrn)%src_num)`, `time%mo`, `time%day_mo`, `time%yrc`, `itrt`, `om_treat_name(itrt)`, `wal_tr_omy(itrt)`, `time%day`, `time%mo`, `time%day_mo`, `time%yrc`, `itrn`, `wallo(iwallo)%trn(itrn)%trn_typ`, `wallo(iwallo)%trn(itrn)%num`, `wallo(iwallo)%trn(itrn)%num`, `wallo(iwallo)%trn(itrn)%num`, `(wallo(iwallo)%trn(itrn)%src(isrc)%typ, wallo(iwallo)%trn(itrn)%src(isrc)%num, wal_omy(iwallo)%trn(itrn)%src(isrc)%hd, isrc = 1, wallo(iwallo)%trn(itrn)%src_num)`, `time%mo`, `time%day_mo`, `time%yrc`, `iuse`, `om_use_name(iuse)`, `wal_use_omy(iuse)`; added `ipou`, `pou(ipou)%name`, `pouy_met(ipou)%duty_tot%duty`, `pouy_met(ipou)%duty_tot%deliv`, `"     POD "`, `ipod`, `pouy_met(ipou)%pod(ipod)%duty`, `pouy_met(ipou)%pod(ipod)%deliv`, `pouy_om(ipou)%pod(ipod)`, `"     POR "`, `ipor`, `pouy_om(ipou)%por(ipor)`

#### Base write structure

- Source expression(s): _none captured_

- Procedure: `header_water_allocation`
- Writer: `header_water_allocation.f90`
- Match: source_output
- Resolved default filename(s): `water_allo_yr.csv`

| Line | Role | Condition | Fields written |
| --- | --- | --- | --- |
| 54 | data | `if (db_mx%wallo_db > 0) then > if (pco%water_allo%y == "y") then > if (pco%csvout == "y") then` | `bsn%name`, `prog` |
| 55 | data | `if (db_mx%wallo_db > 0) then > if (pco%water_allo%y == "y") then > if (pco%csvout == "y") then` | `wallo_hdr` |
| 56 | data | `if (db_mx%wallo_db > 0) then > if (pco%water_allo%y == "y") then > if (pco%csvout == "y") then` | `wallo_hdr_units` |


- Procedure: `wallo_allo_output`
- Writer: `wallo_allo_output.f90`
- Match: source_output
- Resolved default filename(s): `water_allo_yr.csv`

| Line | Role | Condition | Fields written |
| --- | --- | --- | --- |
| 84 | data | `do itrn = 1, wallo(iwallo)%trn_obs > if (time%end_yr == 1) then > if (pco%water_allo%y == "y") then > if (pco%csvout == "y") then` | `time%day`, `time%mo`, `time%day_mo`, `time%yrc`, `itrn`, `wallo(iwallo)%trn(itrn)%trn_typ`, `wallo(iwallo)%trn(itrn)%num`, `wallo(iwallo)%trn(itrn)%num`, `wallo(iwallo)%trn(itrn)%num`, `(wallo(iwallo)%trn(itrn)%src(isrc)%typ, wallo(iwallo)%trn(itrn)%src(isrc)%num, walloy_out(iwallo)%trn(itrn)%src(isrc), isrc = 1, wallo(iwallo)%trn(itrn)%src_num)` |


- Procedure: `wallo_treat_output`
- Writer: `wallo_treat_output.f90`
- Match: source_output
- Resolved default filename(s): `water_allo_yr.csv`

| Line | Role | Condition | Fields written |
| --- | --- | --- | --- |
| 54 | data | `do itrt = 1, db_mx%wtp > if (time%end_yr == 1) then > if (pco%water_allo%y == "y") then > if (pco%csvout == "y") then` | `time%mo`, `time%day_mo`, `time%yrc`, `itrt`, `om_treat_name(itrt)`, `wal_tr_omy(itrt)` |


- Procedure: `wallo_trn_output`
- Writer: `wallo_trn_output.f90`
- Match: source_output
- Resolved default filename(s): `water_allo_yr.csv`

| Line | Role | Condition | Fields written |
| --- | --- | --- | --- |
| 84 | data | `do itrn = 1, wallo(iwallo)%trn_obs > if (time%end_yr == 1) then > if (pco%water_allo%y == "y") then > if (pco%csvout == "y") then` | `time%day`, `time%mo`, `time%day_mo`, `time%yrc`, `itrn`, `wallo(iwallo)%trn(itrn)%trn_typ`, `wallo(iwallo)%trn(itrn)%num`, `wallo(iwallo)%trn(itrn)%num`, `wallo(iwallo)%trn(itrn)%num`, `(wallo(iwallo)%trn(itrn)%src(isrc)%typ, wallo(iwallo)%trn(itrn)%src(isrc)%num, wal_omy(iwallo)%trn(itrn)%src(isrc)%hd, isrc = 1, wallo(iwallo)%trn(itrn)%src_num)` |


- Procedure: `wallo_use_output`
- Writer: `wallo_use_output.f90`
- Match: source_output
- Resolved default filename(s): `water_allo_yr.csv`

| Line | Role | Condition | Fields written |
| --- | --- | --- | --- |
| 54 | data | `do iuse = 1, db_mx%uses > if (time%end_yr == 1) then > if (pco%water_allo%y == "y") then > if (pco%csvout == "y") then` | `time%mo`, `time%day_mo`, `time%yrc`, `iuse`, `om_use_name(iuse)`, `wal_use_omy(iuse)` |


#### Candidate write structure

- Source expression(s): _none captured_

- Procedure: `header_water_allocation`
- Writer: `header_water_allocation.f90`
- Match: source_output
- Resolved default filename(s): `water_allo_yr.csv`

| Line | Role | Condition | Fields written |
| --- | --- | --- | --- |
| 49 | data | `if (pco%water_allo%y == "y") then > if (pco%csvout == "y") then` | `bsn%name`, `prog` |
| 50 | data | `if (pco%water_allo%y == "y") then > if (pco%csvout == "y") then` | `wallo_hdr` |
| 51 | data | `if (pco%water_allo%y == "y") then > if (pco%csvout == "y") then` | `wallo_hdr_units` |


- Procedure: `wallo_pou_output`
- Writer: `wallo_pou_output.f90`
- Match: source_output
- Resolved default filename(s): `water_allo_yr.csv`

| Line | Role | Condition | Fields written |
| --- | --- | --- | --- |
| 154 | data | `if (time%end_yr == 1) then > if (pco%water_allo%y == "y") then > if (pco%csvout == "y") then` | `time%day`, `time%mo`, `time%day_mo`, `"POU "`, `ipou`, `time%yrc`, `ipou`, `pou(ipou)%name`, `pouy_met(ipou)%duty_tot%duty`, `pouy_met(ipou)%duty_tot%deliv` |
| 158 | data | `if (time%end_yr == 1) then > if (pco%water_allo%y == "y") then > if (pco%csvout == "y") then > do ipod = 1, pou(ipou)%pods` | `"     POD "`, `ipod`, `pouy_met(ipou)%pod(ipod)%duty`, `pouy_met(ipou)%pod(ipod)%deliv`, `pouy_om(ipou)%pod(ipod)` |
| 162 | data | `if (time%end_yr == 1) then > if (pco%water_allo%y == "y") then > if (pco%csvout == "y") then > do ipor = 1, pou(ipou)%pors` | `"     POR "`, `ipor`, `pouy_om(ipou)%por(ipor)` |

### `water_allo_yr.txt`

- Review needed: yes
- Writer procedures changed: yes
- Write-block count changed: yes
- Write conditions changed: yes
- Write roles changed: yes
- Base flattened write order: `bsn%name`, `prog`, `wallo_hdr`, `wallo_hdr_units`, `time%day`, `time%mo`, `time%day_mo`, `time%yrc`, `itrn`, `wallo(iwallo)%trn(itrn)%trn_typ`, `wallo(iwallo)%trn(itrn)%num`, `wallo(iwallo)%trn(itrn)%num`, `wallo(iwallo)%trn(itrn)%num`, `(wallo(iwallo)%trn(itrn)%src(isrc)%typ, wallo(iwallo)%trn(itrn)%src(isrc)%num, walloy_out(iwallo)%trn(itrn)%src(isrc), isrc = 1, wallo(iwallo)%trn(itrn)%src_num)`, `time%mo`, `time%day_mo`, `time%yrc`, `itrt`, `om_treat_name(itrt)`, `wal_tr_omy(itrt)`, `time%day`, `time%mo`, `time%day_mo`, `time%yrc`, `itrn`, `wallo(iwallo)%trn(itrn)%trn_typ`, `wallo(iwallo)%trn(itrn)%num`, `wallo(iwallo)%trn(itrn)%num`, `wallo(iwallo)%trn(itrn)%num`, `(wallo(iwallo)%trn(itrn)%src(isrc)%typ, wallo(iwallo)%trn(itrn)%src(isrc)%num, wal_omy(iwallo)%trn(itrn)%src(isrc)%hd, isrc = 1, wallo(iwallo)%trn(itrn)%src_num)`, `time%mo`, `time%day_mo`, `time%yrc`, `iuse`, `om_use_name(iuse)`, `wal_use_omy(iuse)`
- Candidate flattened write order: `bsn%name`, `prog`, `wallo_hdr`, `wallo_hdr_units`, `time%day`, `time%mo`, `time%day_mo`, `time%yrc`, `"POU "`, `ipou`, `pou(ipou)%name`, `pouy_met(ipou)%duty_tot%duty`, `pouy_met(ipou)%duty_tot%deliv`, `"                 POD "`, `ipod`, `pouy_met(ipou)%pod(ipod)%duty`, `pouy_met(ipou)%pod(ipod)%deliv`, `pouy_om(ipou)%pod(ipod)`, `"                 POR "`, `ipor`, `pouy_om(ipou)%por(ipor)`

#### Write-order edits

- `replace` at base index 8 / candidate index 8: removed `itrn`, `wallo(iwallo)%trn(itrn)%trn_typ`, `wallo(iwallo)%trn(itrn)%num`, `wallo(iwallo)%trn(itrn)%num`, `wallo(iwallo)%trn(itrn)%num`, `(wallo(iwallo)%trn(itrn)%src(isrc)%typ, wallo(iwallo)%trn(itrn)%src(isrc)%num, walloy_out(iwallo)%trn(itrn)%src(isrc), isrc = 1, wallo(iwallo)%trn(itrn)%src_num)`, `time%mo`, `time%day_mo`, `time%yrc`, `itrt`, `om_treat_name(itrt)`, `wal_tr_omy(itrt)`, `time%day`, `time%mo`, `time%day_mo`, `time%yrc`, `itrn`, `wallo(iwallo)%trn(itrn)%trn_typ`, `wallo(iwallo)%trn(itrn)%num`, `wallo(iwallo)%trn(itrn)%num`, `wallo(iwallo)%trn(itrn)%num`, `(wallo(iwallo)%trn(itrn)%src(isrc)%typ, wallo(iwallo)%trn(itrn)%src(isrc)%num, wal_omy(iwallo)%trn(itrn)%src(isrc)%hd, isrc = 1, wallo(iwallo)%trn(itrn)%src_num)`, `time%mo`, `time%day_mo`, `time%yrc`, `iuse`, `om_use_name(iuse)`, `wal_use_omy(iuse)`; added `"POU "`, `ipou`, `pou(ipou)%name`, `pouy_met(ipou)%duty_tot%duty`, `pouy_met(ipou)%duty_tot%deliv`, `"                 POD "`, `ipod`, `pouy_met(ipou)%pod(ipod)%duty`, `pouy_met(ipou)%pod(ipod)%deliv`, `pouy_om(ipou)%pod(ipod)`, `"                 POR "`, `ipor`, `pouy_om(ipou)%por(ipor)`

#### Base write structure

- Source expression(s): _none captured_

- Procedure: `header_water_allocation`
- Writer: `header_water_allocation.f90`
- Match: source_output
- Resolved default filename(s): `water_allo_yr.txt`

| Line | Role | Condition | Fields written |
| --- | --- | --- | --- |
| 48 | data | `if (db_mx%wallo_db > 0) then > if (pco%water_allo%y == "y") then` | `bsn%name`, `prog` |
| 49 | data | `if (db_mx%wallo_db > 0) then > if (pco%water_allo%y == "y") then` | `wallo_hdr` |
| 50 | data | `if (db_mx%wallo_db > 0) then > if (pco%water_allo%y == "y") then` | `wallo_hdr_units` |


- Procedure: `wallo_allo_output`
- Writer: `wallo_allo_output.f90`
- Match: source_output
- Resolved default filename(s): `water_allo_yr.txt`

| Line | Role | Condition | Fields written |
| --- | --- | --- | --- |
| 78 | data | `do itrn = 1, wallo(iwallo)%trn_obs > if (time%end_yr == 1) then > if (pco%water_allo%y == "y") then` | `time%day`, `time%mo`, `time%day_mo`, `time%yrc`, `itrn`, `wallo(iwallo)%trn(itrn)%trn_typ`, `wallo(iwallo)%trn(itrn)%num`, `wallo(iwallo)%trn(itrn)%num`, `wallo(iwallo)%trn(itrn)%num`, `(wallo(iwallo)%trn(itrn)%src(isrc)%typ, wallo(iwallo)%trn(itrn)%src(isrc)%num, walloy_out(iwallo)%trn(itrn)%src(isrc), isrc = 1, wallo(iwallo)%trn(itrn)%src_num)` |


- Procedure: `wallo_treat_output`
- Writer: `wallo_treat_output.f90`
- Match: source_output
- Resolved default filename(s): `water_allo_yr.txt`

| Line | Role | Condition | Fields written |
| --- | --- | --- | --- |
| 51 | data | `do itrt = 1, db_mx%wtp > if (time%end_yr == 1) then > if (pco%water_allo%y == "y") then` | `time%mo`, `time%day_mo`, `time%yrc`, `itrt`, `om_treat_name(itrt)`, `wal_tr_omy(itrt)` |


- Procedure: `wallo_trn_output`
- Writer: `wallo_trn_output.f90`
- Match: source_output
- Resolved default filename(s): `water_allo_yr.txt`

| Line | Role | Condition | Fields written |
| --- | --- | --- | --- |
| 78 | data | `do itrn = 1, wallo(iwallo)%trn_obs > if (time%end_yr == 1) then > if (pco%water_allo%y == "y") then` | `time%day`, `time%mo`, `time%day_mo`, `time%yrc`, `itrn`, `wallo(iwallo)%trn(itrn)%trn_typ`, `wallo(iwallo)%trn(itrn)%num`, `wallo(iwallo)%trn(itrn)%num`, `wallo(iwallo)%trn(itrn)%num`, `(wallo(iwallo)%trn(itrn)%src(isrc)%typ, wallo(iwallo)%trn(itrn)%src(isrc)%num, wal_omy(iwallo)%trn(itrn)%src(isrc)%hd, isrc = 1, wallo(iwallo)%trn(itrn)%src_num)` |


- Procedure: `wallo_use_output`
- Writer: `wallo_use_output.f90`
- Match: source_output
- Resolved default filename(s): `water_allo_yr.txt`

| Line | Role | Condition | Fields written |
| --- | --- | --- | --- |
| 51 | data | `do iuse = 1, db_mx%uses > if (time%end_yr == 1) then > if (pco%water_allo%y == "y") then` | `time%mo`, `time%day_mo`, `time%yrc`, `iuse`, `om_use_name(iuse)`, `wal_use_omy(iuse)` |


#### Candidate write structure

- Source expression(s): _none captured_

- Procedure: `header_water_allocation`
- Writer: `header_water_allocation.f90`
- Match: source_output
- Resolved default filename(s): `water_allo_yr.txt`

| Line | Role | Condition | Fields written |
| --- | --- | --- | --- |
| 43 | data | `if (pco%water_allo%y == "y") then` | `bsn%name`, `prog` |
| 44 | data | `if (pco%water_allo%y == "y") then` | `wallo_hdr` |
| 45 | data | `if (pco%water_allo%y == "y") then` | `wallo_hdr_units` |


- Procedure: `wallo_pou_output`
- Writer: `wallo_pou_output.f90`
- Match: source_output
- Resolved default filename(s): `water_allo_yr.txt`

| Line | Role | Condition | Fields written |
| --- | --- | --- | --- |
| 143 | data | `if (time%end_yr == 1) then > if (pco%water_allo%y == "y") then` | `time%day`, `time%mo`, `time%day_mo`, `time%yrc`, `"POU "`, `ipou`, `pou(ipou)%name`, `pouy_met(ipou)%duty_tot%duty`, `pouy_met(ipou)%duty_tot%deliv` |
| 146 | data | `if (time%end_yr == 1) then > if (pco%water_allo%y == "y") then > do ipod = 1, pou(ipou)%pods` | `"                 POD "`, `ipod`, `pouy_met(ipou)%pod(ipod)%duty`, `pouy_met(ipou)%pod(ipod)%deliv`, `pouy_om(ipou)%pod(ipod)` |
| 150 | data | `if (time%end_yr == 1) then > if (pco%water_allo%y == "y") then > do ipor = 1, pou(ipou)%pors` | `"                 POR "`, `ipor`, `pouy_om(ipou)%por(ipor)` |


## Possible renames or replacements

- `recall_db(irec)%name` -> `recall(irec)%filename`: same reader procedure: swift_output; same file extension; similar read-field order
