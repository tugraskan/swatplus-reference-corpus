---
kind: procedure
symbol: constit_db_read
title: constit_db_read
status: filled
source_hash: 5d57ffc923155050
version_label: SWAT+ 62.0.0
locals:
  titldum: Temporary holder for the first title/header line read from the constituent database
    file; the routine reads it and then uses it only to advance past the header.
  i_exist: Logical flag set by `inquire` to indicate whether the configured constituent database
    file exists, so the routine can fall back to empty allocations when the file is missing
    or disabled.
  eof: '`iostat` status code for each file read; it is checked for end-of-file or read failure
    so the loop can stop safely.'
  i: Loop index used when reading arrays of names from the file, such as `cs_db%pests(i)`
    and `cs_db%paths(i)`.
  imax: Local counter initialized but not used in the extracted logic; it appears to be a
    leftover placeholder or unused bookkeeping variable.
  ipest: Loop index over the loaded pesticide names in `cs_db%pests` when matching them to
    `pestdb`.
  ipestdb: Loop index over the pesticide database records in `pestdb` while searching for
    a matching pesticide name.
  ipath: Loop index over the loaded pathogen names in `cs_db%paths` when matching them to
    `path_db`.
  ipathdb: Loop index over the pathogen database records in `path_db` while searching for
    a matching pathogen name.
uses:
  basin_module: '`basin_module` is needed because it provides basin-wide simulation state
    that this routine consults indirectly through the constituent-file path in `in_sim%cs_db`.
    Without that shared basin/input state, the routine would not know which constituent database
    file to open.'
  input_file_module: '`input_file_module` supplies `in_sim%cs_db`, the configured filename
    for the constituent database. That filename controls whether the routine opens a real
    input file or skips file loading and creates empty default arrays.'
  constituent_mass_module: '`constituent_mass_module` provides the shared `cs_db` structure
    that this routine fills. The routine reads counts and names into its allocatable arrays
    and later stores database crosswalk indices and the total constituent count there.'
  maximum_data_module: '`maximum_data_module` matters because `db_mx%pestparm` and `db_mx%path`
    give the upper bounds for scanning the pesticide and pathogen databases. Those limits
    determine how far the routine searches for matching names.'
  pesticide_data_module: '`pesticide_data_module` matters because `pestdb(ipestdb)%name` is
    the lookup table used to translate each constituent pesticide name into a pesticide database
    index stored in `cs_db%pest_num`.'
  pathogen_data_module: '`pathogen_data_module` matters because `path_db(ipathdb)%pathnm`
    is the lookup table used to translate each constituent pathogen name into a pathogen database
    index stored in `cs_db%path_num`.'
---

<!-- facts:header -->

Reads the constituent database file configured for the simulation and crosswalks constituent names to pesticide and pathogen database indices. It also counts total constituent categories and leaves empty default storage when no file is available.

## Bottom Line

`constit_db_read` loads the constituent setup from `in_sim%cs_db` (normally `constituents.cs`) into the shared `cs_db` structure. It reads counts and name lists for pesticides, pathogens, metals, salts, and other constituents, then resolves pesticide and pathogen names to their database indices using `pestdb` and `path_db`.

This matters because later model routines need both the raw constituent lists and the numeric links back to the detailed pesticide/pathogen databases. The routine also computes `cs_db%num_tot`, which summarizes how many total constituent entries are active for the simulation.

## Arguments

<!-- facts:arguments -->

## Where It Fits

This routine runs during model input setup, immediately after `proc_read` starts reading project files. `proc_read` calls it after climate-reading routines and before pesticide metabolite, soil/plant, and HRU/aquifer constituent readers. Its results feed later model setup that depends on resolved constituent counts and the pesticide/pathogen crosswalks.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. Check constituent file availability | The routine checks whether the configured constituent database file exists and whether `in_sim%cs_db` is not the literal string `null`. If the file is unavailable or disabled, it allocates one-element default arrays for pests, paths, metals, and salts so downstream code can still reference `cs_db` safely. |
| 2. Open and skip the title line | When the file is available, the routine opens unit 106 on `in_sim%cs_db` and reads the first record into `titldum`. This consumes the title/header line before numeric data are read. |
| 3. Read pesticide count and names | The routine reads `cs_db%num_pests`, allocates `cs_db%pests(0:cs_db%num_pests)` and `cs_db%pest_num(0:cs_db%num_pests)`, then reads the pesticide names into the array. The `iostat` check stops processing if end-of-file is reached early. |
| 4. Read pathogen count and names | The routine reads `cs_db%num_paths`, allocates `cs_db%paths` and `cs_db%path_num`, and reads the pathogen names from the file. These names are later matched to the pathogen database. |
| 5. Read metal count and names | The routine reads `cs_db%num_metals`, allocates `cs_db%metals` and `cs_db%metals_num`, and fills the metal-name list. This preserves the configured heavy-metal constituents for later use. |
| 6. Read salt count and names | The routine reads `cs_db%num_salts`, allocates `cs_db%salts` and `cs_db%salts_num`, and loads the salt-ion names. The inline comment marks this section as salt ions. |
| 7. Read other constituent count and names | The routine reads `cs_db%num_cs`, allocates `cs_db%cs` and `cs_db%cs_num`, and loads the remaining constituent names. This finishes the raw constituent lists from the file. |
| 8. Match pesticide names to the pesticide database | For each loaded pesticide name, the routine scans `pestdb(1:db_mx%pestparm)` until it finds a matching `pestdb(ipestdb)%name`, then stores that database index in `cs_db%pest_num(ipest)`. This converts names from the constituent file into database references. |
| 9. Match pathogen names to the pathogen database | For each loaded pathogen name, the routine scans `path_db(1:db_mx%path)` until it finds a matching `path_db(ipathdb)%pathnm`, then stores that database index in `cs_db%path_num(ipath)`. This converts pathogen names into database references. |
| 10. Compute total constituent count | The routine sums the counts of pesticides, pathogens, metals, salt ions, and other constituents into `cs_db%num_tot`. This provides a single total used to summarize how many constituent entries are active. |
| 11. Close the constituent file | The routine closes unit 106 and returns. Closing the file ends the read phase and releases the constituent database handle. |

## Modules Used

<!-- facts:uses -->

| Module | State touched | Key components |
| --- | --- | --- |
| [sym:basin_module] | `basin_module` | `inquire uses `in_sim%cs_db`` |
| [sym:input_file_module] | `in_sim` | `in_sim%cs_db` |
| [sym:constituent_mass_module] | `cs_db` | `cs_db%pests(0:0), cs_db%paths(0:0), cs_db%metals(0:0), cs_db%salts(0:0), cs_db%num_pests, cs_db%pests, cs_db%pest_num, cs_db%pests(i), cs_db%num_paths, cs_db%paths, cs_db%path_num, cs_db%paths(i), cs_db%num_metals, cs_db%metals, cs_db%metals_num, cs_db%metals(i), cs_db%num_salts, cs_db%salts, cs_db%salts_num, cs_db%salts(i), cs_db%num_cs, cs_db%cs, cs_db%cs_num, cs_db%cs(i), cs_db%pests(ipest), cs_db%pest_num(ipest), cs_db%paths(ipath), cs_db%path_num(ipath), cs_db%num_tot` |
| [sym:maximum_data_module] | `db_mx` | `db_mx%pestparm, db_mx%path` |
| [sym:pesticide_data_module] | `pestdb` | `pestdb(ipestdb)%name` |
| [sym:pathogen_data_module] | `path_db` | `path_db(ipathdb)%pathnm` |

## Local Variables

<!-- facts:locals -->

## State Changes

| Target | When | Meaning |
| --- | --- | --- |
| `cs_db%pest_num(ipest)` | When a loaded pesticide name exactly matches `pestdb(ipestdb)%name` during the nested pesticide lookup loop. | `cs_db%pest_num(ipest)` is set to the matching pesticide database index so later routines can resolve each constituent pesticide name to the detailed pesticide record. |
| `cs_db%path_num(ipath)` | When a loaded pathogen name exactly matches `path_db(ipathdb)%pathnm` during the nested pathogen lookup loop. | `cs_db%path_num(ipath)` is set to the matching pathogen database index so later routines can resolve each constituent pathogen name to the detailed pathogen record. |
| `cs_db%num_tot` | After all constituent counts are read or defaulted, just before the file is closed. | `cs_db%num_tot` becomes the sum of all loaded constituent categories, giving a total count of active pesticide, pathogen, metal, salt, and other constituent entries. |

## File I/O

<!-- facts:io -->


## Lineage

Source-backed lineage resolved three commits. The procedure was introduced in `df07e3f` as a new file that reads `constituents.cs`, allocates the constituent arrays, crosswalks pesticide and pathogen names, and computes `cs_db%num_tot`. `c7c8e22` kept the same logic while adding the latest upstream source snapshot. `39fabde` made only initialization-related changes: it gave local scalars default values and changed several allocation statements to initialize the integer mapping arrays to zero.

- `df07e3f` added the full `constit_db_read` subroutine, including file existence checking, constituent list reads, name-to-database crosswalking, and total-count computation.
- `39fabde` initialized local variables and zero-filled the mapping arrays on allocation (`pest_num`, `path_num`, `metals_num`, `salts_num`, `cs_num`) so unmapped entries start from 0 instead of undefined values.

## Review Notes

- Direct file I/O exists; verify file meanings and units before finalizing.
- warning: missing_doc: Procedure 'constit_db_read' has no extracted documentation comment.
