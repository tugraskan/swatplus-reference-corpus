---
kind: io
source_symbols:
- pest_metabolite_read
title: '`pest_metabolite.pes`'
status: filled
source_hash: 477d05416260afed
version_label: SWAT+ 62.0.0
---

**Primary target:** `pestcp(:)` (array of `type pesticide_cp`)  
**Read by:** [sym:pest_metabolite_read]

## Bottom Line

The file `pest_metabolite.pes` configures pesticide metabolite data for the model, specifying the number and properties of metabolites derived from parent pesticides.

It is optional and only read if the file exists.

The reader `pest_metabolite_read` loads this file and populates the `pestcp` array with metabolite information linked to parent pesticides.

| Module | Role for this file |
| --- | --- |
| [sym:basin_module] | Provides `cs_db` which contains constituent mass database used to crosswalk metabolite names to constituent indices. |
| [sym:input_file_module] | Used for input file handling and possibly file existence checks. |
| [sym:maximum_data_module] | Provides `db_mx` which contains maximum pesticide parameters count used to loop over pesticide database. |
| [sym:pesticide_data_module] | Defines the `pesticide_cp` type and `pestcp` array where metabolite data is stored. |
| [sym:constituent_mass_module] | Provides `cs_db` which holds constituent names for cross-referencing metabolites. |

## File Variables

The file contains records of pesticide metabolites associated with parent pesticides. Each record specifies the number of metabolites and their decay fractions in different environmental compartments. The reader maps these records into the `pestcp` array of `type pesticide_cp`.

| Col | Header | Target | Type | Units | Meaning |
| --- | --- | --- | --- | --- | --- |
| 2 |  | `pestcp%num_metab` | integer |  | number of metabolites |
| 3 |  | `pestcp%daughter` | type (daughter_decay_fractions) |  | daughter decay fractions for each metabolite |
| 4 |  | `pestcp%decay_f` | real | none | exp of the rate const for degradation of the pest on foliage |
| 5 |  | `pestcp%decay_s` | real | none | exp of the rate const for degradation of the pest in soil |
| 6 |  | `pestcp%decay_a` | real | none | exp of the rate const for degradation of the pest in aquatic |
| 7 |  | `pestcp%decay_b` | real | none | exp of the rate const for degradation of the pest in benthic layer |

## Sample

```text
Example record block (from pest_metabolite.pes):
ParentName 3
Metab1 0.1 0.2 0.3 0.4
Metab2 0.05 0.1 0.15 0.2
Metab3 0.2 0.3 0.1 0.0
```

## Read Pattern

```fortran
open (106,file="pest_metabolite.pes")
read (106,*,iostat=eof) titldum
read (106,*,iostat=eof) header
read (106,*,iostat=eof) titldum, num_metab
rewind (106)
read (106,*,iostat=eof) parent_name, num_metab
read (106,*,iostat=eof) pestcp(ip)%daughter(imeta)%name, pestcp(ip)%daughter(imeta)%foliar_fr, pestcp(ip)%daughter(imeta)%soil_fr, pestcp(ip)%daughter(imeta)%aq_fr, pestcp(ip)%daughter(imeta)%ben_fr
```

## I/O Operations

| Direction | Op | Unit | Statement |
| --- | --- | --- | --- |
| File setup | `open` | 106 | `open (106,file="pest_metabolite.pes")` |
| Input | `read` | 106 | `read (106,*,iostat=eof) titldum` |
| Input | `read` | 106 | `read (106,*,iostat=eof) header` |
| Input | `read` | 106 | `read (106,*,iostat=eof) titldum, num_metab` |
| Input | `read` | 106 | `read (106,*,iostat=eof) titldum` |
| File control | `rewind` | 106 | `rewind (106)` |
| Input | `read` | 106 | `read (106,*,iostat=eof) titldum` |
| Input | `read` | 106 | `read (106,*,iostat=eof) header` |
| Input | `read` | 106 | `read (106,*,iostat=eof) parent_name, num_metab` |
| Input | `read` | 106 | `read (106,*,iostat=eof) pestcp(ip)%daughter(imeta)%name, pestcp(ip)%daughter(imeta)%foliar_fr, pestcp(ip)%daughter(imeta)%soil_fr, pestcp(ip)%daughter(imeta)%aq_fr, pestcp(ip)%daughter(imeta)%ben_fr` |
| File control | `close` | 106 | `close (106)` |

## Readers

| Procedure | Operations | Role |
| --- | --- | --- |
| [sym:pest_metabolite_read] | close, open, read, rewind | Reads the `pest_metabolite.pes` file if it exists, counts the number of parent pesticide records, and for each parent pesticide found in the pesticide database (`pestdb`), allocates and fills the metabolite daughter decay fractions in the `pestcp` array. It also cross-references metabolite names with the constituent mass database (`cs_db`) to assign constituent indices. |

## Review Notes

- Draft input-file overlay generated from static source facts; review and complete the remaining fields before promotion.
- The file is optional and only read if it exists, as indicated by the inquire check.
- The reader crosswalks parent pesticide names with the pesticide database and metabolite names with the constituent mass database to properly link data.
- No sample data was found in the source; the sample read format is a constructed example consistent with the read pattern.
