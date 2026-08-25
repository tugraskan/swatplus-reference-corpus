---
kind: procedure
symbol: recall_read_cs
title: recall_read_cs
status: filled
source_hash: d795aeb2c044b9ec
version_label: SWAT+ 62.0.0
locals:
  titldum: Temporary text buffer for the title/header line read from `cs_recall.rec` and each
    constituent recall file; it is also used to test for the special `'Incoming'` label that
    marks outside-watershed sources.
  header: Temporary text buffer for the second line of the recall files; it is read and skipped
    as file metadata before the data records are counted or loaded.
  ob_name: Holds the object name token read from each recall data record in a constituent
    recall file, identifying the source object associated with the record.
  ob_typ: Holds the object type token read from each recall data record in a constituent recall
    file, alongside `ob_name` when loading the time series.
  imax: Tracks the highest point-source index found in `cs_recall.rec`, so the routine can
    allocate `rec_cs(0:imax)` and the balance arrays to the needed size.
  iyr: Stores the calendar year read from each data row while scanning or loading a recall
    file, and is used to detect the start and end years of the record set.
  jday: Stores the day-of-year field read from daily recall records; it is also reused while
    scanning the file to detect year changes.
  mo: Stores the month field read from monthly or daily recall records and is used to select
    the current step within a year.
  day_mo: Holds the day-of-month field read from the recall files; it is part of the record
    timestamp but not otherwise transformed here.
  eof: I/O status flag from formatted reads; negative values signal end-of-file so the routine
    can stop scanning or loading the current file.
  i_exist: Logical flag set by `inquire` to indicate whether `cs_recall.rec` exists on disk;
    combined with `in_rec%recall_rec` to decide whether this routine should run.
  nbyr: Number of years represented in a constituent recall file; it determines the second
    dimension of `rec_cs(i)%hd_cs`.
  k: Sequence/index value read from the recall list file before loading `rec_cs(i)%name`,
    `rec_cs(i)%typ`, and `rec_cs(i)%filename` for each entry.
  iyrs: Year-slot index into `rec_cs(i)%hd_cs`; it advances as the file is read so data are
    stored in the correct year column.
  iyr_prev: Remembers the previous year while scanning or loading records so the code can
    detect when a year boundary has been crossed.
  istep: Time-step index within the current year; it maps daily/monthly/annual records into
    the first dimension of `rec_cs(i)%hd_cs`.
  ii: Loop index over point-source entries and over the allocated balance arrays.
  i: Point-source record index read from `cs_recall.rec`; it is used to index `rec_cs(i)`
    after the list file is parsed.
  ics: Constituent index used to loop across all simulated constituents when zeroing arrays
    and reading/writing the constituent mass vectors.
  jj: Year loop index used while allocating and initializing `rec_cs(i)%hd_cs` across the
    `nbyr` years in a file.
  kk: Time-step loop index used while allocating and initializing `rec_cs(i)%hd_cs` across
    366 daily steps, 12 monthly steps, or 1 annual step.
uses:
  hydrograph_module: This module is part of the routine's shared SWAT+ state context. Its
    presence indicates the recall reader runs in the same hydrologic bookkeeping environment
    as the rest of the model, even though no specific `hydrograph_module` symbol is directly
    referenced in the visible source span.
  input_file_module: '`input_file_module` supplies `in_rec%recall_rec`, the configuration
    switch that tells this routine whether recall processing is enabled and which recall-list
    filename should be consulted.'
  organic_mineral_mass_module: The routine imports this module as part of the constituent-loading
    environment, but the visible source span does not show a directly named symbol from it.
    It matters here because the recall reader participates in the broader mass-balance setup
    used by SWAT+ constituent handling.
  constituent_mass_module: '`constituent_mass_module` defines the `rec_cs` structure plus
    the `reccsb_*` and `recoutcsb_*` arrays that this routine allocates and fills. Those types
    hold the constituent mass histories that the routine reads from disk and preserves for
    later model use.'
  maximum_data_module: The routine imports this module as part of the model-wide maximum-data
    context, but no directly referenced symbol is visible in the extracted span. It still
    matters because the allocation sizes and shared state are managed in the same global data
    environment as other SWAT+ maxima.
  time_module: '`time_module` supplies the current simulation clock through `time%yrc`, which
    the routine uses to find the first in-file record matching the simulation year and set
    `rec_cs(i)%start_yr`.'
  exco_module: The module is imported because the routine has a branch for `rec_cs(i)%typ
    == 4` that mentions an exco crosswalk, so the exco state is relevant to potential recall-source
    mapping even though that branch is not implemented in the visible code.
---

<!-- facts:header -->

Reads constituent recall definitions and their time-series data files, then loads daily, monthly, or annual constituent mass histories into shared SWAT+ state.

## Bottom Line

`recall_read_cs` scans the recall configuration file to discover how many point-source recall files exist, allocates the constituent balance arrays, and then reads each listed file into `rec_cs` plus the within-watershed and outside-watershed balance arrays. It uses the current simulation year (`time%yrc`) to find the start of the series and stores the end year so later routing and constituent bookkeeping can access the recalled masses.

The routine matters because it sets up all constituent recall inputs before simulation continues. After this subroutine runs, other model code can use the populated `rec_cs`, `reccsb_*`, and `recoutcsb_*` arrays to apply point-source constituent loading through time.

## Arguments

<!-- facts:arguments -->

## Where It Fits

This routine runs during recall-input initialization, after the simulation clock and constituent database counts are available and after `in_rec%recall_rec` tells the model that recall processing is enabled. It prepares the `rec_cs` definitions and balance arrays before later routing and constituent-mass calculations consume them.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. Check whether recall processing is enabled | The routine tests whether `cs_recall.rec` exists or whether the recall input switch is active through `in_rec%recall_rec`. If neither condition holds, it skips all recall setup. |
| 2. Scan the recall-list file and count entries | It opens `cs_recall.rec`, skips the title and header lines, then reads entry indices until end-of-file to determine the largest point-source index (`imax`). |
| 3. Allocate the master recall and balance arrays | Using `imax` and `cs_db%num_cs`, the routine allocates `rec_cs(0:imax)` plus the within-watershed and outside-watershed constituent balance arrays, and initializes every constituent slot to zero. |
| 4. Rewind the recall-list file and reread each entry descriptor | After rewinding unit 107, it rereads the title and header, then loops through each point-source entry to load `rec_cs(i)%name`, `rec_cs(i)%typ`, and `rec_cs(i)%filename`. |
| 5. Open each per-source recall file and read metadata | For every non-type-4 source, it opens the source file, reads the title, year count, and header, sets `pts_type` from the `'Incoming'` label, and allocates `rec_cs(i)%hd_cs` to the correct daily, monthly, or annual shape. |
| 6. Determine the file end year and locate the simulation start year | It scans forward to the last date record to store `rec_cs(i)%end_yr`, rewinds the file, and then advances until `time%yrc` is found so it can set `rec_cs(i)%start_yr`, `istep`, and `iyrs`. |
| 7. Load constituent masses into the per-source time-series array | The main read loop copies each record's constituent vector into `rec_cs(i)%hd_cs(istep,iyrs)%cs`, then advances the daily, monthly, or annual indices and handles year boundaries with extra reads and backspacing. |
| 8. Close the source files and finish the recall-list pass | After each source is processed, it closes the source file, then closes `cs_recall.rec` and exits the outer loop once the recall setup is complete. |

## Modules Used

<!-- facts:uses -->

| Module | State touched | Key components |
| --- | --- | --- |
| [sym:hydrograph_module] | `hydrograph_module` | `No specific imported symbols from `hydrograph_module` were resolved in the context packet.` |
| [sym:input_file_module] | `in_rec` | `in_rec%recall_rec` |
| [sym:organic_mineral_mass_module] | `organic_mineral_mass_module` | `No specific imported symbols from `organic_mineral_mass_module` were resolved in the context packet.` |
| [sym:constituent_mass_module] | `reccsb_d, cs_db, reccsb_m, reccsb_y, reccsb_a, recoutcsb_d, recoutcsb_m, recoutcsb_y, recoutcsb_a, rec_cs` | `reccsb_d(ii)%cs, cs_db%num_cs, reccsb_m(ii)%cs, reccsb_y(ii)%cs, reccsb_a(ii)%cs, reccsb_d(ii)%cs(ics), reccsb_m(ii)%cs(ics), reccsb_y(ii)%cs(ics), reccsb_a(ii)%cs(ics), recoutcsb_d(ii)%cs, recoutcsb_m(ii)%cs, recoutcsb_y(ii)%cs, recoutcsb_a(ii)%cs, recoutcsb_d(ii)%cs(ics), recoutcsb_m(ii)%cs(ics), recoutcsb_y(ii)%cs(ics), recoutcsb_a(ii)%cs(ics), rec_cs(i)%name, rec_cs(i)%typ, rec_cs(i)%filename, rec_cs(i)%pts_type, rec_cs(i)%hd_cs(366,nbyr), rec_cs(i)%hd_cs(kk,jj)%cs, rec_cs(i)%hd_cs(12,nbyr), rec_cs(i)%hd_cs(1,nbyr), rec_cs(i)%hd_cs(1,jj)%cs, rec_cs(i)%end_yr, rec_cs(i)%start_yr, rec_cs(i)%hd_cs(istep,iyrs)%cs(ics)` |
| [sym:maximum_data_module] | `maximum_data_module` | `No specific imported symbols from `maximum_data_module` were resolved in the context packet.` |
| [sym:time_module] | `time` | `time%yrc` |
| [sym:exco_module] | `exco_module` | `No specific imported symbols from `exco_module` were resolved in the context packet.` |

## Local Variables

<!-- facts:locals -->

## State Changes

| Target | When | Meaning |
| --- | --- | --- |
| `reccsb_d(ii)%cs(ics)` | When a non-type-4 recall source is allocated and initialized, and then populated during the main read loop. | Holds the daily constituent-mass history for within-watershed point sources; it is zeroed first and then filled from each source file's time-series records. |
| `reccsb_m(ii)%cs(ics)` | When a non-type-4 recall source is allocated and initialized, and then populated during the main read loop. | Holds the monthly constituent-mass history for within-watershed point sources; it is cleared first and then loaded from the recall file records. |
| `reccsb_y(ii)%cs(ics)` | When a non-type-4 recall source is allocated and initialized, and then populated during the main read loop. | Holds the yearly constituent-mass history for within-watershed point sources; it is zeroed and then filled from the source file. |
| `reccsb_a(ii)%cs(ics)` | When a non-type-4 recall source is allocated and initialized, and then populated during the main read loop. | Holds the annual constituent-mass history for within-watershed point sources; it is initialized to zero and then loaded from the source file. |
| `recoutcsb_d(ii)%cs(ics)` | When a non-type-4 recall source is allocated and initialized, and then populated during the main read loop. | Holds the daily constituent-mass history for outside-watershed point sources; it is zeroed and then populated from the recall data file. |
| `recoutcsb_m(ii)%cs(ics)` | When a non-type-4 recall source is allocated and initialized, and then populated during the main read loop. | Holds the monthly constituent-mass history for outside-watershed point sources; it is cleared and then filled from the source file. |
| `recoutcsb_y(ii)%cs(ics)` | When a non-type-4 recall source is allocated and initialized, and then populated during the main read loop. | Holds the yearly constituent-mass history for outside-watershed point sources; it is zeroed and then loaded from the source file. |
| `recoutcsb_a(ii)%cs(ics)` | When a non-type-4 recall source is allocated and initialized, and then populated during the main read loop. | Holds the annual constituent-mass history for outside-watershed point sources; it is initialized to zero and then loaded from the source file. |
| `rec_cs(i)%pts_type` | Immediately after opening each non-type-4 source file and reading its first title line. | Records whether the source is treated as an outside-watershed input (`2` when the title is `Incoming`) or a within-watershed source (`1` otherwise). |
| `rec_cs(i)%hd_cs(kk,jj)%cs` | For each non-type-4 source file record read in the main loading loop. | Stores the constituent mass vector for the current time step and year slot, preserving the loaded values for later routing and balance calculations. |
| `rec_cs(i)%hd_cs(1,jj)%cs` | After the simulation-year search finds the first record where `iyr == time%yrc`. | Stores the first matching year's constituent vector in the year slot used to start the in-simulation recall series. |
| `rec_cs(i)%end_yr` | After scanning a source file to its last record before rewinding. | Stores the last calendar year present in that recall source file. |
| `rec_cs(i)%start_yr` | When the simulation-year search finds the first record with `iyr == time%yrc`. | Stores the first calendar year at or after which the recall series becomes active in the current simulation. |

## File I/O

<!-- facts:io -->


## Lineage

Four resolved commits changed `recall_read_cs`: df07e3f introduced the subroutine, its module imports, the file-scanning/allocating logic, and the per-source recall loading loops; 35b029c made a small cleanup by removing a blank line near the return; f8bb6ec changed the allocation calls so the constituent vectors and hourly/daily arrays are initialized with `source = 0.` before explicit zeroing; 39fabde initialized the local scalar variables with default values such as `0` and `""`, including `titldum`, `header`, `ob_name`, `ob_typ`, `imax`, `iyr`, `jday`, `mo`, `day_mo`, `eof`, `nbyr`, `k`, `iyrs`, `iyr_prev`, `istep`, `ii`, `i`, `ics`, `jj`, and `kk`. Commit 2ee1889 removed unused scalar declarations (`ipc`, `iexco_om`, `ifirst`, `iexo_allo`) from the routine.

- df07e3f added the entire recall-reading workflow, including the `cs_recall.rec` scan, allocation of `rec_cs`, `reccsb_*`, and `recoutcsb_*`, and the per-source file reads.
- 35b029c only removed a blank line before `return`; it did not change runtime behavior.
- f8bb6ec improved initialization by giving the allocated constituent arrays a zero source value at allocation time, reinforcing the explicit zeroing already present in the loops.
- 39fabde initialized the local scalars to safe defaults so the routine starts from known values before file I/O and indexing logic run.
- 2ee1889 removed unused local variables, reducing clutter without changing the recall-loading algorithm.

## Review Notes

- Direct file I/O exists; verify file meanings and units before finalizing.
- `hydrograph_module`, `organic_mineral_mass_module`, `maximum_data_module`, and `exco_module` were imported but no directly referenced symbols from them were resolved in the visible source span; descriptions therefore stay at module-level.
- The visible source contains a `case (4)` branch with only a comment about an exco crosswalk; no implementation is present in the extracted span, so the exco-related behavior is uncertain beyond that comment.
- `algorithm_steps` revised: collapsed the draft into 8 source-backed steps that follow the actual control flow and file lifecycle more closely than the original 5-step draft.
