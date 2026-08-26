# Source Read Evidence for Schema Review

This report is generated when a comparison has schema entries that changed, disappeared from resolved schemas, or became newly unresolved. It does not certify a final schema. It shows the Fortran read evidence that a human or extractor update should review.

## `flo_con.dtl`

- Schema diff status: `['decision_tables.changed']`
- Review needed: no
- Base schema presence: `{'resolved_sections': ['decision_tables'], 'unresolved_sections': []}`
- Candidate schema presence: `{'resolved_sections': ['decision_tables'], 'unresolved_sections': []}`

### Base exact read evidence

- Procedure: `dtbl_flocon_read`
- Reader: `dtbl_flocon_read.f90`
- Match: exact_filename
- Resolved default filename(s): `flo_con.dtl`
- Source filename expression(s): `in_cond%dtbl_flo`
- Open: line 31, file expression `in_cond%dtbl_flo`, parser value `in_cond%dtbl_flo`, condition `if (.not. i_exist .or. in_cond%dtbl_flo == "null") then / else > do`

| Line | Role | Condition | Fields read |
| --- | --- | --- | --- |
| 32 | title | `if (.not. i_exist .or. in_cond%dtbl_flo == "null") then / else > do` | `titldum` |
| 34 | data | `if (.not. i_exist .or. in_cond%dtbl_flo == "null") then / else > do` | `mdtbl` |
| 36 | data | `if (.not. i_exist .or. in_cond%dtbl_flo == "null") then / else > do` | _no fields captured_ |
| 41 | header | `if (.not. i_exist .or. in_cond%dtbl_flo == "null") then / else > do > do i = 1, mdtbl` | `header` |
| 43 | data | `if (.not. i_exist .or. in_cond%dtbl_flo == "null") then / else > do > do i = 1, mdtbl` | `dtbl_flo(i)%name`, `dtbl_flo(i)%conds`, `dtbl_flo(i)%alts`, `dtbl_flo(i)%acts` |
| 54 | header | `if (.not. i_exist .or. in_cond%dtbl_flo == "null") then / else > do > do i = 1, mdtbl` | `header` |
| 57 | data | `if (.not. i_exist .or. in_cond%dtbl_flo == "null") then / else > do > do i = 1, mdtbl > do ic = 1, dtbl_flo(i)%conds` | `dtbl_flo(i)%cond(ic)`, `(dtbl_flo(i)%alt(ic,ial), ial = 1, dtbl_flo(i)%alts)` |
| 62 | header | `if (.not. i_exist .or. in_cond%dtbl_flo == "null") then / else > do > do i = 1, mdtbl` | `header` |
| 65 | data | `if (.not. i_exist .or. in_cond%dtbl_flo == "null") then / else > do > do i = 1, mdtbl > do iac = 1, dtbl_flo(i)%acts` | `dtbl_flo(i)%act(iac)`, `(dtbl_flo(i)%act_outcomes(iac,ial), ial = 1, dtbl_flo(i)%alts)` |
| 68 | data | `if (.not. i_exist .or. in_cond%dtbl_flo == "null") then / else > do > do i = 1, mdtbl` | _no fields captured_ |


### Candidate exact read evidence

- Procedure: `dtbl_flocon_read`
- Reader: `dtbl_flocon_read.f90`
- Match: exact_filename
- Resolved default filename(s): `flo_con.dtl`
- Source filename expression(s): `in_cond%dtbl_flo`
- Open: line 31, file expression `in_cond%dtbl_flo`, parser value `in_cond%dtbl_flo`, condition `if (.not. i_exist .or. in_cond%dtbl_flo == "null") then / else > do`

| Line | Role | Condition | Fields read |
| --- | --- | --- | --- |
| 32 | title | `if (.not. i_exist .or. in_cond%dtbl_flo == "null") then / else > do` | `titldum` |
| 34 | data | `if (.not. i_exist .or. in_cond%dtbl_flo == "null") then / else > do` | `mdtbl` |
| 36 | data | `if (.not. i_exist .or. in_cond%dtbl_flo == "null") then / else > do` | _no fields captured_ |
| 41 | header | `if (.not. i_exist .or. in_cond%dtbl_flo == "null") then / else > do > do i = 1, mdtbl` | `header` |
| 43 | data | `if (.not. i_exist .or. in_cond%dtbl_flo == "null") then / else > do > do i = 1, mdtbl` | `dtbl_flo(i)%name`, `dtbl_flo(i)%conds`, `dtbl_flo(i)%alts`, `dtbl_flo(i)%acts` |
| 54 | header | `if (.not. i_exist .or. in_cond%dtbl_flo == "null") then / else > do > do i = 1, mdtbl` | `header` |
| 57 | data | `if (.not. i_exist .or. in_cond%dtbl_flo == "null") then / else > do > do i = 1, mdtbl > do ic = 1, dtbl_flo(i)%conds` | `dtbl_flo(i)%cond(ic)`, `(dtbl_flo(i)%alt(ic,ial), ial = 1, dtbl_flo(i)%alts)` |
| 62 | header | `if (.not. i_exist .or. in_cond%dtbl_flo == "null") then / else > do > do i = 1, mdtbl` | `header` |
| 65 | data | `if (.not. i_exist .or. in_cond%dtbl_flo == "null") then / else > do > do i = 1, mdtbl > do iac = 1, dtbl_flo(i)%acts` | `dtbl_flo(i)%act(iac)`, `(dtbl_flo(i)%act_outcomes(iac,ial), ial = 1, dtbl_flo(i)%alts)` |
| 68 | data | `if (.not. i_exist .or. in_cond%dtbl_flo == "null") then / else > do > do i = 1, mdtbl` | _no fields captured_ |


## `lum.dtl`

- Schema diff status: `['decision_tables.changed']`
- Review needed: no
- Base schema presence: `{'resolved_sections': ['decision_tables'], 'unresolved_sections': []}`
- Candidate schema presence: `{'resolved_sections': ['decision_tables'], 'unresolved_sections': []}`

### Base exact read evidence

- Procedure: `dtbl_lum_read`
- Reader: `dtbl_lum_read.f90`
- Match: exact_filename
- Resolved default filename(s): `lum.dtl`
- Source filename expression(s): `in_cond%dtbl_lum`
- Open: line 41, file expression `in_cond%dtbl_lum`, parser value `in_cond%dtbl_lum`, condition `if (.not. i_exist .or. in_cond%dtbl_lum == "null") then / else > do`

| Line | Role | Condition | Fields read |
| --- | --- | --- | --- |
| 42 | title | `if (.not. i_exist .or. in_cond%dtbl_lum == "null") then / else > do` | `titldum` |
| 44 | data | `if (.not. i_exist .or. in_cond%dtbl_lum == "null") then / else > do` | `mdtbl` |
| 46 | data | `if (.not. i_exist .or. in_cond%dtbl_lum == "null") then / else > do` | _no fields captured_ |
| 51 | header | `if (.not. i_exist .or. in_cond%dtbl_lum == "null") then / else > do > do i = 1, mdtbl` | `header` |
| 53 | data | `if (.not. i_exist .or. in_cond%dtbl_lum == "null") then / else > do > do i = 1, mdtbl` | `dtbl_lum(i)%name`, `dtbl_lum(i)%conds`, `dtbl_lum(i)%alts`, `dtbl_lum(i)%acts` |
| 67 | header | `if (.not. i_exist .or. in_cond%dtbl_lum == "null") then / else > do > do i = 1, mdtbl` | `header` |
| 70 | data | `if (.not. i_exist .or. in_cond%dtbl_lum == "null") then / else > do > do i = 1, mdtbl > do ic = 1, dtbl_lum(i)%conds` | `dtbl_lum(i)%cond(ic)`, `(dtbl_lum(i)%alt(ic,ial), ial = 1, dtbl_lum(i)%alts)` |
| 74 | data | `if (.not. i_exist .or. in_cond%dtbl_lum == "null") then / else > do > do i = 1, mdtbl > do ic = 1, dtbl_lum(i)%conds > if (dtbl_lum(i)%cond(ic)%var == "prob_unif") then` | `dtbl_lum(i)%cond(ic)%var`, `dtbl_lum(i)%frac_app` |
| 93 | header | `if (.not. i_exist .or. in_cond%dtbl_lum == "null") then / else > do > do i = 1, mdtbl` | `header` |
| 96 | data | `if (.not. i_exist .or. in_cond%dtbl_lum == "null") then / else > do > do i = 1, mdtbl > do iac = 1, dtbl_lum(i)%acts` | `dtbl_lum(i)%act(iac)`, `(dtbl_lum(i)%act_outcomes(iac,ial), ial = 1, dtbl_lum(i)%alts)` |


### Candidate exact read evidence

- Procedure: `dtbl_lum_read`
- Reader: `dtbl_lum_read.f90`
- Match: exact_filename
- Resolved default filename(s): `lum.dtl`
- Source filename expression(s): `in_cond%dtbl_lum`
- Open: line 41, file expression `in_cond%dtbl_lum`, parser value `in_cond%dtbl_lum`, condition `if (.not. i_exist .or. in_cond%dtbl_lum == "null") then / else > do`

| Line | Role | Condition | Fields read |
| --- | --- | --- | --- |
| 42 | title | `if (.not. i_exist .or. in_cond%dtbl_lum == "null") then / else > do` | `titldum` |
| 44 | data | `if (.not. i_exist .or. in_cond%dtbl_lum == "null") then / else > do` | `mdtbl` |
| 46 | data | `if (.not. i_exist .or. in_cond%dtbl_lum == "null") then / else > do` | _no fields captured_ |
| 51 | header | `if (.not. i_exist .or. in_cond%dtbl_lum == "null") then / else > do > do i = 1, mdtbl` | `header` |
| 53 | data | `if (.not. i_exist .or. in_cond%dtbl_lum == "null") then / else > do > do i = 1, mdtbl` | `dtbl_lum(i)%name`, `dtbl_lum(i)%conds`, `dtbl_lum(i)%alts`, `dtbl_lum(i)%acts` |
| 67 | header | `if (.not. i_exist .or. in_cond%dtbl_lum == "null") then / else > do > do i = 1, mdtbl` | `header` |
| 70 | data | `if (.not. i_exist .or. in_cond%dtbl_lum == "null") then / else > do > do i = 1, mdtbl > do ic = 1, dtbl_lum(i)%conds` | `dtbl_lum(i)%cond(ic)`, `(dtbl_lum(i)%alt(ic,ial), ial = 1, dtbl_lum(i)%alts)` |
| 74 | data | `if (.not. i_exist .or. in_cond%dtbl_lum == "null") then / else > do > do i = 1, mdtbl > do ic = 1, dtbl_lum(i)%conds > if (dtbl_lum(i)%cond(ic)%var == "prob_unif") then` | `dtbl_lum(i)%cond(ic)%var`, `dtbl_lum(i)%frac_app` |
| 93 | header | `if (.not. i_exist .or. in_cond%dtbl_lum == "null") then / else > do > do i = 1, mdtbl` | `header` |
| 96 | data | `if (.not. i_exist .or. in_cond%dtbl_lum == "null") then / else > do > do i = 1, mdtbl > do iac = 1, dtbl_lum(i)%acts` | `dtbl_lum(i)%act(iac)`, `(dtbl_lum(i)%act_outcomes(iac,ial), ial = 1, dtbl_lum(i)%alts)` |


## `manure.frt`

- Schema diff status: `['files.removed', 'newly_unresolved']`
- Review needed: yes
- Base schema presence: `{'resolved_sections': ['files'], 'unresolved_sections': []}`
- Candidate schema presence: `{'resolved_sections': [], 'unresolved_sections': ['unresolved']}`

### Base exact read evidence

- Procedure: `manure_parm_read`
- Reader: `manure_parm_read.f90`
- Match: exact_filename
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


### Candidate exact read evidence

_No exact candidate opened/read evidence found._

### Candidate related read evidence

- Procedure: `manure_db_read`
- Reader: `manure_db_read.f90`
- Match: reader procedure tokens match target, same reader procedure stem, shared filename tokens, similar opened filename/expression
- Resolved default filename(s): `manure_db.frt`
- Source filename expression(s): `manure_db.frt`
- Open: line 27, file expression `"manure_db.frt"`, parser value `manure_db.frt`, condition `if (.not. i_exist .or. "manure_db.frt" == "null") then / else > do`

| Line | Role | Condition | Fields read |
| --- | --- | --- | --- |
| 28 | title | `if (.not. i_exist .or. "manure_db.frt" == "null") then / else > do` | `titldum` |
| 30 | header | `if (.not. i_exist .or. "manure_db.frt" == "null") then / else > do` | `header` |
| 33 | title | `if (.not. i_exist .or. "manure_db.frt" == "null") then / else > do > do while (eof == 0)` | `titldum` |
| 41 | title | `if (.not. i_exist .or. "manure_db.frt" == "null") then / else > do` | `titldum` |
| 43 | header | `if (.not. i_exist .or. "manure_db.frt" == "null") then / else > do` | `header` |
| 47 | data | `if (.not. i_exist .or. "manure_db.frt" == "null") then / else > do > do it = 1, imax` | `manure_db(it)%name`, `manure_db(it)%org_min`, `manure_db(it)%pests`, `manure_db(it)%paths`, `manure_db(it)%hmets`, `manure_db(it)%salts`, `manure_db(it)%constit`, `manure_db(it)%descrip` |

- Procedure: `manure_orgmin_read`
- Reader: `manure_orgmin_read.f90`
- Match: reader procedure tokens match target, same reader procedure stem, shared filename tokens, similar opened filename/expression
- Resolved default filename(s): `manure_om.frt`
- Source filename expression(s): `manure_om.frt`
- Open: line 27, file expression `"manure_om.frt"`, parser value `manure_om.frt`, condition `if (.not. i_exist .or. "manure_om.frt" == "null") then / else > do`

| Line | Role | Condition | Fields read |
| --- | --- | --- | --- |
| 28 | title | `if (.not. i_exist .or. "manure_om.frt" == "null") then / else > do` | `titldum` |
| 30 | header | `if (.not. i_exist .or. "manure_om.frt" == "null") then / else > do` | `header` |
| 33 | title | `if (.not. i_exist .or. "manure_om.frt" == "null") then / else > do > do while (eof == 0)` | `titldum` |
| 41 | title | `if (.not. i_exist .or. "manure_om.frt" == "null") then / else > do` | `titldum` |
| 43 | header | `if (.not. i_exist .or. "manure_om.frt" == "null") then / else > do` | `header` |
| 47 | data | `if (.not. i_exist .or. "manure_om.frt" == "null") then / else > do > do it = 1, imax` | `manure_om(it)%name`, `manure_om(it)%frac_water`, `manure_om(it)%fcbn`, `manure_om(it)%fminn`, `manure_om(it)%fminp`, `manure_om(it)%forgn`, `manure_om(it)%forgp`, `manure_om(it)%fnh3n`, `manure_om(it)%description` |

- Procedure: `manure_allocation_read`
- Reader: `manure_allocation_read.f90`
- Match: reader procedure tokens match target, same reader procedure stem, shared filename tokens
- Resolved default filename(s): `manure_allo.mnu`
- Source filename expression(s): `manure_allo.mnu`
- Open: line 39, file expression `"manure_allo.mnu"`, parser value `manure_allo.mnu`, condition `if (.not. i_exist .or. "manure_allo.mnu" == "null") then / else > do`

| Line | Role | Condition | Fields read |
| --- | --- | --- | --- |
| 40 | title | `if (.not. i_exist .or. "manure_allo.mnu" == "null") then / else > do` | `titldum` |
| 42 | count | `if (.not. i_exist .or. "manure_allo.mnu" == "null") then / else > do` | `imax` |
| 49 | header | `if (.not. i_exist .or. "manure_allo.mnu" == "null") then / else > do > do imro = 1, imax` | `header` |
| 51 | data | `if (.not. i_exist .or. "manure_allo.mnu" == "null") then / else > do > do imro = 1, imax` | `mallo(imro)%name`, `mallo(imro)%rule_typ`, `mallo(imro)%src_obs`, `mallo(imro)%trn_obs` |
| 54 | header | `if (.not. i_exist .or. "manure_allo.mnu" == "null") then / else > do > do imro = 1, imax` | `header` |
| 63 | data | `if (.not. i_exist .or. "manure_allo.mnu" == "null") then / else > do > do imro = 1, imax > do isrc = 1, mallo(imro)%src_obs` | `i` |
| 67 | data | `if (.not. i_exist .or. "manure_allo.mnu" == "null") then / else > do > do imro = 1, imax > do isrc = 1, mallo(imro)%src_obs` | `k`, `mallo(imro)%src(i)%mois_typ`, `mallo(imro)%src(i)%manure_typ`, `mallo(imro)%src(i)%lat`, `mallo(imro)%src(i)%long`, `mallo(imro)%src(i)%stor_init`, `mallo(imro)%src(i)%stor_max`, `mallo(imro)%src(i)%prod_mon` |
| 81 | header | `if (.not. i_exist .or. "manure_allo.mnu" == "null") then / else > do > do imro = 1, imax` | `header` |
| 90 | data | `if (.not. i_exist .or. "manure_allo.mnu" == "null") then / else > do > do imro = 1, imax > do itrn = 1, num_objs` | `i` |
| 94 | data | `if (.not. i_exist .or. "manure_allo.mnu" == "null") then / else > do > do imro = 1, imax > do itrn = 1, num_objs` | `k`, `mallo(imro)%trn(i)%ob_typ`, `mallo(imro)%trn(i)%ob_num`, `mallo(imro)%trn(i)%dtbl`, `mallo(imro)%trn(i)%right` |


## `out_src.wal`

- Schema diff status: `['newly_unresolved', 'runtime_arity.removed']`
- Review needed: yes
- Base schema presence: `{'resolved_sections': ['runtime_arity'], 'unresolved_sections': []}`
- Candidate schema presence: `{'resolved_sections': [], 'unresolved_sections': ['runtime_arity_unresolved']}`

### Base exact read evidence

- Procedure: `water_osrc_read`
- Reader: `water_osrc_read.f90`
- Match: exact_filename
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


### Candidate exact read evidence

_No exact candidate opened/read evidence found._

### Candidate related read evidence

- Procedure: `water_osrc_read`
- Reader: `water_osrc_read.f90`
- Match: shared filename tokens, similar opened filename/expression
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

- Procedure: `header_write`
- Reader: `header_write.f90`
- Match: shared filename tokens, similar opened filename/expression
- Resolved default filename(s): `hru-out.cal`
- Source filename expression(s): `hru-out.cal`
- Open: line 25, file expression `"hru-out.cal"`, parser value `hru-out.cal`, condition `if (cal_soft == "y") then`
- Reads: _none captured_

- Procedure: `water_orcv_read`
- Reader: `water_orcv_read.f90`
- Match: similar opened filename/expression
- Resolved default filename(s): `outside_rcv.wal`
- Source filename expression(s): `outside_rcv.wal`
- Open: line 34, file expression `'outside_rcv.wal'`, parser value `outside_rcv.wal`, condition `if (.not. i_exist .or. 'outside_rcv.wal' == "null") then / else > do`

| Line | Role | Condition | Fields read |
| --- | --- | --- | --- |
| 35 | title | `if (.not. i_exist .or. 'outside_rcv.wal' == "null") then / else > do` | `titldum` |
| 37 | count | `if (.not. i_exist .or. 'outside_rcv.wal' == "null") then / else > do` | `imax` |
| 38 | header | `if (.not. i_exist .or. 'outside_rcv.wal' == "null") then / else > do` | `header` |
| 45 | data | `if (.not. i_exist .or. 'outside_rcv.wal' == "null") then / else > do > do ircv = 1, imax` | `i`, `orcv(ircv)%name`, `orcv(ircv)%filename` |


## `res_rel.dtl`

- Schema diff status: `['decision_tables.changed']`
- Review needed: no
- Base schema presence: `{'resolved_sections': ['decision_tables'], 'unresolved_sections': []}`
- Candidate schema presence: `{'resolved_sections': ['decision_tables'], 'unresolved_sections': []}`

### Base exact read evidence

- Procedure: `dtbl_res_read`
- Reader: `dtbl_res_read.f90`
- Match: exact_filename
- Resolved default filename(s): `res_rel.dtl`
- Source filename expression(s): `in_cond%dtbl_res`
- Open: line 36, file expression `in_cond%dtbl_res`, parser value `in_cond%dtbl_res`, condition `if (.not. i_exist .or. in_cond%dtbl_res == "null") then / else > do`

| Line | Role | Condition | Fields read |
| --- | --- | --- | --- |
| 37 | title | `if (.not. i_exist .or. in_cond%dtbl_res == "null") then / else > do` | `titldum` |
| 39 | data | `if (.not. i_exist .or. in_cond%dtbl_res == "null") then / else > do` | `mdtbl` |
| 41 | data | `if (.not. i_exist .or. in_cond%dtbl_res == "null") then / else > do` | _no fields captured_ |
| 46 | header | `if (.not. i_exist .or. in_cond%dtbl_res == "null") then / else > do > do i = 1, mdtbl` | `header` |
| 48 | data | `if (.not. i_exist .or. in_cond%dtbl_res == "null") then / else > do > do i = 1, mdtbl` | `dtbl_res(i)%name`, `dtbl_res(i)%conds`, `dtbl_res(i)%alts`, `dtbl_res(i)%acts` |
| 59 | header | `if (.not. i_exist .or. in_cond%dtbl_res == "null") then / else > do > do i = 1, mdtbl` | `header` |
| 62 | data | `if (.not. i_exist .or. in_cond%dtbl_res == "null") then / else > do > do i = 1, mdtbl > do ic = 1, dtbl_res(i)%conds` | `dtbl_res(i)%cond(ic)`, `(dtbl_res(i)%alt(ic,ial), ial = 1, dtbl_res(i)%alts)` |
| 67 | header | `if (.not. i_exist .or. in_cond%dtbl_res == "null") then / else > do > do i = 1, mdtbl` | `header` |
| 70 | data | `if (.not. i_exist .or. in_cond%dtbl_res == "null") then / else > do > do i = 1, mdtbl > do iac = 1, dtbl_res(i)%acts` | `dtbl_res(i)%act(iac)`, `(dtbl_res(i)%act_outcomes(iac,ial), ial = 1, dtbl_res(i)%alts)` |
| 73 | data | `if (.not. i_exist .or. in_cond%dtbl_res == "null") then / else > do > do i = 1, mdtbl` | _no fields captured_ |


### Candidate exact read evidence

- Procedure: `dtbl_res_read`
- Reader: `dtbl_res_read.f90`
- Match: exact_filename
- Resolved default filename(s): `res_rel.dtl`
- Source filename expression(s): `in_cond%dtbl_res`
- Open: line 36, file expression `in_cond%dtbl_res`, parser value `in_cond%dtbl_res`, condition `if (.not. i_exist .or. in_cond%dtbl_res == "null") then / else > do`

| Line | Role | Condition | Fields read |
| --- | --- | --- | --- |
| 37 | title | `if (.not. i_exist .or. in_cond%dtbl_res == "null") then / else > do` | `titldum` |
| 39 | data | `if (.not. i_exist .or. in_cond%dtbl_res == "null") then / else > do` | `mdtbl` |
| 41 | data | `if (.not. i_exist .or. in_cond%dtbl_res == "null") then / else > do` | _no fields captured_ |
| 46 | header | `if (.not. i_exist .or. in_cond%dtbl_res == "null") then / else > do > do i = 1, mdtbl` | `header` |
| 48 | data | `if (.not. i_exist .or. in_cond%dtbl_res == "null") then / else > do > do i = 1, mdtbl` | `dtbl_res(i)%name`, `dtbl_res(i)%conds`, `dtbl_res(i)%alts`, `dtbl_res(i)%acts` |
| 59 | header | `if (.not. i_exist .or. in_cond%dtbl_res == "null") then / else > do > do i = 1, mdtbl` | `header` |
| 62 | data | `if (.not. i_exist .or. in_cond%dtbl_res == "null") then / else > do > do i = 1, mdtbl > do ic = 1, dtbl_res(i)%conds` | `dtbl_res(i)%cond(ic)`, `(dtbl_res(i)%alt(ic,ial), ial = 1, dtbl_res(i)%alts)` |
| 67 | header | `if (.not. i_exist .or. in_cond%dtbl_res == "null") then / else > do > do i = 1, mdtbl` | `header` |
| 70 | data | `if (.not. i_exist .or. in_cond%dtbl_res == "null") then / else > do > do i = 1, mdtbl > do iac = 1, dtbl_res(i)%acts` | `dtbl_res(i)%act(iac)`, `(dtbl_res(i)%act_outcomes(iac,ial), ial = 1, dtbl_res(i)%alts)` |
| 73 | data | `if (.not. i_exist .or. in_cond%dtbl_res == "null") then / else > do > do i = 1, mdtbl` | _no fields captured_ |


## `scen_lu.dtl`

- Schema diff status: `['decision_tables.changed']`
- Review needed: no
- Base schema presence: `{'resolved_sections': ['decision_tables'], 'unresolved_sections': []}`
- Candidate schema presence: `{'resolved_sections': ['decision_tables'], 'unresolved_sections': []}`

### Base exact read evidence

- Procedure: `dtbl_scen_read`
- Reader: `dtbl_scen_read.f90`
- Match: exact_filename
- Resolved default filename(s): `scen_lu.dtl`
- Source filename expression(s): `in_cond%dtbl_scen`
- Open: line 35, file expression `in_cond%dtbl_scen`, parser value `in_cond%dtbl_scen`, condition `if (.not. i_exist .or. in_cond%dtbl_scen == "null") then / else > do`

| Line | Role | Condition | Fields read |
| --- | --- | --- | --- |
| 36 | title | `if (.not. i_exist .or. in_cond%dtbl_scen == "null") then / else > do` | `titldum` |
| 38 | data | `if (.not. i_exist .or. in_cond%dtbl_scen == "null") then / else > do` | `mdtbl` |
| 40 | data | `if (.not. i_exist .or. in_cond%dtbl_scen == "null") then / else > do` | _no fields captured_ |
| 45 | header | `if (.not. i_exist .or. in_cond%dtbl_scen == "null") then / else > do > do i = 1, mdtbl` | `header` |
| 47 | data | `if (.not. i_exist .or. in_cond%dtbl_scen == "null") then / else > do > do i = 1, mdtbl` | `dtbl_scen(i)%name`, `dtbl_scen(i)%conds`, `dtbl_scen(i)%alts`, `dtbl_scen(i)%acts` |
| 61 | header | `if (.not. i_exist .or. in_cond%dtbl_scen == "null") then / else > do > do i = 1, mdtbl` | `header` |
| 64 | data | `if (.not. i_exist .or. in_cond%dtbl_scen == "null") then / else > do > do i = 1, mdtbl > do ic = 1, dtbl_scen(i)%conds` | `dtbl_scen(i)%cond(ic)`, `(dtbl_scen(i)%alt(ic,ial), ial = 1, dtbl_scen(i)%alts)` |
| 69 | header | `if (.not. i_exist .or. in_cond%dtbl_scen == "null") then / else > do > do i = 1, mdtbl` | `header` |
| 72 | data | `if (.not. i_exist .or. in_cond%dtbl_scen == "null") then / else > do > do i = 1, mdtbl > do iac = 1, dtbl_scen(i)%acts` | `dtbl_scen(i)%act(iac)`, `(dtbl_scen(i)%act_outcomes(iac,ial), ial = 1, dtbl_scen(i)%alts)` |
| 75 | data | `if (.not. i_exist .or. in_cond%dtbl_scen == "null") then / else > do > do i = 1, mdtbl` | _no fields captured_ |


### Candidate exact read evidence

- Procedure: `dtbl_scen_read`
- Reader: `dtbl_scen_read.f90`
- Match: exact_filename
- Resolved default filename(s): `scen_lu.dtl`
- Source filename expression(s): `in_cond%dtbl_scen`
- Open: line 35, file expression `in_cond%dtbl_scen`, parser value `in_cond%dtbl_scen`, condition `if (.not. i_exist .or. in_cond%dtbl_scen == "null") then / else > do`

| Line | Role | Condition | Fields read |
| --- | --- | --- | --- |
| 36 | title | `if (.not. i_exist .or. in_cond%dtbl_scen == "null") then / else > do` | `titldum` |
| 38 | data | `if (.not. i_exist .or. in_cond%dtbl_scen == "null") then / else > do` | `mdtbl` |
| 40 | data | `if (.not. i_exist .or. in_cond%dtbl_scen == "null") then / else > do` | _no fields captured_ |
| 45 | header | `if (.not. i_exist .or. in_cond%dtbl_scen == "null") then / else > do > do i = 1, mdtbl` | `header` |
| 47 | data | `if (.not. i_exist .or. in_cond%dtbl_scen == "null") then / else > do > do i = 1, mdtbl` | `dtbl_scen(i)%name`, `dtbl_scen(i)%conds`, `dtbl_scen(i)%alts`, `dtbl_scen(i)%acts` |
| 61 | header | `if (.not. i_exist .or. in_cond%dtbl_scen == "null") then / else > do > do i = 1, mdtbl` | `header` |
| 64 | data | `if (.not. i_exist .or. in_cond%dtbl_scen == "null") then / else > do > do i = 1, mdtbl > do ic = 1, dtbl_scen(i)%conds` | `dtbl_scen(i)%cond(ic)`, `(dtbl_scen(i)%alt(ic,ial), ial = 1, dtbl_scen(i)%alts)` |
| 69 | header | `if (.not. i_exist .or. in_cond%dtbl_scen == "null") then / else > do > do i = 1, mdtbl` | `header` |
| 72 | data | `if (.not. i_exist .or. in_cond%dtbl_scen == "null") then / else > do > do i = 1, mdtbl > do iac = 1, dtbl_scen(i)%acts` | `dtbl_scen(i)%act(iac)`, `(dtbl_scen(i)%act_outcomes(iac,ial), ial = 1, dtbl_scen(i)%alts)` |
| 75 | data | `if (.not. i_exist .or. in_cond%dtbl_scen == "null") then / else > do > do i = 1, mdtbl` | _no fields captured_ |


## `transplant.plt`

- Schema diff status: `['files.removed', 'newly_unresolved']`
- Review needed: yes
- Base schema presence: `{'resolved_sections': ['files'], 'unresolved_sections': []}`
- Candidate schema presence: `{'resolved_sections': [], 'unresolved_sections': ['unresolved']}`

### Base exact read evidence

- Procedure: `plant_transplant_read`
- Reader: `plant_transplant_read.f90`
- Match: exact_filename
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


### Candidate exact read evidence

_No exact candidate opened/read evidence found._

### Candidate related read evidence

- Procedure: `plant_transplant_read`
- Reader: `plant_transplant_read.f90`
- Match: reader procedure tokens match target, same reader procedure stem, shared filename tokens, similar opened filename/expression
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


## `water_allocation.wro`

- Schema diff status: `['multi_record.removed', 'newly_unresolved']`
- Review needed: yes
- Base schema presence: `{'resolved_sections': ['multi_record'], 'unresolved_sections': []}`
- Candidate schema presence: `{'resolved_sections': [], 'unresolved_sections': ['multi_record_unresolved']}`

### Base exact read evidence

- Procedure: `water_allocation_read`
- Reader: `water_allocation_read.f90`
- Match: exact_filename
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


### Candidate exact read evidence

_No exact candidate opened/read evidence found._

### Candidate related read evidence

- Procedure: `water_allocation_read`
- Reader: `water_allocation_read.f90`
- Match: reader procedure tokens match target, same reader procedure stem
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

- Procedure: `water_allocation_read`
- Reader: `water_allocation_read.f90`
- Match: reader procedure tokens match target, same reader procedure stem
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


## `water_canal.wal`

- Schema diff status: `['runtime_arity.changed']`
- Review needed: no
- Base schema presence: `{'resolved_sections': ['runtime_arity'], 'unresolved_sections': []}`
- Candidate schema presence: `{'resolved_sections': ['runtime_arity'], 'unresolved_sections': []}`

### Base exact read evidence

- Procedure: `water_canal_read`
- Reader: `water_canal_read.f90`
- Match: exact_filename
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


### Candidate exact read evidence

- Procedure: `water_canal_read`
- Reader: `water_canal_read.f90`
- Match: exact_filename
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


## `water_pipe.wal`

- Schema diff status: `['runtime_arity.changed']`
- Review needed: no
- Base schema presence: `{'resolved_sections': ['runtime_arity'], 'unresolved_sections': []}`
- Candidate schema presence: `{'resolved_sections': ['runtime_arity'], 'unresolved_sections': []}`

### Base exact read evidence

- Procedure: `water_pipe_read`
- Reader: `water_pipe_read.f90`
- Match: exact_filename
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


### Candidate exact read evidence

- Procedure: `water_pipe_read`
- Reader: `water_pipe_read.f90`
- Match: exact_filename
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


## `water_treat.wal`

- Schema diff status: `['newly_unresolved', 'runtime_arity.removed']`
- Review needed: yes
- Base schema presence: `{'resolved_sections': ['runtime_arity'], 'unresolved_sections': []}`
- Candidate schema presence: `{'resolved_sections': [], 'unresolved_sections': ['runtime_arity_unresolved']}`

### Base exact read evidence

- Procedure: `water_treatment_read`
- Reader: `water_treatment_read.f90`
- Match: exact_filename
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


### Candidate exact read evidence

- Procedure: `water_treatment_read`
- Reader: `water_treatment_read.f90`
- Match: exact_filename
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


## `water_use.wal`

- Schema diff status: `['newly_unresolved', 'runtime_arity.removed']`
- Review needed: yes
- Base schema presence: `{'resolved_sections': ['runtime_arity'], 'unresolved_sections': []}`
- Candidate schema presence: `{'resolved_sections': [], 'unresolved_sections': ['runtime_arity_unresolved']}`

### Base exact read evidence

- Procedure: `water_use_read`
- Reader: `water_use_read.f90`
- Match: exact_filename
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


### Candidate exact read evidence

- Procedure: `water_use_read`
- Reader: `water_use_read.f90`
- Match: exact_filename
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
