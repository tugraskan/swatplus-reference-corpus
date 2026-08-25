---
kind: procedure
symbol: gwflow_chan_read
title: gwflow_chan_read
status: filled
source_hash: 36b423a7e63df8ae
version_label: SWAT+ 62.0.0
locals:
  line_buf: Temporary text buffer that holds one full data line from chancell.gw before it
    is split into fields.
  fields: Fixed-size array of substrings produced by split_line; each element holds one parsed
    column from the current chancell.gw record.
  nf: Number of parsed fields returned by split_line for the current input line, used to decide
    whether optional dep_zone and obs columns are present.
  k: Loop index over the channel-cell connection records, from 1 to num_chancells.
  cell_id: Cell identifier parsed from the first column of each chancell.gw record, then stored
    in gw_chan_id(k).
  channel: Channel identifier parsed from the third column of each record, then stored in
    gw_chan_chan(k).
  chan_zone: Channel zone parsed from the fifth column of each record, then stored in gw_chan_zone(k).
  dep_zone: Optional depth-zone identifier parsed from column 6 when present; otherwise reset
    to 0 and stored in gw_chan_dpzn(k).
  obs: Optional observation flag parsed from column 7 when present; otherwise reset to 0 and
    stored in gw_chan_obs(k).
  nobs: Running count of records whose obs flag is positive; later copied into gw_chan_nobs.
  bed_elev: Bed elevation parsed from the second column of each record, then stored in gw_chan_elev(k).
  chan_length: Channel length parsed from the fourth column of each record, then stored in
    gw_chan_len(k).
  i_exist: Logical existence test for chan_depth.gw; controls whether the optional daily depth
    file is opened and processed.
uses:
  gwflow_module: gwflow_module owns the global channel-connection arrays and flags that this
    reader populates, sizes, and initializes; without that shared state the rest of gwflow
    would not know which cell-channel links exist or whether depth-zone and observation data
    are active.
  hydrograph_module: sp_ob%gwflow tells the routine how many gwflow objects/cells to expect,
    and that count becomes num_chancells, which drives array allocation and the record-reading
    loop.
  utils: split_line breaks each text record from chancell.gw into separate columns so the
    routine can read the numeric values with internal reads and detect whether the optional
    trailing columns are present.
---

<!-- facts:header -->

Reads groundwater-channel connection data from chancell.gw and, if present, channel-depth-zone schedules from chan_depth.gw. It fills the gwflow_module arrays and flags that later gwflow routines use to simulate channel exchange.

## Bottom Line

gwflow_chan_read is the gwflow setup reader for channel connections. It opens chancell.gw, reads one row per connected cell, parses the cell id, bed elevation, channel id, channel length, zone, and optional depth-zone / observation columns, then stores those values into the gwflow_module arrays.

It also counts observation links, sets the observation and depth-zone flags, and, when chan_depth.gw exists, allocates storage for daily channel-depth values by depth zone. hyd_connect calls this routine before the rest of gwflow connection setup so the model has the channel-cell mapping and optional depth inputs available during simulation.

## Arguments

<!-- facts:arguments -->

## Where It Fits

This routine runs during gwflow initialization, inside hyd_connect, after sp_ob%gwflow has established how many gwflow objects exist. Its results feed later gwflow setup and simulation routines, especially the channel exchange reader and the time-stepping logic that uses gw_chan_id, gw_chan_chan, gw_chan_len, gw_chan_zone, gw_chan_dpzn, gw_chan_obs, gw_chan_nobs, gw_chan_dep_flag, and gw_chan_ndpzn.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. Announce and open the channel-connection input. | Writes a progress message to the gwflow output unit, then opens chancell.gw on unit 1280 so the connection table can be read. |
| 2. Derive the number of channel-cell links and allocate storage. | Sets num_chancells from sp_ob%gwflow and allocates the gwflow_module arrays for ids, channels, lengths, elevations, zones, depth zones, and observation flags, initializing them to zero. |
| 3. Skip the chancell.gw header records. | Reads and ignores the meta line and column header line before starting the data loop, and clears the observation counter. |
| 4. Read each connection row as text and split it into fields. | Loops over each expected record, reads one full line into line_buf, and calls split_line to break the line into separate column strings and count them. |
| 5. Parse required columns and optional trailing columns. | Converts the first five fields into cell_id, bed_elev, channel, chan_length, and chan_zone, then conditionally reads dep_zone and obs when the line contains six or seven fields. |
| 6. Store the parsed record into shared gwflow arrays. | Copies the parsed values into the gwflow_module arrays for the current index and increments nobs whenever the observation flag is positive. |
| 7. Close chancell.gw and publish observation metadata. | Closes the connection file, stores the total observation count in gw_chan_nobs, and sets gw_chan_obs_flag when at least one observation cell exists. |
| 8. Detect and prepare the optional depth file. | Checks whether chan_depth.gw exists; if it does, sets the depth flag, opens the file, skips its two header lines, computes the maximum depth-zone index from gw_chan_dpzn, allocates gw_chan_dep, and leaves the daily depth rows for gwflow_simulate to read later. |

## Modules Used

<!-- facts:uses -->

| Module | State touched | Key components |
| --- | --- | --- |
| [sym:gwflow_module] | `gw_chan_id, gw_chan_chan, gw_chan_len, gw_chan_elev, gw_chan_zone, gw_chan_dpzn, gw_chan_obs, num_chancells, gw_chan_dep_flag, gw_chan_ndpzn` |  |
| [sym:hydrograph_module] | `sp_ob` | `sp_ob%gwflow` |
| [sym:utils] | `split_line` | `split_line` |

## Local Variables

<!-- facts:locals -->

## State Changes

| Target | When | Meaning |
| --- | --- | --- |
| `num_chancells` | During the setup step after sp_ob%gwflow is available. | num_chancells is set to the gwflow object count so the routine knows how many channel-cell records to allocate for and read from chancell.gw. |
| `gw_chan_len` | After all chancell.gw records have been parsed and gw_chan_ndpzn is known, if chan_depth.gw exists. | gw_chan_len is allocated to num_chancells and initialized to zero, then filled record-by-record with the channel length for each cell-channel connection. |
| `gw_chan_id(k)` | For every record read from chancell.gw inside the k loop. | gw_chan_id(k) receives the cell identifier parsed from the first column of the current connection record. |
| `gw_chan_elev(k)` | For every record read from chancell.gw inside the k loop. | gw_chan_elev(k) receives the bed elevation parsed from the second column of the current connection record. |
| `gw_chan_chan(k)` | For every record read from chancell.gw inside the k loop. | gw_chan_chan(k) receives the channel identifier parsed from the third column of the current connection record. |
| `gw_chan_len(k)` | For every record read from chancell.gw inside the k loop. | gw_chan_len(k) receives the channel length parsed from the fourth column of the current connection record. |
| `gw_chan_zone(k)` | For every record read from chancell.gw inside the k loop. | gw_chan_zone(k) receives the channel zone parsed from the fifth column of the current connection record. |
| `gw_chan_dpzn(k)` | If the current line has at least six fields. | gw_chan_dpzn(k) receives the optional depth-zone identifier; otherwise it remains zero for that connection. |
| `gw_chan_obs(k)` | If the current line has at least seven fields. | gw_chan_obs(k) receives the optional observation flag; otherwise it remains zero for that connection. |
| `gw_chan_nobs` | Whenever a record has obs > 0, and after the loop ends. | gw_chan_nobs is set to the number of channel-cell connections flagged for observation output. |
| `gw_chan_dep_flag` | If chan_depth.gw exists. | gw_chan_dep_flag is turned on to indicate that daily channel-depth input will be available for the simulation phase. |
| `gw_chan_ndpzn` | If chan_depth.gw exists, after gw_chan_dpzn has been populated. | gw_chan_ndpzn is set to the maximum depth-zone index found in the channel-cell table, which determines the size of gw_chan_dep. |

## File I/O

<!-- facts:io -->


## Lineage

`gwflow_chan_read.f90` was introduced in `df07e3f` (2024-03-05, "init all") and has been changed in 8 non-merge commit(s) since, most recently `3cc92b5` (2026-06-02, "gwflow input rework"). Lineage is reconstructed from commit metadata (SHA, date, subject); per-line diffs were unavailable in this build environment, so only the commits touching `gwflow_chan_read.f90` are listed.

- `3cc92b5` (2026-06-02) — gwflow input rework
- `1567fba` (2026-03-31) — gwflow re-merge: input system - gwflow_read, output init extraction, NAM/USGS/stats removal
- `2ee1889` (2025-11-17) — Cleanup of sine warnings.
- `568154c` (2024-10-08) — Increase length of various character variables
- `39fabde` (2024-08-08) — Initialized varables with python script, corrected input data where integers where floats in two input files, trapped underflow errors in th…
- `df07e3f` (2024-03-05) — init all

## Review Notes

- Direct file I/O exists; verify file meanings and units before finalizing.
- warning: missing_doc: Procedure 'gwflow_chan_read' has no extracted documentation comment.
- Lineage was reconstructed from file-level commit metadata; per-line diffs were unavailable in this environment (blobless clone), so line-span filtering was not applied.
