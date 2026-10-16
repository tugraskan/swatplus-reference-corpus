# Source Read Evidence for Schema Review

This report is generated when a comparison has schema entries that changed, disappeared from resolved schemas, or became newly unresolved. It does not certify a final schema. It shows the Fortran read evidence that a human or extractor update should review.

## `aqu_reg.def`

- Schema diff status: `['files.added']`
- Review needed: yes
- Base schema presence: `{'resolved_sections': [], 'unresolved_sections': ['unresolved']}`
- Candidate schema presence: `{'resolved_sections': ['files'], 'unresolved_sections': []}`

### Base exact read evidence

_No exact base opened/read evidence found._

### Base related read evidence

- Procedure: `reg_read_elements`
- Reader: `reg_read_elements.f90`
- Match: shared filename tokens, similar opened filename/expression
- Resolved default filename(s): `ls_reg.def`
- Source filename expression(s): `in_regs%def_reg`, `ls_reg.def`
- Open: line 40, file expression `in_regs%def_reg`, parser value `ls_reg.def`, condition `if (i_exist .or. in_regs%def_reg /= "null") then > do`

| Line | Role | Condition | Fields read |
| --- | --- | --- | --- |
| 41 | title | `if (i_exist .or. in_regs%def_reg /= "null") then > do` | `titldum` |
| 43 | data | `if (i_exist .or. in_regs%def_reg /= "null") then > do` | `mreg`, `mlug` |
| 73 | data | `if (i_exist .or. in_regs%def_reg /= "null") then > do > if (mlug > 0) then` | `i`, `lum_grp%num`, `(lum_grp%name(ilum), ilum = 1, mlug)` |
| 76 | header | `if (i_exist .or. in_regs%def_reg /= "null") then > do` | `header` |
| 99 | data | `if (i_exist .or. in_regs%def_reg /= "null") then > do > do i = 1, mreg` | `k`, `lsu_reg(i)%name`, `lsu_reg(i)%area_ha`, `nspu` |
| 104 | data | `if (i_exist .or. in_regs%def_reg /= "null") then > do > do i = 1, mreg > if (nspu > 0) then` | `k`, `lsu_reg(i)%name`, `lsu_reg(i)%area_ha`, `nspu`, `(elem_cnt(isp), isp = 1, nspu)` |

- Procedure: `aqu_read_elements`
- Reader: `aqu_read_elements.f90`
- Match: shared filename tokens
- Resolved default filename(s): `aqu_catunit.def`
- Source filename expression(s): `in_regs%def_aqu`, `aqu_catunit.def`
- Open: line 34, file expression `in_regs%def_aqu`, parser value `aqu_catunit.def`, condition `if (i_exist .or. in_regs%def_aqu /= "null") then > do`

| Line | Role | Condition | Fields read |
| --- | --- | --- | --- |
| 35 | title | `if (i_exist .or. in_regs%def_aqu /= "null") then > do` | `titldum` |
| 37 | data | `if (i_exist .or. in_regs%def_aqu /= "null") then > do` | `mreg` |
| 39 | header | `if (i_exist .or. in_regs%def_aqu /= "null") then > do` | `header` |
| 53 | data | `if (i_exist .or. in_regs%def_aqu /= "null") then > do > do i = 1, mreg` | `k`, `acu_out(i)%name`, `acu_out(i)%area_ha`, `nspu` |
| 58 | data | `if (i_exist .or. in_regs%def_aqu /= "null") then > do > do i = 1, mreg > if (nspu > 0) then` | `k`, `acu_out(i)%name`, `acu_out(i)%area_ha`, `nspu`, `(elem_cnt(isp), isp = 1, nspu)` |

- Procedure: `aqu_read_elements`
- Reader: `aqu_read_elements.f90`
- Match: shared filename tokens
- Resolved default filename(s): `aqu_catunit.def`
- Source filename expression(s): `in_regs%def_aqu`, `aqu_catunit.def`
- Open: line 87, file expression `in_regs%def_aqu`, parser value `aqu_catunit.def`, condition `if (i_exist .or. in_regs%def_aqu_reg /= "null") then > do`

| Line | Role | Condition | Fields read |
| --- | --- | --- | --- |
| 88 | title | `if (i_exist .or. in_regs%def_aqu_reg /= "null") then > do` | `titldum` |
| 90 | data | `if (i_exist .or. in_regs%def_aqu_reg /= "null") then > do` | `mreg` |
| 92 | header | `if (i_exist .or. in_regs%def_aqu_reg /= "null") then > do` | `header` |
| 96 | data | `if (i_exist .or. in_regs%def_aqu_reg /= "null") then > do > do i = 1, mreg` | `k`, `acu_reg(i)%name`, `acu_reg(i)%area_ha`, `nspu` |
| 101 | data | `if (i_exist .or. in_regs%def_aqu_reg /= "null") then > do > do i = 1, mreg > if (nspu > 0) then` | `k`, `acu_reg(i)%name`, `acu_reg(i)%area_ha`, `nspu`, `(elem_cnt(isp), isp = 1, nspu)` |

- Procedure: `reg_read_elements`
- Reader: `reg_read_elements.f90`
- Match: shared filename tokens
- Resolved default filename(s): `ls_reg.ele`
- Source filename expression(s): `in_regs%ele_reg`, `ls_reg.ele`
- Open: line 131, file expression `in_regs%ele_reg`, parser value `ls_reg.ele`, condition `if (i_exist .or. in_regs%ele_reg /= "null") then > do`

| Line | Role | Condition | Fields read |
| --- | --- | --- | --- |
| 132 | title | `if (i_exist .or. in_regs%ele_reg /= "null") then > do` | `titldum` |
| 134 | header | `if (i_exist .or. in_regs%ele_reg /= "null") then > do` | `header` |
| 138 | data | `if (i_exist .or. in_regs%ele_reg /= "null") then > do > do while (eof == 0)` | `i` |
| 146 | title | `if (i_exist .or. in_regs%ele_reg /= "null") then > do` | `titldum` |
| 148 | header | `if (i_exist .or. in_regs%ele_reg /= "null") then > do` | `header` |
| 153 | data | `if (i_exist .or. in_regs%ele_reg /= "null") then > do > do isp = 1, imax` | `i` |
| 155 | data | `if (i_exist .or. in_regs%ele_reg /= "null") then > do > do isp = 1, imax` | `k`, `reg_elem(i)%name`, `reg_elem(i)%ha`, `reg_elem(i)%obtyp`, `reg_elem(i)%obtypno` |

- Procedure: `aqu_read_elements`
- Reader: `aqu_read_elements.f90`
- Match: shared filename tokens
- Resolved default filename(s): `aqu_catunit.ele`
- Source filename expression(s): `in_regs%ele_aqu`, `aqu_catunit.ele`
- Open: line 147, file expression `in_regs%ele_aqu`, parser value `aqu_catunit.ele`, condition `if (i_exist .or. in_regs%ele_aqu /= "null") then > do`

| Line | Role | Condition | Fields read |
| --- | --- | --- | --- |
| 148 | title | `if (i_exist .or. in_regs%ele_aqu /= "null") then > do` | `titldum` |
| 150 | header | `if (i_exist .or. in_regs%ele_aqu /= "null") then > do` | `header` |
| 154 | data | `if (i_exist .or. in_regs%ele_aqu /= "null") then > do > do while (eof == 0)` | `i` |
| 162 | title | `if (i_exist .or. in_regs%ele_aqu /= "null") then > do` | `titldum` |
| 164 | header | `if (i_exist .or. in_regs%ele_aqu /= "null") then > do` | `header` |
| 169 | data | `if (i_exist .or. in_regs%ele_aqu /= "null") then > do > do isp = 1, imax` | `i` |
| 172 | data | `if (i_exist .or. in_regs%ele_aqu /= "null") then > do > do isp = 1, imax` | `k`, `acu_elem(i)%name`, `acu_elem(i)%obtyp`, `acu_elem(i)%obtypno`, `acu_elem(i)%bsn_frac`, `acu_elem(i)%ru_frac`, `acu_elem(i)%reg_frac` |


### Candidate exact read evidence

_No exact candidate opened/read evidence found._

### Candidate related read evidence

- Procedure: `reg_read_elements`
- Reader: `reg_read_elements.f90`
- Match: shared filename tokens, similar opened filename/expression
- Resolved default filename(s): `ls_reg.def`
- Source filename expression(s): `in_regs%def_reg`, `ls_reg.def`
- Open: line 42, file expression `in_regs%def_reg`, parser value `ls_reg.def`, condition `if (i_exist .or. in_regs%def_reg /= "null") then > do`

| Line | Role | Condition | Fields read |
| --- | --- | --- | --- |
| 43 | title | `if (i_exist .or. in_regs%def_reg /= "null") then > do` | `titldum` |
| 45 | data | `if (i_exist .or. in_regs%def_reg /= "null") then > do` | `mreg`, `mlug` |
| 75 | data | `if (i_exist .or. in_regs%def_reg /= "null") then > do > if (mlug > 0) then` | `i`, `lum_grp%num`, `(lum_grp%name(ilum), ilum = 1, mlug)` |
| 78 | header | `if (i_exist .or. in_regs%def_reg /= "null") then > do` | `header` |
| 101 | data | `if (i_exist .or. in_regs%def_reg /= "null") then > do > do i = 1, mreg` | `k`, `lsu_reg(i)%name`, `lsu_reg(i)%area_ha`, `nspu` |
| 106 | data | `if (i_exist .or. in_regs%def_reg /= "null") then > do > do i = 1, mreg > if (nspu > 0) then` | `k`, `lsu_reg(i)%name`, `lsu_reg(i)%area_ha`, `nspu`, `(elem_cnt(isp), isp = 1, nspu)` |

- Procedure: `aqu_read_elements`
- Reader: `aqu_read_elements.f90`
- Match: shared filename tokens
- Resolved default filename(s): `aqu_catunit.def`
- Source filename expression(s): `in_regs%def_aqu`, `aqu_catunit.def`
- Open: line 36, file expression `in_regs%def_aqu`, parser value `aqu_catunit.def`, condition `if (i_exist .or. in_regs%def_aqu /= "null") then > do`

| Line | Role | Condition | Fields read |
| --- | --- | --- | --- |
| 37 | title | `if (i_exist .or. in_regs%def_aqu /= "null") then > do` | `titldum` |
| 39 | data | `if (i_exist .or. in_regs%def_aqu /= "null") then > do` | `mreg` |
| 41 | header | `if (i_exist .or. in_regs%def_aqu /= "null") then > do` | `header` |
| 55 | data | `if (i_exist .or. in_regs%def_aqu /= "null") then > do > do i = 1, mreg` | `k`, `acu_out(i)%name`, `acu_out(i)%area_ha`, `nspu` |
| 60 | data | `if (i_exist .or. in_regs%def_aqu /= "null") then > do > do i = 1, mreg > if (nspu > 0) then` | `k`, `acu_out(i)%name`, `acu_out(i)%area_ha`, `nspu`, `(elem_cnt(isp), isp = 1, nspu)` |

- Procedure: `aqu_read_elements`
- Reader: `aqu_read_elements.f90`
- Match: shared filename tokens
- Resolved default filename(s): `aqu_catunit.def`
- Source filename expression(s): `in_regs%def_aqu`, `aqu_catunit.def`
- Open: line 89, file expression `in_regs%def_aqu`, parser value `aqu_catunit.def`, condition `if (i_exist .or. in_regs%def_aqu_reg /= "null") then > do`

| Line | Role | Condition | Fields read |
| --- | --- | --- | --- |
| 90 | title | `if (i_exist .or. in_regs%def_aqu_reg /= "null") then > do` | `titldum` |
| 92 | data | `if (i_exist .or. in_regs%def_aqu_reg /= "null") then > do` | `mreg` |
| 94 | header | `if (i_exist .or. in_regs%def_aqu_reg /= "null") then > do` | `header` |
| 98 | data | `if (i_exist .or. in_regs%def_aqu_reg /= "null") then > do > do i = 1, mreg` | `k`, `acu_reg(i)%name`, `acu_reg(i)%area_ha`, `nspu` |
| 103 | data | `if (i_exist .or. in_regs%def_aqu_reg /= "null") then > do > do i = 1, mreg > if (nspu > 0) then` | `k`, `acu_reg(i)%name`, `acu_reg(i)%area_ha`, `nspu`, `(elem_cnt(isp), isp = 1, nspu)` |

- Procedure: `reg_read_elements`
- Reader: `reg_read_elements.f90`
- Match: shared filename tokens
- Resolved default filename(s): `ls_reg.ele`
- Source filename expression(s): `in_regs%ele_reg`, `ls_reg.ele`
- Open: line 133, file expression `in_regs%ele_reg`, parser value `ls_reg.ele`, condition `if (i_exist .or. in_regs%ele_reg /= "null") then > do`

| Line | Role | Condition | Fields read |
| --- | --- | --- | --- |
| 134 | title | `if (i_exist .or. in_regs%ele_reg /= "null") then > do` | `titldum` |
| 136 | header | `if (i_exist .or. in_regs%ele_reg /= "null") then > do` | `header` |
| 140 | data | `if (i_exist .or. in_regs%ele_reg /= "null") then > do > do while (eof == 0)` | `i` |
| 148 | title | `if (i_exist .or. in_regs%ele_reg /= "null") then > do` | `titldum` |
| 150 | header | `if (i_exist .or. in_regs%ele_reg /= "null") then > do` | `header` |
| 155 | data | `if (i_exist .or. in_regs%ele_reg /= "null") then > do > do isp = 1, imax` | `i` |
| 157 | data | `if (i_exist .or. in_regs%ele_reg /= "null") then > do > do isp = 1, imax` | `k`, `reg_elem(i)%name`, `reg_elem(i)%ha`, `reg_elem(i)%obtyp`, `reg_elem(i)%obtypno` |

- Procedure: `aqu_read_elements`
- Reader: `aqu_read_elements.f90`
- Match: shared filename tokens
- Resolved default filename(s): `aqu_catunit.ele`
- Source filename expression(s): `in_regs%ele_aqu`, `aqu_catunit.ele`
- Open: line 149, file expression `in_regs%ele_aqu`, parser value `aqu_catunit.ele`, condition `if (i_exist .or. in_regs%ele_aqu /= "null") then > do`

| Line | Role | Condition | Fields read |
| --- | --- | --- | --- |
| 150 | title | `if (i_exist .or. in_regs%ele_aqu /= "null") then > do` | `titldum` |
| 152 | header | `if (i_exist .or. in_regs%ele_aqu /= "null") then > do` | `header` |
| 156 | data | `if (i_exist .or. in_regs%ele_aqu /= "null") then > do > do while (eof == 0)` | `i` |
| 164 | title | `if (i_exist .or. in_regs%ele_aqu /= "null") then > do` | `titldum` |
| 166 | header | `if (i_exist .or. in_regs%ele_aqu /= "null") then > do` | `header` |
| 171 | data | `if (i_exist .or. in_regs%ele_aqu /= "null") then > do > do isp = 1, imax` | `i` |
| 174 | data | `if (i_exist .or. in_regs%ele_aqu /= "null") then > do > do isp = 1, imax` | `k`, `acu_elem(i)%name`, `acu_elem(i)%obtyp`, `acu_elem(i)%obtypno`, `acu_elem(i)%bsn_frac`, `acu_elem(i)%ru_frac`, `acu_elem(i)%reg_frac` |


## `calibration.cal`

- Schema diff status: `['multi_record.changed']`
- Review needed: no
- Base schema presence: `{'resolved_sections': ['multi_record'], 'unresolved_sections': []}`
- Candidate schema presence: `{'resolved_sections': ['multi_record'], 'unresolved_sections': []}`

### Base exact read evidence

- Procedure: `cal_parmchg_read`
- Reader: `cal_parmchg_read.f90`
- Match: exact_filename
- Resolved default filename(s): `calibration.cal`
- Source filename expression(s): `in_chg%cal_upd`, `calibration.cal`
- Open: line 54, file expression `in_chg%cal_upd`, parser value `calibration.cal`, condition `if (.not. i_exist .or. in_chg%cal_upd == "null") then / else > do`

| Line | Role | Condition | Fields read |
| --- | --- | --- | --- |
| 55 | title | `if (.not. i_exist .or. in_chg%cal_upd == "null") then / else > do` | `titldum` |
| 57 | data | `if (.not. i_exist .or. in_chg%cal_upd == "null") then / else > do` | `mcal` |
| 60 | header | `if (.not. i_exist .or. in_chg%cal_upd == "null") then / else > do` | `header` |
| 65 | data | `if (.not. i_exist .or. in_chg%cal_upd == "null") then / else > do > do i = 1, mcal` | `cal_upd(i)%name`, `cal_upd(i)%chg_typ`, `cal_upd(i)%val`, `cal_upd(i)%conds`, `cal_upd(i)%lyr1`, `cal_upd(i)%lyr2`, `cal_upd(i)%year1`, `cal_upd(i)%year2`, `cal_upd(i)%day1`, `cal_upd(i)%day2`, `nspu` |
| 72 | data | `if (.not. i_exist .or. in_chg%cal_upd == "null") then / else > do > do i = 1, mcal > if (nspu > 0) then` | `cal_upd(i)%name`, `cal_upd(i)%chg_typ`, `cal_upd(i)%val`, `cal_upd(i)%conds`, `cal_upd(i)%lyr1`, `cal_upd(i)%lyr2`, `cal_upd(i)%year1`, `cal_upd(i)%year2`, `cal_upd(i)%day1`, `cal_upd(i)%day2`, `cal_upd(i)%num_tot`, `(elem_cnt(isp), isp = 1, nspu)` |
| 91 | data | `if (.not. i_exist .or. in_chg%cal_upd == "null") then / else > do > do i = 1, mcal > if (nconds > 0) then > do icond = 1, nconds` | `cal_upd(i)%cond(icond)` |


### Candidate exact read evidence

- Procedure: `cal_parmchg_read`
- Reader: `cal_parmchg_read.f90`
- Match: exact_filename
- Resolved default filename(s): `calibration.cal`
- Source filename expression(s): `in_chg%cal_upd`, `calibration.cal`
- Open: line 57, file expression `in_chg%cal_upd`, parser value `calibration.cal`, condition `if (.not. i_exist .or. in_chg%cal_upd == "null") then / else > do`

| Line | Role | Condition | Fields read |
| --- | --- | --- | --- |
| 58 | title | `if (.not. i_exist .or. in_chg%cal_upd == "null") then / else > do` | `titldum` |
| 60 | data | `if (.not. i_exist .or. in_chg%cal_upd == "null") then / else > do` | `mcal` |
| 63 | header | `if (.not. i_exist .or. in_chg%cal_upd == "null") then / else > do` | `header` |
| 68 | data | `if (.not. i_exist .or. in_chg%cal_upd == "null") then / else > do > do i = 1, mcal` | `cal_upd(i)%name`, `cal_upd(i)%chg_typ`, `cal_upd(i)%val`, `cal_upd(i)%conds`, `cal_upd(i)%lyr1`, `cal_upd(i)%lyr2`, `cal_upd(i)%year1`, `cal_upd(i)%year2`, `cal_upd(i)%day1`, `cal_upd(i)%day2`, `nspu` |
| 75 | data | `if (.not. i_exist .or. in_chg%cal_upd == "null") then / else > do > do i = 1, mcal > if (nspu > 0) then` | `cal_upd(i)%name`, `cal_upd(i)%chg_typ`, `cal_upd(i)%val`, `cal_upd(i)%conds`, `cal_upd(i)%lyr1`, `cal_upd(i)%lyr2`, `cal_upd(i)%year1`, `cal_upd(i)%year2`, `cal_upd(i)%day1`, `cal_upd(i)%day2`, `cal_upd(i)%num_tot`, `(elem_cnt(isp), isp = 1, nspu)` |
| 94 | data | `if (.not. i_exist .or. in_chg%cal_upd == "null") then / else > do > do i = 1, mcal > if (nconds > 0) then > do icond = 1, nconds` | `range` |
| 97 | data | `if (.not. i_exist .or. in_chg%cal_upd == "null") then / else > do > do i = 1, mcal > if (nconds > 0) then > do icond = 1, nconds > if (range == "range") then` | `range`, `cal_upd(i)%cond(icond)%var`, `cal_upd(i)%val1`, `cal_upd(i)%val2` |
| 100 | data | `if (.not. i_exist .or. in_chg%cal_upd == "null") then / else > do > do i = 1, mcal > if (nconds > 0) then > do icond = 1, nconds > if (range == "range") then / else` | `cal_upd(i)%cond(icond)` |


## `carbon.bsn`

- Schema diff status: `['files.added']`
- Review needed: no
- Base schema presence: `{'resolved_sections': [], 'unresolved_sections': ['unresolved']}`
- Candidate schema presence: `{'resolved_sections': ['files'], 'unresolved_sections': []}`

### Base exact read evidence

_No exact base opened/read evidence found._

### Base related read evidence

- Procedure: `carbon_read`
- Reader: `carbon_read.f90`
- Match: reader procedure tokens match target, same reader procedure stem, shared filename tokens
- Resolved default filename(s): `basins_carbon.tes`
- Source filename expression(s): `basins_carbon.tes`
- Open: line 21, file expression `'basins_carbon.tes'`, parser value `basins_carbon.tes`, condition `if (.not. i_exist) then / else > do`

| Line | Role | Condition | Fields read |
| --- | --- | --- | --- |
| 22 | title | `if (.not. i_exist) then / else > do` | `titldum` |
| 24 | header | `if (.not. i_exist) then / else > do` | `header` |
| 27 | title | `if (.not. i_exist) then / else > do > do while (eof == 0)` | `titldum` |
| 33 | title | `if (.not. i_exist) then / else > do` | `titldum` |
| 35 | header | `if (.not. i_exist) then / else > do` | `header` |
| 39 | data | `if (.not. i_exist) then / else > do > do icarb = 1, imax` | `cbn_tes` |


### Candidate exact read evidence

- Procedure: `carbon_bsn_read`
- Reader: `carbon_bsn_read.f90`
- Match: exact_filename
- Resolved default filename(s): `carbon.bsn`
- Source filename expression(s): `in_basin%carbon_bsn`, `carbon.bsn`
- Open: line 57, file expression `in_basin%carbon_bsn`, parser value `carbon.bsn`, condition `None`

| Line | Role | Condition | Fields read |
| --- | --- | --- | --- |
| 66 | title | `None` | `titldum` |
| 67 | header | `None` | `header` |
| 69 | data | `None` | `org_frac%frac_seq`, `org_frac%frac_hum_microb`, `org_frac%frac_hum_slow`, `org_frac%frac_hum_passive`, `cb_wtr_coef%prmt_21`, `cb_wtr_coef%prmt_44`, `till_eff_days`, `man_coef%rtof`, `bio_consf`, `till_consf`, `org_con%tmpf`, `org_con%watf`, `org_con%tn`, `org_con%top`, `org_con%tx`, `bmix_a`, `bmix_b`, `bmix_c`, `tillmix_a`, `tillmix_b`, `tillmix_c`, `photo_degrade_factor`, `n_act_frac`, `cnr_cap`, `cnr_ref`, `cpr_cap`, `cpr_ref`, `mathers_int` |


## `cell_sol.gw`

- Schema diff status: `['runtime_arity.added']`
- Review needed: no
- Base schema presence: `{'resolved_sections': [], 'unresolved_sections': ['runtime_arity_unresolved']}`
- Candidate schema presence: `{'resolved_sections': ['runtime_arity'], 'unresolved_sections': []}`

### Base exact read evidence

_No exact base opened/read evidence found._

### Candidate exact read evidence

- Procedure: `gwflow_read`
- Reader: `gwflow_read.f90`
- Match: exact_filename
- Resolved default filename(s): `cell_sol.gw`
- Source filename expression(s): `cell_sol.gw`
- Open: line 1645, file expression `'cell_sol.gw'`, parser value `cell_sol.gw`, condition `if(gw_solute_flag == 1) then > if(i_exist) then > if(i_exist) then`

| Line | Role | Condition | Fields read |
| --- | --- | --- | --- |
| 1646 | header | `if(gw_solute_flag == 1) then > if(i_exist) then > if(i_exist) then` | `header` |
| 1647 | header | `if(gw_solute_flag == 1) then > if(i_exist) then > if(i_exist) then` | `header` |
| 1649 | data | `if(gw_solute_flag == 1) then > if(i_exist) then > if(i_exist) then > do i=1,ncell` | `cell_id`, `(gwsol_state(i)%solute(s)%conc,s=1,gw_nsolute)` |
| 1705 | data | `if(gw_solute_flag == 1) then > if(i_exist) then > if(gwsol_cons == 1) then` | _no fields captured_ |
| 1708 | data | `if(gw_solute_flag == 1) then > if(i_exist) then > if(gwsol_cons == 1) then > if(grid_type == "unstructured") then` | `(cell_int(i),i=1,ncell)` |
| 1720 | data | `if(gw_solute_flag == 1) then > if(i_exist) then > if(gwsol_cons == 1) then > if(grid_type == "unstructured") then / elseif(grid_type == "structured") then > do i=1,grid_nrow` | `(grid_int(i,j),j=1,grid_ncol)` |
| 1745 | header | `if(gw_solute_flag == 1) then > if(i_exist) then > if(gwsol_cons == 1) then > do n=1,num_geol_shale` | `header` |
| 1747 | data | `if(gw_solute_flag == 1) then > if(i_exist) then > if(gwsol_cons == 1) then > do n=1,num_geol_shale > if(grid_type == "unstructured") then` | `(cell_int(i),i=1,ncell)` |
| 1763 | data | `if(gw_solute_flag == 1) then > if(i_exist) then > if(gwsol_cons == 1) then > do n=1,num_geol_shale > if(grid_type == "unstructured") then / elseif(grid_type == "structured") then > do i=1,grid_nrow` | `(grid_int(i,j),j=1,grid_ncol)` |
| 1785 | header | `if(gw_solute_flag == 1) then > if(i_exist) then > if(gwsol_cons == 1) then` | `header` |
| 1787 | data | `if(gw_solute_flag == 1) then > if(i_exist) then > if(gwsol_cons == 1) then > if(grid_type == "unstructured") then` | `(cell_int(i),i=1,ncell)` |
| 1803 | data | `if(gw_solute_flag == 1) then > if(i_exist) then > if(gwsol_cons == 1) then > if(grid_type == "unstructured") then / elseif(grid_type == "structured") then > do i=1,grid_nrow` | `(grid_int(i,j),j=1,grid_ncol)` |


## `cells.gw`

- Schema diff status: `['files.added']`
- Review needed: no
- Base schema presence: `{'resolved_sections': [], 'unresolved_sections': ['unresolved']}`
- Candidate schema presence: `{'resolved_sections': ['files'], 'unresolved_sections': []}`

### Base exact read evidence

_No exact base opened/read evidence found._

### Candidate exact read evidence

- Procedure: `gwflow_read`
- Reader: `gwflow_read.f90`
- Match: exact_filename
- Resolved default filename(s): `cells.gw`
- Source filename expression(s): `cells.gw`, `unit_split_fields(1)`, `unit_split_fields(3)`, `unit_split_fields(4)`, `unit_split_fields(5)`, `unit_split_fields(6)`, `unit_split_fields(7)`, `unit_split_fields(8)`, `unit_split_fields(9)`, `unit_split_fields(10)`, `unit_split_fields(11)`, `unit_split_fields(12)`, `unit_split_fields(13)`, `unit_split_fields(14)`, `unit_split_fields(15)`, `unit_split_fields(16)`, `unit_split_fields(17)`, `unit_split_fields(18)`, `unit_split_fields(19)`, `unit_split_fields(20)`, `unit_split_fields(21)`, `unit_split_fields(22)`, `unit_split_fields(23)`
- Open: line 378, file expression `'cells.gw'`, parser value `cells.gw`, condition `None`

| Line | Role | Condition | Fields read |
| --- | --- | --- | --- |
| 379 | header | `None` | `header` |
| 380 | header | `None` | `header` |
| 382 | data | `do i=1,ncell` | `split_line_buf` |
| 390 | data | `do i=1,ncell` | `cell_id_in` |
| 396 | data | `do i=1,ncell` | `cell_gis_id(i)` |
| 397 | data | `do i=1,ncell` | `gw_state(i)%stat` |
| 398 | data | `do i=1,ncell` | `gw_state(i)%elev` |
| 399 | data | `do i=1,ncell` | `gw_state(i)%thck` |
| 400 | data | `do i=1,ncell` | `K_zone` |
| 401 | data | `do i=1,ncell` | `Sy_zone` |
| 402 | data | `do i=1,ncell` | `delay(i)` |
| 403 | data | `do i=1,ncell` | `gw_state(i)%exdp` |
| 404 | data | `do i=1,ncell` | `gw_state(i)%init` |
| 405 | data | `do i=1,ncell` | `gw_state(i)%xcrd` |
| 406 | data | `do i=1,ncell` | `gw_state(i)%ycrd` |
| 407 | data | `do i=1,ncell` | `gw_state(i)%area` |
| 417 | data | `do i=1,ncell > if(split_nf >= 15 .and. trim(split_fields(15)) /= 'null') then` | `cell_strK_over(i)` |
| 421 | data | `do i=1,ncell > if(split_nf >= 16 .and. trim(split_fields(16)) /= 'null') then` | `cell_strthick_over(i)` |
| 425 | data | `do i=1,ncell > if(split_nf >= 17 .and. trim(split_fields(17)) /= 'null') then` | `bc_type_array(i)` |
| 428 | data | `do i=1,ncell > if(split_nf >= 18 .and. trim(split_fields(18)) /= 'null') then` | `cell_tile_depth_over(i)` |
| 432 | data | `do i=1,ncell > if(split_nf >= 19 .and. trim(split_fields(19)) /= 'null') then` | `cell_tile_area_over(i)` |
| 436 | data | `do i=1,ncell > if(split_nf >= 20 .and. trim(split_fields(20)) /= 'null') then` | `cell_tile_K_over(i)` |
| 440 | data | `do i=1,ncell > if(split_nf >= 21 .and. trim(split_fields(21)) /= 'null') then` | `cell_row(i)` |
| 443 | data | `do i=1,ncell > if(split_nf >= 22 .and. trim(split_fields(22)) /= 'null') then` | `cell_col(i)` |
| 446 | data | `do i=1,ncell > if(split_nf >= 23 .and. trim(split_fields(23)) /= 'null') then` | `cell_init_temp(i)` |


## `chancell.gw`

- Schema diff status: `['files.added']`
- Review needed: no
- Base schema presence: `{'resolved_sections': [], 'unresolved_sections': ['unresolved']}`
- Candidate schema presence: `{'resolved_sections': ['files'], 'unresolved_sections': []}`

### Base exact read evidence

_No exact base opened/read evidence found._

### Candidate exact read evidence

- Procedure: `basin_read_objs`
- Reader: `basin_read_objs.f90`
- Match: exact_filename
- Resolved default filename(s): `chancell.gw`
- Source filename expression(s): `chancell.gw`
- Open: line 52, file expression `'chancell.gw'`, parser value `chancell.gw`, condition `if(bsn_cc%gwflow == 1 ) then > if(i_exist) then > if(sp_ob%gwflow == 0) then`

| Line | Role | Condition | Fields read |
| --- | --- | --- | --- |
| 53 | header | `if(bsn_cc%gwflow == 1 ) then > if(i_exist) then > if(sp_ob%gwflow == 0) then` | `header` |
| 55 | data | `if(bsn_cc%gwflow == 1 ) then > if(i_exist) then > if(sp_ob%gwflow == 0) then > if(eof == 0) then` | _no fields captured_ |
| 56 | header | `if(bsn_cc%gwflow == 1 ) then > if(i_exist) then > if(sp_ob%gwflow == 0) then > if(eof == 0) then` | `header` |
| 62 | data | `if(bsn_cc%gwflow == 1 ) then > if(i_exist) then > if(sp_ob%gwflow == 0) then > if(eof == 0) then > do while (eof == 0)` | `riv_id` |

- Procedure: `gwflow_chan_read`
- Reader: `gwflow_chan_read.f90`
- Match: exact_filename
- Resolved default filename(s): `chancell.gw`
- Source filename expression(s): `chancell.gw`, `unit_fields(1)`, `unit_fields(2)`, `unit_fields(3)`, `unit_fields(4)`, `unit_fields(5)`
- Open: line 34, file expression `'chancell.gw'`, parser value `chancell.gw`, condition `None`

| Line | Role | Condition | Fields read |
| --- | --- | --- | --- |
| 52 | data | `None` | _no fields captured_ |
| 53 | data | `None` | _no fields captured_ |
| 56 | data | `do k=1,num_chancells` | `line_buf` |
| 58 | data | `do k=1,num_chancells` | `cell_id` |
| 59 | data | `do k=1,num_chancells` | `bed_elev` |
| 60 | data | `do k=1,num_chancells` | `channel` |
| 61 | data | `do k=1,num_chancells` | `chan_length` |
| 62 | data | `do k=1,num_chancells` | `chan_zone` |


## `cs_atmo.cli`

- Schema diff status: `['runtime_arity.changed']`
- Review needed: no
- Base schema presence: `{'resolved_sections': ['runtime_arity'], 'unresolved_sections': []}`
- Candidate schema presence: `{'resolved_sections': ['runtime_arity'], 'unresolved_sections': []}`

### Base exact read evidence

- Procedure: `cli_read_atmodep_cs`
- Reader: `cli_read_atmodep_cs.f90`
- Match: exact_filename
- Resolved default filename(s): `cs_atmo.cli`
- Source filename expression(s): `cs_atmo.cli`
- Open: line 37, file expression `'cs_atmo.cli'`, parser value `cs_atmo.cli`, condition `if(cs_db%num_cs > 0) then > if(i_exist) then`

| Line | Role | Condition | Fields read |
| --- | --- | --- | --- |
| 38 | data | `if(cs_db%num_cs > 0) then > if(i_exist) then` | _no fields captured_ |
| 39 | data | `if(cs_db%num_cs > 0) then > if(i_exist) then` | _no fields captured_ |
| 40 | data | `if(cs_db%num_cs > 0) then > if(i_exist) then` | _no fields captured_ |
| 53 | data | `if(cs_db%num_cs > 0) then > if(i_exist) then > do iadep = 1, atmodep_cont%num_sta > if (atmodep_cont%timestep == "aa") then` | `station_name` |
| 56 | data | `if(cs_db%num_cs > 0) then > if(i_exist) then > do iadep = 1, atmodep_cont%num_sta > if (atmodep_cont%timestep == "aa") then > do ics=1,cs_db%num_cs` | `atmodep_cs(iadep)%cs(ics)%rf` |
| 60 | data | `if(cs_db%num_cs > 0) then > if(i_exist) then > do iadep = 1, atmodep_cont%num_sta > if (atmodep_cont%timestep == "aa") then > do ics=1,cs_db%num_cs` | `atmodep_cs(iadep)%cs(ics)%dry` |
| 66 | data | `if(cs_db%num_cs > 0) then > if(i_exist) then > do iadep = 1, atmodep_cont%num_sta > if (atmodep_cont%timestep == "mo") then` | `station_name` |
| 72 | data | `if(cs_db%num_cs > 0) then > if(i_exist) then > do iadep = 1, atmodep_cont%num_sta > if (atmodep_cont%timestep == "mo") then > do ics=1,cs_db%num_cs` | `(atmodep_cs(iadep)%cs(ics)%rfmo(imo),imo=1,atmodep_cont%num)` |
| 79 | data | `if(cs_db%num_cs > 0) then > if(i_exist) then > do iadep = 1, atmodep_cont%num_sta > if (atmodep_cont%timestep == "mo") then > do ics=1,cs_db%num_cs` | `(atmodep_cs(iadep)%cs(ics)%drymo(imo),imo=1,atmodep_cont%num)` |
| 85 | data | `if(cs_db%num_cs > 0) then > if(i_exist) then > do iadep = 1, atmodep_cont%num_sta > if (atmodep_cont%timestep == "yr") then` | `station_name` |
| 91 | data | `if(cs_db%num_cs > 0) then > if(i_exist) then > do iadep = 1, atmodep_cont%num_sta > if (atmodep_cont%timestep == "yr") then > do ics=1,cs_db%num_cs` | `(atmodep_cs(iadep)%cs(ics)%rfyr(iyr),iyr=1,atmodep_cont%num)` |
| 98 | data | `if(cs_db%num_cs > 0) then > if(i_exist) then > do iadep = 1, atmodep_cont%num_sta > if (atmodep_cont%timestep == "yr") then > do ics=1,cs_db%num_cs` | `(atmodep_cs(iadep)%cs(ics)%dryyr(iyr),iyr=1,atmodep_cont%num)` |


### Candidate exact read evidence

- Procedure: `cli_read_atmodep_cs`
- Reader: `cli_read_atmodep_cs.f90`
- Match: exact_filename
- Resolved default filename(s): `cs_atmo.cli`
- Source filename expression(s): `cs_atmo.cli`
- Open: line 32, file expression `'cs_atmo.cli'`, parser value `cs_atmo.cli`, condition `if(cs_db%num_cs > 0) then > if(i_exist) then`

| Line | Role | Condition | Fields read |
| --- | --- | --- | --- |
| 33 | data | `if(cs_db%num_cs > 0) then > if(i_exist) then` | _no fields captured_ |
| 34 | data | `if(cs_db%num_cs > 0) then > if(i_exist) then` | _no fields captured_ |
| 35 | data | `if(cs_db%num_cs > 0) then > if(i_exist) then` | _no fields captured_ |
| 48 | data | `if(cs_db%num_cs > 0) then > if(i_exist) then > do iadep = 1, atmodep_cont%num_sta > if (atmodep_cont%timestep == "aa") then` | `station_name` |
| 51 | data | `if(cs_db%num_cs > 0) then > if(i_exist) then > do iadep = 1, atmodep_cont%num_sta > if (atmodep_cont%timestep == "aa") then > do ics=1,cs_db%num_cs` | `atmodep_cs(iadep)%cs(ics)%rf` |
| 55 | data | `if(cs_db%num_cs > 0) then > if(i_exist) then > do iadep = 1, atmodep_cont%num_sta > if (atmodep_cont%timestep == "aa") then > do ics=1,cs_db%num_cs` | `atmodep_cs(iadep)%cs(ics)%dry` |
| 61 | data | `if(cs_db%num_cs > 0) then > if(i_exist) then > do iadep = 1, atmodep_cont%num_sta > if (atmodep_cont%timestep == "mo") then` | `station_name` |
| 67 | data | `if(cs_db%num_cs > 0) then > if(i_exist) then > do iadep = 1, atmodep_cont%num_sta > if (atmodep_cont%timestep == "mo") then > do ics=1,cs_db%num_cs` | `(atmodep_cs(iadep)%cs(ics)%rfmo(imo),imo=1,atmodep_cont%num)` |
| 74 | data | `if(cs_db%num_cs > 0) then > if(i_exist) then > do iadep = 1, atmodep_cont%num_sta > if (atmodep_cont%timestep == "mo") then > do ics=1,cs_db%num_cs` | `(atmodep_cs(iadep)%cs(ics)%drymo(imo),imo=1,atmodep_cont%num)` |
| 80 | data | `if(cs_db%num_cs > 0) then > if(i_exist) then > do iadep = 1, atmodep_cont%num_sta > if (atmodep_cont%timestep == "yr") then` | `station_name` |
| 86 | data | `if(cs_db%num_cs > 0) then > if(i_exist) then > do iadep = 1, atmodep_cont%num_sta > if (atmodep_cont%timestep == "yr") then > do ics=1,cs_db%num_cs` | `(atmodep_cs(iadep)%cs(ics)%rfyr(iyr),iyr=1,atmodep_cont%num)` |
| 93 | data | `if(cs_db%num_cs > 0) then > if(i_exist) then > do iadep = 1, atmodep_cont%num_sta > if (atmodep_cont%timestep == "yr") then > do ics=1,cs_db%num_cs` | `(atmodep_cs(iadep)%cs(ics)%dryyr(iyr),iyr=1,atmodep_cont%num)` |


## `cs_recall.rec`

- Schema diff status: `['runtime_arity.changed']`
- Review needed: no
- Base schema presence: `{'resolved_sections': ['runtime_arity'], 'unresolved_sections': []}`
- Candidate schema presence: `{'resolved_sections': ['runtime_arity'], 'unresolved_sections': []}`

### Base exact read evidence

- Procedure: `recall_read_cs`
- Reader: `recall_read_cs.f90`
- Match: exact_filename
- Resolved default filename(s): `cs_recall.rec`
- Source filename expression(s): `cs_recall.rec`
- Open: line 47, file expression `"cs_recall.rec"`, parser value `cs_recall.rec`, condition `if (i_exist .or. in_rec%recall_rec /= "null") then > do`

| Line | Role | Condition | Fields read |
| --- | --- | --- | --- |
| 48 | title | `if (i_exist .or. in_rec%recall_rec /= "null") then > do` | `titldum` |
| 50 | header | `if (i_exist .or. in_rec%recall_rec /= "null") then > do` | `header` |
| 56 | data | `if (i_exist .or. in_rec%recall_rec /= "null") then > do > do while (eof == 0)` | `i` |
| 102 | title | `if (i_exist .or. in_rec%recall_rec /= "null") then > do` | `titldum` |
| 104 | header | `if (i_exist .or. in_rec%recall_rec /= "null") then > do` | `header` |
| 109 | data | `if (i_exist .or. in_rec%recall_rec /= "null") then > do > do ii = 1, imax` | `i` |
| 112 | data | `if (i_exist .or. in_rec%recall_rec /= "null") then > do > do ii = 1, imax` | `k`, `rec_cs(i)%name`, `rec_cs(i)%typ`, `rec_cs(i)%filename` |


### Candidate exact read evidence

- Procedure: `recall_read_cs`
- Reader: `recall_read_cs.f90`
- Match: exact_filename
- Resolved default filename(s): `cs_recall.rec`
- Source filename expression(s): `cs_recall.rec`
- Open: line 43, file expression `"cs_recall.rec"`, parser value `cs_recall.rec`, condition `if (i_exist .or. in_rec%recall_rec /= "null") then > do`

| Line | Role | Condition | Fields read |
| --- | --- | --- | --- |
| 44 | title | `if (i_exist .or. in_rec%recall_rec /= "null") then > do` | `titldum` |
| 46 | header | `if (i_exist .or. in_rec%recall_rec /= "null") then > do` | `header` |
| 52 | data | `if (i_exist .or. in_rec%recall_rec /= "null") then > do > do while (eof == 0)` | `i` |
| 98 | title | `if (i_exist .or. in_rec%recall_rec /= "null") then > do` | `titldum` |
| 100 | header | `if (i_exist .or. in_rec%recall_rec /= "null") then > do` | `header` |
| 105 | data | `if (i_exist .or. in_rec%recall_rec /= "null") then > do > do ii = 1, imax` | `i` |
| 108 | data | `if (i_exist .or. in_rec%recall_rec /= "null") then > do > do ii = 1, imax` | `k`, `rec_cs(i)%name`, `rec_cs(i)%typ`, `rec_cs(i)%filename` |


## `dr_path.del`

- Schema diff status: `['runtime_arity.changed']`
- Review needed: no
- Base schema presence: `{'resolved_sections': ['runtime_arity'], 'unresolved_sections': []}`
- Candidate schema presence: `{'resolved_sections': ['runtime_arity'], 'unresolved_sections': []}`

### Base exact read evidence

- Procedure: `dr_path_read`
- Reader: `dr_read_path.f90`
- Match: exact_filename
- Resolved default filename(s): `dr_path.del`
- Source filename expression(s): `in_delr%path`, `dr_path.del`
- Open: line 32, file expression `in_delr%path`, parser value `dr_path.del`, condition `if (i_exist .or. in_delr%path /= "null") then > do`

| Line | Role | Condition | Fields read |
| --- | --- | --- | --- |
| 33 | title | `if (i_exist .or. in_delr%path /= "null") then > do` | `titldum` |
| 35 | header | `if (i_exist .or. in_delr%path /= "null") then > do` | `header` |
| 39 | title | `if (i_exist .or. in_delr%path /= "null") then > do > do while (eof == 0)` | `titldum` |
| 53 | title | `if (i_exist .or. in_delr%path /= "null") then > do` | `titldum` |
| 55 | header | `if (i_exist .or. in_delr%path /= "null") then > do` | `header` |
| 60 | title | `if (i_exist .or. in_delr%path /= "null") then > do > do ii = 1, db_mx%dr_path` | `titldum` |
| 63 | data | `if (i_exist .or. in_delr%path /= "null") then > do > do ii = 1, db_mx%dr_path` | `dr_path_name(ii)`, `(dr_path(ii)%path(ipath), ipath = 1, cs_db%num_paths)` |


### Candidate exact read evidence

- Procedure: `dr_path_read`
- Reader: `dr_path_read.f90`
- Match: exact_filename
- Resolved default filename(s): `dr_path.del`
- Source filename expression(s): `in_delr%path`, `dr_path.del`
- Open: line 32, file expression `in_delr%path`, parser value `dr_path.del`, condition `if (i_exist .or. in_delr%path /= "null") then > do`

| Line | Role | Condition | Fields read |
| --- | --- | --- | --- |
| 33 | title | `if (i_exist .or. in_delr%path /= "null") then > do` | `titldum` |
| 35 | header | `if (i_exist .or. in_delr%path /= "null") then > do` | `header` |
| 39 | title | `if (i_exist .or. in_delr%path /= "null") then > do > do while (eof == 0)` | `titldum` |
| 53 | title | `if (i_exist .or. in_delr%path /= "null") then > do` | `titldum` |
| 55 | header | `if (i_exist .or. in_delr%path /= "null") then > do` | `header` |
| 60 | title | `if (i_exist .or. in_delr%path /= "null") then > do > do ii = 1, db_mx%dr_path` | `titldum` |
| 63 | data | `if (i_exist .or. in_delr%path /= "null") then > do > do ii = 1, db_mx%dr_path` | `dr_path_name(ii)`, `(dr_path(ii)%path(ipath), ipath = 1, cs_db%num_paths)` |


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
- Source filename expression(s): `in_cond%dtbl_flo`, `flo_con.dtl`
- Open: line 31, file expression `in_cond%dtbl_flo`, parser value `flo_con.dtl`, condition `if (.not. i_exist .or. in_cond%dtbl_flo == "null") then / else > do`

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
| 79 | data | `if (.not. i_exist .or. in_cond%dtbl_flo == "null") then / else > do > do i = 1, mdtbl` | _no fields captured_ |


### Candidate exact read evidence

- Procedure: `dtbl_flocon_read`
- Reader: `dtbl_flocon_read.f90`
- Match: exact_filename
- Resolved default filename(s): `flo_con.dtl`
- Source filename expression(s): `in_cond%dtbl_flo`, `flo_con.dtl`
- Open: line 31, file expression `in_cond%dtbl_flo`, parser value `flo_con.dtl`, condition `if (.not. i_exist .or. in_cond%dtbl_flo == "null") then / else > do`

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


## `floodplain.gw`

- Schema diff status: `['files.added']`
- Review needed: no
- Base schema presence: `{'resolved_sections': [], 'unresolved_sections': ['unresolved']}`
- Candidate schema presence: `{'resolved_sections': ['files'], 'unresolved_sections': []}`

### Base exact read evidence

_No exact base opened/read evidence found._

### Base related read evidence

- Procedure: `gwflow_read`
- Reader: `gwflow_read.f90`
- Match: shared filename tokens, similar opened filename/expression
- Resolved default filename(s): `gwflow.floodplain`
- Source filename expression(s): `gwflow.floodplain`
- Open: line 1134, file expression `'gwflow.floodplain'`, parser value `gwflow.floodplain`, condition `if (gw_fp_flag == 1) then > if(i_exist) then`

| Line | Role | Condition | Fields read |
| --- | --- | --- | --- |
| 1135 | header | `if (gw_fp_flag == 1) then > if(i_exist) then` | `header` |
| 1136 | data | `if (gw_fp_flag == 1) then > if(i_exist) then` | `gw_fp_ncells` |
| 1144 | header | `if (gw_fp_flag == 1) then > if(i_exist) then` | `header` |
| 1146 | data | `if (gw_fp_flag == 1) then > if(i_exist) then > do i=1,gw_fp_ncells` | `gw_fp_cellid(i)`, `gw_fp_chanid(i)`, `gw_fp_K(i)`, `gw_fp_area(i)` |

- Procedure: `gwflow_read`
- Reader: `gwflow_read.f90`
- Match: shared filename tokens, similar opened filename/expression
- Source filename expression(s): `gwflow_flux_floodplain`
- Open: line 1181, file expression `'gwflow_flux_floodplain'`, parser value `gwflow_flux_floodplain`, condition `if (gw_fp_flag == 1) then > if(i_exist) then`
- Reads: _none captured_


### Candidate exact read evidence

- Procedure: `gwflow_read`
- Reader: `gwflow_read.f90`
- Match: exact_filename
- Resolved default filename(s): `floodplain.gw`
- Source filename expression(s): `floodplain.gw`
- Open: line 1157, file expression `'floodplain.gw'`, parser value `floodplain.gw`, condition `if(gw_fp_flag == 1) then > if(i_exist) then`

| Line | Role | Condition | Fields read |
| --- | --- | --- | --- |
| 1158 | header | `if(gw_fp_flag == 1) then > if(i_exist) then` | `header` |
| 1159 | data | `if(gw_fp_flag == 1) then > if(i_exist) then` | `gw_fp_ncells` |
| 1167 | header | `if(gw_fp_flag == 1) then > if(i_exist) then` | `header` |
| 1169 | data | `if(gw_fp_flag == 1) then > if(i_exist) then > do i=1,gw_fp_ncells` | `gw_fp_cellid(i)`, `gw_fp_chanid(i)`, `gw_fp_K(i)`, `gw_fp_area(i)` |


## `gwflow_canal.con`

- Schema diff status: `['runtime_arity.added']`
- Review needed: no
- Base schema presence: `{'resolved_sections': [], 'unresolved_sections': ['runtime_arity_unresolved']}`
- Candidate schema presence: `{'resolved_sections': ['runtime_arity'], 'unresolved_sections': []}`

### Base exact read evidence

_No exact base opened/read evidence found._

### Base related read evidence

- Procedure: `gwflow_read`
- Reader: `gwflow_read.f90`
- Match: shared filename tokens, similar opened filename/expression
- Resolved default filename(s): `gwflow.canals`
- Source filename expression(s): `gwflow.canals`
- Open: line 1194, file expression `'gwflow.canals'`, parser value `gwflow.canals`, condition `if (gw_canal_flag == 1) then > if(i_exist) then`

| Line | Role | Condition | Fields read |
| --- | --- | --- | --- |
| 1195 | header | `if (gw_canal_flag == 1) then > if(i_exist) then` | `header` |
| 1200 | data | `if (gw_canal_flag == 1) then > if(i_exist) then` | `gw_ncanal` |
| 1201 | data | `if (gw_canal_flag == 1) then > if(i_exist) then` | _no fields captured_ |
| 1205 | data | `if (gw_canal_flag == 1) then > if(i_exist) then > do i=1,gw_ncanal` | `canal`, `channel`, `width`, `depth`, `thick`, `day_beg`, `day_end` |
| 1229 | header | `if (gw_canal_flag == 1) then > if(i_exist) then` | `header` |
| 1230 | data | `if (gw_canal_flag == 1) then > if(i_exist) then` | `gw_ncanal` |
| 1231 | data | `if (gw_canal_flag == 1) then > if(i_exist) then` | _no fields captured_ |
| 1233 | data | `if (gw_canal_flag == 1) then > if(i_exist) then > do i=1,gw_ncanal` | `canal`, `channel`, `width`, `depth`, `thick`, `day_beg`, `day_end` |
| 1245 | header | `if (gw_canal_flag == 1) then > if(i_exist) then` | `header` |
| 1246 | data | `if (gw_canal_flag == 1) then > if(i_exist) then` | `num_canalK_zones` |
| 1249 | data | `if (gw_canal_flag == 1) then > if(i_exist) then > do i=1,num_canalK_zones` | `dum1`, `canalK_zones(i)` |
| 1253 | header | `if (gw_canal_flag == 1) then > if(i_exist) then` | `header` |
| 1254 | data | `if (gw_canal_flag == 1) then > if(i_exist) then` | `gw_canal_ncells` |
| 1255 | header | `if (gw_canal_flag == 1) then > if(i_exist) then` | `header` |
| 1257 | data | `if (gw_canal_flag == 1) then > if(i_exist) then > do i=1,gw_canal_ncells` | `cell_num`, `canal` |
| 1265 | header | `if (gw_canal_flag == 1) then > if(i_exist) then` | `header` |
| 1266 | data | `if (gw_canal_flag == 1) then > if(i_exist) then` | `gw_ncanal` |
| 1267 | header | `if (gw_canal_flag == 1) then > if(i_exist) then` | `header` |
| 1269 | data | `if (gw_canal_flag == 1) then > if(i_exist) then > do i=1,gw_ncanal` | _no fields captured_ |
| 1271 | header | `if (gw_canal_flag == 1) then > if(i_exist) then` | `header` |
| 1272 | data | `if (gw_canal_flag == 1) then > if(i_exist) then` | `num_canalK_zones` |
| 1274 | data | `if (gw_canal_flag == 1) then > if(i_exist) then > do i=1,num_canalK_zones` | _no fields captured_ |
| 1277 | header | `if (gw_canal_flag == 1) then > if(i_exist) then` | `header` |
| 1280 | data | `if (gw_canal_flag == 1) then > if(i_exist) then` | `gw_canal_ncells` |
| 1281 | header | `if (gw_canal_flag == 1) then > if(i_exist) then` | `header` |
| 1283 | data | `if (gw_canal_flag == 1) then > if(i_exist) then > do i=1,gw_canal_ncells` | `cell_num`, `canal`, `length`, `stage`, `K_zone` |
| 1298 | header | `if (gw_canal_flag == 1) then > if(i_exist) then` | `header` |
| 1299 | data | `if (gw_canal_flag == 1) then > if(i_exist) then` | `gw_ncanal` |
| 1300 | header | `if (gw_canal_flag == 1) then > if(i_exist) then` | `header` |
| 1302 | data | `if (gw_canal_flag == 1) then > if(i_exist) then > do i=1,gw_ncanal` | _no fields captured_ |
| 1304 | header | `if (gw_canal_flag == 1) then > if(i_exist) then` | `header` |
| 1305 | data | `if (gw_canal_flag == 1) then > if(i_exist) then` | `num_canalK_zones` |
| 1307 | data | `if (gw_canal_flag == 1) then > if(i_exist) then > do i=1,num_canalK_zones` | _no fields captured_ |
| 1309 | header | `if (gw_canal_flag == 1) then > if(i_exist) then` | `header` |
| 1310 | data | `if (gw_canal_flag == 1) then > if(i_exist) then` | `gw_canal_ncells` |
| 1311 | header | `if (gw_canal_flag == 1) then > if(i_exist) then` | `header` |
| 1314 | data | `if (gw_canal_flag == 1) then > if(i_exist) then > do i=1,gw_canal_ncells` | `cell_num`, `canal`, `length`, `stage`, `K_zone` |

- Procedure: `gwflow_chan_read`
- Reader: `gwflow_chan_read.f90`
- Match: shared filename tokens, similar opened filename/expression
- Resolved default filename(s): `gwflow.con`
- Source filename expression(s): `gwflow.con`
- Open: line 36, file expression `'gwflow.con'`, parser value `gwflow.con`, condition `None`
- Reads: _none captured_

- Procedure: `gwflow_read`
- Reader: `gwflow_read.f90`
- Match: shared filename tokens, similar opened filename/expression
- Source filename expression(s): `gwflow_flux_canl`
- Open: line 1340, file expression `'gwflow_flux_canl'`, parser value `gwflow_flux_canl`, condition `if (gw_canal_flag == 1) then > if(i_exist) then`
- Reads: _none captured_

- Procedure: `gwflow_read`
- Reader: `gwflow_read.f90`
- Match: shared filename tokens, similar opened filename/expression
- Source filename expression(s): `gwflow_mass_canl`
- Open: line 1647, file expression `'gwflow_mass_canl'`, parser value `gwflow_mass_canl`, condition `if (gw_solute_flag == 1) then > if(i_exist) then > if (gw_canal_flag == 1) then`
- Reads: _none captured_

- Procedure: `gwflow_chan_read`
- Reader: `gwflow_chan_read.f90`
- Match: shared filename tokens, similar opened filename/expression
- Resolved default filename(s): `gwflow.chancells`
- Source filename expression(s): `gwflow.chancells`
- Open: line 35, file expression `'gwflow.chancells'`, parser value `gwflow.chancells`, condition `None`

| Line | Role | Condition | Fields read |
| --- | --- | --- | --- |
| 50 | data | `None` | _no fields captured_ |
| 51 | data | `None` | _no fields captured_ |
| 52 | data | `None` | _no fields captured_ |
| 54 | data | `do k=1,num_chancells` | `cell_ID`, `bed_elev`, `channel`, `chan_length`, `chan_zone` |


### Candidate exact read evidence

- Procedure: `gwflow_read`
- Reader: `gwflow_read.f90`
- Match: exact_filename
- Resolved default filename(s): `gwflow_canal.con`
- Source filename expression(s): `gwflow_canal.con`
- Open: line 1254, file expression `'gwflow_canal.con'`, parser value `gwflow_canal.con`, condition `if(gw_canal_flag == 1) then > if(i_exist) then`

| Line | Role | Condition | Fields read |
| --- | --- | --- | --- |
| 1255 | header | `if(gw_canal_flag == 1) then > if(i_exist) then` | `header` |
| 1262 | data | `if(gw_canal_flag == 1) then > if(i_exist) then > do` | `canal_id`, `obj_tot` |
| 1305 | header | `if(gw_canal_flag == 1) then > if(i_exist) then` | `header` |
| 1310 | data | `if(gw_canal_flag == 1) then > if(i_exist) then > do` | `canal_id`, `obj_tot` |
| 1315 | data | `if(gw_canal_flag == 1) then > if(i_exist) then > do` | `canal_id`, `obj_tot`, `(con_row_buf(j),j=1,obj_tot*3)` |


## `hrucell.gw`

- Schema diff status: `['files.added']`
- Review needed: no
- Base schema presence: `{'resolved_sections': [], 'unresolved_sections': ['unresolved']}`
- Candidate schema presence: `{'resolved_sections': ['files'], 'unresolved_sections': []}`

### Base exact read evidence

_No exact base opened/read evidence found._

### Base related read evidence

- Procedure: `gwflow_read`
- Reader: `gwflow_read.f90`
- Match: shared filename tokens, similar opened filename/expression
- Resolved default filename(s): `gwflow.hrucell`
- Source filename expression(s): `gwflow.hrucell`
- Open: line 1754, file expression `'gwflow.hrucell'`, parser value `gwflow.hrucell`, condition `if (lsu_cells_link == 1) then / else > if (nat_model == 1) then`

| Line | Role | Condition | Fields read |
| --- | --- | --- | --- |
| 1755 | data | `if (lsu_cells_link == 1) then / else > if (nat_model == 1) then` | _no fields captured_ |
| 1756 | data | `if (lsu_cells_link == 1) then / else > if (nat_model == 1) then` | _no fields captured_ |
| 1757 | data | `if (lsu_cells_link == 1) then / else > if (nat_model == 1) then` | _no fields captured_ |
| 1759 | data | `if (lsu_cells_link == 1) then / else > if (nat_model == 1) then` | `nhru_connected` |
| 1763 | data | `if (lsu_cells_link == 1) then / else > if (nat_model == 1) then > do i=1,nhru_connected` | `hru_id` |
| 1767 | data | `if (lsu_cells_link == 1) then / else > if (nat_model == 1) then` | _no fields captured_ |
| 1768 | data | `if (lsu_cells_link == 1) then / else > if (nat_model == 1) then` | _no fields captured_ |
| 1782 | data | `if (lsu_cells_link == 1) then / else > if (nat_model == 1) then > do k=1,num_hru > if(hrus_connected(k).eq.1) then > do while (hru_id.eq.k)` | `hru_id`, `hru_area`, `hru_cells(k,cell_count)`, `poly_area` |
| 1795 | data | `if (lsu_cells_link == 1) then / else > if (nat_model == 1) then > do k=1,num_hru > if(hrus_connected(k).eq.1) then > do while (hru_id.eq.k)` | `hru_id` |


### Candidate exact read evidence

- Procedure: `gwflow_read`
- Reader: `gwflow_read.f90`
- Match: exact_filename
- Resolved default filename(s): `hrucell.gw`
- Source filename expression(s): `hrucell.gw`
- Open: line 2105, file expression `'hrucell.gw'`, parser value `hrucell.gw`, condition `if(lsu_cells_link == 1) then / else`

| Line | Role | Condition | Fields read |
| --- | --- | --- | --- |
| 2106 | data | `if(lsu_cells_link == 1) then / else` | _no fields captured_ |
| 2107 | data | `if(lsu_cells_link == 1) then / else` | _no fields captured_ |
| 2115 | data | `if(lsu_cells_link == 1) then / else > do` | `hru_id` |
| 2127 | data | `if(lsu_cells_link == 1) then / else` | _no fields captured_ |
| 2128 | data | `if(lsu_cells_link == 1) then / else` | _no fields captured_ |
| 2142 | data | `if(lsu_cells_link == 1) then / else > do k=1,sp_ob%hru > if(hrus_connected(k).eq.1) then > do while (hru_id.eq.k)` | `hru_id`, `hru_area`, `hru_cells(k,cell_count)`, `poly_area` |
| 2155 | data | `if(lsu_cells_link == 1) then / else > do k=1,sp_ob%hru > if(hrus_connected(k).eq.1) then > do while (hru_id.eq.k)` | `hru_id` |


## `lsucell.gw`

- Schema diff status: `['files.added']`
- Review needed: no
- Base schema presence: `{'resolved_sections': [], 'unresolved_sections': ['unresolved']}`
- Candidate schema presence: `{'resolved_sections': ['files'], 'unresolved_sections': []}`

### Base exact read evidence

_No exact base opened/read evidence found._

### Base related read evidence

- Procedure: `gwflow_read`
- Reader: `gwflow_read.f90`
- Match: shared filename tokens, similar opened filename/expression
- Resolved default filename(s): `gwflow.lsucell`
- Source filename expression(s): `gwflow.lsucell`
- Open: line 1673, file expression `'gwflow.lsucell'`, parser value `gwflow.lsucell`, condition `if (lsu_cells_link == 1) then`

| Line | Role | Condition | Fields read |
| --- | --- | --- | --- |
| 1674 | header | `if (lsu_cells_link == 1) then` | `header` |
| 1676 | data | `if (lsu_cells_link == 1) then` | `nlsu` |
| 1677 | data | `if (lsu_cells_link == 1) then` | `nlsu_connected` |
| 1681 | data | `if (lsu_cells_link == 1) then > do i=1,nlsu_connected` | `lsu_id` |
| 1685 | header | `if (lsu_cells_link == 1) then` | `header` |
| 1686 | header | `if (lsu_cells_link == 1) then` | `header` |
| 1699 | data | `if (lsu_cells_link == 1) then > do k=1,nlsu > if(lsus_connected(k).eq.1) then > do while (lsu.eq.k)` | `lsu`, `lsu_area`, `lsu_cells(k,cell_count)`, `poly_area` |
| 1708 | data | `if (lsu_cells_link == 1) then > do k=1,nlsu > if(lsus_connected(k).eq.1) then > do while (lsu.eq.k)` | `lsu` |


### Candidate exact read evidence

- Procedure: `gwflow_read`
- Reader: `gwflow_read.f90`
- Match: exact_filename
- Resolved default filename(s): `lsucell.gw`
- Source filename expression(s): `lsucell.gw`
- Open: line 2032, file expression `'lsucell.gw'`, parser value `lsucell.gw`, condition `if(lsu_cells_link == 1) then`

| Line | Role | Condition | Fields read |
| --- | --- | --- | --- |
| 2033 | header | `if(lsu_cells_link == 1) then` | `header` |
| 2035 | data | `if(lsu_cells_link == 1) then` | `nlsu` |
| 2036 | data | `if(lsu_cells_link == 1) then` | `nlsu_connected` |
| 2040 | data | `if(lsu_cells_link == 1) then > do i=1,nlsu_connected` | `lsu_id` |
| 2044 | header | `if(lsu_cells_link == 1) then` | `header` |
| 2045 | header | `if(lsu_cells_link == 1) then` | `header` |
| 2055 | data | `if(lsu_cells_link == 1) then > do k=1,nlsu > if(lsus_connected(k).eq.1) then > do while (lsu.eq.k)` | `lsu` |
| 2056 | data | `if(lsu_cells_link == 1) then > do k=1,nlsu > if(lsus_connected(k).eq.1) then > do while (lsu.eq.k)` | `lsu` |
| 2065 | header | `if(lsu_cells_link == 1) then` | `header` |
| 2066 | data | `if(lsu_cells_link == 1) then` | `nlsu` |
| 2067 | data | `if(lsu_cells_link == 1) then` | `nlsu_connected` |
| 2069 | data | `if(lsu_cells_link == 1) then > do i=1,nlsu_connected` | `lsu_id` |
| 2071 | header | `if(lsu_cells_link == 1) then` | `header` |
| 2072 | header | `if(lsu_cells_link == 1) then` | `header` |
| 2085 | data | `if(lsu_cells_link == 1) then > do k=1,nlsu > if(lsus_connected(k).eq.1) then > do while (lsu.eq.k)` | `lsu`, `lsu_area`, `lsu_cells(k,cell_count)`, `poly_area` |
| 2094 | data | `if(lsu_cells_link == 1) then > do k=1,nlsu > if(lsus_connected(k).eq.1) then > do while (lsu.eq.k)` | `lsu` |


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
- Source filename expression(s): `in_cond%dtbl_lum`, `lum.dtl`
- Open: line 41, file expression `in_cond%dtbl_lum`, parser value `lum.dtl`, condition `if (.not. i_exist .or. in_cond%dtbl_lum == "null") then / else > do`

| Line | Role | Condition | Fields read |
| --- | --- | --- | --- |
| 42 | title | `if (.not. i_exist .or. in_cond%dtbl_lum == "null") then / else > do` | `titldum` |
| 44 | data | `if (.not. i_exist .or. in_cond%dtbl_lum == "null") then / else > do` | `mdtbl` |
| 46 | data | `if (.not. i_exist .or. in_cond%dtbl_lum == "null") then / else > do` | _no fields captured_ |
| 51 | header | `if (.not. i_exist .or. in_cond%dtbl_lum == "null") then / else > do > do i = 1, mdtbl` | `header` |
| 53 | data | `if (.not. i_exist .or. in_cond%dtbl_lum == "null") then / else > do > do i = 1, mdtbl` | `dtbl_lum(i)%name`, `dtbl_lum(i)%conds`, `dtbl_lum(i)%alts`, `dtbl_lum(i)%acts` |
| 65 | header | `if (.not. i_exist .or. in_cond%dtbl_lum == "null") then / else > do > do i = 1, mdtbl` | `header` |
| 68 | data | `if (.not. i_exist .or. in_cond%dtbl_lum == "null") then / else > do > do i = 1, mdtbl > do ic = 1, dtbl_lum(i)%conds` | `dtbl_lum(i)%cond(ic)`, `(dtbl_lum(i)%alt(ic,ial), ial = 1, dtbl_lum(i)%alts)` |
| 72 | data | `if (.not. i_exist .or. in_cond%dtbl_lum == "null") then / else > do > do i = 1, mdtbl > do ic = 1, dtbl_lum(i)%conds > if (dtbl_lum(i)%cond(ic)%var == "prob_unif") then` | `dtbl_lum(i)%cond(ic)%var`, `dtbl_lum(i)%frac_app` |
| 91 | header | `if (.not. i_exist .or. in_cond%dtbl_lum == "null") then / else > do > do i = 1, mdtbl` | `header` |
| 94 | data | `if (.not. i_exist .or. in_cond%dtbl_lum == "null") then / else > do > do i = 1, mdtbl > do iac = 1, dtbl_lum(i)%acts` | `dtbl_lum(i)%act(iac)`, `(dtbl_lum(i)%act_outcomes(iac,ial), ial = 1, dtbl_lum(i)%alts)` |


### Candidate exact read evidence

- Procedure: `dtbl_lum_read`
- Reader: `dtbl_lum_read.f90`
- Match: exact_filename
- Resolved default filename(s): `lum.dtl`
- Source filename expression(s): `in_cond%dtbl_lum`, `lum.dtl`
- Open: line 41, file expression `in_cond%dtbl_lum`, parser value `lum.dtl`, condition `if (.not. i_exist .or. in_cond%dtbl_lum == "null") then / else > do`

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


## `management.sch`

- Schema diff status: `['multi_record.changed']`
- Review needed: no
- Base schema presence: `{'resolved_sections': ['multi_record'], 'unresolved_sections': []}`
- Candidate schema presence: `{'resolved_sections': ['multi_record'], 'unresolved_sections': []}`

### Base exact read evidence

- Procedure: `mgt_read_mgtops`
- Reader: `mgt_read_mgtops.f90`
- Match: exact_filename
- Resolved default filename(s): `management.sch`
- Source filename expression(s): `in_lum%management_sch`, `management.sch`
- Open: line 31, file expression `in_lum%management_sch`, parser value `management.sch`, condition `if (.not. i_exist .or. in_lum%management_sch == "null") then / else > do`

| Line | Role | Condition | Fields read |
| --- | --- | --- | --- |
| 32 | title | `if (.not. i_exist .or. in_lum%management_sch == "null") then / else > do` | `titldum` |
| 34 | header | `if (.not. i_exist .or. in_lum%management_sch == "null") then / else > do` | `header` |
| 37 | data | `if (.not. i_exist .or. in_lum%management_sch == "null") then / else > do > do while (eof == 0)` | `titldum`, `nops`, `nauto` |
| 40 | title | `if (.not. i_exist .or. in_lum%management_sch == "null") then / else > do > do while (eof == 0) > do iauto = 1, nauto` | `titldum` |
| 44 | title | `if (.not. i_exist .or. in_lum%management_sch == "null") then / else > do > do while (eof == 0) > do iops = 1, nops` | `titldum` |
| 53 | title | `if (.not. i_exist .or. in_lum%management_sch == "null") then / else > do` | `titldum` |
| 55 | header | `if (.not. i_exist .or. in_lum%management_sch == "null") then / else > do` | `header` |
| 59 | data | `if (.not. i_exist .or. in_lum%management_sch == "null") then / else > do > do isched = 1, imax` | `sched(isched)%name`, `sched(isched)%num_ops`, `sched(isched)%num_autos` |
| 67 | data | `if (.not. i_exist .or. in_lum%management_sch == "null") then / else > do > do isched = 1, imax > if (m_autos > 0) then > do iauto = 1, m_autos` | `sched(isched)%auto_name(iauto)` |
| 75 | data | `if (.not. i_exist .or. in_lum%management_sch == "null") then / else > do > do isched = 1, imax > if (m_autos > 0) then > do iauto = 1, m_autos > if (sched(isched)%auto_name(iauto) == "pl_hv_summer1" .or. sched(isched)%auto_name(iauto) == "pl_hv_winter1") then` | `sched(isched)%auto_name(iauto)`, `sched(isched)%auto_crop` |
| 81 | data | `if (.not. i_exist .or. in_lum%management_sch == "null") then / else > do > do isched = 1, imax > if (m_autos > 0) then > do iauto = 1, m_autos > if (sched(isched)%auto_name(iauto) == "pl_hv_summer2") then` | `sched(isched)%auto_name(iauto)`, `sched(isched)%auto_crop` |


### Candidate exact read evidence

- Procedure: `mgt_read_mgtops`
- Reader: `mgt_read_mgtops.f90`
- Match: exact_filename
- Resolved default filename(s): `management.sch`
- Source filename expression(s): `in_lum%management_sch`, `management.sch`
- Open: line 33, file expression `in_lum%management_sch`, parser value `management.sch`, condition `if (.not. i_exist .or. in_lum%management_sch == "null") then / else > do`

| Line | Role | Condition | Fields read |
| --- | --- | --- | --- |
| 34 | title | `if (.not. i_exist .or. in_lum%management_sch == "null") then / else > do` | `titldum` |
| 36 | header | `if (.not. i_exist .or. in_lum%management_sch == "null") then / else > do` | `header` |
| 39 | data | `if (.not. i_exist .or. in_lum%management_sch == "null") then / else > do > do while (eof == 0)` | `titldum`, `nops`, `nauto` |
| 42 | title | `if (.not. i_exist .or. in_lum%management_sch == "null") then / else > do > do while (eof == 0) > do iauto = 1, nauto` | `titldum` |
| 46 | title | `if (.not. i_exist .or. in_lum%management_sch == "null") then / else > do > do while (eof == 0) > do iops = 1, nops` | `titldum` |
| 55 | title | `if (.not. i_exist .or. in_lum%management_sch == "null") then / else > do` | `titldum` |
| 57 | header | `if (.not. i_exist .or. in_lum%management_sch == "null") then / else > do` | `header` |
| 61 | data | `if (.not. i_exist .or. in_lum%management_sch == "null") then / else > do > do isched = 1, imax` | `sched(isched)%name`, `sched(isched)%num_ops`, `sched(isched)%num_autos` |
| 69 | data | `if (.not. i_exist .or. in_lum%management_sch == "null") then / else > do > do isched = 1, imax > if (m_autos > 0) then > do iauto = 1, m_autos` | `sched(isched)%auto_name(iauto)` |
| 77 | data | `if (.not. i_exist .or. in_lum%management_sch == "null") then / else > do > do isched = 1, imax > if (m_autos > 0) then > do iauto = 1, m_autos > if (sched(isched)%auto_name(iauto) == "pl_hv_summer1" .or. sched(isched)%auto_name(iauto) == "pl_hv_winter1") then` | `sched(isched)%auto_name(iauto)`, `sched(isched)%auto_crop` |
| 83 | data | `if (.not. i_exist .or. in_lum%management_sch == "null") then / else > do > do isched = 1, imax > if (m_autos > 0) then > do iauto = 1, m_autos > if (sched(isched)%auto_name(iauto) == "pl_hv_summer2") then` | `sched(isched)%auto_name(iauto)`, `sched(isched)%auto_crop` |


## `manure_db.frt`

- Schema diff status: `['files.added']`
- Review needed: no
- Base schema presence: `{'resolved_sections': [], 'unresolved_sections': ['unresolved']}`
- Candidate schema presence: `{'resolved_sections': ['files'], 'unresolved_sections': []}`

### Base exact read evidence

_No exact base opened/read evidence found._

### Base related read evidence

- Procedure: `manure_parm_read`
- Reader: `manure_parm_read.f90`
- Match: shared filename tokens, similar opened filename/expression
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

- Procedure: `manure_allocation_read`
- Reader: `manure_allocation_read.f90`
- Match: shared filename tokens
- Resolved default filename(s): `manure_allo.mnu`
- Source filename expression(s): `manure_allo.mnu`
- Open: line 39, file expression `"manure_allo.mnu"`, parser value `manure_allo.mnu`, condition `if (.not. i_exist .or. "manure_allo.mnu" == "null") then / else > do`

| Line | Role | Condition | Fields read |
| --- | --- | --- | --- |
| 40 | title | `if (.not. i_exist .or. "manure_allo.mnu" == "null") then / else > do` | `titldum` |
| 42 | count | `if (.not. i_exist .or. "manure_allo.mnu" == "null") then / else > do` | `imax` |
| 49 | header | `if (.not. i_exist .or. "manure_allo.mnu" == "null") then / else > do > do imro = 1, imax` | `header` |
| 51 | data | `if (.not. i_exist .or. "manure_allo.mnu" == "null") then / else > do > do imro = 1, imax` | `mallo(imro)%name`, `mallo(imro)%rule_typ`, `mallo(imro)%src_obs`, `mallo(imro)%dmd_obs` |
| 54 | header | `if (.not. i_exist .or. "manure_allo.mnu" == "null") then / else > do > do imro = 1, imax` | `header` |
| 63 | data | `if (.not. i_exist .or. "manure_allo.mnu" == "null") then / else > do > do imro = 1, imax > do isrc = 1, mallo(imro)%src_obs` | `i` |
| 67 | data | `if (.not. i_exist .or. "manure_allo.mnu" == "null") then / else > do > do imro = 1, imax > do isrc = 1, mallo(imro)%src_obs` | `k`, `mallo(imro)%src(i)%mois_typ`, `mallo(imro)%src(i)%manure_typ`, `mallo(imro)%src(i)%lat`, `mallo(imro)%src(i)%long`, `mallo(imro)%src(i)%stor_init`, `mallo(imro)%src(i)%stor_max`, `mallo(imro)%src(i)%prod_mon` |
| 81 | header | `if (.not. i_exist .or. "manure_allo.mnu" == "null") then / else > do > do imro = 1, imax` | `header` |
| 90 | data | `if (.not. i_exist .or. "manure_allo.mnu" == "null") then / else > do > do imro = 1, imax > do idmd = 1, num_objs` | `i` |
| 94 | data | `if (.not. i_exist .or. "manure_allo.mnu" == "null") then / else > do > do imro = 1, imax > do idmd = 1, num_objs` | `k`, `mallo(imro)%dmd(i)%ob_typ`, `mallo(imro)%dmd(i)%ob_num`, `mallo(imro)%dmd(i)%dtbl`, `mallo(imro)%dmd(i)%right` |

- Procedure: `constit_db_read`
- Reader: `constit_db_read.f90`
- Match: shared filename tokens
- Resolved default filename(s): `constituents.cs`
- Source filename expression(s): `in_sim%cs_db`, `constituents.cs`
- Open: line 33, file expression `in_sim%cs_db`, parser value `constituents.cs`, condition `if (.not. i_exist .or. in_sim%cs_db == "null") then / else > do`

| Line | Role | Condition | Fields read |
| --- | --- | --- | --- |
| 34 | title | `if (.not. i_exist .or. in_sim%cs_db == "null") then / else > do` | `titldum` |
| 36 | data | `if (.not. i_exist .or. in_sim%cs_db == "null") then / else > do` | `cs_db%num_pests` |
| 40 | data | `if (.not. i_exist .or. in_sim%cs_db == "null") then / else > do` | `(cs_db%pests(i), i = 1, cs_db%num_pests)` |
| 42 | data | `if (.not. i_exist .or. in_sim%cs_db == "null") then / else > do` | `cs_db%num_paths` |
| 46 | data | `if (.not. i_exist .or. in_sim%cs_db == "null") then / else > do` | `(cs_db%paths(i), i = 1, cs_db%num_paths)` |
| 48 | data | `if (.not. i_exist .or. in_sim%cs_db == "null") then / else > do` | `cs_db%num_metals` |
| 52 | data | `if (.not. i_exist .or. in_sim%cs_db == "null") then / else > do` | `(cs_db%metals(i), i = 1, cs_db%num_metals)` |
| 55 | data | `if (.not. i_exist .or. in_sim%cs_db == "null") then / else > do` | `cs_db%num_salts` |
| 59 | data | `if (.not. i_exist .or. in_sim%cs_db == "null") then / else > do` | `(cs_db%salts(i), i = 1, cs_db%num_salts)` |
| 61 | data | `if (.not. i_exist .or. in_sim%cs_db == "null") then / else > do` | `cs_db%num_cs` |
| 65 | data | `if (.not. i_exist .or. in_sim%cs_db == "null") then / else > do` | `(cs_db%cs(i), i = 1, cs_db%num_cs)` |


### Candidate exact read evidence

- Procedure: `manure_db_read`
- Reader: `manure_db_read.f90`
- Match: exact_filename
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


## `manure_om.frt`

- Schema diff status: `['files.added']`
- Review needed: no
- Base schema presence: `{'resolved_sections': [], 'unresolved_sections': ['unresolved']}`
- Candidate schema presence: `{'resolved_sections': ['files'], 'unresolved_sections': []}`

### Base exact read evidence

_No exact base opened/read evidence found._

### Base related read evidence

- Procedure: `manure_parm_read`
- Reader: `manure_parm_read.f90`
- Match: shared filename tokens, similar opened filename/expression
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

- Procedure: `manure_allocation_read`
- Reader: `manure_allocation_read.f90`
- Match: shared filename tokens, similar opened filename/expression
- Resolved default filename(s): `manure_allo.mnu`
- Source filename expression(s): `manure_allo.mnu`
- Open: line 39, file expression `"manure_allo.mnu"`, parser value `manure_allo.mnu`, condition `if (.not. i_exist .or. "manure_allo.mnu" == "null") then / else > do`

| Line | Role | Condition | Fields read |
| --- | --- | --- | --- |
| 40 | title | `if (.not. i_exist .or. "manure_allo.mnu" == "null") then / else > do` | `titldum` |
| 42 | count | `if (.not. i_exist .or. "manure_allo.mnu" == "null") then / else > do` | `imax` |
| 49 | header | `if (.not. i_exist .or. "manure_allo.mnu" == "null") then / else > do > do imro = 1, imax` | `header` |
| 51 | data | `if (.not. i_exist .or. "manure_allo.mnu" == "null") then / else > do > do imro = 1, imax` | `mallo(imro)%name`, `mallo(imro)%rule_typ`, `mallo(imro)%src_obs`, `mallo(imro)%dmd_obs` |
| 54 | header | `if (.not. i_exist .or. "manure_allo.mnu" == "null") then / else > do > do imro = 1, imax` | `header` |
| 63 | data | `if (.not. i_exist .or. "manure_allo.mnu" == "null") then / else > do > do imro = 1, imax > do isrc = 1, mallo(imro)%src_obs` | `i` |
| 67 | data | `if (.not. i_exist .or. "manure_allo.mnu" == "null") then / else > do > do imro = 1, imax > do isrc = 1, mallo(imro)%src_obs` | `k`, `mallo(imro)%src(i)%mois_typ`, `mallo(imro)%src(i)%manure_typ`, `mallo(imro)%src(i)%lat`, `mallo(imro)%src(i)%long`, `mallo(imro)%src(i)%stor_init`, `mallo(imro)%src(i)%stor_max`, `mallo(imro)%src(i)%prod_mon` |
| 81 | header | `if (.not. i_exist .or. "manure_allo.mnu" == "null") then / else > do > do imro = 1, imax` | `header` |
| 90 | data | `if (.not. i_exist .or. "manure_allo.mnu" == "null") then / else > do > do imro = 1, imax > do idmd = 1, num_objs` | `i` |
| 94 | data | `if (.not. i_exist .or. "manure_allo.mnu" == "null") then / else > do > do imro = 1, imax > do idmd = 1, num_objs` | `k`, `mallo(imro)%dmd(i)%ob_typ`, `mallo(imro)%dmd(i)%ob_num`, `mallo(imro)%dmd(i)%dtbl`, `mallo(imro)%dmd(i)%right` |

- Procedure: `dr_read_om`
- Reader: `dr_read_om.f90`
- Match: shared filename tokens
- Resolved default filename(s): `dr_om.del`
- Source filename expression(s): `in_delr%om`, `dr_om.del`
- Open: line 32, file expression `in_delr%om`, parser value `dr_om.del`, condition `if (i_exist .or. in_delr%om /= "null") then > do`

| Line | Role | Condition | Fields read |
| --- | --- | --- | --- |
| 33 | title | `if (i_exist .or. in_delr%om /= "null") then > do` | `titldum` |
| 35 | header | `if (i_exist .or. in_delr%om /= "null") then > do` | `header` |
| 39 | title | `if (i_exist .or. in_delr%om /= "null") then > do > do while (eof == 0)` | `titldum` |
| 50 | title | `if (i_exist .or. in_delr%om /= "null") then > do` | `titldum` |
| 52 | header | `if (i_exist .or. in_delr%om /= "null") then > do` | `header` |
| 57 | title | `if (i_exist .or. in_delr%om /= "null") then > do > do ii = 1, db_mx%dr_om` | `titldum` |
| 60 | data | `if (i_exist .or. in_delr%om /= "null") then > do > do ii = 1, db_mx%dr_om` | `dr_om_name(ii)`, `dr(ii)` |

- Procedure: `exco_read_om`
- Reader: `exco_read_om.f90`
- Match: shared filename tokens
- Resolved default filename(s): `exco_om.exc`
- Source filename expression(s): `in_exco%om`, `exco_om.exc`
- Open: line 31, file expression `in_exco%om`, parser value `exco_om.exc`, condition `if (i_exist .or. in_exco%om /= "null") then > do`

| Line | Role | Condition | Fields read |
| --- | --- | --- | --- |
| 32 | title | `if (i_exist .or. in_exco%om /= "null") then > do` | `titldum` |
| 34 | header | `if (i_exist .or. in_exco%om /= "null") then > do` | `header` |
| 38 | title | `if (i_exist .or. in_exco%om /= "null") then > do > do while (eof == 0)` | `titldum` |
| 49 | title | `if (i_exist .or. in_exco%om /= "null") then > do` | `titldum` |
| 51 | header | `if (i_exist .or. in_exco%om /= "null") then > do` | `header` |
| 56 | title | `if (i_exist .or. in_exco%om /= "null") then > do > do ii = 1, db_mx%exco_om` | `titldum` |
| 59 | data | `if (i_exist .or. in_exco%om /= "null") then > do > do ii = 1, db_mx%exco_om` | `exco_om_name(ii)`, `exco(ii)` |

- Procedure: `om_water_init`
- Reader: `om_water_init.f90`
- Match: shared filename tokens
- Resolved default filename(s): `om_water.ini`
- Source filename expression(s): `in_init%om_water`, `om_water.ini`
- Open: line 29, file expression `in_init%om_water`, parser value `om_water.ini`, condition `if (.not. i_exist .or. in_init%om_water == "null") then / else > do`

| Line | Role | Condition | Fields read |
| --- | --- | --- | --- |
| 30 | title | `if (.not. i_exist .or. in_init%om_water == "null") then / else > do` | `titldum` |
| 32 | header | `if (.not. i_exist .or. in_init%om_water == "null") then / else > do` | `header` |
| 35 | title | `if (.not. i_exist .or. in_init%om_water == "null") then / else > do > do while (eof == 0)` | `titldum` |
| 45 | title | `if (.not. i_exist .or. in_init%om_water == "null") then / else > do` | `titldum` |
| 47 | header | `if (.not. i_exist .or. in_init%om_water == "null") then / else > do` | `header` |
| 51 | title | `if (.not. i_exist .or. in_init%om_water == "null") then / else > do > do ichi = 1, db_mx%om_water_init` | `titldum` |
| 54 | data | `if (.not. i_exist .or. in_init%om_water == "null") then / else > do > do ichi = 1, db_mx%om_water_init` | `om_init_name(ichi)`, `om_init_water(ichi)` |


### Candidate exact read evidence

- Procedure: `manure_orgmin_read`
- Reader: `manure_orgmin_read.f90`
- Match: exact_filename
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


## `minerals.gw`

- Schema diff status: `['runtime_arity.added']`
- Review needed: no
- Base schema presence: `{'resolved_sections': [], 'unresolved_sections': ['runtime_arity_unresolved']}`
- Candidate schema presence: `{'resolved_sections': ['runtime_arity'], 'unresolved_sections': []}`

### Base exact read evidence

_No exact base opened/read evidence found._

### Candidate exact read evidence

- Procedure: `gwflow_read`
- Reader: `gwflow_read.f90`
- Match: exact_filename
- Resolved default filename(s): `minerals.gw`
- Source filename expression(s): `minerals.gw`
- Open: line 1658, file expression `'minerals.gw'`, parser value `minerals.gw`, condition `if(gw_solute_flag == 1) then > if(i_exist) then > if(gwsol_salt == 1) then > if(i_exist) then`

| Line | Role | Condition | Fields read |
| --- | --- | --- | --- |
| 1659 | header | `if(gw_solute_flag == 1) then > if(i_exist) then > if(gwsol_salt == 1) then > if(i_exist) then` | `header` |
| 1660 | data | `if(gw_solute_flag == 1) then > if(i_exist) then > if(gwsol_salt == 1) then > if(i_exist) then` | `gw_nminl` |
| 1667 | header | `if(gw_solute_flag == 1) then > if(i_exist) then > if(gwsol_salt == 1) then > if(i_exist) then` | `header` |
| 1671 | header | `if(gw_solute_flag == 1) then > if(i_exist) then > if(gwsol_salt == 1) then > if(i_exist) then > if(grid_type == "structured") then > do m=1,gw_nminl` | `header` |
| 1672 | data | `if(gw_solute_flag == 1) then > if(i_exist) then > if(gwsol_salt == 1) then > if(i_exist) then > if(grid_type == "structured") then > do m=1,gw_nminl` | `read_type` |
| 1674 | data | `if(gw_solute_flag == 1) then > if(i_exist) then > if(gwsol_salt == 1) then > if(i_exist) then > if(grid_type == "structured") then > do m=1,gw_nminl > if(read_type == "single") then` | `single_value` |
| 1678 | data | `if(gw_solute_flag == 1) then > if(i_exist) then > if(gwsol_salt == 1) then > if(i_exist) then > if(grid_type == "structured") then > do m=1,gw_nminl > if(read_type == "single") then / elseif(read_type == "array") then > do i=1,grid_nrow` | `(grid_val(i,j),j=1,grid_ncol)` |
| 1685 | data | `if(gw_solute_flag == 1) then > if(i_exist) then > if(gwsol_salt == 1) then > if(i_exist) then > if(grid_type == "structured") then / elseif(grid_type == "unstructured") then > do i=1,ncell` | `(gwsol_minl_state(i)%fract(m),m=1,gw_nminl)` |


## `om_osrc.wal`

- Schema diff status: `['files.added']`
- Review needed: no
- Base schema presence: `{'resolved_sections': [], 'unresolved_sections': ['unresolved']}`
- Candidate schema presence: `{'resolved_sections': ['files'], 'unresolved_sections': []}`

### Base exact read evidence

_No exact base opened/read evidence found._

### Base related read evidence

- Procedure: `om_water_init`
- Reader: `om_water_init.f90`
- Match: shared filename tokens
- Resolved default filename(s): `om_water.ini`
- Source filename expression(s): `in_init%om_water`, `om_water.ini`
- Open: line 29, file expression `in_init%om_water`, parser value `om_water.ini`, condition `if (.not. i_exist .or. in_init%om_water == "null") then / else > do`

| Line | Role | Condition | Fields read |
| --- | --- | --- | --- |
| 30 | title | `if (.not. i_exist .or. in_init%om_water == "null") then / else > do` | `titldum` |
| 32 | header | `if (.not. i_exist .or. in_init%om_water == "null") then / else > do` | `header` |
| 35 | title | `if (.not. i_exist .or. in_init%om_water == "null") then / else > do > do while (eof == 0)` | `titldum` |
| 45 | title | `if (.not. i_exist .or. in_init%om_water == "null") then / else > do` | `titldum` |
| 47 | header | `if (.not. i_exist .or. in_init%om_water == "null") then / else > do` | `header` |
| 51 | title | `if (.not. i_exist .or. in_init%om_water == "null") then / else > do > do ichi = 1, db_mx%om_water_init` | `titldum` |
| 54 | data | `if (.not. i_exist .or. in_init%om_water == "null") then / else > do > do ichi = 1, db_mx%om_water_init` | `om_init_name(ichi)`, `om_init_water(ichi)` |

- Procedure: `dr_read_om`
- Reader: `dr_read_om.f90`
- Match: shared filename tokens
- Resolved default filename(s): `dr_om.del`
- Source filename expression(s): `in_delr%om`, `dr_om.del`
- Open: line 32, file expression `in_delr%om`, parser value `dr_om.del`, condition `if (i_exist .or. in_delr%om /= "null") then > do`

| Line | Role | Condition | Fields read |
| --- | --- | --- | --- |
| 33 | title | `if (i_exist .or. in_delr%om /= "null") then > do` | `titldum` |
| 35 | header | `if (i_exist .or. in_delr%om /= "null") then > do` | `header` |
| 39 | title | `if (i_exist .or. in_delr%om /= "null") then > do > do while (eof == 0)` | `titldum` |
| 50 | title | `if (i_exist .or. in_delr%om /= "null") then > do` | `titldum` |
| 52 | header | `if (i_exist .or. in_delr%om /= "null") then > do` | `header` |
| 57 | title | `if (i_exist .or. in_delr%om /= "null") then > do > do ii = 1, db_mx%dr_om` | `titldum` |
| 60 | data | `if (i_exist .or. in_delr%om /= "null") then > do > do ii = 1, db_mx%dr_om` | `dr_om_name(ii)`, `dr(ii)` |

- Procedure: `exco_read_om`
- Reader: `exco_read_om.f90`
- Match: shared filename tokens
- Resolved default filename(s): `exco_om.exc`
- Source filename expression(s): `in_exco%om`, `exco_om.exc`
- Open: line 31, file expression `in_exco%om`, parser value `exco_om.exc`, condition `if (i_exist .or. in_exco%om /= "null") then > do`

| Line | Role | Condition | Fields read |
| --- | --- | --- | --- |
| 32 | title | `if (i_exist .or. in_exco%om /= "null") then > do` | `titldum` |
| 34 | header | `if (i_exist .or. in_exco%om /= "null") then > do` | `header` |
| 38 | title | `if (i_exist .or. in_exco%om /= "null") then > do > do while (eof == 0)` | `titldum` |
| 49 | title | `if (i_exist .or. in_exco%om /= "null") then > do` | `titldum` |
| 51 | header | `if (i_exist .or. in_exco%om /= "null") then > do` | `header` |
| 56 | title | `if (i_exist .or. in_exco%om /= "null") then > do > do ii = 1, db_mx%exco_om` | `titldum` |
| 59 | data | `if (i_exist .or. in_exco%om /= "null") then > do > do ii = 1, db_mx%exco_om` | `exco_om_name(ii)`, `exco(ii)` |


### Candidate exact read evidence

- Procedure: `om_osrc_read`
- Reader: `om_osrc_read.f90`
- Match: exact_filename
- Resolved default filename(s): `om_osrc.wal`
- Source filename expression(s): `om_osrc.wal`
- Open: line 31, file expression `'om_osrc.wal'`, parser value `om_osrc.wal`, condition `if (.not. i_exist .or. 'om_osrc.wal' == "null") then / else > do`

| Line | Role | Condition | Fields read |
| --- | --- | --- | --- |
| 32 | title | `if (.not. i_exist .or. 'om_osrc.wal' == "null") then / else > do` | `titldum` |
| 34 | count | `if (.not. i_exist .or. 'om_osrc.wal' == "null") then / else > do` | `imax` |
| 35 | header | `if (.not. i_exist .or. 'om_osrc.wal' == "null") then / else > do` | `header` |
| 43 | data | `if (.not. i_exist .or. 'om_osrc.wal' == "null") then / else > do > do iom_osrc = 1, imax` | `om_osrc_name(iom_osrc)`, `osrc_om(iom_osrc)` |


## `om_treat.wal`

- Schema diff status: `['files.added']`
- Review needed: no
- Base schema presence: `{'resolved_sections': [], 'unresolved_sections': ['unresolved']}`
- Candidate schema presence: `{'resolved_sections': ['files'], 'unresolved_sections': []}`

### Base exact read evidence

_No exact base opened/read evidence found._

### Base related read evidence

- Procedure: `treat_read_om`
- Reader: `treat_read_om.f90`
- Match: reader procedure tokens match target
- Resolved default filename(s): `treatment.trt`
- Source filename expression(s): `treatment.trt`
- Open: line 27, file expression `"treatment.trt"`, parser value `treatment.trt`, condition `if (i_exist .or. "treatment.trt" /= "null") then > do`

| Line | Role | Condition | Fields read |
| --- | --- | --- | --- |
| 28 | title | `if (i_exist .or. "treatment.trt" /= "null") then > do` | `titldum` |
| 30 | count | `if (i_exist .or. "treatment.trt" /= "null") then > do` | `imax` |
| 32 | header | `if (i_exist .or. "treatment.trt" /= "null") then > do` | `header` |
| 34 | header | `if (i_exist .or. "treatment.trt" /= "null") then > do` | `header` |
| 44 | data | `if (i_exist .or. "treatment.trt" /= "null") then > do > do ii = 1, db_mx%trt_om` | `trt_om_name(ii)`, `trt(ii)` |

- Procedure: `dr_read_om`
- Reader: `dr_read_om.f90`
- Match: shared filename tokens
- Resolved default filename(s): `dr_om.del`
- Source filename expression(s): `in_delr%om`, `dr_om.del`
- Open: line 32, file expression `in_delr%om`, parser value `dr_om.del`, condition `if (i_exist .or. in_delr%om /= "null") then > do`

| Line | Role | Condition | Fields read |
| --- | --- | --- | --- |
| 33 | title | `if (i_exist .or. in_delr%om /= "null") then > do` | `titldum` |
| 35 | header | `if (i_exist .or. in_delr%om /= "null") then > do` | `header` |
| 39 | title | `if (i_exist .or. in_delr%om /= "null") then > do > do while (eof == 0)` | `titldum` |
| 50 | title | `if (i_exist .or. in_delr%om /= "null") then > do` | `titldum` |
| 52 | header | `if (i_exist .or. in_delr%om /= "null") then > do` | `header` |
| 57 | title | `if (i_exist .or. in_delr%om /= "null") then > do > do ii = 1, db_mx%dr_om` | `titldum` |
| 60 | data | `if (i_exist .or. in_delr%om /= "null") then > do > do ii = 1, db_mx%dr_om` | `dr_om_name(ii)`, `dr(ii)` |

- Procedure: `om_water_init`
- Reader: `om_water_init.f90`
- Match: shared filename tokens
- Resolved default filename(s): `om_water.ini`
- Source filename expression(s): `in_init%om_water`, `om_water.ini`
- Open: line 29, file expression `in_init%om_water`, parser value `om_water.ini`, condition `if (.not. i_exist .or. in_init%om_water == "null") then / else > do`

| Line | Role | Condition | Fields read |
| --- | --- | --- | --- |
| 30 | title | `if (.not. i_exist .or. in_init%om_water == "null") then / else > do` | `titldum` |
| 32 | header | `if (.not. i_exist .or. in_init%om_water == "null") then / else > do` | `header` |
| 35 | title | `if (.not. i_exist .or. in_init%om_water == "null") then / else > do > do while (eof == 0)` | `titldum` |
| 45 | title | `if (.not. i_exist .or. in_init%om_water == "null") then / else > do` | `titldum` |
| 47 | header | `if (.not. i_exist .or. in_init%om_water == "null") then / else > do` | `header` |
| 51 | title | `if (.not. i_exist .or. in_init%om_water == "null") then / else > do > do ichi = 1, db_mx%om_water_init` | `titldum` |
| 54 | data | `if (.not. i_exist .or. in_init%om_water == "null") then / else > do > do ichi = 1, db_mx%om_water_init` | `om_init_name(ichi)`, `om_init_water(ichi)` |

- Procedure: `exco_read_om`
- Reader: `exco_read_om.f90`
- Match: shared filename tokens
- Resolved default filename(s): `exco_om.exc`
- Source filename expression(s): `in_exco%om`, `exco_om.exc`
- Open: line 31, file expression `in_exco%om`, parser value `exco_om.exc`, condition `if (i_exist .or. in_exco%om /= "null") then > do`

| Line | Role | Condition | Fields read |
| --- | --- | --- | --- |
| 32 | title | `if (i_exist .or. in_exco%om /= "null") then > do` | `titldum` |
| 34 | header | `if (i_exist .or. in_exco%om /= "null") then > do` | `header` |
| 38 | title | `if (i_exist .or. in_exco%om /= "null") then > do > do while (eof == 0)` | `titldum` |
| 49 | title | `if (i_exist .or. in_exco%om /= "null") then > do` | `titldum` |
| 51 | header | `if (i_exist .or. in_exco%om /= "null") then > do` | `header` |
| 56 | title | `if (i_exist .or. in_exco%om /= "null") then > do > do ii = 1, db_mx%exco_om` | `titldum` |
| 59 | data | `if (i_exist .or. in_exco%om /= "null") then > do > do ii = 1, db_mx%exco_om` | `exco_om_name(ii)`, `exco(ii)` |


### Candidate exact read evidence

- Procedure: `om_treat_read`
- Reader: `om_treat_read.f90`
- Match: exact_filename
- Resolved default filename(s): `om_treat.wal`
- Source filename expression(s): `om_treat.wal`
- Open: line 30, file expression `'om_treat.wal'`, parser value `om_treat.wal`, condition `if (.not. i_exist .or. 'om_treat.wal' == "null") then / else > do`

| Line | Role | Condition | Fields read |
| --- | --- | --- | --- |
| 31 | title | `if (.not. i_exist .or. 'om_treat.wal' == "null") then / else > do` | `titldum` |
| 33 | count | `if (.not. i_exist .or. 'om_treat.wal' == "null") then / else > do` | `imax` |
| 34 | header | `if (.not. i_exist .or. 'om_treat.wal' == "null") then / else > do` | `header` |
| 42 | data | `if (.not. i_exist .or. 'om_treat.wal' == "null") then / else > do > do iom_tr = 1, imax` | `om_treat_name(iom_tr)`, `wtp_om_treat(iom_tr)` |


## `om_use.wal`

- Schema diff status: `['files.added']`
- Review needed: no
- Base schema presence: `{'resolved_sections': [], 'unresolved_sections': ['unresolved']}`
- Candidate schema presence: `{'resolved_sections': ['files'], 'unresolved_sections': []}`

### Base exact read evidence

_No exact base opened/read evidence found._

### Base related read evidence

- Procedure: `dr_read_om`
- Reader: `dr_read_om.f90`
- Match: shared filename tokens
- Resolved default filename(s): `dr_om.del`
- Source filename expression(s): `in_delr%om`, `dr_om.del`
- Open: line 32, file expression `in_delr%om`, parser value `dr_om.del`, condition `if (i_exist .or. in_delr%om /= "null") then > do`

| Line | Role | Condition | Fields read |
| --- | --- | --- | --- |
| 33 | title | `if (i_exist .or. in_delr%om /= "null") then > do` | `titldum` |
| 35 | header | `if (i_exist .or. in_delr%om /= "null") then > do` | `header` |
| 39 | title | `if (i_exist .or. in_delr%om /= "null") then > do > do while (eof == 0)` | `titldum` |
| 50 | title | `if (i_exist .or. in_delr%om /= "null") then > do` | `titldum` |
| 52 | header | `if (i_exist .or. in_delr%om /= "null") then > do` | `header` |
| 57 | title | `if (i_exist .or. in_delr%om /= "null") then > do > do ii = 1, db_mx%dr_om` | `titldum` |
| 60 | data | `if (i_exist .or. in_delr%om /= "null") then > do > do ii = 1, db_mx%dr_om` | `dr_om_name(ii)`, `dr(ii)` |

- Procedure: `om_water_init`
- Reader: `om_water_init.f90`
- Match: shared filename tokens
- Resolved default filename(s): `om_water.ini`
- Source filename expression(s): `in_init%om_water`, `om_water.ini`
- Open: line 29, file expression `in_init%om_water`, parser value `om_water.ini`, condition `if (.not. i_exist .or. in_init%om_water == "null") then / else > do`

| Line | Role | Condition | Fields read |
| --- | --- | --- | --- |
| 30 | title | `if (.not. i_exist .or. in_init%om_water == "null") then / else > do` | `titldum` |
| 32 | header | `if (.not. i_exist .or. in_init%om_water == "null") then / else > do` | `header` |
| 35 | title | `if (.not. i_exist .or. in_init%om_water == "null") then / else > do > do while (eof == 0)` | `titldum` |
| 45 | title | `if (.not. i_exist .or. in_init%om_water == "null") then / else > do` | `titldum` |
| 47 | header | `if (.not. i_exist .or. in_init%om_water == "null") then / else > do` | `header` |
| 51 | title | `if (.not. i_exist .or. in_init%om_water == "null") then / else > do > do ichi = 1, db_mx%om_water_init` | `titldum` |
| 54 | data | `if (.not. i_exist .or. in_init%om_water == "null") then / else > do > do ichi = 1, db_mx%om_water_init` | `om_init_name(ichi)`, `om_init_water(ichi)` |

- Procedure: `exco_read_om`
- Reader: `exco_read_om.f90`
- Match: shared filename tokens
- Resolved default filename(s): `exco_om.exc`
- Source filename expression(s): `in_exco%om`, `exco_om.exc`
- Open: line 31, file expression `in_exco%om`, parser value `exco_om.exc`, condition `if (i_exist .or. in_exco%om /= "null") then > do`

| Line | Role | Condition | Fields read |
| --- | --- | --- | --- |
| 32 | title | `if (i_exist .or. in_exco%om /= "null") then > do` | `titldum` |
| 34 | header | `if (i_exist .or. in_exco%om /= "null") then > do` | `header` |
| 38 | title | `if (i_exist .or. in_exco%om /= "null") then > do > do while (eof == 0)` | `titldum` |
| 49 | title | `if (i_exist .or. in_exco%om /= "null") then > do` | `titldum` |
| 51 | header | `if (i_exist .or. in_exco%om /= "null") then > do` | `header` |
| 56 | title | `if (i_exist .or. in_exco%om /= "null") then > do > do ii = 1, db_mx%exco_om` | `titldum` |
| 59 | data | `if (i_exist .or. in_exco%om /= "null") then > do > do ii = 1, db_mx%exco_om` | `exco_om_name(ii)`, `exco(ii)` |


### Candidate exact read evidence

- Procedure: `om_use_read`
- Reader: `om_use_read.f90`
- Match: exact_filename
- Resolved default filename(s): `om_use.wal`
- Source filename expression(s): `om_use.wal`
- Open: line 30, file expression `'om_use.wal'`, parser value `om_use.wal`, condition `if (.not. i_exist .or. 'om_use.wal' == "null") then / else > do`

| Line | Role | Condition | Fields read |
| --- | --- | --- | --- |
| 31 | title | `if (.not. i_exist .or. 'om_use.wal' == "null") then / else > do` | `titldum` |
| 33 | count | `if (.not. i_exist .or. 'om_use.wal' == "null") then / else > do` | `imax` |
| 34 | header | `if (.not. i_exist .or. 'om_use.wal' == "null") then / else > do` | `header` |
| 43 | data | `if (.not. i_exist .or. 'om_use.wal' == "null") then / else > do > do iom_use = 1, imax` | `om_use_name(iom_use)`, `wuse_om_efflu(iom_use)` |


## `out_src.wal`

- Schema diff status: `['runtime_arity.added']`
- Review needed: no
- Base schema presence: `{'resolved_sections': [], 'unresolved_sections': ['runtime_arity_unresolved']}`
- Candidate schema presence: `{'resolved_sections': ['runtime_arity'], 'unresolved_sections': []}`

### Base exact read evidence

_No exact base opened/read evidence found._

### Base related read evidence

- Procedure: `header_write`
- Reader: `header_write.f90`
- Match: shared filename tokens, similar opened filename/expression
- Resolved default filename(s): `hru-out.cal`
- Source filename expression(s): `hru-out.cal`
- Open: line 24, file expression `"hru-out.cal"`, parser value `hru-out.cal`, condition `if (cal_soft == "y") then`
- Reads: _none captured_


### Candidate exact read evidence

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


## `outputs.gw`

- Schema diff status: `['files.added']`
- Review needed: no
- Base schema presence: `{'resolved_sections': [], 'unresolved_sections': ['unresolved']}`
- Candidate schema presence: `{'resolved_sections': ['files'], 'unresolved_sections': []}`

### Base exact read evidence

_No exact base opened/read evidence found._

### Candidate exact read evidence

- Procedure: `gwflow_read`
- Reader: `gwflow_read.f90`
- Match: exact_filename
- Resolved default filename(s): `outputs.gw`
- Source filename expression(s): `outputs.gw`, `unit_split_fields(2)`
- Open: line 524, file expression `'outputs.gw'`, parser value `outputs.gw`, condition `None`

| Line | Role | Condition | Fields read |
| --- | --- | --- | --- |
| 525 | header | `None` | `header` |
| 526 | header | `None` | `header` |
| 529 | data | `do` | `split_line_buf` |
| 546 | header | `None` | `header` |
| 547 | header | `None` | `header` |
| 551 | data | `do` | `split_line_buf` |
| 559 | data | `do > select case (trim(split_fields(1))) / case ('head_output_time')` | `combined_yrday` |
| 564 | data | `do > select case (trim(split_fields(1))) / case ('observation_cell')` | `gw_obs_cells_init(m)` |
| 566 | data | `do > select case (trim(split_fields(1))) / case ('detail_debug_cell')` | `gw_cell_obs_ss` |


## `outside_rcv.wal`

- Schema diff status: `['files.added']`
- Review needed: no
- Base schema presence: `{'resolved_sections': [], 'unresolved_sections': ['unresolved']}`
- Candidate schema presence: `{'resolved_sections': ['files'], 'unresolved_sections': []}`

### Base exact read evidence

_No exact base opened/read evidence found._

### Candidate exact read evidence

- Procedure: `water_orcv_read`
- Reader: `water_orcv_read.f90`
- Match: exact_filename
- Resolved default filename(s): `outside_rcv.wal`
- Source filename expression(s): `outside_rcv.wal`
- Open: line 34, file expression `'outside_rcv.wal'`, parser value `outside_rcv.wal`, condition `if (.not. i_exist .or. 'outside_rcv.wal' == "null") then / else > do`

| Line | Role | Condition | Fields read |
| --- | --- | --- | --- |
| 35 | title | `if (.not. i_exist .or. 'outside_rcv.wal' == "null") then / else > do` | `titldum` |
| 37 | count | `if (.not. i_exist .or. 'outside_rcv.wal' == "null") then / else > do` | `imax` |
| 38 | header | `if (.not. i_exist .or. 'outside_rcv.wal' == "null") then / else > do` | `header` |
| 45 | data | `if (.not. i_exist .or. 'outside_rcv.wal' == "null") then / else > do > do ircv = 1, imax` | `i`, `orcv(ircv)%name`, `orcv(ircv)%filename` |


## `phreato.gw`

- Schema diff status: `['files.added']`
- Review needed: no
- Base schema presence: `{'resolved_sections': [], 'unresolved_sections': ['unresolved']}`
- Candidate schema presence: `{'resolved_sections': ['files'], 'unresolved_sections': []}`

### Base exact read evidence

_No exact base opened/read evidence found._

### Candidate exact read evidence

- Procedure: `gwflow_read`
- Reader: `gwflow_read.f90`
- Match: exact_filename
- Resolved default filename(s): `phreato.gw`
- Source filename expression(s): `phreato.gw`
- Open: line 1393, file expression `'phreato.gw'`, parser value `phreato.gw`, condition `if(i_exist) then`

| Line | Role | Condition | Fields read |
| --- | --- | --- | --- |
| 1394 | header | `if(i_exist) then` | `header` |
| 1395 | header | `if(i_exist) then` | `header` |
| 1398 | data | `if(i_exist) then > do` | `single_value` |
| 1405 | header | `if(i_exist) then` | `header` |
| 1406 | header | `if(i_exist) then` | `header` |
| 1408 | data | `if(i_exist) then > do i=1,gw_phyt_npts` | `gw_phyt_dep(i)`, `gw_phyt_rate(i)` |


## `phreato_cell.gw`

- Schema diff status: `['files.added']`
- Review needed: no
- Base schema presence: `{'resolved_sections': [], 'unresolved_sections': ['unresolved']}`
- Candidate schema presence: `{'resolved_sections': ['files'], 'unresolved_sections': []}`

### Base exact read evidence

_No exact base opened/read evidence found._

### Candidate exact read evidence

- Procedure: `gwflow_read`
- Reader: `gwflow_read.f90`
- Match: exact_filename
- Resolved default filename(s): `phreato_cell.gw`
- Source filename expression(s): `phreato_cell.gw`
- Open: line 1412, file expression `'phreato_cell.gw'`, parser value `phreato_cell.gw`, condition `if(i_exist) then`

| Line | Role | Condition | Fields read |
| --- | --- | --- | --- |
| 1413 | header | `if(i_exist) then` | `header` |
| 1414 | header | `if(i_exist) then` | `header` |
| 1417 | data | `if(i_exist) then > do` | `cell_id` |
| 1424 | header | `if(i_exist) then` | `header` |
| 1425 | header | `if(i_exist) then` | `header` |
| 1427 | data | `if(i_exist) then > do i=1,gw_phyt_ncells` | `gw_phyt_ids(i)`, `gw_phyt_area(i)` |


## `pond_cell.gw`

- Schema diff status: `['files.added']`
- Review needed: no
- Base schema presence: `{'resolved_sections': [], 'unresolved_sections': ['unresolved']}`
- Candidate schema presence: `{'resolved_sections': ['files'], 'unresolved_sections': []}`

### Base exact read evidence

_No exact base opened/read evidence found._

### Candidate exact read evidence

- Procedure: `gwflow_read`
- Reader: `gwflow_read.f90`
- Match: exact_filename
- Resolved default filename(s): `pond_cell.gw`
- Source filename expression(s): `pond_cell.gw`
- Open: line 1957, file expression `'pond_cell.gw'`, parser value `pond_cell.gw`, condition `if(i_exist) then`

| Line | Role | Condition | Fields read |
| --- | --- | --- | --- |
| 1958 | header | `if(i_exist) then` | `header` |
| 1959 | header | `if(i_exist) then` | `header` |
| 1961 | data | `if(i_exist) then > do` | `dum_id` |
| 1973 | header | `if(i_exist) then` | `header` |
| 1974 | header | `if(i_exist) then` | `header` |
| 1976 | data | `if(i_exist) then > do` | `dum_id`, `cell_num`, `dum4` |


## `ponds.gw`

- Schema diff status: `['runtime_arity.added']`
- Review needed: no
- Base schema presence: `{'resolved_sections': [], 'unresolved_sections': ['runtime_arity_unresolved']}`
- Candidate schema presence: `{'resolved_sections': ['runtime_arity'], 'unresolved_sections': []}`

### Base exact read evidence

_No exact base opened/read evidence found._

### Candidate exact read evidence

- Procedure: `gwflow_read`
- Reader: `gwflow_read.f90`
- Match: exact_filename
- Resolved default filename(s): `ponds.gw`
- Source filename expression(s): `ponds.gw`
- Open: line 1910, file expression `'ponds.gw'`, parser value `ponds.gw`, condition `if(i_exist) then`

| Line | Role | Condition | Fields read |
| --- | --- | --- | --- |
| 1911 | header | `if(i_exist) then` | `header` |
| 1912 | header | `if(i_exist) then` | `header` |
| 1915 | data | `if(i_exist) then > do` | `dum_id` |
| 1921 | header | `if(i_exist) then` | `header` |
| 1922 | header | `if(i_exist) then` | `header` |
| 1925 | data | `if(i_exist) then > do i=1,gw_npond` | `gw_pond_info(i)%id`, `gw_pond_info(i)%area`, `gw_pond_info(i)%chan`, `gw_pond_info(i)%canal`, `gw_pond_info(i)%unl`, `gw_pond_info(i)%bed_k`, `gw_pond_info(i)%wsta`, `gw_pond_info(i)%evap_co`, `yr_start`, `mo_start`, `dy_start`, `(gw_pond_info(i)%unl_conc(j),j=1,gw_nsolute)` |


## `pumpex.gw`

- Schema diff status: `['files.added']`
- Review needed: no
- Base schema presence: `{'resolved_sections': [], 'unresolved_sections': ['unresolved']}`
- Candidate schema presence: `{'resolved_sections': ['files'], 'unresolved_sections': []}`

### Base exact read evidence

_No exact base opened/read evidence found._

### Base related read evidence

- Procedure: `gwflow_read`
- Reader: `gwflow_read.f90`
- Match: shared filename tokens
- Resolved default filename(s): `gwflow.pumpex`
- Source filename expression(s): `gwflow.pumpex`
- Open: line 951, file expression `'gwflow.pumpex'`, parser value `gwflow.pumpex`, condition `if (gw_pumpex_flag == 1) then > if(i_exist) then`

| Line | Role | Condition | Fields read |
| --- | --- | --- | --- |
| 952 | header | `if (gw_pumpex_flag == 1) then > if(i_exist) then` | `header` |
| 953 | data | `if (gw_pumpex_flag == 1) then > if(i_exist) then` | `gw_npumpex` |
| 962 | data | `if (gw_pumpex_flag == 1) then > if(i_exist) then > do i=1,gw_npumpex` | _no fields captured_ |
| 963 | data | `if (gw_pumpex_flag == 1) then > if(i_exist) then > do i=1,gw_npumpex` | `pumpex_cell`, `gw_pumpex_nperiods(i)` |
| 970 | data | `if (gw_pumpex_flag == 1) then > if(i_exist) then > do i=1,gw_npumpex > do j=1,gw_pumpex_nperiods(i)` | `gw_pumpex_dates(i,1,j)`, `gw_pumpex_dates(i,2,j)`, `gw_pumpex_rates(i,j)` |


### Candidate exact read evidence

- Procedure: `gwflow_read`
- Reader: `gwflow_read.f90`
- Match: exact_filename
- Resolved default filename(s): `pumpex.gw`
- Source filename expression(s): `pumpex.gw`
- Open: line 935, file expression `'pumpex.gw'`, parser value `pumpex.gw`, condition `if(gw_pumpex_flag == 1) then > if(i_exist) then`

| Line | Role | Condition | Fields read |
| --- | --- | --- | --- |
| 936 | header | `if(gw_pumpex_flag == 1) then > if(i_exist) then` | `header` |
| 937 | header | `if(gw_pumpex_flag == 1) then > if(i_exist) then` | `header` |
| 942 | data | `if(gw_pumpex_flag == 1) then > if(i_exist) then > do` | `header`, `pumpex_cell` |
| 955 | header | `if(gw_pumpex_flag == 1) then > if(i_exist) then` | `header` |
| 956 | header | `if(gw_pumpex_flag == 1) then > if(i_exist) then` | `header` |
| 960 | data | `if(gw_pumpex_flag == 1) then > if(i_exist) then > do` | `header`, `pumpex_cell`, `gw_pumpex_rates_tmp`, `pe_yr_s`, `pe_dy_s`, `pe_yr_e`, `pe_dy_e` |


## `recall_db.rec`

- Schema diff status: `['files.added']`
- Review needed: no
- Base schema presence: `{'resolved_sections': [], 'unresolved_sections': ['unresolved']}`
- Candidate schema presence: `{'resolved_sections': ['files'], 'unresolved_sections': []}`

### Base exact read evidence

_No exact base opened/read evidence found._

### Base related read evidence

- Procedure: `recall_read`
- Reader: `recall_read.f90`
- Match: shared filename tokens, similar opened filename/expression
- Resolved default filename(s): `recall.rec`
- Source filename expression(s): `in_rec%recall_rec`, `recall.rec`
- Open: line 47, file expression `in_rec%recall_rec`, parser value `recall.rec`, condition `if (i_exist .or. in_rec%recall_rec /= "null") then > do`

| Line | Role | Condition | Fields read |
| --- | --- | --- | --- |
| 48 | title | `if (i_exist .or. in_rec%recall_rec /= "null") then > do` | `titldum` |
| 50 | header | `if (i_exist .or. in_rec%recall_rec /= "null") then > do` | `header` |
| 54 | data | `if (i_exist .or. in_rec%recall_rec /= "null") then > do > do while (eof == 0)` | `i` |
| 67 | title | `if (i_exist .or. in_rec%recall_rec /= "null") then > do` | `titldum` |
| 69 | header | `if (i_exist .or. in_rec%recall_rec /= "null") then > do` | `header` |
| 73 | data | `if (i_exist .or. in_rec%recall_rec /= "null") then > do > do ii = 1, imax` | `i` |
| 76 | data | `if (i_exist .or. in_rec%recall_rec /= "null") then > do > do ii = 1, imax` | `k`, `recall(i)%name`, `recall(i)%typ`, `recall(i)%filename` |

- Procedure: `recall_read_cs`
- Reader: `recall_read_cs.f90`
- Match: shared filename tokens, similar opened filename/expression
- Resolved default filename(s): `cs_recall.rec`
- Source filename expression(s): `cs_recall.rec`
- Open: line 47, file expression `"cs_recall.rec"`, parser value `cs_recall.rec`, condition `if (i_exist .or. in_rec%recall_rec /= "null") then > do`

| Line | Role | Condition | Fields read |
| --- | --- | --- | --- |
| 48 | title | `if (i_exist .or. in_rec%recall_rec /= "null") then > do` | `titldum` |
| 50 | header | `if (i_exist .or. in_rec%recall_rec /= "null") then > do` | `header` |
| 56 | data | `if (i_exist .or. in_rec%recall_rec /= "null") then > do > do while (eof == 0)` | `i` |
| 102 | title | `if (i_exist .or. in_rec%recall_rec /= "null") then > do` | `titldum` |
| 104 | header | `if (i_exist .or. in_rec%recall_rec /= "null") then > do` | `header` |
| 109 | data | `if (i_exist .or. in_rec%recall_rec /= "null") then > do > do ii = 1, imax` | `i` |
| 112 | data | `if (i_exist .or. in_rec%recall_rec /= "null") then > do > do ii = 1, imax` | `k`, `rec_cs(i)%name`, `rec_cs(i)%typ`, `rec_cs(i)%filename` |

- Procedure: `recall_read_salt`
- Reader: `recall_read_salt.f90`
- Match: shared filename tokens, similar opened filename/expression
- Resolved default filename(s): `salt_recall.rec`
- Source filename expression(s): `salt_recall.rec`
- Open: line 47, file expression `"salt_recall.rec"`, parser value `salt_recall.rec`, condition `if (i_exist .or. "salt_recall.rec" /= "null") then > do`

| Line | Role | Condition | Fields read |
| --- | --- | --- | --- |
| 48 | title | `if (i_exist .or. "salt_recall.rec" /= "null") then > do` | `titldum` |
| 50 | header | `if (i_exist .or. "salt_recall.rec" /= "null") then > do` | `header` |
| 56 | data | `if (i_exist .or. "salt_recall.rec" /= "null") then > do > do while (eof == 0)` | `i` |
| 102 | title | `if (i_exist .or. "salt_recall.rec" /= "null") then > do` | `titldum` |
| 104 | header | `if (i_exist .or. "salt_recall.rec" /= "null") then > do` | `header` |
| 110 | data | `if (i_exist .or. "salt_recall.rec" /= "null") then > do > do ii = 1, imax` | `i` |
| 113 | data | `if (i_exist .or. "salt_recall.rec" /= "null") then > do > do ii = 1, imax` | `k`, `rec_salt(i)%name`, `rec_salt(i)%typ`, `rec_salt(i)%filename` |

- Procedure: `recall_read`
- Reader: `recall_read.f90`
- Match: shared filename tokens
- Source filename expression(s): `recall(i)%filename`
- Open: line 81, file expression `recall(i)%filename`, parser value `recall(i)%filename`, condition `if (i_exist .or. in_rec%recall_rec /= "null") then > do > do ii = 1, imax > if (recall(i)%typ /= 4) then > do`

| Line | Role | Condition | Fields read |
| --- | --- | --- | --- |
| 82 | title | `if (i_exist .or. in_rec%recall_rec /= "null") then > do > do ii = 1, imax > if (recall(i)%typ /= 4) then > do` | `titldum` |
| 84 | count | `if (i_exist .or. in_rec%recall_rec /= "null") then > do > do ii = 1, imax > if (recall(i)%typ /= 4) then > do` | `nbyr` |
| 86 | header | `if (i_exist .or. in_rec%recall_rec /= "null") then > do > do ii = 1, imax > if (recall(i)%typ /= 4) then > do` | `header` |
| 108 | data | `if (i_exist .or. in_rec%recall_rec /= "null") then > do > do ii = 1, imax > if (recall(i)%typ /= 4) then` | `jday`, `mo`, `day_mo`, `iyr` |
| 116 | data | `if (i_exist .or. in_rec%recall_rec /= "null") then > do > do ii = 1, imax > if (recall(i)%typ /= 4) then > if (recall(i)%start_yr <= time%yrc) then > do` | `jday`, `mo`, `day_mo`, `iyr` |
| 130 | data | `if (i_exist .or. in_rec%recall_rec /= "null") then > do > do ii = 1, imax > if (recall(i)%typ /= 4) then > do` | `jday1`, `mo1`, `day_mo`, `iyr` |
| 159 | data | `if (i_exist .or. in_rec%recall_rec /= "null") then > do > do ii = 1, imax > if (recall(i)%typ /= 4) then > do > select case (recall(i)%typ) / case (1)` | `jday`, `mo`, `day_mo`, `iyr`, `ob_typ`, `ob_name`, `recall(i)%hd(jday1,iyrs)` |
| 162 | data | `if (i_exist .or. in_rec%recall_rec /= "null") then > do > do ii = 1, imax > if (recall(i)%typ /= 4) then > do > select case (recall(i)%typ) / case (2)` | `jday`, `mo`, `day_mo`, `iyr`, `ob_typ`, `ob_name`, `recall(i)%hd(mo1,iyrs)` |
| 165 | data | `if (i_exist .or. in_rec%recall_rec /= "null") then > do > do ii = 1, imax > if (recall(i)%typ /= 4) then > do > select case (recall(i)%typ) / case (3)` | `jday`, `mo`, `day_mo`, `iyr`, `ob_typ`, `ob_name`, `ht1` |

- Procedure: `constit_db_read`
- Reader: `constit_db_read.f90`
- Match: shared filename tokens
- Resolved default filename(s): `constituents.cs`
- Source filename expression(s): `in_sim%cs_db`, `constituents.cs`
- Open: line 33, file expression `in_sim%cs_db`, parser value `constituents.cs`, condition `if (.not. i_exist .or. in_sim%cs_db == "null") then / else > do`

| Line | Role | Condition | Fields read |
| --- | --- | --- | --- |
| 34 | title | `if (.not. i_exist .or. in_sim%cs_db == "null") then / else > do` | `titldum` |
| 36 | data | `if (.not. i_exist .or. in_sim%cs_db == "null") then / else > do` | `cs_db%num_pests` |
| 40 | data | `if (.not. i_exist .or. in_sim%cs_db == "null") then / else > do` | `(cs_db%pests(i), i = 1, cs_db%num_pests)` |
| 42 | data | `if (.not. i_exist .or. in_sim%cs_db == "null") then / else > do` | `cs_db%num_paths` |
| 46 | data | `if (.not. i_exist .or. in_sim%cs_db == "null") then / else > do` | `(cs_db%paths(i), i = 1, cs_db%num_paths)` |
| 48 | data | `if (.not. i_exist .or. in_sim%cs_db == "null") then / else > do` | `cs_db%num_metals` |
| 52 | data | `if (.not. i_exist .or. in_sim%cs_db == "null") then / else > do` | `(cs_db%metals(i), i = 1, cs_db%num_metals)` |
| 55 | data | `if (.not. i_exist .or. in_sim%cs_db == "null") then / else > do` | `cs_db%num_salts` |
| 59 | data | `if (.not. i_exist .or. in_sim%cs_db == "null") then / else > do` | `(cs_db%salts(i), i = 1, cs_db%num_salts)` |
| 61 | data | `if (.not. i_exist .or. in_sim%cs_db == "null") then / else > do` | `cs_db%num_cs` |
| 65 | data | `if (.not. i_exist .or. in_sim%cs_db == "null") then / else > do` | `(cs_db%cs(i), i = 1, cs_db%num_cs)` |


### Candidate exact read evidence

- Procedure: `recalldb_read`
- Reader: `recall_read.f90`
- Match: exact_filename
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
- Source filename expression(s): `in_cond%dtbl_res`, `res_rel.dtl`
- Open: line 35, file expression `in_cond%dtbl_res`, parser value `res_rel.dtl`, condition `if (.not. i_exist .or. in_cond%dtbl_res == "null") then / else > do`

| Line | Role | Condition | Fields read |
| --- | --- | --- | --- |
| 36 | title | `if (.not. i_exist .or. in_cond%dtbl_res == "null") then / else > do` | `titldum` |
| 38 | data | `if (.not. i_exist .or. in_cond%dtbl_res == "null") then / else > do` | `mdtbl` |
| 40 | data | `if (.not. i_exist .or. in_cond%dtbl_res == "null") then / else > do` | _no fields captured_ |
| 45 | header | `if (.not. i_exist .or. in_cond%dtbl_res == "null") then / else > do > do i = 1, mdtbl` | `header` |
| 47 | data | `if (.not. i_exist .or. in_cond%dtbl_res == "null") then / else > do > do i = 1, mdtbl` | `dtbl_res(i)%name`, `dtbl_res(i)%conds`, `dtbl_res(i)%alts`, `dtbl_res(i)%acts` |
| 58 | header | `if (.not. i_exist .or. in_cond%dtbl_res == "null") then / else > do > do i = 1, mdtbl` | `header` |
| 61 | data | `if (.not. i_exist .or. in_cond%dtbl_res == "null") then / else > do > do i = 1, mdtbl > do ic = 1, dtbl_res(i)%conds` | `dtbl_res(i)%cond(ic)`, `(dtbl_res(i)%alt(ic,ial), ial = 1, dtbl_res(i)%alts)` |
| 66 | header | `if (.not. i_exist .or. in_cond%dtbl_res == "null") then / else > do > do i = 1, mdtbl` | `header` |
| 69 | data | `if (.not. i_exist .or. in_cond%dtbl_res == "null") then / else > do > do i = 1, mdtbl > do iac = 1, dtbl_res(i)%acts` | `dtbl_res(i)%act(iac)`, `(dtbl_res(i)%act_outcomes(iac,ial), ial = 1, dtbl_res(i)%alts)` |
| 72 | data | `if (.not. i_exist .or. in_cond%dtbl_res == "null") then / else > do > do i = 1, mdtbl` | _no fields captured_ |


### Candidate exact read evidence

- Procedure: `dtbl_res_read`
- Reader: `dtbl_res_read.f90`
- Match: exact_filename
- Resolved default filename(s): `res_rel.dtl`
- Source filename expression(s): `in_cond%dtbl_res`, `res_rel.dtl`
- Open: line 36, file expression `in_cond%dtbl_res`, parser value `res_rel.dtl`, condition `if (.not. i_exist .or. in_cond%dtbl_res == "null") then / else > do`

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


## `rescell.gw`

- Schema diff status: `['files.added']`
- Review needed: no
- Base schema presence: `{'resolved_sections': [], 'unresolved_sections': ['unresolved']}`
- Candidate schema presence: `{'resolved_sections': ['files'], 'unresolved_sections': []}`

### Base exact read evidence

_No exact base opened/read evidence found._

### Candidate exact read evidence

- Procedure: `gwflow_read`
- Reader: `gwflow_read.f90`
- Match: exact_filename
- Resolved default filename(s): `rescell.gw`
- Source filename expression(s): `rescell.gw`
- Open: line 1090, file expression `'rescell.gw'`, parser value `rescell.gw`, condition `if(gw_res_flag == 1) then > if(i_exist) then`

| Line | Role | Condition | Fields read |
| --- | --- | --- | --- |
| 1091 | header | `if(gw_res_flag == 1) then > if(i_exist) then` | `header` |
| 1092 | header | `if(gw_res_flag == 1) then > if(i_exist) then` | `header` |
| 1094 | data | `if(gw_res_flag == 1) then > if(i_exist) then` | `res_thick` |
| 1095 | data | `if(gw_res_flag == 1) then > if(i_exist) then` | `res_K` |
| 1099 | data | `if(gw_res_flag == 1) then > if(i_exist) then` | `num_res_cells` |
| 1100 | header | `if(gw_res_flag == 1) then > if(i_exist) then` | `header` |
| 1102 | data | `if(gw_res_flag == 1) then > if(i_exist) then > do i=1,num_res_cells` | `res_cell`, `res_id`, `res_stage` |
| 1116 | header | `if(gw_res_flag == 1) then > if(i_exist) then` | `header` |
| 1117 | header | `if(gw_res_flag == 1) then > if(i_exist) then` | `header` |
| 1118 | data | `if(gw_res_flag == 1) then > if(i_exist) then` | `res_thick` |
| 1119 | data | `if(gw_res_flag == 1) then > if(i_exist) then` | `res_K` |
| 1120 | data | `if(gw_res_flag == 1) then > if(i_exist) then` | `num_res_cells` |
| 1121 | header | `if(gw_res_flag == 1) then > if(i_exist) then` | `header` |
| 1123 | data | `if(gw_res_flag == 1) then > if(i_exist) then > do i=1,num_res_cells` | `res_cell`, `res_id`, `res_stage` |


## `salt_atmo.cli`

- Schema diff status: `['runtime_arity.changed']`
- Review needed: no
- Base schema presence: `{'resolved_sections': ['runtime_arity'], 'unresolved_sections': []}`
- Candidate schema presence: `{'resolved_sections': ['runtime_arity'], 'unresolved_sections': []}`

### Base exact read evidence

- Procedure: `cli_read_atmodep_salt`
- Reader: `cli_read_atmodep_salt.f90`
- Match: exact_filename
- Resolved default filename(s): `salt_atmo.cli`
- Source filename expression(s): `salt_atmo.cli`
- Open: line 38, file expression `'salt_atmo.cli'`, parser value `salt_atmo.cli`, condition `if(cs_db%num_salts > 0) then > if(i_exist) then`

| Line | Role | Condition | Fields read |
| --- | --- | --- | --- |
| 39 | data | `if(cs_db%num_salts > 0) then > if(i_exist) then` | _no fields captured_ |
| 40 | data | `if(cs_db%num_salts > 0) then > if(i_exist) then` | _no fields captured_ |
| 41 | data | `if(cs_db%num_salts > 0) then > if(i_exist) then` | _no fields captured_ |
| 42 | data | `if(cs_db%num_salts > 0) then > if(i_exist) then` | _no fields captured_ |
| 43 | data | `if(cs_db%num_salts > 0) then > if(i_exist) then` | _no fields captured_ |
| 44 | data | `if(cs_db%num_salts > 0) then > if(i_exist) then` | _no fields captured_ |
| 57 | data | `if(cs_db%num_salts > 0) then > if(i_exist) then > do iadep = 1, atmodep_cont%num_sta > if (atmodep_cont%timestep == "aa") then` | `station_name` |
| 60 | data | `if(cs_db%num_salts > 0) then > if(i_exist) then > do iadep = 1, atmodep_cont%num_sta > if (atmodep_cont%timestep == "aa") then > do isalt=1,cs_db%num_salts` | `salt_ion`, `atmodep_salt(iadep)%salt(isalt)%rf` |
| 64 | data | `if(cs_db%num_salts > 0) then > if(i_exist) then > do iadep = 1, atmodep_cont%num_sta > if (atmodep_cont%timestep == "aa") then > do isalt=1,cs_db%num_salts` | `salt_ion`, `atmodep_salt(iadep)%salt(isalt)%dry` |
| 70 | data | `if(cs_db%num_salts > 0) then > if(i_exist) then > do iadep = 1, atmodep_cont%num_sta > if (atmodep_cont%timestep == "mo") then` | `station_name` |
| 73 | data | `if(cs_db%num_salts > 0) then > if(i_exist) then > do iadep = 1, atmodep_cont%num_sta > if (atmodep_cont%timestep == "mo") then > do isalt=1,cs_db%num_salts` | `salt_ion`, `(atmodep_salt(iadep)%salt(isalt)%rfmo(imo),imo=1,atmodep_cont%num)` |
| 77 | data | `if(cs_db%num_salts > 0) then > if(i_exist) then > do iadep = 1, atmodep_cont%num_sta > if (atmodep_cont%timestep == "mo") then > do isalt=1,cs_db%num_salts` | `salt_ion`, `(atmodep_salt(iadep)%salt(isalt)%drymo(imo),imo=1,atmodep_cont%num)` |
| 83 | data | `if(cs_db%num_salts > 0) then > if(i_exist) then > do iadep = 1, atmodep_cont%num_sta > if (atmodep_cont%timestep == "yr") then` | `station_name` |
| 86 | data | `if(cs_db%num_salts > 0) then > if(i_exist) then > do iadep = 1, atmodep_cont%num_sta > if (atmodep_cont%timestep == "yr") then > do isalt=1,cs_db%num_salts` | `salt_ion`, `(atmodep_salt(iadep)%salt(isalt)%rfyr(iyr),iyr=1,atmodep_cont%num)` |
| 90 | data | `if(cs_db%num_salts > 0) then > if(i_exist) then > do iadep = 1, atmodep_cont%num_sta > if (atmodep_cont%timestep == "yr") then > do isalt=1,cs_db%num_salts` | `salt_ion`, `(atmodep_salt(iadep)%salt(isalt)%dryyr(iyr),iyr=1,atmodep_cont%num)` |


### Candidate exact read evidence

- Procedure: `cli_read_atmodep_salt`
- Reader: `cli_read_atmodep_salt.f90`
- Match: exact_filename
- Resolved default filename(s): `salt_atmo.cli`
- Source filename expression(s): `salt_atmo.cli`
- Open: line 33, file expression `'salt_atmo.cli'`, parser value `salt_atmo.cli`, condition `if(cs_db%num_salts > 0) then > if(i_exist) then`

| Line | Role | Condition | Fields read |
| --- | --- | --- | --- |
| 34 | data | `if(cs_db%num_salts > 0) then > if(i_exist) then` | _no fields captured_ |
| 35 | data | `if(cs_db%num_salts > 0) then > if(i_exist) then` | _no fields captured_ |
| 36 | data | `if(cs_db%num_salts > 0) then > if(i_exist) then` | _no fields captured_ |
| 37 | data | `if(cs_db%num_salts > 0) then > if(i_exist) then` | _no fields captured_ |
| 38 | data | `if(cs_db%num_salts > 0) then > if(i_exist) then` | _no fields captured_ |
| 39 | data | `if(cs_db%num_salts > 0) then > if(i_exist) then` | _no fields captured_ |
| 52 | data | `if(cs_db%num_salts > 0) then > if(i_exist) then > do iadep = 1, atmodep_cont%num_sta > if (atmodep_cont%timestep == "aa") then` | `station_name` |
| 55 | data | `if(cs_db%num_salts > 0) then > if(i_exist) then > do iadep = 1, atmodep_cont%num_sta > if (atmodep_cont%timestep == "aa") then > do isalt=1,cs_db%num_salts` | `salt_ion`, `atmodep_salt(iadep)%salt(isalt)%rf` |
| 59 | data | `if(cs_db%num_salts > 0) then > if(i_exist) then > do iadep = 1, atmodep_cont%num_sta > if (atmodep_cont%timestep == "aa") then > do isalt=1,cs_db%num_salts` | `salt_ion`, `atmodep_salt(iadep)%salt(isalt)%dry` |
| 65 | data | `if(cs_db%num_salts > 0) then > if(i_exist) then > do iadep = 1, atmodep_cont%num_sta > if (atmodep_cont%timestep == "mo") then` | `station_name` |
| 68 | data | `if(cs_db%num_salts > 0) then > if(i_exist) then > do iadep = 1, atmodep_cont%num_sta > if (atmodep_cont%timestep == "mo") then > do isalt=1,cs_db%num_salts` | `salt_ion`, `(atmodep_salt(iadep)%salt(isalt)%rfmo(imo),imo=1,atmodep_cont%num)` |
| 72 | data | `if(cs_db%num_salts > 0) then > if(i_exist) then > do iadep = 1, atmodep_cont%num_sta > if (atmodep_cont%timestep == "mo") then > do isalt=1,cs_db%num_salts` | `salt_ion`, `(atmodep_salt(iadep)%salt(isalt)%drymo(imo),imo=1,atmodep_cont%num)` |
| 78 | data | `if(cs_db%num_salts > 0) then > if(i_exist) then > do iadep = 1, atmodep_cont%num_sta > if (atmodep_cont%timestep == "yr") then` | `station_name` |
| 81 | data | `if(cs_db%num_salts > 0) then > if(i_exist) then > do iadep = 1, atmodep_cont%num_sta > if (atmodep_cont%timestep == "yr") then > do isalt=1,cs_db%num_salts` | `salt_ion`, `(atmodep_salt(iadep)%salt(isalt)%rfyr(iyr),iyr=1,atmodep_cont%num)` |
| 85 | data | `if(cs_db%num_salts > 0) then > if(i_exist) then > do iadep = 1, atmodep_cont%num_sta > if (atmodep_cont%timestep == "yr") then > do isalt=1,cs_db%num_salts` | `salt_ion`, `(atmodep_salt(iadep)%salt(isalt)%dryyr(iyr),iyr=1,atmodep_cont%num)` |


## `salt_recall.rec`

- Schema diff status: `['runtime_arity.changed']`
- Review needed: no
- Base schema presence: `{'resolved_sections': ['runtime_arity'], 'unresolved_sections': []}`
- Candidate schema presence: `{'resolved_sections': ['runtime_arity'], 'unresolved_sections': []}`

### Base exact read evidence

- Procedure: `recall_read_salt`
- Reader: `recall_read_salt.f90`
- Match: exact_filename
- Resolved default filename(s): `salt_recall.rec`
- Source filename expression(s): `salt_recall.rec`
- Open: line 47, file expression `"salt_recall.rec"`, parser value `salt_recall.rec`, condition `if (i_exist .or. "salt_recall.rec" /= "null") then > do`

| Line | Role | Condition | Fields read |
| --- | --- | --- | --- |
| 48 | title | `if (i_exist .or. "salt_recall.rec" /= "null") then > do` | `titldum` |
| 50 | header | `if (i_exist .or. "salt_recall.rec" /= "null") then > do` | `header` |
| 56 | data | `if (i_exist .or. "salt_recall.rec" /= "null") then > do > do while (eof == 0)` | `i` |
| 102 | title | `if (i_exist .or. "salt_recall.rec" /= "null") then > do` | `titldum` |
| 104 | header | `if (i_exist .or. "salt_recall.rec" /= "null") then > do` | `header` |
| 110 | data | `if (i_exist .or. "salt_recall.rec" /= "null") then > do > do ii = 1, imax` | `i` |
| 113 | data | `if (i_exist .or. "salt_recall.rec" /= "null") then > do > do ii = 1, imax` | `k`, `rec_salt(i)%name`, `rec_salt(i)%typ`, `rec_salt(i)%filename` |


### Candidate exact read evidence

- Procedure: `recall_read_salt`
- Reader: `recall_read_salt.f90`
- Match: exact_filename
- Resolved default filename(s): `salt_recall.rec`
- Source filename expression(s): `salt_recall.rec`
- Open: line 43, file expression `"salt_recall.rec"`, parser value `salt_recall.rec`, condition `if (i_exist .or. "salt_recall.rec" /= "null") then > do`

| Line | Role | Condition | Fields read |
| --- | --- | --- | --- |
| 44 | title | `if (i_exist .or. "salt_recall.rec" /= "null") then > do` | `titldum` |
| 46 | header | `if (i_exist .or. "salt_recall.rec" /= "null") then > do` | `header` |
| 52 | data | `if (i_exist .or. "salt_recall.rec" /= "null") then > do > do while (eof == 0)` | `i` |
| 98 | title | `if (i_exist .or. "salt_recall.rec" /= "null") then > do` | `titldum` |
| 100 | header | `if (i_exist .or. "salt_recall.rec" /= "null") then > do` | `header` |
| 106 | data | `if (i_exist .or. "salt_recall.rec" /= "null") then > do > do ii = 1, imax` | `i` |
| 109 | data | `if (i_exist .or. "salt_recall.rec" /= "null") then > do > do ii = 1, imax` | `k`, `rec_salt(i)%name`, `rec_salt(i)%typ`, `rec_salt(i)%filename` |


## `satbuffer.str`

- Schema diff status: `['files.added']`
- Review needed: no
- Base schema presence: `{'resolved_sections': [], 'unresolved_sections': ['unresolved']}`
- Candidate schema presence: `{'resolved_sections': ['files'], 'unresolved_sections': []}`

### Base exact read evidence

_No exact base opened/read evidence found._

### Candidate exact read evidence

- Procedure: `sat_buff_read`
- Reader: `sat_buff_read.f90`
- Match: exact_filename
- Resolved default filename(s): `satbuffer.str`
- Source filename expression(s): `satbuffer.str`
- Open: line 34, file expression `"satbuffer.str"`, parser value `satbuffer.str`, condition `if(i_exist) then > do`

| Line | Role | Condition | Fields read |
| --- | --- | --- | --- |
| 35 | title | `if(i_exist) then > do` | `titldum` |
| 37 | header | `if(i_exist) then > do` | `header` |
| 40 | title | `if(i_exist) then > do > do while (eof == 0)` | `titldum` |
| 46 | title | `if(i_exist) then > do` | `titldum` |
| 48 | header | `if(i_exist) then > do` | `header` |
| 55 | data | `if(i_exist) then > do > do ibuff = 1, imax` | `satbuff_db(ibuff)` |


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
- Source filename expression(s): `in_cond%dtbl_scen`, `scen_lu.dtl`
- Open: line 34, file expression `in_cond%dtbl_scen`, parser value `scen_lu.dtl`, condition `if (.not. i_exist .or. in_cond%dtbl_scen == "null") then / else > do`

| Line | Role | Condition | Fields read |
| --- | --- | --- | --- |
| 35 | title | `if (.not. i_exist .or. in_cond%dtbl_scen == "null") then / else > do` | `titldum` |
| 37 | data | `if (.not. i_exist .or. in_cond%dtbl_scen == "null") then / else > do` | `mdtbl` |
| 39 | data | `if (.not. i_exist .or. in_cond%dtbl_scen == "null") then / else > do` | _no fields captured_ |
| 44 | header | `if (.not. i_exist .or. in_cond%dtbl_scen == "null") then / else > do > do i = 1, mdtbl` | `header` |
| 46 | data | `if (.not. i_exist .or. in_cond%dtbl_scen == "null") then / else > do > do i = 1, mdtbl` | `dtbl_scen(i)%name`, `dtbl_scen(i)%conds`, `dtbl_scen(i)%alts`, `dtbl_scen(i)%acts` |
| 57 | header | `if (.not. i_exist .or. in_cond%dtbl_scen == "null") then / else > do > do i = 1, mdtbl` | `header` |
| 60 | data | `if (.not. i_exist .or. in_cond%dtbl_scen == "null") then / else > do > do i = 1, mdtbl > do ic = 1, dtbl_scen(i)%conds` | `dtbl_scen(i)%cond(ic)`, `(dtbl_scen(i)%alt(ic,ial), ial = 1, dtbl_scen(i)%alts)` |
| 65 | header | `if (.not. i_exist .or. in_cond%dtbl_scen == "null") then / else > do > do i = 1, mdtbl` | `header` |
| 68 | data | `if (.not. i_exist .or. in_cond%dtbl_scen == "null") then / else > do > do i = 1, mdtbl > do iac = 1, dtbl_scen(i)%acts` | `dtbl_scen(i)%act(iac)`, `(dtbl_scen(i)%act_outcomes(iac,ial), ial = 1, dtbl_scen(i)%alts)` |
| 71 | data | `if (.not. i_exist .or. in_cond%dtbl_scen == "null") then / else > do > do i = 1, mdtbl` | _no fields captured_ |


### Candidate exact read evidence

- Procedure: `dtbl_scen_read`
- Reader: `dtbl_scen_read.f90`
- Match: exact_filename
- Resolved default filename(s): `scen_lu.dtl`
- Source filename expression(s): `in_cond%dtbl_scen`, `scen_lu.dtl`
- Open: line 35, file expression `in_cond%dtbl_scen`, parser value `scen_lu.dtl`, condition `if (.not. i_exist .or. in_cond%dtbl_scen == "null") then / else > do`

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


## `shade_factor.shf`

- Schema diff status: `['files.added']`
- Review needed: no
- Base schema presence: `{'resolved_sections': [], 'unresolved_sections': ['unresolved']}`
- Candidate schema presence: `{'resolved_sections': ['files'], 'unresolved_sections': []}`

### Base exact read evidence

_No exact base opened/read evidence found._

### Candidate exact read evidence

- Procedure: `shade_factor_read`
- Reader: `shade_factor_read.f90`
- Match: exact_filename
- Resolved default filename(s): `shade_factor.shf`
- Source filename expression(s): `in_shf%ssff_shf`, `shade_factor.shf`
- Open: line 30, file expression `in_shf%ssff_shf`, parser value `shade_factor.shf`, condition `if (.not. i_exist .or. in_shf%ssff_shf == "null") then / else > do`

| Line | Role | Condition | Fields read |
| --- | --- | --- | --- |
| 31 | title | `if (.not. i_exist .or. in_shf%ssff_shf == "null") then / else > do` | `titldum` |
| 33 | header | `if (.not. i_exist .or. in_shf%ssff_shf == "null") then / else > do` | `header` |
| 36 | title | `if (.not. i_exist .or. in_shf%ssff_shf == "null") then / else > do > do while (eof == 0)` | `titldum` |
| 44 | title | `if (.not. i_exist .or. in_shf%ssff_shf == "null") then / else > do` | `titldum` |
| 46 | header | `if (.not. i_exist .or. in_shf%ssff_shf == "null") then / else > do` | `header` |
| 50 | data | `if (.not. i_exist .or. in_shf%ssff_shf == "null") then / else > do > do idlsu = 1, imax` | `shf_db(idlsu)` |


## `solute.gw`

- Schema diff status: `['files.added']`
- Review needed: no
- Base schema presence: `{'resolved_sections': [], 'unresolved_sections': ['unresolved']}`
- Candidate schema presence: `{'resolved_sections': ['files'], 'unresolved_sections': []}`

### Base exact read evidence

_No exact base opened/read evidence found._

### Candidate exact read evidence

- Procedure: `gwflow_read`
- Reader: `gwflow_read.f90`
- Match: exact_filename
- Resolved default filename(s): `solute.gw`
- Source filename expression(s): `solute.gw`
- Open: line 1570, file expression `'solute.gw'`, parser value `solute.gw`, condition `if(gw_solute_flag == 1) then > if(i_exist) then`

| Line | Role | Condition | Fields read |
| --- | --- | --- | --- |
| 1622 | header | `if(gw_solute_flag == 1) then > if(i_exist) then` | `header` |
| 1623 | header | `if(gw_solute_flag == 1) then > if(i_exist) then` | `header` |
| 1624 | data | `if(gw_solute_flag == 1) then > if(i_exist) then` | `num_ts_transport` |
| 1625 | data | `if(gw_solute_flag == 1) then > if(i_exist) then` | `gw_long_disp` |
| 1632 | header | `if(gw_solute_flag == 1) then > if(i_exist) then` | `header` |
| 1634 | data | `if(gw_solute_flag == 1) then > if(i_exist) then > do s=1,gw_nsolute` | `name`, `gwsol_sorb(s)`, `gwsol_rctn(s)`, `canal_out_conc(s)` |


## `tile.gw`

- Schema diff status: `['files.added']`
- Review needed: no
- Base schema presence: `{'resolved_sections': [], 'unresolved_sections': ['unresolved']}`
- Candidate schema presence: `{'resolved_sections': ['files'], 'unresolved_sections': []}`

### Base exact read evidence

_No exact base opened/read evidence found._

### Candidate exact read evidence

- Procedure: `gwflow_read`
- Reader: `gwflow_read.f90`
- Match: exact_filename
- Resolved default filename(s): `tile.gw`
- Source filename expression(s): `tile.gw`
- Open: line 1001, file expression `'tile.gw'`, parser value `tile.gw`, condition `if(gw_tile_flag == 1) then > if(i_exist) then`

| Line | Role | Condition | Fields read |
| --- | --- | --- | --- |
| 1002 | header | `if(gw_tile_flag == 1) then > if(i_exist) then` | `header` |
| 1007 | data | `if(gw_tile_flag == 1) then > if(i_exist) then` | `tile_depth_val` |
| 1008 | data | `if(gw_tile_flag == 1) then > if(i_exist) then` | `tile_drain_area_val` |
| 1009 | data | `if(gw_tile_flag == 1) then > if(i_exist) then` | `tile_K_val` |
| 1022 | data | `if(gw_tile_flag == 1) then > if(i_exist) then` | `gw_tile_group_flag` |
| 1024 | data | `if(gw_tile_flag == 1) then > if(i_exist) then > if(gw_tile_group_flag.eq.1) then` | `gw_tile_num_group` |
| 1027 | data | `if(gw_tile_flag == 1) then > if(i_exist) then > if(gw_tile_group_flag.eq.1) then > do i=1,gw_tile_num_group` | _no fields captured_ |
| 1028 | data | `if(gw_tile_flag == 1) then > if(i_exist) then > if(gw_tile_group_flag.eq.1) then > do i=1,gw_tile_num_group` | `num_tile_cells(i)` |
| 1030 | data | `if(gw_tile_flag == 1) then > if(i_exist) then > if(gw_tile_group_flag.eq.1) then > do i=1,gw_tile_num_group > do j=1,num_tile_cells(i)` | `gw_tile_groups(i,j)` |
| 1039 | header | `if(gw_tile_flag == 1) then > if(i_exist) then` | `header` |
| 1042 | data | `if(gw_tile_flag == 1) then > if(i_exist) then > if(grid_type == "structured") then > do i=1,grid_nrow` | `(grid_int(i,j),j=1,grid_ncol)` |
| 1053 | data | `if(gw_tile_flag == 1) then > if(i_exist) then > if(grid_type == "structured") then / elseif(grid_type == "unstructured") then > do i=1,ncell` | `gw_state(i)%tile` |


## `tmp.cli`

- Schema diff status: `['multi_section.changed']`
- Review needed: no
- Base schema presence: `{'resolved_sections': ['multi_section'], 'unresolved_sections': []}`
- Candidate schema presence: `{'resolved_sections': ['multi_section'], 'unresolved_sections': []}`

### Base exact read evidence

- Procedure: `cli_tmeas`
- Reader: `cli_tmeas.f90`
- Match: exact_filename
- Resolved default filename(s): `tmp.cli`
- Source filename expression(s): `in_cli%tmp_cli`, `tmp.cli`
- Open: line 38, file expression `in_cli%tmp_cli`, parser value `tmp.cli`, condition `if (.not. i_exist .or. in_cli%tmp_cli == "null") then / else > do`

| Line | Role | Condition | Fields read |
| --- | --- | --- | --- |
| 39 | title | `if (.not. i_exist .or. in_cli%tmp_cli == "null") then / else > do` | `titldum` |
| 41 | header | `if (.not. i_exist .or. in_cli%tmp_cli == "null") then / else > do` | `header` |
| 45 | title | `if (.not. i_exist .or. in_cli%tmp_cli == "null") then / else > do > do while (eof == 0)` | `titldum` |
| 54 | title | `if (.not. i_exist .or. in_cli%tmp_cli == "null") then / else > do` | `titldum` |
| 56 | header | `if (.not. i_exist .or. in_cli%tmp_cli == "null") then / else > do` | `header` |
| 59 | data | `if (.not. i_exist .or. in_cli%tmp_cli == "null") then / else > do > do i = 1, imax` | `tmp_n(i)` |
| 64 | title | `if (.not. i_exist .or. in_cli%tmp_cli == "null") then / else > do` | `titldum` |
| 66 | header | `if (.not. i_exist .or. in_cli%tmp_cli == "null") then / else > do` | `header` |
| 70 | data | `if (.not. i_exist .or. in_cli%tmp_cli == "null") then / else > do > do i = 1, imax` | `tmp(i)%filename` |


### Candidate exact read evidence

- Procedure: `cli_tmeas`
- Reader: `cli_tmeas.f90`
- Match: exact_filename
- Resolved default filename(s): `tmp.cli`
- Source filename expression(s): `in_cli%tmp_cli`, `tmp.cli`
- Open: line 40, file expression `in_cli%tmp_cli`, parser value `tmp.cli`, condition `if (.not. i_exist .or. in_cli%tmp_cli == "null") then / else > do`

| Line | Role | Condition | Fields read |
| --- | --- | --- | --- |
| 41 | title | `if (.not. i_exist .or. in_cli%tmp_cli == "null") then / else > do` | `titldum` |
| 43 | header | `if (.not. i_exist .or. in_cli%tmp_cli == "null") then / else > do` | `header` |
| 47 | title | `if (.not. i_exist .or. in_cli%tmp_cli == "null") then / else > do > do while (eof == 0)` | `titldum` |
| 56 | title | `if (.not. i_exist .or. in_cli%tmp_cli == "null") then / else > do` | `titldum` |
| 58 | header | `if (.not. i_exist .or. in_cli%tmp_cli == "null") then / else > do` | `header` |
| 61 | data | `if (.not. i_exist .or. in_cli%tmp_cli == "null") then / else > do > do i = 1, imax` | `tmp_n(i)` |
| 66 | title | `if (.not. i_exist .or. in_cli%tmp_cli == "null") then / else > do` | `titldum` |
| 68 | header | `if (.not. i_exist .or. in_cli%tmp_cli == "null") then / else > do` | `header` |
| 72 | data | `if (.not. i_exist .or. in_cli%tmp_cli == "null") then / else > do > do i = 1, imax` | `tmp(i)%filename` |


## `tvheads.gw`

- Schema diff status: `['runtime_arity.added']`
- Review needed: no
- Base schema presence: `{'resolved_sections': [], 'unresolved_sections': ['runtime_arity_unresolved']}`
- Candidate schema presence: `{'resolved_sections': ['runtime_arity'], 'unresolved_sections': []}`

### Base exact read evidence

_No exact base opened/read evidence found._

### Candidate exact read evidence

- Procedure: `gwflow_read`
- Reader: `gwflow_read.f90`
- Match: exact_filename
- Resolved default filename(s): `tvheads.gw`
- Source filename expression(s): `tvheads.gw`
- Open: line 1440, file expression `'tvheads.gw'`, parser value `tvheads.gw`, condition `if(i_exist) then`

| Line | Role | Condition | Fields read |
| --- | --- | --- | --- |
| 1441 | header | `if(i_exist) then` | `header` |
| 1442 | header | `if(i_exist) then` | `header` |
| 1446 | data | `if(i_exist) then > do` | `cell_id` |
| 1453 | header | `if(i_exist) then` | `header` |
| 1454 | header | `if(i_exist) then` | `header` |
| 1456 | data | `if(i_exist) then > do i=1,gw_ntvh` | `cell_id`, `(gw_tvh_vals(i,j),j=1,time%nbyr)` |


## `water_allocation.wro`

- Schema diff status: `['multi_record.changed']`
- Review needed: no
- Base schema presence: `{'resolved_sections': ['multi_record'], 'unresolved_sections': []}`
- Candidate schema presence: `{'resolved_sections': ['multi_record'], 'unresolved_sections': []}`

### Base exact read evidence

- Procedure: `water_allocation_read`
- Reader: `water_allocation_read.f90`
- Match: exact_filename
- Resolved default filename(s): `water_allocation.wro`
- Source filename expression(s): `in_watrts%transfer_wro`, `water_allocation.wro`
- Open: line 41, file expression `in_watrts%transfer_wro`, parser value `water_allocation.wro`, condition `if (.not. i_exist .or. in_watrts%transfer_wro == "null") then / else > do`

| Line | Role | Condition | Fields read |
| --- | --- | --- | --- |
| 42 | title | `if (.not. i_exist .or. in_watrts%transfer_wro == "null") then / else > do` | `titldum` |
| 44 | count | `if (.not. i_exist .or. in_watrts%transfer_wro == "null") then / else > do` | `imax` |
| 55 | header | `if (.not. i_exist .or. in_watrts%transfer_wro == "null") then / else > do > do iwro = 1, imax` | `header` |
| 57 | data | `if (.not. i_exist .or. in_watrts%transfer_wro == "null") then / else > do > do iwro = 1, imax` | `wallo(iwro)%name`, `wallo(iwro)%rule_typ`, `wallo(iwro)%src_obs`, `wallo(iwro)%dmd_obs`, `wallo(iwro)%cha_ob` |
| 60 | header | `if (.not. i_exist .or. in_watrts%transfer_wro == "null") then / else > do > do iwro = 1, imax` | `header` |
| 73 | data | `if (.not. i_exist .or. in_watrts%transfer_wro == "null") then / else > do > do iwro = 1, imax > do isrc = 1, wallo(iwro)%src_obs` | `i` |
| 77 | data | `if (.not. i_exist .or. in_watrts%transfer_wro == "null") then / else > do > do iwro = 1, imax > do isrc = 1, wallo(iwro)%src_obs` | `k`, `wallo(iwro)%src(i)%ob_typ` |
| 81 | data | `if (.not. i_exist .or. in_watrts%transfer_wro == "null") then / else > do > do iwro = 1, imax > do isrc = 1, wallo(iwro)%src_obs > if (wallo(iwro)%src(i)%ob_typ == "div_in") then` | `k`, `wallo(iwro)%src(i)%ob_typ`, `wallo(iwro)%src(i)%div_rec` |
| 90 | data | `if (.not. i_exist .or. in_watrts%transfer_wro == "null") then / else > do > do iwro = 1, imax > do isrc = 1, wallo(iwro)%src_obs > if (wallo(iwro)%src(i)%ob_typ == "div_in") then / else` | `k`, `wallo(iwro)%src(i)%ob_typ`, `wallo(iwro)%src(i)%ob_num`, `wallo(iwro)%src(i)%limit_mon` |
| 101 | header | `if (.not. i_exist .or. in_watrts%transfer_wro == "null") then / else > do > do iwro = 1, imax` | `header` |
| 104 | data | `if (.not. i_exist .or. in_watrts%transfer_wro == "null") then / else > do > do iwro = 1, imax > do idmd = 1, num_objs` | `i` |
| 108 | data | `if (.not. i_exist .or. in_watrts%transfer_wro == "null") then / else > do > do iwro = 1, imax > do idmd = 1, num_objs` | `k`, `wallo(iwro)%dmd(i)%ob_typ`, `wallo(iwro)%dmd(i)%ob_num`, `wallo(iwro)%dmd(i)%withdr`, `wallo(iwro)%dmd(i)%amount`, `wallo(iwro)%dmd(i)%right`, `wallo(iwro)%dmd(i)%treat_typ`, `wallo(iwro)%dmd(i)%treatment`, `wallo(iwro)%dmd(i)%rcv_ob`, `wallo(iwro)%dmd(i)%rcv_num`, `wallo(iwro)%dmd(i)%rcv_dtl`, `num_objs` |
| 173 | data | `if (.not. i_exist .or. in_watrts%transfer_wro == "null") then / else > do > do iwro = 1, imax > do idmd = 1, num_objs` | `k`, `wallo(iwro)%dmd(i)%ob_typ`, `wallo(iwro)%dmd(i)%ob_num`, `wallo(iwro)%dmd(i)%withdr`, `wallo(iwro)%dmd(i)%amount`, `wallo(iwro)%dmd(i)%right`, `wallo(iwro)%dmd(i)%treat_typ`, `wallo(iwro)%dmd(i)%treatment`, `wallo(iwro)%dmd(i)%rcv_ob`, `wallo(iwro)%dmd(i)%rcv_num`, `wallo(iwro)%dmd(i)%rcv_dtl`, `wallo(iwro)%dmd(i)%dmd_src_obs`, `(wallo(iwro)%dmd(i)%src(isrc), isrc = 1, num_objs)` |
| 213 | data | `if (.not. i_exist .or. in_watrts%transfer_wro == "null") then / else > do > do iwro = 1, imax > if(div_found == 1) then` | _no fields captured_ |
| 214 | data | `if (.not. i_exist .or. in_watrts%transfer_wro == "null") then / else > do > do iwro = 1, imax > if(div_found == 1) then` | `div_delay` |


### Candidate exact read evidence

- Procedure: `water_allocation_read`
- Reader: `water_allocation_read.f90`
- Match: exact_filename
- Resolved default filename(s): `water_allocation.wro`
- Source filename expression(s): `in_watrts%transfer_wro`, `water_allocation.wro`
- Open: line 47, file expression `in_watrts%transfer_wro`, parser value `water_allocation.wro`, condition `if (.not. i_exist .or. in_watrts%transfer_wro == "null") then / else > do`

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


## `water_canal.wal`

- Schema diff status: `['runtime_arity.added']`
- Review needed: no
- Base schema presence: `{'resolved_sections': [], 'unresolved_sections': ['runtime_arity_unresolved']}`
- Candidate schema presence: `{'resolved_sections': ['runtime_arity'], 'unresolved_sections': []}`

### Base exact read evidence

_No exact base opened/read evidence found._

### Base related read evidence

- Procedure: `header_water_allocation`
- Reader: `header_water_allocation.f90`
- Match: shared filename tokens
- Resolved default filename(s): `water_allo_yr.txt`
- Source filename expression(s): `water_allo_yr.txt`
- Open: line 46, file expression `"water_allo_yr.txt"`, parser value `water_allo_yr.txt`, condition `if (db_mx%wallo_db > 0) then > if (pco%water_allo%y == "y") then`
- Reads: _none captured_

- Procedure: `header_water_allocation`
- Reader: `header_water_allocation.f90`
- Match: shared filename tokens
- Resolved default filename(s): `water_allo_yr.csv`
- Source filename expression(s): `water_allo_yr.csv`
- Open: line 52, file expression `"water_allo_yr.csv"`, parser value `water_allo_yr.csv`, condition `if (db_mx%wallo_db > 0) then > if (pco%water_allo%y == "y") then > if (pco%csvout == "y") then`
- Reads: _none captured_

- Procedure: `header_water_allocation`
- Reader: `header_water_allocation.f90`
- Match: shared filename tokens
- Resolved default filename(s): `water_allo_aa.txt`
- Source filename expression(s): `water_allo_aa.txt`
- Open: line 63, file expression `"water_allo_aa.txt"`, parser value `water_allo_aa.txt`, condition `if (db_mx%wallo_db > 0) then > if (pco%water_allo%a == "y") then`
- Reads: _none captured_

- Procedure: `header_water_allocation`
- Reader: `header_water_allocation.f90`
- Match: shared filename tokens
- Resolved default filename(s): `water_allo_aa.csv`
- Source filename expression(s): `water_allo_aa.csv`
- Open: line 69, file expression `"water_allo_aa.csv"`, parser value `water_allo_aa.csv`, condition `if (db_mx%wallo_db > 0) then > if (pco%water_allo%a == "y") then > if (pco%csvout == "y") then`
- Reads: _none captured_

- Procedure: `water_allocation_read`
- Reader: `water_allocation_read.f90`
- Match: shared filename tokens
- Resolved default filename(s): `water_allocation.wro`
- Source filename expression(s): `in_watrts%transfer_wro`, `water_allocation.wro`
- Open: line 41, file expression `in_watrts%transfer_wro`, parser value `water_allocation.wro`, condition `if (.not. i_exist .or. in_watrts%transfer_wro == "null") then / else > do`

| Line | Role | Condition | Fields read |
| --- | --- | --- | --- |
| 42 | title | `if (.not. i_exist .or. in_watrts%transfer_wro == "null") then / else > do` | `titldum` |
| 44 | count | `if (.not. i_exist .or. in_watrts%transfer_wro == "null") then / else > do` | `imax` |
| 55 | header | `if (.not. i_exist .or. in_watrts%transfer_wro == "null") then / else > do > do iwro = 1, imax` | `header` |
| 57 | data | `if (.not. i_exist .or. in_watrts%transfer_wro == "null") then / else > do > do iwro = 1, imax` | `wallo(iwro)%name`, `wallo(iwro)%rule_typ`, `wallo(iwro)%src_obs`, `wallo(iwro)%dmd_obs`, `wallo(iwro)%cha_ob` |
| 60 | header | `if (.not. i_exist .or. in_watrts%transfer_wro == "null") then / else > do > do iwro = 1, imax` | `header` |
| 73 | data | `if (.not. i_exist .or. in_watrts%transfer_wro == "null") then / else > do > do iwro = 1, imax > do isrc = 1, wallo(iwro)%src_obs` | `i` |
| 77 | data | `if (.not. i_exist .or. in_watrts%transfer_wro == "null") then / else > do > do iwro = 1, imax > do isrc = 1, wallo(iwro)%src_obs` | `k`, `wallo(iwro)%src(i)%ob_typ` |
| 81 | data | `if (.not. i_exist .or. in_watrts%transfer_wro == "null") then / else > do > do iwro = 1, imax > do isrc = 1, wallo(iwro)%src_obs > if (wallo(iwro)%src(i)%ob_typ == "div_in") then` | `k`, `wallo(iwro)%src(i)%ob_typ`, `wallo(iwro)%src(i)%div_rec` |
| 90 | data | `if (.not. i_exist .or. in_watrts%transfer_wro == "null") then / else > do > do iwro = 1, imax > do isrc = 1, wallo(iwro)%src_obs > if (wallo(iwro)%src(i)%ob_typ == "div_in") then / else` | `k`, `wallo(iwro)%src(i)%ob_typ`, `wallo(iwro)%src(i)%ob_num`, `wallo(iwro)%src(i)%limit_mon` |
| 101 | header | `if (.not. i_exist .or. in_watrts%transfer_wro == "null") then / else > do > do iwro = 1, imax` | `header` |
| 104 | data | `if (.not. i_exist .or. in_watrts%transfer_wro == "null") then / else > do > do iwro = 1, imax > do idmd = 1, num_objs` | `i` |
| 108 | data | `if (.not. i_exist .or. in_watrts%transfer_wro == "null") then / else > do > do iwro = 1, imax > do idmd = 1, num_objs` | `k`, `wallo(iwro)%dmd(i)%ob_typ`, `wallo(iwro)%dmd(i)%ob_num`, `wallo(iwro)%dmd(i)%withdr`, `wallo(iwro)%dmd(i)%amount`, `wallo(iwro)%dmd(i)%right`, `wallo(iwro)%dmd(i)%treat_typ`, `wallo(iwro)%dmd(i)%treatment`, `wallo(iwro)%dmd(i)%rcv_ob`, `wallo(iwro)%dmd(i)%rcv_num`, `wallo(iwro)%dmd(i)%rcv_dtl`, `num_objs` |
| 173 | data | `if (.not. i_exist .or. in_watrts%transfer_wro == "null") then / else > do > do iwro = 1, imax > do idmd = 1, num_objs` | `k`, `wallo(iwro)%dmd(i)%ob_typ`, `wallo(iwro)%dmd(i)%ob_num`, `wallo(iwro)%dmd(i)%withdr`, `wallo(iwro)%dmd(i)%amount`, `wallo(iwro)%dmd(i)%right`, `wallo(iwro)%dmd(i)%treat_typ`, `wallo(iwro)%dmd(i)%treatment`, `wallo(iwro)%dmd(i)%rcv_ob`, `wallo(iwro)%dmd(i)%rcv_num`, `wallo(iwro)%dmd(i)%rcv_dtl`, `wallo(iwro)%dmd(i)%dmd_src_obs`, `(wallo(iwro)%dmd(i)%src(isrc), isrc = 1, num_objs)` |
| 213 | data | `if (.not. i_exist .or. in_watrts%transfer_wro == "null") then / else > do > do iwro = 1, imax > if(div_found == 1) then` | _no fields captured_ |
| 214 | data | `if (.not. i_exist .or. in_watrts%transfer_wro == "null") then / else > do > do iwro = 1, imax > if(div_found == 1) then` | `div_delay` |


### Candidate exact read evidence

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


## `water_pipe.wal`

- Schema diff status: `['runtime_arity.added']`
- Review needed: no
- Base schema presence: `{'resolved_sections': [], 'unresolved_sections': ['runtime_arity_unresolved']}`
- Candidate schema presence: `{'resolved_sections': ['runtime_arity'], 'unresolved_sections': []}`

### Base exact read evidence

_No exact base opened/read evidence found._

### Base related read evidence

- Procedure: `om_water_init`
- Reader: `om_water_init.f90`
- Match: shared filename tokens
- Resolved default filename(s): `om_water.ini`
- Source filename expression(s): `in_init%om_water`, `om_water.ini`
- Open: line 29, file expression `in_init%om_water`, parser value `om_water.ini`, condition `if (.not. i_exist .or. in_init%om_water == "null") then / else > do`

| Line | Role | Condition | Fields read |
| --- | --- | --- | --- |
| 30 | title | `if (.not. i_exist .or. in_init%om_water == "null") then / else > do` | `titldum` |
| 32 | header | `if (.not. i_exist .or. in_init%om_water == "null") then / else > do` | `header` |
| 35 | title | `if (.not. i_exist .or. in_init%om_water == "null") then / else > do > do while (eof == 0)` | `titldum` |
| 45 | title | `if (.not. i_exist .or. in_init%om_water == "null") then / else > do` | `titldum` |
| 47 | header | `if (.not. i_exist .or. in_init%om_water == "null") then / else > do` | `header` |
| 51 | title | `if (.not. i_exist .or. in_init%om_water == "null") then / else > do > do ichi = 1, db_mx%om_water_init` | `titldum` |
| 54 | data | `if (.not. i_exist .or. in_init%om_water == "null") then / else > do > do ichi = 1, db_mx%om_water_init` | `om_init_name(ichi)`, `om_init_water(ichi)` |

- Procedure: `header_water_allocation`
- Reader: `header_water_allocation.f90`
- Match: shared filename tokens
- Resolved default filename(s): `water_allo_yr.txt`
- Source filename expression(s): `water_allo_yr.txt`
- Open: line 46, file expression `"water_allo_yr.txt"`, parser value `water_allo_yr.txt`, condition `if (db_mx%wallo_db > 0) then > if (pco%water_allo%y == "y") then`
- Reads: _none captured_

- Procedure: `header_water_allocation`
- Reader: `header_water_allocation.f90`
- Match: shared filename tokens
- Resolved default filename(s): `water_allo_yr.csv`
- Source filename expression(s): `water_allo_yr.csv`
- Open: line 52, file expression `"water_allo_yr.csv"`, parser value `water_allo_yr.csv`, condition `if (db_mx%wallo_db > 0) then > if (pco%water_allo%y == "y") then > if (pco%csvout == "y") then`
- Reads: _none captured_

- Procedure: `header_water_allocation`
- Reader: `header_water_allocation.f90`
- Match: shared filename tokens
- Resolved default filename(s): `water_allo_aa.txt`
- Source filename expression(s): `water_allo_aa.txt`
- Open: line 63, file expression `"water_allo_aa.txt"`, parser value `water_allo_aa.txt`, condition `if (db_mx%wallo_db > 0) then > if (pco%water_allo%a == "y") then`
- Reads: _none captured_

- Procedure: `header_water_allocation`
- Reader: `header_water_allocation.f90`
- Match: shared filename tokens
- Resolved default filename(s): `water_allo_aa.csv`
- Source filename expression(s): `water_allo_aa.csv`
- Open: line 69, file expression `"water_allo_aa.csv"`, parser value `water_allo_aa.csv`, condition `if (db_mx%wallo_db > 0) then > if (pco%water_allo%a == "y") then > if (pco%csvout == "y") then`
- Reads: _none captured_


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
| 52 | data | `if (.not. i_exist .or. 'water_pipe.wal' == "null") then / else > do > do ipipe = 1, imax` | `i`, `pipe(ipipe)%name`, `pipe(ipipe)%stor_mx`, `pipe(ipipe)%ddown_days`, `pipe(ipipe)%loss_fr`, `pipe(ipipe)%num_aqu`, `(pipe(ipipe)%aqu_loss(iaq), iaq = 1, num_aqu)` |


## `water_tower.wal`

- Schema diff status: `['files.added']`
- Review needed: no
- Base schema presence: `{'resolved_sections': [], 'unresolved_sections': ['unresolved']}`
- Candidate schema presence: `{'resolved_sections': ['files'], 'unresolved_sections': []}`

### Base exact read evidence

_No exact base opened/read evidence found._

### Base related read evidence

- Procedure: `header_water_allocation`
- Reader: `header_water_allocation.f90`
- Match: shared filename tokens
- Resolved default filename(s): `water_allo_yr.txt`
- Source filename expression(s): `water_allo_yr.txt`
- Open: line 46, file expression `"water_allo_yr.txt"`, parser value `water_allo_yr.txt`, condition `if (db_mx%wallo_db > 0) then > if (pco%water_allo%y == "y") then`
- Reads: _none captured_

- Procedure: `header_water_allocation`
- Reader: `header_water_allocation.f90`
- Match: shared filename tokens
- Resolved default filename(s): `water_allo_yr.csv`
- Source filename expression(s): `water_allo_yr.csv`
- Open: line 52, file expression `"water_allo_yr.csv"`, parser value `water_allo_yr.csv`, condition `if (db_mx%wallo_db > 0) then > if (pco%water_allo%y == "y") then > if (pco%csvout == "y") then`
- Reads: _none captured_

- Procedure: `header_water_allocation`
- Reader: `header_water_allocation.f90`
- Match: shared filename tokens
- Resolved default filename(s): `water_allo_aa.txt`
- Source filename expression(s): `water_allo_aa.txt`
- Open: line 63, file expression `"water_allo_aa.txt"`, parser value `water_allo_aa.txt`, condition `if (db_mx%wallo_db > 0) then > if (pco%water_allo%a == "y") then`
- Reads: _none captured_

- Procedure: `header_water_allocation`
- Reader: `header_water_allocation.f90`
- Match: shared filename tokens
- Resolved default filename(s): `water_allo_aa.csv`
- Source filename expression(s): `water_allo_aa.csv`
- Open: line 69, file expression `"water_allo_aa.csv"`, parser value `water_allo_aa.csv`, condition `if (db_mx%wallo_db > 0) then > if (pco%water_allo%a == "y") then > if (pco%csvout == "y") then`
- Reads: _none captured_

- Procedure: `header_water_allocation`
- Reader: `header_water_allocation.f90`
- Match: shared filename tokens
- Resolved default filename(s): `water_allo_day.txt`
- Source filename expression(s): `water_allo_day.txt`
- Open: line 12, file expression `"water_allo_day.txt"`, parser value `water_allo_day.txt`, condition `if (db_mx%wallo_db > 0) then > if (pco%water_allo%d == "y") then`
- Reads: _none captured_


### Candidate exact read evidence

- Procedure: `water_tower_read`
- Reader: `water_tower_read.f90`
- Match: exact_filename
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


## `water_treat.wal`

- Schema diff status: `['runtime_arity.added']`
- Review needed: no
- Base schema presence: `{'resolved_sections': [], 'unresolved_sections': ['runtime_arity_unresolved']}`
- Candidate schema presence: `{'resolved_sections': ['runtime_arity'], 'unresolved_sections': []}`

### Base exact read evidence

_No exact base opened/read evidence found._

### Base related read evidence

- Procedure: `header_water_allocation`
- Reader: `header_water_allocation.f90`
- Match: shared filename tokens
- Resolved default filename(s): `water_allo_yr.txt`
- Source filename expression(s): `water_allo_yr.txt`
- Open: line 46, file expression `"water_allo_yr.txt"`, parser value `water_allo_yr.txt`, condition `if (db_mx%wallo_db > 0) then > if (pco%water_allo%y == "y") then`
- Reads: _none captured_

- Procedure: `header_water_allocation`
- Reader: `header_water_allocation.f90`
- Match: shared filename tokens
- Resolved default filename(s): `water_allo_yr.csv`
- Source filename expression(s): `water_allo_yr.csv`
- Open: line 52, file expression `"water_allo_yr.csv"`, parser value `water_allo_yr.csv`, condition `if (db_mx%wallo_db > 0) then > if (pco%water_allo%y == "y") then > if (pco%csvout == "y") then`
- Reads: _none captured_

- Procedure: `header_water_allocation`
- Reader: `header_water_allocation.f90`
- Match: shared filename tokens
- Resolved default filename(s): `water_allo_aa.txt`
- Source filename expression(s): `water_allo_aa.txt`
- Open: line 63, file expression `"water_allo_aa.txt"`, parser value `water_allo_aa.txt`, condition `if (db_mx%wallo_db > 0) then > if (pco%water_allo%a == "y") then`
- Reads: _none captured_

- Procedure: `header_water_allocation`
- Reader: `header_water_allocation.f90`
- Match: shared filename tokens
- Resolved default filename(s): `water_allo_aa.csv`
- Source filename expression(s): `water_allo_aa.csv`
- Open: line 69, file expression `"water_allo_aa.csv"`, parser value `water_allo_aa.csv`, condition `if (db_mx%wallo_db > 0) then > if (pco%water_allo%a == "y") then > if (pco%csvout == "y") then`
- Reads: _none captured_

- Procedure: `water_allocation_read`
- Reader: `water_allocation_read.f90`
- Match: shared filename tokens
- Resolved default filename(s): `water_allocation.wro`
- Source filename expression(s): `in_watrts%transfer_wro`, `water_allocation.wro`
- Open: line 41, file expression `in_watrts%transfer_wro`, parser value `water_allocation.wro`, condition `if (.not. i_exist .or. in_watrts%transfer_wro == "null") then / else > do`

| Line | Role | Condition | Fields read |
| --- | --- | --- | --- |
| 42 | title | `if (.not. i_exist .or. in_watrts%transfer_wro == "null") then / else > do` | `titldum` |
| 44 | count | `if (.not. i_exist .or. in_watrts%transfer_wro == "null") then / else > do` | `imax` |
| 55 | header | `if (.not. i_exist .or. in_watrts%transfer_wro == "null") then / else > do > do iwro = 1, imax` | `header` |
| 57 | data | `if (.not. i_exist .or. in_watrts%transfer_wro == "null") then / else > do > do iwro = 1, imax` | `wallo(iwro)%name`, `wallo(iwro)%rule_typ`, `wallo(iwro)%src_obs`, `wallo(iwro)%dmd_obs`, `wallo(iwro)%cha_ob` |
| 60 | header | `if (.not. i_exist .or. in_watrts%transfer_wro == "null") then / else > do > do iwro = 1, imax` | `header` |
| 73 | data | `if (.not. i_exist .or. in_watrts%transfer_wro == "null") then / else > do > do iwro = 1, imax > do isrc = 1, wallo(iwro)%src_obs` | `i` |
| 77 | data | `if (.not. i_exist .or. in_watrts%transfer_wro == "null") then / else > do > do iwro = 1, imax > do isrc = 1, wallo(iwro)%src_obs` | `k`, `wallo(iwro)%src(i)%ob_typ` |
| 81 | data | `if (.not. i_exist .or. in_watrts%transfer_wro == "null") then / else > do > do iwro = 1, imax > do isrc = 1, wallo(iwro)%src_obs > if (wallo(iwro)%src(i)%ob_typ == "div_in") then` | `k`, `wallo(iwro)%src(i)%ob_typ`, `wallo(iwro)%src(i)%div_rec` |
| 90 | data | `if (.not. i_exist .or. in_watrts%transfer_wro == "null") then / else > do > do iwro = 1, imax > do isrc = 1, wallo(iwro)%src_obs > if (wallo(iwro)%src(i)%ob_typ == "div_in") then / else` | `k`, `wallo(iwro)%src(i)%ob_typ`, `wallo(iwro)%src(i)%ob_num`, `wallo(iwro)%src(i)%limit_mon` |
| 101 | header | `if (.not. i_exist .or. in_watrts%transfer_wro == "null") then / else > do > do iwro = 1, imax` | `header` |
| 104 | data | `if (.not. i_exist .or. in_watrts%transfer_wro == "null") then / else > do > do iwro = 1, imax > do idmd = 1, num_objs` | `i` |
| 108 | data | `if (.not. i_exist .or. in_watrts%transfer_wro == "null") then / else > do > do iwro = 1, imax > do idmd = 1, num_objs` | `k`, `wallo(iwro)%dmd(i)%ob_typ`, `wallo(iwro)%dmd(i)%ob_num`, `wallo(iwro)%dmd(i)%withdr`, `wallo(iwro)%dmd(i)%amount`, `wallo(iwro)%dmd(i)%right`, `wallo(iwro)%dmd(i)%treat_typ`, `wallo(iwro)%dmd(i)%treatment`, `wallo(iwro)%dmd(i)%rcv_ob`, `wallo(iwro)%dmd(i)%rcv_num`, `wallo(iwro)%dmd(i)%rcv_dtl`, `num_objs` |
| 173 | data | `if (.not. i_exist .or. in_watrts%transfer_wro == "null") then / else > do > do iwro = 1, imax > do idmd = 1, num_objs` | `k`, `wallo(iwro)%dmd(i)%ob_typ`, `wallo(iwro)%dmd(i)%ob_num`, `wallo(iwro)%dmd(i)%withdr`, `wallo(iwro)%dmd(i)%amount`, `wallo(iwro)%dmd(i)%right`, `wallo(iwro)%dmd(i)%treat_typ`, `wallo(iwro)%dmd(i)%treatment`, `wallo(iwro)%dmd(i)%rcv_ob`, `wallo(iwro)%dmd(i)%rcv_num`, `wallo(iwro)%dmd(i)%rcv_dtl`, `wallo(iwro)%dmd(i)%dmd_src_obs`, `(wallo(iwro)%dmd(i)%src(isrc), isrc = 1, num_objs)` |
| 213 | data | `if (.not. i_exist .or. in_watrts%transfer_wro == "null") then / else > do > do iwro = 1, imax > if(div_found == 1) then` | _no fields captured_ |
| 214 | data | `if (.not. i_exist .or. in_watrts%transfer_wro == "null") then / else > do > do iwro = 1, imax > if(div_found == 1) then` | `div_delay` |


### Candidate exact read evidence

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


## `water_use.wal`

- Schema diff status: `['runtime_arity.added']`
- Review needed: no
- Base schema presence: `{'resolved_sections': [], 'unresolved_sections': ['runtime_arity_unresolved']}`
- Candidate schema presence: `{'resolved_sections': ['runtime_arity'], 'unresolved_sections': []}`

### Base exact read evidence

_No exact base opened/read evidence found._

### Base related read evidence

- Procedure: `header_water_allocation`
- Reader: `header_water_allocation.f90`
- Match: shared filename tokens
- Resolved default filename(s): `water_allo_yr.txt`
- Source filename expression(s): `water_allo_yr.txt`
- Open: line 46, file expression `"water_allo_yr.txt"`, parser value `water_allo_yr.txt`, condition `if (db_mx%wallo_db > 0) then > if (pco%water_allo%y == "y") then`
- Reads: _none captured_

- Procedure: `header_water_allocation`
- Reader: `header_water_allocation.f90`
- Match: shared filename tokens
- Resolved default filename(s): `water_allo_yr.csv`
- Source filename expression(s): `water_allo_yr.csv`
- Open: line 52, file expression `"water_allo_yr.csv"`, parser value `water_allo_yr.csv`, condition `if (db_mx%wallo_db > 0) then > if (pco%water_allo%y == "y") then > if (pco%csvout == "y") then`
- Reads: _none captured_

- Procedure: `header_water_allocation`
- Reader: `header_water_allocation.f90`
- Match: shared filename tokens
- Resolved default filename(s): `water_allo_aa.txt`
- Source filename expression(s): `water_allo_aa.txt`
- Open: line 63, file expression `"water_allo_aa.txt"`, parser value `water_allo_aa.txt`, condition `if (db_mx%wallo_db > 0) then > if (pco%water_allo%a == "y") then`
- Reads: _none captured_

- Procedure: `header_water_allocation`
- Reader: `header_water_allocation.f90`
- Match: shared filename tokens
- Resolved default filename(s): `water_allo_aa.csv`
- Source filename expression(s): `water_allo_aa.csv`
- Open: line 69, file expression `"water_allo_aa.csv"`, parser value `water_allo_aa.csv`, condition `if (db_mx%wallo_db > 0) then > if (pco%water_allo%a == "y") then > if (pco%csvout == "y") then`
- Reads: _none captured_

- Procedure: `header_water_allocation`
- Reader: `header_water_allocation.f90`
- Match: shared filename tokens
- Resolved default filename(s): `water_allo_day.txt`
- Source filename expression(s): `water_allo_day.txt`
- Open: line 12, file expression `"water_allo_day.txt"`, parser value `water_allo_day.txt`, condition `if (db_mx%wallo_db > 0) then > if (pco%water_allo%d == "y") then`
- Reads: _none captured_


### Candidate exact read evidence

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


## `weather-wgn.cli`

- Schema diff status: `['multi_record.changed']`
- Review needed: no
- Base schema presence: `{'resolved_sections': ['multi_record'], 'unresolved_sections': []}`
- Candidate schema presence: `{'resolved_sections': ['multi_record'], 'unresolved_sections': []}`

### Base exact read evidence

- Procedure: `cli_wgnread`
- Reader: `cli_wgnread.f90`
- Match: exact_filename
- Resolved default filename(s): `weather-wgn.cli`
- Source filename expression(s): `in_cli%weat_wgn`, `weather-wgn.cli`
- Open: line 47, file expression `in_cli%weat_wgn`, parser value `weather-wgn.cli`, condition `if (.not. i_exist .or. in_cli%weat_wgn == "null") then / else > do`

| Line | Role | Condition | Fields read |
| --- | --- | --- | --- |
| 48 | title | `if (.not. i_exist .or. in_cli%weat_wgn == "null") then / else > do` | `titldum` |
| 52 | title | `if (.not. i_exist .or. in_cli%weat_wgn == "null") then / else > do > do while (eof == 0)` | `titldum` |
| 54 | header | `if (.not. i_exist .or. in_cli%weat_wgn == "null") then / else > do > do while (eof == 0)` | `header` |
| 57 | title | `if (.not. i_exist .or. in_cli%weat_wgn == "null") then / else > do > do while (eof == 0) > do mo = 1, 12` | `titldum` |
| 88 | title | `if (.not. i_exist .or. in_cli%weat_wgn == "null") then / else > do` | `titldum` |
| 94 | data | `if (.not. i_exist .or. in_cli%weat_wgn == "null") then / else > do > do iwgn = 1, db_mx%wgnsta` | `wgn_n(iwgn)`, `wgn(iwgn)%lat`, `wgn(iwgn)%long`, `wgn(iwgn)%elev`, `wgn(iwgn)%rain_yrs` |
| 96 | header | `if (.not. i_exist .or. in_cli%weat_wgn == "null") then / else > do > do iwgn = 1, db_mx%wgnsta` | `header` |
| 99 | data | `if (.not. i_exist .or. in_cli%weat_wgn == "null") then / else > do > do iwgn = 1, db_mx%wgnsta > do mo = 1, 12` | `wgn(iwgn)%tmpmx(mo)`, `wgn(iwgn)%tmpmn(mo)`, `wgn(iwgn)%tmpstdmx(mo)`, `wgn(iwgn)%tmpstdmn(mo)`, `wgn(iwgn)%pcpmm(mo)`, `wgn(iwgn)%pcpstd(mo)`, `wgn(iwgn)%pcpskw(mo)`, `wgn(iwgn)%pr_wd(mo)`, `wgn(iwgn)%pr_ww(mo)`, `wgn(iwgn)%pcpd(mo)`, `wgn(iwgn)%rainhmx(mo)`, `wgn(iwgn)%solarav(mo)`, `wgn(iwgn)%dewpt(mo)`, `wgn(iwgn)%windav(mo)` |


### Candidate exact read evidence

- Procedure: `cli_wgnread`
- Reader: `cli_wgnread.f90`
- Match: exact_filename
- Resolved default filename(s): `weather-wgn.cli`
- Source filename expression(s): `in_cli%weat_wgn`, `weather-wgn.cli`
- Open: line 44, file expression `in_cli%weat_wgn`, parser value `weather-wgn.cli`, condition `if (.not. i_exist .or. in_cli%weat_wgn == "null") then / else > do`

| Line | Role | Condition | Fields read |
| --- | --- | --- | --- |
| 45 | title | `if (.not. i_exist .or. in_cli%weat_wgn == "null") then / else > do` | `titldum` |
| 49 | title | `if (.not. i_exist .or. in_cli%weat_wgn == "null") then / else > do > do while (eof == 0)` | `titldum` |
| 51 | header | `if (.not. i_exist .or. in_cli%weat_wgn == "null") then / else > do > do while (eof == 0)` | `header` |
| 54 | title | `if (.not. i_exist .or. in_cli%weat_wgn == "null") then / else > do > do while (eof == 0) > do mo = 1, 12` | `titldum` |
| 85 | title | `if (.not. i_exist .or. in_cli%weat_wgn == "null") then / else > do` | `titldum` |
| 91 | data | `if (.not. i_exist .or. in_cli%weat_wgn == "null") then / else > do > do iwgn = 1, db_mx%wgnsta` | `wgn_n(iwgn)`, `wgn(iwgn)%lat`, `wgn(iwgn)%long`, `wgn(iwgn)%elev`, `wgn(iwgn)%rain_yrs` |
| 93 | header | `if (.not. i_exist .or. in_cli%weat_wgn == "null") then / else > do > do iwgn = 1, db_mx%wgnsta` | `header` |
| 96 | data | `if (.not. i_exist .or. in_cli%weat_wgn == "null") then / else > do > do iwgn = 1, db_mx%wgnsta > do mo = 1, 12` | `wgn(iwgn)%tmpmx(mo)`, `wgn(iwgn)%tmpmn(mo)`, `wgn(iwgn)%tmpstdmx(mo)`, `wgn(iwgn)%tmpstdmn(mo)`, `wgn(iwgn)%pcpmm(mo)`, `wgn(iwgn)%pcpstd(mo)`, `wgn(iwgn)%pcpskw(mo)`, `wgn(iwgn)%pr_wd(mo)`, `wgn(iwgn)%pr_ww(mo)`, `wgn(iwgn)%pcpd(mo)`, `wgn(iwgn)%rainhmx(mo)`, `wgn(iwgn)%solarav(mo)`, `wgn(iwgn)%dewpt(mo)`, `wgn(iwgn)%windav(mo)` |


## `zones.gw`

- Schema diff status: `['files.added']`
- Review needed: no
- Base schema presence: `{'resolved_sections': [], 'unresolved_sections': ['unresolved']}`
- Candidate schema presence: `{'resolved_sections': ['files'], 'unresolved_sections': []}`

### Base exact read evidence

_No exact base opened/read evidence found._

### Candidate exact read evidence

- Procedure: `gwflow_read`
- Reader: `gwflow_read.f90`
- Match: exact_filename
- Resolved default filename(s): `zones.gw`
- Source filename expression(s): `zones.gw`, `unit_split_fields(2)`, `unit_split_fields(3)`, `unit_split_fields(4)`, `unit_split_fields(5)`, `unit_split_fields(6)`
- Open: line 321, file expression `'zones.gw'`, parser value `zones.gw`, condition `None`

| Line | Role | Condition | Fields read |
| --- | --- | --- | --- |
| 322 | header | `None` | `header` |
| 323 | header | `None` | `header` |
| 327 | data | `do` | `split_line_buf` |
| 341 | header | `None` | `header` |
| 342 | header | `None` | `header` |
| 344 | data | `do i=1,nzones_aquK` | `split_line_buf` |
| 346 | data | `do i=1,nzones_aquK` | `zones_aquK(i)` |
| 347 | data | `do i=1,nzones_aquK` | `zones_aquSy(i)` |
| 348 | data | `do i=1,nzones_aquK` | `zones_strK(i)` |
| 349 | data | `do i=1,nzones_aquK` | `zones_strbed(i)` |
| 351 | data | `do i=1,nzones_aquK > if(split_nf >= 6 .and. trim(split_fields(6)) /= 'null') then` | `zones_Kt(i)` |
