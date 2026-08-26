# SWAT+ Input Contract Changes

This is the primary source-level input change report. Filenames are resolved from the same defaults used by the schema extractor. A resolved default can still be overridden by runtime configuration.

## Summary

- Added input defaults: **7**
- Removed input defaults: **4**
- Changed read contracts: **8**
- Possible renames or replacements: **4**
- Candidate open/read blocks with unresolved filenames: **27**
- Newly unresolved filename expressions in the candidate: **1**

## Added inputs

### `outside_src.wal`

- Schema status: `readable_needs_schema_review`
- Review needed: yes
- Source expression(s): `outside_src.wal`

- Procedure: `water_osrc_read`
- Reader: `water_osrc_read.f90`
- Match: source_input
- Resolved default filename(s): `outside_src.wal`
- Source filename expression(s): `outside_src.wal`
- Open: line 34, file expression `'outside_src.wal'`, parser value `outside_src.wal`, condition `if (.not. i_exist .or. 'outside_src.wal' == "null") then / else > do`

| Line | Role | Condition | Fields read |
| --- | --- | --- | --- |
| 35 | title | `if (.not. i_exist .or. 'outside_src.wal' == "null") then / else > do` | `titldum` |
| 37 | count | `if (.not. i_exist .or. 'outside_src.wal' == "null") then / else > do` | `imax` |
| 38 | header | `if (.not. i_exist .or. 'outside_src.wal' == "null") then / else > do` | `header` |
| 47 | data | `if (.not. i_exist .or. 'outside_src.wal' == "null") then / else > do > do isrc = 1, imax` | `osrc(isrc)%name`, `osrc(isrc)%conc(lev)%org_min_typ`, `osrc(isrc)%conc(lev)%org_min_name`, `osrc(isrc)%conc(lev)%pests_typ`, `osrc(isrc)%conc(lev)%pests_name`, `osrc(isrc)%conc(lev)%paths_typ`, `osrc(isrc)%conc(lev)%paths_name`, `osrc(isrc)%conc(lev)%salts_typ`, `osrc(isrc)%conc(lev)%salts_name`, `osrc(isrc)%conc(lev)%constit_typ`, `osrc(isrc)%conc(lev)%constit_name`, `osrc(isrc)%descrip` |
| 89 | header | `if (.not. i_exist .or. 'outside_src.wal' == "null") then / else > do > do isrc = 1, imax > if (cs_db%num_pests > 0) then` | `header` |
| 90 | data | `if (.not. i_exist .or. 'outside_src.wal' == "null") then / else > do > do isrc = 1, imax > if (cs_db%num_pests > 0) then` | `osrc_cs(isrc)%pest` |
| 96 | header | `if (.not. i_exist .or. 'outside_src.wal' == "null") then / else > do > do isrc = 1, imax > if (cs_db%num_paths > 0) then` | `header` |
| 97 | data | `if (.not. i_exist .or. 'outside_src.wal' == "null") then / else > do > do isrc = 1, imax > if (cs_db%num_paths > 0) then` | `osrc_cs(isrc)%path` |

### `place_of_use.wro`

- Schema status: `readable_needs_schema_review`
- Review needed: yes
- Source expression(s): `in_wallo%pou`

- Procedure: `water_allocation_read`
- Reader: `water_allocation_read.f90`
- Match: source_input
- Resolved default filename(s): `place_of_use.wro`
- Source filename expression(s): `in_wallo%pou`
- Open: line 40, file expression `in_wallo%pou`, parser value `in_wallo%pou`, condition `if (.not. i_exist .or. in_wallo%pou /= "null") then > do`

| Line | Role | Condition | Fields read |
| --- | --- | --- | --- |
| 41 | title | `if (.not. i_exist .or. in_wallo%pou /= "null") then > do` | `titldum` |
| 43 | count | `if (.not. i_exist .or. in_wallo%pou /= "null") then > do` | `imax` |
| 58 | header | `if (.not. i_exist .or. in_wallo%pou /= "null") then > do` | `header` |
| 63 | data | `if (.not. i_exist .or. in_wallo%pou /= "null") then > do > do i = 1, imax` | `ipou` |
| 67 | data | `if (.not. i_exist .or. in_wallo%pou /= "null") then > do > do i = 1, imax` | `ip`, `pou(ipou)%name`, `pou(ipou)%typ`, `pou(ipou)%typ_num`, `pou(ipou)%pods`, `pou(ipou)%pors`, `pou(ipou)%dtbl_mx`, `pou(ipou)%rate_max`, `pou(ipou)%dtbl_pod_fr`, `pou(ipou)%dtbl_por_fr` |
| 93 | data | `if (.not. i_exist .or. in_wallo%pou /= "null") then > do > do i = 1, imax > do ipod = 1, ipods` | `pp`, `pou(ipou)%pod(ipod)%num`, `pou(ipou)%pod(ipod)%name`, `pou(ipou)%pod(ipod)%typ`, `pou(ipou)%pod(ipod)%num`, `pou(ipou)%pod(ipod)%conv_typ`, `pou(ipou)%pod(ipod)%conv_num`, `pou(ipou)%pod(ipod)%dtbl_min`, `pou(ipou)%pod(ipod)%const_min`, `pou(ipou)%pod(ipod)%dtbl_wdraw`, `pou(ipou)%pod(ipod)%ann_max`, `pou(ipou)%pod(ipod)%frac`, `pou(ipou)%pod(ipod)%comp` |
| 102 | data | `if (.not. i_exist .or. in_wallo%pou /= "null") then > do > do i = 1, imax > do ipor = 1, ipors` | `pp`, `pou(ipou)%por(ipor)%num`, `pou(ipou)%por(ipor)%name`, `pou(ipou)%por(ipor)%typ`, `pou(ipou)%por(ipor)%num`, `pou(ipou)%por(ipor)%conv_typ`, `pou(ipou)%por(ipor)%conv_num`, `pou(ipou)%por(ipor)%dtbl_max`, `pou(ipou)%por(ipor)%const_max`, `pou(ipou)%por(ipor)%ann_max`, `pou(ipou)%por(ipor)%frac` |

### `point_of_diver.wro`

- Schema status: `readable_needs_schema_review`
- Review needed: yes
- Source expression(s): `in_wallo%pod`

- Procedure: `water_allocation_read`
- Reader: `water_allocation_read.f90`
- Match: source_input
- Resolved default filename(s): `point_of_diver.wro`
- Source filename expression(s): `in_wallo%pod`
- Open: line 194, file expression `in_wallo%pod`, parser value `in_wallo%pod`, condition `if (.not. i_exist .or. in_wallo%pod /= "null") then > do`

| Line | Role | Condition | Fields read |
| --- | --- | --- | --- |
| 195 | title | `if (.not. i_exist .or. in_wallo%pod /= "null") then > do` | `titldum` |
| 197 | count | `if (.not. i_exist .or. in_wallo%pod /= "null") then > do` | `imax` |
| 200 | header | `if (.not. i_exist .or. in_wallo%pod /= "null") then > do` | `header` |
| 210 | data | `if (.not. i_exist .or. in_wallo%pod /= "null") then > do > do ipod = 1, imax` | `pod(ipod)%num`, `pod(ipod)%name`, `pod(ipod)%typ`, `pod(ipod)%typ_num`, `ipous` |
| 220 | data | `if (.not. i_exist .or. in_wallo%pod /= "null") then > do > do ipod = 1, imax` | `pod(ipod)%num`, `pod(ipod)%name`, `pod(ipod)%typ`, `pod(ipod)%typ_num`, `pod(ipod)%pous`, `(pod(ipod)%pou(ipou)%num, pod(ipod)%pou(ipou)%name, pod(ipod)%pou(ipou)%pod_num, pod(ipod)%pou(ipou)%typ, pod(ipod)%pou(ipou)%typ_num, pod(ipod)%pou(ipou)%right, ipou = 1, ipous)` |

### `recall.rec`

- Schema status: `readable_needs_schema_review`
- Review needed: yes
- Source expression(s): `recall.rec`

- Procedure: `recall_read`
- Reader: `recall_read.f90`
- Match: source_input
- Resolved default filename(s): `recall.rec`
- Source filename expression(s): `recall.rec`
- Open: line 116, file expression `"recall.rec"`, parser value `recall.rec`, condition `if (i_exist .or. "recall.rec" /= "null") then > do`

| Line | Role | Condition | Fields read |
| --- | --- | --- | --- |
| 117 | title | `if (i_exist .or. "recall.rec" /= "null") then > do` | `titldum` |
| 119 | header | `if (i_exist .or. "recall.rec" /= "null") then > do` | `header` |
| 123 | data | `if (i_exist .or. "recall.rec" /= "null") then > do > do while (eof == 0)` | `i` |
| 136 | title | `if (i_exist .or. "recall.rec" /= "null") then > do` | `titldum` |
| 137 | header | `if (i_exist .or. "recall.rec" /= "null") then > do` | `header` |
| 140 | data | `if (i_exist .or. "recall.rec" /= "null") then > do > do ii = 1, imax` | `i` |
| 143 | data | `if (i_exist .or. "recall.rec" /= "null") then > do > do ii = 1, imax` | `k`, `recall(i)%name`, `recall(i)%typ`, `recall(i)%filename` |

### `transplant.ops`

- Schema status: `readable_needs_schema_review`
- Review needed: yes
- Source expression(s): `transplant.ops`

- Procedure: `plant_transplant_read`
- Reader: `plant_transplant_read.f90`
- Match: source_input
- Resolved default filename(s): `transplant.ops`
- Source filename expression(s): `transplant.ops`
- Open: line 24, file expression `"transplant.ops"`, parser value `transplant.ops`, condition `if (.not. i_exist .or. "transplant.ops" == " null") then / else > do`

| Line | Role | Condition | Fields read |
| --- | --- | --- | --- |
| 25 | title | `if (.not. i_exist .or. "transplant.ops" == " null") then / else > do` | `titldum` |
| 27 | header | `if (.not. i_exist .or. "transplant.ops" == " null") then / else > do` | `header` |
| 30 | title | `if (.not. i_exist .or. "transplant.ops" == " null") then / else > do > do while (eof == 0)` | `titldum` |
| 37 | title | `if (.not. i_exist .or. "transplant.ops" == " null") then / else > do` | `titldum` |
| 39 | header | `if (.not. i_exist .or. "transplant.ops" == " null") then / else > do` | `header` |
| 43 | data | `if (.not. i_exist .or. "transplant.ops" == " null") then / else > do > do ic = 1, imax` | `transpl(ic)` |

### `water_hru_irr.wal`

- Schema status: `readable_needs_schema_review`
- Review needed: yes
- Source expression(s): `water_hru_irr.wal`

- Procedure: `water_hru_irr_read`
- Reader: `water_hru_irr_read.f90`
- Match: source_input
- Resolved default filename(s): `water_hru_irr.wal`
- Source filename expression(s): `water_hru_irr.wal`
- Open: line 29, file expression `'water_hru_irr.wal'`, parser value `water_hru_irr.wal`, condition `if (i_exist) then > do`

| Line | Role | Condition | Fields read |
| --- | --- | --- | --- |
| 30 | title | `if (i_exist) then > do` | `titldum` |
| 32 | count | `if (i_exist) then > do` | `imax` |
| 33 | header | `if (i_exist) then > do` | `header` |
| 40 | data | `if (i_exist) then > do > do irr = 1, imax` | `hruirr_db(irr)%name`, `hruirr_db(irr)%hrus` |
| 45 | data | `if (i_exist) then > do > do irr = 1, imax > do j = 1, num_hru` | `hruirr_db(irr)%hru_num(j)`, `hruirr_db(irr)%dtbl_lum(j)` |

### `wtps_wuses.wal`

- Schema status: `readable_needs_schema_review`
- Review needed: yes
- Source expression(s): `wtps_wuses.wal`

- Procedure: `wallo_wtps_wuses`
- Reader: `wallo_wtps_wuses.f90`
- Match: source_input
- Resolved default filename(s): `wtps_wuses.wal`
- Source filename expression(s): `wtps_wuses.wal`
- Open: line 27, file expression `'wtps_wuses.wal'`, parser value `wtps_wuses.wal`, condition `if (i_exist .or. 'wtps_wuses.wal' /= "null") then > do`

| Line | Role | Condition | Fields read |
| --- | --- | --- | --- |
| 28 | title | `if (i_exist .or. 'wtps_wuses.wal' /= "null") then > do` | `titldum` |
| 32 | data | `if (i_exist .or. 'wtps_wuses.wal' /= "null") then > do` | `wtps`, `wuses` |
| 53 | title | `if (i_exist .or. 'wtps_wuses.wal' /= "null") then > do` | `titldum` |
| 56 | data | `if (i_exist .or. 'wtps_wuses.wal' /= "null") then > do` | `(wtp_name(iwtp), iwtp = 1, wtps)` |
| 59 | data | `if (i_exist .or. 'wtps_wuses.wal' /= "null") then > do` | `(wuse_name(iwuse), iwuse = 1, wuses)` |
| 61 | title | `if (i_exist .or. 'wtps_wuses.wal' /= "null") then > do` | `titldum` |


## Removed inputs

### `manure.frt`

- Schema status: `certified`
- Review needed: no
- Source expression(s): `manure.frt`

- Procedure: `manure_parm_read`
- Reader: `manure_parm_read.f90`
- Match: source_input
- Resolved default filename(s): `manure.frt`
- Source filename expression(s): `manure.frt`
- Open: line 27, file expression `"manure.frt"`, parser value `manure.frt`, condition `if (.not. i_exist .or. "manure.frt" == "null") then / else > do`

| Line | Role | Condition | Fields read |
| --- | --- | --- | --- |
| 28 | title | `if (.not. i_exist .or. "manure.frt" == "null") then / else > do` | `titldum` |
| 30 | header | `if (.not. i_exist .or. "manure.frt" == "null") then / else > do` | `header` |
| 33 | title | `if (.not. i_exist .or. "manure.frt" == "null") then / else > do > do while (eof == 0)` | `titldum` |
| 41 | title | `if (.not. i_exist .or. "manure.frt" == "null") then / else > do` | `titldum` |
| 43 | header | `if (.not. i_exist .or. "manure.frt" == "null") then / else > do` | `header` |
| 47 | data | `if (.not. i_exist .or. "manure.frt" == "null") then / else > do > do it = 1, imax` | `manure_db(it)` |

### `out_src.wal`

- Schema status: `certified`
- Review needed: no
- Source expression(s): `out_src.wal`

- Procedure: `water_osrc_read`
- Reader: `water_osrc_read.f90`
- Match: source_input
- Resolved default filename(s): `out_src.wal`
- Source filename expression(s): `out_src.wal`
- Open: line 34, file expression `'out_src.wal'`, parser value `out_src.wal`, condition `if (.not. i_exist .or. 'outside_src.wal' == "null") then / else > do`

| Line | Role | Condition | Fields read |
| --- | --- | --- | --- |
| 35 | title | `if (.not. i_exist .or. 'outside_src.wal' == "null") then / else > do` | `titldum` |
| 37 | count | `if (.not. i_exist .or. 'outside_src.wal' == "null") then / else > do` | `imax` |
| 38 | header | `if (.not. i_exist .or. 'outside_src.wal' == "null") then / else > do` | `header` |
| 45 | data | `if (.not. i_exist .or. 'outside_src.wal' == "null") then / else > do > do isrc = 1, imax` | `i`, `osrc(isrc)%name`, `osrc(isrc)%stor_mx`, `osrc(isrc)%lag_days`, `osrc(isrc)%loss_fr` |
| 53 | header | `if (.not. i_exist .or. 'outside_src.wal' == "null") then / else > do > if (cs_db%num_pests > 0) then` | `header` |
| 54 | data | `if (.not. i_exist .or. 'outside_src.wal' == "null") then / else > do > if (cs_db%num_pests > 0) then` | `osrc_cs(isrc)%pest` |
| 60 | header | `if (.not. i_exist .or. 'outside_src.wal' == "null") then / else > do > if (cs_db%num_paths > 0) then` | `header` |
| 61 | data | `if (.not. i_exist .or. 'outside_src.wal' == "null") then / else > do > if (cs_db%num_paths > 0) then` | `osrc_cs(isrc)%path` |

### `transplant.plt`

- Schema status: `certified`
- Review needed: no
- Source expression(s): `transplant.plt`

- Procedure: `plant_transplant_read`
- Reader: `plant_transplant_read.f90`
- Match: source_input
- Resolved default filename(s): `transplant.plt`
- Source filename expression(s): `transplant.plt`
- Open: line 24, file expression `"transplant.plt"`, parser value `transplant.plt`, condition `if (.not. i_exist .or. "transplant.plt" == " null") then / else > do`

| Line | Role | Condition | Fields read |
| --- | --- | --- | --- |
| 25 | title | `if (.not. i_exist .or. "transplant.plt" == " null") then / else > do` | `titldum` |
| 27 | header | `if (.not. i_exist .or. "transplant.plt" == " null") then / else > do` | `header` |
| 30 | title | `if (.not. i_exist .or. "transplant.plt" == " null") then / else > do > do while (eof == 0)` | `titldum` |
| 37 | title | `if (.not. i_exist .or. "transplant.plt" == " null") then / else > do` | `titldum` |
| 39 | header | `if (.not. i_exist .or. "transplant.plt" == " null") then / else > do` | `header` |
| 43 | data | `if (.not. i_exist .or. "transplant.plt" == " null") then / else > do > do ic = 1, imax` | `transpl(ic)` |

### `water_allocation.wro`

- Schema status: `certified`
- Review needed: no
- Source expression(s): `in_watrts%transfer_wro`

- Procedure: `water_allocation_read`
- Reader: `water_allocation_read.f90`
- Match: source_input
- Resolved default filename(s): `water_allocation.wro`
- Source filename expression(s): `in_watrts%transfer_wro`
- Open: line 47, file expression `in_watrts%transfer_wro`, parser value `in_watrts%transfer_wro`, condition `if (.not. i_exist .or. in_watrts%transfer_wro == "null") then / else > do`

| Line | Role | Condition | Fields read |
| --- | --- | --- | --- |
| 48 | title | `if (.not. i_exist .or. in_watrts%transfer_wro == "null") then / else > do` | `titldum` |
| 50 | count | `if (.not. i_exist .or. in_watrts%transfer_wro == "null") then / else > do` | `imax` |
| 65 | header | `if (.not. i_exist .or. in_watrts%transfer_wro == "null") then / else > do > do iwro = 1, imax` | `header` |
| 67 | data | `if (.not. i_exist .or. in_watrts%transfer_wro == "null") then / else > do > do iwro = 1, imax` | `wallo(iwro)%name`, `wallo(iwro)%rule_typ`, `wallo(iwro)%trn_obs` |
| 70 | header | `if (.not. i_exist .or. in_watrts%transfer_wro == "null") then / else > do > do iwro = 1, imax` | `header` |
| 88 | data | `if (.not. i_exist .or. in_watrts%transfer_wro == "null") then / else > do > do iwro = 1, imax > do itrn = 1, num_objs` | `i` |
| 92 | data | `if (.not. i_exist .or. in_watrts%transfer_wro == "null") then / else > do > do iwro = 1, imax > do itrn = 1, num_objs` | `k`, `wallo(iwro)%trn(i)%trn_typ`, `wallo(iwro)%trn(i)%trn_typ_name`, `wallo(iwro)%trn(i)%amount`, `wallo(iwro)%trn(i)%right`, `wallo(iwro)%trn(i)%src_num` |
| 139 | data | `if (.not. i_exist .or. in_watrts%transfer_wro == "null") then / else > do > do iwro = 1, imax > do itrn = 1, num_objs` | `k`, `wallo(iwro)%trn(i)%trn_typ`, `wallo(iwro)%trn(i)%trn_typ_name`, `wallo(iwro)%trn(i)%amount`, `wallo(iwro)%trn(i)%right`, `wallo(iwro)%trn(i)%src_num`, `wallo(iwro)%trn(i)%dtbl_src`, `(wallo(iwro)%trn(i)%src(isrc), isrc = 1, num_src)`, `wallo(iwro)%trn(i)%rcv` |


## Changed input read contracts

### `file.cio`

- Review needed: yes
- Reader procedures changed: no
- Read-block count changed: no
- Read conditions changed: no
- Base flattened read order: `titldum`, `name`, `in_sim`, `name`, `in_basin`, `name`, `in_cli`, `name`, `in_con`, `name`, `in_cha`, `name`, `in_res`, `name`, `in_ru`, `name`, `in_hru`, `name`, `in_exco`, `name`, `in_rec`, `name`, `in_delr`, `name`, `in_aqu`, `name`, `in_herd`, `name`, `in_watrts`, `name`, `in_link`, `name`, `in_hyd`, `name`, `in_str`, `name`, `in_parmdb`, `name`, `in_ops`, `name`, `in_lum`, `name`, `in_chg`, `name`, `in_init`, `name`, `in_sol`, `name`, `in_cond`, `name`, `in_regs`, `name`, `in_path_pcp`, `name`, `in_path_tmp`, `name`, `in_path_slr`, `name`, `in_path_hmd`, `name`, `in_path_wnd`, `line_buffer`
- Candidate flattened read order: `titldum`, `name`, `in_sim`, `name`, `in_basin`, `name`, `in_cli`, `name`, `in_con`, `name`, `in_cha`, `name`, `in_res`, `name`, `in_ru`, `name`, `in_hru`, `name`, `in_exco`, `name`, `in_rec`, `name`, `in_delr`, `name`, `in_aqu`, `name`, `in_herd`, `name`, `in_wallo`, `name`, `in_link`, `name`, `in_hyd`, `name`, `in_str`, `name`, `in_parmdb`, `name`, `in_ops`, `name`, `in_lum`, `name`, `in_chg`, `name`, `in_init`, `name`, `in_sol`, `name`, `in_cond`, `name`, `in_regs`, `name`, `in_path_pcp`, `name`, `in_path_tmp`, `name`, `in_path_slr`, `name`, `in_path_hmd`, `name`, `in_path_wnd`, `line_buffer`

#### Read-order edits

- `replace` at base index 28 / candidate index 28: removed `in_watrts`; added `in_wallo`

#### Base read structure

- Schema status: `readable_needs_schema_review`
- Review needed: yes
- Source expression(s): `file.cio`

- Procedure: `readcio_read`
- Reader: `readcio_read.f90`
- Match: source_input
- Resolved default filename(s): `file.cio`
- Source filename expression(s): `file.cio`
- Open: line 22, file expression `"file.cio"`, parser value `file.cio`, condition `if (i_exist ) then`

| Line | Role | Condition | Fields read |
| --- | --- | --- | --- |
| 23 | title | `if (i_exist ) then` | `titldum` |
| 25 | data | `if (i_exist ) then > do i = 1, 31` | `name`, `in_sim` |
| 27 | data | `if (i_exist ) then > do i = 1, 31` | `name`, `in_basin` |
| 29 | data | `if (i_exist ) then > do i = 1, 31` | `name`, `in_cli` |
| 31 | data | `if (i_exist ) then > do i = 1, 31` | `name`, `in_con` |
| 33 | data | `if (i_exist ) then > do i = 1, 31` | `name`, `in_cha` |
| 35 | data | `if (i_exist ) then > do i = 1, 31` | `name`, `in_res` |
| 37 | data | `if (i_exist ) then > do i = 1, 31` | `name`, `in_ru` |
| 39 | data | `if (i_exist ) then > do i = 1, 31` | `name`, `in_hru` |
| 41 | data | `if (i_exist ) then > do i = 1, 31` | `name`, `in_exco` |
| 43 | data | `if (i_exist ) then > do i = 1, 31` | `name`, `in_rec` |
| 45 | data | `if (i_exist ) then > do i = 1, 31` | `name`, `in_delr` |
| 47 | data | `if (i_exist ) then > do i = 1, 31` | `name`, `in_aqu` |
| 49 | data | `if (i_exist ) then > do i = 1, 31` | `name`, `in_herd` |
| 51 | data | `if (i_exist ) then > do i = 1, 31` | `name`, `in_watrts` |
| 53 | data | `if (i_exist ) then > do i = 1, 31` | `name`, `in_link` |
| 55 | data | `if (i_exist ) then > do i = 1, 31` | `name`, `in_hyd` |
| 57 | data | `if (i_exist ) then > do i = 1, 31` | `name`, `in_str` |
| 59 | data | `if (i_exist ) then > do i = 1, 31` | `name`, `in_parmdb` |
| 61 | data | `if (i_exist ) then > do i = 1, 31` | `name`, `in_ops` |
| 63 | data | `if (i_exist ) then > do i = 1, 31` | `name`, `in_lum` |
| 65 | data | `if (i_exist ) then > do i = 1, 31` | `name`, `in_chg` |
| 67 | data | `if (i_exist ) then > do i = 1, 31` | `name`, `in_init` |
| 69 | data | `if (i_exist ) then > do i = 1, 31` | `name`, `in_sol` |
| 71 | data | `if (i_exist ) then > do i = 1, 31` | `name`, `in_cond` |
| 73 | data | `if (i_exist ) then > do i = 1, 31` | `name`, `in_regs` |
| 76 | data | `if (i_exist ) then > do i = 1, 31` | `name`, `in_path_pcp` |
| 78 | data | `if (i_exist ) then > do i = 1, 31` | `name`, `in_path_tmp` |
| 80 | data | `if (i_exist ) then > do i = 1, 31` | `name`, `in_path_slr` |
| 82 | data | `if (i_exist ) then > do i = 1, 31` | `name`, `in_path_hmd` |
| 84 | data | `if (i_exist ) then > do i = 1, 31` | `name`, `in_path_wnd` |
| 89 | data | `if (i_exist ) then > do i = 1, 31` | `line_buffer` |


#### Candidate read structure

- Schema status: `readable_needs_schema_review`
- Review needed: yes
- Source expression(s): `file.cio`

- Procedure: `readcio_read`
- Reader: `readcio_read.f90`
- Match: source_input
- Resolved default filename(s): `file.cio`
- Source filename expression(s): `file.cio`
- Open: line 22, file expression `"file.cio"`, parser value `file.cio`, condition `if (i_exist ) then`

| Line | Role | Condition | Fields read |
| --- | --- | --- | --- |
| 23 | title | `if (i_exist ) then` | `titldum` |
| 25 | data | `if (i_exist ) then > do i = 1, 31` | `name`, `in_sim` |
| 27 | data | `if (i_exist ) then > do i = 1, 31` | `name`, `in_basin` |
| 29 | data | `if (i_exist ) then > do i = 1, 31` | `name`, `in_cli` |
| 31 | data | `if (i_exist ) then > do i = 1, 31` | `name`, `in_con` |
| 33 | data | `if (i_exist ) then > do i = 1, 31` | `name`, `in_cha` |
| 35 | data | `if (i_exist ) then > do i = 1, 31` | `name`, `in_res` |
| 37 | data | `if (i_exist ) then > do i = 1, 31` | `name`, `in_ru` |
| 39 | data | `if (i_exist ) then > do i = 1, 31` | `name`, `in_hru` |
| 41 | data | `if (i_exist ) then > do i = 1, 31` | `name`, `in_exco` |
| 43 | data | `if (i_exist ) then > do i = 1, 31` | `name`, `in_rec` |
| 45 | data | `if (i_exist ) then > do i = 1, 31` | `name`, `in_delr` |
| 47 | data | `if (i_exist ) then > do i = 1, 31` | `name`, `in_aqu` |
| 49 | data | `if (i_exist ) then > do i = 1, 31` | `name`, `in_herd` |
| 51 | data | `if (i_exist ) then > do i = 1, 31` | `name`, `in_wallo` |
| 53 | data | `if (i_exist ) then > do i = 1, 31` | `name`, `in_link` |
| 55 | data | `if (i_exist ) then > do i = 1, 31` | `name`, `in_hyd` |
| 57 | data | `if (i_exist ) then > do i = 1, 31` | `name`, `in_str` |
| 59 | data | `if (i_exist ) then > do i = 1, 31` | `name`, `in_parmdb` |
| 61 | data | `if (i_exist ) then > do i = 1, 31` | `name`, `in_ops` |
| 63 | data | `if (i_exist ) then > do i = 1, 31` | `name`, `in_lum` |
| 65 | data | `if (i_exist ) then > do i = 1, 31` | `name`, `in_chg` |
| 67 | data | `if (i_exist ) then > do i = 1, 31` | `name`, `in_init` |
| 69 | data | `if (i_exist ) then > do i = 1, 31` | `name`, `in_sol` |
| 71 | data | `if (i_exist ) then > do i = 1, 31` | `name`, `in_cond` |
| 73 | data | `if (i_exist ) then > do i = 1, 31` | `name`, `in_regs` |
| 76 | data | `if (i_exist ) then > do i = 1, 31` | `name`, `in_path_pcp` |
| 78 | data | `if (i_exist ) then > do i = 1, 31` | `name`, `in_path_tmp` |
| 80 | data | `if (i_exist ) then > do i = 1, 31` | `name`, `in_path_slr` |
| 82 | data | `if (i_exist ) then > do i = 1, 31` | `name`, `in_path_hmd` |
| 84 | data | `if (i_exist ) then > do i = 1, 31` | `name`, `in_path_wnd` |
| 89 | data | `if (i_exist ) then > do i = 1, 31` | `line_buffer` |

### `recall_db.rec`

- Review needed: yes
- Reader procedures changed: no
- Read-block count changed: no
- Read conditions changed: no
- Base flattened read order: `titldum`, `header`, `i`, `titldum`, `header`, `i`, `k`, `recall_db(i)%name`, `recall_db(i)%org_min`, `recall_db(i)%pest`, `recall_db(i)%path`, `recall_db(i)%hmet`, `recall_db(i)%salt`, `recall_db(i)%constit`
- Candidate flattened read order: `titldum`, `header`, `i`, `titldum`, `header`, `i`, `k`, `recall_db(i)%name`, `recall_db(i)%org_min`, `recall_db(i)%pest`, `recall_db(i)%path`, `recall_db(i)%hmet`, `recall_db(i)%salt`, `recall_db(i)%constit`, `recall_db(i)%descrip`

#### Read-order edits

- `insert` at base index 14 / candidate index 14: removed _no fields captured_; added `recall_db(i)%descrip`

#### Base read structure

- Schema status: `certified`
- Review needed: no
- Source expression(s): `recall_db.rec`

- Procedure: `recalldb_read`
- Reader: `recall_read.f90`
- Match: source_input
- Resolved default filename(s): `recall_db.rec`
- Source filename expression(s): `recall_db.rec`
- Open: line 24, file expression `"recall_db.rec"`, parser value `recall_db.rec`, condition `if (i_exist .or. "recall_db.rec" /= "null") then > do`

| Line | Role | Condition | Fields read |
| --- | --- | --- | --- |
| 25 | title | `if (i_exist .or. "recall_db.rec" /= "null") then > do` | `titldum` |
| 27 | header | `if (i_exist .or. "recall_db.rec" /= "null") then > do` | `header` |
| 31 | data | `if (i_exist .or. "recall_db.rec" /= "null") then > do > do while (eof == 0)` | `i` |
| 45 | title | `if (i_exist .or. "recall_db.rec" /= "null") then > do` | `titldum` |
| 47 | header | `if (i_exist .or. "recall_db.rec" /= "null") then > do` | `header` |
| 51 | data | `if (i_exist .or. "recall_db.rec" /= "null") then > do > do ii = 1, imax` | `i` |
| 54 | data | `if (i_exist .or. "recall_db.rec" /= "null") then > do > do ii = 1, imax` | `k`, `recall_db(i)%name`, `recall_db(i)%org_min`, `recall_db(i)%pest`, `recall_db(i)%path`, `recall_db(i)%hmet`, `recall_db(i)%salt`, `recall_db(i)%constit` |


#### Candidate read structure

- Schema status: `certified`
- Review needed: no
- Source expression(s): `recall_db.rec`

- Procedure: `recalldb_read`
- Reader: `recall_read.f90`
- Match: source_input
- Resolved default filename(s): `recall_db.rec`
- Source filename expression(s): `recall_db.rec`
- Open: line 24, file expression `"recall_db.rec"`, parser value `recall_db.rec`, condition `if (i_exist .or. "recall_db.rec" /= "null") then > do`

| Line | Role | Condition | Fields read |
| --- | --- | --- | --- |
| 25 | title | `if (i_exist .or. "recall_db.rec" /= "null") then > do` | `titldum` |
| 27 | header | `if (i_exist .or. "recall_db.rec" /= "null") then > do` | `header` |
| 31 | data | `if (i_exist .or. "recall_db.rec" /= "null") then > do > do while (eof == 0)` | `i` |
| 40 | title | `if (i_exist .or. "recall_db.rec" /= "null") then > do` | `titldum` |
| 42 | header | `if (i_exist .or. "recall_db.rec" /= "null") then > do` | `header` |
| 46 | data | `if (i_exist .or. "recall_db.rec" /= "null") then > do > do ii = 1, imax` | `i` |
| 49 | data | `if (i_exist .or. "recall_db.rec" /= "null") then > do > do ii = 1, imax` | `k`, `recall_db(i)%name`, `recall_db(i)%org_min`, `recall_db(i)%pest`, `recall_db(i)%path`, `recall_db(i)%hmet`, `recall_db(i)%salt`, `recall_db(i)%constit`, `recall_db(i)%descrip` |

### `salt_fertilizer.frt`

- Review needed: yes
- Reader procedures changed: no
- Read-block count changed: no
- Read conditions changed: yes
- Base flattened read order: `titldum`, `header`, `fert_salt(isalti)`
- Candidate flattened read order: `titldum`, `header`, `fert_salt(isalti)`

#### Read-order edits

_No field-order edits; the contract changed in structure or conditions._

#### Base read structure

- Schema status: `certified`
- Review needed: no
- Source expression(s): `salt_fertilizer.frt`

- Procedure: `salt_fert_read`
- Reader: `salt_fert_read.f90`
- Match: source_input
- Resolved default filename(s): `salt_fertilizer.frt`
- Source filename expression(s): `salt_fertilizer.frt`
- Open: line 24, file expression `"salt_fertilizer.frt"`, parser value `salt_fertilizer.frt`, condition `if (i_exist) then`

| Line | Role | Condition | Fields read |
| --- | --- | --- | --- |
| 25 | title | `if (i_exist) then` | `titldum` |
| 26 | header | `if (i_exist) then` | `header` |
| 36 | data | `if (i_exist) then > do isalti=1,db_mx%fertparm` | `fert_salt(isalti)` |


#### Candidate read structure

- Schema status: `certified`
- Review needed: no
- Source expression(s): `salt_fertilizer.frt`

- Procedure: `salt_fert_read`
- Reader: `salt_fert_read.f90`
- Match: source_input
- Resolved default filename(s): `salt_fertilizer.frt`
- Source filename expression(s): `salt_fertilizer.frt`
- Open: line 24, file expression `"salt_fertilizer.frt"`, parser value `salt_fertilizer.frt`, condition `if (i_exist) then`

| Line | Role | Condition | Fields read |
| --- | --- | --- | --- |
| 25 | title | `if (i_exist) then` | `titldum` |
| 26 | header | `if (i_exist) then` | `header` |
| 36 | data | `if (i_exist) then > do isalti = 1, db_mx%fertparm` | `fert_salt(isalti)` |

### `water_canal.wal`

- Review needed: yes
- Reader procedures changed: no
- Read-block count changed: no
- Read conditions changed: yes
- Base flattened read order: `titldum`, `imax`, `header`, `i`, `canal(ic)%name`, `canal(ic)%w_sta`, `canal(ic)%init`, `canal(ic)%dtbl`, `canal(ic)%ddown_days`, `canal(ic)%w`, `canal(ic)%d`, `canal(ic)%s`, `canal(ic)%ss`, `canal(ic)%sat_con`, `canal(ic)%loss_fr`, `canal(ic)%bed_thick`, `canal(ic)%div_id`, `canal(ic)%day_beg`, `canal(ic)%day_end`, `num_aqu`, `i`, `canal(ic)%name`, `canal(ic)%w_sta`, `canal(ic)%init`, `canal(ic)%dtbl`, `canal(ic)%ddown_days`, `canal(ic)%w`, `canal(ic)%d`, `canal(ic)%s`, `canal(ic)%ss`, `canal(ic)%sat_con`, `canal(ic)%loss_fr`, `canal(ic)%bed_thick`, `canal(ic)%div_id`, `canal(ic)%day_beg`, `canal(ic)%day_end`, `canal(ic)%num_aqu`, `(canal(ic)%aqu_loss(iaq), iaq = 1, num_aqu)`
- Candidate flattened read order: `titldum`, `imax`, `header`, `i`, `canal(ic)%name`, `canal(ic)%w_sta`, `canal(ic)%init`, `canal(ic)%dtbl`, `canal(ic)%ddown_days`, `canal(ic)%w`, `canal(ic)%d`, `canal(ic)%l`, `canal(ic)%s`, `canal(ic)%ss`, `canal(ic)%sat_con`, `canal(ic)%evap_co`, `num_aqu`, `i`, `canal(ic)%name`, `canal(ic)%w_sta`, `canal(ic)%init`, `canal(ic)%dtbl`, `canal(ic)%ddown_days`, `canal(ic)%w`, `canal(ic)%d`, `canal(ic)%l`, `canal(ic)%s`, `canal(ic)%ss`, `canal(ic)%sat_con`, `canal(ic)%evap_co`, `canal(ic)%num_aqu`, `(canal(ic)%aqu_loss_fr(iaq), iaq = 1, num_aqu)`

#### Read-order edits

- `insert` at base index 11 / candidate index 11: removed _no fields captured_; added `canal(ic)%l`
- `replace` at base index 14 / candidate index 15: removed `canal(ic)%loss_fr`, `canal(ic)%bed_thick`, `canal(ic)%div_id`, `canal(ic)%day_beg`, `canal(ic)%day_end`; added `canal(ic)%evap_co`
- `insert` at base index 28 / candidate index 25: removed _no fields captured_; added `canal(ic)%l`
- `replace` at base index 31 / candidate index 29: removed `canal(ic)%loss_fr`, `canal(ic)%bed_thick`, `canal(ic)%div_id`, `canal(ic)%day_beg`, `canal(ic)%day_end`; added `canal(ic)%evap_co`
- `replace` at base index 37 / candidate index 31: removed `(canal(ic)%aqu_loss(iaq), iaq = 1, num_aqu)`; added `(canal(ic)%aqu_loss_fr(iaq), iaq = 1, num_aqu)`

#### Base read structure

- Schema status: `certified`
- Review needed: no
- Source expression(s): `water_canal.wal`

- Procedure: `water_canal_read`
- Reader: `water_canal_read.f90`
- Match: source_input
- Resolved default filename(s): `water_canal.wal`
- Source filename expression(s): `water_canal.wal`
- Open: line 32, file expression `'water_canal.wal'`, parser value `water_canal.wal`, condition `if (.not. i_exist .or. 'water_canal.wal' == "null") then / else > do`

| Line | Role | Condition | Fields read |
| --- | --- | --- | --- |
| 33 | title | `if (.not. i_exist .or. 'water_canal.wal' == "null") then / else > do` | `titldum` |
| 35 | count | `if (.not. i_exist .or. 'water_canal.wal' == "null") then / else > do` | `imax` |
| 36 | header | `if (.not. i_exist .or. 'water_canal.wal' == "null") then / else > do` | `header` |
| 46 | data | `if (.not. i_exist .or. 'water_canal.wal' == "null") then / else > do > do ic = 1, imax` | `i`, `canal(ic)%name`, `canal(ic)%w_sta`, `canal(ic)%init`, `canal(ic)%dtbl`, `canal(ic)%ddown_days`, `canal(ic)%w`, `canal(ic)%d`, `canal(ic)%s`, `canal(ic)%ss`, `canal(ic)%sat_con`, `canal(ic)%loss_fr`, `canal(ic)%bed_thick`, `canal(ic)%div_id`, `canal(ic)%day_beg`, `canal(ic)%day_end`, `num_aqu` |
| 56 | data | `if (.not. i_exist .or. 'water_canal.wal' == "null") then / else > do > do ic = 1, imax` | `i`, `canal(ic)%name`, `canal(ic)%w_sta`, `canal(ic)%init`, `canal(ic)%dtbl`, `canal(ic)%ddown_days`, `canal(ic)%w`, `canal(ic)%d`, `canal(ic)%s`, `canal(ic)%ss`, `canal(ic)%sat_con`, `canal(ic)%loss_fr`, `canal(ic)%bed_thick`, `canal(ic)%div_id`, `canal(ic)%day_beg`, `canal(ic)%day_end`, `canal(ic)%num_aqu`, `(canal(ic)%aqu_loss(iaq), iaq = 1, num_aqu)` |


#### Candidate read structure

- Schema status: `certified`
- Review needed: no
- Source expression(s): `water_canal.wal`

- Procedure: `water_canal_read`
- Reader: `water_canal_read.f90`
- Match: source_input
- Resolved default filename(s): `water_canal.wal`
- Source filename expression(s): `water_canal.wal`
- Open: line 30, file expression `'water_canal.wal'`, parser value `water_canal.wal`, condition `if (i_exist) then > do`

| Line | Role | Condition | Fields read |
| --- | --- | --- | --- |
| 31 | title | `if (i_exist) then > do` | `titldum` |
| 33 | count | `if (i_exist) then > do` | `imax` |
| 34 | header | `if (i_exist) then > do` | `header` |
| 44 | data | `if (i_exist) then > do > do ic = 1, imax` | `i`, `canal(ic)%name`, `canal(ic)%w_sta`, `canal(ic)%init`, `canal(ic)%dtbl`, `canal(ic)%ddown_days`, `canal(ic)%w`, `canal(ic)%d`, `canal(ic)%l`, `canal(ic)%s`, `canal(ic)%ss`, `canal(ic)%sat_con`, `canal(ic)%evap_co`, `num_aqu` |
| 53 | data | `if (i_exist) then > do > do ic = 1, imax` | `i`, `canal(ic)%name`, `canal(ic)%w_sta`, `canal(ic)%init`, `canal(ic)%dtbl`, `canal(ic)%ddown_days`, `canal(ic)%w`, `canal(ic)%d`, `canal(ic)%l`, `canal(ic)%s`, `canal(ic)%ss`, `canal(ic)%sat_con`, `canal(ic)%evap_co`, `canal(ic)%num_aqu`, `(canal(ic)%aqu_loss_fr(iaq), iaq = 1, num_aqu)` |

### `water_pipe.wal`

- Review needed: yes
- Reader procedures changed: no
- Read-block count changed: no
- Read conditions changed: no
- Base flattened read order: `titldum`, `imax`, `header`, `header`, `i`, `pipe(ipipe)%name`, `pipe(ipipe)%stor_mx`, `pipe(ipipe)%ddown_days`, `pipe(ipipe)%loss_fr`, `num_aqu`, `i`, `pipe(ipipe)%name`, `pipe(ipipe)%stor_mx`, `pipe(ipipe)%ddown_days`, `pipe(ipipe)%loss_fr`, `pipe(ipipe)%num_aqu`, `(pipe(ipipe)%aqu_loss(iaq), iaq = 1, num_aqu)`
- Candidate flattened read order: `titldum`, `imax`, `header`, `header`, `i`, `pipe(ipipe)%name`, `pipe(ipipe)%stor_mx`, `pipe(ipipe)%ddown_days`, `pipe(ipipe)%loss_fr`, `num_aqu`, `i`, `pipe(ipipe)%name`, `pipe(ipipe)%stor_mx`, `pipe(ipipe)%ddown_days`, `pipe(ipipe)%loss_fr`, `pipe(ipipe)%num_aqu`, `(pipe(ipipe)%aqu_loss_fr(iaq), iaq = 1, num_aqu)`

#### Read-order edits

- `replace` at base index 16 / candidate index 16: removed `(pipe(ipipe)%aqu_loss(iaq), iaq = 1, num_aqu)`; added `(pipe(ipipe)%aqu_loss_fr(iaq), iaq = 1, num_aqu)`

#### Base read structure

- Schema status: `certified`
- Review needed: no
- Source expression(s): `water_pipe.wal`

- Procedure: `water_pipe_read`
- Reader: `water_pipe_read.f90`
- Match: source_input
- Resolved default filename(s): `water_pipe.wal`
- Source filename expression(s): `water_pipe.wal`
- Open: line 32, file expression `'water_pipe.wal'`, parser value `water_pipe.wal`, condition `if (.not. i_exist .or. 'water_pipe.wal' == "null") then / else > do`

| Line | Role | Condition | Fields read |
| --- | --- | --- | --- |
| 33 | title | `if (.not. i_exist .or. 'water_pipe.wal' == "null") then / else > do` | `titldum` |
| 35 | count | `if (.not. i_exist .or. 'water_pipe.wal' == "null") then / else > do` | `imax` |
| 36 | header | `if (.not. i_exist .or. 'water_pipe.wal' == "null") then / else > do` | `header` |
| 43 | header | `if (.not. i_exist .or. 'water_pipe.wal' == "null") then / else > do > do ipipe = 1, imax` | `header` |
| 45 | data | `if (.not. i_exist .or. 'water_pipe.wal' == "null") then / else > do > do ipipe = 1, imax` | `i`, `pipe(ipipe)%name`, `pipe(ipipe)%stor_mx`, `pipe(ipipe)%ddown_days`, `pipe(ipipe)%loss_fr`, `num_aqu` |
| 52 | data | `if (.not. i_exist .or. 'water_pipe.wal' == "null") then / else > do > do ipipe = 1, imax` | `i`, `pipe(ipipe)%name`, `pipe(ipipe)%stor_mx`, `pipe(ipipe)%ddown_days`, `pipe(ipipe)%loss_fr`, `pipe(ipipe)%num_aqu`, `(pipe(ipipe)%aqu_loss(iaq), iaq = 1, num_aqu)` |


#### Candidate read structure

- Schema status: `certified`
- Review needed: no
- Source expression(s): `water_pipe.wal`

- Procedure: `water_pipe_read`
- Reader: `water_pipe_read.f90`
- Match: source_input
- Resolved default filename(s): `water_pipe.wal`
- Source filename expression(s): `water_pipe.wal`
- Open: line 32, file expression `'water_pipe.wal'`, parser value `water_pipe.wal`, condition `if (.not. i_exist .or. 'water_pipe.wal' == "null") then / else > do`

| Line | Role | Condition | Fields read |
| --- | --- | --- | --- |
| 33 | title | `if (.not. i_exist .or. 'water_pipe.wal' == "null") then / else > do` | `titldum` |
| 35 | count | `if (.not. i_exist .or. 'water_pipe.wal' == "null") then / else > do` | `imax` |
| 36 | header | `if (.not. i_exist .or. 'water_pipe.wal' == "null") then / else > do` | `header` |
| 43 | header | `if (.not. i_exist .or. 'water_pipe.wal' == "null") then / else > do > do ipipe = 1, imax` | `header` |
| 45 | data | `if (.not. i_exist .or. 'water_pipe.wal' == "null") then / else > do > do ipipe = 1, imax` | `i`, `pipe(ipipe)%name`, `pipe(ipipe)%stor_mx`, `pipe(ipipe)%ddown_days`, `pipe(ipipe)%loss_fr`, `num_aqu` |
| 52 | data | `if (.not. i_exist .or. 'water_pipe.wal' == "null") then / else > do > do ipipe = 1, imax` | `i`, `pipe(ipipe)%name`, `pipe(ipipe)%stor_mx`, `pipe(ipipe)%ddown_days`, `pipe(ipipe)%loss_fr`, `pipe(ipipe)%num_aqu`, `(pipe(ipipe)%aqu_loss_fr(iaq), iaq = 1, num_aqu)` |

### `water_tower.wal`

- Review needed: yes
- Reader procedures changed: no
- Read-block count changed: no
- Read conditions changed: yes
- Base flattened read order: `titldum`, `imax`, `header`, `header`, `i`, `wtow(iwtow)%name`, `wtow(iwtow)%stor_mx`, `wtow(iwtow)%ddown_days`, `wtow(iwtow)%loss_fr`
- Candidate flattened read order: `titldum`, `imax`, `header`, `i`, `wtow(iwtow)%name`, `wtow(iwtow)%stor_mx`, `wtow(iwtow)%ddown_days`, `wtow(iwtow)%loss_fr`

#### Read-order edits

- `delete` at base index 2 / candidate index 2: removed `header`; added _no fields captured_

#### Base read structure

- Schema status: `certified`
- Review needed: no
- Source expression(s): `water_tower.wal`

- Procedure: `water_tower_read`
- Reader: `water_tower_read.f90`
- Match: source_input
- Resolved default filename(s): `water_tower.wal`
- Source filename expression(s): `water_tower.wal`
- Open: line 32, file expression `'water_tower.wal'`, parser value `water_tower.wal`, condition `if (.not. i_exist .or. 'water_tower.wal' == "null") then / else > do`

| Line | Role | Condition | Fields read |
| --- | --- | --- | --- |
| 33 | title | `if (.not. i_exist .or. 'water_tower.wal' == "null") then / else > do` | `titldum` |
| 35 | count | `if (.not. i_exist .or. 'water_tower.wal' == "null") then / else > do` | `imax` |
| 36 | header | `if (.not. i_exist .or. 'water_tower.wal' == "null") then / else > do` | `header` |
| 46 | header | `if (.not. i_exist .or. 'water_tower.wal' == "null") then / else > do > do iwtow = 1, imax` | `header` |
| 48 | data | `if (.not. i_exist .or. 'water_tower.wal' == "null") then / else > do > do iwtow = 1, imax` | `i`, `wtow(iwtow)%name`, `wtow(iwtow)%stor_mx`, `wtow(iwtow)%ddown_days`, `wtow(iwtow)%loss_fr` |


#### Candidate read structure

- Schema status: `certified`
- Review needed: no
- Source expression(s): `water_tower.wal`

- Procedure: `water_tower_read`
- Reader: `water_tower_read.f90`
- Match: source_input
- Resolved default filename(s): `water_tower.wal`
- Source filename expression(s): `water_tower.wal`
- Open: line 28, file expression `'water_tower.wal'`, parser value `water_tower.wal`, condition `if (i_exist) then > do`

| Line | Role | Condition | Fields read |
| --- | --- | --- | --- |
| 29 | title | `if (i_exist) then > do` | `titldum` |
| 31 | count | `if (i_exist) then > do` | `imax` |
| 32 | header | `if (i_exist) then > do` | `header` |
| 42 | data | `if (i_exist) then > do > do iwtow = 1, imax` | `i`, `wtow(iwtow)%name`, `wtow(iwtow)%stor_mx`, `wtow(iwtow)%ddown_days`, `wtow(iwtow)%loss_fr` |

### `water_treat.wal`

- Review needed: yes
- Reader procedures changed: no
- Read-block count changed: no
- Read conditions changed: yes
- Base flattened read order: `titldum`, `imax`, `header`, `i`, `wtp(iwtp)%name`, `wtp(iwtp)%stor_mx`, `wtp(iwtp)%lag_days`, `wtp(iwtp)%loss_fr`, `wtp(iwtp)%org_min`, `wtp(iwtp)%pests`, `wtp(iwtp)%paths`, `wtp(iwtp)%salts`, `wtp(iwtp)%constit`, `wtp(iwtp)%descrip`, `header`, `wtp_cs_treat(iwtp)%pest`, `header`, `wtp_cs_treat(iwtp)%path`
- Candidate flattened read order: `titldum`, `imax`, `header`, `wtp(iwtp)%name`, `wtp(iwtp)%stor_mx`, `wtp(iwtp)%lag_days`, `wtp(iwtp)%loss_fr`, `wtp(iwtp)%num_treats`, `wtp(iwtp)%conc(itrt)%org_min_typ`, `wtp(iwtp)%conc(itrt)%org_min_name`, `wtp(iwtp)%conc(itrt)%pests_typ`, `wtp(iwtp)%conc(itrt)%pests_name`, `wtp(iwtp)%conc(itrt)%paths_typ`, `wtp(iwtp)%conc(itrt)%paths_name`, `wtp(iwtp)%conc(itrt)%salts_typ`, `wtp(iwtp)%conc(itrt)%salts_name`, `wtp(iwtp)%conc(itrt)%constit_typ`, `wtp(iwtp)%conc(itrt)%constit_name`, `wtp(iwtp)%descrip`, `header`, `wtp_cs_treat(iwtp)%pest`, `header`, `wtp_cs_treat(iwtp)%path`

#### Read-order edits

- `delete` at base index 3 / candidate index 3: removed `i`; added _no fields captured_
- `replace` at base index 8 / candidate index 7: removed `wtp(iwtp)%org_min`, `wtp(iwtp)%pests`, `wtp(iwtp)%paths`, `wtp(iwtp)%salts`, `wtp(iwtp)%constit`; added `wtp(iwtp)%num_treats`, `wtp(iwtp)%conc(itrt)%org_min_typ`, `wtp(iwtp)%conc(itrt)%org_min_name`, `wtp(iwtp)%conc(itrt)%pests_typ`, `wtp(iwtp)%conc(itrt)%pests_name`, `wtp(iwtp)%conc(itrt)%paths_typ`, `wtp(iwtp)%conc(itrt)%paths_name`, `wtp(iwtp)%conc(itrt)%salts_typ`, `wtp(iwtp)%conc(itrt)%salts_name`, `wtp(iwtp)%conc(itrt)%constit_typ`, `wtp(iwtp)%conc(itrt)%constit_name`

#### Base read structure

- Schema status: `certified`
- Review needed: no
- Source expression(s): `water_treat.wal`

- Procedure: `water_treatment_read`
- Reader: `water_treatment_read.f90`
- Match: source_input
- Resolved default filename(s): `water_treat.wal`
- Source filename expression(s): `water_treat.wal`
- Open: line 31, file expression `'water_treat.wal'`, parser value `water_treat.wal`, condition `if (.not. i_exist .or. 'water_treat.wal' == "null") then / else > do`

| Line | Role | Condition | Fields read |
| --- | --- | --- | --- |
| 32 | title | `if (.not. i_exist .or. 'water_treat.wal' == "null") then / else > do` | `titldum` |
| 34 | count | `if (.not. i_exist .or. 'water_treat.wal' == "null") then / else > do` | `imax` |
| 35 | header | `if (.not. i_exist .or. 'water_treat.wal' == "null") then / else > do` | `header` |
| 49 | data | `if (.not. i_exist .or. 'water_treat.wal' == "null") then / else > do > do iwtp = 1, imax` | `i`, `wtp(iwtp)%name`, `wtp(iwtp)%stor_mx`, `wtp(iwtp)%lag_days`, `wtp(iwtp)%loss_fr`, `wtp(iwtp)%org_min`, `wtp(iwtp)%pests`, `wtp(iwtp)%paths`, `wtp(iwtp)%salts`, `wtp(iwtp)%constit`, `wtp(iwtp)%descrip` |
| 67 | header | `if (.not. i_exist .or. 'water_treat.wal' == "null") then / else > do > do iwtp = 1, imax > if (cs_db%num_pests > 0) then` | `header` |
| 68 | data | `if (.not. i_exist .or. 'water_treat.wal' == "null") then / else > do > do iwtp = 1, imax > if (cs_db%num_pests > 0) then` | `wtp_cs_treat(iwtp)%pest` |
| 74 | header | `if (.not. i_exist .or. 'water_treat.wal' == "null") then / else > do > do iwtp = 1, imax > if (cs_db%num_paths > 0) then` | `header` |
| 75 | data | `if (.not. i_exist .or. 'water_treat.wal' == "null") then / else > do > do iwtp = 1, imax > if (cs_db%num_paths > 0) then` | `wtp_cs_treat(iwtp)%path` |


#### Candidate read structure

- Schema status: `schema_unresolved_but_readable`
- Review needed: yes
- Source expression(s): `water_treat.wal`

- Procedure: `water_treatment_read`
- Reader: `water_treatment_read.f90`
- Match: source_input
- Resolved default filename(s): `water_treat.wal`
- Source filename expression(s): `water_treat.wal`
- Open: line 34, file expression `'water_treat.wal'`, parser value `water_treat.wal`, condition `if (.not. i_exist .or. 'water_treat.wal' == "null") then / else > do`

| Line | Role | Condition | Fields read |
| --- | --- | --- | --- |
| 35 | title | `if (.not. i_exist .or. 'water_treat.wal' == "null") then / else > do` | `titldum` |
| 37 | count | `if (.not. i_exist .or. 'water_treat.wal' == "null") then / else > do` | `imax` |
| 38 | header | `if (.not. i_exist .or. 'water_treat.wal' == "null") then / else > do` | `header` |
| 45 | data | `if (.not. i_exist .or. 'water_treat.wal' == "null") then / else > do > do iwtp = 1, imax` | `wtp(iwtp)%name`, `wtp(iwtp)%stor_mx`, `wtp(iwtp)%lag_days`, `wtp(iwtp)%loss_fr`, `wtp(iwtp)%num_treats` |
| 51 | data | `if (.not. i_exist .or. 'water_treat.wal' == "null") then / else > do > do iwtp = 1, imax > do itrt = 1, wtp(iwtp)%num_treats` | `wtp(iwtp)%conc(itrt)%org_min_typ`, `wtp(iwtp)%conc(itrt)%org_min_name`, `wtp(iwtp)%conc(itrt)%pests_typ`, `wtp(iwtp)%conc(itrt)%pests_name`, `wtp(iwtp)%conc(itrt)%paths_typ`, `wtp(iwtp)%conc(itrt)%paths_name`, `wtp(iwtp)%conc(itrt)%salts_typ`, `wtp(iwtp)%conc(itrt)%salts_name`, `wtp(iwtp)%conc(itrt)%constit_typ`, `wtp(iwtp)%conc(itrt)%constit_name`, `wtp(iwtp)%descrip` |
| 104 | header | `if (.not. i_exist .or. 'water_treat.wal' == "null") then / else > do > do iwtp = 1, imax > do itrt = 1, wtp(iwtp)%num_treats > if (cs_db%num_pests > 0) then` | `header` |
| 105 | data | `if (.not. i_exist .or. 'water_treat.wal' == "null") then / else > do > do iwtp = 1, imax > do itrt = 1, wtp(iwtp)%num_treats > if (cs_db%num_pests > 0) then` | `wtp_cs_treat(iwtp)%pest` |
| 111 | header | `if (.not. i_exist .or. 'water_treat.wal' == "null") then / else > do > do iwtp = 1, imax > do itrt = 1, wtp(iwtp)%num_treats > if (cs_db%num_paths > 0) then` | `header` |
| 112 | data | `if (.not. i_exist .or. 'water_treat.wal' == "null") then / else > do > do iwtp = 1, imax > do itrt = 1, wtp(iwtp)%num_treats > if (cs_db%num_paths > 0) then` | `wtp_cs_treat(iwtp)%path` |

### `water_use.wal`

- Review needed: yes
- Reader procedures changed: no
- Read-block count changed: no
- Read conditions changed: no
- Base flattened read order: `titldum`, `imax`, `header`, `i`, `wuse(iwuse)%name`, `wuse(iwuse)%stor_mx`, `wuse(iwuse)%lag_days`, `wuse(iwuse)%loss_fr`, `wuse(iwuse)%org_min`, `wuse(iwuse)%pests`, `wuse(iwuse)%paths`, `wuse(iwuse)%salts`, `wuse(iwuse)%constit`, `wuse(iwuse)%descrip`, `header`, `wuse_cs_efflu(iwuse)%pest`, `header`, `wuse_cs_efflu(iwuse)%path`
- Candidate flattened read order: `titldum`, `imax`, `header`, `wuse(iwuse)%name`, `wuse(iwuse)%stor_mx`, `wuse(iwuse)%lag_days`, `wuse(iwuse)%loss_fr`, `wuse(iwuse)%conc(lev)%org_min_typ`, `wuse(iwuse)%conc(lev)%org_min_name`, `wuse(iwuse)%conc(lev)%pests_typ`, `wuse(iwuse)%conc(lev)%pests_name`, `wuse(iwuse)%conc(lev)%paths_typ`, `wuse(iwuse)%conc(lev)%paths_name`, `wuse(iwuse)%conc(lev)%salts_typ`, `wuse(iwuse)%conc(lev)%salts_name`, `wuse(iwuse)%conc(lev)%constit_typ`, `wuse(iwuse)%conc(lev)%constit_name`, `wuse(iwuse)%descrip`, `header`, `wuse_cs_efflu(iwuse)%pest`, `header`, `wuse_cs_efflu(iwuse)%path`

#### Read-order edits

- `delete` at base index 3 / candidate index 3: removed `i`; added _no fields captured_
- `replace` at base index 8 / candidate index 7: removed `wuse(iwuse)%org_min`, `wuse(iwuse)%pests`, `wuse(iwuse)%paths`, `wuse(iwuse)%salts`, `wuse(iwuse)%constit`; added `wuse(iwuse)%conc(lev)%org_min_typ`, `wuse(iwuse)%conc(lev)%org_min_name`, `wuse(iwuse)%conc(lev)%pests_typ`, `wuse(iwuse)%conc(lev)%pests_name`, `wuse(iwuse)%conc(lev)%paths_typ`, `wuse(iwuse)%conc(lev)%paths_name`, `wuse(iwuse)%conc(lev)%salts_typ`, `wuse(iwuse)%conc(lev)%salts_name`, `wuse(iwuse)%conc(lev)%constit_typ`, `wuse(iwuse)%conc(lev)%constit_name`

#### Base read structure

- Schema status: `certified`
- Review needed: no
- Source expression(s): `water_use.wal`

- Procedure: `water_use_read`
- Reader: `water_use_read.f90`
- Match: source_input
- Resolved default filename(s): `water_use.wal`
- Source filename expression(s): `water_use.wal`
- Open: line 32, file expression `'water_use.wal'`, parser value `water_use.wal`, condition `if (.not. i_exist .or. 'water_use.wal' == "null") then / else > do`

| Line | Role | Condition | Fields read |
| --- | --- | --- | --- |
| 33 | title | `if (.not. i_exist .or. 'water_use.wal' == "null") then / else > do` | `titldum` |
| 35 | count | `if (.not. i_exist .or. 'water_use.wal' == "null") then / else > do` | `imax` |
| 36 | header | `if (.not. i_exist .or. 'water_use.wal' == "null") then / else > do` | `header` |
| 50 | data | `if (.not. i_exist .or. 'water_use.wal' == "null") then / else > do > do iwuse = 1, imax` | `i`, `wuse(iwuse)%name`, `wuse(iwuse)%stor_mx`, `wuse(iwuse)%lag_days`, `wuse(iwuse)%loss_fr`, `wuse(iwuse)%org_min`, `wuse(iwuse)%pests`, `wuse(iwuse)%paths`, `wuse(iwuse)%salts`, `wuse(iwuse)%constit`, `wuse(iwuse)%descrip` |
| 68 | header | `if (.not. i_exist .or. 'water_use.wal' == "null") then / else > do > do iwuse = 1, imax > if (cs_db%num_pests > 0) then` | `header` |
| 69 | data | `if (.not. i_exist .or. 'water_use.wal' == "null") then / else > do > do iwuse = 1, imax > if (cs_db%num_pests > 0) then` | `wuse_cs_efflu(iwuse)%pest` |
| 75 | header | `if (.not. i_exist .or. 'water_use.wal' == "null") then / else > do > do iwuse = 1, imax > if (cs_db%num_paths > 0) then` | `header` |
| 76 | data | `if (.not. i_exist .or. 'water_use.wal' == "null") then / else > do > do iwuse = 1, imax > if (cs_db%num_paths > 0) then` | `wuse_cs_efflu(iwuse)%path` |


#### Candidate read structure

- Schema status: `schema_unresolved_but_readable`
- Review needed: yes
- Source expression(s): `water_use.wal`

- Procedure: `water_use_read`
- Reader: `water_use_read.f90`
- Match: source_input
- Resolved default filename(s): `water_use.wal`
- Source filename expression(s): `water_use.wal`
- Open: line 35, file expression `'water_use.wal'`, parser value `water_use.wal`, condition `if (.not. i_exist .or. 'water_use.wal' == "null") then / else > do`

| Line | Role | Condition | Fields read |
| --- | --- | --- | --- |
| 36 | title | `if (.not. i_exist .or. 'water_use.wal' == "null") then / else > do` | `titldum` |
| 38 | count | `if (.not. i_exist .or. 'water_use.wal' == "null") then / else > do` | `imax` |
| 39 | header | `if (.not. i_exist .or. 'water_use.wal' == "null") then / else > do` | `header` |
| 48 | data | `if (.not. i_exist .or. 'water_use.wal' == "null") then / else > do > do iwuse = 1, imax` | `wuse(iwuse)%name`, `wuse(iwuse)%stor_mx`, `wuse(iwuse)%lag_days`, `wuse(iwuse)%loss_fr`, `wuse(iwuse)%conc(lev)%org_min_typ`, `wuse(iwuse)%conc(lev)%org_min_name`, `wuse(iwuse)%conc(lev)%pests_typ`, `wuse(iwuse)%conc(lev)%pests_name`, `wuse(iwuse)%conc(lev)%paths_typ`, `wuse(iwuse)%conc(lev)%paths_name`, `wuse(iwuse)%conc(lev)%salts_typ`, `wuse(iwuse)%conc(lev)%salts_name`, `wuse(iwuse)%conc(lev)%constit_typ`, `wuse(iwuse)%conc(lev)%constit_name`, `wuse(iwuse)%descrip` |
| 90 | header | `if (.not. i_exist .or. 'water_use.wal' == "null") then / else > do > do iwuse = 1, imax > if (cs_db%num_pests > 0) then` | `header` |
| 91 | data | `if (.not. i_exist .or. 'water_use.wal' == "null") then / else > do > do iwuse = 1, imax > if (cs_db%num_pests > 0) then` | `wuse_cs_efflu(iwuse)%pest` |
| 97 | header | `if (.not. i_exist .or. 'water_use.wal' == "null") then / else > do > do iwuse = 1, imax > if (cs_db%num_paths > 0) then` | `header` |
| 98 | data | `if (.not. i_exist .or. 'water_use.wal' == "null") then / else > do > do iwuse = 1, imax > if (cs_db%num_paths > 0) then` | `wuse_cs_efflu(iwuse)%path` |


## Possible renames or replacements

- `out_src.wal` -> `outside_src.wal`: same reader procedure: water_osrc_read; same file extension; similar read-field order. **Human review required; this is not asserted as a rename.**
- `transplant.plt` -> `transplant.ops`: same reader procedure: plant_transplant_read; similar read-field order. **Human review required; this is not asserted as a rename.**
- `water_allocation.wro` -> `place_of_use.wro`: same reader procedure: water_allocation_read; same file extension. **Human review required; this is not asserted as a rename.**
- `water_allocation.wro` -> `point_of_diver.wro`: same reader procedure: water_allocation_read; same file extension. **Human review required; this is not asserted as a rename.**

## Unresolved opened input filenames

The candidate contains 27 unresolved runtime filename expression(s); 1 were introduced by this comparison. Only newly introduced expressions are expanded below.
### `recall_read` at `recall_read.f90`

- Reason: opened input filename could not be resolved
- Expression(s): `recall(i)%filename`
- Procedure: `recall_read`
- Reader: `recall_read.f90`
- Match: source_input
- Source filename expression(s): `recall(i)%filename`
- Open: line 152, file expression `recall(i)%filename`, parser value `recall(i)%filename`, condition `if (i_exist .or. "recall.rec" /= "null") then > do > do ii = 1, imax > if (recall(i)%typ /= 4) then`

| Line | Role | Condition | Fields read |
| --- | --- | --- | --- |
| 153 | title | `if (i_exist .or. "recall.rec" /= "null") then > do > do ii = 1, imax > if (recall(i)%typ /= 4) then` | `titldum` |
| 155 | count | `if (i_exist .or. "recall.rec" /= "null") then > do > do ii = 1, imax > if (recall(i)%typ /= 4) then` | `nbyr` |
| 157 | header | `if (i_exist .or. "recall.rec" /= "null") then > do > do ii = 1, imax > if (recall(i)%typ /= 4) then` | `header` |
| 177 | data | `if (i_exist .or. "recall.rec" /= "null") then > do > do ii = 1, imax > if (recall(i)%typ /= 4) then` | `jday`, `mo`, `day_mo`, `iyr` |
| 185 | data | `if (i_exist .or. "recall.rec" /= "null") then > do > do ii = 1, imax > if (recall(i)%typ /= 4) then > if (recall(i)%start_yr <= time%yrc) then > do` | `jday`, `mo`, `day_mo`, `iyr` |
| 199 | data | `if (i_exist .or. "recall.rec" /= "null") then > do > do ii = 1, imax > if (recall(i)%typ /= 4) then > do` | `jday1`, `mo1`, `day_mo`, `iyr` |
| 227 | data | `if (i_exist .or. "recall.rec" /= "null") then > do > do ii = 1, imax > if (recall(i)%typ /= 4) then > do > select case (recall(i)%typ) / case (1)` | `jday`, `mo`, `day_mo`, `iyr`, `ob_typ`, `ob_name`, `recall(i)%hd(jday1,iyrs)` |
| 230 | data | `if (i_exist .or. "recall.rec" /= "null") then > do > do ii = 1, imax > if (recall(i)%typ /= 4) then > do > select case (recall(i)%typ) / case (2)` | `jday`, `mo`, `day_mo`, `iyr`, `ob_typ`, `ob_name`, `recall(i)%hd(mo1,iyrs)` |
| 235 | data | `if (i_exist .or. "recall.rec" /= "null") then > do > do ii = 1, imax > if (recall(i)%typ /= 4) then > do > select case (recall(i)%typ) / case (3)` | `jday`, `mo`, `day_mo`, `iyr`, `ob_typ`, `ob_name`, `ht1` |
