---
kind: procedure
symbol: res_cs
title: res_cs
status: filled
source_hash: 946cbdbfdf3eef13
version_label: SWAT+ 62.0.0
args:
  jres: Reservoir index. `jres` selects which reservoir's water volume, seepage, state arrays,
    and output records are updated.
  icon: Constituent-data index. `icon` selects the reservoir constituent parameter set that
    supplies settling velocities and reaction coefficients for the tracked species.
  iob: Object index. `iob` is used to find the connected weather station through `ob(iob)%wst`,
    which controls the temperature used for reaction-rate correction.
locals:
  theta: External temperature-adjustment function. It converts each constituent's base reaction
    rate and theta factor into a temperature-corrected first-order rate constant using the
    day's weather temperature.
  iwst: Weather-station index derived from `ob(iob)%wst`; it selects the daily air-temperature
    record used for temperature-sensitive reactions.
  ics: Loop counter over reservoir constituents. It drives the per-constituent budget calculations
    and selects SEO4, SEO3, or boron-specific parameters.
  icmd: Downstream object number for the reservoir. It is taken from `res_ob(jres)%ob` and
    is used to store constituent outflow into the connected object hydrograph.
  k_react: Temperature-corrected first-order reaction rate for the current constituent on
    the current day.
  v_settle: Constituent-specific settling velocity chosen from `res_cs_data(icon)` for SEO4,
    SEO3, or boron.
  cs_mass_beg: Constituent mass present in reservoir water at the start of the day.
  cs_conc_beg: Constituent concentration in reservoir water at the start of the day.
  cs_mass_end: Computed constituent mass remaining in reservoir water at the end of the day
    after all gains and losses.
  cs_conc_end: Computed end-of-day constituent concentration in reservoir water.
  cs_inflow: Mass entering the reservoir from the upstream constituent hydrograph during the
    current day.
  cs_outflow: Mass exported from the reservoir by stream outflow during the current day.
  cs_seep: Mass lost from reservoir water to seepage during the current day.
  cs_settle: Mass removed from the water column by settling to bottom sediments during the
    current day.
  cs_rctn: Mass removed by first-order chemical reaction during the current day.
  cs_prod: Mass produced by reaction, used only for SEO3 when SEO4 reaction mass is converted
    to SEO3.
  seo4_convert: Temporary storage of SEO4 reaction loss so the same mass can be added back
    as SEO3 production when the loop reaches constituent 2.
  mass_avail: Running amount of mass still available to allocate after inflow, outflow, seepage,
    settling, and reaction are applied; it prevents any loss term from exceeding available
    constituent mass.
uses:
  reservoir_data_module: This module provides the constituent inventory and hydrograph containers
    needed to size the constituent loop, read initial reservoir mass and concentration, take
    inflow from the upstream constituent hydrograph, and write outflow to the connected object's
    hydrograph.
  reservoir_module: The reservoir module supplies the reservoir-to-object mapping. `res_ob(jres)%ob`
    identifies which receiving object gets the reservoir's constituent outflow record.
  water_body_module: The water-body module provides reservoir surface area and seepage volume.
    Those fields are needed to turn seepage water loss into constituent mass loss and to convert
    settling velocity into a settled mass over the reservoir area.
  hydrograph_module: The hydrograph module supplies the reservoir flow volume, the connected
    object's weather-station link, and the temporary hydrograph structures that carry the
    computed constituent outflow downstream.
  constituent_mass_module: The constituent-mass module provides the reservoir constituent
    state arrays and upstream/downstream hydrograph constituent fields. `res_cs` reads starting
    mass and concentration from `res_water`, uses `obcs` for incoming and outgoing constituent
    mass, and updates the connected hydrograph entry for the next routing step.
  res_cs_module: The reservoir-constituent module holds both the output balance arrays and
    the parameter table. `res_cs` fills `rescs_d` with daily inflow, losses, ending mass,
    and concentration, and it reads `res_cs_data` for settling velocities and reaction parameters.
  climate_module: The climate module matters because reaction rates are temperature dependent.
    `res_cs` uses the linked weather station's daily average temperature to adjust each constituent's
    reaction rate before computing chemical loss.
  cs_data_module: No resolved candidate reference in the provided context is attributed to
    `cs_data_module`, so its exact imported symbols are uncertain from the packet alone; the
    module is still needed because the routine uses the constituent-database context declared
    there.
---

<!-- facts:header -->

Computes the daily reservoir mass balance for simulated constituents such as selenate, selenite, and boron.

## Bottom Line

res_cs updates the reservoir constituent budget for each simulated constituent in a reservoir. It computes beginning mass and concentration, adds inflow, subtracts stream outflow, seepage, settling, and temperature-controlled reaction loss, and for selenite adds the reduction product formed from selenate.

The routine stores those daily balance terms in `rescs_d`, updates the reservoir constituent state in `res_water`, and copies the computed outflow mass into `obcs(icmd)%hd(1)%cs(ics)` so downstream connected objects can route the exported constituent mass.

## Arguments

<!-- facts:arguments -->

## Where It Fits

This routine runs during reservoir routing after `res_control` has selected the reservoir constituent data index with `icon = res_dat(idat)%cs` and before the reservoir object's constituent hydrograph is copied onward. Its results feed downstream constituent routing through `obcs(icmd)%hd(1)%cs` and reservoir diagnostic output through `rescs_d`.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. identify downstream object | Reads the reservoir-to-object link from `res_ob(jres)%ob` so the routine can find the connected hydrograph and constituent output records for this reservoir. |
| 2. clear daily balance outputs | Initializes all reservoir constituent balance terms in `rescs_d(jres)%cs(ics)` to zero for every simulated constituent before any day-specific calculations begin. |
| 3. require enough water | Skips the constituent balance calculation unless the reservoir holds more than 1 m3 of water, avoiding division and flux calculations for an essentially dry reservoir. |
| 4. loop constituents | Processes each simulated constituent one at a time so species-specific settling and reaction parameters can be applied independently. |
| 5. load beginning state and inflow | Reads beginning-of-day constituent mass and concentration from `res_water`, then adds inflowing constituent mass from `obcs(icmd)%hin(1)%cs(ics)` into the available mass pool. |
| 6. compute stream outflow loss | Converts reservoir outflow volume and starting concentration into a constituent export mass, caps that export to the available mass, and subtracts it from the pool. |
| 7. compute seepage loss | Uses reservoir seepage volume and starting concentration to remove constituent mass lost through seepage, again limiting the loss to the remaining mass. |
| 8. select settling rate | Chooses the species-specific settling velocity for selenate, selenite, or boron, converts it to a mass loss over reservoir area, limits it to the available mass, and subtracts it. |
| 9. compute temperature reaction | Gets the connected weather-station index, evaluates the temperature-adjusted first-order reaction rate with `theta`, converts that rate to mass loss, caps it, and records selenate reaction mass for later selenite production. |
| 10. add selenite product | For selenite only, adds the mass converted from selenate back into the available pool and stores that mass as chemical production. |
| 11. update reservoir end state | Computes ending constituent mass and concentration from the day’s inflow, losses, and production, then writes the updated values back to `res_water`. |
| 12. save diagnostics and downstream export | Stores the daily balance terms, ending mass, concentration, and reservoir volume in `rescs_d`, and copies the outflow constituent mass into `obcs(icmd)%hd(1)%cs(ics)` for downstream routing. |

## Modules Used

<!-- facts:uses -->

| Module | State touched | Key components |
| --- | --- | --- |
| [sym:reservoir_data_module] | `cs_db, res_water, obcs` | `cs_db%num_cs, res_water(jres)%cs(ics), res_water(jres)%csc(ics), obcs(icmd)%hin(1)%cs(ics), obcs(icmd)%hd(1)%cs(ics)` |
| [sym:reservoir_module] | `res_ob` | `res_ob(jres)%ob` |
| [sym:water_body_module] | `res_wat_d` | `res_wat_d(jres)%seep, res_wat_d(jres)%area_ha` |
| [sym:hydrograph_module] | `res, ht2, ob` | `res(jres)%flo, ht2%flo, ob(iob)%wst` |
| [sym:constituent_mass_module] | `cs_db, res_water, obcs` | `cs_db%num_cs, res_water(jres)%cs(ics), res_water(jres)%csc(ics), obcs(icmd)%hin(1)%cs(ics), obcs(icmd)%hd(1)%cs(ics)` |
| [sym:res_cs_module] | `rescs_d, res_cs_data` | `rescs_d(jres)%cs(ics)%inflow, rescs_d(jres)%cs(ics)%outflow, rescs_d(jres)%cs(ics)%seep, rescs_d(jres)%cs(ics)%settle, rescs_d(jres)%cs(ics)%rctn, rescs_d(jres)%cs(ics)%irrig, rescs_d(jres)%cs(ics)%mass, rescs_d(jres)%cs(ics)%conc, res_cs_data(icon)%v_seo4, res_cs_data(icon)%v_seo3, res_cs_data(icon)%v_born, res_cs_data(icon)%theta_seo4, res_cs_data(icon)%theta_seo3, res_cs_data(icon)%theta_born, rescs_d(jres)%cs(ics)%prod, rescs_d(jres)%cs(ics)%volm` |
| [sym:climate_module] | `wst` | `wst(iwst)%weat%tave` |
| [sym:cs_data_module] | `res_cs_data` | `res_cs_data(icon)%v_seo4, res_cs_data(icon)%v_seo3, res_cs_data(icon)%v_born, res_cs_data(icon)%k_seo4, res_cs_data(icon)%k_seo3, res_cs_data(icon)%k_born, res_cs_data(icon)%theta_seo4, res_cs_data(icon)%theta_seo3, res_cs_data(icon)%theta_born` |

## Local Variables

<!-- facts:locals -->

## State Changes

| Target | When | Meaning |
| --- | --- | --- |
| `rescs_d(jres)%cs(ics)%inflow` | Each simulated constituent is processed after the reservoir water volume check passes; the value is reset to the upstream constituent inflow mass for that constituent. | `rescs_d(jres)%cs(ics)%inflow` records the mass entering the reservoir from the upstream hydrograph for the current day so later output can show the source contribution to the mass balance. |
| `rescs_d(jres)%cs(ics)%outflow` | For each constituent during the daily balance calculation, after stream outflow mass is computed and capped by available mass. | `rescs_d(jres)%cs(ics)%outflow` records the mass that leaves the reservoir with streamflow and is later used for output and downstream constituent routing. |
| `rescs_d(jres)%cs(ics)%seep` | For each constituent during the daily balance calculation, after seepage mass is computed and limited to what remains available. | `rescs_d(jres)%cs(ics)%seep` records mass lost from the reservoir to seepage so the daily output separates bottom-water losses from other removal terms. |
| `rescs_d(jres)%cs(ics)%settle` | For each constituent during the daily balance calculation, after settling velocity is selected and settling mass is computed and capped. | `rescs_d(jres)%cs(ics)%settle` records the mass removed from the water column by settling to reservoir sediments. |
| `rescs_d(jres)%cs(ics)%rctn` | For each constituent during the daily balance calculation, after temperature-corrected reaction rate is computed and reaction loss is capped. | `rescs_d(jres)%cs(ics)%rctn` records the amount removed by first-order chemical reaction and is also used to derive SEO4-to-SEO3 conversion. |
| `rescs_d(jres)%cs(ics)%irrig` | Only when the current constituent is SEO3 (`ics == 2`), after SEO4 reaction loss has been saved in `seo4_convert`. | `rescs_d(jres)%cs(ics)%irrig` is not modified by this routine; it remains at zero because reservoir irrigation export is not assigned here. |
| `rescs_d(jres)%cs(ics)%mass` | For each constituent after all inflow, loss, and production terms are applied to the beginning-of-day mass. | `rescs_d(jres)%cs(ics)%mass` stores the computed end-of-day constituent mass remaining in reservoir water. |
| `rescs_d(jres)%cs(ics)%conc` | For each constituent after end-of-day mass is computed and the reservoir volume is known. | `rescs_d(jres)%cs(ics)%conc` stores the corresponding end-of-day concentration in reservoir water. |
| `res_water(jres)%cs(ics)` | For each constituent after the end-of-day reservoir mass is computed. | `res_water(jres)%cs(ics)` is updated to the new reservoir constituent mass state for use by later routines and the next day. |
| `res_water(jres)%csc(ics)` | For each constituent after the end-of-day reservoir concentration is computed. | `res_water(jres)%csc(ics)` is updated to the new reservoir constituent concentration state for use by later routines and the next day. |
| `rescs_d(jres)%cs(ics)%prod` | Only when `ics == 2` and SEO4 reaction mass has been carried forward as `seo4_convert`. | `rescs_d(jres)%cs(ics)%prod` records the SEO3 mass produced by reduction of SEO4 so the output budget can show chemical creation as a positive term. |
| `rescs_d(jres)%cs(ics)%volm` | For each constituent after the daily balance has been computed. | `rescs_d(jres)%cs(ics)%volm` stores the reservoir water volume used in the calculation, allowing output reports to associate the constituent balance with the water volume on that day. |
| `obcs(icmd)%hd(1)%cs(ics)` | For each constituent after the outflow constituent mass is computed. | `obcs(icmd)%hd(1)%cs(ics)` is set to the constituent mass leaving the reservoir so the connected downstream object receives the correct constituent hydrograph entry. |

## File I/O

<!-- facts:io -->


## Lineage

The procedure was added in df07e3f with a complete reservoir-constituent mass balance implementation. Later commits adjusted variable initialization and formatting in 39fabde, changed the reaction-rate call and zero-initialized `theta` as an external in bd18ad4, and made tab/indent cleanup in f1e61a3.

- df07e3f added the full `res_cs` routine, including zeroing diagnostics, conditional execution on reservoir volume, constituent-by-constituent mass balance, and storage of outputs.
- 39fabde initialized local scalars such as `iwst`, `ics`, `cs_mass`, `cs_outflow`, `cs_prod`, and `mass_avail`, reducing uninitialized-state risk without changing the balance equations.
- bd18ad4 declared `theta` as an external function and removed unused local variables `cs_mass`, `cs_mass_out`, `cs_conc`, and the local `theta` declaration, leaving the computation unchanged.
- f1e61a3 changed only formatting/indentation in the settling-rate `elseif` block and did not alter behavior.

## Review Notes

- No direct file I/O was extracted for this procedure.
- warning: missing_doc: Procedure 'res_cs' has no extracted documentation comment.
- algorithm_steps revised: condensed the source into 12 model steps to match the actual control flow while keeping all cited line ranges real.
- `cs_data_module` is imported in the source, but the provided context packet does not resolve a module-owned symbol from that module; the explanation for that module is therefore cautious.
- The source assigns `rescs_d(jres)%cs(ics)%irrig` only during zero initialization; no later nonzero assignment appears in the extracted lines.
