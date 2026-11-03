# Source Read Evidence for Schema Review

This report is generated when a comparison has schema entries that changed, disappeared from resolved schemas, or became newly unresolved. It does not certify a final schema. It shows the Fortran read evidence that a human or extractor update should review.

## `cs_aqu.ini`

- Schema diff status: `['runtime_arity.changed']`
- Review needed: no
- Base schema presence: `{'resolved_sections': ['runtime_arity'], 'unresolved_sections': []}`
- Candidate schema presence: `{'resolved_sections': ['runtime_arity'], 'unresolved_sections': []}`

### Base exact read evidence

- Procedure: `cs_aqu_read`
- Reader: `cs_aqu_read.f90`
- Match: exact_filename
- Resolved default filename(s): `cs_aqu.ini`
- Source filename expression(s): `cs_aqu.ini`
- Open: line 22, file expression `"cs_aqu.ini"`, parser value `cs_aqu.ini`, condition `if (i_exist .or. "cs_aqu.ini" /= "null") then > do`

| Line | Role | Condition | Fields read |
| --- | --- | --- | --- |
| 23 | title | `if (i_exist .or. "cs_aqu.ini" /= "null") then > do` | `titldum` |
| 25 | header | `if (i_exist .or. "cs_aqu.ini" /= "null") then > do` | `header` |
| 27 | header | `if (i_exist .or. "cs_aqu.ini" /= "null") then > do` | `header` |
| 31 | title | `if (i_exist .or. "cs_aqu.ini" /= "null") then > do > do while (eof == 0)` | `titldum` |
| 46 | title | `if (i_exist .or. "cs_aqu.ini" /= "null") then > do` | `titldum` |
| 48 | header | `if (i_exist .or. "cs_aqu.ini" /= "null") then > do` | `header` |
| 50 | header | `if (i_exist .or. "cs_aqu.ini" /= "null") then > do` | `header` |
| 54 | data | `if (i_exist .or. "cs_aqu.ini" /= "null") then > do > do ics = 1, imax` | `cs_aqu_ini(ics)%name`, `cs_aqu_ini(ics)%aqu` |


### Candidate exact read evidence

- Procedure: `cs_aqu_read`
- Reader: `cs_aqu_read.f90`
- Match: exact_filename
- Resolved default filename(s): `cs_aqu.ini`
- Source filename expression(s): `cs_aqu.ini`
- Open: line 23, file expression `"cs_aqu.ini"`, parser value `cs_aqu.ini`, condition `if (i_exist .or. "cs_aqu.ini" /= "null") then > do`

| Line | Role | Condition | Fields read |
| --- | --- | --- | --- |
| 24 | title | `if (i_exist .or. "cs_aqu.ini" /= "null") then > do` | `titldum` |
| 26 | header | `if (i_exist .or. "cs_aqu.ini" /= "null") then > do` | `header` |
| 28 | header | `if (i_exist .or. "cs_aqu.ini" /= "null") then > do` | `header` |
| 32 | title | `if (i_exist .or. "cs_aqu.ini" /= "null") then > do > do while (eof == 0)` | `titldum` |
| 47 | title | `if (i_exist .or. "cs_aqu.ini" /= "null") then > do` | `titldum` |
| 49 | header | `if (i_exist .or. "cs_aqu.ini" /= "null") then > do` | `header` |
| 51 | header | `if (i_exist .or. "cs_aqu.ini" /= "null") then > do` | `header` |
| 55 | data | `if (i_exist .or. "cs_aqu.ini" /= "null") then > do > do ics = 1, imax` | `cs_aqu_ini(ics)%name`, `cs_aqu_ini(ics)%aqu` |


## `cs_channel.ini`

- Schema diff status: `['runtime_arity.changed']`
- Review needed: no
- Base schema presence: `{'resolved_sections': ['runtime_arity'], 'unresolved_sections': []}`
- Candidate schema presence: `{'resolved_sections': ['runtime_arity'], 'unresolved_sections': []}`

### Base exact read evidence

- Procedure: `cs_cha_read`
- Reader: `cs_cha_read.f90`
- Match: exact_filename
- Resolved default filename(s): `cs_channel.ini`
- Source filename expression(s): `cs_channel.ini`
- Open: line 26, file expression `"cs_channel.ini"`, parser value `cs_channel.ini`, condition `if (i_exist .or. "cs_channel.ini" /= "null") then > do`

| Line | Role | Condition | Fields read |
| --- | --- | --- | --- |
| 27 | title | `if (i_exist .or. "cs_channel.ini" /= "null") then > do` | `titldum` |
| 29 | header | `if (i_exist .or. "cs_channel.ini" /= "null") then > do` | `header` |
| 33 | title | `if (i_exist .or. "cs_channel.ini" /= "null") then > do > do while (eof == 0)` | `titldum` |
| 47 | title | `if (i_exist .or. "cs_channel.ini" /= "null") then > do` | `titldum` |
| 50 | header | `if (i_exist .or. "cs_channel.ini" /= "null") then > do` | `header` |
| 53 | data | `if (i_exist .or. "cs_channel.ini" /= "null") then > do > do icsi = 1, imax` | `cs_cha_ini(icsi)%name`, `cs_cha_ini(icsi)%conc` |


### Candidate exact read evidence

- Procedure: `cs_cha_read`
- Reader: `cs_cha_read.f90`
- Match: exact_filename
- Resolved default filename(s): `cs_channel.ini`
- Source filename expression(s): `cs_channel.ini`
- Open: line 28, file expression `"cs_channel.ini"`, parser value `cs_channel.ini`, condition `if (i_exist .or. "cs_channel.ini" /= "null") then > do`

| Line | Role | Condition | Fields read |
| --- | --- | --- | --- |
| 29 | title | `if (i_exist .or. "cs_channel.ini" /= "null") then > do` | `titldum` |
| 31 | header | `if (i_exist .or. "cs_channel.ini" /= "null") then > do` | `header` |
| 35 | title | `if (i_exist .or. "cs_channel.ini" /= "null") then > do > do while (eof == 0)` | `titldum` |
| 49 | title | `if (i_exist .or. "cs_channel.ini" /= "null") then > do` | `titldum` |
| 52 | header | `if (i_exist .or. "cs_channel.ini" /= "null") then > do` | `header` |
| 55 | data | `if (i_exist .or. "cs_channel.ini" /= "null") then > do > do icsi = 1, imax` | `cs_cha_ini(icsi)%name`, `cs_cha_ini(icsi)%conc` |


## `cs_hru.ini`

- Schema diff status: `['runtime_arity.changed']`
- Review needed: no
- Base schema presence: `{'resolved_sections': ['runtime_arity'], 'unresolved_sections': []}`
- Candidate schema presence: `{'resolved_sections': ['runtime_arity'], 'unresolved_sections': []}`

### Base exact read evidence

- Procedure: `cs_hru_read`
- Reader: `cs_hru_read.f90`
- Match: exact_filename
- Resolved default filename(s): `cs_hru.ini`
- Source filename expression(s): `cs_hru.ini`
- Open: line 22, file expression `"cs_hru.ini"`, parser value `cs_hru.ini`, condition `if (i_exist .or. "cs_hru.ini" /= "null") then > do`

| Line | Role | Condition | Fields read |
| --- | --- | --- | --- |
| 23 | title | `if (i_exist .or. "cs_hru.ini" /= "null") then > do` | `titldum` |
| 25 | header | `if (i_exist .or. "cs_hru.ini" /= "null") then > do` | `header` |
| 27 | header | `if (i_exist .or. "cs_hru.ini" /= "null") then > do` | `header` |
| 29 | header | `if (i_exist .or. "cs_hru.ini" /= "null") then > do` | `header` |
| 31 | header | `if (i_exist .or. "cs_hru.ini" /= "null") then > do` | `header` |
| 36 | title | `if (i_exist .or. "cs_hru.ini" /= "null") then > do > do while (eof == 0)` | `titldum` |
| 38 | title | `if (i_exist .or. "cs_hru.ini" /= "null") then > do > do while (eof == 0)` | `titldum` |
| 40 | title | `if (i_exist .or. "cs_hru.ini" /= "null") then > do > do while (eof == 0)` | `titldum` |
| 55 | title | `if (i_exist .or. "cs_hru.ini" /= "null") then > do` | `titldum` |
| 57 | header | `if (i_exist .or. "cs_hru.ini" /= "null") then > do` | `header` |
| 59 | header | `if (i_exist .or. "cs_hru.ini" /= "null") then > do` | `header` |
| 61 | header | `if (i_exist .or. "cs_hru.ini" /= "null") then > do` | `header` |
| 63 | header | `if (i_exist .or. "cs_hru.ini" /= "null") then > do` | `header` |
| 67 | data | `if (i_exist .or. "cs_hru.ini" /= "null") then > do > do ics = 1, imax` | `cs_soil_ini(ics)%name` |
| 69 | data | `if (i_exist .or. "cs_hru.ini" /= "null") then > do > do ics = 1, imax` | `cs_soil_ini(ics)%soil` |
| 71 | data | `if (i_exist .or. "cs_hru.ini" /= "null") then > do > do ics = 1, imax` | `cs_soil_ini(ics)%plt` |


### Candidate exact read evidence

- Procedure: `cs_hru_read`
- Reader: `cs_hru_read.f90`
- Match: exact_filename
- Resolved default filename(s): `cs_hru.ini`
- Source filename expression(s): `cs_hru.ini`
- Open: line 23, file expression `"cs_hru.ini"`, parser value `cs_hru.ini`, condition `if (i_exist .or. "cs_hru.ini" /= "null") then > do`

| Line | Role | Condition | Fields read |
| --- | --- | --- | --- |
| 24 | title | `if (i_exist .or. "cs_hru.ini" /= "null") then > do` | `titldum` |
| 26 | header | `if (i_exist .or. "cs_hru.ini" /= "null") then > do` | `header` |
| 28 | header | `if (i_exist .or. "cs_hru.ini" /= "null") then > do` | `header` |
| 30 | header | `if (i_exist .or. "cs_hru.ini" /= "null") then > do` | `header` |
| 32 | header | `if (i_exist .or. "cs_hru.ini" /= "null") then > do` | `header` |
| 37 | title | `if (i_exist .or. "cs_hru.ini" /= "null") then > do > do while (eof == 0)` | `titldum` |
| 39 | title | `if (i_exist .or. "cs_hru.ini" /= "null") then > do > do while (eof == 0)` | `titldum` |
| 41 | title | `if (i_exist .or. "cs_hru.ini" /= "null") then > do > do while (eof == 0)` | `titldum` |
| 56 | title | `if (i_exist .or. "cs_hru.ini" /= "null") then > do` | `titldum` |
| 58 | header | `if (i_exist .or. "cs_hru.ini" /= "null") then > do` | `header` |
| 60 | header | `if (i_exist .or. "cs_hru.ini" /= "null") then > do` | `header` |
| 62 | header | `if (i_exist .or. "cs_hru.ini" /= "null") then > do` | `header` |
| 64 | header | `if (i_exist .or. "cs_hru.ini" /= "null") then > do` | `header` |
| 68 | data | `if (i_exist .or. "cs_hru.ini" /= "null") then > do > do ics = 1, imax` | `cs_soil_ini(ics)%name` |
| 70 | data | `if (i_exist .or. "cs_hru.ini" /= "null") then > do > do ics = 1, imax` | `cs_soil_ini(ics)%soil` |
| 72 | data | `if (i_exist .or. "cs_hru.ini" /= "null") then > do > do ics = 1, imax` | `cs_soil_ini(ics)%plt` |


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
- Open: line 45, file expression `"cs_recall.rec"`, parser value `cs_recall.rec`, condition `if (i_exist .or. in_rec%recall_rec /= "null") then > do`

| Line | Role | Condition | Fields read |
| --- | --- | --- | --- |
| 46 | title | `if (i_exist .or. in_rec%recall_rec /= "null") then > do` | `titldum` |
| 48 | header | `if (i_exist .or. in_rec%recall_rec /= "null") then > do` | `header` |
| 54 | data | `if (i_exist .or. in_rec%recall_rec /= "null") then > do > do while (eof == 0)` | `i` |
| 100 | title | `if (i_exist .or. in_rec%recall_rec /= "null") then > do` | `titldum` |
| 102 | header | `if (i_exist .or. in_rec%recall_rec /= "null") then > do` | `header` |
| 107 | data | `if (i_exist .or. in_rec%recall_rec /= "null") then > do > do ii = 1, imax` | `i` |
| 110 | data | `if (i_exist .or. in_rec%recall_rec /= "null") then > do > do ii = 1, imax` | `k`, `rec_cs(i)%name`, `rec_cs(i)%typ`, `rec_cs(i)%filename` |


### Candidate exact read evidence

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


## `dr_hmet.del`

- Schema diff status: `['runtime_arity.changed']`
- Review needed: no
- Base schema presence: `{'resolved_sections': ['runtime_arity'], 'unresolved_sections': []}`
- Candidate schema presence: `{'resolved_sections': ['runtime_arity'], 'unresolved_sections': []}`

### Base exact read evidence

- Procedure: `dr_read_hmet`
- Reader: `dr_read_hmet.f90`
- Match: exact_filename
- Resolved default filename(s): `dr_hmet.del`
- Source filename expression(s): `in_delr%hmet`, `dr_hmet.del`
- Open: line 25, file expression `in_delr%hmet`, parser value `dr_hmet.del`, condition `if (i_exist .or. in_delr%hmet /= "null") then > do`

| Line | Role | Condition | Fields read |
| --- | --- | --- | --- |
| 26 | title | `if (i_exist .or. in_delr%hmet /= "null") then > do` | `titldum` |
| 28 | header | `if (i_exist .or. in_delr%hmet /= "null") then > do` | `header` |
| 32 | title | `if (i_exist .or. in_delr%hmet /= "null") then > do > do while (eof == 0)` | `titldum` |
| 46 | title | `if (i_exist .or. in_delr%hmet /= "null") then > do` | `titldum` |
| 48 | header | `if (i_exist .or. in_delr%hmet /= "null") then > do` | `header` |
| 53 | title | `if (i_exist .or. in_delr%hmet /= "null") then > do > do ii = 1, db_mx%dr_hmet` | `titldum` |
| 56 | data | `if (i_exist .or. in_delr%hmet /= "null") then > do > do ii = 1, db_mx%dr_hmet` | `dr_hmet_name(ii)`, `(dr_hmet(ii)%hmet(ihmet), ihmet = 1, cs_db%num_metals)` |


### Candidate exact read evidence

- Procedure: `dr_read_hmet`
- Reader: `dr_read_hmet.f90`
- Match: exact_filename
- Resolved default filename(s): `dr_hmet.del`
- Source filename expression(s): `in_delr%hmet`, `dr_hmet.del`
- Open: line 33, file expression `in_delr%hmet`, parser value `dr_hmet.del`, condition `if (i_exist .or. in_delr%hmet /= "null") then > do`

| Line | Role | Condition | Fields read |
| --- | --- | --- | --- |
| 34 | title | `if (i_exist .or. in_delr%hmet /= "null") then > do` | `titldum` |
| 36 | header | `if (i_exist .or. in_delr%hmet /= "null") then > do` | `header` |
| 40 | title | `if (i_exist .or. in_delr%hmet /= "null") then > do > do while (eof == 0)` | `titldum` |
| 54 | title | `if (i_exist .or. in_delr%hmet /= "null") then > do` | `titldum` |
| 56 | header | `if (i_exist .or. in_delr%hmet /= "null") then > do` | `header` |
| 61 | title | `if (i_exist .or. in_delr%hmet /= "null") then > do > do ii = 1, db_mx%dr_hmet` | `titldum` |
| 64 | data | `if (i_exist .or. in_delr%hmet /= "null") then > do > do ii = 1, db_mx%dr_hmet` | `dr_hmet_name(ii)`, `(dr_hmet(ii)%hmet(ihmet), ihmet = 1, cs_db%num_metals)` |


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
- Open: line 24, file expression `in_delr%path`, parser value `dr_path.del`, condition `if (i_exist .or. in_delr%path /= "null") then > do`

| Line | Role | Condition | Fields read |
| --- | --- | --- | --- |
| 25 | title | `if (i_exist .or. in_delr%path /= "null") then > do` | `titldum` |
| 27 | header | `if (i_exist .or. in_delr%path /= "null") then > do` | `header` |
| 31 | title | `if (i_exist .or. in_delr%path /= "null") then > do > do while (eof == 0)` | `titldum` |
| 45 | title | `if (i_exist .or. in_delr%path /= "null") then > do` | `titldum` |
| 47 | header | `if (i_exist .or. in_delr%path /= "null") then > do` | `header` |
| 52 | title | `if (i_exist .or. in_delr%path /= "null") then > do > do ii = 1, db_mx%dr_path` | `titldum` |
| 55 | data | `if (i_exist .or. in_delr%path /= "null") then > do > do ii = 1, db_mx%dr_path` | `dr_path_name(ii)`, `(dr_path(ii)%path(ipath), ipath = 1, cs_db%num_paths)` |


### Candidate exact read evidence

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


## `dr_pest.del`

- Schema diff status: `['runtime_arity.changed']`
- Review needed: no
- Base schema presence: `{'resolved_sections': ['runtime_arity'], 'unresolved_sections': []}`
- Candidate schema presence: `{'resolved_sections': ['runtime_arity'], 'unresolved_sections': []}`

### Base exact read evidence

- Procedure: `dr_read_pest`
- Reader: `dr_read_pest.f90`
- Match: exact_filename
- Resolved default filename(s): `dr_pest.del`
- Source filename expression(s): `in_delr%pest`, `dr_pest.del`
- Open: line 24, file expression `in_delr%pest`, parser value `dr_pest.del`, condition `if (i_exist .or. in_delr%pest /= "null") then > do`

| Line | Role | Condition | Fields read |
| --- | --- | --- | --- |
| 25 | title | `if (i_exist .or. in_delr%pest /= "null") then > do` | `titldum` |
| 27 | header | `if (i_exist .or. in_delr%pest /= "null") then > do` | `header` |
| 31 | title | `if (i_exist .or. in_delr%pest /= "null") then > do > do while (eof == 0)` | `titldum` |
| 45 | title | `if (i_exist .or. in_delr%pest /= "null") then > do` | `titldum` |
| 47 | header | `if (i_exist .or. in_delr%pest /= "null") then > do` | `header` |
| 52 | title | `if (i_exist .or. in_delr%pest /= "null") then > do > do ii = 1, db_mx%dr_pest` | `titldum` |
| 55 | data | `if (i_exist .or. in_delr%pest /= "null") then > do > do ii = 1, db_mx%dr_pest` | `dr_pest_name(ii)`, `(dr_pest(ii)%pest(ipest), ipest = 1, cs_db%num_pests)` |


### Candidate exact read evidence

- Procedure: `dr_read_pest`
- Reader: `dr_read_pest.f90`
- Match: exact_filename
- Resolved default filename(s): `dr_pest.del`
- Source filename expression(s): `in_delr%pest`, `dr_pest.del`
- Open: line 32, file expression `in_delr%pest`, parser value `dr_pest.del`, condition `if (i_exist .or. in_delr%pest /= "null") then > do`

| Line | Role | Condition | Fields read |
| --- | --- | --- | --- |
| 33 | title | `if (i_exist .or. in_delr%pest /= "null") then > do` | `titldum` |
| 35 | header | `if (i_exist .or. in_delr%pest /= "null") then > do` | `header` |
| 39 | title | `if (i_exist .or. in_delr%pest /= "null") then > do > do while (eof == 0)` | `titldum` |
| 53 | title | `if (i_exist .or. in_delr%pest /= "null") then > do` | `titldum` |
| 55 | header | `if (i_exist .or. in_delr%pest /= "null") then > do` | `header` |
| 60 | title | `if (i_exist .or. in_delr%pest /= "null") then > do > do ii = 1, db_mx%dr_pest` | `titldum` |
| 63 | data | `if (i_exist .or. in_delr%pest /= "null") then > do > do ii = 1, db_mx%dr_pest` | `dr_pest_name(ii)`, `(dr_pest(ii)%pest(ipest), ipest = 1, cs_db%num_pests)` |


## `dr_salt.del`

- Schema diff status: `['runtime_arity.changed']`
- Review needed: no
- Base schema presence: `{'resolved_sections': ['runtime_arity'], 'unresolved_sections': []}`
- Candidate schema presence: `{'resolved_sections': ['runtime_arity'], 'unresolved_sections': []}`

### Base exact read evidence

- Procedure: `dr_read_salt`
- Reader: `dr_read_salt.f90`
- Match: exact_filename
- Resolved default filename(s): `dr_salt.del`
- Source filename expression(s): `in_delr%salt`, `dr_salt.del`
- Open: line 24, file expression `in_delr%salt`, parser value `dr_salt.del`, condition `if (i_exist .or. in_delr%salt /= "null") then > do`

| Line | Role | Condition | Fields read |
| --- | --- | --- | --- |
| 25 | title | `if (i_exist .or. in_delr%salt /= "null") then > do` | `titldum` |
| 27 | header | `if (i_exist .or. in_delr%salt /= "null") then > do` | `header` |
| 31 | title | `if (i_exist .or. in_delr%salt /= "null") then > do > do while (eof == 0)` | `titldum` |
| 45 | title | `if (i_exist .or. in_delr%salt /= "null") then > do` | `titldum` |
| 47 | header | `if (i_exist .or. in_delr%salt /= "null") then > do` | `header` |
| 52 | title | `if (i_exist .or. in_delr%salt /= "null") then > do > do ii = 1, db_mx%dr_salt` | `titldum` |
| 55 | data | `if (i_exist .or. in_delr%salt /= "null") then > do > do ii = 1, db_mx%dr_salt` | `dr_salt_name(ii)`, `(dr_salt(ii)%salt(isalt), isalt = 1, cs_db%num_salts)` |


### Candidate exact read evidence

- Procedure: `dr_read_salt`
- Reader: `dr_read_salt.f90`
- Match: exact_filename
- Resolved default filename(s): `dr_salt.del`
- Source filename expression(s): `in_delr%salt`, `dr_salt.del`
- Open: line 32, file expression `in_delr%salt`, parser value `dr_salt.del`, condition `if (i_exist .or. in_delr%salt /= "null") then > do`

| Line | Role | Condition | Fields read |
| --- | --- | --- | --- |
| 33 | title | `if (i_exist .or. in_delr%salt /= "null") then > do` | `titldum` |
| 35 | header | `if (i_exist .or. in_delr%salt /= "null") then > do` | `header` |
| 39 | title | `if (i_exist .or. in_delr%salt /= "null") then > do > do while (eof == 0)` | `titldum` |
| 53 | title | `if (i_exist .or. in_delr%salt /= "null") then > do` | `titldum` |
| 55 | header | `if (i_exist .or. in_delr%salt /= "null") then > do` | `header` |
| 60 | title | `if (i_exist .or. in_delr%salt /= "null") then > do > do ii = 1, db_mx%dr_salt` | `titldum` |
| 63 | data | `if (i_exist .or. in_delr%salt /= "null") then > do > do ii = 1, db_mx%dr_salt` | `dr_salt_name(ii)`, `(dr_salt(ii)%salt(isalt), isalt = 1, cs_db%num_salts)` |


## `exco_hmet.exc`

- Schema diff status: `['runtime_arity.changed']`
- Review needed: no
- Base schema presence: `{'resolved_sections': ['runtime_arity'], 'unresolved_sections': []}`
- Candidate schema presence: `{'resolved_sections': ['runtime_arity'], 'unresolved_sections': []}`

### Base exact read evidence

- Procedure: `exco_read_hmet`
- Reader: `exco_read_hmet.f90`
- Match: exact_filename
- Resolved default filename(s): `exco_hmet.exc`
- Source filename expression(s): `in_exco%hmet`, `exco_hmet.exc`
- Open: line 24, file expression `in_exco%hmet`, parser value `exco_hmet.exc`, condition `if (i_exist .or. in_exco%hmet /= "null") then > do`

| Line | Role | Condition | Fields read |
| --- | --- | --- | --- |
| 25 | title | `if (i_exist .or. in_exco%hmet /= "null") then > do` | `titldum` |
| 27 | header | `if (i_exist .or. in_exco%hmet /= "null") then > do` | `header` |
| 31 | title | `if (i_exist .or. in_exco%hmet /= "null") then > do > do while (eof == 0)` | `titldum` |
| 45 | title | `if (i_exist .or. in_exco%hmet /= "null") then > do` | `titldum` |
| 47 | header | `if (i_exist .or. in_exco%hmet /= "null") then > do` | `header` |
| 52 | title | `if (i_exist .or. in_exco%hmet /= "null") then > do > do ii = 1, db_mx%exco_hmet` | `titldum` |
| 55 | data | `if (i_exist .or. in_exco%hmet /= "null") then > do > do ii = 1, db_mx%exco_hmet` | `exco_hmet_name(ii)`, `(exco_hmet(ii)%hmet(ihmet), ihmet = 1, cs_db%num_metals)` |


### Candidate exact read evidence

- Procedure: `exco_read_hmet`
- Reader: `exco_read_hmet.f90`
- Match: exact_filename
- Resolved default filename(s): `exco_hmet.exc`
- Source filename expression(s): `in_exco%hmet`, `exco_hmet.exc`
- Open: line 32, file expression `in_exco%hmet`, parser value `exco_hmet.exc`, condition `if (i_exist .or. in_exco%hmet /= "null") then > do`

| Line | Role | Condition | Fields read |
| --- | --- | --- | --- |
| 33 | title | `if (i_exist .or. in_exco%hmet /= "null") then > do` | `titldum` |
| 35 | header | `if (i_exist .or. in_exco%hmet /= "null") then > do` | `header` |
| 39 | title | `if (i_exist .or. in_exco%hmet /= "null") then > do > do while (eof == 0)` | `titldum` |
| 53 | title | `if (i_exist .or. in_exco%hmet /= "null") then > do` | `titldum` |
| 55 | header | `if (i_exist .or. in_exco%hmet /= "null") then > do` | `header` |
| 60 | title | `if (i_exist .or. in_exco%hmet /= "null") then > do > do ii = 1, db_mx%exco_hmet` | `titldum` |
| 63 | data | `if (i_exist .or. in_exco%hmet /= "null") then > do > do ii = 1, db_mx%exco_hmet` | `exco_hmet_name(ii)`, `(exco_hmet(ii)%hmet(ihmet), ihmet = 1, cs_db%num_metals)` |


## `exco_path.exc`

- Schema diff status: `['runtime_arity.changed']`
- Review needed: no
- Base schema presence: `{'resolved_sections': ['runtime_arity'], 'unresolved_sections': []}`
- Candidate schema presence: `{'resolved_sections': ['runtime_arity'], 'unresolved_sections': []}`

### Base exact read evidence

- Procedure: `exco_read_path`
- Reader: `exco_read_path.f90`
- Match: exact_filename
- Resolved default filename(s): `exco_path.exc`
- Source filename expression(s): `in_exco%path`, `exco_path.exc`
- Open: line 24, file expression `in_exco%path`, parser value `exco_path.exc`, condition `if (i_exist .or. in_exco%path /= "null") then > do`

| Line | Role | Condition | Fields read |
| --- | --- | --- | --- |
| 25 | title | `if (i_exist .or. in_exco%path /= "null") then > do` | `titldum` |
| 27 | header | `if (i_exist .or. in_exco%path /= "null") then > do` | `header` |
| 31 | title | `if (i_exist .or. in_exco%path /= "null") then > do > do while (eof == 0)` | `titldum` |
| 45 | title | `if (i_exist .or. in_exco%path /= "null") then > do` | `titldum` |
| 47 | header | `if (i_exist .or. in_exco%path /= "null") then > do` | `header` |
| 52 | title | `if (i_exist .or. in_exco%path /= "null") then > do > do ii = 1, db_mx%exco_path` | `titldum` |
| 55 | data | `if (i_exist .or. in_exco%path /= "null") then > do > do ii = 1, db_mx%exco_path` | `exco_path_name(ii)`, `(exco_path(ii)%path(ipath), ipath = 1, cs_db%num_paths)` |


### Candidate exact read evidence

- Procedure: `exco_read_path`
- Reader: `exco_read_path.f90`
- Match: exact_filename
- Resolved default filename(s): `exco_path.exc`
- Source filename expression(s): `in_exco%path`, `exco_path.exc`
- Open: line 32, file expression `in_exco%path`, parser value `exco_path.exc`, condition `if (i_exist .or. in_exco%path /= "null") then > do`

| Line | Role | Condition | Fields read |
| --- | --- | --- | --- |
| 33 | title | `if (i_exist .or. in_exco%path /= "null") then > do` | `titldum` |
| 35 | header | `if (i_exist .or. in_exco%path /= "null") then > do` | `header` |
| 39 | title | `if (i_exist .or. in_exco%path /= "null") then > do > do while (eof == 0)` | `titldum` |
| 53 | title | `if (i_exist .or. in_exco%path /= "null") then > do` | `titldum` |
| 55 | header | `if (i_exist .or. in_exco%path /= "null") then > do` | `header` |
| 60 | title | `if (i_exist .or. in_exco%path /= "null") then > do > do ii = 1, db_mx%exco_path` | `titldum` |
| 63 | data | `if (i_exist .or. in_exco%path /= "null") then > do > do ii = 1, db_mx%exco_path` | `exco_path_name(ii)`, `(exco_path(ii)%path(ipath), ipath = 1, cs_db%num_paths)` |


## `exco_pest.exc`

- Schema diff status: `['runtime_arity.changed']`
- Review needed: no
- Base schema presence: `{'resolved_sections': ['runtime_arity'], 'unresolved_sections': []}`
- Candidate schema presence: `{'resolved_sections': ['runtime_arity'], 'unresolved_sections': []}`

### Base exact read evidence

- Procedure: `exco_read_pest`
- Reader: `exco_read_pest.f90`
- Match: exact_filename
- Resolved default filename(s): `exco_pest.exc`
- Source filename expression(s): `in_exco%pest`, `exco_pest.exc`
- Open: line 23, file expression `in_exco%pest`, parser value `exco_pest.exc`, condition `if (i_exist .or. in_exco%pest /= "null") then > do`

| Line | Role | Condition | Fields read |
| --- | --- | --- | --- |
| 24 | title | `if (i_exist .or. in_exco%pest /= "null") then > do` | `titldum` |
| 26 | header | `if (i_exist .or. in_exco%pest /= "null") then > do` | `header` |
| 30 | title | `if (i_exist .or. in_exco%pest /= "null") then > do > do while (eof == 0)` | `titldum` |
| 44 | title | `if (i_exist .or. in_exco%pest /= "null") then > do` | `titldum` |
| 46 | header | `if (i_exist .or. in_exco%pest /= "null") then > do` | `header` |
| 51 | title | `if (i_exist .or. in_exco%pest /= "null") then > do > do ii = 1, db_mx%exco_pest` | `titldum` |
| 54 | data | `if (i_exist .or. in_exco%pest /= "null") then > do > do ii = 1, db_mx%exco_pest` | `exco_pest_name(ii)`, `(exco_pest(ii)%pest(ipest), ipest = 1, cs_db%num_pests)` |


### Candidate exact read evidence

- Procedure: `exco_read_pest`
- Reader: `exco_read_pest.f90`
- Match: exact_filename
- Resolved default filename(s): `exco_pest.exc`
- Source filename expression(s): `in_exco%pest`, `exco_pest.exc`
- Open: line 31, file expression `in_exco%pest`, parser value `exco_pest.exc`, condition `if (i_exist .or. in_exco%pest /= "null") then > do`

| Line | Role | Condition | Fields read |
| --- | --- | --- | --- |
| 32 | title | `if (i_exist .or. in_exco%pest /= "null") then > do` | `titldum` |
| 34 | header | `if (i_exist .or. in_exco%pest /= "null") then > do` | `header` |
| 38 | title | `if (i_exist .or. in_exco%pest /= "null") then > do > do while (eof == 0)` | `titldum` |
| 52 | title | `if (i_exist .or. in_exco%pest /= "null") then > do` | `titldum` |
| 54 | header | `if (i_exist .or. in_exco%pest /= "null") then > do` | `header` |
| 59 | title | `if (i_exist .or. in_exco%pest /= "null") then > do > do ii = 1, db_mx%exco_pest` | `titldum` |
| 62 | data | `if (i_exist .or. in_exco%pest /= "null") then > do > do ii = 1, db_mx%exco_pest` | `exco_pest_name(ii)`, `(exco_pest(ii)%pest(ipest), ipest = 1, cs_db%num_pests)` |


## `exco_salt.exc`

- Schema diff status: `['runtime_arity.changed']`
- Review needed: no
- Base schema presence: `{'resolved_sections': ['runtime_arity'], 'unresolved_sections': []}`
- Candidate schema presence: `{'resolved_sections': ['runtime_arity'], 'unresolved_sections': []}`

### Base exact read evidence

- Procedure: `exco_read_salt`
- Reader: `exco_read_salt.f90`
- Match: exact_filename
- Resolved default filename(s): `exco_salt.exc`
- Source filename expression(s): `in_exco%salt`, `exco_salt.exc`
- Open: line 24, file expression `in_exco%salt`, parser value `exco_salt.exc`, condition `if (i_exist .or. in_exco%salt /= "null") then > do`

| Line | Role | Condition | Fields read |
| --- | --- | --- | --- |
| 25 | title | `if (i_exist .or. in_exco%salt /= "null") then > do` | `titldum` |
| 27 | header | `if (i_exist .or. in_exco%salt /= "null") then > do` | `header` |
| 31 | title | `if (i_exist .or. in_exco%salt /= "null") then > do > do while (eof == 0)` | `titldum` |
| 45 | title | `if (i_exist .or. in_exco%salt /= "null") then > do` | `titldum` |
| 47 | header | `if (i_exist .or. in_exco%salt /= "null") then > do` | `header` |
| 52 | title | `if (i_exist .or. in_exco%salt /= "null") then > do > do ii = 1, db_mx%exco_salt` | `titldum` |
| 55 | data | `if (i_exist .or. in_exco%salt /= "null") then > do > do ii = 1, db_mx%exco_salt` | `exco_salt_name(ii)`, `(exco_salt(ii)%salt(isalt), isalt = 1, cs_db%num_salts)` |


### Candidate exact read evidence

- Procedure: `exco_read_salt`
- Reader: `exco_read_salt.f90`
- Match: exact_filename
- Resolved default filename(s): `exco_salt.exc`
- Source filename expression(s): `in_exco%salt`, `exco_salt.exc`
- Open: line 32, file expression `in_exco%salt`, parser value `exco_salt.exc`, condition `if (i_exist .or. in_exco%salt /= "null") then > do`

| Line | Role | Condition | Fields read |
| --- | --- | --- | --- |
| 33 | title | `if (i_exist .or. in_exco%salt /= "null") then > do` | `titldum` |
| 35 | header | `if (i_exist .or. in_exco%salt /= "null") then > do` | `header` |
| 39 | title | `if (i_exist .or. in_exco%salt /= "null") then > do > do while (eof == 0)` | `titldum` |
| 53 | title | `if (i_exist .or. in_exco%salt /= "null") then > do` | `titldum` |
| 55 | header | `if (i_exist .or. in_exco%salt /= "null") then > do` | `header` |
| 60 | title | `if (i_exist .or. in_exco%salt /= "null") then > do > do ii = 1, db_mx%exco_salt` | `titldum` |
| 63 | data | `if (i_exist .or. in_exco%salt /= "null") then > do > do ii = 1, db_mx%exco_salt` | `exco_salt_name(ii)`, `(exco_salt(ii)%salt(isalt), isalt = 1, cs_db%num_salts)` |


## `hmet_hru.ini`

- Schema diff status: `['runtime_arity.changed']`
- Review needed: no
- Base schema presence: `{'resolved_sections': ['runtime_arity'], 'unresolved_sections': []}`
- Candidate schema presence: `{'resolved_sections': ['runtime_arity'], 'unresolved_sections': []}`

### Base exact read evidence

- Procedure: `hmet_hru_aqu_read`
- Reader: `hmet_hru_aqu_read.f90`
- Match: exact_filename
- Resolved default filename(s): `hmet_hru.ini`
- Source filename expression(s): `in_init%hmet_soil`, `hmet_hru.ini`
- Open: line 23, file expression `in_init%hmet_soil`, parser value `hmet_hru.ini`, condition `if (i_exist .or. in_init%hmet_soil /= "null") then > do`

| Line | Role | Condition | Fields read |
| --- | --- | --- | --- |
| 24 | title | `if (i_exist .or. in_init%hmet_soil /= "null") then > do` | `titldum` |
| 28 | header | `if (i_exist .or. in_init%hmet_soil /= "null") then > do > do while (eof == 0)` | `header` |
| 30 | title | `if (i_exist .or. in_init%hmet_soil /= "null") then > do > do while (eof == 0)` | `titldum` |
| 33 | title | `if (i_exist .or. in_init%hmet_soil /= "null") then > do > do while (eof == 0) > do ihmet = 1, cs_db%num_metals` | `titldum` |
| 50 | title | `if (i_exist .or. in_init%hmet_soil /= "null") then > do` | `titldum` |
| 54 | header | `if (i_exist .or. in_init%hmet_soil /= "null") then > do > do ihmeti = 1, imax` | `header` |
| 56 | data | `if (i_exist .or. in_init%hmet_soil /= "null") then > do > do ihmeti = 1, imax` | `hmet_soil_ini(ihmeti)%name` |
| 59 | data | `if (i_exist .or. in_init%hmet_soil /= "null") then > do > do ihmeti = 1, imax > do ipest = 1, cs_db%num_metals` | `titldum`, `hmet_soil_ini(ihmeti)%soil(ihmet)` |
| 61 | data | `if (i_exist .or. in_init%hmet_soil /= "null") then > do > do ihmeti = 1, imax > do ipest = 1, cs_db%num_metals` | `titldum`, `hmet_soil_ini(ihmeti)%plt(ihmet)` |


### Candidate exact read evidence

- Procedure: `hmet_hru_aqu_read`
- Reader: `hmet_hru_aqu_read.f90`
- Match: exact_filename
- Resolved default filename(s): `hmet_hru.ini`
- Source filename expression(s): `in_init%hmet_soil`, `hmet_hru.ini`
- Open: line 24, file expression `in_init%hmet_soil`, parser value `hmet_hru.ini`, condition `if (i_exist .or. in_init%hmet_soil /= "null") then > do`

| Line | Role | Condition | Fields read |
| --- | --- | --- | --- |
| 25 | title | `if (i_exist .or. in_init%hmet_soil /= "null") then > do` | `titldum` |
| 29 | header | `if (i_exist .or. in_init%hmet_soil /= "null") then > do > do while (eof == 0)` | `header` |
| 31 | title | `if (i_exist .or. in_init%hmet_soil /= "null") then > do > do while (eof == 0)` | `titldum` |
| 34 | title | `if (i_exist .or. in_init%hmet_soil /= "null") then > do > do while (eof == 0) > do ihmet = 1, cs_db%num_metals` | `titldum` |
| 51 | title | `if (i_exist .or. in_init%hmet_soil /= "null") then > do` | `titldum` |
| 55 | header | `if (i_exist .or. in_init%hmet_soil /= "null") then > do > do ihmeti = 1, imax` | `header` |
| 57 | data | `if (i_exist .or. in_init%hmet_soil /= "null") then > do > do ihmeti = 1, imax` | `hmet_soil_ini(ihmeti)%name` |
| 60 | data | `if (i_exist .or. in_init%hmet_soil /= "null") then > do > do ihmeti = 1, imax > do ipest = 1, cs_db%num_metals` | `titldum`, `hmet_soil_ini(ihmeti)%soil(ihmet)` |
| 62 | data | `if (i_exist .or. in_init%hmet_soil /= "null") then > do > do ihmeti = 1, imax > do ipest = 1, cs_db%num_metals` | `titldum`, `hmet_soil_ini(ihmeti)%plt(ihmet)` |


## `path_hru.ini`

- Schema diff status: `['runtime_arity.changed']`
- Review needed: no
- Base schema presence: `{'resolved_sections': ['runtime_arity'], 'unresolved_sections': []}`
- Candidate schema presence: `{'resolved_sections': ['runtime_arity'], 'unresolved_sections': []}`

### Base exact read evidence

- Procedure: `path_hru_aqu_read`
- Reader: `path_hru_aqu_read.f90`
- Match: exact_filename
- Resolved default filename(s): `path_hru.ini`
- Source filename expression(s): `in_init%path_soil`, `path_hru.ini`
- Open: line 22, file expression `in_init%path_soil`, parser value `path_hru.ini`, condition `if (i_exist .or. in_init%path_soil /= "null") then > do`

| Line | Role | Condition | Fields read |
| --- | --- | --- | --- |
| 23 | title | `if (i_exist .or. in_init%path_soil /= "null") then > do` | `titldum` |
| 27 | header | `if (i_exist .or. in_init%path_soil /= "null") then > do > do while (eof == 0)` | `header` |
| 29 | title | `if (i_exist .or. in_init%path_soil /= "null") then > do > do while (eof == 0)` | `titldum` |
| 32 | title | `if (i_exist .or. in_init%path_soil /= "null") then > do > do while (eof == 0) > do ipath = 1, cs_db%num_paths` | `titldum` |
| 49 | title | `if (i_exist .or. in_init%path_soil /= "null") then > do` | `titldum` |
| 53 | header | `if (i_exist .or. in_init%path_soil /= "null") then > do > do ipathi = 1, imax` | `header` |
| 55 | data | `if (i_exist .or. in_init%path_soil /= "null") then > do > do ipathi = 1, imax` | `path_soil_ini(ipathi)%name` |
| 57 | data | `if (i_exist .or. in_init%path_soil /= "null") then > do > do ipathi = 1, imax` | `titldum`, `path_soil_ini(ipathi)%soil`, `path_soil_ini(ipathi)%plt` |


### Candidate exact read evidence

- Procedure: `path_hru_aqu_read`
- Reader: `path_hru_aqu_read.f90`
- Match: exact_filename
- Resolved default filename(s): `path_hru.ini`
- Source filename expression(s): `in_init%path_soil`, `path_hru.ini`
- Open: line 23, file expression `in_init%path_soil`, parser value `path_hru.ini`, condition `if (i_exist .or. in_init%path_soil /= "null") then > do`

| Line | Role | Condition | Fields read |
| --- | --- | --- | --- |
| 24 | title | `if (i_exist .or. in_init%path_soil /= "null") then > do` | `titldum` |
| 28 | header | `if (i_exist .or. in_init%path_soil /= "null") then > do > do while (eof == 0)` | `header` |
| 30 | title | `if (i_exist .or. in_init%path_soil /= "null") then > do > do while (eof == 0)` | `titldum` |
| 33 | title | `if (i_exist .or. in_init%path_soil /= "null") then > do > do while (eof == 0) > do ipath = 1, cs_db%num_paths` | `titldum` |
| 50 | title | `if (i_exist .or. in_init%path_soil /= "null") then > do` | `titldum` |
| 54 | header | `if (i_exist .or. in_init%path_soil /= "null") then > do > do ipathi = 1, imax` | `header` |
| 56 | data | `if (i_exist .or. in_init%path_soil /= "null") then > do > do ipathi = 1, imax` | `path_soil_ini(ipathi)%name` |
| 58 | data | `if (i_exist .or. in_init%path_soil /= "null") then > do > do ipathi = 1, imax` | `titldum`, `path_soil_ini(ipathi)%soil`, `path_soil_ini(ipathi)%plt` |


## `path_water.ini`

- Schema diff status: `['runtime_arity.changed']`
- Review needed: no
- Base schema presence: `{'resolved_sections': ['runtime_arity'], 'unresolved_sections': []}`
- Candidate schema presence: `{'resolved_sections': ['runtime_arity'], 'unresolved_sections': []}`

### Base exact read evidence

- Procedure: `path_cha_res_read`
- Reader: `path_cha_res_read.f90`
- Match: exact_filename
- Resolved default filename(s): `path_water.ini`
- Source filename expression(s): `in_init%path_water`, `path_water.ini`
- Open: line 26, file expression `in_init%path_water`, parser value `path_water.ini`, condition `if (i_exist .or. in_init%path_water /= "null") then > do`

| Line | Role | Condition | Fields read |
| --- | --- | --- | --- |
| 27 | title | `if (i_exist .or. in_init%path_water /= "null") then > do` | `titldum` |
| 29 | header | `if (i_exist .or. in_init%path_water /= "null") then > do` | `header` |
| 33 | title | `if (i_exist .or. in_init%path_water /= "null") then > do > do while (eof == 0)` | `titldum` |
| 36 | title | `if (i_exist .or. in_init%path_water /= "null") then > do > do while (eof == 0) > do ipath = 1, cs_db%num_paths` | `titldum` |
| 38 | title | `if (i_exist .or. in_init%path_water /= "null") then > do > do while (eof == 0) > do ipath = 1, cs_db%num_paths` | `titldum` |
| 54 | title | `if (i_exist .or. in_init%path_water /= "null") then > do` | `titldum` |
| 58 | header | `if (i_exist .or. in_init%path_water /= "null") then > do > do ipathi = 1, imax` | `header` |
| 60 | data | `if (i_exist .or. in_init%path_water /= "null") then > do > do ipathi = 1, imax` | `path_init_name(ipathi)` |
| 62 | data | `if (i_exist .or. in_init%path_water /= "null") then > do > do ipathi = 1, imax` | `titldum`, `path_water_ini(ipathi)%water`, `path_water_ini(ipathi)%benthic` |


### Candidate exact read evidence

- Procedure: `path_cha_res_read`
- Reader: `path_cha_res_read.f90`
- Match: exact_filename
- Resolved default filename(s): `path_water.ini`
- Source filename expression(s): `in_init%path_water`, `path_water.ini`
- Open: line 27, file expression `in_init%path_water`, parser value `path_water.ini`, condition `if (i_exist .or. in_init%path_water /= "null") then > do`

| Line | Role | Condition | Fields read |
| --- | --- | --- | --- |
| 28 | title | `if (i_exist .or. in_init%path_water /= "null") then > do` | `titldum` |
| 30 | header | `if (i_exist .or. in_init%path_water /= "null") then > do` | `header` |
| 34 | title | `if (i_exist .or. in_init%path_water /= "null") then > do > do while (eof == 0)` | `titldum` |
| 37 | title | `if (i_exist .or. in_init%path_water /= "null") then > do > do while (eof == 0) > do ipath = 1, cs_db%num_paths` | `titldum` |
| 39 | title | `if (i_exist .or. in_init%path_water /= "null") then > do > do while (eof == 0) > do ipath = 1, cs_db%num_paths` | `titldum` |
| 55 | title | `if (i_exist .or. in_init%path_water /= "null") then > do` | `titldum` |
| 59 | header | `if (i_exist .or. in_init%path_water /= "null") then > do > do ipathi = 1, imax` | `header` |
| 61 | data | `if (i_exist .or. in_init%path_water /= "null") then > do > do ipathi = 1, imax` | `path_init_name(ipathi)` |
| 63 | data | `if (i_exist .or. in_init%path_water /= "null") then > do > do ipathi = 1, imax` | `titldum`, `path_water_ini(ipathi)%water`, `path_water_ini(ipathi)%benthic` |


## `pest_hru.ini`

- Schema diff status: `['runtime_arity.changed']`
- Review needed: no
- Base schema presence: `{'resolved_sections': ['runtime_arity'], 'unresolved_sections': []}`
- Candidate schema presence: `{'resolved_sections': ['runtime_arity'], 'unresolved_sections': []}`

### Base exact read evidence

- Procedure: `pest_hru_aqu_read`
- Reader: `pest_hru_aqu_read.f90`
- Match: exact_filename
- Resolved default filename(s): `pest_hru.ini`
- Source filename expression(s): `in_init%pest_soil`, `pest_hru.ini`
- Open: line 22, file expression `in_init%pest_soil`, parser value `pest_hru.ini`, condition `if (i_exist .or. in_init%pest_soil /= "null") then > do`

| Line | Role | Condition | Fields read |
| --- | --- | --- | --- |
| 23 | title | `if (i_exist .or. in_init%pest_soil /= "null") then > do` | `titldum` |
| 27 | header | `if (i_exist .or. in_init%pest_soil /= "null") then > do > do while (eof == 0)` | `header` |
| 29 | title | `if (i_exist .or. in_init%pest_soil /= "null") then > do > do while (eof == 0)` | `titldum` |
| 32 | title | `if (i_exist .or. in_init%pest_soil /= "null") then > do > do while (eof == 0) > do ipest = 1, cs_db%num_pests` | `titldum` |
| 49 | title | `if (i_exist .or. in_init%pest_soil /= "null") then > do` | `titldum` |
| 51 | header | `if (i_exist .or. in_init%pest_soil /= "null") then > do` | `header` |
| 55 | data | `if (i_exist .or. in_init%pest_soil /= "null") then > do > do ipesti = 1, imax` | `pest_soil_ini(ipesti)%name` |
| 57 | data | `if (i_exist .or. in_init%pest_soil /= "null") then > do > do ipesti = 1, imax > do ipest = 1, cs_db%num_pests` | `titldum`, `pest_soil_ini(ipesti)%soil(ipest)`, `pest_soil_ini(ipesti)%plt(ipest)` |


### Candidate exact read evidence

- Procedure: `pest_hru_aqu_read`
- Reader: `pest_hru_aqu_read.f90`
- Match: exact_filename
- Resolved default filename(s): `pest_hru.ini`
- Source filename expression(s): `in_init%pest_soil`, `pest_hru.ini`
- Open: line 23, file expression `in_init%pest_soil`, parser value `pest_hru.ini`, condition `if (i_exist .or. in_init%pest_soil /= "null") then > do`

| Line | Role | Condition | Fields read |
| --- | --- | --- | --- |
| 24 | title | `if (i_exist .or. in_init%pest_soil /= "null") then > do` | `titldum` |
| 28 | header | `if (i_exist .or. in_init%pest_soil /= "null") then > do > do while (eof == 0)` | `header` |
| 30 | title | `if (i_exist .or. in_init%pest_soil /= "null") then > do > do while (eof == 0)` | `titldum` |
| 33 | title | `if (i_exist .or. in_init%pest_soil /= "null") then > do > do while (eof == 0) > do ipest = 1, cs_db%num_pests` | `titldum` |
| 50 | title | `if (i_exist .or. in_init%pest_soil /= "null") then > do` | `titldum` |
| 52 | header | `if (i_exist .or. in_init%pest_soil /= "null") then > do` | `header` |
| 56 | data | `if (i_exist .or. in_init%pest_soil /= "null") then > do > do ipesti = 1, imax` | `pest_soil_ini(ipesti)%name` |
| 58 | data | `if (i_exist .or. in_init%pest_soil /= "null") then > do > do ipesti = 1, imax > do ipest = 1, cs_db%num_pests` | `titldum`, `pest_soil_ini(ipesti)%soil(ipest)`, `pest_soil_ini(ipesti)%plt(ipest)` |


## `pest_water.ini`

- Schema diff status: `['runtime_arity.changed']`
- Review needed: no
- Base schema presence: `{'resolved_sections': ['runtime_arity'], 'unresolved_sections': []}`
- Candidate schema presence: `{'resolved_sections': ['runtime_arity'], 'unresolved_sections': []}`

### Base exact read evidence

- Procedure: `pest_cha_res_read`
- Reader: `pest_cha_res_read.f90`
- Match: exact_filename
- Resolved default filename(s): `pest_water.ini`
- Source filename expression(s): `in_init%pest_water`, `pest_water.ini`
- Open: line 25, file expression `in_init%pest_water`, parser value `pest_water.ini`, condition `if (i_exist .or. in_init%pest_water /= "null") then > do`

| Line | Role | Condition | Fields read |
| --- | --- | --- | --- |
| 26 | title | `if (i_exist .or. in_init%pest_water /= "null") then > do` | `titldum` |
| 28 | header | `if (i_exist .or. in_init%pest_water /= "null") then > do` | `header` |
| 32 | title | `if (i_exist .or. in_init%pest_water /= "null") then > do > do while (eof == 0)` | `titldum` |
| 35 | title | `if (i_exist .or. in_init%pest_water /= "null") then > do > do while (eof == 0) > do ipest = 1, cs_db%num_pests` | `titldum` |
| 37 | title | `if (i_exist .or. in_init%pest_water /= "null") then > do > do while (eof == 0) > do ipest = 1, cs_db%num_pests` | `titldum` |
| 54 | title | `if (i_exist .or. in_init%pest_water /= "null") then > do` | `titldum` |
| 56 | header | `if (i_exist .or. in_init%pest_water /= "null") then > do` | `header` |
| 60 | data | `if (i_exist .or. in_init%pest_water /= "null") then > do > do ipesti = 1, imax` | `pest_init_name(ipesti)` |
| 62 | data | `if (i_exist .or. in_init%pest_water /= "null") then > do > do ipesti = 1, imax` | `titldum`, `pest_water_ini(ipesti)%water`, `pest_water_ini(ipesti)%benthic` |


### Candidate exact read evidence

- Procedure: `pest_cha_res_read`
- Reader: `pest_cha_res_read.f90`
- Match: exact_filename
- Resolved default filename(s): `pest_water.ini`
- Source filename expression(s): `in_init%pest_water`, `pest_water.ini`
- Open: line 27, file expression `in_init%pest_water`, parser value `pest_water.ini`, condition `if (i_exist .or. in_init%pest_water /= "null") then > do`

| Line | Role | Condition | Fields read |
| --- | --- | --- | --- |
| 28 | title | `if (i_exist .or. in_init%pest_water /= "null") then > do` | `titldum` |
| 30 | header | `if (i_exist .or. in_init%pest_water /= "null") then > do` | `header` |
| 34 | title | `if (i_exist .or. in_init%pest_water /= "null") then > do > do while (eof == 0)` | `titldum` |
| 37 | title | `if (i_exist .or. in_init%pest_water /= "null") then > do > do while (eof == 0) > do ipest = 1, cs_db%num_pests` | `titldum` |
| 39 | title | `if (i_exist .or. in_init%pest_water /= "null") then > do > do while (eof == 0) > do ipest = 1, cs_db%num_pests` | `titldum` |
| 56 | title | `if (i_exist .or. in_init%pest_water /= "null") then > do` | `titldum` |
| 58 | header | `if (i_exist .or. in_init%pest_water /= "null") then > do` | `header` |
| 62 | data | `if (i_exist .or. in_init%pest_water /= "null") then > do > do ipesti = 1, imax` | `pest_init_name(ipesti)` |
| 64 | data | `if (i_exist .or. in_init%pest_water /= "null") then > do > do ipesti = 1, imax` | `titldum`, `pest_water_ini(ipesti)%water`, `pest_water_ini(ipesti)%benthic` |


## `salt_channel.ini`

- Schema diff status: `['runtime_arity.changed']`
- Review needed: no
- Base schema presence: `{'resolved_sections': ['runtime_arity'], 'unresolved_sections': []}`
- Candidate schema presence: `{'resolved_sections': ['runtime_arity'], 'unresolved_sections': []}`

### Base exact read evidence

- Procedure: `salt_cha_read`
- Reader: `salt_cha_read.f90`
- Match: exact_filename
- Resolved default filename(s): `salt_channel.ini`
- Source filename expression(s): `salt_channel.ini`
- Open: line 26, file expression `"salt_channel.ini"`, parser value `salt_channel.ini`, condition `if (i_exist .or. "salt_channel.ini" /= "null") then > do`

| Line | Role | Condition | Fields read |
| --- | --- | --- | --- |
| 27 | title | `if (i_exist .or. "salt_channel.ini" /= "null") then > do` | `titldum` |
| 29 | header | `if (i_exist .or. "salt_channel.ini" /= "null") then > do` | `header` |
| 33 | title | `if (i_exist .or. "salt_channel.ini" /= "null") then > do > do while (eof == 0)` | `titldum` |
| 47 | title | `if (i_exist .or. "salt_channel.ini" /= "null") then > do` | `titldum` |
| 50 | header | `if (i_exist .or. "salt_channel.ini" /= "null") then > do` | `header` |
| 53 | data | `if (i_exist .or. "salt_channel.ini" /= "null") then > do > do isalti = 1, imax` | `salt_cha_ini(isalti)%name`, `salt_cha_ini(isalti)%conc` |


### Candidate exact read evidence

- Procedure: `salt_cha_read`
- Reader: `salt_cha_read.f90`
- Match: exact_filename
- Resolved default filename(s): `salt_channel.ini`
- Source filename expression(s): `salt_channel.ini`
- Open: line 27, file expression `"salt_channel.ini"`, parser value `salt_channel.ini`, condition `if (i_exist .or. "salt_channel.ini" /= "null") then > do`

| Line | Role | Condition | Fields read |
| --- | --- | --- | --- |
| 28 | title | `if (i_exist .or. "salt_channel.ini" /= "null") then > do` | `titldum` |
| 30 | header | `if (i_exist .or. "salt_channel.ini" /= "null") then > do` | `header` |
| 34 | title | `if (i_exist .or. "salt_channel.ini" /= "null") then > do > do while (eof == 0)` | `titldum` |
| 48 | title | `if (i_exist .or. "salt_channel.ini" /= "null") then > do` | `titldum` |
| 51 | header | `if (i_exist .or. "salt_channel.ini" /= "null") then > do` | `header` |
| 54 | data | `if (i_exist .or. "salt_channel.ini" /= "null") then > do > do isalti = 1, imax` | `salt_cha_ini(isalti)%name`, `salt_cha_ini(isalti)%conc` |


## `salt_hru.ini`

- Schema diff status: `['runtime_arity.changed']`
- Review needed: no
- Base schema presence: `{'resolved_sections': ['runtime_arity'], 'unresolved_sections': []}`
- Candidate schema presence: `{'resolved_sections': ['runtime_arity'], 'unresolved_sections': []}`

### Base exact read evidence

- Procedure: `salt_hru_aqu_read`
- Reader: `salt_hru_aqu_read.f90`
- Match: exact_filename
- Resolved default filename(s): `salt_hru.ini`
- Source filename expression(s): `in_init%salt_soil`, `salt_hru.ini`
- Open: line 22, file expression `in_init%salt_soil`, parser value `salt_hru.ini`, condition `if (i_exist .or. in_init%salt_soil /= "null") then > do`

| Line | Role | Condition | Fields read |
| --- | --- | --- | --- |
| 23 | title | `if (i_exist .or. in_init%salt_soil /= "null") then > do` | `titldum` |
| 25 | header | `if (i_exist .or. in_init%salt_soil /= "null") then > do` | `header` |
| 30 | title | `if (i_exist .or. in_init%salt_soil /= "null") then > do > do while (eof == 0)` | `titldum` |
| 32 | title | `if (i_exist .or. in_init%salt_soil /= "null") then > do > do while (eof == 0)` | `titldum` |
| 34 | title | `if (i_exist .or. in_init%salt_soil /= "null") then > do > do while (eof == 0)` | `titldum` |
| 48 | title | `if (i_exist .or. in_init%salt_soil /= "null") then > do` | `titldum` |
| 50 | header | `if (i_exist .or. in_init%salt_soil /= "null") then > do` | `header` |
| 54 | data | `if (i_exist .or. in_init%salt_soil /= "null") then > do > do isalti = 1, imax` | `salt_soil_ini(isalti)%name` |
| 56 | data | `if (i_exist .or. in_init%salt_soil /= "null") then > do > do isalti = 1, imax` | `titldum`, `salt_soil_ini(isalti)%soil` |
| 58 | data | `if (i_exist .or. in_init%salt_soil /= "null") then > do > do isalti = 1, imax` | `titldum`, `salt_soil_ini(isalti)%plt` |

- Procedure: `salt_hru_read`
- Reader: `salt_hru_read.f90`
- Match: exact_filename
- Resolved default filename(s): `salt_hru.ini`
- Source filename expression(s): `salt_hru.ini`
- Open: line 22, file expression `'salt_hru.ini'`, parser value `salt_hru.ini`, condition `if (i_exist .or. 'salt_hru.ini' /= "null") then > do`

| Line | Role | Condition | Fields read |
| --- | --- | --- | --- |
| 23 | title | `if (i_exist .or. 'salt_hru.ini' /= "null") then > do` | `titldum` |
| 25 | header | `if (i_exist .or. 'salt_hru.ini' /= "null") then > do` | `header` |
| 27 | header | `if (i_exist .or. 'salt_hru.ini' /= "null") then > do` | `header` |
| 29 | header | `if (i_exist .or. 'salt_hru.ini' /= "null") then > do` | `header` |
| 31 | header | `if (i_exist .or. 'salt_hru.ini' /= "null") then > do` | `header` |
| 36 | title | `if (i_exist .or. 'salt_hru.ini' /= "null") then > do > do while (eof == 0)` | `titldum` |
| 38 | title | `if (i_exist .or. 'salt_hru.ini' /= "null") then > do > do while (eof == 0)` | `titldum` |
| 40 | title | `if (i_exist .or. 'salt_hru.ini' /= "null") then > do > do while (eof == 0)` | `titldum` |
| 54 | title | `if (i_exist .or. 'salt_hru.ini' /= "null") then > do` | `titldum` |
| 56 | header | `if (i_exist .or. 'salt_hru.ini' /= "null") then > do` | `header` |
| 58 | header | `if (i_exist .or. 'salt_hru.ini' /= "null") then > do` | `header` |
| 60 | header | `if (i_exist .or. 'salt_hru.ini' /= "null") then > do` | `header` |
| 62 | header | `if (i_exist .or. 'salt_hru.ini' /= "null") then > do` | `header` |
| 66 | data | `if (i_exist .or. 'salt_hru.ini' /= "null") then > do > do isalti = 1, imax` | `salt_soil_ini(isalti)%name` |
| 68 | data | `if (i_exist .or. 'salt_hru.ini' /= "null") then > do > do isalti = 1, imax` | `salt_soil_ini(isalti)%soil` |
| 70 | data | `if (i_exist .or. 'salt_hru.ini' /= "null") then > do > do isalti = 1, imax` | `salt_soil_ini(isalti)%plt` |


### Candidate exact read evidence

- Procedure: `salt_hru_aqu_read`
- Reader: `salt_hru_aqu_read.f90`
- Match: exact_filename
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
- Match: exact_filename
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
- Open: line 44, file expression `"salt_recall.rec"`, parser value `salt_recall.rec`, condition `if (i_exist .or. "salt_recall.rec" /= "null") then > do`

| Line | Role | Condition | Fields read |
| --- | --- | --- | --- |
| 45 | title | `if (i_exist .or. "salt_recall.rec" /= "null") then > do` | `titldum` |
| 47 | header | `if (i_exist .or. "salt_recall.rec" /= "null") then > do` | `header` |
| 53 | data | `if (i_exist .or. "salt_recall.rec" /= "null") then > do > do while (eof == 0)` | `i` |
| 99 | title | `if (i_exist .or. "salt_recall.rec" /= "null") then > do` | `titldum` |
| 101 | header | `if (i_exist .or. "salt_recall.rec" /= "null") then > do` | `header` |
| 107 | data | `if (i_exist .or. "salt_recall.rec" /= "null") then > do > do ii = 1, imax` | `i` |
| 110 | data | `if (i_exist .or. "salt_recall.rec" /= "null") then > do > do ii = 1, imax` | `k`, `rec_salt(i)%name`, `rec_salt(i)%typ`, `rec_salt(i)%filename` |


### Candidate exact read evidence

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
