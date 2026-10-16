# SWAT+ Input Contract Changes

This is the primary source-level input change report. Filenames are resolved from the same defaults used by the schema extractor. A resolved default can still be overridden by runtime configuration.

## Summary

- Added input defaults: **46**
- Removed input defaults: **21**
- Changed read contracts: **15**
- Possible renames or replacements: **362**
- Candidate open/read blocks with unresolved filenames: **27**
- Newly unresolved filename expressions in the candidate: **2**

## Added inputs

### `_lyr.bsn`

- Schema status: `readable_needs_schema_review`
- Review needed: yes
- Source expression(s): `carbon_lyr`, `_lyr.bsn`

- Procedure: `carbon_bsn_read`
- Reader: `carbon_bsn_read.f90`
- Match: source_input
- Resolved default filename(s): `_lyr.bsn`
- Source filename expression(s): `carbon_lyr`, `_lyr.bsn`
- Open: line 114, file expression `carbon_lyr`, parser value `_lyr.bsn`, condition `None`

| Line | Role | Condition | Fields read |
| --- | --- | --- | --- |
| 121 | title | `None` | `titldum` |
| 122 | header | `None` | `header` |
| 127 | data | `do` | `layer_id`, `r_hp_rate`, `r_hs_rate`, `r_microb_rate`, `r_meta_rate`, `r_str_rate`, `r_microb_top_rate`, `r_hs_hp`, `r_a1co2`, `r_asco2`, `r_apco2`, `r_abco2` |

### `carbon.bsn`

- Schema status: `certified`
- Review needed: no
- Source expression(s): `in_basin%carbon_bsn`, `carbon.bsn`

- Procedure: `carbon_bsn_read`
- Reader: `carbon_bsn_read.f90`
- Match: source_input
- Resolved default filename(s): `carbon.bsn`
- Source filename expression(s): `in_basin%carbon_bsn`, `carbon.bsn`
- Open: line 57, file expression `in_basin%carbon_bsn`, parser value `carbon.bsn`, condition `None`

| Line | Role | Condition | Fields read |
| --- | --- | --- | --- |
| 66 | title | `None` | `titldum` |
| 67 | header | `None` | `header` |
| 69 | data | `None` | `org_frac%frac_seq`, `org_frac%frac_hum_microb`, `org_frac%frac_hum_slow`, `org_frac%frac_hum_passive`, `cb_wtr_coef%prmt_21`, `cb_wtr_coef%prmt_44`, `till_eff_days`, `man_coef%rtof`, `bio_consf`, `till_consf`, `org_con%tmpf`, `org_con%watf`, `org_con%tn`, `org_con%top`, `org_con%tx`, `bmix_a`, `bmix_b`, `bmix_c`, `tillmix_a`, `tillmix_b`, `tillmix_c`, `photo_degrade_factor`, `n_act_frac`, `cnr_cap`, `cnr_ref`, `cpr_cap`, `cpr_ref`, `mathers_int` |

### `carbon_layers.prt`

- Schema status: `readable_needs_schema_review`
- Review needed: yes
- Source expression(s): `carbon_layers.prt`

- Procedure: `carbon_layers_read`
- Reader: `carbon_layers_read.f90`
- Match: source_input
- Resolved default filename(s): `carbon_layers.prt`
- Source filename expression(s): `carbon_layers.prt`
- Open: line 29, file expression `'carbon_layers.prt'`, parser value `carbon_layers.prt`, condition `None`

| Line | Role | Condition | Fields read |
| --- | --- | --- | --- |
| 32 | title | `None` | `titldum` |
| 34 | header | `None` | `header` |
| 37 | data | `None` | `n_lyr` |

### `cell_sol.gw`

- Schema status: `certified`
- Review needed: no
- Source expression(s): `cell_sol.gw`

- Procedure: `gwflow_read`
- Reader: `gwflow_read.f90`
- Match: source_input
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

### `cellcon.gw`

- Schema status: `readable_needs_schema_review`
- Review needed: yes
- Source expression(s): `cellcon.gw`, `unit_split_fields(1)`, `unit_split_fields(2)`, `unit_split_fields(2+j)`

- Procedure: `gwflow_read`
- Reader: `gwflow_read.f90`
- Match: source_input
- Resolved default filename(s): `cellcon.gw`
- Source filename expression(s): `cellcon.gw`, `unit_split_fields(1)`, `unit_split_fields(2)`, `unit_split_fields(2+j)`
- Open: line 454, file expression `'cellcon.gw'`, parser value `cellcon.gw`, condition `None`

| Line | Role | Condition | Fields read |
| --- | --- | --- | --- |
| 455 | header | `None` | `header` |
| 456 | header | `None` | `header` |
| 458 | data | `do i=1,ncell` | `split_line_buf` |
| 464 | data | `do i=1,ncell` | `cell_id_in` |
| 469 | data | `do i=1,ncell` | `gw_state(i)%ncon` |
| 472 | data | `do i=1,ncell > do j=1,gw_state(i)%ncon` | `cell_con(i)%cell_id(j)` |

### `cells.gw`

- Schema status: `certified`
- Review needed: no
- Source expression(s): `cells.gw`, `unit_split_fields(1)`, `unit_split_fields(3)`, `unit_split_fields(4)`, `unit_split_fields(5)`, `unit_split_fields(6)`, `unit_split_fields(7)`, `unit_split_fields(8)`, `unit_split_fields(9)`, `unit_split_fields(10)`, `unit_split_fields(11)`, `unit_split_fields(12)`, `unit_split_fields(13)`, `unit_split_fields(14)`, `unit_split_fields(15)`, `unit_split_fields(16)`, `unit_split_fields(17)`, `unit_split_fields(18)`, `unit_split_fields(19)`, `unit_split_fields(20)`, `unit_split_fields(21)`, `unit_split_fields(22)`, `unit_split_fields(23)`

- Procedure: `gwflow_read`
- Reader: `gwflow_read.f90`
- Match: source_input
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

### `chan_depth.gw`

- Schema status: `readable_needs_schema_review`
- Review needed: yes
- Source expression(s): `chan_depth.gw`

- Procedure: `gwflow_chan_read`
- Reader: `gwflow_chan_read.f90`
- Match: source_input
- Resolved default filename(s): `chan_depth.gw`
- Source filename expression(s): `chan_depth.gw`
- Open: line 89, file expression `'chan_depth.gw'`, parser value `chan_depth.gw`, condition `if(i_exist) then`

| Line | Role | Condition | Fields read |
| --- | --- | --- | --- |
| 90 | header | `if(i_exist) then` | `header` |
| 91 | header | `if(i_exist) then` | `header` |

### `chancell.gw`

- Schema status: `certified`
- Review needed: no
- Source expression(s): `chancell.gw`, `unit_fields(1)`, `unit_fields(2)`, `unit_fields(3)`, `unit_fields(4)`, `unit_fields(5)`

- Procedure: `basin_read_objs`
- Reader: `basin_read_objs.f90`
- Match: source_input
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
- Match: source_input
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

### `codes.gw`

- Schema status: `readable_needs_schema_review`
- Review needed: yes
- Source expression(s): `codes.gw`

- Procedure: `gwflow_read`
- Reader: `gwflow_read.f90`
- Match: source_input
- Resolved default filename(s): `codes.gw`
- Source filename expression(s): `codes.gw`
- Open: line 224, file expression `'codes.gw'`, parser value `codes.gw`, condition `None`

| Line | Role | Condition | Fields read |
| --- | --- | --- | --- |
| 225 | header | `None` | `header` |
| 226 | data | `None` | `split_line_buf` |
| 228 | data | `None` | `split_line_buf` |

### `floodplain.gw`

- Schema status: `certified`
- Review needed: no
- Source expression(s): `floodplain.gw`

- Procedure: `gwflow_read`
- Reader: `gwflow_read.f90`
- Match: source_input
- Resolved default filename(s): `floodplain.gw`
- Source filename expression(s): `floodplain.gw`
- Open: line 1157, file expression `'floodplain.gw'`, parser value `floodplain.gw`, condition `if(gw_fp_flag == 1) then > if(i_exist) then`

| Line | Role | Condition | Fields read |
| --- | --- | --- | --- |
| 1158 | header | `if(gw_fp_flag == 1) then > if(i_exist) then` | `header` |
| 1159 | data | `if(gw_fp_flag == 1) then > if(i_exist) then` | `gw_fp_ncells` |
| 1167 | header | `if(gw_fp_flag == 1) then > if(i_exist) then` | `header` |
| 1169 | data | `if(gw_fp_flag == 1) then > if(i_exist) then > do i=1,gw_fp_ncells` | `gw_fp_cellid(i)`, `gw_fp_chanid(i)`, `gw_fp_K(i)`, `gw_fp_area(i)` |

### `gwflow.wbgroups`

- Schema status: `readable_needs_schema_review`
- Review needed: yes
- Source expression(s): `gwflow.wbgroups`

- Procedure: `gwflow_output_init`
- Reader: `gwflow_output.f90`
- Match: source_input
- Resolved default filename(s): `gwflow.wbgroups`
- Source filename expression(s): `gwflow.wbgroups`
- Open: line 138, file expression `'gwflow.wbgroups'`, parser value `gwflow.wbgroups`, condition `if(i_exist) then`

| Line | Role | Condition | Fields read |
| --- | --- | --- | --- |
| 139 | header | `if(i_exist) then` | `header` |
| 140 | data | `if(i_exist) then` | `gw_wb_grp_num` |
| 141 | data | `if(i_exist) then` | `max_num` |
| 148 | header | `if(i_exist) then > do i=1,gw_wb_grp_num` | `header` |
| 149 | data | `if(i_exist) then > do i=1,gw_wb_grp_num` | `gw_wb_grp_ncell(i)` |
| 152 | data | `if(i_exist) then > do i=1,gw_wb_grp_num > do j=1,gw_wb_grp_ncell(i)` | `wb_cell` |

### `gwflow_canal.con`

- Schema status: `certified`
- Review needed: no
- Source expression(s): `gwflow_canal.con`

- Procedure: `gwflow_read`
- Reader: `gwflow_read.f90`
- Match: source_input
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

### `hru_pump.gw`

- Schema status: `readable_needs_schema_review`
- Review needed: yes
- Source expression(s): `hru_pump.gw`

- Procedure: `gwflow_read`
- Reader: `gwflow_read.f90`
- Match: source_input
- Resolved default filename(s): `hru_pump.gw`
- Source filename expression(s): `hru_pump.gw`
- Open: line 912, file expression `'hru_pump.gw'`, parser value `hru_pump.gw`, condition `if(i_exist) then`

| Line | Role | Condition | Fields read |
| --- | --- | --- | --- |
| 913 | data | `if(i_exist) then` | _no fields captured_ |
| 914 | data | `if(i_exist) then` | `num_hru_pump_obs` |
| 917 | data | `if(i_exist) then > do i=1,num_hru_pump_obs` | `hru_pump_ids(i)` |

### `hrucell.gw`

- Schema status: `certified`
- Review needed: no
- Source expression(s): `hrucell.gw`

- Procedure: `gwflow_read`
- Reader: `gwflow_read.f90`
- Match: source_input
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

### `lsucell.gw`

- Schema status: `certified`
- Review needed: no
- Source expression(s): `lsucell.gw`

- Procedure: `gwflow_read`
- Reader: `gwflow_read.f90`
- Match: source_input
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

### `manure_db.frt`

- Schema status: `certified`
- Review needed: no
- Source expression(s): `manure_db.frt`

- Procedure: `manure_db_read`
- Reader: `manure_db_read.f90`
- Match: source_input
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

### `manure_om.frt`

- Schema status: `certified`
- Review needed: no
- Source expression(s): `manure_om.frt`

- Procedure: `manure_orgmin_read`
- Reader: `manure_orgmin_read.f90`
- Match: source_input
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

### `minerals.gw`

- Schema status: `certified`
- Review needed: no
- Source expression(s): `minerals.gw`

- Procedure: `gwflow_read`
- Reader: `gwflow_read.f90`
- Match: source_input
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

### `om_osrc.wal`

- Schema status: `certified`
- Review needed: no
- Source expression(s): `om_osrc.wal`

- Procedure: `om_osrc_read`
- Reader: `om_osrc_read.f90`
- Match: source_input
- Resolved default filename(s): `om_osrc.wal`
- Source filename expression(s): `om_osrc.wal`
- Open: line 31, file expression `'om_osrc.wal'`, parser value `om_osrc.wal`, condition `if (.not. i_exist .or. 'om_osrc.wal' == "null") then / else > do`

| Line | Role | Condition | Fields read |
| --- | --- | --- | --- |
| 32 | title | `if (.not. i_exist .or. 'om_osrc.wal' == "null") then / else > do` | `titldum` |
| 34 | count | `if (.not. i_exist .or. 'om_osrc.wal' == "null") then / else > do` | `imax` |
| 35 | header | `if (.not. i_exist .or. 'om_osrc.wal' == "null") then / else > do` | `header` |
| 43 | data | `if (.not. i_exist .or. 'om_osrc.wal' == "null") then / else > do > do iom_osrc = 1, imax` | `om_osrc_name(iom_osrc)`, `osrc_om(iom_osrc)` |

### `om_treat.wal`

- Schema status: `certified`
- Review needed: no
- Source expression(s): `om_treat.wal`

- Procedure: `om_treat_read`
- Reader: `om_treat_read.f90`
- Match: source_input
- Resolved default filename(s): `om_treat.wal`
- Source filename expression(s): `om_treat.wal`
- Open: line 30, file expression `'om_treat.wal'`, parser value `om_treat.wal`, condition `if (.not. i_exist .or. 'om_treat.wal' == "null") then / else > do`

| Line | Role | Condition | Fields read |
| --- | --- | --- | --- |
| 31 | title | `if (.not. i_exist .or. 'om_treat.wal' == "null") then / else > do` | `titldum` |
| 33 | count | `if (.not. i_exist .or. 'om_treat.wal' == "null") then / else > do` | `imax` |
| 34 | header | `if (.not. i_exist .or. 'om_treat.wal' == "null") then / else > do` | `header` |
| 42 | data | `if (.not. i_exist .or. 'om_treat.wal' == "null") then / else > do > do iom_tr = 1, imax` | `om_treat_name(iom_tr)`, `wtp_om_treat(iom_tr)` |

### `om_use.wal`

- Schema status: `certified`
- Review needed: no
- Source expression(s): `om_use.wal`

- Procedure: `om_use_read`
- Reader: `om_use_read.f90`
- Match: source_input
- Resolved default filename(s): `om_use.wal`
- Source filename expression(s): `om_use.wal`
- Open: line 30, file expression `'om_use.wal'`, parser value `om_use.wal`, condition `if (.not. i_exist .or. 'om_use.wal' == "null") then / else > do`

| Line | Role | Condition | Fields read |
| --- | --- | --- | --- |
| 31 | title | `if (.not. i_exist .or. 'om_use.wal' == "null") then / else > do` | `titldum` |
| 33 | count | `if (.not. i_exist .or. 'om_use.wal' == "null") then / else > do` | `imax` |
| 34 | header | `if (.not. i_exist .or. 'om_use.wal' == "null") then / else > do` | `header` |
| 43 | data | `if (.not. i_exist .or. 'om_use.wal' == "null") then / else > do > do iom_use = 1, imax` | `om_use_name(iom_use)`, `wuse_om_efflu(iom_use)` |

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

### `outputs.gw`

- Schema status: `certified`
- Review needed: no
- Source expression(s): `outputs.gw`, `unit_split_fields(2)`

- Procedure: `gwflow_read`
- Reader: `gwflow_read.f90`
- Match: source_input
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

### `outside_rcv.wal`

- Schema status: `certified`
- Review needed: no
- Source expression(s): `outside_rcv.wal`

- Procedure: `water_orcv_read`
- Reader: `water_orcv_read.f90`
- Match: source_input
- Resolved default filename(s): `outside_rcv.wal`
- Source filename expression(s): `outside_rcv.wal`
- Open: line 34, file expression `'outside_rcv.wal'`, parser value `outside_rcv.wal`, condition `if (.not. i_exist .or. 'outside_rcv.wal' == "null") then / else > do`

| Line | Role | Condition | Fields read |
| --- | --- | --- | --- |
| 35 | title | `if (.not. i_exist .or. 'outside_rcv.wal' == "null") then / else > do` | `titldum` |
| 37 | count | `if (.not. i_exist .or. 'outside_rcv.wal' == "null") then / else > do` | `imax` |
| 38 | header | `if (.not. i_exist .or. 'outside_rcv.wal' == "null") then / else > do` | `header` |
| 45 | data | `if (.not. i_exist .or. 'outside_rcv.wal' == "null") then / else > do > do ircv = 1, imax` | `i`, `orcv(ircv)%name`, `orcv(ircv)%filename` |

### `phreato.gw`

- Schema status: `certified`
- Review needed: no
- Source expression(s): `phreato.gw`

- Procedure: `gwflow_read`
- Reader: `gwflow_read.f90`
- Match: source_input
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

### `phreato_cell.gw`

- Schema status: `certified`
- Review needed: no
- Source expression(s): `phreato_cell.gw`

- Procedure: `gwflow_read`
- Reader: `gwflow_read.f90`
- Match: source_input
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

### `pond_cell.gw`

- Schema status: `certified`
- Review needed: no
- Source expression(s): `pond_cell.gw`

- Procedure: `gwflow_read`
- Reader: `gwflow_read.f90`
- Match: source_input
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

### `pond_div.gw`

- Schema status: `readable_needs_schema_review`
- Review needed: yes
- Source expression(s): `pond_div.gw`

- Procedure: `gwflow_read`
- Reader: `gwflow_read.f90`
- Match: source_input
- Resolved default filename(s): `pond_div.gw`
- Source filename expression(s): `pond_div.gw`
- Open: line 1994, file expression `'pond_div.gw'`, parser value `pond_div.gw`, condition `if(i_exist) then > if(i_exist) then`

| Line | Role | Condition | Fields read |
| --- | --- | --- | --- |
| 1995 | header | `if(i_exist) then > if(i_exist) then` | `header` |
| 1996 | header | `if(i_exist) then > if(i_exist) then` | `header` |

### `ponds.gw`

- Schema status: `certified`
- Review needed: no
- Source expression(s): `ponds.gw`

- Procedure: `gwflow_read`
- Reader: `gwflow_read.f90`
- Match: source_input
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

### `pumpex.gw`

- Schema status: `certified`
- Review needed: no
- Source expression(s): `pumpex.gw`

- Procedure: `gwflow_read`
- Reader: `gwflow_read.f90`
- Match: source_input
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

### `recall_db.rec`

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

### `rescell.gw`

- Schema status: `certified`
- Review needed: no
- Source expression(s): `rescell.gw`

- Procedure: `gwflow_read`
- Reader: `gwflow_read.f90`
- Match: source_input
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

### `satbuffer.str`

- Schema status: `certified`
- Review needed: no
- Source expression(s): `satbuffer.str`

- Procedure: `sat_buff_read`
- Reader: `sat_buff_read.f90`
- Match: source_input
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

### `shade_factor.shf`

- Schema status: `certified`
- Review needed: no
- Source expression(s): `in_shf%ssff_shf`, `shade_factor.shf`

- Procedure: `shade_factor_read`
- Reader: `shade_factor_read.f90`
- Match: source_input
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

### `soil_lyr_depths.sol`

- Schema status: `readable_needs_schema_review`
- Review needed: yes
- Source expression(s): `soil_lyr_depths.sol`

- Procedure: `soils_init`
- Reader: `soils_init.f90`
- Match: source_input
- Resolved default filename(s): `soil_lyr_depths.sol`
- Source filename expression(s): `soil_lyr_depths.sol`
- Open: line 166, file expression `"soil_lyr_depths.sol"`, parser value `soil_lyr_depths.sol`, condition `do isol = 1, msoils > if (.not. i_exist) then / else`

| Line | Role | Condition | Fields read |
| --- | --- | --- | --- |
| 167 | title | `do isol = 1, msoils > if (.not. i_exist) then / else` | `titldum` |
| 169 | header | `do isol = 1, msoils > if (.not. i_exist) then / else` | `header` |
| 171 | data | `do isol = 1, msoils > if (.not. i_exist) then / else` | `units` |
| 175 | data | `do isol = 1, msoils > if (.not. i_exist) then / else > do` | `csld` |
| 204 | title | `do isol = 1, msoils > if (.not. i_exist) then / else` | `titldum` |
| 205 | header | `do isol = 1, msoils > if (.not. i_exist) then / else` | `header` |
| 206 | data | `do isol = 1, msoils > if (.not. i_exist) then / else` | `units` |
| 212 | data | `do isol = 1, msoils > if (.not. i_exist) then / else > do i = 1, mlyr > do` | `csld` |

### `solute.gw`

- Schema status: `certified`
- Review needed: no
- Source expression(s): `solute.gw`

- Procedure: `gwflow_read`
- Reader: `gwflow_read.f90`
- Match: source_input
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

### `sw_group.gw`

- Schema status: `readable_needs_schema_review`
- Review needed: yes
- Source expression(s): `sw_group.gw`, `unit_split_fields(2)`, `unit_split_fields(2+j)`

- Procedure: `gwflow_read`
- Reader: `gwflow_read.f90`
- Match: source_input
- Resolved default filename(s): `sw_group.gw`
- Source filename expression(s): `sw_group.gw`, `unit_split_fields(2)`, `unit_split_fields(2+j)`
- Open: line 2281, file expression `'sw_group.gw'`, parser value `sw_group.gw`, condition `if(i_exist) then`

| Line | Role | Condition | Fields read |
| --- | --- | --- | --- |
| 2282 | header | `if(i_exist) then` | `header` |
| 2283 | header | `if(i_exist) then` | `header` |
| 2288 | data | `if(i_exist) then > do` | `split_line_buf` |
| 2293 | data | `if(i_exist) then > do` | `k` |
| 2300 | header | `if(i_exist) then` | `header` |
| 2301 | header | `if(i_exist) then` | `header` |
| 2303 | data | `if(i_exist) then > do i=1,gw_gwsw_ngroup` | `split_line_buf` |
| 2305 | data | `if(i_exist) then > do i=1,gw_gwsw_ngroup` | `gw_gwsw_ncell(i)` |
| 2307 | data | `if(i_exist) then > do i=1,gw_gwsw_ngroup > do j=1,gw_gwsw_ncell(i)` | `gw_gwsw_group(i,j)` |

### `tile.gw`

- Schema status: `certified`
- Review needed: no
- Source expression(s): `tile.gw`

- Procedure: `gwflow_read`
- Reader: `gwflow_read.f90`
- Match: source_input
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

### `transit.gw`

- Schema status: `readable_needs_schema_review`
- Review needed: yes
- Source expression(s): `transit.gw`

- Procedure: `gwflow_read`
- Reader: `gwflow_read.f90`
- Match: source_input
- Resolved default filename(s): `transit.gw`
- Source filename expression(s): `transit.gw`
- Open: line 2236, file expression `'transit.gw'`, parser value `transit.gw`, condition `if(grid_type == "structured") then > if(i_exist) then`

| Line | Role | Condition | Fields read |
| --- | --- | --- | --- |
| 2237 | header | `if(grid_type == "structured") then > if(i_exist) then` | `header` |
| 2238 | header | `if(grid_type == "structured") then > if(i_exist) then` | `header` |
| 2239 | data | `if(grid_type == "structured") then > if(i_exist) then` | `gw_transit_num` |
| 2242 | data | `if(grid_type == "structured") then > if(i_exist) then > do i=1,gw_transit_num` | `cell_transit` |

### `tvheads.gw`

- Schema status: `certified`
- Review needed: no
- Source expression(s): `tvheads.gw`

- Procedure: `gwflow_read`
- Reader: `gwflow_read.f90`
- Match: source_input
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

### `water_canal.wal`

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

### `water_pipe.wal`

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

### `water_tower.wal`

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

### `water_treat.wal`

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

### `water_use.wal`

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

### `zones.gw`

- Schema status: `certified`
- Review needed: no
- Source expression(s): `zones.gw`, `unit_split_fields(2)`, `unit_split_fields(3)`, `unit_split_fields(4)`, `unit_split_fields(5)`, `unit_split_fields(6)`

- Procedure: `gwflow_read`
- Reader: `gwflow_read.f90`
- Match: source_input
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


## Removed inputs

### `basins_carbon.tes`

- Schema status: `readable_needs_schema_review`
- Review needed: yes
- Source expression(s): `basins_carbon.tes`

- Procedure: `carbon_read`
- Reader: `carbon_read.f90`
- Match: source_input
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

### `cs.res`

- Schema status: `readable_needs_schema_review`
- Review needed: yes
- Source expression(s): `cs.res`

- Procedure: `res_read_cs`
- Reader: `res_read_cs.f90`
- Match: source_input
- Resolved default filename(s): `cs.res`
- Source filename expression(s): `cs.res`
- Open: line 29, file expression `"cs.res"`, parser value `cs.res`, condition `if (.not. i_exist .or. in_res%nut_res == "null") then / else > do`

| Line | Role | Condition | Fields read |
| --- | --- | --- | --- |
| 30 | title | `if (.not. i_exist .or. in_res%nut_res == "null") then / else > do` | `titldum` |
| 31 | title | `if (.not. i_exist .or. in_res%nut_res == "null") then / else > do` | `titldum` |
| 33 | data | `if (.not. i_exist .or. in_res%nut_res == "null") then / else > do > do i=1,12` | _no fields captured_ |
| 37 | header | `if (.not. i_exist .or. in_res%nut_res == "null") then / else > do` | `header` |
| 40 | title | `if (.not. i_exist .or. in_res%nut_res == "null") then / else > do > do while (eof == 0)` | `titldum` |
| 49 | title | `if (.not. i_exist .or. in_res%nut_res == "null") then / else > do` | `titldum` |
| 51 | title | `if (.not. i_exist .or. in_res%nut_res == "null") then / else > do` | `titldum` |
| 53 | data | `if (.not. i_exist .or. in_res%nut_res == "null") then / else > do > do i=1,12` | _no fields captured_ |
| 55 | header | `if (.not. i_exist .or. in_res%nut_res == "null") then / else > do` | `header` |
| 59 | title | `if (.not. i_exist .or. in_res%nut_res == "null") then / else > do > do ires = 1, imax` | `titldum` |
| 62 | data | `if (.not. i_exist .or. in_res%nut_res == "null") then / else > do > do ires = 1, imax` | `res_cs_data(ires)` |

### `gwflow.canals`

- Schema status: `readable_needs_schema_review`
- Review needed: yes
- Source expression(s): `gwflow.canals`

- Procedure: `gwflow_read`
- Reader: `gwflow_read.f90`
- Match: source_input
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

### `gwflow.cellhru`

- Schema status: `readable_needs_schema_review`
- Review needed: yes
- Source expression(s): `gwflow.cellhru`

- Procedure: `gwflow_read`
- Reader: `gwflow_read.f90`
- Match: source_input
- Resolved default filename(s): `gwflow.cellhru`
- Source filename expression(s): `gwflow.cellhru`
- Open: line 1868, file expression `'gwflow.cellhru'`, parser value `gwflow.cellhru`, condition `if (lsu_cells_link == 1) then / else > if (nat_model == 1) then > if (nat_model == 1) then > do k=1,sp_ob%outlet / else`

| Line | Role | Condition | Fields read |
| --- | --- | --- | --- |
| 1869 | data | `if (lsu_cells_link == 1) then / else > if (nat_model == 1) then > if (nat_model == 1) then > do k=1,sp_ob%outlet / else` | _no fields captured_ |
| 1870 | data | `if (lsu_cells_link == 1) then / else > if (nat_model == 1) then > if (nat_model == 1) then > do k=1,sp_ob%outlet / else` | _no fields captured_ |
| 1871 | data | `if (lsu_cells_link == 1) then / else > if (nat_model == 1) then > if (nat_model == 1) then > do k=1,sp_ob%outlet / else` | `num_unique` |
| 1872 | data | `if (lsu_cells_link == 1) then / else > if (nat_model == 1) then > if (nat_model == 1) then > do k=1,sp_ob%outlet / else` | _no fields captured_ |
| 1874 | data | `if (lsu_cells_link == 1) then / else > if (nat_model == 1) then > if (nat_model == 1) then > do k=1,sp_ob%outlet / else > do k=1,num_unique` | `hru_cell` |
| 1883 | data | `if (lsu_cells_link == 1) then / else > if (nat_model == 1) then > if (nat_model == 1) then > do k=1,sp_ob%outlet / else > do k=1,num_unique > do while (cell_num.eq.hru_cell)` | `cell_num`, `hru_id`, `cell_area`, `poly_area` |
| 1889 | data | `if (lsu_cells_link == 1) then / else > if (nat_model == 1) then > if (nat_model == 1) then > do k=1,sp_ob%outlet / else > do k=1,num_unique > do while (cell_num.eq.hru_cell)` | `cell_num` |

### `gwflow.chancells`

- Schema status: `readable_needs_schema_review`
- Review needed: yes
- Source expression(s): `gwflow.chancells`

- Procedure: `basin_read_objs`
- Reader: `basin_read_objs.f90`
- Match: source_input
- Resolved default filename(s): `gwflow.chancells`
- Source filename expression(s): `gwflow.chancells`
- Open: line 52, file expression `'gwflow.chancells'`, parser value `gwflow.chancells`, condition `if(bsn_cc%gwflow == 1 ) then > if(i_exist) then > if(sp_ob%gwflow == 0) then`

| Line | Role | Condition | Fields read |
| --- | --- | --- | --- |
| 53 | header | `if(bsn_cc%gwflow == 1 ) then > if(i_exist) then > if(sp_ob%gwflow == 0) then` | `header` |
| 55 | data | `if(bsn_cc%gwflow == 1 ) then > if(i_exist) then > if(sp_ob%gwflow == 0) then > if(eof == 0) then` | _no fields captured_ |
| 56 | header | `if(bsn_cc%gwflow == 1 ) then > if(i_exist) then > if(sp_ob%gwflow == 0) then > if(eof == 0) then` | `header` |
| 62 | data | `if(bsn_cc%gwflow == 1 ) then > if(i_exist) then > if(sp_ob%gwflow == 0) then > if(eof == 0) then > do while (eof == 0)` | `riv_id` |


- Procedure: `gwflow_chan_read`
- Reader: `gwflow_chan_read.f90`
- Match: source_input
- Resolved default filename(s): `gwflow.chancells`
- Source filename expression(s): `gwflow.chancells`
- Open: line 35, file expression `'gwflow.chancells'`, parser value `gwflow.chancells`, condition `None`

| Line | Role | Condition | Fields read |
| --- | --- | --- | --- |
| 50 | data | `None` | _no fields captured_ |
| 51 | data | `None` | _no fields captured_ |
| 52 | data | `None` | _no fields captured_ |
| 54 | data | `do k=1,num_chancells` | `cell_ID`, `bed_elev`, `channel`, `chan_length`, `chan_zone` |

### `gwflow.floodplain`

- Schema status: `readable_needs_schema_review`
- Review needed: yes
- Source expression(s): `gwflow.floodplain`

- Procedure: `gwflow_read`
- Reader: `gwflow_read.f90`
- Match: source_input
- Resolved default filename(s): `gwflow.floodplain`
- Source filename expression(s): `gwflow.floodplain`
- Open: line 1134, file expression `'gwflow.floodplain'`, parser value `gwflow.floodplain`, condition `if (gw_fp_flag == 1) then > if(i_exist) then`

| Line | Role | Condition | Fields read |
| --- | --- | --- | --- |
| 1135 | header | `if (gw_fp_flag == 1) then > if(i_exist) then` | `header` |
| 1136 | data | `if (gw_fp_flag == 1) then > if(i_exist) then` | `gw_fp_ncells` |
| 1144 | header | `if (gw_fp_flag == 1) then > if(i_exist) then` | `header` |
| 1146 | data | `if (gw_fp_flag == 1) then > if(i_exist) then > do i=1,gw_fp_ncells` | `gw_fp_cellid(i)`, `gw_fp_chanid(i)`, `gw_fp_K(i)`, `gw_fp_area(i)` |

### `gwflow.hru_pump_observe`

- Schema status: `readable_needs_schema_review`
- Review needed: yes
- Source expression(s): `gwflow.hru_pump_observe`

- Procedure: `gwflow_read`
- Reader: `gwflow_read.f90`
- Match: source_input
- Resolved default filename(s): `gwflow.hru_pump_observe`
- Source filename expression(s): `gwflow.hru_pump_observe`
- Open: line 931, file expression `'gwflow.hru_pump_observe'`, parser value `gwflow.hru_pump_observe`, condition `if (hru_pump_flag == 1) then`

| Line | Role | Condition | Fields read |
| --- | --- | --- | --- |
| 932 | data | `if (hru_pump_flag == 1) then` | _no fields captured_ |
| 933 | data | `if (hru_pump_flag == 1) then` | `num_hru_pump_obs` |
| 936 | data | `if (hru_pump_flag == 1) then > do i=1,num_hru_pump_obs` | `hru_pump_ids(i)` |

### `gwflow.hrucell`

- Schema status: `readable_needs_schema_review`
- Review needed: yes
- Source expression(s): `gwflow.hrucell`

- Procedure: `gwflow_read`
- Reader: `gwflow_read.f90`
- Match: source_input
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

### `gwflow.huc12cell`

- Schema status: `readable_needs_schema_review`
- Review needed: yes
- Source expression(s): `gwflow.huc12cell`

- Procedure: `gwflow_read`
- Reader: `gwflow_read.f90`
- Match: source_input
- Resolved default filename(s): `gwflow.huc12cell`
- Source filename expression(s): `gwflow.huc12cell`
- Open: line 1807, file expression `'gwflow.huc12cell'`, parser value `gwflow.huc12cell`, condition `if (lsu_cells_link == 1) then / else > if (nat_model == 1) then > if (nat_model == 1) then`

| Line | Role | Condition | Fields read |
| --- | --- | --- | --- |
| 1808 | data | `if (lsu_cells_link == 1) then / else > if (nat_model == 1) then > if (nat_model == 1) then` | _no fields captured_ |
| 1809 | data | `if (lsu_cells_link == 1) then / else > if (nat_model == 1) then > if (nat_model == 1) then` | _no fields captured_ |
| 1811 | data | `if (lsu_cells_link == 1) then / else > if (nat_model == 1) then > if (nat_model == 1) then` | _no fields captured_ |
| 1813 | data | `if (lsu_cells_link == 1) then / else > if (nat_model == 1) then > if (nat_model == 1) then > do k=1,sp_ob%outlet` | `huc12_dum`, `huc12_connect(k)` |
| 1822 | data | `if (lsu_cells_link == 1) then / else > if (nat_model == 1) then > if (nat_model == 1) then` | _no fields captured_ |
| 1823 | data | `if (lsu_cells_link == 1) then / else > if (nat_model == 1) then > if (nat_model == 1) then` | _no fields captured_ |
| 1826 | data | `if (lsu_cells_link == 1) then / else > if (nat_model == 1) then > if (nat_model == 1) then > do k=1,sp_ob%outlet > if(huc12_connect(k).eq.1) then` | `huc12_id` |
| 1830 | data | `if (lsu_cells_link == 1) then / else > if (nat_model == 1) then > if (nat_model == 1) then > do k=1,sp_ob%outlet > if(huc12_connect(k).eq.1) then > do while (huc12_id.eq.huc12(k))` | `huc12_id`, `cell_num` |
| 1853 | data | `if (lsu_cells_link == 1) then / else > if (nat_model == 1) then > if (nat_model == 1) then > do k=1,sp_ob%outlet > if(huc12_connect(k).eq.1) then > do while (huc12_id.eq.huc12(k))` | `huc12_id` |

### `gwflow.input`

- Schema status: `readable_needs_schema_review`
- Review needed: yes
- Source expression(s): `gwflow.input`

- Procedure: `gwflow_read`
- Reader: `gwflow_read.f90`
- Match: source_input
- Resolved default filename(s): `gwflow.input`
- Source filename expression(s): `gwflow.input`
- Open: line 171, file expression `'gwflow.input'`, parser value `gwflow.input`, condition `None`

| Line | Role | Condition | Fields read |
| --- | --- | --- | --- |
| 172 | header | `None` | `header` |
| 173 | header | `None` | `header` |
| 177 | data | `None` | `grid_type` |
| 179 | data | `if (grid_type == "structured") then` | `cell_size` |
| 180 | data | `if (grid_type == "structured") then` | `grid_nrow`, `grid_ncol` |
| 182 | data | `if (grid_type == "structured") then / else if (grid_type == "unstructured") then` | `ncell` |
| 184 | data | `None` | `bc_type` |
| 185 | data | `None` | `conn_type` |
| 186 | data | `None` | `gw_soil_flag` |
| 187 | data | `None` | `gw_satx_flag` |
| 188 | data | `None` | `gw_pumpex_flag` |
| 189 | data | `None` | `gw_tile_flag` |
| 190 | data | `None` | `gw_res_flag` |
| 191 | data | `None` | `gw_wet_flag` |
| 192 | data | `None` | `gw_fp_flag` |
| 193 | data | `None` | `gw_canal_flag` |
| 194 | data | `None` | `gw_solute_flag` |
| 195 | data | `None` | `gw_time_step` |
| 196 | data | `None` | `gwflag_day`, `gwflag_yr`, `gwflag_aa` |
| 197 | data | `None` | `out_cols` |
| 249 | header | `None` | `header` |
| 250 | header | `None` | `header` |
| 251 | data | `None` | `nzones_aquK` |
| 254 | data | `do i=1,nzones_aquK` | `dum`, `zones_aquK(i)` |
| 259 | header | `None` | `header` |
| 260 | data | `None` | `nzones_aquSy` |
| 263 | data | `do i=1,nzones_aquSy` | `dum`, `zones_aquSy(i)` |
| 268 | header | `None` | `header` |
| 269 | data | `None` | `nzones_strK` |
| 272 | data | `do i=1,nzones_strK` | `dum`, `zones_strK(i)` |
| 277 | header | `None` | `header` |
| 278 | data | `None` | `nzones_strbed` |
| 281 | data | `do i=1,nzones_strbed` | `dum`, `zones_strbed(i)` |
| 292 | header | `if (grid_type == "structured") then` | `header` |
| 295 | header | `if (grid_type == "structured") then` | `header` |
| 297 | data | `if (grid_type == "structured") then` | `((grid_status(i,j),j=1,grid_ncol),i=1,grid_nrow)` |
| 442 | header | `if (grid_type == "structured") then` | `header` |
| 443 | data | `if (grid_type == "structured") then` | `((grid_val(i,j),j=1,grid_ncol),i=1,grid_nrow)` |
| 452 | header | `if (grid_type == "structured") then` | `header` |
| 453 | data | `if (grid_type == "structured") then` | `((grid_val(i,j),j=1,grid_ncol),i=1,grid_nrow)` |
| 462 | header | `if (grid_type == "structured") then` | `header` |
| 463 | data | `if (grid_type == "structured") then` | `((grid_int(i,j),j=1,grid_ncol),i=1,grid_nrow)` |
| 475 | header | `if (grid_type == "structured") then` | `header` |
| 476 | data | `if (grid_type == "structured") then` | `((grid_int(i,j),j=1,grid_ncol),i=1,grid_nrow)` |
| 489 | header | `if (grid_type == "structured") then` | `header` |
| 490 | data | `if (grid_type == "structured") then` | `((grid_val(i,j),j=1,grid_ncol),i=1,grid_nrow)` |
| 499 | header | `if (grid_type == "structured") then` | `header` |
| 500 | data | `if (grid_type == "structured") then` | `((grid_val(i,j),j=1,grid_ncol),i=1,grid_nrow)` |
| 509 | header | `if (grid_type == "structured") then` | `header` |
| 510 | data | `if (grid_type == "structured") then` | `((grid_val(i,j),j=1,grid_ncol),i=1,grid_nrow)` |
| 557 | header | `if (grid_type == "structured") then / elseif(grid_type == "unstructured") then > do i=1,13` | `header` |
| 561 | data | `if (grid_type == "structured") then / elseif(grid_type == "unstructured") then > do i=1,ncell` | `dum1`, `gw_state(i)%stat`, `gw_state(i)%elev`, `gw_state(i)%thck`, `K_zone`, `Sy_zone`, `delay(i)`, `gw_state(i)%exdp`, `gw_state(i)%init`, `gw_state(i)%xcrd`, `gw_state(i)%ycrd`, `gw_state(i)%area`, `gw_state(i)%ncon` |
| 567 | data | `if (grid_type == "structured") then / elseif(grid_type == "unstructured") then > do i=1,ncell` | `dum1`, `gw_state(i)%stat`, `gw_state(i)%elev`, `gw_state(i)%thck`, `K_zone`, `Sy_zone`, `delay(i)`, `gw_state(i)%exdp`, `gw_state(i)%init`, `gw_state(i)%xcrd`, `gw_state(i)%ycrd`, `gw_state(i)%area`, `gw_state(i)%ncon`, `(cell_con(i)%cell_id(j),j=1,gw_state(i)%ncon)` |
| 626 | data | `None` | _no fields captured_ |
| 627 | data | `None` | `gw_num_output` |
| 631 | data | `do i=1,gw_num_output` | `gw_output_yr(i)`, `gw_output_day(i)` |
| 637 | data | `None` | _no fields captured_ |
| 638 | data | `None` | `gw_num_obs_wells` |
| 648 | data | `do k=1,gw_num_obs_wells > if(usgs_obs == 1) then` | `gw_obs_cells(k)`, `usgs_id(k)` |
| 650 | data | `do k=1,gw_num_obs_wells > if(usgs_obs == 1) then / else` | `gw_obs_cells(k)` |
| 670 | header | `None` | `header` |
| 671 | data | `None` | `gw_cell_obs_ss` |
| 733 | data | `None` | _no fields captured_ |
| 734 | data | `None` | `gw_bed_change` |

### `gwflow.lsucell`

- Schema status: `readable_needs_schema_review`
- Review needed: yes
- Source expression(s): `gwflow.lsucell`

- Procedure: `gwflow_read`
- Reader: `gwflow_read.f90`
- Match: source_input
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

### `gwflow.pumpex`

- Schema status: `readable_needs_schema_review`
- Review needed: yes
- Source expression(s): `gwflow.pumpex`

- Procedure: `gwflow_read`
- Reader: `gwflow_read.f90`
- Match: source_input
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

### `gwflow.rescells`

- Schema status: `readable_needs_schema_review`
- Review needed: yes
- Source expression(s): `gwflow.rescells`

- Procedure: `gwflow_read`
- Reader: `gwflow_read.f90`
- Match: source_input
- Resolved default filename(s): `gwflow.rescells`
- Source filename expression(s): `gwflow.rescells`
- Open: line 1063, file expression `'gwflow.rescells'`, parser value `gwflow.rescells`, condition `if (gw_res_flag == 1) then > if(i_exist) then`

| Line | Role | Condition | Fields read |
| --- | --- | --- | --- |
| 1064 | header | `if (gw_res_flag == 1) then > if(i_exist) then` | `header` |
| 1065 | header | `if (gw_res_flag == 1) then > if(i_exist) then` | `header` |
| 1067 | data | `if (gw_res_flag == 1) then > if(i_exist) then` | `res_thick` |
| 1068 | data | `if (gw_res_flag == 1) then > if(i_exist) then` | `res_K` |
| 1072 | data | `if (gw_res_flag == 1) then > if(i_exist) then` | `num_res_cells` |
| 1073 | header | `if (gw_res_flag == 1) then > if(i_exist) then` | `header` |
| 1075 | data | `if (gw_res_flag == 1) then > if(i_exist) then > do i=1,num_res_cells` | `res_cell`, `res_id`, `res_stage` |
| 1089 | header | `if (gw_res_flag == 1) then > if(i_exist) then` | `header` |
| 1090 | header | `if (gw_res_flag == 1) then > if(i_exist) then` | `header` |
| 1091 | data | `if (gw_res_flag == 1) then > if(i_exist) then` | `res_thick` |
| 1092 | data | `if (gw_res_flag == 1) then > if(i_exist) then` | `res_K` |
| 1093 | data | `if (gw_res_flag == 1) then > if(i_exist) then` | `num_res_cells` |
| 1094 | header | `if (gw_res_flag == 1) then > if(i_exist) then` | `header` |
| 1096 | data | `if (gw_res_flag == 1) then > if(i_exist) then > do i=1,num_res_cells` | `res_cell`, `res_id`, `res_stage` |

### `gwflow.solutes`

- Schema status: `readable_needs_schema_review`
- Review needed: yes
- Source expression(s): `gwflow.solutes`

- Procedure: `gwflow_read`
- Reader: `gwflow_read.f90`
- Match: source_input
- Resolved default filename(s): `gwflow.solutes`
- Source filename expression(s): `gwflow.solutes`
- Open: line 1357, file expression `'gwflow.solutes'`, parser value `gwflow.solutes`, condition `if (gw_solute_flag == 1) then > if(i_exist) then`

| Line | Role | Condition | Fields read |
| --- | --- | --- | --- |
| 1395 | header | `if (gw_solute_flag == 1) then > if(i_exist) then` | `header` |
| 1396 | header | `if (gw_solute_flag == 1) then > if(i_exist) then` | `header` |
| 1397 | data | `if (gw_solute_flag == 1) then > if(i_exist) then` | `num_ts_transport` |
| 1398 | data | `if (gw_solute_flag == 1) then > if(i_exist) then` | `gw_long_disp` |
| 1402 | header | `if (gw_solute_flag == 1) then > if(i_exist) then` | `header` |
| 1404 | data | `if (gw_solute_flag == 1) then > if(i_exist) then > do s=1,gw_nsolute` | `name`, `gwsol_sorb(s)`, `gwsol_rctn(s)`, `canal_out_conc(s)` |
| 1413 | header | `if (gw_solute_flag == 1) then > if(i_exist) then` | `header` |
| 1417 | header | `if (gw_solute_flag == 1) then > if(i_exist) then > if(grid_type == "structured") then > do s=1,gw_nsolute` | `header` |
| 1418 | data | `if (gw_solute_flag == 1) then > if(i_exist) then > if(grid_type == "structured") then > do s=1,gw_nsolute` | `read_type` |
| 1420 | data | `if (gw_solute_flag == 1) then > if(i_exist) then > if(grid_type == "structured") then > do s=1,gw_nsolute > if(read_type == "single") then` | `single_value` |
| 1424 | data | `if (gw_solute_flag == 1) then > if(i_exist) then > if(grid_type == "structured") then > do s=1,gw_nsolute > if(read_type == "single") then / elseif(read_type == "array") then > do i=1,grid_nrow` | `(grid_val(i,j),j=1,grid_ncol)` |
| 1438 | data | `if (gw_solute_flag == 1) then > if(i_exist) then > if(grid_type == "structured") then / elseif(grid_type == "unstructured") then > do i=1,ncell` | `(gwsol_state(i)%solute(s)%conc,s=1,gw_nsolute)` |
| 1497 | data | `if (gw_solute_flag == 1) then > if(i_exist) then > if (gwsol_cons == 1) then` | _no fields captured_ |
| 1500 | data | `if (gw_solute_flag == 1) then > if(i_exist) then > if (gwsol_cons == 1) then > if(grid_type == "unstructured") then` | `(cell_int(i),i=1,ncell)` |
| 1512 | data | `if (gw_solute_flag == 1) then > if(i_exist) then > if (gwsol_cons == 1) then > if(grid_type == "unstructured") then / elseif(grid_type == "structured") then > do i=1,grid_nrow` | `(grid_int(i,j),j=1,grid_ncol)` |
| 1537 | header | `if (gw_solute_flag == 1) then > if(i_exist) then > if (gwsol_cons == 1) then > do n=1,num_geol_shale` | `header` |
| 1539 | data | `if (gw_solute_flag == 1) then > if(i_exist) then > if (gwsol_cons == 1) then > do n=1,num_geol_shale > if(grid_type == "unstructured") then` | `(cell_int(i),i=1,ncell)` |
| 1555 | data | `if (gw_solute_flag == 1) then > if(i_exist) then > if (gwsol_cons == 1) then > do n=1,num_geol_shale > if(grid_type == "unstructured") then / elseif(grid_type == "structured") then > do i=1,grid_nrow` | `(grid_int(i,j),j=1,grid_ncol)` |

### `gwflow.solutes.minerals`

- Schema status: `readable_needs_schema_review`
- Review needed: yes
- Source expression(s): `gwflow.solutes.minerals`

- Procedure: `gwflow_read`
- Reader: `gwflow_read.f90`
- Match: source_input
- Resolved default filename(s): `gwflow.solutes.minerals`
- Source filename expression(s): `gwflow.solutes.minerals`
- Open: line 1445, file expression `'gwflow.solutes.minerals'`, parser value `gwflow.solutes.minerals`, condition `if (gw_solute_flag == 1) then > if(i_exist) then > if(gwsol_salt == 1) then > if(gwsol_minl == 1) then`

| Line | Role | Condition | Fields read |
| --- | --- | --- | --- |
| 1446 | header | `if (gw_solute_flag == 1) then > if(i_exist) then > if(gwsol_salt == 1) then > if(gwsol_minl == 1) then` | `header` |
| 1447 | data | `if (gw_solute_flag == 1) then > if(i_exist) then > if(gwsol_salt == 1) then > if(gwsol_minl == 1) then` | `gw_nminl` |
| 1454 | header | `if (gw_solute_flag == 1) then > if(i_exist) then > if(gwsol_salt == 1) then > if(gwsol_minl == 1) then` | `header` |
| 1458 | header | `if (gw_solute_flag == 1) then > if(i_exist) then > if(gwsol_salt == 1) then > if(gwsol_minl == 1) then > if(grid_type == "structured") then > do m=1,gw_nminl` | `header` |
| 1459 | data | `if (gw_solute_flag == 1) then > if(i_exist) then > if(gwsol_salt == 1) then > if(gwsol_minl == 1) then > if(grid_type == "structured") then > do m=1,gw_nminl` | `read_type` |
| 1461 | data | `if (gw_solute_flag == 1) then > if(i_exist) then > if(gwsol_salt == 1) then > if(gwsol_minl == 1) then > if(grid_type == "structured") then > do m=1,gw_nminl > if(read_type == "single") then` | `single_value` |
| 1465 | data | `if (gw_solute_flag == 1) then > if(i_exist) then > if(gwsol_salt == 1) then > if(gwsol_minl == 1) then > if(grid_type == "structured") then > do m=1,gw_nminl > if(read_type == "single") then / elseif(read_type == "array") then > do i=1,grid_nrow` | `(grid_val(i,j),j=1,grid_ncol)` |
| 1479 | data | `if (gw_solute_flag == 1) then > if(i_exist) then > if(gwsol_salt == 1) then > if(gwsol_minl == 1) then > if(grid_type == "structured") then / elseif(grid_type == "unstructured") then > do i=1,ncell` | `(gwsol_minl_state(i)%fract(m),m=1,gw_nminl)` |

### `gwflow.streamobs`

- Schema status: `readable_needs_schema_review`
- Review needed: yes
- Source expression(s): `gwflow.streamobs`

- Procedure: `gwflow_read`
- Reader: `gwflow_read.f90`
- Match: source_input
- Resolved default filename(s): `gwflow.streamobs`
- Source filename expression(s): `gwflow.streamobs`
- Open: line 2386, file expression `'gwflow.streamobs'`, parser value `gwflow.streamobs`, condition `if (lsu_cells_link == 1) then / else > if (nat_model == 1) then > if (stream_obs == 1) then`

| Line | Role | Condition | Fields read |
| --- | --- | --- | --- |
| 2389 | data | `if (lsu_cells_link == 1) then / else > if (nat_model == 1) then > if (stream_obs == 1) then` | _no fields captured_ |
| 2390 | data | `if (lsu_cells_link == 1) then / else > if (nat_model == 1) then > if (stream_obs == 1) then` | `gw_num_obs_chan` |
| 2398 | data | `if (lsu_cells_link == 1) then / else > if (nat_model == 1) then > if (stream_obs == 1) then > if(gw_num_obs_chan.gt.0) then > do i=1,gw_num_obs_chan` | `obs_channels(i)` |
| 2400 | data | `if (lsu_cells_link == 1) then / else > if (nat_model == 1) then > if (stream_obs == 1) then > if(gw_num_obs_chan.gt.0) then` | _no fields captured_ |
| 2401 | data | `if (lsu_cells_link == 1) then / else > if (nat_model == 1) then > if (stream_obs == 1) then > if(gw_num_obs_chan.gt.0) then` | `gw_flow_cal` |
| 2403 | data | `if (lsu_cells_link == 1) then / else > if (nat_model == 1) then > if (stream_obs == 1) then > if(gw_num_obs_chan.gt.0) then > if(gw_flow_cal.eq.1) then` | `gw_flow_cal_yrs` |
| 2405 | data | `if (lsu_cells_link == 1) then / else > if (nat_model == 1) then > if (stream_obs == 1) then > if(gw_num_obs_chan.gt.0) then` | _no fields captured_ |
| 2407 | data | `if (lsu_cells_link == 1) then / else > if (nat_model == 1) then > if (stream_obs == 1) then > if(gw_num_obs_chan.gt.0) then > do i=1,num_months` | `(obs_flow_vals(j,i),j=1,gw_num_obs_chan)` |

### `gwflow.tiles`

- Schema status: `readable_needs_schema_review`
- Review needed: yes
- Source expression(s): `gwflow.tiles`

- Procedure: `gwflow_read`
- Reader: `gwflow_read.f90`
- Match: source_input
- Resolved default filename(s): `gwflow.tiles`
- Source filename expression(s): `gwflow.tiles`
- Open: line 989, file expression `'gwflow.tiles'`, parser value `gwflow.tiles`, condition `if (gw_tile_flag == 1) then > if(i_exist) then`

| Line | Role | Condition | Fields read |
| --- | --- | --- | --- |
| 990 | header | `if (gw_tile_flag == 1) then > if(i_exist) then` | `header` |
| 992 | data | `if (gw_tile_flag == 1) then > if(i_exist) then` | `gw_tile_depth` |
| 993 | data | `if (gw_tile_flag == 1) then > if(i_exist) then` | `gw_tile_drain_area` |
| 994 | data | `if (gw_tile_flag == 1) then > if(i_exist) then` | `gw_tile_K` |
| 995 | data | `if (gw_tile_flag == 1) then > if(i_exist) then` | `gw_tile_group_flag` |
| 998 | data | `if (gw_tile_flag == 1) then > if(i_exist) then > if(gw_tile_group_flag == 1) then` | `gw_tile_num_group` |
| 1001 | data | `if (gw_tile_flag == 1) then > if(i_exist) then > if(gw_tile_group_flag == 1) then > do i=1,gw_tile_num_group` | _no fields captured_ |
| 1002 | data | `if (gw_tile_flag == 1) then > if(i_exist) then > if(gw_tile_group_flag == 1) then > do i=1,gw_tile_num_group` | `num_tile_cells(i)` |
| 1004 | data | `if (gw_tile_flag == 1) then > if(i_exist) then > if(gw_tile_group_flag == 1) then > do i=1,gw_tile_num_group > do j=1,num_tile_cells(i)` | `gw_tile_groups(i,j)` |
| 1011 | header | `if (gw_tile_flag == 1) then > if(i_exist) then` | `header` |
| 1014 | data | `if (gw_tile_flag == 1) then > if(i_exist) then > if(grid_type == "structured") then > do i=1,grid_nrow` | `(grid_int(i,j),j=1,grid_ncol)` |
| 1025 | data | `if (gw_tile_flag == 1) then > if(i_exist) then > if(grid_type == "structured") then / elseif(grid_type == "unstructured") then > do i=1,ncell` | `gw_state(i)%tile` |

### `out.key`

- Schema status: `readable_needs_schema_review`
- Review needed: yes
- Source expression(s): `out.key`

- Procedure: `gwflow_read`
- Reader: `gwflow_read.f90`
- Match: source_input
- Resolved default filename(s): `out.key`
- Source filename expression(s): `out.key`
- Open: line 1723, file expression `'out.key'`, parser value `out.key`, condition `if (lsu_cells_link == 1) then / else > if (nat_model == 1) then`

| Line | Role | Condition | Fields read |
| --- | --- | --- | --- |
| 1725 | data | `if (lsu_cells_link == 1) then / else > if (nat_model == 1) then` | _no fields captured_ |
| 1726 | data | `if (lsu_cells_link == 1) then / else > if (nat_model == 1) then` | _no fields captured_ |
| 1728 | data | `if (lsu_cells_link == 1) then / else > if (nat_model == 1) then > do k=1,sp_ob%outlet` | `dum1`, `huc12(k)` |

### `recall.rec`

- Schema status: `readable_needs_schema_review`
- Review needed: yes
- Source expression(s): `in_rec%recall_rec`, `recall.rec`

- Procedure: `recall_read`
- Reader: `recall_read.f90`
- Match: source_input
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

### `soil_plant.ini_cs`

- Schema status: `readable_needs_schema_review`
- Review needed: yes
- Source expression(s): `soil_plant.ini_cs`

- Procedure: `soil_plant_init_cs`
- Reader: `soil_plant_init_cs.f90`
- Match: source_input
- Resolved default filename(s): `soil_plant.ini_cs`
- Source filename expression(s): `soil_plant.ini_cs`
- Open: line 21, file expression `"soil_plant.ini_cs"`, parser value `soil_plant.ini_cs`, condition `if(i_exist) then`

| Line | Role | Condition | Fields read |
| --- | --- | --- | --- |
| 22 | title | `if(i_exist) then` | `titldum` |
| 23 | header | `if(i_exist) then` | `header` |
| 26 | data | `if(i_exist) then > do ii = 1, db_mx%sol_plt_ini` | `sol_plt_ini_cs(ii)%name`, `sol_plt_ini_cs(ii)%pestc`, `sol_plt_ini_cs(ii)%pathc`, `sol_plt_ini_cs(ii)%saltc`, `sol_plt_ini_cs(ii)%hmetc`, `sol_plt_ini_cs(ii)%csc` |

### `treatment.trt`

- Schema status: `readable_needs_schema_review`
- Review needed: yes
- Source expression(s): `treatment.trt`

- Procedure: `treat_read_om`
- Reader: `treat_read_om.f90`
- Match: source_input
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


## Changed input read contracts

### `calibration.cal`

- Review needed: yes
- Reader procedures changed: no
- Read-block count changed: no
- Read conditions changed: yes
- Base flattened read order: `titldum`, `mcal`, `header`, `cal_upd(i)%name`, `cal_upd(i)%chg_typ`, `cal_upd(i)%val`, `cal_upd(i)%conds`, `cal_upd(i)%lyr1`, `cal_upd(i)%lyr2`, `cal_upd(i)%year1`, `cal_upd(i)%year2`, `cal_upd(i)%day1`, `cal_upd(i)%day2`, `nspu`, `cal_upd(i)%name`, `cal_upd(i)%chg_typ`, `cal_upd(i)%val`, `cal_upd(i)%conds`, `cal_upd(i)%lyr1`, `cal_upd(i)%lyr2`, `cal_upd(i)%year1`, `cal_upd(i)%year2`, `cal_upd(i)%day1`, `cal_upd(i)%day2`, `cal_upd(i)%num_tot`, `(elem_cnt(isp), isp = 1, nspu)`, `cal_upd(i)%cond(icond)`
- Candidate flattened read order: `titldum`, `mcal`, `header`, `cal_upd(i)%name`, `cal_upd(i)%chg_typ`, `cal_upd(i)%val`, `cal_upd(i)%conds`, `cal_upd(i)%lyr1`, `cal_upd(i)%lyr2`, `cal_upd(i)%year1`, `cal_upd(i)%year2`, `cal_upd(i)%day1`, `cal_upd(i)%day2`, `nspu`, `cal_upd(i)%name`, `cal_upd(i)%chg_typ`, `cal_upd(i)%val`, `cal_upd(i)%conds`, `cal_upd(i)%lyr1`, `cal_upd(i)%lyr2`, `cal_upd(i)%year1`, `cal_upd(i)%year2`, `cal_upd(i)%day1`, `cal_upd(i)%day2`, `cal_upd(i)%num_tot`, `(elem_cnt(isp), isp = 1, nspu)`, `range`, `range`, `cal_upd(i)%cond(icond)%var`, `cal_upd(i)%val1`, `cal_upd(i)%val2`, `cal_upd(i)%cond(icond)`

#### Read-order edits

- `insert` at base index 26 / candidate index 26: removed _no fields captured_; added `range`, `range`, `cal_upd(i)%cond(icond)%var`, `cal_upd(i)%val1`, `cal_upd(i)%val2`

#### Base read structure

- Schema status: `certified`
- Review needed: no
- Source expression(s): `in_chg%cal_upd`, `calibration.cal`

- Procedure: `cal_parmchg_read`
- Reader: `cal_parmchg_read.f90`
- Match: source_input
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


#### Candidate read structure

- Schema status: `certified`
- Review needed: no
- Source expression(s): `in_chg%cal_upd`, `calibration.cal`

- Procedure: `cal_parmchg_read`
- Reader: `cal_parmchg_read.f90`
- Match: source_input
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

### `delratio.del`

- Review needed: yes
- Reader procedures changed: yes
- Read-block count changed: yes
- Read conditions changed: yes
- Base flattened read order: `titldum`, `mdr_sp`, `header`, `dr_om(i,ii)`, `titldum`, `header`, `titldum`, `titldum`, `header`, `dr_db(ii)`
- Candidate flattened read order: `titldum`, `header`, `titldum`, `titldum`, `header`, `dr_db(ii)`

#### Read-order edits

- `delete` at base index 0 / candidate index 0: removed `titldum`, `mdr_sp`, `header`, `dr_om(i,ii)`; added _no fields captured_

#### Base read structure

- Schema status: `certified`
- Review needed: no
- Source expression(s): `in_delr%del_ratio`, `delratio.del`

- Procedure: `dr_db_read`
- Reader: `dr_db_read.f90`
- Match: source_input
- Resolved default filename(s): `delratio.del`
- Source filename expression(s): `in_delr%del_ratio`, `delratio.del`
- Open: line 24, file expression `in_delr%del_ratio`, parser value `delratio.del`, condition `if (i_exist .or. in_delr%del_ratio /= "null") then > do`

| Line | Role | Condition | Fields read |
| --- | --- | --- | --- |
| 25 | title | `if (i_exist .or. in_delr%del_ratio /= "null") then > do` | `titldum` |
| 27 | header | `if (i_exist .or. in_delr%del_ratio /= "null") then > do` | `header` |
| 31 | title | `if (i_exist .or. in_delr%del_ratio /= "null") then > do > do while (eof == 0)` | `titldum` |
| 40 | title | `if (i_exist .or. in_delr%del_ratio /= "null") then > do` | `titldum` |
| 42 | header | `if (i_exist .or. in_delr%del_ratio /= "null") then > do` | `header` |
| 46 | data | `if (i_exist .or. in_delr%del_ratio /= "null") then > do > do ii = 1, imax` | `dr_db(ii)` |


- Procedure: `dr_read`
- Reader: `dr_read.f90`
- Match: source_input
- Resolved default filename(s): `delratio.del`
- Source filename expression(s): `in_delr%del_ratio`, `delratio.del`
- Open: line 25, file expression `in_delr%del_ratio`, parser value `delratio.del`, condition `if (i_exist .or. in_delr%del_ratio /= 'null') then > do`

| Line | Role | Condition | Fields read |
| --- | --- | --- | --- |
| 26 | title | `if (i_exist .or. in_delr%del_ratio /= 'null') then > do` | `titldum` |
| 28 | data | `if (i_exist .or. in_delr%del_ratio /= 'null') then > do` | `mdr_sp` |
| 31 | header | `if (i_exist .or. in_delr%del_ratio /= 'null') then > do` | `header` |
| 34 | data | `if (i_exist .or. in_delr%del_ratio /= 'null') then > do > do ii = 1, mdr_sp` | `dr_om(i,ii)` |


#### Candidate read structure

- Schema status: `certified`
- Review needed: no
- Source expression(s): `in_delr%del_ratio`, `delratio.del`

- Procedure: `dr_db_read`
- Reader: `dr_db_read.f90`
- Match: source_input
- Resolved default filename(s): `delratio.del`
- Source filename expression(s): `in_delr%del_ratio`, `delratio.del`
- Open: line 25, file expression `in_delr%del_ratio`, parser value `delratio.del`, condition `if (i_exist .or. in_delr%del_ratio /= "null") then > do`

| Line | Role | Condition | Fields read |
| --- | --- | --- | --- |
| 26 | title | `if (i_exist .or. in_delr%del_ratio /= "null") then > do` | `titldum` |
| 28 | header | `if (i_exist .or. in_delr%del_ratio /= "null") then > do` | `header` |
| 32 | title | `if (i_exist .or. in_delr%del_ratio /= "null") then > do > do while (eof == 0)` | `titldum` |
| 41 | title | `if (i_exist .or. in_delr%del_ratio /= "null") then > do` | `titldum` |
| 43 | header | `if (i_exist .or. in_delr%del_ratio /= "null") then > do` | `header` |
| 47 | data | `if (i_exist .or. in_delr%del_ratio /= "null") then > do > do ii = 1, imax` | `dr_db(ii)` |

### `exco.exc`

- Review needed: yes
- Reader procedures changed: yes
- Read-block count changed: yes
- Read conditions changed: yes
- Base flattened read order: `titldum`, `header`, `titldum`, `titldum`, `header`, `titldum`, `namedum`, `exco(ii)`, `titldum`, `header`, `titldum`, `titldum`, `header`, `exco_db(ii)`
- Candidate flattened read order: `titldum`, `header`, `header`, `titldum`, `titldum`, `header`, `header`, `i`, `k`, `exco_db(i)`

#### Read-order edits

- `insert` at base index 1 / candidate index 1: removed _no fields captured_; added `header`
- `delete` at base index 5 / candidate index 6: removed `titldum`, `namedum`, `exco(ii)`, `titldum`; added _no fields captured_
- `replace` at base index 10 / candidate index 7: removed `titldum`, `titldum`, `header`, `exco_db(ii)`; added `i`, `k`, `exco_db(i)`

#### Base read structure

- Schema status: `certified`
- Review needed: no
- Source expression(s): `in_exco%exco`, `exco.exc`

- Procedure: `exco_db_read`
- Reader: `exco_db_read.f90`
- Match: source_input
- Resolved default filename(s): `exco.exc`
- Source filename expression(s): `in_exco%exco`, `exco.exc`
- Open: line 23, file expression `in_exco%exco`, parser value `exco.exc`, condition `if (i_exist .or. in_exco%exco /= "null") then > do`

| Line | Role | Condition | Fields read |
| --- | --- | --- | --- |
| 24 | title | `if (i_exist .or. in_exco%exco /= "null") then > do` | `titldum` |
| 26 | header | `if (i_exist .or. in_exco%exco /= "null") then > do` | `header` |
| 30 | title | `if (i_exist .or. in_exco%exco /= "null") then > do > do while (eof == 0)` | `titldum` |
| 39 | title | `if (i_exist .or. in_exco%exco /= "null") then > do` | `titldum` |
| 41 | header | `if (i_exist .or. in_exco%exco /= "null") then > do` | `header` |
| 45 | data | `if (i_exist .or. in_exco%exco /= "null") then > do > do ii = 1, imax` | `exco_db(ii)` |


- Procedure: `exco_read`
- Reader: `exco_read.f90`
- Match: source_input
- Resolved default filename(s): `exco.exc`
- Source filename expression(s): `in_exco%exco`, `exco.exc`
- Open: line 30, file expression `in_exco%exco`, parser value `exco.exc`, condition `if (i_exist .or. in_exco%exco /= 'null') then > do`

| Line | Role | Condition | Fields read |
| --- | --- | --- | --- |
| 31 | title | `if (i_exist .or. in_exco%exco /= 'null') then > do` | `titldum` |
| 33 | header | `if (i_exist .or. in_exco%exco /= 'null') then > do` | `header` |
| 37 | title | `if (i_exist .or. in_exco%exco /= 'null') then > do > do while (eof == 0)` | `titldum` |
| 46 | title | `if (i_exist .or. in_exco%exco /= 'null') then > do` | `titldum` |
| 48 | header | `if (i_exist .or. in_exco%exco /= 'null') then > do` | `header` |
| 53 | title | `if (i_exist .or. in_exco%exco /= 'null') then > do > do ii = 1, db_mx%exco` | `titldum` |
| 56 | data | `if (i_exist .or. in_exco%exco /= 'null') then > do > do ii = 1, db_mx%exco` | `namedum`, `exco(ii)` |


#### Candidate read structure

- Schema status: `certified`
- Review needed: no
- Source expression(s): `in_exco%exco`, `exco.exc`

- Procedure: `exco_db_read`
- Reader: `exco_db_read.f90`
- Match: source_input
- Resolved default filename(s): `exco.exc`
- Source filename expression(s): `in_exco%exco`, `exco.exc`
- Open: line 27, file expression `in_exco%exco`, parser value `exco.exc`, condition `if (i_exist .or. in_exco%exco /= "null") then > do`

| Line | Role | Condition | Fields read |
| --- | --- | --- | --- |
| 28 | title | `if (i_exist .or. in_exco%exco /= "null") then > do` | `titldum` |
| 30 | header | `if (i_exist .or. in_exco%exco /= "null") then > do` | `header` |
| 32 | header | `if (i_exist .or. in_exco%exco /= "null") then > do` | `header` |
| 36 | title | `if (i_exist .or. in_exco%exco /= "null") then > do > do while (eof == 0)` | `titldum` |
| 45 | title | `if (i_exist .or. in_exco%exco /= "null") then > do` | `titldum` |
| 47 | header | `if (i_exist .or. in_exco%exco /= "null") then > do` | `header` |
| 49 | header | `if (i_exist .or. in_exco%exco /= "null") then > do` | `header` |
| 53 | data | `if (i_exist .or. in_exco%exco /= "null") then > do > do ii = 1, imax` | `i` |
| 56 | data | `if (i_exist .or. in_exco%exco /= "null") then > do > do ii = 1, imax` | `k`, `exco_db(i)` |

### `exco_om.exc`

- Review needed: yes
- Reader procedures changed: no
- Read-block count changed: no
- Read conditions changed: yes
- Base flattened read order: `titldum`, `header`, `titldum`, `titldum`, `header`, `titldum`, `exco_om_name(ii)`, `exco(ii)`
- Candidate flattened read order: `titldum`, `header`, `header`, `titldum`, `titldum`, `header`, `header`, `exco_om_name(ii)`, `exco(ii)`

#### Read-order edits

- `insert` at base index 1 / candidate index 1: removed _no fields captured_; added `header`
- `replace` at base index 5 / candidate index 6: removed `titldum`; added `header`

#### Base read structure

- Schema status: `certified`
- Review needed: no
- Source expression(s): `in_exco%om`, `exco_om.exc`

- Procedure: `exco_read_om`
- Reader: `exco_read_om.f90`
- Match: source_input
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


#### Candidate read structure

- Schema status: `certified`
- Review needed: no
- Source expression(s): `in_exco%om`, `exco_om.exc`

- Procedure: `exco_read_om`
- Reader: `exco_read_om.f90`
- Match: source_input
- Resolved default filename(s): `exco_om.exc`
- Source filename expression(s): `in_exco%om`, `exco_om.exc`
- Open: line 31, file expression `in_exco%om`, parser value `exco_om.exc`, condition `if (i_exist .or. in_exco%om /= "null") then > do`

| Line | Role | Condition | Fields read |
| --- | --- | --- | --- |
| 32 | title | `if (i_exist .or. in_exco%om /= "null") then > do` | `titldum` |
| 34 | header | `if (i_exist .or. in_exco%om /= "null") then > do` | `header` |
| 36 | header | `if (i_exist .or. in_exco%om /= "null") then > do` | `header` |
| 40 | title | `if (i_exist .or. in_exco%om /= "null") then > do > do while (eof == 0)` | `titldum` |
| 51 | title | `if (i_exist .or. in_exco%om /= "null") then > do` | `titldum` |
| 53 | header | `if (i_exist .or. in_exco%om /= "null") then > do` | `header` |
| 55 | header | `if (i_exist .or. in_exco%om /= "null") then > do` | `header` |
| 60 | data | `if (i_exist .or. in_exco%om /= "null") then > do > do ii = 1, db_mx%exco_om` | `exco_om_name(ii)`, `exco(ii)` |

### `file.cio`

- Review needed: yes
- Reader procedures changed: no
- Read-block count changed: no
- Read conditions changed: yes
- Base flattened read order: `titldum`, `name`, `in_sim`, `name`, `in_basin`, `name`, `in_cli`, `name`, `in_con`, `name`, `in_cha`, `name`, `in_res`, `name`, `in_ru`, `name`, `in_hru`, `name`, `in_exco`, `name`, `in_rec`, `name`, `in_delr`, `name`, `in_aqu`, `name`, `in_herd`, `name`, `in_watrts`, `name`, `in_link`, `name`, `in_hyd`, `name`, `in_str`, `name`, `in_parmdb`, `name`, `in_ops`, `name`, `in_lum`, `name`, `in_chg`, `name`, `in_init`, `name`, `in_sol`, `name`, `in_cond`, `name`, `in_regs`, `name`, `in_path_pcp`, `name`, `in_path_tmp`, `name`, `in_path_slr`, `name`, `in_path_hmd`, `name`, `in_path_wnd`
- Candidate flattened read order: `titldum`, `name`, `in_sim`, `name`, `in_basin`, `name`, `in_cli`, `name`, `in_con`, `name`, `in_cha`, `name`, `in_res`, `name`, `in_ru`, `name`, `in_hru`, `name`, `in_exco`, `name`, `in_rec`, `name`, `in_delr`, `name`, `in_aqu`, `name`, `in_herd`, `name`, `in_watrts`, `name`, `in_link`, `name`, `in_hyd`, `name`, `in_str`, `name`, `in_parmdb`, `name`, `in_ops`, `name`, `in_lum`, `name`, `in_chg`, `name`, `in_init`, `name`, `in_sol`, `name`, `in_cond`, `name`, `in_regs`, `name`, `in_path_pcp`, `name`, `in_path_tmp`, `name`, `in_path_slr`, `name`, `in_path_hmd`, `name`, `in_path_wnd`, `line_buffer`

#### Read-order edits

- `insert` at base index 61 / candidate index 61: removed _no fields captured_; added `line_buffer`

#### Base read structure

- Schema status: `readable_needs_schema_review`
- Review needed: yes
- Source expression(s): `file.cio`

- Procedure: `readcio_read`
- Reader: `readcio_read.f90`
- Match: source_input
- Resolved default filename(s): `file.cio`
- Source filename expression(s): `file.cio`
- Open: line 18, file expression `"file.cio"`, parser value `file.cio`, condition `if (i_exist ) then`

| Line | Role | Condition | Fields read |
| --- | --- | --- | --- |
| 19 | title | `if (i_exist ) then` | `titldum` |
| 21 | data | `if (i_exist ) then > do i = 1, 31` | `name`, `in_sim` |
| 23 | data | `if (i_exist ) then > do i = 1, 31` | `name`, `in_basin` |
| 25 | data | `if (i_exist ) then > do i = 1, 31` | `name`, `in_cli` |
| 27 | data | `if (i_exist ) then > do i = 1, 31` | `name`, `in_con` |
| 29 | data | `if (i_exist ) then > do i = 1, 31` | `name`, `in_cha` |
| 31 | data | `if (i_exist ) then > do i = 1, 31` | `name`, `in_res` |
| 33 | data | `if (i_exist ) then > do i = 1, 31` | `name`, `in_ru` |
| 35 | data | `if (i_exist ) then > do i = 1, 31` | `name`, `in_hru` |
| 37 | data | `if (i_exist ) then > do i = 1, 31` | `name`, `in_exco` |
| 39 | data | `if (i_exist ) then > do i = 1, 31` | `name`, `in_rec` |
| 41 | data | `if (i_exist ) then > do i = 1, 31` | `name`, `in_delr` |
| 43 | data | `if (i_exist ) then > do i = 1, 31` | `name`, `in_aqu` |
| 45 | data | `if (i_exist ) then > do i = 1, 31` | `name`, `in_herd` |
| 47 | data | `if (i_exist ) then > do i = 1, 31` | `name`, `in_watrts` |
| 49 | data | `if (i_exist ) then > do i = 1, 31` | `name`, `in_link` |
| 51 | data | `if (i_exist ) then > do i = 1, 31` | `name`, `in_hyd` |
| 53 | data | `if (i_exist ) then > do i = 1, 31` | `name`, `in_str` |
| 55 | data | `if (i_exist ) then > do i = 1, 31` | `name`, `in_parmdb` |
| 57 | data | `if (i_exist ) then > do i = 1, 31` | `name`, `in_ops` |
| 59 | data | `if (i_exist ) then > do i = 1, 31` | `name`, `in_lum` |
| 61 | data | `if (i_exist ) then > do i = 1, 31` | `name`, `in_chg` |
| 63 | data | `if (i_exist ) then > do i = 1, 31` | `name`, `in_init` |
| 65 | data | `if (i_exist ) then > do i = 1, 31` | `name`, `in_sol` |
| 67 | data | `if (i_exist ) then > do i = 1, 31` | `name`, `in_cond` |
| 69 | data | `if (i_exist ) then > do i = 1, 31` | `name`, `in_regs` |
| 72 | data | `if (i_exist ) then > do i = 1, 31` | `name`, `in_path_pcp` |
| 74 | data | `if (i_exist ) then > do i = 1, 31` | `name`, `in_path_tmp` |
| 76 | data | `if (i_exist ) then > do i = 1, 31` | `name`, `in_path_slr` |
| 78 | data | `if (i_exist ) then > do i = 1, 31` | `name`, `in_path_hmd` |
| 80 | data | `if (i_exist ) then > do i = 1, 31` | `name`, `in_path_wnd` |


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

### `gwflow.wetland`

- Review needed: yes
- Reader procedures changed: no
- Read-block count changed: no
- Read conditions changed: yes
- Base flattened read order: `header`, `header`, `header`, `header`, `header`, `dum1`, `wet_thick(ires)`
- Candidate flattened read order: `header`, `header`, `wet_name`, `thick_val`, `hru_idx`

#### Read-order edits

- `replace` at base index 2 / candidate index 2: removed `header`, `header`, `header`, `dum1`, `wet_thick(ires)`; added `wet_name`, `thick_val`, `hru_idx`

#### Base read structure

- Schema status: `certified`
- Review needed: no
- Source expression(s): `gwflow.wetland`

- Procedure: `wet_read_hyd`
- Reader: `wet_read_hyd.f90`
- Match: source_input
- Resolved default filename(s): `gwflow.wetland`
- Source filename expression(s): `gwflow.wetland`
- Open: line 72, file expression `'gwflow.wetland'`, parser value `gwflow.wetland`, condition `if (bsn_cc%gwflow == 1 .and. gw_wet_flag == 1) then > if(i_exist) then`

| Line | Role | Condition | Fields read |
| --- | --- | --- | --- |
| 73 | header | `if (bsn_cc%gwflow == 1 .and. gw_wet_flag == 1) then > if(i_exist) then` | `header` |
| 74 | header | `if (bsn_cc%gwflow == 1 .and. gw_wet_flag == 1) then > if(i_exist) then` | `header` |
| 75 | header | `if (bsn_cc%gwflow == 1 .and. gw_wet_flag == 1) then > if(i_exist) then` | `header` |
| 76 | header | `if (bsn_cc%gwflow == 1 .and. gw_wet_flag == 1) then > if(i_exist) then` | `header` |
| 78 | header | `if (bsn_cc%gwflow == 1 .and. gw_wet_flag == 1) then > if(i_exist) then` | `header` |
| 80 | data | `if (bsn_cc%gwflow == 1 .and. gw_wet_flag == 1) then > if(i_exist) then > do ires=1,imax` | `dum1`, `wet_thick(ires)` |


#### Candidate read structure

- Schema status: `certified`
- Review needed: no
- Source expression(s): `gwflow.wetland`, `unit_wet_name(idig:)`

- Procedure: `wet_read_hyd`
- Reader: `wet_read_hyd.f90`
- Match: source_input
- Resolved default filename(s): `gwflow.wetland`
- Source filename expression(s): `gwflow.wetland`, `unit_wet_name(idig:)`
- Open: line 78, file expression `'gwflow.wetland'`, parser value `gwflow.wetland`, condition `if (bsn_cc%gwflow == 1 .and. gw_wet_flag == 1) then > if(i_exist) then`

| Line | Role | Condition | Fields read |
| --- | --- | --- | --- |
| 79 | header | `if (bsn_cc%gwflow == 1 .and. gw_wet_flag == 1) then > if(i_exist) then` | `header` |
| 80 | header | `if (bsn_cc%gwflow == 1 .and. gw_wet_flag == 1) then > if(i_exist) then` | `header` |
| 82 | data | `if (bsn_cc%gwflow == 1 .and. gw_wet_flag == 1) then > if(i_exist) then > do` | `wet_name`, `thick_val` |
| 86 | data | `if (bsn_cc%gwflow == 1 .and. gw_wet_flag == 1) then > if(i_exist) then > do > if (idig > 0) then` | `hru_idx` |

### `hru-data.hru`

- Review needed: yes
- Reader procedures changed: no
- Read-block count changed: no
- Read conditions changed: yes
- Base flattened read order: `titldum`, `header`, `i`, `titldum`, `header`, `i`, `k`, `hru_db(i)%dbsc`
- Candidate flattened read order: `titldum`, `header`, `i`, `titldum`, `header`, `i`, `k`, `hru_db(i)%dbsc`

#### Read-order edits

_No field-order edits; the contract changed in structure or conditions._

#### Base read structure

- Schema status: `certified`
- Review needed: no
- Source expression(s): `in_hru%hru_data`, `hru-data.hru`

- Procedure: `hru_read`
- Reader: `hru_read.f90`
- Match: source_input
- Resolved default filename(s): `hru-data.hru`
- Source filename expression(s): `in_hru%hru_data`, `hru-data.hru`
- Open: line 43, file expression `in_hru%hru_data`, parser value `hru-data.hru`, condition `if (.not. i_exist .or. in_hru%hru_data == "null") then / else > do`

| Line | Role | Condition | Fields read |
| --- | --- | --- | --- |
| 44 | title | `if (.not. i_exist .or. in_hru%hru_data == "null") then / else > do` | `titldum` |
| 46 | header | `if (.not. i_exist .or. in_hru%hru_data == "null") then / else > do` | `header` |
| 49 | data | `if (.not. i_exist .or. in_hru%hru_data == "null") then / else > do > do while (eof == 0)` | `i` |
| 57 | title | `if (.not. i_exist .or. in_hru%hru_data == "null") then / else > do` | `titldum` |
| 59 | header | `if (.not. i_exist .or. in_hru%hru_data == "null") then / else > do` | `header` |
| 63 | data | `if (.not. i_exist .or. in_hru%hru_data == "null") then / else > do > do ihru = 1, sp_ob%hru` | `i` |
| 66 | data | `if (.not. i_exist .or. in_hru%hru_data == "null") then / else > do > do ihru = 1, sp_ob%hru` | `k`, `hru_db(i)%dbsc` |


#### Candidate read structure

- Schema status: `certified`
- Review needed: no
- Source expression(s): `in_hru%hru_data`, `hru-data.hru`

- Procedure: `hru_read`
- Reader: `hru_read.f90`
- Match: source_input
- Resolved default filename(s): `hru-data.hru`
- Source filename expression(s): `in_hru%hru_data`, `hru-data.hru`
- Open: line 44, file expression `in_hru%hru_data`, parser value `hru-data.hru`, condition `if (.not. i_exist .or. in_hru%hru_data == "null") then / else > do`

| Line | Role | Condition | Fields read |
| --- | --- | --- | --- |
| 45 | title | `if (.not. i_exist .or. in_hru%hru_data == "null") then / else > do` | `titldum` |
| 47 | header | `if (.not. i_exist .or. in_hru%hru_data == "null") then / else > do` | `header` |
| 50 | data | `if (.not. i_exist .or. in_hru%hru_data == "null") then / else > do > do while (eof == 0)` | `i` |
| 58 | title | `if (.not. i_exist .or. in_hru%hru_data == "null") then / else > do` | `titldum` |
| 60 | header | `if (.not. i_exist .or. in_hru%hru_data == "null") then / else > do` | `header` |
| 64 | data | `if (.not. i_exist .or. in_hru%hru_data == "null") then / else > do > do ihru = 1, imax` | `i` |
| 67 | data | `if (.not. i_exist .or. in_hru%hru_data == "null") then / else > do > do ihru = 1, imax` | `k`, `hru_db(i)%dbsc` |

### `hru.con`

- Review needed: yes
- Reader procedures changed: yes
- Read-block count changed: yes
- Read conditions changed: yes
- Base flattened read order: `titldum`, `header`, `ob(i)%num`, `ob(i)%name`, `ob(i)%gis_id`, `ob(i)%area_ha`, `ob(i)%lat`, `ob(i)%long`, `ob(i)%elev`, `ob(i)%props`, `ob(i)%wst_c`, `ob(i)%constit`, `ob(i)%props2`, `ob(i)%ruleset`, `ob(i)%src_tot`, `ob(i)%num`, `ob(i)%name`, `ob(i)%gis_id`, `ob(i)%area_ha`, `ob(i)%lat`, `ob(i)%long`, `ob(i)%elev`, `ob(i)%props`, `ob(i)%wst_c`, `ob(i)%constit`, `ob(i)%props2`, `ob(i)%ruleset`, `ob(i)%src_tot`, `(ob(i)%obtyp_out(isp), ob(i)%obtypno_out(isp), ob(i)%htyp_out(isp), ob(i)%frac_out(isp), isp = 1, nout)`, `dum1`, `dum2`, `dum3`, `dum4`, `dum5`, `dum6`, `dum7`, `dum8`, `huc12_id`, `hru_id`, `dum1`, `dum2`, `dum3`, `dum4`, `dum5`, `dum6`, `dum7`, `dum8`, `huc12_id`
- Candidate flattened read order: `titldum`, `header`, `ob(i)%num`, `ob(i)%name`, `ob(i)%gis_id`, `ob(i)%area_ha`, `ob(i)%lat`, `ob(i)%long`, `ob(i)%elev`, `ob(i)%props`, `ob(i)%wst_c`, `ob(i)%constit`, `ob(i)%props2`, `ob(i)%ruleset`, `ob(i)%src_tot`, `ob(i)%num`, `ob(i)%name`, `ob(i)%gis_id`, `ob(i)%area_ha`, `ob(i)%lat`, `ob(i)%long`, `ob(i)%elev`, `ob(i)%props`, `ob(i)%wst_c`, `ob(i)%constit`, `ob(i)%props2`, `ob(i)%ruleset`, `ob(i)%src_tot`, `(ob(i)%obtyp_out(isp), ob(i)%obtypno_out(isp), ob(i)%htyp_out(isp), ob(i)%frac_out(isp), isp = 1, nout)`

#### Read-order edits

- `delete` at base index 29 / candidate index 29: removed `dum1`, `dum2`, `dum3`, `dum4`, `dum5`, `dum6`, `dum7`, `dum8`, `huc12_id`, `hru_id`, `dum1`, `dum2`, `dum3`, `dum4`, `dum5`, `dum6`, `dum7`, `dum8`, `huc12_id`; added _no fields captured_

#### Base read structure

- Schema status: `certified`
- Review needed: no
- Source expression(s): `hru.con`, `con_file`

- Procedure: `gwflow_read`
- Reader: `gwflow_read.f90`
- Match: source_input
- Resolved default filename(s): `hru.con`
- Source filename expression(s): `hru.con`
- Open: line 1731, file expression `'hru.con'`, parser value `hru.con`, condition `if (lsu_cells_link == 1) then / else > if (nat_model == 1) then`

| Line | Role | Condition | Fields read |
| --- | --- | --- | --- |
| 1735 | data | `if (lsu_cells_link == 1) then / else > if (nat_model == 1) then` | _no fields captured_ |
| 1736 | data | `if (lsu_cells_link == 1) then / else > if (nat_model == 1) then` | _no fields captured_ |
| 1738 | data | `if (lsu_cells_link == 1) then / else > if (nat_model == 1) then > do k=1,sp_ob%outlet` | `dum1`, `dum2`, `dum3`, `dum4`, `dum5`, `dum6`, `dum7`, `dum8`, `huc12_id` |
| 1743 | data | `if (lsu_cells_link == 1) then / else > if (nat_model == 1) then > do k=1,sp_ob%outlet > do while (huc12_id.eq.huc12(k))` | `hru_id` |
| 1746 | data | `if (lsu_cells_link == 1) then / else > if (nat_model == 1) then > do k=1,sp_ob%outlet > do while (huc12_id.eq.huc12(k))` | `dum1`, `dum2`, `dum3`, `dum4`, `dum5`, `dum6`, `dum7`, `dum8`, `huc12_id` |


- Procedure: `hyd_read_connect`
- Reader: `hyd_read_connect.f90`
- Match: source_input
- Resolved default filename(s): `hru.con`, `hru-lte.con`, `rout_unit.con`, `aquifer.con`, `channel.con`, `reservoir.con`, `recall.con`, `exco.con`, `delratio.con`, `outlet.con`, `chandeg.con`, `gwflow.con`
- Source filename expression(s): `con_file`
- Open: line 55, file expression `con_file`, parser value `con_file`, condition `if (i_exist ) then > do`

| Line | Role | Condition | Fields read |
| --- | --- | --- | --- |
| 56 | title | `if (i_exist ) then > do` | `titldum` |
| 58 | header | `if (i_exist ) then > do` | `header` |
| 217 | data | `if (i_exist ) then > do > if (nspu > 0) then > do i = ob1, ob2` | `ob(i)%num`, `ob(i)%name`, `ob(i)%gis_id`, `ob(i)%area_ha`, `ob(i)%lat`, `ob(i)%long`, `ob(i)%elev`, `ob(i)%props`, `ob(i)%wst_c`, `ob(i)%constit`, `ob(i)%props2`, `ob(i)%ruleset`, `ob(i)%src_tot` |
| 294 | data | `if (i_exist ) then > do > if (nspu > 0) then > do i = ob1, ob2 > if (ob(i)%src_tot > 0) then` | `ob(i)%num`, `ob(i)%name`, `ob(i)%gis_id`, `ob(i)%area_ha`, `ob(i)%lat`, `ob(i)%long`, `ob(i)%elev`, `ob(i)%props`, `ob(i)%wst_c`, `ob(i)%constit`, `ob(i)%props2`, `ob(i)%ruleset`, `ob(i)%src_tot`, `(ob(i)%obtyp_out(isp), ob(i)%obtypno_out(isp), ob(i)%htyp_out(isp), ob(i)%frac_out(isp), isp = 1, nout)` |


#### Candidate read structure

- Schema status: `certified`
- Review needed: no
- Source expression(s): `con_file`

- Procedure: `hyd_read_connect`
- Reader: `hyd_read_connect.f90`
- Match: source_input
- Resolved default filename(s): `hru.con`, `hru-lte.con`, `rout_unit.con`, `aquifer.con`, `channel.con`, `reservoir.con`, `recall.con`, `exco.con`, `delratio.con`, `outlet.con`, `chandeg.con`, `gwflow.con`
- Source filename expression(s): `con_file`
- Open: line 57, file expression `con_file`, parser value `con_file`, condition `if (i_exist ) then > do`

| Line | Role | Condition | Fields read |
| --- | --- | --- | --- |
| 58 | title | `if (i_exist ) then > do` | `titldum` |
| 60 | header | `if (i_exist ) then > do` | `header` |
| 220 | data | `if (i_exist ) then > do > if (nspu > 0) then > do i = ob1, ob2` | `ob(i)%num`, `ob(i)%name`, `ob(i)%gis_id`, `ob(i)%area_ha`, `ob(i)%lat`, `ob(i)%long`, `ob(i)%elev`, `ob(i)%props`, `ob(i)%wst_c`, `ob(i)%constit`, `ob(i)%props2`, `ob(i)%ruleset`, `ob(i)%src_tot` |
| 298 | data | `if (i_exist ) then > do > if (nspu > 0) then > do i = ob1, ob2 > if (ob(i)%src_tot > 0) then` | `ob(i)%num`, `ob(i)%name`, `ob(i)%gis_id`, `ob(i)%area_ha`, `ob(i)%lat`, `ob(i)%long`, `ob(i)%elev`, `ob(i)%props`, `ob(i)%wst_c`, `ob(i)%constit`, `ob(i)%props2`, `ob(i)%ruleset`, `ob(i)%src_tot`, `(ob(i)%obtyp_out(isp), ob(i)%obtypno_out(isp), ob(i)%htyp_out(isp), ob(i)%frac_out(isp), isp = 1, nout)` |

### `manure_allo.mnu`

- Review needed: yes
- Reader procedures changed: no
- Read-block count changed: no
- Read conditions changed: yes
- Base flattened read order: `titldum`, `imax`, `header`, `mallo(imro)%name`, `mallo(imro)%rule_typ`, `mallo(imro)%src_obs`, `mallo(imro)%dmd_obs`, `header`, `i`, `k`, `mallo(imro)%src(i)%mois_typ`, `mallo(imro)%src(i)%manure_typ`, `mallo(imro)%src(i)%lat`, `mallo(imro)%src(i)%long`, `mallo(imro)%src(i)%stor_init`, `mallo(imro)%src(i)%stor_max`, `mallo(imro)%src(i)%prod_mon`, `header`, `i`, `k`, `mallo(imro)%dmd(i)%ob_typ`, `mallo(imro)%dmd(i)%ob_num`, `mallo(imro)%dmd(i)%dtbl`, `mallo(imro)%dmd(i)%right`
- Candidate flattened read order: `titldum`, `imax`, `header`, `mallo(imro)%name`, `mallo(imro)%rule_typ`, `mallo(imro)%src_obs`, `mallo(imro)%trn_obs`, `header`, `i`, `k`, `mallo(imro)%src(i)%mois_typ`, `mallo(imro)%src(i)%manure_typ`, `mallo(imro)%src(i)%lat`, `mallo(imro)%src(i)%long`, `mallo(imro)%src(i)%stor_init`, `mallo(imro)%src(i)%stor_max`, `mallo(imro)%src(i)%prod_mon`, `header`, `i`, `k`, `mallo(imro)%trn(i)%ob_typ`, `mallo(imro)%trn(i)%ob_num`, `mallo(imro)%trn(i)%dtbl`, `mallo(imro)%trn(i)%right`

#### Read-order edits

- `replace` at base index 6 / candidate index 6: removed `mallo(imro)%dmd_obs`; added `mallo(imro)%trn_obs`
- `replace` at base index 20 / candidate index 20: removed `mallo(imro)%dmd(i)%ob_typ`, `mallo(imro)%dmd(i)%ob_num`, `mallo(imro)%dmd(i)%dtbl`, `mallo(imro)%dmd(i)%right`; added `mallo(imro)%trn(i)%ob_typ`, `mallo(imro)%trn(i)%ob_num`, `mallo(imro)%trn(i)%dtbl`, `mallo(imro)%trn(i)%right`

#### Base read structure

- Schema status: `certified`
- Review needed: no
- Source expression(s): `manure_allo.mnu`

- Procedure: `manure_allocation_read`
- Reader: `manure_allocation_read.f90`
- Match: source_input
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


#### Candidate read structure

- Schema status: `certified`
- Review needed: no
- Source expression(s): `manure_allo.mnu`

- Procedure: `manure_allocation_read`
- Reader: `manure_allocation_read.f90`
- Match: source_input
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

### `plants.plt`

- Review needed: yes
- Reader procedures changed: no
- Read-block count changed: no
- Read conditions changed: yes
- Base flattened read order: `titldum`, `header`, `titldum`, `titldum`, `header`, `pldb(ic)`
- Candidate flattened read order: `titldum`, `header`, `titldum`, `titldum`, `header`, `pldb(ic)`, `pldb(ic)`, `pl_class(ic)`

#### Read-order edits

- `insert` at base index 6 / candidate index 6: removed _no fields captured_; added `pldb(ic)`, `pl_class(ic)`

#### Base read structure

- Schema status: `certified`
- Review needed: no
- Source expression(s): `in_parmdb%plants_plt`, `plants.plt`

- Procedure: `plant_parm_read`
- Reader: `plant_parm_read.f90`
- Match: source_input
- Resolved default filename(s): `plants.plt`
- Source filename expression(s): `in_parmdb%plants_plt`, `plants.plt`
- Open: line 28, file expression `in_parmdb%plants_plt`, parser value `plants.plt`, condition `if (.not. i_exist .or. in_parmdb%plants_plt == " null") then / else > do`

| Line | Role | Condition | Fields read |
| --- | --- | --- | --- |
| 29 | title | `if (.not. i_exist .or. in_parmdb%plants_plt == " null") then / else > do` | `titldum` |
| 31 | header | `if (.not. i_exist .or. in_parmdb%plants_plt == " null") then / else > do` | `header` |
| 34 | title | `if (.not. i_exist .or. in_parmdb%plants_plt == " null") then / else > do > do while (eof == 0)` | `titldum` |
| 42 | title | `if (.not. i_exist .or. in_parmdb%plants_plt == " null") then / else > do` | `titldum` |
| 44 | header | `if (.not. i_exist .or. in_parmdb%plants_plt == " null") then / else > do` | `header` |
| 48 | data | `if (.not. i_exist .or. in_parmdb%plants_plt == " null") then / else > do > do ic = 1, imax` | `pldb(ic)` |


#### Candidate read structure

- Schema status: `certified`
- Review needed: no
- Source expression(s): `in_parmdb%plants_plt`, `plants.plt`

- Procedure: `plant_parm_read`
- Reader: `plant_parm_read.f90`
- Match: source_input
- Resolved default filename(s): `plants.plt`
- Source filename expression(s): `in_parmdb%plants_plt`, `plants.plt`
- Open: line 32, file expression `in_parmdb%plants_plt`, parser value `plants.plt`, condition `if (.not. i_exist .or. in_parmdb%plants_plt == " null") then / else > do`

| Line | Role | Condition | Fields read |
| --- | --- | --- | --- |
| 33 | title | `if (.not. i_exist .or. in_parmdb%plants_plt == " null") then / else > do` | `titldum` |
| 35 | header | `if (.not. i_exist .or. in_parmdb%plants_plt == " null") then / else > do` | `header` |
| 38 | title | `if (.not. i_exist .or. in_parmdb%plants_plt == " null") then / else > do > do while (eof == 0)` | `titldum` |
| 48 | title | `if (.not. i_exist .or. in_parmdb%plants_plt == " null") then / else > do` | `titldum` |
| 50 | header | `if (.not. i_exist .or. in_parmdb%plants_plt == " null") then / else > do` | `header` |
| 55 | data | `if (.not. i_exist .or. in_parmdb%plants_plt == " null") then / else > do > do ic = 1, imax > if (bsn_cc%nam1 == 0) then` | `pldb(ic)` |
| 57 | data | `if (.not. i_exist .or. in_parmdb%plants_plt == " null") then / else > do > do ic = 1, imax > if (bsn_cc%nam1 == 0) then / else` | `pldb(ic)`, `pl_class(ic)` |

### `print.prt`

- Review needed: yes
- Reader procedures changed: no
- Read-block count changed: no
- Read conditions changed: yes
- Base flattened read order: `titldum`, `header`, `pco%nyskip`, `pco%day_start`, `pco%yrc_start`, `pco%day_end`, `pco%yrc_end`, `pco%int_day`, `header`, `pco%aa_numint`, `pco%aa_numint`, `(pco%aa_yrs(ii), ii = 1, pco%aa_numint)`, `header`, `pco%csvout`, `pco%carbout`, `pco%cdfout`, `header`, `pco%crop_yld`, `pco%mgtout`, `pco%hydcon`, `pco%fdcout`, `header`, `name`, `pco%wb_bsn`, `name`, `pco%nb_bsn`, `name`, `pco%ls_bsn`, `name`, `pco%pw_bsn`, `name`, `pco%aqu_bsn`, `name`, `pco%res_bsn`, `name`, `pco%chan_bsn`, `name`, `pco%sd_chan_bsn`, `name`, `pco%recall_bsn`, `name`, `pco%wb_reg`, `name`, `pco%nb_reg`, `name`, `pco%ls_reg`, `name`, `pco%pw_reg`, `name`, `pco%aqu_reg`, `name`, `pco%res_reg`, `name`, `pco%sd_chan_reg`, `name`, `pco%recall_reg`, `name`, `pco%water_allo`, `name`, `pco%wb_lsu`, `name`, `pco%nb_lsu`, `name`, `pco%ls_lsu`, `name`, `pco%pw_lsu`, `name`, `pco%wb_hru`, `name`, `pco%nb_hru`, `name`, `pco%ls_hru`, `name`, `pco%pw_hru`, `name`, `pco%wb_sd`, `name`, `pco%nb_sd`, `name`, `pco%ls_sd`, `name`, `pco%pw_sd`, `name`, `pco%chan`, `name`, `pco%sd_chan`, `name`, `pco%aqu`, `name`, `pco%res`, `name`, `pco%recall`, `name`, `pco%hyd`, `name`, `pco%ru`, `name`, `pco%pest`, `name`, `pco%salt_basin`, `name`, `pco%salt_hru`, `name`, `pco%salt_ru`, `name`, `pco%salt_aqu`, `name`, `pco%salt_chn`, `name`, `pco%salt_res`, `name`, `pco%salt_wet`, `name`, `pco%cs_basin`, `name`, `pco%cs_hru`, `name`, `pco%cs_ru`, `name`, `pco%cs_aqu`, `name`, `pco%cs_chn`, `name`, `pco%cs_res`, `name`, `pco%cs_wet`
- Candidate flattened read order: `titldum`, `header`, `pco%nyskip`, `pco%day_start`, `pco%yrc_start`, `pco%day_end`, `pco%yrc_end`, `pco%int_day`, `header`, `pco%aa_numint`, `pco%aa_numint`, `(pco%aa_yrs(ii), ii = 1, pco%aa_numint)`, `header`, `pco%csvout`, `pco%use_obj_labels`, `pco%cdfout`, `header`, `pco%crop_yld`, `pco%mgtout`, `pco%hydcon`, `pco%fdcout`, `header`, `name`, `pco%wb_bsn%d`, `pco%wb_bsn%m`, `pco%wb_bsn%y`, `pco%wb_bsn%a`, `name`, `pco%nb_bsn%d`, `pco%nb_bsn%m`, `pco%nb_bsn%y`, `pco%nb_bsn%a`, `name`, `pco%ls_bsn%d`, `pco%ls_bsn%m`, `pco%ls_bsn%y`, `pco%ls_bsn%a`, `name`, `pco%pw_bsn%d`, `pco%pw_bsn%m`, `pco%pw_bsn%y`, `pco%pw_bsn%a`, `name`, `pco%aqu_bsn%d`, `pco%aqu_bsn%m`, `pco%aqu_bsn%y`, `pco%aqu_bsn%a`, `name`, `pco%res_bsn%d`, `pco%res_bsn%m`, `pco%res_bsn%y`, `pco%res_bsn%a`, `name`, `pco%chan_bsn%d`, `pco%chan_bsn%m`, `pco%chan_bsn%y`, `pco%chan_bsn%a`, `name`, `pco%sd_chan_bsn%d`, `pco%sd_chan_bsn%m`, `pco%sd_chan_bsn%y`, `pco%sd_chan_bsn%a`, `name`, `pco%recall_bsn%d`, `pco%recall_bsn%m`, `pco%recall_bsn%y`, `pco%recall_bsn%a`, `name`, `pco%wb_reg%d`, `pco%wb_reg%m`, `pco%wb_reg%y`, `pco%wb_reg%a`, `name`, `pco%nb_reg%d`, `pco%nb_reg%m`, `pco%nb_reg%y`, `pco%nb_reg%a`, `name`, `pco%ls_reg%d`, `pco%ls_reg%m`, `pco%ls_reg%y`, `pco%ls_reg%a`, `name`, `pco%pw_reg%d`, `pco%pw_reg%m`, `pco%pw_reg%y`, `pco%pw_reg%a`, `name`, `pco%aqu_reg%d`, `pco%aqu_reg%m`, `pco%aqu_reg%y`, `pco%aqu_reg%a`, `name`, `pco%res_reg%d`, `pco%res_reg%m`, `pco%res_reg%y`, `pco%res_reg%a`, `name`, `pco%sd_chan_reg%d`, `pco%sd_chan_reg%m`, `pco%sd_chan_reg%y`, `pco%sd_chan_reg%a`, `name`, `pco%recall_reg%d`, `pco%recall_reg%m`, `pco%recall_reg%y`, `pco%recall_reg%a`, `name`, `pco%water_allo%d`, `pco%water_allo%m`, `pco%water_allo%y`, `pco%water_allo%a`, `name`, `pco%wb_lsu%d`, `pco%wb_lsu%m`, `pco%wb_lsu%y`, `pco%wb_lsu%a`, `name`, `pco%nb_lsu%d`, `pco%nb_lsu%m`, `pco%nb_lsu%y`, `pco%nb_lsu%a`, `name`, `pco%ls_lsu%d`, `pco%ls_lsu%m`, `pco%ls_lsu%y`, `pco%ls_lsu%a`, `name`, `pco%pw_lsu%d`, `pco%pw_lsu%m`, `pco%pw_lsu%y`, `pco%pw_lsu%a`, `name`, `pco%wb_hru%d`, `pco%wb_hru%m`, `pco%wb_hru%y`, `pco%wb_hru%a`, `name`, `pco%nb_hru%d`, `pco%nb_hru%m`, `pco%nb_hru%y`, `pco%nb_hru%a`, `name`, `pco%ls_hru%d`, `pco%ls_hru%m`, `pco%ls_hru%y`, `pco%ls_hru%a`, `name`, `pco%pw_hru%d`, `pco%pw_hru%m`, `pco%pw_hru%y`, `pco%pw_hru%a`, `name`, `pco%wb_sd%d`, `pco%wb_sd%m`, `pco%wb_sd%y`, `pco%wb_sd%a`, `name`, `pco%nb_sd%d`, `pco%nb_sd%m`, `pco%nb_sd%y`, `pco%nb_sd%a`, `name`, `pco%ls_sd%d`, `pco%ls_sd%m`, `pco%ls_sd%y`, `pco%ls_sd%a`, `name`, `pco%pw_sd%d`, `pco%pw_sd%m`, `pco%pw_sd%y`, `pco%pw_sd%a`, `name`, `pco%chan%d`, `pco%chan%m`, `pco%chan%y`, `pco%chan%a`, `name`, `pco%sd_chan%d`, `pco%sd_chan%m`, `pco%sd_chan%y`, `pco%sd_chan%a`, `name`, `pco%aqu%d`, `pco%aqu%m`, `pco%aqu%y`, `pco%aqu%a`, `name`, `pco%res%d`, `pco%res%m`, `pco%res%y`, `pco%res%a`, `name`, `pco%recall%d`, `pco%recall%m`, `pco%recall%y`, `pco%recall%a`, `name`, `pco%hyd%d`, `pco%hyd%m`, `pco%hyd%y`, `pco%hyd%a`, `name`, `pco%ru%d`, `pco%ru%m`, `pco%ru%y`, `pco%ru%a`, `name`, `pco%pest%d`, `pco%pest%m`, `pco%pest%y`, `pco%pest%a`, `name`, `pco%salt_basin%d`, `pco%salt_basin%m`, `pco%salt_basin%y`, `pco%salt_basin%a`, `name`, `pco%salt_hru%d`, `pco%salt_hru%m`, `pco%salt_hru%y`, `pco%salt_hru%a`, `name`, `pco%salt_ru%d`, `pco%salt_ru%m`, `pco%salt_ru%y`, `pco%salt_ru%a`, `name`, `pco%salt_aqu%d`, `pco%salt_aqu%m`, `pco%salt_aqu%y`, `pco%salt_aqu%a`, `name`, `pco%salt_chn%d`, `pco%salt_chn%m`, `pco%salt_chn%y`, `pco%salt_chn%a`, `name`, `pco%salt_res%d`, `pco%salt_res%m`, `pco%salt_res%y`, `pco%salt_res%a`, `name`, `pco%salt_wet%d`, `pco%salt_wet%m`, `pco%salt_wet%y`, `pco%salt_wet%a`, `name`, `pco%cs_basin%d`, `pco%cs_basin%m`, `pco%cs_basin%y`, `pco%cs_basin%a`, `name`, `pco%cs_hru%d`, `pco%cs_hru%m`, `pco%cs_hru%y`, `pco%cs_hru%a`, `name`, `pco%cs_ru%d`, `pco%cs_ru%m`, `pco%cs_ru%y`, `pco%cs_ru%a`, `name`, `pco%cs_aqu%d`, `pco%cs_aqu%m`, `pco%cs_aqu%y`, `pco%cs_aqu%a`, `name`, `pco%cs_chn%d`, `pco%cs_chn%m`, `pco%cs_chn%y`, `pco%cs_chn%a`, `name`, `pco%cs_res%d`, `pco%cs_res%m`, `pco%cs_res%y`, `pco%cs_res%a`, `name`, `pco%cs_wet%d`, `pco%cs_wet%m`, `pco%cs_wet%y`, `pco%cs_wet%a`, `name`, `name`, `pco%wb_bsn%d`, `pco%wb_bsn%m`, `pco%wb_bsn%y`, `pco%wb_bsn%a`, `name`, `pco%nb_bsn%d`, `pco%nb_bsn%m`, `pco%nb_bsn%y`, `pco%nb_bsn%a`, `name`, `pco%ls_bsn%d`, `pco%ls_bsn%m`, `pco%ls_bsn%y`, `pco%ls_bsn%a`, `name`, `pco%pw_bsn%d`, `pco%pw_bsn%m`, `pco%pw_bsn%y`, `pco%pw_bsn%a`, `name`, `pco%aqu_bsn%d`, `pco%aqu_bsn%m`, `pco%aqu_bsn%y`, `pco%aqu_bsn%a`, `name`, `pco%res_bsn%d`, `pco%res_bsn%m`, `pco%res_bsn%y`, `pco%res_bsn%a`, `name`, `pco%chan_bsn%d`, `pco%chan_bsn%m`, `pco%chan_bsn%y`, `pco%chan_bsn%a`, `name`, `pco%sd_chan_bsn%d`, `pco%sd_chan_bsn%m`, `pco%sd_chan_bsn%y`, `pco%sd_chan_bsn%a`, `name`, `pco%recall_bsn%d`, `pco%recall_bsn%m`, `pco%recall_bsn%y`, `pco%recall_bsn%a`, `name`, `pco%wb_reg%d`, `pco%wb_reg%m`, `pco%wb_reg%y`, `pco%wb_reg%a`, `name`, `pco%nb_reg%d`, `pco%nb_reg%m`, `pco%nb_reg%y`, `pco%nb_reg%a`, `name`, `pco%ls_reg%d`, `pco%ls_reg%m`, `pco%ls_reg%y`, `pco%ls_reg%a`, `name`, `pco%pw_reg%d`, `pco%pw_reg%m`, `pco%pw_reg%y`, `pco%pw_reg%a`, `name`, `pco%aqu_reg%d`, `pco%aqu_reg%m`, `pco%aqu_reg%y`, `pco%aqu_reg%a`, `name`, `pco%res_reg%d`, `pco%res_reg%m`, `pco%res_reg%y`, `pco%res_reg%a`, `name`, `pco%sd_chan_reg%d`, `pco%sd_chan_reg%m`, `pco%sd_chan_reg%y`, `pco%sd_chan_reg%a`, `name`, `pco%recall_reg%d`, `pco%recall_reg%m`, `pco%recall_reg%y`, `pco%recall_reg%a`, `name`, `pco%water_allo%d`, `pco%water_allo%m`, `pco%water_allo%y`, `pco%water_allo%a`, `name`, `pco%wb_lsu%d`, `pco%wb_lsu%m`, `pco%wb_lsu%y`, `pco%wb_lsu%a`, `name`, `pco%nb_lsu%d`, `pco%nb_lsu%m`, `pco%nb_lsu%y`, `pco%nb_lsu%a`, `name`, `pco%ls_lsu%d`, `pco%ls_lsu%m`, `pco%ls_lsu%y`, `pco%ls_lsu%a`, `name`, `pco%pw_lsu%d`, `pco%pw_lsu%m`, `pco%pw_lsu%y`, `pco%pw_lsu%a`, `name`, `pco%cb_gl_lsu%d`, `pco%cb_gl_lsu%m`, `pco%cb_gl_lsu%y`, `pco%cb_gl_lsu%a`, `name`, `pco%cb_trf_lsu%d`, `pco%cb_trf_lsu%m`, `pco%cb_trf_lsu%y`, `pco%cb_trf_lsu%a`, `name`, `pco%cb_plt_lsu%d`, `pco%cb_plt_lsu%m`, `pco%cb_plt_lsu%y`, `pco%cb_plt_lsu%a`, `name`, `pco%wb_hru%d`, `pco%wb_hru%m`, `pco%wb_hru%y`, `pco%wb_hru%a`, `name`, `pco%nb_hru%d`, `pco%nb_hru%m`, `pco%nb_hru%y`, `pco%nb_hru%a`, `name`, `pco%ls_hru%d`, `pco%ls_hru%m`, `pco%ls_hru%y`, `pco%ls_hru%a`, `name`, `pco%pw_hru%d`, `pco%pw_hru%m`, `pco%pw_hru%y`, `pco%pw_hru%a`, `name`, `pco%cb_hru%d`, `pco%cb_hru%m`, `pco%cb_hru%y`, `pco%cb_hru%a`, `name`, `pco%cb_vars_hru%d`, `pco%cb_vars_hru%m`, `pco%cb_vars_hru%y`, `pco%cb_vars_hru%a`, `name`, `pco%cb_gl_hru%d`, `pco%cb_gl_hru%m`, `pco%cb_gl_hru%y`, `pco%cb_gl_hru%a`, `name`, `pco%cb_trf_hru%d`, `pco%cb_trf_hru%m`, `pco%cb_trf_hru%y`, `pco%cb_trf_hru%a`, `name`, `pco%cb_lyr_hru%d`, `pco%cb_lyr_hru%m`, `pco%cb_lyr_hru%y`, `pco%cb_lyr_hru%a`, `name`, `pco%cb_cpool_hru%d`, `pco%cb_cpool_hru%m`, `pco%cb_cpool_hru%y`, `pco%cb_cpool_hru%a`, `name`, `pco%cb_npool_hru%d`, `pco%cb_npool_hru%m`, `pco%cb_npool_hru%y`, `pco%cb_npool_hru%a`, `name`, `pco%cb_plt_hru%d`, `pco%cb_plt_hru%m`, `pco%cb_plt_hru%y`, `pco%cb_plt_hru%a`, `name`, `pco%cb_flux_hru%d`, `pco%cb_flux_hru%m`, `pco%cb_flux_hru%y`, `pco%cb_flux_hru%a`, `name`, `pco%cb_drv_hru%d`, `pco%cb_drv_hru%m`, `pco%cb_drv_hru%y`, `pco%cb_drv_hru%a`, `name`, `pco%cb_dyn_hru%d`, `pco%cb_dyn_hru%m`, `pco%cb_dyn_hru%y`, `pco%cb_dyn_hru%a`, `name`, `pco%cb_snap_hru%d`, `pco%cb_snap_hru%m`, `pco%cb_snap_hru%y`, `pco%cb_snap_hru%a`, `name`, `pco%wb_sd%d`, `pco%wb_sd%m`, `pco%wb_sd%y`, `pco%wb_sd%a`, `name`, `pco%nb_sd%d`, `pco%nb_sd%m`, `pco%nb_sd%y`, `pco%nb_sd%a`, `name`, `pco%ls_sd%d`, `pco%ls_sd%m`, `pco%ls_sd%y`, `pco%ls_sd%a`, `name`, `pco%pw_sd%d`, `pco%pw_sd%m`, `pco%pw_sd%y`, `pco%pw_sd%a`, `name`, `pco%chan%d`, `pco%chan%m`, `pco%chan%y`, `pco%chan%a`, `name`, `pco%sd_chan%d`, `pco%sd_chan%m`, `pco%sd_chan%y`, `pco%sd_chan%a`, `name`, `pco%aqu%d`, `pco%aqu%m`, `pco%aqu%y`, `pco%aqu%a`, `name`, `pco%res%d`, `pco%res%m`, `pco%res%y`, `pco%res%a`, `name`, `pco%recall%d`, `pco%recall%m`, `pco%recall%y`, `pco%recall%a`, `name`, `pco%hyd%d`, `pco%hyd%m`, `pco%hyd%y`, `pco%hyd%a`, `name`, `pco%ru%d`, `pco%ru%m`, `pco%ru%y`, `pco%ru%a`, `name`, `pco%pest%d`, `pco%pest%m`, `pco%pest%y`, `pco%pest%a`, `name`, `pco%salt_basin%d`, `pco%salt_basin%m`, `pco%salt_basin%y`, `pco%salt_basin%a`, `name`, `pco%salt_hru%d`, `pco%salt_hru%m`, `pco%salt_hru%y`, `pco%salt_hru%a`, `name`, `pco%salt_ru%d`, `pco%salt_ru%m`, `pco%salt_ru%y`, `pco%salt_ru%a`, `name`, `pco%salt_aqu%d`, `pco%salt_aqu%m`, `pco%salt_aqu%y`, `pco%salt_aqu%a`, `name`, `pco%salt_chn%d`, `pco%salt_chn%m`, `pco%salt_chn%y`, `pco%salt_chn%a`, `name`, `pco%salt_res%d`, `pco%salt_res%m`, `pco%salt_res%y`, `pco%salt_res%a`, `name`, `pco%salt_wet%d`, `pco%salt_wet%m`, `pco%salt_wet%y`, `pco%salt_wet%a`, `name`, `pco%cs_basin%d`, `pco%cs_basin%m`, `pco%cs_basin%y`, `pco%cs_basin%a`, `name`, `pco%cs_hru%d`, `pco%cs_hru%m`, `pco%cs_hru%y`, `pco%cs_hru%a`, `name`, `pco%cs_ru%d`, `pco%cs_ru%m`, `pco%cs_ru%y`, `pco%cs_ru%a`, `name`, `pco%cs_aqu%d`, `pco%cs_aqu%m`, `pco%cs_aqu%y`, `pco%cs_aqu%a`, `name`, `pco%cs_chn%d`, `pco%cs_chn%m`, `pco%cs_chn%y`, `pco%cs_chn%a`, `name`, `pco%cs_res%d`, `pco%cs_res%m`, `pco%cs_res%y`, `pco%cs_res%a`, `name`, `pco%cs_wet%d`, `pco%cs_wet%m`, `pco%cs_wet%y`, `pco%cs_wet%a`, `name`, `pco%gwflow_wb%d`, `pco%gwflow_wb%m`, `pco%gwflow_wb%y`, `pco%gwflow_wb%a`, `name`, `pco%gwflow_flux%d`, `pco%gwflow_flux%m`, `pco%gwflow_flux%y`, `pco%gwflow_flux%a`, `name`, `pco%gwflow_heat%d`, `pco%gwflow_heat%m`, `pco%gwflow_heat%y`, `pco%gwflow_heat%a`, `name`, `pco%gwflow_solute%d`, `pco%gwflow_solute%m`, `pco%gwflow_solute%y`, `pco%gwflow_solute%a`, `name`, `pco%gwflow_obs%d`, `pco%gwflow_obs%m`, `pco%gwflow_obs%y`, `pco%gwflow_obs%a`, `name`, `pco%gwflow_pump%d`, `pco%gwflow_pump%m`, `pco%gwflow_pump%y`, `pco%gwflow_pump%a`

#### Read-order edits

- `replace` at base index 14 / candidate index 14: removed `pco%carbout`; added `pco%use_obj_labels`
- `replace` at base index 23 / candidate index 23: removed `pco%wb_bsn`; added `pco%wb_bsn%d`, `pco%wb_bsn%m`, `pco%wb_bsn%y`, `pco%wb_bsn%a`
- `replace` at base index 25 / candidate index 28: removed `pco%nb_bsn`; added `pco%nb_bsn%d`, `pco%nb_bsn%m`, `pco%nb_bsn%y`, `pco%nb_bsn%a`
- `replace` at base index 27 / candidate index 33: removed `pco%ls_bsn`; added `pco%ls_bsn%d`, `pco%ls_bsn%m`, `pco%ls_bsn%y`, `pco%ls_bsn%a`
- `replace` at base index 29 / candidate index 38: removed `pco%pw_bsn`; added `pco%pw_bsn%d`, `pco%pw_bsn%m`, `pco%pw_bsn%y`, `pco%pw_bsn%a`
- `replace` at base index 31 / candidate index 43: removed `pco%aqu_bsn`; added `pco%aqu_bsn%d`, `pco%aqu_bsn%m`, `pco%aqu_bsn%y`, `pco%aqu_bsn%a`
- `replace` at base index 33 / candidate index 48: removed `pco%res_bsn`; added `pco%res_bsn%d`, `pco%res_bsn%m`, `pco%res_bsn%y`, `pco%res_bsn%a`
- `replace` at base index 35 / candidate index 53: removed `pco%chan_bsn`; added `pco%chan_bsn%d`, `pco%chan_bsn%m`, `pco%chan_bsn%y`, `pco%chan_bsn%a`
- `replace` at base index 37 / candidate index 58: removed `pco%sd_chan_bsn`; added `pco%sd_chan_bsn%d`, `pco%sd_chan_bsn%m`, `pco%sd_chan_bsn%y`, `pco%sd_chan_bsn%a`
- `replace` at base index 39 / candidate index 63: removed `pco%recall_bsn`; added `pco%recall_bsn%d`, `pco%recall_bsn%m`, `pco%recall_bsn%y`, `pco%recall_bsn%a`
- `replace` at base index 41 / candidate index 68: removed `pco%wb_reg`; added `pco%wb_reg%d`, `pco%wb_reg%m`, `pco%wb_reg%y`, `pco%wb_reg%a`
- `replace` at base index 43 / candidate index 73: removed `pco%nb_reg`; added `pco%nb_reg%d`, `pco%nb_reg%m`, `pco%nb_reg%y`, `pco%nb_reg%a`
- `replace` at base index 45 / candidate index 78: removed `pco%ls_reg`; added `pco%ls_reg%d`, `pco%ls_reg%m`, `pco%ls_reg%y`, `pco%ls_reg%a`
- `replace` at base index 47 / candidate index 83: removed `pco%pw_reg`; added `pco%pw_reg%d`, `pco%pw_reg%m`, `pco%pw_reg%y`, `pco%pw_reg%a`
- `replace` at base index 49 / candidate index 88: removed `pco%aqu_reg`; added `pco%aqu_reg%d`, `pco%aqu_reg%m`, `pco%aqu_reg%y`, `pco%aqu_reg%a`
- `replace` at base index 51 / candidate index 93: removed `pco%res_reg`; added `pco%res_reg%d`, `pco%res_reg%m`, `pco%res_reg%y`, `pco%res_reg%a`
- `replace` at base index 53 / candidate index 98: removed `pco%sd_chan_reg`; added `pco%sd_chan_reg%d`, `pco%sd_chan_reg%m`, `pco%sd_chan_reg%y`, `pco%sd_chan_reg%a`
- `replace` at base index 55 / candidate index 103: removed `pco%recall_reg`; added `pco%recall_reg%d`, `pco%recall_reg%m`, `pco%recall_reg%y`, `pco%recall_reg%a`
- `replace` at base index 57 / candidate index 108: removed `pco%water_allo`; added `pco%water_allo%d`, `pco%water_allo%m`, `pco%water_allo%y`, `pco%water_allo%a`
- `replace` at base index 59 / candidate index 113: removed `pco%wb_lsu`; added `pco%wb_lsu%d`, `pco%wb_lsu%m`, `pco%wb_lsu%y`, `pco%wb_lsu%a`
- `replace` at base index 61 / candidate index 118: removed `pco%nb_lsu`; added `pco%nb_lsu%d`, `pco%nb_lsu%m`, `pco%nb_lsu%y`, `pco%nb_lsu%a`
- `replace` at base index 63 / candidate index 123: removed `pco%ls_lsu`; added `pco%ls_lsu%d`, `pco%ls_lsu%m`, `pco%ls_lsu%y`, `pco%ls_lsu%a`
- `replace` at base index 65 / candidate index 128: removed `pco%pw_lsu`; added `pco%pw_lsu%d`, `pco%pw_lsu%m`, `pco%pw_lsu%y`, `pco%pw_lsu%a`
- `replace` at base index 67 / candidate index 133: removed `pco%wb_hru`; added `pco%wb_hru%d`, `pco%wb_hru%m`, `pco%wb_hru%y`, `pco%wb_hru%a`
- `replace` at base index 69 / candidate index 138: removed `pco%nb_hru`; added `pco%nb_hru%d`, `pco%nb_hru%m`, `pco%nb_hru%y`, `pco%nb_hru%a`
- `replace` at base index 71 / candidate index 143: removed `pco%ls_hru`; added `pco%ls_hru%d`, `pco%ls_hru%m`, `pco%ls_hru%y`, `pco%ls_hru%a`
- `replace` at base index 73 / candidate index 148: removed `pco%pw_hru`; added `pco%pw_hru%d`, `pco%pw_hru%m`, `pco%pw_hru%y`, `pco%pw_hru%a`
- `replace` at base index 75 / candidate index 153: removed `pco%wb_sd`; added `pco%wb_sd%d`, `pco%wb_sd%m`, `pco%wb_sd%y`, `pco%wb_sd%a`
- `replace` at base index 77 / candidate index 158: removed `pco%nb_sd`; added `pco%nb_sd%d`, `pco%nb_sd%m`, `pco%nb_sd%y`, `pco%nb_sd%a`
- `replace` at base index 79 / candidate index 163: removed `pco%ls_sd`; added `pco%ls_sd%d`, `pco%ls_sd%m`, `pco%ls_sd%y`, `pco%ls_sd%a`
- `replace` at base index 81 / candidate index 168: removed `pco%pw_sd`; added `pco%pw_sd%d`, `pco%pw_sd%m`, `pco%pw_sd%y`, `pco%pw_sd%a`
- `replace` at base index 83 / candidate index 173: removed `pco%chan`; added `pco%chan%d`, `pco%chan%m`, `pco%chan%y`, `pco%chan%a`
- `replace` at base index 85 / candidate index 178: removed `pco%sd_chan`; added `pco%sd_chan%d`, `pco%sd_chan%m`, `pco%sd_chan%y`, `pco%sd_chan%a`
- `replace` at base index 87 / candidate index 183: removed `pco%aqu`; added `pco%aqu%d`, `pco%aqu%m`, `pco%aqu%y`, `pco%aqu%a`
- `replace` at base index 89 / candidate index 188: removed `pco%res`; added `pco%res%d`, `pco%res%m`, `pco%res%y`, `pco%res%a`
- `replace` at base index 91 / candidate index 193: removed `pco%recall`; added `pco%recall%d`, `pco%recall%m`, `pco%recall%y`, `pco%recall%a`
- `replace` at base index 93 / candidate index 198: removed `pco%hyd`; added `pco%hyd%d`, `pco%hyd%m`, `pco%hyd%y`, `pco%hyd%a`
- `replace` at base index 95 / candidate index 203: removed `pco%ru`; added `pco%ru%d`, `pco%ru%m`, `pco%ru%y`, `pco%ru%a`
- `replace` at base index 97 / candidate index 208: removed `pco%pest`; added `pco%pest%d`, `pco%pest%m`, `pco%pest%y`, `pco%pest%a`
- `replace` at base index 99 / candidate index 213: removed `pco%salt_basin`; added `pco%salt_basin%d`, `pco%salt_basin%m`, `pco%salt_basin%y`, `pco%salt_basin%a`
- `replace` at base index 101 / candidate index 218: removed `pco%salt_hru`; added `pco%salt_hru%d`, `pco%salt_hru%m`, `pco%salt_hru%y`, `pco%salt_hru%a`
- `replace` at base index 103 / candidate index 223: removed `pco%salt_ru`; added `pco%salt_ru%d`, `pco%salt_ru%m`, `pco%salt_ru%y`, `pco%salt_ru%a`
- `replace` at base index 105 / candidate index 228: removed `pco%salt_aqu`; added `pco%salt_aqu%d`, `pco%salt_aqu%m`, `pco%salt_aqu%y`, `pco%salt_aqu%a`
- `replace` at base index 107 / candidate index 233: removed `pco%salt_chn`; added `pco%salt_chn%d`, `pco%salt_chn%m`, `pco%salt_chn%y`, `pco%salt_chn%a`
- `replace` at base index 109 / candidate index 238: removed `pco%salt_res`; added `pco%salt_res%d`, `pco%salt_res%m`, `pco%salt_res%y`, `pco%salt_res%a`
- `replace` at base index 111 / candidate index 243: removed `pco%salt_wet`; added `pco%salt_wet%d`, `pco%salt_wet%m`, `pco%salt_wet%y`, `pco%salt_wet%a`
- `replace` at base index 113 / candidate index 248: removed `pco%cs_basin`; added `pco%cs_basin%d`, `pco%cs_basin%m`, `pco%cs_basin%y`, `pco%cs_basin%a`
- `replace` at base index 115 / candidate index 253: removed `pco%cs_hru`; added `pco%cs_hru%d`, `pco%cs_hru%m`, `pco%cs_hru%y`, `pco%cs_hru%a`
- `replace` at base index 117 / candidate index 258: removed `pco%cs_ru`; added `pco%cs_ru%d`, `pco%cs_ru%m`, `pco%cs_ru%y`, `pco%cs_ru%a`
- `replace` at base index 119 / candidate index 263: removed `pco%cs_aqu`; added `pco%cs_aqu%d`, `pco%cs_aqu%m`, `pco%cs_aqu%y`, `pco%cs_aqu%a`
- `replace` at base index 121 / candidate index 268: removed `pco%cs_chn`; added `pco%cs_chn%d`, `pco%cs_chn%m`, `pco%cs_chn%y`, `pco%cs_chn%a`
- `replace` at base index 123 / candidate index 273: removed `pco%cs_res`; added `pco%cs_res%d`, `pco%cs_res%m`, `pco%cs_res%y`, `pco%cs_res%a`
- `replace` at base index 125 / candidate index 278: removed `pco%cs_wet`; added `pco%cs_wet%d`, `pco%cs_wet%m`, `pco%cs_wet%y`, `pco%cs_wet%a`, `name`, `name`, `pco%wb_bsn%d`, `pco%wb_bsn%m`, `pco%wb_bsn%y`, `pco%wb_bsn%a`, `name`, `pco%nb_bsn%d`, `pco%nb_bsn%m`, `pco%nb_bsn%y`, `pco%nb_bsn%a`, `name`, `pco%ls_bsn%d`, `pco%ls_bsn%m`, `pco%ls_bsn%y`, `pco%ls_bsn%a`, `name`, `pco%pw_bsn%d`, `pco%pw_bsn%m`, `pco%pw_bsn%y`, `pco%pw_bsn%a`, `name`, `pco%aqu_bsn%d`, `pco%aqu_bsn%m`, `pco%aqu_bsn%y`, `pco%aqu_bsn%a`, `name`, `pco%res_bsn%d`, `pco%res_bsn%m`, `pco%res_bsn%y`, `pco%res_bsn%a`, `name`, `pco%chan_bsn%d`, `pco%chan_bsn%m`, `pco%chan_bsn%y`, `pco%chan_bsn%a`, `name`, `pco%sd_chan_bsn%d`, `pco%sd_chan_bsn%m`, `pco%sd_chan_bsn%y`, `pco%sd_chan_bsn%a`, `name`, `pco%recall_bsn%d`, `pco%recall_bsn%m`, `pco%recall_bsn%y`, `pco%recall_bsn%a`, `name`, `pco%wb_reg%d`, `pco%wb_reg%m`, `pco%wb_reg%y`, `pco%wb_reg%a`, `name`, `pco%nb_reg%d`, `pco%nb_reg%m`, `pco%nb_reg%y`, `pco%nb_reg%a`, `name`, `pco%ls_reg%d`, `pco%ls_reg%m`, `pco%ls_reg%y`, `pco%ls_reg%a`, `name`, `pco%pw_reg%d`, `pco%pw_reg%m`, `pco%pw_reg%y`, `pco%pw_reg%a`, `name`, `pco%aqu_reg%d`, `pco%aqu_reg%m`, `pco%aqu_reg%y`, `pco%aqu_reg%a`, `name`, `pco%res_reg%d`, `pco%res_reg%m`, `pco%res_reg%y`, `pco%res_reg%a`, `name`, `pco%sd_chan_reg%d`, `pco%sd_chan_reg%m`, `pco%sd_chan_reg%y`, `pco%sd_chan_reg%a`, `name`, `pco%recall_reg%d`, `pco%recall_reg%m`, `pco%recall_reg%y`, `pco%recall_reg%a`, `name`, `pco%water_allo%d`, `pco%water_allo%m`, `pco%water_allo%y`, `pco%water_allo%a`, `name`, `pco%wb_lsu%d`, `pco%wb_lsu%m`, `pco%wb_lsu%y`, `pco%wb_lsu%a`, `name`, `pco%nb_lsu%d`, `pco%nb_lsu%m`, `pco%nb_lsu%y`, `pco%nb_lsu%a`, `name`, `pco%ls_lsu%d`, `pco%ls_lsu%m`, `pco%ls_lsu%y`, `pco%ls_lsu%a`, `name`, `pco%pw_lsu%d`, `pco%pw_lsu%m`, `pco%pw_lsu%y`, `pco%pw_lsu%a`, `name`, `pco%cb_gl_lsu%d`, `pco%cb_gl_lsu%m`, `pco%cb_gl_lsu%y`, `pco%cb_gl_lsu%a`, `name`, `pco%cb_trf_lsu%d`, `pco%cb_trf_lsu%m`, `pco%cb_trf_lsu%y`, `pco%cb_trf_lsu%a`, `name`, `pco%cb_plt_lsu%d`, `pco%cb_plt_lsu%m`, `pco%cb_plt_lsu%y`, `pco%cb_plt_lsu%a`, `name`, `pco%wb_hru%d`, `pco%wb_hru%m`, `pco%wb_hru%y`, `pco%wb_hru%a`, `name`, `pco%nb_hru%d`, `pco%nb_hru%m`, `pco%nb_hru%y`, `pco%nb_hru%a`, `name`, `pco%ls_hru%d`, `pco%ls_hru%m`, `pco%ls_hru%y`, `pco%ls_hru%a`, `name`, `pco%pw_hru%d`, `pco%pw_hru%m`, `pco%pw_hru%y`, `pco%pw_hru%a`, `name`, `pco%cb_hru%d`, `pco%cb_hru%m`, `pco%cb_hru%y`, `pco%cb_hru%a`, `name`, `pco%cb_vars_hru%d`, `pco%cb_vars_hru%m`, `pco%cb_vars_hru%y`, `pco%cb_vars_hru%a`, `name`, `pco%cb_gl_hru%d`, `pco%cb_gl_hru%m`, `pco%cb_gl_hru%y`, `pco%cb_gl_hru%a`, `name`, `pco%cb_trf_hru%d`, `pco%cb_trf_hru%m`, `pco%cb_trf_hru%y`, `pco%cb_trf_hru%a`, `name`, `pco%cb_lyr_hru%d`, `pco%cb_lyr_hru%m`, `pco%cb_lyr_hru%y`, `pco%cb_lyr_hru%a`, `name`, `pco%cb_cpool_hru%d`, `pco%cb_cpool_hru%m`, `pco%cb_cpool_hru%y`, `pco%cb_cpool_hru%a`, `name`, `pco%cb_npool_hru%d`, `pco%cb_npool_hru%m`, `pco%cb_npool_hru%y`, `pco%cb_npool_hru%a`, `name`, `pco%cb_plt_hru%d`, `pco%cb_plt_hru%m`, `pco%cb_plt_hru%y`, `pco%cb_plt_hru%a`, `name`, `pco%cb_flux_hru%d`, `pco%cb_flux_hru%m`, `pco%cb_flux_hru%y`, `pco%cb_flux_hru%a`, `name`, `pco%cb_drv_hru%d`, `pco%cb_drv_hru%m`, `pco%cb_drv_hru%y`, `pco%cb_drv_hru%a`, `name`, `pco%cb_dyn_hru%d`, `pco%cb_dyn_hru%m`, `pco%cb_dyn_hru%y`, `pco%cb_dyn_hru%a`, `name`, `pco%cb_snap_hru%d`, `pco%cb_snap_hru%m`, `pco%cb_snap_hru%y`, `pco%cb_snap_hru%a`, `name`, `pco%wb_sd%d`, `pco%wb_sd%m`, `pco%wb_sd%y`, `pco%wb_sd%a`, `name`, `pco%nb_sd%d`, `pco%nb_sd%m`, `pco%nb_sd%y`, `pco%nb_sd%a`, `name`, `pco%ls_sd%d`, `pco%ls_sd%m`, `pco%ls_sd%y`, `pco%ls_sd%a`, `name`, `pco%pw_sd%d`, `pco%pw_sd%m`, `pco%pw_sd%y`, `pco%pw_sd%a`, `name`, `pco%chan%d`, `pco%chan%m`, `pco%chan%y`, `pco%chan%a`, `name`, `pco%sd_chan%d`, `pco%sd_chan%m`, `pco%sd_chan%y`, `pco%sd_chan%a`, `name`, `pco%aqu%d`, `pco%aqu%m`, `pco%aqu%y`, `pco%aqu%a`, `name`, `pco%res%d`, `pco%res%m`, `pco%res%y`, `pco%res%a`, `name`, `pco%recall%d`, `pco%recall%m`, `pco%recall%y`, `pco%recall%a`, `name`, `pco%hyd%d`, `pco%hyd%m`, `pco%hyd%y`, `pco%hyd%a`, `name`, `pco%ru%d`, `pco%ru%m`, `pco%ru%y`, `pco%ru%a`, `name`, `pco%pest%d`, `pco%pest%m`, `pco%pest%y`, `pco%pest%a`, `name`, `pco%salt_basin%d`, `pco%salt_basin%m`, `pco%salt_basin%y`, `pco%salt_basin%a`, `name`, `pco%salt_hru%d`, `pco%salt_hru%m`, `pco%salt_hru%y`, `pco%salt_hru%a`, `name`, `pco%salt_ru%d`, `pco%salt_ru%m`, `pco%salt_ru%y`, `pco%salt_ru%a`, `name`, `pco%salt_aqu%d`, `pco%salt_aqu%m`, `pco%salt_aqu%y`, `pco%salt_aqu%a`, `name`, `pco%salt_chn%d`, `pco%salt_chn%m`, `pco%salt_chn%y`, `pco%salt_chn%a`, `name`, `pco%salt_res%d`, `pco%salt_res%m`, `pco%salt_res%y`, `pco%salt_res%a`, `name`, `pco%salt_wet%d`, `pco%salt_wet%m`, `pco%salt_wet%y`, `pco%salt_wet%a`, `name`, `pco%cs_basin%d`, `pco%cs_basin%m`, `pco%cs_basin%y`, `pco%cs_basin%a`, `name`, `pco%cs_hru%d`, `pco%cs_hru%m`, `pco%cs_hru%y`, `pco%cs_hru%a`, `name`, `pco%cs_ru%d`, `pco%cs_ru%m`, `pco%cs_ru%y`, `pco%cs_ru%a`, `name`, `pco%cs_aqu%d`, `pco%cs_aqu%m`, `pco%cs_aqu%y`, `pco%cs_aqu%a`, `name`, `pco%cs_chn%d`, `pco%cs_chn%m`, `pco%cs_chn%y`, `pco%cs_chn%a`, `name`, `pco%cs_res%d`, `pco%cs_res%m`, `pco%cs_res%y`, `pco%cs_res%a`, `name`, `pco%cs_wet%d`, `pco%cs_wet%m`, `pco%cs_wet%y`, `pco%cs_wet%a`, `name`, `pco%gwflow_wb%d`, `pco%gwflow_wb%m`, `pco%gwflow_wb%y`, `pco%gwflow_wb%a`, `name`, `pco%gwflow_flux%d`, `pco%gwflow_flux%m`, `pco%gwflow_flux%y`, `pco%gwflow_flux%a`, `name`, `pco%gwflow_heat%d`, `pco%gwflow_heat%m`, `pco%gwflow_heat%y`, `pco%gwflow_heat%a`, `name`, `pco%gwflow_solute%d`, `pco%gwflow_solute%m`, `pco%gwflow_solute%y`, `pco%gwflow_solute%a`, `name`, `pco%gwflow_obs%d`, `pco%gwflow_obs%m`, `pco%gwflow_obs%y`, `pco%gwflow_obs%a`, `name`, `pco%gwflow_pump%d`, `pco%gwflow_pump%m`, `pco%gwflow_pump%y`, `pco%gwflow_pump%a`

#### Base read structure

- Schema status: `certified`
- Review needed: no
- Source expression(s): `in_sim%prt`, `print.prt`

- Procedure: `basin_print_codes_read`
- Reader: `basin_print_codes_read.f90`
- Match: source_input
- Resolved default filename(s): `print.prt`
- Source filename expression(s): `in_sim%prt`, `print.prt`
- Open: line 22, file expression `in_sim%prt`, parser value `print.prt`, condition `if (i_exist .or. in_sim%prt /= "null") then > do`

| Line | Role | Condition | Fields read |
| --- | --- | --- | --- |
| 23 | title | `if (i_exist .or. in_sim%prt /= "null") then > do` | `titldum` |
| 25 | header | `if (i_exist .or. in_sim%prt /= "null") then > do` | `header` |
| 27 | data | `if (i_exist .or. in_sim%prt /= "null") then > do` | `pco%nyskip`, `pco%day_start`, `pco%yrc_start`, `pco%day_end`, `pco%yrc_end`, `pco%int_day` |
| 29 | header | `if (i_exist .or. in_sim%prt /= "null") then > do` | `header` |
| 31 | data | `if (i_exist .or. in_sim%prt /= "null") then > do` | `pco%aa_numint` |
| 35 | data | `if (i_exist .or. in_sim%prt /= "null") then > do > if (pco%aa_numint > 0) then` | `pco%aa_numint`, `(pco%aa_yrs(ii), ii = 1, pco%aa_numint)` |
| 41 | header | `if (i_exist .or. in_sim%prt /= "null") then > do` | `header` |
| 43 | data | `if (i_exist .or. in_sim%prt /= "null") then > do` | `pco%csvout`, `pco%carbout`, `pco%cdfout` |
| 47 | header | `if (i_exist .or. in_sim%prt /= "null") then > do` | `header` |
| 49 | data | `if (i_exist .or. in_sim%prt /= "null") then > do` | `pco%crop_yld`, `pco%mgtout`, `pco%hydcon`, `pco%fdcout` |
| 54 | header | `if (i_exist .or. in_sim%prt /= "null") then > do` | `header` |
| 56 | data | `if (i_exist .or. in_sim%prt /= "null") then > do` | `name`, `pco%wb_bsn` |
| 58 | data | `if (i_exist .or. in_sim%prt /= "null") then > do` | `name`, `pco%nb_bsn` |
| 60 | data | `if (i_exist .or. in_sim%prt /= "null") then > do` | `name`, `pco%ls_bsn` |
| 62 | data | `if (i_exist .or. in_sim%prt /= "null") then > do` | `name`, `pco%pw_bsn` |
| 64 | data | `if (i_exist .or. in_sim%prt /= "null") then > do` | `name`, `pco%aqu_bsn` |
| 66 | data | `if (i_exist .or. in_sim%prt /= "null") then > do` | `name`, `pco%res_bsn` |
| 68 | data | `if (i_exist .or. in_sim%prt /= "null") then > do` | `name`, `pco%chan_bsn` |
| 70 | data | `if (i_exist .or. in_sim%prt /= "null") then > do` | `name`, `pco%sd_chan_bsn` |
| 72 | data | `if (i_exist .or. in_sim%prt /= "null") then > do` | `name`, `pco%recall_bsn` |
| 75 | data | `if (i_exist .or. in_sim%prt /= "null") then > do` | `name`, `pco%wb_reg` |
| 77 | data | `if (i_exist .or. in_sim%prt /= "null") then > do` | `name`, `pco%nb_reg` |
| 79 | data | `if (i_exist .or. in_sim%prt /= "null") then > do` | `name`, `pco%ls_reg` |
| 81 | data | `if (i_exist .or. in_sim%prt /= "null") then > do` | `name`, `pco%pw_reg` |
| 83 | data | `if (i_exist .or. in_sim%prt /= "null") then > do` | `name`, `pco%aqu_reg` |
| 85 | data | `if (i_exist .or. in_sim%prt /= "null") then > do` | `name`, `pco%res_reg` |
| 87 | data | `if (i_exist .or. in_sim%prt /= "null") then > do` | `name`, `pco%sd_chan_reg` |
| 89 | data | `if (i_exist .or. in_sim%prt /= "null") then > do` | `name`, `pco%recall_reg` |
| 91 | data | `if (i_exist .or. in_sim%prt /= "null") then > do` | `name`, `pco%water_allo` |
| 94 | data | `if (i_exist .or. in_sim%prt /= "null") then > do` | `name`, `pco%wb_lsu` |
| 96 | data | `if (i_exist .or. in_sim%prt /= "null") then > do` | `name`, `pco%nb_lsu` |
| 98 | data | `if (i_exist .or. in_sim%prt /= "null") then > do` | `name`, `pco%ls_lsu` |
| 100 | data | `if (i_exist .or. in_sim%prt /= "null") then > do` | `name`, `pco%pw_lsu` |
| 103 | data | `if (i_exist .or. in_sim%prt /= "null") then > do` | `name`, `pco%wb_hru` |
| 105 | data | `if (i_exist .or. in_sim%prt /= "null") then > do` | `name`, `pco%nb_hru` |
| 107 | data | `if (i_exist .or. in_sim%prt /= "null") then > do` | `name`, `pco%ls_hru` |
| 109 | data | `if (i_exist .or. in_sim%prt /= "null") then > do` | `name`, `pco%pw_hru` |
| 113 | data | `if (i_exist .or. in_sim%prt /= "null") then > do` | `name`, `pco%wb_sd` |
| 115 | data | `if (i_exist .or. in_sim%prt /= "null") then > do` | `name`, `pco%nb_sd` |
| 117 | data | `if (i_exist .or. in_sim%prt /= "null") then > do` | `name`, `pco%ls_sd` |
| 119 | data | `if (i_exist .or. in_sim%prt /= "null") then > do` | `name`, `pco%pw_sd` |
| 122 | data | `if (i_exist .or. in_sim%prt /= "null") then > do` | `name`, `pco%chan` |
| 125 | data | `if (i_exist .or. in_sim%prt /= "null") then > do` | `name`, `pco%sd_chan` |
| 128 | data | `if (i_exist .or. in_sim%prt /= "null") then > do` | `name`, `pco%aqu` |
| 131 | data | `if (i_exist .or. in_sim%prt /= "null") then > do` | `name`, `pco%res` |
| 134 | data | `if (i_exist .or. in_sim%prt /= "null") then > do` | `name`, `pco%recall` |
| 137 | data | `if (i_exist .or. in_sim%prt /= "null") then > do` | `name`, `pco%hyd` |
| 140 | data | `if (i_exist .or. in_sim%prt /= "null") then > do` | `name`, `pco%ru` |
| 143 | data | `if (i_exist .or. in_sim%prt /= "null") then > do` | `name`, `pco%pest` |
| 146 | data | `if (i_exist .or. in_sim%prt /= "null") then > do` | `name`, `pco%salt_basin` |
| 148 | data | `if (i_exist .or. in_sim%prt /= "null") then > do` | `name`, `pco%salt_hru` |
| 150 | data | `if (i_exist .or. in_sim%prt /= "null") then > do` | `name`, `pco%salt_ru` |
| 152 | data | `if (i_exist .or. in_sim%prt /= "null") then > do` | `name`, `pco%salt_aqu` |
| 154 | data | `if (i_exist .or. in_sim%prt /= "null") then > do` | `name`, `pco%salt_chn` |
| 156 | data | `if (i_exist .or. in_sim%prt /= "null") then > do` | `name`, `pco%salt_res` |
| 158 | data | `if (i_exist .or. in_sim%prt /= "null") then > do` | `name`, `pco%salt_wet` |
| 161 | data | `if (i_exist .or. in_sim%prt /= "null") then > do` | `name`, `pco%cs_basin` |
| 163 | data | `if (i_exist .or. in_sim%prt /= "null") then > do` | `name`, `pco%cs_hru` |
| 165 | data | `if (i_exist .or. in_sim%prt /= "null") then > do` | `name`, `pco%cs_ru` |
| 167 | data | `if (i_exist .or. in_sim%prt /= "null") then > do` | `name`, `pco%cs_aqu` |
| 169 | data | `if (i_exist .or. in_sim%prt /= "null") then > do` | `name`, `pco%cs_chn` |
| 171 | data | `if (i_exist .or. in_sim%prt /= "null") then > do` | `name`, `pco%cs_res` |
| 173 | data | `if (i_exist .or. in_sim%prt /= "null") then > do` | `name`, `pco%cs_wet` |


#### Candidate read structure

- Schema status: `certified`
- Review needed: no
- Source expression(s): `in_sim%prt`, `print.prt`

- Procedure: `basin_print_codes_read`
- Reader: `basin_print_codes_read.f90`
- Match: source_input
- Resolved default filename(s): `print.prt`
- Source filename expression(s): `in_sim%prt`, `print.prt`
- Open: line 23, file expression `in_sim%prt`, parser value `print.prt`, condition `if (i_exist .or. in_sim%prt /= "null") then > do`

| Line | Role | Condition | Fields read |
| --- | --- | --- | --- |
| 24 | title | `if (i_exist .or. in_sim%prt /= "null") then > do` | `titldum` |
| 26 | header | `if (i_exist .or. in_sim%prt /= "null") then > do` | `header` |
| 28 | data | `if (i_exist .or. in_sim%prt /= "null") then > do` | `pco%nyskip`, `pco%day_start`, `pco%yrc_start`, `pco%day_end`, `pco%yrc_end`, `pco%int_day` |
| 30 | header | `if (i_exist .or. in_sim%prt /= "null") then > do` | `header` |
| 32 | data | `if (i_exist .or. in_sim%prt /= "null") then > do` | `pco%aa_numint` |
| 36 | data | `if (i_exist .or. in_sim%prt /= "null") then > do > if (pco%aa_numint > 0) then` | `pco%aa_numint`, `(pco%aa_yrs(ii), ii = 1, pco%aa_numint)` |
| 42 | header | `if (i_exist .or. in_sim%prt /= "null") then > do` | `header` |
| 44 | data | `if (i_exist .or. in_sim%prt /= "null") then > do` | `pco%csvout`, `pco%use_obj_labels`, `pco%cdfout` |
| 48 | header | `if (i_exist .or. in_sim%prt /= "null") then > do` | `header` |
| 50 | data | `if (i_exist .or. in_sim%prt /= "null") then > do` | `pco%crop_yld`, `pco%mgtout`, `pco%hydcon`, `pco%fdcout` |
| 55 | header | `if (i_exist .or. in_sim%prt /= "null") then > do` | `header` |
| 58 | data | `if (i_exist .or. in_sim%prt /= "null") then > do > if (pco%use_obj_labels == "n") then` | `name`, `pco%wb_bsn%d`, `pco%wb_bsn%m`, `pco%wb_bsn%y`, `pco%wb_bsn%a` |
| 60 | data | `if (i_exist .or. in_sim%prt /= "null") then > do > if (pco%use_obj_labels == "n") then` | `name`, `pco%nb_bsn%d`, `pco%nb_bsn%m`, `pco%nb_bsn%y`, `pco%nb_bsn%a` |
| 62 | data | `if (i_exist .or. in_sim%prt /= "null") then > do > if (pco%use_obj_labels == "n") then` | `name`, `pco%ls_bsn%d`, `pco%ls_bsn%m`, `pco%ls_bsn%y`, `pco%ls_bsn%a` |
| 64 | data | `if (i_exist .or. in_sim%prt /= "null") then > do > if (pco%use_obj_labels == "n") then` | `name`, `pco%pw_bsn%d`, `pco%pw_bsn%m`, `pco%pw_bsn%y`, `pco%pw_bsn%a` |
| 66 | data | `if (i_exist .or. in_sim%prt /= "null") then > do > if (pco%use_obj_labels == "n") then` | `name`, `pco%aqu_bsn%d`, `pco%aqu_bsn%m`, `pco%aqu_bsn%y`, `pco%aqu_bsn%a` |
| 68 | data | `if (i_exist .or. in_sim%prt /= "null") then > do > if (pco%use_obj_labels == "n") then` | `name`, `pco%res_bsn%d`, `pco%res_bsn%m`, `pco%res_bsn%y`, `pco%res_bsn%a` |
| 70 | data | `if (i_exist .or. in_sim%prt /= "null") then > do > if (pco%use_obj_labels == "n") then` | `name`, `pco%chan_bsn%d`, `pco%chan_bsn%m`, `pco%chan_bsn%y`, `pco%chan_bsn%a` |
| 72 | data | `if (i_exist .or. in_sim%prt /= "null") then > do > if (pco%use_obj_labels == "n") then` | `name`, `pco%sd_chan_bsn%d`, `pco%sd_chan_bsn%m`, `pco%sd_chan_bsn%y`, `pco%sd_chan_bsn%a` |
| 74 | data | `if (i_exist .or. in_sim%prt /= "null") then > do > if (pco%use_obj_labels == "n") then` | `name`, `pco%recall_bsn%d`, `pco%recall_bsn%m`, `pco%recall_bsn%y`, `pco%recall_bsn%a` |
| 77 | data | `if (i_exist .or. in_sim%prt /= "null") then > do > if (pco%use_obj_labels == "n") then` | `name`, `pco%wb_reg%d`, `pco%wb_reg%m`, `pco%wb_reg%y`, `pco%wb_reg%a` |
| 79 | data | `if (i_exist .or. in_sim%prt /= "null") then > do > if (pco%use_obj_labels == "n") then` | `name`, `pco%nb_reg%d`, `pco%nb_reg%m`, `pco%nb_reg%y`, `pco%nb_reg%a` |
| 81 | data | `if (i_exist .or. in_sim%prt /= "null") then > do > if (pco%use_obj_labels == "n") then` | `name`, `pco%ls_reg%d`, `pco%ls_reg%m`, `pco%ls_reg%y`, `pco%ls_reg%a` |
| 83 | data | `if (i_exist .or. in_sim%prt /= "null") then > do > if (pco%use_obj_labels == "n") then` | `name`, `pco%pw_reg%d`, `pco%pw_reg%m`, `pco%pw_reg%y`, `pco%pw_reg%a` |
| 85 | data | `if (i_exist .or. in_sim%prt /= "null") then > do > if (pco%use_obj_labels == "n") then` | `name`, `pco%aqu_reg%d`, `pco%aqu_reg%m`, `pco%aqu_reg%y`, `pco%aqu_reg%a` |
| 87 | data | `if (i_exist .or. in_sim%prt /= "null") then > do > if (pco%use_obj_labels == "n") then` | `name`, `pco%res_reg%d`, `pco%res_reg%m`, `pco%res_reg%y`, `pco%res_reg%a` |
| 89 | data | `if (i_exist .or. in_sim%prt /= "null") then > do > if (pco%use_obj_labels == "n") then` | `name`, `pco%sd_chan_reg%d`, `pco%sd_chan_reg%m`, `pco%sd_chan_reg%y`, `pco%sd_chan_reg%a` |
| 91 | data | `if (i_exist .or. in_sim%prt /= "null") then > do > if (pco%use_obj_labels == "n") then` | `name`, `pco%recall_reg%d`, `pco%recall_reg%m`, `pco%recall_reg%y`, `pco%recall_reg%a` |
| 93 | data | `if (i_exist .or. in_sim%prt /= "null") then > do > if (pco%use_obj_labels == "n") then` | `name`, `pco%water_allo%d`, `pco%water_allo%m`, `pco%water_allo%y`, `pco%water_allo%a` |
| 96 | data | `if (i_exist .or. in_sim%prt /= "null") then > do > if (pco%use_obj_labels == "n") then` | `name`, `pco%wb_lsu%d`, `pco%wb_lsu%m`, `pco%wb_lsu%y`, `pco%wb_lsu%a` |
| 98 | data | `if (i_exist .or. in_sim%prt /= "null") then > do > if (pco%use_obj_labels == "n") then` | `name`, `pco%nb_lsu%d`, `pco%nb_lsu%m`, `pco%nb_lsu%y`, `pco%nb_lsu%a` |
| 100 | data | `if (i_exist .or. in_sim%prt /= "null") then > do > if (pco%use_obj_labels == "n") then` | `name`, `pco%ls_lsu%d`, `pco%ls_lsu%m`, `pco%ls_lsu%y`, `pco%ls_lsu%a` |
| 102 | data | `if (i_exist .or. in_sim%prt /= "null") then > do > if (pco%use_obj_labels == "n") then` | `name`, `pco%pw_lsu%d`, `pco%pw_lsu%m`, `pco%pw_lsu%y`, `pco%pw_lsu%a` |
| 105 | data | `if (i_exist .or. in_sim%prt /= "null") then > do > if (pco%use_obj_labels == "n") then` | `name`, `pco%wb_hru%d`, `pco%wb_hru%m`, `pco%wb_hru%y`, `pco%wb_hru%a` |
| 107 | data | `if (i_exist .or. in_sim%prt /= "null") then > do > if (pco%use_obj_labels == "n") then` | `name`, `pco%nb_hru%d`, `pco%nb_hru%m`, `pco%nb_hru%y`, `pco%nb_hru%a` |
| 109 | data | `if (i_exist .or. in_sim%prt /= "null") then > do > if (pco%use_obj_labels == "n") then` | `name`, `pco%ls_hru%d`, `pco%ls_hru%m`, `pco%ls_hru%y`, `pco%ls_hru%a` |
| 111 | data | `if (i_exist .or. in_sim%prt /= "null") then > do > if (pco%use_obj_labels == "n") then` | `name`, `pco%pw_hru%d`, `pco%pw_hru%m`, `pco%pw_hru%y`, `pco%pw_hru%a` |
| 115 | data | `if (i_exist .or. in_sim%prt /= "null") then > do > if (pco%use_obj_labels == "n") then` | `name`, `pco%wb_sd%d`, `pco%wb_sd%m`, `pco%wb_sd%y`, `pco%wb_sd%a` |
| 117 | data | `if (i_exist .or. in_sim%prt /= "null") then > do > if (pco%use_obj_labels == "n") then` | `name`, `pco%nb_sd%d`, `pco%nb_sd%m`, `pco%nb_sd%y`, `pco%nb_sd%a` |
| 119 | data | `if (i_exist .or. in_sim%prt /= "null") then > do > if (pco%use_obj_labels == "n") then` | `name`, `pco%ls_sd%d`, `pco%ls_sd%m`, `pco%ls_sd%y`, `pco%ls_sd%a` |
| 121 | data | `if (i_exist .or. in_sim%prt /= "null") then > do > if (pco%use_obj_labels == "n") then` | `name`, `pco%pw_sd%d`, `pco%pw_sd%m`, `pco%pw_sd%y`, `pco%pw_sd%a` |
| 124 | data | `if (i_exist .or. in_sim%prt /= "null") then > do > if (pco%use_obj_labels == "n") then` | `name`, `pco%chan%d`, `pco%chan%m`, `pco%chan%y`, `pco%chan%a` |
| 127 | data | `if (i_exist .or. in_sim%prt /= "null") then > do > if (pco%use_obj_labels == "n") then` | `name`, `pco%sd_chan%d`, `pco%sd_chan%m`, `pco%sd_chan%y`, `pco%sd_chan%a` |
| 130 | data | `if (i_exist .or. in_sim%prt /= "null") then > do > if (pco%use_obj_labels == "n") then` | `name`, `pco%aqu%d`, `pco%aqu%m`, `pco%aqu%y`, `pco%aqu%a` |
| 133 | data | `if (i_exist .or. in_sim%prt /= "null") then > do > if (pco%use_obj_labels == "n") then` | `name`, `pco%res%d`, `pco%res%m`, `pco%res%y`, `pco%res%a` |
| 136 | data | `if (i_exist .or. in_sim%prt /= "null") then > do > if (pco%use_obj_labels == "n") then` | `name`, `pco%recall%d`, `pco%recall%m`, `pco%recall%y`, `pco%recall%a` |
| 139 | data | `if (i_exist .or. in_sim%prt /= "null") then > do > if (pco%use_obj_labels == "n") then` | `name`, `pco%hyd%d`, `pco%hyd%m`, `pco%hyd%y`, `pco%hyd%a` |
| 142 | data | `if (i_exist .or. in_sim%prt /= "null") then > do > if (pco%use_obj_labels == "n") then` | `name`, `pco%ru%d`, `pco%ru%m`, `pco%ru%y`, `pco%ru%a` |
| 145 | data | `if (i_exist .or. in_sim%prt /= "null") then > do > if (pco%use_obj_labels == "n") then` | `name`, `pco%pest%d`, `pco%pest%m`, `pco%pest%y`, `pco%pest%a` |
| 148 | data | `if (i_exist .or. in_sim%prt /= "null") then > do > if (pco%use_obj_labels == "n") then` | `name`, `pco%salt_basin%d`, `pco%salt_basin%m`, `pco%salt_basin%y`, `pco%salt_basin%a` |
| 150 | data | `if (i_exist .or. in_sim%prt /= "null") then > do > if (pco%use_obj_labels == "n") then` | `name`, `pco%salt_hru%d`, `pco%salt_hru%m`, `pco%salt_hru%y`, `pco%salt_hru%a` |
| 152 | data | `if (i_exist .or. in_sim%prt /= "null") then > do > if (pco%use_obj_labels == "n") then` | `name`, `pco%salt_ru%d`, `pco%salt_ru%m`, `pco%salt_ru%y`, `pco%salt_ru%a` |
| 154 | data | `if (i_exist .or. in_sim%prt /= "null") then > do > if (pco%use_obj_labels == "n") then` | `name`, `pco%salt_aqu%d`, `pco%salt_aqu%m`, `pco%salt_aqu%y`, `pco%salt_aqu%a` |
| 156 | data | `if (i_exist .or. in_sim%prt /= "null") then > do > if (pco%use_obj_labels == "n") then` | `name`, `pco%salt_chn%d`, `pco%salt_chn%m`, `pco%salt_chn%y`, `pco%salt_chn%a` |
| 158 | data | `if (i_exist .or. in_sim%prt /= "null") then > do > if (pco%use_obj_labels == "n") then` | `name`, `pco%salt_res%d`, `pco%salt_res%m`, `pco%salt_res%y`, `pco%salt_res%a` |
| 160 | data | `if (i_exist .or. in_sim%prt /= "null") then > do > if (pco%use_obj_labels == "n") then` | `name`, `pco%salt_wet%d`, `pco%salt_wet%m`, `pco%salt_wet%y`, `pco%salt_wet%a` |
| 163 | data | `if (i_exist .or. in_sim%prt /= "null") then > do > if (pco%use_obj_labels == "n") then` | `name`, `pco%cs_basin%d`, `pco%cs_basin%m`, `pco%cs_basin%y`, `pco%cs_basin%a` |
| 165 | data | `if (i_exist .or. in_sim%prt /= "null") then > do > if (pco%use_obj_labels == "n") then` | `name`, `pco%cs_hru%d`, `pco%cs_hru%m`, `pco%cs_hru%y`, `pco%cs_hru%a` |
| 167 | data | `if (i_exist .or. in_sim%prt /= "null") then > do > if (pco%use_obj_labels == "n") then` | `name`, `pco%cs_ru%d`, `pco%cs_ru%m`, `pco%cs_ru%y`, `pco%cs_ru%a` |
| 169 | data | `if (i_exist .or. in_sim%prt /= "null") then > do > if (pco%use_obj_labels == "n") then` | `name`, `pco%cs_aqu%d`, `pco%cs_aqu%m`, `pco%cs_aqu%y`, `pco%cs_aqu%a` |
| 171 | data | `if (i_exist .or. in_sim%prt /= "null") then > do > if (pco%use_obj_labels == "n") then` | `name`, `pco%cs_chn%d`, `pco%cs_chn%m`, `pco%cs_chn%y`, `pco%cs_chn%a` |
| 173 | data | `if (i_exist .or. in_sim%prt /= "null") then > do > if (pco%use_obj_labels == "n") then` | `name`, `pco%cs_res%d`, `pco%cs_res%m`, `pco%cs_res%y`, `pco%cs_res%a` |
| 175 | data | `if (i_exist .or. in_sim%prt /= "null") then > do > if (pco%use_obj_labels == "n") then` | `name`, `pco%cs_wet%d`, `pco%cs_wet%m`, `pco%cs_wet%y`, `pco%cs_wet%a` |
| 179 | data | `if (i_exist .or. in_sim%prt /= "null") then > do > if (pco%use_obj_labels == "n") then / else > do while (eof >= 0)` | `name` |
| 188 | data | `if (i_exist .or. in_sim%prt /= "null") then > do > if (pco%use_obj_labels == "n") then / else > do while (eof >= 0) > select case(name) / case("basin_wb") > if (pco%wb_bsn%already_read_in) then / else` | `name`, `pco%wb_bsn%d`, `pco%wb_bsn%m`, `pco%wb_bsn%y`, `pco%wb_bsn%a` |
| 196 | data | `if (i_exist .or. in_sim%prt /= "null") then > do > if (pco%use_obj_labels == "n") then / else > do while (eof >= 0) > select case(name) / case("basin_nb") > if (pco%nb_bsn%already_read_in) then / else` | `name`, `pco%nb_bsn%d`, `pco%nb_bsn%m`, `pco%nb_bsn%y`, `pco%nb_bsn%a` |
| 204 | data | `if (i_exist .or. in_sim%prt /= "null") then > do > if (pco%use_obj_labels == "n") then / else > do while (eof >= 0) > select case(name) / case("basin_ls") > if (pco%ls_bsn%already_read_in) then / else` | `name`, `pco%ls_bsn%d`, `pco%ls_bsn%m`, `pco%ls_bsn%y`, `pco%ls_bsn%a` |
| 212 | data | `if (i_exist .or. in_sim%prt /= "null") then > do > if (pco%use_obj_labels == "n") then / else > do while (eof >= 0) > select case(name) / case("basin_pw") > if (pco%pw_bsn%already_read_in) then / else` | `name`, `pco%pw_bsn%d`, `pco%pw_bsn%m`, `pco%pw_bsn%y`, `pco%pw_bsn%a` |
| 220 | data | `if (i_exist .or. in_sim%prt /= "null") then > do > if (pco%use_obj_labels == "n") then / else > do while (eof >= 0) > select case(name) / case("basin_aqu") > if (pco%aqu_bsn%already_read_in) then / else` | `name`, `pco%aqu_bsn%d`, `pco%aqu_bsn%m`, `pco%aqu_bsn%y`, `pco%aqu_bsn%a` |
| 228 | data | `if (i_exist .or. in_sim%prt /= "null") then > do > if (pco%use_obj_labels == "n") then / else > do while (eof >= 0) > select case(name) / case("basin_res") > if (pco%res_bsn%already_read_in) then / else` | `name`, `pco%res_bsn%d`, `pco%res_bsn%m`, `pco%res_bsn%y`, `pco%res_bsn%a` |
| 236 | data | `if (i_exist .or. in_sim%prt /= "null") then > do > if (pco%use_obj_labels == "n") then / else > do while (eof >= 0) > select case(name) / case("basin_cha") > if (pco%chan_bsn%already_read_in) then / else` | `name`, `pco%chan_bsn%d`, `pco%chan_bsn%m`, `pco%chan_bsn%y`, `pco%chan_bsn%a` |
| 244 | data | `if (i_exist .or. in_sim%prt /= "null") then > do > if (pco%use_obj_labels == "n") then / else > do while (eof >= 0) > select case(name) / case("basin_sd_cha") > if (pco%sd_chan_bsn%already_read_in) then / else` | `name`, `pco%sd_chan_bsn%d`, `pco%sd_chan_bsn%m`, `pco%sd_chan_bsn%y`, `pco%sd_chan_bsn%a` |
| 252 | data | `if (i_exist .or. in_sim%prt /= "null") then > do > if (pco%use_obj_labels == "n") then / else > do while (eof >= 0) > select case(name) / case("basin_psc") > if (pco%recall_bsn%already_read_in) then / else` | `name`, `pco%recall_bsn%d`, `pco%recall_bsn%m`, `pco%recall_bsn%y`, `pco%recall_bsn%a` |
| 260 | data | `if (i_exist .or. in_sim%prt /= "null") then > do > if (pco%use_obj_labels == "n") then / else > do while (eof >= 0) > select case(name) / case("region_wb") > if (pco%wb_reg%already_read_in) then / else` | `name`, `pco%wb_reg%d`, `pco%wb_reg%m`, `pco%wb_reg%y`, `pco%wb_reg%a` |
| 268 | data | `if (i_exist .or. in_sim%prt /= "null") then > do > if (pco%use_obj_labels == "n") then / else > do while (eof >= 0) > select case(name) / case("region_nb") > if (pco%nb_reg%already_read_in) then / else` | `name`, `pco%nb_reg%d`, `pco%nb_reg%m`, `pco%nb_reg%y`, `pco%nb_reg%a` |
| 276 | data | `if (i_exist .or. in_sim%prt /= "null") then > do > if (pco%use_obj_labels == "n") then / else > do while (eof >= 0) > select case(name) / case("region_ls") > if (pco%ls_reg%already_read_in) then / else` | `name`, `pco%ls_reg%d`, `pco%ls_reg%m`, `pco%ls_reg%y`, `pco%ls_reg%a` |
| 284 | data | `if (i_exist .or. in_sim%prt /= "null") then > do > if (pco%use_obj_labels == "n") then / else > do while (eof >= 0) > select case(name) / case("region_pw") > if (pco%pw_reg%already_read_in) then / else` | `name`, `pco%pw_reg%d`, `pco%pw_reg%m`, `pco%pw_reg%y`, `pco%pw_reg%a` |
| 292 | data | `if (i_exist .or. in_sim%prt /= "null") then > do > if (pco%use_obj_labels == "n") then / else > do while (eof >= 0) > select case(name) / case("region_aqu") > if (pco%aqu_reg%already_read_in) then / else` | `name`, `pco%aqu_reg%d`, `pco%aqu_reg%m`, `pco%aqu_reg%y`, `pco%aqu_reg%a` |
| 300 | data | `if (i_exist .or. in_sim%prt /= "null") then > do > if (pco%use_obj_labels == "n") then / else > do while (eof >= 0) > select case(name) / case("region_res") > if (pco%res_reg%already_read_in) then / else` | `name`, `pco%res_reg%d`, `pco%res_reg%m`, `pco%res_reg%y`, `pco%res_reg%a` |
| 308 | data | `if (i_exist .or. in_sim%prt /= "null") then > do > if (pco%use_obj_labels == "n") then / else > do while (eof >= 0) > select case(name) / case("region_sd_cha") > if (pco%sd_chan_reg%already_read_in) then / else` | `name`, `pco%sd_chan_reg%d`, `pco%sd_chan_reg%m`, `pco%sd_chan_reg%y`, `pco%sd_chan_reg%a` |
| 316 | data | `if (i_exist .or. in_sim%prt /= "null") then > do > if (pco%use_obj_labels == "n") then / else > do while (eof >= 0) > select case(name) / case("region_psc") > if (pco%recall_reg%already_read_in) then / else` | `name`, `pco%recall_reg%d`, `pco%recall_reg%m`, `pco%recall_reg%y`, `pco%recall_reg%a` |
| 324 | data | `if (i_exist .or. in_sim%prt /= "null") then > do > if (pco%use_obj_labels == "n") then / else > do while (eof >= 0) > select case(name) / case("water_allo") > if (pco%water_allo%already_read_in) then / else` | `name`, `pco%water_allo%d`, `pco%water_allo%m`, `pco%water_allo%y`, `pco%water_allo%a` |
| 332 | data | `if (i_exist .or. in_sim%prt /= "null") then > do > if (pco%use_obj_labels == "n") then / else > do while (eof >= 0) > select case(name) / case("lsunit_wb") > if (pco%wb_lsu%already_read_in) then / else` | `name`, `pco%wb_lsu%d`, `pco%wb_lsu%m`, `pco%wb_lsu%y`, `pco%wb_lsu%a` |
| 340 | data | `if (i_exist .or. in_sim%prt /= "null") then > do > if (pco%use_obj_labels == "n") then / else > do while (eof >= 0) > select case(name) / case("lsunit_nb") > if (pco%nb_lsu%already_read_in) then / else` | `name`, `pco%nb_lsu%d`, `pco%nb_lsu%m`, `pco%nb_lsu%y`, `pco%nb_lsu%a` |
| 348 | data | `if (i_exist .or. in_sim%prt /= "null") then > do > if (pco%use_obj_labels == "n") then / else > do while (eof >= 0) > select case(name) / case("lsunit_ls") > if (pco%ls_lsu%already_read_in) then / else` | `name`, `pco%ls_lsu%d`, `pco%ls_lsu%m`, `pco%ls_lsu%y`, `pco%ls_lsu%a` |
| 356 | data | `if (i_exist .or. in_sim%prt /= "null") then > do > if (pco%use_obj_labels == "n") then / else > do while (eof >= 0) > select case(name) / case("lsunit_pw") > if (pco%pw_lsu%already_read_in) then / else` | `name`, `pco%pw_lsu%d`, `pco%pw_lsu%m`, `pco%pw_lsu%y`, `pco%pw_lsu%a` |
| 365 | data | `if (i_exist .or. in_sim%prt /= "null") then > do > if (pco%use_obj_labels == "n") then / else > do while (eof >= 0) > select case(name) / case("lsu_cb_gl") > if (pco%cb_gl_lsu%already_read_in) then / else` | `name`, `pco%cb_gl_lsu%d`, `pco%cb_gl_lsu%m`, `pco%cb_gl_lsu%y`, `pco%cb_gl_lsu%a` |
| 373 | data | `if (i_exist .or. in_sim%prt /= "null") then > do > if (pco%use_obj_labels == "n") then / else > do while (eof >= 0) > select case(name) / case("lsu_cb_trf") > if (pco%cb_trf_lsu%already_read_in) then / else` | `name`, `pco%cb_trf_lsu%d`, `pco%cb_trf_lsu%m`, `pco%cb_trf_lsu%y`, `pco%cb_trf_lsu%a` |
| 381 | data | `if (i_exist .or. in_sim%prt /= "null") then > do > if (pco%use_obj_labels == "n") then / else > do while (eof >= 0) > select case(name) / case("lsu_cb_plt") > if (pco%cb_plt_lsu%already_read_in) then / else` | `name`, `pco%cb_plt_lsu%d`, `pco%cb_plt_lsu%m`, `pco%cb_plt_lsu%y`, `pco%cb_plt_lsu%a` |
| 389 | data | `if (i_exist .or. in_sim%prt /= "null") then > do > if (pco%use_obj_labels == "n") then / else > do while (eof >= 0) > select case(name) / case("hru_wb") > if (pco%wb_hru%already_read_in) then / else` | `name`, `pco%wb_hru%d`, `pco%wb_hru%m`, `pco%wb_hru%y`, `pco%wb_hru%a` |
| 397 | data | `if (i_exist .or. in_sim%prt /= "null") then > do > if (pco%use_obj_labels == "n") then / else > do while (eof >= 0) > select case(name) / case("hru_nb") > if (pco%nb_hru%already_read_in) then / else` | `name`, `pco%nb_hru%d`, `pco%nb_hru%m`, `pco%nb_hru%y`, `pco%nb_hru%a` |
| 405 | data | `if (i_exist .or. in_sim%prt /= "null") then > do > if (pco%use_obj_labels == "n") then / else > do while (eof >= 0) > select case(name) / case("hru_ls") > if (pco%ls_hru%already_read_in) then / else` | `name`, `pco%ls_hru%d`, `pco%ls_hru%m`, `pco%ls_hru%y`, `pco%ls_hru%a` |
| 413 | data | `if (i_exist .or. in_sim%prt /= "null") then > do > if (pco%use_obj_labels == "n") then / else > do while (eof >= 0) > select case(name) / case("hru_pw") > if (pco%pw_hru%already_read_in) then / else` | `name`, `pco%pw_hru%d`, `pco%pw_hru%m`, `pco%pw_hru%y`, `pco%pw_hru%a` |
| 421 | data | `if (i_exist .or. in_sim%prt /= "null") then > do > if (pco%use_obj_labels == "n") then / else > do while (eof >= 0) > select case(name) / case("hru_cb") > if (pco%cb_hru%already_read_in) then / else` | `name`, `pco%cb_hru%d`, `pco%cb_hru%m`, `pco%cb_hru%y`, `pco%cb_hru%a` |
| 429 | data | `if (i_exist .or. in_sim%prt /= "null") then > do > if (pco%use_obj_labels == "n") then / else > do while (eof >= 0) > select case(name) / case("hru_cb_vars") > if (pco%cb_vars_hru%already_read_in) then / else` | `name`, `pco%cb_vars_hru%d`, `pco%cb_vars_hru%m`, `pco%cb_vars_hru%y`, `pco%cb_vars_hru%a` |
| 438 | data | `if (i_exist .or. in_sim%prt /= "null") then > do > if (pco%use_obj_labels == "n") then / else > do while (eof >= 0) > select case(name) / case("hru_cb_gl") > if (pco%cb_gl_hru%already_read_in) then / else` | `name`, `pco%cb_gl_hru%d`, `pco%cb_gl_hru%m`, `pco%cb_gl_hru%y`, `pco%cb_gl_hru%a` |
| 446 | data | `if (i_exist .or. in_sim%prt /= "null") then > do > if (pco%use_obj_labels == "n") then / else > do while (eof >= 0) > select case(name) / case("hru_cb_trf") > if (pco%cb_trf_hru%already_read_in) then / else` | `name`, `pco%cb_trf_hru%d`, `pco%cb_trf_hru%m`, `pco%cb_trf_hru%y`, `pco%cb_trf_hru%a` |
| 454 | data | `if (i_exist .or. in_sim%prt /= "null") then > do > if (pco%use_obj_labels == "n") then / else > do while (eof >= 0) > select case(name) / case("hru_cb_lyr") > if (pco%cb_lyr_hru%already_read_in) then / else` | `name`, `pco%cb_lyr_hru%d`, `pco%cb_lyr_hru%m`, `pco%cb_lyr_hru%y`, `pco%cb_lyr_hru%a` |
| 462 | data | `if (i_exist .or. in_sim%prt /= "null") then > do > if (pco%use_obj_labels == "n") then / else > do while (eof >= 0) > select case(name) / case("hru_cb_cpool") > if (pco%cb_cpool_hru%already_read_in) then / else` | `name`, `pco%cb_cpool_hru%d`, `pco%cb_cpool_hru%m`, `pco%cb_cpool_hru%y`, `pco%cb_cpool_hru%a` |
| 470 | data | `if (i_exist .or. in_sim%prt /= "null") then > do > if (pco%use_obj_labels == "n") then / else > do while (eof >= 0) > select case(name) / case("hru_cb_npool") > if (pco%cb_npool_hru%already_read_in) then / else` | `name`, `pco%cb_npool_hru%d`, `pco%cb_npool_hru%m`, `pco%cb_npool_hru%y`, `pco%cb_npool_hru%a` |
| 478 | data | `if (i_exist .or. in_sim%prt /= "null") then > do > if (pco%use_obj_labels == "n") then / else > do while (eof >= 0) > select case(name) / case("hru_cb_plt") > if (pco%cb_plt_hru%already_read_in) then / else` | `name`, `pco%cb_plt_hru%d`, `pco%cb_plt_hru%m`, `pco%cb_plt_hru%y`, `pco%cb_plt_hru%a` |
| 486 | data | `if (i_exist .or. in_sim%prt /= "null") then > do > if (pco%use_obj_labels == "n") then / else > do while (eof >= 0) > select case(name) / case("hru_cb_flux") > if (pco%cb_flux_hru%already_read_in) then / else` | `name`, `pco%cb_flux_hru%d`, `pco%cb_flux_hru%m`, `pco%cb_flux_hru%y`, `pco%cb_flux_hru%a` |
| 494 | data | `if (i_exist .or. in_sim%prt /= "null") then > do > if (pco%use_obj_labels == "n") then / else > do while (eof >= 0) > select case(name) / case("hru_cb_drv") > if (pco%cb_drv_hru%already_read_in) then / else` | `name`, `pco%cb_drv_hru%d`, `pco%cb_drv_hru%m`, `pco%cb_drv_hru%y`, `pco%cb_drv_hru%a` |
| 502 | data | `if (i_exist .or. in_sim%prt /= "null") then > do > if (pco%use_obj_labels == "n") then / else > do while (eof >= 0) > select case(name) / case("hru_cb_dyn") > if (pco%cb_dyn_hru%already_read_in) then / else` | `name`, `pco%cb_dyn_hru%d`, `pco%cb_dyn_hru%m`, `pco%cb_dyn_hru%y`, `pco%cb_dyn_hru%a` |
| 510 | data | `if (i_exist .or. in_sim%prt /= "null") then > do > if (pco%use_obj_labels == "n") then / else > do while (eof >= 0) > select case(name) / case("hru_cb_snap") > if (pco%cb_snap_hru%already_read_in) then / else` | `name`, `pco%cb_snap_hru%d`, `pco%cb_snap_hru%m`, `pco%cb_snap_hru%y`, `pco%cb_snap_hru%a` |
| 518 | data | `if (i_exist .or. in_sim%prt /= "null") then > do > if (pco%use_obj_labels == "n") then / else > do while (eof >= 0) > select case(name) / case("hru-lte_wb") > if (pco%wb_sd%already_read_in) then / else` | `name`, `pco%wb_sd%d`, `pco%wb_sd%m`, `pco%wb_sd%y`, `pco%wb_sd%a` |
| 526 | data | `if (i_exist .or. in_sim%prt /= "null") then > do > if (pco%use_obj_labels == "n") then / else > do while (eof >= 0) > select case(name) / case("hru-lte_nb") > if (pco%nb_sd%already_read_in) then / else` | `name`, `pco%nb_sd%d`, `pco%nb_sd%m`, `pco%nb_sd%y`, `pco%nb_sd%a` |
| 534 | data | `if (i_exist .or. in_sim%prt /= "null") then > do > if (pco%use_obj_labels == "n") then / else > do while (eof >= 0) > select case(name) / case("hru-lte_ls") > if (pco%ls_sd%already_read_in) then / else` | `name`, `pco%ls_sd%d`, `pco%ls_sd%m`, `pco%ls_sd%y`, `pco%ls_sd%a` |
| 542 | data | `if (i_exist .or. in_sim%prt /= "null") then > do > if (pco%use_obj_labels == "n") then / else > do while (eof >= 0) > select case(name) / case("hru-lte_pw") > if (pco%pw_sd%already_read_in) then / else` | `name`, `pco%pw_sd%d`, `pco%pw_sd%m`, `pco%pw_sd%y`, `pco%pw_sd%a` |
| 550 | data | `if (i_exist .or. in_sim%prt /= "null") then > do > if (pco%use_obj_labels == "n") then / else > do while (eof >= 0) > select case(name) / case("channel") > if (pco%chan%already_read_in) then / else` | `name`, `pco%chan%d`, `pco%chan%m`, `pco%chan%y`, `pco%chan%a` |
| 558 | data | `if (i_exist .or. in_sim%prt /= "null") then > do > if (pco%use_obj_labels == "n") then / else > do while (eof >= 0) > select case(name) / case("channel_sd") > if (pco%sd_chan%already_read_in) then / else` | `name`, `pco%sd_chan%d`, `pco%sd_chan%m`, `pco%sd_chan%y`, `pco%sd_chan%a` |
| 566 | data | `if (i_exist .or. in_sim%prt /= "null") then > do > if (pco%use_obj_labels == "n") then / else > do while (eof >= 0) > select case(name) / case("aquifer") > if (pco%aqu%already_read_in) then / else` | `name`, `pco%aqu%d`, `pco%aqu%m`, `pco%aqu%y`, `pco%aqu%a` |
| 574 | data | `if (i_exist .or. in_sim%prt /= "null") then > do > if (pco%use_obj_labels == "n") then / else > do while (eof >= 0) > select case(name) / case("reservoir") > if (pco%res%already_read_in) then / else` | `name`, `pco%res%d`, `pco%res%m`, `pco%res%y`, `pco%res%a` |
| 582 | data | `if (i_exist .or. in_sim%prt /= "null") then > do > if (pco%use_obj_labels == "n") then / else > do while (eof >= 0) > select case(name) / case("recall") > if (pco%recall%already_read_in) then / else` | `name`, `pco%recall%d`, `pco%recall%m`, `pco%recall%y`, `pco%recall%a` |
| 590 | data | `if (i_exist .or. in_sim%prt /= "null") then > do > if (pco%use_obj_labels == "n") then / else > do while (eof >= 0) > select case(name) / case("hyd") > if (pco%hyd%already_read_in) then / else` | `name`, `pco%hyd%d`, `pco%hyd%m`, `pco%hyd%y`, `pco%hyd%a` |
| 598 | data | `if (i_exist .or. in_sim%prt /= "null") then > do > if (pco%use_obj_labels == "n") then / else > do while (eof >= 0) > select case(name) / case("ru") > if (pco%ru%already_read_in) then / else` | `name`, `pco%ru%d`, `pco%ru%m`, `pco%ru%y`, `pco%ru%a` |
| 606 | data | `if (i_exist .or. in_sim%prt /= "null") then > do > if (pco%use_obj_labels == "n") then / else > do while (eof >= 0) > select case(name) / case("pest") > if (pco%pest%already_read_in) then / else` | `name`, `pco%pest%d`, `pco%pest%m`, `pco%pest%y`, `pco%pest%a` |
| 614 | data | `if (i_exist .or. in_sim%prt /= "null") then > do > if (pco%use_obj_labels == "n") then / else > do while (eof >= 0) > select case(name) / case("basin_salt") > if (pco%salt_basin%already_read_in) then / else` | `name`, `pco%salt_basin%d`, `pco%salt_basin%m`, `pco%salt_basin%y`, `pco%salt_basin%a` |
| 622 | data | `if (i_exist .or. in_sim%prt /= "null") then > do > if (pco%use_obj_labels == "n") then / else > do while (eof >= 0) > select case(name) / case("hru_salt") > if (pco%salt_hru%already_read_in) then / else` | `name`, `pco%salt_hru%d`, `pco%salt_hru%m`, `pco%salt_hru%y`, `pco%salt_hru%a` |
| 630 | data | `if (i_exist .or. in_sim%prt /= "null") then > do > if (pco%use_obj_labels == "n") then / else > do while (eof >= 0) > select case(name) / case("ru_salt") > if (pco%salt_ru%already_read_in) then / else` | `name`, `pco%salt_ru%d`, `pco%salt_ru%m`, `pco%salt_ru%y`, `pco%salt_ru%a` |
| 638 | data | `if (i_exist .or. in_sim%prt /= "null") then > do > if (pco%use_obj_labels == "n") then / else > do while (eof >= 0) > select case(name) / case("aqu_salt") > if (pco%salt_aqu%already_read_in) then / else` | `name`, `pco%salt_aqu%d`, `pco%salt_aqu%m`, `pco%salt_aqu%y`, `pco%salt_aqu%a` |
| 646 | data | `if (i_exist .or. in_sim%prt /= "null") then > do > if (pco%use_obj_labels == "n") then / else > do while (eof >= 0) > select case(name) / case("channel_salt") > if (pco%salt_chn%already_read_in) then / else` | `name`, `pco%salt_chn%d`, `pco%salt_chn%m`, `pco%salt_chn%y`, `pco%salt_chn%a` |
| 654 | data | `if (i_exist .or. in_sim%prt /= "null") then > do > if (pco%use_obj_labels == "n") then / else > do while (eof >= 0) > select case(name) / case("res_salt") > if (pco%salt_res%already_read_in) then / else` | `name`, `pco%salt_res%d`, `pco%salt_res%m`, `pco%salt_res%y`, `pco%salt_res%a` |
| 662 | data | `if (i_exist .or. in_sim%prt /= "null") then > do > if (pco%use_obj_labels == "n") then / else > do while (eof >= 0) > select case(name) / case("wetland_salt") > if (pco%salt_wet%already_read_in) then / else` | `name`, `pco%salt_wet%d`, `pco%salt_wet%m`, `pco%salt_wet%y`, `pco%salt_wet%a` |
| 671 | data | `if (i_exist .or. in_sim%prt /= "null") then > do > if (pco%use_obj_labels == "n") then / else > do while (eof >= 0) > select case(name) / case("basin_cs") > if (pco%cs_basin%already_read_in) then / else` | `name`, `pco%cs_basin%d`, `pco%cs_basin%m`, `pco%cs_basin%y`, `pco%cs_basin%a` |
| 679 | data | `if (i_exist .or. in_sim%prt /= "null") then > do > if (pco%use_obj_labels == "n") then / else > do while (eof >= 0) > select case(name) / case("hru_cs") > if (pco%cs_hru%already_read_in) then / else` | `name`, `pco%cs_hru%d`, `pco%cs_hru%m`, `pco%cs_hru%y`, `pco%cs_hru%a` |
| 687 | data | `if (i_exist .or. in_sim%prt /= "null") then > do > if (pco%use_obj_labels == "n") then / else > do while (eof >= 0) > select case(name) / case("ru_cs") > if (pco%cs_ru%already_read_in) then / else` | `name`, `pco%cs_ru%d`, `pco%cs_ru%m`, `pco%cs_ru%y`, `pco%cs_ru%a` |
| 695 | data | `if (i_exist .or. in_sim%prt /= "null") then > do > if (pco%use_obj_labels == "n") then / else > do while (eof >= 0) > select case(name) / case("aqu_cs") > if (pco%cs_aqu%already_read_in) then / else` | `name`, `pco%cs_aqu%d`, `pco%cs_aqu%m`, `pco%cs_aqu%y`, `pco%cs_aqu%a` |
| 703 | data | `if (i_exist .or. in_sim%prt /= "null") then > do > if (pco%use_obj_labels == "n") then / else > do while (eof >= 0) > select case(name) / case("channel_cs") > if (pco%cs_chn%already_read_in) then / else` | `name`, `pco%cs_chn%d`, `pco%cs_chn%m`, `pco%cs_chn%y`, `pco%cs_chn%a` |
| 711 | data | `if (i_exist .or. in_sim%prt /= "null") then > do > if (pco%use_obj_labels == "n") then / else > do while (eof >= 0) > select case(name) / case("res_cs") > if (pco%cs_res%already_read_in) then / else` | `name`, `pco%cs_res%d`, `pco%cs_res%m`, `pco%cs_res%y`, `pco%cs_res%a` |
| 719 | data | `if (i_exist .or. in_sim%prt /= "null") then > do > if (pco%use_obj_labels == "n") then / else > do while (eof >= 0) > select case(name) / case("wetland_cs") > if (pco%cs_wet%already_read_in) then / else` | `name`, `pco%cs_wet%d`, `pco%cs_wet%m`, `pco%cs_wet%y`, `pco%cs_wet%a` |
| 727 | data | `if (i_exist .or. in_sim%prt /= "null") then > do > if (pco%use_obj_labels == "n") then / else > do while (eof >= 0) > select case(name) / case("gwflow_wb") > if (pco%gwflow_wb%already_read_in) then / else` | `name`, `pco%gwflow_wb%d`, `pco%gwflow_wb%m`, `pco%gwflow_wb%y`, `pco%gwflow_wb%a` |
| 735 | data | `if (i_exist .or. in_sim%prt /= "null") then > do > if (pco%use_obj_labels == "n") then / else > do while (eof >= 0) > select case(name) / case("gwflow_flux") > if (pco%gwflow_flux%already_read_in) then / else` | `name`, `pco%gwflow_flux%d`, `pco%gwflow_flux%m`, `pco%gwflow_flux%y`, `pco%gwflow_flux%a` |
| 743 | data | `if (i_exist .or. in_sim%prt /= "null") then > do > if (pco%use_obj_labels == "n") then / else > do while (eof >= 0) > select case(name) / case("gwflow_heat") > if (pco%gwflow_heat%already_read_in) then / else` | `name`, `pco%gwflow_heat%d`, `pco%gwflow_heat%m`, `pco%gwflow_heat%y`, `pco%gwflow_heat%a` |
| 751 | data | `if (i_exist .or. in_sim%prt /= "null") then > do > if (pco%use_obj_labels == "n") then / else > do while (eof >= 0) > select case(name) / case("gwflow_solute") > if (pco%gwflow_solute%already_read_in) then / else` | `name`, `pco%gwflow_solute%d`, `pco%gwflow_solute%m`, `pco%gwflow_solute%y`, `pco%gwflow_solute%a` |
| 759 | data | `if (i_exist .or. in_sim%prt /= "null") then > do > if (pco%use_obj_labels == "n") then / else > do while (eof >= 0) > select case(name) / case("gwflow_obs") > if (pco%gwflow_obs%already_read_in) then / else` | `name`, `pco%gwflow_obs%d`, `pco%gwflow_obs%m`, `pco%gwflow_obs%y`, `pco%gwflow_obs%a` |
| 767 | data | `if (i_exist .or. in_sim%prt /= "null") then > do > if (pco%use_obj_labels == "n") then / else > do while (eof >= 0) > select case(name) / case("gwflow_pump") > if (pco%gwflow_pump%already_read_in) then / else` | `name`, `pco%gwflow_pump%d`, `pco%gwflow_pump%m`, `pco%gwflow_pump%y`, `pco%gwflow_pump%a` |

### `salt_hru.ini`

- Review needed: yes
- Reader procedures changed: yes
- Read-block count changed: yes
- Read conditions changed: yes
- Base flattened read order: `titldum`, `header`, `header`, `header`, `header`, `titldum`, `titldum`, `titldum`, `titldum`, `header`, `header`, `header`, `header`, `salt_soil_ini(isalti)%name`, `salt_soil_ini(isalti)%soil`, `salt_soil_ini(isalti)%plt`, `titldum`, `header`, `titldum`, `titldum`, `titldum`, `titldum`, `header`, `salt_soil_ini(isalti)%name`, `titldum`, `salt_soil_ini(isalti)%soil`, `titldum`, `salt_soil_ini(isalti)%plt`
- Candidate flattened read order: `titldum`, `header`, `header`, `header`, `header`, `titldum`, `titldum`, `titldum`, `titldum`, `header`, `header`, `header`, `header`, `salt_soil_ini(isalti)%name`, `salt_soil_ini(isalti)%soil`, `salt_soil_ini(isalti)%plt`

#### Read-order edits

- `delete` at base index 16 / candidate index 16: removed `titldum`, `header`, `titldum`, `titldum`, `titldum`, `titldum`, `header`, `salt_soil_ini(isalti)%name`, `titldum`, `salt_soil_ini(isalti)%soil`, `titldum`, `salt_soil_ini(isalti)%plt`; added _no fields captured_

#### Base read structure

- Schema status: `certified`
- Review needed: no
- Source expression(s): `in_init%salt_soil`, `salt_hru.ini`

- Procedure: `salt_hru_aqu_read`
- Reader: `salt_hru_aqu_read.f90`
- Match: source_input
- Resolved default filename(s): `salt_hru.ini`
- Source filename expression(s): `in_init%salt_soil`, `salt_hru.ini`
- Open: line 23, file expression `in_init%salt_soil`, parser value `salt_hru.ini`, condition `if (i_exist .or. in_init%salt_soil /= "null") then > do`

| Line | Role | Condition | Fields read |
| --- | --- | --- | --- |
| 24 | title | `if (i_exist .or. in_init%salt_soil /= "null") then > do` | `titldum` |
| 26 | header | `if (i_exist .or. in_init%salt_soil /= "null") then > do` | `header` |
| 31 | title | `if (i_exist .or. in_init%salt_soil /= "null") then > do > do while (eof == 0)` | `titldum` |
| 33 | title | `if (i_exist .or. in_init%salt_soil /= "null") then > do > do while (eof == 0)` | `titldum` |
| 35 | title | `if (i_exist .or. in_init%salt_soil /= "null") then > do > do while (eof == 0)` | `titldum` |
| 49 | title | `if (i_exist .or. in_init%salt_soil /= "null") then > do` | `titldum` |
| 51 | header | `if (i_exist .or. in_init%salt_soil /= "null") then > do` | `header` |
| 55 | data | `if (i_exist .or. in_init%salt_soil /= "null") then > do > do isalti = 1, imax` | `salt_soil_ini(isalti)%name` |
| 57 | data | `if (i_exist .or. in_init%salt_soil /= "null") then > do > do isalti = 1, imax` | `titldum`, `salt_soil_ini(isalti)%soil` |
| 59 | data | `if (i_exist .or. in_init%salt_soil /= "null") then > do > do isalti = 1, imax` | `titldum`, `salt_soil_ini(isalti)%plt` |


- Procedure: `salt_hru_read`
- Reader: `salt_hru_read.f90`
- Match: source_input
- Resolved default filename(s): `salt_hru.ini`
- Source filename expression(s): `salt_hru.ini`
- Open: line 23, file expression `'salt_hru.ini'`, parser value `salt_hru.ini`, condition `if (i_exist .or. 'salt_hru.ini' /= "null") then > do`

| Line | Role | Condition | Fields read |
| --- | --- | --- | --- |
| 24 | title | `if (i_exist .or. 'salt_hru.ini' /= "null") then > do` | `titldum` |
| 26 | header | `if (i_exist .or. 'salt_hru.ini' /= "null") then > do` | `header` |
| 28 | header | `if (i_exist .or. 'salt_hru.ini' /= "null") then > do` | `header` |
| 30 | header | `if (i_exist .or. 'salt_hru.ini' /= "null") then > do` | `header` |
| 32 | header | `if (i_exist .or. 'salt_hru.ini' /= "null") then > do` | `header` |
| 37 | title | `if (i_exist .or. 'salt_hru.ini' /= "null") then > do > do while (eof == 0)` | `titldum` |
| 39 | title | `if (i_exist .or. 'salt_hru.ini' /= "null") then > do > do while (eof == 0)` | `titldum` |
| 41 | title | `if (i_exist .or. 'salt_hru.ini' /= "null") then > do > do while (eof == 0)` | `titldum` |
| 55 | title | `if (i_exist .or. 'salt_hru.ini' /= "null") then > do` | `titldum` |
| 57 | header | `if (i_exist .or. 'salt_hru.ini' /= "null") then > do` | `header` |
| 59 | header | `if (i_exist .or. 'salt_hru.ini' /= "null") then > do` | `header` |
| 61 | header | `if (i_exist .or. 'salt_hru.ini' /= "null") then > do` | `header` |
| 63 | header | `if (i_exist .or. 'salt_hru.ini' /= "null") then > do` | `header` |
| 67 | data | `if (i_exist .or. 'salt_hru.ini' /= "null") then > do > do isalti = 1, imax` | `salt_soil_ini(isalti)%name` |
| 69 | data | `if (i_exist .or. 'salt_hru.ini' /= "null") then > do > do isalti = 1, imax` | `salt_soil_ini(isalti)%soil` |
| 71 | data | `if (i_exist .or. 'salt_hru.ini' /= "null") then > do > do isalti = 1, imax` | `salt_soil_ini(isalti)%plt` |


#### Candidate read structure

- Schema status: `certified`
- Review needed: no
- Source expression(s): `salt_hru.ini`

- Procedure: `salt_hru_read`
- Reader: `salt_hru_read.f90`
- Match: source_input
- Resolved default filename(s): `salt_hru.ini`
- Source filename expression(s): `salt_hru.ini`
- Open: line 23, file expression `'salt_hru.ini'`, parser value `salt_hru.ini`, condition `if (i_exist .or. 'salt_hru.ini' /= "null") then > do`

| Line | Role | Condition | Fields read |
| --- | --- | --- | --- |
| 24 | title | `if (i_exist .or. 'salt_hru.ini' /= "null") then > do` | `titldum` |
| 26 | header | `if (i_exist .or. 'salt_hru.ini' /= "null") then > do` | `header` |
| 28 | header | `if (i_exist .or. 'salt_hru.ini' /= "null") then > do` | `header` |
| 30 | header | `if (i_exist .or. 'salt_hru.ini' /= "null") then > do` | `header` |
| 32 | header | `if (i_exist .or. 'salt_hru.ini' /= "null") then > do` | `header` |
| 37 | title | `if (i_exist .or. 'salt_hru.ini' /= "null") then > do > do while (eof == 0)` | `titldum` |
| 39 | title | `if (i_exist .or. 'salt_hru.ini' /= "null") then > do > do while (eof == 0)` | `titldum` |
| 41 | title | `if (i_exist .or. 'salt_hru.ini' /= "null") then > do > do while (eof == 0)` | `titldum` |
| 55 | title | `if (i_exist .or. 'salt_hru.ini' /= "null") then > do` | `titldum` |
| 57 | header | `if (i_exist .or. 'salt_hru.ini' /= "null") then > do` | `header` |
| 59 | header | `if (i_exist .or. 'salt_hru.ini' /= "null") then > do` | `header` |
| 61 | header | `if (i_exist .or. 'salt_hru.ini' /= "null") then > do` | `header` |
| 63 | header | `if (i_exist .or. 'salt_hru.ini' /= "null") then > do` | `header` |
| 67 | data | `if (i_exist .or. 'salt_hru.ini' /= "null") then > do > do isalti = 1, imax` | `salt_soil_ini(isalti)%name` |
| 69 | data | `if (i_exist .or. 'salt_hru.ini' /= "null") then > do > do isalti = 1, imax` | `salt_soil_ini(isalti)%soil` |
| 71 | data | `if (i_exist .or. 'salt_hru.ini' /= "null") then > do > do isalti = 1, imax` | `salt_soil_ini(isalti)%plt` |

### `soil_plant.ini`

- Review needed: yes
- Reader procedures changed: no
- Read-block count changed: no
- Read conditions changed: yes
- Base flattened read order: `titldum`, `header`, `titldum`, `titldum`, `header`, `sol_plt_ini(ii)%name`, `sol_plt_ini(ii)%sw_frac`, `sol_plt_ini(ii)%nutc`, `sol_plt_ini(ii)%pestc`, `sol_plt_ini(ii)%pathc`, `sol_plt_ini(ii)%saltc`, `sol_plt_ini(ii)%hmetc`
- Candidate flattened read order: `titldum`, `header`, `titldum`, `titldum`, `header`, `sol_plt_ini(ii)%name`, `sol_plt_ini(ii)%sw_frac`, `sol_plt_ini(ii)%nutc`, `sol_plt_ini(ii)%pestc`, `sol_plt_ini(ii)%pathc`, `sol_plt_ini(ii)%saltc`, `sol_plt_ini(ii)%hmetc`, `sol_plt_ini(ii)%name`, `sol_plt_ini(ii)%sw_frac`, `sol_plt_ini(ii)%nutc`, `sol_plt_ini(ii)%pestc`, `sol_plt_ini(ii)%pathc`, `sol_plt_ini(ii)%saltc`, `sol_plt_ini(ii)%hmetc`, `sol_plt_ini(ii)%csc`

#### Read-order edits

- `insert` at base index 12 / candidate index 12: removed _no fields captured_; added `sol_plt_ini(ii)%name`, `sol_plt_ini(ii)%sw_frac`, `sol_plt_ini(ii)%nutc`, `sol_plt_ini(ii)%pestc`, `sol_plt_ini(ii)%pathc`, `sol_plt_ini(ii)%saltc`, `sol_plt_ini(ii)%hmetc`, `sol_plt_ini(ii)%csc`

#### Base read structure

- Schema status: `certified`
- Review needed: no
- Source expression(s): `in_init%soil_plant_ini`, `soil_plant.ini`

- Procedure: `soil_plant_init`
- Reader: `soil_plant_init.f90`
- Match: source_input
- Resolved default filename(s): `soil_plant.ini`
- Source filename expression(s): `in_init%soil_plant_ini`, `soil_plant.ini`
- Open: line 23, file expression `in_init%soil_plant_ini`, parser value `soil_plant.ini`, condition `if (i_exist .or. in_init%soil_plant_ini /= "null") then > do`

| Line | Role | Condition | Fields read |
| --- | --- | --- | --- |
| 24 | title | `if (i_exist .or. in_init%soil_plant_ini /= "null") then > do` | `titldum` |
| 26 | header | `if (i_exist .or. in_init%soil_plant_ini /= "null") then > do` | `header` |
| 30 | title | `if (i_exist .or. in_init%soil_plant_ini /= "null") then > do > do while (eof == 0)` | `titldum` |
| 39 | title | `if (i_exist .or. in_init%soil_plant_ini /= "null") then > do` | `titldum` |
| 41 | header | `if (i_exist .or. in_init%soil_plant_ini /= "null") then > do` | `header` |
| 45 | data | `if (i_exist .or. in_init%soil_plant_ini /= "null") then > do > do ii = 1, imax` | `sol_plt_ini(ii)%name`, `sol_plt_ini(ii)%sw_frac`, `sol_plt_ini(ii)%nutc`, `sol_plt_ini(ii)%pestc`, `sol_plt_ini(ii)%pathc`, `sol_plt_ini(ii)%saltc`, `sol_plt_ini(ii)%hmetc` |


#### Candidate read structure

- Schema status: `certified`
- Review needed: no
- Source expression(s): `in_init%soil_plant_ini`, `soil_plant.ini`

- Procedure: `soil_plant_init`
- Reader: `soil_plant_init.f90`
- Match: source_input
- Resolved default filename(s): `soil_plant.ini`
- Source filename expression(s): `in_init%soil_plant_ini`, `soil_plant.ini`
- Open: line 24, file expression `in_init%soil_plant_ini`, parser value `soil_plant.ini`, condition `if (i_exist .or. in_init%soil_plant_ini /= "null") then > do`

| Line | Role | Condition | Fields read |
| --- | --- | --- | --- |
| 25 | title | `if (i_exist .or. in_init%soil_plant_ini /= "null") then > do` | `titldum` |
| 27 | header | `if (i_exist .or. in_init%soil_plant_ini /= "null") then > do` | `header` |
| 31 | title | `if (i_exist .or. in_init%soil_plant_ini /= "null") then > do > do while (eof == 0)` | `titldum` |
| 40 | title | `if (i_exist .or. in_init%soil_plant_ini /= "null") then > do` | `titldum` |
| 42 | header | `if (i_exist .or. in_init%soil_plant_ini /= "null") then > do` | `header` |
| 47 | data | `if (i_exist .or. in_init%soil_plant_ini /= "null") then > do > do ii = 1, imax > if (bsn_cc%nam1 == 0) then` | `sol_plt_ini(ii)%name`, `sol_plt_ini(ii)%sw_frac`, `sol_plt_ini(ii)%nutc`, `sol_plt_ini(ii)%pestc`, `sol_plt_ini(ii)%pathc`, `sol_plt_ini(ii)%saltc`, `sol_plt_ini(ii)%hmetc` |
| 50 | data | `if (i_exist .or. in_init%soil_plant_ini /= "null") then > do > do ii = 1, imax > if (bsn_cc%nam1 == 0) then / else` | `sol_plt_ini(ii)%name`, `sol_plt_ini(ii)%sw_frac`, `sol_plt_ini(ii)%nutc`, `sol_plt_ini(ii)%pestc`, `sol_plt_ini(ii)%pathc`, `sol_plt_ini(ii)%saltc`, `sol_plt_ini(ii)%hmetc`, `sol_plt_ini(ii)%csc` |

### `temperature.cha`

- Review needed: yes
- Reader procedures changed: no
- Read-block count changed: no
- Read conditions changed: yes
- Base flattened read order: `titldum`, `header`, `w_temp`
- Candidate flattened read order: `titldum`, `header`, `titldum`, `titldum`, `header`, `titldum`, `w_temp(ich_temp)`

#### Read-order edits

- `replace` at base index 2 / candidate index 2: removed `w_temp`; added `titldum`, `titldum`, `header`, `titldum`, `w_temp(ich_temp)`

#### Base read structure

- Schema status: `certified`
- Review needed: no
- Source expression(s): `in_cha%temp`, `temperature.cha`

- Procedure: `ch_read_temp`
- Reader: `ch_read_temp.f90`
- Match: source_input
- Resolved default filename(s): `temperature.cha`
- Source filename expression(s): `in_cha%temp`, `temperature.cha`
- Open: line 25, file expression `in_cha%temp`, parser value `temperature.cha`, condition `if (.not. i_exist .or. in_cha%temp == "null") then / else > do`

| Line | Role | Condition | Fields read |
| --- | --- | --- | --- |
| 26 | title | `if (.not. i_exist .or. in_cha%temp == "null") then / else > do` | `titldum` |
| 28 | header | `if (.not. i_exist .or. in_cha%temp == "null") then / else > do` | `header` |
| 30 | data | `if (.not. i_exist .or. in_cha%temp == "null") then / else > do` | `w_temp` |


#### Candidate read structure

- Schema status: `certified`
- Review needed: no
- Source expression(s): `in_cha%temp`, `temperature.cha`

- Procedure: `ch_read_temp`
- Reader: `ch_read_temp.f90`
- Match: source_input
- Resolved default filename(s): `temperature.cha`
- Source filename expression(s): `in_cha%temp`, `temperature.cha`
- Open: line 27, file expression `in_cha%temp`, parser value `temperature.cha`, condition `if (.not. i_exist .or. in_cha%temp == "null") then / else > do`

| Line | Role | Condition | Fields read |
| --- | --- | --- | --- |
| 28 | title | `if (.not. i_exist .or. in_cha%temp == "null") then / else > do` | `titldum` |
| 30 | header | `if (.not. i_exist .or. in_cha%temp == "null") then / else > do` | `header` |
| 34 | title | `if (.not. i_exist .or. in_cha%temp == "null") then / else > do > do while (eof == 0)` | `titldum` |
| 45 | title | `if (.not. i_exist .or. in_cha%temp == "null") then / else > do` | `titldum` |
| 47 | header | `if (.not. i_exist .or. in_cha%temp == "null") then / else > do` | `header` |
| 51 | title | `if (.not. i_exist .or. in_cha%temp == "null") then / else > do > do ich_temp = 1, db_mx%w_temp` | `titldum` |
| 54 | data | `if (.not. i_exist .or. in_cha%temp == "null") then / else > do > do ich_temp = 1, db_mx%w_temp` | `w_temp(ich_temp)` |

### `water_allocation.wro`

- Review needed: yes
- Reader procedures changed: no
- Read-block count changed: no
- Read conditions changed: yes
- Base flattened read order: `titldum`, `imax`, `header`, `wallo(iwro)%name`, `wallo(iwro)%rule_typ`, `wallo(iwro)%src_obs`, `wallo(iwro)%dmd_obs`, `wallo(iwro)%cha_ob`, `header`, `i`, `k`, `wallo(iwro)%src(i)%ob_typ`, `k`, `wallo(iwro)%src(i)%ob_typ`, `wallo(iwro)%src(i)%div_rec`, `k`, `wallo(iwro)%src(i)%ob_typ`, `wallo(iwro)%src(i)%ob_num`, `wallo(iwro)%src(i)%limit_mon`, `header`, `i`, `k`, `wallo(iwro)%dmd(i)%ob_typ`, `wallo(iwro)%dmd(i)%ob_num`, `wallo(iwro)%dmd(i)%withdr`, `wallo(iwro)%dmd(i)%amount`, `wallo(iwro)%dmd(i)%right`, `wallo(iwro)%dmd(i)%treat_typ`, `wallo(iwro)%dmd(i)%treatment`, `wallo(iwro)%dmd(i)%rcv_ob`, `wallo(iwro)%dmd(i)%rcv_num`, `wallo(iwro)%dmd(i)%rcv_dtl`, `num_objs`, `k`, `wallo(iwro)%dmd(i)%ob_typ`, `wallo(iwro)%dmd(i)%ob_num`, `wallo(iwro)%dmd(i)%withdr`, `wallo(iwro)%dmd(i)%amount`, `wallo(iwro)%dmd(i)%right`, `wallo(iwro)%dmd(i)%treat_typ`, `wallo(iwro)%dmd(i)%treatment`, `wallo(iwro)%dmd(i)%rcv_ob`, `wallo(iwro)%dmd(i)%rcv_num`, `wallo(iwro)%dmd(i)%rcv_dtl`, `wallo(iwro)%dmd(i)%dmd_src_obs`, `(wallo(iwro)%dmd(i)%src(isrc), isrc = 1, num_objs)`, `div_delay`
- Candidate flattened read order: `titldum`, `imax`, `header`, `wallo(iwro)%name`, `wallo(iwro)%rule_typ`, `wallo(iwro)%trn_obs`, `header`, `i`, `k`, `wallo(iwro)%trn(i)%trn_typ`, `wallo(iwro)%trn(i)%trn_typ_name`, `wallo(iwro)%trn(i)%amount`, `wallo(iwro)%trn(i)%right`, `wallo(iwro)%trn(i)%src_num`, `k`, `wallo(iwro)%trn(i)%trn_typ`, `wallo(iwro)%trn(i)%trn_typ_name`, `wallo(iwro)%trn(i)%amount`, `wallo(iwro)%trn(i)%right`, `wallo(iwro)%trn(i)%src_num`, `wallo(iwro)%trn(i)%dtbl_src`, `(wallo(iwro)%trn(i)%src(isrc), isrc = 1, num_src)`, `wallo(iwro)%trn(i)%rcv`

#### Read-order edits

- `replace` at base index 5 / candidate index 5: removed `wallo(iwro)%src_obs`, `wallo(iwro)%dmd_obs`, `wallo(iwro)%cha_ob`; added `wallo(iwro)%trn_obs`
- `replace` at base index 11 / candidate index 9: removed `wallo(iwro)%src(i)%ob_typ`; added `wallo(iwro)%trn(i)%trn_typ`, `wallo(iwro)%trn(i)%trn_typ_name`, `wallo(iwro)%trn(i)%amount`, `wallo(iwro)%trn(i)%right`, `wallo(iwro)%trn(i)%src_num`
- `replace` at base index 13 / candidate index 15: removed `wallo(iwro)%src(i)%ob_typ`, `wallo(iwro)%src(i)%div_rec`, `k`, `wallo(iwro)%src(i)%ob_typ`, `wallo(iwro)%src(i)%ob_num`, `wallo(iwro)%src(i)%limit_mon`, `header`, `i`, `k`, `wallo(iwro)%dmd(i)%ob_typ`, `wallo(iwro)%dmd(i)%ob_num`, `wallo(iwro)%dmd(i)%withdr`, `wallo(iwro)%dmd(i)%amount`, `wallo(iwro)%dmd(i)%right`, `wallo(iwro)%dmd(i)%treat_typ`, `wallo(iwro)%dmd(i)%treatment`, `wallo(iwro)%dmd(i)%rcv_ob`, `wallo(iwro)%dmd(i)%rcv_num`, `wallo(iwro)%dmd(i)%rcv_dtl`, `num_objs`, `k`, `wallo(iwro)%dmd(i)%ob_typ`, `wallo(iwro)%dmd(i)%ob_num`, `wallo(iwro)%dmd(i)%withdr`, `wallo(iwro)%dmd(i)%amount`, `wallo(iwro)%dmd(i)%right`, `wallo(iwro)%dmd(i)%treat_typ`, `wallo(iwro)%dmd(i)%treatment`, `wallo(iwro)%dmd(i)%rcv_ob`, `wallo(iwro)%dmd(i)%rcv_num`, `wallo(iwro)%dmd(i)%rcv_dtl`, `wallo(iwro)%dmd(i)%dmd_src_obs`, `(wallo(iwro)%dmd(i)%src(isrc), isrc = 1, num_objs)`, `div_delay`; added `wallo(iwro)%trn(i)%trn_typ`, `wallo(iwro)%trn(i)%trn_typ_name`, `wallo(iwro)%trn(i)%amount`, `wallo(iwro)%trn(i)%right`, `wallo(iwro)%trn(i)%src_num`, `wallo(iwro)%trn(i)%dtbl_src`, `(wallo(iwro)%trn(i)%src(isrc), isrc = 1, num_src)`, `wallo(iwro)%trn(i)%rcv`

#### Base read structure

- Schema status: `certified`
- Review needed: no
- Source expression(s): `in_watrts%transfer_wro`, `water_allocation.wro`

- Procedure: `water_allocation_read`
- Reader: `water_allocation_read.f90`
- Match: source_input
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


#### Candidate read structure

- Schema status: `certified`
- Review needed: no
- Source expression(s): `in_watrts%transfer_wro`, `water_allocation.wro`

- Procedure: `water_allocation_read`
- Reader: `water_allocation_read.f90`
- Match: source_input
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


## Possible renames or replacements

- `gwflow.canals` -> `cell_sol.gw`: same reader procedure: gwflow_read. **Human review required; this is not asserted as a rename.**
- `gwflow.canals` -> `cellcon.gw`: same reader procedure: gwflow_read. **Human review required; this is not asserted as a rename.**
- `gwflow.canals` -> `cells.gw`: same reader procedure: gwflow_read. **Human review required; this is not asserted as a rename.**
- `gwflow.canals` -> `codes.gw`: same reader procedure: gwflow_read. **Human review required; this is not asserted as a rename.**
- `gwflow.canals` -> `floodplain.gw`: same reader procedure: gwflow_read. **Human review required; this is not asserted as a rename.**
- `gwflow.canals` -> `gwflow_canal.con`: same reader procedure: gwflow_read. **Human review required; this is not asserted as a rename.**
- `gwflow.canals` -> `hru_pump.gw`: same reader procedure: gwflow_read. **Human review required; this is not asserted as a rename.**
- `gwflow.canals` -> `hrucell.gw`: same reader procedure: gwflow_read. **Human review required; this is not asserted as a rename.**
- `gwflow.canals` -> `lsucell.gw`: same reader procedure: gwflow_read. **Human review required; this is not asserted as a rename.**
- `gwflow.canals` -> `minerals.gw`: same reader procedure: gwflow_read. **Human review required; this is not asserted as a rename.**
- `gwflow.canals` -> `outputs.gw`: same reader procedure: gwflow_read. **Human review required; this is not asserted as a rename.**
- `gwflow.canals` -> `phreato.gw`: same reader procedure: gwflow_read. **Human review required; this is not asserted as a rename.**
- `gwflow.canals` -> `phreato_cell.gw`: same reader procedure: gwflow_read. **Human review required; this is not asserted as a rename.**
- `gwflow.canals` -> `pond_cell.gw`: same reader procedure: gwflow_read. **Human review required; this is not asserted as a rename.**
- `gwflow.canals` -> `pond_div.gw`: same reader procedure: gwflow_read. **Human review required; this is not asserted as a rename.**
- `gwflow.canals` -> `ponds.gw`: same reader procedure: gwflow_read. **Human review required; this is not asserted as a rename.**
- `gwflow.canals` -> `pumpex.gw`: same reader procedure: gwflow_read. **Human review required; this is not asserted as a rename.**
- `gwflow.canals` -> `rescell.gw`: same reader procedure: gwflow_read. **Human review required; this is not asserted as a rename.**
- `gwflow.canals` -> `solute.gw`: same reader procedure: gwflow_read. **Human review required; this is not asserted as a rename.**
- `gwflow.canals` -> `sw_group.gw`: same reader procedure: gwflow_read. **Human review required; this is not asserted as a rename.**
- `gwflow.canals` -> `tile.gw`: same reader procedure: gwflow_read. **Human review required; this is not asserted as a rename.**
- `gwflow.canals` -> `transit.gw`: same reader procedure: gwflow_read. **Human review required; this is not asserted as a rename.**
- `gwflow.canals` -> `tvheads.gw`: same reader procedure: gwflow_read. **Human review required; this is not asserted as a rename.**
- `gwflow.canals` -> `zones.gw`: same reader procedure: gwflow_read. **Human review required; this is not asserted as a rename.**
- `gwflow.cellhru` -> `cell_sol.gw`: same reader procedure: gwflow_read. **Human review required; this is not asserted as a rename.**
- `gwflow.cellhru` -> `cellcon.gw`: same reader procedure: gwflow_read. **Human review required; this is not asserted as a rename.**
- `gwflow.cellhru` -> `cells.gw`: same reader procedure: gwflow_read. **Human review required; this is not asserted as a rename.**
- `gwflow.cellhru` -> `codes.gw`: same reader procedure: gwflow_read. **Human review required; this is not asserted as a rename.**
- `gwflow.cellhru` -> `floodplain.gw`: same reader procedure: gwflow_read. **Human review required; this is not asserted as a rename.**
- `gwflow.cellhru` -> `gwflow_canal.con`: same reader procedure: gwflow_read. **Human review required; this is not asserted as a rename.**
- `gwflow.cellhru` -> `hru_pump.gw`: same reader procedure: gwflow_read. **Human review required; this is not asserted as a rename.**
- `gwflow.cellhru` -> `hrucell.gw`: same reader procedure: gwflow_read. **Human review required; this is not asserted as a rename.**
- `gwflow.cellhru` -> `lsucell.gw`: same reader procedure: gwflow_read. **Human review required; this is not asserted as a rename.**
- `gwflow.cellhru` -> `minerals.gw`: same reader procedure: gwflow_read. **Human review required; this is not asserted as a rename.**
- `gwflow.cellhru` -> `outputs.gw`: same reader procedure: gwflow_read. **Human review required; this is not asserted as a rename.**
- `gwflow.cellhru` -> `phreato.gw`: same reader procedure: gwflow_read. **Human review required; this is not asserted as a rename.**
- `gwflow.cellhru` -> `phreato_cell.gw`: same reader procedure: gwflow_read. **Human review required; this is not asserted as a rename.**
- `gwflow.cellhru` -> `pond_cell.gw`: same reader procedure: gwflow_read. **Human review required; this is not asserted as a rename.**
- `gwflow.cellhru` -> `pond_div.gw`: same reader procedure: gwflow_read. **Human review required; this is not asserted as a rename.**
- `gwflow.cellhru` -> `ponds.gw`: same reader procedure: gwflow_read. **Human review required; this is not asserted as a rename.**
- `gwflow.cellhru` -> `pumpex.gw`: same reader procedure: gwflow_read. **Human review required; this is not asserted as a rename.**
- `gwflow.cellhru` -> `rescell.gw`: same reader procedure: gwflow_read. **Human review required; this is not asserted as a rename.**
- `gwflow.cellhru` -> `solute.gw`: same reader procedure: gwflow_read. **Human review required; this is not asserted as a rename.**
- `gwflow.cellhru` -> `sw_group.gw`: same reader procedure: gwflow_read. **Human review required; this is not asserted as a rename.**
- `gwflow.cellhru` -> `tile.gw`: same reader procedure: gwflow_read. **Human review required; this is not asserted as a rename.**
- `gwflow.cellhru` -> `transit.gw`: same reader procedure: gwflow_read. **Human review required; this is not asserted as a rename.**
- `gwflow.cellhru` -> `tvheads.gw`: same reader procedure: gwflow_read. **Human review required; this is not asserted as a rename.**
- `gwflow.cellhru` -> `zones.gw`: same reader procedure: gwflow_read. **Human review required; this is not asserted as a rename.**
- `gwflow.chancells` -> `chan_depth.gw`: same reader procedure: gwflow_chan_read. **Human review required; this is not asserted as a rename.**
- `gwflow.chancells` -> `chancell.gw`: same reader procedure: basin_read_objs, gwflow_chan_read; similar read-field order. **Human review required; this is not asserted as a rename.**
- `gwflow.floodplain` -> `cell_sol.gw`: same reader procedure: gwflow_read. **Human review required; this is not asserted as a rename.**
- `gwflow.floodplain` -> `cellcon.gw`: same reader procedure: gwflow_read. **Human review required; this is not asserted as a rename.**
- `gwflow.floodplain` -> `cells.gw`: same reader procedure: gwflow_read. **Human review required; this is not asserted as a rename.**
- `gwflow.floodplain` -> `codes.gw`: same reader procedure: gwflow_read. **Human review required; this is not asserted as a rename.**
- `gwflow.floodplain` -> `floodplain.gw`: same reader procedure: gwflow_read; similar read-field order. **Human review required; this is not asserted as a rename.**
- `gwflow.floodplain` -> `gwflow_canal.con`: same reader procedure: gwflow_read. **Human review required; this is not asserted as a rename.**
- `gwflow.floodplain` -> `hru_pump.gw`: same reader procedure: gwflow_read. **Human review required; this is not asserted as a rename.**
- `gwflow.floodplain` -> `hrucell.gw`: same reader procedure: gwflow_read. **Human review required; this is not asserted as a rename.**
- `gwflow.floodplain` -> `lsucell.gw`: same reader procedure: gwflow_read. **Human review required; this is not asserted as a rename.**
- `gwflow.floodplain` -> `minerals.gw`: same reader procedure: gwflow_read. **Human review required; this is not asserted as a rename.**
- `gwflow.floodplain` -> `outputs.gw`: same reader procedure: gwflow_read. **Human review required; this is not asserted as a rename.**
- `gwflow.floodplain` -> `phreato.gw`: same reader procedure: gwflow_read. **Human review required; this is not asserted as a rename.**
- `gwflow.floodplain` -> `phreato_cell.gw`: same reader procedure: gwflow_read. **Human review required; this is not asserted as a rename.**
- `gwflow.floodplain` -> `pond_cell.gw`: same reader procedure: gwflow_read. **Human review required; this is not asserted as a rename.**
- `gwflow.floodplain` -> `pond_div.gw`: same reader procedure: gwflow_read. **Human review required; this is not asserted as a rename.**
- `gwflow.floodplain` -> `ponds.gw`: same reader procedure: gwflow_read. **Human review required; this is not asserted as a rename.**
- `gwflow.floodplain` -> `pumpex.gw`: same reader procedure: gwflow_read. **Human review required; this is not asserted as a rename.**
- `gwflow.floodplain` -> `rescell.gw`: same reader procedure: gwflow_read. **Human review required; this is not asserted as a rename.**
- `gwflow.floodplain` -> `solute.gw`: same reader procedure: gwflow_read. **Human review required; this is not asserted as a rename.**
- `gwflow.floodplain` -> `sw_group.gw`: same reader procedure: gwflow_read. **Human review required; this is not asserted as a rename.**
- `gwflow.floodplain` -> `tile.gw`: same reader procedure: gwflow_read. **Human review required; this is not asserted as a rename.**
- `gwflow.floodplain` -> `transit.gw`: same reader procedure: gwflow_read. **Human review required; this is not asserted as a rename.**
- `gwflow.floodplain` -> `tvheads.gw`: same reader procedure: gwflow_read. **Human review required; this is not asserted as a rename.**
- `gwflow.floodplain` -> `zones.gw`: same reader procedure: gwflow_read. **Human review required; this is not asserted as a rename.**
- `gwflow.hru_pump_observe` -> `cell_sol.gw`: same reader procedure: gwflow_read. **Human review required; this is not asserted as a rename.**
- `gwflow.hru_pump_observe` -> `cellcon.gw`: same reader procedure: gwflow_read. **Human review required; this is not asserted as a rename.**
- `gwflow.hru_pump_observe` -> `cells.gw`: same reader procedure: gwflow_read. **Human review required; this is not asserted as a rename.**
- `gwflow.hru_pump_observe` -> `codes.gw`: same reader procedure: gwflow_read. **Human review required; this is not asserted as a rename.**
- `gwflow.hru_pump_observe` -> `floodplain.gw`: same reader procedure: gwflow_read. **Human review required; this is not asserted as a rename.**
- `gwflow.hru_pump_observe` -> `gwflow_canal.con`: same reader procedure: gwflow_read. **Human review required; this is not asserted as a rename.**
- `gwflow.hru_pump_observe` -> `hru_pump.gw`: same reader procedure: gwflow_read; similar read-field order. **Human review required; this is not asserted as a rename.**
- `gwflow.hru_pump_observe` -> `hrucell.gw`: same reader procedure: gwflow_read. **Human review required; this is not asserted as a rename.**
- `gwflow.hru_pump_observe` -> `lsucell.gw`: same reader procedure: gwflow_read. **Human review required; this is not asserted as a rename.**
- `gwflow.hru_pump_observe` -> `minerals.gw`: same reader procedure: gwflow_read. **Human review required; this is not asserted as a rename.**
- `gwflow.hru_pump_observe` -> `outputs.gw`: same reader procedure: gwflow_read. **Human review required; this is not asserted as a rename.**
- `gwflow.hru_pump_observe` -> `phreato.gw`: same reader procedure: gwflow_read. **Human review required; this is not asserted as a rename.**
- `gwflow.hru_pump_observe` -> `phreato_cell.gw`: same reader procedure: gwflow_read. **Human review required; this is not asserted as a rename.**
- `gwflow.hru_pump_observe` -> `pond_cell.gw`: same reader procedure: gwflow_read. **Human review required; this is not asserted as a rename.**
- `gwflow.hru_pump_observe` -> `pond_div.gw`: same reader procedure: gwflow_read. **Human review required; this is not asserted as a rename.**
- `gwflow.hru_pump_observe` -> `ponds.gw`: same reader procedure: gwflow_read. **Human review required; this is not asserted as a rename.**
- `gwflow.hru_pump_observe` -> `pumpex.gw`: same reader procedure: gwflow_read. **Human review required; this is not asserted as a rename.**
- `gwflow.hru_pump_observe` -> `rescell.gw`: same reader procedure: gwflow_read. **Human review required; this is not asserted as a rename.**
- `gwflow.hru_pump_observe` -> `solute.gw`: same reader procedure: gwflow_read. **Human review required; this is not asserted as a rename.**
- `gwflow.hru_pump_observe` -> `sw_group.gw`: same reader procedure: gwflow_read. **Human review required; this is not asserted as a rename.**
- `gwflow.hru_pump_observe` -> `tile.gw`: same reader procedure: gwflow_read. **Human review required; this is not asserted as a rename.**
- `gwflow.hru_pump_observe` -> `transit.gw`: same reader procedure: gwflow_read. **Human review required; this is not asserted as a rename.**
- `gwflow.hru_pump_observe` -> `tvheads.gw`: same reader procedure: gwflow_read. **Human review required; this is not asserted as a rename.**
- `gwflow.hru_pump_observe` -> `zones.gw`: same reader procedure: gwflow_read. **Human review required; this is not asserted as a rename.**
- `gwflow.hrucell` -> `cell_sol.gw`: same reader procedure: gwflow_read. **Human review required; this is not asserted as a rename.**
- `gwflow.hrucell` -> `cellcon.gw`: same reader procedure: gwflow_read. **Human review required; this is not asserted as a rename.**
- `gwflow.hrucell` -> `cells.gw`: same reader procedure: gwflow_read. **Human review required; this is not asserted as a rename.**
- `gwflow.hrucell` -> `codes.gw`: same reader procedure: gwflow_read. **Human review required; this is not asserted as a rename.**
- `gwflow.hrucell` -> `floodplain.gw`: same reader procedure: gwflow_read. **Human review required; this is not asserted as a rename.**
- `gwflow.hrucell` -> `gwflow_canal.con`: same reader procedure: gwflow_read. **Human review required; this is not asserted as a rename.**
- `gwflow.hrucell` -> `hru_pump.gw`: same reader procedure: gwflow_read. **Human review required; this is not asserted as a rename.**
- `gwflow.hrucell` -> `hrucell.gw`: same reader procedure: gwflow_read; similar read-field order. **Human review required; this is not asserted as a rename.**
- `gwflow.hrucell` -> `lsucell.gw`: same reader procedure: gwflow_read. **Human review required; this is not asserted as a rename.**
- `gwflow.hrucell` -> `minerals.gw`: same reader procedure: gwflow_read. **Human review required; this is not asserted as a rename.**
- `gwflow.hrucell` -> `outputs.gw`: same reader procedure: gwflow_read. **Human review required; this is not asserted as a rename.**
- `gwflow.hrucell` -> `phreato.gw`: same reader procedure: gwflow_read. **Human review required; this is not asserted as a rename.**
- `gwflow.hrucell` -> `phreato_cell.gw`: same reader procedure: gwflow_read. **Human review required; this is not asserted as a rename.**
- `gwflow.hrucell` -> `pond_cell.gw`: same reader procedure: gwflow_read. **Human review required; this is not asserted as a rename.**
- `gwflow.hrucell` -> `pond_div.gw`: same reader procedure: gwflow_read. **Human review required; this is not asserted as a rename.**
- `gwflow.hrucell` -> `ponds.gw`: same reader procedure: gwflow_read. **Human review required; this is not asserted as a rename.**
- `gwflow.hrucell` -> `pumpex.gw`: same reader procedure: gwflow_read. **Human review required; this is not asserted as a rename.**
- `gwflow.hrucell` -> `rescell.gw`: same reader procedure: gwflow_read. **Human review required; this is not asserted as a rename.**
- `gwflow.hrucell` -> `solute.gw`: same reader procedure: gwflow_read. **Human review required; this is not asserted as a rename.**
- `gwflow.hrucell` -> `sw_group.gw`: same reader procedure: gwflow_read. **Human review required; this is not asserted as a rename.**
- `gwflow.hrucell` -> `tile.gw`: same reader procedure: gwflow_read. **Human review required; this is not asserted as a rename.**
- `gwflow.hrucell` -> `transit.gw`: same reader procedure: gwflow_read. **Human review required; this is not asserted as a rename.**
- `gwflow.hrucell` -> `tvheads.gw`: same reader procedure: gwflow_read. **Human review required; this is not asserted as a rename.**
- `gwflow.hrucell` -> `zones.gw`: same reader procedure: gwflow_read. **Human review required; this is not asserted as a rename.**
- `gwflow.huc12cell` -> `cell_sol.gw`: same reader procedure: gwflow_read. **Human review required; this is not asserted as a rename.**
- `gwflow.huc12cell` -> `cellcon.gw`: same reader procedure: gwflow_read. **Human review required; this is not asserted as a rename.**
- `gwflow.huc12cell` -> `cells.gw`: same reader procedure: gwflow_read. **Human review required; this is not asserted as a rename.**
- `gwflow.huc12cell` -> `codes.gw`: same reader procedure: gwflow_read. **Human review required; this is not asserted as a rename.**
- `gwflow.huc12cell` -> `floodplain.gw`: same reader procedure: gwflow_read. **Human review required; this is not asserted as a rename.**
- `gwflow.huc12cell` -> `gwflow_canal.con`: same reader procedure: gwflow_read. **Human review required; this is not asserted as a rename.**
- `gwflow.huc12cell` -> `hru_pump.gw`: same reader procedure: gwflow_read. **Human review required; this is not asserted as a rename.**
- `gwflow.huc12cell` -> `hrucell.gw`: same reader procedure: gwflow_read. **Human review required; this is not asserted as a rename.**
- `gwflow.huc12cell` -> `lsucell.gw`: same reader procedure: gwflow_read. **Human review required; this is not asserted as a rename.**
- `gwflow.huc12cell` -> `minerals.gw`: same reader procedure: gwflow_read. **Human review required; this is not asserted as a rename.**
- `gwflow.huc12cell` -> `outputs.gw`: same reader procedure: gwflow_read. **Human review required; this is not asserted as a rename.**
- `gwflow.huc12cell` -> `phreato.gw`: same reader procedure: gwflow_read. **Human review required; this is not asserted as a rename.**
- `gwflow.huc12cell` -> `phreato_cell.gw`: same reader procedure: gwflow_read. **Human review required; this is not asserted as a rename.**
- `gwflow.huc12cell` -> `pond_cell.gw`: same reader procedure: gwflow_read. **Human review required; this is not asserted as a rename.**
- `gwflow.huc12cell` -> `pond_div.gw`: same reader procedure: gwflow_read. **Human review required; this is not asserted as a rename.**
- `gwflow.huc12cell` -> `ponds.gw`: same reader procedure: gwflow_read. **Human review required; this is not asserted as a rename.**
- `gwflow.huc12cell` -> `pumpex.gw`: same reader procedure: gwflow_read. **Human review required; this is not asserted as a rename.**
- `gwflow.huc12cell` -> `rescell.gw`: same reader procedure: gwflow_read. **Human review required; this is not asserted as a rename.**
- `gwflow.huc12cell` -> `solute.gw`: same reader procedure: gwflow_read. **Human review required; this is not asserted as a rename.**
- `gwflow.huc12cell` -> `sw_group.gw`: same reader procedure: gwflow_read. **Human review required; this is not asserted as a rename.**
- `gwflow.huc12cell` -> `tile.gw`: same reader procedure: gwflow_read. **Human review required; this is not asserted as a rename.**
- `gwflow.huc12cell` -> `transit.gw`: same reader procedure: gwflow_read. **Human review required; this is not asserted as a rename.**
- `gwflow.huc12cell` -> `tvheads.gw`: same reader procedure: gwflow_read. **Human review required; this is not asserted as a rename.**
- `gwflow.huc12cell` -> `zones.gw`: same reader procedure: gwflow_read. **Human review required; this is not asserted as a rename.**
- `gwflow.input` -> `cell_sol.gw`: same reader procedure: gwflow_read. **Human review required; this is not asserted as a rename.**
- `gwflow.input` -> `cellcon.gw`: same reader procedure: gwflow_read. **Human review required; this is not asserted as a rename.**
- `gwflow.input` -> `cells.gw`: same reader procedure: gwflow_read. **Human review required; this is not asserted as a rename.**
- `gwflow.input` -> `codes.gw`: same reader procedure: gwflow_read. **Human review required; this is not asserted as a rename.**
- `gwflow.input` -> `floodplain.gw`: same reader procedure: gwflow_read. **Human review required; this is not asserted as a rename.**
- `gwflow.input` -> `gwflow_canal.con`: same reader procedure: gwflow_read. **Human review required; this is not asserted as a rename.**
- `gwflow.input` -> `hru_pump.gw`: same reader procedure: gwflow_read. **Human review required; this is not asserted as a rename.**
- `gwflow.input` -> `hrucell.gw`: same reader procedure: gwflow_read. **Human review required; this is not asserted as a rename.**
- `gwflow.input` -> `lsucell.gw`: same reader procedure: gwflow_read. **Human review required; this is not asserted as a rename.**
- `gwflow.input` -> `minerals.gw`: same reader procedure: gwflow_read. **Human review required; this is not asserted as a rename.**
- `gwflow.input` -> `outputs.gw`: same reader procedure: gwflow_read. **Human review required; this is not asserted as a rename.**
- `gwflow.input` -> `phreato.gw`: same reader procedure: gwflow_read. **Human review required; this is not asserted as a rename.**
- `gwflow.input` -> `phreato_cell.gw`: same reader procedure: gwflow_read. **Human review required; this is not asserted as a rename.**
- `gwflow.input` -> `pond_cell.gw`: same reader procedure: gwflow_read. **Human review required; this is not asserted as a rename.**
- `gwflow.input` -> `pond_div.gw`: same reader procedure: gwflow_read. **Human review required; this is not asserted as a rename.**
- `gwflow.input` -> `ponds.gw`: same reader procedure: gwflow_read. **Human review required; this is not asserted as a rename.**
- `gwflow.input` -> `pumpex.gw`: same reader procedure: gwflow_read. **Human review required; this is not asserted as a rename.**
- `gwflow.input` -> `rescell.gw`: same reader procedure: gwflow_read. **Human review required; this is not asserted as a rename.**
- `gwflow.input` -> `solute.gw`: same reader procedure: gwflow_read. **Human review required; this is not asserted as a rename.**
- `gwflow.input` -> `sw_group.gw`: same reader procedure: gwflow_read. **Human review required; this is not asserted as a rename.**
- `gwflow.input` -> `tile.gw`: same reader procedure: gwflow_read. **Human review required; this is not asserted as a rename.**
- `gwflow.input` -> `transit.gw`: same reader procedure: gwflow_read. **Human review required; this is not asserted as a rename.**
- `gwflow.input` -> `tvheads.gw`: same reader procedure: gwflow_read. **Human review required; this is not asserted as a rename.**
- `gwflow.input` -> `zones.gw`: same reader procedure: gwflow_read. **Human review required; this is not asserted as a rename.**
- `gwflow.lsucell` -> `cell_sol.gw`: same reader procedure: gwflow_read. **Human review required; this is not asserted as a rename.**
- `gwflow.lsucell` -> `cellcon.gw`: same reader procedure: gwflow_read. **Human review required; this is not asserted as a rename.**
- `gwflow.lsucell` -> `cells.gw`: same reader procedure: gwflow_read. **Human review required; this is not asserted as a rename.**
- `gwflow.lsucell` -> `codes.gw`: same reader procedure: gwflow_read. **Human review required; this is not asserted as a rename.**
- `gwflow.lsucell` -> `floodplain.gw`: same reader procedure: gwflow_read. **Human review required; this is not asserted as a rename.**
- `gwflow.lsucell` -> `gwflow_canal.con`: same reader procedure: gwflow_read. **Human review required; this is not asserted as a rename.**
- `gwflow.lsucell` -> `hru_pump.gw`: same reader procedure: gwflow_read. **Human review required; this is not asserted as a rename.**
- `gwflow.lsucell` -> `hrucell.gw`: same reader procedure: gwflow_read. **Human review required; this is not asserted as a rename.**
- `gwflow.lsucell` -> `lsucell.gw`: same reader procedure: gwflow_read; similar read-field order. **Human review required; this is not asserted as a rename.**
- `gwflow.lsucell` -> `minerals.gw`: same reader procedure: gwflow_read. **Human review required; this is not asserted as a rename.**
- `gwflow.lsucell` -> `outputs.gw`: same reader procedure: gwflow_read. **Human review required; this is not asserted as a rename.**
- `gwflow.lsucell` -> `phreato.gw`: same reader procedure: gwflow_read. **Human review required; this is not asserted as a rename.**
- `gwflow.lsucell` -> `phreato_cell.gw`: same reader procedure: gwflow_read. **Human review required; this is not asserted as a rename.**
- `gwflow.lsucell` -> `pond_cell.gw`: same reader procedure: gwflow_read. **Human review required; this is not asserted as a rename.**
- `gwflow.lsucell` -> `pond_div.gw`: same reader procedure: gwflow_read. **Human review required; this is not asserted as a rename.**
- `gwflow.lsucell` -> `ponds.gw`: same reader procedure: gwflow_read. **Human review required; this is not asserted as a rename.**
- `gwflow.lsucell` -> `pumpex.gw`: same reader procedure: gwflow_read. **Human review required; this is not asserted as a rename.**
- `gwflow.lsucell` -> `rescell.gw`: same reader procedure: gwflow_read. **Human review required; this is not asserted as a rename.**
- `gwflow.lsucell` -> `solute.gw`: same reader procedure: gwflow_read. **Human review required; this is not asserted as a rename.**
- `gwflow.lsucell` -> `sw_group.gw`: same reader procedure: gwflow_read. **Human review required; this is not asserted as a rename.**
- `gwflow.lsucell` -> `tile.gw`: same reader procedure: gwflow_read. **Human review required; this is not asserted as a rename.**
- `gwflow.lsucell` -> `transit.gw`: same reader procedure: gwflow_read. **Human review required; this is not asserted as a rename.**
- `gwflow.lsucell` -> `tvheads.gw`: same reader procedure: gwflow_read. **Human review required; this is not asserted as a rename.**
- `gwflow.lsucell` -> `zones.gw`: same reader procedure: gwflow_read. **Human review required; this is not asserted as a rename.**
- `gwflow.pumpex` -> `cell_sol.gw`: same reader procedure: gwflow_read. **Human review required; this is not asserted as a rename.**
- `gwflow.pumpex` -> `cellcon.gw`: same reader procedure: gwflow_read. **Human review required; this is not asserted as a rename.**
- `gwflow.pumpex` -> `cells.gw`: same reader procedure: gwflow_read. **Human review required; this is not asserted as a rename.**
- `gwflow.pumpex` -> `codes.gw`: same reader procedure: gwflow_read. **Human review required; this is not asserted as a rename.**
- `gwflow.pumpex` -> `floodplain.gw`: same reader procedure: gwflow_read. **Human review required; this is not asserted as a rename.**
- `gwflow.pumpex` -> `gwflow_canal.con`: same reader procedure: gwflow_read. **Human review required; this is not asserted as a rename.**
- `gwflow.pumpex` -> `hru_pump.gw`: same reader procedure: gwflow_read. **Human review required; this is not asserted as a rename.**
- `gwflow.pumpex` -> `hrucell.gw`: same reader procedure: gwflow_read. **Human review required; this is not asserted as a rename.**
- `gwflow.pumpex` -> `lsucell.gw`: same reader procedure: gwflow_read. **Human review required; this is not asserted as a rename.**
- `gwflow.pumpex` -> `minerals.gw`: same reader procedure: gwflow_read. **Human review required; this is not asserted as a rename.**
- `gwflow.pumpex` -> `outputs.gw`: same reader procedure: gwflow_read. **Human review required; this is not asserted as a rename.**
- `gwflow.pumpex` -> `phreato.gw`: same reader procedure: gwflow_read. **Human review required; this is not asserted as a rename.**
- `gwflow.pumpex` -> `phreato_cell.gw`: same reader procedure: gwflow_read. **Human review required; this is not asserted as a rename.**
- `gwflow.pumpex` -> `pond_cell.gw`: same reader procedure: gwflow_read. **Human review required; this is not asserted as a rename.**
- `gwflow.pumpex` -> `pond_div.gw`: same reader procedure: gwflow_read. **Human review required; this is not asserted as a rename.**
- `gwflow.pumpex` -> `ponds.gw`: same reader procedure: gwflow_read. **Human review required; this is not asserted as a rename.**
- `gwflow.pumpex` -> `pumpex.gw`: same reader procedure: gwflow_read. **Human review required; this is not asserted as a rename.**
- `gwflow.pumpex` -> `rescell.gw`: same reader procedure: gwflow_read. **Human review required; this is not asserted as a rename.**
- `gwflow.pumpex` -> `solute.gw`: same reader procedure: gwflow_read. **Human review required; this is not asserted as a rename.**
- `gwflow.pumpex` -> `sw_group.gw`: same reader procedure: gwflow_read. **Human review required; this is not asserted as a rename.**
- `gwflow.pumpex` -> `tile.gw`: same reader procedure: gwflow_read. **Human review required; this is not asserted as a rename.**
- `gwflow.pumpex` -> `transit.gw`: same reader procedure: gwflow_read. **Human review required; this is not asserted as a rename.**
- `gwflow.pumpex` -> `tvheads.gw`: same reader procedure: gwflow_read. **Human review required; this is not asserted as a rename.**
- `gwflow.pumpex` -> `zones.gw`: same reader procedure: gwflow_read. **Human review required; this is not asserted as a rename.**
- `gwflow.rescells` -> `cell_sol.gw`: same reader procedure: gwflow_read. **Human review required; this is not asserted as a rename.**
- `gwflow.rescells` -> `cellcon.gw`: same reader procedure: gwflow_read. **Human review required; this is not asserted as a rename.**
- `gwflow.rescells` -> `cells.gw`: same reader procedure: gwflow_read. **Human review required; this is not asserted as a rename.**
- `gwflow.rescells` -> `codes.gw`: same reader procedure: gwflow_read. **Human review required; this is not asserted as a rename.**
- `gwflow.rescells` -> `floodplain.gw`: same reader procedure: gwflow_read. **Human review required; this is not asserted as a rename.**
- `gwflow.rescells` -> `gwflow_canal.con`: same reader procedure: gwflow_read. **Human review required; this is not asserted as a rename.**
- `gwflow.rescells` -> `hru_pump.gw`: same reader procedure: gwflow_read. **Human review required; this is not asserted as a rename.**
- `gwflow.rescells` -> `hrucell.gw`: same reader procedure: gwflow_read. **Human review required; this is not asserted as a rename.**
- `gwflow.rescells` -> `lsucell.gw`: same reader procedure: gwflow_read. **Human review required; this is not asserted as a rename.**
- `gwflow.rescells` -> `minerals.gw`: same reader procedure: gwflow_read. **Human review required; this is not asserted as a rename.**
- `gwflow.rescells` -> `outputs.gw`: same reader procedure: gwflow_read. **Human review required; this is not asserted as a rename.**
- `gwflow.rescells` -> `phreato.gw`: same reader procedure: gwflow_read. **Human review required; this is not asserted as a rename.**
- `gwflow.rescells` -> `phreato_cell.gw`: same reader procedure: gwflow_read. **Human review required; this is not asserted as a rename.**
- `gwflow.rescells` -> `pond_cell.gw`: same reader procedure: gwflow_read. **Human review required; this is not asserted as a rename.**
- `gwflow.rescells` -> `pond_div.gw`: same reader procedure: gwflow_read. **Human review required; this is not asserted as a rename.**
- `gwflow.rescells` -> `ponds.gw`: same reader procedure: gwflow_read. **Human review required; this is not asserted as a rename.**
- `gwflow.rescells` -> `pumpex.gw`: same reader procedure: gwflow_read. **Human review required; this is not asserted as a rename.**
- `gwflow.rescells` -> `rescell.gw`: same reader procedure: gwflow_read; similar read-field order. **Human review required; this is not asserted as a rename.**
- `gwflow.rescells` -> `solute.gw`: same reader procedure: gwflow_read. **Human review required; this is not asserted as a rename.**
- `gwflow.rescells` -> `sw_group.gw`: same reader procedure: gwflow_read. **Human review required; this is not asserted as a rename.**
- `gwflow.rescells` -> `tile.gw`: same reader procedure: gwflow_read. **Human review required; this is not asserted as a rename.**
- `gwflow.rescells` -> `transit.gw`: same reader procedure: gwflow_read. **Human review required; this is not asserted as a rename.**
- `gwflow.rescells` -> `tvheads.gw`: same reader procedure: gwflow_read. **Human review required; this is not asserted as a rename.**
- `gwflow.rescells` -> `zones.gw`: same reader procedure: gwflow_read. **Human review required; this is not asserted as a rename.**
- `gwflow.solutes` -> `cell_sol.gw`: same reader procedure: gwflow_read; similar read-field order. **Human review required; this is not asserted as a rename.**
- `gwflow.solutes` -> `cellcon.gw`: same reader procedure: gwflow_read. **Human review required; this is not asserted as a rename.**
- `gwflow.solutes` -> `cells.gw`: same reader procedure: gwflow_read. **Human review required; this is not asserted as a rename.**
- `gwflow.solutes` -> `codes.gw`: same reader procedure: gwflow_read. **Human review required; this is not asserted as a rename.**
- `gwflow.solutes` -> `floodplain.gw`: same reader procedure: gwflow_read. **Human review required; this is not asserted as a rename.**
- `gwflow.solutes` -> `gwflow_canal.con`: same reader procedure: gwflow_read. **Human review required; this is not asserted as a rename.**
- `gwflow.solutes` -> `hru_pump.gw`: same reader procedure: gwflow_read. **Human review required; this is not asserted as a rename.**
- `gwflow.solutes` -> `hrucell.gw`: same reader procedure: gwflow_read. **Human review required; this is not asserted as a rename.**
- `gwflow.solutes` -> `lsucell.gw`: same reader procedure: gwflow_read. **Human review required; this is not asserted as a rename.**
- `gwflow.solutes` -> `minerals.gw`: same reader procedure: gwflow_read. **Human review required; this is not asserted as a rename.**
- `gwflow.solutes` -> `outputs.gw`: same reader procedure: gwflow_read. **Human review required; this is not asserted as a rename.**
- `gwflow.solutes` -> `phreato.gw`: same reader procedure: gwflow_read. **Human review required; this is not asserted as a rename.**
- `gwflow.solutes` -> `phreato_cell.gw`: same reader procedure: gwflow_read. **Human review required; this is not asserted as a rename.**
- `gwflow.solutes` -> `pond_cell.gw`: same reader procedure: gwflow_read. **Human review required; this is not asserted as a rename.**
- `gwflow.solutes` -> `pond_div.gw`: same reader procedure: gwflow_read. **Human review required; this is not asserted as a rename.**
- `gwflow.solutes` -> `ponds.gw`: same reader procedure: gwflow_read. **Human review required; this is not asserted as a rename.**
- `gwflow.solutes` -> `pumpex.gw`: same reader procedure: gwflow_read. **Human review required; this is not asserted as a rename.**
- `gwflow.solutes` -> `rescell.gw`: same reader procedure: gwflow_read. **Human review required; this is not asserted as a rename.**
- `gwflow.solutes` -> `solute.gw`: same reader procedure: gwflow_read; similar read-field order. **Human review required; this is not asserted as a rename.**
- `gwflow.solutes` -> `sw_group.gw`: same reader procedure: gwflow_read. **Human review required; this is not asserted as a rename.**
- `gwflow.solutes` -> `tile.gw`: same reader procedure: gwflow_read. **Human review required; this is not asserted as a rename.**
- `gwflow.solutes` -> `transit.gw`: same reader procedure: gwflow_read. **Human review required; this is not asserted as a rename.**
- `gwflow.solutes` -> `tvheads.gw`: same reader procedure: gwflow_read. **Human review required; this is not asserted as a rename.**
- `gwflow.solutes` -> `zones.gw`: same reader procedure: gwflow_read. **Human review required; this is not asserted as a rename.**
- `gwflow.solutes.minerals` -> `cell_sol.gw`: same reader procedure: gwflow_read. **Human review required; this is not asserted as a rename.**
- `gwflow.solutes.minerals` -> `cellcon.gw`: same reader procedure: gwflow_read. **Human review required; this is not asserted as a rename.**
- `gwflow.solutes.minerals` -> `cells.gw`: same reader procedure: gwflow_read. **Human review required; this is not asserted as a rename.**
- `gwflow.solutes.minerals` -> `codes.gw`: same reader procedure: gwflow_read. **Human review required; this is not asserted as a rename.**
- `gwflow.solutes.minerals` -> `floodplain.gw`: same reader procedure: gwflow_read. **Human review required; this is not asserted as a rename.**
- `gwflow.solutes.minerals` -> `gwflow_canal.con`: same reader procedure: gwflow_read. **Human review required; this is not asserted as a rename.**
- `gwflow.solutes.minerals` -> `hru_pump.gw`: same reader procedure: gwflow_read. **Human review required; this is not asserted as a rename.**
- `gwflow.solutes.minerals` -> `hrucell.gw`: same reader procedure: gwflow_read. **Human review required; this is not asserted as a rename.**
- `gwflow.solutes.minerals` -> `lsucell.gw`: same reader procedure: gwflow_read. **Human review required; this is not asserted as a rename.**
- `gwflow.solutes.minerals` -> `minerals.gw`: same reader procedure: gwflow_read; similar read-field order. **Human review required; this is not asserted as a rename.**
- `gwflow.solutes.minerals` -> `outputs.gw`: same reader procedure: gwflow_read. **Human review required; this is not asserted as a rename.**
- `gwflow.solutes.minerals` -> `phreato.gw`: same reader procedure: gwflow_read. **Human review required; this is not asserted as a rename.**
- `gwflow.solutes.minerals` -> `phreato_cell.gw`: same reader procedure: gwflow_read. **Human review required; this is not asserted as a rename.**
- `gwflow.solutes.minerals` -> `pond_cell.gw`: same reader procedure: gwflow_read. **Human review required; this is not asserted as a rename.**
- `gwflow.solutes.minerals` -> `pond_div.gw`: same reader procedure: gwflow_read. **Human review required; this is not asserted as a rename.**
- `gwflow.solutes.minerals` -> `ponds.gw`: same reader procedure: gwflow_read. **Human review required; this is not asserted as a rename.**
- `gwflow.solutes.minerals` -> `pumpex.gw`: same reader procedure: gwflow_read. **Human review required; this is not asserted as a rename.**
- `gwflow.solutes.minerals` -> `rescell.gw`: same reader procedure: gwflow_read. **Human review required; this is not asserted as a rename.**
- `gwflow.solutes.minerals` -> `solute.gw`: same reader procedure: gwflow_read. **Human review required; this is not asserted as a rename.**
- `gwflow.solutes.minerals` -> `sw_group.gw`: same reader procedure: gwflow_read. **Human review required; this is not asserted as a rename.**
- `gwflow.solutes.minerals` -> `tile.gw`: same reader procedure: gwflow_read. **Human review required; this is not asserted as a rename.**
- `gwflow.solutes.minerals` -> `transit.gw`: same reader procedure: gwflow_read. **Human review required; this is not asserted as a rename.**
- `gwflow.solutes.minerals` -> `tvheads.gw`: same reader procedure: gwflow_read. **Human review required; this is not asserted as a rename.**
- `gwflow.solutes.minerals` -> `zones.gw`: same reader procedure: gwflow_read. **Human review required; this is not asserted as a rename.**
- `gwflow.streamobs` -> `cell_sol.gw`: same reader procedure: gwflow_read. **Human review required; this is not asserted as a rename.**
- `gwflow.streamobs` -> `cellcon.gw`: same reader procedure: gwflow_read. **Human review required; this is not asserted as a rename.**
- `gwflow.streamobs` -> `cells.gw`: same reader procedure: gwflow_read. **Human review required; this is not asserted as a rename.**
- `gwflow.streamobs` -> `codes.gw`: same reader procedure: gwflow_read. **Human review required; this is not asserted as a rename.**
- `gwflow.streamobs` -> `floodplain.gw`: same reader procedure: gwflow_read. **Human review required; this is not asserted as a rename.**
- `gwflow.streamobs` -> `gwflow_canal.con`: same reader procedure: gwflow_read. **Human review required; this is not asserted as a rename.**
- `gwflow.streamobs` -> `hru_pump.gw`: same reader procedure: gwflow_read. **Human review required; this is not asserted as a rename.**
- `gwflow.streamobs` -> `hrucell.gw`: same reader procedure: gwflow_read. **Human review required; this is not asserted as a rename.**
- `gwflow.streamobs` -> `lsucell.gw`: same reader procedure: gwflow_read. **Human review required; this is not asserted as a rename.**
- `gwflow.streamobs` -> `minerals.gw`: same reader procedure: gwflow_read. **Human review required; this is not asserted as a rename.**
- `gwflow.streamobs` -> `outputs.gw`: same reader procedure: gwflow_read. **Human review required; this is not asserted as a rename.**
- `gwflow.streamobs` -> `phreato.gw`: same reader procedure: gwflow_read. **Human review required; this is not asserted as a rename.**
- `gwflow.streamobs` -> `phreato_cell.gw`: same reader procedure: gwflow_read. **Human review required; this is not asserted as a rename.**
- `gwflow.streamobs` -> `pond_cell.gw`: same reader procedure: gwflow_read. **Human review required; this is not asserted as a rename.**
- `gwflow.streamobs` -> `pond_div.gw`: same reader procedure: gwflow_read. **Human review required; this is not asserted as a rename.**
- `gwflow.streamobs` -> `ponds.gw`: same reader procedure: gwflow_read. **Human review required; this is not asserted as a rename.**
- `gwflow.streamobs` -> `pumpex.gw`: same reader procedure: gwflow_read. **Human review required; this is not asserted as a rename.**
- `gwflow.streamobs` -> `rescell.gw`: same reader procedure: gwflow_read. **Human review required; this is not asserted as a rename.**
- `gwflow.streamobs` -> `solute.gw`: same reader procedure: gwflow_read. **Human review required; this is not asserted as a rename.**
- `gwflow.streamobs` -> `sw_group.gw`: same reader procedure: gwflow_read. **Human review required; this is not asserted as a rename.**
- `gwflow.streamobs` -> `tile.gw`: same reader procedure: gwflow_read. **Human review required; this is not asserted as a rename.**
- `gwflow.streamobs` -> `transit.gw`: same reader procedure: gwflow_read. **Human review required; this is not asserted as a rename.**
- `gwflow.streamobs` -> `tvheads.gw`: same reader procedure: gwflow_read. **Human review required; this is not asserted as a rename.**
- `gwflow.streamobs` -> `zones.gw`: same reader procedure: gwflow_read. **Human review required; this is not asserted as a rename.**
- `gwflow.tiles` -> `cell_sol.gw`: same reader procedure: gwflow_read. **Human review required; this is not asserted as a rename.**
- `gwflow.tiles` -> `cellcon.gw`: same reader procedure: gwflow_read. **Human review required; this is not asserted as a rename.**
- `gwflow.tiles` -> `cells.gw`: same reader procedure: gwflow_read. **Human review required; this is not asserted as a rename.**
- `gwflow.tiles` -> `codes.gw`: same reader procedure: gwflow_read. **Human review required; this is not asserted as a rename.**
- `gwflow.tiles` -> `floodplain.gw`: same reader procedure: gwflow_read. **Human review required; this is not asserted as a rename.**
- `gwflow.tiles` -> `gwflow_canal.con`: same reader procedure: gwflow_read. **Human review required; this is not asserted as a rename.**
- `gwflow.tiles` -> `hru_pump.gw`: same reader procedure: gwflow_read. **Human review required; this is not asserted as a rename.**
- `gwflow.tiles` -> `hrucell.gw`: same reader procedure: gwflow_read. **Human review required; this is not asserted as a rename.**
- `gwflow.tiles` -> `lsucell.gw`: same reader procedure: gwflow_read. **Human review required; this is not asserted as a rename.**
- `gwflow.tiles` -> `minerals.gw`: same reader procedure: gwflow_read. **Human review required; this is not asserted as a rename.**
- `gwflow.tiles` -> `outputs.gw`: same reader procedure: gwflow_read. **Human review required; this is not asserted as a rename.**
- `gwflow.tiles` -> `phreato.gw`: same reader procedure: gwflow_read. **Human review required; this is not asserted as a rename.**
- `gwflow.tiles` -> `phreato_cell.gw`: same reader procedure: gwflow_read. **Human review required; this is not asserted as a rename.**
- `gwflow.tiles` -> `pond_cell.gw`: same reader procedure: gwflow_read. **Human review required; this is not asserted as a rename.**
- `gwflow.tiles` -> `pond_div.gw`: same reader procedure: gwflow_read. **Human review required; this is not asserted as a rename.**
- `gwflow.tiles` -> `ponds.gw`: same reader procedure: gwflow_read. **Human review required; this is not asserted as a rename.**
- `gwflow.tiles` -> `pumpex.gw`: same reader procedure: gwflow_read. **Human review required; this is not asserted as a rename.**
- `gwflow.tiles` -> `rescell.gw`: same reader procedure: gwflow_read. **Human review required; this is not asserted as a rename.**
- `gwflow.tiles` -> `solute.gw`: same reader procedure: gwflow_read. **Human review required; this is not asserted as a rename.**
- `gwflow.tiles` -> `sw_group.gw`: same reader procedure: gwflow_read. **Human review required; this is not asserted as a rename.**
- `gwflow.tiles` -> `tile.gw`: same reader procedure: gwflow_read; similar read-field order. **Human review required; this is not asserted as a rename.**
- `gwflow.tiles` -> `transit.gw`: same reader procedure: gwflow_read. **Human review required; this is not asserted as a rename.**
- `gwflow.tiles` -> `tvheads.gw`: same reader procedure: gwflow_read. **Human review required; this is not asserted as a rename.**
- `gwflow.tiles` -> `zones.gw`: same reader procedure: gwflow_read. **Human review required; this is not asserted as a rename.**
- `out.key` -> `cell_sol.gw`: same reader procedure: gwflow_read. **Human review required; this is not asserted as a rename.**
- `out.key` -> `cellcon.gw`: same reader procedure: gwflow_read. **Human review required; this is not asserted as a rename.**
- `out.key` -> `cells.gw`: same reader procedure: gwflow_read. **Human review required; this is not asserted as a rename.**
- `out.key` -> `codes.gw`: same reader procedure: gwflow_read. **Human review required; this is not asserted as a rename.**
- `out.key` -> `floodplain.gw`: same reader procedure: gwflow_read. **Human review required; this is not asserted as a rename.**
- `out.key` -> `gwflow_canal.con`: same reader procedure: gwflow_read. **Human review required; this is not asserted as a rename.**
- `out.key` -> `hru_pump.gw`: same reader procedure: gwflow_read. **Human review required; this is not asserted as a rename.**
- `out.key` -> `hrucell.gw`: same reader procedure: gwflow_read. **Human review required; this is not asserted as a rename.**
- `out.key` -> `lsucell.gw`: same reader procedure: gwflow_read. **Human review required; this is not asserted as a rename.**
- `out.key` -> `minerals.gw`: same reader procedure: gwflow_read. **Human review required; this is not asserted as a rename.**
- `out.key` -> `outputs.gw`: same reader procedure: gwflow_read. **Human review required; this is not asserted as a rename.**
- `out.key` -> `phreato.gw`: same reader procedure: gwflow_read. **Human review required; this is not asserted as a rename.**
- `out.key` -> `phreato_cell.gw`: same reader procedure: gwflow_read. **Human review required; this is not asserted as a rename.**
- `out.key` -> `pond_cell.gw`: same reader procedure: gwflow_read. **Human review required; this is not asserted as a rename.**
- `out.key` -> `pond_div.gw`: same reader procedure: gwflow_read. **Human review required; this is not asserted as a rename.**
- `out.key` -> `ponds.gw`: same reader procedure: gwflow_read. **Human review required; this is not asserted as a rename.**
- `out.key` -> `pumpex.gw`: same reader procedure: gwflow_read. **Human review required; this is not asserted as a rename.**
- `out.key` -> `rescell.gw`: same reader procedure: gwflow_read. **Human review required; this is not asserted as a rename.**
- `out.key` -> `solute.gw`: same reader procedure: gwflow_read. **Human review required; this is not asserted as a rename.**
- `out.key` -> `sw_group.gw`: same reader procedure: gwflow_read. **Human review required; this is not asserted as a rename.**
- `out.key` -> `tile.gw`: same reader procedure: gwflow_read. **Human review required; this is not asserted as a rename.**
- `out.key` -> `transit.gw`: same reader procedure: gwflow_read. **Human review required; this is not asserted as a rename.**
- `out.key` -> `tvheads.gw`: same reader procedure: gwflow_read. **Human review required; this is not asserted as a rename.**
- `out.key` -> `zones.gw`: same reader procedure: gwflow_read. **Human review required; this is not asserted as a rename.**

## Unresolved opened input filenames

The candidate contains 27 unresolved runtime filename expression(s); 2 were introduced by this comparison. Only newly introduced expressions are expanded below.
### `get_num_data_lines` at `utils.f90`

- Reason: opened input filename could not be resolved
- Expression(s): `self%file_name`
- Procedure: `get_num_data_lines`
- Reader: `utils.f90`
- Match: source_input
- Source filename expression(s): `self%file_name`
- Open: line 562, file expression `self%file_name`, parser value `self%file_name`, condition `None`

| Line | Role | Condition | Fields read |
| --- | --- | --- | --- |
| 565 | data | `if (self%start_row_numbr == 1) then` | `self%titldum` |
| 570 | data | `if (self%start_row_numbr == 1) then / else > do i = 1,  self%start_row_numbr - 1` | `self%line` |
| 577 | data | `if (eof == 0) then > do` | `self%line` |
### `recall_read` at `recall_read.f90`

- Reason: opened input filename could not be resolved
- Expression(s): `recall_db(irec)%org_min%name`
- Procedure: `recall_read`
- Reader: `recall_read.f90`
- Match: source_input
- Source filename expression(s): `recall_db(irec)%org_min%name`
- Open: line 121, file expression `recall_db(irec)%org_min%name`, parser value `recall_db(irec)%org_min%name`, condition `do`

| Line | Role | Condition | Fields read |
| --- | --- | --- | --- |
| 122 | title | `do` | `titldum` |
| 124 | count | `do` | `nbyr` |
| 126 | header | `do` | `header` |
| 159 | data | `if (recall_db(irec)%iorg_min == irec) then` | `jday`, `mo`, `day_mo`, `iyr` |
| 167 | data | `if (recall_db(irec)%iorg_min == irec) then > if (recall(irec)%start_yr <= time%yrc) then > do` | `jday`, `mo`, `day_mo`, `iyr` |
| 181 | data | `if (recall_db(irec)%iorg_min == irec) then > do` | `jday1`, `mo1`, `day_mo`, `iyr` |
| 209 | data | `if (recall_db(irec)%iorg_min == irec) then > do > select case (recall_db(irec)%org_min%tstep) / case ("day")` | `jday`, `mo`, `day_mo`, `iyr`, `ob_typ`, `ob_name`, `recall(irec)%hd(jday1,iyrs)` |
| 212 | data | `if (recall_db(irec)%iorg_min == irec) then > do > select case (recall_db(irec)%org_min%tstep) / case ("mo")` | `jday`, `mo`, `day_mo`, `iyr`, `ob_typ`, `ob_name`, `recall(irec)%hd(mo1,iyrs)` |
| 217 | data | `if (recall_db(irec)%iorg_min == irec) then > do > select case (recall_db(irec)%org_min%tstep) / case ("yr")` | `jday`, `mo`, `day_mo`, `iyr`, `ob_typ`, `ob_name`, `ht1` |
