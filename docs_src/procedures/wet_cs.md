---
kind: procedure
symbol: wet_cs
title: wet_cs
status: filled
source_hash: 20591a54db864ce6
version_label: SWAT+ 62.0.0
args:
  icmd: Command index for the wetland's constituent dataset; it selects the `obcs(icmd)` surface
    inflow hydrograph and the `res_cs_data(icon)` parameter set used in the calculations.
  icon: Constituent-parameter index for this wetland; it selects the settling rates and temperature/reaction
    parameters in `res_cs_data(icon)` for the current constituent.
  ihru: HRU index for the wetland being processed; it selects the wetland water volume, seepage
    area, HRU area, weather station link, and soil store that are updated by the routine.
locals:
  theta: External function that temperature-corrects a 20°C reaction rate. `wet_cs` calls
    it to turn the constituent-specific base reaction rate and temperature factor into the
    day’s reaction constant using the current weather temperature.
  iwst: Weather-station index for the current HRU, taken from `ob(ihru)%wst`, so the routine
    can retrieve `wst(iwst)%weat%tave` for temperature-dependent reaction rates.
  ics: Loop counter over simulated constituents in `cs_db%num_cs`; each pass computes the
    wetland balance for one constituent and stores it in the matching output slot.
  k_react: Temperature-adjusted first-order reaction rate constant for the active constituent
    on the current day.
  v_settle: Constituent-specific settling velocity selected from `res_cs_data(icon)` for selenate,
    selenite, or boron, then used to estimate mass settling out of wetland water.
  cs_mass_beg: Beginning-of-day wetland constituent mass pulled from `wet_water(ihru)%cs(ics)`
    before any gains or losses are applied.
  cs_conc_beg: Beginning-of-day wetland constituent concentration computed from starting mass
    and wetland water volume.
  cs_mass_end: Ending wetland constituent mass after inflow, outflow, seepage, settling, reaction,
    and production terms are applied.
  cs_conc_end: Ending constituent concentration in wetland water, derived from `cs_mass_end`
    and the wetland water volume.
  cs_inflow: Mass of constituent entering the wetland from surface runon for the current HRU
    and constituent.
  cs_outflow: Mass of constituent exported with wetland stream outflow during the day, limited
    so it cannot exceed the mass available.
  cs_seep: Mass of constituent lost with wetland seepage, also capped by the available mass.
  cs_settle: Mass of constituent settling to the wetland bottom, computed from concentration,
    settling velocity, and wetland area, then limited by available mass.
  cs_rctn: Mass removed by first-order chemical reaction in the wetland water column, temperature
    corrected with `theta` and limited by available mass.
  cs_prod: Mass produced by reaction for selenite when selenate reduction is carried over;
    it is zero except for the ics=2 branch that receives `seo4_convert`.
  seo4_convert: Carries the selenate reaction loss from the ics=1 pass so that the same mass
    can be added as selenite production during the ics=2 pass.
  mass_avail: Running remaining constituent mass in the wetland after each loss/gain term;
    it prevents any computed removal from exceeding what is available.
  seep_mass: Seepage mass converted to an area basis for soil accounting (`kg/ha`) before
    adding it to the top soil layer and writing it to `wtspcs`.
uses:
  reservoir_data_module: The routine uses the shared constituent count from `cs_db` to size
    the wetland balance loop, so this module determines how many constituent records `wet_cs`
    must process.
  reservoir_module: This module is imported by the routine, but no specific symbols from it
    are referenced in the extracted source span; it therefore matters only as an unresolved
    dependency in the current evidence.
  water_body_module: The wetland seepage and area terms come from `wet_wat_d`; `wet_cs` uses
    seepage volume and wetland surface area to convert concentration into seepage loss and
    settling mass.
  hydrograph_module: The current wetland water volume (`wet(ihru)%flo`), inflow hydrograph
    volume (`ht2%flo`), and weather-station link (`ob(ihru)%wst`) provide the volume balance
    and temperature context needed to compute outflow and reaction losses.
  hru_module: The HRU area is needed to convert wetland constituent outflow and seepage from
    total mass to areal loading (`kg/ha`) before storing it in `wetqcs` and adding seepage
    to soil.
  constituent_mass_module: Constituent-mass data supply the wetland storage arrays, surface
    inflow hydrograph, and soil constituent pools that `wet_cs` reads and updates as it moves
    mass through the wetland system.
  res_cs_module: This module holds the wetland constituent balance outputs and the reservoir-specific
    reaction/settling parameters that drive and record the mass-balance calculations performed
    here.
  climate_module: The weather station daily mean temperature is the input to the `theta` correction,
    so this module provides the temperature that controls reaction-rate adjustment.
  cs_data_module: This module defines the constituent storage and hydrograph arrays that `wet_cs`
    reads from and writes to for wetland mass balance, surface inflow, and soil transfer.
---

<!-- facts:header -->

Computes the wetland constituent mass balance for each simulated constituent. It tracks inflow, outflow, seepage, settling, temperature-driven reaction, and resulting wetland/soil concentrations for an HRU wetland.

## Bottom Line

This subroutine updates wetland constituent mass for every simulated constituent attached to an HRU. Starting from the wetland water mass already stored in `wet_water`, it computes surface inflow, stream outflow, seepage losses, settling losses, and temperature-corrected reaction losses, then writes the end-of-day mass and concentration back to the wetland state.

It matters because later wetland and HRU routing uses these updated values: `wetcs_d` captures the balance terms for output, `wetqcs` carries wetland constituent outflow into the HRU runoff accounting, and seepage is transferred into the top soil layer through `cs_soil` and `wtspcs`.

## Arguments

<!-- facts:arguments -->

## Where It Fits

This routine runs from `wetland_control` after the wetland object has been assigned its constituent pointer (`icon = wet_dat(ires)%cs`) and after the wetland water balance has been updated. It uses the wetland volume, inflow hydrograph, weather station, and constituent parameter data prepared upstream, and its results feed downstream runoff accounting (`wetqcs`) and soil-profile loading from seepage.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. Reset wetland constituent output balances | The routine clears all stored wetland constituent balance terms for every simulated constituent by looping over `cs_db%num_cs` and zeroing inflow, outflow, seepage, settling, reaction, irrigation, mass, and concentration in `wetcs_d(ihru)%cs(ics)`. This ensures the daily output starts from a clean slate before any new calculations are made. |
| 2. Skip the balance unless the wetland contains enough water | The routine only performs the wetland constituent mass balance when `wet(ihru)%flo > 1.`. If the wetland volume is too small, the subroutine returns after leaving the zeroed output state in place. |
| 3. Initialize daily reaction carryover and loop over constituents | When the wetland has sufficient water, the routine clears `seo4_convert` and then iterates over each constituent index from 1 to `cs_db%num_cs`. Each pass computes the water-column mass balance for one constituent. |
| 4. Read starting wetland mass and concentration | For the current constituent, the routine reads the beginning-of-day mass from `wet_water(ihru)%cs(ics)` and converts it to a concentration using the wetland volume `wet(ihru)%flo`. The remaining available mass is initialized to this starting mass. |
| 5. Add surface runon mass | The mass entering from surface runon is taken from `obcs(icmd)%hin_sur(1)%cs(ics)` and added to the running available mass total. |
| 6. Compute and limit stream outflow loss | The routine estimates constituent mass exported with wetland stream outflow from the current concentration and `ht2%flo`, caps that loss so it cannot exceed what remains available, and subtracts it from the running balance. |
| 7. Compute and limit seepage loss | Seepage loss is computed from `wet_wat_d(ihru)%seep` and the starting concentration, then limited by the available mass and removed from the running balance. |
| 8. Select the settling velocity for the current constituent | The routine chooses `v_settle` from `res_cs_data(icon)` based on whether the constituent is selenate, selenite, or boron. It then computes settling loss from concentration, settling velocity, and wetland area, and limits the loss to the remaining available mass. |
| 9. Compute temperature-corrected reaction loss | The weather station linked through `ob(ihru)%wst` provides daily mean temperature for the `theta` correction. The routine selects the appropriate baseline reaction rate and temperature factor from `res_cs_data(icon)`, computes `cs_rctn`, limits it to available mass, and stores the selenate reaction loss in `seo4_convert` for later use. |
| 10. Carry selenate reduction into selenite production | For selenite (`ics == 2`), the routine sets `cs_prod` equal to the previously stored selenate reduction mass and adds that production back into the available mass. This represents conversion of selenate to selenite rather than net disappearance of mass from the wetland system. |
| 11. Update ending mass and concentration | The routine computes the end-of-day wetland mass as beginning mass plus inflow minus outflow, seepage, settling, reaction, and plus production. It then converts that mass back to a concentration using the wetland volume. |
| 12. Store wetland and soil outputs | The computed mass and concentration are written back to `wet_water(ihru)%cs(ics)` and `wet_water(ihru)%csc(ics)`. The balance terms are saved in `wetcs_d(ihru)%cs(ics)`, wetland volume is recorded in `wetcs_d(ihru)%cs(1)%volm`, outflow loading is converted to `wetqcs(ihru,ics)`, and seepage loading is added to the top soil layer in `cs_soil(ihru)%ly(1)%cs(ics)` and stored in `wtspcs(ihru,ics)`. |

## Modules Used

<!-- facts:uses -->

| Module | State touched | Key components |
| --- | --- | --- |
| [sym:reservoir_data_module] | `reservoir_data_module state` | `cs_db%num_cs` |
| [sym:reservoir_module] | `reservoir_module state` |  |
| [sym:water_body_module] | `wet_wat_d` | `wet_wat_d(ihru)%seep, wet_wat_d(ihru)%area_ha` |
| [sym:hydrograph_module] | `wet, ht2, ob` | `wet(ihru)%flo, ht2%flo, ob(ihru)%wst` |
| [sym:hru_module] | `wetqcs, hru, wtspcs` | `hru(ihru)%area_ha` |
| [sym:constituent_mass_module] | `cs_db, wet_water, obcs, cs_soil` | `cs_db%num_cs, wet_water(ihru)%cs(ics), obcs(icmd)%hin_sur(1)%cs(ics), wet_water(ihru)%csc(ics), cs_soil(ihru)%ly(1)%cs(ics)` |
| [sym:res_cs_module] | `wetcs_d, res_cs_data` | `wetcs_d(ihru)%cs(ics)%inflow, wetcs_d(ihru)%cs(ics)%outflow, wetcs_d(ihru)%cs(ics)%seep, wetcs_d(ihru)%cs(ics)%settle, wetcs_d(ihru)%cs(ics)%rctn, wetcs_d(ihru)%cs(ics)%irrig, wetcs_d(ihru)%cs(ics)%mass, wetcs_d(ihru)%cs(ics)%conc, res_cs_data(icon)%v_seo4, res_cs_data(icon)%v_seo3, res_cs_data(icon)%v_born, res_cs_data(icon)%theta_seo4, res_cs_data(icon)%theta_seo3, res_cs_data(icon)%theta_born, wetcs_d(ihru)%cs(ics)%prod, wetcs_d(ihru)%cs(1)%volm` |
| [sym:climate_module] | `wst` | `wst(iwst)%weat%tave` |
| [sym:cs_data_module] | `cs_db, wet_water, obcs, cs_soil` | `cs_db%num_cs, wet_water(ihru)%cs(ics), obcs(icmd)%hin_sur(1)%cs(ics), wet_water(ihru)%csc(ics), cs_soil(ihru)%ly(1)%cs(ics)` |

## Local Variables

<!-- facts:locals -->

## State Changes

| Target | When | Meaning |
| --- | --- | --- |
| `wetcs_d(ihru)%cs(ics)%inflow` | Each constituent pass when `wet(ihru)%flo > 1.` | `wetcs_d(ihru)%cs(ics)%inflow` is set to the day’s surface-runon constituent mass so the wetland output record preserves the inflow term used in the mass balance. |
| `wetcs_d(ihru)%cs(ics)%outflow` | Each constituent pass when `wet(ihru)%flo > 1.` | `wetcs_d(ihru)%cs(ics)%outflow` records the constituent mass exported by wetland stream outflow, capped at available mass to avoid removing more mass than exists. |
| `wetcs_d(ihru)%cs(ics)%seep` | Each constituent pass when `wet(ihru)%flo > 1.` | `wetcs_d(ihru)%cs(ics)%seep` stores the constituent mass lost to seepage from the wetland water body for later reporting and soil transfer. |
| `wetcs_d(ihru)%cs(ics)%settle` | Each constituent pass when `wet(ihru)%flo > 1.` | `wetcs_d(ihru)%cs(ics)%settle` stores the mass that settles out of the wetland water column to the bottom sediment. |
| `wetcs_d(ihru)%cs(ics)%rctn` | Each constituent pass when `wet(ihru)%flo > 1.` | `wetcs_d(ihru)%cs(ics)%rctn` stores the mass removed by temperature-adjusted first-order reaction. |
| `wetcs_d(ihru)%cs(ics)%irrig` | Each constituent pass when `wet(ihru)%flo > 1.` | `wetcs_d(ihru)%cs(ics)%irrig` is reset to zero here and remains unused in this wetland balance, because the routine does not model irrigation removal for the wetland constituent state. |
| `wetcs_d(ihru)%cs(ics)%mass` | Each constituent pass when `wet(ihru)%flo > 1.` | `wetcs_d(ihru)%cs(ics)%mass` is updated to the calculated end-of-day wetland constituent mass after all gains and losses are applied. |
| `wetcs_d(ihru)%cs(ics)%conc` | Each constituent pass when `wet(ihru)%flo > 1.` | `wetcs_d(ihru)%cs(ics)%conc` is updated to the calculated end-of-day constituent concentration in wetland water. |
| `wet_water(ihru)%cs(ics)` | Each constituent pass when `wet(ihru)%flo > 1.` | The wetland constituent mass store is overwritten with the day-end mass so the next timestep starts from the updated wetland inventory. |
| `wet_water(ihru)%csc(ics)` | Each constituent pass when `wet(ihru)%flo > 1.` | The wetland constituent concentration store is overwritten with the day-end concentration for later reporting and routing. |
| `wetcs_d(ihru)%cs(ics)%prod` | Only for `ics == 2`, after `ics == 1` has computed selenate reaction loss | `wetcs_d(ihru)%cs(ics)%prod` records the mass produced by selenate reduction and added to the selenite balance. |
| `wetcs_d(ihru)%cs(1)%volm` | Each constituent pass when `wet(ihru)%flo > 1.` | `wetcs_d(ihru)%cs(1)%volm` stores the wetland water volume used for the constituent balance output. |
| `wetqcs(ihru,ics)` | Each constituent pass when `wet(ihru)%flo > 1.` | `wetqcs(ihru,ics)` is set to the wetland constituent outflow on an area basis (`kg/ha`) so the HRU runoff accounting can include wetland-delivered constituent load. |
| `cs_soil(ihru)%ly(1)%cs(ics)` | Each constituent pass when `wet(ihru)%flo > 1.` | The top soil layer constituent store is increased by seepage loading from the wetland, representing transfer of lost wetland mass into the soil profile. |
| `wtspcs(ihru,ics)` | Each constituent pass when `wet(ihru)%flo > 1.` | `wtspcs(ihru,ics)` records the seepage mass loading added to the top soil layer for HRU-level constituent transport accounting. |

## File I/O

<!-- facts:io -->


## Lineage

The procedure was introduced in `df07e3f` as a new wetland constituent mass-balance routine. `94b6dec` kept the same logic while trimming the imported `hydrograph_module` symbols to `ob`, `ht2`, and `wet`, and `f1e61a3` only fixed indentation on the settling and reaction selection branches; `35b029c` removed a trailing blank line, and `bd18ad4` converted `theta` to an external function while removing its local declaration.

- df07e3f established the full wetland constituent balance workflow: zeroing `wetcs_d`, computing inflow/outflow/seep/settle/rctn/prod, updating `wet_water`, `wetqcs`, `cs_soil`, and `wtspcs`.
- 94b6dec narrowed the `hydrograph_module` imports without changing the mass-balance behavior, leaving the same outputs and calculations in place.
- f1e61a3 made no behavioral change; it only corrected tab spacing in the settling and reaction branch lines.
- bd18ad4 changed the interface to `theta` by declaring it external instead of a local real variable, making the temperature-correction call rely on the external function.

## Review Notes

- No direct file I/O was extracted for this procedure.
- warning: missing_doc: Procedure 'wet_cs' has no extracted documentation comment.
- reservoir_module and cs_data_module are imported but no specific resolved references from those modules were visible in the extracted source span; their rows are retained as unresolved dependencies in the draft.
- algorithm_steps revised: merged the original draft's separate iteration/branch/call/update placeholders into source-aligned steps that follow the actual loop and calculation order.
- The source uses `theta` as an external function after `bd18ad4`; the earlier history showed it was locally declared, so the current interface should be treated as authoritative.
