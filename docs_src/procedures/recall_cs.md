---
kind: procedure
symbol: recall_cs
title: recall_cs
status: filled
source_hash: f91d30c6c0629eb4
version_label: SWAT+ 62.0.0
args:
  irec: Selects which recall point-source definition in `rec_cs` is applied. The index controls
    which hydrograph timing window, point-source type, and constituent hydrograph values are
    used for this call.
locals:
  ics: Loop counter over constituent species; used to visit each simulated constituent in
    `cs_db%num_cs` and update the matching mass slot.
  ichan: Channel index for the source channel connected to the recall object when daily recall
    type 1 removes mass by diversion.
  cs_conc: Temporary calculated constituent concentration in the source channel water, in
    g/m3, used to convert diverted water volume into constituent mass.
  div_mass: Temporary constituent mass change caused by the diversion, in kg; negative values
    remove mass from the source channel.
uses:
  basin_module: '`basin_module` provides basin-level indices such as `icmd` that identify
    the current object whose constituent hydrograph is being built. That index is the bridge
    from the current basin routing context to the recall output arrays updated here.'
  hydrograph_module: '`hydrograph_module` supplies the active object connectivity and hydrograph
    timing data that determine which source channel is tapped, which year window is active,
    and what water hydrograph value drives the daily recall logic. Without these fields the
    routine could not know when to apply the recall or where the diversion comes from.'
  time_module: '`time_module` provides the current calendar year, day, sequential year, and
    month, and those values select the correct hydrograph record for daily, monthly, annual,
    and average-annual recall types. The whole procedure is time-gated by these fields.'
  constituent_mass_module: '`constituent_mass_module` owns the constituent database, recall
    constituent inputs, channel water constituent storage, and the constituent balance arrays
    that this routine updates. Those types are necessary both to read the configured recall
    constituent hydrograph and to write the resulting mass back to the appropriate output
    balance array.'
  ch_cs_module: '`ch_cs_module` holds the channel constituent balance structure where diversion
    mass is recorded. `recall_cs` writes the diversion term so channel-constituent reporting
    can account for mass taken from the channel.'
  gwflow_module: '`gwflow_module` supplies `div_conc_cs`, which stores the concentration associated
    with a diversion for each constituent and recall index. This matters because the routine
    records the concentration used to compute diversion mass, making that value available
    to groundwater/flow coupling and later diagnostics.'
---

<!-- facts:header -->

Updates recall point-source constituent balances for the current simulation time step. It maps the configured recall hydrograph to channel water or exported constituent mass, depending on recall type and point-source direction.

## Bottom Line

`recall_cs` zeroes the per-recall constituent output state for the current step, then loops over every simulated constituent and applies the active recall schedule for the current year. For daily recall type 1 it can either remove constituent mass from the source channel during a diversion or assign source mass from the recall hydrograph; for monthly, annual, and average-annual types it copies the configured constituent hydrograph values into the outgoing object mass.

The routine matters because it produces the constituent mass that downstream channel/object bookkeeping uses for recall point sources. It also records diversion concentration and channel diversion mass balance terms so later channel-constituent reporting can reflect what was added to or removed from the channel.

## Arguments

<!-- facts:arguments -->

## Where It Fits

This routine runs when `command` is processing recall point sources and has already set up the current object state, including `ob(icmd)%hd(1)` and, when needed, the zeroed constituent hydrograph container `obcs(icmd)%hd(1)`. After `recall_cs` finishes, later channel and constituent balance output depends on the updated `obcs(icmd)%hd(1)%cs`, `reccsb_d`, `recoutcsb_d`, `ch_water`, `chcs_d`, and `div_conc_cs` values.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. Initialize the constituent output state for this recall step. | Clear `obcs(icmd)%hd(1)%cs` and reset `div_conc_cs(ics,irec)` for every simulated constituent so the call starts from a blank balance for the current object and recall index. |
| 2. Skip all work when no constituents are simulated. | Only continue if `cs_db%num_cs > 0`; otherwise the procedure returns with the zeroed object state. |
| 3. Branch on the recall point-source type. | Select the recall timing logic for daily, monthly, annual, or average-annual hydrograph handling using `rec_cs(irec)%typ`. |
| 4. For daily recall, require the active year window. | Apply daily recall only when the current calendar year lies between `recall(irec)%start_yr` and `recall(irec)%end_yr`. |
| 5. For daily recall, loop over each constituent and split diversion versus source additions. | For each constituent, negative recall flow removes mass from the connected source channel, while nonnegative recall flow copies constituent mass from the recall hydrograph into the output object. |
| 6. For daily diversions, compute channel concentration and removed mass. | Use the connected channel index from `ob(icmd)%obtypno_out(1)`, compute concentration from `ch_water` and `ch_stor`, store that concentration in `div_conc_cs`, convert diverted water to mass change, cap removal so it cannot exceed available channel constituent mass, then update `ch_water` and `chcs_d`. |
| 7. For daily sources, copy the recall hydrograph constituent mass into the output object. | Set the object constituent mass from `rec_cs(irec)%hd_cs(time%day,time%yrs)%cs(ics)` for the current day and sequential year. |
| 8. Record the daily constituent balance on the correct recall balance array. | Write the object constituent mass to `reccsb_d` when the point source is within the watershed, otherwise to `recoutcsb_d`. |
| 9. If daily recall is outside its active years, clear the output hydrograph state. | Assign `hin_csz` to `obcs(icmd)%hd(1)` when the daily recall is inactive for the current year. |
| 10. For monthly recall, use the active year window and month index. | When the current year is in range, copy each constituent from `rec_cs(irec)%hd_cs(time%mo,time%yrs)%cs(ics)` into the output object and mirror the full mass vector into `reccsb_d` or `recoutcsb_d`; otherwise reset `obcs(icmd)%hd(1)` to `hin_csz`. |
| 11. For annual recall, use the active year check and the first hydrograph month slot. | When the current year passes the annual guard, copy constituents from `rec_cs(irec)%hd_cs(1,time%yrs)%cs(ics)` into the output object and store the same full vector in the appropriate balance array; otherwise clear `obcs(icmd)%hd(1)`. |
| 12. For average-annual recall, copy the fixed representative hydrograph values. | During the active year window, assign each constituent from `rec_cs(irec)%hd_cs(1,1)%cs(ics)` to the output object and to the relevant balance array; the routine does not explicitly clear the object in the inactive case for this branch. |
| 13. Finish and return the updated state to the caller. | Exit the select case and return the updated constituent hydrograph and balance arrays to the caller without further calls. |

## Modules Used

<!-- facts:uses -->

| Module | State touched | Key components |
| --- | --- | --- |
| [sym:basin_module] | `obcs, cs_db, rec_cs, reccsb_d, recoutcsb_d, hin_csz` | `obcs(icmd)%hd(1)%cs, cs_db%num_cs, rec_cs(irec)%typ, rec_cs(irec)%hd_cs, rec_cs(irec)%start_yr, rec_cs(irec)%end_yr, rec_cs(irec)%pts_type, reccsb_d(irec)%cs, recoutcsb_d(irec)%cs, obcs(icmd)%hd(1)` |
| [sym:hydrograph_module] | `recall, ob, ch_stor, hd, icmd` | `recall(irec)%start_yr, recall(irec)%end_yr, ob(icmd)%obtypno_out(1), ch_stor(ichan)%flo, recall(irec)%hd` |
| [sym:time_module] | `time` | `time%yrc, time%day, time%yrs, time%mo` |
| [sym:constituent_mass_module] | `obcs, cs_db, rec_cs, ch_water, reccsb_d, recoutcsb_d, hin_csz` | `obcs(icmd)%hd(1)%cs, cs_db%num_cs, rec_cs(irec)%typ, ch_water(ichan)%cs(ics), obcs(icmd)%hd(1)%cs(ics), rec_cs(irec)%hd_cs, reccsb_d(irec)%cs, recoutcsb_d(irec)%cs, obcs(icmd)%hd(1), rec_cs(irec)%start_yr, rec_cs(irec)%end_yr, rec_cs(irec)%hd_cs(1,1)%cs(ics), rec_cs(irec)%hd_cs(1,1)%cs` |
| [sym:ch_cs_module] | `chcs_d` | `chcs_d(ichan)%cs(ics)%div` |
| [sym:gwflow_module] | `div_conc_cs` | `div_conc_cs` |

## Local Variables

<!-- facts:locals -->

## State Changes

| Target | When | Meaning |
| --- | --- | --- |
| `obcs(icmd)%hd(1)%cs` | When daily recall type 1 is active, the current year is inside the configured start/end window, and `recall(irec)%hd(time%day,time%yrs)%flo` is negative. | The routine treats the recall as a diversion and writes the per-constituent mass vector for the object from the daily recall hydrograph into `obcs(icmd)%hd(1)%cs`. That vector becomes the outbound constituent load for this step. |
| `div_conc_cs(ics,irec)` | For every constituent at the start of the call, before any type-specific processing. | `div_conc_cs(ics,irec)` is reset to zero so stale diversion concentrations from earlier time steps do not persist into the current recall calculation. |
| `ch_water(ichan)%cs(ics)` | When daily recall type 1 is active, the year is in range, the recall flow is negative, and the source channel has enough stored flow (`ch_stor(ichan)%flo > 10.`). | `ch_water(ichan)%cs(ics)` is reduced by the diverted constituent mass so the source channel loses the amount removed by the recall diversion. |
| `chcs_d(ichan)%cs(ics)%div` | When daily recall type 1 is active, the year is in range, the recall flow is negative, and the source channel has enough stored flow. | `chcs_d(ichan)%cs(ics)%div` records the constituent mass change associated with the diversion, giving channel balance reporting the amount removed or added by this recall event. |
| `obcs(icmd)%hd(1)%cs(ics)` | When daily recall type 1 is active, the current recall flow is nonnegative. | `obcs(icmd)%hd(1)%cs(ics)` is assigned the constituent mass from the recall hydrograph, representing a source load rather than a diversion withdrawal. |
| `reccsb_d(irec)%cs` | When the selected recall point source is within the watershed (`rec_cs(irec)%pts_type == 1`) and the active branch has produced the object constituent vector. | `reccsb_d(irec)%cs` stores the within-watershed recall constituent balance for the current step so downstream balance reporting can attribute the source correctly. |
| `recoutcsb_d(irec)%cs` | When the selected recall point source is outside the watershed (`rec_cs(irec)%pts_type /= 1`) and the active branch has produced the object constituent vector. | `recoutcsb_d(irec)%cs` stores the outside-watershed recall constituent balance for the current step so exported inflow mass is tracked separately. |
| `obcs(icmd)%hd(1)` | When the recall type is inactive for the current year in daily, monthly, or annual branches, using the branch-specific year test. | `obcs(icmd)%hd(1)` is reset to `hin_csz`, which clears the constituent hydrograph object to a zero state for the inactive period. |

## File I/O

<!-- facts:io -->


## Lineage

Four source-backed commits were resolved. The initial addition `df07e3f` created `recall_cs` with daily, monthly, annual, and average-annual recall handling. Commit `94b6dec` preserved that logic while bringing in the source as a full file addition. Commit `39fabde` changed the local variable declarations to initialize `ics`, `ichan`, `cs_conc`, and `div_mass`, and also fixed two indentation/alignment issues without changing the algorithm. Commit `92db11b` added `use gwflow_module, only : div_conc_cs`, zeroed `div_conc_cs(ics,irec)` at entry, and stored the computed daily diversion concentration in `div_conc_cs` during negative-flow daily diversion handling.

- `df07e3f` introduced the routine and its core behavior: zero the output hydrograph, branch by recall type, apply daily diversion/source logic, and write within/outside watershed constituent balances.
- `39fabde` made the local counters and temporaries explicitly initialized on declaration, reducing dependence on prior state; it did not alter the constituent-flow logic.
- `92db11b` extended the routine to populate `div_conc_cs` from the computed source-channel concentration and reset that array for each call, adding gwflow-facing concentration tracking for diversions.

## Review Notes

- No direct file I/O was extracted for this procedure.
- algorithm_steps revised: merged the original eight draft blocks into a 13-step model-oriented sequence with line-specific citations.
- Source does not show any explicit file opens, rewinds, or record positioning inside `recall_cs`.
