---
kind: procedure
symbol: sd_channel_surf_link
title: sd_channel_surf_link
status: filled
source_hash: 58a77860f747e58b
version_label: SWAT+ 62.0.0
locals:
  ics: '`ics` is the outer loop counter over SWAT-deg channel objects in `sp_ob%chandeg`;
    each pass works on one channel segment''s floodplain linkage data.'
  iobtyp: '`iobtyp` holds the current floodplain object type code read from `sd_ch(ics)%fp%obtyp(ii)`,
    so the routine can branch between a direct HRU link and a routing-unit expansion.'
  ii: '`ii` is the index over the floodplain object list for the current channel segment,
    used in both the counting pass and the population pass.'
  iihru: '`iihru` is the inner counter used only when expanding a routing unit; it steps through
    `ru_def(iru)%num(iihru)` to enumerate each HRU in that routing unit.'
  ihru_tot: '`ihru_tot` is the running total of HRUs assigned to the current floodplain. It
    is first used to size the arrays, then reset and reused as the insertion index while filling
    them.'
uses:
  hydrograph_module: The hydrograph module provides the global counts and routing-unit membership
    lists that define how many floodplain objects exist and which HRUs belong to each routing
    unit. `sp_ob%chandeg` controls the channel loop, and `ru_def(iru)%num_tot` / `ru_def(iru)%num(iihru)`
    expand an RU object into its constituent HRUs.
  sd_channel_module: The sd-channel module stores the floodplain state this routine initializes.
    `sd_ch(ics)%fp%obj_tot`, `obtyp`, and `obtypno` describe the mixed list of floodplain
    objects to process, while `hru`, `hru_fr`, `ha`, and `hru_tot` are the arrays and summary
    values that this routine allocates and fills for later floodplain routing.
  ru_module: The ru module supplies the shared routing-unit index variable `iru`, which this
    routine assigns when it encounters an RU floodplain object. That index is needed to look
    up the RU's HRU list in `ru_def` and to keep the current RU selection consistent across
    the expansion loop.
  hru_module: The hru module provides the HRU attributes that determine floodplain area accounting
    and wet-floodplain flags. `hru(ihru)%area_ha` is added into the channel floodplain area
    sum, and `hru(ihru)%wet_fp` is set to mark every linked HRU as part of a floodplain connection.
  topography_data_module: The module is imported by this routine, but the extracted source
    does not show any referenced symbols from it. It may be present for shared model context
    or future compatibility, but no traced behavior in this subroutine depends on it in the
    available evidence.
---

<!-- facts:header -->

Builds the floodplain HRU link lists for every SWAT-deg channel object. It counts linked HRUs, allocates storage, records the HRU sequence, and marks contributing HRUs as floodplain-wet.

## Bottom Line

`sd_channel_surf_link` walks each SWAT-deg channel segment and converts the floodplain object list into explicit HRU membership. It first counts how many HRUs will be linked, allocates `sd_ch(ics)%fp%hru` and `hru_fr`, then fills those arrays while summing floodplain area and setting `hru(ihru)%wet_fp = "y"` for every contributing HRU.

The routine matters because later floodplain/overbank behavior depends on the channel-level HRU list, the total floodplain area, and the HRU area fractions it computes. It is a linkage initializer: `proc_cha` calls it after `overbank_read` so the channel floodplain parameters are ready before later routing and time-concentration setup.

## Arguments

<!-- facts:arguments -->

## Where It Fits

This routine runs during channel setup in `proc_cha`, immediately after `overbank_read` has populated the floodplain object metadata. Its output is consumed by later channel routing behavior that needs the floodplain HRU membership, total floodplain area, and per-HRU area fractions to handle overbank exchange and related calculations.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. Initialize loop variables and scan each SWAT-deg channel segment. | The routine starts with zeroed local counters and loops over every channel segment counted in `sp_ob%chandeg`. |
| 2. Skip channel segments that have no floodplain objects. | For each segment, it only processes floodplain linkage data when `sd_ch(ics)%fp%obj_tot > 0`; otherwise it leaves the segment unchanged. |
| 3. Count the total number of HRUs that will be linked to the floodplain. | The routine scans the object list, counting one HRU for each direct `hru` object and expanding each `ru` object by `ru_def(iru)%num_tot` HRUs. |
| 4. Allocate the floodplain HRU arrays. | Using the counted total, it allocates `sd_ch(ics)%fp%hru` and `sd_ch(ics)%fp%hru_fr` so the floodplain can store the HRU sequence and each HRU's area fraction. |
| 5. Reset the floodplain accumulators before filling the lists. | It clears the insertion counter and initializes the floodplain area sum `sd_ch(ics)%fp%ha` to zero. |
| 6. Fill direct HRU links and mark them as floodplain wet. | For each `hru` object, it stores the HRU number, adds that HRU area to the floodplain total, and sets `hru(ihru)%wet_fp = "y"`. |
| 7. Expand routing-unit floodplain objects into their member HRUs. | For each `ru` object, it loops through `ru_def(iru)%num_tot`, adds every member HRU to the floodplain list, accumulates their areas, and marks each one as floodplain wet. |
| 8. Finalize the floodplain HRU count and compute area fractions. | After the list is filled, it stores the final HRU count in `sd_ch(ics)%fp%hru_tot` and computes each `hru_fr` as the HRU area divided by total floodplain area. |
| 9. Continue to the next segment and return. | It closes the segment loop, then returns to the caller once all channel floodplain linkages have been prepared. |

## Modules Used

<!-- facts:uses -->

| Module | State touched | Key components |
| --- | --- | --- |
| [sym:hydrograph_module] | `sp_ob, ru_def` | `sp_ob%chandeg, ru_def(iru)%num_tot, ru_def(iru)%num(iihru)` |
| [sym:sd_channel_module] | `sd_ch` | `sd_ch(ics)%fp%obj_tot, sd_ch(ics)%fp%obtyp(ii), sd_ch(ics)%fp%obtypno(ii), sd_ch(ics)%fp%hru(ihru_tot), sd_ch(ics)%fp%hru_fr(ihru_tot), sd_ch(ics)%fp%ha, sd_ch(ics)%fp%hru_tot, sd_ch(ics)%fp%hru(ihru), sd_ch(ics)%fp%hru_fr(ihru)` |
| [sym:ru_module] | `ru, iru` |  |
| [sym:hru_module] | `hru, ihru` | `hru(ihru)%area_ha, hru(ihru)%wet_fp, hru(iihru)%area_ha` |
| [sym:topography_data_module] | `no resolved imported state or types were identified from `topography_data_module` in the extracted source` |  |

## Local Variables

<!-- facts:locals -->

## State Changes

| Target | When | Meaning |
| --- | --- | --- |
| `iru` | When the floodplain object type for a channel entry is `"ru"` in the second pass through `sd_ch(ics)%fp%obtyp(ii)`. | `iru` is set to the referenced routing-unit number so the routine can read `ru_def(iru)` and expand that routing unit into its component HRUs. |
| `sd_ch(ics)%fp%ha` | When the routine finishes scanning all floodplain objects for a channel segment. | `sd_ch(ics)%fp%ha` accumulates the total floodplain area across every linked HRU in that channel segment, which is needed later to normalize the individual HRU fractions. |
| `ihru` | Each time the routine processes a new direct HRU entry or advances through the member list of a routing-unit entry. | `ihru` becomes the current HRU number being linked into the floodplain arrays. |
| `sd_ch(ics)%fp%hru(ihru_tot)` | Each time the routine writes a new HRU into the floodplain list, either from a direct `hru` object or from `ru_def(iru)%num(iihru)`. | `sd_ch(ics)%fp%hru(ihru_tot)` stores the ordered HRU number associated with that floodplain position. |
| `hru(ihru)%wet_fp` | Whenever an HRU is added to the floodplain list in either the direct HRU case or the routing-unit expansion case. | `hru(ihru)%wet_fp` is set to `"y"` to mark that HRU as part of a floodplain linkage for subsequent model behavior. |
| `sd_ch(ics)%fp%hru_tot` | After the floodplain object list has been fully expanded into HRUs for the current channel segment. | `sd_ch(ics)%fp%hru_tot` stores the final number of HRUs linked to that floodplain, which controls the later fraction loop. |
| `sd_ch(ics)%fp%hru_fr(ihru)` | During the final pass after `sd_ch(ics)%fp%hru_tot` has been set. | `sd_ch(ics)%fp%hru_fr(ihru)` is computed as each linked HRU's area share of the total floodplain area. |

## File I/O

<!-- facts:io -->


## Lineage

Four resolved commits changed `sd_channel_surf_link`. The initial addition in df07e3f created the routine with the channel/floodplain loop logic, direct HRU and routing-unit expansion, area summation, wet-floodplain flags, and fraction calculation. In 94b6dec, the file was brought in from Bitbucket with the same operational logic and the `use` statements shown in the current source. f8bb6ec changed the `allocate (sd_ch(ics)%fp%hru(ihru_tot))` statement to use `source = 0`, and 39fabde initialized the local counters (`ics`, `iobtyp`, `ii`, `iihru`, `ihru_tot`) and changed `allocate (sd_ch(ics)%fp%hru_fr(ihru_tot))` to `source = 0.`.

- df07e3f introduced the entire floodplain-link construction algorithm: count objects, expand routing units into HRUs, allocate storage, accumulate floodplain area, set `wet_fp`, and compute HRU fractions.
- 94b6dec imported the same procedure into the repository with the current module dependencies and baseline logic for channel floodplain linkage setup.
- f8bb6ec made the HRU index array allocation explicit with `source = 0`, ensuring a zero-initialized integer array for floodplain HRU storage.
- 39fabde added explicit initial values for the local counters and zero-initialized `hru_fr`, which reduced uninitialized-state risk in the floodplain linkage build.

## Review Notes

- No direct file I/O was extracted for this procedure.
- warning: missing_doc: Procedure 'sd_channel_surf_link' has no extracted documentation comment.
- algorithm_steps revised: compressed the original 8 draft blocks into 9 source-faithful steps aligned to the visible control flow and line numbers.
