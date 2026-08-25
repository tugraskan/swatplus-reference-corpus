---
kind: procedure
symbol: res_salt
title: res_salt
status: filled
source_hash: 3485e4c46d9d1c0e
version_label: SWAT+ 62.0.0
args:
  jres: Selects which reservoir object to update; the routine uses `jres` to index reservoir
    storage, water-body seepage, and salt balance outputs for that specific reservoir.
locals:
  isalt: Loop counter over salt ions simulated in `cs_db%num_salts`; it drives both the reset
    pass and the daily balance pass for each reservoir salt species.
  icmd: Holds the linked reservoir object number from `res_ob(jres)%ob`, so the routine can
    read the correct constituent inflow hydrograph and write the matching outflow hydrograph
    entry.
  salt_mass_beg: Temporary start-of-day salt mass in reservoir water for the current salt
    ion, loaded from `res_water(jres)%salt(isalt)` before any daily gains or losses are applied.
  salt_conc_beg: Temporary start-of-day salt concentration for the current salt ion, loaded
    from `res_water(jres)%saltc(isalt)` and used to convert water losses to salt losses.
  salt_mass_end: Temporary end-of-day salt mass after inflow, outflow, and seepage are applied;
    this is the value written back to reservoir storage and output records.
  salt_conc_end: Temporary end-of-day salt concentration computed from `salt_mass_end` and
    reservoir volume; this is written back to reservoir state and output records.
  salt_inflow: Temporary daily salt mass entering the reservoir from the upstream object inflow
    hydrograph for the current salt ion.
  salt_outflow: Temporary daily salt mass leaving the reservoir with stream outflow; it is
    computed from outflow volume and concentration, then capped by available salt mass.
  salt_seep: Temporary daily salt mass leaving the reservoir with seepage; it is computed
    from seepage volume and concentration, then capped by available salt mass.
  mass_avail: Tracks the remaining salt mass available to leave the reservoir after inflow
    is added, so outflow and seepage cannot remove more salt than exists.
uses:
  reservoir_data_module: It provides the reservoir-object mapping used to find the corresponding
    object-control index (`icmd`) for the current reservoir, which is needed to read inflow
    hydrographs and publish outflow salt.
  reservoir_module: It supplies the reservoir object number (`res_ob(jres)%ob`) that links
    the reservoir being processed to its object-control record.
  water_body_module: It provides reservoir water-body seepage volume (`res_wat_d(jres)%seep`),
    which is needed to convert seepage water loss into salt mass loss.
  hydrograph_module: It provides the reservoir outflow volume (`res(jres)%flo`) and the temporary
    output hydrograph slot (`ht2%flo`) used to compute and reference the discharge volume
    used in the salt balance.
  constituent_mass_module: It provides the salt-constituent counts, reservoir salt storage
    arrays, and object inflow/outflow hydrographs that the routine reads and updates while
    balancing each salt ion.
  res_salt_module: It stores the per-reservoir, per-salt balance outputs that this routine
    initializes and fills for reporting and for later use by the reservoir output workflow.
---

<!-- facts:header -->

Computes the daily salt mass balance for one reservoir and stores per-salt output diagnostics. It updates reservoir salt mass and concentration after inflow, outflow, and seepage are accounted for.

## Bottom Line

`res_salt` calculates the reservoir salt balance for reservoir `jres` one salt ion at a time. For each ion, it starts from the current reservoir salt mass and concentration, adds incoming salt from the object inflow hydrograph, subtracts salt lost with reservoir discharge and seepage, and writes the updated end-of-day mass and concentration back to reservoir state and to the salt output arrays.

The routine only runs the balance when the reservoir has more than 1 m3 of water. It also limits computed outflow and seepage so they cannot exceed the salt mass still available, which keeps the daily reservoir salt accounting physically consistent and provides the salt outflow value used by downstream object connections.

## Arguments

<!-- facts:arguments -->

## Where It Fits

This routine runs during reservoir processing after the reservoir object/control links and hydrologic hydrographs have been prepared by `res_control`. `res_control` calls it when `cs_db%num_salts > 0`, and the values it writes to `obcs(icmd)%hd(1)%salt` and `ressalt_d` feed later reservoir/constituent output handling and downstream object salt routing.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. zero daily salt outputs for each ion | Initializes every salt-ion balance slot for this reservoir to zero before computing the new day’s balance, clearing prior-day inflow, outflow, seep, mass, and concentration values. |
| 2. skip tiny reservoirs | Checks that the reservoir contains more than 1 m3 of water before attempting a salt balance, so the routine avoids computing concentrations for nearly empty reservoirs. |
| 3. process each salt ion | For each simulated salt ion, loads the starting reservoir salt mass and concentration from `res_water`, and seeds the available-mass tracker with the starting mass. |
| 4. add inflow salt | Reads the salt mass entering from the linked object inflow hydrograph and adds it to the mass available for subsequent outflow and seepage losses. |
| 5. compute and limit discharge loss | Converts reservoir outflow volume and concentration into salt mass lost with stream discharge, then caps that loss at the remaining available salt mass and subtracts it from the balance. |
| 6. compute and limit seepage loss | Converts seepage water volume and concentration into salt mass lost to seepage, caps it at the remaining available salt mass, and subtracts it from the balance. |
| 7. compute end-of-day reservoir salt state | Calculates the ending salt mass and concentration from the start-of-day mass plus inflow minus discharge and seepage losses, using current reservoir volume for the concentration update. |
| 8. store reservoir salt state and diagnostics | Writes the updated mass and concentration back to `res_water`, copies all balance terms and reservoir volume into `ressalt_d` for output, and preserves the ending salt state for later use. |
| 9. publish salt outflow to linked object | Copies the computed salt outflow mass into the object hydrograph so the connected reservoir or downstream object receives the correct salt load. |
| 10. finish reservoir salt update | Ends the salt-ion loop and returns to the caller after all simulated salts for this reservoir have been processed. |

## Modules Used

<!-- facts:uses -->

| Module | State touched | Key components |
| --- | --- | --- |
| [sym:reservoir_data_module] | `reservoir_data_module state and types used by the reservoir process` | `res_ob(jres)%ob, res_ob(jres)` |
| [sym:reservoir_module] | `res_ob` | `res_ob(jres)%ob` |
| [sym:water_body_module] | `res_wat_d` | `res_wat_d(jres)%seep` |
| [sym:hydrograph_module] | `res, ht2` | `res(jres)%flo, ht2%flo` |
| [sym:constituent_mass_module] | `cs_db, res_water, obcs` | `cs_db%num_salts, res_water(jres)%salt(isalt), res_water(jres)%saltc(isalt), obcs(icmd)%hin(1)%salt(isalt), obcs(icmd)%hd(1)%salt(isalt)` |
| [sym:res_salt_module] | `ressalt_d` | `ressalt_d(jres)%salt(isalt)%inflow, ressalt_d(jres)%salt(isalt)%outflow, ressalt_d(jres)%salt(isalt)%seep, ressalt_d(jres)%salt(isalt)%mass, ressalt_d(jres)%salt(isalt)%conc, ressalt_d(jres)%salt(isalt)%volm` |

## Local Variables

<!-- facts:locals -->

## State Changes

| Target | When | Meaning |
| --- | --- | --- |
| `ressalt_d(jres)%salt(isalt)%inflow` | Each salt-ion pass before calculation begins | The routine clears `ressalt_d(jres)%salt(isalt)%inflow` to start a fresh daily record for the current reservoir and salt ion. |
| `ressalt_d(jres)%salt(isalt)%outflow` | Each salt-ion pass before calculation begins | The routine clears `ressalt_d(jres)%salt(isalt)%outflow` so the new daily discharge salt load can be recomputed from current conditions. |
| `ressalt_d(jres)%salt(isalt)%seep` | Each salt-ion pass before calculation begins | The routine clears `ressalt_d(jres)%salt(isalt)%seep` so seepage salt loss can be rebuilt from the day’s seepage volume and concentration. |
| `ressalt_d(jres)%salt(isalt)%mass` | When the reservoir has more than 1 m3 of water and the salt-ion balance is computed | The routine updates `ressalt_d(jres)%salt(isalt)%mass` to the computed end-of-day salt mass remaining in reservoir water. |
| `ressalt_d(jres)%salt(isalt)%conc` | When the reservoir has more than 1 m3 of water and the salt-ion balance is computed | The routine updates `ressalt_d(jres)%salt(isalt)%conc` to the computed end-of-day salt concentration in the reservoir water. |
| `res_water(jres)%salt(isalt)` | When the reservoir has more than 1 m3 of water and the salt-ion balance is computed | The routine replaces the stored reservoir salt mass with the computed end-of-day mass so later routines see the updated reservoir salt storage. |
| `res_water(jres)%saltc(isalt)` | When the reservoir has more than 1 m3 of water and the salt-ion balance is computed | The routine replaces the stored reservoir salt concentration with the computed end-of-day concentration for later reservoir and output calculations. |
| `ressalt_d(jres)%salt(isalt)%volm` | When the reservoir has more than 1 m3 of water and the salt-ion balance is computed | The routine records the current reservoir volume in the salt output structure so the balance output is tied to the water volume used for concentration calculations. |
| `obcs(icmd)%hd(1)%salt(isalt)` | When the reservoir has more than 1 m3 of water and the salt-ion balance is computed | The routine writes the computed salt discharge mass into the linked object hydrograph so downstream routing uses the correct salt load. |

## File I/O

<!-- facts:io -->


## Lineage

Four resolved commits changed `res_salt`. The routine was introduced in `df07e3f`, which added the full reservoir salt-balance subroutine. `35b029c` made only a formatting change by removing two blank lines near the end of the file. `94b6dec` kept the same balance logic but added an end-of-day guard by allowing the routine to run only when reservoir water volume exceeds 1 m3 and still retained the same inflow/outflow/seepage accounting. `39fabde` initialized the local loop counters and temporary salt-balance variables to zero at declaration time.

- df07e3f introduced the reservoir salt balance workflow, including per-salt inflow/outflow/seepage accounting, reservoir-state updates, and publication of salt outflow to the linked object hydrograph.
- 35b029c did not change behavior; it only removed extra blank lines before the return.
- 94b6dec preserved the salt-balance formulas but added the `res(jres)%flo > 1.` guard so the routine skips negligible-water reservoirs.
- 39fabde did not change the balance formulas; it initialized `isalt`, `icmd`, and the temporary salt variables at declaration time to avoid uninitialized values.

## Review Notes

- No direct file I/O was extracted for this procedure.
- warning: missing_doc: Procedure 'res_salt' has no extracted documentation comment.
