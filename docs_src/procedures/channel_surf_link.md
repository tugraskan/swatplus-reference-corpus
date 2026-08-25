---
kind: procedure
symbol: channel_surf_link
title: channel_surf_link
status: filled
source_hash: fd04665e4031629b
version_label: SWAT+ 62.0.0
locals:
  iobtyp: Temporary 3-character object-type code read from `ch_sur(ics)%obtyp(ii)` so the
    routine can branch on whether the linked object is an HRU, HRU-like landscape unit, routing
    unit, channel, or SWAT-deg channel.
  ics: Loop index over channel-surface linkage records; each `ics` selects one entry in `ch_sur`.
  ii: Loop index over the linked objects within one channel-surface record.
  i: A general object index reused in the `hlt` branch as the owning `ob` entry for that linkage;
    it is initialized to zero before looping.
  iob: Resolved object index for the currently linked target object in `ob`; used to write
    flood-link back-references and to fetch area.
  ihru: Counter used to identify the HRU or iterate routing-unit members, depending on branch;
    in the `ru` branch it steps through each member of `ru_def(iru)%num`.
  ichan: Channel number copied from `ch_sur(ics)%chnum`; written into `flood_ch_lnk` as the
    back-reference to the channel.
  tot_ha: Accumulator for the total linked floodplain area across all handled objects in the
    current pass.
  iobtypno: Temporary object-type number read from `ch_sur(ics)%obtypno(ii)`; used to identify
    the specific linked object or routing unit.
uses:
  hydrograph_module: This module supplies the channel-surface linkage tables and object-connectivity
    arrays that the routine reads and updates. `ch_sur` drives the outer loops, `ob` stores
    the resolved object numbers plus `flood_ch_lnk` and `flood_ch_elem`, `sp_ob1` provides
    the first sequential IDs for HRU and HRU-like objects, and `ru_def` provides the member
    list needed to expand a routing unit into its component objects.
  channel_module: This module defines the shared object-connectivity and spatial-object state
    that `channel_surf_link` assigns. The routine needs `ob` to store object IDs, flood pointers,
    and areas, and it needs `sp_ob1` to convert a type-relative object number into the model-wide
    sequential number for HRU and HRU-like targets.
  ru_module: The routing-unit branch uses `iru` to select a routing unit and `ru` is the module
    that owns that routing-unit namespace. Even though this routine only writes `iru` and
    does not dereference `ru` in the visible source, the module is relevant because `iru`
    is a shared routing-unit identifier and the routine’s routing-unit handling depends on
    the routing-unit data model defined there.
  maximum_data_module: The routine uses `db_mx%ch_surf` to determine how many channel-surface
    linkage records exist. That maximum count bounds the outer loop so the routine processes
    every configured channel-surface element without reading past the allocated `ch_sur` array.
  hru_module: The routine marks floodplain wetness by setting `wet_fp` on impacted HRUs. That
    state lives in `hru`, so this module matters because it provides the HRU objects whose
    wet-floodplain flag is switched on when a linked HRU or routing-unit member is flooded.
---

<!-- facts:header -->

Links channel-surface overbank elements to the HRUs, HRU-like landscape units, or routing units they flood. It also marks flooded HRUs and stores back-references from those objects to the channel-surface element.

## Bottom Line

This subroutine walks every channel-surface linkage in `ch_sur` and resolves each linked object into a concrete model object number. For each linkage it records the downstream object mapping in `ob(... )%obj_out`, then writes back-pointers such as `flood_ch_lnk` and `flood_ch_elem` so the flooded object knows which channel and landscape element it belongs to.

It also flips the flooded HRU flag (`wet_fp`) for affected HRUs and accumulates the linked area in `tot_ha`. The routine is part of the overbank-flooding setup: later flow and flood-fraction logic depend on these linkages and on the wet-floodplain state it sets here.

## Arguments

<!-- facts:arguments -->

## Where It Fits

This routine runs after channel-surface linkage data have been populated into `ch_sur` and the object-connectivity tables in `ob` have been allocated. It translates each linkage into actual model object numbers, sets the flood-channel back-pointers, and flags flooded HRUs before later overbank/flood-fraction behavior uses those links and the `wet_fp` state.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. initialize totals | Reset the floodplain area accumulator and the reused object index before processing any channel-surface records. |
| 2. iterate channel-surface records | Loop over every channel-surface linkage record up to `db_mx%ch_surf`, then loop over each linked object in that record. |
| 3. read linkage metadata | Copy the channel number, object type code, and object type number from `ch_sur(ics)` into local variables for branch selection. |
| 4. handle HRU links | For `case ("hru")`, compute the absolute HRU object number, store it in `ob(ics)%obj_out(ii)`, set the linked object's flood-channel pointers, mark the HRU as wet floodplain, and add its area to `tot_ha`. |
| 5. handle HRU-like landscape links | For `case ("hlt")`, compute the absolute HRU-like object number, store it in `ob(i)%obj_out(ii)`, write the flood-channel pointers, and add the object area to `tot_ha`. |
| 6. expand routing-unit links | For `case ("ru")`, read the routing-unit number, loop through every member object listed in `ru_def(iru)%num`, set each member’s flood-channel pointers, add each member area to `tot_ha`, and mark the member HRU as wet floodplain. |
| 7. ignore unsupported types | Treat channel and SWAT-deg channel cases as no-ops in the visible source, leaving them available for future handling or upstream data definitions. |
| 8. finish linkage pass | After all records are processed, exit the loops and return to the caller with the updated connectivity and wet-floodplain flags in place. |

## Modules Used

<!-- facts:uses -->

| Module | State touched | Key components |
| --- | --- | --- |
| [sym:hydrograph_module] | `ch_sur, ob, sp_ob1, ru_def` | `ch_sur(ics)%num, ch_sur(ics)%chnum, ch_sur(ics)%obtyp(ii), ch_sur(ics)%obtypno(ii), ob(ics)%obj_out(ii), sp_ob1%hru, ob(ics)%obtypno_out(ii), ob(iob)%flood_ch_lnk, ob(iob)%flood_ch_elem, ob(iob)%area_ha, ob(i)%obj_out(ii), sp_ob1%hru_lte, ob(i)%obtypno_out(ii), ru_def(iru)%num_tot, ru_def(iru)%num(ihru)` |
| [sym:channel_module] | `ob, sp_ob1` | `ob(ics)%obj_out(ii), ob(ics)%obtypno_out(ii), ob(iob)%flood_ch_lnk, ob(iob)%flood_ch_elem, ob(iob)%area_ha, ob(i)%obj_out(ii), ob(i)%obtypno_out(ii), sp_ob1%hru, sp_ob1%hru_lte` |
| [sym:ru_module] | `ru, iru` |  |
| [sym:maximum_data_module] | `db_mx` | `db_mx%ch_surf` |
| [sym:hru_module] | `hru` | `hru(ihru)%wet_fp, hru(iob)%wet_fp` |

## Local Variables

<!-- facts:locals -->

## State Changes

| Target | When | Meaning |
| --- | --- | --- |
| `ob(ics)%obj_out(ii)` | When `iobtyp` is `"hru"`. | Stores the resolved HRU object number for this channel-surface link in `ob(ics)%obj_out(ii)` so later code can route to the actual HRU object. |
| `ob(iob)%flood_ch_lnk` | When `iobtyp` is `"hru"` or `"ru"`. | Records which channel the linked object is flooded from by writing `ichan` into the object's `flood_ch_lnk` back-pointer. |
| `ob(iob)%flood_ch_elem` | When `iobtyp` is `"hru"`, `"hlt"`, or `"ru"`. | Records the channel-surface element or link index that identifies where the object is flooded from, using `ics` for HRU and routing-unit members and `ii` for the HRU-like landscape unit branch. |
| `hru(ihru)%wet_fp` | When `iobtyp` is `"hru"` or `"ru"`. | Marks the affected HRU as wet floodplain by setting `wet_fp` to `"y"`. |
| `ob(i)%obj_out(ii)` | When `iobtyp` is `"hlt"`. | Stores the resolved HRU-like landscape object number in `ob(i)%obj_out(ii)` for the current link. |
| `iru` | When `iobtyp` is `"ru"`. | Sets `iru` to the routing-unit number read from the channel-surface linkage so the routine can expand that routing unit into its member objects. |
| `hru(iob)%wet_fp` | When `iobtyp` is `"ru"` and the loop visits each routed member object. | Marks each routed member HRU as wet floodplain by setting `hru(iob)%wet_fp` to `"y"`. |

## File I/O

<!-- facts:io -->


## Lineage

Three resolved commits changed `channel_surf_link`. The initial addition in `df07e3f` created the routine and its overbank-link handling. `39fabde` only initialized the local variables in the declarations. `fd90e36` added an explicit `i = 0` assignment before the loops.

- df07e3f introduced the subroutine and its channel-surface linkage behavior for HRU, HRU-like landscape, and routing-unit cases.
- 39fabde changed only local variable initialization in the declarations; it did not alter the linkage algorithm.
- fd90e36 added `i = 0` before processing, matching the initialized-variable cleanup and not changing the modeled flood linkage logic.

## Review Notes

- No direct file I/O was extracted for this procedure.
- warning: missing_doc: Procedure 'channel_surf_link' has no extracted documentation comment.
- algorithm_steps revised: condensed the visible source into 8 steps and cited only line ranges present in the source block.
- Source is a subroutine with no arguments; all behavior depends on module state from `hydrograph_module`, `channel_module`, `ru_module`, `maximum_data_module`, and `hru_module`.
- In the `ru` branch, the source assigns `hru(iob)%wet_fp` even though `iob` is loaded from `ru_def(iru)%num(ihru)`; this follows the visible code and is documented as written.
