---
kind: procedure
symbol: recall_salt
title: recall_salt
status: filled
source_hash: 0591bd3591ac22eb
version_label: SWAT+ 62.0.0
args:
  irec: '`irec` selects which recall-salt entry in `rec_salt` and `recall` to process. Its
    value determines the source type, date limits, and the salt hydrograph data used for the
    current step.'
locals:
  isalt: Loop counter over salt ions, from 1 to `cs_db%num_salts`, so the routine can update
    each salt constituent separately.
  ichan: Holds the channel object number taken from `ob(icmd)%obtypno_out(1)` when the recall
    flow is a diversion; that channel is the source of removed salt mass.
  salt_conc: Temporary concentration of a salt ion in the source channel water, computed from
    channel salt mass and channel storage before diversion mass is calculated.
  div_mass: Temporary salt mass change for a diversion flow. It is computed from concentration
    and diverted flow, then capped so the routine does not remove more salt than the channel
    contains.
uses:
  basin_module: '`basin_module` is needed because this routine writes the recalled salt boundary
    conditions into the basin-wide object state. Those updates become part of the object hydrograph
    that the rest of the basin simulation uses for constituent routing.'
  hydrograph_module: '`hydrograph_module` provides the current simulation object connectivity,
    recall hydrograph timing window, and channel storage/flow used to decide whether the recall
    is active and, for diversions, which channel loses water and salt. Without these fields
    the routine could not select the source channel or apply the date logic.'
  time_module: '`time_module` supplies the current calendar year, simulation year index, day,
    and month that pick the correct recall record for daily, monthly, annual, and average-annual
    salt inputs. The routine is entirely time-driven, so these values control whether and
    how each salt entry is applied.'
  constituent_mass_module: '`constituent_mass_module` holds the salt-count database, the recall-salt
    input records, the channel-water salt masses, the boundary hydrograph slots, and the per-source
    salt balance arrays. This is the core data model that the routine reads from and writes
    to when adding or removing salt mass.'
  ch_salt_module: '`ch_salt_module` matters because it stores the per-channel diversion salt
    balance. The routine writes `chsalt_d(ichan)%salt(isalt)%div` so later channel salt accounting
    can report how much salt was removed by the diversion.'
  gwflow_module: '`gwflow_module` matters because it contributes `div_conc_salt`, the diversion
    salt concentration array. The routine resets and fills that array so groundwater/flow-related
    salt transport logic can use the diversion concentration later in the simulation.'
---

<!-- facts:header -->

Updates salt-recall point sources for the current simulation time step. It either injects salt mass into an object hydrograph or removes salt from a source channel during diversion cases.

## Bottom Line

`recall_salt` applies salt loading from recall point sources after the main recall hydrograph has been set up. For each simulated salt ion, it checks the recall type and active date window, then either copies salt concentrations/masses into the object boundary hydrograph or subtracts salt from the source channel when the recall flow is a diversion.

The routine also records balance outputs for later reporting: inside-watershed sources go to `recsaltb_d`, outside-watershed sources go to `recoutsaltb_d`, channel diversion salt removal is written to `chsalt_d`, and diversion concentration is stored in `div_conc_salt`. These results matter because downstream salt accounting and channel state updates depend on them.

## Arguments

<!-- facts:arguments -->

## Where It Fits

`command` calls this routine after it has built the current recall-object hydrograph and initialized the constituent boundary object (`obcs(icmd)%hd(1)`) for a recall event. `recall_salt` then overwrites the salt portion of that boundary state for the active time step, and later salt routing and balance reporting depend on those updated values.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. Initialize the salt boundary outputs for this recall event. | Clear `obcs(icmd)%hd(1)%salt` and reset every `div_conc_salt(isalt,irec)` entry to zero before processing the current time step. |
| 2. Skip all work when no salts are being simulated. | Only enter the recall logic if `cs_db%num_salts > 0`, using the salt-count database to guard the rest of the routine. |
| 3. Branch by recall-salt input type. | Use `rec_salt(irec)%typ` to choose the daily, monthly, annual, or average-annual handling path for this recall source. |
| 4. For daily recalls, require the current calendar year to be inside the source window. | Process daily salt data only when `time%yrc` falls between `recall(irec)%start_yr` and `recall(irec)%end_yr`. |
| 5. For each salt ion in a daily recall, either remove channel salt for diversions or assign source salt for additions. | Loop over all salts; if the daily recall flow is negative, treat it as a diversion, find the source channel from `ob(icmd)%obtypno_out(1)`, compute source concentration and mass loss, cap the loss to available channel salt, update `ch_water`, and record `chsalt_d%div`. If the flow is not negative, copy the daily salt value from `rec_salt(irec)%hd_salt(time%day,time%yrs)` into `obcs(icmd)%hd(1)%salt`. |
| 6. Store daily source or diversion salt balances by point-source origin. | Write the computed daily salt boundary values to `recsaltb_d` for within-watershed point sources (`pts_type = 1`) or to `recoutsaltb_d` for outside-watershed sources; if the year is outside the active range, restore `obcs(icmd)%hd(1)` from `hin_csz`. |
| 7. For monthly recalls, apply month-based salt hydrographs during the active years. | When the current year is active, copy `rec_salt(irec)%hd_salt(time%mo,time%yrs)%salt` into `obcs(icmd)%hd(1)%salt`, then mirror those monthly salt values into `recsaltb_m` or `recoutsaltb_m` through the same point-source type split. Outside the active years, reset `obcs(icmd)%hd(1)` to `hin_csz`. |
| 8. For annual recalls, apply the annual salt slot and record the matching balance output. | Use the annual salt series indexed as `hd_salt(1,time%yrs)` whenever the year is within the allowed range, then write the same values to `recsaltb_y` or `recoutsaltb_y`; otherwise restore `obcs(icmd)%hd(1)` from `hin_csz`. |
| 9. For average-annual recalls, use the fixed mean annual salt values during the active years. | When the current year is within the source window, copy `rec_salt(irec)%hd_salt(1,1)%salt` into `obcs(icmd)%hd(1)%salt` and record that same value in `recsaltb_a` or `recoutsaltb_a` depending on point-source origin. |
| 10. Return after finishing the selected recall path. | Exit the subroutine once the selected case has been processed and all relevant salt boundary and balance fields have been updated. |

## Modules Used

<!-- facts:uses -->

| Module | State touched | Key components |
| --- | --- | --- |
| [sym:basin_module] | `obcs, cs_db, rec_salt, ch_water, recsaltb_d, recoutsaltb_d, hin_csz` | `obcs(icmd)%hd(1)%salt, cs_db%num_salts, rec_salt(irec)%typ, ch_water(ichan)%salt(isalt), obcs(icmd)%hd(1)%salt(isalt), rec_salt(irec)%hd_salt, recsaltb_d(irec)%salt(isalt), recoutsaltb_d(irec)%salt(isalt), obcs(icmd)%hd(1), rec_salt(irec)%start_yr, rec_salt(irec)%end_yr, rec_salt(irec)%hd_salt(1,1)%salt(isalt)` |
| [sym:hydrograph_module] | `recall, ob, ch_stor, hd, icmd` | `recall(irec)%start_yr, recall(irec)%end_yr, ob(icmd)%obtypno_out(1), ch_stor(ichan)%flo, recall(irec)%hd` |
| [sym:time_module] | `time` | `time%yrc, time%day, time%yrs, time%mo` |
| [sym:constituent_mass_module] | `obcs, cs_db, rec_salt, ch_water, recsaltb_d, recoutsaltb_d, hin_csz` | `obcs(icmd)%hd(1)%salt, cs_db%num_salts, rec_salt(irec)%typ, ch_water(ichan)%salt(isalt), obcs(icmd)%hd(1)%salt(isalt), rec_salt(irec)%hd_salt, recsaltb_d(irec)%salt(isalt), recoutsaltb_d(irec)%salt(isalt), obcs(icmd)%hd(1), rec_salt(irec)%start_yr, rec_salt(irec)%end_yr, rec_salt(irec)%hd_salt(1,1)%salt(isalt)` |
| [sym:ch_salt_module] | `chsalt_d` | `chsalt_d(ichan)%salt(isalt)%div` |
| [sym:gwflow_module] | `div_conc_salt` | `div_conc_salt` |

## Local Variables

<!-- facts:locals -->

## State Changes

| Target | When | Meaning |
| --- | --- | --- |
| `obcs(icmd)%hd(1)%salt` | When the recall type is active and `rec_salt(irec)%pts_type == 1`, the routine sets `obcs(icmd)%hd(1)%salt` from the current recall salt hydrograph; otherwise it is left for the corresponding outside-source balance path or reset when out of range. | This boundary hydrograph holds the salt mass assigned to the current object for the active time step, so later constituent routing sees the recalled salt loading on the object boundary. |
| `div_conc_salt(isalt,irec)` | At the start of every call, for each `isalt` from 1 to `cs_db%num_salts`, the routine sets `div_conc_salt(isalt,irec) = 0.` and then replaces it only in the daily diversion branch when a channel diversion is being processed. | This array stores the diversion concentration used for salt transport accounting; resetting it avoids stale values, and filling it only for diversion cases records the source concentration applied to the withdrawn water. |
| `ch_water(ichan)%salt(isalt)` | In the daily branch, when `recall(irec)%hd(time%day,time%yrs)%flo < 0` and `ch_stor(ichan)%flo > 10.`, the routine subtracts salt mass from `ch_water(ichan)%salt(isalt)` using the capped diversion mass. | The channel water salt mass is reduced to reflect salt removed with diverted water, but only when the channel has enough stored water to support the calculation. |
| `chsalt_d(ichan)%salt(isalt)%div` | In the daily diversion branch after the concentration is computed, the routine assigns `chsalt_d(ichan)%salt(isalt)%div = div_mass`. | This records the salt mass moved by diversion for channel salt balance output, so later reporting can show how much salt left the channel via diversion. |
| `obcs(icmd)%hd(1)%salt(isalt)` | In the daily, monthly, annual, or average-annual source branches, when the current year falls inside the allowed source window, the routine writes the source salt value into `obcs(icmd)%hd(1)%salt(isalt)`. | This is the salt mass delivered to the object boundary by the recall source for the current time step. |
| `recsaltb_d(irec)%salt(isalt)` | After the daily source path finishes and `rec_salt(irec)%pts_type.eq.1`, the routine copies `obcs(icmd)%hd(1)%salt(isalt)` into `recsaltb_d(irec)%salt(isalt)`. | This stores the daily salt balance for a within-watershed point source so later salt accounting can report the source contribution. |
| `recoutsaltb_d(irec)%salt(isalt)` | After the daily source path finishes and `rec_salt(irec)%pts_type` is not 1, the routine copies `obcs(icmd)%hd(1)%salt(isalt)` into `recoutsaltb_d(irec)%salt(isalt)`. | This stores the daily salt balance for an outside-watershed point source so later salt accounting can report imported salt loading. |
| `obcs(icmd)%hd(1)` | When the current year is outside the active range for daily, monthly, or annual recall types, the routine sets `obcs(icmd)%hd(1) = hin_csz`. | This resets the whole boundary hydrograph to the zero-salt template so inactive recall sources do not contribute salt on years when they are not supposed to be active. |

## File I/O

<!-- facts:io -->


## Lineage

Source-backed lineage commits were resolved. The routine was added in df07e3f with the full recall-salt implementation. 94b6dec later added the gwflow import, initialized `div_conc_salt` to zero, and stored the computed diversion concentration. 39fabde only initialized local variables and fixed indentation, and f1e61a3 only fixed a tab alignment in the annual salt assignment. 35b029c made a whitespace-only end-of-file change.

- df07e3f introduced the recall-salt processing logic, including daily/monthly/annual/average-annual branches, diversion handling, and salt balance writes.
- 94b6dec changed behavior by adding `div_conc_salt` tracking and zeroing it before processing each recall source.
- 39fabde did not change behavior; it only initialized local variables and corrected formatting.
- f1e61a3 did not change behavior; it only fixed indentation in the annual case.
- 35b029c did not change behavior; it only removed a trailing blank line.

## Review Notes

- No direct file I/O was extracted for this procedure.
