---
kind: procedure
symbol: recall_nut
title: recall_nut
status: filled
source_hash: f526c4aa2b9a8fda
version_label: SWAT+ 62.0.0
args:
  irec: '`irec` selects which recall hydrograph record to use. The routine reads `recall(irec)%hd(time%day,time%yrs)`
    to get the diversion flow for the current day/year and uses that flow to compute nutrient
    mass removal from the source channel.'
locals:
  ichan: Index of the source channel for the recall diversion. It is taken from `ob(icmd)%obtypno_out(1)`
    and then used to read and update the channel storage state in `ch_stor(ichan)`.
  sol_conc: Temporary concentration of a constituent in the source channel water, expressed
    as g/m3. The routine recalculates it for each constituent so it can convert diverted water
    volume into removed mass.
  div_mass: Temporary diverted constituent mass, in kg, for the current nutrient or oxygen
    constituent. It is computed from `sol_conc` and the recall flow, then clipped so the routine
    never removes more mass than the channel contains.
uses:
  basin_module: '`basin_module` matters because it provides basin-wide connectivity and routing
    context that identifies which channel object is being treated as the source for this recall
    diversion, allowing the routine to act on the correct basin element rather than a local
    copy.'
  hydrograph_module: '`hydrograph_module` matters because it defines the hydrograph storage
    types and object connectivity used here: `ob(icmd)` gives the source channel number, `ch_stor`
    holds the channel nutrient masses and flow, and `recall(irec)%hd` supplies the diversion
    hydrograph that drives the mass-removal calculation.'
  time_module: '`time_module` matters because the routine selects the active recall hydrograph
    entry using the current simulation day and sequential year (`time%day` and `time%yrs`).
    Those indices determine which diversion flow is used for the mass balance on this step.'
  constituent_mass_module: '`constituent_mass_module` matters because this routine performs
    a constituent-mass accounting update for a diversion event. The module provides the broader
    mass-balance context in which the channel stores are interpreted and adjusted.'
---

<!-- facts:header -->

Removes constituent mass from a source channel when a diversion recall takes water out. It updates the channel nutrient/oxygen stores and mirrors zeroed output when the source channel is dry.

## Bottom Line

`recall_nut` handles the nutrient side of a diversion recall. When the diversion flow stored in `recall(irec)%hd(time%day,time%yrs)%flo` is negative, the routine estimates how much mass of each dissolved constituent leaves the source channel with that diverted water and subtracts that mass from channel storage.

It applies the calculation to `no3`, `solp`, `nh3`, `no2`, `dox`, and `orgn`, but only if the source channel has enough water (`ch_stor(ichan)%flo > 10.`). If the channel is too small or empty, it sets the outbound hydrograph constituent values to zero instead of removing mass from storage.

## Arguments

<!-- facts:arguments -->

## Where It Fits

This routine runs during recall/diversion handling in the command workflow after `command` has already loaded the current recall hydrograph record into `ob(icmd)%hd(1)` and detected a negative diversion flow. The results matter immediately to downstream channel routing and mass balance because the source channel storage values are reduced before later model output and transport calculations use them.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. set source channel | The routine identifies the source channel by taking `ob(icmd)%obtypno_out(1)` and storing it in `ichan`. That channel is the storage element whose constituent masses will be reduced. |
| 2. check channel has water | It resets `sol_conc` and only proceeds if the source channel contains more than 10 units of flow. This avoids applying concentration-based mass removal when the channel is effectively dry. |
| 3. remove nitrate mass | It computes nitrate concentration from channel nitrate mass and flow, converts the diverted recall flow into a nitrate mass loss, limits the loss to the available `no3`, and subtracts it from `ch_stor(ichan)%no3`. |
| 4. remove soluble phosphorus mass | It repeats the same concentration-to-mass calculation for soluble phosphorus, caps the loss at available `solp`, and updates the channel storage. |
| 5. remove ammonia mass | It computes and limits the ammonia removal using `ch_stor(ichan)%nh3`, then subtracts that mass from the source channel. |
| 6. remove nitrite mass | It applies the same mass-balance logic to nitrite, ensuring the diverted mass does not exceed `ch_stor(ichan)%no2`. |
| 7. remove dissolved oxygen mass | It calculates the dissolved oxygen mass associated with the diverted water, clips it to the available `dox`, and subtracts it from channel storage. |
| 8. remove organic nitrogen mass | It computes the organic nitrogen loss tied to the diversion flow, limits it to the available `orgn`, and updates the channel store. |
| 9. zero outbound hydrograph when dry | If the source channel flow is not greater than 10, the routine does not remove mass from storage; instead it zeros the outgoing hydrograph constituent fields so the diversion contributes no nutrient load from a dry channel. |
| 10. return to caller | The routine returns after finishing the mass adjustments or the dry-channel zeroing step, leaving the updated storage and hydrograph state for the rest of the model step. |

## Modules Used

<!-- facts:uses -->

| Module | State touched | Key components |
| --- | --- | --- |
| [sym:basin_module] | `ob, ch_stor, recall, hd, icmd` | `ob(icmd)%obtypno_out(1), ch_stor(ichan)%no3, ch_stor(ichan)%flo, recall(irec)%hd, ch_stor(ichan)%solp, ch_stor(ichan)%nh3, ch_stor(ichan)%no2, ch_stor(ichan)%dox, ch_stor(ichan)%orgn, ob(icmd)%hd(1)%no3, ob(icmd)%hd(1)%solp, ob(icmd)%hd(1)%nh3, ob(icmd)%hd(1)%no2, ob(icmd)%hd(1)%dox, ob(icmd)%hd(1)%orgn` |
| [sym:hydrograph_module] | `ob, ch_stor, recall, hd, icmd` | `ob(icmd)%obtypno_out(1), ch_stor(ichan)%no3, ch_stor(ichan)%flo, recall(irec)%hd, ch_stor(ichan)%solp, ch_stor(ichan)%nh3, ch_stor(ichan)%no2, ch_stor(ichan)%dox, ch_stor(ichan)%orgn, ob(icmd)%hd(1)%no3, ob(icmd)%hd(1)%solp, ob(icmd)%hd(1)%nh3, ob(icmd)%hd(1)%no2, ob(icmd)%hd(1)%dox, ob(icmd)%hd(1)%orgn` |
| [sym:time_module] | `time` | `time%day, time%yrs` |
| [sym:constituent_mass_module] | `time, ob, ch_stor, recall, hd` | `time%day, time%yrs` |

## Local Variables

<!-- facts:locals -->

## State Changes

| Target | When | Meaning |
| --- | --- | --- |
| `ch_stor(ichan)%no3` | When `ch_stor(ichan)%flo > 10.` and the available diverted nitrate mass would exceed the current `ch_stor(ichan)%no3`, the routine caps `div_mass` at `-ch_stor(ichan)%no3` before applying the update. | `ch_stor(ichan)%no3` is reduced by the nitrate mass associated with the diverted water, but never below zero. This preserves mass balance when the computed diversion would otherwise remove too much nitrate from the channel. |
| `ch_stor(ichan)%solp` | When `ch_stor(ichan)%flo > 10.` and the computed soluble phosphorus loss exceeds the available `ch_stor(ichan)%solp`, the routine limits the subtraction to the full remaining soluble phosphorus mass. | `ch_stor(ichan)%solp` is decreased by the phosphorus carried with the diverted water, with the subtraction clipped so the channel cannot lose more soluble P than it contains. |
| `ch_stor(ichan)%nh3` | When `ch_stor(ichan)%flo > 10.` and the calculated ammonia loss is larger than `ch_stor(ichan)%nh3`, the routine caps the loss at the available ammonia mass. | `ch_stor(ichan)%nh3` is reduced by the diverted-water ammonia load, but the routine protects the state from becoming negative by limiting the removal to what is stored. |
| `ch_stor(ichan)%no2` | When `ch_stor(ichan)%flo > 10.` and the computed nitrite loss exceeds `ch_stor(ichan)%no2`, the removal is clipped to the full nitrite store. | `ch_stor(ichan)%no2` is updated by subtracting the nitrite mass tied to the diversion, with a floor at zero to keep the mass balance physically valid. |
| `ch_stor(ichan)%dox` | When `ch_stor(ichan)%flo > 10.` and the calculated dissolved oxygen loss is greater than `ch_stor(ichan)%dox`, the routine limits the subtraction to the available dissolved oxygen mass. | `ch_stor(ichan)%dox` is reduced by the diversion-associated oxygen load, but only up to the oxygen currently stored in the channel. |
| `ch_stor(ichan)%orgn` | When `ch_stor(ichan)%flo > 10.` and the organic nitrogen loss is larger than `ch_stor(ichan)%orgn`, the routine clips the loss to the available organic nitrogen mass. | `ch_stor(ichan)%orgn` is decreased by the organic nitrogen carried with the diverted water, while preventing negative storage. |
| `ob(icmd)%hd(1)%no3` | When `ch_stor(ichan)%flo <= 10.` the routine does not compute a nitrate removal and instead sets the outbound nitrate hydrograph field to zero. | `ob(icmd)%hd(1)%no3` is zeroed for a dry or nearly dry source channel so the diversion contributes no nitrate load from absent flow. |
| `ob(icmd)%hd(1)%solp` | When `ch_stor(ichan)%flo <= 10.` the routine zeros the outbound soluble phosphorus hydrograph field rather than trying to remove mass from storage. | `ob(icmd)%hd(1)%solp` is forced to zero so a dry source channel produces no soluble phosphorus output. |
| `ob(icmd)%hd(1)%nh3` | When `ch_stor(ichan)%flo <= 10.` the routine sets the outbound ammonia hydrograph field to zero. | `ob(icmd)%hd(1)%nh3` is cleared because there is no meaningful source-channel flow to carry ammonia in the diversion. |
| `ob(icmd)%hd(1)%no2` | When `ch_stor(ichan)%flo <= 10.` the routine zeros the outbound nitrite hydrograph field. | `ob(icmd)%hd(1)%no2` is cleared so the diversion does not report nitrite from a dry source channel. |
| `ob(icmd)%hd(1)%dox` | When `ch_stor(ichan)%flo <= 10.` the routine sets the outbound dissolved oxygen hydrograph field to zero. | `ob(icmd)%hd(1)%dox` is cleared to match the dry-channel case and prevent an unreal oxygen load from being routed. |
| `ob(icmd)%hd(1)%orgn` | When `ch_stor(ichan)%flo <= 10.` the routine zeros the outbound organic nitrogen hydrograph field. | `ob(icmd)%hd(1)%orgn` is cleared so the diversion exports no organic nitrogen from a channel with insufficient water. |

## File I/O

<!-- facts:io -->


## Lineage

Four resolved commits changed `recall_nut`. `df07e3f` added the routine with the full diversion-mass removal logic. `39fabde` only initialized the local scalars `ichan`, `sol_conc`, `div_mass`, and `dum`. `2ee1889` removed the unused `dum` declaration from the local variables. `dab22e1` commented out an unused format label near the end of the file without changing the algorithm.

- df07e3f introduced the diversion nutrient-removal algorithm for channel recalls, including the per-constituent mass subtraction and dry-channel zeroing behavior.
- 39fabde changed only local-variable initialization and did not alter the computational behavior of the routine.
- 2ee1889 removed the unused `dum` local variable, trimming dead code but leaving the procedure logic unchanged.
- dab22e1 disabled an unused format label at the end of the file; the recall-mass calculations were unaffected.

## Review Notes

- No direct file I/O was extracted for this procedure.
- algorithm_steps revised: merged the original per-constituent repeated branches into one step per constituent and added the dry-channel zeroing step explicitly.
- `basin_module` and `constituent_mass_module` are imported by the source, but no directly resolved symbols from those modules were identified in the context packet; their roles are therefore described at the module level only.
