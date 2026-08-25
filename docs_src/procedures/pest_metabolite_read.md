---
kind: procedure
symbol: pest_metabolite_read
title: pest_metabolite_read
status: filled
source_hash: 801c4d5367b13368
version_label: SWAT+ 62.0.0
locals:
  titldum: Scratch string used to read and discard title or blank/label lines from `pest_metabolite.pes`
    while advancing through the file.
  header: Scratch string used to read and discard the file header line before the parent records
    are parsed.
  parent_name: Stores the parent pesticide name from each parent record so it can be matched
    against `pestdb(ip)%name` before allocating and filling that parent's metabolite data.
  eof: I/O status flag for `read` statements; zero means keep reading, negative values end
    the scan or loading loops.
  imax: Counts how many parent pesticide records were found during the first pass through
    `pest_metabolite.pes`, so the file can be reread with the correct record count.
  i_exist: Holds the `inquire` result for whether `pest_metabolite.pes` is present; the routine
    only processes the file if this flag is true.
  ip: Loop index over pesticide database entries when matching a parent pesticide name to
    `pestdb(ip)%name`, and later reused as a daughter-count reader in the scan pass.
  ipb: Loop index over basin constituent pesticide names in `cs_db%pests` to find the sequential
    basin pesticide number for each metabolite name.
  imeta: Loop index over the metabolites belonging to the current parent pesticide while reading
    daughter records and crosswalking them to basin constituents.
  iparent: Loop index over parent pesticide records in the second pass through the metabolite
    file.
  num_metab: Number of metabolites declared for the current parent pesticide record; used
    to size the daughter array and control the metabolite read loop.
uses:
  basin_module: This module is imported but no resolved symbols from it are used in the extracted
    source span, so it does not affect the routine's visible behavior here.
  input_file_module: This module is imported but no resolved symbols from it are used in the
    extracted source span, so it does not affect the routine's visible behavior here.
  maximum_data_module: The routine uses `db_mx%pestparm` as the upper bound when searching
    the pesticide database for a parent name, so the maximum-data setting limits how many
    `pestdb` entries are examined.
  pesticide_data_module: The routine reads parent names and writes metabolite data into `pestdb`/`pestcp`,
    so this module holds the database entries and calculated crosswalk structures that are
    populated here.
  constituent_mass_module: The routine uses `cs_db%num_pests` and `cs_db%pests(ipb)` to translate
    metabolite names into sequential basin pesticide numbers, which links the metabolite file
    to the basin constituent list.
---

<!-- facts:header -->

Reads the pesticide metabolite definition file and crosswalks parent pesticides to their metabolite daughters and basin pesticide indices.

## Bottom Line

pest_metabolite_read opens `pest_metabolite.pes`, checks that the file exists, and scans it once to count how many parent pesticide records are present. It then rewinds the file and reads each parent entry, allocating each parent's metabolite array and filling the metabolite names, decay fractions, and sequential basin pesticide numbers.

The routine matters because later pesticide processing needs the parent-to-metabolite structure in `pestcp` and the basin crosswalk in `cs_db` to identify which simulated pesticide each daughter name refers to. It is called during model input setup from `proc_read` before downstream HRU and basin reads that rely on pesticide metadata.

## Arguments

<!-- facts:arguments -->

## Where It Fits

This routine runs during input preparation in `proc_read`, immediately after constituent database reading and before soil, pesticide HRU, and other basin initialization steps. Its results populate pesticide metabolite metadata used later when pesticide processes need parent/daughter relationships and sequential basin pesticide numbers.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. Initialize state and test for file presence | Resets the file-scan counters, inquires whether `pest_metabolite.pes` exists, and only enters the parsing logic when the file is present. |
| 2. First pass: count parent records | Opens the file, reads past the title and header, then loops through each parent block by reading the parent line and skipping its metabolite lines to count how many parent records exist. |
| 3. Rewind for data loading | Rewinds unit 106 and rereads the title and header so the file position returns to the start of the structured parent records. |
| 4. Read each parent and allocate metabolite storage | For each parent record, reads the parent name and metabolite count, searches `pestdb` for a matching parent pesticide, allocates that parent's daughter array, and stores the metabolite count in `pestcp(ip)%num_metab`. |
| 5. Load daughter records and map them to basin constituents | Reads each daughter record's name and decay fractions, then searches `cs_db%pests` to assign the daughter's sequential basin pesticide number in `pestcp(ip)%daughter(imeta)%num`. |
| 6. Close the file and return | Closes `pest_metabolite.pes` on unit 106 and exits the routine after the parent and metabolite state has been populated. |

## Modules Used

<!-- facts:uses -->

| Module | State touched | Key components |
| --- | --- | --- |
| [sym:basin_module] | `basin_module` |  |
| [sym:input_file_module] | `input_file_module` |  |
| [sym:maximum_data_module] | `db_mx` | `db_mx%pestparm` |
| [sym:pesticide_data_module] | `pestdb, pestcp` | `pestdb(ip)%name, pestcp(ip)%daughter(num_metab), pestcp(ip)%num_metab, pestcp(ip)%daughter(imeta)%name, pestcp(ip)%daughter(imeta)%foliar_fr, pestcp(ip)%daughter(imeta)%soil_fr, pestcp(ip)%daughter(imeta)%aq_fr, pestcp(ip)%daughter(imeta)%ben_fr, pestcp(ip)%daughter(imeta)%num` |
| [sym:constituent_mass_module] | `cs_db` | `cs_db%num_pests, cs_db%pests(ipb)` |

## Local Variables

<!-- facts:locals -->

## State Changes

| Target | When | Meaning |
| --- | --- | --- |
| `pestcp(ip)%num_metab` | When `parent_name == pestdb(ip)%name` during the second pass over `pest_metabolite.pes`. | `pestcp(ip)%num_metab` is set to the number of daughter metabolites declared for that parent so the model knows how many metabolite slots were allocated and loaded for the matched pesticide. |
| `pestcp(ip)%daughter(imeta)%num` | When a daughter name read from `pest_metabolite.pes` matches `cs_db%pests(ipb)` during the basin crosswalk loop. | `pestcp(ip)%daughter(imeta)%num` is set to the sequential basin pesticide index for that metabolite so later basin calculations can refer to the daughter by simulation number. |

## File I/O

<!-- facts:io -->


## Lineage

Two source-backed commits were resolved. The file was introduced in `df07e3f` with the full `pest_metabolite_read` implementation. `94b6dec` brought in the same source from bitbucket without changing the routine logic, and `39fabde` only initialized the local scalar variables with default values; the file I/O and crosswalk behavior stayed the same.

- df07e3f added `pest_metabolite_read` with file scanning, rewinding, allocation, and crosswalk logic for parent pesticides and their metabolites.
- 39fabde changed local variable declarations to initialize `titldum`, `header`, `parent_name`, `eof`, `imax`, `ip`, `ipb`, `imeta`, `iparent`, and `num_metab` to default values before use.

## Review Notes

- Direct file I/O exists; verify file meanings and units before finalizing.
- warning: missing_doc: Procedure 'pest_metabolite_read' has no extracted documentation comment.
- The `basin_module` and `input_file_module` imports were not resolved to specific used symbols in the extracted span; they may be unused here or used only through implicit side effects.
