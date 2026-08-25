---
kind: procedure
symbol: dr_read_pest
title: dr_read_pest
status: filled
source_hash: 4b8955082db16446
version_label: SWAT+ 62.0.0
locals:
  titldum: Scratch string used to read and discard title/data lines while scanning `dr_pest.del`,
    and to test for end-of-file through `iostat=eof`.
  header: Scratch string used to read and discard the file header line during the scan and
    reload phases.
  eof: IO status flag from `read(..., iostat=eof)`; zero means keep reading, negative signals
    end-of-file and stops the scan or load loop.
  imax: Counts how many pesticide delivery-ratio records are present in `dr_pest.del`, and
    is then used to size the allocation for `dr_pest`, `dr_pest_num`, and `dr_pest_name`.
  ob1: Lower bound of the DR object range in `hydrograph_module`; used to start the loop that
    copies pesticide delivery data into object hydrographs.
  ob2: Upper bound of the DR object range in `hydrograph_module`; used to stop the loop that
    copies pesticide delivery data into object hydrographs.
  i_exist: Receives the result of `inquire(file=in_delr%pest, exist=i_exist)` so the routine
    can tell whether the configured pesticide delivery file exists before attempting to read
    it.
  idr_pest: Loop index over the pesticide delivery-ratio table while allocating arrays, crosswalking
    names, and later mapping object hydrographs to the correct delivery vector.
  ii: Loop index for reading each pesticide delivery-ratio record from the file into `dr_pest_name(ii)`
    and `dr_pest(ii)%pest`.
  ipest: Inner loop index across pesticide constituents when reading or storing the `dr_pest(ii)%pest`
    vector.
  idr: Loop index over delivery-ratio database entries (`dr_db`) when crosswalking file names
    to sequential pesticide record numbers and when mapping objects to DR definitions.
  iob: Loop index over DR objects in the hydrograph object range; used to copy the selected
    pesticide delivery vector into each object's hydrograph state.
uses:
  hydrograph_module: The hydrograph module supplies the DR object bounds (`sp_ob1%dr`, `sp_ob%dr`)
    and object connectivity (`ob(iob)%props`), which are needed to find every DR-linked object
    and decide which delivery-ratio record should be copied into its hydrograph state.
  dr_module: The DR module holds the list of DR file names (`dr_db(idr)%pest_file`) and the
    crosswalk array (`dr_pest_num`), so this routine can match configured DR database entries
    to the sequential rows read from `dr_pest.del`.
  input_file_module: The input-file module provides the configured pesticide delivery input
    filename (`in_delr%pest`), which determines which file is opened and scanned.
  organic_mineral_mass_module: The organic/mineral mass module is imported, but no extracted
    references from it appear in this routine. The lineages and source excerpt show no direct
    use of its state here, so its presence appears unused in the visible body.
  constituent_mass_module: The constituent-mass module defines the pesticide delivery-ratio
    storage (`dr_pest`), the number of pesticides to allocate/read (`cs_db%num_pests`), and
    the object hydrograph constituent array (`obcs(iob)%hd(1)%pest`) that receives the loaded
    pesticide delivery values.
  maximum_data_module: The maximum-data module provides the database-size counters (`db_mx%dr_pest`,
    `db_mx%dr`) that tell this routine how many pesticide DR records exist and how many DR
    database entries need crosswalking.
---

<!-- facts:header -->

Reads the pesticide delivery-ratio table for all delivery-ratio definitions and crosswalks each DR entry to its sequential pesticide file number. It also copies the pesticide delivery values into each object hydrograph's constituent mass state.

## Bottom Line

dr_read_pest opens the delivery-ratio pesticide file named by `in_delr%pest`, counts the data rows, allocates storage for that many delivery-ratio records, and then reads each record into `dr_pest_name` and `dr_pest(ii)%pest`. The file is expected to contain a title line, a header line, and then one line per DR entry with pesticide delivery values.

After loading the table, the routine crosswalks each delivery-ratio file name in `dr_db(idr)%pest_file` to the sequential index in `dr_pest_name`, stores that index in `dr_pest_num(idr)`, and then assigns the matching pesticide delivery vector to `obcs(iob)%hd(1)%pest` for each DR object. That makes the pesticide delivery data available to later hydrograph and constituent-mass calculations.

## Arguments

<!-- facts:arguments -->

## Where It Fits

This routine runs during delivery-ratio database initialization, after `dr_db_read` has already read the main DR file and set up the constituent counts. If pesticides are enabled (`cs_db%num_pests > 0`), later DR hydrograph behavior depends on its results because it populates the pesticide delivery vectors used by each DR object.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. Check whether the pesticide DR file should be read | The routine queries whether the configured pesticide delivery file exists and only proceeds when the file is present or the configured filename is not the literal "null". |
| 2. Open and scan the file to count records | It opens unit 107 on the pesticide delivery file, skips the title and header lines, then reads through the remaining lines to count how many DR records are present in `imax`. |
| 3. Save the record count and allocate storage | The routine stores the record count in `db_mx%dr_pest` and allocates the delivery-ratio arrays sized to that count, including a pesticide vector of length `cs_db%num_pests` for each record. |
| 4. Rewind the file and reload the data section | It rewinds unit 107 and rereads the title and header lines so the file can be processed from the beginning of the data section. |
| 5. Read each pesticide delivery record | For each DR record, the routine advances to the line, backspaces, then reads the DR file name and the pesticide delivery vector into `dr_pest_name(ii)` and `dr_pest(ii)%pest`. |
| 6. Close the pesticide file | After loading the records, the routine closes unit 107 and leaves the read loop. |
| 7. Crosswalk DR database entries to pesticide file rows | The routine loops over each DR database entry and finds the matching pesticide file name in `dr_pest_name`, storing the matching sequential index in `dr_pest_num(idr)`. |
| 8. Copy pesticide delivery data into DR object hydrographs | Using the DR object bounds from `sp_ob1%dr` and `sp_ob%dr`, the routine maps each DR object to its DR definition and copies the matching pesticide delivery vector into `obcs(iob)%hd(1)%pest`. |

## Modules Used

<!-- facts:uses -->

| Module | State touched | Key components |
| --- | --- | --- |
| [sym:hydrograph_module] | `sp_ob1, sp_ob, ob, hd` | `sp_ob1%dr, sp_ob%dr, ob(iob)%props` |
| [sym:dr_module] | `dr_db, dr_pest_num, dr_pest_name` | `dr_db(idr)%pest_file` |
| [sym:input_file_module] | `in_delr` | `in_delr%pest` |
| [sym:organic_mineral_mass_module] | `dr_pest` | `dr_pest(idr_pest)%pest, cs_db%num_pests` |
| [sym:constituent_mass_module] | `dr_pest, cs_db, obcs` | `dr_pest(idr_pest)%pest, cs_db%num_pests, obcs(iob)%hd(1)%pest` |
| [sym:maximum_data_module] | `db_mx` | `db_mx%dr_pest, db_mx%dr` |

## Local Variables

<!-- facts:locals -->

## State Changes

| Target | When | Meaning |
| --- | --- | --- |
| `db_mx%dr_pest` | After the file scan completes and `imax` has been determined from the number of data records in `dr_pest.del`. | `db_mx%dr_pest` is updated to the number of pesticide delivery-ratio records so later allocation and crosswalking loops know how many entries to process. |
| `dr_pest_num(idr)` | When a delivery-ratio database entry's `pest_file` name matches one of the file names read from `dr_pest.del`. | `dr_pest_num(idr)` is set to the sequential row number of the matching pesticide delivery record, giving the DR database a direct index into `dr_pest`. |
| `obcs(iob)%hd(1)%pest` | For each DR-linked object between `sp_ob1%dr` and `sp_ob1%dr + sp_ob%dr - 1` after the DR-to-pesticide crosswalk has been resolved. | `obcs(iob)%hd(1)%pest` receives the pesticide delivery vector for that object's DR definition so the object's hydrograph carries the correct pesticide delivery ratios. |

## File I/O

<!-- facts:io -->


## Lineage

The routine was introduced in commit df07e3f as a new source file with the full pesticide delivery-ratio read/crosswalk logic. Commit 94b6dec changed the pesticide allocation to use `source = 0.` for `dr_pest(idr_pest)%pest` and initialized `dr_pest_num` on allocation; commit f8bb6ec made the pesticide allocation zero-initialized; and commit 39fabde added default initial values for local scalars and zero-initialized `dr_pest_num` during allocation.

- df07e3f added the complete `dr_read_pest` routine, including file scanning, record allocation, crosswalking, and hydrograph population.
- f8bb6ec changed the pesticide delivery array allocation to zero-initialize `dr_pest(idr_pest)%pest`.
- 94b6dec kept the zero-initialized pesticide allocation and also changed `dr_pest_num` allocation to initialize to zero.
- 39fabde initialized local variables such as `titldum`, `header`, `eof`, `imax`, `ob1`, `ob2`, `idr_pest`, `ii`, `ipest`, `idr`, and `iob`, and preserved zero-initialized `dr_pest_num` allocation.

## Review Notes

- Direct file I/O exists; verify file meanings and units before finalizing.
- warning: missing_doc: Procedure 'dr_read_pest' has no extracted documentation comment.
- organic_mineral_mass_module is used via USE association but no extracted symbols from that module are referenced in the visible routine body.
