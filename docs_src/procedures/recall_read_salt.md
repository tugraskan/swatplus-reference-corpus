---
kind: procedure
symbol: recall_read_salt
title: recall_read_salt
status: filled
source_hash: 8a674689618baa34
version_label: SWAT+ 62.0.0
locals:
  titldum: Temporary 80-character text buffer used to read and discard title lines from `salt_recall.rec`
    and each pointed-to salt recall file.
  header: Temporary 80-character text buffer used to read and discard header lines before
    the data records are scanned or loaded.
  ob_name: Holds the object name token read from a salt recall data line so the routine can
    capture the point-source identifier from the file.
  ob_typ: Holds the object type token read from a salt recall data line; used alongside `ob_name`
    when parsing each point-source record.
  imax: Tracks the maximum point-source index found while scanning `salt_recall.rec`, and
    therefore the number of recall entries to allocate.
  iyr: Holds the calendar year read from a daily, monthly, or annual record while the routine
    searches for the file end and simulation start position.
  jday: Holds the Julian day read from a daily record and is also used to advance through
    daily time steps.
  mo: Holds the month number read from monthly or annual records and is used to advance monthly
    time steps.
  day_mo: Holds the day-of-month field read from the recall file records; it is part of the
    record format but is not used for control logic here.
  eof: I/O status flag from each `read`; negative values signal end-of-file or read failure
    and terminate the current scan or load loop.
  i_exist: Logical flag from `inquire` indicating whether `salt_recall.rec` exists before
    the routine attempts to process it.
  nbyr: Number of years represented in the current point-source file; used to size the second
    dimension of `hd_salt`.
  k: Sequence/index value read from `salt_recall.rec` for each point-source entry; used together
    with the stored metadata fields.
  iyrs: Index of the current year slot within `hd_salt`, advanced as the routine steps through
    the record series.
  iyr_prev: Remembers the previous year value so the routine can detect a year boundary while
    stepping through daily or monthly records.
  istep: 'Current time-step position within the active year for the selected recall type:
    day, month, or annual slot.'
  ii: Loop counter used for allocating and initializing the per-point-source salt balance
    arrays and later for traversing loaded point-source entries.
  i: Point-source record index read from `salt_recall.rec`; used to address the corresponding
    `rec_salt(i)` structure.
  isalt: Loop counter over salt constituents; used to allocate, initialize, and assign each
    constituent mass value.
  jj: Year-slot loop counter used when allocating or filling `hd_salt` across all years represented
    in a file.
  kk: Time-step loop counter used when allocating or filling `hd_salt` across all days, months,
    or annual slots for a year.
uses:
  hydrograph_module: The routine works with hydrograph-style time-series storage for recall
    inputs, so this module is the shared home for the structures that hold loaded recall data.
  input_file_module: This module matters because the routine depends on shared input-file
    control state to know whether the configured salt recall file should be processed.
  organic_mineral_mass_module: The routine reads salinity recall data that feed the broader
    organic/mineral mass bookkeeping, so this module is part of the shared model state environment
    even though no specific symbol use was extracted here.
  constituent_mass_module: '`constituent_mass_module` defines the salt constituent storage
    types and the `rec_salt` structures that this routine allocates and fills; it also provides
    `cs_db%num_salts`, which determines how many salt values are read per record. Without
    those shared types, the routine could not size `hd_salt` or store the per-salt balance
    arrays.'
  maximum_data_module: This routine sizes storage from discovered input maxima such as the
    number of point-source entries and years; that maximum-data state is what lets the code
    allocate `rec_salt` and the balance arrays correctly.
  time_module: '`time%yrc` supplies the current simulation year so the routine can find the
    starting record in each recall file and set `rec_salt(i)%start_yr` when the loaded time
    series reaches the active year.'
  exco_module: The code includes a special `typ == 4` branch marked for cross-walking with
    exco data, so `exco_module` is the shared context for that unresolved point-source mapping
    path.
---

<!-- facts:header -->

Reads salt recall configuration and point-source time series, then loads them into shared salinity balance storage.

## Bottom Line

`recall_read_salt` scans `salt_recall.rec` to discover each salt recall file, sizes the shared recall arrays, and then reads each listed file into `rec_salt` and the salt balance arrays. It distinguishes point sources originating inside the watershed from outside sources, records the point-source type, and allocates per-salt storage according to the number of simulated salts in `cs_db%num_salts`.

For each recall file, the routine determines the data span, captures the start and end years, and loads daily, monthly, or annual salt time series into `rec_salt(i)%hd_salt(...)%salt(...)`. Those values become the input state used later by the salinity recall/balance workflow.

## Arguments

<!-- facts:arguments -->

## Where It Fits

This routine runs during input initialization after `time%yrc` and the shared salt-constituent database are available. It is responsible for populating `rec_salt` and the salt balance arrays before later simulation code uses those loaded values to supply recall salinity inputs.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. Initialize counters and check for the master recall list | The routine clears the EOF and maximum-index counters, checks whether `salt_recall.rec` exists, and only proceeds into the read loop when the file is present or the configured file name is not the sentinel value. |
| 2. Scan `salt_recall.rec` to find the highest point-source index | It opens `salt_recall.rec`, reads and discards the title and header lines, then reads successive point-source indices to compute `imax` as the maximum listed source number. |
| 3. Allocate and initialize salt balance storage | Using `imax` and `cs_db%num_salts`, the routine allocates `rec_salt` and the daily, monthly, yearly, and annual salt balance arrays, then zeros every constituent slot for both internal and external point-source categories. |
| 4. Rewind the master list and load point-source metadata | The file is rewound, the title and header are reread, and each point-source record is reread to capture the source index, name, type, and per-source filename into `rec_salt(i)`. |
| 5. Open each recall file and allocate its time-series storage | For every non-exco point-source file, the routine opens the file, reads its title, year count, and header, classifies the point source as inside or outside the watershed from the title string, and allocates `hd_salt` to match daily, monthly, or annual resolution. |
| 6. Determine file end year and simulation start position | The routine scans forward to find the last record year, stores it in `rec_salt(i)%end_yr`, rewinds the file, and then searches for the first record at the current simulation year `time%yrc`, recording `start_yr`, the active year index, and the starting step. |
| 7. Load recall records into the per-source time series | It repeatedly reads each dated record plus object metadata and all salt constituent masses into `rec_salt(i)%hd_salt(istep,iyrs)%salt(isalt)`, then advances daily, monthly, or annual counters and handles year rollovers by updating the step and year indices. |
| 8. Close files and finish the routine | After loading each recall file, the routine closes unit 108, then closes `salt_recall.rec` on unit 107 and returns to the caller. |

## Modules Used

<!-- facts:uses -->

| Module | State touched | Key components |
| --- | --- | --- |
| [sym:hydrograph_module] | `hydrograph_module` | `Imported module only; no specific candidate references were resolved in the extracted source.` |
| [sym:input_file_module] | `input_file_module` | `Imported module only; no specific candidate references were resolved in the extracted source.` |
| [sym:organic_mineral_mass_module] | `organic_mineral_mass_module` | `Imported module only; no specific candidate references were resolved in the extracted source.` |
| [sym:constituent_mass_module] | `recsaltb_d, cs_db, recsaltb_m, recsaltb_y, recsaltb_a, recoutsaltb_d, recoutsaltb_m, recoutsaltb_y, recoutsaltb_a, rec_salt` | `recsaltb_d(ii)%salt, cs_db%num_salts, recsaltb_m(ii)%salt, recsaltb_y(ii)%salt, recsaltb_a(ii)%salt, recsaltb_d(ii)%salt(isalt), recsaltb_m(ii)%salt(isalt), recsaltb_y(ii)%salt(isalt), recsaltb_a(ii)%salt(isalt), recoutsaltb_d(ii)%salt, recoutsaltb_m(ii)%salt, recoutsaltb_y(ii)%salt, recoutsaltb_a(ii)%salt, recoutsaltb_d(ii)%salt(isalt), recoutsaltb_m(ii)%salt(isalt), recoutsaltb_y(ii)%salt(isalt), recoutsaltb_a(ii)%salt(isalt), rec_salt(i)%name, rec_salt(i)%typ, rec_salt(i)%filename, rec_salt(i)%pts_type, rec_salt(i)%hd_salt(366,nbyr), rec_salt(i)%hd_salt(kk,jj)%salt, rec_salt(i)%hd_salt(12,nbyr), rec_salt(i)%hd_salt(1,nbyr), rec_salt(i)%hd_salt(1,jj)%salt, rec_salt(i)%end_yr, rec_salt(i)%start_yr, rec_salt(i)%hd_salt(istep,iyrs)%salt(isalt)` |
| [sym:maximum_data_module] | `maximum_data_module` | `Imported module only; no specific candidate references were resolved in the extracted source.` |
| [sym:time_module] | `time` | `time%yrc` |
| [sym:exco_module] | `exco_module` | `Imported module only; no specific candidate references were resolved in the extracted source.` |

## Local Variables

<!-- facts:locals -->

## State Changes

| Target | When | Meaning |
| --- | --- | --- |
| `recsaltb_d(ii)%salt(isalt)` | When `salt_recall.rec` is present or the configured sentinel check passes, and the initial scan finds the largest listed source index. | `recsaltb_d(ii)%salt(isalt)` is allocated and initialized to zero for each point source and salt constituent so later salinity accounting has a clean daily internal-source balance array. |
| `recsaltb_m(ii)%salt(isalt)` | When `salt_recall.rec` is present or the configured sentinel check passes, and the initial scan finds the largest listed source index. | `recsaltb_m(ii)%salt(isalt)` is allocated and initialized to zero for each point source and salt constituent so later salinity accounting has a clean monthly internal-source balance array. |
| `recsaltb_y(ii)%salt(isalt)` | When `salt_recall.rec` is present or the configured sentinel check passes, and the initial scan finds the largest listed source index. | `recsaltb_y(ii)%salt(isalt)` is allocated and initialized to zero for each point source and salt constituent so later salinity accounting has a clean yearly internal-source balance array. |
| `recsaltb_a(ii)%salt(isalt)` | When `salt_recall.rec` is present or the configured sentinel check passes, and the initial scan finds the largest listed source index. | `recsaltb_a(ii)%salt(isalt)` is allocated and initialized to zero for each point source and salt constituent so later salinity accounting has a clean annual internal-source balance array. |
| `recoutsaltb_d(ii)%salt(isalt)` | When `salt_recall.rec` is present or the configured sentinel check passes, and the initial scan finds the largest listed source index. | `recoutsaltb_d(ii)%salt(isalt)` is allocated and initialized to zero for each point source and salt constituent so later salinity accounting has a clean daily external-source balance array. |
| `recoutsaltb_m(ii)%salt(isalt)` | When `salt_recall.rec` is present or the configured sentinel check passes, and the initial scan finds the largest listed source index. | `recoutsaltb_m(ii)%salt(isalt)` is allocated and initialized to zero for each point source and salt constituent so later salinity accounting has a clean monthly external-source balance array. |
| `recoutsaltb_y(ii)%salt(isalt)` | When `salt_recall.rec` is present or the configured sentinel check passes, and the initial scan finds the largest listed source index. | `recoutsaltb_y(ii)%salt(isalt)` is allocated and initialized to zero for each point source and salt constituent so later salinity accounting has a clean yearly external-source balance array. |
| `recoutsaltb_a(ii)%salt(isalt)` | When `salt_recall.rec` is present or the configured sentinel check passes, and the initial scan finds the largest listed source index. | `recoutsaltb_a(ii)%salt(isalt)` is allocated and initialized to zero for each point source and salt constituent so later salinity accounting has a clean annual external-source balance array. |
| `rec_salt(i)%pts_type` | When the per-source file title line is read and compared to the string `Incoming`. | `rec_salt(i)%pts_type` is set to 2 for outside-watershed inflows and 1 otherwise, which determines how later salinity recall data are interpreted. |
| `rec_salt(i)%hd_salt(kk,jj)%salt` | When a record is read from a daily, monthly, or annual salt recall file into the active step/year position. | `rec_salt(i)%hd_salt(kk,jj)%salt` stores the constituent masses for the current time step and year slot in the per-source hydrograph-style recall array. |
| `rec_salt(i)%hd_salt(1,jj)%salt` | When a daily, monthly, or annual point-source file is allocated for its yearly storage. | `rec_salt(i)%hd_salt(1,jj)%salt` receives the per-constituent zero-initialized storage for each year slot in annual recall files, or the first index of the allocated time grid in the general allocation pattern. |
| `rec_salt(i)%end_yr` | After scanning the point-source file to its last dated record. | `rec_salt(i)%end_yr` is set to the final year found in the source file so the model knows the available data range. |
| `rec_salt(i)%start_yr` | When the routine finds the first record whose year matches `time%yrc`. | `rec_salt(i)%start_yr` is set to that active simulation year so downstream loading starts from the correct year in the source file. |

## File I/O

<!-- facts:io -->


## Lineage

Four resolved commits changed `recall_read_salt`: df07e3f introduced the routine and its full file-scanning/allocation/loading logic; 35b029c made a minor end-of-file cleanup by removing a blank line before `return`; f8bb6ec changed the allocation of the salt arrays and per-source `hd_salt` storage to use `source = 0.` and then explicitly zeroed them; 39fabde initialized the local scalars and buffers with default values. bd18ad4 later commented out `ipc` and removed unused local declarations, but did not change the routine’s behavior.

- df07e3f created the complete salt recall reader, including master-list scanning, per-file allocation, date stepping, and constituent mass loading.
- 35b029c only removed a blank line before the final `return`; no behavioral change is shown in the diff.
- f8bb6ec changed array allocation to initialize salt storage to zero at allocation time for both balance arrays and `hd_salt`, reducing reliance on post-allocation clearing.
- 39fabde added default initializers to local character and integer variables so the routine starts from defined values before reading files.
- bd18ad4 only commented out or removed unused local variables, with no effect on file parsing or state loading.

## Review Notes

- Direct file I/O exists; verify file meanings and units before finalizing.
- warning: missing_doc: Procedure 'recall_read_salt' has no extracted documentation comment.
- algorithm_steps revised: reduced the draft to eight source-backed steps that match the actual control flow and use line-numbered evidence from the provided source block.
- Source uncertainty: `hydrograph_module`, `input_file_module`, `organic_mineral_mass_module`, `maximum_data_module`, and `exco_module` had no resolved candidate references in the packet, so their `outside` fields stay at the module level rather than naming unverified symbols.
