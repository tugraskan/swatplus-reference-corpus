---
kind: procedure
symbol: aqu_read_init
title: aqu_read_init
status: filled
source_hash: 626cd77dfb19c219
version_label: SWAT+ 62.0.0
locals:
  titldum: Scratch character holder used to read and discard title/label lines from `initial.aqu`,
    and also to advance through records while counting them.
  header: Scratch character holder for the file header line read from `initial.aqu` before
    the data records are processed.
  eof: I/O status flag for the reads on unit 105; it controls end-of-file/early-exit behavior
    while scanning and loading `initial.aqu`.
  imax: Record counter for the number of aquifer initialization entries found in `initial.aqu`;
    used to size the allocatable arrays and bound the read loop.
  i_exist: Logical flag from `inquire` indicating whether the configured aquifer input file
    exists before attempting to open it.
  iaqu: Loop counter used to read each aquifer initialization record into `aqu_init_dat_c`.
  iaq: Loop counter over aquifer objects in `sp_ob%aqu` when performing per-aquifer initialization
    work after the file is read.
  ics: Loop counter over initial water-constituent entries in `db_mx%om_water_init` for each
    aquifer object.
uses:
  basin_module: The basin-level aquifer initialization workflow depends on shared module state
    to know which file to read, how large to make the aquifer init arrays, how many aquifer
    objects exist, and how many initial constituent slots each aquifer should iterate over.
  input_file_module: This module supplies the configured aquifer initial-condition filename
    through `in_aqu%init`, which determines whether the routine can open `initial.aqu` at
    all.
  maximum_data_module: This module provides `db_mx%om_water_init`, the limit used in the post-read
    constituent initialization loop for each aquifer object.
  aquifer_module: This module owns the allocatable aquifer initialization data structures
    that are sized here and filled from `initial.aqu`.
  aqu_pesticide_module: These allocatable arrays are the target storage for the data staged
    from `initial.aqu`; without them, the routine cannot preserve aquifer initialization records
    for later use.
  hydrograph_module: The aquifer count in `sp_ob%aqu` controls how many aquifer objects receive
    the subsequent initialization pass after the file load.
  constituent_mass_module: These shared counters define the nested post-read loops that prepare
    each aquifer object and each initial organic/constituent slot.
---

<!-- facts:header -->

Reads and stages the aquifer initial-condition file `initial.aqu` for later aquifer initialization. It counts data records, allocates aquifer initial-data arrays, then loads the character-form records and touches aquifer/constituent counters for setup.

## Bottom Line

`aqu_read_init` prepares aquifer initial-condition data from the configured file `initial.aqu`. It first checks whether the file exists and is enabled, then scans the file to count how many aquifer records are present so it can allocate `aqu_init` and `aqu_init_dat_c` to the right size.

After allocation, it rewinds the file and reads the header plus each aquifer initialization record into `aqu_init_dat_c(iaqu)`. It then loops over the aquifer and constituent/object counts in shared model state to initialize per-aquifer organic/constituent setup points before returning.

## Arguments

<!-- facts:arguments -->

## Where It Fits

This routine runs in the aquifer-processing setup path, called by `proc_aqu` after other aquifer read/initialization routines have been invoked. Its results matter because later aquifer behavior depends on the allocated `aqu_init` and `aqu_init_dat_c` arrays and on the per-aquifer constituent setup loops that it performs.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. Initialize counters and test for input availability | The routine starts with zeroed I/O and size counters, then checks whether the configured aquifer initialization file exists and is not the literal string `null`. If the file is missing or disabled, it allocates a minimal `aqu_init(0:0)` placeholder and skips file loading. |
| 2. Open and scan the file to count records | When the file is available, the routine opens `initial.aqu` on unit 105, reads the title and header lines, and then advances through the remaining records with `read(...,iostat=eof)` while incrementing `imax` for each record encountered. |
| 3. Allocate aquifer initialization storage | Using the counted record total, the routine allocates `aqu_init(0:imax)` and `aqu_init_dat_c(0:imax)` so the shared aquifer initialization state matches the file size. |
| 4. Rewind and reread the file header | The file is rewound to the beginning and the title and header lines are read again so the second pass starts from a clean file position before loading records. |
| 5. Load each aquifer initialization record | The routine loops from `iaqu = 1` to `imax` and reads each aquifer initialization record into `aqu_init_dat_c(iaqu)`, stopping early if an end-of-file condition is reported. |
| 6. Close the file and initialize per-aquifer constituent loops | After the file is processed, the unit is closed. The routine then loops over each aquifer object in `sp_ob%aqu` and over each initial water-constituent slot in `db_mx%om_water_init` to set up the subsequent organic/constituent initialization path. |

## Modules Used

<!-- facts:uses -->

| Module | State touched | Key components |
| --- | --- | --- |
| [sym:basin_module] | `in_aqu, aqu_init, aqu_init_dat_c, sp_ob, db_mx` | `in_aqu%init, aqu_init(0:0), aqu_init(0:imax), aqu_init_dat_c(0:imax), aqu_init_dat_c(iaqu), sp_ob%aqu, db_mx%om_water_init` |
| [sym:input_file_module] | `in_aqu` | `in_aqu%init` |
| [sym:maximum_data_module] | `db_mx` | `db_mx%om_water_init` |
| [sym:aquifer_module] | `aqu_init, aqu_init_dat_c` |  |
| [sym:aqu_pesticide_module] | `aqu_init, aqu_init_dat_c` | `aqu_init(0:0), aqu_init(0:imax), aqu_init_dat_c(0:imax), aqu_init_dat_c(iaqu)` |
| [sym:hydrograph_module] | `sp_ob` | `sp_ob%aqu` |
| [sym:constituent_mass_module] | `sp_ob, db_mx` | `sp_ob%aqu, db_mx%om_water_init` |

## Local Variables

<!-- facts:locals -->

## State Changes

| Target | When | Meaning |
| --- | --- | --- |
| `none extracted` | none extracted | No assignment targets were extracted automatically. |

## File I/O

<!-- facts:io -->


## Lineage

Two source-backed commits were resolved for `aqu_read_init`. The file was introduced in `df07e3f` with the aquifer initialization read/allocate logic, and `39fabde` then initialized the local counters and scratch strings (`titldum`, `header`, `eof`, `imax`, `iaqu`, `iaq`, `ics`) to zero or empty-string defaults.

- df07e3f added `aqu_read_init.f90` with the full aquifer initialization file scan, allocation, rewind, and record-loading logic plus the post-read aquifer/constituent loops.
- 39fabde did not change the algorithmic flow; it only added explicit initial values to the local scratch variables and counters used by the routine.

## Review Notes

- Direct file I/O exists; verify file meanings and units before finalizing.
- info: weak_doc: Procedure 'aqu_read_init' documentation is very short.
