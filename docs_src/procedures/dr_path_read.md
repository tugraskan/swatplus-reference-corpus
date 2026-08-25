---
kind: procedure
symbol: dr_path_read
title: dr_path_read
status: filled
source_hash: 42bb84f5ea2d0370
version_label: SWAT+ 62.0.0
locals:
  titldum: Scratch title/string buffer used to read and skip non-data lines from `dr_path.del`,
    including the first header line and the per-record name line before the data row is parsed.
  header: Scratch string used to read the second header line in `dr_path.del` during both
    the counting pass and the data-loading pass.
  eof: I/O status flag from each `read`; it controls loop termination and detects end-of-file
    or read failure while counting and loading records.
  imax: Counts how many pathogen delivery-ratio records are present in `dr_path.del`, and
    is then used to size the arrays that store them.
  ob1: First sequential delivery-ratio object index; set from `sp_ob1%dr` to define the start
    of the object range whose hydrographs will be filled.
  ob2: Last sequential delivery-ratio object index; computed from `sp_ob1%dr + sp_ob%dr -
    1` to define the end of the object range whose hydrographs will be filled.
  i_exist: Logical flag from `inquire` indicating whether the configured pathogen path file
    exists on disk.
  idr_path: Loop index over pathogen delivery-ratio profiles in the file and later over the
    profiles when crosswalking object state.
  ii: Loop index over each data row while reading `dr_path.del` into `dr_path_name` and `dr_path`.
  ipath: Loop index over the constituent-path entries on each delivery-ratio record when reading
    the row into `dr_path(ii)%path`.
  idr: Loop index over delivery-ratio database entries in `dr_db`, used to find the matching
    pathogen path profile and to map objects to profiles.
  iob: Loop index over delivery-ratio objects in `ob`, used to copy the selected pathogen
    delivery profile into each object hydrograph.
uses:
  hydrograph_module: This module provides the spatial-object bookkeeping that tells the routine
    which delivery-ratio objects exist (`sp_ob1%dr`, `sp_ob%dr`), which object database entry
    to use (`ob(iob)%props`), and where to store the resulting pathogen delivery hydrograph
    (`obcs(iob)%hd(1)%path`).
  dr_module: This module holds the delivery-ratio database and the sequential name/number
    lookup arrays. `dr_path_read` reads `dr_db(idr)%path_file` to match each delivery-ratio
    entry to the pathogen path profile name loaded from file.
  input_file_module: This module supplies the configured input filename for the pathogen path
    file. `in_delr%path` determines which file is opened, and its default is `dr_path.del`.
  organic_mineral_mass_module: The module is imported by the routine, but no extracted symbols
    from it are used in the visible source, so it does not affect the documented behavior
    here.
  constituent_mass_module: This module owns the pathogen delivery-ratio arrays and constituent
    count used by this routine. `dr_path(idr_path)%path` stores the per-profile delivery ratios,
    `cs_db%num_paths` sets their length, and `obcs(iob)%hd(1)%path` receives the selected
    profile for each delivery-ratio object.
  maximum_data_module: This module provides the maximum-data counters that `dr_path_read`
    updates and consults. `db_mx%dr_path` is set from the number of parsed pathogen profiles,
    and `db_mx%dr` controls how many delivery-ratio database entries are crosswalked.
---

<!-- facts:header -->

Reads and crosswalks the delivery-ratio pathogen path file into module arrays. It loads pathogen delivery ratios for each delivery-ratio definition and copies the matching profile into each object hydrograph.

## Bottom Line

`dr_path_read` is the pathogen-delivery counterpart of the delivery-ratio database reader. It opens the configured `dr_path.del` file, counts how many pathogen-delivery records it contains, allocates storage, then reads each named delivery-ratio profile and its pathogen path values into `dr_path` and `dr_path_name`.

After the file is loaded, the routine crosswalks each delivery-ratio database entry (`dr_db(idr)%path_file`) to the sequential profile number in `dr_path_num(idr)`, then uses that mapping to populate `obcs(iob)%hd(1)%path` for every delivery-ratio object. That makes the pathogen delivery ratios available to downstream hydrograph and constituent-mass calculations.

## Arguments

<!-- facts:arguments -->

## Where It Fits

This routine runs during delivery-ratio database initialization, immediately after `dr_db_read` has loaded the general delivery-ratio file list and before downstream modeling needs pathogen delivery ratios. `dr_db_read` calls it only when `cs_db%num_paths > 0`, and the resulting `dr_path_num` and `obcs(iob)%hd(1)%path` state is later used wherever delivery-ratio pathogen hydrographs are applied.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. Initialize scratch variables and counters | Sets up empty string buffers, zero counters, object bounds, and the I/O status flag before any file work begins. |
| 2. Confirm the configured input file should be processed | Checks whether the configured pathogen-path file exists, or whether the path name is not the sentinel value `null`, before attempting to read it. |
| 3. Scan the file to count data records | Opens the file, skips the two header lines, then advances through the remaining records to count how many pathogen delivery-ratio profiles are present. |
| 4. Save the record count and allocate storage | Stores the counted profile total in `db_mx%dr_path` and allocates the profile array, per-profile path arrays, and name/number lookup arrays sized to that count. |
| 5. Rewind and reread the file headers | Repositions the file to the beginning and rereads the title and header lines so the actual data pass starts from the first record again. |
| 6. Load each pathogen delivery-ratio record | For each profile, reads the line name and its `cs_db%num_paths` delivery-ratio values into `dr_path_name(ii)` and `dr_path(ii)%path`. |
| 7. Close the input file after loading | Closes unit 107 after all requested profiles have been read. |
| 8. Crosswalk delivery-ratio database entries to profile numbers | Loops through each delivery-ratio database entry and finds the matching pathogen profile name, storing the sequential profile index in `dr_path_num(idr)`. |
| 9. Assign the selected pathogen path to each delivery-ratio object | Uses the object range defined by the delivery-ratio spatial object counters to copy the mapped pathogen delivery profile into each object's hydrograph state. |
| 10. Return to the caller | Ends the subroutine after the shared delivery-ratio pathogen state has been populated. |

## Modules Used

<!-- facts:uses -->

| Module | State touched | Key components |
| --- | --- | --- |
| [sym:hydrograph_module] | `sp_ob1, sp_ob, ob, hd` | `sp_ob1%dr, sp_ob%dr, ob(iob)%props` |
| [sym:dr_module] | `dr_db, dr_path_num, dr_path_name` | `dr_db(idr)%path_file` |
| [sym:input_file_module] | `in_delr` | `in_delr%path` |
| [sym:organic_mineral_mass_module] | `none resolved` | `No candidate outside references were resolved to `organic_mineral_mass_module` in the extracted context.` |
| [sym:constituent_mass_module] | `dr_path, cs_db, obcs` | `dr_path(idr_path)%path, cs_db%num_paths, obcs(iob)%hd(1)%path` |
| [sym:maximum_data_module] | `db_mx` | `db_mx%dr_path, db_mx%dr` |

## Local Variables

<!-- facts:locals -->

## State Changes

| Target | When | Meaning |
| --- | --- | --- |
| `db_mx%dr_path` | After the file scan completes and `imax` has been determined from the number of non-header records in `dr_path.del`. | Stores the number of pathogen delivery-ratio profiles found in the input file so later allocation and downstream sizing can use the correct count. |
| `dr_path_num(idr)` | When a `dr_db(idr)%path_file` value matches one of the names read into `dr_path_name(idr_path)`. | Records which sequential pathogen profile belongs to each delivery-ratio database entry, enabling later lookup by object property index. |
| `obcs(iob)%hd(1)%path` | For each delivery-ratio object `iob` in the range `sp_ob1%dr` through `sp_ob1%dr + sp_ob%dr - 1` after its property index has been mapped through `dr_path_num`. | Copies the selected pathogen delivery-ratio vector into the object's hydrograph so the object uses the correct pathogen routing profile. |

## File I/O

<!-- facts:io -->


## Lineage

Resolved lineage evidence shows four historical commits affecting the procedure source span, but no diffs were available in the packet for any of them. The available record only confirms that the procedure existed through the source-history checkpoints `df07e3f`, `94b6dec`, `f8bb6ec`, and `39fabde`, without exposing the exact code changes for this routine.

## Review Notes

- Direct file I/O exists; verify file meanings and units before finalizing.
- warning: missing_doc: Procedure 'dr_path_read' has no extracted documentation comment.
- organic_mineral_mass_module is imported but no extracted symbols from it are used in the visible source.
- algorithm_steps revised: split the original broad scan/read/finalization block into file readiness, counting, allocation, reread, load, crosswalk, and object-population steps to match the visible source flow.
