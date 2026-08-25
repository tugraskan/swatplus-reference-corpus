---
kind: procedure
symbol: path_ls_process
title: path_ls_process
status: filled
source_hash: 45905f26915b736c
version_label: SWAT+ 62.0.0
locals:
  j: '`j` is the current HRU index used to access HRU-specific plant and soil pathogen stores.
    It is set from `ihru` at the start of the routine and then used as the indexing base for
    `cs_pl`, `cs_soil`, `pcom`, and `hpath_bal`.'
  ipath: '`ipath` is the loop counter for pathogen types. The routine iterates from 1 to `cs_db%num_paths`
    so each simulated pathogen is updated in turn.'
  ipl: '`ipl` is the loop counter for plants in the current HRU''s plant community. It lets
    the routine apply foliage wash-off and foliage die-off/growth separately for each plant
    that can carry pathogen mass.'
  ipath_db: '`ipath_db` holds the pathogen database index associated with the current soil-plant
    initialization. It is read from `sol_plt_ini(isp_ini)%path` and used to pick the pathogen
    parameters in `path_db` for wash-off, die-off, growth, temperature adjustment, and minimum
    concentration limits.'
  isp_ini: '`isp_ini` stores the soil-plant initialization database index for the current
    HRU. The routine gets it from `hru(ihru)%dbs%soil_plant_init` so it can find the correct
    pathogen initialization mapping.'
  pl_ini: '`pl_ini` saves the foliage pathogen amount before the die-off/growth calculation
    for a plant. It is later used to compute the foliage contribution to the output die-off
    balance as the change from the pre-update value to the post-update value.'
  sol_ini: '`sol_ini` saves the surface-soil pathogen amount before the soil die-off/growth
    calculation. It is later used to compute the soil contribution to the output die-off balance.'
  pl_die_gro: '`pl_die_gro` holds the net foliage rate parameter, computed as plant die-off
    minus plant growth (`do_plnt - gr_plnt`). It is passed to `Theta` so the temperature correction
    can be applied to the foliage pathogen change rate.'
  sol_die_gro: '`sol_die_gro` holds the net surface-soil rate parameter, computed as soil
    die-off minus soil growth (`do_soln - gr_soln`). It is passed to `Theta` so the temperature
    correction can be applied to the soil pathogen change rate.'
  bacdiegrosol_out: '`bacdiegrosol_out` stores the soil-layer contribution to net pathogen
    die-off for the current pathogen. It is computed as the pre-update surface-soil amount
    minus the post-update amount and then combined with the foliage contribution to form `hpath_bal(j)%path(ipath)%die_off`.'
  bacdiegroplt_out: '`bacdiegroplt_out` accumulates the foliage contribution to net pathogen
    die-off across all plants in the HRU. It is reset once per pathogen and then updated after
    each plant''s foliage concentration is recalculated.'
  theta: '`theta` is the external temperature-response function used to convert a baseline
    die-off/growth rate into a temperature-corrected rate. The routine calls it for both foliage
    and surface soil calculations so pathogen change responds to `w%tave` and the pathogen-specific
    adjustment factor `t_adj`.'
  wash_off: '`wash_off` is the computed amount of pathogen washed from foliage into the surface
    soil layer during a rainfall event. It is limited so it cannot exceed the pathogen currently
    on the plant.'
uses:
  pathogen_data_module: '`pathogen_data_module` provides the pathogen database values that
    control every per-pathogen calculation here. The routine needs `washoff` for rainfall
    transfer, `do_plnt` and `gr_plnt` for foliage change, `do_soln` and `gr_soln` for soil
    change, and `conc_min` to enforce the minimum allowable concentration.'
  constituent_mass_module: '`constituent_mass_module` holds the actual pathogen mass arrays
    that this routine updates. `cs_db%num_paths` sets the outer loop count, while `cs_pl(j)%pl_on(ipl)%path(ipath)`
    and `cs_soil(j)%ly(1)%path(ipath)` are the foliage and surface-soil stores being transferred
    and recalculated.'
  output_ls_pathogen_module: '`output_ls_pathogen_module` matters because this routine writes
    the diagnostic pathogen balance outputs. `hpath_bal(j)%path(ipath)%wash` and `hpath_bal(j)%path(ipath)%die_off`
    record the wash-off total and net die-off so later output routines can report them.'
  hru_module: '`hru_module` supplies the active HRU and its soil-plant initialization pointer.
    The routine uses `hru(ihru)%dbs%soil_plant_init` to find which pathogen database entry
    applies to the HRU and `sol_plt_ini(isp_ini)%path` to map that initialization to `path_db`.'
  soil_module: '`soil_module` is included in the routine''s dependencies because the surface-soil
    pathogen update targets the top soil layer. The extracted source does not show a direct
    symbol from this module, so its exact imported state is uncertain from the packet alone.'
  plant_module: '`plant_module` provides the plant-community size used to drive the foliage
    loop. `pcom(j)%npl` determines how many plants in the HRU can contribute to or receive
    foliage pathogen mass updates.'
  climate_module: '`climate_module` provides the daily weather driving the process. `w%precip`
    decides whether wash-off occurs, and `w%tave` is passed to `Theta` so pathogen die-off
    and growth respond to temperature.'
---

<!-- facts:header -->

Updates pathogen mass on plant foliage and in the surface soil layer for each HRU. It applies rainfall wash-off, temperature-dependent die-off/growth, and records the resulting wash and net die-off balances.

## Bottom Line

`path_ls_process` is the land-surface pathogen update routine. For the current HRU, it loops over each simulated pathogen and each plant in the plant community, moves a rainfall-driven fraction of pathogen mass from foliage to the top soil layer, and then applies temperature-adjusted die-off/growth on both foliage and the soil surface layer.

The routine also accumulates pathogen balance outputs in `hpath_bal`, especially total wash-off and net die-off. Those balances let the model report how much pathogen mass was redistributed or lost during the day.

## Arguments

<!-- facts:arguments -->

## Where It Fits

`hru_control` calls `path_ls_process` after `path_ls_swrouting` and `path_ls_runoff` when `cs_db%num_paths > 0`. By that point the HRU, pathogen database mapping, plant community, and daily weather state are already prepared, and the routine's updated pathogen masses and balances feed later transport and output reporting.

<!-- facts:calls -->

## Algorithm

| Step | What happens |
| --- | --- |
| 1. set HRU context | Copies the active HRU index from `ihru` into `j` and initializes the foliage and soil net rate accumulators to zero before any pathogen updates begin. |
| 2. loop over pathogens | Iterates over each simulated pathogen, looks up the HRU's soil-plant initialization and pathogen database index, and resets the per-pathogen wash balance and foliage die-off accumulator. |
| 3. loop over plants | Steps through each plant in the HRU plant community so pathogen wash-off and foliage die-off/growth are applied plant by plant. |
| 4. wash pathogen from foliage when rainfall is high enough | If daily precipitation is at least 2.54 mm, computes foliage wash-off as a fraction of current foliage pathogen mass, caps it at the available mass, adds it to the top soil layer, subtracts it from the plant store, and accumulates the wash balance in `hpath_bal`. |
| 5. apply foliage die-off and regrowth | Stores the pre-update foliage mass, forms a net foliage die-off/growth rate from the pathogen database, applies the temperature-corrected exponential update with `Theta`, enforces nonnegative and minimum concentration limits, and adds the foliage change to the running foliage die-off balance. |
| 6. update surface-soil pathogen mass | Stores the pre-update surface-soil mass, computes the net soil die-off/growth rate, applies the same temperature-corrected exponential update to the top soil layer, enforces nonnegative and minimum concentration limits, and computes the soil contribution to the die-off balance. |
| 7. store total die-off balance and return | Combines the foliage and soil contributions into the HRU pathogen die-off balance for the current pathogen, then exits the routine. |

## Modules Used

<!-- facts:uses -->

| Module | State touched | Key components |
| --- | --- | --- |
| [sym:pathogen_data_module] | `path_db` | `path_db(ipath_db)%washoff, path_db(ipath_db)%do_plnt, path_db(ipath_db)%gr_plnt, path_db(ipath_db)%conc_min, path_db(ipath_db)%do_soln, path_db(ipath_db)%gr_soln` |
| [sym:constituent_mass_module] | `cs_db, cs_pl, cs_soil` | `cs_db%num_paths, cs_pl(j)%pl_on(ipl)%path(ipath), cs_soil(j)%ly(1)%path(ipath)` |
| [sym:output_ls_pathogen_module] | `hpath_bal` | `hpath_bal(j)%path(ipath)%wash, hpath_bal(j)%path(ipath)%die_off` |
| [sym:hru_module] | `hru, sol_plt_ini, ihru` | `hru(ihru)%dbs%soil_plant_init, sol_plt_ini(isp_ini)%path` |
| [sym:soil_module] | `soil_module state is imported through the module use but no specific soil_module symbols are referenced in the extracted source.` |  |
| [sym:plant_module] | `pcom` | `pcom(j)%npl` |
| [sym:climate_module] | `w` | `w%precip, w%tave` |

## Local Variables

<!-- facts:locals -->

## State Changes

| Target | When | Meaning |
| --- | --- | --- |
| `hpath_bal(j)%path(ipath)%wash` | When `w%precip >= 2.54` inside the plant loop. | `hpath_bal(j)%path(ipath)%wash` accumulates the total pathogen mass washed off plant foliage for the current HRU and pathogen. It changes only when rainfall is large enough to trigger wash-off and records the amount transferred from plants to the surface soil layer. |
| `cs_soil(j)%ly(1)%path(ipath)` | After surface-soil die-off/growth is computed for the current pathogen, with the post-update value clipped to at least `path_db(ipath_db)%conc_min`. | `cs_soil(j)%ly(1)%path(ipath)` is increased by rainfall wash-off and then adjusted by temperature-dependent die-off/growth in the top soil layer. The routine keeps it nonnegative and not below the pathogen minimum concentration. |
| `cs_pl(j)%pl_on(ipl)%path(ipath)` | After each foliage wash-off event and again after the foliage die-off/growth update for each plant. | `cs_pl(j)%pl_on(ipl)%path(ipath)` loses mass to wash-off when it rains and then is further updated by temperature-adjusted die-off/growth on the plant surface. The routine enforces nonnegative values and a minimum concentration floor. |
| `hpath_bal(j)%path(ipath)%die_off` | After the foliage and surface-soil contributions have both been computed for the current pathogen. | `hpath_bal(j)%path(ipath)%die_off` stores the net daily pathogen change across foliage and top soil, combining the foliage and soil die-off/growth contributions into one balance value. |

## File I/O

<!-- facts:io -->


## Theory Equations

| Eq. | Title | Formula | Implementation |
| --- | --- | --- | --- |
| 3:4.1.1 |  | $bact_{lp,wsh}=fr_{wsh,lp}*bact_{lp,fol}$ | Verified against SWAT+ 62.0.0 (path_ls_process.f90:42). wash_off = washoff * pl_on%path` (precip >= 2.54mm gate, :41) |
| 3:4.1.2 |  | $bact_{p,wsh}=fr_{wsh,p}*bact_{p,fol}$ | Verified against SWAT+ 62.0.0 (path_ls_process.f90:42). same line, p pool (pools consolidated) |
| 3:4.2.1 | Labile-persistent bacteria on foliage (daily update) | $bact_{lpfol,i}=bact_{lpfol,i-1}*exp(-\mu _{lpfol,net})-bact_{min,lp}$ | Verified against SWAT+ 62.0.0 (path_ls_process.f90:52). pl_on%path * Exp(-Theta(pl_die_gro,t_adj,tave)) - conc_min |
| 3:4.2.10 | Net die-off rate p-solution at 20°C | $\mu_{psol,net,20}=\mu_{psol,die,20}-\mu_{psol,grw,20}$ | Verified against SWAT+ 62.0.0 (path_ls_process.f90:62). net p-solution rate |
| 3:4.2.11 | Net die-off rate lp-sorbed at 20°C | $\mu_{lpsorb,net,20}=\mu_{lpsorb,die,20}-\mu_{lpsorb,grw,20}$ | Verified against SWAT+ 62.0.0 (path_ls_process.f90:62). net lp-sorbed rate |
| 3:4.2.12 | Net die-off rate p-sorbed at 20°C | $\mu_{psorb,net,20}=\mu_{psorb,die,20}-\mu_{psorb,grw,20}$ | Verified against SWAT+ 62.0.0 (path_ls_process.f90:62). net p-sorbed rate |
| 3:4.2.13 | Temperature-adjusted lp-foliar die-off rate | $\mu_{lpfol,net}=\mu_{lpfol,net,20}*\theta_{bact}^{(\overline T_{av}-20)}$ | Verified against SWAT+ 62.0.0 (path_ls_process.f90:53). Theta(rate,t_adj,tave)` = μ_20·θ^(T−20) |
| 3:4.2.14 | Temperature-adjusted p-foliar die-off rate | $\mu_{pfol,net}=\mu_{pfol,net,20}*\theta_{bact}^{(\overline T_{av}-20)}$ | Verified against SWAT+ 62.0.0 (path_ls_process.f90:53). same Theta call |
| 3:4.2.15 | Temperature-adjusted lp-solution die-off rate | $\mu_{lpsol,net}=\mu_{lpsol,net,20}*\theta_{bact}^{(\overline T_{av}-20)}$ | Verified against SWAT+ 62.0.0 (path_ls_process.f90:53). same Theta call |
| 3:4.2.16 | Temperature-adjusted p-solution die-off rate | $\mu_{psol,net}=\mu_{psol,net,20}*\theta_{bact}^{(\overline T_{av}-20)}$ | Verified against SWAT+ 62.0.0 (path_ls_process.f90:63). Theta on the soil pool |
| 3:4.2.17 | Temperature-adjusted lp-sorbed die-off rate | $\mu_{lpsorb,net}=\mu_{lpsorb,net,20}*\theta_{bact}^{(\overline T_{av}-20)}$ | Verified against SWAT+ 62.0.0 (path_ls_process.f90:63). Theta on the soil pool |
| 3:4.2.18 |  | $\mu_{psorb,net}=\mu_{psorb,net,20}*\theta_{bact}^{(\overline T_{av}-20)}$ | Verified against SWAT+ 62.0.0 (path_ls_process.f90:63). Theta on the sorbed pool |
| 3:4.2.2 | Persistent bacteria on foliage (daily update) | $bact_{pfol,i}=bact_{pfol,i-1}*exp(-\mu _{pfol,net})-bact_{min,p}$ | Verified against SWAT+ 62.0.0 (path_ls_process.f90:52). same line, p-foliar pool |
| 3:4.2.3 | Labile-persistent bacteria in solution | $bact_{lpsol,i}=bact_{lpsol,i-1}*exp(-\mu _{lpsol,net})-bact_{min,lp}$ | Verified against SWAT+ 62.0.0 (path_ls_process.f90:51). net-rate definition, foliar |
| 3:4.2.4 | Persistent bacteria in solution | $bact_{psol,i}=bact_{psol,i-1}*exp(-\mu _{psol,net})-bact_{min,p}$ | Verified against SWAT+ 62.0.0 (path_ls_process.f90:63). surface-soil pool: `* Exp(-Theta(sol_die_gro,...)) - conc_min |
| 3:4.2.5 | Labile-persistent bacteria sorbed to soil | $bact_{lpsorb,i}=bact_{lpsord,i-1}*exp(-\mu _{lpsorb,net})-bact_{min,lp}$ | Verified against SWAT+ 62.0.0 (path_ls_process.f90:63). same line, sorbed pool |
| 3:4.2.6 | Persistent bacteria sorbed to soil | $bact_{psorb,i}=bact_{psorb,i-1}*exp(-\mu _{psorb,net})-bact_{min,p}$ | Verified against SWAT+ 62.0.0 (path_ls_process.f90:62). sol_die_gro = do_soln - gr_soln |
| 3:4.2.7 | Net die-off rate lp-foliar at 20°C | $\mu_{lpfol,net,20}=\mu_{lpfol,die,20}-\mu_{lpfol,grw,20}$ | Verified against SWAT+ 62.0.0 (path_ls_process.f90:51). pl_die_gro = do_plnt - gr_plnt` — μ_net,20 = μ_die,20 − μ_grw,20 |
| 3:4.2.8 | Net die-off rate p-foliar at 20°C | $\mu_{pfol,net,20}=\mu_{pfol,die,20}-\mu_{pfol,grw,20}$ | Verified against SWAT+ 62.0.0 (path_ls_process.f90:51). same line (p-foliar) |
| 3:4.2.9 | Net die-off rate lp-solution at 20°C | $\mu_{lpsol,net,20}=\mu_{lpsol,die,20}-\mu_{lpsol,grw,20}$ | Verified against SWAT+ 62.0.0 (path_ls_process.f90:62). net-rate definition, solution |

## Lineage

`path_ls_process` was added in commit `df07e3f` as a new subroutine that performs rainfall wash-off plus temperature-adjusted die-off/growth on foliage and surface soil, and records wash and die-off balances. Commit `16e54aa` changed the foliage balance bookkeeping so `bacdiegroplt_out` is reset for each pathogen and accumulated per plant before being combined with the soil balance. Commit `bd18ad4` only made `theta` an explicit external procedure declaration. Commit `39fabde` initialized the local counters and accumulators to zero, including `j`, `ipath`, `ipl`, `ipath_db`, `isp_ini`, `pl_ini`, `sol_ini`, `pl_die_gro`, `sol_die_gro`, `bacdiegrosol_out`, `bacdiegroplt_out`, and `wash_off`.

- df07e3f introduced the full pathogen wash-off, die-off, growth, and balance-tracking algorithm for `path_ls_process`.
- 16e54aa changed foliage balance accumulation so `bacdiegroplt_out` is tracked across plants within a pathogen loop instead of being assigned once at the end.
- bd18ad4 clarified that `theta` is an external function, affecting procedure interface declaration but not the algorithm itself.
- 39fabde initialized the routine's local working variables, reducing dependence on undefined starting values.

## Review Notes

- No direct file I/O was extracted for this procedure.
- warning: missing_doc: Procedure 'path_ls_process' has no extracted documentation comment.
- soil_module is used by the source but no direct symbol reference was resolved in the packet; its role is inferred from the surface-soil pathogen update.
- algorithm_steps revised: merged the repeated foliage-balance bookkeeping into the foliage update step and kept the full full-time-step flow within 7 steps.
