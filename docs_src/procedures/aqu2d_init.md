---
kind: procedure
symbol: aqu2d_init
title: aqu2d_init
status: filled
source_hash: 16537e4665b3982a
version_label: SWAT+ 62.0.0
locals:
  iaq: Aquifer loop index. It selects the current aquifer object being initialized and scopes
    the linked-channel work for that aquifer.
  mfe: Head pointer for the linked list of channels sorted by drainage area. It marks the
    smallest-area channel currently at the front of the order.
  next1: Walker pointer used while inserting or traversing the sorted channel list. It holds
    the next candidate channel index during the drainage-area ordering pass.
  iprv: Previous pointer in the linked-list insertion walk. It tracks the prior channel index
    so the routine can splice a newly ordered channel into the list.
  ipts: Insertion-pass counter. It counts how many channels have been inspected while placing
    the current channel into the drainage-area order.
  npts: Number of previously placed channels to scan for the current insertion. It is set
    to `icha - 1` before the inner search loop.
  icha: Sequential channel index within the current aquifer. It is used to iterate through
    the aquifer’s channel list and populate the sorted results.
  ichd: Index into `sd_chd` for the channel property record associated with the current channel
    object.
  iob: Object index into `ob` for the current channel’s spatial object record.
  sum_len: Running sum of channel lengths within the aquifer, then reused as the remaining-length
    accumulator while channels are processed in sorted order.
  next: Temporary linked-list array storing the next channel index in drainage-area order
    for each channel in the aquifer.
uses:
  hydrograph_module: The geomorphic baseflow setup depends on `hydrograph_module` because
    it provides the aquifer count, the aquifer-to-channel mapping arrays, the channel object
    records, and the shared `ich` index. `sp_ob%aqu` controls the outer aquifer loop, `aq_ch(iaq)%num_tot`
    and `aq_ch(iaq)%num(icha)` provide the channel membership to sort, `sp_ob1%chandeg`, `ob(iob)%props`,
    and `sd_chd(ichd)%chl` supply the channel geometry, `aqu_cha` holds the sortable channel
    summaries, and `sd_ch(ich)%aqu_link` / `sd_ch(ich)%aqu_link_ch` receive the back-references
    used later by routing code.
  sd_channel_module: The `sd_channel_module` matters because this routine writes the aquifer
    linkage metadata onto each SWAT-deg channel record and reads the channel length from the
    hyd-sed data table. `sd_ch(ich)%aqu_link` and `sd_ch(ich)%aqu_link_ch` become the identifying
    links from a channel back to its aquifer and position in that aquifer, while `sd_chd(ichd)%chl`
    is the channel length used to build aquifer totals and remaining-length calculations.
  maximum_data_module: The `maximum_data_module` provides `db_mx%aqu2d`, which gates whether
    this initialization should run at all. When `aqu2d` is not enabled, the routine returns
    immediately and skips all aquifer-channel and constituent hydrograph allocation.
  constituent_mass_module: The `constituent_mass_module` matters because this routine conditionally
    allocates groundwater-loading hydrographs for salt ions and other constituents. `cs_db%num_tot`
    decides whether any constituent hydrograph state is needed, and `cs_db%num_salts` / `cs_db%num_cs`
    determine whether the `aq_chcs(iaq)%hd(1)%salt` and `aq_chcs(iaq)%hd(1)%cs` arrays must
    be allocated and zeroed.
---

<!-- facts:header -->

Initializes aquifer-to-channel linkage data for the geomorphic baseflow routing setup. It also allocates zeroed groundwater-loading hydrographs when salts or other constituents are being simulated.

## Bottom Line

This routine runs once during channel setup to organize each aquifer’s linked channels by drainage area, store the aquifer/channel cross-reference back onto `sd_ch`, and compute each linked channel’s area, length, total linked length, and remaining length as channels become noncontributing.

If constituent transport is active, it also allocates `aq_chcs` and its `hd(1)` hydrograph so later groundwater-loading calculations have zero-initialized salt and constituent mass arrays to write into.

## Arguments

<!-- facts:arguments -->

## Where It Fits

This routine runs during channel/aquifer initialization after `proc_cha` has read channel, SWAT-deg channel, and hyd-sed input data. Its results are then used by later channel routing and geomorphic baseflow behavior, because the model needs the aquifer-to-channel linkage, sorted drainage-area order, channel-length totals, and optional constituent hydrograph storage before flux calculations begin.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. Exit immediately when geomorphic 2D aquifer handling is disabled. | Checks `db_mx%aqu2d` and returns without allocating or linking anything if the feature is off. |
| 2. Loop over each aquifer object that has linked channels. | For each aquifer, allocates per-aquifer channel storage, a temporary sortable geometry array, and the linked-list helper array, then resets the total-length accumulator. |
| 3. Capture each linked channel’s identity and geometry. | Traverses the aquifer’s channel list, stores the channel’s aquifer linkage back into `sd_ch`, looks up the channel object and hyd-sed record, saves drainage area and length into `aqu_cha`, and accumulates total linked length. |
| 4. Build a drainage-area-sorted linked list of channels. | Inserts each channel into a list ordered by increasing drainage area by walking the partially built list, updating `mfe`, `next`, and `iprv` as needed. |
| 5. Copy the sorted geometry into `aq_ch`. | Uses the linked-list head pointer to write channels into `aq_ch(iaq)%ch` in sorted order by drainage area. |
| 6. Store the aquifer’s total linked channel length. | Saves the accumulated channel length into `aq_ch(iaq)%len_tot` for later baseflow distribution calculations. |
| 7. Compute how much channel length remains after each channel dries up. | Walks the sorted channel list, subtracting each channel length from the running total and storing the remainder in `len_left`. |
| 8. Release the temporary per-aquifer working arrays. | Deallocates the temporary geometry and linked-list arrays before moving to the next aquifer. |
| 9. Allocate groundwater-loading hydrographs only when constituents exist. | If any constituent tracking is active, allocates one `aq_chcs` entry per aquifer and one hydrograph container at `hd(1)` for each aquifer. |
| 10. Allocate and zero salt and constituent arrays as needed. | Creates zero-initialized salt and/or constituent mass arrays inside `aq_chcs(iaq)%hd(1)` when the corresponding database counts are positive. |
| 11. Return to the caller. | Ends the initialization after all aquifer linkage and optional constituent storage has been prepared. |

## Modules Used

<!-- facts:uses -->

| Module | State touched | Key components |
| --- | --- | --- |
| [sym:hydrograph_module] | `sp_ob, aq_ch, sp_ob1, ob, aqu_cha, hd, ich` | `sp_ob%aqu, aq_ch(iaq)%num_tot, aq_ch(iaq)%num(icha), sp_ob1%chandeg, ob(iob)%props, aqu_cha(icha)%area, ob(iob)%area_ha, aqu_cha(icha)%len, aqu_cha(next1)%area, aq_ch(iaq)%ch(icha), aq_ch(iaq)%len_tot, aq_ch(iaq)%ch(icha)%len, aq_ch(iaq)%ch(icha)%len_left` |
| [sym:sd_channel_module] | `sd_ch, sd_chd` | `sd_ch(ich)%aqu_link, sd_ch(ich)%aqu_link_ch, sd_chd(ichd)%chl` |
| [sym:maximum_data_module] | `db_mx` | `db_mx%aqu2d` |
| [sym:constituent_mass_module] | `cs_db, aq_chcs` | `cs_db%num_tot, aq_chcs(iaq)%hd(1), cs_db%num_salts, aq_chcs(iaq)%hd(1)%salt, cs_db%num_cs, aq_chcs(iaq)%hd(1)%cs` |

## Local Variables

<!-- facts:locals -->

## State Changes

| Target | When | Meaning |
| --- | --- | --- |
| `ich` | During the aquifer-channel loop, for each channel in `aq_ch(iaq)%num(icha)`. | `ich` is set to the current channel object number so the routine can index the global SWAT-deg channel arrays and write back aquifer linkage metadata for that specific channel. |
| `sd_ch(ich)%aqu_link` | When a channel is being initialized inside the aquifer loop. | `sd_ch(ich)%aqu_link` is set to the current aquifer index so later routines know which aquifer supplies that channel’s geomorphic baseflow. |
| `sd_ch(ich)%aqu_link_ch` | When a channel is being initialized inside the aquifer loop. | `sd_ch(ich)%aqu_link_ch` is set to the channel’s sequential position within its aquifer, giving later code the local ordering needed to access `aq_ch(iaq)` consistently. |
| `aqu_cha(icha)%area` | For every linked channel after the object record is looked up. | `aqu_cha(icha)%area` is filled with the channel object’s drainage area so the channels can be sorted by area for the linked-list ordering. |
| `aqu_cha(icha)%len` | For every linked channel after the hyd-sed record is looked up. | `aqu_cha(icha)%len` stores the physical channel length, which is later used to compute total linked length and the remaining length after drying. |
| `aq_ch(iaq)%ch(icha)` | After the sorted order is built and copied back into `aq_ch(iaq)%ch`. | `aq_ch(iaq)%ch(icha)` becomes the sorted per-channel geometry record for the aquifer, preserving the area and length values in drainage-area order. |
| `aq_ch(iaq)%len_tot` | After all channels in the aquifer have been measured. | `aq_ch(iaq)%len_tot` stores the total linked channel length in the aquifer and is later used to distribute geomorphic baseflow across the sorted channel set. |
| `aq_ch(iaq)%ch(icha)%len_left` | While walking the sorted channel list to compute cumulative remaining length. | `aq_ch(iaq)%ch(icha)%len_left` records how much total channel length remains after the current channel is taken out of service, supporting dry-up sequencing in later baseflow logic. |
| `aq_chcs(iaq)%hd(1)%salt` | When constituent transport is enabled and `cs_db%num_salts > 0`. | `aq_chcs(iaq)%hd(1)%salt` is allocated and zeroed so later groundwater-loading routines have a salt mass array to populate for this aquifer. |
| `aq_chcs(iaq)%hd(1)%cs` | When constituent transport is enabled and `cs_db%num_cs > 0`. | `aq_chcs(iaq)%hd(1)%cs` is allocated and zeroed so later groundwater-loading routines have a constituent mass array to populate for this aquifer. |

## File I/O

<!-- facts:io -->


## Lineage

Resolved lineage shows four behavior changes. The file was added in df07e3f with the full aquifer-channel sorting and optional constituent-hydrograph initialization logic. f8bb6ec changed the salt and constituent allocations to use `source = 0.` so the arrays are zero-initialized on allocation. 39fabde extended that zero-initialization pattern to `iaq`, `mfe`, `next1`, `iprv`, `ipts`, `npts`, `icha`, `ichd`, `iob`, `sum_len`, `next`, and the `aq_chcs`/`hd` allocations. 2ee1889 only removed extra blank lines and did not change behavior.

- df07e3f introduced `aqu2d_init` and its core work: gating on `db_mx%aqu2d`, sorting aquifer-linked channels by drainage area, storing linkage metadata in `sd_ch`, computing `len_tot` and `len_left`, and allocating optional constituent hydrographs.
- f8bb6ec made `aq_chcs(iaq)%hd(1)%salt` and `aq_chcs(iaq)%hd(1)%cs` zero-initialized at allocation time, removing reliance on a separate assignment for safe initialization.
- 39fabde initialized local counters and the `next` array at declaration/allocation time and added `source = 0.` to the `aq_chcs` and `hd` allocations, keeping the same behavior but making the initialization explicit.

## Review Notes

- No direct file I/O was extracted for this procedure.
- warning: missing_doc: Procedure 'aqu2d_init' has no extracted documentation comment.
