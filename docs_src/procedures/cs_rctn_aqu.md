---
kind: procedure
symbol: cs_rctn_aqu
title: cs_rctn_aqu
status: filled
source_hash: 2968815b981aab62
version_label: SWAT+ 62.0.0
locals:
  n: Loop index for combining the four Runge-Kutta slope values into the final concentration
    increment for each groundwater constituent.
  iaq: Aquifer index. It is set from the current hydrograph object number and used to select
    the matching aquifer state and reaction parameters.
  conc_old: 'Array holding the starting groundwater concentrations for the three modeled species
    before the reaction step: selenate, selenite, and nitrate.'
  conc_new: Array holding the updated concentrations after the Runge-Kutta increment is applied
    to each species.
  conc_rg: Array of trial concentrations passed to the selenium reaction routine for each
    Runge-Kutta slope evaluation.
  k_rg: Runge-Kutta slope array filled by `se_reactions_aquifer`; each row stores the computed
    concentration change for one slope evaluation.
  phi_value: Weighted Runge-Kutta increment for each species, computed from the four slope
    evaluations and added to the starting concentration.
  gw_volume: Computed groundwater volume in the aquifer, used to convert between mass and
    concentration and to handle the no-volume case safely.
  mass_seo4_before: Mass of selenate stored in the aquifer before the reaction update, used
    for the reaction mass balance.
  mass_seo3_before: Mass of selenite stored in the aquifer before the reaction update, used
    for the reaction mass balance.
  mass_seo4_after: Mass of selenate stored in the aquifer after the reaction update, used
    to compute the reaction balance term.
  mass_seo3_after: Mass of selenite stored in the aquifer after the reaction update, used
    to compute the reaction balance term.
  cs_mass_kg: Temporary nitrate mass derived from aquifer nitrate storage and object area,
    then converted to concentration for the reaction calculation.
uses:
  hydrograph_module: The aquifer ID comes from the current hydrograph object (`ob(icmd)`),
    so `hydrograph_module` provides the object connectivity that tells this routine which
    aquifer instance to update and what drainage area to use in the mass-to-concentration
    conversion.
  aquifer_module: The aquifer storage and nitrate storage fields are the physical groundwater
    state being updated here. `aquifer_module` matters because `stor` sets the groundwater
    volume and `no3_st` supplies and receives the nitrate mass state tied to the reaction
    step.
  constituent_mass_module: These are the aquifer constituent mass and concentration containers
    that this routine reads to get current selenium concentrations and writes to after the
    Runge-Kutta update. They are the primary dissolved-state fields being advanced by the
    chemistry step.
  cs_data_module: '`cs_data_module` matters because the caller checks `cs_db%num_cs` before
    invoking this routine, so the module controls whether groundwater constituent reactions
    are active at all.'
  organic_mineral_mass_module: '`organic_mineral_mass_module` is imported by the routine even
    though no specific symbol was resolved in the extracted references; it is part of the
    chemistry state set that supports groundwater constituent/mass handling in the broader
    CS workflow.'
  cs_module: '`cs_module` matters because it holds the carbon/selenium constituent configuration
    used by the groundwater chemistry system, and the caller uses that configuration to decide
    whether this reaction routine should run.'
  cs_aquifer: '`cs_aquifer` supplies the aquifer reaction-balance arrays where this routine
    stores the reaction mass change for each selenium species, so later accounting can separate
    chemical reaction effects from transport and storage changes.'
---

<!-- facts:header -->

Updates aquifer selenium species concentrations with a 4th-order Runge-Kutta reaction step. It also refreshes groundwater nitrate storage and records reaction mass-balance terms for the aquifer.

## Bottom Line

This subroutine computes one groundwater reaction update for an aquifer: it takes the current dissolved selenium and nitrate concentrations, evaluates selenium redox reaction rates through four Runge-Kutta slopes, and writes back the updated concentrations. It is the groundwater chemistry step that turns the reaction-rate model into updated aquifer state.

After the concentrations are advanced, the routine converts them back to stored mass fields and records the mass change caused by reactions in the aquifer reaction-balance object. Those reaction deltas are what later balance accounting uses to track chemical gains and losses in groundwater.

## Arguments

<!-- facts:arguments -->

## Where It Fits

This routine runs during groundwater processing inside `aqu_1d_control`, after the model has identified an aquifer object and before sorption is applied. `aqu_1d_control` prepares the current aquifer state and only calls this routine when constituent chemistry is enabled, and the resulting updated concentrations and reaction-balance terms are then used by later aquifer chemistry accounting, including sorption and mass-balance tracking.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. determine aquifer and groundwater volume | Use the current hydrograph object to pick the aquifer index, then compute groundwater volume from aquifer storage and object area. |
| 2. initialize mass trackers | Clear the before/after selenium mass trackers so the reaction mass balance can be computed from the updated state. |
| 3. load current concentrations | Read the current selenate and selenite concentrations and derive nitrate mass from aquifer nitrate storage and area. |
| 4. compute nitrate concentration | Convert nitrate mass to concentration when groundwater volume is positive; otherwise set nitrate concentration to zero to avoid division by zero. |
| 5. snapshot current selenium mass | Store the current aquifer masses for selenate and selenite so the post-reaction change can be calculated later. |
| 6. evaluate Runge-Kutta K1 | Pass the starting concentrations into the selenium reaction routine to compute the first slope increment. |
| 7. evaluate Runge-Kutta K2 | Form midpoint trial concentrations from K1 and call the selenium reaction routine for the second slope. |
| 8. evaluate Runge-Kutta K3 | Form midpoint trial concentrations from K2 and call the selenium reaction routine for the third slope. |
| 9. evaluate Runge-Kutta K4 | Form full-step trial concentrations from K3 and call the selenium reaction routine for the fourth slope. |
| 10. combine slopes into updated concentrations | Average the four slope estimates with the Runge-Kutta weights to produce the concentration increment and add it to the starting concentrations. |
| 11. write updated dissolved state | Store the new selenate and selenite concentrations and update aquifer nitrate storage from the new nitrate concentration and groundwater volume. |
| 12. convert concentrations back to mass | Convert the updated dissolved selenium concentrations back into aquifer mass values using groundwater volume. |
| 13. record reaction mass balance | Compute before/after mass differences for selenate and selenite and store them in the aquifer reaction-balance terms. |
| 14. return | Exit after the groundwater reaction update is complete. |

## Modules Used

<!-- facts:uses -->

| Module | State touched | Key components |
| --- | --- | --- |
| [sym:hydrograph_module] | `ob, icmd` | `ob(icmd)%num, ob(icmd)%area_ha` |
| [sym:aquifer_module] | `aqu_d` | `aqu_d(iaq)%stor, aqu_d(iaq)%no3_st` |
| [sym:constituent_mass_module] | `cs_aqu` | `cs_aqu(iaq)%cs(1), cs_aqu(iaq)%cs(2), cs_aqu(iaq)%csc(1), cs_aqu(iaq)%csc(2)` |
| [sym:cs_data_module] | `cs_db` | `cs_db%num_cs, cs_db%num_salts` |
| [sym:organic_mineral_mass_module] | `cs_aqu` | `cs_aqu(iaq)%csc(1), cs_aqu(iaq)%csc(2), cs_aqu(iaq)%cs(1), cs_aqu(iaq)%cs(2)` |
| [sym:cs_module] | `cs_db` | `cs_db%num_cs` |
| [sym:cs_aquifer] | `acsb_d` | `acsb_d(iaq)%cs(1)%rctn, acsb_d(iaq)%cs(2)%rctn` |

## Local Variables

<!-- facts:locals -->

## State Changes

| Target | When | Meaning |
| --- | --- | --- |
| `cs_aqu(iaq)%csc(1)` | After the Runge-Kutta update, unconditionally for the active aquifer. | `cs_aqu(iaq)%csc(1)` is overwritten with the new selenate concentration computed from the reaction slopes, so the aquifer carries the updated dissolved concentration forward to later chemistry and transport calculations. |
| `cs_aqu(iaq)%csc(2)` | After the Runge-Kutta update, unconditionally for the active aquifer. | `cs_aqu(iaq)%csc(2)` is overwritten with the new selenite concentration computed from the reaction slopes, so later groundwater accounting uses the post-reaction dissolved state. |
| `aqu_d(iaq)%no3_st` | After the new nitrate concentration is computed; only meaningful when groundwater volume is positive, otherwise the concentration is forced to zero. | `aqu_d(iaq)%no3_st` is recalculated from the updated nitrate concentration and aquifer volume so the aquifer nitrate storage remains consistent with the reaction step. |
| `cs_aqu(iaq)%cs(1)` | After the concentration update, unconditionally for the active aquifer. | `cs_aqu(iaq)%cs(1)` is recalculated from the updated selenate concentration and groundwater volume, giving the new stored selenate mass in the aquifer. |
| `cs_aqu(iaq)%cs(2)` | After the concentration update, unconditionally for the active aquifer. | `cs_aqu(iaq)%cs(2)` is recalculated from the updated selenite concentration and groundwater volume, giving the new stored selenite mass in the aquifer. |
| `acsb_d(iaq)%cs(1)%rctn` | After the updated selenate mass is computed, unconditionally for the active aquifer. | `acsb_d(iaq)%cs(1)%rctn` stores the net change in selenate mass caused by chemical reactions during this call, which is the mass-balance term used by later accounting. |
| `acsb_d(iaq)%cs(2)%rctn` | After the updated selenite mass is computed, unconditionally for the active aquifer. | `acsb_d(iaq)%cs(2)%rctn` stores the net change in selenite mass caused by chemical reactions during this call, which is the mass-balance term used by later accounting. |

## File I/O

<!-- facts:io -->


## Lineage

`cs_rctn_aqu.f90` was introduced in `df07e3f` (2024-03-05, "init all") and has been changed in 6 non-merge commit(s) since, most recently `bd18ad4` (2025-11-24, "Pr 107 (#108)"). Lineage is reconstructed from commit metadata (SHA, date, subject); per-line diffs were unavailable in this build environment, so only the commits touching `cs_rctn_aqu.f90` are listed.

- `bd18ad4` (2025-11-24) — Pr 107 (#108)
- `39fabde` (2024-08-08) — Initialized varables with python script, corrected input data where integers where floats in two input files, trapped underflow errors in th…
- `c639a8c` (2024-07-24) — Revert "Some Fixes to get pesticides running."
- `2405a68` (2024-07-16) — Fixing for Compiling
- `94b6dec` (2024-05-30) — Added latest source code from bitbucket
- `df07e3f` (2024-03-05) — init all

## Review Notes

- No direct file I/O was extracted for this procedure.
- warning: missing_doc: Procedure 'cs_rctn_aqu' has no extracted documentation comment.
- No commits were resolved for this source span in the provided Git Lineage Evidence.
- algorithm_steps revised: expanded the original step list to include the full reaction/update sequence from the source lines.
- Lineage was reconstructed from file-level commit metadata; per-line diffs were unavailable in this environment (blobless clone), so line-span filtering was not applied.
