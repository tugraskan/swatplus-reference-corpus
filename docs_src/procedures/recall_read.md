---
kind: procedure
symbol: recall_read
title: recall_read
status: filled
source_hash: fc2a4fc3708d0771
version_label: SWAT+ 62.0.0
args:
  irec: '`irec` selects which recall database entry to process. The routine uses `recall_db(irec)%org_min%name`
    and `recall_db(irec)%org_min%tstep` to open the right file, choose the allocation shape,
    and decide how to interpret and store the time series for that one recall object.'
locals:
  titldum: Temporary title line read from the start of `recall_db(irec)%org_min%name`, `pest.com`,
    and each pesticide recall file so the routine can skip the file banner before reading
    numeric content.
  header: Temporary header line read after the title line in each input file; it advances
    past file metadata before the data scan begins.
  ob_name: Holds the observation or output name read from recall records in the daily/monthly/annual
    branches before the record is stored or echoed.
  ob_typ: Holds the observation type string read from recall records so the routine can preserve
    the source record metadata alongside the loaded value.
  imax: Tracks the maximum index found while scanning `pest.com` so the routine knows how
    large to make `rec_pest` before loading entries.
  iyr: Current year read from a recall or pesticide file record; it is used to locate the
    simulation start year and to detect year changes while loading data.
  jday: Julian day read from daily-type recall records; it identifies the record date when
    loading day-based values.
  mo: Calendar month read from recall records; it is used with `jday` and `day_mo` to preserve
    the record’s date fields.
  day_mo: Day-of-month field read from recall records and carried through the reads/writes
    as part of the source date metadata.
  eof: I/O status flag returned by each `read`; negative values break out at end-of-file and
    nonzero values control file-scanning loops.
  i_exist: Logical flag from `inquire` that tells the routine whether `pest.com` exists before
    it attempts to open and parse it.
  nbyr: Number of years read from each recall file header; it sets the second dimension for
    the per-year storage arrays.
  k: Leading integer field read from `pest.com` entries before the pesticide community name,
    type, and filename are stored.
  iyrs: Sequential year index into `recall(... )%hd` and `rec_pest(... )%hd_pest`; it is advanced
    as the routine crosses into a new simulation year.
  iyr_prev: Remembers the previously read year so the routine can detect when the input advances
    to a new year and increment `iyrs`.
  istep: Subdaily step counter used to place subdaily flow values into `recall(irec)%hyd_flo`
    and to read pesticide timestep records.
  ipestcom_db: Pointer-like integer read from `pest.com` that identifies which pesticide community
    database entry is being processed.
  ipc: Loop counter over pesticide community database records in `pest.com`; it drives the
    outer pesticide-loading pass.
  i: General loop/index variable used when scanning recall and pesticide lists and when indexing
    `rec_pest` entries.
  ii: Secondary counter used while iterating through the indexed entries after `imax` has
    been determined.
  iexco_om: Unused or unfilled local integer placeholder in this routine; no source lines
    show it being assigned or referenced further.
  iexo_allo: Unused or unfilled local integer placeholder in this routine; no source lines
    show it being assigned or referenced further.
  idaystep: Tracks the current daily aggregation slot when subdaily flow values are accumulated
    into daily `recall(irec)%hd` records.
  jday1: Saved Julian day for the next record read from a recall file so the routine can detect
    record boundaries and write to the correct slot.
  mo1: Saved month for the next record read from a recall file so the routine can place monthly
    data into the correct month index.
  iyr1: Keeps the year from the previous record so the routine can tell when the file advances
    into a new year.
  iprev: Loop index used when checking whether the current recall file has already been seen
    in a previous recall object.
uses:
  hydrograph_module: '`hydrograph_module` provides the shared hydrograph storage types and
    working variables that this routine fills. `recall(irec)%hyd_flo` and `recall(irec)%hd`
    hold the loaded recall time series, `ht1` carries the current hydrologic record being
    stored or accumulated, and `recall(irec)%start_yr` / `recall(i)%end_yr` define the time
    span needed to align the loaded data with the simulation years.'
  input_file_module: '`input_file_module` supplies the configured path to the master recall
    database input, which is the upstream file that `recalldb_read` prepares and that this
    routine later relies on indirectly through the recall database entry being processed.'
  organic_mineral_mass_module: No source-backed use of `organic_mineral_mass_module` state
    was extracted in the provided context, so its specific contribution to this routine is
    uncertain.
  constituent_mass_module: '`constituent_mass_module` defines the pesticide recall storage
    type that this routine allocates and fills from `pest.com` and each pesticide file. The
    loaded `rec_pest(i)` entries are later used to supply pesticide constituent histories
    to the model.'
  maximum_data_module: '`maximum_data_module` provides `db_mx%pestcom`, the count of pesticide
    community entries to scan from `pest.com`. That count controls how many pesticide recall
    files this routine expects to load.'
  time_module: '`time_module` supplies the current simulation year, run length, and subdaily
    step count. Those values control array allocation sizes, determine the starting year offset,
    and gate when records are stored into the correct year slot.'
  exco_module: No source-backed exco-specific state references were extracted beyond the module
    use statement, so its direct role here cannot be named from the provided evidence.
  recall_module: '`recall_module` holds the `recall_db` metadata for the selected recall object,
    including the organic-mineral file name and timestep type. This routine reads that metadata
    to decide which file to open, whether the file has already been handled, and how to size
    and populate the loaded recall arrays.'
---

<!-- facts:header -->

Reads a recall organic-mineral file and, if present, the pesticide community file list to populate shared recall input arrays and metadata. It determines record dimensions, allocates storage, and loads time series into module state for later simulation use.

## Bottom Line

`recall_read` is the file-loader for recall inputs. For the selected recall database entry `irec`, it opens the organic-mineral recall file named in `recall_db(irec)%org_min%name`, reads its header, figures out the start and end years, allocates the needed `recall(irec)` storage, and then loads the time-series data into `recall(irec)%hyd_flo`, `recall(irec)%hd`, and related fields based on the file’s timestep type.

After that, the routine checks for `pest.com`, scans each pesticide community listed there, opens each referenced pesticide recall file, allocates `rec_pest(i)%hd_pest` according to its timestep type, and reads the corresponding records into shared pesticide recall state. The results are used later by the recall-driven water-quality and constituent inputs in the model.

## Arguments

<!-- facts:arguments -->

## Where It Fits

This routine runs after `recalldb_read` has read the master recall database and selected the current recall entry `irec`. Its results feed the model’s later hydrograph, constituent, and pesticide-input behavior because the loaded `recall(...)` and `rec_pest(...)` arrays supply time-indexed input records used during simulation.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. Open the selected organic-mineral recall file and read its header records | The routine opens unit 108 on `recall_db(irec)%org_min%name`, reads the title, number of years, and header, and uses that metadata to begin parsing the selected recall file. |
| 2. Mark an existing recall entry if the file name has already been seen | The routine scans previous recall slots and, if the current organic-mineral file is recognized as already used, records that relationship in `recall_db(irec)%iorg_min`. |
| 3. Allocate storage for the recall series based on timestep type | Using `recall_db(irec)%org_min%tstep`, the routine allocates either subdaily flow plus daily hydrograph storage or daily, monthly, or annual hydrograph storage sized by `time%nbyr`. |
| 4. Identify the start year and align the read position with the simulation year | The routine reads the first date record to set `recall(irec)%start_yr`, then either searches forward to `time%yrc` or offsets `iyrs` so the loaded data align with the model start year. |
| 5. Load recall records and accumulate subdaily or timestep-specific values | The routine loops through the remaining records, advances the year index when needed, and stores data into `recall(irec)%hyd_flo` or the relevant `recall(irec)%hd` slot depending on whether the file is subdaily, daily, monthly, or annual. |
| 6. Save the ending year and close the organic-mineral file | After all recall data are processed, the routine stores the end year in `recall(i)%end_yr` and closes unit 108 for the organic-mineral file. |
| 7. Scan the pesticide community database file list | If `pest.com` exists, the routine opens it, reads header records, scans the integer indices to find the maximum entry, and allocates `rec_pest(0:imax)` accordingly. |
| 8. Rewind the pesticide list and read each community entry | The routine rewinds `pest.com`, rereads the header, loops over `db_mx%pestcom`, and reads each community line into `rec_pest(i)%name`, `rec_pest(i)%typ`, and `rec_pest(i)%filename`. |
| 9. Open each pesticide recall file and allocate its storage | For every pesticide file, the routine opens the file, reads its header, and allocates `rec_pest(i)%hd_pest` to 366, 12, or 1 rows depending on the pesticide timestep type. |
| 10. Read pesticide time series records into shared state | The routine searches for the first simulation year, then reads each pesticide record into `recall(i)%hd(istep,iyrs)` while updating the sequential year counter as the file advances. |
| 11. Close the pesticide file and finish the pesticide list | After each pesticide file has been read, the routine closes unit 108 and, once all communities are processed, closes `pest.com` on unit 107. |

## Modules Used

<!-- facts:uses -->

| Module | State touched | Key components |
| --- | --- | --- |
| [sym:hydrograph_module] | `recall, ht1, hd` | `recall(irec)%hyd_flo, recall(irec)%hd, recall(irec)%start_yr, recall(irec)%hyd_flo(istep,iyrs), ht1%flo, recall(irec)%hd(idaystep,iyrs), recall(irec)%hd(jday1,iyrs), recall(irec)%hd(mo1,iyrs), recall(irec)%hd(1,iyrs), recall(i)%end_yr, recall(i)%hd(istep,iyrs)` |
| [sym:input_file_module] | `in_rec` | `in_rec%recall_rec` |
| [sym:organic_mineral_mass_module] | `none resolved` | `none resolved` |
| [sym:constituent_mass_module] | `rec_pest` | `rec_pest(i)%name, rec_pest(i)%typ, rec_pest(i)%filename, rec_pest(i)%hd_pest(366,nbyr), rec_pest(i)%hd_pest(12,nbyr), rec_pest(i)%hd_pest(1,nbyr)` |
| [sym:maximum_data_module] | `db_mx` | `db_mx%pestcom` |
| [sym:time_module] | `time` | `time%step, time%nbyr, time%yrc, time%yrc_end` |
| [sym:exco_module] | `none resolved` | `none resolved` |
| [sym:recall_module] | `recall_db` | `recall_db(irec)%org_min%name, recall_db(irec)%iorg_min, recall_db(irec)%org_min%tstep` |

## Local Variables

<!-- facts:locals -->

## State Changes

| Target | When | Meaning |
| --- | --- | --- |
| `recall_db(irec)%iorg_min` | When the current recall database entry is not already mapped to a previous one and `recall_db(irec)%org_min%name` is being processed for the first time. | `recall_db(irec)%iorg_min` is set to the current index so later code can recognize this as the owning recall entry for the organic-mineral file rather than a duplicate reference. |
| `recall(irec)%start_yr` | After the first date record is read from the selected organic-mineral recall file. | `recall(irec)%start_yr` stores the first year present in the file so the model can align the file’s records with the simulation timeline. |
| `recall(irec)%hyd_flo(istep,iyrs)` | On each subdaily record when `recall_db(irec)%org_min%tstep` is `'sub'` and the current timestep is being loaded. | `recall(irec)%hyd_flo(istep,iyrs)` stores the subdaily flow converted from `ht1%flo` into a per-step volume for the current sequential year slot. |
| `recall(irec)%hd(idaystep,iyrs)` | On each daily record when `recall_db(irec)%org_min%tstep` is `'day'` and the current day index is being loaded. | `recall(irec)%hd(idaystep,iyrs)` accumulates the hydrologic output for the active daily slot as the routine reads or aggregates the record. |
| `recall(irec)%hd(1,iyrs)` | On annual recall records when `recall_db(irec)%org_min%tstep` is `'yr'` and the record is stored into the one-row annual array. | `recall(irec)%hd(1,iyrs)` receives the annual `ht1` value so the single yearly slot contains the loaded record for that year. |
| `recall(i)%end_yr` | After all records from the selected organic-mineral recall file have been read. | `recall(i)%end_yr` stores the last year encountered in the file so downstream model code can know the span of available recall data. |

## File I/O

<!-- facts:io -->


## Lineage

The resolved history shows three behavior changes to `recall_read`: in 2024-05-30 the routine originally loaded recall files and pesticide files from the master database layout; in 2024-08-12 it was modified to allocate recall arrays using `time%nbyr` and to add `jday1`, `mo1`, and `iyr1` bookkeeping for record handling; in 2024-10-08 it added the monthly diagnostic `write (10108,*)` that echoes loaded monthly recall records. In 2026-01-07 the file was renamed from `recall_read` to `recalldb_read` in the new patch context, but the resolved source span here still shows the `recall_read` subroutine body with the same file-loading behavior.

- 2024-05-30 introduced the core recall/pesticide file loading path, including allocation from the parsed file headers and the loop structure used to populate recall state.
- 2024-08-12 switched allocations to use the simulation-wide year count and added year/step tracking variables, which changed how record placement is aligned to the simulation timeline.
- 2024-10-08 added an output echo for monthly recall records to unit 10108, creating a new diagnostic write without changing the input parsing flow.

## Review Notes

- Direct file I/O exists; verify file meanings and units before finalizing.
- warning: missing_doc: Procedure 'recall_read' has no extracted documentation comment.
- algorithm_steps revised: condensed the initial file-header scan and the final close into clearer source-backed steps; kept the full loading flow under 11 steps.
- Source shows a likely self-comparison bug at line 132 (`recall_db(irec)%org_min%name == recall_db(irec)%org_min%name`); this is reported as uncertain behavior rather than corrected here.
- `input_file_module` and `exco_module` were imported but no source-backed symbol use was extracted in the provided context; their module-specific roles are therefore limited in this overlay.
- The Git lineage evidence includes a 2026-01-07 patch that renamed the routine in a later branch context, but the visible source block for this page still uses `recall_read`.
