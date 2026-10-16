# SWAT+ Output Contract Changes

Source-level output change report: which files SWAT+ opens for writing, and the fields each write statement emits. Filenames are resolved from the same defaults used for inputs; a resolved default can still be overridden by runtime configuration. Outputs carry no schema certification, so entries here are not schema-reviewed.

## Summary

- Added output files: **4**
- Removed output files: **1**
- Changed write contracts: **10**
- Possible renames or replacements: **0**
- Candidate open/write blocks with unresolved filenames: **64**
- Newly unresolved units in the candidate: **0**

## Coverage

SWAT+ opens most output units in a header or initialisation routine and writes to them from other files. Unit-to-filename binding is per-file, so a unit opened elsewhere cannot be named here and is counted as unresolved rather than reported under a `unit_NNN` pseudo-filename. This report therefore covers the writes below and not the rest; widening it needs project-wide unit binding in the parser.

- Output files resolved to a filename: **671**
- Write statements covered: **4499**
- Units whose filename is unresolved: **64**
- Write statements not covered: **143**

## Added outputs

### `SWIFT/object_prt.swf`

- Source expression(s): `"SWIFT/object_prt.swf"`

- Procedure: `swift_output`
- Writer: `swift_output.f90`
- Match: source_output
- Resolved default filename(s): `SWIFT/object_prt.swf`
- Source filename expression(s): `"SWIFT/object_prt.swf"`

| Line | Role | Condition | Fields written |
| --- | --- | --- | --- |
| 266 | data | `do iobj_out = 1, mobj_out` | `" AVE ANNUAL OBJECT OUTPUT FILE  "`, `ob_out(iobj_out)%filename` |
| 270 | data | `do iobj_out = 1, mobj_out` | `"     1    1    1     1    "`, `ob_out(iobj_out)%name`, `ob_out(iobj_out)%name`, `ob(iob)%hd_aa(ihyd)%flo`, `ob(iob)%hd_aa(ihyd)%sed`, `ob(iob)%hd_aa(ihyd)%orgn`, `ob(iob)%hd_aa(ihyd)%sedp`, `ob(iob)%hd_aa(ihyd)%no3`, `ob(iob)%hd_aa(ihyd)%solp`, `ob(iob)%hd_aa(ihyd)%nh3`, `ob(iob)%hd_aa(ihyd)%no2` |

### `SWIFT/recall.swf`

- Source expression(s): `"SWIFT/recall.swf"`

- Procedure: `swift_output`
- Writer: `swift_output.f90`
- Match: source_output
- Resolved default filename(s): `SWIFT/recall.swf`
- Source filename expression(s): `"SWIFT/recall.swf"`

| Line | Role | Condition | Fields written |
| --- | --- | --- | --- |
| 245 | data | `None` | `"         ID            NAME              REC_TYP         FILENAME"` |
| 247 | data | `do irec = 1, db_mx%recall_max` | `irec`, `recall(irec)%name`, `recall(irec)%typ`, `recall(irec)%name` |

### `destination`

- Source expression(s): `destination`

- Procedure: `copy_file`
- Writer: `copy_file.f90`
- Match: source_output
- Resolved default filename(s): `destination`
- Source filename expression(s): `destination`

| Line | Role | Condition | Fields written |
| --- | --- | --- | --- |
| 23 | data | `do` | `trim(line)` |

### `recall(irec)%name`

- Source expression(s): `"SWIFT/" // trim(adjustl(recall(irec)%name))`

- Procedure: `swift_output`
- Writer: `swift_output.f90`
- Match: source_output
- Resolved default filename(s): `recall(irec)%name`
- Source filename expression(s): `"SWIFT/" // trim(adjustl(recall(irec)%name))`

| Line | Role | Condition | Fields written |
| --- | --- | --- | --- |
| 251 | data | `do irec = 1, db_mx%recall_max` | `" AVE ANNUAL RECALL FILE  "`, `recall(irec)%filename` |
| 252 | data | `do irec = 1, db_mx%recall_max` | `"     1    1    1     1    type    "`, `recall(irec)%filename`, `rec_a(irec)%flo`, `rec_a(irec)%sed`, `rec_a(irec)%orgn`, `rec_a(irec)%sedp`, `rec_a(irec)%no3`, `rec_a(irec)%solp`, `rec_a(irec)%nh3`, `rec_a(irec)%no2` |


## Removed outputs

### `reservoir_sed.txt`

- Source expression(s): `"reservoir_sed.txt"`

- Procedure: `res_control`
- Writer: `res_control.f90`
- Match: source_output
- Resolved default filename(s): `reservoir_sed.txt`
- Source filename expression(s): `"reservoir_sed.txt"`

| Line | Role | Condition | Fields written |
| --- | --- | --- | --- |
| 185 | data | `if (jres == 1) then` | `time%day`, `time%yrc`, `jres`, `res(jres)%flo`, `ht1%flo`, `ht2%flo`, `res(jres)%sed`, `ht1%sed`, `ht2%sed` |


## Changed output write contracts

### `SWIFT/aqu_dr.swf`

- Review needed: yes
- Writer procedures changed: no
- Write-block count changed: no
- Write conditions changed: no
- Write roles changed: no
- Base flattened write order: `bsn%name`, `sp_ob%aqu`, `" OUTPUT NAMES - NUBZ"`, `" OUTPUT UNITS - NUBZ"`, `iaqu`, `ht5%flo`, `ht5%sed`, `ht5%orgn`, `ht5%sedp`, `ht5%no3`, `ht5%solp`, `ht5%nh3`, `ht5%no2`
- Candidate flattened write order: `bsn%name`, `sp_ob%aqu`, `"iaqu "`, `hru_swift_hdr%dr`, `"--- "`, `hru_swift_hdr%dr_unit`, `iaqu`, `ht5%flo`, `ht5%sed`, `ht5%orgn`, `ht5%sedp`, `ht5%no3`, `ht5%solp`, `ht5%nh3`, `ht5%no2`

#### Write-order edits

- `replace` at base index 2 / candidate index 2: removed `" OUTPUT NAMES - NUBZ"`, `" OUTPUT UNITS - NUBZ"`; added `"iaqu "`, `hru_swift_hdr%dr`, `"--- "`, `hru_swift_hdr%dr_unit`

#### Base write structure

- Source expression(s): `"SWIFT/aqu_dr.swf"`

- Procedure: `swift_output`
- Writer: `swift_output.f90`
- Match: source_output
- Resolved default filename(s): `SWIFT/aqu_dr.swf`
- Source filename expression(s): `"SWIFT/aqu_dr.swf"`

| Line | Role | Condition | Fields written |
| --- | --- | --- | --- |
| 162 | data | `None` | `bsn%name` |
| 163 | data | `None` | `sp_ob%aqu` |
| 164 | data | `None` | `" OUTPUT NAMES - NUBZ"` |
| 165 | data | `None` | `" OUTPUT UNITS - NUBZ"` |
| 169 | data | `do iaqu = 1, sp_ob%aqu` | `iaqu`, `ht5%flo`, `ht5%sed`, `ht5%orgn`, `ht5%sedp`, `ht5%no3`, `ht5%solp`, `ht5%nh3`, `ht5%no2` |


#### Candidate write structure

- Source expression(s): `"SWIFT/aqu_dr.swf"`

- Procedure: `swift_output`
- Writer: `swift_output.f90`
- Match: source_output
- Resolved default filename(s): `SWIFT/aqu_dr.swf`
- Source filename expression(s): `"SWIFT/aqu_dr.swf"`

| Line | Role | Condition | Fields written |
| --- | --- | --- | --- |
| 205 | data | `None` | `bsn%name` |
| 206 | data | `None` | `sp_ob%aqu` |
| 207 | data | `None` | `"iaqu "`, `hru_swift_hdr%dr` |
| 208 | data | `None` | `"--- "`, `hru_swift_hdr%dr_unit` |
| 212 | data | `do iaqu = 1, sp_ob%aqu` | `iaqu`, `ht5%flo`, `ht5%sed`, `ht5%orgn`, `ht5%sedp`, `ht5%no3`, `ht5%solp`, `ht5%nh3`, `ht5%no2` |

### `SWIFT/chan_dat.swf`

- Review needed: yes
- Writer procedures changed: no
- Write-block count changed: no
- Write conditions changed: no
- Write roles changed: no
- Base flattened write order: `bsn%name`, `" OUTPUT NAMES - NUBZ"`, `icha`, `sd_chd(idb)`
- Candidate flattened write order: `bsn%name`, `sd_chd_hdr`, `icha`, `sd_chd(idb)`

#### Write-order edits

- `replace` at base index 1 / candidate index 1: removed `" OUTPUT NAMES - NUBZ"`; added `sd_chd_hdr`

#### Base write structure

- Source expression(s): `"SWIFT/chan_dat.swf"`

- Procedure: `swift_output`
- Writer: `swift_output.f90`
- Match: source_output
- Resolved default filename(s): `SWIFT/chan_dat.swf`
- Source filename expression(s): `"SWIFT/chan_dat.swf"`

| Line | Role | Condition | Fields written |
| --- | --- | --- | --- |
| 131 | data | `None` | `bsn%name` |
| 132 | data | `None` | `" OUTPUT NAMES - NUBZ"` |
| 137 | data | `do icha = 1, sp_ob%chandeg` | `icha`, `sd_chd(idb)` |


#### Candidate write structure

- Source expression(s): `"SWIFT/chan_dat.swf"`

- Procedure: `swift_output`
- Writer: `swift_output.f90`
- Match: source_output
- Resolved default filename(s): `SWIFT/chan_dat.swf`
- Source filename expression(s): `"SWIFT/chan_dat.swf"`

| Line | Role | Condition | Fields written |
| --- | --- | --- | --- |
| 173 | data | `None` | `bsn%name` |
| 174 | data | `None` | `sd_chd_hdr` |
| 179 | data | `do icha = 1, sp_ob%chandeg` | `icha`, `sd_chd(idb)` |

### `SWIFT/chan_dr.swf`

- Review needed: yes
- Writer procedures changed: no
- Write-block count changed: no
- Write conditions changed: no
- Write roles changed: no
- Base flattened write order: `bsn%name`, `sp_ob%chandeg`, `" OUTPUT NAMES - NUBZ"`, `" OUTPUT UNITS - NUBZ"`, `icha`, `sd_chd(idb)%name`, `ht5%flo`, `ht5%sed`, `ht5%orgn`, `ht5%sedp`, `ht5%no3`, `ht5%solp`, `ht5%nh3`, `ht5%no2`
- Candidate flattened write order: `bsn%name`, `sp_ob%chandeg`, `"icha "`, `"name "`, `hru_swift_hdr%dr`, `"--- "`, `"---- "`, `hru_swift_hdr%dr_unit`, `icha`, `sd_chd(idb)%name`, `ht5%flo`, `ht5%sed`, `ht5%orgn`, `ht5%sedp`, `ht5%no3`, `ht5%solp`, `ht5%nh3`, `ht5%no2`

#### Write-order edits

- `replace` at base index 2 / candidate index 2: removed `" OUTPUT NAMES - NUBZ"`, `" OUTPUT UNITS - NUBZ"`; added `"icha "`, `"name "`, `hru_swift_hdr%dr`, `"--- "`, `"---- "`, `hru_swift_hdr%dr_unit`

#### Base write structure

- Source expression(s): `"SWIFT/chan_dr.swf"`

- Procedure: `swift_output`
- Writer: `swift_output.f90`
- Match: source_output
- Resolved default filename(s): `SWIFT/chan_dr.swf`
- Source filename expression(s): `"SWIFT/chan_dr.swf"`

| Line | Role | Condition | Fields written |
| --- | --- | --- | --- |
| 143 | data | `None` | `bsn%name` |
| 144 | data | `None` | `sp_ob%chandeg` |
| 145 | data | `None` | `" OUTPUT NAMES - NUBZ"` |
| 146 | data | `None` | `" OUTPUT UNITS - NUBZ"` |
| 156 | data | `do icha = 1, sp_ob%chandeg` | `icha`, `sd_chd(idb)%name`, `ht5%flo`, `ht5%sed`, `ht5%orgn`, `ht5%sedp`, `ht5%no3`, `ht5%solp`, `ht5%nh3`, `ht5%no2` |


#### Candidate write structure

- Source expression(s): `"SWIFT/chan_dr.swf"`

- Procedure: `swift_output`
- Writer: `swift_output.f90`
- Match: source_output
- Resolved default filename(s): `SWIFT/chan_dr.swf`
- Source filename expression(s): `"SWIFT/chan_dr.swf"`

| Line | Role | Condition | Fields written |
| --- | --- | --- | --- |
| 185 | data | `None` | `bsn%name` |
| 186 | data | `None` | `sp_ob%chandeg` |
| 187 | data | `None` | `"icha "`, `"name "`, `hru_swift_hdr%dr` |
| 188 | data | `None` | `"--- "`, `"---- "`, `hru_swift_hdr%dr_unit` |
| 198 | data | `do icha = 1, sp_ob%chandeg` | `icha`, `sd_chd(idb)%name`, `ht5%flo`, `ht5%sed`, `ht5%orgn`, `ht5%sedp`, `ht5%no3`, `ht5%solp`, `ht5%nh3`, `ht5%no2` |

### `SWIFT/file_cio.swf`

- Review needed: yes
- Writer procedures changed: no
- Write-block count changed: no
- Write conditions changed: no
- Write roles changed: no
- Base flattened write order: `"SWIFT file.cio"`, `"BASIN         "`, `in_sim%object_cnt`, `in_sim%object_prt`, `in_sim%cs_db`, `"CLIMATE       "`, `"  precip.swf"`, `"CONNECT       "`, `in_con%hru_con`, `in_con%ru_con`, `in_con%aqu_con`, `in_con%chandeg_con`, `in_con%res_con`, `in_con%rec_con`, `in_con%out_con`, `"CHANNEL       "`, `"  chan_dat.swf"`, `"  chan_dr.swf"`, `"RESERVOIR     "`, `"  res_dat.swf"`, `"  res_dr.swf"`, `"ROUT_UNIT     "`, `in_ru%ru_def`, `in_ru%ru_ele`, `"HRU           "`, `"  hru_dat.swf"`, `"  hru_exco.swf"`, `"  hru_wet.swf"`, `"  hru_bmp.swf"`, `"  hru_dr.swf"`, `"RECALL        "`, `in_rec%recall_rec`, `"AQUIFER       "`, `"  aqu_dr.swf"`, `"LS_UNIT       "`, `in_regs%def_lsu`, `in_regs%ele_lsu`
- Candidate flattened write order: `"SWIFT file.cio"`, `"BASIN         "`, `in_sim%object_cnt`, `in_sim%object_prt`, `in_sim%cs_db`, `"CLIMATE       "`, `"  precip.swf"`, `"CONNECT       "`, `in_con%hru_con`, `in_con%ru_con`, `in_con%aqu_con`, `in_con%chandeg_con`, `in_con%res_con`, `in_con%rec_con`, `in_con%out_con`, `"CHANNEL       "`, `"  chan_dat.swf"`, `"  chan_dr.swf"`, `"RESERVOIR     "`, `"  res_dat.swf"`, `"  res_dr.swf"`, `"ROUT_UNIT     "`, `in_ru%ru_def`, `in_ru%ru_ele`, `"HRU           "`, `"  hru_dat.swf"`, `"  hru_exco.swf"`, `"  hru_wet.swf"`, `"  hru_bmp.swf"`, `"  hru_dr.swf"`, `"RECALL        "`, `"  recall.swf"`, `"AQUIFER       "`, `"  aqu_dr.swf"`, `"LS_UNIT       "`, `in_regs%def_lsu`, `in_regs%ele_lsu`

#### Write-order edits

- `replace` at base index 31 / candidate index 31: removed `in_rec%recall_rec`; added `"  recall.swf"`

#### Base write structure

- Source expression(s): `"SWIFT/file_cio.swf"`

- Procedure: `swift_output`
- Writer: `swift_output.f90`
- Match: source_output
- Resolved default filename(s): `SWIFT/file_cio.swf`
- Source filename expression(s): `"SWIFT/file_cio.swf"`

| Line | Role | Condition | Fields written |
| --- | --- | --- | --- |
| 42 | data | `None` | `"SWIFT file.cio"` |
| 43 | data | `None` | `"BASIN         "`, `in_sim%object_cnt`, `in_sim%object_prt`, `in_sim%cs_db` |
| 44 | data | `None` | `"CLIMATE       "`, `"  precip.swf"` |
| 45 | data | `None` | `"CONNECT       "`, `in_con%hru_con`, `in_con%ru_con`, `in_con%aqu_con`, `in_con%chandeg_con`, `in_con%res_con`, `in_con%rec_con`, `in_con%out_con` |
| 47 | data | `None` | `"CHANNEL       "`, `"  chan_dat.swf"`, `"  chan_dr.swf"` |
| 48 | data | `None` | `"RESERVOIR     "`, `"  res_dat.swf"`, `"  res_dr.swf"` |
| 49 | data | `None` | `"ROUT_UNIT     "`, `in_ru%ru_def`, `in_ru%ru_ele` |
| 50 | data | `None` | `"HRU           "`, `"  hru_dat.swf"`, `"  hru_exco.swf"`, `"  hru_wet.swf"`, `"  hru_bmp.swf"`, `"  hru_dr.swf"` |
| 52 | data | `None` | `"RECALL        "`, `in_rec%recall_rec` |
| 53 | data | `None` | `"AQUIFER       "`, `"  aqu_dr.swf"` |
| 54 | data | `None` | `"LS_UNIT       "`, `in_regs%def_lsu`, `in_regs%ele_lsu` |


#### Candidate write structure

- Source expression(s): `"SWIFT/file_cio.swf"`

- Procedure: `swift_output`
- Writer: `swift_output.f90`
- Match: source_output
- Resolved default filename(s): `SWIFT/file_cio.swf`
- Source filename expression(s): `"SWIFT/file_cio.swf"`

| Line | Role | Condition | Fields written |
| --- | --- | --- | --- |
| 61 | data | `None` | `"SWIFT file.cio"` |
| 62 | data | `None` | `"BASIN         "`, `in_sim%object_cnt`, `in_sim%object_prt`, `in_sim%cs_db` |
| 63 | data | `None` | `"CLIMATE       "`, `"  precip.swf"` |
| 64 | data | `None` | `"CONNECT       "`, `in_con%hru_con`, `in_con%ru_con`, `in_con%aqu_con`, `in_con%chandeg_con`, `in_con%res_con`, `in_con%rec_con`, `in_con%out_con` |
| 66 | data | `None` | `"CHANNEL       "`, `"  chan_dat.swf"`, `"  chan_dr.swf"` |
| 67 | data | `None` | `"RESERVOIR     "`, `"  res_dat.swf"`, `"  res_dr.swf"` |
| 68 | data | `None` | `"ROUT_UNIT     "`, `in_ru%ru_def`, `in_ru%ru_ele` |
| 69 | data | `None` | `"HRU           "`, `"  hru_dat.swf"`, `"  hru_exco.swf"`, `"  hru_wet.swf"`, `"  hru_bmp.swf"`, `"  hru_dr.swf"` |
| 71 | data | `None` | `"RECALL        "`, `"  recall.swf"` |
| 72 | data | `None` | `"AQUIFER       "`, `"  aqu_dr.swf"` |
| 73 | data | `None` | `"LS_UNIT       "`, `in_regs%def_lsu`, `in_regs%ele_lsu` |

### `SWIFT/hru_dat.swf`

- Review needed: yes
- Writer procedures changed: no
- Write-block count changed: no
- Write conditions changed: no
- Write roles changed: no
- Base flattened write order: `bsn%name`, `sp_ob%hru`, `" OUTPUT NAMES - NUBZ"`, `" OUTPUT UNITS - NUBZ"`, `ihru`, `ob(ihru)%name`, `hru(ihru)%land_use_mgt_c`, `hru(ihru)%topo%slope`, `soil(ihru)%hydgrp`, `"  null"`, `"   null"`
- Candidate flattened write order: `bsn%name`, `sp_ob%hru`, `"iwst "`, `"name "`, `"land_use_mgt_c"`, `"slope"`, `"hydgrp"`, `"null"`, `"null"`, `"--- "`, `"---- "`, `"--------------"`, `"m/m"`, `"------"`, `"null"`, `"null"`, `ihru`, `ob(ihru)%name`, `hru(ihru)%land_use_mgt_c`, `hru(ihru)%topo%slope`, `soil(ihru)%hydgrp`, `"  null"`, `"   null"`

#### Write-order edits

- `replace` at base index 2 / candidate index 2: removed `" OUTPUT NAMES - NUBZ"`, `" OUTPUT UNITS - NUBZ"`; added `"iwst "`, `"name "`, `"land_use_mgt_c"`, `"slope"`, `"hydgrp"`, `"null"`, `"null"`, `"--- "`, `"---- "`, `"--------------"`, `"m/m"`, `"------"`, `"null"`, `"null"`

#### Base write structure

- Source expression(s): `"SWIFT/hru_dat.swf"`

- Procedure: `swift_output`
- Writer: `swift_output.f90`
- Match: source_output
- Resolved default filename(s): `SWIFT/hru_dat.swf`
- Source filename expression(s): `"SWIFT/hru_dat.swf"`

| Line | Role | Condition | Fields written |
| --- | --- | --- | --- |
| 72 | data | `None` | `bsn%name` |
| 73 | data | `None` | `sp_ob%hru` |
| 74 | data | `None` | `" OUTPUT NAMES - NUBZ"` |
| 75 | data | `None` | `" OUTPUT UNITS - NUBZ"` |
| 77 | data | `do ihru = 1, sp_ob%hru` | `ihru`, `ob(ihru)%name`, `hru(ihru)%land_use_mgt_c`, `hru(ihru)%topo%slope`, `soil(ihru)%hydgrp`, `"  null"`, `"   null"` |


#### Candidate write structure

- Source expression(s): `"SWIFT/hru_dat.swf"`

- Procedure: `swift_output`
- Writer: `swift_output.f90`
- Match: source_output
- Resolved default filename(s): `SWIFT/hru_dat.swf`
- Source filename expression(s): `"SWIFT/hru_dat.swf"`

| Line | Role | Condition | Fields written |
| --- | --- | --- | --- |
| 103 | data | `None` | `bsn%name` |
| 104 | data | `None` | `sp_ob%hru` |
| 105 | data | `None` | `"iwst "`, `"name "`, `"land_use_mgt_c"`, `"slope"`, `"hydgrp"`, `"null"`, `"null"` |
| 106 | data | `None` | `"--- "`, `"---- "`, `"--------------"`, `"m/m"`, `"------"`, `"null"`, `"null"` |
| 108 | data | `do ihru = 1, sp_ob%hru` | `ihru`, `ob(ihru)%name`, `hru(ihru)%land_use_mgt_c`, `hru(ihru)%topo%slope`, `soil(ihru)%hydgrp`, `"  null"`, `"   null"` |

### `SWIFT/hru_exco.swf`

- Review needed: yes
- Writer procedures changed: no
- Write-block count changed: no
- Write conditions changed: yes
- Write roles changed: yes
- Base flattened write order: `bsn%name`, `sp_ob%hru`, `" OUTPUT NAMES - NUBZ"`, `" OUTPUT UNITS - NUBZ"`, `ihru`, `wyld_rto`, `ob(icmd)%hd_aa(ihyd)%sed`, `ob(icmd)%hd_aa(ihyd)%orgn`, `ob(icmd)%hd_aa(ihyd)%sedp`, `ob(icmd)%hd_aa(ihyd)%no3`, `ob(icmd)%hd_aa(ihyd)%solp`, `ob(icmd)%hd_aa(ihyd)%nh3`, `ob(icmd)%hd_aa(ihyd)%no2`
- Candidate flattened write order: `bsn%name`, `sp_ob%hru`, `"HRU "`, `(hru_swift_hdr%hd_type(ihyd), 'wyld_rto', hru_swift_hdr%exco, ihyd = 1, hd_tot%hru)`, `"--- "`, `(hru_swift_hdr%hd_type(ihyd), 'wyld_rto', hru_swift_hdr%exco_unit, ihyd = 1, hd_tot%hru)`, `ihru`, `(hru_swift_hdr%hd_type(ihyd), wyld_rto(ihyd), ob(icmd)%hd_aa(ihyd)%sed, ob(icmd)%hd_aa(ihyd)%orgn, ob(icmd)%hd_aa(ihyd)%sedp, ob(icmd)%hd_aa(ihyd)%no3, ob(icmd)%hd_aa(ihyd)%solp, ob(icmd)%hd_aa(ihyd)%nh3, ob(icmd)%hd_aa(ihyd)%no2, ihyd = 1, hd_tot%hru)`

#### Write-order edits

- `replace` at base index 2 / candidate index 2: removed `" OUTPUT NAMES - NUBZ"`, `" OUTPUT UNITS - NUBZ"`; added `"HRU "`, `(hru_swift_hdr%hd_type(ihyd), 'wyld_rto', hru_swift_hdr%exco, ihyd = 1, hd_tot%hru)`, `"--- "`, `(hru_swift_hdr%hd_type(ihyd), 'wyld_rto', hru_swift_hdr%exco_unit, ihyd = 1, hd_tot%hru)`
- `replace` at base index 5 / candidate index 7: removed `wyld_rto`, `ob(icmd)%hd_aa(ihyd)%sed`, `ob(icmd)%hd_aa(ihyd)%orgn`, `ob(icmd)%hd_aa(ihyd)%sedp`, `ob(icmd)%hd_aa(ihyd)%no3`, `ob(icmd)%hd_aa(ihyd)%solp`, `ob(icmd)%hd_aa(ihyd)%nh3`, `ob(icmd)%hd_aa(ihyd)%no2`; added `(hru_swift_hdr%hd_type(ihyd), wyld_rto(ihyd), ob(icmd)%hd_aa(ihyd)%sed, ob(icmd)%hd_aa(ihyd)%orgn, ob(icmd)%hd_aa(ihyd)%sedp, ob(icmd)%hd_aa(ihyd)%no3, ob(icmd)%hd_aa(ihyd)%solp, ob(icmd)%hd_aa(ihyd)%nh3, ob(icmd)%hd_aa(ihyd)%no2, ihyd = 1, hd_tot%hru)`

#### Base write structure

- Source expression(s): `"SWIFT/hru_exco.swf"`

- Procedure: `swift_output`
- Writer: `swift_output.f90`
- Match: source_output
- Resolved default filename(s): `SWIFT/hru_exco.swf`
- Source filename expression(s): `"SWIFT/hru_exco.swf"`

| Line | Role | Condition | Fields written |
| --- | --- | --- | --- |
| 84 | data | `None` | `bsn%name` |
| 85 | data | `None` | `sp_ob%hru` |
| 86 | data | `None` | `" OUTPUT NAMES - NUBZ"` |
| 87 | data | `None` | `" OUTPUT UNITS - NUBZ"` |
| 90 | data | `do ihru = 1, sp_ob%hru` | `ihru` |
| 102 | data | `do ihru = 1, sp_ob%hru > do ihyd = 1, hd_tot%hru` | `wyld_rto`, `ob(icmd)%hd_aa(ihyd)%sed`, `ob(icmd)%hd_aa(ihyd)%orgn`, `ob(icmd)%hd_aa(ihyd)%sedp`, `ob(icmd)%hd_aa(ihyd)%no3`, `ob(icmd)%hd_aa(ihyd)%solp`, `ob(icmd)%hd_aa(ihyd)%nh3`, `ob(icmd)%hd_aa(ihyd)%no2` |


#### Candidate write structure

- Source expression(s): `"SWIFT/hru_exco.swf"`

- Procedure: `swift_output`
- Writer: `swift_output.f90`
- Match: source_output
- Resolved default filename(s): `SWIFT/hru_exco.swf`
- Source filename expression(s): `"SWIFT/hru_exco.swf"`

| Line | Role | Condition | Fields written |
| --- | --- | --- | --- |
| 115 | data | `None` | `bsn%name` |
| 116 | data | `None` | `sp_ob%hru` |
| 117 | data | `None` | `"HRU "`, `(hru_swift_hdr%hd_type(ihyd), 'wyld_rto', hru_swift_hdr%exco, ihyd = 1, hd_tot%hru)` |
| 120 | data | `None` | `"--- "`, `(hru_swift_hdr%hd_type(ihyd), 'wyld_rto', hru_swift_hdr%exco_unit, ihyd = 1, hd_tot%hru)` |
| 140 | data | `do ihru = 1, sp_ob%hru` | `ihru`, `(hru_swift_hdr%hd_type(ihyd), wyld_rto(ihyd), ob(icmd)%hd_aa(ihyd)%sed, ob(icmd)%hd_aa(ihyd)%orgn, ob(icmd)%hd_aa(ihyd)%sedp, ob(icmd)%hd_aa(ihyd)%no3, ob(icmd)%hd_aa(ihyd)%solp, ob(icmd)%hd_aa(ihyd)%nh3, ob(icmd)%hd_aa(ihyd)%no2, ihyd = 1, hd_tot%hru)` |

### `SWIFT/hru_wet.swf`

- Review needed: yes
- Writer procedures changed: no
- Write-block count changed: no
- Write conditions changed: no
- Write roles changed: no
- Base flattened write order: `bsn%name`, `sp_ob%hru`, `" OUTPUT NAMES - NUBZ"`, `" OUTPUT UNITS - NUBZ"`, `ihru`, `wet_hyd(ihyd)%psa`, `wet_hyd(ihyd)%pdep`, `wet_hyd(ihyd)%esa`, `wet_hyd(ihyd)%edep`
- Candidate flattened write order: `bsn%name`, `sp_ob%hru`, `"ires"`, `"psa "`, `"pdep"`, `"esa "`, `"edep"`, `"----"`, `"frac"`, `"mm  "`, `"frac"`, `"mm  "`, `ihru`, `wet_hyd(ihyd)%psa`, `wet_hyd(ihyd)%pdep`, `wet_hyd(ihyd)%esa`, `wet_hyd(ihyd)%edep`

#### Write-order edits

- `replace` at base index 2 / candidate index 2: removed `" OUTPUT NAMES - NUBZ"`, `" OUTPUT UNITS - NUBZ"`; added `"ires"`, `"psa "`, `"pdep"`, `"esa "`, `"edep"`, `"----"`, `"frac"`, `"mm  "`, `"frac"`, `"mm  "`

#### Base write structure

- Source expression(s): `"SWIFT/hru_wet.swf"`

- Procedure: `swift_output`
- Writer: `swift_output.f90`
- Match: source_output
- Resolved default filename(s): `SWIFT/hru_wet.swf`
- Source filename expression(s): `"SWIFT/hru_wet.swf"`

| Line | Role | Condition | Fields written |
| --- | --- | --- | --- |
| 111 | data | `None` | `bsn%name` |
| 112 | data | `None` | `sp_ob%hru` |
| 113 | data | `None` | `" OUTPUT NAMES - NUBZ"` |
| 114 | data | `None` | `" OUTPUT UNITS - NUBZ"` |
| 123 | data | `do ihru = 1, sp_ob%hru > if (hru(ihru)%dbs%surf_stor > 0) then` | `ihru`, `wet_hyd(ihyd)%psa`, `wet_hyd(ihyd)%pdep`, `wet_hyd(ihyd)%esa`, `wet_hyd(ihyd)%edep` |


#### Candidate write structure

- Source expression(s): `"SWIFT/hru_wet.swf"`

- Procedure: `swift_output`
- Writer: `swift_output.f90`
- Match: source_output
- Resolved default filename(s): `SWIFT/hru_wet.swf`
- Source filename expression(s): `"SWIFT/hru_wet.swf"`

| Line | Role | Condition | Fields written |
| --- | --- | --- | --- |
| 153 | data | `None` | `bsn%name` |
| 154 | data | `None` | `sp_ob%hru` |
| 155 | data | `None` | `"ires"`, `"psa "`, `"pdep"`, `"esa "`, `"edep"` |
| 156 | data | `None` | `"----"`, `"frac"`, `"mm  "`, `"frac"`, `"mm  "` |
| 165 | data | `do ihru = 1, sp_ob%hru > if (hru(ihru)%dbs%surf_stor > 0) then` | `ihru`, `wet_hyd(ihyd)%psa`, `wet_hyd(ihyd)%pdep`, `wet_hyd(ihyd)%esa`, `wet_hyd(ihyd)%edep` |

### `SWIFT/precip.swf`

- Review needed: yes
- Writer procedures changed: no
- Write-block count changed: no
- Write conditions changed: no
- Write roles changed: no
- Base flattened write order: `bsn%name`, `db_mx%wst`, `" OUTPUT NAMES - NUBZ"`, `" OUTPUT UNITS - NUBZ"`, `iwst`, `wst(iwst)%name`, `wst(iwst)%precip_aa`, `wst(iwst)%pet_aa`
- Candidate flattened write order: `bsn%name`, `db_mx%wst`, `"iwst "`, `"name "`, `"precip_aa/"`, `yrs_print`, `'yrs'`, `"pet_aa/"`, `yrs_print`, `'yrs'`, `"--- "`, `"---- "`, `"mm"`, `"mm"`, `iwst`, `wst(iwst)%name`, `wst(iwst)%precip_aa`, `wst(iwst)%pet_aa`

#### Write-order edits

- `replace` at base index 2 / candidate index 2: removed `" OUTPUT NAMES - NUBZ"`, `" OUTPUT UNITS - NUBZ"`; added `"iwst "`, `"name "`, `"precip_aa/"`, `yrs_print`, `'yrs'`, `"pet_aa/"`, `yrs_print`, `'yrs'`, `"--- "`, `"---- "`, `"mm"`, `"mm"`

#### Base write structure

- Source expression(s): `"SWIFT/precip.swf"`

- Procedure: `swift_output`
- Writer: `swift_output.f90`
- Match: source_output
- Resolved default filename(s): `SWIFT/precip.swf`
- Source filename expression(s): `"SWIFT/precip.swf"`

| Line | Role | Condition | Fields written |
| --- | --- | --- | --- |
| 59 | data | `None` | `bsn%name` |
| 60 | data | `None` | `db_mx%wst` |
| 61 | data | `None` | `" OUTPUT NAMES - NUBZ"` |
| 62 | data | `None` | `" OUTPUT UNITS - NUBZ"` |
| 66 | data | `do iwst = 1, db_mx%wst` | `iwst`, `wst(iwst)%name`, `wst(iwst)%precip_aa`, `wst(iwst)%pet_aa` |


#### Candidate write structure

- Source expression(s): `"SWIFT/precip.swf"`

- Procedure: `swift_output`
- Writer: `swift_output.f90`
- Match: source_output
- Resolved default filename(s): `SWIFT/precip.swf`
- Source filename expression(s): `"SWIFT/precip.swf"`

| Line | Role | Condition | Fields written |
| --- | --- | --- | --- |
| 90 | data | `None` | `bsn%name` |
| 91 | data | `None` | `db_mx%wst` |
| 92 | data | `None` | `"iwst "`, `"name "`, `"precip_aa/"`, `yrs_print`, `'yrs'`, `"pet_aa/"`, `yrs_print`, `'yrs'` |
| 93 | data | `None` | `"--- "`, `"---- "`, `"mm"`, `"mm"` |
| 97 | data | `do iwst = 1, db_mx%wst` | `iwst`, `wst(iwst)%name`, `wst(iwst)%precip_aa`, `wst(iwst)%pet_aa` |

### `SWIFT/res_dat.swf`

- Review needed: yes
- Writer procedures changed: no
- Write-block count changed: no
- Write conditions changed: no
- Write roles changed: no
- Base flattened write order: `bsn%name`, `sp_ob%res`, `" OUTPUT NAMES - NUBZ"`, `" OUTPUT UNITS - NUBZ"`, `ires`, `res_hyd(ires)%name`, `res_hyd(ires)%psa`, `res_hyd(ires)%pvol`, `res_hyd(ires)%esa`, `res_hyd(ires)%evol`
- Candidate flattened write order: `bsn%name`, `sp_ob%res`, `"icha "`, `"name "`, `"psa  "`, `"pvol "`, `"esa  "`, `"evol "`, `"---- "`, `"---- "`, `"frac "`, `"m3   "`, `"frac "`, `"m3   "`, `ires`, `res_hyd(ires)%name`, `res_hyd(ires)%psa`, `res_hyd(ires)%pvol`, `res_hyd(ires)%esa`, `res_hyd(ires)%evol`

#### Write-order edits

- `replace` at base index 2 / candidate index 2: removed `" OUTPUT NAMES - NUBZ"`, `" OUTPUT UNITS - NUBZ"`; added `"icha "`, `"name "`, `"psa  "`, `"pvol "`, `"esa  "`, `"evol "`, `"---- "`, `"---- "`, `"frac "`, `"m3   "`, `"frac "`, `"m3   "`

#### Base write structure

- Source expression(s): `"SWIFT/res_dat.swf"`

- Procedure: `swift_output`
- Writer: `swift_output.f90`
- Match: source_output
- Resolved default filename(s): `SWIFT/res_dat.swf`
- Source filename expression(s): `"SWIFT/res_dat.swf"`

| Line | Role | Condition | Fields written |
| --- | --- | --- | --- |
| 175 | data | `None` | `bsn%name` |
| 176 | data | `None` | `sp_ob%res` |
| 177 | data | `None` | `" OUTPUT NAMES - NUBZ"` |
| 178 | data | `None` | `" OUTPUT UNITS - NUBZ"` |
| 180 | data | `do ires = 1, sp_ob%res` | `ires`, `res_hyd(ires)%name`, `res_hyd(ires)%psa`, `res_hyd(ires)%pvol`, `res_hyd(ires)%esa`, `res_hyd(ires)%evol` |


#### Candidate write structure

- Source expression(s): `"SWIFT/res_dat.swf"`

- Procedure: `swift_output`
- Writer: `swift_output.f90`
- Match: source_output
- Resolved default filename(s): `SWIFT/res_dat.swf`
- Source filename expression(s): `"SWIFT/res_dat.swf"`

| Line | Role | Condition | Fields written |
| --- | --- | --- | --- |
| 219 | data | `None` | `bsn%name` |
| 220 | data | `None` | `sp_ob%res` |
| 221 | data | `None` | `"icha "`, `"name "`, `"psa  "`, `"pvol "`, `"esa  "`, `"evol "` |
| 222 | data | `None` | `"---- "`, `"---- "`, `"frac "`, `"m3   "`, `"frac "`, `"m3   "` |
| 224 | data | `do ires = 1, sp_ob%res` | `ires`, `res_hyd(ires)%name`, `res_hyd(ires)%psa`, `res_hyd(ires)%pvol`, `res_hyd(ires)%esa`, `res_hyd(ires)%evol` |

### `SWIFT/res_dr.swf`

- Review needed: yes
- Writer procedures changed: no
- Write-block count changed: no
- Write conditions changed: no
- Write roles changed: no
- Base flattened write order: `bsn%name`, `sp_ob%res`, `" OUTPUT NAMES - NUBZ"`, `" OUTPUT UNITS - NUBZ"`, `ires`, `ob(icmd)%name`, `ht5%flo`, `ht5%sed`, `ht5%orgn`, `ht5%sedp`, `ht5%no3`, `ht5%solp`, `ht5%nh3`, `ht5%no2`
- Candidate flattened write order: `bsn%name`, `sp_ob%res`, `"ires "`, `"name "`, `hru_swift_hdr%dr`, `"---- "`, `"---- "`, `hru_swift_hdr%dr_unit`, `ires`, `ob(icmd)%name`, `ht5%flo`, `ht5%sed`, `ht5%orgn`, `ht5%sedp`, `ht5%no3`, `ht5%solp`, `ht5%nh3`, `ht5%no2`

#### Write-order edits

- `replace` at base index 2 / candidate index 2: removed `" OUTPUT NAMES - NUBZ"`, `" OUTPUT UNITS - NUBZ"`; added `"ires "`, `"name "`, `hru_swift_hdr%dr`, `"---- "`, `"---- "`, `hru_swift_hdr%dr_unit`

#### Base write structure

- Source expression(s): `"SWIFT/res_dr.swf"`

- Procedure: `swift_output`
- Writer: `swift_output.f90`
- Match: source_output
- Resolved default filename(s): `SWIFT/res_dr.swf`
- Source filename expression(s): `"SWIFT/res_dr.swf"`

| Line | Role | Condition | Fields written |
| --- | --- | --- | --- |
| 187 | data | `None` | `bsn%name` |
| 188 | data | `None` | `sp_ob%res` |
| 189 | data | `None` | `" OUTPUT NAMES - NUBZ"` |
| 190 | data | `None` | `" OUTPUT UNITS - NUBZ"` |
| 194 | data | `do ires = 1, sp_ob%res` | `ires`, `ob(icmd)%name`, `ht5%flo`, `ht5%sed`, `ht5%orgn`, `ht5%sedp`, `ht5%no3`, `ht5%solp`, `ht5%nh3`, `ht5%no2` |


#### Candidate write structure

- Source expression(s): `"SWIFT/res_dr.swf"`

- Procedure: `swift_output`
- Writer: `swift_output.f90`
- Match: source_output
- Resolved default filename(s): `SWIFT/res_dr.swf`
- Source filename expression(s): `"SWIFT/res_dr.swf"`

| Line | Role | Condition | Fields written |
| --- | --- | --- | --- |
| 231 | data | `None` | `bsn%name` |
| 232 | data | `None` | `sp_ob%res` |
| 233 | data | `None` | `"ires "`, `"name "`, `hru_swift_hdr%dr` |
| 234 | data | `None` | `"---- "`, `"---- "`, `hru_swift_hdr%dr_unit` |
| 238 | data | `do ires = 1, sp_ob%res` | `ires`, `ob(icmd)%name`, `ht5%flo`, `ht5%sed`, `ht5%orgn`, `ht5%sedp`, `ht5%no3`, `ht5%solp`, `ht5%nh3`, `ht5%no2` |


## Possible renames or replacements

_None._
